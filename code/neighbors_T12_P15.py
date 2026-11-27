"""T12 + P15: neighbor coupling — B's ceiling & gate vs A's type; ceiling
erosion vs k rock neighbors (submodular bites)."""
import numpy as np
from itertools import product
n=4;s=0.5;log2n=np.log2(n);pF=np.full(n,1/n)
def H(p):
    p=p[p>1e-15];return float(-(p*np.log2(p)).sum())
def ch(f):
    C=np.full((n,n),(1-f)/n);C[np.arange(n),np.arange(n)]+=f;return C
C=ch(1-s);p_fe=pF[:,None]*C;q=(p_fe/p_fe.sum(0)[None]).T
def A_policy(kind):
    P=np.zeros((n,n))
    if kind=="sage":P[np.arange(n),np.arange(n)]=1
    elif kind=="rock":P=C.copy()
    elif kind=="covert":
        lam=1/(n*q.max())
        for f in range(n):
            for eA in range(n):
                r=np.clip((1/n-lam*q[eA])/(1-lam),0,None);r/=r.sum()
                P[f,:]+=C[f,eA]*(1-lam)*r;P[f,f]+=C[f,eA]*lam
    else:P[:,:]=1/n
    return P
for kind in ["absent","covert","rock","sage"]:
    PA=A_policy(kind)
    J=pF[:,None,None]*C[:,:,None]*PA[:,None,:]
    jf=J.reshape(n,-1)
    print(kind,"ceiling",(H(jf)-H(jf.sum(0)))/log2n)
for k in range(5):  # P15 rock-neighbor erosion
    joint=np.zeros([n]*(k+2))
    for f in range(n):
        for st in product(range(n),repeat=k+1):
            p=pF[f]*C[f,st[0]]
            for a in st[1:]:p*=C[f,a]
            joint[(f,)+st]=p
    jf=joint.reshape(n,-1)
    print("k",k,"ceiling",(H(jf)-H(jf.sum(0)))/log2n)
