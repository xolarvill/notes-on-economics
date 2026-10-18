"""Independent optimization and accounting checks for Chapter 15.
Use the project's uv-managed .venv; no empirical calibration is asserted.
"""
import sys
sys.dont_write_bytecode=True
import importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar, brentq

spec=importlib.util.spec_from_file_location('intertemporal_trade',Path(__file__).resolve().parents[1]/'images/intertemporal_trade.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def utility(c,sigma):
    return np.log(c) if sigma==1 else (c**(1-sigma)-1)/(1-sigma)


def check_allocation():
    count=0
    for q1,q2,b0 in [(1.,3.,0.),(3.,1.,0.),(2.,2.,-.4),(1.,1.,.6)]:
        for R in [.85,1.,1.25]:
            for beta in [.8,1.]:
                for sigma in [.5,1.,2.]:
                    v=m.allocation(q1,q2,R,beta,sigma,b0,1.1)
                    W=q1+1.1*b0+q2/R
                    direct=minimize_scalar(lambda c: -utility(c,sigma)-beta*utility(R*(W-c),sigma),
                                           bounds=(1e-9,W-1e-9),method='bounded',options={'xatol':1e-13})
                    np.testing.assert_allclose(v['c1'],direct.x,rtol=2e-7,atol=2e-7)
                    np.testing.assert_allclose(v['c1']+v['b1'],q1+1.1*b0,atol=1e-12)
                    np.testing.assert_allclose(v['c2'],q2+R*v['b1'],atol=1e-12)
                    np.testing.assert_allclose(v['c1']**(-sigma),beta*R*v['c2']**(-sigma),rtol=1e-12)
                    count+=1
    R=brentq(lambda R:sum(m.allocation(*q,R)['b1'] for q in [(1.,3.),(3.,1.)]),.1,4.)
    np.testing.assert_allclose(R,1.,atol=1e-12)
    print(f'{count} direct CRRA optimizations and both sequential budgets; two-country return: passed')




def check_shocks_and_returns():
    count=0
    for R in [.85,1.,1.25]:
        for beta in [.8,1.]:
            for sigma in [.5,1.,2.]:
                q1,q2,b0,R0=1.7,2.4,-.2,1.1
                v=m.allocation(q1,q2,R,beta,sigma,b0,R0)
                g=(beta*R)**(1/sigma); D=1+g/R; W=v['wealth']; h=1e-5
                def result(r): return m.allocation(q1,q2,r,beta,sigma,b0,R0)
                lo,hi=result(R-h),result(R+h)
                numeric=(hi['c1']-lo['c1'])/(2*h)
                analytic=-q2/(R**2*D)-W*g*(1/sigma-1)/(R**2*D**2)
                np.testing.assert_allclose(numeric,analytic,rtol=2e-8,atol=1e-9)
                welfare=lambda x:utility(x['c1'],sigma)+beta*utility(x['c2'],sigma)
                np.testing.assert_allclose((welfare(hi)-welfare(lo))/(2*h),v['c1']**(-sigma)*v['b1']/R,rtol=3e-8,atol=1e-9)
                for d1,d2 in [(h,0),(0,h),(h,h)]:
                    new=m.allocation(q1+d1,q2+d2,R,beta,sigma,b0,R0)
                    np.testing.assert_allclose(new['c1']-v['c1'],(d1+d2/R)/D,atol=1e-12)
                    np.testing.assert_allclose(new['b1']-v['b1'],d1-(d1+d2/R)/D,atol=1e-12)
                count+=1
    print(f'{count} return/welfare derivatives and 54 income-timing responses: passed')


def check_projects():
    from scipy.optimize import minimize
    count=0
    for R in [.9,1.15]:
        for A in [.8,1.4]:
            for alpha,delta in [(.35,.4),(.5,1.)]:
                for sigma in [1.,2.]:
                    q1,q2,beta=2.,2.,.95
                    v=m.project(q1,q2,A,alpha,delta,R,beta,sigma)
                    def c2(x):
                        c,k=x
                        return q2+A*k**alpha+(1-delta)*k+R*(q1-c-k)
                    def obj(x):
                        end=c2(x)
                        if end<=0:return 1e10+1e8*(-end)
                        return -utility(x[0],sigma)-beta*utility(end,sigma)
                    direct=minimize(obj,[1.,.2],method='SLSQP',bounds=[(1e-8,None),(1e-8,None)],
                                    constraints=[{'type':'ineq','fun':lambda x:c2(x)-1e-8}],
                                    options={'ftol':1e-12,'maxiter':1000})
                    assert direct.success,direct.message
                    np.testing.assert_allclose(direct.x,[v['c1'],v['k']],rtol=1e-5,atol=1e-6)
                    np.testing.assert_allclose(c2(direct.x),v['c2'],rtol=1e-6)
                    np.testing.assert_allclose(v['ca'],v['saving']-v['k'],atol=1e-12)
                    # Derivative of total wealth, consumption, and the CA w.r.t. productivity.
                    h=1e-5;lo=m.project(q1,q2,A-h,alpha,delta,R,beta,sigma)
                    hi=m.project(q1,q2,A+h,alpha,delta,R,beta,sigma)
                    dk=v['k']/((1-alpha)*A);D=1+(beta*R)**(1/sigma)/R
                    for name,deriv in [('k',dk),('wealth',v['k']**alpha/R),
                                       ('c1',v['k']**alpha/(R*D)),('ca',-v['k']**alpha/(R*D)-dk)]:
                        np.testing.assert_allclose((hi[name]-lo[name])/(2*h),deriv,rtol=1e-8,atol=1e-8)
                    # Include terminal disinvestment, not extra GDP, in the final trade balance.
                    tb2=q2+A*v['k']**alpha-v['c2']+(1-delta)*v['k']
                    ca2=tb2+(R-1)*v['b1']
                    np.testing.assert_allclose(ca2,-v['b1'],atol=1e-12)
                    count+=1
    for A,k,c,b in [(1.,.25,2.125,-.375),(1.4,.49,2.245,-.735)]:
        v=m.project(A=A)
        np.testing.assert_allclose([v['k'],v['c1'],v['b1']],[k,c,b],atol=1e-12)
    print(f'{count} independent joint consumption/capital optima, project derivatives and settlement accounts: passed')


def check_finite_and_infinite():
    rng=np.random.default_rng(15)
    for T in [2,3,7,20]:
        for R in [.95,1.05,1.2]:
            q=rng.uniform(1.,3.,T);c=rng.uniform(.8,2.,T);b0=.25
            b=b0
            for y,spend in zip(q,c):b=R*b+y-spend
            discount=R**(-np.arange(1,T+1,dtype=float))
            np.testing.assert_allclose(np.dot(c,discount)+b/R**T,b0+np.dot(q,discount),atol=2e-12)
            beta=.94;sigma=1.4;g=(beta*R)**(1/sigma)
            C1=(R*b0+np.dot(q,R**(-np.arange(T,dtype=float))))/sum((g/R)**j for j in range(T))
            cons=C1*g**np.arange(T); b=b0
            for y,spend in zip(q,cons):b=R*b+y-spend
            np.testing.assert_allclose(b,0.,atol=3e-11)
            np.testing.assert_allclose(cons[:-1]**(-sigma),beta*R*cons[1:]**(-sigma),rtol=1e-12)
    R=1.05;N=1600;t=np.arange(1,N+1,dtype=float);disc=R**(-t);Delta=.3
    # Annuity responses from independently summed discounted endowments.
    for h in [1,3,12]:
        news=np.where(t==h,Delta,0.)
        permanent=np.where(t>=h,Delta,0.)
        np.testing.assert_allclose((R-1)*np.dot(news,disc),(R-1)*Delta/R**h,rtol=1e-12)
        np.testing.assert_allclose((R-1)*np.dot(permanent,disc),Delta*R**(1-h),rtol=1e-12)
    # Stable discounted recursion avoids numerical instability of debt levels at a long horizon.
    q=2.+.3*np.exp(-t/8.);b0=-.8
    cbar=(R-1)*(b0+np.dot(q,disc))
    discounted=b0+np.cumsum((q-cbar)*disc)
    np.testing.assert_allclose(discounted[-1],0.,atol=2e-14)
    debt=-.4
    discounted_rollover=[]
    for horizon in range(1,31):
        debt=R*debt
        discounted_rollover.append(debt/R**horizon)
    np.testing.assert_allclose(discounted_rollover,-.4,atol=1e-14)
    assert discounted_rollover[-1]<0  # pure rollover violates the no-Ponzi limit
    print('12 finite-horizon telescoping/Euler/settlement checks and 7 infinite-horizon annuity/limit checks: passed')


def check_credit_limits():
    count=0;binding=0
    for q1,q2 in [(1.,3.),(3.,1.),(.8,2.4)]:
        for R in [.9,1.1]:
            for sigma in [1.,2.]:
                for debtcap in [0.,.4,2.]:
                    beta=.95;v=m.allocation(q1,q2,R,beta,sigma)
                    cap=q1+debtcap;W=q1+q2/R
                    analytic=min(v['c1'],cap)
                    ceiling=min(cap,W-1e-10)
                    direct=minimize_scalar(lambda c:-utility(c,sigma)-beta*utility(q2+R*(q1-c),sigma),
                                           bounds=(1e-10,ceiling),method='bounded',options={'xatol':1e-13})
                    np.testing.assert_allclose(analytic,direct.x,rtol=2e-7,atol=2e-7)
                    c2=q2+R*(q1-analytic);mu=analytic**(-sigma)-beta*R*c2**(-sigma)
                    assert mu>=-1e-12
                    np.testing.assert_allclose(mu*(cap-analytic),0.,atol=1e-12)
                    if v['c1']>cap:
                        assert c2>0 and mu>0
                        h=1e-6
                        higher=min(v['c1'],q1+debtcap+h)
                        np.testing.assert_allclose((higher-analytic)/h,1.,atol=2e-9)
                        binding+=1
                    count+=1
    np.testing.assert_allclose(1/1.4-1/2.6,.32967032967032966,atol=1e-14)
    print(f'{count} constrained direct optimizations, KKT checks and {binding} binding liquidity responses: passed')


def check_accounts():
    rng=np.random.default_rng(150)
    for _ in range(100):
        C,G,I,TB,NPI,NCT=rng.normal(size=6)
        Y=C+G+I+TB;GNDI=Y+NPI+NCT;S=GNDI-C-G
        CA=TB+NPI+NCT
        np.testing.assert_allclose(S-I,CA,atol=1e-12)
        A0,L0=rng.uniform(50,100,2);KA,assetflow,valA,valL,ocA,ocL=rng.normal(size=6)
        # Enforce current+capital = financial, then independently reconstruct gross stocks.
        liabilityflow=assetflow-CA-KA
        A1=A0+assetflow+valA+ocA;L1=L0+liabilityflow+valL+ocL
        np.testing.assert_allclose((A1-L1)-(A0-L0),CA+KA+valA-valL+ocA-ocL,atol=5e-14)
        # Reserve-flow sign for the later IS-LM-BP bridge.
        privateFA=rng.normal();reserves=CA-privateFA
        np.testing.assert_allclose(CA+(-privateFA),reserves,atol=1e-12)
    assert (117-92)-(100-80)==-5+(12-2)==5
    print('100 saving/investment, gross stock-flow/valuation and reserve-sign reconciliations: passed')


if __name__=='__main__':
    check_allocation()
    check_shocks_and_returns()
    check_projects()
    check_finite_and_infinite()
    check_credit_limits()
    check_accounts()
