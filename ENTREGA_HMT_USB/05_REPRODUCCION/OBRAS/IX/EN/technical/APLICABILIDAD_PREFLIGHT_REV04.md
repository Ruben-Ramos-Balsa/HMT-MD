# Aplicabilidad del control precompilatorio REV04

Este preflight local cierra las entradas materiales del delta analítico y editorial de zeta. Verifica el núcleo común, la apertura y los antecedentes congelados; localiza las fórmulas, la numeración y las dependencias activas; ejecuta nuevamente los controles focales de Schur, memoria y expectativas. Su recibo se vuelve a comprobar antes de cada pasada de LuaLaTeX y al finalizar. Una modificación de una entrada invalida el recibo.

No se emite aquí `PASS_HMT_MD_PRECOMPILE`: ese nombre pertenece exclusivamente al programa canónico v2. El estado local `PASS_PREFLIGHT_ANALITICO_EDITORIAL_LOCAL_REV04` no acredita una realización física, la positividad global de Weil ni RH. La revisión matemática focal tiene su residencia separada en `REVISION_MATEMATICA_FOCAL_REV04.md`.

El patrón editorial canónico de IV muestra una aplicabilidad adicional posible: un claim independiente sobre identidad documental, con conclusión `APPLICATION_IN_PROGRESS` y componentes del tronco declarados exclusivamente como contexto. Esa vía requiere expediente, evidencia y alta registral propios; no se obtiene renombrando este recibo local. El editor de los registros es la tarea designada por el autor, no este programa. Ningún registro global se modifica desde aquí.

La autorización se refiere al encargo editorial actual de incorporar las propuestas recibidas; no se atribuye al autor aprobación de huellas nuevas. La matriz técnica está revisada por el editor principal. La condensación autorizada del resumen conserva las expresiones en sus residencias del cuerpo y las conclusiones, consignadas como `FUSIONAR_SIN_PERDIDA`.

Uso: `python3 technical/preflight_editorial_rev04.py --inspect` no escribe. Tras congelar fuentes: `python3 technical/preflight_editorial_rev04.py --freeze technical/preflight_rev04/runs/CORTE --confirm-freeze REV04_SOURCES_FROZEN --python /usr/bin/python3`. Consumo: `python3 technical/preflight_editorial_rev04.py --check RUTA_DEL_RECIBO`. El compilador debe abortar si el último comando no devuelve cero. El runtime de Schur requiere `mpmath==1.3.0`; los otros dos verificadores se ejecutan con biblioteca estándar aislada. Se ejecutan los tres también bajo `-O`.

Los archivos de sistema de TeX y las fuentes tipográficas no son entradas científicas del manuscrito; se enumeran los paquetes demandados pero este control local no sella la instalación completa de TeX. No se ha compilado desde este verificador.
