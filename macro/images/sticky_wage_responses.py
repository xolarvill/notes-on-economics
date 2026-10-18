"""Solved price/wage-contract experiment; illustrative parameters, no data.

Run: .venv/bin/python macro/images/sticky_wage_responses.py
The generalized matrix pencil uses (x, price inflation, wage inflation, g_prev).
Flexible contracts impose static markup conditions, never infinite PC slopes.
"""
from pathlib import Path
import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'notes-economics-mpl'))
import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy.linalg import eig
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def coefficients(beta=.99,sigma=1.,phi=1.,alpha=1/3,ep=6.,ew=6.,tp=.75,tw=.75,pp=1.5,px=.125):
    gp=alpha/(1-alpha);gw=sigma+phi/(1-alpha)
    ap=0 if tp==0 else (1-tp)*(1-beta*tp)/tp*(1-alpha)/(1-alpha+ep*alpha)
    aw=0 if tw==0 else (1-tw)*(1-beta*tw)/(tw*(1+ew*phi))
    return dict(beta=beta,sigma=sigma,phi=phi,alpha=alpha,ep=ep,ew=ew,
                tp=tp,tw=tw,pp=pp,px=px,gp=gp,gw=gw,ap=ap,aw=aw)


def pencil(p):
    b,s,ap,aw,gp,gw,pp,px=[p[k] for k in ['beta','sigma','ap','aw','gp','gw','pp','px']]
    L=np.array([[s+px,pp,0.,0.],[-ap*gp,1+ap,-ap,-ap],
                [-aw*gw,-aw,1+aw,aw],[0.,-1.,1.,1.]])
    R=np.array([[s,1.,0.,0.],[0.,b,0.,0.],[0.,0.,b,0.],[0.,0.,0.,1.]])
    if p['tp']==0:
        L[1]=[gp,-1,1,1];R[1]=0 # mc=gp*x+g=0
    if p['tw']==0:
        L[2]=[-gw,-1,1,1];R[2]=0 # wage markup=g-gw*x=0
    return L,R


def solve(rho=.5,**kwargs):
    p=coefficients(**kwargs);L,R=pencil(p)
    roots,vec=eig(L,R)
    stable=np.flatnonzero(np.abs(roots)<1-1e-9)
    assert len(stable)==1,(p,roots)
    assert all(abs(z)>1+1e-9 for n,z in enumerate(roots) if n not in stable)
    F=np.real_if_close(vec[:,stable[0]]/vec[3,stable[0]]).astype(float)
    G=float(np.real(roots[stable[0]]))
    np.testing.assert_allclose(L@F,G*R@F,atol=1e-10)
    np.testing.assert_allclose(G,1+F[2]-F[1],atol=1e-10)
    # Coefficients on nu, with J=h_w-h_p and no current-nu term in g_prev.
    change=np.array([0.,-1.,1.])
    mat=L[:3,:3]-rho*R[:3,:3]-np.outer((R@F)[:3],change)
    H=np.r_[np.linalg.solve(mat,np.array([-1.,0.,0.])),0.]
    J=H[2]-H[1]
    np.testing.assert_allclose(L@H,R@(F*J+rho*H)+np.array([-1.,0.,0.,0.]),atol=1e-10)
    # Independent scalar polynomial and explicit shock formulas from the text.
    if p['tp'] and p['tw']:
        b,s,ap,aw,gp,gw,pp,px=[p[k] for k in ['beta','sigma','ap','aw','gp','gw','pp','px']]
        D=Poly([s+px+ap*gp*pp,-b*(s+px)-s-ap*gp,s*b])
        LL=Poly([-1.,1+b+ap+aw,-b]);E=aw*gw-ap*gp
        polynomial=LL*D+E*ap*Poly([0.,pp,-1.])
        candidates=[z.real for z in polynomial.roots() if abs(z.imag)<1e-8 and abs(z)<1-1e-9]
        assert len(candidates)==1
        np.testing.assert_allclose(G,candidates[0],atol=1e-9)
        fx=-ap*G*(pp-G)/D(G)
        fp=ap*(gp*fx+G)/(1-b*G)
        fw=aw*(gw*fx-G)/(1-b*G)
        np.testing.assert_allclose(F,[fx,fp,fw,1.],atol=1e-9)
        K=1-b*rho-b*(G-1)+aw+ap
        LLnu=E/K
        PPnu=(ap*gp+(b*fp+ap)*LLnu)/(1-b*rho)
        hx=-1/(s*(1-rho)+px+(pp-rho)*PPnu-(s*fx+fp)*LLnu)
        np.testing.assert_allclose(H,[hx,PPnu*hx,(PPnu+LLnu)*hx,0.],atol=1e-9)
        np.testing.assert_allclose(J,LLnu*hx,atol=1e-9)
    return dict(p=p,F=F,H=H,G=G,J=J,roots=roots,rho=rho)


def response(rho=.5,shock=.001,horizon=24,**kwargs):
    sol=solve(rho=rho,**kwargs);p=sol['p'];F,H=sol['F'],sol['H']
    nu=shock*rho**np.arange(horizon+1)
    gprev=0.;rows=[]
    for v in nu:
        x,pi,pw,_=F*gprev+H*v
        g=gprev+pw-pi
        ex=F[0]*g+H[0]*rho*v
        epi=F[1]*g+H[1]*rho*v
        epw=F[2]*g+H[2]*rho*v
        rate=p['pp']*pi+p['px']*x+v
        real=rate-epi
        mu=g-p['gw']*x
        np.testing.assert_allclose(x,ex-real/p['sigma'],atol=1e-10)
        if p['tp']:
            np.testing.assert_allclose(pi,p['beta']*epi+p['ap']*(p['gp']*x+g),atol=1e-10)
        else: np.testing.assert_allclose(g+p['gp']*x,0.,atol=1e-10)
        if p['tw']:
            np.testing.assert_allclose(pw,p['beta']*epw+p['aw']*(p['gw']*x-g),atol=1e-10)
        else: np.testing.assert_allclose(mu,0.,atol=1e-10)
        np.testing.assert_allclose(g,sol['G']*gprev+sol['J']*v,atol=1e-10)
        rows.append([x,pi,pw,g,mu,real,rate])
        gprev=g
    return np.array(rows),sol


def main():
    variants=[('Sticky prices',dict(tp=.75,tw=0),'#426b93','--'),
              ('Sticky wages',dict(tp=0,tw=.75),'#b66b27',':'),
              ('Both contracts',dict(tp=.75,tw=.75),'#236a53','-')]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,
                         'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(3,2,figsize=(8,7.4),layout='constrained')
    titles=['Output gap','Price inflation','Wage inflation','Real-wage gap',
            'Wage-markup deviation','Expected real interest rate']
    summary=[]
    for name,args,color,ls in variants:
        path,sol=response(**args)
        for k,ax in enumerate(axes.flat):
            scale=1e4 if k in (1,2,5) else 100
            ax.plot(np.arange(len(path)),scale*path[:,k],color=color,ls=ls,lw=1.6,label=name)
        summary.append((name,path[0].tolist(),sol['G'],sol['roots'].tolist()))
        if name=='Both contracts':
            print('Both-contract state policy F:',sol['F'])
            print('Both-contract shock policy H:',sol['H'],'J=',sol['J'])
    for k,ax in enumerate(axes.flat):
        ax.axhline(0,color='#aaaaaa',lw=.7)
        ax.set(title=titles[k],xlabel='Quarters after innovation',
               ylabel='Basis points (quarterly)' if k in (1,2,5) else 'Log deviation × 100')
        ax.set_xticks([0,6,12,18,24]);ax.grid(axis='y',color='#eeeeee',lw=.6)
    axes.flat[0].legend(frameon=False,fontsize=8,loc='lower right')
    out=Path(__file__).with_suffix('.pdf')
    fig.savefig(out,metadata={'CreationDate':None,'ModDate':None,'Title':'Price and wage contract responses'})
    fig.savefig(out.with_suffix('.png'),dpi=160)
    print('Verified each unreduced equilibrium equation and contract limit.')
    for row in summary:print(row)
    # Contract memory is visible even when the policy innovation has no persistence.
    iid,sol=response(rho=0)
    assert abs(iid[1,0])>1e-9
    print('IID both-contract output at t=0,1:',iid[:2,0])
    print(out)


if __name__=='__main__':main()
