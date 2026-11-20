from style import *
import json, numpy as np
Q=json.load(open('./quality.json'))
BLUE='#4C72B0'; ORANGE='#DD8452'; GREEN='#2E8B57'
xy=lambda k: np.array(Q[k]).T
fig,axs=plt.subplots(1,2,figsize=(TEXTW,1.85),sharey=True)
fig.subplots_adjust(left=0.1,right=0.99,top=0.84,bottom=0.21,wspace=0.08)
a,b=axs
x,y=xy('a_disease'); a.plot(x,y,color=BLUE,lw=1.3,label='Disease')
x,y=xy('a_other'); a.plot(x,y,color=ORANGE,lw=1.3,ls='--',label='\\texttt{other}')
lab={'80':'80','112':'112','160':'160','224':'224','original':'Orig.'}
for k,v in Q['vlines'].items():
    a.axvline(v,color='0.45',ls=':',lw=0.8); a.text(v,1.03,lab[k],ha='center',va='bottom',fontsize=8.5,transform=a.get_xaxis_transform())
a.legend(loc='upper left',bbox_to_anchor=(0.0,0.98),handlelength=1.8,frameon=True,facecolor='white',edgecolor='none',framealpha=1,borderpad=0.3)
a.text(-0.2,1.13,'(a)',transform=a.transAxes,fontweight='bold')
x,y=xy('b_disease'); b.plot(x,y,color=BLUE,lw=1.3,label='Disease')
x,y=xy('b_other_orig'); b.plot(x,y,color=ORANGE,lw=1.3,ls='--',label='\\texttt{other}, original')
x,y=xy('b_other_matched'); b.plot(x,y,color=GREEN,lw=1.3,ls='-.',label='\\texttt{other}, matched')
b.legend(loc='upper left',handlelength=1.8)
b.text(-0.06,1.13,'(b)',transform=b.transAxes,fontweight='bold')
for ax in axs:
    ax.set_xlim(0.27,1.02); ax.set_ylim(0,1.02); ax.set_xticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    ax.set_xlabel('Effective resolution')
a.set_ylabel('Cumulative fraction')
fig.savefig('out/fig_quality_by_source.pdf')
