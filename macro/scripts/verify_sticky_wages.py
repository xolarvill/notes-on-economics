"""Independent primitive and equilibrium checks for the sticky-wage chapter.
Run from repository root: .venv/bin/python macro/scripts/verify_sticky_wages.py
"""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import numpy as np
from scipy.optimize import minimize,minimize_scalar
spec=importlib.util.spec_from_file_location('sw','macro/images/sticky_wage_responses.py')
sw=importlib.util.module_from_spec(spec);spec.loader.exec_module(sw)
rng=np.random.default_rng(620)
for J in [3,6,9]:
 for epsilon in [2.,6.,10.]:
  W=rng.uniform(.5,2,J);r=(epsilon-1)/epsilon;N=1.1
  index=np.mean(W**(1-epsilon))**(1/(1-epsilon))
  demand=(W/index)**(-epsilon)*N
  agg=lambda n:np.mean(n**r)**(1/r)
  opt=minimize(lambda n:np.mean(W*n),np.full(J,N),method='SLSQP',
      bounds=[(1e-8,None)]*J,constraints={'type':'ineq','fun':lambda n:agg(n)-N},
      options={'ftol':1e-12,'maxiter':300})
  assert opt.success
  np.testing.assert_allclose(np.mean(W*opt.x),index*N,rtol=1e-8)
  np.testing.assert_allclose(agg(demand),N,rtol=1e-12)
print('9 independent CES labor optimizations passed.')
for phi in [0.,.5,1.,2.]:
 epsilon=6.;mu=epsilon/(epsilon-1);chi=1/mu;sigma=1.3
 k=np.arange(140);bw=(.99*.75)**k
 W,P,C,N,xi=[np.exp(rng.normal(0,.02,len(k))) for _ in range(5)]
 lam=xi*C**(-sigma)/P
 reset=(mu*chi*np.sum(bw*xi*W**(epsilon*(1+phi))*N**(1+phi))
                /np.sum(bw*lam*W**epsilon*N))**(1/(1+epsilon*phi))
 def objective(z):
  n=(z/W)**(-epsilon)*N
  return np.sum(bw*(lam*z*n-xi*chi*n**(1+phi)/(1+phi)))
 opt=minimize_scalar(lambda z:-objective(z),bounds=(.5,1.6),method='bounded',options={'xatol':1e-12})
 np.testing.assert_allclose(reset,opt.x,rtol=2e-7)
 n=(reset/W)**(-epsilon)*N
 foc=np.sum(bw*n*((1-epsilon)*lam+epsilon*xi*chi*n**phi/reset))
 assert abs(foc)<1e-10
 # Primitive chain-rule derivative, evaluated away from the optimum.
 z=reset*1.02;dh=1e-6;n=(z/W)**(-epsilon)*N
 derivative=np.sum(bw*n*((1-epsilon)*lam+epsilon*xi*chi*n**phi/z))
 np.testing.assert_allclose((objective(z+dh)-objective(z-dh))/(2*dh),derivative,rtol=1e-7)
 # Local reset-wage approximation against the exact nonlinear formula.
 w,p,c,nn,q=[rng.normal(size=len(k)) for _ in range(5)]
 errors=[]
 for step in [.001,.0005,.00025]:
  W,P,C,N,xi=[np.exp(step*z) for z in [w,p,c,nn,q]]
  lam=xi*C**(-sigma)/P
  exact=np.log((mu*chi*np.sum(bw*xi*W**(epsilon*(1+phi))*N**(1+phi))
                   /np.sum(bw*lam*W**epsilon*N))**(1/(1+epsilon*phi)))
  linear=step*np.sum(bw*(p+sigma*c+phi*nn+epsilon*phi*w))/(np.sum(bw)*(1+epsilon*phi))
  errors.append(abs(exact-linear))
 assert 3.7<errors[0]/errors[1]<4.3,errors
 for exponent in [epsilon,epsilon*(1+phi)]:
  errors=[]
  for step in [.001,.0005,.00025]:
   reset=np.exp(step);theta=.75
   index=((1-theta)*reset**(1-epsilon)+theta)**(1/(1-epsilon))
   dispersion=(1-theta)*(reset/index)**(-exponent)+theta*(1/index)**(-exponent)
   errors.append(abs(dispersion-1))
  assert 3.7<errors[0]/errors[1]<4.3,errors
print('4 nonlinear wage optima, primitive derivatives, and quadratic error orders passed.')
count=0
for sigma in [.5,1.]:
 for phi in [.5,1.]:
  for alpha in [0.,1/3]:
   for tp in [.5,.75,.9]:
    for tw in [.5,.75,.9]:
     for rho in [0.,.5,.9]:
      sw.solve(sigma=sigma,phi=phi,alpha=alpha,tp=tp,tw=tw,rho=rho)
      count+=1
print(count,'scalar-polynomial / generalized-eigenvalue policy checks passed.')
# Independent finite-horizon block system using (x, pi_p, pi_w, current g).
for tp,tw in [(.75,.75),(.75,0),(0,.75),(0,0)]:
 T=100;size=4*(T+1);matrix=np.zeros((size,size));rhs=np.zeros(size)
 par=sw.coefficients(tp=tp,tw=tw)
 b,s,ap,aw,gp,gw,pp,px=[par[k] for k in ['beta','sigma','ap','aw','gp','gw','pp','px']]
 for t in range(T+1):
  row=4*t
  matrix[row:row+4,row:row+4]=[[s+px,pp,0,0],[-ap*gp,1,0,-ap],[-aw*gw,0,1,aw],[0,1,-1,1]]
  rhs[row]=-.001*.5**t
  if tp==0:matrix[row+1,row:row+4]=[gp,0,0,1]
  if tw==0:matrix[row+2,row:row+4]=[-gw,0,0,1]
  if t<T:
   matrix[row,row+4]=-s;matrix[row,row+5]=-1
   if tp:matrix[row+1,row+5]=-b
   if tw:matrix[row+2,row+6]=-b
  if t:matrix[row+3,row-1]=-1
 direct=np.linalg.solve(matrix,rhs).reshape(-1,4)
 path,sol=sw.response(tp=tp,tw=tw,horizon=T)
 np.testing.assert_allclose(direct[:12,:],path[:12,:4],atol=1e-10)
 if tp==tw==0:
  np.testing.assert_allclose(path[:,0],0,atol=1e-12)
  np.testing.assert_allclose(path[:,1],-.001*.5**np.arange(T+1)/(1.5-.5),atol=1e-12)
print('4 independently solved finite-horizon boundary systems passed, including both-flexible neutrality.')
# Reference identities with both constant markups.
for alpha in [0.,1/3,.7]:
 sigma=1.3;phi=.8;chi=.9;mu=6/5;gamma=sigma+(phi+alpha)/(1-alpha)
 for A in [.9,1.,1.1]:
  Y=((1-alpha)/(chi*mu**2)*A**((1+phi)/(1-alpha)))**(1/gamma)
  N=(Y/A)**(1/(1-alpha))
  wage=mu*chi*Y**sigma*N**phi
  np.testing.assert_allclose(wage,(1-alpha)/mu*A*N**(-alpha))
print('9 natural-allocation accounting and markup identities passed.')
# Original source is literal, recoverable comparison material.
s=Path('macro/chapters/sticky-wages.tex').read_text()
archive=s.split('% BEGIN ORIGINAL STICKY WAGE COURSE TEXT (comparison only)\n')[1].split('\n% END ORIGINAL STICKY WAGE COURSE TEXT')[0]
original='\n'.join(x[2:] if x.startswith('% ') else '' for x in archive.splitlines())+'\n'
EXPECTED_ORIGINAL_SHA256='e88a98bb5f8b6b9ede674ab3a350b3f20f192634cc186e3f17ebd590a57dd4ad'
assert hashlib.sha256(original.encode()).hexdigest()==EXPECTED_ORIGINAL_SHA256
print('Original sticky-wage course archive verified; all checks passed.')
