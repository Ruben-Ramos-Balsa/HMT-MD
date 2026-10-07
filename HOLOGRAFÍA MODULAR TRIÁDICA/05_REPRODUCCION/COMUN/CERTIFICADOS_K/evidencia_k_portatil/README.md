# Reproducción del selector terminal

Esta carpeta conserva diecinueve archivos íntegros, con las rutas relativas que utilizan los verificadores originales. `MANIFIESTO.json` identifica sus propietarios y huellas. Las fuentes y los certificados no han sido alterados.

Desde esta carpeta:

```sh
python3 -I -S 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/15_SELECTOR_GLOBAL_DOBLE_LECTURA/verificar_cierre_afin_monodromico_terminal.py --check-certificate
python3 -O -I -S 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/15_SELECTOR_GLOBAL_DOBLE_LECTURA/verificar_cierre_afin_monodromico_terminal.py --check-certificate
```

Ambas ejecuciones reproducen el certificado conservado. El programa incorpora el censo de 19.446 registros y la condición conjunta excepcional–temporal, además del contraste de la fibra terminal de tres estados. Las condiciones y el alcance de cada censo se conservan en el JSON.

El programa orbital histórico incluido conserva una comprobación de la revisión literal `2026-07-22.2` de `CURRENT.json`. La copia de procedencia disponible tiene revisión `2026-09-01.AUTHORIAL-RECTOR-2084`, aunque conserva las mismas doce coordenadas. Por ello su ejecución independiente con `--check-certificate` se detiene en esa comprobación documental posterior a la selección. Esta diferencia se registra expresamente; el verificador de cierre afín anterior no consulta esa revisión. No se ha sustituido la fecha ni modificado el certificado histórico para producir un resultado favorable.

No se ejecuta Lean. La reproducción aquí indicada es un control aritmético y documental del selector terminal con las entradas y condiciones declaradas en el programa.
