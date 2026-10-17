"""Illustrative endogenous-growth figures; no external data.

Run from the repository root with the uv-managed project environment:
    .venv/bin/python macro/images/endogenous_growth_figures.py
Requires numpy and matplotlib.
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'notes-economics-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,'pdf.fonttype':42,
                     'axes.spines.top':False,'axes.spines.right':False})
base=Path(__file__).parent
blue,green,red='#294b87','#24724d','#ae4c45'
meta={'CreationDate':None,'ModDate':None}
t=np.linspace(0,60,400)
rho,theta,delta=.04,2.,.02
B=.1; growth=(B-delta-rho)/theta; xi=B-delta-growth
B_high=.12; growth_high=(B_high-delta-rho)/theta; xi_high=B_high-delta-growth_high
fig,ax=plt.subplots(figsize=(7,3.2),layout='constrained')
ax.plot(t,growth*t,color=blue,lw=1.7,label='Baseline: growth 0.02')
ax.plot(t,np.log(1.1)+growth*t,color=green,lw=1.5,ls='--',label='10% higher initial stock: same growth')
ax.plot(t,np.log(xi_high/xi)+growth_high*t,color=red,lw=1.7,label='Higher productivity B: growth 0.03')
ax.set(xlabel='Time (model units)',ylabel=r'$\log[C(t)/C_{\mathrm{base}}(0)]$',
       xlim=(0,60),ylim=(-.04,2.12))
ax.legend(frameon=False,fontsize=8.5,loc='upper left')
fig.savefig(base/'endogenous_ak_paths.pdf',metadata=meta); plt.close(fig)
capital1=np.linspace(0,1,500)
output=2*np.sqrt(capital1)+np.sqrt(1-capital1)
fig,ax=plt.subplots(figsize=(7,3),layout='constrained')
ax.plot(capital1,output,color=blue,lw=1.7)
for k,label,color,offset in [(.5,'Wedge-distorted: (0.5, 0.5)',red,(-120,-36)),
                             (.8,'Efficient: (0.8, 0.2)',green,(-95,18))]:
    y=2*np.sqrt(k)+np.sqrt(1-k)
    ax.scatter([k],[y],s=26,color=color,zorder=3)
    ax.plot([k,k],[.9,y],ls=':',color=color,lw=1)
    ax.annotate(label,(k,y),xytext=offset,textcoords='offset points',color=color,fontsize=9)
ax.set(xlabel=r'Capital at firm 1, $k_1$; firm 2 receives $1-k_1$',
       ylabel=r'Total output $2\sqrt{k_1}+\sqrt{1-k_1}$',xlim=(0,1),ylim=(.9,2.48))
fig.savefig(base/'endogenous_allocation.pdf',metadata=meta); plt.close(fig)
print('Generated AK path and allocation figures from chapter equations.')
