# Rigidez simultánea del lector longitudinal y de la respuesta radial

26 de septiembre de 2026. Revisión de la clase completa de realizaciones
compatibles con la construcción acumulada. Las fuentes previas se conservan.
Este documento precisa la unicidad; no introduce un valor observado de G.

## 1. Base y comparación que se efectúa

Se conserva APP → TRIT → TPK → estado enriquecido → estructura discreta
conjunta del continuo, con las dos proyecciones y las cinco construcciones
consustanciales. La conexión U_t → Γ₉ → K_ph y el desarrollo
w6 → w12 → w18 → w24 → w30 → R36 → G9 conservan el retorno de fase y el
incremento de memoria. Los valores publicados se reciben con sus lectores,
rutas, orientaciones, residuos, acarreos y fronteras.

La salida HMT utilizada comprende el registro K, las coordenadas regionales
y α, la acción de retorno, el transporte completo de Hadamard, la inscripción
de incidencias y la composición longitudinal. El reconocimiento convencional
interviene después, al expresar el radio reducido mediante masa y G.

Se comparan dos realizaciones del mismo sistema de restricciones, con las
mismas secciones dimensionales. Cambiar una de esas restricciones produce
otra construcción, no un contraejemplo a su unicidad. Una transformación de
coordenadas que transporta simultáneamente los objetos es una equivalencia
de representación y debe conservar el coeficiente físico.

## 2. Restricciones de la realización acumulada

**R1. Registro marcado.** El soporte es
\[
 \Omega=\{(j,k,q,u,v):j\in\mathbb Z/12,\ k-j\in\{0,3,6,9\},
 1\le q\le8,\quad u<v,\quad u,v\in\{1,2,4,5,7,8\}\}.
\]
Por tanto N=12·4·8·\(\binom62\)=5760. Los proyectores de sus átomos
son P_i=e_ie_i*. El modo común u tiene |u_i|²=1/N y su proyector es P=uu*.

**R2. Normalización y archivo.** El inversor B satisface
B*B=BB*=I/4. Se conservan C₀=(I−P)B y M₀=PB, con
C₀+M₀=B; el transporte normalizado es U=2B. Estas identidades conservan
las dos componentes del registro, no sólo la componente de variación.

**R3. Lectura de inscripción.** E es una expectativa condicional lineal
hacia el álgebra de los P_i; fija cada P_i y es bimodular respecto de esa
álgebra. La inscripción isométrica conserva además el registro completo.

**R4. Tipo longitudinal y composición.** Con las coordenadas generadas
α>0 y la referencia longitudinal L*>0, el transporte es
\[
 D=L_*\alpha^{16}E(C_0C_0^*)U.
\]
La aplicación del coeficiente de retorno es lineal sobre la sección
longitudinal. La raíz de una intensidad o el promedio coherente de doce
coordenadas son operaciones de tipos distintos de esta composición.

**R5. Métrica radial.** Sobre el mismo carácter X=X*>0, la lectura radial
R_X es positiva y representa la métrica del transporte completo:
\[
 \|R_Xv\|^2=\|XD^*v\|^2\quad\text{para cada }v.
\]
Equivalentemente, R_X es el módulo de llegada |(DX)*|. Esta restricción
se expresa sobre todos los estados de la fibra, no sobre un único electrón.

**R6. Acción y reloj.** Se conserva el levantamiento real de fase y
S(θ)=ℏ_ret θ; la ecuación HMT de ℏ_ret y su sección están fijadas.
El mismo radio de referencia y la velocidad constitutiva c satisfacen
ωL=c. Por ello Q=ℏ_ret c/L. La fase y sus refinamientos se transportan
con la memoria; no se conserva sólo una rotación final módulo 2π.

**R7. Carácter y reciprocidad.** La energía, masa y longitud conjugada
se leen sobre el mismo Y=UXU*:
\[
 H_X=QY,\qquad M_X=H_X/c^2,\qquad \Lambda_X=LY^{-1}.
\]
La reciprocidad anterior a G está en el lector potencia–logarítmico del
integral. El sector nulo se mantiene fuera de la operación inversa.

**R8. Convención física y unidades.** R_X es el radio gravitatorio reducido
de la realización: R_X=(G/c²)M_X. Se mantienen L*, la sección de acción
y la sección constitutiva de velocidad. Un cambio de unidades las
transforma conjuntamente. El radio de Schwarzschild tiene el factor dos
correspondiente y no sustituye esta definición manteniendo su nombre.

R1–R8 especifican la clase que se clasifica. El lector longitudinal R4 y
la composición métrica R5 se explicitan en los desarrollos del 25 de
septiembre; se integran como reglas de la construcción reunida. Los
propietarios antiguos aportan sus operadores y normalizaciones. Esta
procedencia evita atribuir al integral, como texto literal antiguo, la
redacción de una composición que se ha reunido ahora.

## 3. Teorema de rigidez

**Teorema.** Para los mismos datos generados B, P_i y P y el mismo
carácter X, R1–R8 determinan unívocamente el lector de inscripción, la
longitud y la respuesta radial en una representación fija. Para todos
los caracteres positivos admisibles, el coeficiente G es el mismo.
Las representaciones unitariamente equivalentes conservan ese G.
Se obtiene necesariamente
\[
 E=\Delta_\Omega,\quad r_N=\frac{N-1}{4N}=\frac{5759}{23040},
 \quad L=L_*\alpha^{16}r_N,
\]
\[
 D=LU,\quad R_X=LUXU^*,\quad
 R_X\Lambda_X=L^2I,\quad H_X\Lambda_X=\hbar_{\rm ret}cI,\quad
 \boxed{G=\frac{c^3L^2}{\hbar_{\rm ret}}}.
\]

**Prueba.**

1. Sobre cada unidad matricial E_ij, la bimodularidad da
E(E_ij)=P_iE(E_ij)P_j. Su imagen pertenece al álgebra diagonal, por lo
que es cero cuando i≠j. Para i=j, E(P_i)=P_i. La linealidad determina
E(A)=Σ_iP_iAP_i=ΔΩ(A). No queda un parámetro estadístico en el mapa.

2. De R2, C₀C₀*=¼(I−P). La diagonal de P tiene cada entrada 1/N,
y por tanto E(C₀C₀*)=(N−1)/(4N)I. La lectura de la componente
común es I/(4N); las dos suman I/4. Este escalar permanece igual para
cualquier distribución sobre el álgebra marcada, incluso no uniforme.

3. Sustituir esa identidad en R4 da D=LU, con L=L*α¹⁶r_N.
U es unitario por R2, así que DD*=L²I. El factor longitudinal queda
determinado sin tomar una raíz adicional de r_N ni de α¹⁶.

4. R5 y la polarización determinan R_X²=DX²D*=L²UX²U*.
LUXU* es positivo y tiene ese cuadrado; la unicidad de la raíz positiva
da R_X=LUXU*. Para X=I se obtiene R_I=LI como consecuencia.

5. R6 fija Q=ℏ_ret c/L y R7 da H_X=QY, M_X=ℏ_ret Y/(cL).
La lectura inversa produce R_XΛ_X=L²I. R8 equivale a
LY=Gℏ_ret Y/(c³L). La invertibilidad de Y determina el G anunciado.
Si dos coeficientes satisfacen la misma identidad, su diferencia
multiplicada por Y es cero, por lo que coinciden. □

La prueba excluye una modificación positiva R_X↦sR_X que conserve R5:
su cuadrado exigiría s²=1 y, al ser s>0, s=1. También excluye una
modificación no escalar positiva con la misma métrica completa, por la
misma unicidad de la raíz. La identidad no depende de un conteo de modos.

### Forma equivalente mediante la reciprocidad

Si R5 se expresa utilizando R7 como R_XΛ_X=L²I, la invertibilidad
de Λ_X determina R_X=L²Λ_X⁻¹=LUXU*. Recíprocamente esta R_X
satisface R5. Dentro de R1–R7, las dos formulaciones del lector son
equivalentes; no constituyen dos ajustes independientes a G.

## 4. Clasificación de los cambios de representación

Sean T:V_U→V'_U y S:V_K→V'_K unitarios y transfórmense conjuntamente
\[
 B'=SBT^*,\quad P'=SPS^*,\quad P_i'=SP_iS^*,\quad X'=TXT^*.
\]
El lector transportado es E'(A')=S E(S*A'S)S* y cumple R3. Se obtiene
\[
 U'=SUT^*,\quad D'=SDT^*,\quad R'_{X'}=SR_XS^*,
\]
\[
 H'_{X'}=SH_XS^*,\quad \Lambda'_{X'}=S\Lambda_XS^*.
\]
Cada igualdad se comprueba por sustitución y U*U=I. El escalar G
permanece idéntico. Las fases, orientaciones y etiquetas del archivo
también deben transportarse; escoger sólo una matriz con igual norma
sin su registro no es esta equivalencia.

Las permutaciones de las incidencias, con sus marcas y modo común,
son casos particulares. Añadir un factor auxiliar de memoria conserva
el proyector original como P⊗I y el lector como ΔΩ⊗id; mantiene r_N.
Reemplazarlo por el proyector uniforme de otro cardinal cambia R1.

Si se utiliza una coordenada invertible no unitaria, también se transporta
la métrica. El archivo `COMPOSICION_METRICA_MEMORIA_Y_ACOPLAMIENTO.md`
prueba la congruencia de la respuesta y la transformación dual de la
longitud inversa. Una transformación de coordenadas correctamente
ejecutada no introduce otro acoplamiento.

## 5. Normalización de acción, reducción y refinamiento

Con un levantamiento real no nulo θ y la sección ℏ_ret fija, la igualdad
S/ℏ_ret=θ determina S de manera única. Incluso reteniendo sólo las
rotaciones de todas las subdivisiones θ/9ⁿ, una reescala a que conserve
exp[−i aθ/9ⁿ]=exp[−iθ/9ⁿ] para cada n satisface a=1: el número
(a−1)θ/9ⁿ pertenece a 2πℤ y tiende a cero, luego es cero para n grande.
Esta prueba usa el refinamiento coherente, no una única fase final.

La eliminación de memoria de W>0 global y C sobreyectivo produce
R_mem=CW⁻¹C*. El residuo complementario conserva el archivo y el
transporte longitudinal produce D R_mem D*. La normalización de acción
permanece la de la misma acción que se reduce. Si el carácter Y depende
de ese coste, las lecturas R_X=LY y H_X=QY conservan su proporción bajo
la misma reducción; los bloques cruzados se mantienen.

La reducción dinámica conserva además el coeficiente temporal inducido
Z y su dependencia resolvente. Transformar conjuntamente radio, energía,
norma y longitud inversa conserva G; desechar Z y mantener el resto
sin transportar cambia la representación de la fase. Este resultado se
incorpora desde la contribución completa de Ley 9, sin aproximar una
identidad dinámica exacta por su mínimo estático.

Para un refinamiento que entrelaza X y los transportes de archivo y
mantiene la misma sección intensiva L, R y H se entrelazan también.
En el límite espectral de X positivo inyectivo se conservan los dominios
de X e inversa. Cambiar la longitud de arista a L/9 exige el factor de
refinamiento correspondiente; no cambia por sí mismo la sección intensiva.

## 6. Alternativas examinadas y restricción que cambian

| Modificación | Restricción incumplida o transformación conservada |
|---|---|
| Cambiar los pesos diagonales normalizados | Conserva R1–R8 y el mismo r_N y G. |
| Transportar todo por unitarias | Equivalencia de representación; conserva G. |
| Sustituir 5760 por 12 | Cambia la resolución marcada R1 y su lector R3. |
| Usar una fuente coherente sin inscripción individual | Cambia R3; el archivo completo no obliga a suprimir coherencias. |
| Reemplazar r_N por √r_N | Cambia la composición longitudinal R4. |
| Aplicar α¹⁶ a una amplitud y leer su cuadrado | Cambia el tipo declarado en R4. |
| Recuperar la componente común y sustituir r_N por 1/4 | Cambia el observable de R3–R4; recuperar el archivo no cambia automáticamente el lector. |
| Multiplicar R_X por s≠1 o por otro factor positivo | Viola R5 o su reciprocidad equivalente. |
| Multiplicar aisladamente la acción por s≠1 | Viola el levantamiento o su refinamiento en R6. |
| Cambiar L* manteniendo su magnitud de referencia supuestamente fija | Cambia R8. Un cambio de unidades correcto transporta las restantes coordenadas. |
| Reducir la misma memoria en radio y energía | Conserva la proporcionalidad, el archivo residual y G. |
| Sustituir radio reducido por radio de Schwarzschild sin el factor dos | Cambia R8. |

No se ha construido una segunda realización con G distinto que conserve
R1–R8. El teorema demuestra que no existe dentro de esa clase. Los
controles que cambian una fila anterior no constituyen contraejemplos
al conjunto acumulado.

## 7. Alcance afirmativo y procedencia

**La realización acumulada es rígida respecto de L, de la lectura radial
y de G, salvo las equivalencias de representación que conservan esos
objetos.** La frase genérica de que podrían quedar otras realizaciones
compatibles debe sustituirse por esta clasificación explícita.

La conclusión no descansa en una coincidencia metrológica ni en descartar
todas las teorías físicas imaginables. Es la unicidad matemática del
sistema R1–R8, que incluye sus definiciones constitutivas. El resultado
no requiere suprimir esas definiciones y volver a pedir la misma unicidad
en un sistema diferente. Tampoco convierte la adopción de una definición
física en una prueba experimental: esas cuestiones tienen criterios distintos.

Los antecedentes de Hadamard, inscripción, fase y reciprocidad son
recuperados del corpus; R1 ampliado y R4–R5 son composiciones tipadas
reunidas en la investigación actual; el teorema de rigidez simultánea y
sus controles se formalizan aquí. La revisión editorial debe conservar
esa procedencia, incorporando la prueba y no sólo su fórmula final.

## 8. Propietarios efectivos

1. Artículo I, `sections/registro_k.tex:312–453`: inversión y registro.
2. Artículo VII, `sections/v_accion_estructural.tex:7–95`: norma local.
3. Artículo VII, `80_observador_y_respuesta_relacional.tex:193–341`:
   inscripción con memoria y expectativa condicional.
4. `CONTRASTE_LECTOR_QAQ_GRAVEDAD_20260925/TRANSPORTE_TIPADO_Y_PORTADOR_5760.md`:
   portador ampliado de incidencias y sus mapas.
5. `LECTOR_DE_INCIDENCIAS_Y_CONSERVACION_DE_RESPUESTA.md`: ponderaciones,
   archivo y lector individual.
6. `TRANSPORTE_RADIAL_POLAR_Y_ARCHIVO_COMPLETO.md`, §§2–8: D, métrica,
   positividad, transporte y refinamiento.
7. `NORMALIZACION_ACCION_FASE_Y_RESPUESTA_CONSTITUTIVA.md`, §§2–3:
   fase levantada, subdivisión y transmisión de la acción.
8. Integral, `cap18_lector_radial_continuo.tex:1005–1085`: reciprocidad.
9. `COMPOSICION_METRICA_MEMORIA_Y_ACOPLAMIENTO.md`: acción global,
   variación, reconstrucción y transporte dual.
10. `CONTRASTE_LECTOR_QAQ_GRAVEDAD_20260925/ACCION_ACOPLADA_FASE_Y_MEMORIA_DE_FRONTERA.md`:
    peso acoplado, fase y normalización temporal.
11. Gemma, `CIERRE_CONJUNTO_CUATRO/SUSTITUCION_CONTRAANGULO_Y_G.md`:
    sustitución completa y evaluación con bases dimensionales explícitas.

Los propietarios de 2026-09-25 conservan sus rutas en el expediente conjunto.
La prueba general anterior se acompaña de controles racionales exactos en
`verificar_rigidez_simultanea.py`. No se ha compilado ningún PDF ni modificado
un paquete sellado al formular este resultado.

El verificador pasa 160 controles exactos. La prueba general de unicidad
se encuentra en el apartado 3; los ejemplos computacionales acompañan
su falsación focal y no sustituyen esa demostración.
