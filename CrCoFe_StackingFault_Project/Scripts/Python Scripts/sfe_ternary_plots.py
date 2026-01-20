import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ternary
from scipy.interpolate import LinearNDInterpolator
import re

# 🧭 Paths
BASE_DIR = os.path.join("..", "..", "Results", "All the results compiled")
OUTPUT_DIR = os.path.join("..", "..", "Plots", "ternary_SFE_plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🎯 Target properties to plot
SFE_PROPERTIES = ["γ_ISF(mJ/m²)", "γ_ESF(mJ/m²)", "γ_Twin(mJ/m²)"]
TEMPS = [150, 300, 500]


def safe_filename(name):
    """Replace special symbols for Windows-safe filenames."""
    name = name.replace("γ", "gamma_").replace("²", "2").replace("/", "_per_")
    return re.sub(r"[^a-zA-Z0-9_.\-]", "_", name)


def extract_compositions(df):
    """Extract Cr, Co, Fe fractions from composition string."""
    comps = df["composition"].str.extract(
        r"Cr(?P<Cr>[\d\.]+)_Co(?P<Co>[\d\.]+)_Fe(?P<Fe>[\d\.]+)"
    ).astype(float)
    df["Cr"] = comps["Cr"]
    df["Co"] = comps["Co"]
    df["Fe"] = comps["Fe"]
    return df


def make_ternary_plot(df, property_name, temperature, output_dir):
    """Make ternary contour plot for one property and temperature."""
    data = df[df["T(K)"] == temperature]
    if data.empty:
        print(f"⚠️ No data for {temperature} K - {property_name}")
        return

    points = data[["Cr", "Co", "Fe"]].values
    values = data[property_name].values

    interp = LinearNDInterpolator(points, values, fill_value=np.nan)

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

    cntr = plt.tricontourf(x, y, grid_z, levels=15, cmap="plasma")

    tax.boundary(linewidth=2.0)
    tax.gridlines(multiple=0.2, color="gray", linewidth=0.5)
    tax.left_axis_label("Fe fraction", fontsize=12)
    tax.right_axis_label("Co fraction", fontsize=12)
    tax.bottom_axis_label("Cr fraction", fontsize=12)
    tax.set_title(f"{property_name} at {temperature} K", fontsize=14, pad=20)

    cbar = fig.colorbar(cntr, ax=tax.ax, orientation="vertical", shrink=0.8)
    cbar.set_label(property_name, fontsize=10)

    tax.ticks(axis="lbr", multiple=0.2, linewidth=1, tick_formats="%.1f")
    tax.clear_matplotlib_ticks()

    # ✅ Make filename safe for Windows
    safe_name = safe_filename(f"{property_name}_{temperature}K.png")
    save_path = os.path.join(output_dir, safe_name)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {save_path}")


def main():
    csv_path = os.path.join(BASE_DIR, "SFE_all.csv")
    df = pd.read_csv(csv_path)
    df = extract_compositions(df)

    for temp in TEMPS:
        for prop in SFE_PROPERTIES:
            make_ternary_plot(df, prop, temp, OUTPUT_DIR)

    print(f"\n✨ All SFE ternary plots saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
