#!/usr/bin/env python3
"""Render BayAreaLa8s Terraform for Real Enterprises course marketing PNGs (BayServe style)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "course-terraform-for-real-enterprises-marketing.png"
OUT_SQUARE = ROOT / "docs" / "course-terraform-for-real-enterprises-marketing-square.png"

# BayAreaLa8s brand (aligned with BayServe / Data Engineering / Microservices)
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
    ("Enterprise Remote State", "S3 · DynamoDB locks · encrypted backends"),
    ("Multi-Account Design", "OU model · assume-role · state boundaries"),
    ("Reusable Modules", "VPC · compute · versioned interfaces"),
    ("CI/CD for Terraform", "GitHub Actions · OIDC · plan on PR"),
    ("Environment Promotion", "dev → test → prod with same modules"),
    ("Drift Detection", "Console change → plan → remediate"),
    ("Rollback & Recovery", "State versions · runbooks · Git revert"),
    ("Security & Compliance", "Least privilege · tags · Checkov gates"),
    ("FinOps Lab Control", "lab-pause / lab-resume · near-zero idle cost"),
    ("22 Hands-On Labs", "Live AWS stacks employers recognize"),
    ("4 Capstone Tracks", "Landing Zone · Shared Services · DR · Platform"),
    ("Not Toy Projects", "Governance · ops excellence · hire-ready demos"),
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

    # Terraform pipeline constellation (right side): plan → apply → state
    cx, cy = int(w * 0.78), int(h * 0.34)
    # Hex-inspired rings (IaC graph)
    for rr, color in ((130, TEAL), (190, (36, 120, 145)), (250, GOLD)):
        for i in range(6):
            ang = i * (math.pi * 2 / 6) - math.pi / 2
            x = int(cx + math.cos(ang) * rr)
            y = int(cy + math.sin(ang) * rr * 0.72)
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            ang2 = ((i + 1) % 6) * (math.pi * 2 / 6) - math.pi / 2
            x2 = int(cx + math.cos(ang2) * rr)
            y2 = int(cy + math.sin(ang2) * rr * 0.72)
            draw.line([(x, y), (x2, y2)], fill=color, width=1)

    # Vertical pipeline spine: code → plan → apply → state
    spine = [
        (cx - 70, cy + 40),
        (cx, cy + 10),
        (cx + 70, cy + 40),
        (cx, cy + 95),
    ]
    for i in range(len(spine) - 1):
        draw.line([spine[i], spine[i + 1]], fill=GOLD_LT, width=2)
    labels_xy = spine
    for x, y in labels_xy:
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=CARD, outline=GOLD, width=2)
    draw.ellipse((cx - 10, cy, cx + 10, cy + 20), fill=GOLD)

    return img


def render_wide() -> Image.Image:
    img = paint_backdrop(W, H)
    draw = ImageDraw.Draw(img)

    title = font(50, bold=True)
    subtitle = font(26, bold=False)
    body = font(22, bold=False)
    small = font(18, bold=False)
    card_title = font(21, bold=True)
    card_body = font(15, bold=False)
    ribbon = font(20, bold=True)
    eyebrow = font(20, bold=True)

    draw_chevron_shield(draw, 72, 58, scale=1.05)

    draw.text((168, 62), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((168, 94), "Terraform for Real Enterprises", font=title, fill=WHITE)
    draw.text((168, 154), "(Not Toy Projects)", font=title, fill=WHITE)
    draw.rectangle((168, 226, 560, 234), fill=GOLD)
    draw.text(
        (168, 254),
        "Build · Secure · Automate · Govern · Recover · Operate",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (168, 298),
        "Enterprise IaC at scale — multi-account, modules, CI/CD,\n"
        "drift, rollback, and cost control — not Hello World tutorials.",
        font=body,
        fill=MUTED,
        spacing=8,
    )

    metrics = [
        ("Duration", "8 weeks · 64–72 hours\nInstructor-led / Hybrid / Self-paced"),
        ("Audience", "DevOps · SRE · Cloud\nPlatform · Architects · Students"),
        ("Outcome", "Hire-ready enterprise IaC\n22 labs + 4 capstone tracks"),
    ]
    mx, my = 168, 390
    for i, (label, value) in enumerate(metrics):
        x0 = mx + i * 340
        rounded_rect(draw, (x0, my, x0 + 320, my + 118), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, my, x0 + 8, my + 118), fill=GOLD)
        draw.text((x0 + 22, my + 16), label, font=small, fill=GOLD_LT)
        draw.text((x0 + 22, my + 46), value, font=card_body, fill=WHITE, spacing=4)

    journey = [
        "Foundations",
        "Accounts",
        "Modules",
        "CI/CD",
        "Promotion",
        "Recovery",
        "Security",
        "Capstone",
    ]
    jy = 530
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

    draw.text((168, 620), "Why students and enterprises enroll", font=subtitle, fill=WHITE)
    cols = 3
    card_w, card_h = 540, 68
    gx, gy = 168, 668
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
        "BayAreaLa8s  ·  bayareala8s.com  ·  Terraform · AWS · GitHub Actions · OIDC · Modules · Capstone",
        font=ribbon,
        fill=WHITE,
    )
    return img


def render_square() -> Image.Image:
    """LinkedIn / social square crop of the same brand story."""
    sw, sh = 1080, 1080
    img = paint_backdrop(sw, sh)
    draw = ImageDraw.Draw(img)

    title = font(38, bold=True)
    subtitle = font(20, bold=False)
    body = font(19, bold=False)
    small = font(16, bold=False)
    card_title = font(19, bold=True)
    card_body = font(14, bold=False)
    ribbon = font(15, bold=True)
    eyebrow = font(18, bold=True)

    draw_chevron_shield(draw, 56, 44, scale=0.95)
    draw.text((148, 48), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((148, 80), "Terraform for Real", font=title, fill=WHITE)
    draw.text((148, 128), "Enterprises", font=title, fill=WHITE)
    draw.rectangle((148, 188, 460, 194), fill=GOLD)
    draw.text(
        (56, 218),
        "Build · Secure · Automate · Govern · Recover · Operate",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (56, 258),
        "Enterprise IaC for students and platform teams —\n"
        "multi-account, CI/CD, drift, and cost control.",
        font=body,
        fill=MUTED,
        spacing=6,
    )

    pills = [
        ("8 weeks", "64–72 hours"),
        ("22 labs", "AWS live stacks"),
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
