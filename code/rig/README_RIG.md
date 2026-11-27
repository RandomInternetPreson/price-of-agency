# The rig jobs — what to run on the 7×4090 box, and what came back already

Everything here was smoke-tested on CPU in the session container (PyTorch 2.14, Python 3.13).
The world module reproduces the printed T11′ floors to three decimals before anything else runs
(`python and_world.py` prints `match=True` four times; if it doesn't, stop).

## 0. One-time setup (Windows, PowerShell)

```powershell
cd P:\AND_repo\code\rig            # or wherever you unzipped
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install numpy matplotlib
pip install torch --index-url https://download.pytorch.org/whl/cu128   # pick the CUDA tag your driver supports from pytorch.org/get-started
python -c "import torch; print(torch.__version__, torch.cuda.device_count(), 'GPUs')"
python and_world.py                # must print match=True x4
python watcher_tournament.py --smoke   # ~1 min on one GPU; writes results_smoke/
```

The smoke run exercises every watcher (exact Bayesian, wrong-wiring Bayesian, three count
miners, a GRU and a transformer) on three tiny configs. If it finishes and prints `floors:` lines,
the pipeline is good.

## 1. The GPU job — neural-watcher tournament (the only genuinely GPU-shaped item)

```powershell
# core grid + regress arm: 72 + 40 configs, ~2-4 min each on a 4090 -> about 1 hour on 6 GPUs
python watcher_tournament.py --tiers A,R --gpus 1,2,3,4,5,6
python summarize_tournament.py results
```

- One worker process per GPU index in `--gpus`; GPU 0 is left alone by default (monitors). If the
  other agent is holding 4-6, use `--gpus 1,2,3` (it just takes twice as long).
- Resumable: kill it any time; rerun the same command and it skips finished configs
  (`results\shard_*.jsonl`). Per-config lifetime curves land in `results\curves\*.npz`.
- Logs: `results\shard_k.log`. Each config prints its exact floor first, then the learned floors.
- Hardening grid when you have an evening: `--tiers B` (n=6, m_S=64, watcher also sees outcomes;
  ~360 configs, ~2 h on 6 GPUs). `--tiers C` is everything else (small archs, h=0) — overnight.

What to bring back: `results\TOURNAMENT_SUMMARY.md` and the three `fig_*.png`. The summary already
answers the three questions in tables:
- **Q3 (clever weak watcher):** per config, exact floor vs the floors of watchers who do NOT know the
  structure; `inv exact` / `inv learned` columns say whether each kind of watcher reads the gated
  agent below the sage. The thing to look at: at m_S = 1024 does a transformer with a 512-day window
  still get the inversion, and how far above the exact floor does it sit (`gap`)?
- **Q5 (wiring hardened, learned side):** random wirings and the large habit space, for the learned
  watchers. (The exact side is already done below.)
- **Q7 (regress):** floors vs coin generator. If a learned watcher's floor falls as the LCG state
  shrinks (32 → 8 bits) while the fresh-coin Bayesian's does not, the watcher has acquired the
  generator; the gap between them is the price of assuming freshness.

## 2. CPU jobs — already run here; rerun to reproduce (seconds to a minute)

```powershell
python wiring_hardening_exact.py          # 3,372 exact floors, ~10 s on the Xeon; results_exact\wiring_hardening_SUMMARY.md
python divergence_model_small.py          # ~15 s; results_exact\divergence_small_RESULTS.md + figures\divergence_small_v0.png
```

Both outputs are committed under `results_exact\`; see `docs/RESULTS_2026-10-24_rig_v1.0.md` for the
readings offered for ruling. Nothing in the manuscript was touched.

## 3. If something breaks

- `CUDA out of memory`: only possible on tier B/C transformer configs at T=512; rerun with the same
  command — the failed config is logged with a traceback and skipped, the rest proceed.
- A worker dies silently: look at `results\shard_k.log`; relaunch the same command.
- Torch import fails under the venv but works outside: the CUDA wheel tag didn't match the driver;
  reinstall with the tag pytorch.org lists for your driver version.

## hank_port/ (2026-11-09) — the bandwidth block in a standard HANK
`pip install sequence-jacobian` (1.0.0). CPU only. `python test_nesting.py` (nesting check, ~4 min);
`python run_hank_v01.py` (steady-state predictions, ~12 min); `python hank_pigou.py` (externality, ~12 min);
`python run_hank_irf.py` (dynamics incl. nonlinear gate crossing, ~12 min). Results land in
`code/rig/results_exact/hank_*` and `figures/hank_*.png`. All text written utf-8.

### Stress objective #1 — sign-stability sweep (rig, CPU, ~3.5 h on 48 workers)
    cd code\rig\hank_port
    pip install sequence-jacobian
    $env:PYTHONUTF8=1
    python sweep_signs.py --fast --smoke                      # 2 draws, ~2 min, checks the install
    python sweep_signs.py --fast --draws 600 --workers 24     # ~40 min; resumable; rerun the same line to continue
    python summarize_sweep.py                                 # -> results_sweep_fast/SWEEP_SUMMARY.md, figures/hank_sweep_signs.png
Send back the results_sweep_fast folder (zip it). Fast mode: nA=80, nref=3, fixed-price arms only for P-A' (~1-1.5 min
per draw on one core). Do NOT run more than ~24 workers: the dense solves are memory-bandwidth bound and 48 workers
throttled every worker 5-10x on 2026-11-09. Full mode (no --fast, 2000 draws) is the overnight version.

### Stress objective #2 — certified upper bound on the plateau edge (rig, CPU-parallel)
    cd code\rig
    $env:PYTHONUTF8=1
    python plateau_edge_bnb.py 4 0.5 1e-3 3600 --workers 48 --incumbent 0.310536   # closes n=4 (expect ~1 h)
    python plateau_edge_bnb.py 5 0.5 1e-3 7200 --workers 48                        # n=5: bound, maybe closure
    python plateau_edge_bnb.py 6 0.5 1e-3 14400 --workers 48 --incumbent 0.334841  # n=6: certified upper bound after 4 h
Needs only numpy + scipy (the .venv_hank works). Results append to results_exact/plateau_edge_bnb_n*_s*.txt.
Rectangular branch-and-bound on the separable concave objective (Falk–Soland), with symmetry breaking and a
min-entropy bound; single-core n=3 closes in 4 s (edge = 1 − 1/log2 3 = 0.369070 exactly), n=4 reaches 0.411 in 5 min.

### Stress objective #4 — the town under lying masters and remembering seas (rig, GPUs 1–6, ~30 min)
In the torch venv from Nov 8 (needs only torch + numpy), from code\rig, one window per GPU:
    $env:PYTHONUTF8=1
    $env:CUDA_VISIBLE_DEVICES=1; python town_stress_T13.py --seasons 20000 --shard 0 --nshards 6
    $env:CUDA_VISIBLE_DEVICES=2; python town_stress_T13.py --seasons 20000 --shard 1 --nshards 6
    ... up to --shard 5 on GPU 6. Resumable. Then:  python summarize_town_stress.py
(`--smoke` on CPU reproduces the exact T13 numbers: 0.074 / 0.049 / 0.439 in ~90 s.) 9,720 configurations:
master accuracy × sea memory × reader-error persistence × shared blindness × master slump × misdirection, k = 0..9 each.

### Stress objective #6 — the acting → reading conjecture as a model (one GPU, ~10 min)
    $env:PYTHONUTF8=1
    $env:CUDA_VISIBLE_DEVICES=1; python living_town_skill.py --runs 2000 --days 600
    python summarize_living_town_skill.py
216 configurations (decay λ × recovery μ × hub accuracy × crowding strength × initial skill). CPU smoke: `--smoke` (15 s).
