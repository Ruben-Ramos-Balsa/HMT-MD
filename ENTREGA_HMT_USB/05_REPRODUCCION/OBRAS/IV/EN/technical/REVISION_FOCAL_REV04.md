# Revisión focal de instalación y álgebra orientada — REV04

Fecha: 11 de septiembre de 2026. Resultado: `PASS_QA_DOCUMENTAL_FOCAL_IV_REV04`.

## Alcance comprobado

La revisión se limita al parche autorizado en `extension.tex`, `continuo_conjunto.tex` y `01_hilbert_nonadico.tex`, a las seis fuentes comunes y a la incorporación íntegra de `registro_imagen_integral.tex`. No modifica manuscritos, preflight, índices generales ni registros de otros artículos. La habilidad `preserve-hmt-continuity` se aplica preservando los enunciados con sus pruebas, la procedencia y la diferencia entre inclusión documental y suficiencia demostrativa.

Los tres archivos instalados son idénticos por bytes a los de la propuesta congelada `/private/tmp/hmt-iv-rev04-propuesta.sofEYz`. El recibo [QA_REV04.json](QA_REV04.json) conserva las huellas y el resultado de cada comparación.

- **8/8 enunciados y demostraciones:** al sustituir la numeración manual por entornos LaTeX, se preservan los cuerpos completos, con normalización exclusiva de espacios y de tres remisiones internas. La proposición automática que ya existía se conserva aparte.
- **444/444 bloques matemáticos anteriores:** 110 en `extension.tex`, 217 en `continuo_conjunto.tex` y 117 en `01_hilbert_nonadico.tex`. El censo usa delimitadores `\(...\)`, `\[...\]` y entornos `equation`, `align`, `gather`, con multiplicidad; no se presenta como inventario universal de todo fragmento entre dólares.
- **6/6 fuentes comunes:** `nucleo.tex`, `trit_desarrollo.tex`, `tpk_desarrollo_integrado.tex`, `memoria_resolvente.tex`, `figures/app.tex` y `figures/regimenes_trit.tex`, byteidénticas a REV03 y con sus inclusiones comprobadas.
- **Imagen integral de K:** SHA-256 `8405c2303b2f2f3bd80a47aa934e37073bbf4a91347f5f9df3647d37be3d7107`, idéntica al propietario de II REV03. Se incluye una vez, antes de «Dos lecturas racionales». Se conservan imagen, inversa, controles fuera de imagen y condiciones de transporte.

## Comprobación reproducible

[verificar_weyl_orientado_rev04.py](verificar_weyl_orientado_rev04.py) emplea sólo la biblioteca estándar. Su ejecución sin argumentos es autónoma: se copió exclusivamente el programa a un directorio temporal y se ejecutó desde otro directorio vacío, tanto normal como con optimización. No utiliza rutas personales, fuentes TeX, red ni valores objetivo en ese modo.

```text
python3 -I -S technical/verificar_weyl_orientado_rev04.py
python3 -I -S -O technical/verificar_weyl_orientado_rev04.py
```

Ambas ejecuciones dan `PASS_WEYL_ORIENTADO_REV04`, código de salida cero y JSON idéntico. Se comprueban exactamente 531441 ternas del cociclo, 59049 acciones compuestas sobre la base, 729 elementos representados distintos, 1458 identidades de inversa y tres controles que rechazan convenciones incorrectas. El cociclo de la sección ordenada es `bc`; el área alternante es `ad−bc`; el exponente del conmutador `ghg⁻¹h⁻¹` es `bc−ad`. El centro se calcula, no se presume por el cardinal.

La ejecución normal de [verificar_imagen_firmada.py](verificar_imagen_firmada.py) dio `PASS_EXACT_SIGNED_IMAGE_ALGEBRA`: 4096 reconstrucciones binarias, rango 12, trece relaciones lineales independientes, menor de valor absoluto 12 y siete controles negativos. **No se ejecuta con `-O`**, porque el programa propietario exige aserciones. Sus datos de referencia se utilizan sólo para regresión posterior, separados de las identidades generales.

El modo `--auditar-instalacion` es distinto del modo algebraico autónomo: exige como argumentos la carpeta REV03, la propuesta y el propietario de II para efectuar esas comparaciones históricas. Admite además `--compilation-receipt` para cotejar el PDF con un recibo externo. Ese modo guarda únicamente `technical/QA_REV04.json`; no compila ni modifica fuentes. La huella del programa final figura en el recibo para permitir comprobar qué versión produjo los resultados.

## Numeración y localizadores resueltos

La compilación comunicada por el editor es `20260911T110500Z_a2dc2114`, con 138 páginas y PDF SHA-256 `0e06b9eb074eae35af83ae2a3eee712742c32b4e08f3471663ce7a5e045058ad`. Se ha recalculado la huella y leído su TOC/AUX. Esto sustituye el estado inicial de «páginas pendientes» por localizadores efectivos, sin atribuir una compilación o inspección visual a este control.

| Enunciado anterior | Etiqueta preservada o introducida | Número resuelto | Página impresa = física |
|---|---|---:|---:|
| Proposición 1 | `iv:cont:concatenacion` | 4.1 | 37 |
| Proposición 2 | `iv:cont:esperanza` | 4.2 | 38 |
| Proposición 3 | `iv:cont:gram` | 4.3 | 39 |
| Teorema 4 | `iv:cont:terminal` | 4.4 | 39 |
| Proposición 5 | `iv:cont:cancelacion` | 4.5 | 40 |
| Proposición 6 | `iv:cont:rectangular-exacta` | 4.6 | 41 |
| Proposición automática anterior | `iv:rectangular-natural` | 4.7 | 41 |
| Proposición 7 | `iv:cont:memoria-natural` | 4.8 | 42 |
| Proposición 8 | `iv:cont:memoria-homologia` | 4.9 | 42 |

El mapa correlativo está en §4.9, página 44, `iv:cont:mapa-correlativo`; la imagen integral de K, en §6.9, páginas 75–77, `img09:seccion`; el puente de Weyl, en §9.2.1, páginas 112–113, `iv:weyl-area-extension`. La proposición de extensión central es 9.1, página 113, `iv:prop:heisenberg-orientado`.

## Recorrido material

El recorrido recursivo contiene 56 archivos TeX distintos incluido el maestro. El [mapa actualizado](MAPA_RECORRIDO_HMT_20260911.md) conserva las distinciones anteriores y enlaza el orden efectivo: núcleo común → prolongación e historias → construcción correlativa del continuo → regiones → registro y α → incidencia excepcional → realización hilbertiana → acción y canales angulares → elipse y radio → dualidad → pantallas → acción y realización dinámica. Es un recorrido expositivo y de dependencias, no una separación de las cinco operaciones en cinco entradas independientes.

La revisión sólo produce comprobaciones finitas de álgebra, preservación e identidad documental. No certifica todas las genealogías, la selección de historias concretas, los resultados terminales ni la validez matemática global mediante la compilación. La inspección visual de esta salida corresponde a un control separado.
