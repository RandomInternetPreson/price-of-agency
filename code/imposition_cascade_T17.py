"""T17: The Ledger of Imposition (Aaron's coinage).
Hierarchy: L levels, branching b. Exogenous variance sigma arrives at top.
Each agent absorbs up to capacity c_l (proportional to resources, declining
downward). CRUCIAL MECHANISM: unabsorbed variance is BROADCAST to each
subordinate (one manager's residual schedule chaos lands whole on every
worker's life, not split). Agency loss = imposed variance x elasticity(level),
elasticity rising toward the bottom (Ch 7 time-poverty multiplier).
All quantities exact (expectations). Tag: [EXACT within model class]."""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
L=4; b=4                      # levels: 0 exec(1),1 regional(4),2 managers(16),3 workers(64)
heads=np.array([b**l for l in range(L)])
sigma=100.0                   # incoming variance units at top
cap=np.array([60.0,20.0,6.0,1.0])    # absorption capacity per person ~ resources
elast=np.array([0.008,0.02,0.1,0.565])  # aim-loss per unit imposed (Ch7-shaped)
imposed=np.zeros(L); resid=sigma
for l in range(L):
    absorbed=min(resid,cap[l]); imposed[l]=resid  # variance each person at level l faces
    resid=resid-absorbed                          # residual broadcast to EACH child
agency_loss_pc=imposed*elast
agency_loss_total=agency_loss_pc*heads
print("level  heads  faced-variance/person  absorbed  agency-loss/person  agency-loss-total")
names=["executive","regional","manager","worker"]
for l in range(L):
    print(f"{names[l]:>9}  {heads[l]:>4}   {imposed[l]:>8.1f}            {min(imposed[l],cap[l]):>6.1f}     {agency_loss_pc[l]:>8.2f}          {agency_loss_total[l]:>8.1f}")
print(f"\nbottom vs top, per person: variance x{imposed[-1]/max(imposed[0]-cap[0],1e-9):.1f} of top's residual; agency loss x{agency_loss_pc[-1]/agency_loss_pc[0]:.0f}")
print(f"share of total agency loss borne by workers: {agency_loss_total[-1]/agency_loss_total.sum():.1%}")
fig,axes=plt.subplots(1,2,figsize=(14,6))
ax=axes[0]
y=[3,2,1,0]
for l in range(L):
    w=0.5+3.2*(imposed[l]-min(imposed[l],cap[l]))/sigma if l<L-1 else 0
    ax.barh(y[l],imposed[l],height=0.28,color='tab:red',alpha=0.75,label='variance faced, per person' if l==0 else None)
    ax.barh(y[l]-0.3,min(imposed[l],cap[l]),height=0.28,color='tab:green',alpha=0.75,label='absorbed (capacity ~ resources)' if l==0 else None)
    ax.text(imposed[l]+1.5,y[l],f"{names[l]}  (x{heads[l]})",va='center',fontsize=10)
    if l<L-1:
        ax.annotate("",xy=(imposed[l+1]*0.8,y[l+1]+0.35),xytext=(imposed[l]*0.5,y[l]-0.42),
                    arrowprops=dict(arrowstyle='-|>',lw=1+4*(imposed[l]-min(imposed[l],cap[l]))/sigma,color='0.3'))
ax.text(45,3.35,"residual is BROADCAST:\none level's unabsorbed chaos lands\nwhole on every person below",fontsize=9.5,color='0.25')
ax.set_yticks([]); ax.set_xlabel("variance units, per person"); ax.legend(loc='lower right',fontsize=9)
ax.set_title("The cascade: absorption shrinks downward,\nimposition survives downward")
ax=axes[1]
ax.bar(np.arange(L)-0.18,agency_loss_pc,width=0.36,color='tab:red',label='agency loss per person')
ax.bar(np.arange(L)+0.18,agency_loss_total,width=0.36,color='darkred',alpha=0.7,label='agency loss, level total')
ax.set_yscale('log'); ax.set_xticks(range(L)); ax.set_xticklabels(names)
ax.set_title("The double penalty: the bottom faces the most variance\nAND pays the highest price per unit (Ch 7 elasticity)")
ax.legend(fontsize=9); ax.grid(alpha=0.25,axis='y')
plt.suptitle("T17 — The Ledger of Imposition  [EXACT within model]: imposition narrows upward, multiplies downward",fontsize=12.5)
plt.tight_layout(rect=[0,0,1,0.92])
import os
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'imposition_cascade_T17.png'), dpi=150)
print("figure saved")
