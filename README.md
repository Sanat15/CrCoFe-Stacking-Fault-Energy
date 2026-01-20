# Stacking Fault Energy and Lattice Parameter Evaluation in Cr–Co–Fe Alloys
Computational materials science project using LAMMPS, MEAM potentials, and post-processing in Python.

---

## 📁 Folder Structure Overview
MM309N_Assignment2_Group9/
│
├── 📂 Benchmarking/
│ ├── in.benchmark_Cr
│ ├── in.benchmark_Co
│ ├── in.benchmark_Fe
│ ├── log.benchmark_Cr
│ ├── log.benchmark_Co
│ ├── log.benchmark_Fe
│ └── compositions.txt
│
├── 📂 Plots/
│ ├── 📂 ternary_SFE_plots/
│ │ ├── gamma_ISF_150K.png
│ │ ├── gamma_ISF_300K.png
│ │ ├── gamma_ISF_500K.png
│ │ ├── gamma_ESF_150K.png
│ │ ├── gamma_ESF_300K.png
│ │ ├── gamma_ESF_500K.png
│ │ ├── gamma_Twin_150K.png
│ │ ├── gamma_Twin_300K.png
│ │ └── gamma_Twin_500K.png
│ │
│ └── 📂 ternary_Lattice_plots/
│ │ ├── a_fcc_150K.png
│ │ ├── a_fcc_300K.png
│ │ ├── a_fcc_500K.png
│ │ ├── a_hcp_150K.png
│ │ ├── a_hcp_300K.png
│ │ ├── a_hcp_500K.png
│ │ ├── a_dhcp_150K.png
│ │ ├── a_dhcp_300K.png
│ │ └── a_dhcp_500K.png
│ │
│ ├── 📂 Ovito images/
│ │ ├── Cr0.33_Co0.33_Fe0.33_fcc_150K.png
│ │ ├── Cr0.50_Co0.25_Fe0.25_hcp_300K.png
│ │ ├── Cr0.67_Co0.17_Fe0.17_fcc_500K.png
│ │ └── Cr1.00_Co0.00_Fe0.00_dhcp_500K.png
│ │
│ └── 📂 SFE_vs_Temp
│ ├── ISF_vs_Temp.png
│ ├── ESF_vs_Temp.png
│ └── Twin_vs_Temp.png
│
├── 📂 Report/
│ ├── Report.pdf
│ └── Report.tex
│
├── 📂 Results/
│ ├── 📂 Cr0.33_Co0.33_Fe0.33/
│ │ ├── 📂 dat_files/
│ │ ├── 📂 cfg_files/
│ │ ├── 📂 out_files/
│ │ └── log.lammps
│ ├── (21 compositions total)
│ │
│ └── 📂 All_Results_Compiled/
│ ├── SEF_all.csv
│ └── Lattice_all.csv
│
├── 📂 Scripts/
│ ├── 📂 LAMMPS_scripts/
│ │ ├── CrCoFe.in
│ │ ├── CrCoFe_dhcp.in
│ │
│ ├── 📂 Python_scripts/
│ │ ├── extract_energies_and_lattice.py
│ │ ├── sfe_ternary_plots.py
│ │ ├── lattice_plots.py
│ │ └── make_dhcp_simple.py
│ │ ├── make_csv_annni_vs_dmlf.py         
│ │ └── make_plots_annni_vs_scaled_dmlf.py 
│ │ 
│ ├── 📂 Potentials/
│ │ ├── CrCoFe.meam
│ │ ├── library.meam
│ │ └── dhcp_10x10x5.data
│ │
│ └── run_all.sh
│
├── 📂 ANNNI_vs_DMLF model comparisions/       
│   ├── ANNNI_vs_DMLF_calibrated.csv          
│   ├── output.png                           
│   ├── output (1).png                        
│   └── output (2).png
|
└── MM_309N_Assignment2.pdf


---

## File Purpose Summary

### Simulation and Benchmarking
- `Benchmarking/`: Contains input (`in.benchmark_...`) and log files for MEAM potential verification of Cr, Co, and Fe.  
- `Potentials/`: Contains the MEAM potential (`CrCoFe.meam`) and `library.meam` used for all simulations.

### Results and Post-Processing
- `Results/`: Contains folders for all 21 ternary compositions.  
  Each composition folder includes:
  - `dat_files/`: Atomic data files from LAMMPS.
  - `cfg_files/`: Configurations for OVITO visualization.
  - `out_files/`: Output text files with stacking fault and lattice parameter data.
  - `log.lammps`: Run log for that composition.

- `All_Results_Compiled/`: Contains combined `.csv` files:
  - `SEF_all.csv` — Stacking Fault Energy data (ISF, ESF, Twin).
  - `Lattice_all.csv` — Lattice parameters (a for FCC, HCP, DHCP).

### Scripts
- `extract_energies_and_DMLF.py` — Extracts stacking fault energy data into `SEF_all.csv`.  
- `extract_lattice_parameters.py` — Extracts lattice constants from `.out` files into `Lattice_all.csv`.  
- `plot_all_ternary.py` — Generates ternary contour plots for SFE data.  
- `lattice_plots.py` — Generates ternary contour plots for lattice parameters.  
- `organize_results.py` — Automatically creates `dat_files/`, `cfg_files/`, and `out_files/` inside each composition folder.  
- `run_all.sh` — Batch script to execute all LAMMPS runs.

### ANNNI vs DMLF Model Comparisons
- `ANNNI_vs_DMLF_calibrated.csv — Final comparison between analytical ANNNI model and DMLF predictions after unit calibration
- `output.png — Intrinsic SFE comparison plot
- `output (1).png — Extrinsic SFE comparison plot
- `output (2).png — Twin fault energy comparison plot

This folder validates the DMLF SFE predictions against a physics-based ANNNI Ising model using real LAMMPS lattice parameters and calibrated scaling factors. Ensures relative error < 20%.

---

## Notes
- Run Python scripts from the **main project directory**.  
- Ensure all dependencies (`numpy`, `pandas`, `matplotlib`, `scipy`, `python-ternary`) are installed.  
- Output plots are stored in the `Plots/` directory.
- The ovito images arn't separated by colour as for that pro version was required.

---

## Contributors
**Group 9 – MEMS**
- Sanat Kumar Shukla  
- Kondeti Praveen Kumar
- Saumya Sharma
- Abhijeet Singh Parihar
