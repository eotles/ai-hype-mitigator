/**
 * AI Hype Mitigator — Cloudflare Worker Backend
 *
 * Exposes three endpoints that enhance the GitHub Pages demo with
 * Claude-powered content analysis and dynamic challenge generation:
 *
 *   POST /api/analyze   — Detect AI content in a social media post
 *   POST /api/challenge — Generate a tailored expertise challenge
 *   POST /api/validate  — Evaluate a free-text answer
 *
 * Required secret (set via `wrangler secret put ANTHROPIC_API_KEY`):
 *   ANTHROPIC_API_KEY
 *
 * Optional environment variable (wrangler.toml [vars]):
 *   ALLOWED_ORIGIN  — e.g. "https://<your-username>.github.io"
 *                     Defaults to "*" (any origin) for development.
 */

const ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages";
const MODEL = "claude-haiku-4-5-20251001"; // fast + affordable for interactive use

// ─── CORS ────────────────────────────────────────────────────────────────────

function corsHeaders(origin, env) {
  const allowed = env.ALLOWED_ORIGIN || "*";
  return {
    "Access-Control-Allow-Origin": allowed === "*" ? "*" : origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function optionsResponse(origin, env) {
  return new Response(null, { status: 204, headers: corsHeaders(origin, env) });
}

function jsonResponse(data, status = 200, origin, env) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin, env),
    },
  });
}

// ─── ANTHROPIC HELPER ────────────────────────────────────────────────────────

async function callClaude(apiKey, systemPrompt, userMessage) {
  const res = await fetch(ANTHROPIC_API_URL, {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }],
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Anthropic API error ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.content[0].text;
}

// ─── ENDPOINT: /api/analyze ──────────────────────────────────────────────────

async function handleAnalyze(request, env, origin) {
  const { post } = await request.json();
  if (!post || typeof post !== "string") {
    return jsonResponse({ error: "Missing or invalid 'post' field." }, 400, origin, env);
  }

  const system = `You are an AI content classifier embedded in a social media platform.
Your job is to decide whether a social media post makes claims about artificial intelligence,
machine learning, or closely related topics (e.g. LLMs, neural networks, AGI, generative AI).

Respond with ONLY a valid JSON object — no prose, no markdown fences — in exactly this shape:
{
  "isAI": true | false,
  "confidence": <number 0.0–1.0>,
  "keywords": ["<term1>", "<term2>", ...],
  "reason": "<one-sentence explanation>"
}`;

  const raw = await callClaude(env.ANTHROPIC_API_KEY, system,
    `Classify this social media post:\n\n"${post}"`);

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return jsonResponse({ error: "Failed to parse model response.", raw }, 500, origin, env);
  }

  return jsonResponse(parsed, 200, origin, env);
}

// ─── ENDPOINT: /api/challenge ─────────────────────────────────────────────────

async function handleChallenge(request, env, origin) {
  const { topic, difficulty = "medium" } = await request.json();

  const system = `You are a technical quiz generator for an AI expertise verification system.
Generate a single multiple-choice question to test whether a social media user genuinely
understands AI/ML at a technical level.

The question must:
- Be directly answerable by someone with real AI/ML knowledge
- Have exactly 4 answer options (A, B, C, D style content — no letter prefixes needed)
- Have one unambiguously correct answer
- Include a clear, educational explanation

Respond with ONLY a valid JSON object — no markdown fences — in exactly this shape:
{
  "category": "<e.g. Linear Algebra | Machine Learning | Python/NumPy>",
  "question": "<question text>",
  "supplementary": "<optional matrix, code snippet, or formula — empty string if none>",
  "supplementaryType": "<'math' | 'code' | ''>",
  "options": ["<opt1>", "<opt2>", "<opt3>", "<opt4>"],
  "correct": "<exact text of the correct option>",
  "explanation": "<explanation of the correct answer>"
}`;

  const userMsg = topic
    ? `Generate a ${difficulty}-difficulty question relevant to this AI topic: "${topic}"`
    : `Generate a ${difficulty}-difficulty AI/ML technical question on any topic.`;

  const raw = await callClaude(env.ANTHROPIC_API_KEY, system, userMsg);

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return jsonResponse({ error: "Failed to parse model response.", raw }, 500, origin, env);
  }

  return jsonResponse(parsed, 200, origin, env);
}

// ─── ENDPOINT: /api/validate ──────────────────────────────────────────────────

async function handleValidate(request, env, origin) {
  const { question, correct, userAnswer } = await request.json();

  if (!question || !correct || !userAnswer) {
    return jsonResponse({ error: "Missing required fields: question, correct, userAnswer." }, 400, origin, env);
  }

  const system = `You are an AI/ML answer evaluator. Given a technical question, the official
correct answer, and a user's free-text answer, determine whether the user's answer is
substantively correct (allowing for paraphrasing and minor wording differences).

Respond with ONLY a valid JSON object — no markdown fences — in exactly this shape:
{
  "isCorrect": true | false,
  "feedback": "<one or two sentences of constructive feedback>"
}`;

  const userMsg = `Question: ${question}\nCorrect answer: ${correct}\nUser's answer: ${userAnswer}`;
  const raw = await callClaude(env.ANTHROPIC_API_KEY, system, userMsg);

  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return jsonResponse({ error: "Failed to parse model response.", raw }, 500, origin, env);
  }

  return jsonResponse(parsed, 200, origin, env);
}

// ─── MAIN HANDLER ─────────────────────────────────────────────────────────────

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "*";

    if (request.method === "OPTIONS") {
      return optionsResponse(origin, env);
    }

    if (request.method !== "POST") {
      return jsonResponse({ error: "Method not allowed." }, 405, origin, env);
    }

    const url = new URL(request.url);

    try {
      switch (url.pathname) {
        case "/api/analyze":
          return await handleAnalyze(request, env, origin);
        case "/api/challenge":
          return await handleChallenge(request, env, origin);
        case "/api/validate":
          return await handleValidate(request, env, origin);
        default:
          return jsonResponse({ error: "Not found." }, 404, origin, env);
      }
    } catch (err) {
      console.error(err);
      return jsonResponse({ error: err.message }, 500, origin, env);
    }
  },
};
