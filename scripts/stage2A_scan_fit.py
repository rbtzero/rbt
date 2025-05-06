"""stage2A_scan_fit.py

Robust Stage-2A implementation that searches integer k-triples and tunes the
four continuous parameters (η, ξ, χ, λ) to reproduce PDG masses + three CKM
entries.  It is deliberately SciPy-free to avoid NumPy/SciPy version
conflicts on Colab; the optimiser is a very small ad-hoc Nelder–Mead clone
based on `numpy` only.

How to run (Colab):
===================
```python
!python scripts/stage2A_scan_fit.py           # writes stage2A_lock.json
```
Output files
-----------
    stage2A_console.txt   – human readable summary (redirect if desired)
    stage2A_lock.json     – reproducibility artefact consumed by CI

The script needs only NumPy ≥ 1.23 (< 3.0).  No SciPy, no other deps.
"""
from __future__ import annotations

import itertools
import json
import math
import os
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

# -----------------------------------------------------------------------------
# PDG reference numbers (GeV) – 2024 central values
# -----------------------------------------------------------------------------
PDG_MASS_GEV = {
    'u': 0.00216,  'c': 1.27,   't': 172.7,
    'd': 0.00467,  's': 0.093,  'b': 4.18,
    'e': 0.000511, 'mu': 0.1057,'tau': 1.777,
}
PDG_CKM = {'Vus': 0.2243, 'Vcb': 0.0410, 'Vub': 0.0036}

# Target accuracy gates (Stage-2A spec)
MASS_THR   = 2.0   # factor ≤ 2×
CKM_FRAC_T = 0.15  # ≤ 15 % off

# Integer k search grid
K_MIN, K_MAX = 0, 18
MIN_SPAN     = 4   # k_high − k_low ≥ 4 ensures > 2.5 orders magnitude

np.random.seed(42)  # full determinism

# -----------------------------------------------------------------------------
# Model definitions
# -----------------------------------------------------------------------------

def mass_formula(k: int, eta: float, xi: float, chi: float) -> float:
    """m(k) = η · exp(−ξ k² − χ k)."""
    return eta * math.exp(-xi * k**2 - chi * k)


def gaussian_overlap(ki: int, kj: int, lam: float) -> float:
    """|V_ij| kernel before row normalisation."""
    return math.exp(-lam * (ki - kj) ** 2)


def calc_masses(k_triplet: Tuple[int, int, int], params: np.ndarray) -> Dict[str, float]:
    eta, xi, chi, _ = params
    kl, km, kh = k_triplet
    k_up   = {'u': kl, 'c': km, 't': kh}
    k_down = {'d': kl, 's': km, 'b': kh}
    k_lep  = {'e': kl, 'mu': km, 'tau': kh}

    masses = {}
    for name, k in {**k_up, **k_down, **k_lep}.items():
        masses[name] = mass_formula(k, eta, xi, chi)
    return masses


def calc_ckm(k_triplet: Tuple[int, int, int], params: np.ndarray) -> Dict[str, float]:
    eta, xi, chi, lam = params
    kl, km, kh = k_triplet
    k_up_vec   = [kl, km, kh]
    k_down_vec = [kl, km, kh]

    M = np.zeros((3, 3))
    for i, ku in enumerate(k_up_vec):
        for j, kd in enumerate(k_down_vec):
            M[i, j] = gaussian_overlap(ku, kd, lam)
    V = M / np.linalg.norm(M, axis=1, keepdims=True)
    return {'Vus': abs(V[0, 1]), 'Vcb': abs(V[1, 2]), 'Vub': abs(V[0, 2])}

# -----------------------------------------------------------------------------
# Minimal Nelder–Mead (2-D code adapted to 4-D) – enough for Stage-2A search
# -----------------------------------------------------------------------------

def nelder_mead(func, x0, args=(), max_iter=400, alpha=1.0, gamma=2.0, rho=0.5, sigma=0.5):
    """Tiny, dependency-free Nelder–Mead implementation (4-D)."""
    n = len(x0)
    # initial simplex
    simplex = [x0]
    for i in range(n):
        x = np.array(x0, copy=True)
        x[i] += 0.05 if x[i] == 0 else 0.05 * x[i]
        simplex.append(x)
    simplex = np.array(simplex)

    f_vals = np.array([func(x, *args) for x in simplex])

    for _ in range(max_iter):
        # sort
        idx = np.argsort(f_vals)
        simplex, f_vals = simplex[idx], f_vals[idx]
        best = simplex[0]

        # centroid of best n points (excluding worst)
        centroid = np.mean(simplex[:-1], axis=0)

        # reflection
        xr = centroid + alpha * (centroid - simplex[-1])
        fr = func(xr, *args)
        if fr < f_vals[0]:
            # expansion
            xe = centroid + gamma * (xr - centroid)
            fe = func(xe, *args)
            if fe < fr:
                simplex[-1], f_vals[-1] = xe, fe
            else:
                simplex[-1], f_vals[-1] = xr, fr
        elif fr < f_vals[-2]:
            simplex[-1], f_vals[-1] = xr, fr
        else:
            # contraction
            xc = centroid + rho * (simplex[-1] - centroid)
            fc = func(xc, *args)
            if fc < f_vals[-1]:
                simplex[-1], f_vals[-1] = xc, fc
            else:
                # shrink
                simplex[1:] = simplex[0] + sigma * (simplex[1:] - simplex[0])
                f_vals[1:] = [func(x, *args) for x in simplex[1:]]
    # return best
    idx = np.argmin(f_vals)
    return simplex[idx], f_vals[idx]

# -----------------------------------------------------------------------------
# Cost function
# -----------------------------------------------------------------------------

def chi2(params: np.ndarray, k_triplet: Tuple[int, int, int]) -> float:
    masses = calc_masses(k_triplet, params)
    V      = calc_ckm(k_triplet, params)
    # mass error in log-space
    mass_err = sum((math.log(masses[n]) - math.log(PDG_MASS_GEV[n])) ** 2 for n in PDG_MASS_GEV)
    # CKM fractional error
    ckm_err  = sum(((V[k] - PDG_CKM[k]) / PDG_CKM[k]) ** 2 for k in PDG_CKM)
    return mass_err + 150.0 * ckm_err

# -----------------------------------------------------------------------------
# Scan integer k triples, optimise, pick global best
# -----------------------------------------------------------------------------

def main():
    best = {
        'chi2': float('inf'),
        'k_triplet': None,
        'params': None,
    }

    for k_triplet in itertools.combinations(range(K_MIN, K_MAX + 1), 3):
        if k_triplet[2] - k_triplet[0] < MIN_SPAN:
            continue
        # initial guess (η, ξ, χ, λ)
        x0 = np.array([0.5, 0.2, 0.0, 0.05])
        params_opt, c_val = nelder_mead(chi2, x0, args=(k_triplet,), max_iter=600)
        if c_val < best['chi2']:
            best.update({'chi2': c_val, 'k_triplet': k_triplet, 'params': params_opt})

    # Pretty print
    kl, km, kh = best['k_triplet']
    eta, xi, chi, lam = best['params']
    print("Best k-triplet (light,mid,heavy):", best['k_triplet'])
    print(f"η={eta:.6g} GeV, ξ={xi:.6g}, χ={chi:.6g}, λ={lam:.6g}")
    print("χ² =", best['chi2'])

    masses = calc_masses(best['k_triplet'], best['params'])
    for label, names in [('Up', ('u','c','t')), ('Down', ('d','s','b')), ('Lept', ('e','mu','tau'))]:
        row = "  ".join(f"{n}={masses[n]:.3g} ({masses[n]/PDG_MASS_GEV[n]:.2f}×)" for n in names)
        print(f"{label:<5}:", row)

    V = calc_ckm(best['k_triplet'], best['params'])
    print("\nCKM:")
    for k, val in V.items():
        print(f"{k}: {val:.4f} (target {PDG_CKM[k]:.4f}, ratio {val/PDG_CKM[k]:.2f})")

    lock = {
        'k_values': best['k_triplet'],
        'eta_GeV': eta,
        'xi': xi,
        'chi': chi,
        'lam': lam,
        'chi2': best['chi2'],
    }
    Path('stage2A_lock.json').write_text(json.dumps(lock, indent=2))
    print("\nstage2A_lock.json written.")


if __name__ == '__main__':
    main() 