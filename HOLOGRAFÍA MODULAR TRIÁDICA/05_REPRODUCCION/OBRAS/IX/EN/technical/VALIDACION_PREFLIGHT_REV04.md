# Cierre local y enlace canónico editorial

## Corte vigente tras revisión visual

El corte local `20260911_05` y el expediente canónico `f411edf231992fe8` suceden a los cortes descritos más abajo. Conservan los mismos resultados y las seis fuentes comunes. El delta visual consta de cuatro saltos de página y una actualización del metadato de numeración en procedencia; las fórmulas se mantienen. Los seis controles focales vuelven a pasar. El enunciado y los estados del claim documental coinciden exactamente con el registrado. Las puertas directas y la propuesta de dos evidencias nuevas se conservan en la carpeta de ese corte. Los apartados siguientes documentan el primer cierre, no su vigencia tras ajustes.

## Antecedente del primer cierre local

El corte local 20260911_02 incluye 37 fuentes activas y 71 entradas materiales. Las seis fuentes comunes y la apertura coinciden con REV03. Hay 364 etiquetas, 219 referencias y siete citas bibliográficas, sin destinos ausentes ni duplicaciones. Los 48 resultados con título manual se conservan por tipo, título y orden y se numeran mediante `HMTresultado`; se conservan 47 marcadores de demostración en esos cinco archivos. Son controles documentales, no un censo exhaustivo de todas las demostraciones del manuscrito.

El delta de fórmulas registra una sustitución prospectiva del desplazamiento regular por la representación límite, su entrelazamiento tipado y cuatro fórmulas expuestas del diccionario Mellin–Fourier. La condensación del resumen registra seis expresiones con residencia verificable como `FUSIONAR_SIN_PERDIDA`. El resto de fórmulas expuestas se conserva. La matriz y el recibo incluyen el diff completo de los once archivos TeX modificados.

Schur, memoria y expectativas se ejecutaron nuevamente en modo normal y `-O`: 21, 1046 y 25 controles, respectivamente. El recibo local y las seis salidas están en `preflight_rev04/runs/20260911_02`. La prueba negativa conserva el rechazo real del recibo 01 después de cambiar autorizadamente el compilador, seguido de la aceptación del corte 02. Ninguna ejecución de este control invoca TeX.

La adaptación canónica emplea el patrón editorial de IV, con conclusión `APPLICATION_IN_PROGRESS`. Se han cotejado 19 referencias de contexto a los siete componentes y correlaciones del tronco, todas `CONTEXT_DEPENDENCY`, y una dependencia probatoria del claim exclusivamente documental. No se registran estas referencias como cierre científico de zeta. `preparar_editorial_canonico_rev04.py` escribe sólo en `technical`; no modifica registros y no ejecuta la puerta canónica por sí mismo. `verificar_editorial_canonico_rev04.py` comprueba en lectura el certificado y el canvas.

El expediente y la propuesta de alta están en `canonical_rev04/runs/8c7c1375f9ec7b89`. La propuesta contiene un claim editorial y dos evidencias verificadas materialmente. El editor único de registros debe aplicar el alta y preservar estados existentes. A continuación se ejecuta `python3 -B technical/preparar_editorial_canonico_rev04.py bind-contract` para ligar las huellas actuales de los registros. Sólo el programa canónico `precompile_hmt_md.py` puede emitir `PASS_HMT_MD_PRECOMPILE`; su recibo se produce antes de compilar por el compilador del editor principal.

Un nuevo ajuste visual debe conservar el corte anterior, regenerar el recibo local en otra carpeta y materializar otro corte canónico con su propuesta aditiva; no se sobrescribe un recibo anterior. La vigencia de un recibo se decide por su consumo y sus huellas actuales, no por existir un archivo histórico con PASS.
