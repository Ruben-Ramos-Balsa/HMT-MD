#!/bin/bash
set -euo pipefail
hmt_tensor='/Users/ruben/Documents/New project/output/CIERRE_ACUMULATIVO_II_V_20260922/II_TENSOR'
hmt_mathlib='/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'
hmt_article_i='/Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922'
hmt_packages=$(find "$hmt_mathlib/.lake/packages" -type d -path '*/.lake/build/lib/lean' -print | paste -sd: -)
hmt_i_modules=$(python3 -I -S -c 'import json,pathlib,sys; p=pathlib.Path(sys.argv[1]); d=json.loads((p/"REGISTRO_REPRODUCCION.json").read_text()); print(":".join(dict.fromkeys(str((p/v["object"]).parent) for v in d["modules"].values())))' "$hmt_article_i")
export LEAN_PATH="$hmt_tensor:$hmt_i_modules:$hmt_mathlib/.lake/build/lib/lean:$hmt_packages"
'/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean' \
  -DwarningAsError=true --root="$hmt_tensor" \
  -o "$hmt_tensor/PentadicTensorCarrier.olean" \
  "$hmt_tensor/PentadicTensorCarrier.lean" 2>&1 | tee "$hmt_tensor/PentadicTensorCarrier.log"
'/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin/lean' \
  -DwarningAsError=true --root="$hmt_tensor" \
  -o "$hmt_tensor/SelectedPentadicTensor.olean" \
  "$hmt_tensor/SelectedPentadicTensor.lean" 2>&1 | tee "$hmt_tensor/SelectedPentadicTensor.log"
