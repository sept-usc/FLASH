# FLASH copy for verifiable.pro

This package contains an English explainer and a matching Simplified Chinese edition. It is a manuscript package, not a published article. The existing verifiable.pro site has not been modified.

| File | Purpose |
| --- | --- |
| [`en.md`](en.md) | English source with the site's front matter and numbered citations |
| [`zh.md`](zh.md) | Chinese edition, inheriting metadata and sources from English |
| [`PIPELINE_INPUT.md`](PIPELINE_INPUT.md) | Source packet for the daily editorial pipeline |

## Filing metadata

Suggested slug: `flash-confidential-gpu-checkpoint`.

- Kind: `explainer`.
- Primary topic: `confidential-computing`.
- Stack layers: `runtime`, `hardware`.
- Automated byline: `research`.
- State: `draft: true`.
- Publication date: intentionally unset. The site's `published` field means the date actually filed on verifiable.pro and is required even for a build including drafts. Set it when the editorial pipeline assigns the filing date; do not treat the current manuscript as an already published item.

The manuscript follows the existing content schema. It is not ready to import into a build until that date has been assigned. No live article URL is asserted here.

## Card copy

**English title:** FLASH: checkpointing confidential LLM inference on NVIDIA H100

**English teaser:** Saving a confidential inference session should preserve its protection as well as its progress. FLASH retains GPU ciphertext and tracks dirty pages to reduce the final checkpoint pause.

**中文标题：** FLASH：在 NVIDIA H100 上为机密 LLM 推理建立检查点

**中文摘要：** 保存机密推理会话，需要同时保留计算进度与状态保护。FLASH 复用 GPU 密文并跟踪脏页，以减少建立检查点时的最终停顿。

Use the `dek` in each edition for the site's page description and list summary. The natural search terms are confidential LLM inference, GPU checkpoint and recovery, NVIDIA H100, Intel TDX, UVM dirty-page tracking, and hybrid-key checkpointing. The site derives search and machine-readable output from the article; it has no separate article `tags` field.

## Figure cross-references

The repository's redesigned diagrams are editable vector explanations of the paper, rather than original paper figures:

| Asset | Article section | English link or caption | 中文链接或图注 |
| --- | --- | --- | --- |
| [`../figures/hybrid-key.svg`](../figures/hybrid-key.svg) | Reuse the GPU's ciphertext | FLASH stores the GPU copy engine's ciphertext alongside separately protected CPU state and key material. | FLASH 保存 GPU 复制引擎生成的密文，并分别保护 CPU 状态和相关密钥材料。 |
| [`../figures/dirty-tracking.svg`](../figures/dirty-tracking.svg) | Copy in the background, then capture the dirty delta | Writes during background copying are tracked at 2 MB granularity; the final pause copies the dirty delta. | 后台复制期间按 2 MB 粒度记录写入，最终暂停时只补拷脏页增量。 |
| [`../figures/checkpoint-latency.png`](../figures/checkpoint-latency.png) | What the H100 evaluation measures | Original paper Figure 6 compares concurrent-copy and stop-and-copy latency in the evaluated workloads. | 论文原图 6 对比评测工作负载下的并发复制与 stop-and-copy 延迟。 |

The current site Markdown subset does not expose arbitrary inline figure blocks. These assets can be linked from the copy. Embedding them in the live article requires the site's supported image pipeline or a reviewed article-figure feature; do not paste HTML that its renderer escapes. Keep the source and figure attribution when integrating them.

## Presentation and attribution

The README's “Presented by verifiable.pro” mark denotes editorial presentation and links to verifiable.pro. It is separate from the ACM artifact badges and does not assert verifiable.pro certification or independent reproduction. Both article editions disclose that the site's editor co-authored FLASH.

Once an actual article route exists, the repository's presentation mark may link directly to that route. Until then, link to the existing domain and keep the manuscript links in the repository valid.

## Validation

The site's `tools/lint_content.py` functions report zero editorial warnings for this package. The English body is approximately 1,200 words. Both editions cite the same four numbered sources. The final paper is linked by an existing immutable Git commit, so its source link works independently of the README PR's merge status.
