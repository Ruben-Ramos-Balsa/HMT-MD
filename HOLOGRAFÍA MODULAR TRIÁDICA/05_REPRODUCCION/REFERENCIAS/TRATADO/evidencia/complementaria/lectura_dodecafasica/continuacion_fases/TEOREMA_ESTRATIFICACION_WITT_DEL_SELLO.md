# Estratificación del sello por la rotación interna de Witt

**Autores:** Oumar Haidara Fall; Rubén Ramos Balsa  
**Fecha:** 22 de julio de 2026  
**Autoridad semántica:** `CURRENT.json`, revisión 2026-07-22.2  
**Estatuto:** reconocimiento estructural posterior y certificado nuevo; no se
presenta como generador del sello

## 1. Pregunta

Los primeros setenta y dos trits de la fracción decimal formada por el sello
dodecafásico se dividen en doce bloques:

\[
\begin{aligned}
&020022\mid222111\mid211201\mid021101\mid002001\mid020111\mid\\
&200110\mid121012\mid010122\mid001001\mid221110\mid222110.
\end{aligned}
\]

Bajo la orientación visible \(\Psi(w)=-w\), siete bloques pertenecen al
catálogo N33 de \(243\) palabras. La mera igualdad cardinal \(7+5=12\) no
explica la selección. La pregunta correcta es si el operador de Witt ya
fijado organiza los doce bloques palabra por palabra.

## 2. Rotación de Witt

Sea \(J=A_W\) la matriz de Paley--Witt utilizada en el corpus. Sobre
\(\mathbb F_3^6\) verifica

\[
J^2=-I,
\qquad
J^4=I.
\]

Sea \(\mathcal C\subset\mathbb F_3^6\) el catálogo visible de \(243\)
palabras. Para cada palabra \(w\), definimos su profundidad de entrada

\[
d_W(w)=\min\{k\in\{0,1,2,3\}:J^kw\in\mathcal C\},
\]

cuando existe. La definición no usa una constante física ni una comparación
decimal: utiliza un operador y un catálogo ya fijados. Aplicada al sello, sí
es un análisis posterior, porque los bloques se suministran como entrada.

## 3. Teorema de estratificación (5+2+5)

### Teorema

Las profundidades mínimas de los doce bloques son

\[
\boxed{(0,1,0,2,0,2,2,0,2,1,2,0).}
\]

Por posiciones,

\[
\begin{aligned}
d_W^{-1}(0)&=\{1,3,5,8,12\},\\
d_W^{-1}(1)&=\{2,10\},\\
d_W^{-1}(2)&=\{4,6,7,9,11\},\\
d_W^{-1}(3)&=\varnothing.
\end{aligned}
\]

Por tanto,

\[
\boxed{12=5+2+5}
\]

no como coincidencia cardinal, sino como primera entrada de cada palabra en
una filtración concreta:

\[
\mathcal C
\subset
\mathcal C\cup J^{-1}\mathcal C
\subset
\mathcal C\cup J^{-1}\mathcal C\cup J^{-2}\mathcal C.
\]

### Demostración

El certificado calcula las cuatro palabras

\[
w,Jw,J^2w,J^3w
\]

para cada bloque y consulta literalmente su pertenencia al índice N33. Además
recorre las \(729\) palabras del ambiente. Los tamaños de los estratos de
primera entrada son

\[
243,\quad163,\quad130,\quad88,\quad105,
\]

donde \(105\) corresponde a palabras que no entran en las cuatro posiciones
de la órbita. Los doce bloques del sello pertenecen a los tres primeros
estratos y ninguno requiere \(J^3\). \(\square\)

## 4. Relación exacta con el soporte (7+5)

Como (J^2=-I), la condición visible (-w\in\mathcal C) equivale a
(J^2w\in\mathcal C). Se obtiene

\[
\{m:J^2w_m\in\mathcal C\}
=\{1,4,5,6,7,9,11\}.
\]

Su complemento es

\[
\{2,3,8,10,12\}.
\]

Este soporte \(7+5\) es exacto, pero no constituye por sí solo una
descomposición en hojas disjuntas. Las posiciones

\[
\{1,3,4,5,6,8\}
\]

entran en el catálogo bajo más de un exponente de \(J\). En particular, una
palabra puede pertenecer simultáneamente a la hoja directa y a la hoja
reflejada. La cardinalidad \(7+5\) no selecciona de manera única una fase de
Witt.

La profundidad mínima elimina la superposición mediante una regla explícita
y produce la descomposición disjunta \(5+2+5\). Sin embargo, adoptar
"primera entrada" como dinámica generativa exige todavía demostrar que el
estado TPK completo impone ese orden; aquí se formaliza y certifica la
estratificación, no se presupone esa selección.

## 5. Cotejo con el libro direccional

La secuencia de profundidades no tiene período seis. De hecho, las seis
parejas antipodales \((m,m+6)\) poseen profundidades distintas. El libro
N/E/S/O de \(108\) pasos, en cambio, repite todos sus campos tras \(54\)
pasos, es decir, tras seis ventanas nonádicas.

Por tanto, ningún lector local y equivariante que reciba sólo ese libro puede
seleccionar la secuencia \((0,1,0,2,0,2,2,0,2,1,2,0)\). La estratificación
confirma de nuevo que la separación dodecafásica requiere memoria de rama,
supervivencia u orientación enriquecida que la proyección direccional no
conserva.

## 6. Alcance

Queda demostrado:

1. el soporte visible \(7+5\), palabra por palabra;
2. su no disjunción como sistema de hojas de Witt;
3. la estratificación mínima y disjunta \(5+2+5\);
4. la ausencia de bloques en profundidad tres o fuera de la órbita saturada;
5. la incompatibilidad de esta secuencia con cualquier lector local del
   libro direccional periódico.

No se deduce de este teorema:

1. el siguiente bloque del sello a partir del anterior;
2. el orden dodecafásico sin suministrar los doce bloques;
3. una ley de prolongación global desde APP mínima.

La diferencia es de tipo lógico: el calibre de Witt reconoce y estratifica
todo el sello; no lo emite todavía.

## 7. Procedencia

- `ARQUITECTURA_AUTORAL_PREEXISTENTE`: \(A_W\), la orientación
  \(\Psi=-I\) y el catálogo N33.
- `FORMALIZACION_NUEVA`: profundidad mínima de entrada en el catálogo bajo
  la rotación \(J\).
- `CERTIFICADO_NUEVO`: estratos globales
  \(243/163/130/88/105\), soporte \(7+5\), superposiciones y perfil
  \(5+2+5\) del sello.
- `RECONOCIMIENTO_ESTRUCTURAL_POSTERIOR`: los bloques del sello son la entrada
  del análisis, no su salida.

## 8. Reproducción

```bash
python3 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_estratificacion_witt_sello.py --check-certificate
python3 -O 16_CIERRE_GLOBAL_HMT_MD_2026-07-22/02_LECTURA_DODECAFASICA/continuacion_fases/verificar_estratificacion_witt_sello.py --check-certificate
```
