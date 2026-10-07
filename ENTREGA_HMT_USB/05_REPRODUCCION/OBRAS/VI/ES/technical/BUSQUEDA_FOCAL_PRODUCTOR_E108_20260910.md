# Búsqueda focal del productor del registro dodecafásico

Fecha: 2026-09-10. Consulta de propietarios, independiente de las conclusiones de los validadores posteriores. No se ha editado `sections/09_dependencias_anteriores.tex`, ningún manuscrito previo, gate o manifiesto. No se ha ejecutado código que escriba sobre las fuentes históricas.

## 1. Alcance

Se siguieron los propietarios enlazados desde `sections/registro_k.tex` y su nota de procedencia en el Artículo I. La búsqueda se centró en la función

`x_term → R12(x_term) → E108^(90,120)(R12(x_term))`,

con los términos `E108`, `E_{108}`, `R12`, `R_{12}`, `emit_window`, registros90/120 y `nu120`. Se consultaron el árbol de fuentes del integral de2249páginas y su corpus técnico preservado. Las coincidencias nominales no se contaron como implementaciones.

Raíces abreviadas:

- **F:** `output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/`
- **B:** `output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/`
- **I:** `output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/`

Todas las rutas son relativas a `/Users/ruben/Documents/New project`.

## 2. Lo que sí definen los propietarios

### Extracción de las ventanas y conteo de eventos

F/`manuscrito/propietarios_exactos/tpk/U016_registro_dodecafasico_hadamard_k.tex`, líneas27–84, define las doce ventanas, su orientación y el evento

`e_m = Σ_m · #{t∈E_m : d_t∈{2,4,6,8}}`.

La misma fuente define `R12(x)=((E_m,τ_m,σ_m,κ_m,Λ_m))`. Por tanto, **R12 tiene una función precisa de extracción del historial**: conserva la subruta, orientación, firma, memoria y frontera de cada ventana. No se lo confunde con el mero calendario ni se declara que esta proyección falte.

F/`manuscrito/sections/hmt/03g_ciclo_dodecafasico_tpk_rev7.tex`, leído completo (293líneas), expone lo mismo en líneas139–159 y la carta integral de eventos en191–257. Su ecuación `U12^sgn=H12(K)` es una relación reversible entre publicaciones; no se usa como definición del dominio de R12.

La nota completa

`output/AUDITORIA_INTEGRAL_PUBLICABILIDAD_HMT_MD_20260906/COORDINACION_20260906/LEY9/ACTUALIZACION_TPK_ETA_Y_DETERMINANTE.md`

añade una actualización efectiva del conteo:

`z_(m+1)=z_m+a_m^evt e_m`,

`y_(m+1)=S^-1 y_m+a_m^evt S^-1 e_0`.

Su prueba en§1 es directa y conserva los eventos después del retorno de fase. El objeto producido sigue siendo el vector contado de doce eventos, no todas las coordenadas del libro de incidencias de E108.

### Publicación de los canales y transformación armónica

U016, líneas256–326, da la cadena causal y las25coordenadas publicadas. En concreto, líneas283–296 presentan

`E108(R12(x_term))=(b90,b120,Q_TPK)`

con ambas listas y `Q_TPK=6263`. La primera fórmula coordenada completa que sigue es la transformación ΠH, mediante las sumas de órbitas y combinaciones de diferencias.

F/`colaboracion/partes_i_ii/source/base_residencias/base_c10_sin_encabezado.tex`, líneas267–346, conserva esta misma separación: R12 está escrito como extracción del historial; E108 tiene dominio, codominio y sus valores terminales; ΠH tiene acción coordenada explícita. El cuadrado de naturalidad de U016, líneas356–380, conserva prefijos al prolongar; no enumera por sí solo las multiplicidades de las visitas ni la familia de trazas que produce las25coordenadas.

## 3. Resultados de la búsqueda ejecutable

No se encontró una definición de `emit_window` ni una implementación denominada E108/R12 que produzca las25coordenadas, en los archivos `.py/.tex` del árbol focal. La búsqueda adicional en el corpus técnico preservado y en las fuentes reunidas de I tampoco localizó esa función. Esto delimita una recuperación material, no prueba inexistencia en todo el corpus.

El programa real

B/`03_CONTROL_ADMISION/PROPIETARIOS_PAQUETE/EXT_TPK_RUNTIME_PROJECT/16_CIERRE_GLOBAL_HMT_MD_2026-07-22/01_SELECTOR_CONSTANTES/selector_interno_constantes.py`

se leyó completo (428líneas). Es un productor de selección inicial y frontera R36: `lift_chain` en126, `boundary_candidates` en185. Recibe el catálogo visible y las matrices primitivasL0,L1,AW. No produce R12 ni U. Las funciones `reconstruct_hensel`243 y `emit_hensel`252 son inversas sobre una palabra suministrada; su utilización posterior en el mismo archivo muestra dos colas distintas y está rotulada como control de no unicidad desde esas primitivas. No se ha promovido este par codificador/decodificador a productor de E108.

El archivo histórico B/`01_FUENTE_SUCESORA/datos/flujo_hensel_20_bloques.json`, leído íntegro, conserva estados3-ádicos y tríadas. Su propio campo `notes.warning` declara que esos estados codifican las cifras de constantes recibidas como oráculo. Ese archivo **no se incorpora como origen del registro** ni se utiliza para suplir la genealogía de las regiones. Es un testigo histórico de codificación inversa, separado de los productores posteriores que el coordinador está reuniendo.

Las coincidencias de `nu120` en los módulos del atlas de masas designan el funcional

`Σ_C sign(Σ_(m∈C) e_m)`

sobre ciclos de eventos; por ejemplo B/`00_CORPUS_RECTOR_PRESERVADO/08_PROPIETARIOS_MECANICA_DIMENSIONAL/pruebas/python/verificar_atlas_genealogia_masas.py`, líneas321–341. No son por ese nombre la enumeración de trazas reducidas de longitud120 que recibe el compilador incidencial. No se ha trasladado el funcional de un dominio al otro.

## 4. Por qué el conteo elemental no sustituye al libro

De la definición de U016 se sigue `|e_m|≤9` para una sola traza de108ticks; de aquí `|(D3e)_m|≤18`, `|(D4e)_m|≤18` y `|Σe_m|≤108`. Las coordenadas terminales publicadas incluyen, por ejemplo,−684 y `Q=6263`.

Estas desigualdades no contradicen el extractor enriquecido, que puede utilizar otras coordenadas, incidencias y multiplicidades. Sí excluyen identificar sin otra operación el vector elemental de doce eventos con la entrada que, por las solas diferenciasD3,D4y suma, produciría aquellas25coordenadas. La extensión del libro no es un detalle prescindible del tipo del mapa.

## 5. Conclusión limitada

Se recuperan positivamente R12, la producción incremental de sus eventos, la transformaciónΠH y las reconstrucciones posteriores. No se localizó en estos propietarios una regla ejecutable completa que seleccione y enumere el libro canónico orientado usado por E108. El punto exacto por reunir sigue siendo esa selección y sus multiplicidades, no la inversión de Hadamard ni la normalización deα_A.

No se encontró un productor válido que permita eliminar esta distinción de procedencia. Tampoco se fabricó un libro desde U,K o un valor metrológico. La sección09 estable no cambia; la conclusión permite al coordinador mantener el contenido recuperado y el alcance documental real sin anunciar clausura global de la entrega.
