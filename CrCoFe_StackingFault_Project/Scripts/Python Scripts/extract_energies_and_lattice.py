import os
import pandas as pd
import re

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, '..', 'Results')
OUTPUT_DIR = os.path.join(RESULTS_DIR, 'All_Results_Compiled')
os.makedirs(OUTPUT_DIR, exist_ok=True)

records = []

print("🔍 Extracting SFE data from composition folders...")

for comp_folder in os.listdir(RESULTS_DIR):
    path = os.path.join(RESULTS_DIR, comp_folder)
    if not os.path.isdir(path) or comp_folder == 'All_Results_Compiled':
        continue

    out_dir = os.path.join(path, "out_files")
    if not os.path.exists(out_dir):
        continue

    for file in os.listdir(out_dir):
        if not file.endswith(".out"):
            continue

        filepath = os.path.join(out_dir, file)
        with open(filepath, 'r') as f:
            content = f.read()

        # Extract temperature, fault type, and gamma
        match = re.search(r'Temperature:\s*(\d+)', content)
        temp = int(match.group(1)) if match else None

        if 'ISF' in file:
            fault = 'ISF'
        elif 'ESF' in file:
            fault = 'ESF'
        elif 'Twin' in file or 'TWIN' in file:
            fault = 'Twin'
        else:
            fault = 'Unknown'

        gamma_match = re.search(r'Stacking fault energy:\s*([-+]?\d*\.\d+|\d+)', content)
        gamma = float(gamma_match.group(1)) if gamma_match else None

        records.append({
            'Composition': comp_folder,
            'Temperature': temp,
            'Fault_Type': fault,
            'Gamma_mJ_m2': gamma
        })

df = pd.DataFrame(records)
df = df.dropna(subset=['Gamma_mJ_m2'])
csv_path = os.path.join(OUTPUT_DIR, 'SEF_all.csv')
df.to_csv(csv_path, index=False)

print(f"✅ SEF_all.csv generated successfully at: {csv_path}")
