# FLASH input for the daily editorial pipeline

Generate a bilingual explainer for verifiable.pro from the primary sources below. Treat the neighboring manuscript files as prepared copy and source organization, not as evidence that a pipeline run has completed. Use the pipeline's normal research, claim checking, drafting, review, and filing stages. The requested outcome is generated copy and cross-references; publication is a separate action.

## Editorial angle

FLASH addresses reliable confidential LLM inference: protected GPU state must be saved without a long serving pause, and recovered state must retain integrity and freshness checks. Explain why retaining already-encrypted GPU data and tracking writes at the driver boundary fit that goal. Give the reader the trust assumptions and the exact scope of the reported performance.

## Primary sources

1. Final PDF: <https://github.com/sept-usc/FLASH/blob/cfe082f3fa9d6f68374b312c934fc86668ffc510/docs/flash-atc2026.pdf>. Local copy: `../flash-atc2026.pdf`.
2. Code and reproduction instructions: <https://github.com/sept-usc/FLASH>.
3. Official artifact evaluation record: <https://sysartifacts.github.io/atc2026/results>.
4. Preserved artifact: <https://doi.org/10.5281/zenodo.23199897>.

## Claims and boundaries to preserve

- Exact title: FLASH: Fault-Led, Attested, Secure Hybrid-Key Checkpoint for Confidential Inference. Venue: ACM SIGOPS ATC 2026.
- Authors: Jonghyun Lee, Taewoon Kang, Yongqin Wang, Rachit Rajat, Mengyuan Li, Gunjae Koo, Daniel Wong, Murali Annavaram. Use the final PDF's author list rather than the earlier accepted-paper entry.
- Preserve the GPU copy engine's device-to-host ciphertext; CPU state and the source GPU key are protected under the checkpoint key. Retain IVs and authentication tags. Recovery still reconstructs and decrypts saved state. Source: Sections 5.1–5.2.
- Track writes with UVM write faults at 2 MB granularity. Most copying overlaps with inference; the final pause captures dirty data. No changes to the LLM kernels or offline PTX analysis. Source: Section 5.3.
- Static data is captured once and reused. Recovery restores static and dynamic state. The released default static mode uses host-to-device allocation flags; learning is opt-in. Source: Section 5.4 and `benchmarks/flash/ckpt_agent.c`.
- Security protocol covers confidentiality, integrity and freshness under the stated CPU/GPU TEE, guest software and trusted remote-service assumptions. Attestation is evidence about loaded software, not a correctness guarantee. Availability and volume/access-pattern/timing leakage are outside its protection. Source: Sections 3 and 6.
- Evaluation: one 80 GB H100 in confidential mode, Intel TDX, vLLM 0.8.5, three models, Chatbot and Reasoning, tmpfs image staging. Source: Section 7.1.
- Reported summary: 1.2 s mean stop-and-copy across FLASH and FLASH-SC. 9.4× relative to PhOS, 7.8× relative to GCR at a one-minute interval. Comparison implementations are reimplemented data paths, not original systems running unchanged. Source: Sections 7.1–7.2.
- Serving impact varies by workload. Do not claim uniformly low overhead or confuse checkpoint pause with recovery time. Source: Section 7.3.
- Released repository supplies driver changes and evaluation programs; complete remote attestation/key-release service deployment needs additional integration.
- All three ACM artifact badges are recorded on the official evaluation page. Do not claim verifiable.pro independently reproduced the results or certified FLASH.

## Cross-references and disclosure

Link the project repository, final PDF, archived artifact, and existing verifiable.pro articles on remote attestation. Link the two redesigned mechanism diagrams through the README or direct repository assets. Keep the GitHub README link back to verifiable.pro distinct from the ACM badges. Disclose that editor Mengyuan Li is a co-author. Assign an actual filing date only when the pipeline files the article.
