# Ampliación justificativa del inventario: incidencia, acción y recuperación

19 de septiembre de 2026. Sucesor aditivo de REV04. El adjunto autoral se conserva íntegro en `ADJUNTO_INTEGRO_CKM_20260919.md`, incluidos sus enlaces y conclusiones. Este documento distingue la recuperación de contenido anterior de las consecuencias algebraicas reunidas durante la revisión. No modifica los PDF entregados.

## 1. Alcance y residencia genealógica

El ejemplo recibido se incorpora a la jerarquía existente, cuyo origen permanece en APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del continuo. Las coordenadas regionales de π, φ y e, el registro dodecafásico y las dos determinaciones de α tienen sus productores en los inventarios anteriores. Aquí se despliegan operaciones posteriores que utilizan esas salidas, sin convertir una entrada local de un módulo en un dato externo a la construcción.

El carácter conjunto de la generación no exige evaluar todas las coordenadas a la vez. La exposición conserva el orden efectivo de producción, selección, transporte, lectura y recuperación. Las cinco construcciones del continuo permanecen aspectos correlativos del mismo desarrollo; las divisiones editoriales de los consumidores físicos no las sustituyen por cinco dominios independientes.

Antecedentes inmediatos:

- [Microinventario de K y enlaces](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV04_RELECTURA_Y_JERARQUIA/31_MICROINVENTARIO_K_Y_ENLACES.md>).
- [Jerarquía causal y realizaciones, JC-015–JC-024](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV04_RELECTURA_Y_JERARQUIA/33_JERARQUIA_CAUSAL_Y_REALIZACIONES.md>).
- [Contrato de completitud](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV04_RELECTURA_Y_JERARQUIA/34_INTEGRACION_Y_CONTRATO_DE_COMPLETITUD.md>).

## 2. DJ-01. Normalización orbital del autocruce pentagonal

**Antecedente:** JC-015. **Estatuto:** RESULTADO_RECUPERADO. La arquitectura autoral del semicuadrado precede a su formalización mediante el grupoide de pares; esa formalización ya está escrita en la fuente consultada.

La identidad `25/2 = 5²/2` no agota la explicación del coeficiente. Deben incluirse individualmente:

1. La producción y selección del soporte pentagonal P en la incidencia anterior.
2. La construcción de P × P como pares ordenados.
3. La involución concreta j(x,y) = (y,x).
4. La separación entre pares diagonales y pares no diagonales.
5. Las cinco órbitas fijas y sus estabilizadores de orden dos.
6. Las diez órbitas libres y sus estabilizadores triviales.
7. El peso orbital 1/|Stab| y su justificación por órbita–estabilizador.
8. La evaluación 10 + 5/2 = 25/2.
9. El cardinal ordinario de órbitas, 15, distinto de la medida orbital.
10. La asignación al canal 23 y su signo, que pertenecen a las reglas sectoriales completas.

La normalización se deriva de la acción sobre el soporte. La elección de la función angular conserva su propia regla; ni el número 5 ni el conteo de órbitas aislado reemplazan el sistema sectorial.

**Propietario:** [Incidencia marcada y normalización bidireccional](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_ARGUMENTAL_APERTURAS_CIERRES_20260915/II/manuscript_es/sections/08g_normalizacion_bidireccional.tex:28>).

**Destino:** demostración contigua al sistema sectorial CKM; ejemplo explicativo completo en el documento 36. La nomenclatura de grupoides se introduce después de construir pares, inversión y pesos, para que el nombre no sustituya el mecanismo.

## 3. DJ-02. Composición CKM desde las coordenadas generadas

**Antecedentes:** JC-016 y JC-017. **Estatuto:** RESULTADO_RECUPERADO. Se actualiza el pendiente de lectura del adaptador común: su fuente ha sido abierta y cotejada. No se ha recompilado durante esta revisión.

El adaptador recibe las salidas de la base seleccionada del artículo I y de la acción del artículo II. Define las coordenadas

\[
x=(a,u,d)=\left(1000\alpha,\frac{2(\eta_{\rm ret}+\alpha)}6,
\frac{180}{\pi}\Delta_{\rm regional}\right),
\]

donde la torsión regional completa no se sustituye por la corrección de vacancia. La carta sectorial actúa mediante

\[
\theta=Mx,\qquad
M=\begin{pmatrix}2&-5&28\\0&7&-25/2\\1&-20&-2/3\end{pmatrix}.
\]

Se conservarán como pasos distintos:

1. La producción de los datos de incidencia y la posición orientada del pivote.
2. La acción del sistema sectorial sobre una terna de coordenadas.
3. Su evaluación como matriz M.
4. La independencia de esa evaluación respecto de todo marco admitido por la definición correspondiente.
5. La recuperación de x desde θ.
6. La sustitución efectiva de las coordenadas generadas en el adaptador.
7. Las cotas del dominio angular, obtenidas allí desde `SelectedAction.action_domain`.
8. La conversión a radianes con la coordenada π generada.
9. La matriz unitaria, su invariante de Jarlskog y sus condiciones de positividad.
10. El transporte espectral, con las entradas del espectro que realmente utiliza.

La dependencia de la fase es especialmente informativa:

\[
\delta=9a,\qquad
3857\delta=9(1528\theta_{12}+3380\theta_{23}+801\theta_{13}).
\]

La prueba de la segunda igualdad consiste en la identidad exacta

\[
(1528,3380,801)M=(3857,0,0).
\]

Se obtiene así una relación verificable entre cuatro salidas angulares de una misma carta. No requiere introducir una fase CP medida. El adaptador ya contiene `phase_check`; esta revisión recupera su contenido para que aparezca en la exposición.

**Propietarios:** [Adaptador efectivo, coordenadas y recuperación](</Users/ruben/Documents/ChatGPT/jueces y controles/CIERRE_II_III_DESDE_BASE_20260918/article_ii/ArticleIICKMFromSharedBase.lean:47>), [marcos de incidencia y evaluación](</Users/ruben/Documents/New project/output/PAQUETE_ARTICULO_I_CADENA_EXCEPCIONAL_20260919/lean/biblioteca/SectorIncidenceData.lean:85>).

**Precisión de alcance:** la independencia del marco es la igualdad para todo marco admitido por el sistema definido. La identidad de transporte de espectros no convierte unos espectros arbitrarios en una nueva derivación de masas quark ni de PMNS. Esta precisión conserva el resultado completo de CKM sin atribuirle otro enunciado.

## 4. DJ-03. Recuperación sectorial mediante área y lector ponderado

**Antecedentes:** JC-020–JC-022. **Estatuto:** RESULTADO_RECUPERADO.

La construcción contiene dos ocupaciones N₉₀ y N₁₂₀. Sus lectores son

\[
N=N_{90}+N_{120},\qquad D=90N_{90}+120N_{120}.
\]

La inversión exacta es

\[
N_{90}=4N-D/30,\qquad N_{120}=D/30-3N.
\]

El texto deberá conservar los siguientes pasos atómicos:

1. Los sectores del calendario y sus espacios de ocupación.
2. El operador local con autovalores 0, 1 y 2.
3. Las sumas sectoriales, sus multiplicidades y cotas.
4. El carácter angular que determina a₀.
5. La escala positiva γa₀ℓ²P y la lectura areal A = γa₀ℓ²P N.
6. El segundo lector D y su origen espectral.
7. El determinante 30 de la transformación (N₉₀,N₁₂₀) ↦ (N,D).
8. La inversión y la condición D ∈ 30ℤ.
9. Las desigualdades 90N ≤ D ≤ 120N.
10. Las cotas individuales 0 ≤ N₉₀,N₁₂₀ ≤ 36 del modelo de 18 enlaces por sector.
11. El acceso a D desde el Hamiltoniano modular K_A = cI + Δ_mod D, que exige Δ_mod ≠ 0 y normalización conocida.
12. La distinción entre recuperar las dos ocupaciones y recuperar la configuración microscópica completa.

Un ejemplo concreto revela la utilidad: las ocupaciones (1,0) y (0,1) tienen el mismo N y, por tanto, la misma lectura areal en esa escala. El segundo lector da 90 y 120, respectivamente. La pareja de lecturas recupera qué sector estaba ocupado. Esa es una afirmación exacta de recuperabilidad, más informativa que una mención general a la conservación de información.

**Propietario:** [Carácter angular, área y recuperación](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_ARGUMENTAL_APERTURAS_CIERRES_20260915/II/manuscript_es/sections/09_area.tex:144>).

## 5. DJ-04. Fluctuaciones, inversión y áreas complementarias

**Antecedente:** DJ-03. **Estatuto:** RESULTADO_RECUPERADO.

Para la familia finita de estados reducidos de la fuente, la derivación de la función de partición da

\[
\frac{d\langle D\rangle_\Delta}{d\Delta}=-\operatorname{Var}_\Delta(D),
\qquad
\frac{ds}{d\Delta}=-\Delta\operatorname{Var}_\Delta(D).
\]

El inventario deberá incluir la normalización de la familia, su producto de factores, las multiplicidades 18 + 18, las varianzas sectoriales y la cancelación de los términos de primera derivada en la entropía.

La inversión de cada ocupación local n ↦ 2−n produce

\[
\mathcal RN\mathcal R^*=72I-N,\qquad
\mathcal RD\mathcal R^*=7560I-D,
\]

y de la conjugación de los estados se siguen

\[
s(-\Delta)=s(\Delta),\qquad
\langle A\rangle_{-\Delta}+\langle A\rangle_\Delta
=72\gamma a_0\ell_P^2.
\]

Se incorporarán la prueba de conjugación, el caso uniforme Δ=0 y los límites orientados. La conservación entrópica, el área complementaria y la inversión microscópica son tres afirmaciones relacionadas, con pruebas diferenciadas. Las unidades mediante k_B y ℓ²P se exponen después de los lectores adimensionales correspondientes.

**Propietario:** [Respuesta sectorial e inversión de ocupaciones](</Users/ruben/Documents/ChatGPT/jueces y controles/REVISION_ARGUMENTAL_APERTURAS_CIERRES_20260915/II/manuscript_es/sections/09c_entropia_sectorial.tex:113>).

## 6. DJ-05. Recuperación diferencial de la respuesta constitutiva

**Antecedentes:** JC-018–JC-021. **Estatuto:** FORMALIZACION_REUNIDA de una consecuencia algebraica del lector; la procedencia de esta exposición diferencial, anterior al adjunto, no se declara agotada.

La fuente construye T sobre dos hojas y después

\[
\mathcal V=(I-T^{90})(I-T^{120})^{-1},\qquad
f(s)=\frac{1+s+s^2}{1+s+s^2+s^3}.
\]

Su derivada es negativa en (0,1), por lo que f posee la inversa declarada entre (0,1) y (3/4,1). La inversión cúbica y la recuperación de los canales ya están demostradas en el propietario.

Para expresar la sensibilidad de las lecturas, sea

\[
g(t)=\log f(e^{-30t}),\quad \sigma(t)=g'(t)>0\quad(t>0).
\]

La positividad resulta de f>0, f′<0 y (e⁻³⁰ᵗ)′<0. En x>|y| definimos

\[
B=g(x-y)-g(x+y),\qquad V=-g(x-y)-g(x+y).
\]

Escribiendo a=σ(x−y)>0 y b=σ(x+y)>0, la regla de la cadena da

\[
\frac{\partial(B,V)}{\partial(x,y)}
=\begin{pmatrix}a-b&-a-b\\-a-b&a-b\end{pmatrix},
\qquad \det=-4ab<0.
\]

Por tanto, estas coordenadas conservan localmente las dos variables angulares y satisfacen Bₓ=Vᵧ y Bᵧ=Vₓ. El resultado complementa el inversor global ya construido; no reemplaza su prueba. Las derivadas se toman respecto de coordenadas de la respuesta. Una ley de evolución en el espacio-tiempo requeriría además la dinámica y el acoplamiento que corresponda, y no se introduce por cambiar el nombre de estas derivadas.

**Propietario del lector e inversor:** [Operador constitutivo y reconstrucción de canales](</Users/ruben/Documents/New project/output/REPARACION_ENTREGA_MULTIPLATAFORMA_20260916/ENTREGA/ES/PAQUETES/03_VACIO_ELECTROMAGNETICO_ES/payload/spanish_source/manuscrito/sections/04_respuesta_constitutiva.tex:54>).

## 7. DJ-06. Memoria afín de la vuelta observable completa

**Antecedentes:** JC-023 y JC-024. **Estatuto:** RESULTADO_RECUPERADO.

El calendario distingue retorno posicional, retorno orientacional y retorno de fase. El registro de un bloque de 27 transiciones tiene incremento (1,18); cuatro bloques dan (4,72). La representación afín utiliza un elemento R₄ de orden cuatro, un vector u fijado por su acción vectorial y una escala ℓ₀ con procedencia dimensional:

\[
\rho(\gamma)=(R_4^{c_g(\gamma)},\ell_0c_s(\gamma)u).
\]

La composición semidirecta y la aditividad del cociclo prueban

\[
\rho(\gamma_{108})=(I,72\ell_0u),\qquad
\rho(\gamma_{108}^{N})=(I,72N\ell_0u).
\]

El retorno de la parte rotacional y la acumulación traslacional aparecen juntos en una misma fórmula. La exposición deberá mostrar la ley (R,a)(S,b)=(RS,a+Rb), el uso de R₄u=u, la inversión y la repetición. La longitud de ruta 72ℓ₀ conserva su tipo; la curvatura local y la densidad gravitatoria pertenecen a la realización posterior.

**Propietario:** [Cociclo y representación afín del retorno](</Users/ruben/Documents/New project/output/REPARACION_ENTREGA_MULTIPLATAFORMA_20260916/ENTREGA/ES/PAQUETES/02_BARBERO_CKM_CONSTANTES_ES/payload/manuscript_es/sections/gravedad_memoria_afin.tex:67>).

## 8. Contenido que se mejora sin duplicarlo como resultado nuevo

La expansión completa de H₅, la corrección de retorno η, la escala de acción y la factorización constitutiva de Barbero–Immirzi ya están sustancialmente registradas en REV04. Su desarrollo debe conservar todos los grados, coeficientes, escalas y consumidores. El ejemplo recibido se utiliza para mejorar la explicación de esas dependencias, no para anunciar nuevamente su descubrimiento.

N42 se conserva como antecedente de reconstrucción sectorial con el estatuto que declara su propio texto. Las fuentes posteriores de normalización orbital, sistema sectorial y adaptador efectivo se consultan conjuntamente; la nota histórica no sustituye los desarrollos posteriores ni estos borran su procedencia.

## 9. Incorporaciones editoriales y estados efectivos

- DJ-01 → prueba del coeficiente y ejemplo de normalización en CKM.
- DJ-02 → composición de coordenadas y relación CP; el adaptador está leído, no recompilado en este turno.
- DJ-03 → demostración y ejemplo de recuperación sectorial en área/información.
- DJ-04 → subsección propia de fluctuaciones e inversión, con unidades posteriores.
- DJ-05 → consecuencia diferencial del lector constitutivo, separada de una dinámica temporal.
- DJ-06 → ejemplo de retorno con memoria en la realización afín.

Todos quedan incorporados al inventario sucesor. Su presencia material en los PDF anteriores no se altera ni se da por actualizada. Los compromisos P01–P10 permanecen en vigor.
