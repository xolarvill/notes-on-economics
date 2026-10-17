"""Constructed growth-synthesis paths, not empirical estimates.

Run from the repository root with the uv-managed environment:
    .venv/bin/python macro/images/growth_path_diagnosis.py
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
t = np.linspace(0, 30, 1201)
elapsed = np.maximum(t - 10, 0)
after = t >= 10
benchmark = 100 * np.exp(0.03 * t)
# Baseline utilization is 0.90; capacity is benchmark / 0.90.
# At date 10, utilization falls to 0.81 and then recovers toward 0.90.
temporary = benchmark * np.where(after, 1 - 0.10 * np.exp(-elapsed / 4), 1)
level = benchmark * np.where(after, 0.90, 1)
slower = benchmark * np.exp(-0.015 * elapsed)

assert np.allclose(temporary[~after], benchmark[~after])
assert np.isclose(temporary[after][0] / benchmark[after][0], 0.90)
assert np.allclose(level[after] / benchmark[after], 0.90)
assert np.isclose(np.diff(np.log(slower))[-1] / np.diff(t)[-1], 0.015)
assert np.isclose(np.diff(np.log(level))[-1] / np.diff(t)[-1], 0.03)
assert temporary[-1] / benchmark[-1] > 0.999

series = [(benchmark, 'Benchmark: growth 3%', '#555555', '--'),
          (temporary, 'Temporary utilization decline', '#294b87', '-'),
          (level, 'Lasting 10% level loss', '#24724d', '-.'),
          (slower, 'Trend growth falls to 1.5%', '#ae4c45', ':')]
fig, axes = plt.subplots(2, 1, figsize=(7, 4.9), sharex=True, layout='constrained')
for y, label, color, style in series:
    axes[0].plot(t, np.log(y / 100), label=label, color=color, ls=style, lw=1.7)
    axes[1].plot(t, 100 * (y / benchmark - 1), color=color, ls=style, lw=1.7)
for ax in axes:
    ax.axvline(10, color='#888888', ls=':', lw=0.8)
    ax.set_xlim(0, 30)
    ax.grid(axis='y', alpha=0.15)
axes[0].set_ylabel(r'Log output, $\log[Y(t)/100]$')
axes[0].set_ylim(-0.04, 1.13)
axes[0].legend(frameon=False, ncol=2, loc='upper left', fontsize=8)
axes[1].set_ylabel('Deviation from benchmark (%)')
axes[1].set_xlabel('Time (model units); change at date 10')
axes[1].set_ylim(-29, 2)
fig.savefig(Path(__file__).with_suffix('.pdf'), metadata={'CreationDate': None, 'ModDate': None})
plt.close(fig)
print('PASS constructed path checks; generated growth_path_diagnosis.pdf')
