# Ejecución encadenada del selector regional

Este suplemento compone el selector racional publicado con los registros de
transición ya formalizados. No modifica el artículo ni el paquete anterior.

## Resultado

`IteratedCylinderSelector.lean` prueba que:

1. La búsqueda inicial termina cuando los extremos racionales tienen la
   misma parte entera. Esa parte entera se calcula; no se suministra.
2. Cada siguiente dígito se selecciona dentro del cilindro del padre
   calculado en el paso anterior. La publicación futura no es una entrada.
3. La ejecución no falla a ninguna profundidad natural y coincide con la
   publicación regional previamente demostrada.
4. Las palabras y los registros producidos coinciden con los existentes;
   sus dos matrices de transición satisfacen las ecuaciones y son únicas.

El arranque respeta el guard de parte entera de `fractional_bounds`.
La búsqueda de precisión usa `Nat.find` sobre las cotas del lector;
no se afirma que reproduzca el calendario de incrementos concreto de Python.

La definición completa es una formalización matemática en una sección
`noncomputable`. El selector finito `choose` sí es ejecutable. El contador
de esta ejecución es el de refinamiento, no el reloj de nueve transiciones
microscópicas del estado enriquecido completo. No se ha definido uno de esos
relojes mediante el otro ni se afirma que esta composición pruebe esa identidad.

## Dependencias conservadas

- `RationalCellIntegerShift.lean`: traducción entre coordenadas completas y
  fraccionarias, escrita por «Aclarar la tarea».
- `FiniteCylinderSelector.lean`: selección mediante recorte y candidato único,
  escrita por «Aclarar la tarea».
- Base sellada: `PAQUETE_ARTICULO_I_SUPERVIVENCIA_REGISTROS_20260919`, 257 módulos.
  Se reutilizan sus objetos autenticados; no se rehacen sus demostraciones.

## Reproducción local

Con la base y la biblioteca Mathlib de la entrega instaladas en sus rutas
registradas, ejecutar desde esta carpeta, por orden:

```sh
python3 compile_local.py RationalCellIntegerShift
python3 compile_local.py FiniteCylinderSelector
python3 compile_local.py IteratedCylinderSelector
```

El comprobador fija la huella del recibo base, comprueba fuentes y objetos
importados, ejecuta Lean 4.21.0 y exige las consultas de axiomas enumeradas.
Admite únicamente `propext`, `Classical.choice` y `Quot.sound` en estos módulos.
Un fallo reemplaza el estado anterior por FAIL; no conserva un PASS obsoleto.

Esta carpeta es el suplemento de desarrollo para integración, no un reemplazo
del paquete autónomo de entrega. No declara formalizados FLM/Monstruo ni todos
los resultados del artículo I.
