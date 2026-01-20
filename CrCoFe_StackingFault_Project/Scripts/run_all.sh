#!/bin/bash
# ------------------------------------------------------------
# Run all Cr–Co–Fe compositions for fcc, hcp, dhcp
# Each at T = 150, 300, 500 K
# Automatically sorts results by composition folder
# ------------------------------------------------------------
#chmod +x run_all.sh
#./run_all.sh
# --- Define compositions (Cr Co Fe) ---
compositions=(
  "0.50 0.50 0.00"
)

# --- Simulation parameters ---
phases=("fcc" "hcp" "dhcp")
temperatures=(150 300 500)

# --- Run loop ---
for comp in "${compositions[@]}"; do
  read -r xCr xCo xFe <<< "$comp"
  folder="Cr${xCr}_Co${xCo}_Fe${xFe}"
  mkdir -p "$folder"

  echo "=== Composition: Cr=$xCr Co=$xCo Fe=$xFe ==="

  for phase in "${phases[@]}"; do
    for T in "${temperatures[@]}"; do
      echo ">>> Running ${phase} at ${T} K for ${folder}"

      cd "$folder" || exit 1

      if [ "$phase" = "dhcp" ]; then
        mpirun -np 4 lmp \
          -var T_run $T \
          -var xCr $xCr -var xCo $xCo -var xFe $xFe \
          -in ../CrCoFe_dhcp.in > log_${phase}_${T}K.out
      else
        mpirun -np 4 lmp \
          -var phase $phase \
          -var T_run $T \
          -var xCr $xCr -var xCo $xCo -var xFe $xFe \
          -in ../CrCoFe.in > log_${phase}_${T}K.out
      fi

      cd ..

      echo ">>> Finished ${phase} at ${T} K for ${folder}"
    done
  done
done

echo "✅ All runs complete and sorted by composition."

