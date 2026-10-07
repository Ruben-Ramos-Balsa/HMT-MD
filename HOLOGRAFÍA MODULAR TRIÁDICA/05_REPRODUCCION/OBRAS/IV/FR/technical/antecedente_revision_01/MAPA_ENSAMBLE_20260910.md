# Dependencias materiales del Artículo IV: integración REV02

Actualización de la sucesora: el bloque acción–par angular–elipse–radio de la
sección 3 está incorporado en `iv_accion_antecedente.tex`,
`iv_angulos_antecedente.tex` e `iv_elipse_radio.tex`, y se especializa en
`02_dualidad_t.tex` y `03_pantallas_coordinadas.tex`. Su incorporación y las
fusiones están registradas en `MAPA_DE_FUSIONES_REV02.md`. La redacción
condicional del informe original que sigue conserva el diagnóstico anterior
a esta incorporación; no declara pendiente ese bloque en REV02. El original
permanece intacto en la entrega de IV REV01.

Revisión focal del 10 de septiembre de 2026. Se han releído íntegramente los
cuatro cuerpos de IV y los seis propietarios conservados en `antecedentes/`.
Se han contrastado además los cuerpos pertinentes de I (revisión de helicidad,
127 páginas) y II (revisión 08, 196 páginas). El documento registra la clausura
focal; no sustituye el control del núcleo común ni declara cerrado el nuevo PDF.

## 1. Fuentes de las que tomar las incorporaciones

**I:**
`/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/`

**II:**
`/Users/ruben/Documents/New project/output/ARTICULO_II_REV08_ENTREGA_20260909/manuscrito/`

**IV:** esta carpeta. Las rutas relativas de las dos tablas siguientes se
interpretan respecto de I o II, respectivamente. Los seis propietarios del
integral de 2.249 páginas y sus huellas constan en `REGISTRO_PROCEDENCIA.json`.

## 2. Dependencias de I: del registro al retículo y a Moonshine

| Incorporación material | Archivos y localizadores de I | Consumo en IV |
|---|---|---|
| APP–TRIT–TPK y estructura conjunta del continuo | Fuente común que el editor concilie, partiendo de `sections/nucleo.tex` y `sections/extension.tex` con sus inclusiones; etiquetas `sec:nucleo`, `sec:extension`, `eq:residuo-cociente`, `eq:app-levantada`, `eq:algebras-trit`, `eq:actualizacion`, `eq:semillas`, `eq:emisor-seis`, `eq:holonomia-memoria` | Las cuatro secciones. Define estados, fase, rutas, residuos/cocientes, frontera, memoria y prolongación antes de representarlos linealmente. |
| Regiones y realizaciones de π, φ, e; estructura de i | `sections/generacion.tex` con las inclusiones pertinentes y el sector elíptico TRIT; `eq:palabras-regionales`, `eq:lector-pi`, `eq:propagacion`, `eq:fav`, `eq:cilindro`, `gen:prefijos-regionales` | Weyl usa π e i como representación posterior; el carácter de A5 usa el cuerpo cuadrático ya reconocido; la bandera usa las palabras regionales. |
| Registro de doce ventanas y reconstrucción de K | `sections/registro_k.tex`, incluidas `revision_k.tex` y `k_reversibilidad.tex`; `subsec:k-registro-integral`, `subsec:k-terminal`, `eq:k-lector-firmado`, `eq:k-sumas-armonicas`, `eq:k-bloques-firmados`, `eq:k-u-firmado`, `lem:k-hadamard`, `prop:k-sello`, `eq:k-vector`, `prop:k-transversal` | La dirección de IV no recibe solamente doce enteros: necesita su procedencia, la subred integral, el origen de fase y la orientación. |
| Construcción del código y diseño | `sections/excepcional.tex`, líneas 132–228; `exc:aw`, `exc:codigo`, `exc:codigo-witt`, `exc:enumerador` | `iv:prop:codigo-once` perfora precisamente este código [12,6,6]₃; también sostiene el pegado Niemeier. |
| Selección de la bandera desde K y el registro de α | `sections/excepcional.tex`, líneas 230–336, más `incidencia_registro.tex`, `incidencia_normalizacion.tex`, `incidencia_bandera.tex`; `exc:k`, `exc:bk`, `exc:precarry`, `exc:halpha`, `exc:selector-bandera`, `exc:origen` | Fija o*=1 y la componente distinguida de vα. Debe contener los bloques regionales y la normalización previa al acarreo, no extraer signos de los decimales finales de α. |
| Carta A5/C5, proyector P3 y dirección no nula | `sections/k_direccion_dimensional.tex`, completo; `exc:k-direccion`, `eq:k-proyectores-incidencia`, `lem:k-sector-no-nulo`, `eq:k-vector-direccional`, `eq:k-norma-direccion`, `eq:k-proyector-diez` | Dependencia directa de `iv:eq:p11-uk`, `iv:eq:p10`, `iv:prop:12-11-10`. Las doce clases, el carácter y la norma exacta no se sustituyen por una remisión al integral. |
| Niemeier y vecino de Leech | `sections/excepcional.tex`, líneas 597–757, más `incidencia_reticulo.tex`; `exc:niemeier-def`, `exc:niemeier-teorema`, `exc:vector`, `exc:vecino`, `exc:teorema-leech`, `exc:leech` | Dependencia directa de `iv:eq:26-24` y `iv:thm:pantallas-isomorfas`. Requiere métrica A2, cámara positiva, índice tres, paridad, unimodularidad y exclusión de raíces. |
| FLM, carácter y Monstruo | `sections/excepcional.tex`, desde línea 758; `exc:voa`, `exc:flm`, `exc:moonshine`, `exc:j`, `exc:alcance`, más `incidencia_automorfismos.tex` | Da el codominio excepcional de la realización conjunta y la invariancia modular de J usada en `iv:eq:semiconjugacion-modular`. Requiere cociclo de retículo, levantamiento, módulo torcido y producto de vértice; atribución FLM/Borcherds explícita. |
| Segunda presentación, simetría dual y Fricke | `sections/moonshine_comparacion.tex`, completo; `km:estabilidad-vecino`, `km:traza-tipo`, `km:moonshine-tres`, `km:dual-ciclico`, `km:equivalencia-voa`, `km:Phi23`, `km:fricke-prop`, `km:j-nivel2`, `km:j-nivel3` | Contenido propio del tema Moonshine de IV. La prueba usa el mismo vecino de Leech y verifica estabilidad bajo la isometría de orden tres. Φ23 depende de los isomorfismos elegidos; no es canónico sin esa elección. |

`sections/excepcional.tex` ya incluye las piezas auxiliares anteriores. Su traslado
completo exige además `revision_incidencia_argumento.tex`,
`estrella_pentadica_recuperada.tex`, `figures/estrella_cinco_regiones.tex` y
`pantallas_dualidad.tex`. Esta última pieza contiene resultados que IV desarrolla
otra vez con dominios operatorios explícitos: puede conservarse o reunirse mediante
una intervención editorial autorizada, pero no omitirse inadvertidamente al copiar
el archivo padre. Las etiquetas se mantienen distintas (`exc:` frente a `iv:`).

La prolongación binaria de las cinco regiones y la enumeración de M12 no son
premisas de la perforación ternaria ni de la prueba directa del vecino de Leech.
Si se conserva el corredor íntegro de I, son contenido propio que permanece con sus
pruebas. Si se hace una extracción ulterior, su eventual exclusión debe registrarse
como selección temática, no como supresión de una dependencia reticular.

### El registro de 25 coordenadas no se reduce a su inversión

En `I/sections/registro_k.tex:217–237`, las 25 coordenadas se presentan como salida
del extractor; la reconstrucción explícita posterior comienza en esa salida. II
añade dos cuerpos útiles para el ensamblaje autónomo:

- `II/sections/registro_incidencias.tex`: visitas y trazas → recuentos A,C,V →
  bloques z → (D3z,D4z,Q(z)); etiquetas `eq:registro-bloque-incidencial`,
  `eq:registro-composicion-incidencial`, `prop:registro-36-residuos`.
- `II/sections/registro_imagen_integral.tex`: caracterización de la imagen integral,
  inversión y concordancia con Hadamard; etiquetas `img09:imagen`, `img09:inversa`,
  `img09:triangulo`, `img09:contrato-productor`, `img09:acumulacion`.

Conviene incorporar ambos junto a la extracción, conservando sus condiciones.
El segundo demuestra exactamente la inversión **una vez producidos** los eventos
y sus contribuciones; el primero conserva la regla de recuento y su dominio. La
familia de visitas, su enumeración y la normalización inicial deben viajar con
el productor correspondiente. No se presenta la reversibilidad como una generación
de esos datos a partir del resultado esperado. Esto es una localización del nivel
que demuestra cada cuerpo, no una declaración de ausencia del mecanismo en el corpus.

## 3. Dependencia de II: acción y especialización del radio, incorporada en REV02

Las cuatro secciones actuales de IV no utilizan numéricamente h, ℏ, H5 ni el par
angular. `iv:def:dualidad` fija R0>0 como parámetro del dominio; la identidad
unitaria se demuestra para todos los radios positivos. `Iλ` es un funcional
adimensional de rutas. Polyakov aparece como codominio variacional declarado,
no como consecuencia de una igualdad entre esos dos funcionales.

Por eso, la derivación de Planck de II es una dependencia efectiva **cuando IV
incorpore la escala de acción o determine R0 mediante la elipse**. La incorporación
coherente que evita dejar esa prolongación en un parámetro libre es ésta:

| Resultado que se añada a IV | Cuerpos indispensables de II | Datos y alcance |
|---|---|---|
| Sección de acción ℏ y retorno | `sections/05_accion.tex` completo, con su inclusión `revision_planck.tex`; etiquetas `sec:action`, `eq:el-h4`, `eq:el-lector-determinantal`, `eq:el-decada`, `eq:el-h5`, `eq:el-da`, `eq:el-cpi`, `eq:el-eta`, `eq:el-secciones-accion`, `eq:el-ratio`, `eq:revision-renovacion` | H4 y Smith fijan el cociente de 16 hojas; la norma y φ fijan la década; H5 y la renovación fijan las coordenadas anterior/posterior. La aplicación del lector y el grado de cada coeficiente conservan su definición. |
| Definición estructural y contraste físico de Planck | `sections/definicion_planck_rev06.tex` y `sections/revision_planck_contraste.tex`; `sec:ii-definicion-planck`, `eq:ii-definicion-planck-retorno`, `sec:revision-planck-contraste` | Distinguen ΣH, ℏpre, ℏret, h=2πℏ y la carta de unidades. Si se anuncia reconocimiento físico, conservar también la diferencia calculada con la referencia, no convertir proximidad en identidad exacta. |
| Par angular necesario para la elipse | `sections/05b_coordenadas_angulares.tex`; `eq:ii-par-angular`, `prop:ii-desplazamiento-angular`, `eq:ii-accion-cartas` | A=1000α y C*=2(ηret+α) en la carta declarada; conversión única entre grados y radianes. Las fórmulas posteriores de Barbero no son necesarias para R0 si se hace una extracción por clausura. |
| Forma y radio de la elipse | `sections/07_elipse.tex` y `sections/12_dualidad_t.tex:1–106`; `sec:ellipse`, `eq:ii-t-elipse`, `prop:ii-t-radio`, `eq:ii-t-radio`, `eq:ii-t-recuperacion-angular`, `eq:ii-t-matriz` | Requiere ℏ>0 y |C*/A|<1; obtiene R0=((A−C*)/(A+C*))^(1/4), aSbS=2ℏ, y D(η)=diag(aS²,bS²)/(2ℏ). La forma de radio pierde la escala común; la elipse completa la conserva. |

Una vez incorporado este bloque, se especializa el Hamiltoniano de IV en ese R0.
La identidad `U_T H(R0) U_T^{-1}=H(R0^{-1})` ya demostrada no necesita
reconstrucción. La especialización no determina por sí sola la escala de cuerda
α′ ni el mapa de rutas a configuraciones de Polyakov. Tampoco requiere introducir
las distribuciones Fermi–Dirac/Bose–Einstein, CKM o un catálogo de masas.

La fuente `05_accion.tex` utiliza previamente α y φ generadas y el registro local
H4: estos antecedentes son parte del bloque I trasladado, no entradas metrológicas.
H5 conserva además el selector 169, la matriz central Bc y los recuentos que fija
`revision_planck.tex`. No basta copiar sólo la mantisa de ℏ.

## 4. Revisión matemática de los cuatro cuerpos

No se ha detectado un error algebraico que obligue a modificar sus enunciados.
Se conservaron explícitamente las siguientes precisiones, que el ensamblaje no
debe aplanar:

1. **Hilbert:** la fibra de fase (Z/9)^d no es el estado genealógico completo ni
   F3^(2d) como grupo. La prueba de Weyl necesita el carácter central primitivo.
   Las inclusiones a⊗I y a⊗p tienen trazas diferentes y producen cierres diferentes.
   La prueba de tipo II1 usa expectativas traza-preservantes y densidad L2, no
   solamente una coincidencia de cardinales.
2. **T:** el dominio autoadjunto exige ΣE²|ψ|²<∞. El intercambio permuta exactamente
   esa suma; por tanto transporta el dominio completo, no sólo los vectores de
   soporte finito. En el cambio de sección, la relación (9,−1) se transporta a su
   intercambiada: no se afirma que S preserve L9. El mínimo entero se alcanza en
   suelo/techo de (wR0⁴−9m)/(81+R0⁴), por coercividad de la cuadrática.
3. **Pantallas:** la prueba de G11 deriva distancia ≥5 por perforación; el conteo
   perfecto y un vector de peso 3 fuerzan una palabra de peso exactamente 5.
   P10²=P10 resulta de P11EK=EK=EKP11; la dirección perdida es ℓK. El isomorfismo
   conjunto conserva v11 dentro de su grafo: no identifica V11 con V10. El producto
   incluye un espacio real, un dominio de radios y un retículo; es una equivalencia
   de esas presentaciones coordinadas, no un único espacio vectorial de dimensión 11.
4. **Acción y supercarga:** la aditividad de Iλ depende del dato precedente en la
   primera arista de cada segmento. El teorema de Q²W=HW es de transporte y mantiene
   sus operadores e hipótesis: para ψ∈D(Qhat²), Qhatψ∈D(Qhat), de modo que se puede
   aplicar Q dos veces a Wψ. Afirma la identidad sobre la imagen transportada, no la
   construcción universal de Q ni una equivalencia con todo el codominio físico.

La identificación de las dos álgebras de vértices de órdenes 2 y 3 es posterior a
los teoremas clásicos respectivos. Su transporte conserva el orden de los
automorfismos: nunca transforma por conjugación la involución en un elemento de
orden tres. Fricke, la simetría dual del orbifold y T no comparten dominio.

## 5. Delta aplicado

Sólo se han corregido cuatro erratas de notación o terminología en IV:

- `01_hilbert_nonadico.tex`: «hiperinfinito» → «hiperfinito» y
  «hiperinfinita» → «hiperfinita».
- `03_pantallas_coordinadas.tex`: `RR^{12}` → `\RR^{12}` y
  `mathscr G_K` → `\mathscr G_K`.

Las barras ausentes cambiaban la representación tipográfica del dominio y el
codominio. Las definiciones correctas coinciden literalmente en su contenido con
`antecedentes/pantallas_integral.tex`. No cambian mapas, pruebas, condiciones,
resultados ni arquitectura. I, II, III, propietarios, punteros y manifiestos
globales permanecen intactos. Estatuto: corrección editorial puntual de contenido
recuperado; no resultado nuevo.
