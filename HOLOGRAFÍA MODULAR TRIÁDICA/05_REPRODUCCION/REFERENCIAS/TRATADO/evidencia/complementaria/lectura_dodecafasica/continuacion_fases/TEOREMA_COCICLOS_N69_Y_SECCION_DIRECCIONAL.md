# Cociclos dodecafásicos, incidencia N69 y sección direccional mínima

> **Actualización de alcance.** El resultado posterior
> `15_SELECTOR_GLOBAL_DOBLE_LECTURA` construye un selector global que evita
> elegir una dirección de N69 arista por arista, una vez dado el conjunto no
> ordenado de ocho bloques. Por ello, la sección direccional descrita aquí no
> es necesaria en esa factorización global. Los teoremas de imposibilidad de
> los lectores uniformes permanecen exactos. La única dependencia anterior se
> ha trasladado a la selección intrínseca de los ocho bloques y se delimita en
> `TEOREMA_NO_GO_S8_N71_N72.md`.

## 1. Resultado

El cierre mejora en dos puntos precisos.

Primero, existe un bosque de pasos (90/120) determinado por la geometría
de (mathbb Z/12), y no por los valores del sello. Respecto de ese bosque,
los nueve residuos orientados del sello aparecen todos en el atlas de
invariantes N69 sometido a la rotación de Witt. Desaparece así la excepción
artificial que producía una elección anterior del bosque.

Segundo, una vez conocidos esos nueve residuos módulo (3^6=729), la cara
excepcional

\[
B_{\mathrm{exc}}=H_e\cap P_\pi=\{4,6,9,10\}
\]

selecciona una sola de las (64=2^6) elevaciones posibles a
\([0,999]^{12}). El resultado es exactamente

\[
K=(234,543,140,729,659,824,621,58,914,794,146,601).
\]

No se necesita imponer el total (Q=6263). De hecho, (Q=6263) deja quince
elevaciones, mientras que la cara excepcional deja una.

El punto restante queda reducido a un objeto matemático de tipo único: una
**sección direccional** que asigne a cada una de las nueve aristas una
dirección del atlas N69--Witt. El atlas contiene los nueve valores, pero las
familias uniformes naturales de fase, carga, calendario, rotación de Witt y
orientación de ida y vuelta no seleccionan las nueve posiciones a la vez.

## 2. El bosque canónico de pasos (90/120)

Identificamos los doce sectores con (mathbb Z/12). El paso (120), leído
como desplazamiento (+4), descompone el conjunto en las cuatro órbitas

\[
\begin{aligned}
\mathcal O_1&=(1,5,9),&
\mathcal O_2&=(2,6,10),\\
\mathcal O_3&=(3,7,11),&
\mathcal O_4&=(4,8,12).
\end{aligned}
\]

Las tres raíces procedentes del cilindro (W_{24}) ocupan los sectores
(1,2,3). Por tanto, las tres primeras órbitas ya poseen una raíz. La arista
de paso (90), es decir, (1\to4), enraíza la cuarta órbita. Al añadir dos
aristas de paso (+4) en cada órbita se obtiene el bosque

\[
\begin{array}{c|c}
\text{paso }+3 & 1\to4\\
\hline
\text{paso }+4 &
1\to5,\;5\to9,\;
2\to6,\;6\to10,\;
3\to7,\;7\to11,\;
4\to8,\;8\to12.
\end{array}
\]

Ésta es la elección natural porque procede de la descomposición orbital del
paso (+4). No consulta (K), (alpha) ni ninguna cifra decimal objetivo.
Las tres componentes contienen, cada una, una sola de las raíces (1,2,3).

El prefijo (W_{24}) fija mediante intersección exacta de cilindros las tres
coordenadas

\[
(K_1,K_2,K_3)=(234,543,140).
\]

## 3. Atlas N69--Witt

Para cada estado (t=0,\ldots,99), N69 publica cuatro palabras de seis
trits:

\[
q_t,\qquad a_t,\qquad c_t,\qquad w_t.
\]

Sea (J) la rotación interna de Witt empleada por N69, con

\[
J^2=-I.
\]

Definimos el atlas indexado

\[
\mathcal A_{69}
=
\left\{
(t,x,k,J^kx_t):
t\in\{0,\ldots,99\},\;
x\in\{q,a,c,w\},\;
k\in\mathbb Z/4
\right\}.
\]

El atlas tiene (100\cdot4\cdot4=1600) direcciones indexadas y (640)
palabras distintas. La multiplicidad conserva información: dos direcciones
distintas pueden producir la misma palabra visible.

La definición del bosque y la construcción del atlas se ejecutan antes de
leer el sello canónico. Sólo entonces se usa (K) como contraste externo.

## 4. Los nueve residuos orientados

Para una arista orientada (i\to j), escribimos

\[
\omega_{ij}=K_i-K_j,
\qquad
\bar\omega_{ij}=\omega_{ij}\pmod{729}.
\]

En el orden topológico del bosque, el contraste canónico da

\[
\begin{aligned}
(\omega_e)_{e\in E(F)}
=(&-495,-425,-281,-481,671,\\
  &-255,30,475,-543),
\end{aligned}
\]

y por tanto

\[
(\bar\omega_e)_{e\in E(F)}
=(234,304,448,248,671,474,30,475,186).
\]

Sus representaciones de seis trits son

\[
\boxed{
022200,
102021,
121121,
100012,
220212,
122120,
001010,
122121,
020220.
}
\]

Las nueve palabras pertenecen a (mathcal A_{69}). Sus multiplicidades de
dirección, en el mismo orden, son

\[
(5,3,2,1,3,1,1,3,5).
\]

En consecuencia, existen

\[
5\cdot3\cdot2\cdot1\cdot3\cdot1\cdot1\cdot3\cdot5=1350
\]

secciones indexadas que representan esa misma salida ordenada.

Este hecho es una incidencia exacta y significativa: el registro N69 ya
contiene todos los valores residuales necesarios. No es todavía una regla de
selección, porque la pertenencia a un atlas no distingue una dirección entre
varias.

## 5. Teorema de imposibilidad para los lectores uniformes mínimos

La cuestión correcta no es si cada palabra aparece en algún lugar, sino si
una sola regla definida con anterioridad produce las nueve.

Se agotaron cuatro familias.

### 5.1. Canal y potencia de Witt fijos

Se fija (x\in\{q,a,c,w\}) y (k\in\mathbb Z/4), y se permite recorrer
libremente los cien tiempos:

\[
R_{x,k}(t)=J^k x_t.
\]

Hay (16) lectores. El mejor contiene sólo tres de los nueve residuos.

### 5.2. Combinación lineal de todos los invariantes N69

La familia anterior se amplía permitiendo mezclar simultáneamente los cuatro
invariantes. Para

\[
\lambda_q,\lambda_a,\lambda_c,\lambda_w,b,c\in\mathbb F_3,
\qquad k\in\mathbb Z/4,
\]

se considera

\[
R(t)=J^k\left(
\lambda_q q_t+\lambda_a a_t+\lambda_c c_t+\lambda_w w_t
+(bp_t+c)\mathbf1
\right),
\]

donde (p_t) recorre los cinco relojes indicados en el apartado siguiente.
Se agotan

\[
5\cdot3^4\cdot3^2\cdot4=14580
\]

lectores uniformes. El mejor contiene cinco de los nueve residuos. Por tanto,
la obstrucción no procede de haber exigido un único canal.

### 5.3. Carácter afín de fase y carga

Sean (B_{t,1},B_{t,2},B_{t,3}) las tres bandas de frontera. La carga
(chi_i) puede ser visible o Witt--dual. La fase (p) se toma, por separado,
de cualquiera de los cinco relojes publicados:

1. fase física del predecesor;
2. fase de frontera;
3. calendario de Beatty;
4. predecesor del calendario de Beatty;
5. bit de apertura o poda.

Para

\[
a,b,c\in\mathbb F_3,qquad k\in\mathbb Z/4,
\]

se define

\[
c_i=a\chi_i+bp+c,
\qquad
R(t)=J^k\left(\sum_{i=1}^{3}c_iB_{t,i}\right).
\]

La familia contiene

\[
5\cdot2\cdot3^3\cdot4=1080
\]

lectores uniformes. Incluye la inversión de orientación: sobre
(mathbb F_3), el cambio de signo está contenido en los coeficientes y en
(J^2=-I). El mejor lector contiene cuatro de los nueve residuos.

### 5.4. Comparación fase--carga

También se agotó la familia no lineal que asigna un signo según coincidencia:

\[
c_i=
\begin{cases}
\varepsilon,&\chi_i=p+\delta,\\
-\varepsilon,&\chi_i\ne p+\delta,
\end{cases}
\]

con carga visible o dual, tres traslaciones de fase, dos orientaciones y las
cuatro potencias de Witt. Sus (144) lectores alcanzan como máximo tres de
los nueve residuos.

Por tanto:

\[
\boxed{
\text{ninguna regla uniforme de las familias declaradas selecciona los nueve cociclos.}
}
\]

La conclusión no excluye una regla más rica de TPK. Localiza lo que esa regla
debe conservar: una elección dependiente de la arista, sensible a la hoja y a
la orientación.

## 6. Las (64) elevaciones y la cara excepcional

Fijadas las raíces ((234,543,140)) y las nueve congruencias

\[
x_i-x_j\equiv\bar\omega_{ij}\pmod{729},
\]

el barrido exhaustivo de ([0,999]^{12}) produce exactamente (64)
soluciones. La potencia (64=2^6) expresa seis decisiones de hoja: un mismo
residuo módulo (729) puede elevarse, en ciertas coordenadas, a dos valores
del intervalo decimal.

La lectura excepcional se construye sin consultar (K):

\[
P_\pi=\{2,4,5,6,7,8,9,10,11\},
\]

\[
H_e=\{1,3,4,6,9,10\},
\]

\[
B_{\mathrm{exc}}=P_\pi\cap H_e=\{4,6,9,10\}.
\]

Para una elevación (x\), definimos su corona alta por el umbral interno
(3^6=729):

\[
B(x)=\{i:x_i\ge729\}.
\]

El resultado exhaustivo es

\[
\#\{x:B(x)=B_{\mathrm{exc}}\}=1.
\]

El único superviviente es el sello (K) publicado. Como controles de
ablación:

\[
\begin{array}{c|c}
\text{condición}&\text{supervivientes}\
\hline
\sum_i x_i\equiv2\pmod3&64\\
\sum_i x_i=6263&15\\
\operatorname{supp}_+(H_4x)=\{1,2,3,5\}&1\\
B(x)=B_{\mathrm{exc}}&1
\end{array}
\]

La corona excepcional resuelve toda la ambigüedad de elevación sin utilizar
el total entero ni el soporte firmado. La transformación de Hadamard del
superviviente produce exactamente

\[
U_{12}=
(2378,1406,2479,-452,998,-551,-668,-204,-371,-322,-28,-997).
\]

## 7. Dato requerido por una factorización local y alternativa global

Si se exige factorizar el cierre arista por arista, el objeto requerido no es
un escalar, una suma total ni un corrector decimal. Es una sección

\[
\sigma_F:E(F)
\longrightarrow
\{0,\ldots,99\}\times\{q,a,c,w\}\times\mathbb Z/4
\]

tal que, para (sigma_F(e)=(t,x,k)),

\[
\bar\omega_e=J^kx_t.
\]

Una formulación equivalente es un calendario dodecafásico enriquecido que
conserve, para cada arista, canal, hoja, orientación y potencia de Witt.

El certificado prueba dos cosas simultáneas:

1. el codominio correcto ya está en N69: no falta inventar nueve números;
2. N69 visible no distingue una sección entre las (1350) que representan
   la salida canónica.

Una vez construida (sigma_F), el resto del cierre local es forzado:

\[
W_{24}
\longrightarrow
(K_1,K_2,K_3)
\xrightarrow{\;\sigma_F\;}
\text{64 elevaciones}
\xrightarrow{\;B_{\mathrm{exc}}\;}
K
\xrightarrow{\;H_4^{\oplus3}\;}
U_{12}.
\]

Existe, sin embargo, una alternativa global ya certificada. En vez de elegir
nueve direcciones independientemente, se intersecta la familia decimal
completa con la regla N69 estratificada y la cara excepcional. Esa operación
selecciona simultáneamente la regla y el sello, pero es relativa al conjunto
no ordenado de ocho bloques. Por tanto, la sección (sigma_F) deja de ser el
único cierre posible; el problema anterior común a ambas factorizaciones es
producir ese conjunto de ocho incidencias desde el estado TPK enriquecido.

## 8. Premisas y fuerza probatoria

- La estructura del bosque y la enumeración de elevaciones son
  `EXACTO_INTERNO`.
- La pertenencia de las nueve palabras al atlas N69 es `EXACTO_INTERNO` como
  incidencia, no como selección.
- Los tres teoremas de imposibilidad son `EXACTO_INTERNO` para las familias
  que se definen y agotan expresamente.
- La unicidad por corona es `RELATIVO_A_PRIMITIVAS` del lector Witt vigente.
- La sección direccional queda localizada como requisito de la factorización
  local; el selector global la sustituye bajo su premisa de cobertura.
- La selección intrínseca del conjunto de ocho bloques no queda construida
  por N71--N74.

## 9. Procedencia

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: N69, las cargas visible y Witt--dual,
  la orientación de ida y vuelta, los pasos (90/120), el marco de Witt y la
  corona (H_e\cap P_\pi).
- `FORMALIZACION_NUEVA`: elección orbital del bosque canónico.
- `CERTIFICADO_NUEVO`: incidencia de los nueve residuos, barridos de los
  lectores uniformes y enumeración de las (64) elevaciones.
- `RESULTADO_NUEVO`: la corona excepcional, por sí sola, reduce (64\to1).

## 10. Falsadores

El resultado queda refutado en cualquiera de estos casos:

1. una de las nueve palabras deja de pertenecer al atlas N69--Witt;
2. un lector uniforme de una de las familias declaradas contiene las nueve;
3. las congruencias producen un número distinto de (64) elevaciones en
   ([0,999]^{12});
4. la condición (B(x)=H_e\cap P_\pi) deja más de una elevación;
5. el superviviente no coincide con (K) o su transformada de Hadamard no
   coincide con (U_{12}).

El verificador comprueba los cinco puntos.

## 11. Relación de sustitución

Este resultado conserva la obstrucción de periodicidad del registro
direccional de (108) pasos y la cobertura fase--carga de (W_{72}). Sustituye
únicamente la elección no canónica del bosque usada en
`TEOREMA_OBSTRUCCION_Y_DATO_MINIMO_W72.md` por la elección orbital anterior.
La interfaz lineal mínima sigue teniendo nueve aristas; cambia la carta para
respetar de forma directa la descomposición de (mathbb Z/12) bajo el paso
(+4).

## 12. Reproducción

```bash
python3 verificar_cociclos_n69_y_seccion_direccional.py --check-certificate
python3 -O verificar_cociclos_n69_y_seccion_direccional.py --check-certificate
```

El programa emplea sólo la biblioteca estándar, no usa `assert` y produce un
certificado idéntico en ambos modos.
