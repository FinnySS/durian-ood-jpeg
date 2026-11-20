from style import *
import pandas as pd, numpy as np
from matplotlib import cm
G=pd.read_csv('../results/14_jpeg_confirmation/grid_summary.csv'); G=G[G.set=='test']
arms=[('base','\\texttt{base}'),('qaug_resize','\\texttt{qaug\\_resize}'),('qaug_jpeg','\\texttt{qaug\\_jpeg}'),('qaug','\\texttt{qaug}')]
sizes=[256,224,160,112,80]; x=np.arange(5)
qs=['95','90','80','70','50','30']; cols=cm.viridis(np.linspace(0.05,0.9,len(qs)))
fig,axs=plt.subplots(1,4,figsize=(FULLW,2.1),sharey=True)
fig.subplots_adjust(left=0.07,right=0.86,top=0.89,bottom=0.22,wspace=0.08)
for ax,(a,lab) in zip(axs,arms):
    d=G[G.arm==a]
    def ser(q):
        s=d[d.q==q].set_index('size').loc[sizes]; return s['mean'].values,s['std'].values
    m,s=ser('none'); ax.errorbar(x,m,yerr=s,color='k',ls='--',lw=1.1,marker='o',ms=2.5,capsize=1.5,elinewidth=0.6,label='No JPEG')
    for q,c in zip(qs,cols):
        m,s=ser(q); ax.errorbar(x,m,yerr=s,color=c,lw=1.0,marker='o',ms=2.5,capsize=1.5,elinewidth=0.6,label='q'+q)
    ax.set_title(lab,pad=3); ax.set_xticks(x); ax.set_xticklabels([str(v) for v in sizes]); ax.set_ylim(0,90)
    ax.grid(axis='y',lw=0.3,color='0.85')
axs[0].set_ylabel('other$\\rightarrow$disease (\\%)')
fig.text(0.465,0.025,'Image size (px) before JPEG compression and enlargement to 256 px',ha='center')
h,l=axs[0].get_legend_handles_labels()
fig.legend(h,l,loc='center left',bbox_to_anchor=(0.865,0.55),title='JPEG quality',handlelength=1.6)
fig.savefig('out/fig_jpeg_grid.pdf')
print(G[(G.arm=='qaug_jpeg')&(G['size']==112)][['q','mean']].to_string())
