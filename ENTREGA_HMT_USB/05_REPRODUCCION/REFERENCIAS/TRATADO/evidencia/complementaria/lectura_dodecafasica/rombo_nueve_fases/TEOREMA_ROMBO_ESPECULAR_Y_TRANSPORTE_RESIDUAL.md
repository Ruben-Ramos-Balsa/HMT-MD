# El rombo especular y el transporte residual del sello dodecafásico

**Autores:** Oumar Haidara Fall; Rubén Ramos Balsa  
**Fecha:** 22 de julio de 2026  
**Revisión canónica utilizada:** `CURRENT.json`, 2026-07-22.2  
**Estatuto:** cierre finito exacto, formalización nueva de un lector orientado y delimitación demostrada de su prolongación

## 1. Resultado principal

La novena fase contiene un rombo combinatorio exacto

\[
5\longrightarrow2\longrightarrow1
\]

que conserva una transferencia unitaria entre las ramas de \(\pi\) y \(e\).
La rama especular saturada, elegida por propiedades internas y sin consultar el
sello dodecafásico, determina la palabra

\[
020022\mid222111.
\]

El retorno a la misma fase nueve pasos antes aporta el bloque

\[
211201.
\]

Por consiguiente se obtiene el cilindro ternario

\[
\mathcal W_{18}=020022\mid222111\mid211201.
\]

La conversión por extremos racionales prueba, sin redondeo, que este cilindro
fuerza exactamente las dos primeras tríadas decimales

\[
\boxed{234\mid543}.
\]

No se trata sólo de que dieciocho trits coincidan con el comienzo de una
expansión conocida. Todos los puntos del cilindro \(I(\mathcal W_{18})\)
pertenecen a la misma celda decimal de profundidad dos. El tercer bloque
ternario, \(211201\), transporta de manera efectiva el estado residual: cierra
la segunda tríada \(543\) y deja el resto necesario para continuar la lectura.

Este resultado converge con un cálculo independiente. Las raíces internas
\(103,523,450\), el selector regional \(169\) y los cocientes exactos del cambio
de carta \(38,195,168\) generan

\[
103+523-450-169=7,
\qquad
169+38+195-168=234.
\]

Así, el primer componente \(K_1=234\) se obtiene por dos recorridos que no lo
reciben como dato: el diamante de cambio de carta y el cilindro de la rama
especular.

## 2. Objetos y convenciones

Una configuración local se escribe como una terna ordenada

\[
B=(B_\pi,B_e,B_\varphi),\qquad B_\bullet\in\mathbb F_3^6.
\]

Las diferencias se calculan componente a componente en \(\mathbb F_3\). Si
\(W=w_1\cdots w_\ell\) es una palabra ternaria, se denota por \([W]_3\) su
valor entero y por

\[
I(W)=
\left[
\frac{[W]_3}{3^\ell},
\frac{[W]_3+1}{3^\ell}
\right)
\]

el cilindro que determina. Una tríada decimal de profundidad \(m\) está
forzada cuando \(I(W)\) queda contenido en una única celda de la partición
\(1000^{-m}\mathbb Z\).

El símbolo \(K_t\) de los calendarios de retención es un contador escalar de
profundidad. No es el sello dodecafásico

\[
K=(234,543,140,729,659,824,621,058,914,794,146,601).
\]

La distinción evita identificar indebidamente un retorno de fase con un
retorno del estado completo.

## 3. Teorema del rombo de supervivencia

### Teorema 1

En las tablas certificadas de las fases \(20,21,22\), las ramas seleccionadas
tienen cardinalidades \(5,2,1\). Cada una de las cinco ramas de la fase \(20\)
alcanza los dos vértices de la fase \(21\), y ambos vértices alcanzan el único
vértice de la fase \(22\).

### Demostración

Los dos vértices intermedios son

\[
\begin{aligned}
&201100\mid001211\mid101021,\\
&201211\mid001100\mid101021,
\end{aligned}
\]

y el vértice terminal es

\[
101110\mid101012\mid112120.
\]

La tabla de extensiones contiene diez incidencias en el primer paso: dos por
cada una de las cinco ramas. Contiene después dos incidencias, una desde cada
vértice intermedio hacia el mismo vértice terminal. El verificador recorre
todas las filas y exige esas incidencias, no sólo sus cardinalidades. \(\square\)

### Consecuencia

La salida visible no conserva la ascendencia. Cinco historias distintas se
vuelven indistinguibles después de dos pasos. Por ello, una lectura global no
puede vivir únicamente en la palabra visible: debe conservar orientación,
procedencia de rama y fase.

## 4. Selección interna de la rama especular saturada

La rama efectiva en la fase \(20\) es

\[
B=
(221022,020100,211021).
\]

Entre las cuatro ramas especulares existe una única rama que satisface
simultáneamente:

1. conserva la componente \(\varphi\);
2. conserva \(B_\pi+B_e\) en \(\mathbb F_3^6\);
3. concentra el defecto en la semipalabra terminal;
4. presenta los defectos saturados \(111\) y \(222\) en orientaciones opuestas.

Es

\[
B^\ast=(221100,020022,211021).
\]

Las diferencias son

\[
\delta_\pi=B_\pi^\ast-B_\pi=000111,
\qquad
\delta_e=B_e^\ast-B_e=000222.
\]

Al interpretar las dos primeras filas como enteros ternarios, se obtiene

\[
(683,171)\longmapsto(684,170),
\]

es decir, una transferencia exacta \((+1,-1)\) que conserva la suma.

### Definición 1. Lector de vacancia orientada

Para esta puerta se define

\[
\mathcal V(B^\ast,B)
=B_e^\ast\;\Vert\;(\delta_e)_{4:6}\;\Vert\;(\delta_\pi)_{4:6},
\]

donde \(\Vert\) denota concatenación y el orden \(e\to\pi\) conserva la
orientación de la transferencia. En la rama saturada,

\[
\boxed{\mathcal V(B^\ast,B)=020022\mid222111.}
\]

Esta definición tiene estatuto `FORMALIZACION_NUEVA`. La rama se selecciona
sin usar \(K\), \(\alpha\) ni datos metrológicos. La unicidad global del lector
para todas las fases no se presupone: es precisamente la propiedad que debe
establecer una prolongación completa.

## 5. Conversión exacta a tríadas decimales

### Lema 2

La palabra \(020022\) no fuerza una primera tríada decimal.

### Demostración

\[
I(020022)=\left[\frac{170}{729},\frac{171}{729}\right)
=\left[\frac{170}{729},\frac{19}{81}\right).
\]

Este intervalo atraviesa la frontera entre las celdas decimales \(233\) y
\(234\). Por tanto, la raíz visible sola no determina \(K_1\). \(\square\)

### Lema 3

La palabra de doce trits \(020022\mid222111\) fuerza exactamente la tríada
\(234\).

### Demostración

\[
I(020022222111)
=\left[\frac{124645}{531441},\frac{124646}{531441}\right)
\subset
\left[\frac{234}{1000},\frac{235}{1000}\right).
\]

El intervalo residual después de emitir \(234\) es

\[
R_{12}^{(1)}=
\left[
\frac{287806}{531441},
\frac{288806}{531441}
\right).
\]

Este resto todavía intersecta las celdas siguientes \(541,542,543\); por
tanto, doce trits fuerzan una sola tríada. \(\square\)

### Teorema 4. Transporte residual de la misma fase

El retorno de nueve fases desde \(t=11\) hasta \(t=20\) conserva la clase de
fase \(2\), aunque no conserva el estado. Su suma \(\pi+e\) en \(t=11\) es

\[
211201.
\]

Al añadir este bloque al lector orientado se obtiene

\[
I(020022222111211201)
=\left[
\frac{90866818}{387420489},
\frac{90866819}{387420489}
\right)
\subset
\left[
\frac{234543}{10^6},
\frac{234544}{10^6}
\right).
\]

Por tanto, los dieciocho trits fuerzan exactamente

\[
\boxed{K_1=234,\qquad K_2=543.}
\]

Después de \(K_1\), el intervalo residual queda contraído a

\[
R_{18}^{(1)}=
\left[
\frac{210423574}{387420489},
\frac{210424574}{387420489}
\right),
\]

que pertenece por completo a la celda \(543\). Después de emitir \(K_2\), el
nuevo estado residual es

\[
R_{18}^{(2)}=
\left[
\frac{54248473}{387420489},
\frac{55248473}{387420489}
\right).
\]

Este último intervalo intersecta exactamente las tres celdas \(140,141,142\).
Así, \(211201\) sí transporta el siguiente estado residual y emite \(K_2\),
pero no determina por sí solo \(K_3\). \(\square\)

## 6. Convergencia con el diamante independiente

El selector orbital-funcional produce las raíces

\[
(N_\pi,N_e,N_\varphi)=(103,523,450).
\]

La microfibra de \(\pi\) selecciona, por modo y estabilizador, la coordenada
singular \(\rho_\pi=169\). De ahí se genera

\[
A_1=N_\pi+N_e-N_\varphi-\rho_\pi=7.
\]

El transductor exacto \(729\to1000\) produce las primeras tríadas
\((141,718,618)\) y los cocientes de enlace

\[
(c_\pi,c_e,c_\varphi)=(38,195,168).
\]

La misma coordenada regional da

\[
K_1=\rho_\pi+c_\pi+c_e-c_\varphi=234.
\]

Ninguno de estos cálculos recibe \(A_1\) o \(K_1\) como entrada. El hecho de
que el cilindro especular fuerce también \(234\) constituye un control cruzado
entre dos construcciones distintas. No prueba todavía que el lector
\(\mathcal V\) sea el único lector global posible, pero elimina la interpretación
de \(234\) como una mera cifra copiada en esta primera fase.

## 7. Relación con el catálogo de 243 palabras

En el índice completo

\[
104976\longrightarrow468\ U6\longrightarrow243\ w6,
\]

la palabra \(020022\) posee una única preimagen \(U6\):

\[
(252,109,252,903,850,850),
\]

con multiplicidad \(144\). Esto enlaza la raíz visible del rombo con el
catálogo finito.

Sin embargo, la prolongación congelada del certificado antiguo es

\[
020022020001000222102000121210,
\]

y diverge del sello ya en el séptimo trit. Por tanto, la preimagen única de
\(020022\) no basta para seleccionar la prolongación dodecafásica. La memoria
especular y el retorno de fase aportan información adicional que el cociente
\(w6\) ha olvidado.

## 8. Control negativo en las retenciones posteriores

El calendario presenta las primeras retenciones en

\[
20,42,64,86,108,
\]

separadas por \(22\). Al reconstruir las familias locales condicionadas de
cilindros, los números de soluciones compatibles son

\[
5,3,3,1,3.
\]

El defecto saturado \((000111,000222)\) aparece una vez en la primera
retención y ninguna vez en las cuatro siguientes:

\[
1,0,0,0,0.
\]

En consecuencia, no es correcto reiterar mecánicamente el patrón de \(t=20\)
cada nueve fases o cada veintidós pasos. La prolongación requiere el estado
enriquecido, no sólo el número de fase y la condición de retención. Este
control es `RELATIVO_A_PRIMITIVAS`, porque las familias de cilindros usadas en
la ablación proceden de los tres canales ya fijados.

## 9. Teorema de insuficiencia de las dos tablas cardinales de 108 pasos

Se examinaron las dos realizaciones históricas de las rutas norte, este, sur y
oeste. Ambas contienen \(432=4\times108\) filas, pero difieren en \(391\) de
sus \(432\) cifras locales.

El conteo de las cifras \(1,3,5,7\), agrupado en doce ventanas de nueve pasos,
da respectivamente

\[
(1,7,9,0,7,0,1,7,9,0,7,0)
\]

y

\[
(9,6,7,6,9,6,7,6,9,6,7,6).
\]

Ninguno coincide siquiera con las centenas del sello

\[
(2,5,1,7,6,8,6,0,9,7,1,6).
\]

Además, el pseudocódigo histórico de cuatro cursores, ejecutado literalmente,
produce

\[
(222,222,222,333,333,333)^2.
\]

Ninguno de los cien pares de pesos decimales ni las tres cartas aditivas
ensayadas produce \(K\). Esto demuestra que aquellas dos tablas no pueden
identificarse con el registro enriquecido que genera el estado dodecafásico.
No refuta la arquitectura TPK completa; localiza la pérdida de información en
las proyecciones históricas.

## 10. Dato mínimo necesario para la prolongación

La siguiente fase del cierre no necesita otra constante objetivo. Necesita un
registro ejecutable que conserve, para cada traza:

1. el estado inicial y la dinámica elegida;
2. el identificador, los extremos y la continuación de la traza;
3. la clase longitudinal y su residuo;
4. el signo inducido por la orientación TRIT;
5. el predicado de corona o interior;
6. la fase y la memoria de rama;
7. la regla exacta de agregación hacia \(U_{12}\) o \(K\).

Ésta es una frontera de identificabilidad demostrada. No autoriza a sustituir
el registro por el sello final ni a declarar que las tablas cardinales ya lo
contienen.

## 11. Estatuto de procedencia y fuerza probatoria

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: las puertas especulares, el retorno de
  nueve fases, el estado dodecafásico y el cambio de carta.
- `RESULTADO_RECUPERADO`: la preimagen única de \(020022\) en el catálogo de
  243 palabras.
- `FORMALIZACION_NUEVA`: el lector de vacancia orientada \(\mathcal V\).
- `CERTIFICADO_NUEVO`: el rombo \(5\to2\to1\), las dos tríadas forzadas, el
  transporte residual y el teorema de insuficiencia de las tablas publicadas.

Son `EXACTO_INTERNO` el rombo, la transferencia unitaria, los defectos, la
conversión intervalar y las dos tríadas forzadas. Es
`RECONOCIMIENTO_EXTERNO_TIPADO` su igualdad con el comienzo ternario del sello
ya certificado. La canonicidad global de \(\mathcal V\) y su prolongación a
las doce fases permanecen como la tarea matemática delimitada por este
resultado.

## 12. Reproducción

Desde la raíz del proyecto:

```bash
python3 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/rombo_nueve_fases/verificar_rombo_nueve_fases.py --check-certificate
python3 -O 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/rombo_nueve_fases/verificar_rombo_nueve_fases.py --check-certificate
```

Ambas ejecuciones deben finalizar sin error y producir exactamente el
contenido de `CERTIFICADO_ROMBO_NUEVE_FASES.json`.
