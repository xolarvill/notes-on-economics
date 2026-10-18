"""Original deterministic open-economy examples; no empirical observations.
Run .venv/bin/python macro/images/intertemporal_trade.py to regenerate figures.
"""
import os
from pathlib import Path
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def allocation(q1, q2, R=1., beta=1., sigma=1., b0=0., R0=1.):
    if not (q1 > 0 and q2 > 0 and R > 0 and beta > 0 and sigma > 0):
        raise ValueError('Positive endowments, gross return, discount and curvature required.')
    wealth = q1 + R0*b0 + q2/R
    if wealth <= 0:
        raise ValueError('Lifetime resources must be positive.')
    growth = (beta*R)**(1/sigma)
    c1 = wealth/(1+growth/R)
    c2 = growth*c1
    return dict(c1=c1, c2=c2, b1=q1+R0*b0-c1, wealth=wealth, growth=growth)


def project(q1=2., q2=2., A=1., alpha=.5, delta=1., R=1., beta=1., sigma=1.):
    if not (0 < alpha < 1 and 0 <= delta <= 1 and R > 1-delta and A > 0):
        raise ValueError('Finite concave investment optimum required.')
    k = (alpha*A/(R-1+delta))**(1/(1-alpha))
    proceeds = A*k**alpha+(1-delta)*k
    wealth = q1 + (q2+proceeds)/R - k
    growth = (beta*R)**(1/sigma)
    c1 = wealth/(1+growth/R)
    c2 = growth*c1
    b1 = q1-c1-k
    return dict(k=k, proceeds=proceeds, wealth=wealth, c1=c1, c2=c2,
                b1=b1, saving=q1-c1, ca=q1-c1-k)


def figures():
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':8,
                         'axes.spines.top':False, 'axes.spines.right':False,
                         'axes.titlesize':9, 'axes.labelsize':8,
                         'xtick.labelsize':7, 'ytick.labelsize':7,
                         'pdf.fonttype':42, 'legend.fontsize':7})
    root=Path(__file__).resolve().parent
    fig, axes=plt.subplots(1,2,figsize=(6.3,3.0),layout='constrained')
    for ax, q, country in zip(axes, [(1.,3.),(3.,1.)], ['A: borrows today','B: lends today']):
        c=allocation(*q)
        x=np.linspace(.12,3.96,450)
        ax.fill_between([0,4],[4,0],color='#e8f2ea',alpha=.7)
        ax.plot([0,4],[4,0],color='#255d49',lw=1.5,label='Budget: slope −1')
        ax.plot(x,q[0]*q[1]/x,ls='--',color='#87939f',lw=1.)
        ax.plot(x,c['c1']*c['c2']/x,color='#476fa5',lw=1.2,label='Indifference curves')
        ax.scatter(*q,color='#ac5342',s=19,zorder=5)
        ax.scatter(c['c1'],c['c2'],color='#255d49',s=23,zorder=5)
        ax.annotate(f'Autarky {tuple(map(int,q))}',q,xytext=(7,10),textcoords='offset points',fontsize=7)
        ax.annotate('Trade (2, 2)',(2,2),xytext=(15,10),textcoords='offset points',fontsize=7)
        ax.annotate('',xy=(1.82,2.18) if q[0]==1 else (2.18,1.82),
                    xytext=(1.18,2.82) if q[0]==1 else (2.82,1.18),
                    arrowprops={'arrowstyle':'->','color':'#ac5342','lw':1.3})
        ax.set(xlim=(0,4.35),ylim=(0,4.35),xlabel='Consumption at date 1',ylabel='Consumption at date 2',title=country)
        ax.set_xticks([0,1,2,3,4]); ax.set_yticks([0,1,2,3,4])
    axes[0].legend(loc='upper right',frameon=False)
    fig.savefig(root/'intertemporal_exchange.pdf'); fig.savefig(root/'intertemporal_exchange.png',dpi=180)
    plt.close(fig)

    fig, axes=plt.subplots(2,2,figsize=(6.3,4.8),layout='constrained')
    shocks=[('Temporary loss',(1.,2.)),('Persistent loss',(1.,1.)),('Future income news',(2.,3.))]
    for ax,(title,q) in zip(axes.flat[:3],shocks):
        c=allocation(*q)
        x=np.array([1,2]); width=.28
        ax.bar(x-width/2,q,width,color='#88a3ba',label='Income Q')
        ax.bar(x+width/2,[c['c1'],c['c2']],width,color='#56836c',label='Consumption C')
        ax.set(title=title,xticks=x,xticklabels=['Date 1','Date 2'],ylim=(0,3.6),ylabel='Goods')
        ax.text(.04,.94,f"Date-1 assets: {c['b1']:+.2f}",transform=ax.transAxes,va='top',fontsize=7)
    axes.flat[0].legend(loc='upper left',bbox_to_anchor=(.03,.86),borderaxespad=0,frameon=False)
    ax=axes.flat[3]
    values=[project(A=a) for a in (1.,1.4)]
    names=['C₁','Saving S₁','Investment I₁','CA₁']
    x=np.arange(4)
    for offset,v,col,lab in [(-.16,values[0],'#88a3ba','A₂ = 1'),(.16,values[1],'#56836c','A₂ = 1.4')]:
        ax.bar(x+offset,[v['c1'],v['saving'],v['k'],v['ca']],.3,color=col,label=lab)
    ax.axhline(0,color='#60666d',lw=.6)
    ax.set(title='A more productive future project',xticks=x,xticklabels=names,ylabel='Goods',ylim=(-.9,2.6))
    ax.legend(frameon=False,loc='upper right')
    fig.savefig(root/'external_adjustment.pdf');fig.savefig(root/'external_adjustment.png',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    figures()
    for a in (1.,1.4):
        print('project',a,project(A=a))
