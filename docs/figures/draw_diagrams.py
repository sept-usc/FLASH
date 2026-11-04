#!/usr/bin/env python3
"""Draw the README's conceptual FLASH diagrams as editable SVGs.

Run with Python 3. PNG export additionally needs CairoSVG:
    python3 -m pip install cairosvg
    python3 docs/figures/draw_diagrams.py --png

The figures explain the final paper's Sections 5.2/5.3 and Figures 4/5.
They are explanatory redraws, not benchmark data or verbatim paper figures.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK = "#000000"
TEXT = "#14191E"
MUTED = "#46525D"
TEAL = "#08766C"
TEAL_WASH = "#E9F6F2"
BLUE_WASH = "#EAF1FA"
ROSE = "#A62E30"
ROSE_WASH = "#FCE9E5"
AMBER_WASH = "#FFF1D4"


class Diagram:
    def __init__(self, width: int, height: int, title: str, description: str):
        self.width, self.height = width, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            'role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="description">{escape(description)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" '
            'refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10Z" fill="#000000"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
        ]

    def rect(self, x, y, w, h, fill="#FFFFFF", radius=10, stroke=INK, sw=1.8):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, value, size=22, weight=400, fill=TEXT, anchor="start", mono=False):
        font = "'SFMono-Regular',Consolas,monospace" if mono else "Arial,Helvetica,sans-serif"
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(value)}</text>'
        )

    def line(self, x1, y1, x2, y2, arrow=False, dashed=False, sw=2):
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{INK}" stroke-width="{sw}"'
            + (' marker-end="url(#arrow)"' if arrow else "")
            + (' stroke-dasharray="7 6"' if dashed else "")
            + '/>'
        )

    def number(self, x, y, number, fill=TEAL_WASH):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="19" fill="{fill}" stroke="{INK}" stroke-width="1.8"/>')
        self.text(x, y + 7, str(number), size=21, weight=700, anchor="middle")

    def save(self, name: str, png=False):
        path = ROOT / f"{name}.svg"
        path.write_text("\n".join(self.parts + ["</svg>"]) + "\n")
        if png:
            import cairosvg
            cairosvg.svg2png(url=str(path), write_to=str(ROOT / f"{name}.png"), scale=1.5)


def hybrid_key(png: bool):
    d = Diagram(1360, 748,
        "FLASH hybrid-key checkpoint: retain the GPU ciphertext",
        "The conventional secure checkpoint decrypts GPU ciphertext inside the CPU TEE and encrypts it again under the checkpoint key. FLASH preserves GPU ciphertext and its IVs and tags, while wrapping CPU state and the source GPU key separately under the checkpoint key. PCIe and stored images carry encrypted data.")
    d.text(40, 49, "Keep GPU ciphertext. Remove repeated CPU crypto.", 30, 700)
    d.text(40, 82, "The GPU already encrypts data before it crosses untrusted PCIe.", 21, fill=MUTED)

    d.text(40, 139, "CONVENTIONAL SECURE CHECKPOINT", 20, 700, ROSE)
    d.text(40, 185, "GPU TEE", 18, 700)
    d.text(354, 185, "UNTRUSTED PCIe", 16, 700, MUTED, "middle")
    d.text(462, 185, "CPU TEE", 18, 700)
    d.text(1036, 185, "ENCRYPTED IMAGE", 18, 700)

    d.rect(40, 202, 214, 136, BLUE_WASH)
    d.text(147, 238, "HBM state", 24, 700, anchor="middle")
    d.line(71, 252, 223, 252, sw=1.2)
    d.text(147, 282, "CE encrypts", 22, anchor="middle")
    d.text(147, 312, "K_D2H", 21, anchor="middle", mono=True)

    d.line(254, 270, 456, 270, arrow=True)
    d.text(355, 245, "GPU ciphertext", 18, anchor="middle")
    d.text(355, 302, "K_D2H", 18, fill=MUTED, anchor="middle", mono=True)

    d.rect(462, 202, 494, 136, TEAL_WASH)
    d.rect(481, 224, 197, 89, "#FFFFFF", 7)
    d.text(579.5, 257, "Decrypt", 23, 700, anchor="middle")
    d.text(579.5, 290, "K_D2H", 20, anchor="middle", mono=True)
    d.line(678, 269, 726, 269, arrow=True)
    d.rect(733, 224, 203, 89, "#FFFFFF", 7)
    d.text(834.5, 257, "Encrypt", 23, 700, anchor="middle")
    d.text(834.5, 290, "K_CKPT", 20, anchor="middle", mono=True)
    d.line(956, 270, 1026, 270, arrow=True)

    d.rect(1036, 202, 284, 136, "#F5F6F8")
    d.text(1178, 249, "GPU + CPU state", 23, 700, anchor="middle")
    d.text(1178, 289, "under K_CKPT", 21, anchor="middle", mono=True)
    d.text(709, 369, "Decrypt → encrypt, on every checkpoint", 21, 700, ROSE, "middle")

    d.line(40, 401, 1320, 401, sw=1.2)
    d.text(40, 446, "FLASH HYBRID-KEY CHECKPOINT", 20, 700, TEAL)
    d.text(40, 487, "GPU TEE", 18, 700)
    d.text(354, 487, "UNTRUSTED PCIe", 16, 700, MUTED, "middle")
    d.text(462, 487, "CPU TEE", 18, 700)
    d.text(1036, 487, "ENCRYPTED IMAGE", 18, 700)

    d.rect(40, 504, 214, 136, BLUE_WASH)
    d.text(147, 540, "HBM state", 24, 700, anchor="middle")
    d.line(71, 554, 223, 554, sw=1.2)
    d.text(147, 584, "CE encrypts", 22, anchor="middle")
    d.text(147, 614, "K_D2H", 21, anchor="middle", mono=True)
    d.line(254, 552, 456, 552, arrow=True)
    d.text(355, 532, "GPU ciphertext", 18, anchor="middle")
    d.text(355, 583, "K_D2H", 18, fill=MUTED, anchor="middle", mono=True)

    d.rect(462, 504, 494, 154, TEAL_WASH)
    d.text(709, 540, "Retain ciphertext + IVs + tags", 23, 700, TEAL, "middle")
    d.line(485, 555, 1026, 555, arrow=True)
    d.rect(481, 580, 455, 58, "#FFFFFF", 7)
    d.text(708.5, 604, "CPU state + source K_D2H", 20, 700, anchor="middle")
    d.text(708.5, 627, "wrap under K_CKPT", 18, anchor="middle")
    d.line(956, 611, 1026, 611, arrow=True)

    d.rect(1036, 504, 284, 154, "#F5F6F8")
    d.text(1178, 533, "GPU ciphertext", 22, 700, anchor="middle")
    d.text(1178, 559, "under K_D2H · IVs · tags", 17, anchor="middle")
    d.line(1054, 575, 1302, 575, sw=1.2)
    d.text(1178, 604, "CPU state + GPU key", 21, 700, anchor="middle")
    d.text(1178, 633, "under K_CKPT", 19, anchor="middle", mono=True)

    d.text(40, 710, "GPU ciphertext is reused; CPU state and the source GPU key are protected separately.", 22, 700)
    d.save("hybrid-key", png)


def page_row(d: Diagram, x, y, dirty=False, all_rw=False):
    for i in range(3):
        fill = ROSE_WASH if dirty and i == 1 else TEAL_WASH if all_rw else BLUE_WASH
        d.rect(x + i * 100, y, 80, 84, fill, 5)
        d.text(x + i * 100 + 40, y + 29, f"P{i}", 20, 700, anchor="middle")
        d.text(x + i * 100 + 40, y + 62, "RW" if all_rw or dirty and i == 1 else "RO", 22, anchor="middle")


def dirty_tracking(png: bool):
    d = Diagram(1360, 752,
        "FLASH UVM dirty tracking: concurrent copy followed by a small dirty delta",
        "First, the driver marks GPU-resident UVM regions read-only and starts a background copy while inference runs. A write fault marks its 2 MB region dirty and restores write permission. At a quiesce point, FLASH pauses inference to recopy dirty regions, restores read-write permissions, and resumes serving. Three example regions and the dirty bitmap illustrate the process.")
    d.text(40, 49, "Copy in the background. Pause only for the dirty delta.", 30, 700)
    d.text(40, 82, "UVM write faults identify which 2 MB regions changed during concurrent copying.", 21, fill=MUTED)

    d.rect(40, 112, 840, 44, TEAL_WASH, 7)
    d.text(460, 141, "CONCURRENT COPY  ·  INFERENCE CONTINUES", 20, 700, TEAL, "middle")
    d.rect(920, 112, 400, 44, AMBER_WASH, 7)
    d.text(1120, 141, "STOP-AND-COPY  ·  SHORT PAUSE", 18, 700, TEXT, "middle")

    for x in [40, 480, 920]:
        d.rect(x, 178, 400, 477, "#FFFFFF", 11)

    d.number(78, 216, 1)
    d.text(110, 224, "Protect and copy", 25, 700)
    d.text(64, 268, "Set tracked regions read-only.", 21)
    d.text(64, 296, "Begin the background copy.", 21)
    page_row(d, 100, 335)
    d.text(240, 448, "Each box is a 2 MB region", 18, fill=MUTED, anchor="middle")
    d.line(240, 463, 240, 509, arrow=True)
    d.rect(112, 521, 256, 70, BLUE_WASH, 7)
    d.text(240, 550, "Background image", 22, 700, anchor="middle")
    d.text(240, 577, "inference keeps running", 17, fill=MUTED, anchor="middle")

    d.number(518, 216, 2)
    d.text(550, 224, "Record writes", 25, 700)
    d.text(504, 268, "First write raises a UVM fault.", 21)
    d.text(504, 296, "Mark its region dirty; allow writes.", 21)
    page_row(d, 540, 335, dirty=True)
    d.text(680, 449, "P1 written → bitmap bit = 1", 18, 700, ROSE, "middle")
    d.line(680, 463, 680, 509, arrow=True)
    d.rect(552, 521, 256, 70, "#F5F6F8", 7)
    d.text(582, 562, "Dirty bitmap", 19, 700)
    for i, bit in enumerate("010"):
        d.rect(700 + i * 30, 539, 30, 35, ROSE_WASH if bit == "1" else "#FFFFFF", 0, sw=1.2)
        d.text(715 + i * 30, 564, bit, 21, 700, anchor="middle", mono=True)

    d.number(958, 216, 3, AMBER_WASH)
    d.text(990, 224, "Pause, copy, resume", 25, 700)
    d.text(944, 268, "Quiesce at a consistent point.", 21)
    d.text(944, 296, "Recopy only marked regions.", 21)
    page_row(d, 980, 335, dirty=True)
    d.line(1120, 419, 1120, 496, arrow=True)
    d.rect(1000, 508, 240, 60, ROSE_WASH, 7)
    d.text(1120, 546, "Dirty delta: P1 only", 22, 700, anchor="middle")
    d.text(1120, 605, "Restore RW permissions", 21, 700, anchor="middle")
    d.text(1120, 633, "Resume inference", 22, 700, TEAL, "middle")

    d.line(440, 376, 474, 376, arrow=True)
    d.line(880, 376, 914, 376, arrow=True)
    d.rect(40, 685, 21, 21, BLUE_WASH, 3, sw=1.5)
    d.text(73, 703, "RO = read-only", 18)
    d.rect(265, 685, 21, 21, ROSE_WASH, 3, sw=1.5)
    d.text(298, 703, "RW = read-write; marked region is dirty", 18)
    d.text(1320, 703, "Conceptual flow; not a timing scale", 18, fill=MUTED, anchor="end")
    d.save("dirty-tracking", png)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--png", action="store_true", help="also export PNGs using CairoSVG")
    args = parser.parse_args()
    hybrid_key(args.png)
    dirty_tracking(args.png)
