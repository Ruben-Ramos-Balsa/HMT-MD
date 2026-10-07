# El defecto −1/12, la recuperación dodecafásica y el balance de memoria

## Procedencia y alcance

La interpretación interior–borde es una aportación conceptual previa de Rubén. Esta nota recupera los operadores ya escritos en el corpus y desarrolla su control cuantitativo. No modifica un PDF, no rederiva las constantes mediante objetivos externos y no certifica la regularidad hidrodinámica ni un valor de tensión superficial.

El punto de corte es la publicación de un registro dodecafásico del estado APP–TRIT–TPK. El registro de doce coordenadas no sustituye al estado completo con ruta, orientación y memoria. Las construcciones conjuntas del continuo conservan su lugar anterior a las aplicaciones terminales.

Fuentes leídas:

1. [Realizaciones de −1/12, cuerpo del capítulo 33](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/base_83/c27_body.tex>), secciones «Defecto de los proyectores de diferencia cíclica» y «Realización angular».
2. [Registro y extractor transversal U016](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex>), ecuaciones y prueba de completitud del extractor (líneas 520–595).
3. [Fuente hidrodinámica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/incorporaciones/parte_v_resoluciones_extensas_20260819/editor_ready/03_navier_stokes.tex>), estado enriquecido, carry entre niveles y memorias positiva/firmada (líneas 54–109).
4. El verificador adjunto reutiliza, en solo lectura, las operaciones racionales del certificado de proyectores conservado en la base sellada. Fija una orientación para el desplazamiento cíclico; invertirla sustituye cada diferencia por su versión conjugada y conserva los proyectores, B y las cotas. No identifica los dos registros orientados.

La recuperación del registro ya estaba demostrada en U016. La descomposición completa del defecto, las cotas óptimas y la identidad de energía bajo actualización se reúnen aquí como desarrollo local; su prioridad global dentro de todo el corpus no se ha auditado.

## 1. El racional es una publicación de un operador

Sea \(S\) el desplazamiento cíclico de doce coordenadas. Definimos

\[
D_3=I-S^3,\quad D_4=I-S^4,\qquad
P_3=\frac14\sum_{j=0}^3S^{3j},\quad
P_4=\frac13\sum_{j=0}^2S^{4j}.
\]

Estos proyectores ortogonales tienen rangos tres y cuatro. Su producto es el proyector \(P_0\) sobre las constantes: los pasos tres y cuatro generan el ciclo completo. El defecto firmado es

\[
E=P_3-P_4,\qquad \tau(E)=\frac{\operatorname{Tr}E}{12}=-\frac1{12}.
\]

La otra realización documentada es \(30/120-30/90=-1/12\). La igualdad escalar no identifica por sí misma los mapas de ambas realizaciones.

La estructura que queda oculta al publicar sólo la traza es

\[
\operatorname{Spec}(E)=
\{-1\ (3),\ 0\ (7),\ +1\ (2)\}.
\]

En efecto, \(P_3-P_0\) y \(P_4-P_0\) son proyectores ortogonales de rangos dos y tres. Por tanto,

\[
E^2=|E|=P_3+P_4-2P_0,\qquad
\tau(|E|)=\frac5{12}.
\]

El mismo operador conserva un balance firmado de −1/12 y una dimensión transversal normalizada de 5/12. Intercambiar los dos canales cambia \(E\) por \(-E\), pero deja \(|E|\) invariante. Esto no identifica 5/12 con una energía física: explica qué distingue la lectura con signo de la lectura positiva.

## 2. Recuperación conjunta y cota óptima

Para un registro \(z\in\mathbb R^{12}\) o \(\mathbb C^{12}\), sean

\[
\bar z=\frac1{12}\sum_{m=0}^{11}z_m,\qquad
B=D_3^*D_3+D_4^*D_4.
\]

El espectro exacto, con multiplicidades, es

\[
0\ (1),\quad 2\ (2),\quad 3\ (2),\quad 4\ (1),\quad
5\ (4),\quad 7\ (2).
\]

Una prueba completa es diagonalizar el desplazamiento: el modo \(k\) tiene autovalor

\[
b_k=4\sin^2(\pi k/4)+4\sin^2(\pi k/3).
\]

Aquí la notación trigonométrica sólo expresa el espectro de una matriz ya construida con enteros. El certificado evita incluso esta evaluación y verifica todos los subespacios por álgebra racional.

Se obtiene, para TODO registro,

\[
\boxed{
2\|z-\bar z\mathbf1\|^2
\le \|D_3z\|^2+\|D_4z\|^2
\le 7\|z-\bar z\mathbf1\|^2.}
\]

Ambas cotas son óptimas. Si \(B^\dagger\) es la inversa sobre el complemento de las constantes y cero sobre ellas,

\[
\boxed{z=\bar z\mathbf1+
B^\dagger(D_3^*D_3z+D_4^*D_4z).}
\]

Con datos \((a,b,q)=(D_3z,D_4z,\sum z_m)\), se recupera

\[
z=(q/12)\mathbf1+B^\dagger(D_3^*a+D_4^*b).
\]

Para datos arbitrarios, la expresión es una reconstrucción por mínimos cuadrados; pertenece a la imagen exacta del extractor sólo si reproduce ambos canales y la carga. Para datos enteros deben conservarse las congruencias de imagen descritas por U016: la forma de Smith es \(\operatorname{diag}(1,\ldots,1,12)\). No se sustituye esa condición por redondeo.

Un canal aislado deja un núcleo de dimensión tres o cuatro. Ambos juntos dejan únicamente la media; la carga elimina esa última ambigüedad. La recuperación se refiere al registro publicado, no a toda su genealogía profunda.

La desigualdad también vale para registros con valores en un espacio de Hilbert y, por suma o integración, para familias de registros. Esta extensión no introduce constantes crecientes con el número de celdas. No demuestra, por sí sola, que el transporte físico entre escalas conserve esa norma.

## 3. Retorno de fase y actualización de memoria

La forma cuadrática interna

\[
\mathcal M(z)=\frac12\langle z,Bz\rangle
=\frac12(\|D_3z\|^2+\|D_4z\|^2)
\]

satisface \(S^*BS=B\), de modo que \(\mathcal M(Sz)=\mathcal M(z)\).

Dada una actualización real del TPK y su registro publicado \(z^+\), definamos su incremento respecto del desplazamiento de fase por

\[
\eta=z^+-Sz.
\]

Esta \(\eta\) es una salida de la actualización completa, no una entrada libre elegida para cerrar una estimación. La identidad exacta es

\[
\boxed{\mathcal M(z^+)-\mathcal M(z)
=\operatorname{Re}\langle BSz,\eta\rangle
+\frac12\langle\eta,B\eta\rangle.}
\]

La rotación de fase sola conserva la forma; el cambio de memoria registra términos de intercambio. No es lícito deducir conservación energética del mero retorno de fase. Asimismo, la parte constante de la memoria sólo queda visible si se conserva la carga \(q\).

Esta identidad es un balance algebraico, no una ley constitutiva nueva de la actualización. La sustitución efectiva para el lector de eventos de U016 está desarrollada en [Actualización TPK, memoria publicada y determinantes dodecafásicos](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/ACTUALIZACION_TPK_ETA_Y_DETERMINANTE.md>): el incremento es el evento firmado que acaba de producirse, transportado al marco de fase correspondiente. No es un parámetro libre.

## 4. Aplicación que propone Rubén: interior, frontera y fluidos

El paso útil es transportar el registro y sus dos canales al balance de frontera, en lugar de insertar el número −1/12 como un coeficiente aislado.

La fuente hidrodinámica ya conserva el defecto no lineal

\[
C_{M\leftarrow N}
=P_MB(u_N,u_N)-B_M(P_Mu_N,P_Mu_N),
\]

y separa una memoria firmada de otra positiva. Esa distinción es compatible en función con separar \(E\) y \(|E|\), pero una correspondencia entre ambos pares exige el mapa efectivo, no sólo esta analogía.

Para cerrar esa aplicación específica deben determinarse desde el transporte TPK:

- qué registro \(z\) publica cada celda o interfaz;
- qué carga y qué actualización \(\eta\) conserva;
- el operador que convierte sus diferencias en el carry hidrodinámico;
- la relación de \(\mathcal M\) con el funcional físico y su escala dimensional;
- la compatibilidad de esa relación con refinamiento y evolución temporal.

La cota 2–7 resuelve el control del registro dodecafásico sobre su media. El paso restante de esta aplicación es demostrar que el operador de transporte y la evolución proporcionan el control requerido sobre el campo hidrodinámico. Esta nota no sustituye ese paso por el signo o por la traza.

Para el ejemplo de agua con interfaz, la tensión superficial interviene en el balance de esfuerzos de la superficie libre; no debe confundirse automáticamente ese problema con el enunciado de regularidad en dominio periódico. Véanse las [notas de fenómenos interfaciales del MIT](https://math.mit.edu/sites/bush/wp-content/uploads/2018/02/18.357-LecNotes-2010.pdf) y el dominio periódico expresamente fijado en la propia fuente HMT consultada.

## 5. Comprobación y falsadores

[Verificador exacto](verificar_defecto_dodecafasico_y_recuperacion.py). Usa matrices racionales de dimensión doce, no cálculos de cifras ni datos metrológicos. Verifica toda la identidad de reconstrucción, no una muestra de registros.

Controles negativos: eliminar un canal, eliminar la carga, o sustituir el par diferencial por la traza pierde recuperabilidad. Confundir rotación con actualización elimina el término de memoria. El éxito del verificador acredita estas identidades locales; no acredita por sí solo una realización física.
