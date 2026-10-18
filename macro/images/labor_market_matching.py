"""Real search-and-matching examples; original figures, no empirical data.

Run with .venv/bin/python macro/images/labor_market_matching.py.
Continuous-time rates use months. Transitions solve match values backwards
and unemployment forwards, rather than substitute a sequence of steady states.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import os
import tempfile

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Parameters:
    r: float = .004
    s: float = .02
    z: float = 1.
    b: float = .6
    A: float = .5
    k: float = .5
    eta: float = .5
    xi: float = .5


def steady(p=Parameters(), fixed_wage=None, planner=False):
    assert p.r > 0 and p.s > 0 and p.A > 0 and p.k > 0
    assert p.z > p.b >= 0 and 0 < p.xi < 1 and 0 < p.eta < 1
    weight = p.xi if planner else p.eta
    if fixed_wage is None:
        def entry(th):
            return p.k * (p.r+p.s) / p.A * th**p.xi + weight*p.k*th - (1-weight)*(p.z-p.b)
        upper = 1.
        while entry(upper) < 0:
            upper *= 2
        th = brentq(entry, 0., upper, xtol=1e-14)
        wage = (1-weight)*p.b + weight*(p.z+p.k*th)
    else:
        wage = float(fixed_wage)
        assert p.b < wage < p.z, 'The fixed-wage experiment requires positive worker and firm surpluses.'
        th = (p.A*(p.z-wage)/(p.k*(p.r+p.s)))**(1/p.xi)
    f = p.A*th**(1-p.xi)
    q = p.A*th**(-p.xi)
    u = p.s/(p.s+f)
    v = th*u
    J = (p.z-wage)/(p.r+p.s)
    D = (wage-p.b)/(p.r+p.s+f)
    U = (p.b+f*D)/p.r
    Y = p.z*(1-u)
    C = Y+p.b*u-p.k*v
    assert C > 0
    return dict(th=th, f=f, q=q, u=u, v=v, w=wage, J=J, D=D, S=J+D,
                U=U, W=U+D, Y=Y, C=C)


def fundamentals(t, kind, p=Parameters()):
    decay = np.exp(-np.asarray(t)/6.)
    z = p.z*(1-.02*decay) if kind == 'productivity' else p.z+0*decay
    A = p.A*(1-.20*decay) if kind == 'matching' else p.A+0*decay
    s = p.s*(1+decay) if kind == 'separations' else p.s+0*decay
    assert kind in ('productivity', 'matching', 'separations')
    return z, A, s


def transition(kind, p=Parameters(), horizon=240., end=36., points=721):
    base = steady(p)

    def market(t, surplus):
        z, A, s = fundamentals(t, kind, p)
        th = ((1-p.eta)*A*surplus/p.k)**(1/p.xi)
        f = A*th**(1-p.xi)
        return z, A, s, th, f

    def surplus_rhs(t, arr):
        surplus = arr[0]
        z, A, s, th, f = market(t, surplus)
        return [(p.r+s+p.eta*f)*surplus-(z-p.b)]

    backward = solve_ivp(surplus_rhs, (horizon, 0.), [base['S']], method='DOP853',
                         rtol=2e-11, atol=2e-12, max_step=.5, dense_output=True)
    assert backward.success

    def unemployment_rhs(t, arr):
        surplus = backward.sol(t)[0]
        z, A, s, th, f = market(t, surplus)
        return [s*(1-arr[0])-f*arr[0]]

    forward = solve_ivp(unemployment_rhs, (0., end), [base['u']], method='DOP853',
                        rtol=2e-11, atol=2e-12, max_step=.25, dense_output=True)
    assert forward.success
    t = np.linspace(0., end, points)
    surplus = backward.sol(t)[0]
    z, A, s, th, f = market(t, surplus)
    u = forward.sol(t)[0]
    q = A*th**(-p.xi)
    w = (1-p.eta)*p.b+p.eta*(z+p.k*th)
    J = (1-p.eta)*surplus
    D = p.eta*surplus
    v = th*u
    Y = z*(1-u)
    C = Y+p.b*u-p.k*v
    assert np.all((u > 0) & (u < 1)) and np.all(C > 0) and np.all(surplus > 0)
    np.testing.assert_allclose(q*J, p.k, rtol=2e-13)
    np.testing.assert_allclose(f*u, q*v, rtol=2e-13)
    np.testing.assert_allclose(w*(1-u)+p.b*u+(z-w)*(1-u)-p.k*v, C, atol=1e-13)
    return dict(t=t, S=surplus, th=th, f=f, q=q, u=u, v=v, w=w, J=J, D=D,
                Y=Y, C=C, z=z, A=A, s=s, base=base, p=p,
                backward=backward, forward=forward, market=market)


def figures():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'ps.fonttype': 42})
    p = Parameters(); base = steady(p)
    directory = Path(__file__).resolve().parent
    fig, axes = plt.subplots(1, 2, figsize=(10.3, 4.05), constrained_layout=True)
    ax = axes[0]
    th = np.linspace(.03, 1.35, 400)
    jc = p.z-p.k*(p.r+p.s)/p.A*th**p.xi
    ws = (1-p.eta)*p.b+p.eta*(p.z+p.k*th)
    ax.plot(th, jc, color='#244d74', label='Job creation')
    ax.plot(th, ws, color='#b56c2f', label='Nash wage')
    ax.plot(base['th'], base['w'], 'o', color='#202b36')
    ax.axvline(base['th'], color='.6', lw=.8, ls=':')
    ax.axhline(base['w'], color='.6', lw=.8, ls=':')
    ax.annotate('Equilibrium', (base['th'], base['w']), xytext=(.15, 1.035),
                arrowprops={'arrowstyle': '->', 'color': '.3'}, fontsize=9)
    ax.set(title='A. The wage and recruitment must agree', xlabel='Vacancies / unemployed workers',
           ylabel='Real wage (goods per month)', ylim=(.80, 1.14))
    ax.legend(frameon=False, loc='lower right', fontsize=9)
    ax = axes[1]
    u = np.linspace(.025, .105, 500)
    for pp, color, label in [(p, '#244d74', 'Baseline matching'),
                              (replace(p, A=.4), '#b56c2f', 'Matching efficiency -20%')]:
        st = steady(pp)
        v = (pp.s*(1-u)/(pp.A*u**pp.xi))**(1/(1-pp.xi))
        ax.plot(100*u, 100*v, color=color, label=label)
        ax.plot(100*u, 100*st['th']*u, '--', lw=1, color=color)
        ax.plot(100*st['u'], 100*st['v'], 'o', color=color)
    ax.text(7.3, 5.4, 'Dashed: entry rays', fontsize=8, color='.3', rotation=20)
    ax.set(title='B. Balanced flows and vacancy entry', xlabel='Unemployed / labor force (%)',
           ylabel='Vacancies / labor force (%)', ylim=(0, 7), xlim=(2.5, 10.5))
    ax.legend(frameon=False, fontsize=8, loc='upper right')
    for ax in axes: ax.grid(alpha=.13)
    fig.savefig(directory/'labor_market_equilibrium.pdf', metadata={'CreationDate': None})
    fig.savefig(directory/'labor_market_equilibrium.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(10.4, 6.4), constrained_layout=True)
    series = [('th', 'Market tightness', '% from baseline'),
              ('u', 'Unemployment rate', 'Percentage-point change'),
              ('v', 'Vacancies per worker', '% from baseline'),
              ('f', 'Job-finding hazard', '% from baseline'),
              ('w', 'Real wage', '% from baseline'),
              ('Y', 'Market output', '% from baseline')]
    experiments = [('productivity', 'Productivity -2%', '#244d74'),
                   ('matching', 'Matching efficiency -20%', '#b56c2f'),
                   ('separations', 'Separation hazard +100%', '#527c5a')]
    for kind, label, color in experiments:
        path = transition(kind)
        for ax, (key, title, units) in zip(axes.flat, series):
            values = 100*(path[key]-base[key]) if key == 'u' else 100*(path[key]/base[key]-1)
            ax.plot(path['t'], values, color=color, lw=1.5, label=label)
            ax.set(title=title, ylabel=units, xlabel='Months after news')
            ax.axhline(0, color='.55', lw=.6)
            ax.grid(alpha=.13)
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.savefig(directory/'labor_market_transitions.pdf', metadata={'CreationDate': None})
    fig.savefig(directory/'labor_market_transitions.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    p = Parameters(); baseline = steady(p)
    print('Stationary baseline:', baseline)
    print('Productivity -0.5%, flexible:', steady(replace(p, z=.995)))
    print('Productivity -0.5%, fixed real wage:', steady(replace(p, z=.995), fixed_wage=baseline['w']))
    for kind in ('productivity', 'matching', 'separations'):
        path = transition(kind)
        peak = int(np.argmax(path['u']))
        print(kind, 'impact:', {key:float(path[key][0]) for key in ('th','u','v','f','w','Y')},
              'peak unemployment:', path['t'][peak], path['u'][peak])
    figures()
