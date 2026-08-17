#!/usr/bin/env python3
"""Render BayAreaLa8s AI Automation & Agents with AWS Bedrock marketing PNGs (BayServe style)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "course-ai-automation-agents-bedrock-marketing.png"
OUT_SQUARE = ROOT / "docs" / "course-ai-automation-agents-bedrock-marketing-square.png"

# BayAreaLa8s brand (aligned with BayServe / Terraform / Data Engineering)
NAVY = (10, 31, 51)
NAVY_2 = (14, 48, 74)
TEAL = (13, 143, 173)
TEAL_DK = (8, 110, 135)
GOLD = (201, 162, 39)
GOLD_LT = (232, 201, 98)
WHITE = (248, 251, 253)
MUTED = (186, 204, 214)
CARD = (18, 52, 78)
CARD_EDGE = (36, 92, 118)

W, H = 1920, 1080

CAPABILITIES = [
    ("AWS Bedrock Integration", "Nova Lite · Converse API · least-privilege IAM"),
    ("Structured AI Outputs", "JSON contracts · schema validation · fallbacks"),
    ("Step Functions Orchestration", "Retries · Catch · idempotent workflows"),
    ("AI-Powered APIs", "API Gateway · /classify · /summarize · /route"),
    ("Enterprise Agents", "Tool allow-lists · memory · policy gates"),
    ("Human-in-the-Loop", "Approval workflows · risk evaluation"),
    ("Observability & Audit", "Correlation IDs · DynamoDB trail · dashboards"),
    ("Governance & Safety", "Redaction · never-log rules · cost limits"),
    ("SAM Lab Stack", "Lambda · API · SFN · DynamoDB · CloudWatch"),
    ("Start / Stop Cost Control", "Deploy · verify · teardown · near-zero idle"),
    ("8 Weeks Hands-On", "Live AWS labs employers recognize"),
    ("4 Capstone Projects", "Incident · Docs · Approvals · Agents"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Neue.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_chevron_shield(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    s = scale
    draw.polygon(
        [
            (x + 8 * s, y + 2 * s),
            (x + 56 * s, y + 2 * s),
            (x + 64 * s, y + 28 * s),
            (x + 0 * s, y + 28 * s),
        ],
        fill=GOLD,
    )
    draw.polygon(
        [
            (x + 4 * s, y + 30 * s),
            (x + 60 * s, y + 30 * s),
            (x + 68 * s, y + 56 * s),
            (x - 4 * s, y + 56 * s),
        ],
        fill=TEAL,
    )
    draw.polygon(
        [
            (x + 0 * s, y + 58 * s),
            (x + 64 * s, y + 58 * s),
            (x + 70 * s, y + 80 * s),
            (x + 32 * s, y + 88 * s),
            (x - 6 * s, y + 80 * s),
        ],
        fill=(6, 28, 46),
    )


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill,
    outline=None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def paint_backdrop(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)

    for y in range(h):
        t = y / h
        r = int(NAVY[0] * (1 - t) + NAVY_2[0] * t)
        g = int(NAVY[1] * (1 - t) + (NAVY_2[1] + 20) * t)
        b = int(NAVY[2] * (1 - t) + TEAL_DK[2] * t * 0.55)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((w * 0.55, -120, w * 1.15, h * 0.72), fill=(13, 143, 173, 55))
    gdraw.ellipse((-200, h * 0.55, w * 0.4, h * 1.2), fill=(201, 162, 39, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Agent / workflow constellation (right side): API → Bedrock → SFN → Action
    cx, cy = int(w * 0.78), int(h * 0.32)
    for rr, color in ((120, TEAL), (180, (36, 120, 145)), (240, GOLD)):
        for i in range(8):
            ang = i * (math.pi * 2 / 8) - math.pi / 2
            x = int(cx + math.cos(ang) * rr)
            y = int(cy + math.sin(ang) * rr * 0.68)
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)
            ang2 = ((i + 1) % 8) * (math.pi * 2 / 8) - math.pi / 2
            x2 = int(cx + math.cos(ang2) * rr)
            y2 = int(cy + math.sin(ang2) * rr * 0.68)
            draw.line([(x, y), (x2, y2)], fill=color, width=1)

    # Vertical agent spine: request → model → validate → act
    spine = [
        (cx - 80, cy + 30),
        (cx, cy - 5),
        (cx + 80, cy + 30),
        (cx, cy + 90),
    ]
    for i in range(len(spine) - 1):
        draw.line([spine[i], spine[i + 1]], fill=GOLD_LT, width=2)
    for x, y in spine:
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=CARD, outline=GOLD, width=2)
    # center “brain” node
    draw.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=GOLD)
    draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=NAVY)

    return img


def render_wide() -> Image.Image:
    img = paint_backdrop(W, H)
    draw = ImageDraw.Draw(img)

    title = font(44, bold=True)
    subtitle = font(26, bold=False)
    body = font(22, bold=False)
    small = font(18, bold=False)
    card_title = font(21, bold=True)
    card_body = font(15, bold=False)
    ribbon = font(20, bold=True)
    eyebrow = font(20, bold=True)

    draw_chevron_shield(draw, 72, 58, scale=1.05)

    draw.text((168, 62), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((168, 94), "AI Automation & Agents", font=title, fill=WHITE)
    draw.text((168, 148), "with AWS Bedrock", font=title, fill=WHITE)
    draw.rectangle((168, 214, 560, 222), fill=GOLD)
    draw.text(
        (168, 242),
        "Orchestrate · Validate · Govern · Observe · Control Cost",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (168, 286),
        "Production-grade AI systems — not chatbots. Workflows, guardrails,\n"
        "agents, and ops excellence on live AWS.",
        font=body,
        fill=MUTED,
        spacing=8,
    )

    metrics = [
        ("Duration", "8 weeks · 64–72 hours\nInstructor-led / Hybrid / Self-paced"),
        ("Audience", "Cloud · DevOps · Platform\nAI/ML · Architects · Engineers"),
        ("Outcome", "Hire-ready AI automation\n4 capstone tracks on AWS"),
    ]
    mx, my = 168, 380
    for i, (label, value) in enumerate(metrics):
        x0 = mx + i * 340
        rounded_rect(draw, (x0, my, x0 + 320, my + 118), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, my, x0 + 8, my + 118), fill=GOLD)
        draw.text((x0 + 22, my + 16), label, font=small, fill=GOLD_LT)
        draw.text((x0 + 22, my + 46), value, font=card_body, fill=WHITE, spacing=4)

    journey = [
        "Foundations",
        "Bedrock",
        "Validate",
        "Orchestrate",
        "APIs",
        "Ops",
        "Agents",
        "Capstone",
    ]
    jy = 520
    draw.text((168, jy), "Learning journey (lab-first)", font=small, fill=MUTED)
    jx = 168
    step_w = 168
    for i, step in enumerate(journey):
        box = (jx, jy + 28, jx + step_w, jy + 66)
        rounded_rect(draw, box, 10, (12, 60, 82), TEAL, 1)
        tw = draw.textlength(step, font=small)
        draw.text((jx + max(8, (step_w - tw) / 2), jy + 40), step, font=small, fill=WHITE)
        if i < len(journey) - 1:
            draw.text((jx + step_w + 4, jy + 38), "→", font=small, fill=GOLD)
        jx += step_w + 20

    draw.text((168, 610), "Why students and enterprises enroll", font=subtitle, fill=WHITE)
    cols = 3
    card_w, card_h = 540, 68
    gx, gy = 168, 658
    gap_x, gap_y = 20, 10
    for i, (name, desc) in enumerate(CAPABILITIES):
        col = i % cols
        row = i // cols
        x0 = gx + col * (card_w + gap_x)
        y0 = gy + row * (card_h + gap_y)
        rounded_rect(draw, (x0, y0, x0 + card_w, y0 + card_h), 12, CARD, CARD_EDGE, 1)
        draw.ellipse((x0 + 16, y0 + 26, x0 + 28, y0 + 38), fill=GOLD)
        draw.text((x0 + 44, y0 + 10), name, font=card_title, fill=WHITE)
        draw.text((x0 + 44, y0 + 38), desc, font=card_body, fill=MUTED)

    draw.rectangle((0, H - 64, W, H), fill=(6, 22, 36))
    draw.rectangle((0, H - 68, W, H - 64), fill=GOLD)
    draw.text(
        (72, H - 44),
        "BayAreaLa8s  ·  bayareala8s.com  ·  Bedrock · Lambda · Step Functions · Agents · Capstone",
        font=ribbon,
        fill=WHITE,
    )
    return img


def render_square() -> Image.Image:
    """LinkedIn / social square crop of the same brand story."""
    sw, sh = 1080, 1080
    img = paint_backdrop(sw, sh)
    draw = ImageDraw.Draw(img)

    title = font(36, bold=True)
    subtitle = font(20, bold=False)
    body = font(19, bold=False)
    small = font(16, bold=False)
    card_title = font(19, bold=True)
    card_body = font(14, bold=False)
    ribbon = font(15, bold=True)
    eyebrow = font(18, bold=True)

    draw_chevron_shield(draw, 56, 44, scale=0.95)
    draw.text((148, 48), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((148, 80), "AI Automation & Agents", font=title, fill=WHITE)
    draw.text((148, 124), "with AWS Bedrock", font=title, fill=WHITE)
    draw.rectangle((148, 180, 460, 186), fill=GOLD)
    draw.text(
        (56, 210),
        "Orchestrate · Validate · Govern · Observe · Control Cost",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (56, 250),
        "Production AI systems for students and platform teams —\n"
        "workflows, agents, guardrails on live AWS.",
        font=body,
        fill=MUTED,
        spacing=6,
    )

    pills = [
        ("8 weeks", "64–72 hours"),
        ("Live AWS labs", "SAM · Bedrock · SFN"),
        ("4 Capstones", "Hire-ready projects"),
    ]
    for i, (a, b) in enumerate(pills):
        x0 = 56 + i * 330
        rounded_rect(draw, (x0, 340, x0 + 310, 340 + 92), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, 340, x0 + 8, 432), fill=GOLD)
        draw.text((x0 + 22, 356), a, font=card_title, fill=WHITE)
        draw.text((x0 + 22, 390), b, font=small, fill=MUTED)

    highlights = CAPABILITIES[:6]
    for i, (name, desc) in enumerate(highlights):
        row = i // 2
        col = i % 2
        x0 = 56 + col * 500
        y0 = 460 + row * 110
        rounded_rect(draw, (x0, y0, x0 + 480, y0 + 96), 12, CARD, CARD_EDGE, 1)
        draw.ellipse((x0 + 18, y0 + 40, x0 + 32, y0 + 54), fill=GOLD)
        draw.text((x0 + 48, y0 + 22), name, font=card_title, fill=WHITE)
        draw.text((x0 + 48, y0 + 54), desc, font=card_body, fill=MUTED)

    draw.rectangle((0, sh - 56, sw, sh), fill=(6, 22, 36))
    draw.rectangle((0, sh - 60, sw, sh - 56), fill=GOLD)
    draw.text(
        (40, sh - 38),
        "BayAreaLa8s  ·  Students & Enterprise  ·  bayareala8s.com",
        font=ribbon,
        fill=WHITE,
    )
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wide = render_wide()
    wide.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")

    square = render_square()
    square.save(OUT_SQUARE, "PNG", optimize=True)
    print(f"Wrote {OUT_SQUARE}")


if __name__ == "__main__":
    main()
