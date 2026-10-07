# Inversión espectral y compatibilidad angular del sector de vacío

## Genealogía y objetivo

Se parte de las construcciones recuperadas en [la traza generativa focal](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/TRAZA_GENERACION_VACIO_TERMICAS.md>). El origen permanece en las semillas y en las operaciones APP–TRIT–TPK. El presente desarrollo compone lectores posteriores de ese mismo origen; no usa magnitudes observadas para seleccionar las semillas, las fases o las constantes anteriores.

La jerarquía pertinente, con sus dependencias transversales, es:

```text
Semillas y hojas APP, con residuo y cociente
└─ Orientación TRIT y operaciones TPK, con fase y memoria
   └─ Estado prolongable y estructura discreta conjunta del continuo
      ├─ Realizaciones π, φ, e y clausura firmada de α
      │  └─ Selector regional y par angular A, C*
      │     └─ B = A_rad I + C*_rad R → T = exp(−B) → q+, q−
      └─ Calendario e incidencia → 90, 120
                         q+, q− + 90,120 → V → r+, r−
                                             ├─ μ, ε, Z, c normalizados
                                             └─ lector inverso de los canales
```

Las dos líneas que concurren en V son antecedentes del mismo objeto; no son dos continuos independientes. Los canales angulares participan también en el funcional de Barbero–Immirzi. Esa reutilización conserva el parentesco estructural, pero no identifica el cociente resolvente de vacío con el funcional lineal dodecafásico.

Las identidades de partida y la inversión hasta r± ya estaban en el capítulo de vacío. Aquí se reúne explícitamente su composición con la recuperación del par angular y se incorpora un control racional. No se atribuye novedad histórica a esta composición: la búsqueda de precedentes fuera de los propietarios focales no está concluida.

## 1. Inversión única del lector de incidencia

Los cardinales de fase dan 90 y 120; su máximo común divisor es 30. Para un canal \(0<q<1\), se escribe \(s=q^{30}\). La identidad publicada se reduce a

\[
r=\frac{1-q^{90}}{1-q^{120}}
=F(s)=\frac{1+s+s^2}{1+s+s^2+s^3}.
\]

Se tiene \(F(0)=1\), \(F(1)=3/4\) y

\[
F'(s)=-\frac{s^2(3+2s+s^2)}{(1+s+s^2+s^3)^2}<0
\qquad(0<s<1).
\]

Por continuidad y monotonía estricta, para cada \(r\in(3/4,1)\) existe exactamente un \(s\in(0,1)\) con \(F(s)=r\). Eliminar el denominador proporciona el polinomio

\[
P_r(s)=r s^3+(r-1)(s^2+s+1).
\]

La recuperación es, por tanto, una operación bien definida: tomar la única raíz de \(P_r\) en \((0,1)\) y después su raíz trigésima positiva. La condición de intervalo es parte de la definición; no se selecciona una raíz por proximidad a un decimal físico.

Esta operación no es una segunda generación de las constantes ni una inversión causal. Es el inverso matemático de un lector ya aplicado, útil para comprobar qué información de los canales permanece en su salida.

## 2. Recuperación de los canales desde dos coordenadas

Las coordenadas normalizadas del manuscrito satisfacen

\[
\widehat Z=\frac{r_-}{r_+},\qquad
\widehat c=\frac1{r_+r_-}.
\]

Por positividad,

\[
r_+=\frac1{\sqrt{\widehat Z\widehat c}},\qquad
r_-=\sqrt{\frac{\widehat Z}{\widehat c}}.
\]

Cuando ambos resultados están en \((3/4,1)\), la inversión anterior determina de manera única \(s_+,s_-\), y con ellos \(q_+,q_-\). La aplicación de pares de canales al par \((\widehat Z,\widehat c)\) es así inyectiva en el dominio considerado. Esto no afirma que todos los pares del dominio ambiente sean producidos por las semillas HMT: la imagen efectiva del generador conserva sus restricciones anteriores.

El producto de sectores sin el cociente no permite reconstruir ambos canales. El cociente aporta la información orientada que falta. Al intercambiar las hojas se permutan r± y s±, permanece \(\widehat c\) y se transforma \(\widehat Z\mapsto\widehat Z^{-1}\). La inversión respeta exactamente esa involución.

### Imagen exacta del dominio de canales

Las condiciones sobre r± dan una descripción explícita del codominio, sin escoger valores objetivo:

\[
1<\widehat Z\widehat c<\frac{16}{9},\qquad
\frac9{16}<\frac{\widehat Z}{\widehat c}<1.
\]

Equivalentemente,

\[
1<\widehat c<\frac{16}{9},\qquad
\max\!\left(\widehat c^{-1},\frac9{16}\widehat c\right)
<\widehat Z<
\min\!\left(\widehat c,\frac{16}{9\widehat c}\right).
\]

La equivalencia prueba tanto necesidad como suficiencia: cualquier pareja positiva que satisface estas desigualdades produce r± en el intervalo requerido y, mediante las dos cúbicas, una única pareja de canales. En coordenadas logarítmicas \(u=\log\widehat c\), \(v=\log\widehat Z\), el dominio es

\[
0<u<\log\frac{16}{9},\qquad
|v|<\min\!\left(u,\log\frac{16}{9}-u\right).
\]

El intercambio de orientación es \((u,v)\mapsto(u,-v)\). Queda así expresada la imagen exacta del lector sobre el dominio ambiente \((0,1)^2\), no sólo una prueba de inyectividad. Las restricciones adicionales del generador HMT, si seleccionan un subconjunto de canales, se transportan dentro de este dominio y no quedan demostradas por su sola descripción.

## 3. Compatibilidad con α y el contraángulo

El propietario angular conserva

\[
q_+q_-=D_A,\qquad
\alpha=-\frac9{100\pi}\log D_A,\qquad
C^*=\frac{90}{\pi}\log\frac{q_-}{q_+}.
\]

Estas expresiones son posteriores a la generación de α y del par angular. Componiéndolas con \(s_\pm=q_\pm^{30}\), resultan

\[
\boxed{\alpha=-\frac3{1000\pi}\log(s_+s_-)},
\qquad
\boxed{C^*=\frac3\pi\log\frac{s_-}{s_+}}.
\]

La primera expresión recupera la contracción común; la segunda, la separación orientada. El intercambio de hojas conserva α y cambia de signo C*. La misma realización de π que intervino en la rama angular aparece en estas fórmulas; no se inserta un nuevo valor externo para recuperar las coordenadas.

El resultado es una condición de compatibilidad entre realizaciones: formar los canales desde el par angular, calcular el operador de vacío e invertir sus coordenadas conduce al mismo par angular. No es una definición primaria alternativa de α, ni prueba por sí sola sus dos vías de generación dodecafásica, ni implica recuperar la historia íntegra de acarreo a partir de dos números.

Fuente angular: [canales y recuperación de invariantes](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/wrappers/capitulo_38_jerarquia_unica.tex:1368>).

## 4. Relación con otros lectores del mismo estado

El funcional de Barbero–Immirzi recibe q± y las incidencias 90/120, pero aplica a esos canales la diferencia de un funcional con pesos 12:-1. El vacío utiliza el cociente \((1-q^{90})/(1-q^{120})\). Son operaciones distintas sobre antecedentes compartidos. La relación precisa entre ambos sectores es esa concurrencia de entradas estructurales y la compatibilidad con la involución; no una igualdad de sus valores.

Los cuantos eléctricos incorporan, además, la sección de acción. En particular, \(R_K\) y \(G_0\) dependen de α y Z pero no de h de forma independiente, mientras que \(\Phi_0\) y \(K_J\) retienen la raíz de la sección de acción y su inversa. La sección térmica combina acción, reloj e información ternaria. Así se obtiene una red de dependencias con información conservada diferente en cada lector.

La definición funcional apropiada para este sector es **sistema de coordenadas espectrales de contracción y orientación**, acompañado de las rectas dimensionales del manuscrito. No sustituye la definición de todo el estado ni el TPK por una matriz aislada.

## 5. Implementación y comprobación

El [control racional](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/verificar_inversion_sector_vacio.py>) efectúa:

1. La selección de fases y el censo que producen 90/120; después calcula su divisor común 30.
2. La evaluación racional del lector para diez parejas de prueba y la comprobación exacta de las dos identidades constitutivas.
3. La recuperación de r± desde las coordenadas, la verificación exacta de veinte raíces cúbicas y su encierro por bisección racional con anchura \(2^{-80}\).
4. El control de inversión de orientación y el rechazo de cuatro sectores ajenos al intervalo admisible.
5. Veinte controles del dominio exacto de coordenadas —parejas originales e invertidas— y el rechazo de seis parejas exteriores o de frontera.

La ejecución ha terminado con `PASS_LOCAL_RATIONAL_VACUUM_SECTOR_INVERSION`; el [registro de resultados y alcance](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/RECIBO_INVERSION_SECTOR_VACIO.json>) conserva las comprobaciones y la huella del programa. Las parejas racionales son casos algebraicos de prueba; no se presentan como estados físicos obtenidos de las semillas. La prueba general de existencia y unicidad es la monotonía anterior, no el censo de diez ejemplos. No se han empleado decimales objetivo ni se han modificado los programas o PDFs originales.

Este control amplía la comprobación de interrelaciones. No certifica por sí mismo la producción primaria de constantes, la historia de selección de todos los lectores ni la correspondencia experimental del modelo.

## 6. Ley de composición transportada del lector espectral

La inversión permite determinar qué operación sobre los valores representa la composición de canales. No se escoge una nueva constante: se transporta la multiplicación de los canales ya definidos por el mismo lector F. El resultado siguiente es una formalización algebraica de esa composición; no se reivindica prioridad histórica ni se atribuye al estado completo una ley obtenida en su realización sectorial.

Sea \(\psi=F^{-1}\). En el dominio \(D=[3/4,1)\), que añade el límite q=1 al sector contractivo, se define

\[
\boxed{r\odot t=F\bigl(\psi(r)\psi(t)\bigr).}
\]

Como \(\psi(r\odot t)=\psi(r)\psi(t)\), esta operación es asociativa, conmutativa y cancelativa. Su elemento neutro es \(F(1)=3/4\). Sólo ese elemento tiene inverso dentro de D: las otras raíces están en \((0,1)\) y su inversa multiplicativa sale de ese intervalo. El sector estrictamente contractivo no contiene el neutro, aunque es cerrado bajo composición.

La coordenada

\[
\ell(r)=-\frac1{30}\log\psi(r)
\]

identifica este monoide con \((\mathbb R_{\ge0},+)\). En particular, \(\ell(r\odot t)=\ell(r)+\ell(t)\), y para un canal generado q se tiene \(\ell(r)=-\log q\). Es una coordenada del transporte posterior, no una reconstrucción de su historia.

El producto numérico ordinario no representa esta composición:

\[
F(1/2)=\frac{14}{15},\qquad
\frac{14}{15}\odot\frac{14}{15}=F(1/4)=\frac{84}{85}
\ne\frac{196}{225}.
\]

La operación inducida conserva una relación que se perdería si se sustituyera el transporte por la mera multiplicación de sus valores espectrales.

### Cancelación y prolongación inversa

Dados r,u en D, la ecuación \(r\odot t=u\) tiene solución en D exactamente cuando \(u\ge r\). En tal caso es única y vale

\[
t=F\!\left(\frac{\psi(u)}{\psi(r)}\right).
\]

La condición deriva de que el cociente de raíces debe pertenecer a \((0,1]\). Distingue una inversión admisible dentro del sector contractivo de una prolongación que sale de él.

La misma función racional F es estrictamente decreciente en todo \(s>0\), con límites 1 en cero y 0 en infinito. Por tanto, extender el dominio escalar a \(0<r<1\) transporta el grupo \((\mathbb R_{>0},\cdot)\). Su inversa tiene una expresión particularmente simple:

\[
F(s^{-1})=sF(s),\qquad
\boxed{r^{\ominus}=\psi(r)\,r},\qquad
r\odot r^{\ominus}=\frac34.
\]

Esta extensión es una completación algebraica del lector. Los nuevos canales q>1 no se atribuyen por ello al dominio físico ni a la imagen de semillas previamente certificados. La involución cambia el signo de \(\ell\) y es distinta del intercambio de las dos hojas.

## 7. Sustitución operatoria y conservación de la orientación

En un mismo marco de la involución \(R^2=I\), sean \(P_\pm=(I\pm R)/2\) y

\[
T_a=q_{a,+}P_++q_{a,-}P_-,\qquad
V_a=F(T_a^{30}).
\]

Para canales positivos, el cálculo funcional satisface \(\psi(V_a)=T_a^{30}\). Los operadores de este sector conmutan porque comparten los dos proyectores. Si la composición considerada es \(T_{a\circ b}=T_aT_b\), entonces

\[
\boxed{V_{a\circ b}=F\bigl(\psi(V_a)\psi(V_b)\bigr),}
\]

no \(V_aV_b\) en general. La prueba se obtiene de \((T_aT_b)^{30}=T_a^{30}T_b^{30}\) y de la descomposición por proyectores. Para cualquier función racional admisible f,

\[
P_\pm f(T)=f(q_\pm)P_\pm.
\]

Esta igualdad precisa la sustitución permitida entre una ecuación de canal y su realización operatoria. Una traza o promedio de los canales no es, en general, multiplicativa y no puede sustituir esas proyecciones en todas las ecuaciones.

El intercambio \((r_+,r_-)\mapsto(r_-,r_+)\) es un automorfismo involutivo de la ley componente a componente. Si se quiere representarlo como conjugación, debe conservarse un operador que intercambie P+ y P−. Con \(R=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\), sirve \(L=\operatorname{diag}(1,-1)\), pues \(LRL^{-1}=-R\). Conjugar por R no intercambia sus propios sectores.

En las coordenadas recuperadas \(x=(\ell(r_+)+\ell(r_-))/2\), \(y=(\ell(r_+)-\ell(r_-))/2\), la composición suma las parejas. El intercambio de hojas actúa como \((x,y)\mapsto(x,-y)\); la inversión de ambos canales en la completación algebraica actúa como \((x,y)\mapsto(-x,-y)\). Son dos involuciones diferentes y conmutan en este sector.

El alcance no se extiende automáticamente a operadores con marcos no conmutativos. En ese caso el producto de dos operadores positivos puede no ser autoadjunto, la potencia del producto no tiene por qué separarse y no existe esta diagonalización simultánea. Tampoco el cierre algebraico del dominio ambiente prueba que la imagen de las semillas sea cerrada bajo la composición: para esa promoción hay que conservar el transporte efectivo de las historias correspondientes.

## 8. Control de la ley de composición

El [programa de comprobación algebraica](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/verificar_composicion_lector_vacio.py>) verifica con racionales la cúbica, la composición, la asociatividad, la identidad, la inversión extendida y la orientación. Incluye encierros racionales calculados sólo desde las coordenadas, el contraejemplo al producto ordinario y un caso de marcos no conmutativos cuyo producto no es autoadjunto. Las pruebas generales son las identidades anteriores; los casos finitos no las sustituyen. El [recibo de ejecución](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/RECIBO_COMPOSICION_LECTOR_VACIO.json>) registra 49 composiciones, 343 casos de asociatividad, siete identidades e inversiones extendidas y cuatro rechazos de dominio. La ejecución terminó con `PASS_LOCAL_VACUUM_READER_COMPOSITION`.
