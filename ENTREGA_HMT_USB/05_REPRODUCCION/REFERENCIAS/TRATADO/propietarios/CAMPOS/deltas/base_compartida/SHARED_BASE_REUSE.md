# Entrada común de acción, electrón e incidencia

## Uso

Los desarrollos posteriores importan `SharedArticleIBase`. La entrada importa
`SelectedArticleIComposition` y `SelectedRegionalIncidence`, sin copiar sus
demostraciones. El registro compartido es exactamente
`HMT.I.TerminalSelector.regionalRegister`, no un nuevo registro de valores.

`HMT.Shared.ArticleI.shared_action_electron_incidence` reúne las publicaciones
de alfa a toda profundidad, el orden decimal −34, las dos secciones de acción,
la composición electrónica y la acción positiva del operador en la base
electrónica, junto con la bandera de incidencia y las propiedades demostradas
de la retícula de rango 24: paridad, integralidad, autodualidad y mínimo 4.
Las dos identidades previas comprueban por igualdad definicional que los
lectores aritmético y de incidencia utilizan ese mismo registro.

El orden −34 pertenece a la escala de acción construida; no reemplaza la
declaración de unidades físicas. Las ramas numérica y de incidencia comparten
procedencia: no se afirma que el número 10^-34 por sí solo genere la retícula.
Los resultados posteriores de Barbero, CKM, respuesta del vacío y desarrollos
excepcionales se añaden mediante sus propios módulos y pruebas, reutilizando
la base, sin redefinirla ni presentar un import como una demostración nueva.

## Integración única

El ensamblado coordinado es `PAQUETE_CONTINUIDAD_K_UNIDAD_20260918`.
Este directorio es un delta de desarrollo, no otra biblioteca completa ni
un reemplazo del paquete del artículo. El ensamblador incorpora:

- `SharedArticleIBase.lean` en `lean/terminal/`;
- los cuatro módulos de acción/electrón, ya entregados, en `lean/biblioteca/`;
- los recibos y hashes nuevos, manteniendo los recibos anteriores;
- la entrada nueva entre los objetivos obligatorios del verificador común.

Cada distribución autónoma contiene la clausura de fuentes que necesita.
Durante el desarrollo hay una única versión de cada módulo; en las
distribuciones se copian exactamente esos archivos y sus hashes. No se
mantienen reescrituras divergentes del mismo núcleo.

## Conservación acumulativa

`LEAN_BASELINE_20260918.json` fija 137 contenidos Lean distintos presentes
en el manifiesto del ensamblado al capturarlo. La captura verificó sus bytes.
`verify_lean_preservation.py` compara esta línea de base inmutable con un
manifiesto sucesor y comprueba los archivos reales. Una fuente puede cambiar
de carpeta; una versión sustituida debe conservarse con sus bytes originales
en el historial y continuar inventariada. Se rechazan pérdidas aunque se
haya borrado también la fila correspondiente del manifiesto sucesor.

Ejemplo desde esta carpeta, indicando la carpeta de entrega que se verifica:

```sh
python3 -I -S verify_lean_preservation.py \
  --baseline LEAN_BASELINE_20260918.json \
  --manifest RUTA_ENTREGA/MANIFIESTO.json --root RUTA_ENTREGA
```

Este control complementa el inventario del ensamblador; no sustituye la
compilación ni demuestra cobertura matemática. No preserva archivos ajenos
al inventario capturado. La línea de base y el delta se conservan también en
un ZIP separado, sin sobrescribir la entrega previa.

## Verificación y alcance

`shared_verification_v2/VERIFICATION.json` registra la compilación de la
entrada nueva con Lean 4.21.0 y advertencias tratadas como errores, utilizando
los objetos de sus dependencias ya existentes. No es una recompilación
transitiva limpia del conjunto. Las tres consultas de axiomas no contienen
`sorryAx`; la composición conserva `Lean.ofReduceBool` del selector finito.
El dominio S8 del selector sigue explícito: esta entrada no añade una prueba
de su producción. Tampoco declara formalizados FLM, Moonshine o teoría M.

El recibo causal conserva el orden de las publicaciones HMT y las dos vías
de alfa. Su control pasó; no se confunde ese control con una prueba Lean.
La revisión independiente cotejó los enunciados y confirmó que no se añaden
premisas, registros alternativos ni axiomas. Se corrigió además el ejecutor
para que rechace una carpeta de compilación no vacía y un orden inválido de
imports locales: así no puede reutilizar silenciosamente objetos residuales.

Los PDF, sus fuentes LaTeX y los ZIP anteriores permanecen intactos.
