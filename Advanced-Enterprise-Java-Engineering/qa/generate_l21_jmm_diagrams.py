#!/usr/bin/env python3
"""Hand-drawn L-2.1 thread / JMM teaching diagrams. Does not rewrite D-001–017 boxes."""
from __future__ import annotations

import shutil
import struct
import subprocess
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "diagrams" / "java" / "l21"
D005 = ROOT / "diagrams" / "java"


def png_placeholder(path: Path, width: int = 960, height: int = 420) -> None:
    raw = b"".join(b"\x00" + bytes((244, 247, 250)) * width for _ in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    path.write_bytes(png)


def rasterize(svg: Path, png: Path, height: int = 420) -> None:
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        subprocess.run([rsvg, "-h", str(height), "-o", str(png), str(svg)], check=True)
        return
    ql = shutil.which("qlmanage")
    if ql:
        out = png.parent
        subprocess.run([ql, "-t", "-s", "1920", "-o", str(out), str(svg)], check=True, capture_output=True)
        thumb = out / f"{svg.name}.png"
        if thumb.exists():
            thumb.rename(png)
            return
    png_placeholder(png, 960, height)


HEADER = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" role="img" aria-labelledby="t d">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0a1f33"/></marker>
  <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#b42318"/></marker>
  <marker id="arrowOk" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#0d7a4f"/></marker>
</defs>
<rect width="100%" height="100%" fill="#f4f7fa"/>
<text id="t" x="40" y="36" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#0a1f33">{title}</text>
<text x="40" y="58" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0d8fad">{subtitle}</text>
<desc id="d">{desc}</desc>
"""

FOOTER = """<text x="40" y="406" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#5c6b7a">BayPay Financial Services is fictional. BayLearn AEJE. L-2.1 Threads and Java memory model.</text>
</svg>
"""


def card(x: int, y: int, w: int, h: int, fill: str = "#ffffff", stroke: str = "#0d8fad") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def threads_svg() -> str:
    return (
        HEADER.format(
            title="1. A thread owns a stack. The heap is shared.",
            subtitle="Locals stay on the stack. Payment lives on the heap. Both threads point at the same object.",
            desc="API thread and worker thread each have a private stack and program counter. Both reference one Payment on the shared heap.",
        )
        + card(40, 80, 250, 280)
        + card(355, 110, 250, 220, "#e8f4f8")
        + card(670, 80, 250, 280)
        + """
<text x="165" y="108" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0a1f33">API thread</text>
<text x="165" y="138" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">program counter</text>
<rect x="60" y="156" width="210" height="88" rx="4" fill="#f4f7fa" stroke="#0a1f33" stroke-width="1"/>
<text x="165" y="178" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">stack (private)</text>
<text x="165" y="200" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">markAuthorized()</text>
<text x="165" y="220" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">local: payment ref</text>
<text x="165" y="268" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d8fad">cannot see worker locals</text>

<text x="480" y="138" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0a1f33">Shared heap</text>
<text x="480" y="168" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">Payment</text>
<text x="480" y="196" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">authorized = ?</text>
<text x="480" y="218" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">amount = 84.00 USD</text>
<text x="480" y="250" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d8fad">one object, two threads</text>
<text x="480" y="300" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#5c6b7a">Harbor Bike Co invoice-8841</text>

<text x="795" y="108" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0a1f33">Worker thread</text>
<text x="795" y="138" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">program counter</text>
<rect x="690" y="156" width="210" height="88" rx="4" fill="#f4f7fa" stroke="#0a1f33" stroke-width="1"/>
<text x="795" y="178" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">stack (private)</text>
<text x="795" y="200" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">awaitAuthorized()</text>
<text x="795" y="220" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">local: payment ref</text>
<text x="795" y="268" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d8fad">cannot see API locals</text>

<line x1="290" y1="220" x2="355" y2="200" stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="670" y1="200" x2="605" y2="200" stroke="#0a1f33" stroke-width="2" marker-end="url(#arrow)"/>
"""
        + FOOTER
    )


def stale_svg() -> str:
    return (
        HEADER.format(
            title="2. Shared heap ≠ shared view. Stale authorized is legal.",
            subtitle="Left: no happens-before. Right: volatile write/read or monitor unlock/lock.",
            desc="Without a happens-before edge the worker may read authorized false after the API wrote true. A volatile write or unlock/lock publishes both authorized and amount.",
        )
        + card(40, 78, 430, 300, "#fdecea", "#b42318")
        + card(490, 78, 430, 300, "#e8f6ef", "#0d7a4f")
        + """
<text x="255" y="104" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#b42318">No happens-before</text>
<text x="80" y="136" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">API writes authorized = true</text>
<text x="80" y="156" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">API writes amount = 84.00</text>
<text x="80" y="188" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#b42318">Worker working copy: false</text>
<text x="80" y="216" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">while (!authorized) spin</text>
<line x1="80" y1="236" x2="380" y2="236" stroke="#b42318" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arrowRed)"/>
<text x="255" y="262" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#b42318">stale or torn: true + 0.00</text>
<text x="255" y="292" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">HTTP already returned AUTHORIZED</text>
<text x="255" y="348" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#b42318">ledger never posted</text>

<text x="705" y="104" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#0d7a4f">Happens-before edge</text>
<text x="520" y="136" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">volatile authorized = true</text>
<text x="520" y="156" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">or unlock after both writes</text>
<text x="520" y="188" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d7a4f">Worker later reads / locks</text>
<text x="520" y="216" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0a1f33">sees authorized and amount</text>
<line x1="520" y1="236" x2="850" y2="236" stroke="#0d7a4f" stroke-width="2" marker-end="url(#arrowOk)"/>
<text x="705" y="262" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d7a4f">one barrier, both fields</text>
<text x="705" y="292" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">worker leaves the spin</text>
<text x="705" y="348" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#0d7a4f">same JVM — not two pods</text>
"""
        + FOOTER
    )


def edges_svg() -> str:
    return (
        HEADER.format(
            title="3. Three APIs create a happens-before edge.",
            subtitle="They are not interchangeable. volatile publishes one field. Lock/unlock also excludes.",
            desc="Volatile write happens-before a later read of the same field. Monitor unlock happens-before the next lock. Lock.unlock happens-before the next lock.",
        )
        + card(40, 80, 880, 90)
        + card(40, 184, 880, 90)
        + card(40, 288, 880, 90)
        + """
<text x="56" y="108" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#0d8fad">volatile</text>
<text x="200" y="108" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">API writes authorized = true</text>
<line x1="430" y1="104" x2="560" y2="104" stroke="#0d7a4f" stroke-width="2" marker-end="url(#arrowOk)"/>
<text x="495" y="94" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#0d7a4f">write → later read</text>
<text x="580" y="108" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">Worker reads authorized</text>
<text x="56" y="148" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">Use for a flag or a Payment hand-off. Does not make balance += amount atomic.</text>

<text x="56" y="212" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#0d8fad">synchronized</text>
<text x="200" y="212" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">API unlocks monitor M</text>
<line x1="430" y1="208" x2="560" y2="208" stroke="#0d7a4f" stroke-width="2" marker-end="url(#arrowOk)"/>
<text x="495" y="198" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#0d7a4f">unlock → later lock</text>
<text x="580" y="212" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">Worker locks M</text>
<text x="56" y="252" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">Visibility plus mutual exclusion. Cannot time out. Do not lock a customer-id String.</text>

<text x="56" y="316" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#0d8fad">lock / unlock</text>
<text x="200" y="316" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">API lock.unlock() in finally</text>
<line x1="430" y1="312" x2="560" y2="312" stroke="#0d7a4f" stroke-width="2" marker-end="url(#arrowOk)"/>
<text x="495" y="302" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#0d7a4f">unlock → later lock</text>
<text x="580" y="316" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0a1f33">Worker lock.lock()</text>
<text x="56" y="356" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#5c6b7a">Same JMM edge as synchronized. Use when the waiter must tryLock or interrupt.</text>
"""
        + FOOTER
    )


def write_pair(stem: str, title: str, mermaid: str, alt: str, svg: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{stem}.source.md").write_text(
        f"# {title}\n\n- Module: 2\n- Maps to: L-2.1\n- Complexity: 1\n\n```mermaid\n{mermaid}\n```\n",
        encoding="utf-8",
    )
    (dest / f"{stem}.alt.md").write_text(alt.rstrip() + "\n", encoding="utf-8")
    svg_path = dest / f"{stem}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    rasterize(svg_path, dest / f"{stem}.png")


def main() -> None:
    write_pair(
        "threads-stack-heap",
        "L-2.1 picture 1 — Threads, stack, and heap",
        "flowchart LR\n  API[API thread stack] --> Pay[Payment on shared heap]\n  WRK[Worker thread stack] --> Pay",
        "Diagram L-2.1-1: API thread and worker thread each have a private stack. Both point at one Payment on the shared heap. BayPay is a fictional payment platform used for instruction.",
        threads_svg(),
        PACK,
    )
    write_pair(
        "stale-authorized",
        "L-2.1 picture 2 — Stale authorized versus happens-before",
        "flowchart LR\n  API[API writes authorized true] -.->|no happens-before| W[worker spins on false]\n  API2[volatile write or unlock] -->|happens-before| W2[worker sees true and amount]",
        "Diagram L-2.1-2: Without happens-before the worker may keep authorized false. A volatile write or unlock/lock publishes authorized and amount together. BayPay is fictional instruction.",
        stale_svg(),
        PACK,
    )
    write_pair(
        "happens-before-edges",
        "L-2.1 picture 3 — volatile, synchronized, lock/unlock",
        "flowchart TB\n  V[volatile write then read] --> HB[happens-before]\n  S[synchronized unlock then lock] --> HB\n  L[Lock.unlock then lock] --> HB",
        "Diagram L-2.1-3: Three BayPay APIs create happens-before: volatile write/read, synchronized unlock/lock, and Lock.unlock then lock. BayPay is a fictional payment platform used for instruction.",
        edges_svg(),
        PACK,
    )

    d005_svg = stale_svg().replace(
        "2. Shared heap ≠ shared view. Stale authorized is legal.",
        "AEJE-D-005 — Java memory visibility",
    )
    write_pair(
        "AEJE-D-005",
        "AEJE-D-005 — Java memory visibility",
        "flowchart LR\n  T1[API thread write] -->|no happens-before| Cache[worker stale authorized false]\n  T1b[volatile or unlock] -->|happens-before| Main[worker sees true and amount]",
        "Diagram AEJE-D-005: Java memory visibility. Left panel: worker may spin on stale authorized false. Right panel: volatile write or unlock/lock publishes authorized and amount. BayPay is fictional instruction.",
        d005_svg,
        D005,
    )
    (PACK / "README.md").write_text(
        """# L-2.1 visuals — Threads and the Java Memory Model

Three teaching pictures for [L-2.1](../../../course/modules/02-advanced-java-concurrency/lessons/L-2.1.md). BayPay is fictional.

| # | File | What to see |
|---|---|---|
| 1 | [threads-stack-heap.svg](threads-stack-heap.svg) | Each thread has a private stack. `Payment` lives on the shared heap. |
| 2 | [stale-authorized.svg](stale-authorized.svg) | Shared heap is not a shared view. Course catalog twin: [AEJE-D-005](../AEJE-D-005.svg). |
| 3 | [happens-before-edges.svg](happens-before-edges.svg) | `volatile`, `synchronized` unlock/lock, and `Lock.unlock`/`lock`. |

Open the SVG (or the mermaid in `*.source.md`). PNG is a raster sibling for slides.

Read left to right: **who owns the stack → why the worker can miss the write → which API creates the edge.**
""",
        encoding="utf-8",
    )
    print("wrote L-2.1 JMM visual pack + AEJE-D-005")


if __name__ == "__main__":
    main()
