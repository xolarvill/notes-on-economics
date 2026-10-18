"""Schematic IS-LM comparisons derived from the NK chapter's conditional equations.

Run from the repository root with the uv-managed environment:
    .venv/bin/python macro/images/islm_comparison.py

No data or empirical calibration. The drawings deliberately match the geometry
of the two models. Axis ticks identify equilibria, not comparable numeric units.
The NK money slopes are consistent with MIU: sigma=.4, nu_m=4/3, i_bar=.75,
eta=1, alpha_m=.3. These legibility choices differ from the quarterly experiment.
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEMAND = '#236a53'
LIQUIDITY = '#426b93'
NEW = '#b66b27'
GRAY = '#8b9297'


def intersection(a, b, c, d):
    """Solve u=a-b*z, u=c+d*z; verify both original curves."""
    z = (a-c)/(b+d)
    u = a-b*z
    np.testing.assert_allclose(u, c+d*z, atol=1e-12)
    return z, u


def axes_style(ax, title, xlabel, ylabel, xlim, ylim):
    ax.set(xlim=xlim, ylim=ylim, xlabel=xlabel, ylabel=ylabel)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_bounds(0, ylim[1])
    ax.spines['bottom'].set_bounds(0, xlim[1])
    ax.tick_params(length=0, labelsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.xaxis.set_label_coords(1., -.10)
    ax.xaxis.label.set_horizontalalignment('right')
    ax.yaxis.set_label_coords(-.10, .57)
    ax.plot(xlim[1], 0, marker='>', ms=4, color='black', clip_on=False)
    ax.plot(0, ylim[1], marker='^', ms=4, color='black', clip_on=False)
    ax.set_title(title, loc='left', fontsize=11, pad=15, weight='bold')


def equilibrium(ax, point, name, xtick, ytick, color, offset):
    x, y = point
    ax.plot([x, x], [0, y], color=GRAY, lw=.7, ls=(0, (3, 3)))
    ax.plot([0, x], [y, y], color=GRAY, lw=.7, ls=(0, (3, 3)))
    ax.plot(x, y, 'o', color=color, ms=4, zorder=5)
    ax.annotate(name, (x, y), xytext=offset, textcoords='offset points',
                fontsize=10, color=color, weight='bold')
    ax.set_xticks([*ax.get_xticks(), x], [*(t.get_text() for t in ax.get_xticklabels()), xtick])
    ax.set_yticks([*ax.get_yticks(), y], [*(t.get_text() for t in ax.get_yticklabels()), ytick])


def label(ax, x, y, txt, color):
    ax.text(x, y, txt, color=color, fontsize=10,
            bbox={'facecolor':'white','edgecolor':'none','pad':1.5})


def save(fig, stem):
    out = Path(__file__).with_name(stem+'.pdf')
    fig.savefig(out, metadata={'CreationDate':None,'ModDate':None,'Title':stem})
    fig.savefig(out.with_suffix('.png'), dpi=190)
    plt.close(fig)
    print(out)


def main():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                         'mathtext.fontset':'dejavusans','pdf.fonttype':42,
                         'ps.fonttype':42})
    # LEFT: a linear intermediate goods market and money demand.
    # C=.9+.6(Y-.5), I=2-i, G=1.4; M/P=.3Y-i.
    c_prop, b_inv = .6, 1.
    A = .9-.6*.5+2+1.4
    is_a, is_b = A/b_inv, (1-c_prop)/b_inv
    money0, money1, k, h = .4, 1.2, .3, 1.
    E0 = intersection(is_a,is_b,-money0/h,k/h)
    E1 = intersection(is_a,is_b,-money1/h,k/h)
    assert E1[0]>E0[0] and E1[1]<E0[1]
    for Y,i in [E0,E1]:
        np.testing.assert_allclose(Y, .9+.6*(Y-.5)+(2-i)+1.4)
        assert 2-i>0
    # RIGHT: the same geometry in NK log deviations, scaled by .01.
    sigma, nu_m, ibar = .4, 4/3, .75
    am, eta = sigma/nu_m, 1/(nu_m*ibar)
    scale = .01
    d, expected_pi = .1, 0.
    real0, real1 = money0*scale, money1*scale
    N0 = intersection(expected_pi+sigma*d,sigma,-real0/eta,am/eta)
    N1 = intersection(expected_pi+sigma*d,sigma,-real1/eta,am/eta)
    np.testing.assert_allclose(N0, np.array(E0)*scale)
    np.testing.assert_allclose(N1, np.array(E1)*scale)
    for (y,j), balances in [(N0,real0),(N1,real1)]:
        np.testing.assert_allclose(y,d-(j-expected_pi)/sigma)
        np.testing.assert_allclose(balances,am*y-eta*j)
    fig, axs = plt.subplots(1,2,figsize=(8,4.6))
    fig.subplots_adjust(left=.09,right=.97,bottom=.30,top=.82,wspace=.36)
    for n, (ax, factor) in enumerate(zip(axs,[1,scale])):
        z=np.linspace(0,10,350)*factor
        axes_style(ax, ['(a) Intermediate macro','(b) Microfounded NK'][n],
                   [r'Output $Y$',r'Output $\hat y_t$'][n],
                   [r'Nominal rate $i$',r'Nominal rate $j_t$'][n],
                   (0,10*factor),(0,4.4*factor))
        ax.plot(z,is_a*factor-is_b*z,color=DEMAND,lw=1.8)
        ax.plot(z,k*z-money0*factor,color=LIQUIDITY,lw=1.8)
        ax.plot(z,k*z-money1*factor,color=LIQUIDITY,lw=1.8,ls='--')
        point0,point1 = (E0,E1) if n==0 else (N0,N1)
        equilibrium(ax,point0,r'$E_0$', [r'$Y_0$',r'$\hat y_0$'][n],
                    [r'$i_0$',r'$j_0$'][n],'black',(6,8))
        equilibrium(ax,point1,r'$E_1$', [r'$Y_1$',r'$\hat y_1$'][n],
                    [r'$i_1$',r'$j_1$'][n],NEW,(6,-14))
        label(ax,1.0*factor,3.72*factor,'IS',DEMAND)
        label(ax,8.45*factor,2.35*factor,r'$LM_0$',LIQUIDITY)
        label(ax,8.65*factor,1.28*factor,r'$LM_1$',LIQUIDITY)
        shift_rate=.6
        shift_x0=(shift_rate+money0)/k
        shift_x1=(shift_rate+money1)/k
        np.testing.assert_allclose(k*shift_x0-money0,k*shift_x1-money1)
        ax.annotate('',xy=(shift_x1*factor,shift_rate*factor),xytext=(shift_x0*factor,shift_rate*factor),
                    arrowprops={'arrowstyle':'->','color':NEW,'lw':1.3})
        ax.text(3.8*factor,.78*factor,r'$M/P\uparrow$' if n==0 else r'$\hat m_t-\hat p_t\uparrow$',
                color=NEW,fontsize=9)
        ax.text(.5,-.31, ['Given consumption and investment\nFixed price and behavioral coefficients',
                         'Euler IS and money-utility LM\nFixed price and future outlook'][n],
                transform=ax.transAxes,ha='center',va='top',fontsize=9,linespacing=1.5)
    save(fig,'islm_microfoundations_comparison')

    # News about future consumption changes NK d, leaving money and P fixed.
    d1=d+.018
    news0=N0
    news1=intersection(sigma*d1,sigma,-real0/eta,am/eta)
    assert news1[0]>news0[0] and news1[1]>news0[1]
    np.testing.assert_allclose(news1[0],d1-news1[1]/sigma)
    np.testing.assert_allclose(real0,am*news1[0]-eta*news1[1])

    # Taylor closure, holding expected next gap and inflation fixed.
    # j=e+rn+sigma*E[x_next]-sigma*x; pi=beta*e+kappa*x.
    beta, kap, pp, px = .99,.064375,1.5,.125
    sigma_rule, exnext, epi, rn = 1.,.025,0.,0.
    shock0,shock1=.005,.015
    H=epi+rn+sigma_rule*exnext
    mp_slope=pp*kap+px
    mp0=pp*beta*epi+shock0
    mp1=pp*beta*epi+shock1
    R0=intersection(H,sigma_rule,mp0,mp_slope)
    R1=intersection(H,sigma_rule,mp1,mp_slope)
    assert R1[0]<R0[0] and R1[1]>R0[1]
    for (x,j),nu in [(R0,shock0),(R1,shock1)]:
        pi=beta*epi+kap*x
        np.testing.assert_allclose(x,exnext-(j-epi-rn)/sigma_rule)
        np.testing.assert_allclose(j,pp*pi+px*x+nu)
    fig,axs=plt.subplots(1,2,figsize=(8,4.6))
    fig.subplots_adjust(left=.09,right=.97,bottom=.30,top=.82,wspace=.36)
    ax=axs[0];z=np.linspace(0,.105,350)
    axes_style(ax,'(a) Higher expected future output',r'Output $\hat y_t$',
               r'Nominal rate $j_t$',(0,.105),(0,.047))
    ax.plot(z,sigma*d-sigma*z,color=DEMAND,lw=1.8)
    ax.plot(z,sigma*d1-sigma*z,color=DEMAND,lw=1.8,ls='--')
    ax.plot(z,am*z-real0,color=LIQUIDITY,lw=1.8)
    equilibrium(ax,news0,r'$E_0$',r'$\hat y_0$',r'$j_0$','black',(-21,-17))
    equilibrium(ax,news1,r'$E_1$',r'$\hat y_1$',r'$j_1$',NEW,(6,6))
    label(ax,.011,.034,r'$IS_0$',DEMAND);label(ax,.031,.038,r'$IS_1$',DEMAND)
    label(ax,.093,.022,'LM',LIQUIDITY)
    news_rate=.032
    news_x0=(sigma*d-news_rate)/sigma
    news_x1=(sigma*d1-news_rate)/sigma
    np.testing.assert_allclose(sigma*d-sigma*news_x0,sigma*d1-sigma*news_x1)
    ax.annotate('',xy=(news_x1,news_rate),xytext=(news_x0,news_rate),
                arrowprops={'arrowstyle':'->','color':NEW,'lw':1.3})
    ax.text(.022,.034,r'$d_t\uparrow$',color=NEW,fontsize=9)
    ax.text(.5,-.31,'Higher expected future consumption\nFixed money and current price',
            transform=ax.transAxes,ha='center',va='top',fontsize=9,linespacing=1.5)
    ax=axs[1];z=np.linspace(0,.03,350)
    axes_style(ax,'(b) A policy-rule disturbance',r'Output gap $x_t$',
               r'Nominal rate $j_t$',(0,.03),(0,.03))
    ax.plot(z,H-sigma_rule*z,color=DEMAND,lw=1.8)
    ax.plot(z,mp0+mp_slope*z,color=LIQUIDITY,lw=1.8)
    ax.plot(z,mp1+mp_slope*z,color=LIQUIDITY,lw=1.8,ls='--')
    equilibrium(ax,R0,r'$E_0$',r'$x_0$',r'$j_0$','black',(6,-17))
    equilibrium(ax,R1,r'$E_1$',r'$x_1$',r'$j_1$',NEW,(-24,7))
    label(ax,.003,.024,'IS',DEMAND)
    label(ax,.024,.0085,r'$MP_0$',LIQUIDITY)
    label(ax,.024,.022,r'$MP_1$',LIQUIDITY)
    mp_arrow_x=.021
    ax.annotate('',xy=(mp_arrow_x,mp1+mp_slope*mp_arrow_x),xytext=(mp_arrow_x,mp0+mp_slope*mp_arrow_x),
                arrowprops={'arrowstyle':'->','color':NEW,'lw':1.3})
    ax.text(.022,.014,r'$\nu_t\uparrow$',color=NEW,fontsize=9)
    ax.text(.5,-.31,'Taylor rule + NKPC determine MP\nFixed outlook; accommodating money',
            transform=ax.transAxes,ha='center',va='top',fontsize=9,linespacing=1.5)
    save(fig,'islm_expectations_and_policy')
    print('Verified: goods and money equations, both monetary intersections,')
    print('news shifts, and the unreduced IS/NKPC/Taylor equations for MP.')
    print('Intermediate equilibria:',E0,E1)
    print('Conditional NK equilibria:',N0,N1)
    print('Conditional Taylor equilibria:',R0,R1)


if __name__=='__main__':
    main()
