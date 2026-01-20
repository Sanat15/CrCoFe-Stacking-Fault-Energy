#!/usr/bin/env python3
# Simple guaranteed-working DHCP generator for LAMMPS

import math, random

# ---- Parameters ----
a = 3.54        # lattice parameter a (Å)
c = 5.75        # lattice parameter c (Å)
nx = 10         # repetitions along x
ny = 10         # repetitions along y
nrepeats = 5    # number of ABAC repeats (each repeat = 4 layers)
xCo = 0.33
xCr = 0.33
xFe = 1.0 - xCo - xCr
seed = 12345
outname = "dhcp_10x10x5.data"

random.seed(seed)

# ---- Geometry setup ----
e1 = (a, 0.0, 0.0)
e2 = (a/2.0, a*math.sqrt(3)/2.0, 0.0)

# ABAC stacking: A(0,0), B(2/3,1/3), A(0,0), C(1/3,2/3)
shifts = [(0.0, 0.0), (2.0/3.0, 1.0/3.0), (0.0, 0.0), (1.0/3.0, 2.0/3.0)]
dz = c / 4.0

coords = []
for layer_idx in range(4 * nrepeats):
    sfx, sfy = shifts[layer_idx % 4]
    z = layer_idx * dz
    for ix in range(nx):
        for iy in range(ny):
            fx = ix + sfx
            fy = iy + sfy
            x = fx * e1[0] + fy * e2[0]
            y = fx * e1[1] + fy * e2[1]
            coords.append((x, y, z))

natoms = len(coords)
nCo = int(round(xCo * natoms))
nCr = int(round(xCr * natoms))
nFe = natoms - nCo - nCr
types = [1]*nCo + [2]*nCr + [3]*nFe
random.shuffle(types)

xs = [p[0] for p in coords]
ys = [p[1] for p in coords]
zs = [p[2] for p in coords]
xlo, xhi = min(xs)-0.5, max(xs)+0.5
ylo, yhi = min(ys)-0.5, max(ys)+0.5
zlo, zhi = min(zs)-0.5, max(zs)+0.5

# ---- Write file ----
with open(outname, "w") as f:
    f.write(f"DHCP supercell generated: a={a} c={c} nx={nx} ny={ny} repeats={nrepeats}\n")
    f.write(f"{natoms} atoms\n\n")
    f.write("3 atom types\n\n")
    f.write(f"{xlo:.6f} {xhi:.6f} xlo xhi\n")
    f.write(f"{ylo:.6f} {yhi:.6f} ylo yhi\n")
    f.write(f"{zlo:.6f} {zhi:.6f} zlo zhi\n\n")
    f.write("Masses\n\n")
    f.write("1 58.933\n2 51.996\n3 55.845\n\n")
    f.write("Atoms # atomic\n\n")
    for i, (pos, t) in enumerate(zip(coords, types), start=1):
        f.write(f"{i} {t} {pos[0]:.8f} {pos[1]:.8f} {pos[2]:.8f}\n")

print(f"Wrote {outname} with {natoms} atoms (Co={nCo}, Cr={nCr}, Fe={nFe})")

