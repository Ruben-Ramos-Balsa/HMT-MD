# Campos exponenciales del sector torcido: construcción y compatibilidades

Esta continuación conserva el mismo origen seleccionado y la cadena
APP–TRIT–TPK → estado enriquecido → estructura discreta conjunta del continuo.
El retículo marcado, la selección de K, la incidencia excepcional y su cociclo
son los antecedentes efectivos. No se introduce un nuevo selector, un valor
objetivo de K ni una matriz reticular elegida para obtener Moonshine.

## Construcciones efectivas añadidas

Los modos semienteros y la representación finita del corte anterior producen
ahora campos, no sólo un espacio graduado. En la coordenada ramificada t, con
z=t², el potencial creador tiene coeficiente x(−n−1/2)/(n+1/2) en grado 2n+1.
El aniquilador tiene el signo opuesto. Las exponenciales se construyen mediante
sumas finitas en cada coeficiente, para cualquier grado natural: no se impone
un corte global de frecuencias.

El operador de energía demuestra la truncación de la exponencial aniquiladora
sobre cada estado. La base real del tensor con el factor finito permite definir
el núcleo exponencial normalmente ordenado, probar que sus cortes finitos se
estabilizan y obtener un campo Laurent sobre el portador completo. Se prueba
también su acción sobre el espacio fundamental de peso 3/2.

La involución y la inversión de carga actúan sobre los coeficientes de ambas
exponenciales por el signo (−1)^d. Para el núcleo con desplazamiento entero s,
el signo correcto del coeficiente k es (−1)^(k−s), no (−1)^k. La combinación
par tiene coeficientes impares desplazados nulos. Tras retirar t^s, desciende
exactamente a z=t² y preserva el sector torcido positivo. Su restricción es un
campo Laurent efectivo y entrelaza la inclusión del sector; no se supone esa
invariancia.

El conmutador mixto se obtiene derivando el potencial real. La reordenación de
las dos exponenciales se demuestra mediante una recurrencia finita independiente
para cada par de grados. Su contracción impar es −2⟨x,y⟩/(2n+1), con el
emparejamiento del mismo retículo heredado. No se recibe una identidad BCH como
hipótesis.

La serie escalar leída de ese conmutador se identifica con el múltiplo entero
de la serie impar universal, no con una cifra ajustada. Su exponencial formal,
construida por recurrencia y caracterizada por una ecuación diferencial formal,
es la potencia entera de la unidad (1−X)/(1+X) con exponente ⟨x,y⟩. La
biblioteca escalar procede de la colaboración con «radion»; el enlace con el
conmutador reticular se demuestra aquí. Esta identidad escalar no se confunde
con la identidad de reordenación cerrada del producto de dos campos completos.

La energía creadora aumenta el grado d y la aniquiladora lo disminuye. En el
tensor, el núcleo de coeficiente k y desplazamiento s cambia dos veces el peso
conforme en k−s. El término fundamental 3/2 se conserva y se cancela en el
conmutador, no se elimina del portador.
Después del descenso y de la restricción positiva, el coeficiente de grado k
lleva el espacio propio de peso d al de peso d+k. Esto se demuestra para
cualquier d complejo y k entero, no sólo en una tabla de pesos bajos.

Se incorpora asimismo el ensamblaje de cuatro bloques de campos. El bloque
par–par es exactamente el campo reticular ya construido. Los otros tres bloques
son argumentos explícitos de ese ensamblador: éste demuestra linealidad,
truncación y recuperación de cada bloque, pero no fabrica sus argumentos ni
su localidad. Las fuentes de este ensamblador proceden de la colaboración con
«Revisar tesis HMT desde cero» y se conservan sin cambios matemáticos.

## Alcance exacto y continuidad

Todos estos resultados usan el mismo parámetro de origen o : Fin 12 y el mismo
Lattice o; se aplican al selectedOrigin antecedente sin otra elección. El
desplazamiento s del núcleo se declara como parámetro. Retirarlo para el descenso
no demuestra una normalización FLM ni reemplaza el factor y el desplazamiento
que corresponden a cada estado en la familia de campos completa.

La construcción todavía debe reunirse con la normalización reticular, la
corrección de los descendientes torcidos y los productos entre los sectores,
con sus identidades de localidad y de iteración. El ensamblador no sustituye
esas pruebas. La entrega tampoco acredita los tres resultados clásicos
posteriores: carácter J=j−744 de V^natural; identificación de su grupo de
automorfismos con el Monstruo; familia de McKay–Thompson y propiedad de género
cero. El manuscrito utiliza para ellos los teoremas de FLM y Borcherds; una
cita de esos teoremas no es una importación disponible en este cierre Lean.

No se atribuye una nueva prioridad al álgebra de operadores de vértice ni se
presenta este incremento como la formalización completa del artículo I.
Las pruebas heredadas de K y del retículo no se vuelven a abrir ni se declaran
ausentes. Los comentarios de alcance de los paquetes antiguos describen sus
cortes históricos; el recibo de este incremento describe las nuevas pruebas.

## Reproducción y conservación

`recibos/incremento/VERIFICATION.json` enumera el cierre exacto compilado y las
consultas de axiomas de cada declaración pública. `REPRODUCCION.md` explica la
ejecución explícita mediante `reproducir.py`. No se ejecuta código por conectar
un USB. La carpeta y su ZIP contienen los mismos archivos.

Se conserva íntegro y una sola vez el paquete anterior de 388 módulos, con sus
2395 archivos. El verificador autentica esos antecedentes y no los recompila;
compila únicamente el incremento enumerado. Los módulos nuevos admiten sólo
los axiomas ordinarios de Lean propext, Classical.choice y Quot.sound. Las
declaraciones nativas heredadas que usan Lean.ofReduceBool permanecen identificadas
en sus recibos originales; no se ocultan ni se convierten en axiomas nuevos.

Los controles de conservación, de procedencia causal y de pruebas Lean son
independientes. Los dos primeros no sustituyen al tercero ni recertifican las
afirmaciones del corpus completo. Los PDF y las entregas selladas anteriores no
se modifican.
