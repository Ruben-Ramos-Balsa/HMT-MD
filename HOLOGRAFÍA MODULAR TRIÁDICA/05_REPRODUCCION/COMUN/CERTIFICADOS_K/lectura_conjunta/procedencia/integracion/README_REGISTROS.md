# Registros de transición desde los lectores regionales

La cadena APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta
del continuo es la genealogía heredada de los lectores regionales. Este delta
opera después de esas publicaciones: no redefine el generador ni recertifica
las cinco construcciones del continuo. El núcleo y sus propietarios quedan
vinculados en el recibo genealógico; no se añaden como axiomas Lean.

El resultado HMT objeto de esta integración es la construcción de los cuatro
registros de transición desde `regionalPrefixes`, seguida de la recuperación
de sus dos elevaciones. La secuencia efectiva es:

`regionalPrefixes → blockFromPrefix → bandFromWord → wordFromPrefix → recordAt → solveMatrix`.

Los prefijos regionales proceden de los lectores ya comprobados y de sus cotas
internas. El certificado heredado fija 600 trits, agrupados en 100 bloques de
seis: cada bloque pertenece al ambiente de 729 palabras. Esa profundidad es
la utilizada por este certificado finito, no una cota de la prolongación HMT.
`recordAt` conserva el orden de las tres publicaciones y, para cada una, las
filas de los tiempos `t` y `t+1`. Las cuatro especializaciones usan `t=0,1,2,3`.

`RegionalTransitionRecords.lean` reúne siete resultados:

- evaluación exacta de los registros, y su identificación con `X0,Y0,X1,Y1`;
- identificación de los primeros bloques con `selectedSeeds`;
- identificación de las elevaciones calculadas con `L0,L1`;
- ecuaciones de transición, unicidad entre matrices ternarias y existencia
  de un único par de elevaciones para esos registros construidos.

Las tablas `X/Y`, las elevaciones publicadas y los enteros de comprobación
aparecen en las conclusiones y certificados de evaluación, no como argumentos
de los constructores regionales. La auditoría de dependencias del ejecutor
contrasta esta separación sobre los constructores Lean efectivos; su recibo
está en `regional_records_build/VERIFICATION.json`.

Lean y su aritmética sirven como lenguaje de prueba de esa lectura HMT. No se
introducen constantes reales convencionales, decimales objetivo ni valores
metrológicos para seleccionar las filas o resolver las elevaciones.

El alcance preciso es **lector regional posterior → registros → elevaciones**.
No se identifica aquí `recordAt` con nueve iteraciones del operador enriquecido
`Upd∘Tra∘Sel`: esa igualdad tendría otro dominio y otro enunciado. Tampoco se
declara ausente del corpus por no ser el resultado de este módulo.

`RECIBO_REGISTROS_GENEALOGICO.json` conserva los nueve campos efectivos y la
herencia documental; `RECIBO_REGISTROS_CAUSAL.json` comprueba el orden causal.
Sus controles no sustituyen las siete pruebas Lean ni amplían su alcance.
El paquete sellado de 238 módulos no se modifica.
