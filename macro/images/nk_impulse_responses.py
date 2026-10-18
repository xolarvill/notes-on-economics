"""Original New Keynesian policy experiment: illustrative parameters, no data.

Run with the repository's uv-managed environment:
    .venv/bin/python macro/images/nk_impulse_responses.py
Checks use the unreduced IS, Phillips, rule, and money equations.
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def solve_policy(beta=.99, sigma=1., phi=1., alpha=1/3, epsilon=6., theta=.75,
                 phi_pi=1.5, phi_x=.125, rho=.5, nu_m=2.):
    lam = (1-theta)*(1-beta*theta)/theta
    omega = (1-alpha)/(1-alpha+epsilon*alpha)
    gamma = sigma+(phi+alpha)/(1-alpha)
    kappa = lam*omega*gamma
    den = (sigma*(1-rho)+phi_x)*(1-beta*rho)+kappa*(phi_pi-rho)
    ax = -(1-beta*rho)/den
    bp = -kappa/den
    jr = phi_pi*bp+phi_x*ax+1
    rr = jr-rho*bp
    D = sigma+phi_x+kappa*phi_pi
    A = np.array([[sigma, 1-beta*phi_pi],
                  [kappa*sigma, kappa+beta*(sigma+phi_x)]])/D
    v = np.array([ax,bp])
    b = np.array([1,kappa])/D
    np.testing.assert_allclose(v, rho*A@v-b, rtol=1e-11)
    np.testing.assert_allclose(bp, beta*rho*bp+kappa*ax)
    np.testing.assert_allclose(ax, rho*ax-(jr-rho*bp)/sigma)
    assert np.max(np.abs(np.linalg.eigvals(A))) < 1
    return dict(kappa=kappa, ax=ax, bp=bp, jr=jr, rr=rr,
                eta=1/(nu_m*(1/beta-1)), alpha_m=sigma/nu_m,
                A=A, den=den)


def paths(rho=.5, e=.001, horizon=20):
    p = solve_policy(rho=rho)
    t = np.arange(horizon+1)
    nu = e*rho**t
    x, pi = p['ax']*nu, p['bp']*nu
    j, r = p['jr']*nu, p['rr']*nu
    price = np.cumsum(pi)
    money = price+p['alpha_m']*x-p['eta']*j
    # Evaluate the primitive local equations, including t=0 and the last date.
    np.testing.assert_allclose(pi, .99*rho*pi+p['kappa']*x, atol=1e-15)
    np.testing.assert_allclose(x, rho*x-(j-rho*pi), atol=1e-15)
    np.testing.assert_allclose(j, 1.5*pi+.125*x+nu, atol=1e-15)
    np.testing.assert_allclose(r, j-rho*pi, atol=1e-15)
    np.testing.assert_allclose(np.diff(np.r_[0., price]), pi, atol=1e-15)
    np.testing.assert_allclose(money-price, p['alpha_m']*x-p['eta']*j, atol=1e-15)
    np.testing.assert_allclose(price, p['bp']*e*(1-rho**(t+1))/(1-rho), atol=1e-15)
    return t, (x,pi,j,r,price,money), p


def main():
    t, series, p = paths()
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
                         'pdf.fonttype':42,'ps.fonttype':42,
                         'axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(3,2,figsize=(8,7.3),layout='constrained')
    names = ['Output gap','Inflation','Nominal interest rate',
             'Expected real interest rate','Price level','Money stock']
    for k,(ax,y,name) in enumerate(zip(axes.flat,series,names)):
        rate = k in (1,2,3)
        scale = 10000 if rate else 100
        ax.axhline(0,color='#a3a3a3',lw=.8)
        ax.plot(t,scale*y,color='#236a53',lw=1.8,marker='o',ms=2.7)
        if k in (4,5):
            ax.axhline(100*p['bp']*.001/(1-.5),color='#637a91',lw=1,ls='--',label='Long-run level')
            ax.legend(frameon=False,fontsize=8,loc='best')
        ax.set(title=name,xlabel='Quarters after innovation',
               ylabel='Basis points (quarterly)' if rate else 'Log deviation × 100')
        ax.set_xticks([0,5,10,15,20])
        ax.grid(axis='y',color='#eeeeee',lw=.6)
    out=Path(__file__).with_suffix('.pdf')
    fig.savefig(out,metadata={'CreationDate':None,'ModDate':None,
                             'Title':'New Keynesian policy-rule impulse responses'})
    print('Verified local equilibrium; kappa=',p['kappa'],'D_nu=',p['den'])
    print('Impact [x, pi, j, r, price, money]:',[float(y[0]) for y in series])
    print(out)


if __name__=='__main__':
    main()
