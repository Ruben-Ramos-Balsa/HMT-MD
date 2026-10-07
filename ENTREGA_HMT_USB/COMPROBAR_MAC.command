#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 06_VERIFICACION/verificar_integridad.py
result=$?
read -r -p "Press Enter / Pulsa Intro / Entrée"
exit "$result"
