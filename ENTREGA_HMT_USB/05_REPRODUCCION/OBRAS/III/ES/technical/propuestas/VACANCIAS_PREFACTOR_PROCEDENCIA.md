# Polarización discreta y modo trítico: procedencia de la ampliación

## Alcance y residencia

Fragmento: `vacancias_prefactor.tex`, preparado para la sucesora REV02 de III,
antes de «Retorno de hoja, incidencia areal–volumétrica y orientación constitutiva».
No se ha incluido en `main.tex`, no se ha compilado y no se ha alterado el núcleo
común, I, II, ni un PDF. No contiene una derivación nueva de la masa electrónica.
El editor integra el fragmento después de revisar estas dependencias.

El desarrollo recupera dos resultados del integral y amplía su explicación:
la polarización centrada con su balance temporal; el modo TRIT y la norma de
incompatibilidad entre las proyecciones aritméticas. Las figuras anteriores
permanecen intactas. No se añade una figura porque las dos construcciones se
comprenden directamente mediante sus mapas, la matriz y las pruebas.

## Fuentes materiales leídas

Base integral absoluta:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente`

1. `manuscrito/sections/md/06l_vacancias_corriente_rev11.tex`, íntegro:
   δ y leyes de vacancias; líneas 106–136, P_N y J_N, ecuaciones 58.19–58.20
   en p. 1055 impresa del integral2249, página física1056.
2. `manuscrito/sucesor_102/espirales/cap58_electron_lector_helicoidal.tex`,
   íntegro; líneas20–42, modo trítico común, s=1/2, 3/4=90/120 y √3/4;
   §58.5.2, p.1056 impresa, física1057.
3. Propietario del desarrollo completo del prefactor en I117:
   `/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_MEMORIA_Y_COHERENCIA_EDITORIAL_20260909/sections/electron.tex`,
   líneas163–264, definición de proyecciones, matriz conjunta, espectro y norma.
   La prueba ya figura en I117, pp.83–84. Su reproducción es necesaria aquí
   porque III no contiene el capítulo electrónico de I.
4. En III140, `base_articulo_I/sections/vacancias_capacidad.tex` y
   `base_articulo_I/sections/revision_monodromia.tex` conservan la codificación
   inferior y su memoria; `base_articulo_I/sections/primos_retornos.tex:141–191`
   contiene la discrepancia acotada en su aplicación de Dirichlet, p.58 impresa.
5. En III140, `manuscrito/sections/04_respuesta_constitutiva.tex:14–48`
   define V=(I−T^90)(I−T^120)^−1, r_± y f(s); §16 pp.116–118 impresas.

## Resultados, alcance y genealogía

| Bloque | Procedencia | Construcción conservada | Alcance de la incorporación |
|---|---|---|---|
| Polarización P_N e incremento J_N | RESULTADO_RECUPERADO | Cardinales729/1000 del refinamiento, δ, codificación de fase, suma centrada y memoria | Prueba completa de telescopía, cota estricta en toda ventana y densidad |
| Convenciones superior/inferior | Formalización auxiliar de compatibilidad editorial; no se declara novedad conceptual | Origen de fase y convención de extremos | El término de frontera transporta una convención a otra; no se modifica el núcleo I |
| Realización en carga y tiempo | INTERFAZ_FISICA con datos explícitos | Salida escalar previa, sección u_Q y tiempos t_N crecientes | Balance dimensional exacto; no selecciona una unidad física ni una configuración espacial |
| Acoplamiento por iota, V, ell | Especificación de la composición lineal, no identificación HMT ya deducida | Dominio/codominio de excitación y observación | Si los mapas son fijos y lineales, transportan el balance; el fragmento no los elige por una corriente objetivo |
| Modo trítico y prefactor | RESULTADO_RECUPERADO | APP tridimensional→Σ/Π→censo→proyecciones; selector M_ph=(1,−1,0)^3 | Espectro completo, s=1/2 y norma √3/4, sin dato de masa |
| Defecto3/4 y sectores90/120 | RESULTADO_RECUPERADO y exposición conjunta | Defecto del plano APP; longitudes de los sectores del TPK; respuesta posterior contractiva | Igualdad del defecto con el límite de r(q), no equivalencia de operadores |

APP aporta los alfabetos, las dos hojas, sus cocientes y la multiplicidad de
fibras. TRIT aporta el modo firmado canónico, que se conserva como vector y no
solamente como valor singular. TPK aporta el refinamiento, la fase y la historia
de capacidad/vacancias, así como los sectores90/120 de las respuestas posteriores.
Las evaluaciones de constantes o de masas no seleccionan ninguno de esos datos.
La norma aislada no reconstruye los proyectores; el estado con memoria y la
representación de fibras los conservan. Los coeficientes de 1/4 y3/16 se
obtienen del censo, no de una ecuación electrónica objetivo.

El fragmento no demuestra una identificación espacial con Maxwell. Define
Q_N=P_Nu_Q e I_N=(Q_(N+1)−Q_N)/Δt_N y enumera los datos de la composición
constitutiva. Tampoco identifica la respuesta r(q)>3/4 en 0<q<1 con el
defecto constante3/4: su igualdad ocurre en el límite q→1. El retorno de fase
conserva la memoria acumulada; no se modifica la distinción entre reloj e historia.

## Pruebas focales

Ejecutar desde cualquier directorio:

```sh
python3 -I -S verificar_vacancias_prefactor.py
```

El programa enumera los 729 triples de APP, calcula la matriz N y M con
aritmética racional exacta, verifica nueve autovectores independientes y la
norma al cuadrado 3/16. Comprueba asimismo la compatibilidad de techo/suelo,
las identidades telescópicas y la cota en 4.000 casos racionales, así como
la factorización de la respuesta en 130 puntos racionales. Las comprobaciones
son controles focales posteriores a la construcción; las demostraciones
universales y los límites están escritos en el TeX. Ningún `assert` puede
desactivarse: todos los controles utilizan `ensure` y lanzan excepción.

Este programa no certifica el PDF completo, la masa, una identidad física,
la compatibilidad de las dos vías de alfa ni la novedad histórica. La
compilación y la revisión visual corresponden al editor integrador.

Resultados ejecutados en esta entrega: `PASS_VACANCIAS_PREFACTOR_FOCAL`,
tanto con ejecución ordinaria como con `-O`; `PASS_TEX_FRAGMENT_STRUCTURE`
para los entornos y referencias internas; y
`PASS_HMT_GENERATED_CONSTANTS_OUTPUT_ONLY` al auditar el fragmento junto con
`RECIBO_CONSTANTES_VACANCIAS_PREFACTOR.json`. Este último controla el orden
causal focal; no sustituye el recibo genealógico integrado del artículo,
la compilación o su revisión visual. Las referencias del fragmento tienen
el prefijo `iii:vp:`; la única referencia externa es `iii:sec:constitutiva`.
