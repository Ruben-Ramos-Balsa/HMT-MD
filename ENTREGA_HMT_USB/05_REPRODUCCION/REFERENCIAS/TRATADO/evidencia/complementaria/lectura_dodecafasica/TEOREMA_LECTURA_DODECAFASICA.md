# Lectura armónica del registro dodecafásico enriquecido

## 1. Corrección de tipo

El observable firmado de doce componentes no se obtiene de la palabra
periódica de seis componentes duplicada por el escáner mínimo. Son objetos de
tipos diferentes. El dominio de la lectura es el estado TPK enriquecido, que
conserva orientación, hoja y una cocadena entera sobre los doce sectores:

\[
x=(v,\varepsilon,h,K,\partial x),\qquad K\in\mathbb Z^{12}.
\]

La palabra visible \(v\) puede tener período seis; el registro orientado \(K\)
no queda determinado por ella. Exigir una inversión \(v\mapsto K\) después de
haber olvidado hoja y orientación confunde una proyección no inyectiva con el
estado completo.

## 2. Operadores

La carta enriquecida puede presentarse de dos maneras equivalentes. Si el
registro completo se serializa, su lectura es la proyección tipada

\[
\Lambda_{12}(x)=K.
\]

Si el estado conserva los observables transversales producidos por los dos
canales, se usa en cambio

\[
\mathcal E_{3,4}^{Q}(x)=
\bigl(b^{(3)},b^{(4)},Q\bigr)
=\bigl((I-S^3)K,(I-S^4)K,\langle\mathbf1,K\rangle\bigr).
\]

El operador de agregación \(\mathcal R_{3,4}^{Q}\) resuelve simultáneamente
las veinticinco ecuaciones enteras, comprueba sus redundancias y rechaza una
familia incompatible. No consulta el vector canónico durante la resolución.

Sobre las tres órbitas de paso tres se aplica la transformada de
Walsh–Hadamard:

\[
\mathcal H_{12}K=
\operatorname{reint}\bigl(H_4K^{(0)},H_4K^{(1)},H_4K^{(2)}\bigr),
\qquad H_4^2=4I_4.
\]

Por consiguiente, \(\mathcal H_{12}\) es inyectiva sobre \(\mathbb Z^{12}\) y
su inversa en la imagen es \(\frac14\mathcal H_{12}\), con el mismo orden de
reintercalación. La lectura transversal es

\[
\mathcal E_{3,4}(K)=
\bigl((I-S^3)K,(I-S^4)K,\langle\mathbf1,K\rangle\bigr).
\]

Como \(\gcd(3,4)=1\), la intersección de los núcleos de las dos diferencias es
la recta constante, y el modo total elimina esa última libertad. Así,
\(\mathcal E_{3,4}\) también determina \(K\) de manera única. En consecuencia,

\[
\boxed{
(b^{(3)},b^{(4)},Q)
\xrightarrow{\ \mathcal R_{3,4}^{Q}\ }
K
\xrightarrow{\ \mathcal H_{12}\ }
U_{12}^{\rm sgn}.}
\]

## 3. Resultado canónico

Para el registro declarado por el estado TPK canónico,

\[
K=(234,543,140,729,659,824,621,058,914,794,146,601),
\]

se obtiene

\[
\mathcal H_{12}K=
(2378,1406,2479,-452,998,-551,-668,-204,-371,-322,-28,-997).
\]

La descomposición en partes positiva y negativa es canónica y posee soportes
disjuntos.

## 4. Covariancia y ablaciones

La acción diedral sobre el registro se transporta a los modos mediante
\(\mathcal H_{12}\rho\mathcal H_{12}^{-1}\). Esto expresa covariancia: una
reflexión no deja fijos los contrastes orientados, sino que los transforma de
forma controlada.

Suprimir \(Q\) deja la libertad \(K\mapsto K+c\mathbf1\). Alterar una sola
coordenada de una cocadena transversal canónica rompe las ecuaciones
redundantes y es rechazado. La suma de posiciones opuestas
\(K_m+K_{m+6}\) pierde el subespacio
antihoja. Olvidar la orientación identifica \(K\) con su reflejo pese a que sus
contrastes son distintos. Finalmente, existen estados con la misma palabra
visible periódica y registros diferentes. Las tres ablaciones demuestran que
hoja, orientación y registro no son adornos: constituyen exactamente la
información que el cociente mínimo elimina.

## 5. Alcance

Queda construido el operador solicitado

\[
\boxed{
X_{\mathrm{TPK}}^{\mathrm{enr}}
\xrightarrow{\mathcal E_{3,4}^{Q}}
(b^{(3)},b^{(4)},Q)
\xrightarrow{\mathcal R_{3,4}^{Q}}K
\xrightarrow{\mathcal H_{12}}U_{12}^{\mathrm{sgn}}.
}
\]

El enunciado no afirma que una proyección bruta o periódica permita recuperar
el registro que previamente se descartó. Esa inversión no pertenece a la
lectura del estado completo y las ablaciones prueban por qué no puede añadirse
sin una sección suplementaria.
