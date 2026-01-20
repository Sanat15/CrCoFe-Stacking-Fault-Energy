"""
make_csv_annni_vs_dmlf.py
Creates a calibrated comparison CSV: ANNNI vs (scaled) DMLF for ISF/ESF/Twin.

Inputs
------
- SFE_all.csv            # must contain columns:
                         # composition, T(K), E_fcc(eV/atom), E_hcp(eV/atom),
                         # E_dhcp(eV/atom), γ_ISF(mJ/m²), γ_ESF(mJ/m²), γ_Twin(mJ/m²)
- Lattice_all.csv        # must contain columns:
                         # composition, T(K), a_fcc(Å)
  (Note: if your a_fcc values are cell lengths from LAMMPS supercells,
   divide by 10 to convert to Å for one conventional fcc cell as below.)

Output
------
- ANNNI_vs_DMLF_calibrated.csv
"""

import pandas as pd
import numpy as np
from math import sqrt

SFE_FILE = "SFE_all.csv"
LAT_FILE = "Lattice_all.csv"
OUT_FILE = "ANNNI_vs_DMLF_calibrated.csv"

# ---- Helper functions ------------------------------------------------------
def annni_from_bulk(Efcc, Ehcp, Edhcp):
    """
    ANNNI (J1, J2) from bulk energies (per atom):
      E_fcc  = J0 - J1 - J2
      E_hcp  = J0 + J1 - J2
      E_dhcp = J0 + J2
    => J1 = 0.5*(E_hcp - E_fcc)
       J2 = 0.5*(E_dhcp - 0.5*(E_fcc + E_hcp))
    """
    J1 = 0.5 * (Ehcp - Efcc)
    J2 = 0.5 * (Edhcp - 0.5 * (Efcc + Ehcp))
    return J1, J2

def numerators_from_J(J1, J2):
    """
    Fault-energy numerators (eV per {111} site):
      γ_ISF  ∝ 4(J1 + J2)
      γ_ESF  ∝ 4J1 + 8J2
      γ_Twin ∝ 2J1 + 4J2
    """
    gI_num = 4.0 * (J1 + J2)
    gE_num = 4.0 * J1 + 8.0 * J2
    gT_num = 2.0 * J1 + 4.0 * J2
    return gI_num, gE_num, gT_num

def to_mJ_per_m2(numerator_eV_per_site, a_angstrom):
    """
    Convert numerator (eV per {111} site) → γ (mJ/m²):
      A = (sqrt(3)/4) * a^2      [Å² per {111} site]
      1 eV/Å² = 16021.766 mJ/m²
    """
    A = (sqrt(3.0) / 4.0) * (a_angstrom ** 2)
    return (numerator_eV_per_site / A) * 16021.766

def ls_scale(y_target, x_model):
    """Least-squares scalar s minimizing || y - s x ||² (ignore x<=0)."""
    m = x_model > 0
    x, y = x_model[m], y_target[m]
    return float((x * y).sum() / (x * x).sum())

# ---- Load & merge ----------------------------------------------------------
sfe = pd.read_csv(SFE_FILE)
lat = pd.read_csv(LAT_FILE)

# Merge a_fcc(T) and convert to Å if needed (here: ÷10 as used in our runs)
df = sfe.merge(lat[["composition", "T(K)", "a_fcc(Å)"]],
               on=["composition", "T(K)"], how="left").copy()
df["a(Å)"] = df["a_fcc(Å)"] / 10.0

# The four alloys of interest
targets = [
    "Cr0.00_Co0.00_Fe1.00",
    "Cr0.33_Co0.33_Fe0.33",
    "Cr0.50_Co0.25_Fe0.25",
    "Cr0.67_Co0.17_Fe0.17",
]

rows = []
for comp in targets:
    sub = df[df["composition"] == comp].sort_values("T(K)").head(3).copy()
    for _, r in sub.iterrows():
        Efcc, Ehcp, Edhcp = r["E_fcc(eV/atom)"], r["E_hcp(eV/atom)"], r["E_dhcp(eV/atom)"]
        a = r["a(Å)"]

        # ANNNI
        J1, J2 = annni_from_bulk(Efcc, Ehcp, Edhcp)
        gI_num, gE_num, gT_num = numerators_from_J(J1, J2)
        gI = to_mJ_per_m2(gI_num, a)
        gE = to_mJ_per_m2(gE_num, a)
        gT = to_mJ_per_m2(gT_num, a)

        rows.append({
            "composition": comp, "T(K)": int(r["T(K)"]), "a(Å)": a,
            "γ_ISF_ANNNI": gI, "γ_ESF_ANNNI": gE, "γ_Twin_ANNNI": gT,
            "γ_ISF_DMLF": r["γ_ISF(mJ/m²)"],
            "γ_ESF_DMLF": r["γ_ESF(mJ/m²)"],
            "γ_Twin_DMLF": r["γ_Twin(mJ/m²)"],
        })

res = pd.DataFrame(rows)

# ---- Per-fault calibration factors (constant scale per fault type) ---------
sISF = ls_scale(res["γ_ISF_ANNNI"].values,  res["γ_ISF_DMLF"].values)
sESF = ls_scale(res["γ_ESF_ANNNI"].values,  res["γ_ESF_DMLF"].values)
sTwin= ls_scale(res["γ_Twin_ANNNI"].values, res["γ_Twin_DMLF"].values)

# Apply scaling and compute % errors vs scaled DMLF
res["γ_ISF_DMLF_scaled"]  = sISF * res["γ_ISF_DMLF"]
res["γ_ESF_DMLF_scaled"]  = sESF * res["γ_ESF_DMLF"]
res["γ_Twin_DMLF_scaled"] = sTwin * res["γ_Twin_DMLF"]

for k in ["ISF", "ESF", "Twin"]:
    res[f"%Error_vs_scaled_{k}"] = 100.0 * (
        (res[f"γ_{k}_ANNNI"] - res[f"γ_{k}_DMLF_scaled"]) / res[f"γ_{k}_DMLF_scaled"]
    )

# Save
res.to_csv(OUT_FILE, index=False)

print("Saved:", OUT_FILE)
print(f"Scale factors -> ISF: {sISF:.6f}, ESF: {sESF:.6f}, Twin: {sTwin:.6f}")
print("Max |%Error|:",
      {k: res[f"%Error_vs_scaled_{k}"].abs().max() for k in ["ISF","ESF","Twin"]})
