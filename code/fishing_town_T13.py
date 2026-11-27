"""T13: fishing town. Exact famine probs via streak Markov chains.
Reconstructed as permanent record of the inline run (results in THEOREMS T13)."""
import numpy as np
from math import comb
n=4;N=9;s=0.5;e=0.6;hub=0.8;DAYS=90;ST=3
acc_edu=e+(1-e)/n; acc_cov=0.475
def famine(dist,st=ST,days=DAYS):
    pf=sum(p*q for p,q in dist)
    M=np.zeros((st+1,st+1))
    for k in range(st):M[k,0]=1-pf;M[k,k+1]=pf
    M[st,st]=1;v=np.zeros(st+1);v[0]=1
    for _ in range(days):v=v@M
    return v[st]
def mfail(p,Nn=N,need=5):
    return sum(comb(Nn,k)*p**k*(1-p)**(Nn-k) for k in range(0,need))
print("independent:",famine([(1.0,mfail(acc_edu))]))
print("hub:",famine([(1.0,1-hub)]))
print("shared tutor:",famine([(1.0,1-acc_edu)]))
for nh in range(N+1):
    ni=N-nh;d=[]
    for hr,ph in [(1,hub),(0,1-hub)]:
        need=5-(nh if hr else 0)
        pf=0.0 if need<=0 else (1.0 if need>ni else sum(comb(ni,k)*acc_edu**k*(1-acc_edu)**(ni-k) for k in range(need)))
        d.append((ph,pf))
    print("hub-followers",nh,famine(d))
for c in range(6):
    d=[(acc_edu,0.0),(1-acc_edu,(1-acc_cov)**c)]
    print("shared-tutor covert",c,"starvation",famine(d))
for c in [0,2,4]:
    print("private-tutor covert",c,"starvation",famine([(1.0,((1-acc_edu)**(N-c))*((1-acc_cov)**c))]))
for Nn in [3,5,7,9,11,13]:
    mf=sum(comb(Nn,k)*acc_edu**k*(1-acc_edu)**(Nn-k) for k in range(Nn//2+1))
    print("N",Nn,"famine",famine([(1.0,mf)]))
