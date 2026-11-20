from style import *
import json, numpy as np
# EfficientNet-B0 from notebook 14, MobileNetV3-Large and MobileNetV4-Conv-S from notebook 22
D=json.load(open('./components.json'))
names=['EfficientNet-B0','MobileNetV3-Large','MobileNetV4-Conv-S']
x=np.arange(5); xl=['Orig.','224','160','112','80']
ARMS=[('base','#7f7f7f','o','-','\\texttt{base}'),('qaug','#2E8B57','s','-','\\texttt{qaug}'),
      ('qaug_jpeg','#1f5fa8','^','--','\\texttt{qaug\\_jpeg}'),('qaug_resize','#d2691e','v',':','\\texttt{qaug\\_resize}')]
fig,axs=plt.subplots(1,3,figsize=(TEXTW,1.8),sharey=True)
fig.subplots_adjust(left=0.105,right=0.995,top=0.9,bottom=0.225,wspace=0.1)
for ax,n in zip(axs,names):
    for k,c,m,ls,lab in ARMS:
        mu=np.array(D[n][k]['mean']); sd=np.array(D[n][k]['sd'])
        ax.fill_between(x,mu-sd,mu+sd,color=c,alpha=0.12,lw=0)
        ax.plot(x,mu,color=c,marker=m,ms=3.0,ls=ls,lw=1.1,label=lab)
    ax.set_title(n,pad=3); ax.set_xticks(x); ax.set_xticklabels(xl); ax.set_ylim(0,80); ax.set_yticks([0,20,40,60,80])
    ax.grid(axis='y',lw=0.3,color='0.85')
axs[0].set_ylabel('other$\\rightarrow$disease (\\%)')
axs[0].legend(loc='upper left',handlelength=2.0,fontsize=7.5,ncol=1,borderaxespad=0.3,labelspacing=0.2)
fig.text(0.55,0.02,'Stress-test level (original, or size in px before JPEG q70)',ha='center')
fig.savefig('out/fig_ablation.pdf')
