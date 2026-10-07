#!/bin/bash
set -euo pipefail
task_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
mathlib_dir='/Users/ruben/Documents/ChatGPT/jueces y controles/FORMALIZACION_PRINCIPALES_20260916/deps/mathlib4'
lean_dir='/Users/ruben/.elan/toolchains/leanprover--lean4---v4.21.0/bin'
cd -- "$mathlib_dir"
"$lean_dir/lake" env lean --root="$task_dir" -o "$task_dir/NormalProductAlgebra.olean" "$task_dir/NormalProductAlgebra.lean"
