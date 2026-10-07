# Cobertura editorial de lectores gamma y complemento de Schur

11 de septiembre de 2026. Conversión aditiva de dos desarrollos ya contrastados.
Sólo se modificaron los dos cuerpos nuevos y esta nota; no se compiló el PDF,
no se editaron el preámbulo, el núcleo común, el índice ni los propietarios.

## Fuentes y huellas del corte

| Archivo | SHA-256 |
|---|---|
| ampliacion/expediente/AGENTE_CARTAS_Y_EXPECTATIVA.md | `4094e198a3258aeb7702e94ce0a2e294273d11d23872f580c167bc4ea808c006` |
| ampliacion/expediente/AGENTE_SCHUR_DETALLES.md | `7828db1d98d31e8a1c8ba4e3c3cd15976aaa9be375b96ee7866338c623802725` |
| ampliacion/lectores_gamma.tex | `d96471c9843d62382a48ae761c9c8a89af07a7bd87f9ad2b62ec5392d28ff0ec` |
| ampliacion/schur_y_coercividad.tex | `7e651c40c1af085956fd09b77aaefad83b1f36b6616dfa31d6126bb0aa7b1545` |

Las entradas se preservan íntegras en expediente. No se ha promovido ningún
control de archivos o de conversión a prueba de positividad global.

## Mapa de gamma: origen → destino

La sección principal es `sec:lectores-gamma`.

| Origen | Contenido conservado | Destino |
|---|---|---|
| §1 | Cuatro resultados, distinción entre los dos momentos y TPK completo | `gamma-add-sub-5` |
| §2 | Propietarios, rutas, localizadores, extensión efectiva de lectura | Comentarios documentales iniciales y expediente íntegro; nombres científicos en el cuerpo |
| §3 | Genealogía, normalización, traslación, dominio y signo de la diferencia | `gamma-add-sub-32` |
| §4, (1) | Odómetro sobre generadores, modo uniforme, acarreo y todos los cruces | `gamma-add-sub-47`, `gamma-add-eq-1` |
| §5.1, (2)–(4) | Acción de expectativa uniforme, prueba, factor exacto y complemento | `gamma-add-sub-110`, `gamma-add-eq-2` a `gamma-add-eq-4` |
| §5.2, (5) | Refinamiento Helmert, naturalidad y distinción del promedio | `gamma-add-sub-156`, `gamma-add-eq-5` |
| §5.3, (6) | Conjugación simultánea, conservación de dos Grams y alcance | `gamma-add-eq-6` |
| §6.1, (7) | Frontera bidireccional, métrica, normalización polar y cruces | `gamma-add-eq-7` |
| §6.2, (8)–(9) | Carta polar de cinco roles, Gram, coordenadas y polarización | `gamma-add-eq-8`, `gamma-add-eq-9` |
| §7, (10) | Falsador de canal aislado, energía añadida por suma directa y subespacio cíclico | `gamma-add-sub-259`, `gamma-add-eq-10` |
| §8, (11)–(16) | Cotraza con signo, norma, reconstrucción de todas las filas y forma completa | `gamma-add-eq-11` a `gamma-add-eq-16`; alias `gamma-add:cola-lector` |
| §9, (17)–(18) | Transferencia alcanzable, unicidad, contracción condicionada, defecto y dos momentos | `gamma-add-eq-17`, `gamma-add-eq-18`, `gamma-add-display-37` |
| §10 | Procedencia matemática, 25 controles normales/optimizados, alcance | `gamma-add-sub-412`; datos administrativos y comandos en comentarios y expediente |

## Mapa de Schur: origen → destino

La sección principal es `sec:schur-coercividad`.

| Origen | Contenido conservado | Destino |
|---|---|---|
| §1 | Corte causal, ventana, resultado local y procedencia | `schur-add-sub-6` |
| §2, S1 | Dominio cerrado, indicadores, medias, detalles y cota retenida | `schur-add-sub-46`, `schur-add-eq-S1` |
| §3, S2–S3 | Operador de detalles, complemento exacto, prueba e índice negativo | `schur-add-schur-exacto`, `schur-add-eq-S2`, `schur-add-eq-S3` |
| §4, S4–S6 | Imágenes logarítmicas, dominios operatorios, Gram completo y orden de matrices | `schur-add-sub-148`, `schur-add-eq-S4` a `schur-add-eq-S6` |
| §4, S7 | Residual, expansión exacta, Galerkin y error del complemento infinito | `schur-add-residual`, `schur-add-eq-S7` |
| §4, S8 | Separación logarítmica, cota global corregida, integrales singulares y certificación | `schur-add-eq-S8` |
| §5.1, S9 | Margen de detalles N=13, dominio sin reloj primo y valores intervalares | `schur-add-eq-S9` |
| §5.2, S10–S11 | Bloque de media, Tonelli, serie y cola certificada | `schur-add-eq-S10`, `schur-add-eq-S11` |
| §5.3, S12 | Prueba local del signo de r', varianza logarítmica, polar y cruces | `schur-add-eq-S12` |
| §5.4 | Schur positivo, determinante desplazado y coercividad 1/2 | `schur-add:coercividad-ventana` |
| §6 | Todos los refinamientos, diferencia Gram/Schur, contracción y dilatación con dos momentos | Subsección de refinamiento, sin cambiar el alcance a todas las ventanas |
| §7 | 21 controles intervalares, matriz adversarial, falsadores y extensión siguiente | Subsección final; comandos/estados técnicos en comentarios |
| Localizadores | Todos los propietarios y sus rutas | Comentarios finales y expediente íntegro |

## Precisiones contiguas añadidas

1. Se explicitan A_f, B_f, c_Gamma, mu y las dos columnas completas J_+, J_-,
   con dominios y prueba por expansión de su diferencia. No son nuevos
   generadores de constantes; fijan los lectores utilizados en el argumento.
2. La carta bidireccional mantiene como condiciones la inclusión isométrica,
   beta0 inyectivo y Lambda positivo. Se añade la prueba de conservación
   métrica. «Unitaria» se precisa como isometría entre espacios efectivos;
   no se afirma sobreyectividad sobre un ambiente mayor.
3. La carta de cinco roles conserva su Gram de partida; se explicita
   F34*J34F34=eta y la prueba de su transporte mediante T normalizada.
4. El lema `schur-add-retencion-detalles` reúne la prueba de S1: primitiva
   celular, Dirichlet, convolución, Plancherel, cola gamma positiva y cotas
   primas/polares. Se conserva además el argumento de existencia de una
   partición suficientemente fina para una ventana fija.
5. La traslación de la cota local se justifica por conservación de
   correlaciones y compensación de factores polares.

## Condiciones de ensamblaje y riesgos delimitados

- Root debe definir el anclaje `ap:procedencia-reproduccion`. Es la única
  referencia externa a estos dos archivos; las remisiones matemáticas entre
  ellos están resueltas.
- La selección combinatoria particular de las cinco octadas y los factores
  de beta0 no se construyen de nuevo en esta conversión. Se conservan las
  fórmulas y las hipótesis que bastan para sus identidades de cartas, con
  comentarios ENSAMBLAJE que remiten a PP 134–181 y PT 85–155. Su genealogía
  específica no puede darse por demostrada por coincidencias de dimensiones.
- La contracción alcanzable general permanece condicionada; Schur prueba
  su realización en la ventana certificada. No se declara el signo en toda
  ventana ni la identificación de un T_N concreto por mera dilatación.
- Las afirmaciones antiguas de lectura, gates y conservación administrativa
  se conservan en comentarios; no se presentan como nueva validación de
  esta conversión. No se afirma QA visual ni compilación realizada.

## Controles de conservación y sintaxis

Se comprobaron los 37 displays de gamma y los 33 de Schur contra los textos
LaTeX, normalizando únicamente blancos, delimitadores, etiquetas y recursos
de alineación. Los 70 contenidos se conservan; cinco displays se distribuyeron
en líneas alineadas sin cambio de fórmulas. Se retienen también las pruebas,
condiciones, cotas, contraejemplos y las explicaciones de alcance por el mapa
anterior. El cotejo textual no sustituye esta lectura matemática.

El control estático encontró 108 etiquetas propias, ninguna duplicada,
ningún entorno desbalanceado y sólo la referencia externa al apéndice
documental ya comunicada. El cuerpo público no contiene rutas locales ni
URLs crudas. Queda a cargo del editor único la compilación y la revisión
visual de fórmulas, títulos y paginación.
