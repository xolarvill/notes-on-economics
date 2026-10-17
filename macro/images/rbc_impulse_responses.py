"""First-order RBC teaching experiment; no data, estimation, or empirical fit.

Regenerate from the repository root with the uv-managed environment:
    .venv/bin/python macro/images/rbc_impulse_responses.py
Equations and coefficient matching are shown in the RBC chapter. Both policies
are solved afresh: changing persistence changes household decisions.
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'notes-economics-mpl'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def solve_policy(rho=.95, alpha=.33, beta=.99, delta=.025, sigma=1., phi=1., hours=1/3):
    rent=1/beta-1+delta
    v=rent/alpha
    s_i=delta/v
    s_c=1-s_i
    x=(alpha/rent)**(1/(1-alpha))  # Abar=1
    n=hours
    k=x*n
    y=k**alpha*n**(1-alpha)
    c=s_c*y
    wage=(1-alpha)*y/n
    chi=wage/(c**sigma*n**phi)
    bk=alpha*(1+phi)/(phi+alpha)
    ba=(1+phi)/(phi+alpha)
    bc=-(1-alpha)*sigma/(phi+alpha)
    gk=1-delta+v*bk
    ga=v*ba
    gc=v*(s_c-bc)
    omega=beta*rent
    tau=sigma-omega*bc
    upsilon=omega*(bk-1)
    zeta=omega*ba*rho
    roots=np.roots([tau*gc,-(tau*gk+upsilon*gc-sigma),upsilon*gk])
    candidates=[]
    for root in roots:
        if abs(root.imag)>1e-10:
            continue
        pk=float(root.real)
        J=tau*pk-upsilon
        denominator=sigma+J*gc-tau*rho
        if abs(denominator)<1e-12:
            continue
        pa=(J*ga-zeta)/denominator
        hk=gk-gc*pk
        ha=ga-gc*pa
        if abs(hk)<1:
            candidates.append((pk,pa,hk,ha))
    assert len(candidates)==1, candidates
    pk,pa,hk,ha=candidates[0]
    return dict(rho=rho,alpha=alpha,beta=beta,delta=delta,sigma=sigma,phi=phi,
                rent=rent,v=v,s_i=s_i,s_c=s_c,chi=chi,n=n,k=k,y=y,c=c,
                i=delta*k,wage=wage,bk=bk,ba=ba,bc=bc,gk=gk,ga=ga,gc=gc,
                omega=omega,tau=tau,upsilon=upsilon,zeta=zeta,
                pk=pk,pa=pa,hk=hk,ha=ha,roots=roots)


def response(p, size=.01, periods=81):
    a=size*p['rho']**np.arange(periods)
    k=np.zeros(periods)
    for t in range(periods-1):
        k[t+1]=p['hk']*k[t]+p['ha']*a[t]
    c=p['pk']*k+p['pa']*a
    n=(a+p['alpha']*k-p['sigma']*c)/(p['phi']+p['alpha'])
    y=a+p['alpha']*k+(1-p['alpha'])*n
    inv=(y-p['s_c']*c)/p['s_i']
    q=y-k
    w=y-n
    out=dict(a=a,k=k,c=c,n=n,y=y,i=inv,q=q,w=w)
    # Original, unreduced linear equations independently evaluated along the path.
    assert np.allclose(w,p['sigma']*c+p['phi']*n)
    assert np.allclose(y,p['s_c']*c+p['s_i']*inv)
    assert np.allclose(k[1:],(1-p['delta'])*k[:-1]+p['delta']*inv[:-1])
    assert np.allclose(p['sigma']*(c[1:]-c[:-1]),p['omega']*q[1:])
    assert k[0]==0 and a[0]==size
    return out


def main():
    persistent=solve_policy(.95)
    iid=solve_policy(0.)
    paths=[response(persistent),response(iid)]
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9,
                         'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(3,2,figsize=(7.2,7.2),layout='constrained')
    labels=[('a','Productivity'),('y','Output'),('c','Consumption'),
            ('i','Investment'),('n','Hours'),('k','Capital available at t')]
    t=np.arange(41)
    for ax,(key,title) in zip(axes.flat,labels):
        ax.plot(t,100*paths[0][key][:41],color='#294b87',lw=1.6,label=r'$\rho_a=0.95$')
        ax.plot(t,100*paths[1][key][:41],color='#24724d',lw=1.5,ls='--',label=r'$\rho_a=0$')
        ax.axhline(0,color='#999999',lw=.6)
        ax.set_title(title,loc='left',fontsize=10)
        ax.set_xlim(0,40)
        ax.set_xticks([0,10,20,30,40])
        ax.set_ylabel('100 × log deviation')
        ax.grid(axis='y',alpha=.15)
    for ax in axes[-1]:
        ax.set_xlabel('Quarters after the innovation')
    axes[0,0].legend(frameon=False,fontsize=8)
    fig.savefig(Path(__file__).with_suffix('.pdf'),metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)
    for p,path in zip([persistent,iid],paths):
        print('rho=',p['rho'],'policy:',{s:round(p[s],9) for s in ['pk','pa','hk','ha']})
        print('impact percent:',{s:round(100*path[s][0],6) for s in ['a','y','c','i','n','k']})
    print('steady:',{s:round(persistent[s],9) for s in ['rent','s_c','s_i','k','y','c','i','chi']})
    print('PASS independent original linear equations, capital timing, and both freshly solved policies; figure generated.')


if __name__=='__main__':
    main()
