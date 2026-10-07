# Transducción aritmético-geométrica y recuperación desde el registro bilateral

14 de septiembre de 2026. Ampliación posterior a la carpeta 02, que permanece intacta. Se conserva la denominación autoral aprobada **constante holográfica de acoplamiento aritmético-geométrico** para el objeto generado K, distinguiéndolo de sus representaciones escalares, sus marcos y los operadores que lo transportan.

## 1. Objetos y dependencias de la composición

El punto de partida es el registro generado por APP–TRIT–TPK, dentro del estado enriquecido y de la estructura discreta conjunta del continuo. La inversión de Hadamard, el orden de las ventanas, los lectores de incidencia y la expansión con acarreo son antecedentes del manuscrito. La aplicación de esta nota empieza sobre ese registro producido; no construye retrospectivamente las semillas desde sus valores.

Conviene separar cuatro objetos:

1. K es el registro ordenado, con origen, orientación y procedencia. Su realización lineal ocupa H=R12.
2. kappa es una lectura escalar de K, con base mil y doce posiciones fijadas.
3. O_K es la matriz cuyas columnas son las doce traslaciones del registro; permite identificar coordenadas y respuestas lineales porque se ha probado su invertibilidad.
4. W_a es un operador bilateral sobre estados: recibe un vector, lo distribuye entre dos canales y conserva su norma. No es K ni kappa.

Fuentes inmediatas:

- [Registro y transformación integral](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/sections/registro_k.tex:305>): H12, registro firmado, inversión y K.
- [Marco cíclico y respuestas](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/EXPLORACION.md:123>): espectro de O_K, inversa e identificación de operadores.
- [Balance bilateral](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_02_NOMBRE_Y_RADIO_20260914/PRUEBA_INVERSA_BIDIRECCIONAL.md:144>): definición y recuperación de W_a en el ciclo ternario.
- [Terminal y recuperación no estacionaria](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/10.tex:140>): telescopía, límite fuerte y adjunto.
- [Isometría incidencial](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/05.tex:3>): F, su imagen y su producto ponderado.
- [Separación y decodificación de memorias](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/APORTE_INCIDENCIA.md:54>): M, radios exactos y reconstrucción entera.

No se identifica todo el estado enriquecido con las doce coordenadas de este lector. La recuperación demostrada concierne a este registro y a las funciones que tienen en él y en las marcas acompañantes sus argumentos suficientes.

## 2. Balance bilateral en fibras y transferencia completa

Sean B,C:H→H' dos isometrías con el mismo dominio, a>0,

\[
 p=a^2+a+1,\qquad c=(2a+1)p,\qquad
 Q_-=aB-C,\quad Q_+=(a+1)B+C.
\]

La ley ampliada por el desarrollo principal es

\[
 (a+1)Q_-^*Q_-+aQ_+^*Q_+=cI.
\]

Su prueba usa B*B=C*C=I: los términos B*C+C*B aparecen con coeficientes opuestos y se cancelan. No requiere que B*C tenga orden tres. Sean

\[
 A_a=\frac{\sqrt{a+1}}{\sqrt c}Q_-,\qquad
 D_a=\frac{\sqrt a}{\sqrt c}Q_+,
 \qquad W_av=(A_av,D_av).
\]

Así W_a*W_a=I. La letra D_a de esta sección designa el segundo canal bilateral; los lectores D3,D4 de las memorias antecedentes conservan sus fórmulas propias.

### Proposición 1 — Transferencia cuantitativa en cualquier dimensión

El canal que se continúa satisface

\[
 \|A_a\|^2\le r_a:=\frac{(a+1)^3}{(2a+1)(a^2+a+1)}
 =1-\frac{a^3}{(2a+1)(a^2+a+1)}<1.
\]

**Prueba.** La desigualdad triangular da ||aB−C||≤a+1. Multiplicar por (a+1)/c prueba la cota. Expandir c−(a+1)^3=a^3 prueba la igualdad y la positividad estricta. Por el balance, D_a*D_a≥(1−r_a)I.

Considérese ahora una sucesión de pares isométricos B_n,C_n:H_n→H_(n+1), con el mismo a, sin imponer conmutación entre pasos. Sean A_n,D_n los canales anteriores, R0=I y R_(n+1)=A_nR_n. Definimos

\[
 Z_Nv=(R_Nv,D_0v,D_1R_1v,\ldots,D_{N-1}R_{N-1}v).
\]

El balance local telescopa:

\[
 Z_N^*Z_N=I,\qquad
 R_N^*R_N+\sum_{n<N}R_n^*D_n^*D_nR_n=I,
 \qquad \|R_N\|^2\le r_a^N.
\]

Consecuentemente, el terminal positivo límite es cero y

\[
 Z_\infty v=(D_nR_nv)_{n\ge0},\qquad
 Z_\infty^*Z_\infty=I,
\]

\[
 \boxed{v=\sum_{n\ge0}R_n^*D_n^*m_n,
 \qquad\|Z_\infty^*\|=1.}
\]

La serie converge en norma: las truncaciones de una sucesión cuadrado-sumable convergen y el adjunto de una isometría es acotado. Con datos exactos, usar sólo los primeros N complementos da el residuo exacto R_N*R_Nv, de norma a lo sumo r_a^N||v||. Con ruido de norma conjunta ε, esa reconstrucción tiene error a lo sumo ε+r_a^N||v||. Con todo el registro, el error es a lo sumo ε.

Esta política concreta continúa el primer canal y archiva el segundo. Si una evolución distinta del manuscrito conserva un terminal positivo no nulo, hay que incluir A_infty^(1/2)v y su adjunto: la conclusión de agotamiento no se traslada a cualquier secuencia por analogía.

### Proposición 2 — Memorias finitas sin terminal

Para M_Nv=(D_nR_nv)_(n<N),

\[
 M_N^*M_N=I-R_N^*R_N\ge(1-r_a^N)I.
\]

La inversa de mínimos cuadrados

\[
 L_N=(I-R_N^*R_N)^{-1}M_N^*
\]

recupera v exactamente y satisface ||L_N||≤(1−r_a^N)^−1/2. Es una inversa de un registro finito; no se confunde con la suma infinita ni con el adjunto truncado, que conserva el sesgo explícito de la proposición 1.

En el caso específico B=I,C=S4 del registro, la cota mejora a

\[
 \|A_a\|^2=\frac{a+1}{2a+1}.
\]

Para a=8 es 9/17; el otro autovalor del Gram es 441/1241 en el sector fijo. La tasa 9/17 es exacta en esta carta. La cota válida para cualesquiera dos isometrías es 729/1241.

Con un árbol que refine ambos canales, cada nivel completo también es isométrico. No se suman en una misma norma todas las capas completas: cada una ya contiene la norma total. La conservación debe expresarse mediante sus aplicaciones de refinamiento o por un registro de complementos como el anterior.

## 3. Marco cíclico, valor y respuesta tras la prolongación

Sea Z cualquiera de las isometrías completas anteriores, o una composición con las del manuscrito conservando todos sus terminales y complementos. Para

\[
 O_K=(K,SK,\ldots,S^{11}K),
\]

el resultado antecedente es

\[
 589609I\le O_K^*O_K\le39225169I.
\]

### Teorema 3 — Transducción de coordenadas con condicionamiento conservado

Si x=O_Kb, entonces z=Zx determina

\[
 b=O_K^{-1}Z^*z,
 \qquad\|\delta b\|\le\frac{\|\delta z\|}{\sqrt{589609}}.
\]

**Prueba.** Z*Z=I y O_K es invertible. El producto de Gram de ZO_K es O_K*O_K; las cotas y la inversa se conservan. Las doce columnas siguen formando una base de la imagen transportada, aunque el espacio de almacenamiento posea infinitas coordenadas.

Para un operador H que conmute con S, la respuesta completa y=HK determina H=O_yO_K^-1. Si sólo se recibe z=Zy+e, se recupera y_hat=Z*z y después

\[
 \widehat H=O_{\widehat y}O_K^{-1},\qquad
 \|\widehat H-H\|\le\sqrt{12/589609}\,\|e\|.
\]

La prueba usa ||O_e||≤√12||e||. Se mantiene la hipótesis HS=SH; doce respuestas son necesarias en el protocolo para un operador general. Una respuesta aquí es un vector completo, no un único escalar.

La conjugación del desplazamiento en im Z es S_Z=ZSZ*. De este modo S_Z^jZ=ZS^j. No se sustituye por una traslación arbitraria entre casillas de memoria.

### Lectura posicional

Con B0=1000 y d=B0^12−1, sea la fila

\[
 \ell=(B_0^{11},B_0^{10},\ldots,1)/d.
\]

Su extensión lineal actúa sobre H y kappa(K)=ell K en el dominio de palabras. El lector transportado tiene representante Z ell*, de modo que

\[
 \kappa(K)=\langle Z\ell^*,ZK\rangle,\qquad
 |\delta\kappa|\le\|\ell\|\,\|e\|,
\]

\[
 \|\ell\|^2=
 \frac{B_0^{12}+1}{(B_0^2-1)(B_0^{12}-1)}.
\]

La igualdad de norma procede de la suma geométrica. Desde los primeros N complementos, sin terminal y usando el adjunto truncado, el error adicional queda acotado por ||ell|| r_a^N||K||. Con la inversa L_N de la proposición 2, ese sesgo desaparece y la amplificación de ruido se declara explícitamente.

En el dominio entero 0,...,999, el conocimiento exacto de kappa recupera N=d kappa y sus doce bloques mediante divisiones euclídeas. Con error escalar menor que 1/(2d), el redondeo de d kappa recupera N. Éste es un umbral de precisión escalar; no se confunde con los radios de ruido vectorial de memoria.

## 4. Incidencia geométrica, carga y decodificación exacta

Escribimos Pi=I−11*/12 para distinguir el modo uniforme del proyector fijo ternario. La isometría del manuscrito es

\[
 Fv=(\mu(v),\mathcal I\Pi v/6),\qquad
 \mu(v)=\mathbf1^*v/12,
\]

con producto ||(mu,y)||_Y²=12mu²+||y||² en su imagen. El Gram I*I=36I+30·11* prueba F*F=I. Por tanto

\[
 Fv=FZ^*z,\qquad
 \|FZ^*e\|_Y\le\|e\|.
\]

La lectura raw I Pi v tiene error a lo sumo 6||e||. El registro firmado H12 v tiene error a lo sumo 2||e||. La recuperación de u=P3 Pi K y del proyector P10 se realiza con los mismos lectores y la misma carta, no con un proyector elegido después del ruido.

La incidencia combinatoria seleccionada por K_j≥729 no es continua en K4=729. Por ello conviene decodificar primero el registro entero. Desde una isometría completa, si ||e||<1/2, redondear cada coordenada de Z*z recupera K entero: cada error coordenado está acotado por ||Z*e||≤||e||. Restituye después, sin error, kappa, las firmas, u, P10 y el soporte {4,6,9,10}. Las marcas externas a K que utiliza la bandera excepcional deben conservarse por sus propios canales.

### Las dos memorias anteriores no adquieren carga por una isometría posterior

Conservamos Mv=(D3v,D4T3v), con ||L_M||=9/4 sobre 1-perp y ker M=R1. Sea E=W_a⊕W_a en el espacio de sus dos memorias. Como E es isométrico,

\[
 (EM)^*(EM)=M^*M,
 \quad\ker(EM)=\mathbb R\mathbf1.
\]

De z=EMv+e se obtiene Mv+E*e aplicando E*. Con carga q exacta,

\[
 \widehat v=(q/12)\mathbf1+L_ME^*z,
 \qquad\|\widehat v-v\|\le\tfrac94\|e\|.
\]

Si se usa carga aproximada, el error uniforme y el centrado son ortogonales y

\[
 \|\widehat v-v\|^2\le |\delta q|^2/12+(81/16)\|e\|^2.
\]

El transporte bilateral conserva también todas las distancias de la imagen entera. Por ello los radios probados para M permanecen exactamente

\[
 r_0=2\sqrt{146}/81\quad\text{sin carga},\qquad
 r_q=4\sqrt{73}/81\quad\text{con carga exacta}.
\]

Dentro de r0 se recupera Pi K, y con ello la dirección y su proyector. Dentro de rq, conservando q, se recupera K completo y la selección en el umbral. Lo mismo vale al aplicar después cualquier isometría completa de profundidad finita o infinita al espacio de memorias: se compone su adjunto antes de decodificar. El radio corresponde a la norma conjunta de los datos almacenados; al cambiar la normalización se transforma también el radio.

Esta igualdad no afirma que W mejore numéricamente el condicionamiento original de M. Demuestra que permite redistribuir o prolongar su información sin deteriorarlo y sin ocultar el canal uniforme que M no observa.

## 5. Norma del registro y normalización sin pérdida de orientación

El origen material de la norma no es una elección externa. La transformación conservada es K=H12 U_sgn/4, con H12*H12=4I. De ahí

\[
 \boxed{\|K\|^2=\tfrac14\|U_{\rm sgn}\|^2=4251257.}
\]

La norma cuadrada del registro firmado es 17005028. Las doce traslaciones son ortogonales como operadores y conservan la misma norma ν=√4251257, de modo que tr(O_K*O_K)=12ν²=51015084. La división K/ν normaliza cada columna orbital a norma uno y conserva su origen y orientación si se conserva el orden de esas columnas.

Esta normalización es uniforme a lo largo de la órbita de K y bajo sus transportes isométricos. No es una afirmación de que todos los registros generados tengan el mismo ν. Tampoco hace ortogonales las columnas: sus autovalores de Gram siguen siendo los anteriores divididos por 4251257, con valores diferentes.

Puede obtenerse una normalización operatoria isométrica usando el Gram completo, no sólo ν:

\[
 \mathcal P_K=O_K(O_K^*O_K)^{-1/2},\qquad
 \mathcal P_K^*\mathcal P_K=I.
\]

El inverso de raíz existe por la cota 589609>0. Así Z P_K es isométrico en cualquier profundidad. El factor unitario conserva el marco ortonormal orientado en las cartas fijadas, pero por sí solo descarta las amplitudes y el Gram del marco original. La recuperación íntegra utiliza el par

\[
 (\mathcal P_K,G_K),\qquad G_K=O_K^*O_K,
 \qquad O_K=\mathcal P_KG_K^{1/2}.
\]

Por ejemplo, multiplicar K por un escalar positivo conserva P_K y cambia G_K; K y −K tienen el mismo Gram, pero factores polares opuestos y distinta lectura lineal kappa. Ninguno de los dos factores sustituye por sí solo al par completo. La normalización polar es una herramienta general aplicada al marco producido, no una nueva constante física ni una derivación de K.

Una traslación del origen conserva ν, pero en la carta posicional fija

\[
 \kappa(SK)=1000\kappa(K)-K_1.
\]

Por tanto la norma orbital común no vuelve invariante la lectura escalar bajo cambios de origen. Para transportar la misma lectura se transporta también ell por la matriz inversa del cambio de carta. Un cambio unitario general puede abandonar las coordenadas enteras de bloques; el algoritmo de divisiones euclídeas utiliza la carta de bloques recuperada, no cualquier coordenada rotada.

## 6. Ejemplo operativo comprobado

En a=8, U=S4, los dos canales sin normalizar del registro son

\[
 Q_-K=(1213,3520,499,5774,4358,5798,4822,-137,7078,5809,1028,4079),
\]

\[
 Q_+K=(2765,5711,1881,6619,6845,8210,5735,1123,8460,7689,1454,6138).
\]

Su suma dividida por17 recupera cada bloque de K exactamente. El control también verificó la identidad matricial 9Q-*Q-+8Q+*Q+=1241I, antes de evaluar esos canales.

Para probar la cadena con ruido, se calcularon las dos memorias racionalizadas z=MK/√8. Se añadió 1/10 a su primera coordenada y cero a las restantes. Después se transportó cada bloque de doce coordenadas por los dos canales bilaterales, se recuperó z mediante su inversa por suma y se aplicó el decodificador de memorias con q=6263, sin entregar K al procedimiento inversor.

El ruido en la norma original de memoria es √8/10, menor que rq. El transporte isométrico normalizado conserva esa norma; los canales enteros sin normalizar se utilizan sólo para efectuar las operaciones exactas. El ensayo examina 924 candidatos con carga correcta y devuelve

\[
 K=(234,543,140,729,659,824,621,58,914,794,146,601),
\]

\[
 N=234543140729659824621058914794146601,\qquad
 d=999999999999999999999999999999999999,
 \qquad\kappa=N/d,
\]

y el soporte incidencial {4,6,9,10}, incluida la componente exactamente igual a729. El residuo racionalizado mínimo es 1/100. En este ejemplo el ruido se introdujo antes del transporte bilateral; la prueba de la sección4 cubre además perturbaciones arbitrarias posteriores de norma inferior al radio, mediante la contractividad del adjunto.

Se reutilizaron en modo de lectura las funciones de [verificar_exploracion.py](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/verificar_exploracion.py:112>), cargadas mediante `runpy.run_path(...,run_name='read_only_transduction')`. Se construyeron Q± y el lector racionalizado M/√8 con Fraction; la función principal de escritura no se ejecutó. No se modificó el verificador ni se crearon recibos.

La nueva capacidad concreta es transportar, repartir y recuperar un registro con lectores aritméticos y geométricos conocidos, preservando sus cotas y corrigiendo errores antes de la selección incidencial. Descansa en la generación previa de K, la invertibilidad no supuesta de O_K, la ley bilateral, la separación discreta de M y las pruebas de límite. No presenta la identidad abstracta f Z*Z=f como generación del continuo ni como prueba de que un registro finito contenga todas las historias.

## 7. Procedencia del aporte

La función de K como acoplamiento entre lectura numérica e incidencia es arquitectura autoral preexistente. H12, F, los lectores de kappa, M y sus inversas son resultados antecedentes. El balance bilateral general pertenece al desarrollo principal de esta ampliación. Esta nota aporta su composición explícita con el marco cíclico y los lectores, una tasa uniforme de transferencia, la distinción entre adjunto truncado e inversa finita y el ejemplo de recuperación bilateral con ruido. Se trata de ampliaciones del expediente; no se afirma prioridad histórica universal.
