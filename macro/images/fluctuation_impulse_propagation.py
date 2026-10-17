"""Timing illustration: a single innovation and alternative activity persistence.

No data or estimated structural responses. Regenerate from the repository root:
    .venv/bin/python macro/images/fluctuation_impulse_propagation.py
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 9,
                     'pdf.fonttype': 42, 'axes.spines.top': False,
                     'axes.spines.right': False})
t = np.arange(-2, 21)
innovation = np.where(t == 0, -1.0, 0.0)
fig, axes = plt.subplots(2, 1, figsize=(7, 4.6), sharex=True, layout='constrained')
axes[0].plot(t, innovation, 'o-', color='#555555', lw=1.3, ms=3)
axes[0].set_ylabel(r'Innovation $\varepsilon_t$')
axes[0].set_title('One innovation; different propagation', fontsize=10, loc='left')
for rho, color, style in [(0.0, '#777777', ':'), (0.5, '#294b87', '--'), (0.85, '#24724d', '-')]:
    x = np.zeros_like(t, dtype=float)
    last = 0.0
    for j, eps in enumerate(innovation):
        x[j] = rho * last + eps
        last = x[j]
    assert np.all(x[t < 0] == 0)
    assert x[t == 0][0] == -1
    assert np.allclose(x[t >= 0], -rho ** t[t >= 0])
    assert np.isclose(sum(-rho ** k for k in range(1000)), -1 / (1 - rho))
    axes[1].plot(t, x, style, color=color, lw=1.6, marker='o', ms=2.5,
                 label=fr'$\rho={rho:g}$')
for ax in axes:
    ax.axhline(0, color='#999999', lw=0.6)
    ax.axvline(0, color='#999999', lw=0.7, ls=':')
    ax.set_xlim(-2, 20)
    ax.set_ylim(-1.08, 0.1)
    ax.set_yticks([-1, -0.5, 0])
    ax.grid(axis='y', alpha=0.15)
axes[1].set_ylabel(r'Activity deviation $x_t$')
axes[1].set_xlabel('Periods relative to the innovation (no calendar length assigned)')
axes[1].set_xticks([0, 4, 8, 12, 16, 20])
axes[1].legend(frameon=False, loc='lower right', fontsize=9)
fig.savefig(Path(__file__).with_suffix('.pdf'), metadata={'CreationDate': None, 'ModDate': None})
plt.close(fig)
print('PASS single-innovation timing, impact, recursion, and cumulative responses; generated figure.')
