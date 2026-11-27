"""S1: The living town. Fishers observe results and adapt; two conditions:
(A) infinite fish (payoff = on-fish indicator, no crowding penalty)
(B) finite fish (daily yield Y split among boats on the fish ground)
Start: established broadcast town (all favor the hub). Fishers learn by
exponential moving average of realized payoff for {follow hub, follow self},
softmax choice + small exploration. Tag: SIMULATION (seeded, many runs).
Scores Aaron's conversion prediction and the congestion mechanism."""
import numpy as np
rng=np.random.default_rng(20260730)
N=9; nG=4; own=0.7; hub=0.8; Y=12.0; DAYS=300; RUNS=400
alpha=0.15; temp=0.15; eps=0.05

def run(finite):
    frac_hub=np.zeros(DAYS); maj_hit=np.zeros(DAYS)
    for r in range(RUNS):
        ema=np.tile([1.0,0.2],(N,1))   # [hub, self] biased: established broadcast town
        for d in range(DAYS):
            F=rng.integers(nG)
            hub_call=F if rng.random()<hub else rng.integers(nG)
            picks=np.zeros(N,dtype=int); choice=np.zeros(N,dtype=int)
            for i in range(N):
                own_call=F if rng.random()<own else rng.integers(nG)
                p=np.exp(ema[i]/temp); p/=p.sum()
                c=rng.choice(2,p=p) if rng.random()>eps else rng.integers(2)
                choice[i]=c
                picks[i]=hub_call if c==0 else own_call
            on=(picks==F)
            if finite:
                k=on.sum()
                pay=np.where(on, Y/max(k,1), 0.0)
                pay=np.minimum(pay, Y)  # cap
                pay=pay/Y*3.0           # normalize scale for EMA stability
            else:
                pay=on.astype(float)
            for i in range(N):
                ema[i,choice[i]]=(1-alpha)*ema[i,choice[i]]+alpha*pay[i]
            frac_hub[d]+= (choice==0).mean()
            maj_hit[d]+= (on.sum()>=5)
    return frac_hub/RUNS, maj_hit/RUNS

fa,ma=run(False); fb,mb=run(True)
def famine_est(m): # approx famine prob from mean daily majority-hit in window
    q=1-m.mean(); 
    # exact streak chain with iid approx
    M=np.zeros((4,4))
    for k in range(3):M[k,0]=1-q;M[k,k+1]=q
    M[3,3]=1;v=np.zeros(4);v[0]=1
    for _ in range(90):v=v@M
    return v[3]
print("condition          hub-frac d0-10  hub-frac d290-300  maj-hit early  maj-hit late  famine early  famine late")
for tag,f,m in [("A infinite fish",fa,ma),("B finite fish  ",fb,mb)]:
    print(f"{tag}   {f[:10].mean():.3f}          {f[-10:].mean():.3f}             {m[:30].mean():.3f}         {m[-30:].mean():.3f}        {famine_est(m[:30]):.4f}       {famine_est(m[-30:]):.4f}")
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(13,4.6))
ax[0].plot(fa,label="A: infinite fish",color='tab:red'); ax[0].plot(fb,label="B: finite fish",color='tab:blue')
ax[0].set_xlabel("day"); ax[0].set_ylabel("fraction following the hub"); ax[0].legend(); ax[0].grid(alpha=0.3)
ax[0].set_title("Does the broadcast town convert?")
ax[1].plot(np.convolve(ma,np.ones(15)/15,'valid'),color='tab:red',label="A: majority-hit rate")
ax[1].plot(np.convolve(mb,np.ones(15)/15,'valid'),color='tab:blue',label="B: majority-hit rate")
ax[1].set_xlabel("day"); ax[1].legend(); ax[1].grid(alpha=0.3)
ax[1].set_title("Town accuracy as the structure evolves")
plt.suptitle("S1 The Living Town [SIMULATION, 400 runs]: observation alone vs observation + finite fish")
plt.tight_layout(); import os; plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'living_town_S1.png'), dpi=140)
print("saved figure")
