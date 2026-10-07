# Levantamiento unitario del refinamiento y transporte de lectores

14 de septiembre de 2026. Nota aditiva de la tercera ampliación. No modifica REFINAMIENTO_CONSERVATIVO.md, los documentos sellados anteriores ni el paper. Construye un enlace explícito entre la biyección aritmética por residuos y la ley bilateral isométrica, conservando sus dominios distintos.

## 1. Procedencia y distinción de realizaciones

El transporte L_c(x,y)=(Bx−c,By+c), su dominio positivo y su inversa están demostrados en [REFINAMIENTO_CONSERVATIVO.md](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_03_REFINAMIENTO_UNIDAD_Y_TRANSDUCCION_20260914/REFINAMIENTO_CONSERVATIVO.md:121>), §§3–5, especialmente el teorema 3 por residuos y las fórmulas del registro finito. Sus §§6–7 prueban el límite y los cilindros, sin identificar el número límite con toda la historia.

La ley bilateral para dos transportes isométricos con dominio y codominio comunes está demostrada en [LEY_BILATERAL_UNIDAD_Y_TRANSDUCCION.md](</Users/ruben/Documents/New project/output/EXPLORACION_FUNCION_ESTRUCTURAL_REGISTRO_20260914/AMPLIACION_03_REFINAMIENTO_UNIDAD_Y_TRANSDUCCION_20260914/LEY_BILATERAL_UNIDAD_Y_TRANSDUCCION.md:63>), §3. El principio de transportar operadores en la imagen, sin identificarla con todo un ambiente mayor, está conservado en [nuclear/05.tex](</Users/ruben/Documents/New project/output/PAPER_FUNDACIONAL_CONSERVACION_MEMORIA_HMT_MD_20260912/source/nuclear/05.tex:26>), líneas 26–58.

La novedad focal es componer esas flechas: una etiqueta admisible y su acarreo se convierten, por una biyección exacta, en una etiqueta refinada; su linealización sobre bases ortonormales da un transporte unitario al que puede aplicarse la ley bilateral. Se clasifica como **FORMALIZACION_NUEVA de esta composición**. La aritmética posicional y la linealización de biyecciones son métodos matemáticos conocidos, sin reclamación de prioridad universal.

La base de las parejas sigue siendo una publicación posterior dentro de la cadena APP–TRIT–TPK ya declarada. El espacio de etiquetas que se define abajo es un dominio aritmético explícito: no se declara automáticamente igual a un dominio filtrado de historias TPK ni al espacio de doce coordenadas de K.

La conservación original de L_c es la suma después de reescalar. La unitariedad nueva conservará una suma de cuadrados de **amplitudes sobre etiquetas**, no la cantidad x²+y² de una pareja numérica. Esa distinción es esencial para el enlace.

## 2. La biyección exacta de etiquetas

Sean B≥2 y M≥1 enteros. Definimos los conjuntos finitos

\[
\mathcal D_{B,M}=
\{(x,y,c)\in\mathbb Z_{\ge0}^2\times\{0,\ldots,B-1\}:
x+y=M,\ c\le Bx\},
\]

\[
\mathcal E_{BM}=
\{(X,Y)\in\mathbb Z_{\ge0}^2:X+Y=BM\}.
\tag{1}
\]

La condición c≤Bx conserva la no negatividad de la primera coordenada. Cuando x=0 sólo permite c=0; para x≥1 permite los B acarreos.

**Teorema 1.** La aplicación

\[
\ell:\mathcal D_{B,M}\to\mathcal E_{BM},\qquad
\ell(x,y,c)=(Bx-c,By+c)
\tag{2}
\]

es biyectiva. Ambos conjuntos tienen cardinal BM+1. Su inversa es

\[
\boxed{c=Y\bmod B,\qquad
y=\frac{Y-c}{B},\qquad x=\frac{X+c}{B}.}
\tag{3}
\]

**Prueba.** La imagen pertenece a E por la condición de dominio y por la suma X+Y=BM. Dado (X,Y), el residuo c es el único elemento del alfabeto con Y≡c módulo B. Como X+Y es divisible por B, X+c también lo es. Las dos preimágenes son no negativas y suman M. Si c>0, x no puede ser cero. La sustitución comprueba la imagen y la unicidad. Hay M+1 etiquetas con c=0 y M etiquetas para cada c>0, en total (M+1)+(B−1)M=BM+1. ∎

## 3. Unitariedad sobre las bases de etiquetas

Tomamos los espacios de Hilbert con medida de conteo

\[
\mathscr H_D=\ell^2(\mathcal D_{B,M}),\qquad
\mathscr H_E=\ell^2(\mathcal E_{BM}),
\]

reales o complejos, y sus bases ortonormales etiquetadas. La aplicación lineal

\[
\boxed{J|x,y,c\rangle=|Bx-c,By+c\rangle}
\tag{4}
\]

es unitaria: J*J=I_D y JJ*=I_E.

**Prueba.** El teorema 1 asegura que J permuta biyectivamente dos bases ortonormales completas. Su adjunto actúa sobre las etiquetas mediante (3). Para ψ=Σ_d ψ_d|d⟩,

\[
\|J\psi\|^2=\sum_{e\in\mathcal E}|\psi_{\ell^{-1}(e)}|^2
=\sum_{d\in\mathcal D}|\psi_d|^2=\|\psi\|^2.
\]

La sobreyectividad da ambas identidades unitarias. ∎

Esta construcción puede representar un procesamiento reversible de etiquetas o de amplitudes. No supone un dispositivo físico que lo realice ni convierte x,y,c en amplitudes. Por ejemplo, la etiqueta |73,27,1⟩ tiene norma 1, no norma √(73²+27²+1).

## 4. Lectores diagonales y recuperación del acarreo

Para una función real h sobre un conjunto finito, escribimos M_h para el operador diagonal que multiplica cada vector de base por h en esa etiqueta. La biyección cumple

\[
\boxed{J^*M_hJ=M_{h\circ\ell}.}
\tag{5}
\]

Se prueba actuando sobre cada etiqueta de la base.

En la salida definimos

\[
f_E(X,Y)=\frac{X}{BM},\quad
g_E(X,Y)=\frac{Y}{BM},\quad
\gamma_E(X,Y)=Y\bmod B.
\]

En la entrada usamos f_D=x/M, g_D=y/M y γ_D=c. Entonces

\[
\boxed{
J^*M_{f_E}J=M_{\,x/M-c/(BM)},\qquad
J^*M_{g_E}J=M_{\,y/M+c/(BM)},\qquad
J^*M_{\gamma_E}J=M_c.}
\tag{6}
\]

Así se transporta exactamente la transferencia de unidad. Puesto que f_E+g_E=1, la suma de los dos lectores es la identidad. La última igualdad conserva el acarreo como un observable entero recuperable. No se confunde este dato con una fracción normalizada o con una etiqueta de trayectoria que no se haya especificado.

## 5. Profundidad arbitraria: dominio completo de rutas

Sea Pₙ(B,M) el conjunto de rutas de longitud n que parten de **todas** las parejas no negativas de suma M y siguen, en cada etapa, las condiciones de D para su suma correspondiente. La ruta contiene su pareja inicial y sus n acarreos admisibles.

Para π∈Pₙ, sea Φₙ(π) su pareja final. Por inducción inversa con (3),

\[
\boxed{\Phi_n:\mathcal P_n(B,M)\longrightarrow
\mathcal E_{B^nM}\text{ es una biyección},\qquad
|\mathcal P_n(B,M)|=B^nM+1.}
\tag{7}
\]

**Prueba.** Desde cualquier pareja de suma BⁿM, el residuo recupera el último acarreo y una única pareja anterior de suma Bⁿ⁻¹M. Repetir n veces produce una única ruta que parte de una pareja de suma M. La composición directa devuelve el extremo original. ∎

La cuenta también es transparente desde las entradas. Hay M parejas con x₀≥1; cada una admite Bⁿ palabras canónicas. La pareja de frontera x₀=0,y₀=M admite únicamente la palabra de todos ceros. El total es MBⁿ+1.

La linealización

\[
J_n:\ell^2(\mathcal P_n(B,M))
\longrightarrow\ell^2(\mathcal E_{B^nM}),\qquad
J_n|\pi\rangle=|\Phi_n(\pi)\rangle
\tag{8}
\]

es, por tanto, unitaria. Con la profundidad conservada se recuperan la entrada y todos los acarreos. En particular, sobre la pareja final,

\[
c_j=\left\lfloor\frac{Y}{B^{n-j}}\right\rfloor\bmod B,
\quad y_0=\left\lfloor\frac{Y}{B^n}\right\rfloor,
\quad x_0=M-y_0.
\tag{9}
\]

Estas funciones definen lectores diagonales de la memoria completa.

Las aplicaciones son compatibles con prolongación: Φₙ₊₁(π,c)=L_c(Φₙ(π)). Esto no afirma que Jₙ y Jₙ₊₁ sean una misma unitaria entre espacios de igual dimensión. La dimensión crece; para el paso siguiente se incorpora la nueva etiqueta de acarreo admisible. El dominio no es sin más el producto de todas las etiquetas anteriores por B dígitos, porque la etiqueta de frontera sólo admite c=0.

### Entrada inicial fijada

Si se fija una pareja (x₀,y₀) con x₀≥1, hay Bⁿ rutas y su imagen es exactamente

\[
\{(B^nx_0-C,B^ny_0+C):0\le C\le B^n-1\}.
\tag{10}
\]

La linealización es unitaria hacia el subespacio generado por esa imagen, no hacia todo ℓ²(E_{BⁿM}). En x₀=0 la imagen consta de una sola etiqueta. Los cilindros y sus fronteras de la nota antecedente corresponden a esta imagen de una entrada fijada; no autorizan sustituirla por el dominio completo de (7).

## 6. Composición bilateral con una permutación de entradas

Sea R una permutación de D_{B,M}, linealizada unitariamente sobre H_D. Definimos dos transportes con exactamente los mismos tipos,

\[
\mathcal B=J,\qquad \mathcal C=JR:
\mathscr H_D\to\mathscr H_E.
\tag{11}
\]

Se mantiene B para la base aritmética y se usa la letra caligráfica B para el transporte. No se selecciona R a partir de un resultado buscado; cualquier permutación previamente declarada de las etiquetas admisibles produce esta composición.

Para a>0, p=a²+a+1 y N=(2a+1)p, sean

\[
Q_-=a\mathcal B-\mathcal C=J(aI-R),\qquad
Q_+=(a+1)\mathcal B+\mathcal C=J((a+1)I+R).
\tag{12}
\]

Por el balance bilateral,

\[
\boxed{(a+1)Q_-^*Q_-+aQ_+^*Q_+=NI_D,}
\]

\[
\boxed{W_a\psi=
\frac1{\sqrt N}\bigl(\sqrt{a+1}\,Q_-\psi,
\sqrt a\,Q_+\psi\bigr),\qquad W_a^*W_a=I_D.}
\tag{13}
\]

**Prueba directa.** Como B y C son unitarios, los Grams de Q₋ y Q₊ tienen términos cruzados −a(B*C+C*B) y +(a+1)(B*C+C*B). Al ponderar por a+1 y a se cancelan. Los términos diagonales suman N. No se exige R³=I ni conmutación de transportes entre espacios diferentes. ∎

Para canales sin normalizar u=Q₋ψ,v=Q₊ψ,

\[
\boxed{J\psi=\frac{u+v}{2a+1},\qquad
\psi=J^*\frac{u+v}{2a+1}.}
\tag{14}
\]

El estado se recupera también mediante Wₐ* desde los canales normalizados, con norma del inversor igual a 1. La unitaria J se deshace mediante los residuos del teorema 1. Se han compuesto, por tanto, el refinamiento aritmético reversible y la conservación bilateral sin identificar sus dos normas originales.

Una condición explícita de compatibilidad de la pareja sin normalizar es

\[
\boxed{[(a+1)I_E+JRJ^*]u
=[aI_E-JRJ^*]v.}
\tag{15}
\]

En efecto, equivale a JRJ*(u+v)=av−(a+1)u. Si se cumple, definir ψ mediante (14) da Q₋ψ=u y Q₊ψ=v; la necesidad resulta de sustituir los canales verdaderos. Es una condición en H_E, con sus tipos compuestos explícitamente.

## 7. Ley adicional para los lectores, no sólo para la norma

Sea F cualquier operador autoadjunto sobre H_E y F_J=J*FJ. Entonces

\[
\boxed{W_a^*\operatorname{diag}(F,F)W_a
=\frac{a(a+1)F_J+R^*F_JR}{p}.}
\tag{16}
\]

**Prueba.** Expandir (a+1)Q₋*FQ₋+aQ₊*FQ₊ cancela los términos cruzados B*FC+C*FB. El coeficiente de B*FB es a(a+1)(2a+1), y el de C*FC es 2a+1. Dividir por N y usar C=JR produce (16). ∎

En a=8 son los pesos exactos 72/73 y 1/73. Para F=I se recupera la isometría. Para un lector no constante, (16) permite calcular qué cambia al leer los mismos observables diagonales en ambos canales. Si R conmuta con F_J, se conserva ese lector. Si no, la norma total sigue conservada pero su lectura diagonal puede variar de manera exactamente determinada.

El operador que conserva el lector original A sobre la imagen completa es WₐAWₐ*, con identidad de imagen WₐWₐ*. No se lo sustituye automáticamente por diag(F,F). Este último corresponde a otra elección de observable y su relación correcta es (16).

## 8. Ejemplo exacto: base diez y suma cien

Para B=10,M=100, los espacios D y E tienen dimensión 1001. La etiqueta

\[
d_1=(73,27,1)
\]

se transforma exactamente en e₁=(729,271). En ella, los lectores de (6) dan

\[
f_E(e_1)=\frac{729}{1000}
=\frac{73}{100}-\frac1{1000},\quad
g_E(e_1)=\frac{271}{1000},\quad
\gamma_E(e_1)=1.
\tag{17}
\]

Para exhibir una composición bilateral no trivial, declaramos R como la transposición de las dos etiquetas admisibles d₁=(73,27,1) y d₂=(73,27,2), dejando fijas todas las demás. Esta regla no consulta α ni ajusta una amplitud. La segunda salida es e₂=(728,272).

En a=8, para ψ=|d₁⟩,

\[
Q_-\psi=8|e_1\rangle-|e_2\rangle,\qquad
Q_+\psi=9|e_1\rangle+|e_2\rangle.
\tag{18}
\]

Sus normas cuadradas son 65 y 82, y

\[
9\cdot65+8\cdot82=585+656=1241=17\cdot73.
\]

La suma de los dos canales es 17|e₁⟩, por lo que (14) y el residuo recuperan exactamente |d₁⟩, incluido su acarreo 1.

Si se lee F=M_{f_E} diagonalmente en ambos canales normalizados, (16) da

\[
\langle W_8\psi,\operatorname{diag}(F,F)W_8\psi\rangle
=\frac{72\cdot729+728}{73\cdot1000}
=\frac{729}{1000}-\frac1{73000}.
\tag{19}
\]

La lectura complementaria es uno menos ese valor. Para el lector diagonal de acarreo, el mismo procedimiento da (72·1+2)/73=74/73. Esto no significa que se haya perdido o cambiado el acarreo del registro de entrada: el observable transportado W₈M_cW₈* tiene sobre W₈|d₁⟩ el valor propio exacto 1. El ejemplo distingue conservación de información y cambio de una lectura elegida sobre los canales.

## 9. Relación tipada con K y alcance

La unitaria aritmética J construida aquí actúa sobre BM+1 etiquetas; en el ejemplo, sobre 1001 dimensiones. K pertenece a la realización de doce coordenadas del registro dodecafásico. No hay una identificación dimensional implícita entre esos dos espacios.

Para una composición concreta con K mediante este protocolo habría que declarar un selector material de doce rutas distintas y su realización J₁₂:R¹²→ℓ²(D), con procedencia de las etiquetas y de las operaciones que se pretendan transportar. Con tal dato explícito, JJ₁₂ sería una isometría y se podría comprobar la compatibilidad del operador de rutas con los lectores de K. Esta nota no inventa ese selector ni usa una inclusión arbitraria como generador.

La condición anterior pertenece únicamente a esa composición entre doce coordenadas y el nuevo espacio aritmético. No modifica ni rebaja las isometrías W ya construidas directamente sobre K y sus memorias en R¹², cuyos dominios y operadores están definidos en el manuscrito y en las notas anteriores.

El resultado autónomo de esta nota es completo: la transformación aritmética con acarreo posee una biyección, una unitaria sobre sus etiquetas, lectores diagonales entrelazados, recuperación de rutas a cualquier profundidad y una composición bilateral explícita. Sus estados son los del dominio combinatorio declarado, no automáticamente las historias filtradas TPK. No se infiere de esta construcción un resultado sobre CH ni una validación física global.
