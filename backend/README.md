# AI Hype Mitigator — Backend (Cloudflare Worker)

The GitHub Pages demo works fully **without** this backend — it uses local keyword
detection and a built-in problem bank.

If you want **Claude-powered** content analysis and **dynamic challenge generation**
(challenges tailored to the exact AI topic of each post), deploy this Cloudflare Worker.

---

## Prerequisites

| Tool | Install |
|------|---------|
| Node.js ≥ 18 | https://nodejs.org |
| Wrangler CLI | `npm install -g wrangler` |
| Cloudflare account | https://dash.cloudflare.com/sign-up (free tier is sufficient) |
| Anthropic API key | https://console.anthropic.com |

---

## 1 — Log in to Cloudflare

```bash
wrangler login
```

---

## 2 — Create `wrangler.toml`

Create the file `backend/wrangler.toml` (it is git-ignored by default to avoid
accidentally committing your account ID):

```toml
name = "ai-hype-mitigator"
main = "worker.js"
compatibility_date = "2024-01-01"

[vars]
# Replace with your GitHub Pages URL to restrict CORS, or leave "*" for development
ALLOWED_ORIGIN = "https://<your-github-username>.github.io"
```

---

## 3 — Add your Anthropic API key as a secret

```bash
cd backend
wrangler secret put ANTHROPIC_API_KEY
# Paste your key when prompted — it is stored encrypted, never in source
```

---

## 4 — Deploy

```bash
wrangler deploy
```

Wrangler will print your Worker URL, e.g.:

```
https://ai-hype-mitigator.<your-subdomain>.workers.dev
```

---

## 5 — Connect the frontend

Open `docs/index.html` and find the `BACKEND_URL` constant near the top of the
`<script>` block (add it if using a custom build). Set it to your Worker URL:

```js
const BACKEND_URL = "https://ai-hype-mitigator.<your-subdomain>.workers.dev";
```

When `BACKEND_URL` is set, the frontend will call:

| Endpoint | Purpose |
|----------|---------|
| `POST /api/analyze` | Claude classifies whether the post is AI-related |
| `POST /api/challenge` | Claude generates a challenge tailored to the post topic |
| `POST /api/validate` | Claude evaluates free-text answers (optional mode) |

When `BACKEND_URL` is empty/unset, the frontend falls back to its built-in
keyword detection and static problem bank — no backend required.

---

## API Reference

### `POST /api/analyze`

**Request body:**
```json
{ "post": "ChatGPT is going to replace all software engineers by next year!" }
```

**Response:**
```json
{
  "isAI": true,
  "confidence": 0.97,
  "keywords": ["ChatGPT", "software engineers"],
  "reason": "Post makes a prediction about AI replacing human jobs."
}
```

---

### `POST /api/challenge`

**Request body:**
```json
{ "topic": "large language models", "difficulty": "medium" }
```

Both fields are optional. `difficulty` accepts `"easy"`, `"medium"`, or `"hard"`.

**Response:**
```json
{
  "category": "Machine Learning",
  "question": "In the transformer attention formula softmax(QKᵀ/√dₖ)V, what is the purpose of dividing by √dₖ?",
  "supplementary": "",
  "supplementaryType": "",
  "options": [
    "Prevent dot products from growing too large, causing vanishing softmax gradients",
    "Speed up matrix multiplication",
    "Normalise the value vectors",
    "Ensure the output sums to 1"
  ],
  "correct": "Prevent dot products from growing too large, causing vanishing softmax gradients",
  "explanation": "Without scaling, large dₖ causes dot products to have large magnitudes, pushing softmax into near-zero-gradient regions."
}
```

---

### `POST /api/validate`

**Request body:**
```json
{
  "question": "What does ReLU return for x = -3?",
  "correct": "0",
  "userAnswer": "Zero, because ReLU clips negatives to zero"
}
```

**Response:**
```json
{
  "isCorrect": true,
  "feedback": "Correct! ReLU(x) = max(0, x), so any negative input maps to 0."
}
```

---

## Cost Estimate

The Worker uses `claude-haiku-4-5-20251001`, the fastest and most affordable
Claude model. A typical session (1 analyze + 1 challenge call) uses roughly
300–600 input tokens and 200–400 output tokens — well under $0.001 per user
interaction at current Anthropic pricing.

Cloudflare Workers free tier allows 100,000 requests/day.
