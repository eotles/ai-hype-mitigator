#!/usr/bin/env python3
"""Generate social-card.png for AI Hype Mitigator."""

from PIL import Image, ImageDraw, ImageFont
import math

WIDTH, HEIGHT = 1200, 630

FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def make_gradient(width, height):
    """Blue-to-purple left-to-right gradient background."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    # From #3b5fe2 (blue) on the left to #7c3aed (purple) on the right
    r1, g1, b1 = 0x3b, 0x5f, 0xe2
    r2, g2, b2 = 0x7c, 0x3a, 0xed
    for x in range(width):
        t = x / (width - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))
    return img


def draw_shield(draw, cx, cy, size, color=(255, 255, 255)):
    """Draw a simple shield shape centered at (cx, cy)."""
    w = size
    h = int(size * 1.2)
    x0 = cx - w // 2
    y0 = cy - h // 2

    # Shield polygon: flat top with rounded sides, pointed bottom
    pts = [
        (x0, y0),                          # top-left
        (x0 + w, y0),                       # top-right
        (x0 + w, y0 + int(h * 0.55)),       # right-mid
        (cx, y0 + h),                        # bottom point
        (x0, y0 + int(h * 0.55)),           # left-mid
    ]
    draw.polygon(pts, fill=color)


def main():
    img = make_gradient(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(img)

    WHITE = (255, 255, 255)
    WHITE_70 = (255, 255, 255, 178)
    DARK_BAND = (15, 23, 42)           # near-black bottom bar
    BADGE_BG = (255, 255, 255, 38)     # semi-transparent white

    # ── Shield icon ──────────────────────────────────────────────────────────
    shield_x, shield_y = 80, 90
    draw_shield(draw, shield_x, shield_y, 48, WHITE)

    # ── Title ─────────────────────────────────────────────────────────────────
    font_title = ImageFont.truetype(FONT_SANS_BOLD, 72)
    draw.text((120, 55), "AI Hype Mitigator", font=font_title, fill=WHITE)

    # ── Divider line ──────────────────────────────────────────────────────────
    draw.rectangle([56, 148, 900, 152], fill=WHITE)

    # ── Subtitle ──────────────────────────────────────────────────────────────
    font_sub = ImageFont.truetype(FONT_SANS, 42)
    draw.text((56, 170), "Verified AI Discourse", font=font_sub, fill=WHITE)

    # ── Body text (NO strikethrough) ──────────────────────────────────────────
    font_body = ImageFont.truetype(FONT_SANS, 34)
    WHITE_MUTED = (220, 225, 255)
    draw.text((56, 240), "Ensuring AI content creators demonstrate", font=font_body, fill=WHITE_MUTED)
    draw.text((56, 285), "real expertise before posting.", font=font_body, fill=WHITE_MUTED)

    # ── Badges ────────────────────────────────────────────────────────────────
    font_badge = ImageFont.truetype(FONT_SANS_BOLD, 26)
    badges = ["Quiz-based verification", "AI-powered analysis", "Open source"]
    badge_y = 370
    pad_x, pad_y = 20, 10
    radius = 22
    x_cursor = 56

    # Use RGBA layer for semi-transparent badges
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    for label in badges:
        bbox = font_badge.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        bw = tw + pad_x * 2
        bh = th + pad_y * 2
        # Rounded rect
        odraw.rounded_rectangle(
            [x_cursor, badge_y, x_cursor + bw, badge_y + bh],
            radius=radius,
            fill=(255, 255, 255, 50),
            outline=(255, 255, 255, 100),
            width=2,
        )
        x_cursor += bw + 20

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Re-draw badge text on top
    x_cursor = 56
    for label in badges:
        bbox = font_badge.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        bw = tw + pad_x * 2
        bh = th + pad_y * 2
        text_x = x_cursor + pad_x - bbox[0]
        text_y = badge_y + pad_y - bbox[1]
        draw.text((text_x, text_y), label, font=font_badge, fill=WHITE)
        x_cursor += bw + 20

    # ── Bottom bar with URL ───────────────────────────────────────────────────
    bar_h = 68
    draw.rectangle([0, HEIGHT - bar_h, WIDTH, HEIGHT], fill=DARK_BAND)
    font_url = ImageFont.truetype(FONT_SANS, 30)
    draw.text((56, HEIGHT - bar_h + 18), "eotles.com/ai-hype-mitigator", font=font_url, fill=(148, 163, 184))

    out_path = "docs/social-card.png"
    img.save(out_path, "PNG", optimize=True)
    print(f"Saved {out_path} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
