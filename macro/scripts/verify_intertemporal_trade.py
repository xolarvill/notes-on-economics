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


if __name__=='__main__':
    check_allocation()
