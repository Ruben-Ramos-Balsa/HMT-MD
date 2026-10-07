# Curvatura de la conexión canónica total y comparación de representaciones

Desarrollo focal del 29 de septiembre de 2026. Esta nota conserva el objetivo
original: la curvatura del mismo operador total y su límite. Construye una
realización canónica precisa de curvatura nula; no la identifica sin prueba
con el Hamiltoniano cuántico interactuante utilizado en las notas anteriores.

## 1. Procedencia y dominio

Se conserva APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo.
La actualización completa conserva hojas, orientación, acarreo, ruta,
frontera y memoria. La escala de acción y los acoplamientos son salidas HMT
recibidas, no valores objetivo utilizados para escoger un operador.

Los propietarios efectivos son:

- `RETROACCION_PCH_Y_RESTRICCIONES_VARIACIONALES.md`, §§2–4: acción conjunta,
  potencial canónico total después de la reducción de segunda clase y
  álgebra de primera clase con la métrica variable.
- `LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md`, §§1–3: identidad Noether–Legendre.
- `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/31_corriente_y_respuesta_cartan.tex`:
  acción, eliminación de contorsión y corriente material conjunta.
- `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex`,
  líneas 7–36 y 61–84: realización cuántica con mapa, dominio y condición
  de cierre declarados. Ese pasaje no calcula el conmutador total.
- `/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/XII_ES/nuclear/09.tex`,
  líneas 98–145: archivo completo isométrico e inversa explícita.

El reconocimiento convencional posterior consiste aquí en el lenguaje de
conexiones y formas simplécticas aplicado al potencial que ya produjo la
acción. Se trabaja en su carta regular, después de las reducciones de
segunda clase, con parámetros de soporte interior o con el borde tratado
por la misma acción. La sección positiva de acción ℏ permanece fija durante
esta variación, como en el antecedente variacional. No se supone una medida
de Liouville infinita ni una cuantización de campos ya completada.

## 2. Cálculo de la curvatura desde la acción total

Sea Θ el potencial canónico TOTAL de la acción conjunta. Incluye la
contribución geométrica, las conexiones y materia y sus términos mixtos
después de reducir las restricciones de segunda clase. Escribamos

\[
 \Omega=-d\Theta,\qquad \iota_{X_f}\Omega=df,
 \qquad \{f,g\}=\Omega(X_f,X_g).
 \tag{1}
\]

Con estas convenciones, X_f(g)=−{f,g} y
[X_f,X_g]=−X_{\{f,g\}}. Por ejemplo, Θ=p dq da
X_f=f_p∂_q−f_q∂_p y {q,p}=1.

En una trivialización de la línea de fase, definimos la conexión construida
del potencial, no de la conclusión buscada:

\[
 \nabla_X=X-\frac{i}{\hbar}\Theta(X),
 \qquad H_X^{\rm can}=-\Theta(X).
 \tag{2}
\]

Su curvatura se calcula para cualesquiera campos X,Y de la carta:

\[
 \begin{aligned}
 \mathcal F^{\rm can}_{X,Y}
 &=XH_Y^{\rm can}-YH_X^{\rm can}-H_{[X,Y]}^{\rm can}
       +\frac{i}{\hbar}[H_X^{\rm can},H_Y^{\rm can}]\\
 &=-X\Theta(Y)+Y\Theta(X)+\Theta([X,Y])\\
 &=-d\Theta(X,Y)=\Omega(X,Y).
 \end{aligned}
 \tag{3}
\]

En la línea de fase los coeficientes H_X son multiplicadores y conmutan.
Las derivadas de los campos y de los coeficientes variables están incluidas
en la fórmula exterior (3); no se congela la métrica para obtenerla.

Sea Σ la superficie regular de las restricciones TOTALES C_a=0.
Por la primera clase del antecedente, {C_a,C_b}=f_ab^c C_c,
con las funciones de estructura métricas conservadas. Para V tangente a Σ,
Ω(X_Ca,V)=dC_a(V)=0. Por tanto los X_Ca son direcciones
características, y las combinaciones suaves X,Y de ellas satisfacen

\[
 \boxed{\left.\mathcal F^{\rm can}_{X,Y}\right|_\Sigma=0.}
 \tag{4}
\]

La dependencia de f_ab^c en el estado no añade una excepción: los términos
C_c X_f se anulan sobre Σ. Para dos restricciones individuales, (3)
fuera de Σ da Ω(X_Ca,X_Cb)={C_a,C_b}=f_ab^c C_c.
Así la reducción a cero procede de la primera clase de la misma acción,
no de declarar plana una conexión arbitraria. Las direcciones incluyen
las deformaciones normales y tangenciales y el calibre recibidos.

Este resultado no congela la gravedad ni elimina la materia: usa Θ total.
Tampoco afirma que Ω sea cero en todas las direcciones del espacio de fases.
Planitud sobre las hojas características no implica, sin un argumento
topológico adicional, trivialidad de toda holonomía global de esas hojas.

## 3. Operadores: lo que preserva la construcción y lo que no identifica

La realización precuántica asociada en la carta es

\[
 Q_{\rm pre}(f)=-i\hbar\nabla_{X_f}+f
 =-i\hbar X_f+f-\Theta(X_f).
 \tag{5}
\]

Usando [∇X,∇Y]=∇[X,Y]+(i/ℏ)Ω(X,Y) y los signos de (1),
se obtiene por expansión

\[
 [Q_{\rm pre}(f),Q_{\rm pre}(g)]
       =i\hbar Q_{\rm pre}(\{f,g\}).
 \tag{6}
\]

Es una identidad de operadores diferenciales sobre secciones suaves en
la carta. No necesita introducir el conmutador deseado como axioma.
Para una función de estructura a y una restricción C,

\[
 Q_{\rm pre}(aC)
 =a Q_{\rm pre}(C)+C\bigl(Q_{\rm pre}(a)-a\bigr).
 \tag{7}
\]

No debe perderse el segundo término antes de restringir a Σ. Una
restricción de la función clásica C a Σ no es lo mismo que imponer
Q(C)ψ=0 sobre un espacio de Hilbert de estados cuánticos.

En particular, ni H_X^can ni Q_pre(C) se identifican por nombre con
el operador interactuante de `HAMILTONIANO_FINITO_HIGGS_FOCK.md` y
`EVOLUCION_ACOPLADA_Y_LIMITE.md`. El primero es el coeficiente de la
conexión de fase; el segundo también contiene la derivación X_C.

Un control concreto de esta distinción es Θ=p dq, f=p²/2:

\[
 Q_{\rm pre}(p^2/2)=-i\hbar p\partial_q-p^2/2.
 \tag{8}
\]

Si ψ depende sólo de q, (8) en general depende de p. Por tanto no
preserva esa polarización por simple restricción; no es el operador
−ℏ²∂_q²/2 sobre funciones de q. Este ejemplo no refuta ningún
operador HMT: impide confundir dos realizaciones distintas al declarar
probado un enunciado sobre una de ellas.

## 4. Archivo completo, transporte y límite

El archivo isométrico con inversa explícita de XII/09 sí permite
transportar una relación operatoria ya probada. Para dos presentaciones
completas V_a:H→M_a, V_b:H→M_b del mismo estado,

\[
 W_{ba}=V_bV_a^*,\qquad W_{cb}W_{ba}=W_{ca},
 \qquad H_b=W_{ba}H_aW_{ba}^*.
 \tag{9}
\]

La última igualdad transporta también el dominio. Los bucles de
presentaciones son exactamente triviales. Esto no identifica como
iguales dos rutas físicas distintas conservadas por el TPK.

Para transportar (4) o (6) a una realización concreta con mapas I y
al límite, debe comprobarse sobre su núcleo común

\[
 \nabla_N^{\rm op} I=I\nabla_N^{\rm can}.
 \tag{10}
\]

Una igualdad de (10) implica R_op I=I R_can, por composición y
resta del corchete, y por tanto anulación en la imagen física declarada.
El teorema de `CURVATURA_TOTAL_MEMORIA_Y_LIMITE.md`, §7, demuestra el
paso al límite cuando las inclusiones efectivas entrelazan esas conexiones
y conservan los núcleos. Ni (9) ni la precisión numérica 729^−n
sustituyen (10) para otro operador no identificado con el transportado.

## 5. Resultado de esta intervención

Se ha calculado y demostrado (4) para la conexión canónica de la acción
total, y (6) para su realización diferencial precuántica. Son resultados
positivos con geometría dinámica y fuente material conjunta. No son una
verificación de la identidad F_total=0 para el Hamiltoniano cuántico
interactuante anterior y su límite espacial–quiral: ese enunciado exige
identificar los operadores en (10). Esta nota no declara inexistente esa
identificación en todo el corpus, ni modifica los PDF, ni certifica un
nuevo archivo Lean.
