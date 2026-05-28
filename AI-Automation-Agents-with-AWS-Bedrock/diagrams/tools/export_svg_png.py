#!/usr/bin/env python3
"""Export detailed .drawio diagrams to SVG and PNG."""

from __future__ import annotations

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (drawio source dir, svg output dir, png output dir)
EXPORT_DIRS = [
    (ROOT / "drawio", ROOT / "svg", ROOT / "png"),
    (ROOT / "student" / "drawio", ROOT / "student" / "svg", ROOT / "student" / "png"),
]

AWS_COLORS = {
    "lambda": "#D86613", "api_gateway": "#8C4FFF", "step_functions": "#E7157B",
    "eventbridge": "#E7157B", "dynamodb": "#527FFF", "s3": "#3F8624",
    "cloudwatch": "#E7157B", "bedrock": "#232F3E", "iam": "#DD3522",
    "user": "#232F3E", "client": "#232F3E", "cognito": "#8C4FFF",
    "sns": "#E7157B", "waf": "#DD3522", "document": "#879196",
    "secrets": "#DD3522", "generic": "#879196", "default": "#D86613",
}

BOX_FILLS = {
    "neutral": ("#F2F3F3", "#879196"),
    "code": ("#232F3E", "#232F3E"),
    "danger": ("#FADBD8", "#DD3522"),
    "success": ("#E9F7EF", "#248814"),
    "legend": ("#FFFFFF", "#232F3E"),
    "objective": ("#E8F4FD", "#527FFF"),
    "instructor": ("#FFF8E6", "#FFB800"),
    "student": ("#F3E8FF", "#8C4FFF"),
    "zone": ("#F7F8F8", "#879196"),
}


def decode_val(raw: str) -> str:
    return raw.replace("&#10;", "\n").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def box_style(style: str) -> str:
    if "fillColor=#232F3E" in style and "fontColor=#FFFFFF" in style:
        return "code"
    if "fillColor=#FADBD8" in style:
        return "danger"
    if "fillColor=#E9F7EF" in style:
        return "success"
    if "fillColor=#E8F4FD" in style:
        return "objective"
    if "fillColor=#FFF8E6" in style and "strokeColor=#FFB800" in style:
        return "instructor"
    if "fillColor=#F3E8FF" in style:
        return "student"
    if "fillColor=#FFFFFF" in style and "LEGEND" in style:
        return "legend"
    if "dashed=1" in style and "fontStyle=1" in style:
        return "zone"
    return "neutral"


def shape_from_style(style: str) -> str:
    m = re.search(r"shape=mxgraph\.aws4\.([^;]+)", style)
    if m:
        s = m.group(1).replace("identity_and_access_management", "iam")
        return s.split(";")[0]
    if "ellipse" in style and "fillColor=#232F3E" in style:
        return "step"
    return "generic"


def fill_from_style(style: str) -> str:
    m = re.search(r"fillColor=([^;]+)", style)
    if m and m.group(1).startswith("#"):
        return m.group(1)
    return AWS_COLORS["default"]


def parse_drawio(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    diagram = root.find("diagram")
    model = diagram.find("mxGraphModel") if diagram is not None else None
    cells = model.find("root") if model is not None else None
    pw = int(model.get("pageWidth", 1600)) if model is not None else 1600
    ph = int(model.get("pageHeight", 1100)) if model is not None else 1100
    title = diagram.get("name", path.stem) if diagram is not None else path.stem

    vertices, edges, boxes, steps, titles = [], [], [], [], []
    if cells is None:
        return {"vertices": vertices, "edges": edges, "boxes": boxes, "steps": steps,
                "titles": titles, "width": pw, "height": ph, "title": title}

    for cell in cells.findall("mxCell"):
        style = cell.get("style", "")
        val = decode_val(cell.get("value", "") or "")
        geo = cell.find("mxGeometry")
        if geo is None:
            continue
        x, y = float(geo.get("x", 0)), float(geo.get("y", 0))
        w, h = float(geo.get("width", 80)), float(geo.get("height", 80))

        if cell.get("edge") == "1":
            edges.append({
                "source": cell.get("source"), "target": cell.get("target"),
                "label": val, "dashed": "dashed=1" in style,
                "color": re.search(r"strokeColor=([^;]+)", style).group(1) if "strokeColor=" in style else "#232F3E",
                "bold": "strokeWidth=2" in style,
            })
            continue

        if cell.get("vertex") != "1" or cell.get("id") in ("0", "1"):
            continue

        if "fontSize=20" in style or "fontSize=18" in style:
            titles.append({"text": val, "x": x, "y": y, "size": 20 if "fontSize=20" in style else 18})
            continue
        if "fontSize=12" in style and "fillColor=none" in style:
            titles.append({"text": val, "x": x, "y": y, "size": 12})
            continue

        if shape_from_style(style) == "step":
            steps.append({"num": val, "x": x, "y": y})
            continue

        if "aspect=fixed" in style and "mxgraph.aws4" in style:
            vertices.append({
                "id": cell.get("id"), "label": val, "x": x, "y": y, "w": w, "h": h,
                "shape": shape_from_style(style), "fill": fill_from_style(style),
            })
            continue

        if val.strip():
            bstyle = box_style(style)
            boxes.append({"label": val, "x": x, "y": y, "w": w, "h": h, "style": bstyle,
                          "text_light": bstyle == "code"})

    return {"vertices": vertices, "edges": edges, "boxes": boxes, "steps": steps,
            "titles": titles, "width": pw, "height": ph, "title": title}


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _lines(text: str, x: float, y: float, size: int = 10, light: bool = False, bold: bool = False) -> list[str]:
    fill = "#FFFFFF" if light else "#232F3E"
    weight = "bold" if bold else "normal"
    out = []
    for i, line in enumerate(text.split("\n")):
        dy = y + 14 + i * (size + 4)
        out.append(
            f'<text x="{x}" y="{dy}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{_esc(line)}</text>'
        )
    return out


def render_svg(data: dict) -> str:
    w, h = data["width"], data["height"]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'<rect width="100%" height="100%" fill="#ffffff"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">'
        '<path d="M0,0 L9,3 L0,6 Z" fill="#232F3E"/></marker></defs>',
    ]

    for t in data.get("titles", []):
        sz = t.get("size", 14)
        fill = "#565656" if sz == 12 else "#232F3E"
        weight = "bold" if sz >= 18 else "normal"
        lines.append(
            f'<text x="{t["x"]}" y="{t["y"]+sz}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="{sz}" font-weight="{weight}" fill="{fill}">{_esc(t["text"])}</text>'
        )

    for box in data["boxes"]:
        fill, stroke = BOX_FILLS.get(box["style"], BOX_FILLS["neutral"])
        rx = 0 if box["style"] == "code" else 6
        dash = 'stroke-dasharray="6,4"' if box["style"] == "zone" else ""
        lines.append(
            f'<rect x="{box["x"]}" y="{box["y"]}" width="{box["w"]}" height="{box["h"]}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" {dash}/>'
        )
        lines.extend(_lines(box["label"], box["x"] + 10, box["y"] + 8, 10, box.get("text_light", False),
                              bold=box["label"].startswith("LEARNING") or box["label"].startswith("LEGEND")))

    for step in data.get("steps", []):
        cx, cy = step["x"] + 14, step["y"] + 14
        lines.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#232F3E"/>')
        lines.append(
            f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="12" font-weight="bold" '
            f'fill="#FFFFFF">{_esc(step["num"])}</text>'
        )

    vmap = {v["id"]: v for v in data["vertices"]}
    for v in data["vertices"]:
        color = AWS_COLORS.get(v["shape"], v["fill"])
        lines.append(
            f'<rect x="{v["x"]}" y="{v["y"]}" width="{v["w"]}" height="{v["h"]}" '
            f'rx="4" fill="{color}" stroke="#ffffff" stroke-width="2"/>'
        )
        cx = v["x"] + v["w"] / 2
        parts = v["label"].split("\n")
        for i, part in enumerate(parts[:2]):
            lines.append(
                f'<text x="{cx}" y="{v["y"]+v["h"]+14+i*12}" text-anchor="middle" '
                f'font-size="9" fill="#232F3E">{_esc(part)}</text>'
            )

    for e in data["edges"]:
        s, t = vmap.get(e["source"]), vmap.get(e["target"])
        if not s or not t:
            continue
        x1, y1 = s["x"] + s["w"] / 2, s["y"] + s["h"] / 2
        x2, y2 = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
        color = e.get("color", "#232F3E")
        dash = 'stroke-dasharray="8,4"' if e.get("dashed") else ""
        sw = 2.5 if e.get("bold") else 1.5
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#arrow)" {dash}/>'
        )
        if e.get("label"):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
            lines.append(
                f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="9" fill="{color}">'
                f'{_esc(e["label"][:40])}</text>'
            )

    lines.append(
        f'<text x="40" y="{h-16}" font-size="9" fill="#879196">'
        f'BayAreaLa8s — AI Automation &amp; Agents with AWS Bedrock | AWS Architecture Icons (aws4)</text>'
    )
    lines.append("</svg>")
    return "\n".join(lines)


def svg_to_png(svg_path: Path, png_path: Path) -> bool:
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2.0)
        return png_path.exists()
    except Exception:
        return False


def export_directory(drawio_dir: Path, svg_dir: Path, png_dir: Path) -> tuple[int, int]:
    svg_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(drawio_dir.glob("*.drawio"))
    png_ok = 0
    for f in files:
        data = parse_drawio(f)
        svg_path = svg_dir / f"{f.stem}.svg"
        png_path = png_dir / f"{f.stem}.png"
        svg_path.write_text(render_svg(data), encoding="utf-8")
        if svg_to_png(svg_path, png_path):
            png_ok += 1
        print(f"  {f.stem}: svg + {'png' if png_path.exists() else 'png skipped'}")
    return len(files), png_ok


def main() -> int:
    total_files = 0
    total_png = 0
    for drawio_dir, svg_dir, png_dir in EXPORT_DIRS:
        if not drawio_dir.exists():
            continue
        rel = drawio_dir.relative_to(ROOT)
        print(f"\nExporting {rel}/")
        count, png_ok = export_directory(drawio_dir, svg_dir, png_dir)
        total_files += count
        total_png += png_ok
    if total_files == 0:
        print("No drawio files — run generate_all_diagrams.py and generate_student_diagrams.py first")
        return 1
    print(f"\nExported {total_files} SVG, {total_png} PNG")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
