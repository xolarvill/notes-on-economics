"""Independent checks of the chapter's nonlinear primitives and local equations.

Run from the repository root: .venv/bin/python macro/scripts/verify_new_keynesian.py
Requires numpy and scipy in the project's uv-managed environment.
"""
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
import hashlib
import numpy as np
from scipy.optimize import minimize, minimize_scalar
spec=importlib.util.spec_from_file_location('nk','macro/images/nk_impulse_responses.py')
nk=importlib.util.module_from_spec(spec); spec.loader.exec_module(nk)
rng=np.random.default_rng(1729)
checks={}
# Finite J CES duality versus direct constrained optimization, not reduced demands.
for J in [2,4,7]:
    for eps in [2.,6.,10.]:
        prices=rng.uniform(.5,2,J); C=1.2; r=(eps-1)/eps
        P=J*np.mean(prices**(1-eps))**(1/(1-eps))
        q=(J*prices/P)**(-eps)*C
        agg=lambda z: np.mean(z**r)**(1/r)
        opt=minimize(lambda z: prices@z,np.full(J,C),bounds=[(1e-8,None)]*J,
                     constraints={'type':'ineq','fun':lambda z: agg(z)-C},
                     method='SLSQP',options={'ftol':1e-12,'maxiter':200})
        assert opt.success, opt.message
        np.testing.assert_allclose(prices@opt.x,P*C,rtol=2e-8)
        np.testing.assert_allclose(agg(q),C,rtol=1e-12)
checks['CES primal-dual optimizations']=9
# Calvo implicit FOC and closed nonlinear solution, against actual profit max.
for alpha in [0.,1/3,.6]:
    beta=.99; theta=.75; eps=6.; sigma=1.5
    k=np.arange(120); weights=(beta*theta)**k
    Y=np.exp(rng.normal(0,.02,len(k))); P=np.exp(rng.normal(0,.01,len(k)))
    W=(1-alpha)*(eps-1)/eps*np.exp(rng.normal(0,.01,len(k)))
    A=np.exp(rng.normal(0,.01,len(k))); xi=np.exp(rng.normal(0,.01,len(k)))
    zeta=eps*alpha/(1-alpha)
    mc=W/(1-alpha)*A**(-1/(1-alpha))*Y**(alpha/(1-alpha))
    F=xi*Y**(1-sigma)*P**(eps-1)
    reset=(eps/(eps-1)*np.sum(weights*F*mc*P**zeta)/np.sum(weights*F))**(1/(1+zeta))
    def profit(z):
        demand=(z/P)**(-eps)*Y
        cost=W*(demand/A)**(1/(1-alpha))
        sdf=beta**k*xi*Y**(-sigma)/P # constants omitted equally
        return np.sum(theta**k*sdf*(z*demand-cost))
    opt=minimize_scalar(lambda z:-profit(z),bounds=(.8,1.2),method='bounded',options={'xatol':1e-12})
    np.testing.assert_allclose(opt.x,reset,rtol=1e-7)
    demand=(reset/P)**(-eps)*Y
    ownmc=W/(1-alpha)*A**(-1/(1-alpha))*demand**(alpha/(1-alpha))
    resid=np.sum(weights*F*((1-eps)+eps*ownmc/reset))
    assert abs(resid)<1e-12
    # Compare exact price with first-order formula; shrink all log disturbances.
    q0=rng.normal(size=len(k)); y0=rng.normal(size=len(k)); p0=rng.normal(size=len(k)); mc0=rng.normal(size=len(k))
    errs=[]
    for h in [.001,.0005,.00025]:
        PP=np.exp(h*p0); FF=np.exp(h*(q0+(1-sigma)*y0+(eps-1)*p0))
        MC=(eps-1)/eps*np.exp(h*mc0)
        exact=np.log((eps/(eps-1)*np.sum(weights*FF*MC*PP**zeta)/np.sum(weights*FF))**(1/(1+zeta)))
        lin=h*np.sum(weights*(mc0+zeta*p0))/(np.sum(weights)*(1+zeta))
        errs.append(abs(exact-lin))
    assert 3.7<errs[0]/errs[1]<4.3, errs
    assert 3.7<errs[1]/errs[2]<4.3, errs
checks['nonlinear Calvo optimization / quadratic approximation']=3
# Money opportunity-cost derivatives in gross and net-log units.
beta=.99; i0=1/beta-1; nu_m=2.; sigma=1.
f=lambda j: np.log((np.exp(j)/beta-1)/(np.exp(j)/beta))
h=1e-7
np.testing.assert_allclose((f(h)-f(-h))/(2*h),1/i0,rtol=1e-7)
checks['money derivative']=1
# Exact index aggregation and dispersion have quadratic local errors.
for alpha in [0.,1/3,.6]:
    eps=6.; theta=.75; hp=eps/(1-alpha); errs=[]
    for h in [.001,.0005,.00025]:
        new=np.exp(h)
        P=((1-theta)*new**(1-eps)+theta)**(1/(1-eps))
        Delta=(1-theta)*(new/P)**(-hp)+theta*(1/P)**(-hp)
        errs.append(abs(Delta-1))
    assert 3.8<errs[0]/errs[1]<4.2
checks['dispersion second order']=3
# Determinacy, original equations, and coefficient matching over many parameters.
count=0
for sigma in [.5,1.,2.]:
 for alpha in [0.,1/3,.6]:
  for theta in [.4,.75,.9]:
   for rho in [0.,.5,.95]:
    for pp in [.2,.9,1.,1.5,3.]:
     for px in [0.,.125,.5]:
      beta=.99; phi=1.; eps=6.
      kap=(1-theta)*(1-beta*theta)/theta*(1-alpha)/(1-alpha+eps*alpha)*(sigma+(phi+alpha)/(1-alpha))
      D=sigma+px+kap*pp
      Am=np.array([[sigma,1-beta*pp],[kap*sigma,kap+beta*(sigma+px)]])/D
      criterion=kap*(pp-1)+(1-beta)*px
      if abs(criterion)>1e-11:
       assert (np.max(np.abs(np.linalg.eigvals(Am)))<1)==(criterion>0)
      if criterion>1e-11:
       p=nk.solve_policy(sigma=sigma,alpha=alpha,theta=theta,rho=rho,phi_pi=pp,phi_x=px)
       v=np.array([p['ax'],p['bp']]); b=np.array([1,kap])/D
       direct=np.linalg.solve(np.eye(2)-rho*Am,-b)
       np.testing.assert_allclose(v,direct,rtol=1e-10)
      count+=1
checks['parameter / eigenvalue cases']=count
# Recover conditional AD-AS and check ALL four source equations.
for _ in range(100):
 sig=rng.uniform(.5,2); eta=rng.uniform(1,50); am=rng.uniform(.3,1.5); kap=rng.uniform(.01,.3); bet=.99
 d,m,e,past,yn=rng.normal(size=5)
 y=(m+sig*eta*d+(eta-bet)*e-past+kap*yn)/(sig*eta+am+kap)
 price=past+bet*e+kap*(y-yn)
 rate=am/eta*y-(m-price)/eta
 np.testing.assert_allclose(y,d-(rate-e)/sig,atol=1e-12)
 np.testing.assert_allclose(m-price,am*y-eta*rate,atol=1e-12)
 np.testing.assert_allclose(price,m+sig*eta*d+eta*e-(sig*eta+am)*y,atol=1e-12)
checks['conditional IS-LM / AD-AS cases']=100
# Household exact Euler residual along the local policy has second-order error.
p=nk.solve_policy(); errors=[]
for h in [1e-3,5e-4,2.5e-4]:
 x=p['ax']*h; xn=.5*x; pi=p['bp']*h; pin=.5*pi; j=p['jr']*h
 residual=np.exp(j)*np.exp(-(xn-x)-pin)-1
 errors.append(abs(residual))
# The deterministic conditional mean path is exactly compatible with exponential Euler
# for log utility and these coefficients, so check stochastic expectation separately.
assert max(errors)<1e-14
var=0.1 # a symmetric next-date innovation, scaled jointly with today's state
errors=[]
for h in [.01,.005,.0025]:
 x=p['ax']*h; j=p['jr']*h
 vals=[]
 for sign in [-1,1]:
  vn=.5*h+sign*var*h
  vals.append(np.exp(j-(p['ax']*vn-x)-p['bp']*vn))
 errors.append(abs(np.mean(vals)-1))
assert 3.99<errors[0]/errors[1]<4.01
checks['stochastic Euler quadratic error']=1
# Full original comments must decode exactly, byte-for-byte.
s=Path('macro/chapters/new-keynesian.tex').read_text()
archive=s.split('% BEGIN ORIGINAL NK COURSE TEXT (pre-revision; comparison only)\n')[1].split('\n% END ORIGINAL NK COURSE TEXT')[0]
restored='\n'.join(line[2:] if line.startswith('% ') else '' for line in archive.splitlines())+'\n'
assert hashlib.sha256(restored.encode()).hexdigest() == '9c0e2859c48a0312451506ec921056c7aa26671588581b7dcbf8c4f452515fe0'
print(checks)
print('All independent mathematical checks passed.')
