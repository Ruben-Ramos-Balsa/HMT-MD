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
