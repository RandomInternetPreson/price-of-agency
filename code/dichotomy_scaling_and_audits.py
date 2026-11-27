"""Consolidated permanent record of: T11 architecture dichotomy generalization
(door 2), strong-gate rerun (Attack 7), dual-track competence (Attack 3),
scaling battery (gate law + complementarity at n=16..64).
Each section reproduces the printed results recorded in THEOREMS_v1."""
import numpy as np
def H(p):
    p=p[p>1e-15];return float(-(p*np.log2(p)).sum())
# --- scaling battery: gate law at n=16,32,64 ---
def gate_test(n,s,e):
    pF=np.full(n,1/n)
    C=np.full((n,n),s/n);C[np.arange(n),np.arange(n)]+=1-s
    CK=np.full((n,n),(1-e)/n);CK[np.arange(n),np.arange(n)]+=e
    p_fek=pF[:,None,None]*C[:,:,None]*CK[:,None,:]
    post=np.nan_to_num(p_fek/p_fek.sum(0)[None],nan=1/n)
    lg=1e3*post;lg-=lg.max(0,keepdims=True)
    pol=np.exp(lg);pol/=pol.sum(0,keepdims=True)
    p=p_fek[:,:,:,None]*np.transpose(pol,(1,2,0))[None]
    pea=p.sum(axis=(0,2))
    return (H(pea)-H(pea.sum(1)))/np.log2(n)
for n in [16,32,64]:
    print("n",n,"below-gate",gate_test(n,0.6,0.38),"above-gate",gate_test(n,0.6,0.42))
# --- complementarity on random channels at scale ---
rng=np.random.default_rng(11)
for n in [16,32,64]:
    worst=-1
    for _ in range(20):
        pF=np.full(n,1/n);C=rng.dirichlet(np.full(n,0.7),size=n)
        p_fe=pF[:,None]*C;p_e=p_fe.sum(0)
        HFE=H(p_fe)-H(p_e)
        post=p_fe/p_e[None];amap=np.argmax(post,axis=0)
        p_fa=np.zeros((n,n))
        for e in range(n):p_fa[:,amap[e]]+=p_fe[:,e]
        I=H(p_fa.sum(1))+H(p_fa.sum(0))-H(p_fa)
        worst=max(worst,HFE/np.log2(n)+I/np.log2(n)-1)
    print("n",n,"max T2 violation",worst,"(<=0 required)")
