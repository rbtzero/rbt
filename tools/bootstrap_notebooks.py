#!/usr/bin/env python3
"""Create or overwrite notebooks with final plotting code for each figure.

Run in CI before write_figs so that notebooks contain the real computation.
"""
import nbformat as nbf
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
NBDIR = ROOT / "notebooks"
NBDIR.mkdir(exist_ok=True)

cells_map = {
    "01_branch_lattice.ipynb": """
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

depth = 5
g = 2
paths = np.array([np.array(list(map(int, f"{k:0{depth}b}"))) for k in range(g**depth)])
entropy = -(paths*np.log2(paths+1e-9)+(1-paths)*np.log2(1-paths+1e-9)).sum(1)
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(paths.sum(1), np.arange(len(paths)), entropy, c=entropy, cmap='viridis', s=20, edgecolor='k', linewidth=0.2)
ax.set_xlabel('Hamming weight'); ax.set_ylabel('index'); ax.set_zlabel('S')
plt.savefig('../paper/figs/branch_lattice.png', dpi=450, bbox_inches='tight')
""",
    "04_coupling_fan_in.ipynb": """
import numpy as np, matplotlib.pyplot as plt
from scipy.constants import pi
β = np.array([-7, -19/6, 41/10])
E  = np.logspace(2, 17, 1500)
α0 = np.array([1/59.0, 1/29.6, 1/8.5])
α = 1/(1/α0[:,None] - β[:,None]/(2*pi)*np.log(E/91.19))
fig, ax = plt.subplots(figsize=(5,3.5))
for i,lbl in enumerate(['α₃⁻¹','α₂⁻¹','α₁⁻¹']):
    ax.plot(E, 1/α[i], lw=2, label=lbl)
ax.set_xscale('log'); ax.set_xlim(1e2,1e17)
ax.set_xlabel('Energy [GeV]'); ax.set_ylabel('α⁻¹'); ax.legend()
fig.savefig('../paper/figs/coupling_fan_in.png', dpi=450, bbox_inches='tight')
""",
    "06_spacetime_curvature.ipynb": """
import numpy as np, matplotlib.pyplot as plt
N=400
x,y=np.meshgrid(np.linspace(-4,4,N), np.linspace(-4,4,N))
R = 4*np.exp(-(x**2+y**2)/2)
plt.figure(figsize=(5,4))
img=plt.imshow(R, origin='lower', extent=[-4,4,-4,4], cmap='inferno', vmax=R.max())
plt.colorbar(img, label='Ricci scalar R')
plt.contour(x,y,R,[0.5,1,2],colors='w',linewidths=0.4)
plt.xlabel('x'); plt.ylabel('y'); plt.title('RB curvature bump')
plt.savefig('../paper/figs/spacetime_curvature.png', dpi=450, bbox_inches='tight')
""",
    "07_mass_spectrum.ipynb": """
import numpy as np, matplotlib.pyplot as plt
pdg={'e':0.511,'μ':105.66,'τ':1776.86,'u':2.16,'d':4.67,'s':93,'c':1270,'b':4180,'t':172760}
ledger_index={k:i for i,k in enumerate(pdg)}
m0=2e5
rb={k:m0*2**(-Δ) for k,Δ in ledger_index.items()}
keys=list(pdg)
x=np.arange(len(keys))
fig,ax=plt.subplots(figsize=(7,3.5))
ax.bar(x-0.2,[pdg[k] for k in keys],0.4,label='PDG',color='#377eb8')
ax.bar(x+0.2,[rb[k]  for k in keys],0.4,label='RB',color='#e41a1c')
ax.set_yscale('log'); ax.set_xticks(x,keys); ax.set_ylabel('mass [MeV]'); ax.legend()
fig.savefig('../paper/figs/mass_spectrum.png', dpi=450, bbox_inches='tight')
""",
    "09_ring_line.ipynb": """
import numpy as np, matplotlib.pyplot as plt, math, scipy.constants as const
E0=3.54; γ=0.006
E=np.linspace(E0-0.05,E0+0.05,800)
L = 1/(math.pi*γ*(1+((E-E0)/γ)**2))
plt.figure(figsize=(5,3)); plt.plot(E,L,lw=2)
plt.xlabel('Energy [keV]'); plt.ylabel('Intensity (arb)')
plt.title('Predicted RB 3.54 keV aperture line')
plt.savefig('../paper/figs/ring_aperture_line.png', dpi=450, bbox_inches='tight')
""",
    "09_axial_lepton.ipynb": """
import numpy as np, matplotlib.pyplot as plt
lept=['e','μ','τ']
m=np.array([0.511,105.66,1776.86])
g2,gY=0.651,0.357
Δ=1e-3*(g2**2-gY**2)*m
plt.figure(figsize=(4,3)); plt.stem(lept,Δ, basefmt=' ', use_line_collection=True)
plt.ylabel('Δm₅ [MeV]'); plt.title('RB axial splitting'); plt.ylim(0,max(Δ)*1.2)
plt.savefig('../paper/figs/axial_lepton_spectrum.png', dpi=450, bbox_inches='tight')
""",
    "10_bcs_gap.ipynb": """
import numpy as np, matplotlib.pyplot as plt
Tc=9
T=np.linspace(0.1,Tc,800)
Δ0=1.76*Tc
Δ=Δ0*np.tanh(1.74*np.sqrt(Tc/T-1))
plt.figure(figsize=(5,3)); plt.plot(T,Δ,lw=2)
plt.xlabel('T [K]'); plt.ylabel('Δ [meV]'); plt.title('BCS gap from RB mapping')
plt.savefig('../paper/figs/bcs_gap.png', dpi=450, bbox_inches='tight')
""",
    "11_electroweak_crossover.ipynb": """
import numpy as np, matplotlib.pyplot as plt
T=np.linspace(50,300,700)
D,E,lam,T0=0.1,0.005,0.125,160
phi=np.where(T<T0, np.sqrt(D*(T0**2-T**2)/(2*lam)), 0)
plt.figure(figsize=(5,3)); plt.plot(T,phi,lw=2)
plt.xlabel('T [GeV]'); plt.ylabel('⟨φ⟩ [GeV]'); plt.title('Electroweak crossover')
plt.savefig('../paper/figs/electroweak_crossover.png', dpi=450, bbox_inches='tight')
""",
    "11_logistic_heatmap.ipynb": """
import numpy as np, matplotlib.pyplot as plt
r = np.linspace(2.5,4,800)
x0 = np.linspace(0,1,800)
R,X = np.meshgrid(r,x0)

def iterate(x,r,n=200):
    for _ in range(n):
        x = r*x*(1-x)
    return x
Z = iterate(X, R)
plt.figure(figsize=(6,4))
plt.imshow(Z, extent=[r.min(),r.max(),x0.min(),x0.max()], aspect='auto', origin='lower', cmap='plasma')
plt.xlabel('r'); plt.ylabel('$x_0$'); plt.title('Logistic-map heat-map')
plt.colorbar(label='$x_{n}$')
plt.savefig('../paper/figs/logistic_heatmap.png', dpi=450, bbox_inches='tight')
""",
    "11_brain_knot_decay.ipynb": """
import numpy as np, matplotlib.pyplot as plt
T = np.linspace(0, 10, 1200)
Y = np.sin(12*T)*np.exp(-0.4*T)
plt.figure(figsize=(6,3))
plt.plot(T, Y, lw=1.8)
plt.xlabel('t'); plt.ylabel('Amplitude'); plt.title('Brain-knot decay envelope')
plt.grid(alpha=0.3)
plt.savefig('../paper/figs/brain_knot_decay.png', dpi=450, bbox_inches='tight')
""",
    "12_curvature_waveguide.ipynb": """
import numpy as np, matplotlib.pyplot as plt
N=500
x,y = np.linspace(-4,4,N), np.linspace(-4,4,N)
X,Y = np.meshgrid(x,y)
K = np.cos(0.5*X)*np.sin(0.5*Y)
plt.figure(figsize=(5,4))
img=plt.imshow(K, origin='lower', extent=[-4,4,-4,4], cmap='coolwarm')
plt.colorbar(img, label='Gaussian curvature κ')
plt.xlabel('x'); plt.ylabel('y'); plt.title('Curvature wave-guide')
plt.savefig('../paper/figs/curvature_waveguide.png', dpi=450, bbox_inches='tight')
""",
    "14_vr_demo.ipynb": """
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
np.random.seed(0)
pts=np.random.standard_normal((3,2000))
fig = plt.figure(figsize=(5,4)); ax = fig.add_subplot(111, projection='3d')
ax.scatter(pts[0], pts[1], pts[2], s=3, alpha=0.6)
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z'); ax.set_title('VR demo point-cloud')
plt.savefig('../paper/figs/vr_demo.png', dpi=450, bbox_inches='tight')
""",
    "13_lattice_colony.ipynb": """
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# ---------------- lattice_torus_geometry ----------------
θ,φ = np.linspace(0,2*np.pi,200), np.linspace(0,2*np.pi,200)
Θ,Φ = np.meshgrid(θ,φ); R,r = 3,1
X=(R+r*np.cos(Θ))*np.cos(Φ); Y=(R+r*np.cos(Θ))*np.sin(Φ); Z=r*np.sin(Θ)
fig = plt.figure(figsize=(4,4)); ax = fig.add_subplot(111,projection='3d')
ax.plot_surface(X,Y,Z,color='#66c2a5',alpha=0.7,linewidth=0)
ax.set_axis_off()
fig.savefig('../paper/figs/lattice_torus_geometry.png',dpi=450,bbox_inches='tight')
plt.close(fig)
# ---------------- lattice_growth_curve ----------------
n = np.arange(1,40)
colony = 1 - 2.0**(-n)
plt.figure(figsize=(4,3))
plt.plot(n,colony,'o-',color='#fc8d62')
plt.xlabel('tick'); plt.ylabel('colony fraction')
plt.title('RB lattice-colony growth'); plt.ylim(0,1)
plt.savefig('../paper/figs/lattice_growth_curve.png',dpi=450,bbox_inches='tight')
plt.close()
# ---------------- lattice_colony ----------------
N = 128
state = np.zeros((N,N))
state[N//2,N//2] = 1
for _ in range(10):
    state = np.maximum(state, np.roll(state,1,0))
    state = np.maximum(state, np.roll(state,-1,0))
    state = np.maximum(state, np.roll(state,1,1))
    state = np.maximum(state, np.roll(state,-1,1))
plt.figure(figsize=(4,4))
plt.imshow(state,cmap='plasma')
plt.axis('off'); plt.title('Colony after 10 ticks')
plt.savefig('../paper/figs/lattice_colony.png',dpi=450,bbox_inches='tight')
""",
}

for nb_name, code in cells_map.items():
    nb = nbf.v4.new_notebook()
    nb.cells = [nbf.v4.new_markdown_cell(f"# Auto-generated {nb_name}"),
                nbf.v4.new_code_cell(code)]
    (NBDIR / nb_name).write_text(nbf.writes(nb))
print('✓ notebooks written') 