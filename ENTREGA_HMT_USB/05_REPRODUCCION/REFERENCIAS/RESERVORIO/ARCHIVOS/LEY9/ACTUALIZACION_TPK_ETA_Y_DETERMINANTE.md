# Actualización TPK, memoria publicada y determinantes dodecafásicos

## Alcance y procedencia

La precisión autoral de Rubén es vinculante para esta construcción: **el incremento \(\eta\) sale de la actualización TPK**. No se incorpora como fuerza, coeficiente o dato libre que se elija para satisfacer un balance. Esta nota explicita esa salida en el lector de eventos dodecafásicos ya definido por U016 y enlaza sus operadores de fase con el lector de vacío y con una familia de momentos.

El punto de corte es una publicación del estado generado por APP–TRIT–TPK. Las direcciones, hojas, acarreo y rutas son anteriores al recuento; el vector contado no sustituye el registro enriquecido ni su genealogía. La conexión nonádica conjunta y las cinco construcciones inseparables del continuo no se reemplazan por este espacio de doce coordenadas.

- **RESULTADO_RECUPERADO:** partición en doce ventanas, signo y conteo de U016; proyectores cíclicos que publican \(-1/12\); cociente de canales \(90/120\).
- **FORMALIZACION_NUEVA:** escritura incremental del conteo en un marco móvil, balance exacto y representación determinantal conjunta. La prioridad de estas formulaciones dentro de todo el corpus no se declara comprobada.
- **CERTIFICADO_NUEVO:** verificación racional de las identidades matriciales completas, no campaña de decimales.

Fuentes y cruces:

1. [U016: ventanas y evento firmado](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex:27>), especialmente la ecuación etiquetada `eq:evento-firmado-ventana` en la fuente.
2. [Realización de \(-1/12\) por proyectores](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/base_83/c27_body.tex:245>).
3. [Completación tres–cuatro del vacío](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/integracion_83/continuo_constantes/tex/parte_iii/capitulos/c31_vacio_epsilon_mu_z_c.tex:130>).
4. [Cruce con el lector de vacío de ACLARAR](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/ACLARAR/INTERRELACIONES_ESTRUCTURALES_VACIO.md>).
5. [Cruce con los momentos periódicos de OVERLEAF](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/OVERLEAF/RED_LECTORES_MOMENTOS_Y_SUSTITUCIONES.md>).
6. [Desarrollo anterior de LEY9: defecto, recuperación y balance](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/DEFECTO_DODECAFASICO_RECUPERACION_Y_BORDE.md>).

## 1. La actualización produce el incremento

Sea \(x^+=\mathcal Ux\) una actualización del estado TPK y \(r\) el lector publicado considerado. Si \(R\) representa en ese lector el desplazamiento de fase correspondiente al paso, el incremento transportado es

\[
\boxed{\eta_{\rm inc}(x)=r(\mathcal Ux)-Rr(x).}
\]

Esta fórmula expresa su procedencia, no concede libertad para escogerlo. Para hacerla efectiva se sustituye el lector y la actualización de la coordenada considerada.

### Actualización explícita del conteo de U016

Las ventanas son \(E_m=\{9m+1,\ldots,9m+9\}\), \(0\le m<12\). U016 define

\[
\Sigma=(+,+,+,-,-,-,+,+,+,-,-,-),\qquad
a_m^{\rm evt}=\Sigma_m\sum_{t\in E_m}
\mathbf1_{\{2,4,6,8\}}(d_t).
\]

Los \(d_t\) son las direcciones de la traza TPK; no se eligen mediante un valor posterior. El símbolo \(a_m^{\rm evt}\) designa exclusivamente este evento firmado. Los vectores canónicos se escribirán \(\mathbf e_m\), para no confundirlos con el número de Euler ni con los eventos escalares.

En coordenadas de ventanas fijas, la publicación acumulada del prefijo es

\[
z_m=\sum_{j<m}a_j^{\rm evt}\mathbf e_j,\qquad
z_{m+1}=z_m+a_m^{\rm evt}\mathbf e_m.
\]

No se introduce una dinámica alternativa: se escribe como recurrencia la suma que define el lector fuente. El dato de cada paso lo proporciona la traza anterior.

Fijamos \(S\mathbf e_j=\mathbf e_{j+1\pmod {12}}\) y el marco móvil \(y_m=S^{-m}z_m\). Entonces

\[
\boxed{
y_{m+1}=S^{-1}y_m+\eta_m,\qquad
\eta_m=a_m^{\rm evt}S^{-1}\mathbf e_0.}
\]

**Prueba.** Sustituir la recurrencia de \(z_m\) y usar \(S^{-m}\mathbf e_m=\mathbf e_0\). No interviene ninguna condición de conservación impuesta después.

Aquí \(R=S^{-1}\). La fórmula anterior que utilizaba \(Sz\) fijaba la orientación contraria para el transporte; no deben mezclarse ambas convenciones en una misma ecuación. Los proyectores y las cotas cuadráticas son invariantes al invertir la orientación, pero los registros orientados permanecen distintos.

El paso representa una ventana completa de nueve ticks. Si se desea la lectura tick a tick, se añade únicamente el sumando \(\Sigma_m\mathbf1_{\{2,4,6,8\}}(d_t)\mathbf e_m\) del tick que acaba de producirse; no se anticipan los ticks posteriores.

### Memoria después del retorno de fase

Iterar doce pasos da

\[
y_{12}=S^{-12}y_0+
\sum_{m=0}^{11}S^{-(11-m)}\eta_m
=y_0+\sum_{m=0}^{11}a_m^{\rm evt}\mathbf e_m.
\]

Así, **\(S^{12}=I\) no elimina la acumulación de eventos**. Para el prefijo que arranca en cero, \(y_{12}\) es precisamente el vector fuente de doce eventos firmados. El programa verifica que la matriz que lleva los doce recuentos a esa publicación final es \(I_{12}\): el retorno no los borra ni los permuta.

De forma general, cuando el mismo transporte \(R\) se aplica en cada paso,

\[
r(\mathcal U^n x)-R^n r(x)
=\sum_{j=0}^{n-1}R^{n-1-j}\eta_{\rm inc}(\mathcal U^j x).
\]

Es una suma transportada de incrementos producidos, no una trayectoria futura suministrada al generador. Conservar el conteo no equivale a recuperar el orden de todos los ticks; ese orden sigue en el ledger.

## 2. El balance recibe la salida calculada, no un parámetro

Con los operadores fuente

\[
D_3=I-S^3,\quad D_4=I-S^4,\qquad
B=D_3^*D_3+D_4^*D_4,
\qquad
\mathcal M(y)=\tfrac12\langle y,By\rangle,
\]

se cumplen \(S^*BS=B\) y \(B_{00}=4\). Por ello, para registros reales,

\[
\boxed{
\mathcal M(y_{m+1})-\mathcal M(y_m)
=a_m^{\rm evt}(By_m)_0+2(a_m^{\rm evt})^2.}
\]

La carga \(q(y)=\sum_j y_j\) satisface simultáneamente

\[
\boxed{q(y_{m+1})-q(y_m)=a_m^{\rm evt}.}
\]

**Prueba.** La invariancia bajo \(S^{-1}\) reduce la primera diferencia a
\(\mathcal M(y_m+a_m^{\rm evt}\mathbf e_0)-\mathcal M(y_m)\). Al expandir, el término mixto es \(a_m^{\rm evt}(By_m)_0\) y el cuadrático es
\(\tfrac12(a_m^{\rm evt})^2B_{00}=2(a_m^{\rm evt})^2\).
La carga es invariante bajo la permutación y suma el evento firmado.

El signo de la variación no queda fijado por el retorno de fase: depende del intercambio con el registro que ya existe. La recuperación conjunta mediante \(D_3,D_4,q\) conserva tanto el registro relativo como su carga. La forma \(\mathcal M\) por sí sola pierde esta última.

Este resultado explicita la actualización de **esta coordenada publicada**. No se identifica el recuento con todas las coordenadas del estado TPK ni se convierte esta forma interna en una energía hidrodinámica por cambio de nombre.

## 3. Del mismo ciclo al lector de vacío

Los proyectores

\[
P_3=\tfrac14(I+S^3+S^6+S^9),\qquad
P_4=\tfrac13(I+S^4+S^8)
\]

tienen imágenes \(H_3=\operatorname{Fix}(S^3)\) y \(H_4=\operatorname{Fix}(S^4)\), de dimensiones tres y cuatro. Su defecto es \(E=P_3-P_4\), con \(\operatorname{Tr}E/12=-1/12\).

El desplazamiento \(S\) actúa en \(H_3\) como un ciclo de tres posiciones y en \(H_4\) como uno de cuatro. En consecuencia,

\[
\det_{H_3}(I-sS)=1-s^3,\qquad
\det_{H_4}(I-sS)=1-s^4.
\]

Para \(0<s<1\),

\[
\boxed{
\frac{\det_{H_3}(I-sS)}{\det_{H_4}(I-sS)}
=\frac{1-s^3}{1-s^4}
=\frac{1+s+s^2}{1+s+s^2+s^3}=F(s).}
\]

En el lector fuente de vacío, \(s=q^{30}\). Se obtiene exactamente
\(F(q^{30})=(1-q^{90})/(1-q^{120})\), después de que los canales \(q_\pm\) hayan sido producidos por su rama angular.

Esta representación es más precisa que relacionar números por coincidencia: **la traza que publica \(-1/12\) y el determinante que publica \(F(s)\) operan sobre el mismo par de espacios cíclicos**. La cancelación del modo constante común explica la forma finita de \(F\) en \(s=1\), donde vale \(3/4\). No se identifica por ello una matriz de doce coordenadas con todo el operador físico de vacío; se construye una representación determinantal exacta de su función escalar de canal.

### Sector antipodal y cuarto de giro

Sea \(P_-=(I-S^6)/2\), \(V_-=\operatorname{Ran}P_-\). En \(V_-\),

\[
J=S^3,\quad J^2=-I,\quad J^*=-J.
\]

El proyector \(Q=P_4P_-\) tiene rango dos. Como \(P_3P_-=0\),

\[
\boxed{E|_{V_-}=-Q,\qquad B|_{V_-}=5I-3Q.}
\]

En \(\operatorname{Ran}Q\) se tiene \(S^2=-I\) y

\[
\det_{\operatorname{Ran}Q}(I-sS)=1+s^2.
\]

Por tanto, la factorización del lector separa exactamente los sectores:

\[
F(s)=
\underbrace{\frac{1+s+s^2}{1+s}}_{\text{sector }S^6=+I}
\underbrace{\frac1{1+s^2}}_{\text{sector }S^6=-I}.
\]

El factor cuadrático corresponde a un plano real con estructura compleja dentro del mismo ciclo. En ese plano \(B=2I\); en su complemento dentro de \(V_-\), \(B=5I\). Invertir la orientación cambia \(J\) por \(-J\), pero no cambia \(B\) ni \(F\). La forma orientada \(\omega(u,v)=\langle Ju,v\rangle\) conserva una información que el balance cuadrático y el determinante escalar no distinguen.

## 4. El mismo defecto genera una tabla y una familia de momentos

La traza de los transportes del defecto produce, sin escoger una nueva tabla,

\[
a_n=\operatorname{Tr}(S^nE)
=3\mathbf1_{3\mid n}-4\mathbf1_{4\mid n}.
\]

En \(n=0\), \(a_0/12=-1/12\). Para \(n=1,\ldots,12\), la tabla es

\[
(0,0,3,-4,0,3,0,-4,3,0,0,-1).
\]

Tiene período doce y suma nula por período. La expansión determinantal proporciona

\[
-\log F(s)=\sum_{n\ge1}\frac{a_n}{n}s^n,\qquad |s|<1.
\]

La rama del logaritmo se fija por \(\log F(0)=0\). Para \(0<s<1\) es la rama real. Una demostración equivalente deriva la expresión racional y obtiene

\[
-\frac{sF'(s)}{F(s)}
=\frac{3s^3}{1-s^3}-\frac{4s^4}{1-s^4}.
\]

Aplicando a **esta tabla producida** el lector de momentos ya trabajado por OVERLEAF, con variable \(z\),

\[
\boxed{
M_a(z)=\sum_{n\ge1}\frac{a_n}{n^z}
=(3^{1-z}-4^{1-z})\mathcal Z_3(z),
\qquad \operatorname{Re}z>1.}
\]

La prueba agrupa separadamente los múltiplos de tres y de cuatro en el dominio de convergencia absoluta. En particular,

\[
M_a(2)=\frac{\mathcal Z_3(2)}{12}.
\]

En el borde \(z=1\), los parciales son
\(H_{\lfloor N/3\rfloor}-H_{\lfloor N/4\rfloor}\), de modo que

\[
M_a(1)=\log(4/3)=-\log F(1).
\]

Este último es un límite convergente por cancelación, no una suma de dos series divergentes calculadas por separado. Quedan enlazados el defecto dimensional, las fases de retorno, el cociente determinantal y los momentos mediante operaciones explícitas. Ninguno de esos valores reemplaza la historia TPK que produjo el lector.

## 5. Comprobación y falsadores

El [verificador local](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/verificar_actualizacion_tpk_y_determinantes.py>) utiliza aritmética racional. Comprueba:

- la recurrencia del marco móvil y su matriz de transferencia durante las doce ventanas;
- los coeficientes completos de la identidad de balance y, adicionalmente, 120 casos de signo y recuento;
- los proyectores, la estructura compleja antipodal y \(B|_{V_-}=5I-3Q\);
- los polinomios determinantes mediante las identidades de Newton, contrastados además por eliminación racional;
- la tabla de trazas, su período y la identidad racional de la derivada logarítmica.

La demostración analítica de los momentos está escrita en la sección 4; el control de matrices no se presenta como prueba automática de una continuación meromorfa.

Falsadores: imponer \(\eta=0\) pese a existir eventos altera la recurrencia; borrar la carga impide recuperar la media; reemplazar \(S\) por \(S^{-1}\) sólo en una mitad de la actualización altera el transporte; conservar únicamente \(-1/12\) pierde el espectro; un determinante escalar no decide la orientación de \(J\). Los ensayos de recuento verifican el lector sobre su dominio algebraico y no declaran que toda palabra ambiente sea una historia superviviente.

No se han modificado PDFs, fuentes científicas anteriores ni el documento común. La skill de constantes generadas se utiliza para comprobar el rol causal; ese control no sustituye las pruebas anteriores.
