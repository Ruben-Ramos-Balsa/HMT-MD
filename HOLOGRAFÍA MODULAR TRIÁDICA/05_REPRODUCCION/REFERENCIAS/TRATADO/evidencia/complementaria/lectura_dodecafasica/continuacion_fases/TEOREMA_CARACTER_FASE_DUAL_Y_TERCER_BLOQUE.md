# Carácter fase--dual y determinación del tercer componente del sello

**Autores:** Oumar Haidara Fall; Rubén Ramos Balsa  
**Fecha:** 22 de julio de 2026  
**Autoridad semántica utilizada:** `CURRENT.json`, revisión 2026-07-22.2  
**Estatuto:** formalización nueva y certificado nuevo sobre arquitectura autoral preexistente; teorema finito exacto relativo a las cartas N69--N74

## 1. Enunciado principal

El rombo de supervivencia de la novena fase y su retorno previamente
certificado producen la palabra de dieciocho trits

\[
W_{18}=020022\mid222111\mid211201.
\]

La fase inmediatamente anterior al origen de ese retorno es \(t=10\). Su
terna superviviente, ordenada por los canales \((\pi,e,\varphi)\), es

\[
B_{10}=(022212,110001,100021).
\]

Esta terna posee carga dual de Witt

\[
\rho_W(B_{10})=(0,1,2)
\]

y fase ternaria \(p_{10}=10\bmod 3=1\). El carácter que conserva el canal cuya
carga coincide con la fase e invierte los otros dos es

\[
\varepsilon_i(p,\rho)=
\begin{cases}
+1,&\rho_i=p,\\
-1,&\rho_i\ne p.
\end{cases}
\]

En coordenadas de \(\mathbb F_3\), \(-1=2\), por lo que

\[
\varepsilon(1,(0,1,2))=(2,1,2).
\]

Su evaluación sobre \(B_{10}\) da

\[
\boxed{
-B_{10,\pi}+B_{10,e}-B_{10,\varphi}=021101.
}
\]

La concatenación resultante es

\[
\boxed{
W_{24}=020022\mid222111\mid211201\mid021101.
}
\]

El cilindro ternario definido por esta palabra queda contenido por completo en
una única celda decimal de profundidad tres:

\[
I(W_{24})
=
\left[
\frac{66241910521}{282429536481},
\frac{66241910522}{282429536481}
\right)
\subset
\left[
\frac{234543140}{10^9},
\frac{234543141}{10^9}
\right).
\]

Por tanto, sin redondeo y antes de comparar con el sello vigente, el lector
fuerza exactamente

\[
\boxed{234\mid543\mid140.}
\]

La comparación posterior reconoce estos tres enteros como
\((K_1,K_2,K_3)\). En particular,

\[
\boxed{K_3=140.}
\]

## 2. Procedencia de los primeros dieciocho trits

El bloque inicial no se reconstruye a partir de \(K\). En la fase \(t=20\),
la rama efectiva es

\[
B=(221022,020100,211021).
\]

La única rama especular que conserva \(\varphi\), conserva la suma
\(\pi+e\) y concentra el defecto saturado en la semipalabra terminal es

\[
B^*=(221100,020022,211021).
\]

Sus defectos orientados son

\[
\delta_\pi=000111,
\qquad
\delta_e=000222.
\]

El lector de vacancia orientada ya certificado concatena la hoja visible de
\(e\) y los defectos terminales en el orden \(e\to\pi\):

\[
020022\mid222\mid111=020022\mid222111.
\]

El retorno \(t=11\to20\) conserva la clase de fase, pero no el estado. En su
origen, la suma \(\pi+e\) es \(211201\). Esto produce \(W_{18}\). El siguiente
dato cronológico no es una fase elegida entre muchas: es el predecesor
inmediato \(t=10\) de \(t=11\).

Así, la secuencia de procedencia es

\[
t=20\ \text{(rombo saturado)}
\longleftarrow
t=11\ \text{(retorno de la misma clase de fase)}
\longleftarrow
t=10\ \text{(predecesor inmediato)}.
\]

Esta lectura es retrospectiva en el calendario de fases y progresiva en el
cilindro ternario. No confunde retorno de fase con retorno de estado.

## 3. Selección coinductiva de la terna en \(t=10\)

En \(t=10\) hay once ramas locales. La tabla N72 marca una sola rama efectiva:

\[
022212\mid110001\mid100021.
\]

Las once ramas sobreviven el primer horizonte, pero sólo una sobrevive el
segundo. La rama efectiva queda, por tanto, determinada antes de evaluar el
carácter fase--dual. No se escoge una rama porque produzca \(021101\): se usa
la rama que ya había seleccionado el protocolo de supervivencia.

Este orden lógico es esencial:

\[
\text{ramas locales}
\xrightarrow{\mathrm{EF\!-!G9}}
B_{10}
\xrightarrow{\varepsilon_{p_{10},\rho_W}}
021101.
\]

La palabra objetivo no interviene en ninguna de las dos flechas.

## 4. Definición y naturalidad del carácter fase--dual

Sea

\[
B=(b_0,b_1,b_2)\in(\mathbb F_3^6)^3
\]

una terna de frontera. Para la matriz de Witt \(A_W\), se define la carga dual
de cada canal por

\[
\rho_i(B)=\sum_{j=1}^{6}(b_iA_W)_j\pmod3.
\]

Sea \(p\in\mathbb F_3\) la fase ternaria. Definimos el carácter fase--dual

\[
\chi_{p,B}
=\sum_{i=0}^{2}\varepsilon_i(p,\rho(B))b_i,
\qquad
\varepsilon_i(p,\rho)=
\begin{cases}
1,&\rho_i=p,\\
-1,&\rho_i\ne p.
\end{cases}
\]

La definición depende sólo de la coincidencia entre fase y carga, no del
nombre \((\pi,e,\varphi)\) de un canal. Satisface dos propiedades exactas.

### Lema 1. Covariancia por permutación

Si se permutan simultáneamente los canales y sus cargas, la palabra
\(\chi_{p,B}\) no cambia.

### Demostración

La permutación sólo reordena los sumandos de la definición. El predicado
\(\rho_i=p\) se transporta junto con el canal, por lo que cada coeficiente
permanece unido a su sumando. El certificado verifica las seis permutaciones.
\(\square\)

### Lema 2. Invariancia por renombrado afín de las fases

Para \(a\in\mathbb F_3^\times\) y \(b\in\mathbb F_3\), la transformación

\[
(\rho,p)\longmapsto(a\rho+b,ap+b)
\]

conserva todos los coeficientes \(\varepsilon_i\).

### Demostración

Como \(a\ne0\), se tiene

\[
a\rho_i+b=ap+b\quad\Longleftrightarrow\quad\rho_i=p.
\]

El certificado recorre los seis renombrados afines. \(\square\)

### Corolario 3. Unicidad relativa

Entre los caracteres de dos niveles que:

1. dependen únicamente de la igualdad fase--carga;
2. conservan con signo positivo la componente coincidente;
3. invierten con signo negativo el complemento;

el carácter \(\chi_{p,B}\) es único.

Éste es el sentido exacto de la canonicidad demostrada. No se afirma que los
datos desnudos N69--N74 obliguen a introducir cualquier lector imaginable. Se
afirma que, una vez fijados los tres requisitos internos anteriores, no queda
una elección de canal, signo o etiqueta. La adopción de estos requisitos como
lector global tiene estatuto `FORMALIZACION_NUEVA`.

## 5. Unicidad algebraica en la fase \(t=10\)

Las tres primeras columnas de \(B_{10}\) forman la matriz

\[
M=
\begin{pmatrix}
0&2&2\\
1&1&0\\
1&0&0
\end{pmatrix},
\qquad
\det M=1\pmod3.
\]

Por tanto, las tres filas de \(B_{10}\) son linealmente independientes en
\(\mathbb F_3^6\). El mapa

\[
\mathbb F_3^3\longrightarrow\mathbb F_3^6,
\qquad
(c_\pi,c_e,c_\varphi)\longmapsto
c_\pi B_\pi+c_eB_e+c_\varphi B_\varphi
\]

es inyectivo. En consecuencia, \(021101\) posee un único vector de
coeficientes:

\[
(c_\pi,c_e,c_\varphi)=(2,1,2).
\]

La unicidad no se deduce de haber comparado varias fórmulas aproximadas: es un
teorema de rango sobre \(\mathbb F_3\).

## 6. Relación con la transformación de Hadamard

Se completa la terna con una vacancia nula y se aplica el bloque \(H_4\). Las
cuatro filas producen

\[
\begin{array}{c|c|c}
\text{coeficientes sobre }(\pi,e,\varphi)&\text{palabra}&\text{lectura}\\
\hline
(1,1,1)&202201&q\\
(1,1,2)&002222&a\\
(1,2,1)&012202&\text{carácter impar en }e\\
(1,2,2)&112220&\text{cuarta componente}
\end{array}
\]

El carácter fase--dual crudo es la orientación opuesta de la fila impar en
\(e\):

\[
021101=-012202.
\]

Esto explica por qué el bloque aparece simultáneamente en la lectura de fase y
en la descomposición de Hadamard. Hadamard, por sí solo, no selecciona una de
sus cuatro filas; la fase \(p=1\), la carga \(\rho_W=(0,1,2)\) y la orientación
del TRIT realizan esa selección.

Los observables de frontera publicados \((q,a,c,\operatorname{colw},\rho_W,r)\)
se reproducen exactamente desde \(B_{10}\). Ninguno de \(q,a,c\), sus
transformadas por \(A_W\), las cargas de fila o los pesos de columna es
\(021101\). Esto localiza el nuevo dato: no era una de las columnas ya
impresas, sino el carácter de reflexión seleccionado por fase.

## 7. Puente crudo--visible con el catálogo N33

La proyección vigente del catálogo es

\[
\Psi(U_6)=-U_6\pmod3.
\]

Por ello, la palabra cruda \(021101\) se observa en el catálogo como

\[
\Psi(021101)=012202.
\]

El índice exhaustivo N33 demuestra que \(012202\) posee una única preimagen
\(U_6\):

\[
U_6=(963,890,850,292,129,292),
\]

con multiplicidad \(144\). Su reducción directa es

\[
U_6\bmod3=021101.
\]

Así quedan enlazadas tres presentaciones del mismo objeto:

\[
\boxed{
\text{carácter fase--dual crudo }021101
\xleftrightarrow{\;\Psi=-1\;}
\text{palabra visible }012202
\xleftrightarrow{\;N33\;}
U_6.
}
\]

La fuente histórica `F004_3.0.alfa.txt` ya registraba esta preimagen en la
clase `B4-o2`, con firma de energía \(717717\). Por ello, la palabra y su
región son `RESULTADO_RECUPERADO`; lo nuevo aquí es la formalización del mapa
de fase que las alcanza desde N72 y su certificado.

## 8. Demostración intervalar de \(K_3=140\)

Para una palabra ternaria \(W\) de longitud \(\ell\), sea

\[
I(W)=
\left[
\frac{[W]_3}{3^\ell},
\frac{[W]_3+1}{3^\ell}
\right).
\]

En el presente caso,

\[
[W_{24}]_3=66241910521,
\qquad
3^{24}=282429536481.
\]

La contención

\[
I(W_{24})\subset
\left[
\frac{234543140}{10^9},
\frac{234543141}{10^9}
\right)
\]

se verifica mediante multiplicaciones enteras cruzadas. Por tanto todos los
reales compatibles con \(W_{24}\), y no sólo su extremo inferior, comparten
las tres primeras tríadas decimales. Esto descarta que \(140\) sea un efecto
de redondeo o la selección de un único representante del cilindro.

Después de emitir \(234\mid543\mid140\), el intervalo residual es

\[
\left[
\frac{206001709660}{282429536481},
\frac{207001709660}{282429536481}
\right).
\]

El siguiente componente decimal queda localizado en

\[
K_4\in\{729,730,731,732\}.
\]

El sello vigente toma \(K_4=729\), pero los veinticuatro trits todavía no lo
fuerzan. Esta frontera se conserva explícitamente: haber cerrado \(K_3\) no se
convierte en una afirmación falsa sobre \(K_4\).

## 9. Por qué \(D_3\) y \(D_4\) no intervienen en la selección

Las diferencias dodecafásicas se definen, una vez conocido \(K\), por

\[
(D_sK)_m=K_m-K_{m+s},\qquad s\in\{3,4\}.
\]

El componente \(K_3\) participa en las posiciones \((3,12)\) de \(D_3K\) y en
las posiciones \((3,11)\) de \(D_4K\). Por ello, utilizar los valores publicados
de esas diferencias para elegir \(021101\) introduciría el propio componente
que se intenta construir. En este certificado, \(D_3\) y \(D_4\) se calculan
sólo después del reconocimiento, como control de tipos. La construcción de
\(021101\) usa exclusivamente fase, carga dual, orientación y supervivencia.

## 10. Ablaciones y límite de la regla congelada

La prueba no se limita al caso positivo.

### 10.1 Cambio de fase

En \(B_{10}\), desplazar la fase produce

\[
\begin{array}{c|c}
p&\chi_{p,B_{10}}\\
\hline
1&021101\\
2&001111\\
0&112220
\end{array}
\]

Sólo la fase real produce el cuarto bloque ternario del sello.

### 10.2 Cambio de orientación

Invertir la orientación produce \(012202\), la palabra visible del catálogo,
pero no el bloque crudo que prolonga el cilindro. Esto verifica que la
distinción crudo--visible no es decorativa.

### 10.3 Sustitución por el observable \(a\)

El carácter publicado

\[
a=\pi+e-\varphi
\]

produce \(002222\), no \(021101\). La prolongación no se obtiene confundiendo
dos observables distintos.

### 10.4 Sustitución del predecesor por el sucesor

Aplicar la misma regla a \(t=11\), en vez de al predecesor \(t=10\), produce
\(122012\). La cronología del retorno es parte de la construcción.

### 10.5 Todas las ramas N72

Al aplicar la regla congelada a todas las ramas publicadas entre \(t=5\) y
\(t=25\), aparecen tres coincidencias con bloques ternarios de \(K\):

1. \(021101\) en la rama efectiva de \(t=10\);
2. \(221110\) en una rama rechazada de \(t=16\);
3. \(021101\) en una rama rechazada de \(t=20\).

La supervivencia elimina las dos coincidencias espurias. Sobre las ramas
efectivas, la única coincidencia es la de \(t=10\).

### 10.6 Todos los caracteres lineales

Un carácter lineal fijo, independiente de la fase, alcanza como máximo un
bloque distinto del sello en toda la ventana de ramas efectivas. Además, el
décimo bloque ternario \(001001\) no aparece en ninguna rama N72 bajo ninguno
de los veintiséis caracteres lineales no nulos.

En la tabla N69 de cien estados, una búsqueda libre por los veintiséis
caracteres encuentra los doce bloques, cada uno varias veces. Esto demuestra
que la mera existencia de una coincidencia no constituye una selección. La
regla fase--dual congelada reduce esa abundancia a dos incidencias: \(021101\)
en la fila N69 \(t=11\), correspondiente a N72 \(t=10\), y \(020111\) en
N69 \(t=81\). Los datos actuales no proporcionan una ley cronológica que
convierta la segunda incidencia en la continuación del sello.

## 11. Alcance exacto

Queda probado:

1. la procedencia interna de \(021101\) desde la terna superviviente de
   \(t=10\), mediante un carácter natural que no consulta \(K\), \(\alpha\),
   CODATA ni otra constante física;
2. la unicidad del vector de coeficientes \((2,1,2)\) sobre esa terna;
3. la covariancia del carácter bajo permutación de canales y renombrado afín
   de fases;
4. su identificación como orientación opuesta de la fila impar en \(e\) del
   bloque de Hadamard;
5. el puente exacto entre la palabra cruda, la palabra visible y una única
   preimagen \(U_6\) de N33;
6. la contención intervalar que fuerza \(K_1=234\), \(K_2=543\) y
   \(K_3=140\).

No queda probado por esta única regla:

1. que el carácter fase--dual emita los ocho bloques ternarios restantes;
2. que la incidencia N69 \(t=81\) sea el siguiente paso de una recurrencia
   dodecafásica;
3. que APP mínima, sin las cartas enriquecidas de fase, carga y supervivencia,
   determine ya todo \(K\).

La conclusión no es una objeción añadida después del resultado. Es la frontera
exacta establecida por las ablaciones: el tercer componente decimal sí queda
cerrado; la prolongación total requiere un operador adicional de ordenación de
las incidencias posteriores.

## 12. Procedencia documental

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: rombo N72, retorno N74, firma de
  frontera N69, carga \(\rho_W\), orientación TRIT y catálogo N33.
- `RESULTADO_RECUPERADO`: palabra cruda \(021101\), palabra visible \(012202\),
  preimagen \(U_6\), multiplicidad \(144\) y clasificación histórica
  `B4-o2`.
- `FORMALIZACION_NUEVA`: carácter fase--dual definido por coincidencia entre
  fase y carga.
- `CERTIFICADO_NUEVO`: unicidad por rango, naturalidad, contención del cilindro
  de 24 trits y barridos adversariales.

## 13. Reproducción

Desde la raíz del proyecto:

```bash
python3 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_caracter_fase_dual.py --check-certificate
python3 -O 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_caracter_fase_dual.py --check-certificate
```

Ambas ejecuciones producen una salida byte a byte idéntica. El verificador no
usa sentencias de aserción desactivables y el resultado congela las huellas
SHA-256 de todas sus fuentes.
