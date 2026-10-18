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

for xi, eta in product([.3, .5, .7], [.3, .7]):
    p = replace(p0, xi=xi, eta=eta)
    st = model.steady(p); th = st['th']
    slope = p.k*(p.r+p.s)*p.xi/p.A*th**(p.xi-1)+p.eta*p.k
    formulas = {'z': (1-p.eta)/slope, 'b': -(1-p.eta)/slope,
                'k': -((p.r+p.s)/st['q']+p.eta*th)/slope,
                's': -(p.k/st['q'])/slope,
                'A': p.k*(p.r+p.s)*th**p.xi/(p.A**2*slope),
                'eta': -(p.k*th+p.z-p.b)/slope}
    for key, derivative in formulas.items():
        h = 1e-5*getattr(p, key)
        plus = model.steady(replace(p, **{key: getattr(p, key)+h}))['th']
        minus = model.steady(replace(p, **{key: getattr(p, key)-h}))['th']
        np.testing.assert_allclose((plus-minus)/(2*h), derivative, rtol=1e-7)
print('36 implicit comparative-static derivatives agree with independently re-solved equilibria.')

for xi, k, u0 in product([.3, .5, .7], [.3, .8], [.02, .1, .35]):
    p = replace(p0, xi=xi, k=k)
    def welfare(log_th):
        th = np.exp(log_th); f = p.A*th**(1-p.xi); ubar = p.s/(p.s+f)
        return p.z/p.r-(p.z-p.b+p.k*th)*(ubar/p.r+(u0-ubar)/(p.r+p.s+f))
    optimum = minimize_scalar(lambda x: -welfare(x), bounds=(-7, 4), method='bounded',
                              options={'xatol': 1e-12})
    th_opt = np.exp(optimum.x)
    planner = model.steady(p, planner=True)
    np.testing.assert_allclose(th_opt, planner['th'], rtol=3e-6)
    efficient = model.steady(replace(p, eta=xi))
    np.testing.assert_allclose(efficient['th'], planner['th'], rtol=1e-12)
    for eta in [.2, .8]:
        private = model.steady(replace(p, eta=eta))
        assert welfare(np.log(private['th'])) < welfare(np.log(planner['th']))+1e-10
    # Numerical integration of primitive consumption checks the welfare formula.
    th = planner['th']; f = planner['f']; ubar = planner['u']
    value, _ = quad(lambda t: np.exp(-p.r*t)*(p.z-(p.z-p.b+p.k*th)
                    *(ubar+(u0-ubar)*np.exp(-(p.s+f)*t))), 0, np.inf)
    np.testing.assert_allclose(value, welfare(np.log(th)), rtol=2e-10)
print('18 direct resource-welfare optimizations reproduce the planner/Hosios allocation at different initial employment stocks.')

base = model.steady()
for kind in ('productivity', 'matching', 'separations'):
    path = model.transition(kind, end=36.)
    shorter = model.transition(kind, horizon=120., end=36.)
    for key in ('S','th','u','w','Y'):
        np.testing.assert_allclose(path[key], shorter[key], atol=2e-10, rtol=2e-10)
    # Independently price labor/home cash flows and firm cash flows, given the path.
    def asset_rhs(t, values):
        U, W, J = values
        S = path['backward'].sol(t)[0]
        z, A, s, th, f = path['market'](t, S)
        w = (1-p0.eta)*p0.b+p0.eta*(z+p0.k*th)
        return [p0.r*U-p0.b-f*(W-U),
                p0.r*W-w+s*(W-U), (p0.r+s)*J-z+w]
    assets = solve_ivp(asset_rhs, (240., 0.), [base['U'], base['W'], base['J']],
                       method='DOP853', rtol=2e-12, atol=1e-11, max_step=.25, dense_output=True)
    assert assets.success
    U, W, J = assets.sol(path['t'])
    np.testing.assert_allclose(J, path['J'], atol=3e-9, rtol=3e-9)
    np.testing.assert_allclose(W-U, path['D'], atol=3e-9, rtol=3e-9)
    # Independent integrating-factor quadrature of the unemployment path.
    def rates(t):
        S = path['backward'].sol(t)[0]
        z, A, s, th, f = path['market'](t, S)
        return s, f
    def K_between(a,b):
        return quad(lambda t: sum(rates(t)), a, b, epsabs=1e-10)[0]
    for t in [.5, 2., 5., 12.]:
        u = np.exp(-K_between(0,t))*base['u']
        u += quad(lambda a: np.exp(-K_between(a,t))*rates(a)[0], 0, t, epsabs=1e-11)[0]
        np.testing.assert_allclose(u, path['forward'].sol(t)[0], atol=1e-10, rtol=1e-9)
    assert path['u'][0] == base['u']
    assert path['th'][0] < base['th']
    assert np.argmax(path['u']) > 0
    assert np.all(path['J'] > 0) and np.all(path['D'] > 0) and np.all(path['C'] > 0)
print('3 nonlinear transitions pass independent worker/firm asset integrations, 12 integrating-factor quadratures, and doubled terminal horizons.')

# Check the complete three-state accounting, including the changing denominator.
rng = np.random.default_rng(31013)
for _ in range(40):
    E,U,O = rng.uniform(.05,1,3)
    eu,eo,ue,uo,oe,ou = rng.uniform(.001,.2,6)
    dE = ue*U+oe*O-(eu+eo)*E
    dU = eu*E+ou*O-(ue+uo)*U
    dO = eo*E+uo*U-(oe+ou)*O
    np.testing.assert_allclose(dE+dU+dO,0,atol=2e-16)
    L = E+U; u = U/L; dL = (oe+ou)*O-eo*E-uo*U
    formula = eu*(1-u)+ou*O/L-(ue+uo)*u-u*dL/L
    derivative = (dU*L-U*(dE+dU))/L**2
    np.testing.assert_allclose(formula,derivative,atol=2e-16)
    generator = np.array([[-eu-eo,eu,eo], [ue,-ue-uo,uo], [oe,ou,-oe-ou]])
    h = 1e-4
    before = np.array([E,U,O])@expm(-h*generator)
    after = np.array([E,U,O])@expm(h*generator)
    finite = (after[1]/sum(after[:2])-before[1]/sum(before[:2]))/(2*h)
    np.testing.assert_allclose(finite,formula,atol=5e-10,rtol=5e-7)
print('40 three-state population and unemployment-denominator identities passed.')

# Numbers printed in the chapter must refer to the solved variants, not reused wages.
text = (module_path.parents[1]/'chapters/labor-markets.tex').read_text()
for st in [base, model.steady(replace(p0,z=.995)),
           model.steady(replace(p0,z=.995),fixed_wage=base['w'])]:
    assert f"{st['th']:.6f}".lstrip('0') in text
    assert f"{st['w']:.6f}".lstrip('0') in text
    assert f"{100*st['u']:.4f}" in text
for kind in ('productivity','matching','separations'):
    path=model.transition(kind)
    i=np.argmax(path['u'])
    assert f"{100*(path['th'][0]/base['th']-1):.4f}" in text
    assert f"{100*path['u'][i]:.4f}" in text
    assert f"{path['t'][i]:.2f}" in text
print('All reported stationary and transition table values verified; all Chapter 13 checks passed.')
