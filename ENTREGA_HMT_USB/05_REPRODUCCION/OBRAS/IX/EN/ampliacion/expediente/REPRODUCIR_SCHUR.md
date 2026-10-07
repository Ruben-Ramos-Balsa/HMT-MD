# Reproducción focal del certificado de Schur

Este certificado prueba las cotas numéricas de la demostración contenida en
`AGENTE_SCHUR_DETALLES.md`. No regenera el corpus completo ni certifica RH.

## Entorno efectivamente utilizado

- Ejecutable: `/usr/bin/python3` (Python 3.9 de este equipo).
- Biblioteca: `mpmath==1.3.0`, en el entorno de usuario ya existente.
- No se instaló ni modificó ninguna biblioteca global para esta tarea.
- Se impide crear `__pycache__` en las fuentes heredadas.

Comandos efectivamente ejecutados desde `/Users/ruben/Documents/New project`:

```sh
/usr/bin/python3 output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/verificar_schur_ventana_nonadica.py --receipt output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/CERTIFICADO_SCHUR_R_UN_NOVENO.json
/usr/bin/python3 -O output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/verificar_schur_ventana_nonadica.py --receipt output/WEIL_DOBLE_CIRCULO_DESARROLLO_20260911/CERTIFICADO_SCHUR_R_UN_NOVENO_OPTIMIZADO.json
```

Los dos dan `PASS_SCHUR_FIXED_WINDOW_ONE_NINTH`, con 21 controles.
No debe añadirse `-S`: esa opción elimina la carga de `site-packages`, donde
reside la dependencia. En este equipo el Python empaquetado de Codex tampoco
dispone de `mpmath`; no es el ejecutable usado por estos recibos.

## Entorno local portable

En un equipo nuevo puede prepararse un entorno virtual, sin instalaciones
globales. Los siguientes comandos son instrucciones de instalación local;
no se ejecutaron durante esta tarea:

```sh
python3 -m venv .venv-schur
.venv-schur/bin/python -m pip install -r requirements_schur.txt
.venv-schur/bin/python verificar_schur_ventana_nonadica.py --receipt CERTIFICADO_SCHUR_R_UN_NOVENO.json
.venv-schur/bin/python -O verificar_schur_ventana_nonadica.py --receipt CERTIFICADO_SCHUR_R_UN_NOVENO_OPTIMIZADO.json
```

La instalación requiere acceso a un índice de paquetes o a una copia local
de la distribución de `mpmath`. No es parte de la demostración matemática.

## Fuentes heredadas incluidas para la reproducción

El script prefiere la copia local `dependencias_viii/`, con los siete
archivos siguientes. Sólo si esa carpeta no existe busca la carpeta hermana
`ARTICULO_VIII_PRIMOS_ESTRUCTURA_ESPECTRAL_20260910`. Una copia local
incompleta produce un error; no se mezclan fuentes de ambos cortes.

```text
fuente/pruebas/python/verificar_gram_nueve_ventanas.py
fuente/pruebas/python/partes_finitas_exactas.py
fuente/pruebas/python/a9_native.py
manuscrito/03_DOBLE_CIRCULO_Y_TRANSPORTE_ESPECTRAL.md
antecedentes/nonadica/pi_1000_decimales.txt
antecedentes/nonadica/certificado_generacion_estructural.json
antecedentes/nonadica/SHA256SUMS
```

El lector verifica las huellas fijadas de la publicación de π, su certificado
y ese manifiesto. El recibo local conserva además las huellas de los
propietarios numéricos y del manuscrito antecedente. Estas lecturas son
posteriores a la generación HMT; no son valores objetivo que seleccionen
el funcional ni ceros de zeta.

`preparar_dependencias_schur.py` ha copiado exactamente esos siete archivos
y verificado su identidad byte a byte con los originales. El resultado y
las rutas, tamaños y SHA-256 figuran en
`MANIFIESTO_DEPENDENCIAS_SCHUR.json`, estado
`PASS_SEVEN_DEPENDENCIES_BYTE_IDENTICAL`. No se modificó ningún original.
El preparador no se necesita para ejecutar el certificado cuando la copia
local ya acompaña esta carpeta.

Esta carpeta contiene así los antecedentes materiales mínimos del cálculo
focal; la dependencia externa `mpmath` permanece declarada y no vendorizada.
No se presenta esa inclusión como copia del corpus completo ni como prueba
global de autonomía científica del VIII. Los recibos normal y optimizado
registran `LOCAL_BYTE_IDENTICAL_COPY` y las huellas de los siete archivos,
el verificador y la nota matemática.

## Ensayo separado, sin certificado de positividad

`explorar_schur_ventana_con_primo.py` es un ensayo finito posterior para
una ventana de longitud `7/10`, donde sí actúa el reloj `log(2)`.
Usa NumPy y una cuadratura sin cota intervalar; no forma parte del certificado
de longitud `1/9`, no se ejecuta mediante los comandos anteriores y no
debe interpretarse como prueba del signo. Su salida declara
`EXPLORATION_NOT_CERTIFIED`. Esta investigación queda separada del cierre
focal actual.
