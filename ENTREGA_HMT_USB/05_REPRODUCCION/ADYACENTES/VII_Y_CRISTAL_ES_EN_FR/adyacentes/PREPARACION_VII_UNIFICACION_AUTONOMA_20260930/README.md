# Preparación material de VII: acción conjunta y gravitación

Esta carpeta es una preparación separada, no una edición publicada ni un PDF
compilado. La fuente de VII del 29 de septiembre y la entrega anterior permanecen
intactas. No se añade Feigenbaum como dependencia de este desarrollo.

## Ensamblaje

`ensamblar_preparacion.py` copia íntegramente la fuente de **Relaciones estructurales
entre las constantes físicas** a `copia_vii/`. Conserva su núcleo, antecedentes,
desarrollos, figura PDF y fuentes de figuras. La única transformación de esa base
es aditiva. El cuerpo se inserta en `main.tex`, inmediatamente después de
`desarrollos/normalizacion_conjunta.tex` y antes de `desarrollos/narrativa.tex`:

1. El nuevo fragmento `00_antecedentes*.tex`, recibido en `latex/`.
2. `02_color_y_representacion_interna.tex`, antecedente material de color.
3. `10_gravedad_energia_autoinercia.tex`, copia literal de la entrega anterior.
4. `20_accion_retroaccion_restricciones.tex`, copia literal de la misma entrega.

El programa no condensa solapamientos ni elimina demostraciones. Los dos fragmentos
conservan sus hipótesis y la distinción entre el lector radial `H_X`, el Hamiltoniano
conjunto y la realización canónica precuántica. La preparación no convierte una
identidad radial ni la planitud característica en un cierre cuántico global.

El anuncio `latex/01_anuncio_resultado.tex` se incorpora mediante un input en la
variante `desarrollos/apertura_unificacion_20260930.tex`, justo antes de las
palabras clave. La apertura original sigue íntegra en su ruta; sólo cambia la
llamada de `main.tex` a la variante. `latex/40_conclusion_integracion.tex` se
incluye después de la conclusión original, dentro del mismo grupo tipográfico.
Retirar esos inputs recupera literalmente los textos de base. No se reemplazan
las conclusiones previas por el nuevo enunciado.

Desde esta carpeta:

```text
python3 -I -S ensamblar_preparacion.py
python3 -I -S ensamblar_preparacion.py --check-only
python3 -I -S registrar_integracion.py
```

Si el antecedente todavía no está disponible, se materializan las restantes copias
y el informe registra expresamente el input aún no resuelto; no se crea un texto
vacío ni se anuncia completo el ensamblaje. Puede seleccionarse una ruta explícita
con `--antecedentes RUTA`. Una copia modificada manualmente se preserva: el programa
se detiene antes de sobrescribirla. No hay opción de compilación ni comandos de
sellado o publicación.

## Fuentes y evidencia locales

- `copia_vii/main.tex`: entrada LaTeX de la preparación; sus inputs y figura son
  relativos a esta carpeta. El árbol puede trasladarse sin depender de rutas
  absolutas de la máquina para esos recursos.
- `evidencia_ronda/`: textos, scripts, recibos y datos pequeños de la ronda
  matemática del 29–30 de septiembre. Se conservan literalmente, sin declarar
  ejecutados de nuevo sus controles ni modificar rutas históricas internas.
- `fuentes_propietarias/`: copias locales de propietarios ya reunidos en la
  entrega anterior, con sus subdirectorios de procedencia. Su presencia no
  significa que estén incluidos en el cuerpo LaTeX ni sustituye sus pruebas.
- `procedencia_entrega/`: mapas editoriales anteriores, conservados como
  procedencia y no confundidos con el estado del nuevo ensamblaje.
- `PROCEDENCIA_ENSAMBLADO.json`: fuente, copia, SHA-256, tamaño y transformación
  de cada archivo. La inserción del main se puede retirar exactamente para
  recuperar el original. No es un sellado del paquete precedente.
- `CONTROL_ENSAMBLADO.json`: recorrido de inputs, figuras, etiquetas y referencias,
  con distinción de incidencias heredadas y nuevas.
- `DESARROLLO_ACUMULADO.md`: los seis fragmentos íntegros, cada uno con ruta, huella
  y bloque LaTeX; se genera después de materializarlos, sin nuevos enunciados.
- `registros_integracion/AGREGADO_SEIS_FRAGMENTOS.tex`: agregado literal para las
  puertas documentales de genealogía y constantes, no entrada alternativa al main
  ni documento destinado a compilar. `registrar_integracion.py` adapta el generador
  focal existente sin modificar las puertas ni el núcleo heredado.

El entorno TeX no se incluye: la base utiliza LuaLaTeX o XeLaTeX con `fontspec`,
`unicode-math`, STIX Two y los paquetes declarados en su preámbulo. No se ha
instalado ni ejecutado un compilador. Los programas de evidencia conservan sus
dependencias originales; portabilidad de fuentes LaTeX y reproducción científica
de cada programa son controles diferentes.

## Alcance de los controles

La lectura estática sigue los inputs literales y el `input@path` conservado del
núcleo `base_articulo_I`. Detecta recursos ausentes, ciclos, etiquetas duplicadas
y referencias no resueltas. Distingue incidencias que ya estaban en VII de las
introducidas por los fragmentos. También repite ese recorrido sobre una copia
temporal trasladada y compara los resultados, sin recurrir al árbol original.
No ejecuta macros arbitrarias, no inspecciona
páginas y no sustituye una compilación.

Un resultado `PASS_PREPARACION_MATERIAL_FOCAL` acredita únicamente la copia y ese
ensamblaje literal. **No acredita autonomía demostrativa, validación matemática
global, aprobación editorial ni inclusión efectiva en un PDF.** La residencia de
las dependencias necesarias debe contrastarse semánticamente con el contenido
completo del antecedente nuevo, los fragmentos y el núcleo conservado. La skill
`preserve-hmt-continuity` exige mantener separados esos controles; por ello la
carpeta conserva las pruebas completas y no las reemplaza por un inventario.
