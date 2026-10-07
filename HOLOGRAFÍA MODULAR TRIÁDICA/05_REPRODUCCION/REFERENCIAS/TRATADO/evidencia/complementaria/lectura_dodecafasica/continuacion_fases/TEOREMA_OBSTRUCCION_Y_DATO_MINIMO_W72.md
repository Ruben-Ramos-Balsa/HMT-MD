# Caracteres de fase, obstrucción local y coordenadas mínimas del sello

> **Actualización tipada.** La minimalidad lineal demostrada aquí se conserva,
> pero la elección concreta del bosque ha sido refinada por la descomposición
> orbital del paso (+4). La carta vigente para este cierre y su relación de
> sustitución están en
> `TEOREMA_COCICLOS_N69_Y_SECCION_DIRECCIONAL.md`. El presente archivo se
> mantiene como testigo de la cobertura (W_{72}) y de la primera
> formalización de la interfaz de nueve aristas.

**Autores:** Oumar Haidara Fall; Rubén Ramos Balsa  
**Autoridad semántica:** `CURRENT.json`, revisión 2026-07-22.2  
**Fecha:** 22 de julio de 2026

## 1. Resultado

El prefijo ya construido sin utilizar el sello ni la constante de estructura
fina es

\[
W_{24}=020022\mid222111\mid211201\mid021101.
\]

Este prefijo determina exactamente las tres primeras coordenadas decimales

\[
(K_1,K_2,K_3)=(234,543,140).
\]

La pregunta restante consta de dos partes diferentes:

1. comprobar si los caracteres locales de fase y carga contienen los ocho
   bloques que prolongan (W_{24}) hasta (W_{72});
2. determinar qué información es necesaria para ordenar esos bloques y
   reconstruir el estado dodecafásico.

La respuesta exacta es la siguiente.

* La familia natural de caracteres por comparación fase--carga contiene siete
  de los ocho bloques del sufijo. El único ausente es
  (W_{10}=001001).
* Un carácter afín muy simple de la misma frontera produce exactamente ese
  bloque en (t=30), sin consultar (K), \(\alpha\) ni ninguna constante
  metrológica.
* La presencia de los ocho bloques no establece todavía su orden. Fijadas las
  tres coordenadas que ya proporciona (W_{24}), la información lineal mínima
  para reconstruir (K\in\mathbb Z^{12}) consta de nueve cociclos orientados.
  Existe una elección canónica sobre los pasos (3) y (4) cuya matriz tiene
  determinante (-1).

Así, la obstrucción deja de ser una ausencia indeterminada. Se separa en una
obstrucción de **contenido**, que queda resuelta por el carácter afín, y una
obstrucción de **orden dodecafásico**, cuya interfaz mínima se identifica y se
demuestra.

## 2. La familia local fase--carga

Sea

\[
B_t=
\begin{pmatrix}
b_{t,\pi}\\ b_{t,e}\\ b_{t,\varphi}
\end{pmatrix}\in M_{3\times6}(\mathbb F_3)
\]

la frontera superviviente de N69. Se consideran dos cargas por canal:

\[
r_i(B_t)=\sum_{j=1}^6(B_t)_{ij},
\qquad
\rho_{W,i}(B_t)=\sum_{j=1}^6(B_tA_W)_{ij}pmod3.
\]

La primera es la carga visible de fila; la segunda es su transporte por la
rotación interna de Witt. Sea (p_t=(t-1)\bmod3) la fase física. Para

\[
q\in\{r,\rho_W\},\qquad
\delta\in\mathbb F_3,\qquad
\varepsilon\in\{+1,-1\},
\]

definimos

\[
c_i(q,p_t;\delta,\varepsilon)=
\begin{cases}
\varepsilon,&q_i=p_t+\delta,\\
-\varepsilon,&q_i\ne p_t+\delta,
\end{cases}
\]

y el carácter

\[
\chi_{q,\delta,\varepsilon}(B_t)
=\sum_{i=1}^3c_i(q,p_t;\delta,\varepsilon)b_{t,i}
\in\mathbb F_3^6.
\]

Esta definición agota las tres traslaciones de la fase, ambas orientaciones y
las dos cargas naturales ya presentes en el registro. Conmuta con la
permutación simultánea de los canales y no privilegia una cifra decimal.

## 3. Teorema de obstrucción local

### Teorema 1

Al aplicar todos los caracteres

\[
\chi_{q,\delta,\varepsilon},
\qquad
q\in\{r,\rho_W\},\ delta\in\mathbb F_3,
\ \varepsilon\in\{+1,-1\},
\]

a las cien fronteras (B_0,\ldots,B_{99}) de N69, las posiciones del sello
que aparecen son

\[
\{4,5,6,7,8,9,11,12\}.
\]

En particular,

\[
\boxed{001001=W_{10}\notin
\operatorname{im}\{\chi_{q,\delta,\varepsilon}\}.}
\]

Por tanto, ningún selector que se limite a reordenar salidas de esta familia
puede prolongar (W_{24}) hasta (W_{72}).

### Demostración

El certificado recorre literalmente las cien filas N69, recalcula ambas
cargas desde cada matriz (B_t), genera los doce caracteres locales por fila
y compara sus salidas con los doce bloques de (W_{72}). Para la carga
Witt--dual se obtienen las posiciones

\[
\{4,5,6,7,9,11,12\};
\]

para la carga visible,

\[
\{5,6,7,8,12\}.
\]

Su unión es exactamente

\[
\{4,5,6,7,8,9,11,12\},
\]

y no contiene la posición diez. Como una permutación de salidas no puede
crear una palabra que no está en la imagen, la imposibilidad es inmediata.
\(\square\)

El teorema no afirma que ningún operador imaginable pueda generar el bloque.
Afirma algo más preciso y comprobable: la familia local natural ya
investigada no puede hacerlo.

## 4. El carácter afín que completa el contenido

En la frontera (t=30) se tiene

\[
\rho_W(B_{30})=(0,1,2),
\qquad
p_{30}=2.
\]

Definimos ahora el carácter afín

\[
\widetilde c_i=\rho_{W,i}(B_{30})+p_{30}\pmod3.
\]

Entonces

\[
\widetilde c=(2,0,1)
\]

y la evaluación directa produce

\[
\boxed{
\widetilde\chi(B_{30})
=2b_{30,\pi}+b_{30,\varphi}
=001001.
}
\]

Este resultado tiene tres propiedades importantes.

1. El coeficiente se calcula a partir de la fase y de la carga Witt--dual de
   la propia frontera.
2. No intervienen (K), \(\alpha\), CODATA ni una comparación con una cifra
   real.
3. Es exactamente el único bloque del sufijo que faltaba en la imagen de la
   familia por comparación.

En consecuencia, la familia ampliada contiene los ocho bloques necesarios:

\[
002001, 020111, 200110, 121012,
010122, 001001, 221110, 222110.
\]

Éste es un cierre de **cobertura**. Aún no es un emisor ordenado: la prueba no
identifica una regla única que asigne esas ocho incidencias, en ese orden, a
los sectores (5,\ldots,12).

## 5. La interfaz lineal mínima de orden

El prefijo (W_{24}) fija (K_1,K_2,K_3). Consideremos el grafo de Cayley

\[
\operatorname{Cay}(\mathbb Z/12\mathbb Z;\,+3,+4).
\]

Tomamos como raíces los sectores (1,2,3) y el siguiente bosque orientado:

\[
\begin{aligned}
1&\to4 &&(+3),&
1&\to5 &&(+4),\\
4&\to7 &&(+3),&
4&\to8 &&(+4),\\
5&\to9 &&(+4),&
7&\to10&&(+3),\\
7&\to11&&(+4),&
8&\to12&&(+4),\\
2&\to6 &&(+4).
\end{aligned}
\]

Para una arista (u\to v), sea

\[
\delta_{uv}=K_u-K_v.
\]

### Teorema 2

La aplicación

\[
\Theta:\mathbb Z^{12}\longrightarrow\mathbb Z^{12},
\qquad
K\longmapsto
\bigl(K_1,K_2,K_3,(\delta_{uv})_{uv\in F}\bigr)
\]

es un automorfismo de retículas. En el orden anterior,

\[
\det\Theta=-1.
\]

Por tanto, las tres raíces y las nueve diferencias reconstruyen un único
sello entero, sin divisiones ni condiciones de congruencia adicionales.

### Demostración

El bosque tiene doce vértices, tres componentes y nueve aristas. Cada
componente posee una raíz fijada. Si (u\to v), entonces

\[
K_v=K_u-\delta_{uv}.
\]

La propagación desde las tres raíces determina sucesivamente todos los
vértices. La matriz formada por las tres evaluaciones de raíz y las nueve
filas de incidencia del bosque tiene determinante (-1); luego su inversa
tiene coeficientes enteros. \(\square\)

### Minimalidad

Una vez fijados (K_1,K_2,K_3), quedan nueve grados de libertad enteros. Un
mapa lineal con menos de nueve coordenadas escalares tiene rango menor que
nueve y, por tanto, no puede ser inyectivo. Las nueve diferencias anteriores
alcanzan exactamente ese límite. La interfaz no sólo es suficiente: es
mínima dentro de la clase lineal.

## 6. Evaluación canónica

Las nueve coordenadas correspondientes de las cartas (D_3,D_4) son

\[
(-495,-425,108,671,-255,-173,475,-543,-281).
\]

Partiendo de

\[
(K_1,K_2,K_3)=(234,543,140),
\]

la integración sobre el bosque da, sin utilizar \(\alpha\),

\[
\boxed{
K=(234,543,140,729,659,824,621,058,914,794,146,601).
}
\]

Las tres transformadas de Hadamard sobre las órbitas de paso tres producen

\[
\boxed{
U_{12}=(2378,1406,2479,-452,998,-551,
-668,-204,-371,-322,-28,-997).
}
\]

El certificado prueba además la fórmula sobre 250 vectores enteros
independientes. La evaluación canónica utiliza las nueve diferencias
publicadas como entrada; no afirma haberlas extraído ya de R36.

## 7. Localización exacta de la flecha restante

El resultado sustituye una frase vaga por un diagrama tipado:

\[
W_{24}
\longrightarrow(K_1,K_2,K_3),
\]

\[
\boxed{
\text{estado TPK enriquecido}
\longrightarrow
(\delta_{uv})_{uv\in F}
}
\quad\text{[mapa de agregación que debe realizarse]},
\]

\[
(K_1,K_2,K_3,\delta_F)
\xrightarrow[\det=-1]{\Theta^{-1}}
K
\xrightarrow{H_4^{\oplus3}}
U_{12}.
\]

La familia fase--carga y su extensión afín demuestran que el registro contiene
incidencias de los ocho bloques. El bosque demuestra qué información ordenada
es suficiente y mínima. Lo que debe construir el agregador no es de nuevo el
sello entero, ni (\alpha), ni veinticuatro diferencias redundantes: son
exactamente nueve cociclos orientados sobre este bosque, o una carta integral
equivalente de rango nueve.

## 8. Estatuto de procedencia y fuerza probatoria

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: monodromía N69, cargas visible y
  Witt--dual, orientación en dos sentidos, pasos (3/4), cartas (D_3,D_4) y
  transformación de Hadamard.
- `RESULTADO_RECUPERADO`: (W_{24}), las doce palabras ternarias del sello y
  las diferencias publicadas.
- `FORMALIZACION_NUEVA`: familia completa de comparación fase--carga y carta
  raíz--bosque.
- `RESULTADO_NUEVO`: localización del único defecto de cobertura en
  (W_{10}=001001) y carácter afín (\rho_W+p) que lo resuelve en (t=30).
- `CERTIFICADO_NUEVO`: barrido exhaustivo de las cien fronteras, determinante
  (-1), rango nueve, reconstrucción de (K,U_{12}) y 250 pruebas enteras.

Capas probatorias:

- obstrucción de la familia local: `EXACTO_INTERNO`;
- carácter afín de (t=30): `EXACTO_INTERNO` como incidencia;
- reconstrucción por bosque: `EXACTO_INTERNO` para todo
  (K\in\mathbb Z^{12});
- evaluación del sello: `RELATIVO_A_PRIMITIVAS`, porque las nueve diferencias
  son datos de entrada de la carta;
- producción de esas nueve diferencias desde la dinámica: tarea única aún no
  realizada por este certificado.

## 9. Reproducción

```bash
python3 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_obstruccion_y_dato_minimo_w72.py --check-certificate
python3 -O 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_obstruccion_y_dato_minimo_w72.py --check-certificate
```
