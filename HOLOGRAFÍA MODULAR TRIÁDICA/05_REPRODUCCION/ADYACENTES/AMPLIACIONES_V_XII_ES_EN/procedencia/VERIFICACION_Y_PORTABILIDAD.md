# Pruebas focales conservadas

Los fragmentos de V, VII y XII incluyen sus demostraciones completas. Estos
archivos adicionales conservan la procedencia y permiten reproducir sus
comprobaciones; no sustituyen el contenido demostrativo del PDF.

- `reloj/verificar_reloj.py`: 24.024 controles exactos del calendario y sus
  cocientes. La copia local escribe sólo su propio resultado.
- `CIERRE_CONJUNTO_ACCION_HOLOGRAFIA_20260928/ley9/verificar_curva.py`:
  103 controles de la composición térmico-geométrica.
- `CIERRE_CONJUNTO_ACCION_HOLOGRAFIA_20260928/ley9/verificar_recuperacion.py`:
  132 controles racionales y multiprecisión de recuperación y energía libre.

Los dos últimos requieren Python y `mpmath`. En la copia del verificador de
curva se ha sustituido únicamente el localizador absoluto de pi por la copia
relativa de `entradas/pi_1000_decimales.txt`; su SHA-256 debe coincidir con el
original registrado. Los demás cálculos permanecen literales. Los antecedentes
numéricos y sus notas se mantienen en la misma jerarquía relativa que esperan
los programas. Los localizadores absolutos conservados dentro de esos JSON
identifican su procedencia histórica; no son dependencias de ejecución de
estos tres verificadores portátiles.

La sustitución de horizonte se ha cotejado algebraicamente en el manuscrito:
`G hbar = c^3 L_alpha^2`, `R_S = 2 G M / c^2` y
`k_B T_H = hbar c / (4 pi R_S)` implican
`T_M = eta^2 s_0^2 / (8 pi k_B L_alpha^2 M)` y
`S_M T_M = M c^2 / 2`. La temperatura a masa fija no contiene un factor
adicional de velocidad en el denominador. Se conserva la distinción
`R = 2 R_S` en la realización correspondiente.

La entrega de «Ley 9 puertas» y sus propietarios quedan identificados en
`MANIFIESTO_ENTREGA.json`. Sus comprobaciones previas son antecedentes; los
resultados locales de los tres programas documentan la reproducción de esta
ronda. No se ha cambiado un estatuto científico por una mera comprobación de
huellas o por la compilación del PDF.
