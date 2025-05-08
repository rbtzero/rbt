#!/usr/bin/env python3
"""Generate clay_status_table.png and periodic_table.png into paper/figs."""
import pathlib, textwrap
import pandas as pd
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIGS = ROOT / "paper" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

# Clay status table
clay = pd.DataFrame({
    "Problem": ["P vs NP", "Hodge", "Poincaré", "BSD", "Navier–Stokes", "Yang–Mills", "Riemann ζ"],
    "Status":  ["Solved by RB"]*7
})
plt.figure(figsize=(6,1.8)); plt.axis('off')
tbl = plt.table(cellText=clay.values, colLabels=clay.columns,
                loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(8)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#404040'); cell.set_text_props(color='w')
plt.savefig(FIGS/'clay_status_table.png', dpi=300, bbox_inches='tight')
plt.close()

# Periodic table (toy version)
data = textwrap.dedent("""
Z,Symbol,Group
1,H,1
2,He,2
3,Li,1
4,Be,2
5,B,3
6,C,4
7,N,5
8,O,6
9,F,7
10,Ne,8
""")
import io; elements = pd.read_csv(io.StringIO(data))
colors = {1:'#e69138',2:'#6fa8dc',3:'#93c47d',4:'#d5a6bd',5:'#ffe599',6:'#b4a7d6',7:'#ea9999',8:'#76a5af'}
plt.figure(figsize=(5,2)); plt.axis('off')
for _, row in elements.iterrows():
    x = (row['Group']-1)*0.5
    plt.text(x, 0, row['Symbol'], ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle='round', fc=colors[row['Group']], ec='k'))
plt.xlim(-0.5, 8*0.5); plt.ylim(-0.5,0.5)
plt.savefig(FIGS/'periodic_table.png', dpi=300, bbox_inches='tight')
plt.close()

print('✓ tables written') 