# Archivo íntegro de los cuatro desarrollos de Feigenbaum

Se conservan literalmente los cuerpos siguientes. Las delimitaciones históricas se leen en su orden de fecha y quedan actualizadas por las demostraciones acumulativas de las secciones 15–17 del tercer documento. La exposición pública reunida se entrega en archivo separado; este archivo conserva también los intentos, controles y delimitaciones anteriores.



---

<!-- COMIENZO ÍNTEGRO desarrollo -->

# Retorno dodecafásico, memoria de rutas y renormalización cuadrática en HMT

Desarrollo del 29 de septiembre de 2026. Se conserva la familia del capítulo de Feigenbaum del corpus y se amplían sus propiedades analíticas y su certificación finita. Los manuscritos publicados permanecen intactos.

## 1. Genealogía y objeto de la demostración

El objeto inicial es la publicación crítica de la rueda dodecafásica orientada ya construida en el corpus. APP evalúa suma y producto sobre las dos hojas de la retícula de dígitos, conservando cociente y residuo; TRIT determina régimen y orientación; el transporte TPK selecciona, transporta y actualiza el estado con sus registros de acarreo, frontera y memoria. La conexión nonádica prolonga ese estado, con retorno de fase y avance de memoria. Sus lectores actúan sobre la misma estructura discreta del continuo.

El lector focal de la fuente es
\[
\mathcal P_{\mathrm{crit}}:U_{12}^{\mathrm{sign}}\longrightarrow
\mathbb R/2\pi\mathbb Z,\qquad
m\longmapsto\phi_m=\frac{(3m-1)\pi}{18},\quad 1\le m\le12.
\]
Para evaluar el momento angular se conserva el representante orientado de esa carta: sustituirlo por otro representante módulo \(2\pi\) cambiaría el momento. La traza uniforme fija \(w_m=1/12\). La cadena focal es
\[
\text{APP–TRIT–TPK}\longrightarrow
\text{estructura discreta del continuo}\longrightarrow U_{12}^{\mathrm{sign}}
\xrightarrow{\mathcal P_{\mathrm{crit}}}(\phi_m,w_m)
\longrightarrow u_0\longrightarrow f_\lambda
\longrightarrow\text{retornos y renormalización}.
\]

La escritura abreviada conserva como antecedente el estado completo y sus prolongaciones; la familia escalar es una lectura de ese antecedente. Se toma como estructura de partida explícita el lector ya fijado, con su orden, orientación y sector uniforme. Las conclusiones se refieren a ese lector concreto; la unicidad de ese lector entre todas las publicaciones posibles del TPK queda fuera de estas pruebas.

La coordenada \(\pi_{\mathrm{HMT}}\) empleada por la carta pertenece a las salidas internas del corpus. Su factor se cancela exactamente al normalizar el segundo momento. Los valores de Feigenbaum intervienen exclusivamente en el reconocimiento posterior, nunca en la definición de la familia o en la certificación de raíces.

## 2. Perfil exacto y criticidad cuadrática

Sea \(s_m=3m-1\). La suma entera
\[
\sum_{m=1}^{12}s_m^2=5394=6\cdot899
\]
determina
\[
\kappa_0=\frac{36}{\pi\sqrt{899}},\qquad
k_m=\kappa_0\phi_m=\frac{2s_m}{\sqrt{899}},
\]
\[
u_0(x)=\frac1{12}\sum_{m=1}^{12}(1-\cos(k_mx)),\qquad
f_{\lambda,0}(x)=1-\lambda u_0(x).
\]
Por identidad del segundo momento,
\[
u_0(0)=u_0'(0)=0,\quad u_0''(0)=2,\quad
f_{\lambda,0}''(0)=-2\lambda.
\]
La representación analítica conserva coeficientes racionales:
\[
u_0(z)=\sum_{j\ge1}(-1)^{j+1}
\frac{4^j\sum_m s_m^{2j}}{12\,899^j(2j)!}z^{2j}
=z^2-\frac{715769}{2424603}z^4
+\frac{1353832978}{32695771455}z^6+\cdots.
\]
Así, el registro finito de doce sectores produce un perfil entero, con criticidad cuadrática y escala fijadas antes de iterar.

## 3. Robustez estructural con cotas uniformes

La deformación ya presente en el código de procedencia es
\[
w_m(\eta)=\frac{1+\eta p_m}{12},\qquad
p_m=12\cos(3\phi_m)-\cos(4\phi_m).
\]
Definimos
\[
M_{2,\eta}=\sum_mw_m(\eta)\phi_m^2,\quad
\kappa_\eta=\sqrt{2/M_{2,\eta}},\quad k_{m,\eta}=\kappa_\eta\phi_m,
\]
\[
u_\eta(x)=\sum_mw_m(\eta)(1-\cos(k_{m,\eta}x)),\qquad
f_{\lambda,\eta}=1-\lambda u_\eta.
\]

**Teorema 1.** Para \(|\eta|\le1/40\), los pesos son positivos y suman uno. El perfil es par, entero, satisface \(u_\eta''(0)=2\) y es estrictamente creciente en \((0,1]\). Para \(0<\lambda\le2/u_\eta(1)\), el mapa lleva \([-1,1]\) en sí mismo, tiene un único punto crítico en ese intervalo y cumple
\[
S f_{\lambda,\eta}(x)\le-\frac{640}{47647}<0,\qquad0<|x|\le1.
\]

**Demostración.** Las sumas de los cosenos \(3\phi_m\) y \(4\phi_m\) se anulan por ciclos de longitudes cuatro y tres. Como \(|p_m|\le13\),
\[
\frac9{160}\le w_m\le\frac{53}{480},\qquad
\frac{27}{40}M_{2,0}\le M_{2,\eta}\le\frac{53}{40}M_{2,0}.
\]
Se deduce
\[
k_{\max,\eta}^2\le\frac{196000}{24273}<9<\pi^2,\qquad
k_{\min,\eta}^2\ge\frac{640}{47647}.
\]
Para \(0<x\le1\), todos los senos \(\sin(k_{m,\eta}x)\) son positivos, de donde
\[
u_\eta'(x)=\sum_mw_mk_m\sin(k_mx)>0,\qquad
u_\eta'''(x)=-\sum_mw_mk_m^3\sin(k_mx)<0.
\]
El cociente \(u_\eta'''/u_\eta'\) es el negativo de una media positiva de los \(k_m^2\). La invariancia de la schwarziana bajo cambios afines del valor da
\[
S f_{\lambda,\eta}
=\frac{u_\eta'''}{u_\eta'}-\frac32
\left(\frac{u_\eta''}{u_\eta'}\right)^2
\le-k_{\min,\eta}^2.
\]
La paridad cubre \(x<0\), y la imagen del intervalo es
\([1-\lambda u_\eta(1),1]\). \(\square\)

La anchura \(1/40\) es una elección para obtener cotas uniformes, distinta de una constante fundamental o de un umbral óptimo. El sector original sigue siendo \(\eta=0\).

## 4. Coordenada holomorfa cuadrática global en una franja

**Teorema 2.** Para \(|\eta|\le1/40\), en
\[
\mathcal S=\{z\in\mathbb C:|\operatorname{Re}z|<\pi/3\}
\]
existe una función holomorfa, impar y univalente \(b_\eta\), con \(b_\eta'(0)=1\), tal que
\[
\boxed{u_\eta(z)=b_\eta(z)^2,\qquad
f_{\lambda,\eta}(z)=1-\lambda b_\eta(z)^2.}
\]

**Demostración.** Para \(z=x+iy\) en la semibanda derecha,
\[
\operatorname{Re}u_\eta'(z)
=\sum_mw_mk_m\sin(k_mx)\cosh(k_my)>0.
\]
La integral de \(u_\eta'\) sobre el segmento entre dos puntos, dividida por la diferencia de los extremos, tiene parte real positiva. La convexidad de la semibanda prueba allí la inyectividad. La paridad da el resultado correspondiente a la izquierda.

Además,
\[
\operatorname{Im}u_\eta(x+iy)
=\sum_mw_m\sin(k_mx)\sinh(k_my)
\]
tiene el signo de \(y\) para \(x>0\). Sobre el eje real positivo \(u_\eta>0\); sobre el imaginario,
\[
u_\eta(iy)=\sum_mw_m(1-\cosh(k_my))
\]
es estrictamente negativo fuera de cero y decrece estrictamente con \(|y|\). Estas separaciones, la inyectividad de cada semibanda y la paridad prueban que las fibras de \(u_\eta\) en \(\mathcal S\) son exactamente \(\{z,-z\}\), salvo la fibra del origen.

La función \(u_\eta(z)/z^2\), prolongada con valor uno en cero, es holomorfa y carece de ceros en la franja simplemente conexa. Tiene un logaritmo holomorfo \(L_\eta\) con \(L_\eta(0)=0\), que es par por unicidad de la normalización. Definimos
\[
b_\eta(z)=z\exp\!\left(\frac12L_\eta(z)\right).
\]
Entonces \(b_\eta^2=u_\eta\), \(b_\eta\) es impar y \(b_\eta'(0)=1\). La igualdad \(b_\eta(z)=b_\eta(w)\) obliga a \(w=z\) o \(w=-z\). El segundo caso sólo da igualdad en el origen. Esto prueba su univalencia. \(\square\)

Las doce fases determinan así una deformación conforme explícita del pliegue cuadrático. La conjugación dinámica completa conserva esa deformación:
\[
b_\eta\circ f_{\lambda,\eta}\circ b_\eta^{-1}(w)
=b_\eta(1-\lambda w^2),
\]
en sus dominios de composición. La factorización demostrada y una conjugación a toda la familia cuadrática son afirmaciones distintas.

## 5. Retorno, cambio de escala y memoria

Sean \(a=-f(1)>0\), \(H_a(x)=-ax\), \(J=H_a([-1,1])\). Cuando \(J\subset[-1,1]\) es admisible para el retorno, \(f^2(J)\subset J\) y las composiciones están definidas,
\[
\mathcal Rf=H_a^{-1}f^2H_a,\qquad
\mathcal Rf(x)=-a^{-1}f(f(-ax)).
\]
Si además \(f(J)\subset(0,1]\), se conserva un único máximo cuadrático central:
\[
(\mathcal Rf)(0)=1,\qquad
(\mathcal Rf)''(0)=-a f'(1)f''(0)<0.
\]
La composición de schwarzianas da, en los puntos regulares,
\[
S(\mathcal Rf)(x)=a^2
\left[(Sf)(f(-ax))f'(-ax)^2+(Sf)(-ax)\right]<0.
\]
Las inclusiones de dominios forman parte de las hipótesis y se comprueban a cada escala.

Sea \(v_\eta=(u_\eta|_{[0,1]})^{-1}\). Las ramas inversas son
\[
\beta_\sigma(y)=\sigma v_\eta((1-y)/\lambda),\quad
\sigma\in\{-1,+1\},
\]
con el registro crítico \(\beta_0(1)=0\). El paso
\[
(x,w)\longmapsto(f(x),w\mathbin{\|}\sigma(x))
\]
se invierte sobre su imagen leyendo la última hoja y aplicando \(\beta_\sigma\). La palabra conserva decisiones de rama; el valor anterior se reconstruye por la ecuación del mapa.

El retorno agrupa dos transiciones. Desde el extremo \(x'\) y sus hojas \((\sigma_0,\sigma_1)\) se recupera
\[
x=H_a^{-1}\beta_{\sigma_0}
\!\left(\beta_{\sigma_1}(H_ax')\right).
\]
También se reconstruyen los puntos intermedios. Los registros APP–TRIT–TPK de hoja, acarreo, ruta, frontera y memoria se concatenan conservando su identidad. El signo de la rama analítica es un registro adicional: no reemplaza esos datos por una etiqueta binaria.

Si \(C_N\) agrupa las historias de longitud \(2N\) en pares, las restricciones satisfacen
\[
\pi^{\mathrm{ret}}_{N,M}C_N
=C_M\pi^f_{2N,2M},\qquad M\le N.
\]
Ambos miembros suprimen los mismos pares terminales y conservan las mismas ramas inversas. Queda demostrado el transporte compatible de historias finitas.

## 6. Escalas acumuladas y derivada del operador

Sean \(c_n=f^{2^n}(0)\), \(c_0=1\) y \(H_n(x)=c_nx\). Mientras las composiciones sean admisibles y \(c_n\ne0\),
\[
\boxed{\mathcal R^nf=H_n^{-1}f^{2^n}H_n},\qquad
(\mathcal R^nf)(1)=\frac{c_{n+1}}{c_n}=-a_n.
\]
La inducción se obtiene de \(H_nH_{a_n}=H_{n+1}\). La convención \(a_n>0\) exige alternancia de signo de \(c_n\). En una raíz superestable de período \(2^N\), \(c_N=0\): esa normalización se hace singular y deben utilizarse los niveles anteriores o un límite controlado.

Para \(z=-ax\), \(w=f(z)\) y una perturbación \(h\), la derivada completa es
\[
\boxed{
D\mathcal R_f[h](x)=
-\frac{h(w)+f'(w)h(z)}a+
\frac{h(1)}a
\left[\mathcal Rf(x)-xf'(w)f'(z)\right].
}
\]
Se deriva usando \(\dot a=-h(1)\), \(\dot z=xh(1)\),
\(\dot w=h(z)+xf'(z)h(1)\) y la variación del denominador. Si \(h(0)=0\), resulta \(D\mathcal R_f[h](0)=0\). La dirección paramétrica inicial HMT es \(h=-u_\eta\).

Esta fórmula incluye la variación de escala; congelar \(a\) daría otro operador linealizado.

## 7. Raíces e itinerarios certificados hasta período 256

Sea \(F_n(\lambda)=f_{\lambda,0}^{2^n}(0)\). Se calcula
\[
x_0=p_0=0,\qquad x_{j+1}=1-\lambda u_0(x_j),\qquad
p_{j+1}=-u_0(x_j)-\lambda u_0'(x_j)p_j.
\]
Entonces \(F_n=x_{2^n}\) y \(F_n'=p_{2^n}\).

El programa adjunto usa intervalos racionales con redondeo entero hacia afuera, raíz cuadrada encerrada por raíz entera y seno/coseno con resto de Taylor explícito. La cota exacta \(|u_0''|\le2\) permite evaluación centrada con resto cuadrático.

Las aproximaciones históricas sólo proponen cajas de radio \(10^{-42}\). Se certifican signos opuestos en sus extremos, \(F_n'\) separado de cero en toda la caja y exclusión de los retornos de períodos propios divisores de \(2^n\). Valor intermedio y monotonía prueban existencia y unicidad local; la exclusión de divisores prueba período mínimo.

| Nivel | Período mínimo | Centro de la caja, redondeado |
|---:|---:|---:|
| 1 | 2 | 1.345913990471832792210949 |
| 2 | 4 | 1.763379787846910127290794 |
| 3 | 8 | 1.850413796950136464530567 |
| 4 | 16 | 1.868979756606798125150574 |
| 5 | 32 | 1.872955034435659740004205 |
| 6 | 64 | 1.873806367467030119412262 |
| 7 | 128 | 1.873988695221365362307169 |
| 8 | 256 | 1.874027744154450672897008 |

La primera raíz tiene la expresión exacta \(\lambda_1=1/u_0(1)\). Las cajas completas y sus comprobaciones están en el certificado JSON.

Se han encerrado los 502 estados preclausura de estos ocho niveles, todos separados de cero, y sus palabras completas de signos. En particular,
\[
\operatorname{sign}f_{\lambda_n,0}^{2^j}(0)=(-1)^j,\qquad0\le j<n.
\]
Quedan acreditadas las orientaciones finitas de los reescalados anteriores a la clausura. Las inclusiones de intervalos restrictivos a todas las escalas constituyen una comprobación adicional.

Para \(\delta_n=(\lambda_{n-1}-\lambda_{n-2})/(\lambda_n-\lambda_{n-1})\), un intervalo decimal exterior abreviado es
\[
\boxed{
4.66921218915020415455609621588966392804
<\delta_8<
4.66921218915020415455609621588966392863.
}
\]
La anchura del intervalo completo es inferior a \(5.808\cdot10^{-37}\). Mide el error numérico de la razón finita \(\delta_8\), distinto del error de aproximación al límite universal.

## 8. Persistencia analítica de las raíces deformadas

Para cada nivel certificado, \(F_n'(\lambda_n)\ne0\). La función implícita produce una rama analítica local \(\lambda_n(\eta)\) con
\[
f_{\lambda_n(\eta),\eta}^{2^n}(0)=0.
\]
Por continuidad, los retornos propios siguen separados de cero para \(\eta\) suficientemente pequeño; se preservan período mínimo e itinerario. La existencia de esos entornos locales queda demostrada. Su anchura común aún no se identifica con toda la franja estructural \(1/40\).

Con \(M=M_{2,\eta}\), la respuesta del perfil es
\[
v_\eta(x)=\partial_\eta u_\eta(x)
=\sum_m\frac{p_m}{12}(1-\cos(k_{m,\eta}x))
-\frac{M'}{2M}\,x u_\eta'(x).
\]
El segundo término conserva la normalización del segundo momento. Si \(q_j=\partial_\eta x_j\) a \(\lambda\) fija,
\[
q_0=0,\qquad q_{j+1}=-\lambda v_\eta(x_j)-\lambda u_\eta'(x_j)q_j,
\qquad
\boxed{\lambda_n'(\eta)=-q_{2^n}/p_{2^n}}.
\]
Así queda explícita la cadena pesos–escala–respuesta–parámetro superestable. Esta no degeneración finita es distinta de la transversalidad asintótica a la hoja estable del punto fijo universal.

## 9. Colas analíticas y propagación del error

Para \(\eta=0\), sean
\[
\mu_{2j}=\frac1{12}\sum_mk_m^{2j},\quad
p_N(z)=\sum_{j=1}^N(-1)^{j+1}\frac{\mu_{2j}}{(2j)!}z^{2j},
\quad\Omega=\frac{70}{\sqrt{899}}.
\]
Si \(q_N=\Omega^2r^2/[(2N+3)(2N+4)]<1\),
\[
\|u_0-p_N\|_r\le
\frac{\mu_{2N+2}r^{2N+2}}{(2N+2)!(1-q_N)}.
\]
La desigualdad \(\mu_{2j+2}\le\Omega^2\mu_{2j}\) domina la cola por una serie geométrica. Para \(0\le s\le2N+2\),
\[
\|(u_0-p_N)^{(s)}\|_r\le
\frac{\mu_{2N+2}r^{2N+2-s}}{(2N+2-s)!}
\left(1-\frac{\Omega^2r^2}{(2N+3-s)(2N+4-s)}\right)^{-1},
\]
cuando el denominador es positivo.

Para transportar errores por un retorno se controlan también sus dominios: si \(\|f-g\|\le\varepsilon\), \(a_f,a_g\ge a_*>0\), las composiciones quedan en un dominio convexo común y allí \(\|f'\|\le L,\ \|g\|\le M\), entonces
\[
\|\mathcal Rf-\mathcal Rg\|_r
\le\varepsilon\left[\frac{1+L+L^2r}{a_*}+\frac{M}{a_*^2}\right].
\]
La prueba suma la perturbación exterior, la interior, el cambio del argumento por \(|a_f-a_g|\le\varepsilon\) y la variación del denominador. Estas cotas evitan reutilizar la suma inicial de cosenos como si todos los perfiles renormalizados conservaran esa misma forma.

## 10. Paso preciso al límite universal

Quedan demostradas la robustez uniforme, la coordenada holomorfa univalente, el transporte reversible de historias finitas, las raíces e itinerarios hasta período 256 y su persistencia analítica local. La certificación incluye siete controles negativos y aritméticos; entre ellos, una raíz de período dos se rechaza como raíz de período mínimo cuatro por la comprobación de divisores propios.

El paso a \(\delta_F=\lim_n\delta_n\) requiere identificar una cascada infinitamente renormalizable en esta familia, controlar su aproximación al punto fijo y acreditar transversalidad en la dirección \(\lambda\). La teoría de universalidad paramétrica de Lyubich hace explícita esa última hipótesis: una familia analítica quadratic-like debe cortar transversalmente la clase híbrida correspondiente. Entonces sus distancias paramétricas satisfacen una ley asintótica \(C\delta_F^{-n}\). [Lyubich, 1999, teorema de universalidad y teorema 9.5](https://www.math.stonybrook.edu/~mlyubich/Archive/Selected/universe.pdf).

Para \(g_N=\mathcal R^N f_{\lambda_*}\), la condición concreta es
\[
\nu_{g_N}\!\left(D\mathcal R^N_{f_{\lambda_*}}[-u_0]\right)\ne0,
\]
donde \(\nu_{g_N}\) es normal a la hoja estable. Usar en su lugar un autovector izquierdo del punto fijo exige controlar también la inclinación de esa hoja. Las fórmulas de sensibilidad y las cotas precedentes preparan ese cálculo sin cambiar el generador.

La negatividad schwarziana y la forma multiplicativa, por sí solas, no implican todas las hipótesis holomorfas de los teoremas de transversalidad. [Levin–Shen–van Strien, §§2 y 7.3](https://arxiv.org/html/1902.06732v2).

Los extremos \(\lambda=0\) y \(2/u_\eta(1)\) producen respectivamente itinerarios \(RRR\ldots\) y \(RLLL\ldots\). Para obtener existencia de una combinatoria infinita intermedia se debe justificar el paso de continuidad de itinerarios en esta normalización. La denominación «familia completa» tiene hipótesis precisas que no se sustituyen por esos dos extremos. [De Melo–van Strien, capítulo II, §§4–5](https://www.ma.imperial.ac.uk/~svanstri/Files/demelo-strien.pdf). Este desarrollo conserva ese paso como obligación específica y no identifica automáticamente las ocho cajas con una única rama principal infinita.

La reconstrucción de rutas y la contracción estable de un operador funcional son propiedades diferentes. Un control explícito lo muestra: para \(f(x)=1-\frac32x^2\), \(a=1/2\), \(h(x)=x^2\), el intervalo \([-1/2,1/2]\) es restrictivo y, sin embargo,
\[
D\mathcal R_f[h](1)=33/8>1=\|h\|_\infty.
\]
Una prueba espectral debe aislar la dirección inestable y controlar las estables. La existencia del punto fijo universal en la literatura constituye un resultado sobre ese operador, distinto de acreditar la intersección de una familia particular. [Lanford, prueba asistida por ordenador](https://repo-archives.ihes.fr/A_GARDER/20180409/Test/I_Prepublications/LANFORD/1968-2013/P_81_17/P_81_17_web.pdf).

El resultado entregado es un encadenamiento ampliado con demostraciones analíticas y certificación finita. La igualdad con el límite universal a profundidad arbitraria conserva las obligaciones asintóticas expresamente identificadas en esta sección.

## Procedencia y reproducción

La fuente focal es el archivo c37_feigenbaum.tex, conservado en:

    output/TRATADO_GENERATIVO_HMT_MD_20260919/REV03/source/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/feigenbaum/c37_feigenbaum.tex

Se consultó también la copia del integral de 2.249 páginas. El resolvedor histórico que informa 2.084 páginas se conserva como registro técnico; ese resultado no sustituye la selección documental posterior.

Deformación y semillas:

    output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_vacancias_criticidad.py
    output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/certificados/vacancias_criticidad.json

Se lee únicamente el miembro de parámetros superestables del sector uniforme como propuestas de cajas. Los valores históricos de las constantes de Feigenbaum quedan fuera de esa lectura.

Antecedente de reconstrucción de ramas:

    output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/TRAZA_GENERATIVA_COORDINADA.md

Reproducción desde la raíz del proyecto, con biblioteca estándar:

    python3 -I -S output/FEIGENBAUM_HMT_DESARROLLO_20260929/certificar_raices.py

El programa genera CERTIFICADO_RAICES_INTERVALOS.json y entrega PASS_LOCAL_FINITE_ROOTS_AND_RATIOS al validar las condiciones numéricas declaradas. Certifica cajas, derivadas, períodos, itinerarios y razones finitas. Los recibos causales documentan procedencia y dependencias; su función es distinta de las demostraciones y del cálculo por intervalos.

<!-- FIN ÍNTEGRO desarrollo -->


---

<!-- COMIENZO ÍNTEGRO prolongacion -->

# Profundidad, memoria y realización de los retornos dodecafásicos

Ampliación demostrativa del 29 de septiembre de 2026. Antecedente conservado: `DESARROLLO_DEMOSTRATIVO_FEIGENBAUM.md` y su certificado racional de ocho raíces. Esta ampliación conserva la familia y los manuscritos publicados.

## 1. Construcción heredada y objeto focal

APP evalúa suma y producto sobre las dos hojas de la retícula de dígitos, conservando cociente y residuo. TRIT determina régimen y orientación. El transporte TPK selecciona, transporta y actualiza el estado con sus registros de acarreo, frontera y memoria. Sus lectores actúan sobre la misma estructura discreta del continuo. La prolongación `w6→w12→w18→w24→w30→R36→G9` conserva esta procedencia; la vuelta nonádica retorna la fase y aumenta la memoria.

El lector crítico de la rueda dodecafásica ya fijado en el corpus produce
\[
\phi_j=\frac{(3j-1)\pi_{\rm HMT}}{18},\qquad
w_j(\eta)=\frac{1+\eta[12\cos(3\phi_j)-\cos(4\phi_j)]}{12},
\]
\[
k_{j,\eta}=\sqrt{\frac2{\sum_\ell w_\ell(\eta)\phi_\ell^2}}\,\phi_j,
\quad u_\eta(x)=\sum_{j=1}^{12}w_j(\eta)(1-\cos(k_{j,\eta}x)),
\quad f_{\lambda,\eta}(x)=1-\lambda u_\eta(x).
\]
Se conserva el representante angular orientado utilizado por el momento. La coordenada \(\pi_{\rm HMT}\) es una salida anterior de la misma construcción; su factor se cancela en las frecuencias normalizadas del sector uniforme. \(\lambda\) es el parámetro libre de esta familia posterior. La cifra objetivo de Feigenbaum permanece fuera de sus entradas.

El desarrollo antecedente demuestra, para \(|\eta|\le1/40\), pesos positivos de suma uno, \(\sum w_jk_j^2=2\), \(0<k_j<3<\pi\), criticidad cuadrática, crecimiento estricto de \(u_\eta\) en \((0,1]\), y
\[
f_{\lambda,\eta}([-1,1])\subseteq[-1,1],\qquad
S f_{\lambda,\eta}(x)\le-640/47647<0
\]
para \(0<\lambda\le2/u_\eta(1)\) y \(0<|x|\le1\).

Esta ampliación compone tres operaciones recuperadas: el refinamiento con acarreo de XI, los lectores cilíndricos del álgebra holonómica y la conservación bilateral de memoria. El horizonte de iteración, la profundidad de lectura y el calendario TPK conservan sus dominios distintos.

## 2. Crecimiento exterior y resolución interior

La ley de refinamiento del artículo XI, con base entera \(B\ge2\), es
\[
L_c(x,y)=(Bx-c,By+c),\qquad 0\le c<B.
\]
Para una palabra \(c_1\ldots c_m\), su registro es
\[
C_m=\sum_{j=1}^m c_jB^{m-j},\qquad
(x_m,y_m)=(B^mx_0-C_m,B^my_0+C_m).
\]
La suma exterior vale \(B^mM_0\), con \(M_0=x_0+y_0\). La lectura normalizada del registro pertenece al cilindro
\[
I_m(C_m)=\left[\frac{C_m}{B^m},\frac{C_m+1}{B^m}\right],
\qquad \operatorname{diam}I_m=B^{-m}.
\]
La pareja entera y la escala recuperan los cocientes, residuos y ceros iniciales de la palabra. Los extremos con doble expansión conservan su marca de frontera. Así se coordinan crecimiento de soporte y refinamiento de lectura sin identificar historias distintas por su sola imagen límite.

La composición es exacta:
\[
L_D^{[b]}\circ L_C^{[a]}=L_{B^bC+D}^{[a+b]}.
\]
Por asociatividad, agrupar una historia de dieciocho eventos en nueve bloques de dos o en dos bloques de nueve produce el mismo registro. A nivel de retorno \(2^N\), el horizonte común es \(9\,2^N\). La prueba es una igualdad de composición sobre la misma historia ordenada; mantiene sus acarreos y sus subbloques recuperables.

El cristal aporta la formulación de límites:
\[
X_\infty=\varprojlim X_m,\qquad
r^*a=a\circ r,\qquad
r^*e_x=\sum_{r(y)=x}e_y,
\qquad \mathfrak H_{\rm cyl}=\varinjlim\mathfrak H_m.
\]
Los estados se restringen; los lectores se prolongan. La preimagen preserva productos, unidad e idempotentes. Una familia exactamente compatible induce un lector en el límite directo. Los aproximantes que sólo son compatibles hasta error requieren, además, una estimación de convergencia en su completación. La sección siguiente proporciona esa estimación para el retorno crítico.

### Capacidad y vacancias del registro

El lector de capacidad de XI compara bloques de \(729\) y \(1000\) posibilidades. Con \(\rho=\log_{1000}729=\log_{10}9\), conserva
\[
\mathcal C_k=\lfloor(k+1)\rho\rfloor,\qquad
\mathcal C_k-\mathcal C_{k-1}=1-z_k,
\]
\[
\mathcal C_b-\mathcal C_a+\sum_{k=a+1}^b z_k=b-a,
\qquad T_{\rm cap}(a)=\lceil a/\rho\rceil-1\quad(a\ge1).
\]
Cada vacancia registra una transición durante la cual se mantiene la capacidad; la longitud cronológica queda conservada en el balance. La fase de capacidad y la fase cronológica son lectores distintos.

Para almacenar un prefijo de \(m\) dígitos de base nueve, una capacidad decimal suficiente es
\[
a(m)=\left\lceil\frac{m\rho}{3}\right\rceil.
\]
El cociente y el residuo permiten convertir el entero \(C_m\) entre bases, manteniendo aparte la profundidad \(m\). Se cumplen
\[
9^m\le1000^{a(m)}\le729^{T_{\rm cap}(a(m))+1}.
\]
Estas desigualdades también se deciden mediante potencias enteras, sin redondear logaritmos. El presupuesto de lectura de la sección siguiente se traduce así a capacidad del registro conservando las unidades. Esta cuenta dimensiona el almacenamiento; las reglas de supervivencia determinan, adicionalmente, qué historias nativas son admisibles.

## 3. Presupuesto explícito de profundidad para cada retorno

**Teorema.** Fijado \(|\eta|\le1/40\), normalícense
\[
t=\lambda u_\eta(1)/2\in[0,1],\qquad z=(x+1)/2,
\]
\[
F_{t,\eta}(z)=1-t\frac{u_\eta(2z-1)}{u_\eta(1)},\qquad z\in[0,1].
\]
Para todo entero \(q\ge1\) y dos parámetros \(t,s\),
\[
\left|F_{t,\eta}^{q}(1/2)-F_{s,\eta}^{q}(1/2)\right|
\le S_q|t-s|,
\qquad S_q=\sum_{j=0}^{q-1}(6\sqrt2)^j<9^q.
\]
En consecuencia, un cilindro de parámetros en base nueve, de profundidad \(m=2^N+r\), encierra la lectura del retorno \(q=2^N\) en un intervalo de diámetro inferior a \(9^{-r}\).

**Demostración.** La función \((1-\cos v)/v^2\) decrece para \(0<v<\pi\): el signo de su derivada es el de \(v\sin v-2(1-\cos v)\), negativo porque \(\tan(v/2)>v/2\). Por el segundo momento,
\[
u_\eta(1)\ge\frac{1-\cos3}{9}\sum_jw_jk_j^2
=\frac{2(1-\cos3)}9>\frac13.
\]
La última desigualdad se verifica, por ejemplo, acotando \(\cos3\) mediante su suma de Taylor alternada hasta grado ocho, que es menor que \(-1/2\). Además, Cauchy–Schwarz da \(|u_\eta'(x)|\le\sqrt2\) en la recta real. Se deduce
\[
\operatorname{Lip}_zF_{t,\eta}\le6\sqrt2<9,\qquad
\operatorname{Lip}_tF_{t,\eta}\le1.
\]
Si \(d_j\) es la diferencia entre las dos órbitas, entonces \(d_0=0\) y \(d_{j+1}\le6\sqrt2\,d_j+|t-s|\). La inducción prueba la suma geométrica. Para \(|t-s|\le9^{-m}\), el diámetro es menor que \(9^{q-m}\). Sustituir \(q=2^N\) y \(m=q+r\) termina la prueba. □

La cota controla la incertidumbre de parámetro con \(\eta\) fijado. Una implementación añade y propaga separadamente el error de evaluación de cosenos y de redondeo; el certificado racional antecedente ofrece esas operaciones. La cota es suficiente y conservadora, con coste que crece con el horizonte.

**Lector límite.** Realícese \(t\) desde \((x_0,y_0)=(1,0)\), \(B=9\), de modo que
\[
(x_m,y_m)=(9^m-C_m,C_m),\qquad t_m=C_m/9^m.
\]
Los lectores \(E_{q,m}=F_{t_m,\eta}^{q}(1/2)\), llevados a un nivel común, cumplen
\[
\|E_{q,m+a}-r^*E_{q,m}\|_\infty\le S_q9^{-m}.
\]
Convergen uniformemente a un lector continuo \(E_q\) en la completación del álgebra cilíndrica. La versión conjuntista
\[
J_{q,m}(C)=\{F_{t,\eta}^{q}(1/2):t\in I_m(C)\}
\]
es exactamente anidada y sus diámetros tienden a cero. Este resultado da el paso al límite de la **lectura a horizonte fijo**, con control de profundidad a cualquier horizonte solicitado.

## 4. Palabra de duplicación y lector nonádico de la cronología

Los ocho itinerarios certificados en el antecedente obedecen
\[
W_1=+,\qquad W_{n+1}=W_n\,(-1)^n\,W_n.
\]
Su continuación prefijal única es
\[
\tau_j=(-1)^{v_2(j)},\qquad j\ge1;
\qquad \tau_{2j}=-\tau_j,\quad\tau_{2j+1}=+.
\]
La prueba utiliza \(v_2(2^n+r)=v_2(r)\) para \(0<r<2^n\). Es una recurrencia a toda profundidad, y la coincidencia con los ocho retornos calculados constituye su comprobación finita en la familia.

En el orden lexicográfico con paridad de un mapa con máximo crítico, el factor de orientación previo al lugar \(k\) es \(\prod_{j<k}(-\tau_j)\). La palabra \(\tau\) es estrictamente mayor que cualquiera de sus desplazamientos positivos. En efecto, el primer desacuerdo con un desplazamiento impar ocurre en \(k=1\) o \(2\); un desplazamiento par reduce la comparación a la mitad y duplica \(k\). Por tanto el primer desacuerdo está en \(k=2^r\). Allí
\[
\prod_{j<2^r}(-\tau_j)=(-1)^r=\tau_{2^r},
\]
y la diferencia orientada con el signo opuesto es positiva. Esta demostración también prueba aperiodicidad.

El registro cronológico conserva
\[
K=\rho_9(K)+9q_9(K).
\]
Su lector diádico es
\[
\ell_n(B_K)=[\rho_9(K)+9q_9(K)]_{2^n}=[K]_{2^n}.
\]
Sobre la carta de historias en que \(\Gamma_9 B_K=B_{K+9}\),
\[
\ell_n(\Gamma_9B_K)=\ell_n(B_K)+9\pmod{2^n},\qquad
\pi_{n+1,n}\ell_{n+1}=\ell_n.
\]
Como nueve es impar, el avance por nueve visita las \(2^n\) posiciones. Su conjugación con el avance unitario es \(j\mapsto9j\). Para \(0<j<2^n\),
\[
v_2(9j\bmod2^n)=v_2(j),
\]
de modo que el remuestreo nonádico conserva también la palabra orientada en cada ciclo certificado.

Este lector utiliza residuo **y** cociente. Las fases de \(K=1\) y \(K=10\) coinciden módulo nueve, mientras sus signos diádicos son opuestos. La memoria distingue las dos historias. La propiedad aritmética del remuestreo vale para todo multiplicador impar; el calendario HMT fija aquí la elección de nueve.

## 5. Memoria bilateral compatible a profundidad infinita

Sean \(\mathcal H_n=\ell^2(\mathbb Z/2^n\mathbb Z)\),
\[
C_ne_j=e_{j+1},\qquad
J_ne_j=(e_j+e_{j+2^n})/\sqrt2.
\]
Una comprobación sobre la base da \(J_n^*J_n=I\) y \(C_{n+1}J_n=J_nC_n\), incluidos los términos de borde.

El artículo XI aporta los proyectores
\[
P_0=\frac19\begin{pmatrix}8&-\sqrt8\\-\sqrt8&1\end{pmatrix},\qquad
P_1=\frac19\begin{pmatrix}1&\sqrt8\\\sqrt8&8\end{pmatrix}.
\]
Son ortogonales y complementarios. Por tanto
\[
\mathbb U_n=P_0\otimes I+P_1\otimes C_n
=\begin{pmatrix}T_n&D_n\\D_n&R_n\end{pmatrix}
\]
es unitario, con
\[
T_n=(8I+C_n)/9,\quad D_n=\sqrt8(C_n-I)/9,\quad R_n=(I+8C_n)/9.
\]
La naturalidad ya probada implica
\[
\mathbb U_{n+1}(I_2\otimes J_n)=(I_2\otimes J_n)\mathbb U_n,
\quad \mathbb U_n^a=P_0\otimes I+P_1\otimes C_n^a
\quad(a\in\mathbb Z).
\]
El límite de Hilbert se identifica con \(L^2(\mathbb Z_2,\mu_{\rm Haar})\), llevando \(e_j^{(n)}\) a \(2^{n/2}\mathbf1_{j+2^n\mathbb Z_2}\). Las identidades se prolongan por densidad y acotación. Para todo vector \(v\) y todo tiempo entero \(a\),
\[
\boxed{\|T_{\infty,a}v\|^2+\|D_{\infty,a}v\|^2=\|v\|^2,}
\]
\[
\boxed{v=T_{\infty,a}^*(T_{\infty,a}v)+D_{\infty,a}^*(D_{\infty,a}v).}
\]
Aquí \(T_{\infty,a}=(8I+C_\infty^a)/9\). La composición bilateral conserva el archivo entre pasos; componer solamente \(T_n\) describe otra operación.

La permutación \(S_ne_j=e_{9j\bmod2^n}\) satisface
\[
S_{n+1}J_n=J_nS_n,\qquad S_nC_nS_n^{-1}=C_n^9.
\]
Así se obtiene en el límite
\[
S_\infty C_\infty S_\infty^{-1}=C_\infty^9,
\quad (I_2\otimes S_\infty)\mathbb U_\infty
(I_2\otimes S_\infty^{-1})=\mathbb U_\infty^9.
\]
La representación temporal es fiel: \(C_\infty^a=C_\infty^b\) fuerza \(2^n\mid a-b\) para todo \(n\), de donde \(a=b\). Preparaciones particulares pueden conservar simetrías temporales. La identidad operatoria conserva esta distinción.

El punto proyectivo \(([K]_{2^n})_n\) y un vector de \(L^2\) tienen tipos diferentes: una historia puntual induce una Dirac, mientras las amplitudes normalizables pertenecen al espacio de Hilbert. El resultado construye un lector equivarante de la cronología; las restantes coordenadas nativas del TPK acompañan el registro completo.

## 6. Existencia y separación de las obligaciones asintóticas

### 6.1. Realización de la palabra infinita en toda la franja

**Teorema de existencia.** Para cada \(|\eta|\le1/40\) existe al menos un
\[
\lambda_\infty(\eta)\in
\left[\frac1{2u_\eta(1)},\frac2{u_\eta(1)}\right]
\]
tal que
\[
\boxed{\operatorname{sign}f_{\lambda_\infty(\eta),\eta}^{j}(0)
=(-1)^{v_2(j)}\quad\text{para todo }j\ge1.}
\]
La conclusión realiza el itinerario infinito de duplicación dentro de la familia fijada. El cuantificador de existencia se mantiene separado de una selección única y de la ley de distancias entre parámetros superestables.

**Demostración.** Fijamos \(\eta\). Escribimos \(K_\lambda\) para la palabra de signos de la órbita crítica; cuando ésta retorna por primera vez a cero, la palabra termina en ese cero. Usamos el orden unimodal con máximo, cuyo factor antes de comparar el símbolo \(j\) es el producto de los signos \(-K_i\), \(i<j\).

En el extremo izquierdo la imagen de todo el intervalo está en \([1/2,1]\); por tanto \(K_-=+++\cdots\). En el extremo derecho la órbita es \(0\mapsto1\mapsto-1\mapsto-1\), de donde \(K_+=+---\cdots\). Comparando los símbolos segundo y tercero, respectivamente, se obtiene
\[
K_-<\tau<K_+.
\]

Si \(K_{\lambda_0}\) es infinita y distinta de \(\tau\), la primera diferencia ocurre en un lugar finito. La continuidad de los correspondientes iterados hace localmente constante el lado de la comparación. Queda examinar un parámetro superestable, de primer período \(p\), con palabra \(W0\), donde \(|W|=p-1\).

Para \(\lambda\) cercano a \(\lambda_0\), sea \(g_\lambda=f_{\lambda,\eta}^p\) y \(a=g_\lambda(0)\). Se tiene \(g_\lambda'(0)=0\), y una cota local uniforme de la segunda derivada da
\[
g_\lambda(x)=a+O(x^2).
\]
Para \(|a|\) suficientemente pequeño y distinto de cero, \(g_\lambda\) lleva \([-2|a|,2|a|]\) en \([a-|a|/2,a+|a|/2]\). Los retornos conservan el signo de \(a\), y las \(p-1\) posiciones intermedias conservan \(W\). Las palabras vecinas son, por ello, \((W+)^\infty\) o \((W-)^\infty\); los parámetros con \(a=0\) conservan \(W0\).

Si \(\tau\) difiere de \(W\) antes del lugar \(p\), esa diferencia fija el mismo lado para las tres palabras. Si comparte \(W\), pongamos
\[
s=\tau_p,\qquad e=\prod_{j<p}(-\tau_j),\qquad A=Ws.
\]
El signo de la comparación de \(\tau\) con \(W0\) y con \((W,-s)^\infty\) es \(es\). Para compararla con \(A^\infty\), sea \(q\) el primer lugar en que \(\tau_{p+q}\ne\tau_q\). Existe por aperiodicidad. Hasta el lugar \(p+q-1\), ambas palabras coinciden, y el signo de orientación se factoriza como \(O_pO_{q-1}\), con \(O_p=-es\). La maximalidad estricta ya demostrada da
\[
O_{q-1}(\tau_q-\tau_{p+q})>0.
\]
En consecuencia, la comparación de \(\tau\) con \(A^\infty\) tiene signo \(-O_p=es\). Las tres posibilidades locales están al mismo lado de \(\tau\).

Si ningún parámetro realizara \(\tau\), los conjuntos \(\{\lambda:K_\lambda<\tau\}\) y \(\{\lambda:K_\lambda>\tau\}\) serían abiertos, disjuntos, no vacíos y cubrirían el intervalo de parámetros. La conexidad del intervalo excluye esa partición. Existe, por tanto, el parámetro anunciado. □

Este argumento de continuidad de itinerarios se aplica después de fijar el generador HMT y su familia analítica; sus hipótesis se verifican aquí directamente. La construcción conserva la palabra infinita sin introducir como dato un parámetro de la familia cuadrática ni el valor universal.

### 6.2. Márgenes que impiden perder el itinerario al tomar límites

Escribamos \(c_p=f_{\lambda,\eta}^p(0)\). Una cota racional uniforme suficiente es
\[
|f'|,|f''|\le16,\qquad
B_p:=16^p\frac{16^p-1}{15}\ge\|(f^p)''\|_{[-1,1]}.
\]
En efecto, \(1-\cos v\ge v^2/2-v^4/24\ge v^2/8\) para \(|v|\le3\), de modo que \(u_\eta(1)\ge1/4\), \(\lambda\le8\) y ambas derivadas se acotan por \(16\), usando los momentos. La regla de la cadena prueba por inducción la cota \(B_p\).

La palabra \(\tau\) satisface \(\tau_{2p}=-\tau_p\) para todo \(p\). Para cualquiera de sus realizaciones, \(c_{2p}\) y \(c_p\) tienen signos opuestos. Como \((f^p)'(0)=0\), Taylor da
\[
|c_{2p}-c_p|\le\tfrac12B_p|c_p|^2.
\]
El lado izquierdo es mayor que \(|c_p|\), y por tanto
\[
\boxed{|c_p|>2/B_p>0.}
\]
Para cada horizonte fijo existe así un margen uniforme que impide que una sucesión de realizaciones pierda su signo al converger. En las coordenadas compactas \((\eta,b)\), \(b=\lambda u_\eta(1)\in[1/2,2]\), el conjunto de realizaciones de \(\tau\) es cerrado y compacto, y su proyección sobre toda la franja de \(\eta\) es sobreyectiva.

El mismo argumento sirve para un árbol de prefijos: si se realizan todos los prefijos de \(\tau\), una subsucesión compacta conserva cada signo, porque los prefijos suficientemente largos incluyen simultáneamente los lugares \(p\) y \(2p\). El teorema de existencia proporciona ahora la no vacuidad que ese argumento necesita.

### 6.3. Intervalos invariantes de retorno a todos los niveles

**Teorema de retornos anidados.** Para cualquiera de las realizaciones del teorema 6.1, sean \(c_j=f^j(0)\) y
\[
J_n=\operatorname{conv}\{c_{2^n},c_{2^{n+1}}\},\qquad n\ge1.
\]
Entonces \(0\in\operatorname{int}J_n\), \(J_{n+1}\subset J_n\),
\[
f^{2^n}(J_n)=J_n,
\]
y las \(2^n\) imágenes \(J_n,f(J_n),\ldots,f^{2^n-1}(J_n)\) son disjuntas. Los retornos normalizados son unimodales de máximo, con valor crítico uno y la misma palabra \(\tau\). Estos intervalos son núcleos invariantes de retorno; una normalización que exija extremos periódicos puede ampliar el núcleo al intervalo restrictivo maximal correspondiente y debe especificar ese paso.

**Demostración del primer retorno.** Sea \(F\) un mapa unimodal de máximo con \(F(0)=1\) y palabra \(\tau\), y \(d_j=F^j(0)\). Sus primeros signos son \(+,-,+,+,+,-,+\). El intervalo \(I=[d_2,1]\) es invariante: \(F(d_2)=d_3>0\), \(F(1)=d_2<0\), y el máximo es uno. Pongamos \(J=[d_2,d_4]\). Como \(F\) decrece en positivos y
\[
F(d_3)=d_4>0> d_6=F(d_5),
\]
se tiene \(d_3<d_5\), y por tanto \(F(J)=[d_3,1]\).

Además \(d_3>d_4\). Para comprobarlo, \(F^2\) es estrictamente creciente entre los dos puntos positivos \(d_3,d_4\), porque sus imágenes \(d_4,d_5\) son positivas. Sus valores son \(F^2(d_3)=d_5>0>d_6=F^2(d_4)\), lo que fuerza ese orden. Así \(J\) y \(F(J)\) quedan separados por un intervalo abierto, y
\[
F^2(J)=F([d_3,1])=[d_2,d_4]=J.
\]
El mapa \(F^2|_J\) tiene un único mínimo crítico: la imagen \(F(J)\) permanece positiva. La conjugación \(h(x)=d_2x\) invierte orientación y normaliza el retorno como máximo con valor uno. Su itinerario es
\[
\operatorname{sign}\frac{d_{2j}}{d_2}
=-\tau_{2j}=\tau_j.
\]
Se puede repetir el mismo argumento a cualquier profundidad.

**Disjunción inductiva.** Supónganse disjuntas las \(p=2^n\) imágenes del padre \(J_n\), y sea \(g=f^p\). El primer retorno aplicado al mapa normalizado produce \(B=J_{n+1}\), \(A=g(B)\), con \(A\cap B=\varnothing\), \(g(B)=A\), \(g(A)=B\). Para \(0\le j<p\), una intersección de \(f^j(A)\) y \(f^j(B)\), al aplicarle \(f^{p-j}\), produciría una intersección de \(B\) y \(A\). Por tanto esas dos imágenes son disjuntas. Las imágenes correspondientes a distintos \(j\) pertenecen a imágenes disjuntas del padre. Quedan demostradas las \(2p\) imágenes disjuntas y el retorno \(f^{2p}(B)=B\). La fórmula de los extremos resulta de componer las normalizaciones \(x\mapsto c_{2^n}x\). □

Los conjuntos compactos
\[
\Lambda_n=\bigcup_{0\le j<2^n}f^j(J_n)
\]
son no vacíos y anidados. Su intersección \(\Lambda_\infty\) tiene un lector continuo sobre el odómetro diádico: a cada punto se le asigna la etiqueta de la única componente que ocupa a cada nivel. Todas las sucesiones compatibles de etiquetas tienen preimagen por compacidad, y el avance por \(f\) suma uno en las etiquetas. Esta aplicación es una semiconjugación sobreyectiva. Para promoverla a conjugación puntual se requiere demostrar que los diámetros de las componentes tienden a cero; esa promoción métrica se mantiene separada.

### 6.4. Alcance matemático del avance

Quedan demostrados el lector crítico con precisión a horizonte arbitrario, la realización del itinerario infinito para toda la franja declarada, sus intervalos invariantes de retorno a todos los niveles, la conservación bilateral en el límite de refinamiento y la compatibilidad de su cronología con la lectura nonádica. Las pruebas utilizan el crecimiento de soporte, las reglas de acarreo y los lectores ya construidos en HMT, junto con el análisis explícito de la familia que éstos publican.

La teoría de universalidad paramétrica de Lyubich distingue la combinatoria de duplicación de la transversalidad respecto de la hoja estable de renormalización. Su resultado proporciona el marco de reconocimiento posterior; las hipótesis de normalización y transversalidad de la familia concreta deben conservarse al aplicarlo. Véase [Lyubich, *Feigenbaum–Coullet–Tresser Universality and Milnor’s Hairiness Conjecture*](https://www.math.stonybrook.edu/~mlyubich/Archive/Selected/universe.pdf).

El siguiente enunciado métrico conserva todavía obligaciones específicas:
\[
\lim_{n\to\infty}
\frac{\lambda_{n-1}-\lambda_{n-2}}{\lambda_n-\lambda_{n-1}}
=\delta.
\]
Se requiere identificar la cascada elegida, transportar sus retornos al dominio funcional del renormalizador y certificar la proyección inestable del vector paramétrico, junto con el control de colas que permita pasar de certificados finitos al límite. Los ocho intervalos de raíces previos conservan su validez y su significado local. La existencia demostrada aquí permite una realización infinita; por sí sola no prueba que esos ocho intervalos sean los primeros elementos de una única cascada global.

Un falsador distingue ambas obligaciones: una reparametrización tangente \(\lambda-\lambda_\infty=s^p\) conserva las órbitas y sus historias, mientras una ley \(\lambda_n-\lambda_\infty\sim C\delta^{-n}\) pasa a \(s_n\sim C^{1/p}\delta^{-n/p}\). La nueva razón de diferencias converge a \(\delta^{1/p}\). Por eso el control de la escala paramétrica aporta información adicional a la memoria y a la profundidad.

El resultado infinito presente pertenece a la construcción y persistencia del itinerario, a la precisión de sus lectores y a la restitución operatoria. La identificación decimal universal queda separada con esa obligación concreta, sin convertir una razón finita en un certificado asintótico.

## 7. Procedencia material y controles

1. Familia crítica y ocho raíces: `DESARROLLO_DEMOSTRATIVO_FEIGENBAUM.md`, §§1–10, y `CERTIFICADO_RAICES_INTERVALOS.json`, conservados en este directorio.
2. XI, paquete español de memoria de 22 de septiembre de 2026: `output/INSERCIONES_MEMORIA_COMPATIBILIDAD_SERIE_20260922/PAQUETES/staging/20260922T150204Z_d4ab7bd9/ES/10_MEMORIA_COMPATIBILIDAD_ES_20260922/antecedentes/paquete_predecesor/source/libro/03_refinamiento.tex`, líneas 174–417; `05_levantamiento.tex`, líneas 150–232.
3. Mismo paquete, `modulos/10_holonomia_memoria.tex`, líneas 12–38: representación bilateral; líneas 134–140: amplificación compatible.
4. Cristal, `output/DOBLE_PROYECCION_HOLOGRAFICA_CRISTAL_TEMPORAL_APERIODICO_MONOGRAFIA_AUTOSUFICIENTE/manuscrito/generated/algebra_holonomica.tex`, líneas 183–290: cociclo, sistemas de estados y lectores, graduación de memoria.
5. Núcleo permanente, `PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE/TPK_GRAFO_OPERATORIO_TIPADO.json`: OP02, OP17 y estado enriquecido. La genealogía común se hereda con sus propietarios; esta ampliación demuestra sus lectores focales.
6. XI, fuente activa `output/INSERCIONES_MEMORIA_COMPATIBILIDAD_SERIE_20260922/ARTICULOS/10/ES/source/sections/vacancias_capacidad.tex`: capacidad, vacancias, unidades y reloj inverso.

Los controles de cálculo de este directorio comprueban instancias exactas de las identidades, las palabras certificadas y falsadores de pérdida de memoria. Las pruebas escritas por inducción, continuidad y paso al límite fundamentan el alcance infinito. Los verificadores de genealogía controlan procedencia y roles causales.

<!-- FIN ÍNTEGRO prolongacion -->


---

<!-- COMIENZO ÍNTEGRO escalado -->

# Transversalidad, convergencia y escalado de la cascada crítica HMT

Desarrollo acumulativo del 29 de septiembre de 2026. Se conservan íntegramente `DESARROLLO_DEMOSTRATIVO_FEIGENBAUM.md`, `PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md`, sus programas y sus certificados. Esta ampliación introduce una prueba cuantitativa de entrada, una construcción de la hoja estable y el escalado paramétrico local. Los manuscritos publicados permanecen inalterados.

**Resultado acumulativo de §§14–17.** La primera raíz nueva existe a todos los niveles, conserva la palabra canónica de duplicación y converge al cruce estable certificado. La prueba de primera salida identifica los límites global y local; la unicidad de intersección con las clases híbridas identifica finalmente sus centros. Para la familia uniforme HMT, el cociente de los intervalos sucesivos de las raíces originales converge a \(\delta\), con resto de potencia. Las reservas conservadas en las etapas anteriores quedan resueltas con el alcance y las dependencias explícitas de §§16–17. Las constantes numéricas del resto paramétrico y el error del octavo cociente respecto al límite permanecen diferenciados de esta demostración de convergencia.

## 1. Procedencia y resultado

APP evalúa suma y producto sobre las dos hojas de la retícula, conservando cociente y residuo. TRIT determina régimen y orientación. El transporte TPK selecciona, transporta y actualiza el estado con sus registros de acarreo, frontera y memoria. Sus lectores actúan sobre la misma estructura discreta del continuo. La prolongación `w6→w12→w18→w24→w30→R36→G9` conserva esta procedencia y distingue retorno de fase de incremento de memoria.

El lector crítico de la rueda dodecafásica, construido en los propietarios citados en §11 y transportado en los dos desarrollos antecedentes, produce
\[
\phi_j=\frac{(3j-1)\pi_{\mathrm{HMT}}}{18},\qquad
w_j=\frac1{12},\qquad
k_j=\sqrt{\frac2{\sum_{\ell=1}^{12}w_\ell\phi_\ell^2}}\,\phi_j
=\frac{2(3j-1)}{\sqrt{899}}.
\]
La coordenada \(\pi_{\mathrm{HMT}}\) conserva su origen APP–TRIT–TPK; su factor común se cancela en este segundo momento. El lector resultante es
\[
u_0(x)=\frac1{12}\sum_{j=1}^{12}(1-\cos k_jx),\qquad
f_\lambda(x)=1-\lambda u_0(x).
\tag{1}
\]
El sector focal es el uniforme, \(\eta=0\). La ampliación antecedente conserva por separado la familia ponderada \(|\eta|\le1/40\). Las nuevas cotas numéricas corresponden a (1).

La familia es par, entera, con \(f_\lambda(0)=1\), crítico cuadrático y segundo momento \(\sum_jw_jk_j^2=2\). El parámetro \(\lambda\) recorre una familia posterior al generador HMT. La constante objetivo de Feigenbaum permanece fuera de las entradas de (1).

**Resultado principal.** Existe un único
\[
\lambda_*\in[1.874038,1.874039]
\tag{2}
\]
para el que el cuarto retorno normalizado de (1) pertenece a la hoja estable local del punto fijo real de duplicación. El cruce de la familia con esa hoja es transversal, con separación cuantificada. Para todo \(n\ge0\),
\[
\boxed{\|R^{4+n}f_{\lambda_*}-g\|_{\mathcal A}
<0.001666\,(0.83996)^n.}
\tag{3}
\]
La cascada superestable local asociada a este cruce posee parámetros \(\mu_j\) y constantes \(C\ne0\), \(0<\theta<1\), tales que
\[
\mu_j-\lambda_*=C\delta^{-j}\bigl[1+O(\theta^j)\bigr],
\qquad
\frac{\mu_{j-1}-\mu_{j-2}}{\mu_j-\mu_{j-1}}\longrightarrow\delta.
\tag{4}
\]
Aquí \(\delta>1\) es el autovalor inestable del operador de duplicación. La selección de \(\mu_j\) se realiza mediante los retornos locales de §8. La obligación adicional de identificación con el selector global, formulada en §10 durante la etapa intermedia, queda satisfecha en §§15–17: todos los términos globales conservan la combinatoria y los centros coinciden para todo nivel suficientemente alto al igualar sus períodos.

## 2. Carta analítica y retorno efectivo

Se emplea la carta de funciones pares
\[
s=x^2,\qquad z=\frac{s-1}{5/2},\qquad
f(x)=1-x^2V(z),\qquad V(z)=\sum_{j\ge0}v_jz^j.
\]
Las coordenadas del espacio de Banach son
\[
u=10v_0,\qquad \nu=(v_1,v_2,\ldots),\qquad
\|(\Delta u,\Delta\nu)\|_{\mathcal A}
=|\Delta u|+\sum_{j\ge1}|\Delta v_j|.
\tag{5}
\]
En particular, el coeficiente constante de \(V\) tiene peso diez. Esta normalización coincide con la carta \(u/10\) de Hertling–Spandl, §2.

Sea \(a=-f(1)=v_0-1\). Para los retornos reales admisibles,
\[
(Rf)(x)=-\frac{f(f(-ax))}{a}.
\tag{6}
\]
El programa evalúa una factorización exacta de (6). Definiendo
\[
S=\frac{a^2s-1}{5/2},\qquad b=V(S),\qquad
h=1-a^2sb,\qquad t=\frac{h^2-1}{5/2},
\]
\[
\operatorname{shift}V(z)=\sum_{j\ge0}v_{j+1}z^j,
\]
resulta
\[
\boxed{V_R=a\,b\,(h+1)\left[V(t)+\frac25\operatorname{shift}V(t)\right].}
\tag{7}
\]
Para comprobarla, se usa \(v_0=1+a\),
\(h^2-1=-a^2sb(h+1)\) y
\(V(t)-v_0=t\operatorname{shift}V(t)\). Así,
\(a+1-h^2V(t)=a^2sb(h+1)[V(t)+(2/5)\operatorname{shift}V(t)]\),
que es precisamente \(asV_R\).

Los momentos iniciales son racionales:
\[
\frac1{12}\sum_jk_j^{2m}
=\frac1{12}\left(\frac4{899}\right)^m
\sum_{j=1}^{12}(3j-1)^{2m}.
\tag{8}
\]
Por ello, tanto (7) como la construcción inicial utilizan intervalos racionales; las funciones trigonométricas iniciales se representan por sus series con resto exterior.

## 3. Cotas externas utilizadas como reconocimiento posterior

Una vez construida (1), se utiliza el teorema de hiperbolicidad de Lanford como certificado analítico del operador (6). Sean \(g_0\) el polinomio central publicado y \(g\) el punto fijo. Las estimaciones utilizadas son
\[
\|g-g_0\|_{\mathcal A}<\varepsilon_0=4\,10^{-5},
\]
y, en la bola \(\|f-g_0\|_{\mathcal A}<0.01\), los bloques de \(DR\), escritos \(R=(U,V)\), satisfacen
\[
U_u\ge a_0=4.521,\quad
\|U_\nu\|\le b_0=0.560,\quad
\|V_u\|\le c_0=0.756,\quad
\|V_\nu\|\le d_0=0.719.
\tag{9}
\]
El punto fijo posee una única dirección inestable, con autovalor real positivo \(\delta>1\); el resto del espectro queda dentro del disco unidad. Las cifras de (9) proceden de las estimaciones publicadas, no de una nueva reproducción de la prueba de Lanford en este expediente. Los coeficientes de \(g_0\) están incorporados explícitamente en `CENTRE` del programa, conforme a la tabla 2 de Hertling–Spandl.

Fuentes: [Lanford, estimaciones de hiperbolicidad](https://repo-archives.ihes.fr/A_GARDER/20180409/Test/I_Prepublications/LANFORD/1968-2013/P_81_17/P_81_17_web.pdf); [Hertling–Spandl, carta analítica y tabla 2](https://arxiv.org/pdf/1410.3277).

## 4. Certificado racional de entrada y dirección

`certificar_entrada_renormalizacion.py` divide (2) en dieciséis intervalos racionales iguales. Propaga cuatro retornos de (7) y la derivada exacta respecto a \(\lambda\), usando diferenciación de la composición y redondeo exterior a cien posiciones decimales.

Cada serie consta de un polinomio de grado 32 con coeficientes intervalares y un error analítico arbitrario \(E\), \(\|E\|_1\le\epsilon\). Este error puede modificar también coeficientes bajos. Para \(\|q\|_1<1\),
\[
\|E\circ q\|_1\le\epsilon,\qquad
\|E'\circ q\|_1\le\frac{\epsilon}{(1-\|q\|_1)^2},\qquad
\|\operatorname{shift}E\|_1\le\epsilon.
\tag{10}
\]
Los productos incluyen los términos polinomio–error y error–error. La cola inicial se acota por su primer término absoluto y una razón geométrica, utilizando \(\|1+(5/2)z\|_1=7/2\). Cada argumento compuesto permanece estrictamente dentro de la bola unidad de esta álgebra.

Para \(\Gamma(\lambda)=R^4f_\lambda=(u_\lambda,\nu_\lambda)\), el certificado da las siguientes cotas conservadoras, uniformes en (2):

| Cantidad | Cota certificada exterior |
|---|---:|
| \(\|\Gamma(\lambda)-g_0\|_{\mathcal A}\) | \(<0.004993128\) |
| \(\|\nu_\lambda-\nu_{g_0}\|_1\) | \(<0.001396077\) |
| \(u'_\lambda\) | \(>3821.289115\) |
| \(\|\nu'_\lambda\|_1\) | \(<551.757000\) |
| \(\|\nu'_\lambda\|_1/u'_\lambda\) | \(<0.144386<1/4\) |
| Error analítico de la función | \(<8.482\,10^{-19}\) |
| Error analítico de la tangente | \(<4.569\,10^{-15}\) |

Los decimales completos, los dieciséis subintervalos y cada retorno intermedio se conservan en `CERTIFICADO_ENTRADA_RENORMALIZACION.json`.

El cono \(\|\dot\nu\|_1\le|\dot u|/4\) es invariante bajo (9):
\[
|\dot u_{\rm nuevo}|\ge(4.521-0.560/4)|\dot u|
=4.381|\dot u|,
\]
\[
\|\dot\nu_{\rm nueva}\|_1\le(0.756+0.719/4)|\dot u|
=0.93575|\dot u|<\tfrac14(4.381)|\dot u|.
\tag{11}
\]
La dirección paramétrica certificada entra, por tanto, en un cono uniformemente expansivo del operador.

## 5. Construcción cuantitativa de la hoja estable

Traslademos \(g\) al origen y escribamos las coordenadas como \((x,y)=(u-u_g,\nu-\nu_g)\). Fijemos
\[
L=0.16,\qquad r=0.004,\qquad
A=a_0-Lc_0=4.40004,\qquad q=d_0+c_0L=0.83996.
\tag{12}
\]
El cilindro \(|x|\le Lr\), \(\|y\|_1\le r\) está dentro de la bola de (9), puesto que
\((1+L)r+\varepsilon_0=0.00468<0.01\).

Considérese el espacio completo de funciones \(\sigma:B_r\to\mathbb R\) con \(\sigma(0)=0\) y constante de Lipschitz a lo sumo \(L\), dotado de la distancia uniforme. Para cada \(y\), se define \((\mathcal G\sigma)(y)\) como la raíz en \([-L\|y\|_1,L\|y\|_1]\) de
\[
F_\sigma(x,y)=U(x,y)-\sigma(V(x,y)).
\tag{13}
\]
En ese intervalo, \(\|V(x,y)\|_1\le q\|y\|_1<r\). Al incrementar \(x\), (9) muestra que \(F_\sigma\) crece al menos con pendiente \(A\). En sus extremos,
\[
F_\sigma(L\|y\|_1,y)
\ge[AL-b_0-Ld_0]\|y\|_1,
\]
y la desigualdad opuesta vale en el extremo negativo. El margen es
\[
AL-b_0-Ld_0=0.0289664>0.
\tag{14}
\]
Se obtiene una raíz única. Comparando (13) para dos valores de \(y\),
\[
\operatorname{Lip}(\mathcal G\sigma)
\le\frac{b_0+Ld_0}{A}
=\frac{0.67504}{4.40004}<0.16.
\]
Comparando dos gráficos,
\[
\|\mathcal G\sigma-\mathcal G\widetilde\sigma\|_\infty
\le A^{-1}\|\sigma-\widetilde\sigma\|_\infty,
\qquad A^{-1}<0.228.
\tag{15}
\]
El teorema de contracción produce un único gráfico fijo \(x=\sigma_*(y)\). Sobre él,
\[
\|y_n\|_1\le q^n\|y_0\|_1,
\qquad
\|(x_n,y_n)\|_{\mathcal A}\le(1+L)q^n\|y_0\|_1.
\tag{16}
\]
Además, la distancia vertical \(d(x,y)=x-\sigma_*(y)\) cumple
\[
|d(R(x,y))|\ge A|d(x,y)|
\]
mientras la órbita permanece en el cilindro. Toda órbita que permanece allí indefinidamente pertenece al gráfico. Este identifica exactamente la hoja estable local y proporciona la estimación (16). Su regularidad local coincide con la variedad estable analítica del punto fijo hiperbólico.

## 6. Existencia, unicidad y transversalidad del parámetro

Defínase, para \(\lambda\) en (2),
\[
H(\lambda)=u_\lambda-u_g-
\sigma_*(\nu_\lambda-\nu_g).
\]
El certificado asegura \(\|\nu_\lambda-\nu_g\|_1<0.001436077<r\). Para \(\lambda_2>\lambda_1\),
\[
H(\lambda_2)-H(\lambda_1)
\ge\int_{\lambda_1}^{\lambda_2}
\bigl[u'_t-L\|\nu'_t\|_1\bigr]dt
>3733.007995\,(\lambda_2-\lambda_1).
\tag{17}
\]
Para decidir los signos extremos se utiliza \(\|g-g_0\|_{\mathcal A}<\varepsilon_0\) y \(|\sigma_*(y)|\le L\|y\|_1\). La evaluación puntual racional produce
\[
H(1.874038)<-0.0011856110945,
\qquad H(1.874039)>0.0021866053399.
\tag{18}
\]
Por continuidad, existe una raíz; (17) prueba su unicidad y la transversalidad del cruce. En esa raíz, (16) y
\((1+L)(0.001396077+0.00004)<0.001666\)
demuestran (3).

La cota es uniforme en el número de retornos: convierte el avance de profundidad en un error operatorial geométrico explícito.

## 7. Admisibilidad real de todos los retornos

Los cuatro retornos iniciales se acompañan, en cada subintervalo racional, de las desigualdades
\[
0<a=-f(1)<1,\qquad b=f(a)>a,\qquad f(b)<a.
\tag{19}
\]
El programa guarda \(a,b,f(b)\) antes de cada aplicación de (7). La unimodalidad, la paridad y el crítico cuadrático se conservan bajo estos retornos normalizados.

Para las iteraciones siguientes basta una verificación uniforme en la bola de (9). Si \(E=V-V_{g_0}\), la norma (5) da, para \(-0.4\le z\le0\),
\[
|E(z)|\le0.004,\qquad |E'(z)|\le0.01.
\]
La segunda desigualdad usa \(\sup_{j\ge1}j(0.4)^{j-1}=1\). La evaluación racional de los coeficientes centrales proporciona
\[
\frac65<V(z)<\frac85,\qquad |V'(z)|<\frac12,
\qquad 0.39<a<0.41.
\tag{20}
\]
En consecuencia,
\[
f'(x)=-2x\left[V(z)+\frac25x^2V'(z)\right],
\]
y el corchete supera uno para \(0\le x\le1\). El mapa es unimodal y preserva \([-1,1]\). Además,
\[
b=f(a)>1-(0.41)^2\frac85=\frac{4569}{6250}>a,
\]
\[
f(b)<1-\left(\frac{4569}{6250}\right)^2\frac65
=\frac{35028967}{97656250}<0.39<a.
\tag{21}
\]
Las órbitas de la hoja estable satisfacen (19) a toda profundidad. Así, las iteraciones analíticas del operador corresponden a retornos reales de duplicación, con sus dominios y orientaciones conservados.

## 8. Escalado de la cascada superestable local

La conclusión métrica requiere dos cruces: el de la familia con la hoja estable, demostrado en §6, y el de la variedad inestable con el blanco superestable. El segundo está probado por Eckmann–Wittwer para
\(\Sigma_2=\{\psi:\psi(1)=0\}\), correspondiente al ciclo superestable de período dos. La normalización (6) coincide con la del operador real par empleado allí.

El teorema general de Collet–Eckmann–Lanford, §6, proposición 6.1 y teoremas 6.2–6.3, aplica a un mapa de Banach \(C^2\), un punto fijo con un único autovalor inestable \(\delta>1\), una curva transversal a su hoja estable y un blanco transversal a su variedad inestable. Las preimágenes locales del blanco intersectan la curva en puntos que satisfacen
\[
\delta^j(\mu_j-\lambda_*)\longrightarrow C\ne0.
\tag{22}
\]
El índice \(j\) cuenta los retornos locales. Como la curva inicial aquí es \(R^4f_\lambda\), el período físico es \(2^{j+5}\) cuando el blanco se toma en \(\Sigma_2\); cualquier número fijo de pasos empleado para traer el blanco al entorno local se incorpora en un desplazamiento fijo del índice y en \(C\).

Las condiciones reales de §7 y la rama real de duplicación del blanco fijan el período exacto y el itinerario. La sucesión se selecciona por esta continuación local orientada. Tomando diferencias en (22) se obtiene el límite de razones de (4).

Fuentes de los dos resultados utilizados: [Eckmann–Wittwer, *A complete proof of the Feigenbaum conjectures*](https://link.springer.com/article/10.1007/BF01013368); [Collet–Eckmann–Lanford, §6](https://people.math.harvard.edu/~knill/history/lanford/papers/ColletEckmannLanford.pdf).

### Resto asintótico de potencia

La analiticidad de nuestra familia permite precisar (22). En la construcción de coordenadas normales de Collet–Eckmann–Lanford se aplanan únicamente la variedad estable, la variedad inestable y la hipersuperficie blanco. Estas tres subvariedades admiten cambios locales \(C^2\) con derivadas acotadas. El corte suave empleado se realiza en la coordenada escalar inestable; la foliación completa se obtiene después mediante el cambio construido.

En esas coordenadas, la corrección se escribe como una serie de incrementos \(w_j\) cuya norma \(C^1\) satisface
\[
\|w_j\|_{C^1}\le C_1\rho^j,\qquad 0<\rho<1.
\]
La regla de la cadena para el mapa cortado, con derivadas de órdenes uno y dos uniformemente acotadas, proporciona
\[
\|w_j\|_{C^2}\le C_2B^j
\]
para algún \(B\ge1\). La norma ponderada de la construcción controla la norma \(C^1\) ordinaria en el dominio considerado. Por interpolación,
\[
[Dw_j]_\beta\le C_3
\left(\rho^{1-\beta}B^\beta\right)^j.
\]
Se elige
\[
0<\beta<\min\left\{1,
\frac{-\log\rho}{\log B-\log\rho}\right\}.
\tag{23}
\]
La serie converge en \(C^{1,\beta}\). Sea \(z\) la coordenada normal resultante, normalizada para que las preimágenes del blanco satisfagan \(z=\delta^{-j}\), absorbiendo el desplazamiento fijo de índice. Como nuestra curva es analítica y transversal,
\[
z(\Gamma(\lambda))=c(\lambda-\lambda_*)
+O(|\lambda-\lambda_*|^{1+\beta}),\qquad c\ne0.
\]
La inversión local da
\[
\mu_j-\lambda_*=C\delta^{-j}
+O\left(\delta^{-(1+\beta)j}\right).
\tag{24}
\]
Esto demuestra el resto de (4), con \(\theta=\delta^{-\beta}\). La existencia de la tasa está probada; los valores numéricos de \(\beta\), \(\theta\) y la constante del resto requieren una evaluación cuantitativa adicional de esas coordenadas. La tasa operatorial \(0.83996\) de (3) conserva su propio dominio.

### Conversión del resto en error de las razones

Si \(\mu_j-\lambda_*=C\delta^{-j}(1+e_j)\), con \(|e_j|\le M\theta^j\), se escribe
\[
\mu_{j-1}-\mu_j=C(\delta-1)\delta^{-j}(1+r_j),
\quad
r_j=\frac{\delta e_{j-1}-e_j}{\delta-1}.
\]
Con \(K=M(\delta+\theta)/(\delta-1)\), se tiene \(|r_j|\le K\theta^{j-1}\). Por tanto,
\[
\boxed{
\left|\frac{\mu_{j-2}-\mu_{j-1}}{\mu_{j-1}-\mu_j}-\delta\right|
\le\frac{\delta K(1+\theta)\theta^{j-2}}
{1-K\theta^{j-1}}}
\tag{25}
\]
cuando \(K\theta^{j-1}<1\). Esta fórmula separa la precisión de evaluación de cada raíz del error de truncamiento de la cascada.

## 9. Continuación certificada de las ocho raíces iniciales

El nuevo programa `certificar_continuacion_finita.py` conserva la familia (1) y el certificado anterior de ocho raíces. Para \(2\le n\le8\), estudia
\[
S_n(\lambda)=f_\lambda^{2^n}(0)
\]
desde la caja certificada de \(\lambda_{n-1}\) hasta \(1.874039\). La cobertura racional completa contiene exactamente la raíz heredada \(\lambda_{n-1}\) y la raíz nueva \(\lambda_n\). En particular, \(\lambda_n\) es la única raíz nueva en \((\lambda_{n-1},1.874039]\).

Las cajas se excluyen por signo del retorno o por una derivada local de signo certificado. Las cajas ancla conservan existencia y unicidad por signos extremos y monotonía local. Sus extremos cubren exactamente cada intervalo; se verifican las adyacencias. La evaluación usa los momentos (8), Horner de orden 32, colas geométricas exteriores y \(|u_0''|\le2\). La cola uniforme del potencial es menor que \(1.294\,10^{-58}\) en \(|x|\le3/2\).

El certificado final contiene 650 cajas procesadas y 332 hojas de cobertura. El primer nivel tiene la expresión exacta \(\lambda_1=1/u_0(1)\). Las aproximaciones siguientes se muestran únicamente como orientación; sus cajas completas se conservan en los certificados:

| Nivel | Parámetro superestable |
|---:|---:|
| 1 | 1.345913990471832792210949095… |
| 2 | 1.763379787846910127290794030… |
| 3 | 1.850413796950136464530566778… |
| 4 | 1.868979756606798125150574309… |
| 5 | 1.872955034435659740004205128… |
| 6 | 1.873806367467030119412262311… |
| 7 | 1.873988695221365362307168780… |
| 8 | 1.874027744154450672897007573… |

## 10. Alcance de la etapa intermedia y registro del enlace global

**Estado actualizado.** Esta sección conserva la delimitación previa a §§15–17. Esas secciones demuestran la continuación indefinida, la coincidencia del límite y la identificación eventual de los centros originales. El puente de atractores propuesto más abajo permanece como alternativa histórica; el cierre efectivo utiliza la cobertura de itinerarios y la primera salida de §16.

Quedan demostrados conjuntamente:

1. La procedencia del lector crítico de la rueda HMT y la conservación de su familia.
2. La selección como primeras raíces nuevas de los ocho niveles calculados.
3. La entrada de la familia renormalizada en el entorno hiperbólico, con tangente en un cono expansivo.
4. La existencia y unicidad del parámetro (2) dentro del intervalo certificado, con cruce transversal.
5. La convergencia operatorial a toda profundidad con la cota explícita (3).
6. El escalado universal de la cascada local orientada de ese cruce, con el resto de potencia (24).

El selector global del corpus pide la primera raíz nueva después de la anterior, desde el comienzo de la familia. Para identificarlo a todo nivel con \(\mu_j\) debe transportarse el componente real de renormalización que contiene las ocho raíces hasta el componente local de §8, conservando el orden de parámetros y el itinerario. Una prueba de monotonía apropiada del kneading, o un transporte certificado equivalente, cerraría exactamente esta flecha.

La cobertura de §9 controla los niveles uno a ocho. Por sí sola permite todavía la posibilidad lógica de otro componente de acumulación en \((\lambda_8,1.874038)\), o de un pliegue posterior de la selección paramétrica. El cruce único de §6 controla su intervalo local. Por ello se conservan dos nombres: \(\lambda_n\) para el selector finito global y \(\mu_j\) para la cascada local de §8. Su identificación infinita queda expresamente fuera del resultado actual.

**Actualización posterior.** §15 demuestra la existencia y la combinatoria de todos los términos del selector global y excluye completamente el intervalo intermedio indicado. La reserva precedente sobre ese intervalo queda resuelta; la igualdad eventual con los centros locales conserva su enunciado separado.

Un puente suficiente y localizado consiste en cubrir el intervalo intermedio mediante continuaciones de ciclos atractores de período acotado, certificar que sus cuencas contienen la órbita crítica, tratar sus bifurcaciones de duplicación y solapar esa cobertura con la selección orientada de las hojas superestables locales. La cobertura excluiría puntos críticos periódicos de período superior al máximo cubierto: tales puntos formarían su propio atractor superestable y su órbita no convergería al ciclo de período menor certificado. En una bifurcación de un retorno \(F\) con \(F'=-1\), la Schwarziana negativa da el coeficiente
\[
\frac{F'''}6+\frac{(F'')^2}4=-\frac{SF}{6}>0.
\]
La derivada paramétrica no nula del multiplicador y las cotas del resto completarían el tratamiento de ese empalme. Esta cobertura aún no forma parte de los certificados entregados.

Asimismo, (25) requiere valores cuantificados de \(K,\theta\) para proporcionar un error numérico del octavo cociente respecto a \(\delta\). La estrechez del intervalo de evaluación del cociente finito, del orden de \(10^{-37}\), certifica esa evaluación; su diferencia respecto al límite constituye otra estimación.

## 11. Relación con los controles recuperados del corpus

La lectura focal de los propietarios del integral y de los paquetes especializados recupera técnicas útiles, con sus dominios preservados:

- **Profundidad nonádica y memoria bilateral:** los lectores cilíndricos, la composición con acarreo y las prolongaciones compatibles producen la resolución arbitraria utilizada en `PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md`, §§2–5. La cota observable \(729^{-m}\) del artículo XI mide el refinamiento de ese lector.
- **Control paramétrico:** el antecedente demuestra \(\operatorname{diam}F_t^{2^N}(1/2)<9^{-r}\) para cilindros de profundidad \(m=2^N+r\). Esta cota permite resolver cada retorno finito con precisión prefijada.
- **Resolventes y residuos:** los controles de Schur conservan la estructura de una estimación de cola. Para un bloque estable \(D\) con \(\|D\|\le q<|z|\), y residuo \(E=C-(zI-D)Z\), se deduce
  \[
  \|B(zI-D)^{-1}C-BZ\|
  \le\frac{\|B\|\,\|E\|}{|z|-q}.
  \]
  Su aplicación numérica a un nuevo bloque requiere las cotas de ese bloque.
- **Transversalidad del lector crítico:** el propietario `ley9/cierre_feigenbaum.tex` registra la proyección inestable de la tangente como condición de cierre; `c37_feigenbaum.tex` conserva el criterio de renormalización. Las secciones 4–6 reúnen y verifican esa condición para (1).

Los controles de rigidez de los lectores de dígitos, del contraángulo o de las formas de Weil pertenecen a operadores distintos. Su estructura de prueba orienta la composición; las cifras se transfieren sólo después de identificar los correspondientes dominios y operadores. En esta ampliación la derivada efectiva de (7), la separación (17) y la contracción (16) realizan ese trabajo específico.

Propietarios materiales consultados:

1. `output/TRATADO_GENERATIVO_HMT_MD_20260919/REV03/source/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/feigenbaum/c37_feigenbaum.tex`, líneas 279–320, criterio de renormalización y estimaciones finales.
2. Dentro de ese mismo árbol `public_final`, `ley9/cierre_feigenbaum.tex` y `feigenbaum/01b_extension_dodecafasica_ponderada.tex`.
3. `output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/01_FUENTE_SUCESORA/pruebas/python/verificar_vacancias_criticidad.py` y su certificado sectorial.
4. `output/PREPARACION_ENTREGA_USB_20260928/ENTREGA_HMT_USB/03_FUENTES_Y_REPRODUCCION/COLECCION_DOCUMENTAL/02_ARTICULOS/XI/ES/ARCHIVOS/source/nuclear/09.tex`, cotas de refinamiento, y `nuclear/03.tex`, memoria bilateral.
5. En el mismo catálogo documental, `02_ARTICULOS/III/ES/ARCHIVOS/source/base_articulo_II/sections/03b_memoria_resolvente.tex`, residuos y resolventes.

Esta consulta es focal: identifica los cuerpos utilizados y conserva sus referencias; no declara una lectura íntegra de todas las monografías.

## 12. Reproducción y controles de alcance

Desde la raíz del proyecto:

```bash
python3 -I -S output/FEIGENBAUM_HMT_DESARROLLO_20260929/certificar_entrada_renormalizacion.py --levels 4 --order 32 --pieces 16 --output output/FEIGENBAUM_HMT_DESARROLLO_20260929/CERTIFICADO_ENTRADA_RENORMALIZACION.json
python3 -I -S output/FEIGENBAUM_HMT_DESARROLLO_20260929/certificar_continuacion_finita.py --seconds 55 --max-boxes 800 --self-test --output output/FEIGENBAUM_HMT_DESARROLLO_20260929/CERTIFICADO_CONTINUACION_FINITA.json
python3 -I -S output/FEIGENBAUM_HMT_DESARROLLO_20260929/verificar_escalado_local.py
```

La última comprobación verifica las desigualdades racionales del gráfico, la coherencia material de los certificados y los límites de las conclusiones. Los certificados finitos acompañan las pruebas escritas de las secciones 5–8; las dependencias teoremáticas externas de §§3 y 8 conservan sus fuentes explícitas.

Controles negativos: cambiar el peso diez de (5), omitir la derivada de la escala \(a\), tratar el error analítico como si careciera de coeficientes bajos, saltar la condición (19), igualar la tasa de memoria con la tasa paramétrica, o identificar \(\lambda_n\) y \(\mu_j\) sin transporte de su componente invalida la conclusión correspondiente.

## 13. Compatibilidad conjunta, prolongación y selección de la primera raíz

Ampliación posterior del mismo día. La indicación autoral propone utilizar la coherencia conjunta de HMT–MD y de la estructura discreta del continuo para excluir una continuación distinta de la cascada local. Esta sección recupera los operadores pertinentes y determina qué implicación expresa ese argumento en el lector crítico concreto.

### 13.1. Regla forward recuperada

El propietario `manuscrito/sections/hmt/06e_certificado_generacion_monodromica_rev7.tex`, líneas 303–335 y 433–453, parte del estado de frontera R36 con carácter \(\chi\) y residuo interno. La actualización es
\[
\mathcal U_K^\chi=
\operatorname{Upd}_K^\chi\circ
\operatorname{Tra}_K^\chi\circ
\operatorname{Sel}_K^\chi,
\qquad
N_{K+1}=729N_K+d_K^\chi.
\tag{26}
\]
El dígito y la actualización dependen del estado precedente. Dos secciones forward con el mismo estado completo R36 coinciden por inducción. La subrelación \(\operatorname{Ext}^{\chi,\rightarrow}\) es el grafo de esa actualización; la relación total \(\operatorname{Ext}\) admite multiplicidad de continuaciones según los datos y caracteres.

En las líneas 337–367 del mismo propietario, las horquillas racionales certifican la publicación del sucesor ya construido. El artículo XI, `nucleo_ampliado/lectores_cilindros_incidencia.tex`, líneas 432–471 y 615–647, demuestra la compatibilidad de las prolongaciones con esos lectores regionales y con la firma conjunta. El propietario `manuscrito/ampliacion_20260919/frontera_coinductiva_supervivencia.tex`, líneas 85–128, prueba existencia de una historia por ramificación finita y continuidad de los prefijos, y explicita la intervención adicional del lector y de la regla funcional para individualizar una región.

Estas reglas transportan orientación, residuo, cociente, acarreo, frontera y memoria. Su aplicación a la cascada debe conservar además la selección ordenada del parámetro del lector crítico.

### 13.2. Independencia de las constantes antecedentes respecto del parámetro libre

Sea \(B\) el estado HMT que proporciona la rueda y sus constantes antecedentes. Escribamos \(\mathcal C(B)\) para el conjunto de esas publicaciones y \(u_B\) para el perfil crítico. En el dominio declarado por `feigenbaum/c37_feigenbaum.tex`, líneas 3–80 y 147–170, la construcción posterior es
\[
(B,\lambda)\longmapsto f_{B,\lambda}(x)=1-\lambda u_B(x),
\qquad 0<\lambda\le 2/u_B(1).
\tag{27}
\]
Para un mismo \(B\), la lectura de las constantes anteriores se factoriza por la proyección al primer componente:
\[
\widetilde{\mathcal C}(B,\lambda)
=\mathcal C\circ\operatorname{pr}_B(B,\lambda)
=\mathcal C(B).
\tag{28}
\]
En consecuencia, dos valores distintos de \(\lambda\) conservan las mismas publicaciones antecedentes. La igualdad es una propiedad de esta construcción causal: el perfil se fija antes de variar \(\lambda\), y el factor \(\pi_{\mathrm{HMT}}\) se cancela en su normalización cuadrática.

**Lema.** Supóngase que una condición \(A\) se evalúa únicamente sobre esas publicaciones antecedentes. Para todo \(B\) fijo,
\[
\{\lambda\in\Lambda:A(\widetilde{\mathcal C}(B,\lambda))\}
=
\begin{cases}
\Lambda,&A(\mathcal C(B))\text{ se cumple},\\
\varnothing,&A(\mathcal C(B))\text{ falla}.
\end{cases}
\tag{29}
\]
**Demostración.** Sustituir (28) hace independiente de \(\lambda\) el predicado. Por tanto, lo satisfacen todos los parámetros del dominio o ninguno. Esto incluye una comparación de las constantes antecedentes con intervalos metrológicos.

La unicidad de la sección \(B\) y la restricción posterior \(f_{B,\lambda}^{2^n}(0)=0\) producen una fibra de soluciones en \(\lambda\). La regla que elige su primer elemento requiere su propio transporte. La dependencia global propuesta por el autor puede actuar sobre ella mediante un predicado adicional que involucre efectivamente esa raíz, su itinerario y su prolongación; (29) identifica por qué las publicaciones antecedentes, evaluadas por sí solas, conservan toda la fibra.

Este resultado mantiene el orden HMT: la metrología contrasta salidas previamente construidas y la selección de la raíz se demuestra en el lector que la produce.

### 13.3. Lema de transporte ordenado del selector

Sea \(P_n\) un conjunto ordenado de candidatos genealógicos con mínimo \(p_n^*\). Sea \(Z_n\) el conjunto original de raíces candidatas del corpus, con el orden real, y sea \(L_n:P_n\to Z_n\) un lector monótono. Se dice que su imagen es **coinicial** cuando
\[
\forall z\in Z_n\quad\exists p\in P_n:
L_n(p)\le z.
\tag{30}
\]
Entonces
\[
\boxed{L_n(p_n^*)=\min Z_n
\quad\Longleftrightarrow\quad
L_n(P_n)\text{ es coinicial en }Z_n.}
\tag{31}
\]
**Demostración.** Si la imagen del mínimo es el mínimo global, se toma \(p=p_n^*\) en (30). Recíprocamente, dado \(z\in Z_n\), la coinicialidad proporciona \(p\) con \(L_n(p)\le z\). La monotonía da \(L_n(p_n^*)\le L_n(p)\le z\). Como \(L_n(p_n^*)\in Z_n\), es el mínimo global. La sobreyectividad de \(L_n\) constituye una condición suficiente, más fuerte que (30).

Este lema convierte la propuesta de selección genealógica en una implicación verificable. Para la cascada, la actualización nativa debe producir los mínimos compatibles \(p_n^*\); el lector ha de transportar su orden y ser coinicial sobre las raíces originales, incluyendo la exclusión de cualquier raíz anterior fuera de su imagen. La unicidad de una prolongación y la monotonía del lector son propiedades distintas, y ambas se registran con sus dominios.

Cuando las identidades anteriores se cumplen en todos los niveles y el transporte preserva la rama local ya construida, la inducción identifica el selector global con ella. El escalado de §8 se aplica entonces a esa misma sucesión. La sección presente prueba el criterio de transporte (31); conserva pendiente su verificación global para el lector de raíces de (1).

**Corrección de alcance.** El teorema de §14.1 recupera la cobertura completa y la preservación del mínimo en la carta ordenada del continuo. El estatuto pendiente de la frase precedente queda sustituido para ese transporte. La identificación del mínimo con la rama local conserva una obligación dinámica distinta, explicitada en §14.4.

### 13.4. Dos índices y una obligación localizada

La profundidad nonádica \(m\) refina la lectura de un objeto; el índice \(n\) de la cascada cambia su período a \(2^n\). En el primer caso se truncan prefijos de una misma publicación. En el segundo se continúa un componente dinámico y se lee una nueva raíz: los conjuntos de parámetros de período exacto \(2^n\) y \(2^{n+1}\) son distintos y carecen de esa inclusión de prefijos.

En los ocho niveles iniciales, el certificado de §9 demuestra la selección global mediante cobertura y exclusión. En la carta local, §§5–8 demuestran el cruce y la continuación transversal. La obligación restante es construir la lectura ordenada entre ambos regímenes con la coinicialidad (30), o ejecutar la cobertura dinámica equivalente descrita en §10. Las reglas (26) conservan la historia durante esa construcción; (28) conserva las constantes antecedentes.

El control negativo consiste en introducir un candidato de raíz anterior a la imagen seleccionada sin modificar \(B\). El teorema de cierre debe excluirlo mediante un invariante concreto del lector crítico. La mera igualdad de las publicaciones \(\mathcal C(B)\) permanece cierta por (28), por lo que esa igualdad sola no realiza la exclusión.

### 13.5. Procedencia y alcance de esta ampliación

Se recuperan la actualización forward, la compatibilidad de cilindros y la distinción de dominios desde los propietarios citados. Se añaden las formulaciones (28)–(31) y sus pruebas como controles de la aplicación focal. Los resultados de transversalidad, error operatorial y escalado local de las secciones anteriores conservan su fuerza. Esta ampliación registra una comprobación de la implicación propuesta; no declara cumplida la coinicialidad global.

Las rutas de los propietarios del integral de esta sección tienen como prefijo común `output/TRATADO_GENERATIVO_HMT_MD_20260919/REV03/source/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/`. El capítulo `feigenbaum/c37_feigenbaum.tex` reside bajo `colaboracion/parte_iii/source/public_final/`. La ruta de XI tiene el prefijo del catálogo USB consignado en §11, seguido de `XI/ES/ARCHIVOS/source/`.

### 13.6. Selección mínima mediante supervivencia a profundidad arbitraria

La composición con la supervivencia produce además un selector global preciso. Se mantiene la familia uniforme \(\eta=0\), construida en §1, y se utilizan los resultados demostrados en *PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md*, §§6.1–6.2. Sean
\[
I=\left[\frac1{2u_0(1)},\frac2{u_0(1)}\right],\qquad
c_j(\lambda)=f_\lambda^j(0),\qquad
\tau_j=(-1)^{v_2(j)}.
\]
El conjunto
\[
\Lambda_\tau=\{\lambda\in I:\operatorname{sign}c_j(\lambda)=\tau_j
\text{ para todo }j\ge1\}
\]
es compacto y no vacío. El control de derivadas de ese propietario proporciona
\[
B_j=\frac{16^j(16^j-1)}{15},\qquad
|c_j(\lambda)|>\frac2{B_j}\quad(\lambda\in\Lambda_\tau).
\tag{32}
\]
Definamos
\[
\varepsilon_j=\frac1{B_j},\qquad
A_N=\{\lambda\in I:\tau_jc_j(\lambda)\ge\varepsilon_j,\
1\le j\le N\}.
\tag{33}
\]
Cada \(A_N\) es compacto por continuidad de los iterados y no vacío porque contiene \(\Lambda_\tau\). Además,
\[
A_{N+1}\subseteq A_N,\qquad
\bigcap_{N\ge1}A_N=\Lambda_\tau.
\tag{34}
\]
La inclusión de derecha a izquierda se sigue de (32). La inclusión inversa se sigue de los márgenes estrictamente positivos de (33), que fijan cada signo.

**Teorema del mínimo superviviente.** Los mínimos \(a_N=\min A_N\) satisfacen
\[
\boxed{a_N\uparrow a_*=\min\Lambda_\tau.}
\tag{35}
\]
**Demostración.** La inclusión (34) hace creciente la sucesión de mínimos, acotada dentro de \(I\); tiene, por tanto, un límite \(a\). Para cada \(r\), todos los términos \(a_N\), \(N\ge r\), pertenecen al cerrado \(A_r\); así \(a\in A_r\). Por (34), \(a\in\Lambda_\tau\). Para cualquier \(\lambda\in\Lambda_\tau\), se tiene \(a_N\le\lambda\) a todo nivel, y al pasar al límite, \(a\le\lambda\). Esto prueba (35).

En el lector cilíndrico HMT, el objeto \(a_*\) posee prefijos compatibles a toda profundidad, con orientación, residuo y memoria conservados. Su elección utiliza el orden de la lectura paramétrica y la supervivencia completa. La existencia del mínimo es una conclusión de compacidad; la decisión efectiva de supervivencia y una cota computable del error \(a_*-a_N\) requieren controles cuantitativos adicionales.

Los parámetros \(a_N\) resuelven restricciones de signos con margen. Sus fronteras pueden satisfacer \(\tau_jc_j=\varepsilon_j\), mientras las raíces superestables satisfacen \(c_{2^n}=0\). Por ello (35) establece un selector global de realización infinita y preserva, como objeto distinto, el selector de primeras raíces del corpus.

### 13.7. Recuperación del parámetro desde la historia crítica completa

El segundo término de la historia crítica proporciona un lector inverso exacto:
\[
c_1(\lambda)=1,\qquad
c_2(\lambda)=1-\lambda u_0(1),\qquad
\boxed{\lambda=\frac{1-c_2(\lambda)}{u_0(1)}.}
\tag{36}
\]
La positividad \(u_0(1)>0\), demostrada para el perfil, hace válida la división. En consecuencia, dos historias críticas completas iguales tienen el mismo parámetro. La palabra de signos \(\tau\) constituye una publicación reducida de esa historia; conserva su combinatoria y omite la magnitud de \(c_2\).

Las fórmulas (35)–(36) precisan la contribución de supervivencia y memoria: la primera construye una selección ordenada del itinerario infinito; la segunda recupera el parámetro cuando se conserva la historia completa. Para identificar \(a_*\) con el cruce \(\lambda_*\) de §6 debe probarse su pertenencia a la misma hoja estable local, por ejemplo mediante permanencia y convergencia de \(R^{4+n}f_{a_*}\) en el dominio certificado. La mera pertenencia \(a_*\in J\) deja sin decidir esa condición dinámica.

El cierre solicitado requiere asimismo que las raíces finitas elegidas por el mínimo global sean los centros sucesivos de esa hoja. El criterio (31) expresa una vía suficiente para demostrarlo. Las construcciones (35)–(36) son resultados del desarrollo acumulativo; su alcance conserva explícitas estas dos identificaciones.

## 14. Transporte completo desde el continuo y realización espectral del perfil

Esta ampliación reúne la carta ordenada de la doble proyección del artículo XI REV11 y la construcción de momentos y Jacobi del artículo de Grassmannianos REV07. Mantiene el sector uniforme y la familia de §1. El orden causal parte de las operaciones APP, de la orientación TRIT y del transporte TPK; el perfil dodecafásico y sus momentos son lectores posteriores de la estructura discreta conjunta. Los ceros paramétricos se definen después de construir ese perfil.

### 14.1. Cobertura de todas las raíces y transporte de su mínimo

El artículo XI, sección ch_cierre_cardinal, líneas 435–497, construye la publicación arquimediana sobreyectiva desde cilindros compatibles y su cociente ordenado. Dentro de su universo declarado \(\mathfrak G\), demuestra el isomorfismo de cuerpos ordenados completos
\[
\iota:\mathbb R_{\rm HMT}^{\mathfrak G}
   \xrightarrow{\cong}\mathbb R^{\mathfrak G}.
\tag{37}
\]
Se cambia aquí el nombre \(\eta\) del propietario por \(\iota\), para distinguirlo del parámetro de ponderación, fijado a cero. La segunda proyección conserva incidencia, frontera y memoria sobre el mismo antecedente; el cociente de evaluación y la historia completa mantienen sus dominios respectivos.

Construyamos en el cuerpo HMT, antes de seleccionar una raíz,
\[
\cos_{\rm H}(t)=\sum_{k=0}^{\infty}\frac{(-1)^kt^{2k}}{(2k)!},
\qquad
u_{\rm H}(x)=\frac1{12}\sum_{m=1}^{12}
\left[1-\cos_{\rm H}\!\left(\frac{2(3m-1)x}{\sqrt[\rm H]{899}}\right)\right],
\]
\[
F_a(x)=1-a\,u_{\rm H}(x),\qquad S_n^{\rm H}(a)=F_a^{\,2^n}(0).
\tag{38}
\]
Los enteros y el segundo momento son los ya derivados del lector dodecafásico. La raíz cuadrada es la positiva del cuerpo ordenado. La serie convergente realiza analíticamente ese lector; conserva el perfil y el coeficiente normalizador de §1.

**Teorema de transporte del retorno.** Para todo parámetro del dominio interno de (38),
\[
\iota(F_a(x))=f_{\iota(a)}(\iota(x)),\qquad
\iota(S_n^{\rm H}(a))=S_n(\iota(a)).
\tag{39}
\]
**Demostración.** El isomorfismo ordenado fija los racionales y preserva la raíz positiva. Preserva los límites convergentes: cada entorno de radio racional positivo se transporta a otro del mismo radio. Aplicado a las sumas parciales de (38), transporta el coseno y \(u_{\rm H}\). La primera igualdad resulta de conservar suma y producto; la segunda, por inducción sobre el número de iteraciones.

Fijado un centro anterior \(a_{n-1}\), definamos \(Z_n^{\rm H}\) por retorno cero, período crítico exacto \(2^n\) y \(a>a_{n-1}\), dentro del dominio paramétrico declarado. Sea \(Z_n\) el conjunto definido por las mismas condiciones para \(f_\lambda\), a la derecha de \(\iota(a_{n-1})\). Entonces
\[
\boxed{\iota[Z_n^{\rm H}]=Z_n,\qquad
\iota(\min Z_n^{\rm H})=\min Z_n.}
\tag{40}
\]
La segunda igualdad se afirma cuando existe el mínimo; la primera preserva también la no existencia de candidatos.

**Demostración.** (39) preserva el retorno cero y los retornos anteriores que determinan el período exacto. El orden conserva la posición respecto del centro previo. La sobreyectividad de (37), aplicada a cualquier parámetro raíz, prueba la cobertura inversa. Si \(a_*\) es el mínimo, cualquier \(z\in Z_n\) tiene la forma \(\iota(a)\), con \(a\in Z_n^{\rm H}\), de donde \(\iota(a_*)\le z\). La afirmación inversa utiliza \(\iota^{-1}\).

Queda satisfecha la coinicialidad (30) para este lector completo. La reserva de §§13.3–13.5 sobre la disponibilidad del transporte ordenado queda corregida. Se cubren todos los candidatos de la carta, incluidos los que una ejecución finita todavía no haya aislado. Las igualdades se interpretan conjuntamente en el universo interno indicado en XI; identificarlo con un universo ambiente arbitrario sería otra afirmación. Los intervalos racionales y los retornos finitos de los certificados previos tienen la realización explícita (38)–(39).

### 14.2. Representación de Jacobi del perfil dodecafásico completo

Definamos la medida atómica del lector,
\[
s_m=\frac{4(3m-1)^2}{899},\qquad
\nu_0=\frac1{12}\sum_{m=1}^{12}\delta_{s_m},\qquad
M_r=\int s^r\,d\nu_0(s).
\tag{41}
\]
Los doce nodos son distintos y positivos. Para un polinomio \(p\ne0\) de grado menor que \(r\le12\),
\[
\sum_{i,j=0}^{r-1}p_iM_{i+j}p_j
=\frac1{12}\sum_{m=1}^{12}p(s_m)^2>0.
\tag{42}
\]
Un polinomio de grado menor que doce no se anula en los doce nodos. En grado doce aparece \(\prod_m(s-s_m)\), de norma nula.

El mecanismo de la sección jacobi_spectral, líneas 35–136, aplicado a esta medida, produce polinomios ortonormales \(\psi_0,\ldots,\psi_{11}\), con \(\psi_0=1\). Sean
\[
Q_{mj}=\psi_j(s_m)/\sqrt{12},\quad
D=\operatorname{diag}(s_m),\quad J_{12}=Q^{\mathsf T}DQ.
\]
Se cumplen
\[
Q^{\mathsf T}Q=I,\quad DQ=QJ_{12},\qquad
\boxed{u_0(x)=e_0^{\mathsf T}
\bigl[I-\cos(x\sqrt{J_{12}})\bigr]e_0.}
\tag{43}
\]
**Demostración.** La ortogonalidad procede de (42). La multiplicación por \(s\) produce una recurrencia de tres términos: los elementos separados por más de una posición se anulan por ortogonalidad y grado. Fijar positivos los coeficientes principales hace positivas las subdiagonales. Por cálculo funcional,
\(\cos(x\sqrt{J_{12}})=Q^{\mathsf T}\cos(x\sqrt D)Q\).
El vector \(Qe_0\) es constante, de valor \(1/\sqrt{12}\); sustituirlo recupera la suma de §1.

El artículo de Grassmannianos desarrolla este mecanismo para medidas marcadas y refinamientos. Aquí se aplica a (41); el rango doce pertenece a este lector. Las marcas genealógicas se conservan junto al lector, conforme a la fidelidad marcada del propietario. \(J_{12}\) representa el perfil analítico; el estado completo conserva adicionalmente rutas, orientación y memoria.

El verificador de esta ampliación comprueba con fracciones exactas los doce grados de norma positiva, la anulación del grado doce, el entrelazador \(VT=DV\) en base mónica y la autoadjunción ponderada \(HT=T^{\mathsf T}H\). Comprueba los momentos de grado cero a treinta; la identidad para todo grado se sigue del entrelazador. Sus primeros coeficientes son
\[
a_0=2,\qquad \beta_1=\frac{2493348}{808201}.
\tag{44}
\]

### 14.3. Sensibilidad orientada del retorno

Para un retorno exacto de período \(p=2^n\), sean
\[
c_j=f_\lambda^j(0),\quad q_j=\partial_\lambda c_j,\quad
D_j=\prod_{k=1}^j f_\lambda'(c_k),\quad D_0=1.
\]
Antes del retorno crítico, los factores de \(D_{p-1}\) son distintos de cero. Diferenciación y telescopaje dan
\[
q_{j+1}=-u_0(c_j)+f_\lambda'(c_j)q_j,\qquad
\boxed{\frac{q_p}{D_{p-1}}
=-\sum_{j=1}^{p-1}\frac{u_0(c_j)}{D_j}.}
\tag{45}
\]
En la palabra canónica, \(\operatorname{sign}c_j=(-1)^{v_2(j)}\). El signo de \(f_\lambda'(c_j)\) es el opuesto; por tanto,
\[
\operatorname{sign}D_j=(-1)^{j+\sum_{k=1}^jv_2(k)}
=(-1)^{s_2(j)},
\tag{46}
\]
usando \(\sum_{k=1}^jv_2(k)=j-s_2(j)\), donde \(s_2(j)\) cuenta los unos binarios. La sensibilidad normalizada es
\[
\mathcal T_n=-\sum_{j=1}^{2^n-1}(-1)^{s_2(j)}t_j,\qquad
t_j=\frac{u_0(c_j)}{|D_j|}>0.
\tag{47}
\]
La positividad nodal de (42) determina \(u_0\); (47) conserva además los productos orbitales y sus orientaciones.

Un intento de prueba por momentos exigiría una medida positiva \(\rho\) en \([0,1]\) con \(t_j=\int z^{j-1}\,d\rho\). Bajo esa condición,
\[
\mathcal T_n=\int_0^1
\frac{1-\prod_{r=0}^{n-1}(1-z^{2^r})}{z}\,d\rho(z)>0
\tag{48}
\]
para \(\rho\ne0\), extendiendo el integrando por su valor \(1\) en cero. La identidad se obtiene expandiendo el producto binario.

El control racional en la raíz de período cuatro previamente certificada obtiene
\[
t_1\approx0.40425224267600139730,\quad
t_2\approx0.04925249167432646403,\quad
t_3\approx0.15740870098294833737
\]
y el intervalo exterior riguroso
\[
0.296096033367379523967764444238832345360107
<\mathcal T_2<
0.296096033367379523967764444238832345360112.
\tag{49}
\]
También certifica \(t_3>t_2\). Una medida positiva sobre \([0,1]\) impondría \(t_3\le t_2\); ese levantamiento concreto de los pesos orbitales a momentos positivos queda descartado. El signo positivo de (49) permanece certificado. Este control distingue el fallo de una prueba propuesta del fallo de la propiedad que se pretendía probar.

### 14.4. Alcance de las composiciones recuperadas

(37)–(40) resuelven cobertura, orden y transporte global de la selección mínima. (43) reúne el lector crítico con la realización espectral, preservando exactamente sus doce fases. Ambos resultados proceden de las estructuras indicadas por el autor y corrigen el alcance excesivo del diagnóstico anterior.

El cierre solicitado añade la igualdad entre los centros elegidos por ese mínimo y los de la rama local de §§6–8 a todo nivel. El transporte completo conserva esa pregunta y sus respuestas; su sobreyectividad por sí sola no decide qué componente dinámico contiene el mínimo. El criterio de descenso del propio XI distingue el transporte por una biyección de la identificación con una operación nativa anterior.

La exclusión de candidatos anteriores debe actuar sobre (39), su itinerario y (45), o mediante una cobertura dinámica equivalente. A fecha de esta ampliación, las ocho primeras raíces y la rama local conservan sus certificados separados. Los controles (43) y (49) se registran con ese alcance y no como una certificación infinita de su igualdad.

Propietarios de esta composición:

- Artículo XI REV11: sections/ch_cierre_cardinal.tex:435–497; sections/ch_descenso_por_fibras.tex:10–39; sections/ch_memoria_y_naturalidad.tex:12–35; sections/supervivencia_punto_fijo.tex:32–109. Prefijo: output/PREPARACION_ENTREGA_USB_20260928/ENTREGA_HMT_USB/03_FUENTES_Y_REPRODUCCION/ACTUALIZACIONES_20260928/FINAL01/PAQUETES/ARTICULO_XI_REV11_ES_EN_FINAL_BN_20260928/ARTICULO_XI_REV11_ES_EN_FINAL_BN/ES/source/.
- Grassmannianos REV07: sections/jacobi_spectral.tex:35–136,174–259 y sections/lectores_formas_compatibles.tex:40–115. Prefijo: output/GRASSMANNIANOS_CUBO_HISTORICO_REV07_20260928/ES/source/. Los resultados se aplican con la medida y las marcas declaradas en §14.2.

## 15. Continuación indefinida de la primera raíz y exclusión del intervalo intermedio

El apéndice contiguo *CLASIFICACION_ITINERARIOS_FEIGENBAUM.md* contiene la demostración completa, incluidos todos los casos de la inducción. Conserva la familia (1) y el selector de primera raíz nueva del corpus. Las operaciones sobre la carta ordenada se transportan por (38)–(40); la palabra y su lectura nonádica conservan la procedencia demostrada en el desarrollo de prolongación.

### 15.1. Clasificación y existencia a toda profundidad

Escribamos \(W_n=\tau_1\cdots\tau_{2^n-1}\), con \(\tau_j=(-1)^{v_2(j)}\), y \(a_*=\min\Lambda_\tau\). La existencia y compacidad de \(\Lambda_\tau\) están demostradas en el desarrollo de prolongación, §§6.1–6.2; su selección mínima, en §13.6.

**Clasificación.** Todo mapa unimodal estricto de máximo, sobre un intervalo invariante, cuyo crítico tiene período exacto \(2^n\) y cuyo itinerario \(K\) satisface \(K<\tau\), tiene itinerario \(W_n0\).

La inducción se realiza mediante el retorno efectivo. Para período al menos ocho, la comparación con \(\tau\), junto con los intervalos que atraparían órbitas de signos incompatibles, fuerza el prefijo \((+,-,+,+,+,-)\). De aquí se obtienen
\[
J_1=[d_2,d_4],\quad F(J_1)=[d_3,1],\quad
d_4<d_3,\quad F^2(J_1)=J_1.
\]
El retorno normalizado por \(h(x)=d_2x\) tiene máximo uno, período mitad e itinerario \(K'_j=-K_{2j}<\tau\). El orden se conserva porque
\[
O_{2q-1}(K)=-O_{q-1}(K'),\qquad
K_{2q}-\tau_{2q}=-(K'_q-\tau_q).
\]
Los casos iniciales son \(+0\) y \(+-+0\); la inducción reconstruye \(W_n0\). Para los mapas pares, también \(0<d_4<-d_2<1\), de modo que el retorno se extiende a \([-1,1]\) y coincide con (6).

Antes de \(a_*\), todos los itinerarios son menores que \(\tau\): los conjuntos de comparación estricta son abiertos por la separación demostrada en §6.1 del antecedente; el intervalo anterior a \(a_*\) es conexo y comienza con \(+^\infty<\tau\).

**Existencia de cada primera raíz.** Supóngase construida \(\lambda_{n-1}<a_*\), y sea \(p=2^{n-1}\). Los ceros de \(c_p\) en \([\lambda_{n-1},a_*]\) forman un conjunto finito no vacío: la función es analítica y \(c_p(a_*)\ne0\). Sea \(z<a_*\) su último cero. En \((z,a_*]\), \(c_p\) tiene signo \(\tau_p\). Para \(g_\lambda=f_\lambda^p\),
\[
g_\lambda'(0)=0,\qquad
c_{2p}(\lambda)=c_p(\lambda)+O(c_p(\lambda)^2).
\]
Cerca de \(z\), por la derecha, \(c_{2p}\) tiene signo \(\tau_p\); en \(a_*\), tiene el contrario. Existe un cero de \(c_{2p}\) en \((z,a_*)\), y su período es exactamente \(2p\), pues allí \(c_p\ne0\). La finitud de los ceros proporciona la primera raíz nueva en \((\lambda_{n-1},a_*)\). El último cero auxiliar prueba existencia; la elección efectiva sigue siendo la primera raíz. La base es \(\lambda_1=1/u_0(1)<a_*\).

### 15.2. Límite de la sucesión original

**Teorema.** El selector original existe a todos los niveles y satisface
\[
\boxed{K_{\lambda_n}=W_n0,\qquad
\lambda_n\nearrow a_*=\min\Lambda_\tau.}
\tag{50}
\]
**Demostración.** La existencia precedente da una sucesión creciente acotada por \(a_*\). La clasificación fija todos sus itinerarios. Sea \(b\le a_*\) su límite. Para cada \(p\), los términos suficientemente avanzados conservan los signos opuestos \(\tau_p,\tau_{2p}\). Taylor y (32) dan
\[
|c_{2p}(\lambda_n)-c_p(\lambda_n)|
\le\tfrac12 B_p|c_p(\lambda_n)|^2,\qquad
|c_p(\lambda_n)|>2/B_p.
\]
Al pasar al límite se conserva \(\operatorname{sign}c_p(b)=\tau_p\), con módulo al menos \(2/B_p>0\). Para todo \(p\), esto implica \(b\in\Lambda_\tau\); la minimalidad da \(b=a_*\).

El resultado resuelve existencia indefinida, conservación de la cascada simbólica y selección de su primer parámetro límite para la regla global original. La completación HMT transporta esta sucesión y su límite conservando orden y lectura.

### 15.3. Certificado de exclusión del intervalo intermedio

El programa de puente certifica
\[
\Lambda_\tau\cap[\lambda_{8,\rm inf},1.874038]=\varnothing,
\tag{51}
\]
donde
\[
\lambda_{8,\rm inf}
=1.874027744154450672897007573595092408435133414523352839687903472138975
\]
es el extremo inferior racional del intervalo certificado de \(\lambda_8\).

La cobertura contiene 374 intervalos exactamente adyacentes y ninguna región pendiente: 319 con \(c_{512}>0\), 10 con \(c_{1024}<0\), dos con \(c_{2048}>0\), todos opuestos al signo de \(\tau\), y 43 próximos a centros de períodos 256, 512 o 1024, excluidos por su segundo retorno.

En este último caso, \(g=f_\lambda^p\), \(d=g(0)\) y una cota uniforme \(|g''|\le M\) entre cero y \(d\) satisfacen \(M|d|<2\). Entonces
\[
|g(d)-d|\le\tfrac12M|d|^2<|d|\quad(d\ne0).
\]
Ambos retornos tienen el mismo signo; para \(d=0\), ambos son cero. Las dos situaciones excluyen \(\tau_{2p}=-\tau_p\) con signos estrictos.

La evaluación utiliza momentos racionales, colas geométricas del potencial y de su segunda derivada, y \(|u_0'''|<6\). El centrado paramétrico intersecta la envolvente natural con
\[
c_j(\lambda_{\rm medio})+
\partial_\lambda c_j(I)\,(I-\lambda_{\rm medio});
\]
la derivada se propaga sobre la caja completa. La autoaplicación de \([-1,1]\) se demuestra antes de restringir a ella las envolventes.

La primera ejecución parcial permanece íntegra en el certificado. La reanudación trabaja sobre sus seis intervalos pendientes y completa la cobertura. El verificador de esta ampliación comprueba huellas, teselado y cada desigualdad de signo o de Taylor registrada.

### 15.4. Localización conjunta

El cruce local \(\lambda_*\) realiza \(\tau\) por sus retornos reales a toda profundidad, de modo que \(a_*\le\lambda_*\). Por (50), \(\lambda_8<a_*\); junto con (51),
\[
\boxed{1.874038<a_*\le\lambda_*<1.874039.}
\tag{52}
\]
Quedan resueltas las reservas anteriores sobre acumulaciones del selector por debajo de este intervalo y sobre el abandono de su itinerario canónico.

La igualdad \(a_*=\lambda_*\) exige identificar las realizaciones pertinentes de \(\tau\) dentro de esta caja con la hoja estable local, o una prueba de aislamiento equivalente. La unicidad del cruce demostrada en §6 se refiere a esa hoja local. La existencia de retornos reales a toda profundidad y la permanencia en una bola analítica concreta son condiciones distintas.

La continuación global (50), la cobertura (51) y el escalado local (4) conservan sus dominios y sus certificados. La identificación de sus parámetros de acumulación y de sus centros queda separada hasta completar el aislamiento.

## 16. Aislamiento por primera salida y coincidencia de los límites

Esta sección completa el aislamiento identificado en §15.4. Conserva la familia HMT (1), la selección mínima (50), la carta (5) y la hoja estable de §§5–7. La prueba utiliza el orden \(a_*\le\lambda_*\): basta excluir una separación hacia el lado negativo del cono expansivo.

### 16.1. Cotas superior e inferior del transporte transversal

Además de (9), el lema 2.1 de [Hertling–Spandl, §2](https://arxiv.org/pdf/1410.3277) proporciona \(\|D\Phi\|<0.9\) en la misma bola de radio \(0.01\), donde
\[
\Phi_u(u,\nu)=u-\frac{U(u,\nu)-u}{3.669}.
\]
Por tanto,
\[
\left|1-\frac{U_u-1}{3.669}\right|<0.9,\qquad
U_u<1+1.9(3.669)=7.9711.
\tag{53}
\]
El número \(3.669\) pertenece al precondicionador publicado de este certificado analítico; la familia generada (1) conserva sus coeficientes previos.

Tomemos \(\kappa=0.21\). Para dos puntos de la bola unidos por una secante con
\(\Delta u<0\), \(\|\Delta\nu\|_1\le\kappa|\Delta u|\), la integración de los bloques de \(DR\) sobre el segmento da
\[
4.4034|\Delta u|
\le|\Delta u'|\le8.0887|\Delta u|,\qquad \Delta u'<0,
\tag{54}
\]
\[
\|\Delta\nu'\|_1
\le(0.756+0.719\kappa)|\Delta u|
=0.90699|\Delta u|
<\kappa(4.4034)|\Delta u|.
\tag{55}
\]
Aquí \(4.4034=4.521-0.560\kappa\) y \(8.0887=7.9711+0.560\kappa\). Así, el cono de secantes conserva orientación y se expande mientras el segmento permanezca en la bola.

### 16.2. Reducción de una separación infinita a una región finita

Supongamos \(a_*<\lambda_*\), y pongamos
\[
f_n=R^{4+n}f_{a_*},\qquad
s_n=R^{4+n}f_{\lambda_*},\qquad
(\Delta u_n,\Delta\nu_n)=f_n-s_n.
\]
La cota positiva de \(u'\) y \(\|\nu'\|_1/u'<0.144386<\kappa\) sobre \(\Gamma(J)\) sitúan la secante inicial en el cono negativo. La hoja estable está escrita respecto de \(g\), con
\[
s_n=g+e_n,\quad
\|e_n\|_{\mathcal A}<0.001666(0.83996)^n,\quad
|(e_n)_u|\le0.16\|(e_n)_\nu\|_1.
\tag{56}
\]
Los controles de entrada implican
\[
|\Delta u_0|
<0.004993128+0.00004
 +0.16(0.001396077+0.00004)
=0.00526290032< h,\qquad h=0.006.
\tag{57}
\]
Mientras \(|\Delta u_n|<h\), (55)–(56) dan
\[
\|f_n-g_0\|_{\mathcal A}
<(1+\kappa)h+0.001666+0.00004
=0.008966<0.01.
\tag{58}
\]
El punto \(s_n\) y el segmento entre ambos también permanecen en esa bola convexa. La expansión inferior (54) obliga a una primera salida finita \(N\), y la cota superior aplicada al paso precedente proporciona
\[
0.006\le-\Delta u_N<0.0485322,\qquad
\|\Delta\nu_N\|_1\le0.21|\Delta u_N|.
\tag{59}
\]
Se utiliza la desigualdad \(8.0887h=0.0485322\); el salto completo, y no únicamente la superficie de primera salida, queda incluido.

En consecuencia, \(f_N\) pertenece a la siguiente región:
\[
\begin{split}
\mathcal C_-=\{\,g+(d_u,d_\nu)+e:\;&
-0.0485322\le d_u\le-0.006,\\
&\|d_\nu\|_1\le0.21|d_u|,\quad
|e_u|+\|e_\nu\|_1\le0.001666,\\
&|e_u|\le0.16\|e_\nu\|_1\,\}.
\end{split}
\tag{60}
\]
Como \(a_*\) realiza \(\tau\), todos sus retornos normalizados son autoaplicaciones unimodales de \([-1,1]\) con el mismo itinerario. Esta propiedad procede de la inducción de retornos, independientemente de la distancia de \(f_N\) a \(g_0\). Por eso el certificado siguiente trata \(\mathcal C_-\) intersectada con esa clase de autoaplicaciones.

### 16.3. Exclusión certificada de la región de primera salida

El programa certificar_caps_kneading.py y su certificado CERTIFICADO_CAP_NEGATIVA_PRIMERA_SALIDA.json cubren exactamente el intervalo de (59) mediante 64 bandas racionales adyacentes. Todas quedan excluidas; ninguna subdivisión adicional ni región pendiente intervienen en el resultado.

De las 64 bandas, 54 presentan un signo contrario y diez un retorno contractivo de período 16 o 32. La mayor cota de Lipschitz de esos retornos es menor que \(0.475146491\); el horizonte máximo de exclusión es el iterado 64.

La evaluación conserva como variables compartidas los primeros cuarenta coeficientes de la perturbación, junto con una cota explícita de su cola infinita. Para cada banda, el centro es \(g_0\) desplazado en la coordenada \(u\). Si \(a,b\ge0\) acotan las sensibilidades duales en \(u,\nu\), el soporte de la incertidumbre del punto fijo y del residuo estable es
\[
0.00004\max(a,b)
+0.001666\max\left(b,\frac{0.16a+b}{1.16}\right).
\tag{61}
\]
La segunda expresión se obtiene maximizando \(a|e_u|+b\|e_\nu\|_1\) bajo las dos restricciones de (56). De este modo se utiliza la orientación de la hoja estable demostrada previamente, además de su norma.

Sea \(x_j\) la órbita del centro y \(L_j\) su sensibilidad lineal a todos los coeficientes compartidos. El modelo de Taylor tiene la forma
\[
c_j=x_j+L_j(\Delta v)+r_j,\qquad |r_j|\le E_j.
\]
Si \(\rho_j\) acota \(|L_j(\Delta v)|+E_j\), la recurrencia exterior empleada es
\[
E_{j+1}\le |f_0'(x_j)|E_j
+\tfrac12\sup|f_0''|\rho_j^2
+\sup|\Delta f'|\rho_j.
\tag{62}
\]
Las derivadas se acotan sobre el segmento de los dos estados. La órbita central se verifica dentro de \([-1,1]\); las otras órbitas pertenecen a ese intervalo por la autoaplicación incluida en el dominio certificado. Los cálculos utilizan redondeo racional exterior, incluyendo las colas geométricas.

Cada banda se excluye por una de dos desigualdades:

1. Un valor crítico tiene signo estrictamente opuesto a \(\tau_j\).
2. Para \(p=2^k\), el retorno \(H=f^p\) tiene constante de Lipschitz \(L_p<1\) sobre el segmento entre \(0\) y \(H(0)\). Entonces
\[
|H(H(0))-H(0)|\le L_p|H(0)|.
\]
Si \(H(0)\ne0\), los dos valores tienen el mismo signo; si \(H(0)=0\), ambos se anulan. En ambos casos queda excluido el itinerario estricto \(\tau_{2p}=-\tau_p\).

La constante \(L_p\) se obtiene propagando el segmento inicial \([-r,r]\), \(r\ge|H(0)|\), junto a las cajas de la órbita crítica y multiplicando las cotas exteriores de las derivadas. Se acotan los mapas de la banda completa, manteniendo (61).

### 16.4. Teorema de coincidencia del parámetro de acumulación

**Teorema.** Para la familia uniforme HMT (1), el límite de la selección original de primeras raíces coincide con el cruce estable certificado:
\[
\boxed{\lambda_n\nearrow a_*=\lambda_*,
\qquad 1.874038<\lambda_*<1.874039.}
\tag{63}
\]

**Demostración.** (50)–(52) dan \(\lambda_n\uparrow a_*\le\lambda_*\), con ambos parámetros en \(J\). Si la desigualdad fuera estricta, (54)–(59) producirían un retorno \(f_N\in\mathcal C_-\) que realiza \(\tau\). La cobertura completa de §16.3 excluye precisamente esa posibilidad. Luego \(a_*=\lambda_*\).

La prueba controla todas las profundidades mediante una primera salida finita y una cobertura uniforme de su región. Las reservas de §§10, 14.4 y 15.4 relativas a la coincidencia de límites quedan resueltas por (63).

## 17. Identificación de los centros originales y escalado global

El último paso conserva la selección de (50). La continuación local y los parámetros originales se comparan por su período exacto y su clase híbrida; la coincidencia se obtiene mediante una unicidad en un entorno paramétrico fijo.

### 17.1. Realización analítica de grado dos y transversalidad

El punto fijo \(g\) de §3 es par, analítico, de crítico cuadrático y combinatoria estacionaria de duplicación. El teorema 2.1 de [de Faria–de Melo–Pinto](https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n3-p01.pdf), aplicado a esa única combinatoria, da un conjunto límite de un solo elemento, con extensión holomorfa propia de grado dos entre discos topológicos anidados. Su atracción sobre el intervalo identifica ese elemento con \(g\), pues \(Rg=g\).

El lema 3.2 de la misma fuente extiende un número fijo de retornos a una vecindad analítica completa de \(g\), con imágenes de grado dos y módulo positivo. La norma (5) controla la norma uniforme sobre una vecindad compleja suficientemente pequeña de \([-1,1]\), porque \(|(x^2-1)/2.5|<1\) allí. La convergencia (3) entra en dicha vecindad; la dependencia analítica de los retornos proporciona, para cierto entero fijo \(d\), una familia
\[
\mathcal F_\lambda=R^d f_\lambda
\tag{64}
\]
de mapas de grado dos, analítica en un entorno complejo de \(\lambda_*\). Los discos y el número de retornos se fijan antes de variar \(\lambda\) en ese entorno.

La tangente paramétrica pertenece al cono expansivo, mientras la hoja estable satisface la pendiente de §5. Los retornos preservan esa separación. La realización de grado dos identifica localmente la hoja estable con la clase híbrida del mapa infinitamente renormalizable; por ello (64) es transversal a esa clase.

El cambio de espacio analítico se justifica detalladamente en §8.2 del apéndice CLASIFICACION_ITINERARIOS_FEIGENBAUM.md. Una dirección tangente a la clase híbrida produciría tangentes renormalizadas decrecientes, por la convergencia uniforme sobre un disco híbrido y la estimación de Cauchy. La dirección certificada satisface, en cambio, \(|\dot f(1)|=|\dot u|/10\) y crece bajo los retornos por el cono expansivo. Esta evaluación común de ambos representantes prueba la transversalidad sin suponer equivalencia de sus normas.

### 17.2. Unicidad en una vecindad fija

Para \(n>d\), la clasificación de §15 da
\[
K(\mathcal F_{\lambda_n})=W_{n-d}0.
\tag{65}
\]
El enderezamiento de un mapa de grado dos conserva la órbita crítica; (65) identifica su clase híbrida con la del centro cuadrático canónico de período \(2^{n-d}\). Las cotas a priori de la sucesión real de duplicación son las empleadas en el teorema de universalidad de Lyubich.

El [teorema 7.4 de Lyubich, pp. 387–388](https://www.maths.tcd.ie/EMIS/journals/Annals/149_2/lyubich.pdf#page=69) da una sola intersección con cada una de esas clases, a niveles suficientemente altos, sobre la transversal analítica y dentro de una vecindad fija del parámetro de acumulación.

Por (63), \(\lambda_n\) entra finalmente en esa vecindad. La continuación local de §8, indexada por el mismo período, pertenece a la misma clase híbrida. La unicidad implica
\[
\boxed{\lambda_n=\widehat\mu_n\quad(n\ge n_0),}
\tag{66}
\]
donde \(\widehat\mu_n\) designa el centro local de período físico \(2^n\). Es una reindexación de \(\mu_j\) mediante un desplazamiento fijo determinado por los retornos y el blanco de §8. La selección original de \(\lambda_n\) permanece intacta.

El entero \(n_0\) es existencial en esta prueba. La continuación de todos los niveles y la palabra \(W_n0\) ya están demostradas en (50); (66) aporta la identidad métrica necesaria para el límite.

### 17.3. Teorema de escalado para las primeras raíces HMT

**Teorema.** Para la familia uniforme (1), sean \(\lambda_n\) las sucesivas primeras raíces nuevas de período crítico exacto \(2^n\). Existen \(C>0\), \(0<\theta<1\) y \(M<\infty\) tales que, para todo \(n\) suficientemente grande,
\[
\lambda_*-\lambda_n=C\delta^{-n}(1+e_n),
\qquad |e_n|\le M\theta^n,
\tag{67}
\]
y
\[
\boxed{\lim_{n\to\infty}
\frac{\lambda_{n-1}-\lambda_{n-2}}
{\lambda_n-\lambda_{n-1}}=\delta.}
\tag{68}
\]

**Demostración.** (66) transporta el escalado local (24) a las raíces originales; el desplazamiento finito de índices se absorbe en \(C,M\). Su signo es positivo porque \(\lambda_n<\lambda_*\).

El resto de potencia admite además una justificación directa mediante la holonomía de clases híbridas. El lema 7.3 de Lyubich da regularidad \(C^{1+\beta}\), con derivada no nula, sobre la transversal en el punto de acumulación. La dinámica unidimensional inestable es analítica y tiene multiplicador \(\delta>1\); su coordenada linealizante hace que los centros sucesivos estén a distancia proporcional a \(\delta^{-n}\). Componer con la inversa de la holonomía da un término lineal no nulo y un resto \(O(\delta^{-(1+\beta)n})\). Así se puede tomar \(\theta=\delta^{-\beta}\).

Escribiendo
\[
r_n=\frac{\delta e_{n-1}-e_n}{\delta-1},
\qquad K=\frac{M(\delta+\theta)}{\delta-1},
\]
se obtiene
\[
\lambda_n-\lambda_{n-1}
=C(\delta-1)\delta^{-n}(1+r_n),\qquad
|r_n|\le K\theta^{n-1}.
\]
Por tanto,
\[
\left|
\frac{\lambda_{n-1}-\lambda_{n-2}}
{\lambda_n-\lambda_{n-1}}-\delta
\right|
\le
\frac{\delta K(1+\theta)\theta^{n-2}}
{1-K\theta^{n-1}},
\quad K\theta^{n-1}<1.
\tag{69}
\]
El lado derecho tiende a cero, demostrando (68).

### 17.4. Encadenamiento y alcance del cierre

La composición efectiva es: lector dodecafásico APP–TRIT–TPK; perfil (1); transporte ordenado de retornos (38)–(40); clasificación y existencia de las primeras raíces (50); localización (52); aislamiento por primera salida (63); identidad eventual de centros (66); escalado (67)–(69). La representación de Jacobi (43) conserva el perfil completo de este lector y sus marcas permanecen en el antecedente.

La expansión espacial del lector HMT y el refinamiento nonádico aportan la genealogía y la evaluación a profundidad arbitraria. El escalado entre parámetros se demuestra mediante la dinámica del retorno, la transversalidad y el aislamiento que acabamos de componer. Las pruebas analíticas citadas intervienen sobre la familia ya construida; sus valores de comparación no seleccionan sus fases ni sus coeficientes.

El cierre se refiere al selector global original del sector uniforme \(\eta=0\), con las dependencias teoremáticas enumeradas. Las cotas numéricas de \(M,\theta,n_0\), la estimación efectiva del error de \(\delta_8\) respecto a \(\delta\) y la extensión cuantificada a \(\eta\ne0\) conservan su estatuto separado. La anchura de una caja de raíces finitas mide precisión de evaluación, mientras (69) mide convergencia hacia el límite.

Los programas y certificados contiguos permiten reproducir las partes finitas de la prueba. La continuación a toda profundidad se sustenta en las inducciones, el argumento uniforme de primera salida y los teoremas de identificación, con sus dominios explícitos.

<!-- FIN ÍNTEGRO escalado -->


---

<!-- COMIENZO ÍNTEGRO clasificacion -->

# Clasificación de los retornos superestables anteriores al itinerario infinito y convergencia del selector global

## 1. Objeto y procedencia

Este apéndice conserva la familia publicada por el lector dodecafásico HMT:

\[
u_0(x)=\frac1{12}\sum_{m=1}^{12}\left(1-\cos\frac{2(3m-1)x}{\sqrt{899}}\right),
\qquad f_\lambda(x)=1-\lambda u_0(x).
\]

La construcción APP–TRIT–TPK del perfil, sus coeficientes y sus lectores precede a este argumento. El objeto del apéndice es el transporte del selector de raíces ya fijado en `c37_feigenbaum.tex`, líneas 247–256; se conserva íntegramente su definición. Las propiedades analíticas y de unimodalidad de esta familia constan en `DESARROLLO_DEMOSTRATIVO_FEIGENBAUM.md`; la existencia y compacidad del conjunto de parámetros con itinerario infinito, junto con sus márgenes de separación, están demostradas en §§6.1–6.2 de `PROLONGACION_NONADICA_Y_LIMITE_FEIGENBAUM.md`.

El argumento siguiente es propio y utiliza exclusivamente esas propiedades y las operaciones de retorno de la familia fijada. No utiliza como entrada un parámetro de otra familia ni el valor de una constante universal. Las hojas de los itinerarios aquí utilizados son las dos ramas monótonas del lector crítico; las restantes coordenadas y la memoria HMT conservan su residencia en el estado del que procede el lector.

Escribimos
\[
c_j(\lambda)=f_\lambda^j(0),\qquad
\tau_j=(-1)^{v_2(j)},\qquad
W_n=\tau_1\cdots\tau_{2^n-1}.
\]
El itinerario de una órbita crítica que retorna por primera vez al origen termina en el símbolo cero. El orden de itinerarios es el orden unimodal de máximo: antes de comparar el símbolo de índice \(j\), el factor de orientación es
\[
O_{j-1}(K)=\prod_{i=1}^{j-1}(-K_i).
\]
El orden ordinario de los símbolos es \(-1<0<1\).

## 2. Clasificación anterior a la palabra infinita

**Teorema 1.** Sea \(F:I\to I\), con \(I=[\ell,1]\), \(\ell<0\), un mapa continuo, estrictamente creciente a la izquierda de cero y estrictamente decreciente a su derecha, cuyo máximo satisface \(F(0)=1\). Supóngase que cero tiene período exacto \(2^n\), con \(n\ge1\), y que su itinerario crítico \(K\) satisface \(K<\tau\). Entonces
\[
\boxed{K=W_n0.}
\]
La conclusión se refiere al itinerario, y permite que parámetros distintos de una familia tengan ese mismo itinerario.

**Demostración.** Denotemos \(d_j=F^j(0)\). Para período dos el itinerario es \(+0=W_10\). Consideremos un período exacto \(p=2^n\ge4\).

Se tiene \(d_2<0\). En efecto, \(d_2=0\) daría período dos. Si \(d_2>0\), la monotonía de la rama positiva da
\[
F([d_2,1])=[d_2,d_3]\subset[d_2,1],
\]
y la órbita crítica permanece en un intervalo estrictamente positivo, incompatible con el retorno a cero.

Los signos iniciales son entonces \(+,-\). El factor de orientación para comparar el tercer signo es \(-1\); por ello \(K<\tau\) obliga a \(d_3>0\). Un cero en ese lugar produciría período tres.

Tampoco puede ocurrir \(d_4<0\). Bajo esta hipótesis,
\[
d_2<d_4<0,
\qquad F([d_2,d_4])=[d_3,d_5]\subset(0,1],
\]
pues \(d_4=F(d_3)>F(1)=d_2\) y \(d_5=F(d_4)>F(d_2)=d_3\). La rama positiva es decreciente, de modo que
\[
F^2([d_2,d_4])=[d_6,d_4]\subset[d_2,d_4].
\]
Aquí \(d_6\ge d_2\), porque \(d_5\le1\), y \(d_6<d_4\), porque \(d_5>d_3\). Este intervalo estrictamente negativo atrapa los retornos pares de la órbita crítica, y excluye el retorno a cero. Por tanto \(d_4\ge0\). Si \(p=4\), se obtiene precisamente \(+-+0=W_20\).

Supongamos ahora \(p\ge8\). Entonces \(d_4>0\). Los factores de orientación para los signos quinto y sexto son, respectivamente, \(-1\) y \(+1\). Como \(\tau_5=+1\) y \(\tau_6=-1\), la desigualdad \(K<\tau\) obliga a
\[
\operatorname{sign}(d_1,\ldots,d_6)=(+,-,+,+,+,-).
\tag{1}
\]
Los signos cero en esos lugares están excluidos por el período exacto.

Construimos el intervalo de retorno
\[
J=[d_2,d_4].
\]
La desigualdad \(F(d_3)=d_4>0>d_6=F(d_5)\), junto con \(d_3,d_5>0\), implica \(d_3<d_5\); por tanto
\[
F(J)=[d_3,1].
\]
Además \(d_4<d_3\). Para comprobarlo, la imagen por \(F\) del intervalo de extremos \(d_3,d_4\) es estrictamente positiva, pues sus imágenes extremas son \(d_4,d_5>0\). En ese intervalo \(F^2\) es estrictamente creciente. Sus valores extremos satisfacen
\[
F^2(d_3)=d_5>0>d_6=F^2(d_4),
\]
lo que fuerza \(d_3>d_4\). En consecuencia,
\[
J\cap F(J)=\varnothing,
\qquad F^2(J)=F([d_3,1])=[d_2,d_4]=J.
\tag{2}
\]

El mapa \(F^2|_J\) posee un único mínimo en cero. La conjugación por \(h(x)=d_2x\), que invierte la orientación, define
\[
G=h^{-1}\circ F^2\circ h:
\left[\frac{d_4}{d_2},1\right]\longrightarrow
\left[\frac{d_4}{d_2},1\right].
\tag{3}
\]
Este mapa satisface las mismas hipótesis de máximo que \(F\), con \(G(0)=1\), y su crítico tiene período exacto \(p/2\). Su itinerario es
\[
K'_j=-K_{2j}.
\tag{4}
\]
Todos los símbolos impares de \(K\) son positivos, porque las posiciones pares pertenecen a \(J\) y las impares a \(F(J)\subset(0,1]\).

La transformación (4) conserva el orden de comparación con \(\tau\). En efecto, \(\tau_{2j-1}=+1\) y \(\tau_{2j}=-\tau_j\). Si \(q\) es el primer lugar en que \(K'\) y \(\tau\) difieren, el primer lugar de diferencia entre \(K\) y \(\tau\) es \(2q\), y
\[
O_{2q-1}(K)=-O_{q-1}(K'),
\qquad K_{2q}-\tau_{2q}=-(K'_q-\tau_q).
\tag{5}
\]
El producto que determina el orden es idéntico. Las identidades siguen siendo válidas cuando el primer símbolo distinto es el cero final. Así \(K'<\tau\).

La inducción aplicada a \(G\) da \(K'=W_{n-1}0\). Las posiciones impares positivas y (4) reconstruyen exactamente \(K=W_n0\). Queda demostrado el teorema. □

El teorema demuestra también que cada mapa clasificado posee los retornos restrictivos de duplicación anteriores a su retorno superestable, con los dominios de (2)–(3). No presupone una monotonía del parámetro de una familia.

**Normalización simétrica de la familia fijada.** Cuando \(F\) es par y está definido sobre \([-1,1]\), las desigualdades anteriores dan además
\[
F(d_4)=d_5>d_3=F(d_2)=F(-d_2).
\]
Como ambos argumentos \(d_4,-d_2\) son positivos y \(F\) decrece en esa rama,
\[
0<d_4<-d_2<1.
\tag{5a}
\]
Por tanto \(F^2([d_2,-d_2])=[d_2,d_4]\), y la misma conjugación \(h(x)=d_2x\) define sobre todo \([-1,1]\) un mapa par de máximo cuya imagen es \([d_4/d_2,1]\subset[-1,1]\). Coincide exactamente con el operador \(RF=-F(F(-ax))/a\), \(a=-F(1)\), utilizado en el corpus. Esta ampliación simétrica conserva el retorno crítico, su período y su itinerario.

## 3. Primer parámetro de itinerario infinito

Trabajamos sobre el intervalo compacto ya utilizado en la demostración de existencia,
\[
L=\left[\frac1{2u_0(1)},\frac2{u_0(1)}\right].
\]
Sea
\[
\Lambda_\tau=\{\lambda\in L:
\operatorname{sign}c_j(\lambda)=\tau_j\text{ para todo }j\ge1\}.
\]
Por §§6.1–6.2 del desarrollo de prolongación, este conjunto es no vacío y compacto. Por tanto existe
\[
a=\min\Lambda_\tau.
\tag{6}
\]

**Lema 2.** Para todo \(\lambda\in[1/(2u_0(1)),a)\), se tiene \(K_\lambda<\tau\).

**Demostración.** En el extremo izquierdo, el itinerario es \(+^\infty<\tau\). El argumento de separación de §6.1 demuestra que los conjuntos de comparación estricta con \(\tau\) son abiertos: en un itinerario infinito distinto de \(\tau\), la primera diferencia finita persiste por continuidad; en un parámetro superestable, las dos palabras periódicas vecinas y la palabra con cero final se sitúan en el mismo lado de \(\tau\), por su maximalidad estricta. El intervalo anterior a \(a\) carece, por definición, de parámetros con itinerario \(\tau\). Su conexidad mantiene la comparación inicial en todo ese intervalo. □

## 4. Existencia de cada primera raíz nueva

Conservamos el selector original. La primera raíz es
\[
\lambda_1=\frac1{u_0(1)},
\]
y, para \(n\ge2\), \(\lambda_n\) es la primera raíz de \(c_{2^n}\) situada a la derecha de \(\lambda_{n-1}\) que satisface
\[
c_{2^j}(\lambda_n)\ne0\quad(1\le j<n).
\tag{7}
\]
Como cualquier primer período que divida \(2^n\) es una potencia de dos, (7) equivale a exigir período crítico exacto \(2^n\).

**Lema 3.** Todas las raíces de este selector existen y cumplen
\[
\lambda_1<\lambda_2<\cdots<\lambda_n<a.
\tag{8}
\]

**Demostración.** El signo \(c_2(a)<0\) implica \(\lambda_1<a\). Supongamos construida \(\lambda_{n-1}<a\), y pongamos \(p=2^{n-1}\). La función analítica \(c_p(\lambda)\) no es idénticamente cero, puesto que \(c_p(a)\ne0\). Su conjunto de ceros en \([\lambda_{n-1},a]\) es finito, no vacío y carece de \(a\). Sea \(z<a\) su último cero.

En \((z,a]\), el signo de \(c_p\) es constante e igual a \(s=\tau_p\). Para \(g_\lambda=f_\lambda^p\), se tiene
\[
g_\lambda(0)=c_p(\lambda),\qquad g'_\lambda(0)=0.
\]
Una cota uniforme local de la segunda derivada da
\[
c_{2p}(\lambda)
=g_\lambda(c_p(\lambda))
=c_p(\lambda)+O(c_p(\lambda)^2).
\tag{9}
\]
Al aproximarse \(\lambda\) a \(z\) por la derecha, el término de primer orden domina; por tanto \(c_{2p}(\lambda)\) tiene signo \(s\). En \(a\), su signo es
\[
\tau_{2p}=-\tau_p=-s.
\]
El teorema del valor intermedio proporciona un cero \(\beta\in(z,a)\) de \(c_{2p}\). Como \(c_p\ne0\) en ese intervalo, el período crítico en \(\beta\) es exactamente \(2p\).

La analiticidad y \(c_{2p}(a)\ne0\) implican que los ceros de \(c_{2p}\) en \([\lambda_{n-1},a]\) son finitos. Entre sus ceros de período exacto \(2p\), situados a la derecha de \(\lambda_{n-1}\), existe así un primero. Es el selector original \(\lambda_n\), y satisface \(\lambda_n\le\beta<a\). □

La utilización del último cero auxiliar \(z\) pertenece únicamente a la prueba de existencia. El parámetro seleccionado continúa siendo la **primera raíz nueva** \(\lambda_n\).

## 5. Convergencia del selector global al primer itinerario infinito

**Teorema 4.** Para la familia HMT fijada y el selector original, todos los itinerarios seleccionados son canónicos y
\[
\boxed{K_{\lambda_n}=W_n0,\qquad
\lambda_n\nearrow\min\Lambda_\tau.}
\tag{10}
\]

**Demostración.** Los lemas 2–3 sitúan cada parámetro seleccionado por debajo de \(a\), con itinerario menor que \(\tau\). El teorema 1 identifica ese itinerario con \(W_n0\). La sucesión es creciente y acotada por \(a\); sea \(b\le a\) su límite.

Fijemos \(p\ge1\). Para \(n\) suficientemente grande, \(2p<2^n\). Entonces los signos de \(c_p(\lambda_n)\) y \(c_{2p}(\lambda_n)\) coinciden con \(\tau_p\) y \(\tau_{2p}=-\tau_p\), respectivamente. La cota de §6.2,
\[
\|(f_\lambda^p)''\|\le B_p,
\qquad B_p=16^p\frac{16^p-1}{15},
\]
y la identidad \((f_\lambda^p)'(0)=0\) implican
\[
|c_{2p}(\lambda_n)-c_p(\lambda_n)|
\le\tfrac12B_p|c_p(\lambda_n)|^2.
\]
Como los dos términos del lado izquierdo tienen signos contrarios,
\[
|c_p(\lambda_n)|>2/B_p.
\tag{11}
\]
Por continuidad, \(c_p(b)\) conserva el signo \(\tau_p\) y satisface \(|c_p(b)|\ge2/B_p>0\). Esto vale para cada \(p\), de modo que \(b\in\Lambda_\tau\). La minimalidad de \(a\) da \(b\ge a\), y por tanto \(b=a\). □

La prueba completa conserva el selector global y produce sus itinerarios y su límite. La información de los primeros ocho niveles es compatible con el resultado, pero la demostración de (10) no extrapola esos ocho niveles: utiliza inducción, intervalos invariantes y separación uniforme de cada signo.

## 6. Relación exacta con el cruce local certificado

Sea \(J=[J_{\rm lo},J_{\rm hi}]\) el intervalo del cruce local \(\lambda_*\) construido en `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §§5–8. Allí \(\lambda_*\in\Lambda_\tau\), y por ello
\[
a\le\lambda_*.
\]
Si se demuestra
\[
\Lambda_\tau\cap[\lambda_8,J_{\rm lo}]=\varnothing,
\tag{12}
\]
el teorema 4 implica
\[
J_{\rm lo}<a\le\lambda_*<J_{\rm hi}.
\tag{13}
\]
La identificación ulterior \(a=\lambda_*\) se deduce, por ejemplo, de que \(\lambda_*\) sea el único parámetro de \(J\) con itinerario \(\tau\). La unicidad de un cruce con una **hoja estable local** y la unicidad de todos los parámetros de itinerario \(\tau\) en \(J\) son afirmaciones distintas: para pasar de la primera a la segunda se debe controlar que los retornos de cualquier realización de \(\tau\) en \(J\) permanezcan en el dominio local, o demostrar un enunciado de aislamiento equivalente.

Análogamente, una vez identificado \(a=\lambda_*\), la igualdad eventual de las primeras raíces \(\lambda_n\) con los centros \(\mu_j\) de la continuación local se obtiene si, para cada período suficientemente grande, el centro local es el único centro de itinerario \(W_n0\) en un entorno pertinente de \(\lambda_*\) que contenga la cola de \(\lambda_n\). La correspondencia conserva el desplazamiento fijo de índices de §8. Estas son las condiciones concretas de transporte del selector; la conclusión (10) ya está demostrada sin ellas.

## 7. Controles lógicos y falsadores

1. El teorema 1 requiere un máximo unimodal estricto y un intervalo invariante. Si alguno de los dos ramos pierde monotonía, los intervalos (2) pueden dejar de ser restrictivos y la clasificación debe comprobarse de nuevo.
2. La condición \(K<\tau\) es esencial. Después de la palabra límite pueden existir centros de período \(2^n\) con otras combinatorias; el teorema no los identifica con \(W_n0\).
3. La analiticidad en el parámetro proporciona aislamiento y finitud de los ceros sobre el compacto. Para una familia solamente continua, la existencia de una primera raíz estrictamente posterior requiere un argumento adicional.
4. Un límite de raíces críticas puede, en general, perder signos al alcanzar un retorno de período menor. La desigualdad (11) excluye precisamente ese fenómeno para esta sucesión y cada horizonte fijo.
5. La convergencia de las primeras raíces al primer parámetro de itinerario \(\tau\) no equivale a la unicidad de todos los parámetros de ese itinerario ni determina por sí misma una tasa métrica. El cruce transversal y la identificación de la rama aportan esas conclusiones posteriores.

## 8. Transferencia métrica al selector original bajo la identificación del límite

En esta sección se conserva como hipótesis explícita la identificación
\[
\boxed{a_*:=\min\Lambda_\tau=\lambda_*.}
\tag{H}
\]
Su comprobación corresponde al aislamiento paramétrico de §6 y a su certificado específico. La demostración siguiente establece la consecuencia de (H); no utiliza la existencia de la cascada local como prueba de (H). Así queda separada la comprobación de aislamiento de la transferencia métrica.

**Nota de activación.** La hipótesis (H) queda demostrada en `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §16, mediante la primera salida del cono negativo y la cobertura racional completa de 64 bandas, sin huecos, de `CERTIFICADO_CAP_NEGATIVA_PRIMERA_SALIDA.json`. El enunciado condicional se conserva para exhibir esta dependencia de la transferencia; el resultado de §16 la satisface para la familia uniforme aquí estudiada.

La familia, el perfil dodecafásico, los retornos y el selector se mantienen exactamente como en §§1–5. Los resultados externos empleados a continuación reconocen la dinámica de ese objeto ya construido. Sus valores universales no intervienen en la selección de coeficientes ni de parámetros de la familia HMT.

**Teorema 5.** Supóngase (H), además de las cotas de entrada, admisibilidad y transversalidad de `TRANSVERSALIDAD_Y_ESCALADO_LOCAL_FEIGENBAUM.md`, §§4–7. Entonces la sucesión original de primeras raíces nuevas satisface, para ciertas constantes \(C>0\) y \(0<\theta<1\),
\[
\boxed{\lambda_*-\lambda_n=C\delta^{-n}
\bigl(1+O(\theta^n)\bigr),}
\tag{14}
\]
donde \(\delta>1\) es el autovalor inestable del operador de duplicación en el punto fijo reconocido. En particular,
\[
\frac{\lambda_{n-1}-\lambda_{n-2}}
     {\lambda_n-\lambda_{n-1}}
=\delta+O(\theta^n).
\tag{15}
\]
La sucesión coincide eventualmente con los centros de la continuación local, una vez que ambos índices se refieren al mismo período físico. La prueba mantiene el selector de primera raíz de §1.

### 8.1. Obtención de un dominio cuadrático semejante común

Escribamos \(g\) para el punto fijo de la renormalización y
\(\Gamma(\lambda)=R^4f_\lambda\). La carta analítica utilizada en el certificado es
\[
f(x)=1-x^2V\!\left(\frac{x^2-1}{2.5}\right),\qquad
V(z)=\frac{u}{10}+\sum_{k\ge1}\nu_kz^k,
\]
con norma de diferencias \(|\Delta u|+\|\Delta\nu\|_1\). Las desigualdades de admisibilidad prueban que \(g\) es par, analítico, unimodal, cuadrático y de tipo de duplicación; además, \(g(x)=\varphi(x^2)\) con \(\varphi'<0\) en \([0,1]\).

El teorema 2.1 de de Faria–de Melo–Pinto, aplicado al conjunto de combinatorias formado únicamente por la duplicación, proporciona un conjunto límite de un solo punto con extensión cuadrática semejante. Como \(Rg=g\), la convergencia real de ese teorema identifica dicho punto con \(g\). El lema 3.2 proporciona, en un entorno analítico de \(g\), una iteración finita de renormalización con dominio cuadrático semejante y módulo uniformemente positivo. Los localizadores son §2.1–2.3, pp. 736–738, y §3.1, lema 3.2, p. 745, de [de Faria–de Melo–Pinto, *Global hyperbolicity of renormalization for Cr unimodal mappings*](https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n3-p01.pdf).

Para comprobar la pertenencia al entorno de ese lema, sea \(\Omega_\epsilon\) un entorno complejo suficientemente pequeño de \([-1,1]\), con
\[
\rho_\epsilon:=\sup_{x\in\Omega_\epsilon}
\left|\frac{x^2-1}{2.5}\right|<1,
\qquad M_\epsilon:=\sup_{x\in\Omega_\epsilon}|x|^2<\infty.
\]
La restricción de la carta certificada satisface
\[
\|\Delta f\|_{\Omega_\epsilon}
\le M_\epsilon\left(\frac{|\Delta u|}{10}
          +\rho_\epsilon\|\Delta\nu\|_1\right)
\le C_\epsilon\|\Delta f\|_{\mathcal A}.
\tag{16}
\]
El certificado da
\[
\|R^m\Gamma(\lambda_*)-g\|_{\mathcal A}
<0.001666(0.83996)^m.
\]
Se elige por ello un entero fijo \(m\) que sitúe esta imagen en el entorno del lema 3.2. La continuidad de la composición finita proporciona un intervalo \(I_*\) alrededor de \(\lambda_*\) donde las mismas operaciones están definidas. Si \(N\) es la iteración suministrada por dicho lema, ponemos
\[
d=4+m+N,\qquad
\mathcal F_\lambda=R^df_\lambda,\quad \lambda\in I_*.
\tag{17}
\]
La familia \(\mathcal F\) posee representantes cuadráticos semejantes de grado dos, sobre un dominio común y con módulo positivo uniforme. Su dependencia analítica real admite una complejificación local del parámetro. El número \(d\) es fijo y cuenta las duplicaciones realizadas antes de aplicar el resultado paramétrico.

Esta construcción prueba la existencia del dominio y de \(d\); no les atribuye valores numéricos que el certificado local no haya calculado. La asintótica utiliza su finitud, no una estimación numérica de su tamaño.

### 8.2. Transporte de la transversalidad certificada

La dirección de \(\Gamma\) satisface el cono
\[
\|\dot\nu\|_1\le\tfrac14|\dot u|,\qquad \dot u\ne0.
\]
Las cotas diferenciales certificadas implican invariancia de este cono y
\[
|\dot u_{k+1}|\ge4.381|\dot u_k|
\tag{18}
\]
a lo largo de la órbita de \(\Gamma(\lambda_*)\). Todos sus puntos permanecen en el dominio certificado. En particular, la dirección transportada por los pasos finitos de (17) conserva una componente expansiva no nula.

La clase híbrida del punto fijo coincide con su variedad estable en el espacio de gérmenes cuadráticos semejantes: [Lyubich, *Feigenbaum–Coullet–Tresser universality and Milnor's hairiness conjecture*, teorema 6.1, pp. 371–372](https://www.maths.tcd.ie/EMIS/journals/Annals/149_2/lyubich.pdf). La transversalidad sigue siendo válida al pasar a ese espacio, como puede comprobarse sin identificar normas de Banach diferentes. En efecto, si \(\partial_\lambda\mathcal F_{\lambda_*}\) fuese tangente a la clase híbrida, sería la tangente de un disco analítico contenido en ella. La convergencia exponencial uniforme de la renormalización sobre un subdisco compacto, seguida de la estimación de Cauchy en su parámetro, haría converger a cero la evaluación en \(x=1\) de sus tangentes renormalizadas. Sin embargo, en la carta anterior,
\[
\dot f(1)=-\dot u/10,
\]
y (18) hace crecer su valor absoluto. Ambas derivadas representan el mismo germen y tienen la misma evaluación real. La contradicción demuestra
\[
\partial_\lambda\mathcal F_{\lambda_*}
\notin T_{\mathcal F_{\lambda_*}}\mathcal H_{c_\infty}.
\tag{19}
\]
Así, \(S=\{\mathcal F_\lambda\}\) es una transversal analítica compleja a la clase híbrida del límite de duplicación.

### 8.3. Identificación eventual de las primeras raíces por su período

Denotemos por \(c_r\) el centro cuadrático canónico de período \(2^r\), obtenido mediante \(r\) duplicaciones sucesivas del centro de período uno. Este símbolo designa el parámetro de la familia cuadrática de reconocimiento; se distingue de las funciones orbitales \(c_j(\lambda)=f_\lambda^j(0)\) de las secciones anteriores. Si se desea evitar cualquier coincidencia tipográfica, puede escribirse \(c_r^{\rm quad}\).

El teorema 4 y (H) dan \(\lambda_n\to\lambda_*\), por lo que \(\lambda_n\in I_*\) para \(n\) suficientemente grande. La clasificación e intervalos restrictivos de §2 muestran que, cuando \(n>d\),
\[
\mathcal F_{\lambda_n}=R^df_{\lambda_n}
\quad\text{tiene período crítico exacto }2^{n-d}
\quad\text{e itinerario }W_{n-d}0.
\tag{20}
\]
Su órbita crítica permanece en el intervalo real invariante, contenido en el dominio cuadrático semejante; su conjunto de Julia lleno es, por tanto, conexo. La rectificación conserva la órbita postcrítica y las ramas reales. Al recorrer sus retornos restrictivos se obtienen \(n-d\) duplicaciones canónicas y, al final, un punto crítico fijo. Este último rectifica al centro \(0\); las inversas sucesivas de la rectificación de las copias de duplicación dan el centro único \(c_{n-d}^{\rm quad}\). Esta es la aplicación concreta de la parametrización por combinatoria y del homeomorfismo de rectificación de las copias, descritos en Lyubich, §5.1–5.3, pp. 362–364. Se concluye
\[
\mathcal F_{\lambda_n}\in\mathcal H_{c_{n-d}^{\rm quad}}.
\tag{21}
\]

El teorema 7.4 de Lyubich, pp. 387–388, da una única intersección local de \(S\) con cada clase \(\mathcal H_{c_r^{\rm quad}}\) para \(r\) suficientemente grande. Sus hipótesis de cotas complejas a priori se cumplen para la cascada cuadrática real de duplicación, conforme al teorema 5.6, p. 367, del mismo trabajo. Escribamos \(\zeta_r\) para el parámetro de esa intersección. Las ecuaciones (20)–(21), la convergencia al cruce y la unicidad local implican
\[
\boxed{\lambda_n=\zeta_{n-d}\quad\text{para todo }n\text{ suficientemente grande}.}
\tag{22}
\]
La unicidad utilizada aquí corresponde a **cada clase híbrida canónica** en un entorno fijo del cruce. No se infiere de la mera existencia de una cascada local ni de la unicidad del cruce con la hoja estable. La ecuación (22) identifica el selector original, ya definido globalmente, con las intersecciones locales; no introduce un selector sustitutorio.

En particular, sea \(\mu_j\) la cascada local de §8 del documento principal, y sea \(s\) el entero fijo determinado por su período físico exacto:
\[
\operatorname{per}_{\rm crit}(f_{\mu_j})=2^{j+s}.
\]
En la presentación con curva \(R^4f_\lambda\) y blanco de período dos, \(s=5\); los pasos fijos adicionales usados para localizar el blanco modifican \(s\). Por (21) y la misma unicidad,
\[
\mu_j=\zeta_{j+s-d},\qquad
\boxed{\lambda_n=\mu_{n-s}\quad(n\text{ suficientemente grande}).}
\tag{23}
\]
El desplazamiento \(d\) de la preparación cuadrática semejante y el desplazamiento \(s\) de los períodos del blanco son objetos distintos. La identificación se efectúa por el período físico, no igualando esos dos enteros.

### 8.4. Resto de potencia mediante holonomía transversal

El lema 7.3 de Lyubich, p. 384 y demostración en pp. 384–387, aporta regularidad \(C^{1+\beta}\)-conforme, para algún \(\beta>0\), de la holonomía entre transversales a la clase híbrida del punto de Feigenbaum. Su definición en p. 384 se refiere a los conjuntos de conexidad sobre las transversales; contiene, en particular, los centros considerados aquí. Podemos reducir el exponente para que \(0<\beta\le1\).

Sea \(h\) la holonomía desde \(S\) hacia la variedad inestable y sea \(z\) una coordenada analítica que linealiza la restricción unidimensional de la renormalización:
\[
z(g)=0,\qquad z(Rq)=\delta z(q).
\tag{24}
\]
La existencia de esta coordenada se obtiene aplicando la linealización de un germen holomorfo repulsor, de multiplicador \(\delta>1\), a la variedad inestable analítica. La dirección expansiva de (18), la invariancia del cono y el retorno estacionario identifican ese multiplicador con el autovalor inestable positivo empleado en el certificado.

Si \(q_r\) es el centro de la clase \(\mathcal H_{c_r^{\rm quad}}\) situado en la variedad inestable, la compatibilidad de rectificación y renormalización da \(Rq_r=q_{r-1}\). Esta identidad es la que se utiliza en la demostración del teorema 7.4, p. 388. Por (24), existe \(b\ne0\), que absorbe cualquier índice inicial fijo, tal que
\[
z(q_r)=b\delta^{-r}
\tag{25}
\]
para todo \(r\) suficientemente grande.

La regularidad de \(h\) y la transversalidad (19) dan, sobre el conjunto de conexidad cercano a \(\lambda_*\),
\[
H(\lambda):=z\bigl(h(\mathcal F_\lambda)\bigr)
=A(\lambda-\lambda_*)
+O\!\left(|\lambda-\lambda_*|^{1+\beta}\right),
\qquad A\ne0.
\tag{26}
\]
Como \(H(\zeta_r)=b\delta^{-r}\), la estimación inferior
\(|H(\lambda)|\ge |A|\,|\lambda-\lambda_*|/2\) en un entorno suficientemente pequeño implica primero
\(|\zeta_r-\lambda_*|=O(\delta^{-r})\). Sustituyendo esta cota en el resto de (26), resulta
\[
\zeta_r-\lambda_*=rac bA\delta^{-r}
+O\!\left(\delta^{-(1+\beta)r}\right).
\tag{27}
\]
Aplicamos (22) con \(r=n-d\). El desplazamiento finito modifica el coeficiente principal y la constante del resto. Puesto que \(\lambda_n<\lambda_*\), se obtiene (14), con
\[
C=-\frac bA\delta^d>0,
\qquad \theta=\delta^{-\beta}\in(0,1).
\]
Finalmente,
\[
\lambda_n-\lambda_{n-1}
=C(\delta-1)\delta^{-n}\bigl(1+O(\theta^n)\bigr),
\]
lo que demuestra (15). □

### 8.5. Alcance cuantitativo y condición de activación

El argumento prueba la existencia de un resto geométrico para las **primeras raíces globales** cuando se verifica (H). La tasa \(0.83996\) ya certificada controla la convergencia de los mapas renormalizados sobre la hoja estable. La tasa \(\theta=\delta^{-\beta}\) de (14) controla la transferencia al parámetro mediante la holonomía; ambas conservan sus dominios respectivos.

Esta sección no asigna valores certificados a \(\beta\), \(\theta\), \(C\), al tamaño del entorno \(I_*\), al número de retornos preparatorios \(d\) ni al primer índice de coincidencia de (22)–(23). La prueba asintótica requiere que existan, y las construcciones anteriores acreditan esa existencia. Para activar el teorema 5 en la familia concreta se incorpora la demostración material de (H); un certificado de primeras raíces finitas o un cruce estable único, considerados aisladamente, no sustituyen esa identificación.

<!-- FIN ÍNTEGRO clasificacion -->
