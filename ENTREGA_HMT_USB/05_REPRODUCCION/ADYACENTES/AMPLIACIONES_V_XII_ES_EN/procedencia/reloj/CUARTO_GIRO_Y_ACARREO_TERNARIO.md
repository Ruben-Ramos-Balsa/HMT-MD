# Cuarto de giro, acarreo ternario y memoria del reloj completo

29 de septiembre de 2026. Desarrollo focal para la acumulación global. Los PDF y las fuentes anteriores permanecen intactos.

## Procedencia y alcance

La existencia del cuarto de giro está demostrada en `XII_ES/ampliacion_20260922.tex`, mediante la isometría W y la identidad C12 W = W J0. El acarreo y la extensión no escindida están demostrados en `XII_ES/sections/registro_k.tex`. Ambos archivos pertenecen a `CUMPLIMIENTO_EDITORIAL_20260928/fuentes`. El presente resultado reúne esas dos construcciones y determina exactamente qué memoria pierde su reducción al cuarto de giro. No presenta como nuevos ni el teorema chino de los restos ni el cuarto de giro ya construido.

### APP:

Se reciben las hojas aritméticas y sus nueve posiciones, con residuo, cociente e incidencias. El calendario es una lectura de las rutas producidas, no un sustituto de la generación.

### TRIT:

Se conservan régimen y orientación, incluida la diferencia entre retorno de fase y prolongación del estado. La componente de orden tres que aparecerá abajo se deriva aritméticamente del reloj recibido; no se identifica por su cardinal solamente con todos los datos de TRIT.

### TPK:

Se componen dos salidas existentes: el calendario observable de 108 posiciones, con inclusión β ↦ 9β de C12 y reducción a C9; y el plano de período cuatro del operador C12, con C12 W = W J0 y J0² = −I. La actualización enriquecida y la holonomía nonádica preceden a ambos lectores.

### Estado enriquecido:

La división θ = r + 9β, con 0 ≤ r < 9 y 0 ≤ β < 12, describe el calendario reducido. El registro de incidencias, la hoja y la memoria ilimitada permanecen en el estado de origen. Aquí r es de base cero; la fuente utiliza r+1 al enumerar posiciones.

### Estructura discreta conjunta del continuo:

Se recibe la construcción conjunta con sus cinco aspectos y sus lectores tipados. El cálculo siguiente actúa sobre una publicación finita posterior; no separa los aspectos del continuo ni pretende reconstruirlo a partir de un residuo.

### Salida HMT focal:

El cuarto de giro y la fase nonádica recuperan exactamente un cociente de 36 posiciones. El reloj de 108 conserva, además, una fibra ternaria. Esa fibra sostiene la parte no escindida de la extensión del reloj y queda invisible en la reducción de 36 posiciones.

### Reconocimiento convencional posterior:

La descomposición por residuos coprimos prueba las identidades siguientes. La notación angular π/2 reconoce J0 después de su construcción, sin elegir por aproximación decimal el operador original.

## 1. El reloj se separa en una componente cuaternaria y una ternaria de orden 27

La aplicación

\[
F:C_{108}\longrightarrow C_4\times C_{27},\qquad
F(\theta)=(j,z)=(\theta\bmod4,\theta\bmod27)
\]

es un isomorfismo. Su inversa es

\[
\theta=81j+28z\pmod{108}.
\]

Prueba: 81 es 1 módulo 4 y 0 módulo 27; 28 es 0 módulo 4 y 1 módulo 27. El inverso restituye ambos residuos y el producto de los dos órdenes es 108.

Bajo este isomorfismo, la inclusión β ↦ 9β se convierte en

\[
\beta\longmapsto(\beta\bmod4,9\beta\bmod27),
\]

y la proyección a C9 es (j,z) ↦ z mod 9. Por tanto, la sucesión exacta original contiene una componente cuaternaria separable y la extensión ternaria

\[
0\longrightarrow C_3\longrightarrow C_{27}\longrightarrow C_9\longrightarrow0.
\]

Esta última no se escinde: C3 × C9 tiene exponente 9 y C27 tiene exponente 27. La no escisión del reloj completo se localiza así en el acarreo ternario, aunque el plano de cuarto de giro sea perfectamente definido.

## 2. La fase del plano y el residuo cuaternario global se relacionan mediante la posición nonádica

Sea b = β mod 4. El plano W lee b. El residuo global j verifica

\[
j=r+b\pmod4.
\]

Prueba: θ = r + 9β y 9 ≡ 1 mod 4. Sobre el núcleo r = 0 ambas coordenadas coinciden. Fuera de él, deben transportarse conjuntamente.

La función β mod 4 no es un homomorfismo de C108: β(8) = β(1) = 0, mientras β(9) = 1. Su composición contiene el acarreo

\[
b''=b+b'+\left\lfloor\frac{r+r'}9\right\rfloor\pmod4,
\qquad r''=r+r'\pmod9.
\]

Así, el par (r,b) representa C36 con su ley efectiva, y equivale a (θ mod 9, θ mod 4) mediante j = r+b mod 4. Olvidar el acarreo alteraría la operación, no sólo la notación.

## 3. Tres historias del calendario comparten la lectura reducida

El lector (r,b) tiene núcleo {0,36,72}. Cada par admite exactamente tres preimágenes θ, θ+36 y θ+72 en C108. Por ejemplo:

\[
\theta=0,36,72:\quad r=0,\quad b=0,
\quad z=0,9,18.
\]

La fase nonádica y el plano de cuarto de giro coinciden, pero la componente ternaria de orden 27 las distingue. Para la coordenada dodecafásica, añadir k = β mod 3 permite recuperar

\[
\beta=9b+4k\pmod{12}.
\]

Se recupera β, no la memoria ilimitada ni todas las incidencias del estado enriquecido. Después de 108 actualizaciones puede retornar el calendario entero mientras la memoria nonádica aumenta en 12, tal como ya establece la fuente.

El cociente C36 sí admite una sección homomorfa de su proyección a C9: n ↦ 28n mod 36. Por tanto, la lectura reducida elimina precisamente la obstrucción ternaria a la escisión. Éste es un contenido estructural de la pérdida de memoria, además de un conteo de preimágenes.

## 4. Ángulo de representación y fase del reloj

El carácter fiel del reloj es χ108(θ) = exp(2πiθ/108). En las coordenadas anteriores:

\[
\chi_{108}(\theta)
=\exp(2\pi i j/4)^3\exp(2\pi i z/27)^7.
\]

La identidad se deduce al dividir θ = 81j+28z por 108. El exponente 3 invierte la orientación del factor cuaternario; no se puede suprimir. Para θ = 27, j = 3 y z = 0: el factor cuaternario vale −i y su cubo vale i, restituyendo la fase correcta.

Sobre θ = 9β, el carácter fiel avanza π/6 por unidad de β, mientras el plano W avanza π/2: su carácter es el cubo de esa restricción. La misma representación de C12 admite nueve extensiones como carácter de C108, con índices ℓ ≡ 3 mod 12. El índice 27 corresponde a la proyección θ mod 4. Esta clasificación explicita los lectores; no modifica el cuarto de giro ni selecciona una frecuencia física por semejanza de fases.

El cuarto de giro relativo de una frecuencia de masa, estudiado en la contribución coordinada, debe conservar su propio lector temporal. En particular, el tiempo 27 t0/|ΔΞ| procede de ΔΩ = 2πΔΞ/(108t0). No se identifica automáticamente con una actualización β ↦ β+1 del plano W.

## 5. Lectura narrativa

El cuarto de giro tiene una genealogía operatoria precisa en el registro HMT. Su significado se amplía al conservar simultáneamente el reloj del que se extrae: el cuarto organiza una relación orientada en el plano, y la componente ternaria conserva distinciones que ese plano no representa. La fase retorna mientras otra coordenada continúa distinguiendo la trayectoria.

Ésta es la aportación focal: situar la pérdida exacta de información en una aplicación concreta, exhibir las tres preimágenes y mostrar qué propiedad de composición desaparece al reducirlas. La memoria no se añade verbalmente a una figura circular; aparece en la ley de acarreo que relaciona las coordenadas.

Al reunirlo con la elipse de acción, el mismo cuarto de giro tiene una lectura areal h/4. Al reunirlo con una frecuencia relativa, tiene una lectura ΔE·t = h/4. Son composiciones ya justificadas o justificadas en la contribución coordinada, con lectores definidos. El nuevo diagrama evita confundir esos resultados entre sí o con una proximidad numérica aislada.

## 6. Comprobación y límites del resultado

`verificar_reloj.py` comprueba exhaustivamente las 108 posiciones, todos sus pares de composición, la reducción de 36 posiciones, el acarreo y las identidades de caracteres mediante fracciones exactas. Incluye falsadores para la identificación incorrecta de b con j, la supresión del cubo orientado y la restitución del calendario completo desde sólo (r,b).

La prueba general está en las identidades anteriores. La comprobación finita cubre exactamente estos grupos finitos; no se presenta como formalización global del corpus ni como nueva ley cosmológica. La inclusión matemática en los PDF queda para la integración editorial autorizada.
