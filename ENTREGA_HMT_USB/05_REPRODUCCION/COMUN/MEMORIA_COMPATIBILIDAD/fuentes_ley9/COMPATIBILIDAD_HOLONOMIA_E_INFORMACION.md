# Compatibilidad constitutiva, holonomía relativa e información operacional

22 de septiembre de 2026. Desarrollo acumulativo autorizado por Rubén. Se conserva el texto literal aprobado en `NARRATIVA_APROBADA_Y_MANDATO_DESARROLLO.md`; esta nota añade demostraciones y no sustituye ninguna edición.

## 1. Antecedentes y alcance de las composiciones

La genealogía de partida es APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. APP conserva las evaluaciones aditiva y multiplicativa, cociente y residuo sobre sus hojas; TRIT conserva régimen y orientación; TPK compone selección, transporte y actualización con memoria, acarreo, ruta y frontera. Se mantiene U_t → Γ9 → K_ph: la última es una representación reducida posterior. La prolongación w6 → w12 → w18 → w24 → w30 → R36 → G9 precede a los lectores regionales y al cierre dodecafásico. π, φ, e y α son salidas correlacionadas de esta genealogía, no valores metrológicos que seleccionen estados.

El corte focal está después de la sección de acción, el par angular y los lectores de incidencia. Se heredan x=A_rad, y=C*_rad, q±=exp(−x∓y), la respuesta de incidencias 90/120 y ζ=artanh(C*/A). Se distingue el ciclo dodecafásico C12, la holonomía Γ9 y la nueva composición de lectores descrita aquí. Las cinco construcciones del continuo permanecen consustanciales; esta nota no modifica ni recertifica sus generadores.

El propósito es componer operadores ya realizados y demostrar consecuencias, no seleccionar coeficientes a partir de resultados físicos. Las nuevas pruebas emplean álgebra, series y cálculo diferencial como lenguaje posterior. No se afirma prioridad histórica universal, un nuevo régimen experimental ni una refutación de la teoría de información.

La preservación y el control focal de orden causal no equivalen a certificación global. Persiste como antecedente de gestión la divergencia de AGENTS.md detectada en el arranque global; no se ha alterado ni resellado ese archivo. El integral autoral de la serie y los deltas del 21 de septiembre se conservan frente al resolutor histórico de 2.084 páginas.

## 2. Reciprocidad diferencial de velocidad e impedancia

El artículo III construye

\[
T=e^{-xI-y\mathcal R},\quad
V=(I-T^{90})(I-T^{120})^{-1}=r_+P_++r_-P_-,
\quad r_\pm=f(e^{-30(x\pm y)}),
\]

con f(s)=(1−s³)/(1−s⁴), x>|y| y proyectores de hoja conservados. La cámara física marcada x>y>0 y su conjugada están contenidas en esta familia analítica. Se define

\[
c_\ell=\log\widehat c=-\log r_+-\log r_-,\qquad
z_\ell=\log\widehat Z=\log r_--\log r_+.
\]

Estas letras son coordenadas logarítmicas normalizadas, no nuevas constantes ni el contraángulo C*. Sean u=30(x+y), v=30(x−y), g(w)=log f(e^-w), a=g'(u), b=g'(v). Entonces

\[
g'(w)=\frac3{e^{3w}-1}-\frac4{e^{4w}-1}>0,
\qquad
D(c_\ell,z_\ell)=-30
\begin{pmatrix}a+b&a-b\\a-b&a+b\end{pmatrix}.
\]

Los autovalores son −60a y −60b. El Jacobiano es simétrico y definido negativo, su determinante es 3600ab>0 y

\[
\boxed{\partial_y\log\widehat c=\partial_x\log\widehat Z.}
\]

Prueba: se derivan cℓ=−g(u)−g(v) y zℓ=g(v)−g(u). La positividad de g' procede del decrecimiento estricto en k>0 de k/(exp(kw)−1), o de la expresión racional positiva dada en §4.

La igualdad relaciona la respuesta de la velocidad a la separación orientada con la respuesta de la impedancia a la coordenada común. Ambas sensibilidades proceden de una misma función espectral. Es una reciprocidad de esta familia constitutiva; no se identifica sin prueba con una ley termodinámica o de electromagnetismo macroscópico.

## 3. Potencial espectral y conexión de profundidad dos con Catalán

### Construcción del potencial

Definimos, desde los canales ya construidos,

\[
\mathscr F(x,y)=\sum_{\sigma=\pm1}\sum_{n\ge1}
\left[\frac{e^{-120n(x+\sigma y)}}{120n^2}
-\frac{e^{-90n(x+\sigma y)}}{90n^2}\right].
\]

En todo compacto de x>|y| la serie y sus derivadas de cualquier orden fijo convergen uniformemente: x±y tienen un mínimo positivo, y una potencia de n multiplicada por una exponencial decreciente es sumable. Derivando término a término y usando −log(1−z)=Σ z^n/n,

\[
\boxed{\partial_x\mathscr F=c_\ell,\qquad
\partial_y\mathscr F=z_\ell.}
\]

El Hessiano es el Jacobiano de §2, por lo que F es estrictamente cóncava. Su constante aditiva queda fijada por F→0 cuando x−|y|→∞. F es un potencial matemático de la respuesta; no se le asignan unidades de energía ni se declara un potencial termodinámico.

### Realización por un mismo momento espectral

Sea D2(z)=Σ_{n≥1} z^n/n². Su reconocimiento como dilogaritmo es posterior a esta definición por serie. En |z|<1 satisface (z∂z)²D2=z/(1−z). Entonces

\[
\mathscr F=\sum_{\sigma=\pm}
\left[\frac{D_2(q_\sigma^{120})}{120}
-\frac{D_2(q_\sigma^{90})}{90}\right].
\]

El momento orientado de Catalán que construye el artículo III satisface

\[
\mathcal C_2(s)=\operatorname{Im}D_2(is)
=\sum_{k\ge0}\frac{(-1)^ks^{2k+1}}{(2k+1)^2},\qquad
\mathcal C_2(1)=G_{\rm Cat}.
\]

Prueba: las potencias pares de i son reales y las impares tienen parte imaginaria (−1)^k. La serie converge absolutamente incluso en s=1. Para 0≤s<1, aplicar término a término dos veces s∂s devuelve s/(1+s²), el coeficiente orientado del resolvente del cuarto de giro ya presente en el corpus. La identidad diferenciada en s=1, si se utiliza, se interpreta por continuación analítica o límite de Abel: la serie dos veces diferenciada no converge ordinariamente en ese extremo. La identificación C2(1)=G_Cat procede directamente de la serie original absolutamente convergente.

Por tanto, el momento de Catalán y el potencial constitutivo se reúnen mediante un mismo momento espectral de profundidad dos, evaluado en soportes diferentes: cuarto de giro orientado y contracciones de los sectores 90/120. Esta composición no identifica Catalán con F ni afirma que su único valor extremo determine todos los canales. La familia analítica y sus argumentos conservan información que un valor aislado no contiene.

### Compatibilidad con amplificación

Para T_m=T⊗I_{9^m} y τ_m=Tr/(2·9^m), se tiene exactamente

\[
\mathscr F_m=2\tau_m\left[
\frac{D_2(T_m^{120})}{120}-\frac{D_2(T_m^{90})}{90}\right]
=\mathscr F.
\]

La multiplicidad 9^m cancela la normalización. El mismo argumento conserva sus derivadas. Esto acredita amplificación de la representación, no cualquier refinamiento imaginable de TPK. No se sustituye el operador temporal por una lista de autovalores sin marcas de hoja.

Para cualquier lazo suave cerrado en esta familia analítica,

\[
\oint(c_\ell\,dx+z_\ell\,dy)=0.
\]

La igualdad se refiere a la proyección constitutiva de dos coordenadas. No implica que la historia enriquecida o su holonomía operatoria sean triviales.

## 4. Restitución exacta y sensibilidad finita

Con L=log(16/9), el mapa (x,y)↦(cℓ,zℓ) es un difeomorfismo real analítico de x>|y| sobre

\[
0<c_\ell+z_\ell<L,\qquad 0<c_\ell-z_\ell<L.
\]

Prueba: g crece estrictamente de log(3/4) a 0; las combinaciones cℓ+zℓ=−2g(u) y cℓ−zℓ=−2g(v) recuperan u,v mediante g^-1. Entonces x=(u+v)/60 e y=(u−v)/60. La inyectividad se mantiene al restringir a la imagen efectivamente producida por HMT; no se declara que HMT produzca todo el cono.

Con s=e^-w,

\[
a(w)=g'(w)=
\frac{s^3(s^2+2s+3)}{(1+s+s^2)(1+s+s^2+s^3)},
\quad 0<a(w)<\frac12.
\]

La función es estrictamente decreciente, a(0+)=1/2 y a(w)~3e^-3w en infinito. Para probar el decrecimiento,

\[
a'(w)=-\frac9{4\sinh^2(3w/2)}+
\frac{16}{4\sinh^2(2w)}<0,
\]

porque k/sinh(kw/2) decrece estrictamente en k>0. Se tienen además ½e^-3w<a(w)<3e^-3w. La cota inferior resulta al multiplicar denominadores de

\[
2(s^2+2s+3)-(1+s+s^2)(1+s+s^2+s^3)
=(1-s)(5+7s+6s^2+3s^3+s^4)>0;
\]

la superior resulta de 3(1+s+s²)(1+s+s²+s³)−(s²+2s+3)>0.

Si m=30(x−|y|), M=30(x+|y|), la norma del inverso del Jacobiano es 1/[60a(M)]. Sobre una región convexa con ambos argumentos en [m0,M0],

\[
60a(M_0)\|p-q\|\leq\|F(p)-F(q)\|
\leq60a(m_0)\|p-q\|,
\quad F=(c_\ell,z_\ell).
\]

Prueba: integrar el Hessiano sobre el segmento; para la cota inferior se usa −〈F(p)−F(q),p−q〉≥60a(M0)‖p−q‖² y Cauchy–Schwarz. La superior usa su norma máxima. Son cotas de errores finitos en ese dominio.

En y=0 y x→∞, ambas direcciones se contraen por igual: el número de condición matricial es uno, pero la norma del inverso crece como e^{90x}/180. Por tanto, invertibilidad exacta y recuperación robusta frente a error absoluto son propiedades diferentes. En |y|→x con x fijo>0 no hay singularidad diferencial: una derivada tiende a 1/2 y la otra a a(60x)>0.

## 5. El cuarto de giro procede del ciclo dodecafásico

Se recupera la construcción del artículo III: en R^12, C12 e_j=e_(j+1 mod12), Q=P4_cyc(I−C12^6)/2 y

\[
u_0=(1,0,-1,0,1,0,-1,0,1,0,-1,0)^T,\quad
v_0=C_{12}u_0,\qquad W=(u_0,v_0)/\sqrt6.
\]

W^TW=I, WW^T=Q y C12 W=WJ0, donde J0=[[0,−1],[1,0]], J0²=−I. En particular C12³W=−WJ0. El plano tiene así un entrelazador explícito con el ciclo; no se ha introducido un giro externo para ajustar una respuesta.

El artículo X realiza Sζ=diag(e^{ζ/2},e^-ζ/2) y Jζ=SζJ0Sζ^-1. Sobre ese plano definimos

\[
U_\zeta(\theta)=S_\zeta e^{-\theta J_0}S_\zeta^{-1}
=\begin{pmatrix}
\cos\theta&e^\zeta\sin\theta\\
-e^{-\zeta}\sin\theta&\cos\theta
\end{pmatrix}.
\]

El signo de θ fija la orientación elegida. La razón generada ξ=C*/A, con |ξ|<1 y ambos ángulos expresados en la misma unidad, satisface ζ=artanh ξ. En la orientación conjugada, (ε,ξ)→(−ε,−ξ) conserva la sección positiva de acción mediante el recuperador orientado del corpus; ζ cambia de signo.

## 6. Lazo relativo de dos transportes

Sean U=Uζs(θ), V=Uζr(φ) y H=UVU^-1V^-1. Los productos se leen con acción de derecha a izquierda. Con δ=ζs−ζr y χ=sinhδ sinθ sinφ,

\[
\boxed{\det H=1,\qquad\operatorname{tr}H=2+4\chi^2,\qquad
H=I\Longleftrightarrow\chi=0.}
\]

Prueba. Conjugando simultáneamente por Sζr^-1, V es R(−φ), y U tiene términos e^±δ sinθ. La multiplicación directa da UV−VU=−2χ diag(1,−1) en esa referencia. Luego H−I=(UV−VU)U^-1V^-1, lo que demuestra la equivalencia con χ=0. La multiplicación, o la identidad de trazas para matrices unimodulares, da tr H=2+4χ². Su polinomio característico es λ²−(2+4χ²)λ+1; por tanto

\[
\lambda_\pm=(\sqrt{1+\chi^2}\pm|\chi|)^2
=\exp[\pm2\operatorname{arsinh}|\chi|].
\]

Esto es una holonomía relativa de la composición declarada. No se identifica con Γ9 ni con una actualización completa de TPK por semejanza de nombres.

### Especialización enteramente determinada por el par conjugado

Sean U₊=Uζ(π/2), U₋=U−ζ(π/2). Ambos satisfacen U₊²=U₋²=−I, pero

\[
U_+U_-=-\operatorname{diag}(e^{2\zeta},e^{-2\zeta}),\qquad
\boxed{H=(U_+U_-)^2=\operatorname{diag}(e^{4\zeta},e^{-4\zeta}).}
\]

Al escribir ξ=tanhζ=C*/A, con ambos ángulos expresados en la misma unidad, se obtiene

\[
\boxed{H=\operatorname{diag}\left(
\left[\frac{1+\xi}{1-\xi}\right]^2,
\left[\frac{1-\xi}{1+\xi}\right]^2\right),\qquad
\operatorname{tr}H-2=\frac{16\xi^2}{(1-\xi^2)^2}.}
\]

La fórmula de H compone el cuarto de giro y las formas conjugadas del mismo par. Su expresión es exacta en la razón angular generada ξ.

En la rama positiva de acción del corpus, A_deg=1000α y C*_deg=2(η_ret+α), con ℏ_ret=s0η_ret. Por tanto,

\[
\xi=\frac{\eta_{\rm ret}+\alpha}{500\alpha},\qquad
\rho=e^{4\zeta}
=\left(\frac{501\alpha+\eta_{\rm ret}}{499\alpha-\eta_{\rm ret}}\right)^2,
\quad 0<\eta_{\rm ret}<499\alpha.
\]

Los coeficientes 501 y 499 son 500±1; 500 procede del factor 1000/2 del par angular y no es un nuevo parámetro. Con los ejes orientados conservados, la restitución es

\[
\boxed{\eta_{\rm ret}=\alpha\left[
500\frac{\sqrt\rho-1}{\sqrt\rho+1}-1\right].}
\]

La derivada dη_ret/dρ=500α/[√ρ(√ρ+1)²] es positiva. La cámara η_ret>0 corresponde a ρ>(501/499)²; el borde η_ret→499α corresponde a ρ→∞. Es una lectura inversa del coeficiente adimensional de acción desde el transporte relativo y la coordenada α ya construida. Conserva la escala s0 como antecedente: una transformación unimodular de forma no determina por sí sola esa escala dimensional. La orientación conjugada invierte ρ y transporta la etiqueta de acción; no convierte η_ret en acción negativa.

### Iteración del lazo y acumulación orientada

Sea ρ=e^{4ζ}=((1+ξ)/(1−ξ))². Para todo entero n,

\[
H^n=\operatorname{diag}(\rho^n,\rho^{-n}),\qquad
Q_n=\rho^nQ_0,\quad P_n=\rho^{-n}P_0.
\]

La prueba es la multiplicación de matrices diagonales, extendida a n<0 mediante el inverso. Se conservan el producto Q_nP_n=Q_0P_0 y el área simpléctica, mientras el estado cambia para ζ≠0 y X_0≠0. En el programa de cuatro operaciones, los incrementos de fase declarados suman cero en cada repetición; esa contabilidad de fases no determina el transporte total del estado.

Para ζ≠0 y Q_0≠0 se recupera exactamente n=log|Q_n/Q_0|/(4ζ). Si Q_0=0, P_0≠0 permite n=−log|P_n/P_0|/(4ζ). La lectura requiere conocer la preparación y conservar una referencia. La extensión multiplicativa H^{n+m}=H^nH^m corresponde a un incremento logarítmico aditivo 4(n+m)ζ. Invertir el lazo cambia el signo de ese incremento.

Así, un programa fijo y repetido admite una respuesta que registra su iteración. Esto es una realización matemática de acumulación operacional en la composición estudiada. No se identifica n con todo el acarreo o la memoria de Γ9, ni se deduce una entropía nula para la dinámica completa a partir de la periodicidad de su programa de fases. Si la amplitud inicial es desconocida y sólo se dispone del estado final, n no queda determinado por esa lectura aislada.

### Levantamiento explícito a las doce fases

Sea S̃ζ=I−Q+WSζW^T y L±=S̃±ζ C12³ S̃±ζ^-1. En Ran Q actúan U₊,U₋, respectivamente; en el complemento ambos actúan como C12³. Por tanto,

\[
L_+L_-L_+^{-1}L_-^{-1}=I-Q+WHW^T.
\]

La acción complementaria se cancela. La traza del operador de doce fases es 10+tr H. El entrelazamiento y la composición son exactos y están comprobados racionalmente usando los vectores enteros u0,v0. Este levantamiento reúne el antecedente dodecafásico y el transporte elíptico; no afirma que su secuencia sea por sí misma la actualización autónoma original de TPK.

### Refinamiento y límite

La amplificación H_m=H⊗I_{9^m} conserva (1/9^m)Tr H_m=Tr H, norma y espectro distintos de multiplicidades. Con embeddings v↦v⊗e0, H_(m+1)ι_m=ι_mH_m. El operador uniforme define en el límite inductivo Hilbertiano una extensión acotada, con la misma norma. Es el límite de esta amplificación; no se sustituye por él otro sistema de refinamientos del corpus.

## 7. Qué distingue un cambio de carta de un efecto relativo

El transporte de coordenadas T_n=Sζ(n+1)R(−θn)Sζn^-1 telescopa:

\[
T_{N-1}\cdots T_0
=S_{\zeta_N}R\left(-\sum_n\theta_n\right)S_{\zeta_0}^{-1}.
\]

Si retornan carta y fase, resulta I. El conmutador de §6 compone evoluciones de formas distintas en una referencia común; no es ese cambio pasivo.

Bajo un cambio común de representación P, U,V,H se conjugan por P. Traza y espectro de H permanecen invariantes. Si además X↦PX y g↦P^-TgP^-1, se conserva X^TgX y toda lectura energética correctamente transportada. Así, un H≠I no desaparece por renombrar coordenadas.

Esto constituye un protocolo matemático relacional cerrado. Su implementación experimental requiere que las evoluciones e inversas sean operaciones físicas disponibles y que sistema, referencia y controlador tengan una realización común. No se afirma aquí una fuerza nueva ni una fuente de energía.

### Conservación de área y conservación de una misma energía

Cada cuarto de giro conserva su propia métrica: gζ=diag(e^-ζ,e^ζ) para U₊, y g−ζ para U₋. No existe una métrica positiva común cuando ζ≠0. Prueba: G=[[a,b],[b,d]]>0 y U₊^TGU₊=G obligan a b=0,d=ae^{2ζ}; U₋^TGU₋=G exige d=ae^-2ζ. Son compatibles sólo con ζ=0.

Por tanto, conservar el área simpléctica no equivale a conservar una misma forma energética durante toda composición de estos transportes. En la referencia g_r=S_r^{-T}S_r^{-1}, con ω_r>0, X≠0 y E_r(X)=ω_r X^Tg_rX/2,

\[
\frac{E_r(HX)}{E_r(X)}
=\frac{x^T\bar H^T\bar Hx}{x^Tx},
\qquad \bar H=S_r^{-1}HS_r,\quad x=S_r^{-1}X.
\]

Los extremos son los cuadrados de los valores singulares. En el caso conjugado diagonal son e^{±8|ζ|}, mientras las dilataciones del estado son e^{±4ζ}. Esta diferencia de exponentes es necesaria. Cambiar físicamente de operación exige contabilizar el controlador; la ganancia de una lectura no acredita creación de energía.

### El orden requiere una lectura orientada

Intercambiar U₊ y U₋ invierte H. La traza y el conjunto de ganancias extremas son iguales para H y H^-1. Esos escalares detectan el efecto del lazo pero no su orientación. Dos entradas independientes con sus respuestas vectoriales completas reconstruyen H; una medida escalar no basta en general.

En el caso conjugado, con ejes de referencia marcados, sean G_Q=E_r(He_Q)/E_r(e_Q), G_P=E_r(He_P)/E_r(e_P). La lectura

\[
\mathcal O=\tfrac14\log(G_Q/G_P)=4\zeta
\]

recupera la orientación y cambia de signo al invertir el lazo. Los ejes y la métrica deben transportarse juntos bajo un cambio de representación. Así se distingue la orientación sin atribuirla a una traza que la elimina.

## 8. Información de historia frente a estadística de ocupación

Los productos U₊U₋U₊⁻¹U₋⁻¹ y U₊U₊⁻¹U₋U₋⁻¹ contienen las mismas cuatro operaciones con las mismas multiplicidades. El segundo vale I; el primero es H≠I para ζ≠0. Por tanto, cualquier estadística que dependa únicamente de las multiplicidades asigna el mismo resultado a dos protocolos con acciones diferentes sobre el estado.

La conclusión exacta es que esa estadística no constituye una descripción suficiente para predecir la respuesta de la composición. No se refuta Shannon: una distribución sobre secuencias ordenadas puede representar el orden. Se distingue la información que se ha conservado en el observable elegido.

Proponemos llamar **información operacional de una historia**, en esta representación, a la clase de su transporte ordenado distinguible por las lecturas admitidas. Sea una colección de detectores D definidos sobre operadores: puede incluir D_{X,L}(H)=L(HX), con preparación X y lector lineal L, o D_tr(H)=tr H. Dos historias son equivalentes si D(H1)=D(H2) para todos los detectores admitidos. Ampliar la colección puede separar clases antes indistinguibles. Con respuestas vectoriales completas en una base se reconstruye todo operador lineal; con sólo traza puede persistir H~H^-1. Así se distingue el detector de una respuesta del estado del detector espectral del operador.

Esta definición no identifica el transporte con toda la genealogía TPK: historias distintas pueden producir el mismo operador en una representación. La información latente en otras hojas, incidencias y prolongaciones se conserva en sus propios lectores.

La dimensión estadística y la operacional son compatibles. La tasa de crecimiento combinatorio, o entropía topológica, cuenta el crecimiento asintótico de configuraciones admisibles; una tasa de entropía de Shannon requiere además una distribución. Un mapa de observación determina qué transformaciones pueden reconstruirse. Ninguna de las pruebas anteriores declara entropía termodinámica universal nula. El aporte es precisar qué descripción es suficiente para una tarea de predicción o restitución.

## 9. Consecuencias y nuevas definiciones propuestas

1. **Potencial espectral constitutivo:** \(\mathscr F\), definido por los momentos 90/120; sus dos derivadas son log velocidad y log impedancia. Es una definición matemática posterior a los canales, sin interpretación energética añadida.
2. **Reciprocidad constitutiva diferencial:** igualdad de sensibilidades cruzadas demostrada en §2. Proporciona una restricción conjunta verificable, además de los valores.
3. **Defecto de cierre relativo:** tr H−2, que detecta el lazo no trivial, acompañado de una lectura orientada como O cuando se requiere distinguir el orden. La traza sola no define toda la memoria.
4. **Restitución operacional:** recuperación de la acción de la historia desde una colección especificada de observables; se distingue de la restitución de dos canales y de la reconstrucción integral del estado.
5. **Margen de restitución:** la cota 60a(M0) de §4 cuantifica estabilidad absoluta en un dominio, mientras la inyectividad sólo afirma unicidad exacta.

Las coordenadas de masa, frecuencia, radios y temperatura de la nota anterior permanecen intactas. Esta nota añade dos niveles: compatibilidad diferencial entre lectores escalares y memoria de orden en composiciones operatorias. No se identifica el factor de dilatación de H con una masa nueva sin pasar por el lector de masas correspondiente.

## 10. Procedencia y pruebas reproducibles

Fuentes activas, bajo `/Users/ruben/Documents/New project/output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/`:

- `03/ES/source/manuscrito/sections/04_respuesta_constitutiva.tex`: cociente 90/120, espectro positivo, inversión y normalización.
- `03/ES/source/manuscrito/sections/05_ciclo_catalan.tex:69`: plano de cuarto de giro, W, resolvente y momento orientado.
- `10/ES/source/libro/reciprocidad_radial.tex:154`: recuperador orientado de acción; `:200`: Sζ, Jζ y entrelazamiento.
- `10/ES/source/libro/01_acoplamiento.tex:292`: identificación de operadores y holonomía relativa desde respuestas; sus cotas permanecen como antecedente distinto.
- `10/ES/source/libro/principios_holograficos.tex:340`: conservación de operadores y productos en la imagen de una isometría, y separación respecto de Γ9.
- `HIBRIDACION_ACCION_MASA_PROPAGACION.md`: convexidad previa, masas/frecuencias/radios, pesos térmicos y transporte de acción.

La búsqueda focal de procedencia en estos propietarios localizó el potencial angular implícito por su lector y los operadores del lazo, pero no el enunciado conjunto reunido aquí. Se registra como formalización y prueba focal de su composición, sin atribuir al asistente los antecedentes autorales ni reivindicar originalidad universal.

El programa `verificar_compatibilidad_holonomia.py` comprueba identidades racionales, controles de signos y falsadores. La prueba general, la convergencia de series y los límites son los textos anteriores; los casos finitos no los sustituyen.
