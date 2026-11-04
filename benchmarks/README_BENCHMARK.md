# Running FLASH's benchmarks

Complete [README_SETUP.md](../modified_driver_code/README_SETUP.md) first, including step 7:
`verify_driver.sh` must report every check as `PASS`. All benchmarks run inside
the guest VM. Clone this repository as `artifact_flash`, as shown in the
[top-level README](../README.md). In each terminal, set the repository root
from your checkout before using the commands below:

```bash
cd /path/to/artifact_flash
export FLASH_ROOT="$PWD"
```

`/path/to/artifact_flash` is your local checkout path. All paths below use
`FLASH_ROOT`, so build steps do not depend on the previous working directory.

## Build prerequisites

FLASH's checkpoint code and both baselines link against OpenSSL for AES-GCM,
so install the headers once before building anything under `benchmarks/`:

```bash
sudo apt-get install -y libssl-dev
```

Without it every `make` below stops at
`openssl/evp.h: No such file or directory`.

## System settings

Apply these inside the guest after every boot, before running any benchmark.
None of them persist across a reboot, and skipping any of them changes the
results without an error or warning.

### Transparent huge pages

```bash
echo always | sudo tee /sys/kernel/mm/transparent_hugepage/shmem_enabled
echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
```

Check that both report `[always]`:

```bash
cat /sys/kernel/mm/transparent_hugepage/shmem_enabled
cat /sys/kernel/mm/transparent_hugepage/enabled
```

The benchmarks move tens of gigabytes through host memory. With the default
4 KB pages, the first touch of each page in a TDX guest is expensive, and 2 MB
pages cut the number of those operations by 512x.

### GPU clocks and confidential computing ready state

```bash
sudo nvidia-smi -lgc 1980
sudo nvidia-smi -lmc 2619

sudo nvidia-smi conf-compute -srs 1
```

When idle, the H100 drops to about 17% of its peak clock and does not ramp up
fast enough for short transfers, which lowers measured bandwidth by roughly
40%. Locking the clocks removes that. The last command marks the GPU ready to
accept work in confidential computing mode.

`nvidia-persistenced` must already be running with `--uvm-persistence-mode`:

```bash
ps aux | grep [n]vidia-persistenced     # expect --uvm-persistence-mode
```

That is a one-time change to the systemd unit, not a per-boot command; see
"UVM persistence mode" in step 2 of
[README_SETUP.md](../modified_driver_code/README_SETUP.md) if the flag is
`--no-persistence-mode`.

---

## Table 1

### Build

```bash
make -C "$FLASH_ROOT/benchmarks/table1_bandwidth"
```

### Run

Run both binaries once in the TD (confidential computing on) and once in a
legacy VM (confidential computing off):

```bash
(cd "$FLASH_ROOT/benchmarks/table1_bandwidth" &&
  ./memory_transfer_benchmark_sync 2>&1 | tee table1_sync.log)
(cd "$FLASH_ROOT/benchmarks/table1_bandwidth" &&
  ./memory_transfer_benchmark_async 2>&1 | tee table1_async.log)
```

---

## Generating Figures 3, 6, 7 and Table 4

These results come from the same experiment: serving LLM inference with
vLLM while each system (PhoS, GCR, FLASH-SC, FLASH) takes periodic
checkpoints. Each run produces the data for all four:

- **Figure 3:** dirty data rate
- **Figure 6:** concurrent-copy and stop-and-copy latency
- **Figure 7:** dirty memory size in the concurrent-copy phase
- **Table 4:** ratio of concurrent-copy time to total tracking time

### Build

```bash
make -C "$FLASH_ROOT/benchmarks/flash"
make -C "$FLASH_ROOT/benchmarks/phos_emul"
make -C "$FLASH_ROOT/benchmarks/gcr_emul"
make -C "$FLASH_ROOT/benchmarks/prealloc"
```

### Preallocate checkpoint buffers

Set `FLASH_SHM_SIZE` to your tmpfs limit (e.g. `200G`), and set the buffer
variables below to capacities in GiB that fit the selected workload and guest.
Leave room for image metadata. The static image must fit the model's weights;
PhoS needs both base and delta images to fit the full allocation footprint.

**Capacity:** 80 GiB staging + two 90 GiB images + 17 GiB static data consume
277 GiB, exceeding the original 200 GiB tmpfs. Prepare one system at a time;
size its buffers to the workload or add guest RAM and increase tmpfs. The
workload and OS also need RAM. A fresh guest boot clears previous tmpfs
buffers; reapply the per-boot settings above. Preallocation overwrites images
at the named paths, so preserve any images you need first.

```bash
: "${FLASH_SHM_SIZE:?Set the tmpfs limit, with sufficient guest RAM}"
sudo mount -o "remount,size=$FLASH_SHM_SIZE,huge=always" /dev/shm
df -h /dev/shm
free -h
```

For FLASH with static classification, prepare all four buffers:

```bash
: "${FLASH_STAGING_GB:?Set staging capacity in GiB}"
: "${FLASH_BASE_GB:?Set base image capacity in GiB}"
: "${FLASH_DELTA_GB:?Set delta image capacity in GiB}"
: "${FLASH_STATIC_GB:?Set static image capacity in GiB}"
sudo "$FLASH_ROOT/benchmarks/prealloc/ckpt_prealloc" \
  --gpu-size-gb "$FLASH_STAGING_GB" \
  --file "/dev/shm/ckpt_base.img:$FLASH_BASE_GB" \
  --file "/dev/shm/ckpt_delta.img:$FLASH_DELTA_GB" \
  --file "/dev/shm/ckpt_static.img:$FLASH_STATIC_GB"
```

For `v3`, omit the static image option. For PhoS and GCR, omit
`--gpu-size-gb` and the static image option: PhoS uses base and delta images;
GCR uses only the base image. Preallocation ends with `=== done ===`. FLASH's
delta can grow if its initial capacity is too small, adding first-touch costs
during the measured run.

The FLASH commands below use `--no-prealloc` after this manual preparation:
the agent's automatic preparation expects `./ckpt_prealloc`, whereas the
Makefile builds that utility in `benchmarks/prealloc/`.

### Set up the Python environment

```bash
python3 -m venv "$FLASH_ROOT/.venv"
source "$FLASH_ROOT/.venv/bin/activate"
python -m pip install -r "$FLASH_ROOT/benchmarks/requirements.txt" \
  --extra-index-url https://download.pytorch.org/whl/cu124
```

The requirements pin vLLM 0.8.5 and PyTorch 2.6.0 with CUDA 12.4. The extra
package index supplies the pinned `+cu124` PyTorch wheels; see the
[official PyTorch 2.6.0 installation commands](https://docs.pytorch.org/get-started/previous-versions/#v260).

### Download the models and dataset

The Llama models require Hugging Face access approval. Request access to the
model repositories and authenticate before downloading:

```bash
hf auth login
bash "$FLASH_ROOT/benchmarks/download.sh"
```

Models go to `~/huggingface/`, and ShareGPT goes to `~/`, where
`bench_inference_vllm_async.py` searches for it. To download only the assets
for the Llama-3.2-1B examples below, use
`bash "$FLASH_ROOT/benchmarks/download.sh" sharegpt llama1b`.

### Model and application configurations

Flags for `bench_inference_vllm_async.py` (paper Table 2). Every run also uses
`--dataset sharegpt --ignore-eos --gpu-memory-utilization 0.85 --seed 0`.
Output tokens set both `--min-tokens` and `--max-tokens`.

| Application | Model | `--model` | Output tokens | `--max-concurrent` | `--rate` | `--max-model-len` |
|---|---|---|---|---|---|---|
| Chatbot (Short) | Llama-3.2-1B | `~/huggingface/Llama-3.2-1B-Instruct` | 512 | 512 | 30.0 | 4096 |
| Chatbot (Short) | Qwen-2.5-7B | `~/huggingface/Qwen2.5-7B-Instruct` | 512 | 256 | 20.0 | 4096 |
| Chatbot (Short) | Llama-2-13B | `~/huggingface/Llama-2-13b-chat-hf` | 512 | 64 | 5.0 | 4096 |
| Reasoning (Long) | Llama-3.2-1B | `~/huggingface/Llama-3.2-1B-Instruct` | 8192 | 200 | 1.0 | 16384 |
| Reasoning (Long) | Qwen-2.5-7B | `~/huggingface/Qwen2.5-7B-Instruct` | 8192 | 64 | 0.5 | 10000 |
| Reasoning (Long) | Llama-2-13B | `~/huggingface/Llama-2-13b-chat-hf` | 4096 | 32 | 0.5 | 4096 |

Checkpoint interval (1, 3 or 5 minutes):

| Interval | FLASH `ckpt_agent` | PhoS | GCR |
|---|---|---|---|
| 1 min | `--interval 60` | `PHOS_CKPT_INTERVAL_MS=60000` | `GCR_CKPT_INTERVAL_MS=60000` |
| 3 min | `--interval 180` | `PHOS_CKPT_INTERVAL_MS=180000` | `GCR_CKPT_INTERVAL_MS=180000` |
| 5 min | `--interval 300` | `PHOS_CKPT_INTERVAL_MS=300000` | `GCR_CKPT_INTERVAL_MS=300000` |

### Run FLASH

Run one system at a time. These examples use the Llama-3.2-1B short-output
configuration. The 1,200-second submission window leaves time for the initial
400-second delay and periodic checkpoints. `--rounds 10` is an upper limit:
the run can produce fewer checkpoints if the application exits first. Extend
the workload duration when using longer intervals or slower configurations.

#### Terminal 1: start the workload

Set `FLASH_ROOT` as above and activate the virtual environment in this terminal.

```bash
source "$FLASH_ROOT/.venv/bin/activate"
mkdir -p "$FLASH_ROOT/benchmarks/results"
cd "$FLASH_ROOT/benchmarks/flash"
LD_PRELOAD="$FLASH_ROOT/benchmarks/flash/libckpt_vllm.so" \
  python "$FLASH_ROOT/benchmarks/flash/bench_inference_vllm_async.py" \
  --model "$HOME/huggingface/Llama-3.2-1B-Instruct" \
  --dataset sharegpt --rate 30 --duration 1200 --ignore-eos \
  --min-tokens 512 --max-tokens 512 --max-concurrent 512 \
  --max-model-len 4096 --gpu-memory-utilization 0.85 --seed 0 \
  --out-jsonl "$FLASH_ROOT/benchmarks/results/flash_requests.jsonl" \
  2>&1 | tee "$FLASH_ROOT/benchmarks/results/flash_workload.log"
```

#### Terminal 2: start the checkpoint agent

Set `FLASH_ROOT` in this terminal too. Use `v3-static` for FLASH with static
classification. The agent must run from `benchmarks/flash/` so it can invoke
`./ckpt_core`.

```bash
mkdir -p "$FLASH_ROOT/benchmarks/results"
cd "$FLASH_ROOT/benchmarks/flash"
sudo ./ckpt_agent --mode v3-static --no-prealloc \
  --delay 400 --interval 60 --rounds 10 \
  2>&1 | tee "$FLASH_ROOT/benchmarks/results/flash_checkpoint.log"
```

To measure FLASH without static classification, prepare the `v3` buffers and
repeat the workload in a new process, replacing `--mode v3-static` with
`--mode v3`. Use distinct result filenames for each run. Do not run both
agents against the same workload.

### Run the PhoenixOS emulation (PhoS)

Prepare both base and delta buffers for PhoS, activate the environment, and
run the same workload with its interception library. The emulation triggers
checkpoints internally; do not launch the FLASH checkpoint agent.

```bash
source "$FLASH_ROOT/.venv/bin/activate"
mkdir -p "$FLASH_ROOT/benchmarks/results"
cd "$FLASH_ROOT/benchmarks/flash"
PHOS_SCAN_KERNELS=1 PHOS_CKPT_DELAY=400 \
  PHOS_CKPT_INTERVAL_MS=60000 PHOS_CKPT_ROUNDS=10 PHOS_STAGING_MB=4096 \
  LD_PRELOAD="$FLASH_ROOT/benchmarks/phos_emul/libphos_intercept.so" \
  python "$FLASH_ROOT/benchmarks/flash/bench_inference_vllm_async.py" \
  --model "$HOME/huggingface/Llama-3.2-1B-Instruct" \
  --dataset sharegpt --rate 30 --duration 1200 --ignore-eos \
  --min-tokens 512 --max-tokens 512 --max-concurrent 512 \
  --max-model-len 4096 --gpu-memory-utilization 0.85 --seed 0 \
  --out-jsonl "$FLASH_ROOT/benchmarks/results/phos_requests.jsonl" \
  2>&1 | tee "$FLASH_ROOT/benchmarks/results/phos.log"
```

### Run the GCR emulation

Prepare GCR's base buffer, then run:

```bash
source "$FLASH_ROOT/.venv/bin/activate"
mkdir -p "$FLASH_ROOT/benchmarks/results"
cd "$FLASH_ROOT/benchmarks/flash"
GCR_CKPT_DELAY=400 GCR_CKPT_INTERVAL_MS=60000 GCR_CKPT_ROUNDS=10 \
  CKPT_STAGING_MB=4096 \
  LD_PRELOAD="$FLASH_ROOT/benchmarks/gcr_emul/libgcr_intercept.so" \
  python "$FLASH_ROOT/benchmarks/flash/bench_inference_vllm_async.py" \
  --model "$HOME/huggingface/Llama-3.2-1B-Instruct" \
  --dataset sharegpt --rate 30 --duration 1200 --ignore-eos \
  --min-tokens 512 --max-tokens 512 --max-concurrent 512 \
  --max-model-len 4096 --gpu-memory-utilization 0.85 --seed 0 \
  --out-jsonl "$FLASH_ROOT/benchmarks/results/gcr_requests.jsonl" \
  2>&1 | tee "$FLASH_ROOT/benchmarks/results/gcr.log"
```

### Read the outputs

The workload prints completed requests, throughput, time to first token, and
inter-token latency. `--out-jsonl` saves per-request measurements under
`benchmarks/results/`. The checkpoint logs report phase timings and dirty
sizes; the FLASH agent also prints a CSV summary at the end. Its final
`Restore Emulation` section is an estimated transfer time, not a measured
end-to-end restore benchmark.

The default FLASH images are `/dev/shm/ckpt_base.img`,
`/dev/shm/ckpt_delta.img`, and, in `v3-static` mode,
`/dev/shm/ckpt_static.img`. They are overwritten by later checkpoints and
removed when the guest reboots. Copy any images needed for further analysis
before preparing another run.
