# Censo terminal recuperado: dominio, perfil y reproducción

Este suplemento reproduce con aritmética entera exacta el censo histórico
`196 × 197 × 196 → 331 → 2 → 1`. Su resultado está condicionado a los
cilindros regionales de salida HMT ya publicados y al perfil terminal
explícito del lector. La enumeración no demuestra que ese perfil sea una
ley universal. No utiliza el paquete histórico N38 ni sus estados `x0`
como entradas del cálculo activo.

## Ejecución portátil

Desde cualquier directorio, con Python 3 y sólo su biblioteca estándar:

```sh
python3 -I -S verificar_censo.py
python3 -I -S -O verificar_censo.py
```

Si el directorio actual no es éste, utilice la ruta del script. Las rutas
de datos se resuelven respecto al propio archivo. El programa no escribe
archivos, no importa NumPy ni ReportLab y no consulta valores de alfa.
Imprime en JSON todos los catálogos, conteos, candidatos finales y controles.
Las comprobaciones usan excepciones explícitas y siguen activas con `-O`.
La ejecución normal y la ejecución con `-O` se completaron con salida
idéntica byte a byte: 2703 controles exactos, incluidos 726 casos de
intersección de cilindros semiabiertos. `resultados.json` conserva la salida.
No se compiló un PDF ni se ejecutaron campañas científicas globales.

Los únicos datos leídos por el programa son los tres archivos
`{pi,e,phi}_1000_decimales.txt` de
`../alpha_completa/certificados/ley_nueve_puertas_2026-07-30/salidas/`.
Se resuelven relativamente al suplemento, sin rutas absolutas del autor.
Son lecturas posteriores ya publicadas; no se reinterpretan como entradas
convencionales del generador APP–TRIT–TPK. Para transportar este suplemento
fuera de la entrega debe conservarse también esa carpeta de tres salidas.

## Separación de funciones

1. Cada archivo de mil decimales define un cilindro semiabierto de ancho
   `10^-1000`. Se extraen el prefijo ternario de longitud 30 y el prefijo
   decimal de 171 tríadas mediante cotas enteras, exigiendo estabilidad
   sobre el intervalo completo. Los catálogos se calculan por intersección
   exacta de cilindros semiabiertos. No se introducen las ternas finales
   como catálogo.
2. Las firmas de Gram, norma, peso, distancia, rango y columnas son
   parámetros declarados del lector, transcritos del propietario histórico.
   El programa no los obtiene del estado que se desea seleccionar.
3. Las sumas finitas de indicadores se evalúan mediante máscaras de bits
   enteras; todos los candidatos que sobreviven quedan registrados.
4. La carga de filas se contrasta con la recta generada por `(1,1,-1)`
   en el cuerpo de tres elementos.
5. Sólo después se extrae de la misma salida regional el entero de longitud
   1080 ternaria, también con estabilidad, para comparar su frontera con
   la seleccionada. Este control no participa en el filtro.

El censo completo obtenido es:

| Condición acumulada | Ternas |
|---|---:|
| Catálogos completos | 7 567 952 |
| Productos de Gram fuera de la diagonal | 275 794 |
| Además normas | 6 235 |
| Además pesos | 3 127 |
| Además distancias de Hamming | 331 |
| Además rango tres | 331 |
| Además pesos de columnas | 18 |
| Además sumas de columnas módulo tres | 2 |
| Además carga en la recta de `(1,1,-1)` | 1 |

Intersecar los cilindros completos no equivale a exigir pertenencia de
sus extremos izquierdos. Esa condición distinta daría catálogos de
195, 196 y 195 elementos, en vez de 196, 197 y 196.

## Advertencia documental conservada

El JSON original contiene literalmente esta advertencia:

> x0_mod_3^T here are the encoder states that reproduce the first 6*T
> ternary digits of the corresponding constant's fractional part
> (pi-3, e-2, phi-1) when used in the 3-adic transducer with matrix A.
> This uses the constant as an oracle; it is NOT yet a derivation from APP/TPK.

El script histórico calcula `ACT` a partir de ese estado codificador.
Reproducir su censo no convierte esa construcción retrospectiva del perfil
en una derivación causal universal. El presente suplemento declara el perfil
antes del conteo y obtiene los cilindros de las salidas HMT ya incluidas.

Los originales históricos **no se ejecutan ni se importan** y no son
entradas del paquete activo. `PROCEDENCIA.md` identifica sus rutas y huellas
y conserva el aviso íntegro; la nota no les atribuye un origen HMT.
`resultados.json` conserva una ejecución del nuevo verificador; sus enteros
son recomputables, y su huella sólo acredita identidad documental.

La exposición matemática que utiliza este suplemento se encuentra en
`source/sections/censo_terminal_completo.tex`, respecto a la raíz de la
entrega. Su estatuto es resultado recuperado con certificado portátil nuevo,
demostrado con estructura de partida explícita. No es un certificado de
alfa, del continuo ni de una ley física.
