#!/usr/bin/env python3
"""Render the five remaining publication diagrams directly with Matplotlib.
This bypasses Inkscape so we can commit the final high-resolution PNGs. Run once locally.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np, pathlib, textwrap
root = pathlib.Path(__file__).resolve().parents[1]
figdir = root / 'paper' / 'figs'
figdir.mkdir(parents=True, exist_ok=True)

# 1. axiom_flow.png --------------------------------------------------
fig, ax = plt.subplots(figsize=(12,2))
ax.axis('off')
boxes = ["δ-Glitch","Counting ⇒ ℕ","Number-Tower\n(ℤ ℚ ℝ ℂ ℍ 𝕆)","Gauge Stack\nU(1) SU(2) SU(3)","Spacetime & Gravity","Mass Spectrum → Life"]
colors=['#e1f5fe','#fff9c4','#c8e6c9','#ffe0b2','#d1c4e9','#ffccbc']
for i,(txt,c) in enumerate(zip(boxes,colors)):
    ax.add_patch(patches.Rectangle((i*1.6,0.2),1.5,0.6,facecolor=c,edgecolor='k'))
    ax.text(i*1.6+0.75,0.5,txt,ha='center',va='center',fontsize=9)
# arrows
for i in range(5):
    ax.annotate('',xy=(i*1.6+1.5,0.5),xytext=((i+1)*1.6,0.5),
                arrowprops=dict(arrowstyle='-|>',lw=1))
ax.set_xlim(-0.2,8.5); ax.set_ylim(0,1)
fig.savefig(figdir/'axiom_flow.png',dpi=300,bbox_inches='tight')
plt.close(fig)

# 2. intro_timeline.png ---------------------------------------------
fig, ax = plt.subplots(figsize=(12,1.5))
ax.axis('off')
pts=[("Newton 1687",0),("Maxwell 1865",2),("GR 1915",4),("QFT 1928-75",6),("Recursive Becoming 2025",9)]
ax.hlines(0, -0.5,9.5,color='#777',lw=2)
for label,x in pts:
    ax.plot(x,0,'o',color='#008080',ms=6)
    ax.text(x,0.3,label,ha='center',va='bottom',fontsize=9,color='#000')
fig.savefig(figdir/'intro_timeline.png',dpi=300,bbox_inches='tight')
plt.close(fig)

# 3. gauge_stack.png -------------------------------------------------
fig, ax = plt.subplots(figsize=(6,3))
ax.axis('off')
labels=[('U(1)',0.8,'#66c2a5'),('SU(2)',0.5,'#fc8d62'),('SU(3)',0.2,'#8da0cb')]
for i,(lbl,y,c) in enumerate(labels):
    ax.add_patch(patches.Rectangle((0.1,y),0.8,0.25,facecolor=c,edgecolor='k'))
    ax.text(0.5,y+0.125,lbl,ha='center',va='center',fontsize=12)
ax.annotate('Curvature',xy=(0.5,0),xytext=(0.5,0.12),ha='center',arrowprops=dict(arrowstyle='-|>',lw=1))
fig.savefig(figdir/'gauge_stack.png',dpi=300,bbox_inches='tight')
plt.close(fig)

# 4. number_tower.png ----------------------------------------------
fig, ax = plt.subplots(figsize=(3,6))
ax.axis('off')
boxes=[('ℕ','#d9d9d9'),('ℤ','#bde1ff'),('ℚ / ℝ','#d9d9d9'),('ℂ','#bde1ff'),('ℍ','#d9d9d9'),('𝕆','#bde1ff')]
for i,(txt,c) in enumerate(boxes):
    ax.add_patch(patches.Rectangle((0.2,1+i*0.8),1.6,0.6,facecolor=c,edgecolor='k'))
    ax.text(1,1+i*0.8+0.3,txt,ha='center',va='center',fontsize=14)
ax.annotate('adjunction ×2',xy=(0.05,1),xytext=(0.05,5.6),va='center',ha='center',rotation=90,arrowprops=dict(arrowstyle='-|>',lw=1))
fig.savefig(figdir/'number_tower.png',dpi=300,bbox_inches='tight')
fig.savefig(figdir/'number_tower_flow.pdf',bbox_inches='tight')
plt.close(fig)

# 5. tests_overview.png --------------------------------------------
import pandas as pd
rows=[
    ("XRISM/Resolve",2026,"3.54 keV ring-aperture line"),
    ("MAGIS-100",2028,"2π axial-lepton phase shift"),
    ("CASPEr-SW",2027,"Negative EDM slope"),
    ("Super-Charm",2029,"720 MeV mono-γ + / E"),
    ("Curv. waveguide",2025,"<0.05 dB m⁻¹ loss"),
    ("Immersive VR",2026,"<10 mW power budget")
]
df=pd.DataFrame(rows,columns=['Experiment','Year','RB Prediction'])
fig,ax=plt.subplots(figsize=(7,3))
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
fig.savefig(figdir/'tests_overview.png',dpi=300,bbox_inches='tight')
fig.savefig(figdir/'tests_overview.pdf',bbox_inches='tight')
plt.close(fig)

# 6. periodic_table.png ------------------------------------------------
elements = [
    # 1st period
    (1,'H',0,0), (2,'He',17,0),
    # 2nd period
    (3,'Li',0,1),(4,'Be',1,1), (5,'B',12,1),(6,'C',13,1),(7,'N',14,1),(8,'O',15,1),(9,'F',16,1),(10,'Ne',17,1),
    # 3rd period
    (11,'Na',0,2),(12,'Mg',1,2),(13,'Al',12,2),(14,'Si',13,2),(15,'P',14,2),(16,'S',15,2),(17,'Cl',16,2),(18,'Ar',17,2),
    # 4th period
    (19,'K',0,3),(20,'Ca',1,3),(21,'Sc',2,3),(22,'Ti',3,3),(23,'V',4,3),(24,'Cr',5,3),(25,'Mn',6,3),(26,'Fe',7,3),(27,'Co',8,3),(28,'Ni',9,3),(29,'Cu',10,3),(30,'Zn',11,3),(31,'Ga',12,3),(32,'Ge',13,3),(33,'As',14,3),(34,'Se',15,3),(35,'Br',16,3),(36,'Kr',17,3),
    # 5th period
    (37,'Rb',0,4),(38,'Sr',1,4),(39,'Y',2,4),(40,'Zr',3,4),(41,'Nb',4,4),(42,'Mo',5,4),(43,'Tc',6,4),(44,'Ru',7,4),(45,'Rh',8,4),(46,'Pd',9,4),(47,'Ag',10,4),(48,'Cd',11,4),(49,'In',12,4),(50,'Sn',13,4),(51,'Sb',14,4),(52,'Te',15,4),(53,'I',16,4),(54,'Xe',17,4),
    # 6th period
    (55,'Cs',0,5),(56,'Ba',1,5),(57,'La',2,8),
    (72,'Hf',3,5),(73,'Ta',4,5),(74,'W',5,5),(75,'Re',6,5),(76,'Os',7,5),(77,'Ir',8,5),(78,'Pt',9,5),(79,'Au',10,5),(80,'Hg',11,5),(81,'Tl',12,5),(82,'Pb',13,5),(83,'Bi',14,5),(84,'Po',15,5),(85,'At',16,5),(86,'Rn',17,5),
    # 7th period
    (87,'Fr',0,6),(88,'Ra',1,6),(89,'Ac',2,9),
    (104,'Rf',3,6),(105,'Db',4,6),(106,'Sg',5,6),(107,'Bh',6,6),(108,'Hs',7,6),(109,'Mt',8,6),(110,'Ds',9,6),(111,'Rg',10,6),(112,'Cn',11,6),(113,'Nh',12,6),(114,'Fl',13,6),(115,'Mc',14,6),(116,'Lv',15,6),(117,'Ts',16,6),(118,'Og',17,6),
    # Lanthanides (row index 8)
    (58,'Ce',3,8),(59,'Pr',4,8),(60,'Nd',5,8),(61,'Pm',6,8),(62,'Sm',7,8),(63,'Eu',8,8),(64,'Gd',9,8),(65,'Tb',10,8),(66,'Dy',11,8),(67,'Ho',12,8),(68,'Er',13,8),(69,'Tm',14,8),(70,'Yb',15,8),(71,'Lu',16,8),
    # Actinides (row index 9)
    (90,'Th',3,9),(91,'Pa',4,9),(92,'U',5,9),(93,'Np',6,9),(94,'Pu',7,9),(95,'Am',8,9),(96,'Cm',9,9),(97,'Bk',10,9),(98,'Cf',11,9),(99,'Es',12,9),(100,'Fm',13,9),(101,'Md',14,9),(102,'No',15,9),(103,'Lr',16,9)
]

fig, ax = plt.subplots(figsize=(12,6))
ax.axis('off')

# Draw grid
for Z,sym,x,y in elements:
    rect = patches.Rectangle((x,y),1,1,facecolor='#f0f0f0',edgecolor='k',lw=0.5)
    ax.add_patch(rect)
    ax.text(x+0.5,y+0.6,str(Z),ha='center',va='center',fontsize=6)
    ax.text(x+0.5,y+0.25,sym,ha='center',va='center',fontsize=10,fontweight='bold')

ax.set_xlim(-0.5,18.5); ax.set_ylim(-1,10)
ax.set_aspect('equal')
fig.savefig(figdir/'periodic_table.png',dpi=300,bbox_inches='tight')
fig.savefig(figdir/'periodic_table.pdf',bbox_inches='tight')
plt.close(fig)

print('✓ periodic table rendered') 