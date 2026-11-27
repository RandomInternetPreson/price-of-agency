"""T16: iterative-time model — T sequential glimpses; time gate; P8 shape."""
import numpy as np
from itertools import product
n=4;s=0.5;g=0.35;log2n=np.log2(n);pF=np.full(n,1/n)
def H(p):
    p=p[p>1e-15];return float(-(p*np.log2(p)).sum())
def ch(f):
    C=np.full((n,n),(1-f)/n);C[np.arange(n),np.arange(n)]+=f;return C
C_E=ch(1-s);C_G=ch(g);p_fe=pF[:,None]*C_E
for T in range(7):
    pea=np.zeros((n,n));acc=0.0
    for e in range(n):
        for gs in product(range(n),repeat=T):
            wj=p_fe[:,e].copy()
            for gg in gs:wj=wj*C_G[:,gg]
            if wj.sum()<1e-15:continue
            a=int(np.argmax(wj));pea[e,a]+=wj.sum();acc+=wj[a]
    print("T",T,"delta_A",(H(pea)-H(pea.sum(1)))/log2n,"acc",acc)
