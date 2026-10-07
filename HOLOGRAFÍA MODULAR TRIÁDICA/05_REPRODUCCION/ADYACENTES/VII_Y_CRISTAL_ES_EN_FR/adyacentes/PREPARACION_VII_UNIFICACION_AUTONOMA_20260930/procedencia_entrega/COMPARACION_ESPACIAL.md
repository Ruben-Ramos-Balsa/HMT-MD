# Archivo, evolución y comparación espacial del operador interactuante

Composición focal del 30 de septiembre de 2026. Fragmento asociado:
`latex/30_archivo_evolucion_comparacion.tex`.
No modifica las fuentes ni sustituye el Hamiltoniano recibido.

## 1. Destino y procedencia efectiva

El destino es **Gravitación, torsión y dinámica cosmológica**,
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/VIII_ES/manuscrito/`.
Su `cuerpo_en_desarrollo.tex` incluye 30d en la línea 69, 30b en la 73,
30c en la 75 y 33 en la 83. VIII designa este corte material, no el antiguo
artículo de primos. El sucesor focal del 29 de septiembre no contiene una
carpeta `fuentes/VIII_ES` que sustituya este proyecto.

Se conserva APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo, con sus cinco construcciones consustanciales, hojas,
orientación, residuos, acarreo, ruta, frontera y memoria. Las constantes y
lectores son salidas anteriores; no se seleccionan por valores objetivo.
En las variaciones y conjugaciones siguientes se conserva una misma sección
de acción \(\hbar>0\) y una misma carta de unidades.

Se reúnen las pruebas recuperadas de historias completas, archivo,
suspensión y refinamiento. La composición explícita de los mapas de archivo
con el reloj se desarrolla aquí; la comparación espacial se expresa como
un residuo preciso, no como una negación de los resultados anteriores.

## 2. Índices y operador conservado

| Índice | Operación | Resultado |
|---|---|---|
| Archivo \(n\) | \(V_n,J_n\), división del residuo | Isometría y entrelazamiento exacto con dominio |
| Precisión \(k\) | Colas de torres, Yukawa y torsión | Convergencia de formas y resolventes |
| Espacio \(m\) | Inclusiones de vértices/aristas, medidas | Igualdades de 30b–30c y entrelazamiento YM específico |
| Reloj \(s,r\) | Suspensión y parametrización | Evolución continua y retorno completo |

El espacio de todas las historias es \(\mathscr H=\bigoplus_x\mathscr H_x\).
Se conserva el operador de `LIMITE_MATERIA_MEMORIA.md`, §3:

\[
H_{\rm loc}=\bigoplus_xh_x,\qquad
h_x=\hbar cK_{{\rm gauge},x}+d\Gamma(D_{T,x}^*W_xD_{T,x})
+H_{H,\mathrm{cin},x}+V_{H,x}+H_{Y,x}+H_{{\rm tor},x}.
\tag{1}
\]

La celularización y los modos fermiónicos de esta carta permanecen fijados;
las historias y las amplitudes escalares no se cortan. El bloque
\(D_T^*WD_T\) es la respuesta geométrica de segundo orden, no un operador
de Weyl rebautizado. Yukawa contiene su adjunto y las mezclas en la misma
base. La torsión utiliza la corriente total antes del cuadrado, después
de eliminar una sola vez la contorsión.

Para que VIII no dependa de la prueba insertada en VII, el fragmento 30
incluye también la prueba de forma cerrada en cada fibra: dominio con
derivada escalar y peso cuártico, cotas del término Yukawa y cuadrático,
coercividad desplazada y representación autoadjunta. Las cotas son por
fibra; no se promueve esa prueba a una uniformidad espacial no calculada.
Se reúnen las dependencias de `EVOLUCION_ACOPLADA_Y_LIMITE.md` y
`LIMITE_MATERIA_MEMORIA.md`, no una nueva elección de dinámica.

Su dominio es \(\Psi_x\in\operatorname{Dom}h_x\),
\(\sum_x\|h_x\Psi_x\|^2<\infty\). La cota
\(\|(h_x-z)^{-1}\|\le|\operatorname{Im}z|^{-1}\) prueba autoadjunción de la
suma sin exigir una cota inferior uniforme en \(x\).

La normalización de medidas es efectiva:
\(A_xf=\sqrt{Z_x}e^{S_x/2}f\), de \(L^2(\mu_0)\) a
\(L^2(\mu_x)\), con \(d\mu_x=Z_x^{-1}e^{-S_x}d\mu_0\).
Componerla con el transporte de hoja y espín produce el unitario
\(C_\mu\) sobre las historias. Se conserva \(U=C_\mu e^{-iTH_{\rm loc}/\hbar}\)
y su orden, no se supone conmutación de ambos factores.

## 3. Archivo: la cola y los dominios son parte de la prueba

Para el retorno unitario completo \(C\), sea \(T_9=(8I+C)/9\) y
\[
\eta v=\frac1{27}(8(C-I)v,-(C-I)v,\ldots,-(C-I)v),\qquad
I-T_9^*T_9=\eta^*\eta=\frac8{81}(I-C)^*(I-C).
\]
Hay ocho componentes de coeficiente \(-1\). Definimos
\[
V_nv=(T_9^nv,\eta v,\ldots,\eta T_9^{n-1}v),\qquad
J_n(r,m_0,\ldots,m_{n-1})=(T_9r,m_0,\ldots,m_{n-1},\eta r).
\tag{2}
\]
La telescopía de normas prueba que son isometrías y \(J_nV_n=V_{n+1}\).
Sobre \(\mathscr M_n=\operatorname{Im}V_n\),
\[
A_n^{\rm arch}=V_nAV_n^*,\quad
\operatorname{Dom}A_n^{\rm arch}=V_n\operatorname{Dom}A,\quad
A_n^{\rm arch}V_n=V_nA,\quad J_nA_n^{\rm arch}=A_{n+1}^{\rm arch}J_n.
\tag{3}
\]
El archivo infinito es
\[
Vv=(Pv,\eta v,\eta T_9v,\ldots),\qquad
v=Pv+\sum_{j\ge0}T_9^{*j}\eta^*(\eta T_9^jv),\quad
P=\operatorname{proj}\ker(I-C).
\tag{4}
\]
El teorema espectral da \(T_9^n\to P\), y la telescopía prueba isometría
e inversa en norma. Se trabaja sobre la imagen compatible, sin completar
arbitrariamente el operador en su complemento. En el sector graduado
bilateral \(P=0\); a profundidad finita la cola \(T_9^nv\) sigue siendo
indispensable. (3) transporta el operador completo y sus conmutadores.

## 4. Composición explícita de archivo, suspensión y reloj

Pónganse \(E(s)=e^{-isH_{\rm loc}/\hbar}\),
\(B=U^{-1}=E(T)^*C_\mu^{-1}\) y
\(\mathscr K=L^2([0,T];\mathscr H)\). La suspensión recibida es
\[
P_B=-i\hbar\partial_s,\quad
\operatorname{Dom}P_B=\{f\in H^1:f(T)=Bf(0)\},\qquad
\mathbb K=\mathcal EP_B\mathcal E^*,\quad
(\mathcal Ef)(s)=E(s)f(s).
\tag{5}
\]
Su dominio exacto es \(\mathcal E\operatorname{Dom}P_B\). La frontera
unitaria prueba autoadjunción. Los vectores del dominio satisfacen
\(\psi(T)=C_\mu^{-1}\psi(0)\); en la intersección regular actúa
\(-i\hbar\partial_s+H_{\rm loc}\). La monodromía es \(E(s)UE(s)^*\).
No se evalúan clases \(L^2\) arbitrarias en fase cero.

El mapa \(V_n\) no actúa originalmente sobre \(\mathscr K\). Su elevación
correcta es
\[
\mathcal V_n=I_{L^2([0,T])}\otimes V_n,\quad
\mathbb K_n=\mathcal V_n\mathbb K\mathcal V_n^*,\quad
\operatorname{Dom}\mathbb K_n=\mathcal V_n\operatorname{Dom}\mathbb K,
\]
\[
\mathcal J_n=I\otimes J_n,\qquad
\mathcal J_n\mathcal V_n=\mathcal V_{n+1}.
\tag{6}
\]
Todos estos operadores actúan sobre las imágenes compatibles. Para
\(W(r)=e^{-ir\mathbb K/\hbar}\), el mapa compuesto es
\[
I_n(r)=\mathcal V_nW(r).
\]
Sobre \(\operatorname{Dom}\mathbb K\), la derivación fuerte da
\[
\partial_rI_n=-\frac{i}{\hbar}\mathbb K_nI_n,\quad
(\partial_r+i\mathbb K_n/\hbar)I_n=I_n\partial_r,\quad
\mathcal J_nI_n=I_{n+1},\quad
\mathbb K_{n+1}\mathcal J_n=\mathcal J_n\mathbb K_n .
\tag{7}
\]
La segunda igualdad se aplica a secciones regulares; luego transporta el
dominio de la conexión. Conserva la frontera por
\(\mathcal V_n\operatorname{Dom}\mathbb K\), no por un dominio nuevo.
La parametrización de Legendre queda así compuesta con el archivo, no
simplemente citada. No se duplica la dinámica \(W\) en otro término.

Éste es un entrelazamiento exacto del **reloj**. Los generadores
\(-i\hbar(N(r)\partial_r+N'(r)/2)\) también se transportan por \(W\).
No se identifican con lapsos espaciales arbitrarios \(N(x)\).

La convergencia de lectores mantiene fijos medida, cinética, potencial
cuártico, volúmenes y transportes. Las colas convergentes de masas dan
convergencia en norma de las matrices Yukawa y torsionales por fibra.
El dominio común de formas y el control de los términos lineales por
el cuártico dan resolventes convergentes; la suma directa converge
fuertemente. Por tanto \(E_k,U_k,B_k\) y los grupos de (5) convergen
fuertemente. Este límite de precisión no sustituye un límite espacial.

## 5. Composición espacial efectivamente recuperada

30b demuestra para mapas fijos
\(D_{m+1}J_m=K_mD_m\), \(K_m^*W_{m+1}K_m=W_m\).
Para \(B_m=D_m^*W_mD_m\), resulta \(J_m^*B_{m+1}J_m=B_m\) como forma.
Si \(J_m\) es isométrico y los dominios permiten las acciones, el defecto
operatorio exacto es
\[
B_{m+1}J_m-J_mB_m=(I-J_mJ_m^*)B_{m+1}J_m.
\tag{8}
\]
La corriente de 30c conserva
\(s_m=P_m^{\mathsf T}s_{m+1}\) y
\(M_m\sigma_m=P_m^{\mathsf T}M_{m+1}\sigma_{m+1}\).
Si cambia \(J_m\), 30b conserva también
\(2\operatorname{Re}\langle D_{m+1}J_mf,
W_{m+1}D_{m+1}(\delta_NJ_m)f\rangle\).

30d conserva
\(\operatorname{Hol}_A(R_C\gamma)=\rho_C(\operatorname{Hol}_{\rm TPK}\gamma)\),
con identidad, concatenación, inversión y subdivisión. El sucesor XII de
septiembre29 conserva la composición y el cociclo de memoria; no convierte
dos caminos de iguales extremos en el mismo camino.

El generador YM posee su cuadrado fuerte específico. Sus mapas
\[
J_{m,g}=\mathcal T_{m+1,g}^{-1}J_m\mathcal T_{m,g},\qquad
H_{m,g}^{\rm YM}=\mathcal T_{m,g}^{-1}H_m^0\mathcal T_{m,g}
\]
dan \(H_{m+1,g}^{\rm YM}J_{m,g}=J_{m,g}H_{m,g}^{\rm YM}\), con dominio
y proyección física transportados. Se conserva este resultado positivo,
sin atribuir tácitamente su cuadrado a todos los otros sumandos de (1).

## 6. Comparación canónica–operatoria y residuo único

La acción total entrega \(\Omega=-d\Theta\) y
\(\nabla^{\rm can}=d-i\Theta/\hbar\), plana en las direcciones
características de su superficie regular de restricciones. Se conserva
el anclaje de cada deformación al campo característico correspondiente.

Sobre una misma base y dominio común, sea \(I_0\) un mapa de secciones
canónicas admisibles a la realización operatoria. Definimos
\[
E_N=\nabla_N^{\rm op}I_0-I_0\nabla_N^{\rm can}.
\]
Si las conexiones se escriben \(\delta_N+(i/\hbar)A_N^a\),
\[
E_N=\frac{i}{\hbar}\Delta_N,\qquad
\Delta_N=A_N^{\rm op}I_0-I_0A_N^{\rm can}
                      -i\hbar\,\delta_NI_0 .
\tag{9}
\]
\(A_N^{\rm can}\) es aquí el **coeficiente de conexión**, no el operador
precuántico completo \(\mathcal P_f=-i\hbar\nabla_{X_f}+f\): su
derivación de base no se cuenta dos veces. \(A_N^{\rm op}\) es el generador
espacial efectivo de la realización, no se redefine como \(\mathcal P_f\).

La regla \(E_N^{JI}=E_N^J I+JE_N^I\) se prueba insertando y restando
\(J\nabla I\). La suma transportada puede anularse por cancelación:
no se exige que cada defecto intermedio sea cero. Con \(\hbar\) fija,
la misma regla vale para \(\Delta_N\). Para el archivo con conexión transportada:
\[
A_N^{\rm arch}=VA_N^{\rm op}V^*+i\hbar(\delta_NV)V^*,\qquad
E_N^{VI_0}=VE_N^{I_0}.
\tag{10}
\]
La conexión es intrínsecamente \(\nabla^{\rm arch}=V\nabla^{\rm op}V^*\)
en el fibrado de imágenes compatibles. En la escritura ambiental de (10),
la combinación con la derivada preserva ese subfibrado; el coeficiente
aislado no se declara autoadjunto en todo el ambiente. Si se utiliza la
derivada proyectada \(P_V\delta_N\), \(P_V=VV^*\), su coeficiente es
\(VA_N^{\rm op}V^*+i\hbar P_V(\delta_NV)V^*\) sobre la imagen.
Para el archivo fijo, \(\delta_NV=0\). La isometría implica
\(E_N^{VI_0}=0\Longleftrightarrow E_N^{I_0}=0\). La memoria no borra un
residuo ni crea otro. La misma regla compone las normalizaciones unitarias
y los mapas del reloj; (7) demuestra el caso de reloj con mapa explícito.

Para curvaturas, en el dominio común:
\[
R^{\rm op}_{NM}I_0-I_0R^{\rm can}_{NM}
=\nabla_N^{\rm op}E_M-\nabla_M^{\rm op}E_N
+E_N\nabla_M^{\rm can}-E_M\nabla_N^{\rm can}-E_{[N,M]} .
\tag{11}
\]
Se obtiene expandiendo los dos productos ordenados. Con \(\hbar\) fija,
\(R=(i/\hbar)F\); se conservan los términos cruzados y del mapa móvil.
Si se variara físicamente la sección de acción, aparecerían además
\(-(\delta_N\log\hbar)A_M+(\delta_M\log\hbar)A_N\) en \(F\);
esa variación no se realiza en (5)–(11).

**Resultado.** Archivo, normalización de medidas y reloj tienen mapas
explícitos, inversas sobre sus imágenes y dominios transportados. Los
cuadrados espaciales de (8), las corrientes y YM están identificados.
Por sus dominios y codominios, esos mapas no forman por sí solos un mapa
desde las secciones canónicas hasta el operador completo (1).
El punto que esta composición no identifica es únicamente \(I_0\) y el
valor de (9) para deformaciones espaciales arbitrarias. No se declara
inexistencia global, ni se reabren la acción, el archivo, el retorno o las
constantes. Tampoco se usa el cierre canónico para cambiar \(H_{\rm loc}\).

El control recuperado de precuantización explica por qué el mapa no es
una mera restricción: con \(\Theta=p\,dq\),
\(\mathcal P_{p^2/2}=-i\hbar p\partial_q-p^2/2\) no preserva las funciones
independientes de \(p\), mientras la cinética de configuración es de segundo
orden. Descarta esa identificación automática, no otro mapa HMT construido.
La planitud local, cuando se transfiera por (9), no implica holonomía global
trivial.

## 7. Localizadores y estado de la reunión

Ronda reutilizada:
`/Users/ruben/Documents/New project/output/COMPOSICION_CUATRO_INTERACCIONES_20260929/`.
Pruebas: `quantum/LIMITE_MATERIA_MEMORIA.md`, §§2–6;
`quantum/SUSPENSION_RELOJ_INTERACTUANTE.md`, teoremas 1–4;
`quantum/LEGENDRE_PCH_Y_RELOJ_PARAMETRIZADO.md`, §4;
`quantum/PRECUANTIZACION_PCH_Y_FIDELIDAD.md`, §§2–4;
`quantum/CURVATURA_TOTAL_MEMORIA_Y_LIMITE.md`, composición de conexiones.
No se rotulan estas pruebas recuperadas como resultados nuevos.

La recomposición explícita (6)–(7) y la regla con cancelaciones (9)–(10)
conservan además la procedencia de la revisión independiente reunida en
`/Users/ruben/Documents/New project/output/COORDINACION_CIERRE_CORPUS_ACLARAR_20260930/REVISION_INDEPENDIENTE_RECOMPOSICION.md`,
§§2–3. Se incorporan con prueba, sin duplicar ni reatribuir sus antecedentes.

Propietarios bajo
`/Users/ruben/Documents/excelencia academica/output/CUMPLIMIENTO_EDITORIAL_20260928/fuentes/`:

- `XII_ES/nuclear/09.tex`: historias y retorno, líneas 56–64; archivo
  infinito, inversa, operadores y sector graduado.
  `XII_ES/sections/retornos_completos.tex`: retorno completo e inversa.
- `VI_ES/sections/05_registro_operador_masa.tex`,
  `05b_electron_estados_ley_masas_20260927.tex` y
  `13_fock_pauli_composicion.tex`: torres, balance y naturalidad de Fock.
- `VIII_ES/manuscrito/30b_variacion_energia_memoria.tex`, líneas 261–309;
  `30c_composicion_corriente_conexion.tex`, líneas 239–270;
  `30d_realizacion_geometrica.tex`, líneas 30–58.
- `X_ES/sections/ym_complete.tex`, etiquetas
  `eq:pdf2-ym-gibbs-transport-global`,
  `eq:pdf2-ym-full-probability-isomorphism`,
  `eq:pdf2-ym-g-dynamics`: álgebra completa, medidas y generador.

Sucesor:
`/Users/ruben/Documents/excelencia academica/output/AMPLIACION_PUNTUAL_FINAL_ES_EN_20260929/fuentes/XII_ES/sections/tpk_desarrollo_integrado.tex`,
líneas 219–335: actualización enriquecida, composición y cociclo.

Integral:
`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/manuscrito/sections/md/11p_gravedad_variacional_hamiltoniana_rev11.tex`
y `04ab_postulados_cuanticos_genealogicos_rev2.tex` en el mismo directorio
(líneas 178–207 y 339–382): realización canónica y reconstrucción hilbertiana.

Los recibos de historias, suspensión, Legendre y curvatura canónica de la
ronda se conservan intactos. Certifican sus archivos, no estos bytes nuevos.
La entrega debe registrar separadamente conservación, integración editorial
y alcance matemático. No se editan los PDF ni se declara integrado este
fragmento antes de su incorporación por el editor único.
