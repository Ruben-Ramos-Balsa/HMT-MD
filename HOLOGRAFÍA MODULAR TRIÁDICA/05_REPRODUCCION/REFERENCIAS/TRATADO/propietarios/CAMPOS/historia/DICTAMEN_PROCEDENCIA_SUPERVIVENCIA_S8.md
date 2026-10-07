# Supervivencia nonádica y procedencia de los ocho bloques dodecafásicos

## 1. Dos operaciones matemáticamente distintas

La dinámica de nueve fases contiene un resultado positivo preciso. En cada
puerta publicada, la componente de autoescala permanece fija y también
permanece fija la suma de las componentes de cierre y propagación. La
ambigüedad local reside únicamente en la distribución entre estas dos últimas
componentes. La supervivencia hacia fronteras posteriores rompe esa simetría y
selecciona una sola orientación en las ventanas certificadas.

Este mecanismo prueba que el estado profundo conserva más información que la
salida visible. No prueba, por sí solo, que el contenido completo del registro
haya sido producido sin una condición anterior. Deben separarse los mapas

\[
\{ \text{ramas locales de una frontera fijada}\}
\longrightarrow
\{ \text{rama superviviente}\}
\]

y

\[
\text{estado APP--TRIT--TPK}
\longrightarrow
\text{sucesión completa de fronteras}.
\]

El primero está certificado en las ventanas publicadas. El segundo es la ley
de prolongación global que debe construir el contenido antes de reconocerlo.

## 2. Lo que declara el propio registro

El archivo rector de la rama de veinte bloques afirma expresamente que los
nombres \(\pi,e,\varphi\) son etiquetas obtenidas por comparación y que el
paquete no demuestra un selector autónomo. Su resumen declara como base
`sample_output_12triads` junto con el certificado de persistencia. N69, por su
parte, registra que la generación infinita completa no se declara probada y
localiza el mapa pendiente en

\[
F_{\mathrm{HMT}}(B_t,C_t)\longmapsto\operatorname{Sig}_{t+1},
\]

donde \(B_t\) es la frontera enriquecida y \(C_t\) conserva el cilindro, la
hoja, el acarreo y la orientación.

Estas declaraciones no invalidan la supervivencia. Fijan su dominio lógico:
la supervivencia selecciona una rama dentro del registro suministrado; no
construye retrospectivamente ese registro.

## 3. Contraste exhaustivo con el sufijo de ocho bloques

Sea

\[
\mathcal S_8=
\{002001,020111,200110,121012,
010122,001001,221110,222110\}.
\]

La rama publicada de veinte pasos contiene exactamente dos elementos de este
conjunto:

\[
\mathcal S_8\cap\mathcal B_{20}
=\{010122,020111\}.
\]

Sus incidencias son inequívocas:

\[
010122=B_{9,\varphi},
\qquad
020111=B_{19,\pi}.
\]

La tabla focal de persistencia \(t=5,\ldots,13\) sólo contiene el primero. La
imagen completa de la ventana N72, incluso después de añadir sus lectores
comparativos y la extensión afín, contiene cuatro:

\[
\{010122,020111,221110,222110\}.
\]

Faltan en toda esa imagen

\[
\boxed{\{001001,002001,121012,200110\}}.
\]

Por tanto, ninguna restricción de tiempos, fases, profundidades o ramas de la
ventana publicada puede seleccionar \(\mathcal S_8\): cuatro de sus elementos
no pertenecen al codominio disponible.

El lector N69 completo sí contiene las ocho palabras. Éste es un teorema de
cobertura, no aún un teorema de selección: la pertenencia deja 442 palabras
posibles y no determina qué ocho incidencias, con qué posiciones y con qué
orientación, constituyen la dodecafase.

## 4. Consecuencia para el cierre del sello

La monodromía nonádica es una parte necesaria del cierre porque aporta la
memoria que distingue orientaciones con la misma salida local. No puede
sustituir al selector de contenido mientras se limite a cilindros ya fijados
por las sucesiones reconocidas como \(\pi,e,\varphi\).

La pieza matemática que conecta ambos resultados debe ser una sección de
incidencias indexadas

\[
\Sigma:\mathcal X_{\mathrm{TPK}}^{\mathrm{enr}}
\longrightarrow\mathcal I_{69},
\]

capaz de prolongar el estado conservando frontera, fase, acarreo, hoja y
orientación. Debe seleccionar el contenido y su posición antes de consultar
el sello decimal, el campo firmado o la palabra de \(\alpha\).

El selector orbital ya certificado resuelve la etapa posterior: una vez dado
el repertorio no ordenado de ocho palabras, la órbita
\(4\to8\to12\), la cara excepcional y la procedencia temporal N69 aíslan el
único estado canónico. El resultado presente determina exactamente qué parte
anterior no puede atribuirse a la ventana finita de supervivencia.

## 5. Procedencia y fuerza

- La arquitectura de nueve fases es `ARQUITECTURA_AUTORAL_PREEXISTENTE`.
- Las tablas de supervivencia son `RESULTADO_RECUPERADO`.
- La separación entre selector de rama y selector de contenido es
  `FORMALIZACION_NUEVA`.
- La auditoría de procedencia y cobertura es `CERTIFICADO_NUEVO`.
- Fuerza: `EXACTO_INTERNO_SOBRE_REGISTROS_PUBLICADOS`.

El resultado se reproduce en ejecución ordinaria y optimizada mediante
`verificar_procedencia_supervivencia_s8.py`.
