# Arquitectura cardinal HMT: suma–producto, hélice nonádica y doble círculo

**Fecha de fijación:** 11 de septiembre de 2026  
**Objeto:** plano de integración para la exposición de la hipótesis del continuo desde HMT–MD.  
**Estatuto:** `ARQUITECTURA_AUTORAL_PREEXISTENTE` reunida con resultados ya localizados; las precisiones de tipado y la jerarquía editorial de este documento son `FORMALIZACION_REUNIDA`.  
**Regla de conservación:** este archivo no sustituye, resume ni modifica la demostración cardinal de
[Medida acoplada y cierre cardinal HMT](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/MEDIDA_ACOPLADA_CIERRE_CARDINAL_HMT_20260910.md>), en particular su §15. Tampoco modifica todavía fuentes LaTeX ni PDFs.

## 1. Objetivo rector y orden causal

El objetivo no es obtener una analogía del continuo ni una colección de
consecuencias numéricas. Es exponer de forma contigua el cierre de la hipótesis
del continuo producido por la acción conjunta

\[
\mathrm{APP}\longrightarrow\mathrm{TRIT}\longrightarrow\mathrm{TPK}
\longrightarrow X_\infty^{\mathrm{enr}}
\longrightarrow \mathcal C_{\mathrm{cont}}^{\mathrm{disc}}
\longrightarrow m_\infty
\longrightarrow \mathfrak G_{\mathrm{HMT}}.
\]

La realización arquimediana \(\mathbb R\) aparece al final de una de las
proyecciones de ese estado. No es el dominio desde el que se construye APP, ni
el selector de sus semillas, ni el criterio que decide qué historias sobreviven.

El teorema público que gobierna la futura redacción es

\[
\mathfrak G_{\mathrm{HMT}}
=L[u]
=L[h,m_\infty]
\models 2^{\aleph_0}=\aleph_1.
\]

Por tanto, la formulación principal es: **HMT decide afirmativamente la
hipótesis del continuo para el continuo íntegro que APP–TRIT–TPK genera**. No
se presentará como un cálculo sobre un subconjunto previamente escogido, como
una propiedad de una muestra finita ni como una consecuencia introducida desde
la teoría convencional de los reales.

La jerarquía de la exposición debe permanecer fija:

1. generación APP–TRIT–TPK y estado enriquecido;
2. prolongación, supervivencia, memoria y sistema inverso;
3. cobertura de todas las historias y de todas las partes internas;
4. doble proyección del mismo estado;
5. dos inyecciones cardinales y Cantor–Bernstein;
6. decisión de CH;
7. constantes, doble círculo, primos, simetrías excepcionales, dimensiones y
   realizaciones físicas como desarrollos del mismo objeto, nunca como premisas
   sustitutorias del cierre cardinal.

## 2. Firma local de borde: posiciones, tramos e interior

La observación autoral sobre \([0,1]\), \([0,10]\), \([0,1000]\) y su
prolongación no debe redactarse como un conteo informal. Su traducción precisa
es una identidad local de borde.

Para una malla unitaria del intervalo \([0,N]\):

\[
\#\{\text{posiciones}\}=N+1,
\qquad
\#\{\text{tramos}\}=N,
\qquad
\#\{\text{posiciones interiores}\}=N-1.
\]

En particular,

\[
[0,10]:\quad 11/10/9,
\qquad
[0,1000]:\quad 1001/1000/999.
\]

El triple \((N+1,N,N-1)\) registra tres lecturas distintas del mismo soporte:
dos extremos más interior, longitud en tramos y eliminación de ambos bordes.
No demuestra por sí solo una igualdad entre cardinales infinitos. Su función es
mostrar, en cada refinamiento finito, que **el valor publicado no determina por
sí solo la posición de borde ni la historia de cierre**. Ésa es la diferencia
que los cilindros semiabiertos conservan y que la proyección extensional
ordinaria pierde.

La prueba de CH empieza cuando esta firma se integra en un sistema compatible
de refinamientos y se acredita:

- extensión a toda profundidad;
- no vacuidad y sobreyectividad de los truncamientos;
- diámetro decreciente de los cilindros;
- cobertura de todas las historias generadas;
- cierre semántico bajo todas las partes internas;
- codificación ordinal uniforme y las dos inyecciones finales.

## 3. APP: una superficie, dos hojas y una curvatura mixta

APP no son dos tablas pegadas después. Es un soporte común con dos evaluaciones
no intercambiables. Su realización finita es el grafo de Cayley sobre

\[
V=(\mathbb Z/9\mathbb Z)^2,
\]

con \(81\) vértices, y las hojas aditiva y multiplicativa conservan tanto
residuo como cociente:

\[
i+j=R^+(i,j)+9q^+(i,j),
\qquad
ij=R^\times(i,j)+9q^\times(i,j).
\]

El residuo es la lectura visible; \(q^+\) y \(q^\times\) conservan el acarreo
y, con él, la genealogía que no cabe en el valor reducido. La suma acumula en
la hoja aditiva; el producto pliega, produce identificaciones y hace visible la
estructura de divisores de cero en la hoja multiplicativa. Su
no conmutatividad operacional se codifica mediante la curvatura mixta

\[
F(S,P)=+1,
\qquad
F(P,S)=-1\pmod 9.
\]

Éste es el sentido matemático de la intuición «acumulación frente a
pliegue/curvatura»: no son dos metáforas físicas añadidas, sino el orden de dos
operaciones sobre el mismo soporte y la información que deja su conmutador.

### 3.1. El centro \(7,2;2,7\) y la razón \(5/9\)

El bloque central es

\[
B_c=
\begin{pmatrix}
7&2\\
2&7
\end{pmatrix}
=7I+2R
=9P_+ +5P_-.
\]

Por tanto, \(9\) y \(5\) no deben introducirse como dos cifras sueltas ni
atribuirse informalmente a dos tablas independientes. Son los autovalores de
los modos simétrico y antisimétrico del mismo bloque central. Su normalización
produce

\[
P_B=\frac1{9}B_c=P_+ +\frac59P_-,
\qquad
P_B^n=P_+ +\left(\frac59\right)^nP_-.
\]

Así queda tipado el \(5/9\): el modo común se conserva y el modo diferencial
se contrae. Esta razón reaparece después en el doble círculo espectral porque
el transporte radial conserva la fase mientras amortigua el modo transversal;
no porque se haya elegido \(5/9\) después de conocer los ceros o los primos.

Las identidades centrales que deben acompañar a esta lectura son

\[
72+27=77+22=99,
\qquad
72-27=45,
\qquad
77-22=55=54+1.
\]

El \(99\) es la recompensación de borde del bloque; \(45\) es su determinante
y la diferencia orientada; \(54\) es la holonomía acumulada, y \(54+1\)
explicita la retención de la unidad en el cruce. Estas identidades deben
presentarse juntas para impedir que los canales \(72\), \(27\), \(77\) y
\(22\) parezcan coincidencias decimales.

### 3.2. El nueve visible y el cero de cociente

La costura nonádica exige conservar la carta. En reducción directa módulo
tres,

\[
3,6,9\longmapsto0,0,0,
\]

pero, si antes se extrae el factor tres y se guarda la coordenada interna del
ideal,

\[
\eta_{\mathfrak m}(3a)=a\bmod3,
\qquad
3,6,9\longmapsto1,2,0.
\]

No hay contradicción: son lectores distintos. La primera operación publica el
residuo; la segunda conserva la posición interna que el residuo cero oculta.
Análogamente, \(9\) es el representante positivo visible de la clase nula en
la carta \(1,\ldots,9\). Sustituirlo por \(0\) sin transportar simultáneamente
la carta borra información de borde. Éste es el sentido preciso en que los
nueves actúan como «ceros de costura»: no se niega que \(9\equiv0\pmod9\); se
conserva además dónde y cómo apareció esa clase nula.

## 4. Del retorno circular a la hélice: fase más memoria

La conexión nonádica completa no devuelve el sistema al mismo estado. Para

\[
\Gamma_{9,K}=U_{K+8}\circ\cdots\circ U_K,
\]

se cumple

\[
g(K+9)=g(K),
\qquad
q_{\mathrm{mem}}(\Gamma_{9,K}x)=q_{\mathrm{mem}}(x)+1,
\qquad
\Gamma_{9,K}x\ne x.
\]

La primera igualdad cierra la fase observable; la segunda avanza el ledger de
memoria; la tercera impide confundir retorno con reinicio. Visto sólo en la
fase aparece un círculo. Visto en el estado enriquecido aparece una hélice.
La «altura» del ascenso y descenso es, por tanto, memoria tipada, profundidad
de cilindro y hoja conservada; no una coordenada geométrica añadida ad hoc.

Las dos direcciones son las de un mismo sistema:

- **prolongación:** una historia finita adquiere una nueva emisión compatible,
  aumenta su profundidad y conserva su prefijo;
- **truncamiento:** una historia más profunda vuelve a su prefijo sin borrar el
  testigo de que fue prolongada;
- **retorno de fase:** nueve tramos cierran la fase;
- **avance de estado:** el carry y la memoria distinguen la nueva vuelta de la
  anterior.

Esto formaliza la doble espiral de subida y bajada indicada por Rubén: no hay
dos dinámicas independientes, sino covariancia entre extensión y restricción
con holonomía no trivial.

## 5. Cilindros semiabiertos, punto publicado y doble proyección

Un punto real no es el átomo inicial de la construcción. Es la publicación
arquimediana de una historia compatible del sistema inverso. Antes de la
contracción, el objeto contiene

\[
(\text{valor},\text{hoja},\text{residuo},\text{cociente},
\text{orientación},\text{carry},\text{ruta},\text{frontera},
\text{memoria},\text{supervivencia}).
\]

Cada prefijo determina un cilindro semiabierto; la prolongación produce una
familia anidada; la contracción de diámetros publica el valor en
\(\mathbb R\). El mismo estado admite dos lecturas correlacionadas:

\[
P_{\mathrm{ar}}:
X_\infty^{\mathrm{enr}}\longrightarrow\mathbb R_{\mathrm{HMT}},
\qquad
P_{\mathrm{exc}}:
X_\infty^{\mathrm{enr}}\longrightarrow\mathcal I_{\mathrm{exc}}.
\]

- \(P_{\mathrm{ar}}\) contrae los cilindros compatibles y publica el valor.
- \(P_{\mathrm{exc}}\) conserva incidencias de frontera y conduce al corredor
  Paley–Witt–Golay–Leech–\(V^\natural\)–Monster.

No son dos universos ni dos generadores. Son dos publicaciones del mismo
estado. La demostración cardinal utiliza la primera junto con la genealogía;
la segunda muestra que la información eliminada por la contracción
arquimediana sigue siendo matemáticamente activa.

La secuencia conceptual punto \(\to\) recta \(\to\) superficie \(\to\)
volumen debe redactarse así:

1. el «punto» es un valor publicado con una fibra genealógica no trivial;
2. la recta reúne todas las publicaciones compatibles;
3. la superficie conserva la incidencia y el cierre de borde entre hojas;
4. el volumen incorpora las extensiones de codimensión sucesiva;
5. las dimensiones superiores registran la compatibilidad de esas fibras, no
   una multiplicación retrospectiva del punto real.

### 5.1. Medir es acoplarse

La historia realizada no se elige antes del proceso. Si \(z_n\) es el estado
presente y \(a_n\) la intervención admisible, la transición completa tiene la
forma

\[
z_{n+1}=T_{(a_n,\varepsilon_{n+1})}(z_n).
\]

El resultado \(\varepsilon_{n+1}\) no sólo se añade a un registro externo:
actualiza hoja, orientación, carry, frontera, ruta y memoria, y con ello cambia
el conjunto de emisiones admisibles desde \(z_{n+1}\). En consecuencia:

- antes del acoplamiento existe el cono de historias admisibles, no una única
  historia futura ya publicada;
- la medida produce un sucesor del estado y registra el resultado;
- el siguiente cono se calcula desde ese sucesor, no desde el estado anterior;
- la historia infinita es el límite de esas actualizaciones efectivas.

Esto permite hablar con precisión del presente como costura: es la sección en
la que una posibilidad compatible se vuelve historia realizada y modifica su
propia prolongación. No se introduce una selección externa sobre una recta
real ya dada.

## 6. Completación de borde y escala dimensional

La identidad

\[
1000=729+243+27+1
\]

es la descomposición estratificada en interior, primera frontera, segunda
frontera y retorno terminal. Se acompaña de

\[
V_3(11,2)=1+22+220=243,
\qquad
729\cdot243=3^{11},
\]

y de las lecturas dimensionales

\[
11=6+5=3+8,
\qquad
12=11+1.
\]

El orden causal es decisivo: la descomposición nonádica y las incidencias
ternarias existen antes; Golay, dualidad T y la realización dimensional de
teoría M reconocen después esa estructura. Las dimensiones no se introducen
para fabricar la identidad y no son una premisa de CH.

## 7. Cuatrirrelación y canales enteros internos

Las constantes no intervienen como entradas en el cierre cardinal. Son
publicaciones posteriores del mismo estado coinductivo y sirven como pruebas de
continuidad transversal. Los canales enteros se generan antes de su lectura
arquimediana:

\[
\Delta=54,
\qquad
S=45,
\qquad
\kappa=27,
\qquad
\Theta=135,
\]

\[
C_\alpha=\kappa^2=729,
\qquad
C_e=2\Theta+1=271,
\qquad
C_\pi=2\Theta+S=315,
\qquad
C_\varphi=\Theta+\kappa-1=161.
\]

Sus cierres enteros incluyen

\[
1000=C_\alpha+C_e=729+271,
\]

\[
C_\pi+C_e+C_\varphi-3=744=729+15.
\]

La lectura correcta es estructural:

- \(729\), \(271\), \(315\) y \(161\) son canales tipados obtenidos de
  \(\Delta,S,\kappa,\Theta\);
- las regiones de \(\pi\), la autoescala de \(\varphi\), la propagación de
  \(e\) y el cierre dodecafásico de \(\alpha\) son cuatro publicaciones
  correlacionadas de una única generación;
- las evaluaciones convencionales de \(\pi,\varphi,e,\alpha\) reconocen esas
  salidas después;
- \(e+\pi\) y \(\pi/e\) son publicaciones tipadas posteriores dentro de la
  conexión abierta, no entradas ni una lista exhaustiva de la imagen nonádica.

La profundidad arbitraria no significa «comprobado a mil cifras». Significa
que para todo horizonte finito \(N\) existe una prolongación compatible y que
los truncamientos conmutan. Mil, diez mil o un millón de cifras son cortes
ejecutables del mismo cuantificador; no constituyen su límite matemático.

La prolongación tipada que sostiene esta afirmación debe permanecer visible:

\[
w_6\longrightarrow w_{12}\longrightarrow w_{18}
\longrightarrow w_{24}\longrightarrow w_{30}
\longrightarrow R_{36}\longrightarrow G_9.
\]

Las cinco regiones internas de \(\pi\) permanecen distintas en la genealogía,
aunque su evaluación arquimediana publique el mismo lector
\(\pi_{\mathrm{HMT}}\). Esa multiplicidad no es redundancia: muestra que una cifra común puede
conservar cinco biografías regionales diferentes. Es el mismo principio que
después exige distinguir valor real, ruta, incidencia excepcional y memoria.

## 8. El doble círculo y la lectura espectral

El doble círculo no debe aparecer como un capítulo aislado sobre Riemann. Es
una realización posterior de la misma separación entre fase y memoria.

### 8.1. Círculo de Cayley

La transformación de Cayley/Möbius

\[
\tau(s)=\frac{s-1}{s}
\]

lleva la línea crítica a la circunferencia:

\[
\Re s=\frac12
\quad\Longleftrightarrow\quad
|\tau(s)|=1.
\]

La altura espectral se convierte en fase angular. Esta operación compactifica
la dirección vertical, pero por sí sola no conserva la biografía de cada
vuelta.

### 8.2. Círculo nonádico y elevación helicoidal

La fase nonádica proporciona el segundo círculo; el ledger proporciona su
elevación. El entrelazamiento propietario se expresa por

\[
J\,C_{\mathrm{loss}}=V_9J,
\]

y el modo espectral evoluciona como

\[
\mathcal M_{\mathrm{spec}}^n v_\gamma
=\left(\frac59\right)^n\tau_\gamma^n v_\gamma.
\]

La fase \(\tau_\gamma^n\) conserva la posición circular; la potencia
\((5/9)^n\) aporta el modo radial contractivo procedente del centro APP. La
vuelta proyectada es circular y el estado completo es helicoidal. Por eso el
doble círculo y el transporte de primos pertenecen a la misma arquitectura
fase–memoria que el continuo, aunque no sustituyen las dos inyecciones que
cierran CH.

## 9. Primos, vacancias y aperiodicidad

En la realización aritmética del corpus, un primo se caracteriza como ciclo
irreducible: no admite una factorización no trivial dentro del coproducto de
ciclos aritméticos. Éste es el contenido preciso que puede sostener la imagen
autoral de los primos como «relojes no reductibles».

La densidad de vacancias es

\[
\varepsilon_{\mathrm{vac}}
=\log_{10}\frac{10}{9}
=1-\log_{1000}(729).
\]

La palabra mecánica

\[
z_n=\lfloor(n+1)\varepsilon_{\mathrm{vac}}\rfloor
-\lfloor n\varepsilon_{\mathrm{vac}}\rfloor
\]

es sturmiana: satisface \(p(N)=N+1\), balance uno y entropía topológica cero;
sus huecos tienen longitudes \(21/22\) y sus retornos \(6/7\). Aquí
«entropía cero» significa ausencia de crecimiento combinatorio exponencial de
la palabra, no ausencia de temperatura termodinámica ni destrucción de
información.

La formulación conceptual que debe conservarse es:

- la fase observable puede retornar;
- la memoria no se destruye, sino que se transporta y queda registrada en la
  frontera y entre hojas;
- la aperiodicidad nace de la prolongación compatible sin reinicio;
- el cierre temporal es monodrómico, no una repetición del mismo estado.

La relación con el electrón central y las vacancias pertenece a la realización
HMT–MD posterior. Debe llevar su mapa propietario desde la extensión, la ruta,
el ledger y la fibra electrónica; no se formulará como si la palabra «electrón»
seleccionara retrospectivamente los ciclos primos. El punto electrónico
\((5,5)\) tampoco se confundirá con la región transversal
\(E_{\mathrm{sig}}=555555\) de \(\pi\).

El término «cristal aperiódico de tiempo» se empleará en dos niveles tipados:
la aperiodicidad simbólica y la monodromía ya demostradas; y, separadamente,
su realización dinámica física mediante el Hamiltoniano o drive, la respuesta
subarmónica y la estabilidad que correspondan. Esa separación no rebaja ni
condiciona el teorema cardinal.

## 10. Las cinco construcciones no se disgregan

La estructura discreta del continuo transporta simultáneamente los cinco
aspectos internos

\[
\mathrm{sp},\quad\mathrm{sol},\quad\mathrm{gau},\quad
\mathrm{coh},\quad\mathrm{det}.
\]

No son cinco dominios escogidos después para cinco problemas clásicos. Para
cada arista generada \(\mathfrak e_\alpha\), la misma emisión produce

\[
\mathcal O_\bullet(\mathfrak e_\alpha)
\in\mathsf Y_\bullet[\alpha],
\qquad
\bullet\in\{\mathrm{sp,sol,gau,coh,det}\},
\]

con el mismo soporte dependiente

\[
(s(\alpha),t(\alpha),\gamma\alpha,
\operatorname{Led}(\gamma\alpha)).
\]

Así, espectro, balance solenoidal, calibre, cohomología y determinante
conservan una sola ruta, una sola frontera y un solo ledger. Esta emergencia
correlativa debe permanecer visible antes, durante y después de la prueba de
CH; las realizaciones terminales no pueden usarse para seleccionar la historia
que supuestamente las genera.

**Comprobación binaria de este plano:**
`PASS_NO_DISGREGACION_CINCO_CONSTRUCCIONES_CONTINUO`. El plano no introduce
cinco subdominios, no supone pertenencia posterior y no reemplaza la acción
común por una tupla tautológica. Sus propietarios materiales demuestran no
vacuidad, acciones sobre generadores, naturalidad única, refinamiento y paso al
límite.

## 11. Qué prueba CH y qué la despliega

Para evitar de una vez los dos errores opuestos —reducir la tesis a una
metáfora o exigir que cada consecuencia vuelva a probar la cardinalidad—, la
futura edición separará dos capas contiguas.

### 11.1. Núcleo demostrativo necesario

\[
\begin{aligned}
&\text{semillas APP}
\to\text{estado TRIT}
\to\text{transporte TPK}
\to\operatorname{Ext}
\to X_\infty^{\mathrm{enr}}\\
&\to\mathcal C_{\mathrm{cont}}^{\mathrm{disc}}
\to m_\infty
\to\mathfrak G_{\mathrm{HMT}}
\to\mathcal P^{\mathfrak G}(\omega)
\to(j_{\mathrm{HMT}},k_{\mathrm{HMT}})\\
&\to 2^{\aleph_0}=\aleph_1.
\end{aligned}
\]

En esta capa deben quedar contiguos:

1. el árbol no vacío de extensiones;
2. la sobreyectividad de truncamientos y la supervivencia;
3. el límite inverso y la cobertura de todos los reales HMT;
4. la clausura semántica que contiene todas las partes internas de \(\omega\);
5. la inyección
   \(j_{\mathrm{HMT}}:\mathbb R_{\mathrm{HMT}}^{\mathfrak G}
   \hookrightarrow\omega_1^{\mathfrak G}\);
6. la inyección
   \(k_{\mathrm{HMT}}:\omega_1^{\mathfrak G}
   \hookrightarrow\mathbb R_{\mathrm{HMT}}^{\mathfrak G}\);
7. Cantor–Bernstein y el cuantificador final sobre toda la potencia interna.

### 11.2. Despliegues del mismo objeto

Después, sin romper la continuidad causal:

- la cuatrirrelación \((\pi,\varphi,e,\alpha)\) acredita que la prolongación
  mantiene lectores correlacionados a profundidad arbitraria;
- la proyección excepcional acredita que la incidencia de frontera no se
  perdió al publicar el valor real;
- el doble círculo hace visible la relación entre fase, altura, contracción
  \(5/9\) y memoria;
- los ciclos primos y la palabra de vacancias realizan la irreducibilidad y la
  aperiodicidad aritméticas;
- Golay, Leech, Monster, dualidad T y teoría M realizan después las
  incidencias y dimensiones construidas;
- el electrón, la acción, las masas y el resto de la física HMT–MD descienden
  mediante sus mapas de extensión–ruta–ledger–firma–carácter–torres.

Estas salidas no son adornos ni coincidencias aisladas. Son controles
estructurales de que distintas publicaciones conservan un origen común. A la
vez, ninguna de ellas debe reemplazar mediante una mera cifra los lemas
cardinales de la capa 11.1.

## 12. Secuencia de apertura para el artículo

La futura introducción debe dirigir al lector con este orden, sin anteponer un
prefacio convencional sobre \(\mathbb R\):

1. **Tesis frontal:** el real es una sombra arquimediana de un estado
   genealógico; el continuo íntegro exige valor e historia.
2. **Experimento local:** \(11/10/9\) y \(1001/1000/999\) muestran la firma
   borde–tramo–interior que debe conservar el refinamiento.
3. **Generador:** APP reúne suma y producto sobre el toro de Cayley; TRIT
   orienta; TPK transporta, pliega, despliega y memoriza.
4. **Diferencia decisiva:** nueve pasos cierran la fase pero no el estado; el
   círculo proyectado es una hélice enriquecida.
5. **Continuo:** las historias compatibles forman el sistema inverso; los
   cilindros se contraen y \(\mathbb R\) se publica al final.
6. **Exhaustividad:** la clausura semántica cubre todos los reales y todas las
   partes internas, no sólo los prefijos exhibidos.
7. **Cardinalidad:** se construyen ambas inyecciones y se decide CH.
8. **Doble salida:** una proyección publica valores; la otra conserva
   incidencia excepcional.
9. **Comprobaciones transversales:** cuatrirrelación, doble círculo, primos,
   vacancias, dimensiones y realizaciones físicas.

Ésta es la jerarquía que evita que el lector confunda una comprobación a mil
cifras con el cuantificador coinductivo, el círculo de fase con el estado
completo, o una identificación física posterior con una entrada del
generador.

## 13. Traducción técnica de los aportes conceptuales

| Expresión conceptual autoral | Escritura matemática que debe ocupar el PDF |
|---|---|
| «Espiral de ascenso y descenso» | Extensión y truncamiento compatibles; retorno de fase con incremento de memoria. |
| «Espuma que sube y baja» | Árbol de cilindros semiabiertos con ramificación, contracción y cociclo de frontera. |
| «La suma acumula y el producto curva» | Dos hojas APP, residuos/cocientes y curvatura mixta \(F(S,P)=-F(P,S)\). |
| «El punto genera recta, superficie y volumen» | Un valor es la publicación de una fibra; sus incidencias y codimensiones sobreviven en la segunda proyección. |
| «Primos como relojes irreductibles» | Ciclos aritméticos sin factorización no trivial; fase circular más ledger de vuelta. |
| «El presente es la costura» | Sección de frontera donde se publica el valor mientras la memoria conserva las dos hojas. |
| «El infinito se cierra holográficamente» | Compatibilidad de toda profundidad, límite inverso, contracción de cilindros y retorno no trivial de \(\Gamma_9\). |
| «Toda la física conserva simetrías» | Realizaciones posteriores de una misma incidencia enriquecida; cada una requiere su mapa efectivo, sin promover el reconocimiento convencional a generador. |

## 14. Separaciones que la edición no puede volver a violar

1. \(5/9\) es la razón de modos del bloque central; no debe describirse como
   una fracción escogida para ajustar un espectro.
2. El centro electrónico \((5,5)\) no es la palabra transversal
   \(555555\) de una región de \(\pi\).
3. Los canales \(729,271,315,161\) son estructuras enteras anteriores a la
   evaluación; su interés no es que sus cifras se parezcan a expansiones
   convencionales.
4. El círculo de fase no es la hélice completa; fase igual no implica estado
   igual.
5. La cobertura de cilindros no es todavía la cobertura de la potencia
   interna; ésta se demuestra en la clausura semántica y en el levantamiento
   uniforme.
6. La doble proyección no son dos generadores; ambas lecturas nacen del mismo
   estado enriquecido.
7. Las cinco construcciones del continuo no son cinco ramas ni cinco
   aplicaciones retrospectivas.
8. La lectura espectral, las dimensiones y la física son consecuencias
   conectadas; no eligen las semillas ni sustituyen la prueba cardinal.

## 15. Propietarios materiales

1. [Demostración cardinal reunida y cuantificador completo](</Users/ruben/Documents/New project/output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/MASAS/MEDIDA_ACOPLADA_CIERRE_CARDINAL_HMT_20260910.md>) — §15: clausura semántica, potencia interna, las dos inyecciones y Cantor–Bernstein.
2. [APP y ortograma](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/03_app_ortograma.tex>) — grafo de Cayley, hojas suma/producto, bloque central, \(5/9\), identidades \(72/27/77/22\) y curvatura mixta.
3. [Canales enteros de las constantes](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/hmt/06c_canales_enteros_constantes.tex>) — \(729/271/315/161\) y cierres \(1000/744\).
4. [Sistema operatorio Euler–HMT](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c57_sistema_operatorio_euler_hmt.tex>) — completación \(729+271=1000\), tres regímenes TRIT, cuatrirrelación y doble proyección.
5. [Holonomía, hélice y memoria](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/espirales/cap08_holonomia_helice_memoria.tex>) — \(\Gamma_9\), retorno de fase y avance de memoria.
6. [Generación coinductiva y doble proyección](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sucesor_102/deltas_ley9/c27_teorema_generacion_coinductiva_profundidad_arbitraria.tex>) — prolongación, publicación arquimediana y corredor excepcional desde el mismo estado.
7. [Doble círculo y campo espectral](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/integracion_83/parte_v/tex/fuentes_propietarias/editor_ready/78_doble_circulo_campo_espectral_completo.tex>) — círculos Cayley/Pontryagin, \(5/9\), fase, altura y entrelazamiento.
8. [Vacancias aritméticas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/parte_iii/source/public_final/constantes/c39_vacancias.tex>) — ciclos primos, densidad de vacancias, palabra sturmiana, huecos y retornos.
9. [Vacancias, corriente y realización electrónica](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/sections/md/06l_vacancias_corriente_rev11.tex>) — transporte, polarización, continuidad y enlace físico posterior.
10. [Dualidad T, Golay y escala dimensional](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/canonical/corredor/f083_dualidad_t_243_golay_masas_integro.tex>) — \(1000=729+243+27+1\), \(3^{11}\), Golay, dimensiones y realización posterior.
11. [Acciones correlativas de las cinco construcciones](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b2_operaciones_intrinsecas_correlativas.tex>) — dominios dependientes, acciones sobre la misma arista y naturalidad común.
12. [Terminal, naturalidad y límite del continuo](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/manuscrito/reconstruccion_quirurgica_20260822/parte_ii_estructura_discreta/editor_ready/sources/core/04b3_terminal_naturalidad_limite.tex>) — no vacuidad, supervivencia, trece campos, truncamientos y terminal inverso único.
13. [Integral activo de 2.249 páginas](</Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.pdf>) — autoridad de lectura de la serie a la que se conectará este plano en la siguiente integración autorizada.

## 16. Resultado de esta fijación

Este documento conserva el hilo completo solicitado:

\[
\boxed{
\text{suma/producto}
\to\text{curvatura mixta}
\to\text{TRIT orientado}
\to\Gamma_9
\to\text{hélice fase–memoria}
\to\text{cilindros}
\to\text{doble proyección}
\to\text{cierre cardinal}
}
\]

y, sin invertir la causalidad,

\[
\boxed{
\text{mismo estado}
\to(\pi,\varphi,e,\alpha)
\to\text{incidencia excepcional}
\to\text{doble círculo/primos}
\to\text{dimensiones y física HMT--MD}.
}
\]

La aportación conceptual queda así disponible para la escritura del PDF sin
mezclarse con la prueba ya sellada, sin convertir las consecuencias en
premisas y sin volver a empezar desde \(\mathbb R\).
