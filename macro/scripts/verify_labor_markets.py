"""Independent primitive, flow, bargaining, and equilibrium checks for Chapter 13.
Run: .venv/bin/python macro/scripts/verify_labor_markets.py
"""
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path
from dataclasses import replace
from itertools import product
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize_scalar, root

module_path = Path(__file__).resolve().parents[1]/'images/labor_market_matching.py'
spec = importlib.util.spec_from_file_location('labor_market_matching', module_path)
model = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = model
spec.loader.exec_module(model)
p0 = model.Parameters()

for f, s, dt in product([.03, .4, 1.2], [.01, .15], [.1, 1., 3.]):
    Q = np.array([[-f, f], [s, -s]])
    transition = expm(Q*dt)
    expected = np.array([[1-f/(s+f)*(1-np.exp(-(s+f)*dt)), f/(s+f)*(1-np.exp(-(s+f)*dt))],
                         [s/(s+f)*(1-np.exp(-(s+f)*dt)), 1-s/(s+f)*(1-np.exp(-(s+f)*dt))]])
    np.testing.assert_allclose(transition, expected, atol=2e-14)
    for u0 in [.02, .2, .8]:
        observed = np.array([u0, 1-u0])@transition
        u = s/(s+f)+(u0-s/(s+f))*np.exp(-(s+f)*dt)
        np.testing.assert_allclose(observed[0], u, atol=2e-14)
    mean, _ = quad(lambda a: np.exp(-f*a), 0, np.inf)
    np.testing.assert_allclose(mean, 1/f, rtol=1e-10)
print('18 Markov-matrix transition cases and 54 unemployment-stock paths passed; waiting-time integrals agree.')

for k, xi, eta in product([.15, .5, 1.], [.3, .5, .7], [.3, .5, .7]):
    p = replace(p0, k=k, xi=xi, eta=eta)
    st = model.steady(p)
    U, W = np.linalg.solve([[p.r+st['f'], -st['f']], [-p.s, p.r+p.s]], [p.b, st['w']])
    np.testing.assert_allclose([U, W, W-U], [st['U'], st['W'], st['D']], rtol=2e-11)
    np.testing.assert_allclose(st['q']*st['J'], p.k, rtol=2e-12)
    np.testing.assert_allclose(st['f']*st['u'], p.s*(1-st['u']), rtol=1e-13)
    np.testing.assert_allclose(st['f']*st['u'], st['q']*st['v'], rtol=1e-13)
    # Direct Nash optimization treats this individual pair's outside value as fixed.
    def neg_log_nash(w):
        d = (w-p.r*U)/(p.r+p.s)
        j = (p.z-w)/(p.r+p.s)
        if min(d, j) <= 0: return np.inf
        return -p.eta*np.log(d)-(1-p.eta)*np.log(j)
    optimum = minimize_scalar(neg_log_nash, bounds=(p.r*U+1e-10, p.z-1e-10),
                              method='bounded', options={'xatol': 1e-13})
    np.testing.assert_allclose(optimum.x, st['w'], rtol=1e-7)
    # Solve the two primitive wage/entry equations jointly, not their scalar reduction.
    def equations(arr):
        th = np.exp(arr[0]); wage = arr[1]
        f = p.A*th**(1-p.xi); q = p.A*th**(-p.xi)
        D = (wage-p.b)/(p.r+p.s+f)
        J = (p.z-wage)/(p.r+p.s)
        return [q*J-p.k, (1-p.eta)*D-p.eta*J]
    sol = root(equations, [np.log(st['th'])+.05, st['w']-.001])
    assert sol.success
    np.testing.assert_allclose([np.exp(sol.x[0]), sol.x[1]], [st['th'], st['w']], rtol=1e-8)
    np.testing.assert_allclose(st['C'], st['w']*(1-st['u'])+p.b*st['u']
                               +(p.z-st['w'])*(1-st['u'])-p.k*st['v'], atol=2e-15)
print('27 stationary equilibria agree with direct bargaining optimization, worker Bellman systems, joint entry/sharing roots, and resource accounts.')
