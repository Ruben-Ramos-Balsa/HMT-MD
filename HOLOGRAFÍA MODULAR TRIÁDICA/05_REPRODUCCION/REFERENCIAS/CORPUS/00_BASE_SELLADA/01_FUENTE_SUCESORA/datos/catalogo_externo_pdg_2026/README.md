# Catálogo externo tipado PDG 2026

Este directorio contiene una vista versionada de las 1.170 entradas de
`pdgparticle` y de todas sus propiedades de masa o anchura publicadas en las
*Summary Tables* de la edición 2026. El snapshot de entrada es
`pdg-2026.0.sqlite`, SHA-256
`40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe`.

El catálogo es una capa de comparación externa. No selecciona rutas, firmas,
torres, coeficientes ni realizaciones HMT--MD. Todas las filas conservan el
estatuto `RECONOCIMIENTO_EXTERNO`; la cobertura HMT se declara en columnas
separadas. `ACTIVE` se reserva exclusivamente a una propiedad de masa cuya
reconstrucción calibrada es identificable en la fuente activa; nunca se aplica
por arrastre a la identidad, carga o representación de la partícula y nunca
significa predicción prospectiva.

## Regla de identidad y no duplicación

- Cada entrada de `pdgparticle` produce una fila `PARTICLE_IDENTITY`. Por tanto,
  cargas y antipartículas permanecen separadas.
- Cada propiedad `M` o `G` de las *Summary Tables* se publica una sola vez bajo
  el grupo PDG que la posee.
- La columna `particle_output_ids` enlaza esa propiedad con todas las
  identidades de carga/antipartícula pertinentes. El valor metrológico común no
  se replica artificialmente.
- Si el snapshot no contiene una masa de neutrino asociada a `pdgparticle`, no
  se crea ninguna. Tampoco se añaden masas universales para anyones u objetos
  topológicos.

## Artefactos

- `catalogo_externo_pdg_2026.csv`: vista tabular íntegra.
- `catalogo_externo_pdg_2026.json`: la misma información, con metadatos y
  recuentos.
- `fuentes_metrologicas_2026.json`: PDG, BIPM SI 9.ª ed. v4.01, CODATA 2022 y
  CODATA 2018, con sus funciones probatorias separadas.
- `MANIFEST_SHA256.json`: huellas y tamaños de los artefactos.

El snapshot SQLite no se incorpora al paquete. Su licencia declarada por PDG es
CC BY 4.0; su procedencia, edición, fecha de publicación y huella quedan
congeladas en los metadatos.

## Reproducción

Desde la raíz del paquete:

```bash
python3 -I -B -S pruebas/python/generar_catalogo_externo_pdg_2026.py \
  --snapshot /ruta/a/pdg-2026.0.sqlite
python3 -I -B -S pruebas/python/verificar_catalogo_externo_pdg_2026.py \
  --snapshot /ruta/a/pdg-2026.0.sqlite
```

La segunda orden regenera en un directorio temporal y exige igualdad byte a
byte. Cuando el snapshot no esté disponible, la opción `--sin-regenerar`
comprueba estructura, recuentos, tipado y huellas de los artefactos
empaquetados.
