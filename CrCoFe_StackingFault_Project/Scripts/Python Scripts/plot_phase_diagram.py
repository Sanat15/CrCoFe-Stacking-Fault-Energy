# ---- plot_phase_diagram.py ----
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ternary
from scipy.interpolate import LinearNDInterpolator
import os
import re

BASE_DIR = os.path.join("..", "..", "Results", "All the results compiled")
OUTPUT_PATH = os.path.join("..", "..", "Plots", "phase_diagram.png")
CSV_FILE = os.path.join(BASE_DIR, "SFE_all.csv")

df = pd.read_csv(CSV_FILE)

# Extract composition
df[["Cr", "Co", "Fe"]] = df["composition"].str.extract(r"Cr([\d\.]+)_Co([\d\.]+)_Fe([\d\.]+)").astype(float)
df["ΔE_hcp-fcc(eV/atom)"] = df["E_hcp(eV/atom)"] - df["E_fcc(eV/atom)"]

# Pick one temperature (e.g. 300 K)
data = df[df["T(K)"] == 300]

points = data[["Cr", "Co", "Fe"]].values
values = data["ΔE_hcp-fcc(eV/atom)"].values
interp = LinearNDInterpolator(points, values, fill_value=np.nan)

# Build ternary grid
step = 0.02
grid = []
for i in np.arange(0, 1 + step, step):
    for j in np.arange(0, 1 - i + step, step):
        k = 1 - i - j
        if k >= 0:
            grid.append((i, j, k))
grid = np.array(grid)
grid_z = interp(grid)
grid_z = np.nan_to_num(grid_z, nan=np.nanmean(values))

fig, tax = ternary.figure(scale=1.0)
fig.set_size_inches(7, 6)

x = [p[1] + 0.5 * p[2] for p in grid]
y = [np.sqrt(3) / 2 * p[2] for p in grid]
cntr = plt.tricontourf(x, y, grid_z, levels=20, cmap="coolwarm")

tax.boundary(linewidth=2)
tax.gridlines(multiple=0.2, color="gray", linewidth=0.5)
tax.left_axis_label("Fe fraction")
tax.right_axis_label("Co fraction")
tax.bottom_axis_label("Cr fraction")
tax.set_title("Phase Stability Map (ΔE = E_HCP - E_FCC at 300 K)", fontsize=13)
fig.colorbar(cntr, ax=tax.ax, label="ΔE (eV/atom)")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300)
print(f"✅ Saved: {OUTPUT_PATH}")
