"""T14: correlation floor. rho = prob of common tutor shock per day."""
import numpy as np
from math import comb
acc=0.7;acc_cov=0.475;ST=3;DAYS=90
def famine(pf,st=ST,days=DAYS):
    M=np.zeros((st+1,st+1))
    for k in range(st):M[k,0]=1-pf;M[k,k+1]=pf
    M[st,st]=1;v=np.zeros(st+1);v[0]=1
    for _ in range(days):v=v@M
    return v[st]
def mfail(Nn,p=acc):
    return sum(comb(Nn,k)*p**k*(1-p)**(Nn-k) for k in range(Nn//2+1))
for rho in [0.0,0.05,0.15,0.30]:
    for Nn in [9,31]:
        print("rho",rho,"N",Nn,"famine",famine(rho*(1-acc)+(1-rho)*mfail(Nn)))
    print("  floor:",famine(rho*(1-acc)))
for c in [0,2,4]:  # wildcard starvation floors at any rho: rho*(1-acc)*(1-acc_cov)^c
    print("wildcards",c,"starvation floor factor",(1-acc_cov)**c)
