# Periodicidad exacta y obstrucción del registro direccional de 108 pasos

**Autores:** Oumar Haidara Fall; Rubén Ramos Balsa  
**Fecha:** 22 de julio de 2026  
**Autoridad semántica:** `CURRENT.json`, revisión 2026-07-22.2  
**Estatuto:** certificado nuevo sobre una fuente histórica no normativa

## 1. Objeto examinado

El libro histórico `rutas_TPK_108_APP9x9.xlsx` contiene cuatro recorridos,
denotados por \(N,E,S,O\), con \(108\) pasos cada uno. En cada paso registra

\[
r(t),\quad \delta(t),\quad \text{movimiento},\quad (i,j),\quad
\text{orientación},\quad A_+(i,j),\quad A_\times(i,j),\quad
d_{\rm lex},\quad \tau(i+j),\quad \tau_{\rm dig}.
\]

La segunda copia del libro es idéntica byte a byte. Ambas tienen huella

\[
\operatorname{SHA256}=
06144b2dec3a0b06a26c771020b082125d5e86c4c066af15a1705ed2c1738966.
\]

El libro se utiliza como cantera documental. No se identifica con el estado
TPK enriquecido ni sustituye su memoria de rama.

## 2. Teorema de periodicidad

Sea \(R_d(t)\) la fila del recorrido \(d\in\{N,E,S,O\}\), excluida la etiqueta
absoluta \(t\). Entonces

\[
\boxed{R_d(t+54)=R_d(t),\qquad 1\leq t\leq54.}
\]

### Demostración

El certificado compara los once campos publicados de cada par de filas
\((t,t+54)\), para las cuatro direcciones. Son

\[
4\cdot54\cdot11=2376
\]

igualdades exactas. No se comparan sumas parciales ni representaciones
gráficas: se comparan las celdas del libro una a una. Todas coinciden. Por
tanto, el registro de \(108\) pasos es la concatenación de dos copias de un
registro de \(54\) pasos. \(\square\)

Al agrupar el recorrido en ventanas consecutivas de nueve pasos,

\[
W_{d,m}=\bigl(R_d(9m-8),\ldots,R_d(9m)\bigr),
\qquad 1\leq m\leq12,
\]

se obtiene inmediatamente

\[
\boxed{W_{d,m+6}=W_{d,m},\qquad 1\leq m\leq6.}
\]

La repetición se conserva al aplicar la transformación de Hadamard a las
cuatro direcciones. El certificado lo verifica para las sumas de las hojas
aditiva y multiplicativa, las dos coordenadas, y la lectura logarítmica
discreta.

## 3. Obstrucción dodecafásica

Considérese un lector determinista \(F\) que:

1. recibe únicamente los campos publicados en una ventana direccional;
2. aplica la misma regla en las doce posiciones;
3. no recibe el índice absoluto de la vuelta ni memoria exterior al libro.

La segunda condición expresa equivariancia por traslación de fase. Como
(W_{m+6}=W_m), se tiene

\[
F(W_{m+6})=F(W_m).
\]

Por consiguiente, toda salida de este tipo posee período divisor de seis.

### Corolario

El libro direccional aislado no puede producir ni el sello dodecafásico

\[
K=(234,543,140,729,659,824,621,058,914,794,146,601)
\]

ni el observable firmado

\[
U_{12}^{\rm sgn}=
(2378,1406,2479,-452,998,-551,-668,-204,-371,-322,-28,-997),
\]

porque ambos distinguen cada posición \(m\) de \(m+6\). Esta comparación se
ejecuta sólo después de demostrar la periodicidad; no selecciona ninguna
regla ni interviene en el teorema.

## 4. Significado matemático

La obstrucción no es un fallo del sistema dodecafásico. Localiza el tipo de
información que la tabla direccional ha olvidado. Las coordenadas, las dos
hojas APP, la orientación visible y los indicadores ternarios vuelven al
mismo valor tras \(54\) pasos. Por ello, la ruptura del período seis requiere
algún dato que no aparece en esta proyección:

- procedencia de rama;
- memoria de cociente y arrastre;
- orientación enriquecida de ida y vuelta;
- supervivencia a futuras fronteras;
- o un dato equivalente del estado TPK completo.

El resultado coincide con la distinción canónica

\[
\mathrm{TPKFullState}\neq\mathrm{CT108RawProjection}.
\]

La tabla sí sirve como control direccional de los movimientos. No contiene,
por sí sola, el dato que separa las dos mitades de la dodecafase.

## 5. Alcance y control negativo

El teorema excluye lectores locales y equivariantes que reciben sólo el libro
publicado. No excluye:

- un lector del ledger TPK enriquecido;
- un lector que conserve memoria coinductiva de rama;
- un mapa que reciba otro estado interno previamente derivado.

También puede romperse artificialmente la repetición introduciendo el número
absoluto de vuelta. Tal modificación distingue \(m\) de \(m+6\), pero la
tabla no proporciona una razón interna para elegir una función concreta de
ese índice. La mera posibilidad de usarlo no constituye una construcción
canónica.

## 6. Procedencia

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: los cuatro recorridos y su división en
  (108=12\cdot9) pasos.
- `CERTIFICADO_NUEVO`: las 2376 igualdades, la periodicidad exacta de 54 pasos,
  su forma en doce ventanas y la obstrucción de período seis.
- `EXACTO_INTERNO`: el resultado es exacto respecto del libro publicado.
- `NO_PROMOCION_AUTOMATICA`: el libro mantiene su estatuto histórico y no
  sustituye al canon vigente.

## 7. Reproducción

Desde la raíz del proyecto:

```bash
python3 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/analizar_registro_direccional_108.py --check-certificate
python3 -O 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/analizar_registro_direccional_108.py --check-certificate
```

Las dos ejecuciones producen resultados idénticos. El verificador utiliza
aritmética entera, lectura directa de OOXML y comprobaciones que permanecen
activas bajo `python3 -O`.
