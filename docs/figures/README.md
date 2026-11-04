# Paper figures

These PNGs are rendered crops from the final paper included at
[`../flash-atc2026.pdf`](../flash-atc2026.pdf):

**Jonghyun Lee et al. FLASH: Fault-Led, Attested, Secure Hybrid-Key Checkpoint for
Confidential Inference. ACM SIGOPS ATC 2026. DOI:
[10.1145/3828523.3857076](https://doi.org/10.1145/3828523.3857076).**

The paper is licensed under **Creative Commons Attribution 4.0 International
(CC BY 4.0)**, as stated on its first page. The only changes to these figures
are cropping and rasterization; labels and data are unchanged.

| File | Source |
| --- | --- |
| `hybrid-key.png` | Figure 4, PDF page 5 |
| `dirty-tracking.png` | Figure 5, PDF page 6 |
| `checkpoint-latency.png` | Figure 6, PDF page 10 |

Regenerate from any directory with Poppler's `pdftoppm` installed:

```bash
bash docs/figures/render.sh  # when invoked from the repository root
```

Each crop is rendered at 300 DPI directly from the final PDF to keep the
README independent of older figure sources.
