"""
make_plots_annni_vs_scaled_dmlf.py
Reads ANNNI_vs_DMLF_calibrated.csv and plots:
  - γ_ISF:  ANNNI vs Scaled DMLF
  - γ_ESF:  ANNNI vs Scaled DMLF
  - γ_Twin: ANNNI vs Scaled DMLF

Output
------
- Shows three figures interactively (save as needed from your IDE),
  or uncomment plt.savefig(...) lines to write PDFs/PNGs.
"""

import pandas as pd
import matplotlib.pyplot as plt

IN_FILE = "ANNNI_vs_DMLF_calibrated.csv"

df = pd.read_csv(IN_FILE)

targets = [
    "Cr0.00_Co0.00_Fe1.00",
    "Cr0.33_Co0.33_Fe0.33",
    "Cr0.50_Co0.25_Fe0.25",
    "Cr0.67_Co0.17_Fe0.17",
]
labels = ["Cr0Fe1", "Cr0.33Co0.33Fe0.33", "Cr0.50Co0.25Fe0.25", "Cr0.67Co0.17Fe0.17"]
linestyles = {"ANNNI": "-", "Scaled DMLF": "--"}

def plot_one(kind, title):
    plt.figure(figsize=(10,6))
    for comp, label in zip(targets, labels):
        sub = df[df["composition"]==comp].sort_values("T(K)")
        plt.plot(sub["T(K)"], sub[f"γ_{kind}_ANNNI"],
                 linestyle=linestyles["ANNNI"], linewidth=2, label=f"{label} ANNNI")
        plt.plot(sub["T(K)"], sub[f"γ_{kind}_DMLF_scaled"],
                 linestyle=linestyles["Scaled DMLF"], linewidth=2, label=f"{label} Scaled DMLF")
    plt.title(f"{title}: ANNNI vs Scaled DMLF", fontsize=14)
    plt.xlabel("Temperature (K)", fontsize=12)
    plt.ylabel("γ (mJ/m²)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(ncol=2)
    # plt.savefig(f"{kind}_ANNNI_vs_scaledDMLF.pdf", bbox_inches="tight")
    plt.show()

plot_one("ISF",  "Intrinsic Stacking Fault Energy")
plot_one("ESF",  "Extrinsic Stacking Fault Energy")
plot_one("Twin", "Twin Fault Energy")
