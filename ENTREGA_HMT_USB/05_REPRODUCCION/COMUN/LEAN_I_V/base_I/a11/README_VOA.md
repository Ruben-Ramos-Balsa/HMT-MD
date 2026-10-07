# Continuación algebraica del retículo seleccionado — Artículo I

Este paquete conserva íntegramente, por huella, los archivos manifestados de
BASE_COMPARTIDA y añade la continuación algebraica sobre **el mismo punto
marcado y el mismo retículo**. No introduce nuevamente el registro publicado.

## Orden operativo

1. El núcleo compartido conserva su orden APP → TRIT → TPK → estado enriquecido
   → publicaciones regionales correlacionadas → registro seleccionado → incidencia.
   Sus lecturas, condiciones y pruebas están en las fuentes heredadas; no se
   sustituyen por los valores numéricos de salida.
2. `SharedArticleIBase` reúne acción, electrón e incidencia. `SelectedLatticeAlgebra`
   prolonga el mismo retículo por el cociclo de signo, la extensión central y
   el álgebra compleja torcida, reutilizando siete módulos previos sin cambios.
3. `SymmetricTransport` y `LatticeOscillatorFock` construyen el portador simétrico
   de modos, sus operadores y las relaciones de conmutación. Los modos abarcan
   todos los índices naturales; no son un corte de dimensión finita. Los modos
   y los grados no tienen cota, pero cada elemento es una combinación algebraica
   finita. No se afirma una completación de Hilbert.
4. `WittLatticeZeroModes`, `WittNegationLift` y `LatticeParityCarrier` añaden modos
   cero, desplazamientos del retículo, involución y proyectores par/impar.
5. `APPFockRigidity` conserva el origen aritmético del índice 54 y la rigidez del
   parámetro positivo 12. `APPFockIndex` construye el operador finito de grado dos
   sobre 24 + 300 coordenadas: su dimensión es 324 y su traza es 54. Comprueba
   también el acoplamiento orientado del agregado suma–producto y el falsador
   de la fuente. La comparación con la norma radial es una igualdad de valores
   construidos; no se usa como un entrelazador operatorio ni como selección del
   registro. `SelectedVOAInput` reúne la continuación sobre el origen seleccionado.
6. `FoundationRegression` repite los controles del contrato común dentro de la
   misma compilación; el suplemento original se conserva íntegro en
   `suplementos/FoundationContract`.

## Reproducción

Se requieren Python 3 (biblioteca estándar), Lean 4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`, con sus dependencias compiladas.
Desde esta carpeta:

```sh
python3 -I -S reproducir_voa.py --plan
python3 -I -S reproducir_voa.py --mathlib /ruta/a/mathlib --lean /ruta/a/lean
```

`--plan` verifica rutas, huellas y clausura de imports; no compila ni demuestra
por sí mismo. La segunda orden compila la clausura declarada, interroga los
axiomas de los teoremas y escribe su resultado en
`resultados/lean_unificado/VERIFICATION.json`. Un ZIP íntegro no equivale a ese
resultado. `PACKAGE_ASSEMBLY.json` acredita sólo la conservación y el montaje.
El recibo causal conserva los nueve campos genealógicos y el alcance heredado.
Su control de metadatos está separado de Lean y no se presenta como un teorema.

El comprobador original `verificar_lean.py` permanece idéntico. La nueva entrada
`reproducir_voa.py` amplía sus raíces y controles. Los ejecutables históricos se
conservan como procedencia; algunos retienen sus rutas locales originales. La
entrada portátil de esta ampliación es `reproducir_voa.py`.

## Alcance formal exacto

Se conservan explícitos la interfaz S8 no ordenada del antecedente y el límite
de confianza `Lean.ofReduceBool` de su selector finito. Esta ampliación no los
elimina ni los convierte en un nuevo axioma. No incorpora una hipótesis de
igualdad con el registro para sustituir su selección anterior.

Las nuevas pruebas construyen cociclo, extensión central, álgebra torcida,
portador oscilatorio, conmutadores, modos cero e involución sobre el retículo
seleccionado. El álgebra asociativa torcida no se identifica con una VOA completa.
La descomposición par/impar es la del portador no torcido; no afirma haber
construido por ella sola el módulo torcido ni el producto del orbifold.
La involución corresponde al cociclo triangular construido; no presupone una
identificación con una normalización diagonal específica de FLM.

**FLM y Moonshine no se han añadido como axiomas.** La compilación de esta
continuación no se presenta como formalización íntegra de esos teoremas ni de
todo el PDF. Los desarrollos LaTeX copiados bajo `procedencia/latex` documentan
la composición y sus fuentes; copiarlos no transforma sus teoremas en pruebas Lean.

## Conservación y caché

`versiones_previas/MANIFIESTO_BASE_COMPARTIDA.json` conserva el manifiesto de
partida. Todos sus archivos mantienen su contenido y ruta relativa. El suplemento
FoundationContract también se copia byte a byte, incluidos sus testigos históricos.
Sus objetos compilados históricos son procedencia y no se adoptan como caché del
nuevo runner.

Si se solicitó caché local, los 122 objetos de la base se copian sólo después de
verificar fuentes y huellas contra su recibo. Quedan en `resultados/`, fuera del
manifiesto y del ZIP. El runner vuelve a validar sus dependencias, compilador y
huellas; no acepta como acierto una caché sin recibo. Quien recibe únicamente el
ZIP recompila los módulos propios sobre el mismo Mathlib.
