# FLASH explanatory diagrams and paper figures

The README's first two diagrams are original vector redraws that explain the
final paper's mechanisms with simplified layouts. They are not verbatim paper
figures or new experimental results.

| Files | Purpose and source |
| --- | --- |
| `hybrid-key.svg`, `hybrid-key.png` | Hybrid-key checkpoint data path; paper Section 5.2 and Figure 4 |
| `dirty-tracking.svg`, `dirty-tracking.png` | Concurrent copy, UVM write-fault tracking at 2 MB granularity, and the dirty-delta pause; Section 5.3 and Figure 5 |
| `checkpoint-latency.png` | Unmodified rendered crop of paper Figure 6, PDF page 10 |
| `paper-originals/figure-4-hybrid-key.png` | Original paper Figure 4 crop, PDF page 5 |
| `paper-originals/figure-5-dirty-tracking.png` | Original paper Figure 5 crop, PDF page 6 |

The SVGs contain accessible titles and descriptions, use standard fonts, and
remain editable. PNG versions are exported at 1.5 times their SVG dimensions.
Black borders and arrows describe structure; blue marks protected GPU state or
read-only regions, teal marks the FLASH path, and rose marks repeated crypto or
dirty regions. Color is reinforced by text labels.

## Regenerate the diagrams

From the repository root, using Python 3:

```bash
python3 docs/figures/draw_diagrams.py
```

To also export PNGs, install CairoSVG in your Python environment, then run:

```bash
python3 -m pip install cairosvg
python3 docs/figures/draw_diagrams.py --png
```

CairoSVG requires a working Cairo installation. On macOS, the installed Cairo
library may need to be added to `DYLD_FALLBACK_LIBRARY_PATH`. SVG generation
itself uses only Python's standard library and does not need Cairo.

To re-extract the original paper crops with Poppler's `pdftoppm`:

```bash
bash docs/figures/render.sh
```

This updates the `paper-originals/` crops and `checkpoint-latency.png`; it does
not overwrite the redrawn diagrams.

## Attribution and scope

**Jonghyun Lee et al. FLASH: Fault-Led, Attested, Secure Hybrid-Key Checkpoint for
Confidential Inference. ACM SIGOPS ATC 2026. DOI:
[10.1145/3828523.3857076](https://doi.org/10.1145/3828523.3857076).**

Source: [`../flash-atc2026.pdf`](../flash-atc2026.pdf). The paper is licensed under
**Creative Commons Attribution 4.0 International (CC BY 4.0)**, as stated on its
first page. The redraws adapt its mechanisms and retain that attribution.
The plotting script is covered by the repository's code license.

The hybrid-key diagram explains checkpoint creation. It omits restore-time
decryption, destination re-encryption, and the remote key-release protocol;
the source GPU key is wrapped under the checkpoint key, not stored in the
clear. The dirty-tracking diagram uses three example dynamic regions and one
write to illustrate the dirty bitmap. It omits static allocation
classification and does not represent measured phase durations.
