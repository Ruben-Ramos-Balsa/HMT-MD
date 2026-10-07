# Acción, memoria reducida y trabajo recuperable

22 de septiembre de 2026. Desarrollo exploratorio separado. No modifica los
artículos ni sus certificados. Autor de HMT–MD: Rubén. Los resultados siguientes
son consecuencias de las hipótesis y realizaciones indicadas; no constituyen
todavía una predicción validada en un dispositivo ni una entrega editorial sellada.
El control global de continuidad conserva la discrepancia editorial de AGENTS.md;
este borrador no declara haber superado esa puerta ni la sustituye por álgebra local.

## 1. Procedencia y composición concreta

La construcción de partida del corpus es APP → TRIT → TPK → estado enriquecido.
Se reciben sus salidas de acción y los transportes de memoria en sus realizaciones
posteriores. No se modifica el generador ni se introducen constantes metrológicas
para seleccionar sus estados. La composición aquí examinada termina en la
realización gaussiana y energética declarada, no en un teorema sobre todo material.

Propietarios, bajo
`/Users/ruben/Documents/New project/output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/`:

- `10/ES/source/nuclear/12.tex:20–41`: ecuación de las secciones de acción.
- `02/ES/source/sections/07b_geometria_elipse.tex:79–114`: ley areal.
- El mismo archivo, `:209–252`: realización inductiva–capacitiva y energía.
- `10/ES/source/nuclear/12.tex:305–498`: acoplamiento nonádico reversible,
  preparación gaussiana, covarianza, pureza y espectro.
- El mismo archivo, `:500–527`: lector térmico y razón de temperaturas.
- `DESARROLLO_TRANSPORTE_COMPENSADO.md`, contiguo: composición compensada,
  contraste direccional y su prueba. Se conserva íntegramente.

La búsqueda focal en los propietarios II, V, VII y X no localizó una exposición
reunida de las identidades energía–pureza y del balance de trabajo que se desarrollan
a continuación. Esto no acredita prioridad sobre todo el corpus ni sobre la literatura.
La pasividad y la ergotropía son conceptos establecidos. La aportación de esta nota
es componerlos con el acoplamiento específico y la realización energética ya escritos.

## 2. Qué significa incorporar la ecuación de Planck

En la notación del propietario:

\[
H_5=\frac12\sqrt{\frac{1000\alpha}{\varphi}}-\alpha
+\frac9{16}\alpha^2-\frac59\alpha^3
+\frac7{48}\alpha^4-\frac1{54}\alpha^5,
\]
\[
D_A=e^{-100\pi\alpha/9},\qquad
\mathcal C_\pi=169\alpha^6+\frac{D_A\alpha^7}{1-D_A\alpha},
\]
\[
\hbar_{\rm pre}=\mathcal A_0H_5,\qquad
\hbar_{\rm ret}=\mathcal A_0\left(H_5-\frac{90}{\pi}\mathcal C_\pi\right),
\qquad h_s=2\pi\hbar_s.
\]

La escala dimensional del texto es \(\mathcal A_0=10^{-34}\mathcal U_S\).
Su década y la carta dimensional tienen antecedentes distintos. Se mantienen
explícitos: la fórmula no es una igualdad entre una magnitud dimensional y un
número sin unidad. Tampoco depende únicamente de α: conserva las coordenadas
π y φ, la orientación y la escala del lector de acción.

Para una sección positiva fija, abreviemos \(\hbar=\hbar_s\). La elipse del
corpus tiene semiejes \(\sqrt{2\hbar}e^{\eta/2}\) y
\(\sqrt{2\hbar}e^{-\eta/2}\), donde \(\eta=\operatorname{artanh}(C^*/A)\).
Su área orientada satisface

\[
\mathcal A(\theta)=\hbar\theta,\qquad \mathcal A(2\pi)=h.
\]

En la realización LC, ya construida con reloj ω e impedancia de referencia,

\[
\mathcal H_\eta(Q,P)=\frac\omega2(e^{-\eta}Q^2+e^\eta P^2).
\]

Sobre esa órbita, \(\mathcal H_\eta=\hbar\omega=hf\), con
\(f=\omega/(2\pi)\). La convención hamiltoniana del propietario da
\(\dot\theta=-\omega\); por ello \(d\mathcal A/dt=-\hbar\omega\).
La energía positiva coincide con la magnitud de esa velocidad areal en esta
realización y sección fija. No se identifica esta área acumulada con la acción
lagrangiana de una trayectoria arbitraria.

Interpretación: la ecuación interna determina la escala de acción por unidad de
fase; el reloj determina su ritmo. La deformación de la elipse y el orden del
transporte conservan información adicional que no queda fijada por hf.
La covarianza gaussiana utilizada después es una preparación cuántica distinta
de un punto sobre la órbita clásica: su energía inicial es hf/2, no hf.

## 3. Hipótesis del resultado energético

Se preparan dos modos gaussianos puros, centrados e idénticos, cada uno con

\[
V_0=\frac\hbar2MM^{\mathsf T},\qquad
M=\operatorname{diag}(e^{\eta/2},e^{-\eta/2}).
\]

Actúa el acoplamiento ya presente en X:

\[
U_H=\frac19\begin{pmatrix}
8I+H&\sqrt8(H-I)\\
\sqrt8(H-I)&I+8H
\end{pmatrix},\qquad H\in\operatorname{Sp}(2,\mathbb R),
\]

transportado a la carta inicial mediante M⊕M. El estado conjunto permanece puro.
Los dos lectores energéticos finales tienen igual frecuencia ω, conservan la
métrica inicial \(G_\eta=M^{-\mathsf T}M^{-1}\), y no incluyen una energía de
interacción residual entre modos. Las operaciones de extracción comienzan y
terminan con esos mismos lectores. La accesibilidad física de todas las operaciones
permitidas es una hipótesis de la cota de trabajo, no un resultado de fabricación.

Pongamos

\[
\tau=\operatorname{tr}(HH^{\mathsf T})-2\geq0,\qquad
W_v=\frac{8I+HH^{\mathsf T}}9,\qquad
W_m=\frac{I+8HH^{\mathsf T}}9.
\]

Entonces \(V_j=(\hbar/2)MW_jM^{\mathsf T}\). Denotamos por
\(\mu=\operatorname{Tr}\rho_v^2\) la pureza visible y por
\(\nu=\mu^{-1}\) su valor simpléctico normalizado. No se usa ν para la
frecuencia, que se escribe f o ω.

## 4. Identidad energía–pureza

**Proposición.** Con las hipótesis anteriores, si ΔE_v es la energía visible por
encima del estado inicial, entonces

\[
\frac{\Delta E_v}{hf}=\frac\tau{36},\qquad
\nu^2=1+\frac{8\tau}{81},\qquad
\boxed{\mu^{-2}-1=\frac{32}{9}\frac{\Delta E_v}{hf}.}
\]

**Prueba.** Para un estado centrado y el lector cuadrático fijado,
\(E_v=(\omega/2)\operatorname{tr}(G_\eta V_v)
=(\hbar\omega/4)\operatorname{tr}W_v\).
Como \(\operatorname{tr}W_v=2+\tau/9\), restar la energía inicial
\(\hbar\omega/2\) da la primera igualdad. El teorema del corpus da
\(\det W_v=1+8\tau/81\) y \(\mu=(\det W_v)^{-1/2}\).
Eliminar τ produce la igualdad encuadrada. La prueba no requiere que H sea
simétrica ni que sus valores propios coincidan con sus valores singulares.

La ley elimina los parámetros particulares del recorrido. El coeficiente 32/9
queda determinado por el reparto del acoplamiento, no por un ajuste posterior
a energía y pureza. La escala h se conserva hasta la normalización.

**Control de especificidad.** Para \(W_p=pI+(1-p)HH^{\mathsf T}\),
\(0<p<1\), se obtiene en cambio

\[
\mu^{-2}-1=4p\frac{\Delta E}{hf}.
\]

La elección del corpus es p=8/9. Por tanto un contraste puede estimar
\(p_{\rm obs}=(\mu^{-2}-1)/(4\Delta E/(hf))\) y compararlo con 8/9,
si ΔE>0, sin ajustar p a los mismos datos. Programar un mezclador con ese
valor comprobaría la emulación, no el origen natural de ese reparto en HMT.

La identidad no es universal para cualquier gaussiana: desplazamientos coherentes
añaden energía sin cambiar la pureza; ruido térmico inicial y métricas distintas
cambian la relación. Estos son falsadores de una extensión indebida, no excepciones
que se deban ocultar en el ajuste.

W_v es una combinación convexa de matrices de covarianza producida por la reducción
de un estado gaussiano conjunto. No se sustituye ese estado por una mezcla
probabilística de dos estados puros: esa mezcla sería, en general, no gaussiana y
su pureza no vendría dada por el determinante de la covarianza.

## 5. Trabajo recuperable y restricción local

La ergotropía es el máximo descenso de la energía del estado mediante operaciones
unitarias cíclicas con el lector energético fijo. No incluye automáticamente el
coste neto de construir, preparar o controlar un aparato.

El espectro gaussiano del corpus tiene poblaciones

\[
\lambda_j=(1-r)r^j,\qquad r=\frac{\nu-1}{\nu+1}.
\]

Están ordenadas decrecientemente con la energía del oscilador. El estado pasivo
tiene por ello energía \(E_{v,\rm pas}=hf\nu/2\). Se alcanza por una operación
gaussiana: \(S=\sqrt\nu\,W_v^{-1/2}\) tiene determinante uno y
\(SW_vS^{\mathsf T}=\nu I\). El orden de las poblaciones demuestra además
que es mínimo entre todas las unitarias, no sólo entre las gaussianas.

En consecuencia,

\[
\boxed{\frac{\mathcal W_v}{hf}
=\frac{(\nu-1)(9\nu-7)}{32},\qquad
\frac{E_{v,\rm pas}-hf/2}{hf}=\frac{\nu-1}{2}.}
\]

Estas dos cantidades suman
\(\Delta E_v/(hf)=9(\nu^2-1)/32\).
El término pasivo es energía inaccesible bajo las operaciones locales declaradas;
no se le atribuye por ello un flujo de calor ya realizado.

### Acceso conjunto a la memoria

El segundo modo satisface \(\det W_m=\det W_v=\nu^2\) y
\(\Delta E_m=8\Delta E_v\). Así,

\[
\Delta E_{\rm tot}=9\Delta E_v=hf\frac\tau4.
\]

Con operaciones conjuntas, la inversión del acoplamiento restaura el producto
inicial. Como el estado total es puro y el producto inicial es el estado
fundamental del lector conjunto, se puede recuperar idealmente todo ΔE_tot.
Las operaciones locales independientes dejan dos estados pasivos de energía
hfν/2 cada uno. Por tanto,

\[
\boxed{\mathcal W_{\rm conjunta}-\mathcal W_{\rm local}
=hf(\nu-1)=hf(\mu^{-1}-1).}
\]

Se ha cuantificado el trabajo adicional habilitado por acceso conjunto a las
correlaciones. La preparación inicial requirió aportar energía: esta identidad
no produce una ganancia neta de un ciclo completo ni una fuente de energía gratuita.
Tampoco dice que la información sea idéntica a la energía como magnitud física.
«Local» significa aquí unitarias de producto U_v⊗U_m; no incluye mediciones,
comunicación clásica ni realimentación. El incremento no es una energía de
interacción residual: procede de la restricción operativa sobre el estado
correlacionado y de sus espectros marginales. El cociente 1:8 corresponde a las
energías sobre el vacío, no a las energías totales ni a las ergotropías.

## 6. Casos exactos y conservación del desarrollo anterior

Para el lazo del corpus

\[
H_n=\begin{pmatrix}1+n&n^2\\n&n^2-n+1\end{pmatrix},\qquad
\tau_n=n^2(2n^2-2n+5),
\]

el caso n=1 da

\[
\nu=11/9,\quad\mu=9/11,\quad
\Delta E_v=\frac5{36}hf,\quad
\mathcal W_v=\frac1{36}hf,\quad
E_{v,\rm pas}-hf/2=\frac19hf.
\]

El conjunto tiene ΔE_tot=5hf/4, trabajo local 37hf/36 y ventaja conjunta 2hf/9.
El caso n=−1 tiene los mismos valores propios de H, pero τ=9:

\[
\nu=\sqrt{17}/3,\qquad \Delta E_v=hf/4,\qquad
\mathcal W_v=\frac{9-2\sqrt{17}}{12}hf.
\]

La energía añadida visible difiere en razón 9/5 con frecuencia y sección de
acción iguales. Cambiar n por −n no invierte por completo el recorrido:
\(H_{-n}\ne H_n^{-1}\). La inversión matricial verdadera conserva τ en
dimensión dos. Por tanto no se atribuye a una reversión temporal completa la
asimetría de esta familia.

Para el transporte compensado de la nota anterior,
\(C(a,b)=R(a)B(b)R(a)^{-1}B(b)^{-1}\), ya se probó
\(\tau_C=4\sin^2a\sinh^2(2b)\). La composición energética da ahora

\[
\boxed{\Delta E_v(C)=\frac{hf}{9}\sin^2a\sinh^2(2b),}
\]
\[
\mathcal W_{\rm conjunta}-\mathcal W_{\rm local}
=hf\left(\sqrt{1+\frac{32}{81}\sin^2a\sinh^2(2b)}-1\right).
\]

La conexión con Planck permanece explícita: en la sección pre,
hf=2π A0 H5(α,φ)f; en la sección ret se sustituye H5 por η_ret.
No se ha supuesto una variación experimental de α ni una alternancia libre
entre secciones dimensionales.

## 7. Boltzmann y lectura térmica: composición, no omisión

Para ν>1, el estado pasivo tiene temperatura equivalente

\[
k_BT_{\rm pas}=\frac{hf}{\log[(\nu+1)/(\nu-1)]}.
\]

Al usar el mismo reloj que el transductor del corpus,
\(hf=k_B\Theta_{\rm clk}\log3\), queda

\[
\frac{T_{\rm pas}}{\Theta_{\rm clk}}
=\frac{\log3}{\log[(\nu+1)/(\nu-1)]}.
\]

Para n=1 se recupera exactamente log3/log10, resultado ya escrito en X.
La entropía es la del espectro gaussiano, con ocupación (ν−1)/2. La nueva
composición energética mantiene ese resultado y no le atribuye novedad.
La temperatura equivalente del estado pasivo no implica que el estado inicial
reducido ya estuviese en equilibrio térmico ni que se haya disipado calor.

## 8. Contraste y alcance de la novedad

La literatura ya relaciona coherencia, correlaciones y extracción de trabajo.
El objetivo específico no es reclamar esa relación general, sino contrastar la
ley conjunta de este transporte: coeficiente 32/9, reparto energético 1:8,
familia orientada H_n, escala de acción y diferencia entre acceso local y conjunto.

Dos niveles experimentales permanecen separados:

1. Emulación: realizar U_H y comprobar las identidades. Verifica una realización
   del modelo, no la tesis de que cualquier material tenga ese acoplamiento.
2. Predicción física: determinar prospectivamente desde la construcción qué
   dispositivo, grados de libertad, frecuencia, preparación y acoplamiento
   realizan esos objetos, sin ajustar 8/9 a los datos de la prueba. Medir energía,
   covarianza, pureza, costes de control y energía de restauración por separado.

La temperatura o la pureza no deben inferirse usando la misma ley que se quiere
comprobar si se pretende un contraste independiente. Un trabajo recuperado se
compara con un balance que incluya preparación, controles y memoria restaurada.

Referencias externas de contraste, posteriores a esta composición del corpus:

- Kua, Serafini y Genoni, *Daemonic ergotropy of Gaussian quantum states and the
  role of measurement-induced purification via general-dyne detection*,
  https://arxiv.org/abs/2506.22288. Fórmulas generales de energía, pureza y pasividad;
  no es una validación del acoplamiento HMT ni de sus constantes.
- *Experimental Extraction of Coherent Ergotropy and Its Energetic Cost in a
  Superconducting Qubit*, https://arxiv.org/abs/2506.16881.
- Hou et al., *Combining energy efficiency and quantum advantage in cyclic
  machines*, https://doi.org/10.1038/s41467-025-60179-5. Experimento con control
  coherente entre ciclos. No mide el presente transporte nonádico.

Resultado de trabajo: composición algebraica con estructura de partida explícita.
No se declara una nueva constante universal, una ventaja experimental observada,
una violación de la termodinámica ni un mecanismo validado de electricidad sin calor.
