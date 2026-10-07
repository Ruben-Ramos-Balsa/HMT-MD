#!/bin/bash
set -euo pipefail
hmt_workspace='/Users/ruben/Documents/New project'
hmt_principal="$hmt_workspace/output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922"
hmt_mathlib='/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'
hmt_delta="$hmt_workspace/output/CIERRE_ACUMULATIVO_II_V_20260922/III"
hmt_owners="$hmt_workspace/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/angular_constitutive_bridge"
hmt_lean='/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean'
hmt_objects=$(jq -r --arg base "$hmt_principal/" '.modules[].object | $base + . | sub("/[^/]+$"; "")' "$hmt_principal/REGISTRO_REPRODUCCION.json" | sort -u | paste -sd: -)
hmt_packages=$(find "$hmt_mathlib/.lake/packages" -type d -path '*/.lake/build/lib/lean' -print | paste -sd: -)
export LEAN_PATH="$hmt_delta:$hmt_objects:$hmt_mathlib/.lake/build/lib/lean:$hmt_packages"
for hmt_module in ElectricQuanta ActionElectricComposition; do
  "$hmt_lean" -DwarningAsError=true --root="$hmt_owners" \
    -o "$hmt_delta/$hmt_module.olean" "$hmt_owners/$hmt_module.lean" \
    2>&1 | tee "$hmt_delta/$hmt_module.log"
done
"$hmt_lean" -DwarningAsError=true --root="$hmt_delta" \
  -o "$hmt_delta/SelectedConstitutivePublication.olean" \
  "$hmt_delta/SelectedConstitutivePublication.lean" \
  2>&1 | tee "$hmt_delta/SelectedConstitutivePublication.log"
