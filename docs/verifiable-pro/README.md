# FLASH manuscript for verifiable.pro

The [English explainer](en.md) and [Simplified Chinese edition](zh.md) were generated through the existing daily editorial pipeline from the final FLASH paper and a selected primary-source packet. They are unpublished drafts. This owner-selected paper request uses the pipeline's editorial generation and preview components; it is separate from the scheduled recent-news scan.

## Filing metadata

Suggested slug: `flash-confidential-gpu-checkpoint`.

| Field | Value |
| --- | --- |
| Kind | `explainer` |
| Primary topic | `confidential-computing` |
| Stack layers | `runtime`, `hardware` |
| Automated byline | `research` |
| State | `draft: true` |

The `published` date in the hidden draft is a provisional preparation date supplied by the pipeline's required schema. It does not mean the article appeared on verifiable.pro. Set the actual filing date before publication. No live article URL is asserted here, and the website itself has not been modified.

The article's title and `dek` supply its searchable headline, page description, and list summary. Its natural subject terms include confidential LLM inference, GPU checkpoint and recovery, NVIDIA H100, Intel TDX, UVM dirty-page tracking, and hybrid-key checkpointing. The site has no separate article `tags` field.

## Figures and contextual references

The repository contains two editable explanations of the paper's mechanisms:

| Asset | Article section | English caption | 中文图注 |
| --- | --- | --- | --- |
| [`../figures/hybrid-key.svg`](../figures/hybrid-key.svg) | Keep the encryption already performed | FLASH stores the GPU copy engine's ciphertext alongside separately protected CPU state and key material. | FLASH 保存 GPU 复制引擎生成的密文，并分别保护 CPU 状态和相关密钥材料。 |
| [`../figures/dirty-tracking.svg`](../figures/dirty-tracking.svg) | Find writes while inference continues | Writes during background copying are tracked at 2 MB granularity; the final pause captures the dirty delta. | 后台复制期间按 2 MB 粒度跟踪写入，最终暂停时补拷脏页增量。 |

The draft preview renders these SVGs with the full bilingual copy. The current website's article Markdown subset does not expose arbitrary inline figure blocks; embedding them in a live article requires supported image integration. Keep the figure attribution when integrating them.

Both editions link to these existing verifiable.pro articles:

- [Remote attestation for AI workloads, explained](https://verifiable.pro/articles/remote-attestation-for-ai-workloads-explained/)
- [How to read a remote attestation report](https://verifiable.pro/articles/how-to-read-a-remote-attestation-report/)
- [Published private AI compute designs](https://verifiable.pro/articles/private-ai-compute-published-designs/)

The primary sources in the manuscripts link the final paper by an existing immutable Git commit, the [FLASH repository](https://github.com/sept-usc/FLASH), the [official ATC artifact evaluation record](https://sysartifacts.github.io/atc2026/results), and the [preserved artifact](https://doi.org/10.5281/zenodo.23199897).

## Presentation and disclosure

The README's “Presented by verifiable.pro” mark denotes editorial presentation. It is separate from the ACM artifact badges and does not assert verifiable.pro certification or independent reproduction. Both editions disclose that editor Mengyuan Li co-authored FLASH.

Once an actual article route exists, the repository's presentation link can point to it. Until then, the domain and these repository manuscript links provide valid cross-references.

## Validation and integration

The pipeline matched all four source citations in both languages, checked that the three contextual links return their expected live canonical URLs, and verified the preview's citation anchors. The site's editorial linter reports zero warnings. Quantitative serving and recovery results were checked against the final paper's Tables 5–6 and Sections 7.3–7.4.

The pipeline's existing publication adapter is limited to its standard single-source news packets. This multi-source explainer needs the normal editorial integration before it can be published. The saved preview does not authorize a site PR, merge, or deployment.
