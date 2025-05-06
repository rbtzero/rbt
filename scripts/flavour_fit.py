import numpy as np
from scipy.optimize import minimize

# ----------------------------
# Experimental reference data
# ----------------------------
PDG_MASS_GEV = {
    # up-type quarks
    'u': 0.00216,
    'c': 1.27,
    't': 172.7,
    # down-type quarks
    'd': 0.00467,
    's': 0.093,
    'b': 4.18,
    # charged leptons
    'e': 0.000511,
    'mu': 0.1057,
    'tau': 1.777,
}

PDG_CKM = {
    'Vus': 0.2243,
    'Vcb': 0.0410,
    'Vub': 0.0036,
}

# ----------------------------
# Integer winding numbers k_i
# ----------------------------
# Up-type quarks (u,c,t), Down-type quarks (d,s,b), Charged leptons (e,mu,tau)
K_UP   = {'u': 14, 'c': 11, 't': 0}
K_DOWN = {'d': 14, 's': 11, 'b': 0}
K_LEP  = {'e': 14, 'mu': 11, 'tau': 0}


# ------------------------------------------
# Model: masses and CKM mixing from {η,ξ,χ,λ}
# ------------------------------------------

def mass_formula(k: int, eta: float, xi: float, chi: float) -> float:
    """m(k) = η · exp(−ξ k² − χ k)  [GeV]"""
    return eta * np.exp(-xi * k**2 - chi * k)


def predicted_masses(params):
    """Return dict of model masses for the nine charged fermions."""
    eta, xi, chi, _lambda = params  # λ not used for masses

    masses = {}
    for name, k in K_UP.items():
        masses[name] = mass_formula(k, eta, xi, chi)
    for name, k in K_DOWN.items():
        masses[name] = mass_formula(k, eta, xi, chi)
    for name, k in K_LEP.items():
        masses[name] = mass_formula(k, eta, xi, chi)
    return masses


def gaussian_overlap(k_i: int, k_j: int, lam: float) -> float:
    """Return unnormalised overlap amplitude exp(−λ Δk²)."""
    return np.exp(-lam * (k_i - k_j) ** 2)


def predicted_CKM(params):
    """Return dict with |Vus|, |Vcb|, |Vub| from Gaussian overlaps."""
    eta, xi, chi, lam = params
    # Build unnormalised matrix in generation order (u,c,t) rows ; (d,s,b) cols
    k_up_vec   = [K_UP['u'], K_UP['c'], K_UP['t']]
    k_down_vec = [K_DOWN['d'], K_DOWN['s'], K_DOWN['b']]
    M = np.zeros((3, 3))
    for i, ku in enumerate(k_up_vec):
        for j, kd in enumerate(k_down_vec):
            M[i, j] = gaussian_overlap(ku, kd, lam)
    # Row-normalise to unit L2 norm (approximate unitarity)
    row_norms = np.linalg.norm(M, axis=1, keepdims=True)
    V = M / row_norms
    return {
        'Vus': abs(V[0, 1]),
        'Vcb': abs(V[1, 2]),
        'Vub': abs(V[0, 2]),
    }


# ------------------------------------------
# Cost function for optimisation
# ------------------------------------------

def cost_function(params):
    masses = predicted_masses(params)
    ckm    = predicted_CKM(params)

    # Log-space mass errors (gives equal weight per decade)
    mass_err2 = 0.0
    for name, m_exp in PDG_MASS_GEV.items():
        m_th = masses[name]
        mass_err2 += (np.log(m_th) - np.log(m_exp)) ** 2

    # CKM fractional errors
    ckm_err2 = 0.0
    for key, val_exp in PDG_CKM.items():
        val_th = ckm[key]
        ckm_err2 += ((val_th - val_exp) / val_exp) ** 2

    # Weight CKM so that typical contributions match
    return mass_err2 + 10.0 * ckm_err2


# --------------------------
# Fit parameters to the data
# --------------------------

initial_guess = np.array([
    1.0,   # η [GeV]
    0.10,  # ξ
    0.10,  # χ
    1.00,  # λ
])

result = minimize(cost_function, initial_guess, method='Nelder-Mead', options={'maxiter': 10000, 'xatol': 1e-9, 'fatol': 1e-9})

eta_opt, xi_opt, chi_opt, lam_opt = result.x

# --------------------------
# Pretty-print the outcome
# --------------------------
print("Optimisation successful:", result.success, "in", result.nit, "iterations\n")
print(f"η  = {eta_opt:.6e} GeV")
print(f"ξ  = {xi_opt:.6e}")
print(f"χ  = {chi_opt:.6e}")
print(f"λ  = {lam_opt:.6e}\n")

masses_opt = predicted_masses(result.x)
ckm_opt    = predicted_CKM(result.x)

# Helper for aligned printing
names_up   = ['u', 'c', 't']
names_down = ['d', 's', 'b']
names_lept = ['e', 'mu', 'tau']

print("Mass spectrum (GeV):")
for group_name, names in [('Up-type quarks', names_up),
                          ('Down-type quarks', names_down),
                          ('Charged leptons', names_lept)]:
    m_th_list  = [masses_opt[n] for n in names]
    m_exp_list = [PDG_MASS_GEV[n] for n in names]
    ratio_list = [m_th / m_exp for m_th, m_exp in zip(m_th_list, m_exp_list)]

    th_str  = ', '.join([f"{n}={m_th:.3g}" for n, m_th in zip(names, m_th_list)])
    exp_str = ', '.join([f"{n}={m_exp:.3g}" for n, m_exp in zip(names, m_exp_list)])
    ratio_str = ', '.join([f"{n}={r:.2f}" for n, r in zip(names, ratio_list)])
    print(f"{group_name}:  {th_str}\n               PDG:  {exp_str}\n            Ratio:  {ratio_str}\n")

print("Key CKM elements:")
for key, val_exp in PDG_CKM.items():
    val_th = ckm_opt[key]
    ratio  = val_th / val_exp
    print(f"|{key}| = {val_th:.4f}  (exp: {val_exp:.4f},  ratio: {ratio:.2f})")

print("\nTotal χ²-like cost =", cost_function(result.x)) 