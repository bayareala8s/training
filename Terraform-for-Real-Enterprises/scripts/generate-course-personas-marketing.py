#!/usr/bin/env python3
"""Render BayAreaLa8s Terraform for Real Enterprises — personas / career-outcomes marketing PNGs."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "course-terraform-for-real-enterprises-personas.png"
OUT_SQUARE = ROOT / "docs" / "course-terraform-for-real-enterprises-personas-square.png"

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

# persona, real-world benefit, career outcome (no salary/job guarantees)
PERSONAS = [
    (
        "DevOps / Cloud Engineer",
        "Ship remote state, modules, and GitHub Actions OIDC with lab-pause cost control.",
        "Upskill for production IaC delivery — stronger interview demos.",
    ),
    (
        "Platform / SRE",
        "Drift detection, rollback runbooks, tags, and promotion across environments.",
        "Ready for promotion talks on reliability, governance & ops excellence.",
    ),
    (
        "Solutions Architect",
        "Multi-account design plus 4 capstones (Landing Zone · Shared Services · DR · Platform).",
        "Win trust in client conversations with live AWS Terraform proof.",
    ),
    (
        "Infrastructure Automation Engineer",
        "Versioned modules, CI plan/apply gates, and Checkov compliance in the pipeline.",
        "Stand out for roles that demand enterprise-grade automation — not tutorials.",
    ),
    (
        "Career Switcher / Student",
        "Portfolio: remote state, promotion, drift labs, and a graded Week 8 capstone.",
        "Build hire-ready evidence employers recognize.",
    ),
    (
        "Engineering Manager",
        "Team patterns for approvals, least privilege, FinOps pause/resume, and change control.",
        "Lead IaC initiatives with standards your org can adopt.",
    ),
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


def rounded_rect(draw, box, radius, fill, outline=None, width: int = 1) -> None:
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
    gdraw.ellipse((w * 0.5, -100, w * 1.1, h * 0.55), fill=(13, 143, 173, 50))
    gdraw.ellipse((-180, h * 0.6, w * 0.35, h * 1.15), fill=(201, 162, 39, 24))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Soft network (career graph) top-right
    cx, cy = int(w * 0.88), int(h * 0.18)
    for rr, color in ((70, TEAL), (110, GOLD)):
        for i in range(6):
            ang = i * (math.pi * 2 / 6) - math.pi / 2
            x = int(cx + math.cos(ang) * rr)
            y = int(cy + math.sin(ang) * rr * 0.65)
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color)
    return img


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font_obj) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_wide() -> Image.Image:
    img = paint_backdrop(W, H)
    draw = ImageDraw.Draw(img)

    title = font(42, bold=True)
    subtitle = font(24, bold=False)
    body = font(20, bold=False)
    small = font(17, bold=False)
    card_title = font(22, bold=True)
    card_body = font(16, bold=False)
    card_career = font(15, bold=True)
    ribbon = font(19, bold=True)
    eyebrow = font(20, bold=True)

    draw_chevron_shield(draw, 72, 48, scale=1.0)
    draw.text((160, 52), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((160, 84), "Who Benefits — Real-World Outcomes", font=title, fill=WHITE)
    draw.rectangle((160, 146, 720, 154), fill=GOLD)
    draw.text(
        (160, 172),
        "Terraform for Real Enterprises (Not Toy Projects)",
        font=subtitle,
        fill=WHITE,
    )
    draw.text(
        (160, 212),
        "Upskill for enterprise IaC roles — portfolio projects that support\n"
        "interviews, promotions, and client conversations.",
        font=body,
        fill=MUTED,
        spacing=6,
    )

    cols, rows = 3, 2
    card_w, card_h = 560, 280
    gx, gy = 100, 310
    gap_x, gap_y = 24, 20

    for i, (persona, benefit, career) in enumerate(PERSONAS):
        col = i % cols
        row = i // cols
        x0 = gx + col * (card_w + gap_x)
        y0 = gy + row * (card_h + gap_y)
        rounded_rect(draw, (x0, y0, x0 + card_w, y0 + card_h), 16, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, y0, x0 + 10, y0 + card_h), fill=GOLD)

        draw.ellipse((x0 + 28, y0 + 28, x0 + 52, y0 + 52), fill=GOLD)
        draw.text((x0 + 64, y0 + 30), persona, font=card_title, fill=WHITE)

        draw.text((x0 + 28, y0 + 78), "On the job", font=small, fill=GOLD_LT)
        by = y0 + 106
        for line in wrap_text(draw, benefit, card_body, card_w - 56):
            draw.text((x0 + 28, by), line, font=card_body, fill=MUTED)
            by += 24

        draw.text((x0 + 28, y0 + 180), "Career path", font=small, fill=GOLD_LT)
        cy = y0 + 208
        for line in wrap_text(draw, career, card_career, card_w - 56):
            draw.text((x0 + 28, cy), line, font=card_career, fill=WHITE)
            cy += 22

    draw.rectangle((0, H - 64, W, H), fill=(6, 22, 36))
    draw.rectangle((0, H - 68, W, H - 64), fill=GOLD)
    draw.text(
        (72, H - 44),
        "BayAreaLa8s  ·  bayareala8s.com  ·  Upskill · Portfolio · Interviews · Promotions · Client demos",
        font=ribbon,
        fill=WHITE,
    )
    return img


def render_square() -> Image.Image:
    sw, sh = 1080, 1080
    img = paint_backdrop(sw, sh)
    draw = ImageDraw.Draw(img)

    title = font(32, bold=True)
    subtitle = font(18, bold=False)
    body = font(17, bold=False)
    small = font(14, bold=False)
    card_title = font(17, bold=True)
    card_body = font(13, bold=False)
    card_career = font(13, bold=True)
    ribbon = font(14, bold=True)
    eyebrow = font(17, bold=True)

    personas = PERSONAS[:4]

    draw_chevron_shield(draw, 48, 36, scale=0.85)
    draw.text((136, 40), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((136, 70), "Who Benefits", font=title, fill=WHITE)
    draw.text((48, 118), "Terraform for Real Enterprises", font=subtitle, fill=WHITE)
    draw.rectangle((48, 148, 420, 154), fill=GOLD)
    draw.text(
        (48, 170),
        "Upskill for enterprise IaC roles — portfolio projects that\n"
        "support interviews, promotions, and client demos.",
        font=body,
        fill=MUTED,
        spacing=4,
    )

    card_w, card_h = 470, 300
    gx, gy = 48, 250
    gap_x, gap_y = 24, 20

    for i, (persona, benefit, career) in enumerate(personas):
        col = i % 2
        row = i // 2
        x0 = gx + col * (card_w + gap_x)
        y0 = gy + row * (card_h + gap_y)
        rounded_rect(draw, (x0, y0, x0 + card_w, y0 + card_h), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, y0, x0 + 8, y0 + card_h), fill=GOLD)

        draw.ellipse((x0 + 20, y0 + 22, x0 + 40, y0 + 42), fill=GOLD)
        draw.text((x0 + 50, y0 + 22), persona, font=card_title, fill=WHITE)

        draw.text((x0 + 20, y0 + 64), "On the job", font=small, fill=GOLD_LT)
        by = y0 + 88
        for line in wrap_text(draw, benefit, card_body, card_w - 40):
            draw.text((x0 + 20, by), line, font=card_body, fill=MUTED)
            by += 20

        draw.text((x0 + 20, y0 + 180), "Career path", font=small, fill=GOLD_LT)
        cy = y0 + 204
        for line in wrap_text(draw, career, card_career, card_w - 40):
            draw.text((x0 + 20, cy), line, font=card_career, fill=WHITE)
            cy += 20

    draw.rectangle((0, sh - 52, sw, sh), fill=(6, 22, 36))
    draw.rectangle((0, sh - 56, sw, sh - 52), fill=GOLD)
    draw.text(
        (36, sh - 36),
        "BayAreaLa8s  ·  Upskill · Portfolio · Interviews · Promotions",
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
