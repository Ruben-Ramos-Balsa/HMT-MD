# Lectura conjunta y transporte del artículo I

Sucesor aditivo del paquete del selector iterado de 19 de septiembre.
Conserva sus fuentes, LaTeX, datos y pruebas; añade siete módulos Lean.
No modifica los PDF ni declara cerrado el artículo completo.

El contexto es APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo. Las nueve fases son una conexión conjunta; una
factorización en cartas no las convierte en nueve filtros independientes.
Retornar de fase no reinicia la historia.

## Resultado comprobado

Los mismos bloques efectivamente devueltos por el selector regional refinan
los cilindros y alimentan la firma, el acarreo y el lector de Paley–Witt.
La compatibilidad entre emisión y productor está demostrada en
`ProducedFrameProjection.produced_emission`: no es una igualdad recibida como
hipótesis de esa instancia. `same_produced_state` reúne el productor,
las palabras, la compatibilidad de los cilindros y el acarreo.

El transporte de marcos depende del prefijo almacenado. Se prueban covarianza,
reversibilidad, naturalidad, unicidad de la corriente compatible y
recuperación de la emisión visible. La especialización al marco fijo
recupera exactamente el lector anterior. La firma y los cilindros permanecen
en el historial producido; no se afirma que el lector visible recupere toda
la memoria oculta.

Los cilindros semiabiertos tienen intersección unipuntual; la lectura de
incidencia y la numérica se componen sobre la misma ejecución. La renovación
nonádica posterior actúa sobre la fibra completa de 468 elementos desde
cualquier fase, con soporte total; no se la sustituye por evaluación puntual.

El selector terminal anterior queda conservado. Su resultado es invariante
por el orden de enumeración del repertorio de entrada; esta invariancia no
demuestra por sí sola la producción de los ocho miembros del repertorio.

## Orden de lectura y reproducción

1. Las instrucciones y fuentes conservadas del núcleo, en `INICIO_AQUI.md`,
   `lean/` y `fuentes/`, fijan el origen y los tipos de las operaciones.
2. `deltas/selector/` contiene el selector iterado y la firma de sus hijos.
3. `deltas/lectura_conjunta/RegionalSemiopenLimit.lean` e
   `IteratedJointProjection.lean` reúnen cilindros, emisión y código.
4. `CalibratedPaleyTransport.lean` y `PrefixFrameProjection.lean` transportan
   el lector por prefijos sin inventar un marco independiente en cada nivel.
5. `ProducedFrameProjection.lean` compone ese lector con el productor real.
6. `NonadicJointRenewal.lean` trata la realización posterior conjunta.
7. `UnorderedTerminalTransfer.lean` reutiliza el selector terminal y conserva
   explícita su premisa sobre el repertorio.

Con Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, previamente instalados:

```sh
python3 -I -S reproducir_lectura_conjunta.py --plan
python3 -I -S reproducir_lectura_conjunta.py --mathlib /ruta/a/mathlib4 --lean /ruta/a/lean
```

El plan comprueba imports, fuentes y orden. La segunda orden compila las
dependencias necesarias y comprueba las declaraciones señaladas. Sólo se
reutilizan objetos cuando coinciden fuente, compilador, dependencias y
huella del objeto; en un equipo nuevo se recompilan desde las fuentes.
No se pide reconstruir a mano el orden de archivos.

## Alcance exacto

Los nuevos módulos de lectura y transporte no contienen `sorry`, axiomas
locales ni nueva reducción nativa. El adaptador terminal hereda la dependencia
`Lean.ofReduceBool` del selector finito anterior; no se oculta.

`JointOutput` contiene cilindros, hijos y firma, no todas las fibras del
estado enriquecido. La regla de transporte `g` sigue siendo una operación
explícita suministrada sobre ese historial; no se identifica sin prueba con
las matrices L0/L1. Una agenda decimal arbitraria no se denomina trayectoria
consecutiva: para ese caso se utiliza `decimalDepth n = n`.

Permanecen fuera de los enunciados reunidos la identificación de este dominio
con la admisibilidad terminal completa que selecciona K y la construcción
íntegra FLM/Moonshine. Esto delimita lo que el código demuestra; no afirma
que el material correspondiente sea inexistente en el corpus. Los resultados
anteriores de K, sus lectores, L0/L1 y los retículos no se retiran.

## Conservación

El manifiesto y el README anteriores están en `versiones_previas/`.
`recibos/lectura_conjunta/` conserva las verificaciones focales y la de esta
integración. La comprobación de conservación distingue archivos idénticos
de teoremas demostrados; ni un hash ni el número de módulos prueban un PDF.
