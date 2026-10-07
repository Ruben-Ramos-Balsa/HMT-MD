# Suplemento Lean focal de IV y V

Suplemento integrado el 14 de septiembre de 2026. **Seis unidades compiladas,
49 declaraciones comprobadas por Lean4.21.0**, incluidos lemas auxiliares y
controles negativos expresados como teoremas. Son42 declaraciones nuevas de
certificación y7 reutilizadas del balance bilateral, no49 resultados físicos
nuevos ni una formalización completa de los artículos.

`RESULTADO_LEAN.json` contiene la ejecución propia: seis compilaciones con
salida0, inventario exacto de declaraciones/axiomas y cuatro mutaciones erróneas
rechazadas. El mapa documenta la correspondencia con las fuentes matemáticas;
el campo current_bilateral_owner identifica el desarrollo local incorporado.

## Dependencias y reproducción sin descargas

Única dependencia: el toolchain **Lean4.21.0** ya instalado, con su biblioteca
`Std`. No se usa Mathlib, Lake, paquetes externos ni `native_decide`.
`lean-toolchain` fija la versión, pero el comprobador recibe directamente
el binario instalado y rechaza lanzadores Elan/Lake. No instala nada.

Desde cualquier directorio, usando rutas absolutas para el programa y binario:

```sh
python3 -I -S -B /ruta/al/suplemento/verificar_lean.py \
  --lean-bin /ruta/al/toolchain/lean-4.21.0/bin/lean
```

Desde esta carpeta pueden seleccionarse las unidades pertinentes:

```sh
python3 -I -S -B verificar_lean.py --lean-bin /ruta/al/bin/lean --article IV
python3 -I -S -B verificar_lean.py --lean-bin /ruta/al/bin/lean --article V
```

`IV` comprueba23 declaraciones en tres unidades; `V`,33 en cuatro unidades.
Las siete del balance se comparten; la unión tiene49, no56. La selección
predeterminada `ALL` comprueba las seis unidades de esta propuesta conjunta.
Cada `.lean` es independiente y sólo importa `Std`; también puede ejecutarse:

```sh
/ruta/al/bin/lean -DwarningAsError=true IVRegistro.lean
```

El comprobador imprime JSON sin escribir por defecto. `--output RUTA_NUEVA`
guarda un recibo nuevo y rechaza sobrescribirlo. `--negative-controls` compila
copias mutadas en una carpeta temporal hija del suplemento, que retira al
terminar; por ello esa opción requiere una copia de trabajo escribible.
Las fuentes buenas permanecen intactas. En una distribución sellada ejecutar
sin esa opción, o probarla después de extraer el paquete en una carpeta nueva.

## Qué se ha formalizado

El mapa máquina `MAPA_TEOREMAS.json` enumera **cada declaración**, su unidad,
dominio, propietario, etiquetas y líneas de origen. Las rutas TeX son relativas
a la raíz de fuentes de cada artículo; sus hashes identifican el corte previo
a la integración editorial actual, no certifican futuros cambios de esas fuentes.
Los propietarios no se cargan ni se necesitan para compilar Lean. El mapa
documenta correspondencia matemática; el compilador comprueba el enunciado Lean,
no traduce automáticamente el texto del manuscrito.

### IV: registro e intercambio

- `IVRegistro.lean`: para **todo** bloque entero de cuatro coordenadas,
  demuestra `H4(H4 x)=4x`, recuperación por división entera, inyectividad y
  caracterización de la imagen por divisibilidad de `H4 u` entre4.
  Levanta la operación a las tres órbitas `(r,r+3,r+6,r+9)` del registro de12
  coordenadas y prueba recuperación e inyectividad para cualquier registro.
  Generaliza el patrón `h4Block` de `HMT/Dodecaphase.lean` de continuoREV14:
  no se limita a sus tres igualdades sobre el vector literal archivado.
  El contraejemplo final sólo muestra que olvidar coordenadas pierde información.
- `IVDualidad.lean`: intercambio en `Int²`, involución del estado con una
  inversión abstracta cuya ley es hipótesis explícita, intercambio de la forma
  `u*m²+v*w²`, involución por cambio de índices y conjugación de operadores
  diagonales sobre funciones `Int² -> Int`. El último lema demuestra que la
  conjugación por dos mapas inversos transporta cualquier involución.

**Frontera precisa:** el radio positivo real, la sustitución analítica
`u=R⁻²,v=R²`, `ell²`, autoadjunción, transporte de dominios, resolvente compacto,
VOA, Moonshine y teoríaM no están formalizados en estas unidades. Tampoco el
extractor íntegro de25 coordenadas ni la producción o selección de canales.
La recuperación Hadamard no se presenta como productor de una semilla.

### V: acoplamiento, exclusión y factores

- `VAcoplamiento.lean`: representa `Z/9Z` mediante `Fin9` y operaciones modulares
  explícitas. Para cualquier tipo `S` y lectura `r:S->Fin9`, prueba ambas
  composiciones inversas de `(s,a)↦(s,a+r(s))`, inyectividad y sobreyectividad.
  Distingue esa reversibilidad del olvido posterior del aparato mediante un
  contraejemplo concreto.
- `VFermiones.lean`: construye los operadores de creación y aniquilación sobre
  la base ordenada `vacío,e0,e1,e0∧e1`, con **amplitudes enteras arbitrarias**.
  Prueba nilpotencia, CAR para modos iguales/distintos e idempotencia de ocupación.
  No son pruebas restringidas a cuatro vectores de ejemplo: las amplitudes se
  cuantifican universalmente. Además demuestra idempotencia en `I->Int` para
  cualquier tipo `I`, bajo CAR, conservación de resta y nilpotencia explícitas.
  Construye el intercambio graduado —signo menos en el sector de dos partículas—,
  prueba su involución y transporte de creación, aniquilación y ocupación.
  Las identidades de transporte escalar se prueban para todo escalar entero.
  El contraejemplo final rechaza el intercambio que omite el signo exterior.
- `VFactores.lean`: enumera recursivamente los pesos de **todas** las ocupaciones
  binarias de una lista finita cualquiera. Demuestra por inducción que la suma
  es el producto de los factores `(1+u)` y que existen `2^g` términos,
  conservando multiplicidades. Los pesos son enteros libres, no datos térmicos.

**Frontera precisa:** no se formalizan la construcción exterior general sobre
Hilbert, los operadores complejos arbitrarios, CCR bosónica, la topología de
Fock, el teorema relativista de espín–estadística, la medición física, las
exponenciales térmicas, las derivadas de `log Z`, la serie bosónica infinita ni
el límite termodinámico. La factorización es el componente combinatorio
finito del teorema impreso, no toda su realización analítica.

### Balance bilateral compartido

`BalanceBilateral.lean` es copia **byteidéntica** del libroREV02, SHA-256
`7a64d9c467cde94750a3f627a142ccecf4cdebd573eb6f61fb0e416f933c8934`.
Sus siete declaraciones certifican, sobre enteros,

```text
9(8x-y)² + 8(9x+y)² = 17(72x²+y²),
(8x-y)+(9x+y)=17x,
8(9x+y)-9(8x-y)=17y.
```

La suma en dimensión finita arbitraria y la inyectividad del par completo
tienen pruebas. La especialización `17*73` supone explícitamente igualdad
de las sumas de cuadrados. El propietario bilateral está incorporado en la sección de acoplamiento
aritmético-geométrico; el mapa conserva además su procedencia en el libro.
No deben atribuirse a esta unidad la ley operatoria general de parámetro `a`,
los adjuntos `B*,C*`, ni su producción desde APP–TRIT–TPK. La unidad preserva
el comentario de procedencia original, sin arrastrar otras dependencias del libro.

## Fundamentos y controles del propio comprobador

Cada teorema tiene `#print axioms`. Las fuentes aceptadas no usan `sorry`,
`admit` ni axiomas propios. Los axiomas estándar que aparecen son un subconjunto
de `propext`, `Quot.sound` y `Classical.choice`, y quedan registrados por
declaración. No se afirma ausencia de esos fundamentos de Lean.

El comprobador exige versión, importación exclusiva de `Std`, inventario exacto
de teoremas, salida0 de Lean con advertencias como errores y auditoría completa
de axiomas. También verifica la identidad del certificado bilateral reutilizado.
El recibo JSON no sustituye las pruebas Lean ni el contraste con el texto.

Se ejecutaron y rechazaron cuatro cambios deliberadamente falsos: signo de una
fila Hadamard, signo de la inversa del acoplamiento, signo del intercambio
exterior y signo del factor fermiónico. Sus diagnósticos pueden contener
`sorryAx` porque Lean rellena provisionalmente un objetivo fallido al informar
del error; **esas compilaciones terminan con error y no son pruebas aceptadas**.
Ninguna unidad aprobada depende de ese axioma. Los mutantes no se entregan como
fuentes, sólo se conserva el diagnóstico en el recibo de ensayo.

## Selección por artículo

IV necesita `IVRegistro.lean`, `IVDualidad.lean` y `BalanceBilateral.lean`.
V necesita `VAcoplamiento.lean`, `VFermiones.lean`, `VFactores.lean` y
`BalanceBilateral.lean`. Acompañar cada selección con este README, el mapa,
el comprobador y `lean-toolchain`; ejecutar con el perfil correspondiente.
No denominar49 al inventario individual de ninguno de los artículos.

Las huellas anteriores se conservan como procedencia. El recibo de controles
de la entrega documenta la ejecución del perfil correspondiente; la reproducción
del ZIP se registra separadamente de los ensayos anteriores.
