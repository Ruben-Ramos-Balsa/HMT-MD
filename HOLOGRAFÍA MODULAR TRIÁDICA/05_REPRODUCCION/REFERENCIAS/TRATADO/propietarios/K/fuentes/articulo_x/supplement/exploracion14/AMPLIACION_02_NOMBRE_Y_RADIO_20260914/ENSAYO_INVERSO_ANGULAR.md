# Inversión del transporte, corrección angular y ensayo inverso de alfa

14 de septiembre de 2026. Ampliación focal de `LECTURA_TERNARIA_COMPLETA.md`. El objetivo es estudiar la introducción de la salida heredada \(10^4\alpha_A\) como dato de un problema inverso. Tal ensayo determina un operador candidato; se distingue de una derivación de alfa y de una modificación de las fuentes selladas.

## 1. Dominio y antecedentes efectivos

El registro K y las coordenadas \(\pi,\varphi,e,\alpha_A\) se reciben de su producción APP–TRIT–TPK y sus lectores documentados. La evaluación presente empieza después de esa producción, sobre el portador de doce posiciones del registro y sus memorias. Conserva la orientación de los desplazamientos, el modo fijo y sus complementos; no selecciona semillas ni valores generadores a partir del objetivo del ensayo.

En la carta euclídea del registro se mantienen

\[
 U=S^4,\quad U^3=I,\quad
 P_0=(I+U+U^2)/3,\quad P=I-P_0,\quad L=8I-U.
\]

El resultado anterior es \(L^*L=49P_0+73P\). El rango de P0 es cuatro y el de P ocho. Las normas exactas de K, \(P_{11}K\), \(D_3K\), \(D_4T_3K\), \(u=P_3P_{11}K\) y \(P_{10}(K)K\) permanecen como antecedentes, sin recalibración.

Los propietarios consultados para la composición angular son:

- [Coordenadas angulares y reversión de canales](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/iv_angulos_antecedente.tex:1>), archivo completo: A, C*, cambios de carta, canales positivos y distribución sobre las seis parejas.
- [Carácter de acción y continuación regional](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/iv_accion_antecedente.tex:1>), archivo completo: H5, D_A, C_pi y eta_ret.
- [Elipse, fase paramétrica y reciprocidad](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/iv_elipse_radio.tex:1>), archivo completo: razón angular, transporte de métrica, fase polar y matrices recíprocas.
- [Covarianza canónica](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/antecedentes_ii/sections/07c_covarianza_accion.tex:1>), archivo completo: M_eta, reciprocidad y transformación conjunta de covarianza.
- [Inversión de trayectorias](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/tpk_desarrollo_integrado.tex:423>), subsección completa: inversión del orden, orientación y términos conservados.
- [Conjugación incidencial y frontera](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_incidencias.tex:1>), archivo completo: la negación de un canal y la inversión de una ventana no equivalen a negar su bloque entero.

## 2. Qué conservan las inversiones y conjugaciones ya definidas

**Proposición 1.** Sustituir el ciclo U por su inverso conserva la forma de la lectura:

\[
 (8I-U^{-1})^*(8I-U^{-1})
 =65I-8(U+U^{-1})=49P_0+73P.
\]

**Prueba.** U es ortogonal, de modo que U*=U^-1. Al expandir ambos productos aparecen la misma suma \(U+U^{-1}\) y la misma identidad. El proyector fijo tampoco cambia al invertir U. Por tanto, para cada vector fijo v la razón de normas conserva exactamente su valor.

La inversión del orden de las doce posiciones es una matriz ortogonal R con \(RSR^{-1}=S^{-1}\). Así, \(RUR^{-1}=U^{-1}\), y R conserva P0. Una negación global adicional tampoco cambia la norma. La traslación de origen \(S^j\), incluida la antipodal \(S^6\), conmuta con U. Ninguna de estas operaciones modifica el índice 73 ni el peso \(w(v)=\|P_0v\|^2/\|v\|^2\).

**Proposición 2.** Para una carta invertible G, sea

\[
 U'=GUG^{-1},\quad L'=GLG^{-1},\quad
 v'=Gv,\quad g'=G^{-*}G^{-1}.
\]

Entonces

\[
 \frac{\langle L'v',g'L'v'\rangle}{\langle v',g'v'\rangle}
 =\frac{\|Lv\|^2}{\|v\|^2}.
\]

**Prueba.** Sustituir \(L'v'=GLv\) y \(G^*g'G=I\). La identidad vale también para la proyección transportada \(P_0'=GP_0G^{-1}\).

Ésta es la composición pertinente con la reciprocidad y la deformación elíptica ya construidas: el manuscrito transporta conjuntamente estado, operador y forma. En un plano realizado mediante M_eta, la métrica es \(M_\eta^{-T}M_\eta^{-1}\); la semejanza conserva los autovalores del ciclo. Conservar artificialmente el producto euclídeo anterior mientras se cambia G define otro observable, no la misma lectura expresada en otra carta.

La involución de canales \(q_+\leftrightarrow q_-\) conserva A, revierte C* y transporta \(\eta_{\rm el}\mapsto-\eta_{\rm el}\). En su dominio ya definido no añade una fase pequeña al operador S4. La fase polar de una elipse tampoco es su fase espectral: su relación \(\tan\phi=e^{-\eta_{\rm el}}\tan\theta\) es un cambio de parametrización de la curva, no la sustitución del autovalor de un transporte semejante.

La conjugación de incidencias merece una precisión distinta. El propietario da

\[
 z_m^\dagger=z_{\rho(m)}
  +100\mathbf1_{\{c_{\rho(m)}\ne0\}}-20c_{\rho(m)},
 \qquad c_m=[C_m]_{10},
\]

con los términos de frontera antes de la reducción decimal. Esta operación no es en general una isometría del vector de bloques. Aplicarla a K requiere el empalme con su libro de incidencias y sus extremos; no se la reemplaza por una corrección angular inventada. Esta nota no modifica ese libro ni identifica automáticamente todos sus lectores de bloques.

## 3. La corrección regional existente y su escala propia

La composición de los propietarios angular y de acción produce

\[
 A_{\deg}=1000\alpha_A,\qquad
 C^*_{\deg}=2(\eta_{\rm ret}+\alpha_A),\qquad
 \eta_{\rm ret}=H_5-\frac{90}{\pi}\mathcal C_\pi(\alpha_A),
\]

\[
 \mathcal C_\pi(\alpha_A)
 =169\alpha_A^6+
 \frac{D_A\alpha_A^7}{1-D_A\alpha_A},\qquad
 D_A=\exp(-100\pi\alpha_A/9).
\]

Si se distingue la coordenada anterior al retorno \(C^*_{\mathrm{pre},\deg}=2(H_5+\alpha_A)\), se deduce exactamente

\[
 \boxed{\theta_{C,\mathrm{pre}}-\theta_{C,\mathrm{ret}}
 =\frac\pi{180}\,2(H_5-\eta_{\rm ret})
 =\mathcal C_\pi(\alpha_A).}
\]

Es una corrección angular genuinamente compuesta desde las fuentes, con conversión de unidades una sola vez. Su evaluación posterior es aproximadamente

\[
 \mathcal C_\pi(\alpha_A)=2.55207421805\,10^{-11}\ {m rad}.
\]

Los otros ángulos definidos conservan sus escalas y sus dominios:

| Coordenada ya definida | Evaluación aproximada en radianes |
|---|---:|
| theta_A | 0.127362829013 |
| theta_C | 0.0370662264658 |
| theta_C/6, sobre cada pareja antipodal | 0.00617770441097 |
| corrección regional de theta_C | 0.0000000000255207421805 |

No se introdujeron divisores adicionales ni se exploraron combinaciones para acercar estas cantidades al ensayo. Los canales q± son positivos reales de atenuación; su exponente no se convierte automáticamente en una fase unitaria multiplicando por i. La composición examinada produce esas coordenadas de acción, pero no una instrucción que cambie el ciclo U por una rotación del ángulo inverso calculado a continuación.

## 4. Problema inverso de fase: solución explícita y operador completo

Sea \(s_\alpha=10^4\alpha_A\), recibido legítimamente como dato de ensayo. En un sector de fase unitaria,

\[
 |8-e^{i\theta}|^2=65-16\cos\theta.
\]

La solución de orientación positiva próxima al ángulo ternario es

\[
 \boxed{\theta_\alpha=\arccos\frac{65-s_\alpha}{16},\qquad
 \delta_\alpha=\frac{2\pi}{3}-\theta_\alpha.}
\]

La ecuación equivalente, sin restar dos ángulos cercanos, es

\[
 73-s_\alpha
 =8(1-\cos\delta_\alpha+\sqrt3\sin\delta_\alpha).
\]

El intervalo heredado de alfa en la nota anterior da, aproximadamente,

\[
 \delta_\alpha=0.00190956706826\ {m rad}
 =0.109410133709^\circ,\qquad
 \theta_\alpha=119.890589866291^\circ.
\]

La corrección regional de la sección anterior no coincide con esta diferencia de fase: es aproximadamente 7.48·10^7 veces menor. La desigualdad también se obtiene con cotas amplias, \(\delta_\alpha>10^{-3}\) y \(\mathcal C_\pi<10^{-7}\), sin depender de las cifras mostradas.

El ensayo se realiza sobre las doce posiciones, no sólo sobre una matriz de orden dos. Defínase, a partir del mismo U,

\[
 J=\frac{U-U^2}{\sqrt3},\qquad
 J^*=-J,\quad J^2=-P,\quad JP_0=0.
\]

**Proposición 3.** La familia real

\[
 U_\theta=P_0+\cos\theta\,P+\sin\theta\,J
\]

es ortogonal, coincide con U para \(\theta=2\pi/3\), y satisface

\[
 (8I-U_\theta)^*(8I-U_\theta)
 =49P_0+(65-16\cos\theta)P.
\]

**Prueba.** Las relaciones entre P0, P y J anulan los términos cruzados y dan \(U_\theta^*U_\theta=P_0+(\cos^2\theta+\sin^2\theta)P=I\). Expandir la segunda identidad usa \(U_\theta+U_\theta^*=2P_0+2\cos\theta P\). Finalmente, \(U=P_0-P/2+(\sqrt3/2)J\).

Para \(\theta=\theta_\alpha\), el complemento P tiene lectura exactamente s_alpha. Es una solución del problema inverso explícitamente alimentada por s_alpha, no una predicción independiente de ese valor. La orientación inversa \(-\theta_\alpha\) da la misma norma.

La familia conserva la ortogonalidad y permite el acoplamiento con memoria

\[
 T_\theta=(8I+U_\theta)/9,\qquad
 D_\theta=\sqrt8(U_\theta-I)/9,\qquad
 T_\theta^*T_\theta+D_\theta^*D_\theta=I.
\]

En cambio,

\[
 U_\theta^3=P_0+\cos(3\theta)P+\sin(3\theta)J.
\]

La pequeña diferencia no nula delta_alpha rompe \(U_\theta^3=I\). Por ello esta familia no mantiene la representación original del grupo cíclico de orden tres. Tampoco mantiene su determinante original: \(\det(8I-U_\theta)=7^4(65-16\cos\theta)^4\). Su carta real no aporta por sí misma una matriz entera ni el cociente reticular de índice 73. Las hipótesis de la conservación unitaria sobreviven; las del índice entero ternario deben distinguirse.

## 5. Restricción adicional al conservar el sector fijo y el estado

Para cualquiera de los seis objetos v ya utilizados,

\[
 s_\theta(v)=49w(v)+(65-16\cos\theta)(1-w(v)),
\]

de donde

\[
 49\le s_\theta(v)\le81-32w(v).
\]

**Consecuencia operativa.** Alcanzar s_alpha mediante esta familia, manteniendo v y P0, exige

\[
 w(v)\le\frac{81-s_\alpha}{32}
 \simeq0.250827322099.
\]

Las normas exactas anteriores dan \(w>9/32\) para K, \(P_{11}K\), \(D_3K\) y u. Por tanto su máximo es menor que 72, mientras que s_alpha es mayor que 72. Ni siquiera un cambio arbitrario de fase dentro de esta familia unitaria puede producir el objetivo sobre esos cuatro estados.

| Estado conservado | Máximo posible de s_theta, aproximado | Fase inversa requerida, cuando existe |
|---|---:|---:|
| K | 54.1922726227 | fuera del intervalo permitido |
| P11 K | 71.4670172771 | fuera del intervalo permitido |
| D3 K | 69.3474270513 | fuera del intervalo permitido |
| u | 66.8296175021 | fuera del intervalo permitido |
| D4 T3 K | 81 | 119.8905898663 grados |
| P10(K) K | 77.3923674871 | 133.5296853010 grados |

Para la última fila, la solución se obtiene de

\[
 \cos\theta_v=\frac1{16}\left(65-
 \frac{s_\alpha-49w(v)}{1-w(v)}\right).
\]

Éste es nuevamente un diagnóstico inverso. No se cambió el estado ni se eligió una combinación para ajustar alfa. Las fases distintas requeridas muestran que insertar la misma fase reconstruida del sector puro en cualquier vector mixto no produce automáticamente el mismo cociente total.

Los lectores originales de memoria son polinomios en S y conmutan con U_theta. El entrelazamiento con la isometría completa V2 conserva \(s_\theta(V_2v)=s_\theta(v)\). Archivar los complementos en vez de descartarlos no elimina estas restricciones; distribuye su contribución sin alterar el cociente conjunto.

## 6. Alcance y reproducción

La inversión de orientación y el transporte covariante existentes preservan la lectura original. La corrección regional C_pi está compuesta explícitamente y pertenece al contraángulo de acción. La familia U_theta es una formalización nueva del ensayo inverso sobre el portador completo: conserva P0, la orientación elegida y la norma, pero el dato s_alpha selecciona su fase. Para considerarla una realización previa del TPK haría falta identificar una composición ya generada que produzca esa U_theta, su acción sobre el registro, y su relación con la fase ternaria original. Las fuentes focales leídas no contienen esa identificación; esta localización de alcance no declara su ausencia en todo el corpus.

Los cálculos numéricos se realizaron con Decimal a setenta cifras, usando el punto medio del intervalo de alfa heredado únicamente para mostrar aproximaciones. Las series de seno y coseno y una bisección determinaron delta; H5, D_A, C_pi y eta_ret se evaluaron desde las fórmulas escritas. Las fases mostradas a diez decimales son diagnósticas, no certificados de un nuevo límite. Las desigualdades sobre los cuatro estados imposibles se comprueban exactamente mediante el signo en Q(sqrt5) de sus pesos anteriores.

No se ha modificado la nota ternaria previa, ninguna fuente sellada ni ningún PDF. La genealogía de alfa conserva su dirección original; sólo el ensayo inverso usa su salida como argumento declarado.
