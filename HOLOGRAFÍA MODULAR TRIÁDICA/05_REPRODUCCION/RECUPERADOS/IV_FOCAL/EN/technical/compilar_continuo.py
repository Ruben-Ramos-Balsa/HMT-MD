#!/usr/bin/env python3
"""Compilación de la sucesora: consume el preflight real, sin emitirlo.

Reutiliza íntegro el controlador de REV02 y sólo fija el nombre público del
PDF. Los hashes de las fuentes y del recibo se cotejan antes de cada pasada.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('iv_continuo_compiler', HERE/'compilar_iv.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.PDF_NAME = 'MOONSHINE_DUALIDAD_T_TEORIA_M_CONTINUO.pdf'

if __name__ == '__main__':
    raise SystemExit(driver.main())
