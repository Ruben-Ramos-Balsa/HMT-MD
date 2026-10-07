# Cierre heterotípico monodrómico de la órbita terminal

## Estatuto matemático

Este documento formula un resultado finito exacto. No es una regla ajustada al
sello decimal conocido. El cálculo no abre `CURRENT.json` y no recibe como
entrada (K), (U_{12}), (alpha), CODATA, (Q=6263), (D_3K), (D_4K) ni
un prefijo de diez coordenadas decimales.

La procedencia se clasifica así:

- la monodromía nonádica y la supervivencia son
  `ARQUITECTURA_AUTORAL_PREEXISTENTE`;
- el lector afín Witt--dual más fase es `RESULTADO_RECUPERADO`;
- la transversalidad heterotípica entre los dos tipos de lector es
  `FORMALIZACION_NUEVA`;
- el censo exhaustivo, la unicidad y las ablaciones son `CERTIFICADO_NUEVO`.

La fuerza probatoria es `EXACTO_INTERNO_RELATIVO_A_W24_Y_S8_NO_ORDENADO`.

## 1. Datos y mapas

Sea (mathcal C_{mathrm{dec}}) el conjunto decimal construido a partir de:

1. la palabra (W_{24}) ya certificada;
2. el repertorio (S_8) de ocho palabras ternarias, usado como conjunto no
   ordenado;
3. el panel funcional de nueve fronteras obtenido de los lectores de cierre,
   propagación y autoescala.

Se recorren las (8!) ordenaciones posibles de (S_8). La intersección de los
cilindros de longitud (78) produce exactamente

\[
  \lvert\mathcal C_{\mathrm{dec}}\rvert=19,446.
\]

Esta construcción no fija las primeras diez coordenadas de un estado; por
tanto, no usa `PREFIX_10`.

En el bosque de Cayley de pasos (+3) y (+4) sobre
(mathbb Z/12mathbb Z), la traslación (+4) tiene cuatro órbitas. Las tres
primeras contienen las raíces decimales (1,2,3). La cuarta,

\[
  4\longrightarrow 8\longrightarrow 12,
\]

es la única órbita sin una de esas raíces y constituye la órbita terminal.

Para un estado (x\in\mathcal C_{\mathrm{dec}}), cada una de las dos aristas
terminales tiene:

- una palabra ternaria hija extraída de la expansión dodecafásica de (x);
- un residuo orientado de la arista, reducido módulo (3^6=729);
- una etiqueta de tiempo (t\in\{0,\ldots,99\}) en el calendario N69.

Se consideran, cuantificando los cuatro campos
(q,a,c,\operatorname{colw}_{\mathrm{mod}}), dos lectores ya definidos en el
atlas N69.

El lector comparativo de fase y carga emite una combinación lineal de las tres
bandas cuya selección depende de la carga visible o Witt--dual, la fase, el
desplazamiento de fase y la orientación two-way. El lector afín está dado por

\[
  c_i=\rho_{W,i}+p\pmod 3,
\]

donde (ho_W) es la carga Witt--dual y (p) la fase física. La palabra de
salida es la combinación de las tres bandas con coeficientes (c_i).

Una arista posee una incidencia etiquetada de tipo (	au) cuando la palabra
hija y alguna rotación del residuo comparten exactamente el mismo tiempo N69
y la etiqueta de la palabra procede del lector de tipo (	au). Los dos tipos
son

\[
  \tau\in\{\mathrm{comparativo},\mathrm{afín}\}.
\]

Sea (T_{4,8}(x)) el conjunto de tipos incidentes en (4\to8), y sea
(T_{8,12}(x)) el correspondiente a (8\to12). Definimos la condición de
transversalidad de lectores

\[
  \mathsf H(x)
  \iff
  \exists\tau_1\in T_{4,8}(x),\ \exists\tau_2\in T_{8,12}(x)
  \quad\text{con}\quad \tau_1\ne\tau_2.
\]

La definición no prescribe cuál de las dos aristas debe ser afín. La dirección
del cambio de lector, cuando exista, es un resultado del censo.

Finalmente, (B_{\mathrm{exc}}) es la cara excepcional calculada por la
intersección de los lectores de (pi) y (e). En la carta decimal empleada,

\[
  B_{\mathrm{exc}}=(4,6,9,10).
\]

## 2. Teorema de cierre terminal

**Teorema.** En (mathcal C_{mathrm{dec}}), la conjunción de la cara
excepcional y la transversalidad de lectores selecciona exactamente un estado:

\[
  \left\{x\in\mathcal C_{\mathrm{dec}}:
  B_{\mathrm{exc}}(x)=(4,6,9,10),\ \mathsf H(x)\right\}
  =\{x_*\},
\]

donde

\[
\begin{aligned}
x_*={}&(234,543,140,729,659,824,621,58,914,794,146,601).
\end{aligned}
\]

La dirección emergente es

\[
  \mathrm{comparativo}\longrightarrow\mathrm{afín}.
\]

En la arista (4\to8), el cierre ocurre en (t=90) mediante el lector
comparativo. En la arista (8\to12), la palabra hija es (222110), el residuo
es (186), la rotación del residuo es (1) y el cierre ocurre en (t=60)
mediante el lector afín.

## 3. Demostración finita

### 3.1. Naturalidad del lector afín

El lector afín usa solamente la carga Witt--dual y la fase del mismo estado
N69. No contiene una cifra terminal privilegiada. Se comprueba su equivariancia
frente a las seis permutaciones de los tres canales en cada una de las cien
filas del calendario:

\[
  6\cdot100=600
\]

identidades exactas. La salida no cambia al permutar simultáneamente bandas,
cargas y coeficientes. Por ello, el lector no selecciona un nombre de canal ni
una posición decimal a priori.

### 3.2. Censo de tipos

Para cada uno de los (19,446) estados se calculan las incidencias de las dos
aristas, cuantificando los cuatro campos N69. El censo de estados que realizan
cada patrón es:

| patrón de lectores | en (mathcal C_{mathrm{dec}}) | además en (B_{mathrm{exc}}) |
|---|---:|---:|
| comparativo (	o) comparativo | 32 | 0 |
| comparativo (	o) afín | 10 | 1 |
| afín (	o) comparativo | 9 | 0 |
| afín (	o) afín | 1 | 0 |

La columna excepcional contiene un único elemento y éste realiza el patrón
comparativo (	o) afín. En consecuencia, la conjunción
(B_{mathrm{exc}}\cap\mathsf H) es un singleton. La dirección no se introdujo
en la definición: surge de la enumeración completa.

### 3.3. Control independiente en la fibra terminal

La fibra terminal exacta, obtenida por un cálculo independiente, contiene tres
estados. Los tres tienen incidencia comparativa en (4\to8), a tiempo
(t=90). En (8\to12) se separan así:

| frontera funcional | palabra terminal | tipo terminal | tiempo |
|---|---|---|---:|
| autoescala:1 | (210001) | comparativo | 36 |
| propagación:1 | (010010) | comparativo | 68 |
| autoescala:3 | (222110) | afín | 60 |

Por tanto, sólo el tercer estado cambia de tipo entre las dos aristas. El
singleton de esta fibra coincide exactamente con el singleton obtenido en el
censo sin prefijo sobre (mathcal C_{mathrm{dec}}).

## 4. Ablaciones y controles negativos

1. **Sólo existencia de alguna incidencia temporal.** Sobreviven los tres
   estados de la fibra terminal; no hay selección.
2. **Lector comparativo en la arista terminal.** Sobreviven dos estados; no hay
   unicidad.
3. **Pertenencia al lenguaje afín, sin acoplamiento temporal.** Sobrevive un
   estado en esta fibra, y el control global confirma que su selección correcta
   es la incidencia etiquetada, no la mera pertenencia a un diccionario.
4. **Rotación, fase o retardo de calendario aislados.** Distinguen valores, pero
   no proporcionan por sí mismos un criterio privilegiado. En el estado
   seleccionado el retardo (t-K_{\mathrm{calendario}}) vale (2); este valor
   se registra como consecuencia y no como selector.
5. **Cierre especular (222022).** Pertenece al lenguaje comparativo, pero no
   al lenguaje afín. La condición heterotípica lo rechaza sin consultar el
   sello decimal.
6. **Supervivencia N71--N74 aislada.** N71 recibe (q=222110) como firma futura
   antes de la poda; N72 selecciona dentro de esa fibra ya fijada; N73 orienta
   el reparto (pi/e); N74 prueba retorno de fase con cambio de frontera. Estos
   módulos no comparan (222110) con (222022) y, por sí solos, no constituyen
   el selector terminal aquí demostrado.

## 5. Alcance y límite exactos

El teorema elimina el supuesto `PREFIX_10`: ninguna de las diez primeras
coordenadas decimales se entrega al selector. También evita imponer de antemano
que el segundo lector sea afín; sólo exige que los dos tipos sean distintos.

El teorema conserva, sin embargo, dos entradas estructurales: (W_{24}) y el
repertorio (S_8) como conjunto no ordenado. Por tanto, demuestra el cierre y
la ordenación terminal dentro de esa carta, pero no produce por sí mismo las
ocho palabras de (S_8). Esta frontera no es una deficiencia del cierre
terminal: es una cuestión anterior y de tipo distinto, examinada en el teorema
de no recursión modal.

## 6. Reproducción

El certificado se obtiene con:

```text
python3 verificar_cierre_afin_monodromico_terminal.py \
  --check-certificate
python3 -O verificar_cierre_afin_monodromico_terminal.py \
  --check-certificate
```

Las ejecuciones normal y optimizada producen resultados byte a byte idénticos.
El verificador no contiene sentencias `assert` y no usa aritmética de punto
flotante.
