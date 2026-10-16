"""Generate the illustrative OLG figure from its stated model equations.

From the repository root, use the uv-managed project environment:
    .venv/bin/python macro/images/olg_capital_and_consumption.py
Requires numpy and matplotlib. No external data are used.
"""
from pathlib import Path
import os
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

alpha, beta, population, depreciation = .25, .96, 1.02, 1.
kappa = beta / (1 + beta)
capital = (kappa * (1-alpha) / population) ** (1 / (1-alpha))
golden = (alpha / (population - 1 + depreciation)) ** (1 / (1-alpha))
x = np.linspace(0, .55, 700)
capital_map = kappa * (1-alpha) * x**alpha / population
consumption = x**alpha - (population - 1 + depreciation) * x
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'pdf.fonttype': 42, 'axes.titleweight': 'normal'})
fig, axes = plt.subplots(1, 2, figsize=(8, 3.15), layout='constrained')
blue, green, red = '#294b87', '#24724d', '#ae4c45'
ax = axes[0]
ax.plot(x, capital_map, color=blue, lw=1.8, label=r'$k_{t+1}=Mk_t^\alpha$')
ax.plot(x, x, color='#666666', ls='--', lw=1, label='45-degree line')
ax.scatter([capital], [capital], color=blue, s=20, zorder=4)
ax.axvline(capital, 0, capital/.55, color=blue, ls=':', lw=1)
ax.annotate(r'$k^*$', (capital, 0), xytext=(0, -19), textcoords='offset points',
            ha='center', color=blue)
# A positive initial stock moves toward the fixed point by repeated market clearing.
k = .035
for _ in range(4):
    next_k = kappa*(1-alpha)*k**alpha/population
    ax.plot([k, k, next_k], [k, next_k, next_k], color=green, lw=.9, alpha=.85)
    k = next_k
ax.set(xlim=(0,.55), ylim=(0,.55), xlabel=r'Inherited $k_t$', ylabel=r'Next $k_{t+1}$',
       title='Capital dynamics')
ax.set_xticks([0,.15,.4,.55])
ax.legend(frameon=False, fontsize=8, loc='upper left')
ax = axes[1]
ax.plot(x, consumption, color=green, lw=1.8)
for k, label, color, offset in [(golden,r'$k_{\mathrm{GR}}$',green,(-20,13)),
                                (capital,r'$k^*$',red,(10,10))]:
    value = k**alpha-(population-1+depreciation)*k
    ax.scatter([k],[value],color=color,s=22,zorder=4)
    ax.plot([k,k],[0,value],color=color,ls=':',lw=1)
    ax.annotate(label,(k,value),xytext=offset,textcoords='offset points',color=color)
ax.set(xlim=(0,.55), ylim=(0,.56), xlabel=r'Stationary $k$',
       ylabel=r'$\bar c(k)=f(k)-(n+\delta)k$',title='Stationary consumption')
ax.text(.97,.08,r'$k^*>k_{\mathrm{GR}}$'+'\nOveraccumulation',transform=ax.transAxes,
        ha='right',va='bottom',color=red,fontsize=9)
fig.savefig(Path(__file__).with_suffix('.pdf'),metadata={'CreationDate':None,'ModDate':None})
plt.close(fig)
print(f'k*={capital:.10f}; k_GR={golden:.10f}; R*={alpha*capital**(alpha-1):.10f}')
