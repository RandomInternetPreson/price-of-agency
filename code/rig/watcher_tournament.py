"""
watcher_tournament.py -- the neural-watcher tournament (Ch 15 §3: the clever
weak watcher / the wiring theorem hardened / the surveillance regress).

THE QUESTION. Theorem 11 / T11' score Vera against the STRONGEST watcher: an
exact Bayesian who knows the true wiring and habit space and updates perfectly.
Its floors are exact (and_world.exact_floors). Real watchers are pattern-miners
with wrong models. This tournament puts a zoo of weaker watchers on the same
behavioral streams and asks, per configuration:
  (Q3) how much watcher does the inversion cost? -- does a watcher who does NOT
       know the structure still read the gated agent below the sage, and how
       close does it get to the exact floor delta_inf;
  (Q5) does the dichotomy (gated: permanent inversion; additive: one-time-pad
       equality at h=3) survive on random wirings and large habit spaces
       (m_S up to 1024), for the exact watcher AND for the learned ones;
  (Q7) the regress: when the "fresh" coin is itself a pseudo-random generator
       with a hidden seed (lcg:k), can a watcher with enough capacity acquire
       the generator and collapse the floor? (iid = the book's assumption.)

SCORING. Every watcher W outputs a predictive distribution p_W(a | E_t, history)
at each step. Its reading of the agent is the log-loss in units of log2 n:
    delta_W(t) = E[ -log2 p_W(A_t | .) ] / log2 n.
For the exact Bayesian this equals E[H(pred)]/log2 n = the book's delta_A(t)
(checked and reported side by side). For a mis-specified watcher log-loss is the
only honest generalization: it can exceed 1 (worse than ignorance). The floor
estimate is the mean over the last quarter of the lifetime.

WATCHERS.
  bayes          exact posterior over S under the TRUE wiring (the book's watcher)
  bayes-wrong    exact posterior under the OTHER named wiring (gated<->additive):
                 the cleverly wrong watcher
  markov-k       in-context count-based miner, context = (E_t, last k (E,A)) k=0,1,2
  gru-s/gru-l    recurrent sequence models trained from scratch on fresh lifetimes
  tf-s/tf-l      causal transformers, same
Neural watchers never see S, U, or F at prediction time; obs=EA feeds them
(E_t, E_{t-1}, A_{t-1}); obs=EAF also feeds F_{t-1} (outcomes seen a day late,
the Ch 9 §4 "also sees outcomes" variant). Training data is unlimited (fresh
streams every step) so the only limit is capacity + optimization = acquisition.

USAGE (one process per GPU, resumable, results in JSONL + per-config curves):
  python watcher_tournament.py --smoke                      # 2-minute pipeline check
  python watcher_tournament.py --tiers A,R --gpus 1,2,3,4,5,6
  python watcher_tournament.py --tiers B --gpus 1,2,3,4,5,6 # hardening grid (hours)
  python summarize_tournament.py results/                   # tables + figures
Tiers: A core (n=4; lam/hand; gated/additive/random; m_S 8/1024; h 1-3; gru-l, tf-l)
       R regress (iid vs lcg:8/12/16/32 coins; T=512)
       B hardening (n=6, m_S=64, obs=EAF added)     C everything else (small archs, h=0)
"""
import argparse, hashlib, json, math, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import and_world as aw

# --------------------------------------------------------------------------
# configuration grid
# --------------------------------------------------------------------------
ARCH = {  # name: (kind, width, layers, steps, batch, lr)
    'gru-s': ('gru', 64, 1, 1500, 256, 2e-3),
    'gru-l': ('gru', 256, 2, 4000, 256, 1.5e-3),
    'tf-s': ('tf', 64, 2, 1500, 256, 1e-3),
    'tf-l': ('tf', 192, 4, 4000, 256, 7e-4),
}


def cfg_id(c):
    key = json.dumps(c, sort_keys=True)
    return hashlib.sha1(key.encode()).hexdigest()[:10]


def build_grid(tiers):
    cfgs = []

    def add(**kw):
        c = dict(n=4, s=0.5, policy='hand', wiring='gated', m_S=8, h=2, obs='EA',
                 gen='iid', arch='tf-l', T=256)
        c.update(kw)
        if 'T' not in kw:
            c['T'] = 512 if c['m_S'] >= 1024 else 256      # large habit spaces need longer lifetimes to converge
        c['id'] = cfg_id({k: v for k, v in c.items() if k != 'id'})
        if c['id'] not in {x['id'] for x in cfgs}:
            cfgs.append(c)

    if 'A' in tiers:
        for pol in ['lam', 'hand']:
            for wiring in ['gated', 'additive', 'random:1']:
                for m_S in [8, 1024]:
                    for h in [1, 2, 3]:
                        for arch in ['gru-l', 'tf-l']:
                            add(tier='A', policy=pol, wiring=wiring, m_S=m_S, h=h, arch=arch)
    if 'R' in tiers:
        for pol in ['lam', 'hand']:
            for wiring in ['gated', 'additive']:
                for gen in ['iid', 'lcg:8', 'lcg:12', 'lcg:16', 'lcg:32']:
                    for arch in ['gru-l', 'tf-l']:
                        add(tier='R', policy=pol, wiring=wiring, m_S=8, h=3, gen=gen, arch=arch, T=512)
    if 'B' in tiers:
        for n in [4, 6]:
            for pol in ['lam', 'hand']:
                for wiring in ['gated', 'additive', 'random:1']:
                    for m_S in [8, 64, 1024]:
                        for h in [1, 2, 3]:
                            for obs in ['EA', 'EAF']:
                                for arch in ['gru-l', 'tf-l']:
                                    add(tier='B', n=n, policy=pol, wiring=wiring, m_S=m_S, h=h, obs=obs, arch=arch)
    if 'C' in tiers:
        for n in [4, 6]:
            for pol in ['lam', 'hand']:
                for wiring in ['gated', 'additive', 'random:1', 'random:2']:
                    for m_S in [8, 64, 1024]:
                        for h in [0, 1, 2, 3]:
                            for obs in ['EA', 'EAF']:
                                for arch in ['gru-s', 'gru-l', 'tf-s', 'tf-l']:
                                    add(tier='C', n=n, policy=pol, wiring=wiring, m_S=m_S, h=h, obs=obs, arch=arch)
    if 'smoke' in tiers:
        add(tier='smoke', policy='hand', wiring='gated', m_S=8, h=2, arch='gru-s', T=64)
        add(tier='smoke', policy='hand', wiring='additive', m_S=8, h=3, arch='tf-s', T=64)
        add(tier='smoke', policy='lam', wiring='additive', m_S=8, h=3, gen='lcg:8', arch='tf-s', T=64)
    # tier-A/R configs already present are not re-added by B/C (dedup by id)
    return cfgs


# --------------------------------------------------------------------------
# watchers
# --------------------------------------------------------------------------
def bayes_curve(st, L, L_F, obs, device, torch, eps=0.0):
    """Exact Bayesian over S. Returns (logloss_curve, entropy_curve) in bits.
    eps > 0 hedges the predictive with eps*uniform and restarts the posterior when the
    model is refuted (zero likelihood) -- used for the mis-specified watchers."""
    E = torch.as_tensor(st['E'], device=device); A = torch.as_tensor(st['A'], device=device)
    F = torch.as_tensor(st['F'], device=device)
    Lt = torch.as_tensor(L, device=device, dtype=torch.float64)           # (S, e, a)
    LFt = torch.as_tensor(L_F, device=device, dtype=torch.float64)        # (S, f, e, a)
    B, T = E.shape; m_S = Lt.shape[0]
    post = torch.full((B, m_S), 1.0 / m_S, device=device, dtype=torch.float64)
    ll = torch.zeros(T, device=device, dtype=torch.float64); ent = torch.zeros_like(ll)
    for t in range(T):
        Le = Lt[:, E[:, t], :]                                             # (S, B, a)
        pred = torch.einsum('bs,sba->ba', post, Le)                        # (B, a)
        if eps > 0:
            pred = (1 - eps) * pred + eps / pred.shape[1]
        pa = pred.gather(1, A[:, t:t + 1]).squeeze(1).clamp_min(1e-300)
        ll[t] = -torch.log2(pa).mean()
        ent[t] = -(pred * torch.log2(pred.clamp_min(1e-300))).sum(1).mean()
        if obs == 'EAF':
            lik = LFt[:, F[:, t], E[:, t], A[:, t]].T                      # (B, S)
        else:
            lik = Le.gather(2, A[:, t].view(1, B, 1).expand(m_S, B, 1)).squeeze(2).T
        post = post * lik
        z = post.sum(1, keepdim=True)
        post = torch.where(z > 0, post / z.clamp_min(1e-300), torch.full_like(post, 1.0 / m_S))
    return ll.cpu().numpy(), ent.cpu().numpy()


def markov_curve(st, k, n, device, torch, alpha=0.5):
    """In-context count miner: context = (E_t, (E,A)_{t-1..t-k}); Laplace-alpha predictive."""
    E = torch.as_tensor(st['E'], device=device); A = torch.as_tensor(st['A'], device=device)
    B, T = E.shape
    nctx = n * (n * n) ** k
    counts = torch.zeros(B, nctx, n, device=device, dtype=torch.float32)
    ll = torch.zeros(T, device=device, dtype=torch.float64)
    ar = torch.arange(B, device=device)
    for t in range(T):
        ctx = E[:, t].clone()
        for j in range(1, k + 1):
            if t - j >= 0:
                ctx = ctx * (n * n) + (E[:, t - j] * n + A[:, t - j])
            else:
                ctx = ctx * (n * n)                                        # padding token 0
        c = counts[ar, ctx]                                                # (B, n)
        pred = (c + alpha) / (c.sum(1, keepdim=True) + n * alpha)
        pa = pred.gather(1, A[:, t:t + 1]).squeeze(1)
        ll[t] = -torch.log2(pa.double()).mean()
        counts[ar, ctx, A[:, t]] += 1.0
    return ll.cpu().numpy()


def make_model(kind, n, width, layers, T, obs, torch, nn):
    class Watcher(nn.Module):
        def __init__(s):
            super().__init__()
            s.kind = kind
            s.embE = nn.Embedding(n, width); s.embEp = nn.Embedding(n + 1, width)
            s.embAp = nn.Embedding(n + 1, width); s.embFp = nn.Embedding(n + 1, width)
            if kind == 'gru':
                s.core = nn.GRU(width, width, num_layers=layers, batch_first=True)
            else:
                s.pos = nn.Embedding(T, width)
                layer = nn.TransformerEncoderLayer(width, max(1, width // 32), 4 * width, dropout=0.0,
                                                   batch_first=True, norm_first=True, activation='gelu')
                s.core = nn.TransformerEncoder(layer, layers, enable_nested_tensor=False)
                s.register_buffer('mask', torch.triu(torch.full((T, T), float('-inf')), 1))
            s.out = nn.Linear(width, n)

        def forward(s, E, Ap, Ep, Fp):
            x = s.embE(E) + s.embAp(Ap) + s.embEp(Ep) + (s.embFp(Fp) if obs == 'EAF' else 0)
            if s.kind == 'gru':
                y, _ = s.core(x)
            else:
                Tn = x.shape[1]
                x = x + s.pos(torch.arange(Tn, device=x.device))[None]
                y = s.core(x, mask=s.mask[:Tn, :Tn], is_causal=True)
            return s.out(y)
    return Watcher()


def shifted_inputs(st, n, device, torch):
    E = torch.as_tensor(st['E'], device=device); A = torch.as_tensor(st['A'], device=device)
    F = torch.as_tensor(st['F'], device=device)
    pad = torch.full_like(E[:, :1], n)                                     # token n = "no history"
    Ap = torch.cat([pad, A[:, :-1]], 1); Ep = torch.cat([pad, E[:, :-1]], 1); Fp = torch.cat([pad, F[:, :-1]], 1)
    return E, Ap, Ep, Fp, A


def train_neural(cfg, world, G, eval_st, device, torch, nn, smoke=False, log=print):
    kind, width, layers, steps, batch, lr = ARCH[cfg['arch']]
    if smoke:
        steps, batch = 60, 32
    n, T, m_S, m_U = cfg['n'], cfg['T'], cfg['m_S'], 2 ** cfg['h']
    torch.manual_seed(int(cfg['id'], 16) % (2 ** 31))
    rng = np.random.default_rng(int(cfg['id'], 16) % (2 ** 31) + 1)
    model = make_model(kind, n, width, layers, T, cfg['obs'], torch, nn).to(device)
    nparams = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.05)
    lossf = nn.CrossEntropyLoss()
    hist = []
    t0 = time.time()
    for it in range(steps):
        st = aw.sample_streams(rng, world, G, m_S, m_U, batch, T, cfg['gen'])
        E, Ap, Ep, Fp, A = shifted_inputs(st, n, device, torch)
        logits = model(E, Ap, Ep, Fp)
        loss = lossf(logits.reshape(-1, n), A.reshape(-1))
        opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step()
        if it % max(1, steps // 20) == 0 or it == steps - 1:
            hist.append((it, loss.item() / math.log(2) / math.log2(n)))
            if it % max(1, steps // 5) == 0:
                log(f"    [{cfg['arch']}] step {it:5d}/{steps} train delta_W={hist[-1][1]:.4f}  ({time.time() - t0:.0f}s)")
    model.eval()
    with torch.no_grad():
        E, Ap, Ep, Fp, A = shifted_inputs(eval_st, n, device, torch)
        ll = []
        for i in range(0, E.shape[0], 512):
            logits = model(E[i:i + 512], Ap[i:i + 512], Ep[i:i + 512], Fp[i:i + 512])
            lp = torch.log_softmax(logits.double(), -1)
            ll.append(-lp.gather(2, A[i:i + 512, :, None]).squeeze(2) / math.log(2))
        ll = torch.cat(ll, 0).mean(0).cpu().numpy()                        # (T,) bits
        acc = None
    return ll, dict(params=nparams, steps=steps, batch=batch, train_curve=hist, train_seconds=time.time() - t0)


# --------------------------------------------------------------------------
# one configuration
# --------------------------------------------------------------------------
def run_config(cfg, device, outdir, smoke=False, log=print):
    import torch, torch.nn as nn
    torch.backends.cuda.matmul.allow_tf32 = True; torch.backends.cudnn.allow_tf32 = True
    n, s, m_S, h, T = cfg['n'], cfg['s'], cfg['m_S'], cfg['h'], cfg['T']
    m_U = 2 ** h
    world = aw.World(n, s)
    pol = world.policy(cfg['policy'])
    aim, dA_E, wall = world.stats(pol)
    G = aw.action_table(pol, aw.quantile_map(cfg['wiring'], m_S, m_U), m_S, m_U)
    L_F, L = aw.lik_tables(G, world)
    d0, dinf = aw.exact_floors(L, world)
    log(f"  cfg {cfg['id']} {cfg['policy']}/{cfg['wiring']} m_S={m_S} h={h} obs={cfg['obs']} gen={cfg['gen']} "
        f"arch={cfg['arch']}  | sage={world.sage:.3f} wall={wall:.3f} d0={d0:.3f} dinf(exact)={dinf:.3f}")

    B_eval = 128 if smoke else 2048
    rng_eval = np.random.default_rng(777)
    eval_st = aw.sample_streams(rng_eval, world, G, m_S, m_U, B_eval, T, cfg['gen'])
    log2n = world.log2n
    curves, floors = {}, {}

    def floor_of(curve, frac=4):
        return float(np.mean(curve[-max(1, T // frac):]))

    # exact Bayesian, true wiring
    ll, ent = bayes_curve(eval_st, L, L_F, cfg['obs'], device, torch)
    curves['bayes'] = ll / log2n; curves['bayes_entropy'] = ent / log2n
    # cleverly wrong Bayesian: other named wiring (only meaningful for gated/additive)
    other = {'gated': 'additive', 'additive': 'gated'}.get(cfg['wiring'], 'gated')
    Gw = aw.action_table(pol, aw.quantile_map(other, m_S, m_U), m_S, m_U)
    L_Fw, Lw = aw.lik_tables(Gw, world)
    llw, _ = bayes_curve(eval_st, Lw, L_Fw, cfg['obs'], device, torch, eps=1e-3)
    curves['bayes-wrong'] = llw / log2n
    # pattern miners
    for k in [0, 1, 2]:
        if n * (n * n) ** k * n * B_eval > 4e8:      # memory guard
            continue
        curves[f'markov-{k}'] = markov_curve(eval_st, k, n, device, torch) / log2n
    # the neural watcher of this config
    ll, info = train_neural(cfg, world, G, eval_st, device, torch, nn, smoke=smoke, log=log)
    curves[cfg['arch']] = ll / log2n
    for k_, v in curves.items():
        floors[k_] = floor_of(v)

    rec = dict(cfg, sage=world.sage, aim=aim, dA_E=dA_E, wall=wall, d0=d0, dinf_exact=dinf,
               floors=floors, first_day={k_: float(v[0]) for k_, v in curves.items()},
               neural=info, device=str(device), B_eval=B_eval,
               inverted_exact=bool(dinf < world.sage),
               inverted_neural=bool(floors[cfg['arch']] < world.sage),
               gap_neural_minus_exact=float(floors[cfg['arch']] - dinf),
               bayes_consistency=float(abs(floors['bayes'] - floors['bayes_entropy'])),
               bayes_converged=float(floor_of(curves['bayes'], 8) - dinf),   # ~0 when the exact watcher has reached its floor by end of life
               floors_last8th={k_: floor_of(v, 8) for k_, v in curves.items()})
    np.savez_compressed(os.path.join(outdir, 'curves', f"{cfg['id']}.npz"), **curves)
    log(f"    floors: exact {dinf:.3f} | bayes(mc) {floors['bayes']:.3f} | wrong {floors['bayes-wrong']:.3f} | "
        + " | ".join(f"{k_} {floors[k_]:.3f}" for k_ in floors if k_.startswith('markov'))
        + f" | {cfg['arch']} {floors[cfg['arch']]:.3f}   inverted: exact {rec['inverted_exact']} neural {rec['inverted_neural']}")
    return rec


# --------------------------------------------------------------------------
# worker / launcher
# --------------------------------------------------------------------------
def done_ids(outdir):
    ids = set()
    for fn in os.listdir(outdir):
        if fn.endswith('.jsonl'):
            with open(os.path.join(outdir, fn)) as f:
                for line in f:
                    try:
                        ids.add(json.loads(line)['id'])
                    except Exception:
                        pass
    return ids


def worker(args):
    import torch
    device = torch.device(args.device if args.device else ('cuda' if torch.cuda.is_available() else 'cpu'))
    cfgs = build_grid(args.tiers.split(','))
    mine = [c for i, c in enumerate(cfgs) if i % args.nshards == args.shard]
    done = done_ids(args.out)
    todo = [c for c in mine if c['id'] not in done]
    logf = open(os.path.join(args.out, f'shard_{args.shard}.log'), 'a')

    def log(msg):
        print(msg, flush=True); logf.write(msg + '\n'); logf.flush()
    log(f"worker shard {args.shard}/{args.nshards} on {device}: {len(todo)} configs to do ({len(mine) - len(todo)} already done)")
    outf = open(os.path.join(args.out, f'shard_{args.shard}.jsonl'), 'a')
    for i, cfg in enumerate(todo):
        t0 = time.time()
        try:
            rec = run_config(cfg, device, args.out, smoke=args.smoke, log=log)
            rec['seconds'] = time.time() - t0
            outf.write(json.dumps(rec) + '\n'); outf.flush()
            log(f"  done {i + 1}/{len(todo)} in {rec['seconds']:.0f}s")
        except Exception as ex:
            import traceback
            log(f"  FAILED cfg {cfg['id']}: {ex}\n{traceback.format_exc()}")
    log("worker finished")


def launch(args):
    gpus = [g.strip() for g in args.gpus.split(',') if g.strip()]
    os.makedirs(os.path.join(args.out, 'curves'), exist_ok=True)
    cfgs = build_grid(args.tiers.split(','))
    done = done_ids(args.out)
    print(f"grid: {len(cfgs)} configs for tiers {args.tiers}; {len(done & {c['id'] for c in cfgs})} already done; "
          f"launching {len(gpus)} workers on GPUs {gpus}")
    procs = []
    for j, g in enumerate(gpus):
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=g)
        cmd = [sys.executable, os.path.abspath(__file__), '--worker', '--shard', str(j), '--nshards', str(len(gpus)),
               '--tiers', args.tiers, '--out', args.out, '--device', 'cuda:0']
        procs.append(subprocess.Popen(cmd, env=env))
        time.sleep(1.0)
    for p in procs:
        p.wait()
    print("all workers finished; now run:  python summarize_tournament.py", args.out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--tiers', default='A,R')
    ap.add_argument('--gpus', default='1,2,3,4,5,6', help='CUDA device indices, one worker each (GPU 0 drives the monitors)')
    ap.add_argument('--out', default=os.path.join(HERE, 'results'))
    ap.add_argument('--worker', action='store_true'); ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--nshards', type=int, default=1); ap.add_argument('--device', default=None)
    ap.add_argument('--smoke', action='store_true', help='tiny grid, tiny budgets, any device: pipeline check')
    args = ap.parse_args()
    if args.smoke:
        args.tiers = 'smoke'; args.out = os.path.join(HERE, 'results_smoke')
        os.makedirs(os.path.join(args.out, 'curves'), exist_ok=True)
        args.shard, args.nshards = 0, 1
        worker(args)
    elif args.worker:
        os.makedirs(os.path.join(args.out, 'curves'), exist_ok=True)
        worker(args)
    else:
        launch(args)
