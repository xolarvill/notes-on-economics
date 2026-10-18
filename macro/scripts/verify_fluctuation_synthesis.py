"""Check the synthesis chapter's new state-memory and welfare calculations.
Run: .venv/bin/python macro/scripts/verify_fluctuation_synthesis.py
"""
import sys
sys.dont_write_bytecode=True
import importlib.util
import numpy as np
spec=importlib.util.spec_from_file_location('sw','macro/images/sticky_wage_responses.py')
sw=importlib.util.module_from_spec(spec);spec.loader.exec_module(sw)
count=0
for G in [0.,.3,.8260096344872536,.95]:
 for rho in [0.,.3,.5,.8260096344872536,.95]:
  e=.001;J=-.04277639340371418;gprev=0.
  for t in range(25):
   g=G*gprev+J*e*rho**t
   exact=J*e*(t+1)*G**t if G==rho else J*e*(G**(t+1)-rho**(t+1))/(G-rho)
   np.testing.assert_allclose(g,exact,atol=1e-15)
   gprev=g;count+=1
print(count,'recursive versus closed-form contract-memory values passed, including equal roots.')
for rho in [0.,.5,.9]:
 for pp in [1.1,1.5,2.]:
  path,sol=sw.response(tp=0,tw=0,rho=rho,pp=pp,horizon=12)
  nu=.001*rho**np.arange(13)
  inflation=-nu/(pp-rho)
  rate=-rho*nu/(pp-rho)
  np.testing.assert_allclose(path[:,0],0,atol=1e-12)
  np.testing.assert_allclose(path[:,1],inflation,atol=1e-12)
  np.testing.assert_allclose(path[:,6],rate,atol=1e-12)
print('9 independently solved flexible-contract neutrality and nominal-adjustment cases passed.')
chi=.9;hours=.8
for phi in [.5,1.,1.5,2.]:
 def burden(z):
  return chi*hours**(1+phi)*((1+z)**(1+phi)+(1-z)**(1+phi))/(2*(1+phi))
 baseline=burden(0)
 assert burden(.1)>baseline
 # The symmetric allocation's second derivative gives the displayed welfare term.
 step=1e-4
 second=(burden(step)-2*baseline+burden(-step))/step**2
 np.testing.assert_allclose(second,chi*phi*hours**(1+phi),rtol=1e-6)
 if phi in [.5,1.5]:
  errors=[]
  for z in [.1,.05]:
   approx=baseline+chi*phi*hours**(1+phi)*z**2/2
   errors.append(abs(burden(z)-approx))
  assert 15<errors[0]/errors[1]<17
print('4 uneven-hours welfare derivatives and symmetric Taylor-error checks passed.')
