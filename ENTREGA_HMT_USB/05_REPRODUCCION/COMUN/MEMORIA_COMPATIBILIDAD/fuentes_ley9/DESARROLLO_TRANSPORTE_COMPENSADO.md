# Transporte compensado, memoria geométrica y contraste energético

Fecha: 22 de septiembre de 2026. Nota exploratoria separada; no modifica ni
certifica los manuscritos de la serie. Autoría de HMT–MD: Rubén. La composición
matricial siguiente es un desarrollo de trabajo a partir de sus realizaciones.

## Base, procedencia y corte causal

Se conserva APP → TRIT → TPK → estado enriquecido. APP reúne las dos hojas
aritméticas con residuo y cociente; TRIT conserva régimen y orientación;
la actualización TPK compone selección, transporte y actualización de memoria.
Las realizaciones matriciales que se utilizan son posteriores a esa construcción.
La holonomía nonádica Γ9 y su memoria no se sustituyen por las matrices de esta nota.

Propietarios activos, bajo
`/Users/ruben/Documents/New project/output/ACTUALIZACION_NUCLEO_SERIE_20260921/ARTICULOS/`:

- `07/ES/source/manuscrito/30c_composicion_corriente_conexion.tex`, sección
  «Representaciones cuadráticas del TRIT»: matrices elíptica, hiperbólica y
  parabólica, y diferencial de transportes invertibles.
- `07/ES/source/manuscrito/30b_variacion_energia_memoria.tex`, ecuación
  `vii:eq:energia-memoria-discreta`: E=⟨Df,W Df⟩, W>0; campos y pesos explícitos.
- `07/ES/source/manuscrito/29_retorno_y_memoria_traslacional.tex`: memoria
  traslacional del retorno observable. Es antecedente distinto del conmutador.
- `02/ES/source/sections/07b_geometria_elipse.tex`: elipse de acción de área h,
  semiejes de producto 2ħ y realización constitutiva LC.
- `03/ES/source/manuscrito/sections/03b_vacancias_prefactor.tex`: polarización
  acotada y corriente centrada de la discrepancia de refinamiento.
- `10/ES/source/nuclear/11.tex`, ecuaciones 28–33: lazo elíptico–parabólico
  H_n, memoria y balance de área orientada.
- `10/ES/source/nuclear/12.tex`, ecuaciones 5.1–5.10 y 6.3–6.6: acoplamiento
  nonádico reversible de dos modos, covarianza y mezcla reducida.

Los regímenes TRIT, el funcional energético y el retorno con memoria son resultados
recuperados. La composición compensada y el protocolo de contraste se reúnen aquí.
La búsqueda focal en II, VII, X y la narración española del 19 de septiembre no
localizó esta identidad exacta reunida; no se afirma prioridad en todo el corpus.
La teoría algebraica de trazas de conmutadores en SL(2) es conocida: véase
[Goldman, Trace Coordinates on Fricke spaces](https://arxiv.org/abs/0901.1404).
No se presenta como un descubrimiento universal de álgebra matricial.

Los parámetros a,b de abajo son parámetros de las realizaciones, no constantes
físicas ajustadas. La tarea termina en este nivel local. Demostrar qué rutas TPK
admiten una realización material de este protocolo y con qué parámetros requiere
componer sus lectores efectivos; no se supone que toda matriz invertible sea una
ruta TPK. Tampoco se identifica el defecto de conmutación con torsión de Cartan
sin la correspondiente conexión y soldadura.

## 1. Una compensación que conserva área sin restaurar el estado

Sean las matrices presentes en el propietario:

\[
J_{\rm e}=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
J_{\rm h}=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Cumplen J_e²=−I, J_h²=I y [J_e,J_h]=2 diag(1,−1). Definimos

\[
R(a)=e^{aJ_{\rm e}},\quad B(b)=e^{bJ_{\rm h}},\quad
C(a,b)=R(a)B(b)R(a)^{-1}B(b)^{-1}.
\]

La convención de acción sobre columnas es de derecha a izquierda. El protocolo
contiene cada transformación y su inversa, pero no las deshace en orden inverso.
Por tanto, no es un retroceso completo del recorrido. Ese retroceso sería, por
ejemplo, R B B⁻¹ R⁻¹=I.

**Proposición.** Para a,b reales:

\[
\det C=1,\qquad \operatorname{tr}C=2+4\sin^2a\sinh^2b.
\]

**Prueba.** Escribamos c=cos a, s=sin a, u=cosh b, v=sinh b. Las matrices son
R=((c,s),(-s,c)), B=((u,v),(v,u)), con c²+s²=1 y u²−v²=1. Todas tienen
determinante uno. La multiplicación da

\[
\begin{aligned}
C_{11}&=u^2+2csuv-(c^2-s^2)v^2,\\
C_{12}&=-2s^2uv-2csv^2,\\
C_{21}&=-2s^2uv+2csv^2,\\
C_{22}&=u^2-2csuv-(c^2-s^2)v^2.
\end{aligned}
\]

Su traza es 2u²−2(c²−s²)v²=2+4s²v². Si sv≠0, supera dos y C es
hiperbólica, con autovalores positivos recíprocos

\[
e^{\lambda},\ e^{-\lambda},\qquad
\lambda=2\operatorname{arsinh}(|\sin a\sinh b|)>0.
\]

Esto se obtiene de cosh λ=tr(C)/2 y cosh(2 arsinh x)=1+2x². Si sv=0,
b=0 o R=±I, y C=I.

La expansión local es C=I+2ab diag(1,−1)+O(|a|²|b|+|a||b|²).
El efecto residual empieza por el producto de las dos operaciones: no aparece
al aplicar cualquiera de ellas sola seguida de su inversa.

### Consecuencia para la elipse de acción

Una matriz real bidimensional con determinante uno conserva la forma de área.
Por tanto C transforma la elipse de acción en otra elipse de la misma área h.
Si Σ es una matriz de covarianza positiva, Σ'=CΣCᵀ cumple detΣ'=detΣ.
La distribución de semiejes y su orientación sí pueden cambiar.

Los autovalores e^{±λ} describen las direcciones propias y la iteración de C.
No son en general sus valores singulares ni los factores de cambio de los
semiejes euclídeos en una sola aplicación. Esta distinción evita identificar
una elongación observada con λ sin reconstruir la métrica de lectura.

**Resultado interpretativo:** la conservación del área de acción puede coexistir
con acumulación de deformación orientada. Se dispone de un observable de memoria
geométrica sin introducir una nueva constante universal. λ depende de a,b.
Ni detC=1 ni la conservación de esa área demuestran energía física constante.

## 2. Medir el residuo con el funcional ya construido

En una fibra de retorno, para campo f y peso hermítico W>0 declarados, aplicar
el lector del corpus:

\[
E_C(f)=\langle (I-C)f,W(I-C)f\rangle.
\]

Si sv≠0, C carece de autovalor uno. Luego E_C(f)>0 para todo f≠0, mientras
el retroceso completo da residuo cero. Se conserva la normalización dimensional
del funcional propietario: no se identifican automáticamente sus números con
julios, calor, masa ni corriente de conducción.

Al invertir realmente el recorrido se invierte C. La traza y λ no distinguen
C de C⁻¹. Para recuperar dirección hace falta observar más que ese escalar:
el vector residual, las componentes de transporte o una sonda con resolución
de fase. Éste es un falsador de una lectura puramente escalar.

Ejemplo racional de control, sin ajuste a datos físicos:

\[
R=\begin{pmatrix}3/5&4/5\\-4/5&3/5\end{pmatrix},\qquad
B=\begin{pmatrix}5/4&3/4\\3/4&5/4\end{pmatrix}.
\]

En él trC=86/25, detC=1 y los autovalores son
(43±6√34)/25. El script adjunto verifica este caso y 169 pares racionales,
incluidos controles nulos, retroceso completo y conservación de detΣ.
Los ensayos finitos no reemplazan la prueba general anterior.

## 2 bis. Composición con el lector de entrelazamiento existente

El artículo X, nuclear/12.tex:300–455, construye para H simpléctico
bidimensional el acoplamiento reversible de dos modos

\[
U_H=\frac19\begin{pmatrix}
8I+H&\sqrt8(H-I)\\
\sqrt8(H-I)&I+8H
\end{pmatrix}.
\]

Con dos gaussianas puras idénticas preparadas desde la elipse de acción, y
transportando conjuntamente la carta inicial, demuestra

\[
\nu(H)^2=1+\frac8{81}\{\operatorname{tr}(HH^{\mathsf T})-2\},
\qquad \operatorname{Tr}\rho_{\rm vis}^2=\nu(H)^{-1}.
\]

Se mantiene esa preparación; no se introduce un Hamiltoniano nuevo. La
transformación completa es reversible y conserva la pureza global.

**Corolario compuesto.** Para C(a,b) de esta nota:

\[
\operatorname{tr}(CC^{\mathsf T})-2
=16\sin^2a\sinh^2b\cosh^2b,
\]
\[
\boxed{\nu_C^2=1+\frac{32}{81}\sin^2a\sinh^2(2b).}
\]

Prueba: escribir las cuatro entradas como d+k, l−m, l+m, d−k, con
d=1+2s²v², k=2csuv, l=−2s²uv, m=2csv². La suma de sus cuadrados es
2(d²+k²+l²+m²)=2+16s²u²v². Se sustituye en el teorema de X.
El ejemplo racional anterior da ν_C²=17/9 y pureza 3/√17.

La cancelación de ħ y de la deformación inicial exige esa preparación y el
transporte conjunto de carta: no es una afirmación para estados arbitrarios.
Un protocolo con sv≠0 produce mezcla reducida; la inversión completa del
acoplamiento puede deshacerla. Mezcla reducida, energía almacenada y calor
constituyen tres lecturas distintas.

### Contraste firmado usando una familia ya construida en el corpus

En X se da H_n=((1+n,n²),(n,n²−n+1)), n entero. Su balance alternante de
memoria depende de n², pero su cociente de determinantes de covarianza es

\[
\mathcal R_n=\frac{\det V_{{\rm vis},n}}{\det V_0}
=1+\frac8{81}n^2(2n^2-2n+5).
\]

La resta, ahora reunida como contraste direccional, elimina todos los términos
pares y da exactamente

\[
\boxed{\mathcal R_{-n}-\mathcal R_n=\frac{32n^3}{81}.}
\]

Para n=±1, las respuestas son 121/81 y 153/81, con purezas 9/11 y 3/√17.
Aquí H_-n no es H_n⁻¹: cambiar el parámetro orientado del lazo no equivale a
deshacer todas las operaciones en orden inverso. Tampoco H_n=H_1^n.
La lectura alternante de área no es automáticamente el observable de Barbero.

El propietario formula la mezcla mediante el conmutador [D,J], con
D=√8(H−I)/9. Si D conmuta con la estructura compleja compatible con el
estado inicial, puede transportar memoria sin mezclar ese producto gaussiano.
Si no conmuta, el teorema determina la mezcla. La ausencia de mezcla de ese
estado no demuestra ausencia de toda disipación material.

La resta anterior es un corolario de resultados existentes, no una nueva
constante universal. La fórmula para C es una composición adicional sobre la
familia de realizaciones admitida por el teorema. Para contrastar un mecanismo
HMT en un material, sus transportes y acoplamientos deben determinarse antes
de medir: programar arbitrariamente esas matrices sólo verifica su emulación.

## 3. Un contraste adicional ya calculable para la vacancia

El propietario III fija δ=log10(10/9), z_n∈{0,1},
P_N=Σ_{n<N}(z_n−δ), |P_b−P_a|<1. En intervalos iguales t0,
I_n=A(z_n−δ), A=u_Q/t0. Para L=b−a:

\[
\frac1{A^2}\sum_{n=a}^{b-1}I_n^2
=L\delta(1-\delta)+(1-2\delta)(P_b-P_a).
\]

La prueba usa z_n²=z_n. Así, el desequilibrio neto queda acotado pero
I_rms/|A|→√(δ(1−δ)). Esta ley admite un contraste sin ajustar una nueva
constante: A es el salto entre los dos niveles de corriente. Se exige la misma
realización temporal y un acoplamiento que no filtre la sucesión sin contabilizarlo.

Un balance firmado nulo no cancela una lectura cuadrática. Si se conecta además
una resistencia ideal R>0 con esta corriente por intervalos, el modelo de
contraste da Q_R=Rt0 ΣI_n². Su aparición es posterior al generador y no un
axioma HMT. Ese modelo permite comprobar, en vez de suponer, una reducción de calor.

## 4. Propuesta experimental, todavía sin realización material certificada

Separar dos cuestiones:

1. **Memoria de orden:** comparar recorridos compensados, recorridos con orden
   intercambiado y retrocesos completos. Medir una respuesta remanente vectorial
   o con resolución de fase. No basta una intensidad o una carga neta.
2. **Recuperación de energía:** medir energía de entrada, energía útil/devuelta,
   variación de almacenamiento y calor, incluyendo preparación y restauración
   del dispositivo. Retorno de fase no autoriza fijar ΔE_almacenada=0.

Para un contraste escalar de un solo puerto, v₂(t)=v₁(T−t) conserva la
distribución de amplitudes y el espectro de potencia. En régimen periódico,
un mismo sistema lineal estacionario predice igual potencia media; una ley
instantánea i=g(v) también da igual integral de vi. Una diferencia reproducible
exploraría dependencia histórica, pero no identificaría por sí sola HMT: deben
compararse histéresis, calentamiento y modelos dinámicos convencionales.
En sistemas de varios puertos se conservan además los espectros cruzados.

El objetivo «transporte con menor disipación» se contrasta a igual transferencia
útil, fidelidad y ritmo. No equivale a energía gratuita ni a electrones que
desaparecen. Una atenuación requiere distinguir energía, amplitud de señal,
población de portadores y carga conservada antes de atribuir una causa gravitatoria.

Antecedente experimental para distinguir almacenamiento, recuperación y pérdidas:
[Defay et al., Enhanced electrocaloric efficiency via energy recovery (2018)](https://doi.org/10.1038/s41467-018-04027-9).
No es evidencia experimental de la composición HMT aquí propuesta.

## Qué se obtuvo y qué no se ha incorporado

Se obtuvo una identidad universal en la familia matricial explícita, un lector
positivo de su residuo, un control de inversión y una ley exacta del segundo
momento de la corriente de vacancias. No se obtuvo una nueva constante universal,
un prototipo de electricidad sin calentamiento ni una demostración de decaimiento
electrónico gravitatorio. La vinculación prospectiva entre los parámetros del
protocolo y un dispositivo debe fijarse antes de recoger sus datos. No se ha
modificado ningún PDF, fuente sellada, claim canónico ni manifiesto de la serie.
