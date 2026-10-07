# Continuación reticular: productos de campos y estructura conforme

Este paquete conserva íntegros los **2076 archivos** del sucesor de traslación
en `antecedente/`. Añade la involución comprobada de todos los campos, el cierre
conforme de 17 módulos y el cierre exacto de productos/Virasoro del recibo final.
Las fuentes añadidas son 33 módulos; las copias en los recibos son sus
testigos de compilación, no desarrollos alternativos.

## Resultado y cadena de reproducción

Se reutiliza el mismo origen seleccionado por APP–TRIT–TPK, el mismo estado
enriquecido, el retículo marcado, la base integral, el cociclo, el vacío y el
mapa estado–campo. No se vuelve a seleccionar K ni se introduce una función
modular o un valor objetivo como generador. La estructura discreta conjunta
del continuo y su procedencia permanecen en el antecedente sin disgregación.

La secuencia nueva es: inversa del Gram derivada → estado cuadrático ω →
modos reales de su campo → `L₀=E` y `L₋₁=T` → conmutador con todos los modos
de Heisenberg → defecto central y recurrencia cúbica → término central
calculado sobre todas las cargas puras → relaciones completas de Virasoro,
con carga central 24 leída del rango ya construido. Los productos residuales
se identifican con los campos de los estados correspondientes; se conserva
la restricción al sector fijo no torcido de la involución.

El recibo `recibos/productos/VERIFICATION.json` contiene
119 declaraciones públicas y
111 teoremas/lemas del último incremento, después
de autenticar 340 módulos antecedentes. Sus entradas solicitadas son:

- `SelectedConformalVertex`
- `LatticeEvenLocality`
- `LatticeEvenConformal`

La cadena anterior no es una afirmación de cierre del sector torcido,
la multiplicación orbifold, la identificación del Monster o el teorema FLM.
Esos objetos no se obtienen renombrando el portador ni suponiendo una
interfaz que reciba su conclusión. El alcance exacto está en las declaraciones
Lean, no en el número de archivos. La especialización seleccionada conserva `Lean.ofReduceBool` únicamente en las declaraciones enumeradas por el recibo: `HMT.I.SelectedConformalVertex.selected_vertex_products`, `HMT.I.SelectedConformalVertex.selected_virasoro`, `HMT.I.SelectedConformalVertex.selected_local_conformal_publication`.

## Contenido

- `lean/vertex`, `lean/conformal`, `lean/involution`: fuentes nuevas reunidas
  según sus propietarios; no se editan las fuentes anteriores.
- `antecedente/`: paquete anterior completo, incluidos sus antecedentes,
  fuentes, demostraciones, programas y documentos de procedencia.
- `recibos/`: registros completos, consultas y objetos compilados autenticados.
  Los `.olean` históricos se conservan; no sustituyen las fuentes ni sus pruebas.
- `MANIFIESTO.json`: ruta, tamaño y SHA-256 de cada archivo entregado.
- `reproducir.py`: entrada única que configura las rutas internas relativas.

## Ejecución

Desde la carpeta desplegada:

```sh
python3 -I -S reproducir.py --plan --report-dir plan_nuevo
python3 -I -S reproducir.py --report-dir resultados_nuevos
```

`--plan` autentica y resuelve las dependencias, pero **no compila ni demuestra**.
La segunda orden compila únicamente el incremento nuevo y consulta todas sus
declaraciones públicas. Los directorios de resultados deben ser nuevos.
Los 340 módulos anteriores se reutilizan tras verificar sus fuentes, objetos,
recibos, compilador y dependencias; Mathlib no se reconstruye.

Se necesita el entorno externo de Lean 4.21.0 y el checkout de Mathlib fijado
por `compiler.mathlib_commit` en el recibo. No se copia otra biblioteca por
cada lema ni se descarga software automáticamente. En otra máquina indique:

```sh
python3 -I -S reproducir.py --lean /ruta/bin/lean --mathlib /ruta/mathlib4 \
  --report-dir resultados_nuevos
```

Todas las opciones `--*-root`, `--*-report-dir`, `--base` y `--*-helper`
siguen disponibles para una reorganización explícita. Las fuentes y recibos
de esta entrega son autocontenidos; el compilador y la biblioteca estándar
matemática son requisitos del entorno, no pruebas nuevas suministradas como
axiomas. La comprobación causal documental y la conservación de archivos
son controles distintos de la comprobación de los teoremas por Lean.
