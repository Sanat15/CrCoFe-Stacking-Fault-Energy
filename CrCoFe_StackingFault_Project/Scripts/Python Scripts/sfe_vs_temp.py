import pandas as pd
import matplotlib.pyplot as plt
import os

# === Paths ===
INPUT_FILE = "../../Results/All_the_results_compiled/SFE_all.csv"
OUTPUT_DIR = "../../Plots/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load data ===
df = pd.read_csv(INPUT_FILE)

# === Extract unique compositions ===
compositions = df["composition"].unique()

# === Define energy types and their labels ===
energy_types = {
    "γ_ISF(mJ/m²)": "Intrinsic Stacking Fault Energy (ISF)",
    "γ_ESF(mJ/m²)": "Extrinsic Stacking Fault Energy (ESF)",
    "γ_Twin(mJ/m²)": "Twin Boundary Energy (TWE)"
}

# === Loop over each energy type and plot ===
for energy_col, energy_label in energy_types.items():
    plt.figure(figsize=(8, 6))

    for comp in compositions:
        subset = df[df["composition"] == comp]
        plt.plot(
            subset["T(K)"],
            subset[energy_col],
            marker="o",
            label=comp,
        )

    # === Formatting ===
    plt.title(f"Variation of {energy_label} with Temperature", fontsize=12)
    plt.xlabel("Temperature (K)", fontsize=11)
    plt.ylabel(f"{energy_label} (mJ/m²)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)

    # === Legend outside ===
    plt.legend(
        title="Composition",
        fontsize=8,
        title_fontsize=9,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
    )

    # === Adjust layout and save ===
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    output_file = os.path.join(OUTPUT_DIR, f"{energy_col.replace('γ_', '').replace('(mJ/m²)', '').strip()}_vs_temp.png")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ Saved clean plot for {energy_label} to: {output_file}")
