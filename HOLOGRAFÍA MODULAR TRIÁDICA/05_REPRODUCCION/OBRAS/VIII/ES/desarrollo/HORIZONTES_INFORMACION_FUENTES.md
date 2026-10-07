# Recuperación de horizontes e información — artículo VII

Fecha: 10 de septiembre de 2026. Incorporación focal autorizada.

Destino: manuscrito/70_horizontes_e_informacion.tex.
La sección reúne nueve enunciados con sus nueve pruebas, además de la
demostración breve del corte mínimo, el cálculo de la multiplicidad efectiva
y el argumento de naturalidad y conservación de entropía bajo transporte.
No modifica II, V, el integral, la acción material ni el cálculo de amplitud.
No acredita la autonomía completa de VII ni una autorización de publicación.

## Fuentes leídas y conservadas

Los tres propietarios indicados se leyeron completos. Sus copias son idénticas
por SHA-256 a los originales y al inventario FUENTES_Y_ALCANCE.json.

1. **Entropía sectorial, 307 líneas.**
   Origen: /Users/ruben/Documents/New project/output/ARTICULO_II_REV10_EDICION_INTEGRADA_20260910/manuscrito/sections/09c_entropia_sectorial.tex.
   Copia: fuentes_conservadas/horizontes_informacion/09c_entropia_sectorial.tex.
   SHA-256: c71610279d4c36baae0cb808150b575f11cf0cf593064cb877bbcbd295a60ecb.
2. **Confluencia, 212 líneas.**
   Origen: /Users/ruben/Documents/New project/output/ARTICULO_II_REV10_EDICION_INTEGRADA_20260910/manuscrito/sections/11_confluencia.tex.
   Copia: fuentes_conservadas/horizontes_informacion/11_confluencia.tex.
   SHA-256: 83650142f394117d28f58951c282d19838d3932762da6f004a026bfa83b6a056.
3. **Doble hoja y Kruskal, 144 líneas.**
   Origen: /Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_iv_v/tex/residencias/85_agujero_negro_doble_hoja.tex.
   Copia: fuentes_conservadas/horizontes_informacion/85_agujero_negro_doble_hoja.tex.
   SHA-256: 7ddae72507830be9e4f77cd947dfad129602738a4e3dc9c1a820d4e10dfdf825.

Antecedente adicional consultado para materializar la remisión al corte de 81
enlaces, que ya forma parte de la confluencia:

4. Origen: /Users/ruben/Documents/New project/output/ARTICULO_II_REV10_EDICION_INTEGRADA_20260910/manuscrito/sections/09_area.tex.
   Copia: fuentes_conservadas/horizontes_informacion/09_area_antecedente_corte.tex.
   SHA-256: 39b8d600e66393d07fea6e96f0838d6b2f09c80307c050e0f06af13c29e9d0a4.
   Se consultaron su construcción de incidencia y el teorema del corte mínimo
   con prueba. La copia preserva el archivo completo; no sustituye por inclusión
   nominal sus otras dependencias, que se reunirán en el antecedente areal.

## Mapa fuente → resultado público

| Fuente y localizadores | Destino por etiqueta | Contenido y estatuto |
|---|---|---|
| Doble hoja, 5–44 | vii:subsec:hojas-purificacion | Canales, estado de hoja, vector bipartito, traza parcial y entropía exacta. RESULTADO_RECUPERADO. |
| Entropía sectorial, 1–94 | vii:subsec:purificacion-sectorial; vii:prop:respuesta-sectorial | 18+18 factores, ocupaciones, Gibbs finito, TFD, momentos y entropía. RESULTADO_RECUPERADO. |
| Entropía sectorial, 96–148 | vii:eq:deficit-informacional; vii:eq:respuestas-area-entropia | Déficit respecto del estado uniforme, varianzas, derivadas y escala de área. RESULTADO_RECUPERADO. |
| Entropía sectorial, 150–204 | vii:thm:inversion-sectorial | Complementación 0↔2, constantes 72 y 7560, área complementaria, entropía par y distancia relativa. RESULTADO_RECUPERADO. |
| Entropía sectorial, 206–307 | vii:thm:ley-modular-finita | Referencia fiel, primera ley infinitesimal, corrección finita de entropía relativa y positividad; prueba también para estados no conmutativos. RESULTADO_RECUPERADO. |
| Confluencia, 55–123; área, teorema del corte mínimo | vii:subsec:conversion-informacion-area | Energía de decisión, área elemental, tensión energía/área, corte mínimo y estado uniforme de 81 enlaces. RESULTADO_RECUPERADO. |
| Confluencia, 4–53 y 125–171 | vii:subsec:balance-horizonte | Unidad Planck, horizonte cosmológico, producto TS=E y dos duraciones de media acción; rama positiva y sección común. RESULTADO_RECUPERADO. |
| Confluencia, 198–212 | Párrafo posterior a vii:eq:diferencial-horizonte | Multiplicidad efectiva e^π y exponencial hiperbólico, conservando el mapa de realización como dato adicional. RESULTADO_RECUPERADO. |
| Doble hoja, 46–103 | vii:thm:kruskal-hojas | Carta, métrica, inversión, radio y horizontes, vacío exterior. RESULTADO_RECUPERADO. |
| Doble hoja, 105–144; confluencia, 173–196 | vii:subsec:transporte-informacion-horizonte | Unitaria, isomorfismo/UCP, estado, flujo modular, refinamiento y bipartición transportada. RESULTADO_RECUPERADO. |

La reorganización reúne las leyes modular infinitesimal y finita en un teorema,
y los momentos y sus respuestas en una proposición. Sus fórmulas, condiciones
y argumentos permanecen explícitos.

## Precisiones algebraicas incorporadas

Los conceptos son preexistentes; las siguientes precisiones tienen estatuto
FORMALIZACION_NUEVA:

- Desarrollo del diferencial radial del horizonte cosmológico:
  T_cos dS_H=2 dE_Lambda y S_H dT_cos=−dE_Lambda, con constantes fijas.
  Se deriva de sus tres fórmulas; no se sustituye por una primera ley
  termodinámica sin especificar trabajo.
- Inversa exterior, monotonicidad para recuperar r, diferenciales y jacobiano
  c r exp(r/R)/(2 R^3). Se desarrollan las componentes de Einstein que se
  anulan para f=1−R/r.
- Tipado de la unitaria mediante medida imagen y prueba de positividad completa,
  transporte de esperanzas y cálculo funcional. La medida simétrica permite
  realizar unitariamente el intercambio de hojas.
- En refinamiento, la conservación de coordenadas geométricas y la misma
  isometría de registros justifican la igualdad de las composiciones.

## Condiciones y separación de lectores

- Delta real finito para fidelidad. La ley modular fija Delta0, gamma_BI,
  a0 y ell_P; la respuesta de familia varía Delta.
- Rama positiva y pareja térmica ya determinada en su carta. La igualdad de
  la pareja no selecciona por sí sola una nueva escala térmica.
- Registro binario, 36 enlaces sectoriales, corte de 81 enlaces y horizonte
  conservan dominios, estados y mapas de realización distintos.
- T_cos=hbar c/(2 pi k_B R) pertenece a la realización cosmológica. No se
  asigna automáticamente a la carta Schwarzschild–Kruskal.
- En Kruskal, x identifica el estado publicado; R(x), c y G son constantes
  de la carta mientras t,r varían. Una variación espacio-temporal de esos
  parámetros tiene sus términos de derivación propios.
- G*hbar fijo conserva ell_P si también se mantiene c; a radio fijo conserva
  la entropía adimensional del horizonte.
- La conservación de entrelazamiento transporta la bipartición o su álgebra.
  Se mantienen entropías finitas y el soporte del estado modular.
- Reversibilidad lógica del registro y disipación física conservan alcances
  diferentes.

## Dependencias internas acordadas con el editor

El editor reunirá los antecedentes completos con estas etiquetas:

1. vii:sec:canales-angulares: A_rad, C*_rad y q±=exp(−A_rad∓C*_rad),
   con su generación anterior.
2. vii:sec:area-sectorial: incidencia 18+18, ocupaciones, significado de
   90/120, gamma_BI, a0 y escala areal angular.
3. vii:sec:unidad-accion-area: h, hbar, G, c, ell_P, t_P,
   T108=2πt_P, cartas y genealogía.
4. vii:sec:transduccion-termica: Boltzmann, temperatura de reloj,
   sección térmica común y E_P=k_B Theta_clk log3=hbar/t_P.

La remisión vii:sec:retorno-memoria-gravedad ya reside en
manuscrito/29_retorno_y_memoria_traslacional.tex.
Las demás referencias del fragmento son internas a él.

## Verificación efectuada

Lectura completa y huellas de los propietarios; revisión algebraica de las
pruebas; control estático de etiquetas, referencias y emparejamiento de
entornos. No se compiló PDF ni se ejecutó campaña numérica adicional.
Los controles sectoriales anteriores son antecedentes focales, no una
certificación universal de VII.
