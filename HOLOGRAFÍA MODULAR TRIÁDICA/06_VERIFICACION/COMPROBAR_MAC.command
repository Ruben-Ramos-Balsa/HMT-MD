#!/bin/sh
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Se requiere Python 3 para comprobar archivos. Los PDF no requieren Python."
  exit 1
fi
python3 -I -B -S verificar_integridad.py
status=$?
printf '\nPulse Intro para cerrar. / Press Return to close.\n'
read -r answer
exit "$status"
