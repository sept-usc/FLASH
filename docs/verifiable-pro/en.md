---
title: FLASH: checkpointing confidential LLM inference on NVIDIA H100
dek: FLASH retains GPU ciphertext and tracks modified memory pages to shorten checkpoint pauses in confidential inference. Its H100 and Intel TDX evaluation shows how recovery support can be built around the encrypted GPU data path.
kind: explainer
topics: [confidential-computing]
layers: [runtime, hardware]
agent: research
evidence: [paper, code]
draft: true
disclosure: Mengyuan Li, editor of verifiable.pro, is a co-author of FLASH. This article presents that research; it does not report an independent reproduction by verifiable.pro.
sources:
  - FLASH: Fault-Led, Attested, Secure Hybrid-Key Checkpoint for Confidential Inference | Jonghyun Lee et al., ACM SIGOPS ATC 2026 | 2026 | https://github.com/sept-usc/FLASH/blob/cfe082f3fa9d6f68374b312c934fc86668ffc510/docs/flash-atc2026.pdf
  - FLASH source code and reproduction instructions | FLASH authors | accessed 2026-11-04 | https://github.com/sept-usc/FLASH
  - ATC 2026 artifact evaluation results | Systems Research Artifacts | accessed 2026-11-04 | https://sysartifacts.github.io/atc2026/results
  - jonghyunL/artifact_flash: ATC Artifact Evaluation | Zenodo | 2026-10-07 | https://doi.org/10.5281/zenodo.23199897
related: [remote-attestation-for-ai-workloads-explained, how-to-read-a-remote-attestation-report]
---

FLASH is a checkpoint and recovery system for confidential large language model (LLM) inference. It saves the data state needed to resume serving while limiting the time that inference must pause. The design combines encrypted checkpoint storage with memory tracking in NVIDIA's driver, and the paper evaluates it on one NVIDIA H100 GPU with Intel Trust Domain Extensions (TDX). The result concerns a specific operational problem: keeping protected inference state recoverable without repeatedly stopping the service for a full GPU memory dump.[^1]

The paper, *FLASH: Fault-Led, Attested, Secure Hybrid-Key Checkpoint for Confidential Inference*, is by Jonghyun Lee, Taewoon Kang, Yongqin Wang, Rachit Rajat, Mengyuan Li, Gunjae Koo, Daniel Wong, and Murali Annavaram, for ACM SIGOPS ATC 2026.[^1]

## Why encrypted inference is harder to checkpoint

During inference, a model accumulates a key-value (KV) cache holding attention state from the tokens it has processed. Losing the cache discards work already done for active requests. A checkpoint saves this state so that recovery can resume from a saved position. In a confidential deployment, a CPU trusted execution environment (TEE) and a GPU TEE are designed to keep model and request data from a malicious cloud host within their hardware threat models.[^1]

That protection changes the checkpoint path. GPU data must cross an untrusted PCIe connection before it can be saved. The H100 copy engine encrypts transfers leaving protected GPU memory. A conventional secure checkpoint then decrypts the arriving data in the CPU TEE and encrypts it again under a checkpoint key. This adds CPU cryptographic work to an already constrained transfer.[^1]

In the paper's setup, confidential-mode bandwidth drops from roughly 40 GB/s to 7.3 GB/s. Moving 80 GB at that rate alone takes about 11 seconds, before the extra checkpoint encryption. Pausing inference for the full operation therefore makes checkpoint creation a visible service interruption.[^1]

## Reuse the GPU's ciphertext

FLASH preserves the ciphertext that the copy engine already produced. A custom driver interface retrieves the encrypted pages with their initialization vectors (IVs) and authentication tags. The checkpoint stores these pages directly, removing the CPU decrypt-then-reencrypt cycle from the frequent checkpoint path.[^1]

The resulting image uses two key domains. GPU pages retain their device-to-host encryption under the source session key. CPU state and the source GPU key are protected under the checkpoint key. The stored metadata gives a recovery agent the context needed to authenticate and decrypt the original GPU pages. Data entering a destination GPU then follows that destination's protected transfer path.[^1]

This changes when cryptographic work happens. FLASH avoids redundant CPU encryption work each time it creates a checkpoint; recovery still has to reconstruct and decrypt the saved state. A shorter checkpoint pause should therefore be interpreted separately from recovery latency.[^1]

## Copy in the background, then capture the dirty delta

Keeping ciphertext reduces the cost per byte. FLASH also reduces the amount of data that must move while serving is paused. It first copies GPU memory while inference continues. Writes during that background copy can make saved pages stale, so FLASH must identify the pages that need copying again.[^1]

FLASH brings allocations under NVIDIA Unified Virtual Memory (UVM) control by interposing on allocation calls. It marks tracked pages read-only. A later write raises a fault that the driver records in a dirty bitmap before allowing the write to proceed. Tracking uses 2 MB regions, trading some overcounting for fewer fault-handling events than tracking individual 4 KB pages.[^1]

After background copying, FLASH pauses execution to copy the dirty delta and then resumes serving. This is the stop-and-copy phase. Its latency depends on the state modified during the tracking window, rather than the full GPU footprint. The mechanism operates below the LLM kernels and does not require offline analysis of their PTX code.[^1]

## Keep static data in the recovery image

Model weights usually stay unchanged after initialization. In the paper's static-allocation design, FLASH captures static state once and reuses it in later checkpoint images. Those pages remain write-protected, and a subsequent write promotes the affected region to dynamic state. Recovery still restores both static and dynamic data.[^1]

The released evaluation agent exposes `v3-static` for static classification. Its default identifies allocations using host-to-device transfer flags; a separate `--learn` option enables the learning path. These implementation choices matter when matching a run to the design described in the paper.[^2]

## Bind saved state to keys, page positions, and freshness

Confidentiality alone is insufficient when the host storing an image is untrusted. It could alter a page, put an authentic page in the wrong position, or present an old checkpoint. FLASH's security protocol addresses these as separate obligations.[^1]

Authentication tags protect encrypted page contents. An authenticated manifest records page positions and their cryptographic metadata, and its hash is bound to a TDX-signed freshness report. A trusted remote attestation service holds checkpoint keys and the latest freshness record. During recovery, the protocol checks the record before releasing the key to an accepted confidential virtual machine.[^1]

Attestation supplies evidence about the software loaded in that environment; the design still trusts that software to perform the checks correctly. It also trusts the CPU and GPU security mechanisms, the guest kernel and driver, and the remote service's state. The paper's analysis does not cover availability against a malicious host or hide checkpoint sizes, access patterns, and timing.[^1]

## What the H100 evaluation measures

The evaluation uses one 80 GB H100 in confidential computing mode, Intel TDX, and vLLM 0.8.5. It tests Llama-3.2-1B, Qwen-2.5-7B, and Llama-2-13B under short-context Chatbot and long-context Reasoning workloads. Checkpoint images are staged in DRAM-backed tmpfs.[^1]

The paper summarizes an average stop-and-copy latency of 1.2 seconds across FLASH and its FLASH-SC ablation, which omits static classification. It reports a 9.4-fold reduction relative to its PhoenixOS-based comparison, PhOS, and a 7.8-fold reduction relative to GCR at a one-minute checkpoint interval. The comparison systems are reimplemented data paths on the same confidential stack; the original published artifacts do not run unchanged on that platform.[^1]

These measurements establish the reported checkpoint pause in that setup. They do not imply that every inference request sees the same improvement. The paper also measures time to first token and time between tokens, and reports a less favorable high-concurrency Llama-1B Chatbot case. Serving impact depends on the workload and the interaction between tracking and the framework's synchronization points.[^1]

## Inspect the artifact and its evaluation record

The [FLASH repository](https://github.com/sept-usc/FLASH) contains the modified NVIDIA UVM driver, checkpoint and restore programs, and comparison benchmarks. Reproduction requires the documented H100 and TDX environment and pinned driver, CUDA, and vLLM versions. Integrating the paper's complete remote attestation and key-release service requires work beyond the released evaluation programs.[^2]

The [ATC artifact evaluation results](https://sysartifacts.github.io/atc2026/results) list FLASH with Artifacts Available, Artifacts Evaluated – Functional, and Results Reproduced badges. The evaluated artifact is preserved in [Zenodo](https://doi.org/10.5281/zenodo.23199897). These are the conference's recorded evaluation outcomes.[^3, 4]

:::analysis
FLASH connects two requirements that confidential AI services must consider together: protected state must remain recoverable, and recovery must retain the integrity and freshness checks that give the saved state meaning. The implementation shows how retaining existing ciphertext and tracking writes in the driver can shorten the checkpoint pause. For a deployment, the remaining checks include the exact software version, the recovery integration, and the trusted service that binds key release to the accepted checkpoint.
:::
