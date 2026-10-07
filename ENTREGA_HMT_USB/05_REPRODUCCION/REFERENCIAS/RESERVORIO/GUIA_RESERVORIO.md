# Reservorio de desarrollos y coordinación HMT–MD

Guía de lectura de la unidad independiente `03_RESERVORIO`.

## Qué contiene

`ARCHIVOS` conserva íntegra la carpeta `COORDINACION_20260906`: 136 archivos, incluida la [traza generativa coordinada](ARCHIVOS/TRAZA_GENERATIVA_COORDINADA.md), notas de desarrollo, mapas estructurales, programas y recibos. El nombre de coordinación no describe por sí solo todo su contenido: además del reparto histórico de trabajo hay desarrollos matemáticos escritos en la traza y en las notas de `LEY9`, `MASAS`, `ACLARAR` y `OVERLEAF`.

La carpeta mantiene la redacción, las fechas y los estados de trabajo originales. Una mención histórica a un pendiente, una versión o un control no se convierte por esta copia en un juicio sobre las publicaciones posteriores. Los recibos se preservan como recibos; el acto de integrarlos no constituye una nueva comprobación matemática.

## Cómo leerlo sin el árbol privado de origen

1. Comenzar por [TRAZA_GENERATIVA_COORDINADA.md](ARCHIVOS/TRAZA_GENERATIVA_COORDINADA.md), cuyo orden enlaza las ramas y sus propietarios.
2. Abrir las notas citadas desde el [índice de equivalencias](INDICE_EQUIVALENCIAS.md): su primera sección ofrece enlaces relativos a los 136 archivos internos. No hace falta traducir manualmente sus rutas privadas antiguas.
3. Usar la segunda sección del mismo índice para los 187 propietarios y datos externos seleccionados. Cada entrada conserva la ruta original como identificador de procedencia y proporciona un enlace relativo a la copia situada dentro de este reservorio. Buscar el nombre o la ruta citados conduce al enlace local; no es necesario que exista `/Users/ruben` en el ordenador del lector.

`DEPENDENCIAS/CORPUS_2249` reúne los propietarios directos seleccionados del integral; `DEPENDENCIAS/OTROS` reúne las fuentes concretas restantes, sin copiar sus árboles completos. Las correspondencias de identidad con el corpus integral que también acompaña la entrega constan en `PLAN_INCLUSION_RESERVORIO.json`. Se comparan bytes mediante SHA-256, no sólo títulos ni nombres de archivo. La duplicación limitada permite consultar esos propietarios sin salir de `03_RESERVORIO`.

La selección propuesta añade 187 archivos, 4.330.629 bytes: 167 tienen una copia idéntica en el ZIP del corpus principal y 20 se recuperan de las ubicaciones concretas referidas. Entre estos últimos se encuentran fuentes nucleares del continuo, piezas del desarrollo electrónico, tres archivos de procedencia CKM, la arquitectura narrativa y las cinco notas del doble círculo enlazadas por su entrada. No se incorporan indiscriminadamente todos los informes, índices de versiones, PDF históricos ni directorios mencionados.

## Programas conservados y alcance de esta integración

Los programas se copian sin alterarlos. Se preservan además los tres archivos de datos que varios programas locales abren en la carpeta superior: `VALORES_RECALCULADOS_CORPUS.json`, `VALORES_ESPECTRALES_RECALCULADOS.json` y `RECOMPROBACION_CONSTANTES/REPLAY_RESULTADOS.json`; también se recogen las tablas y auxiliares concretos identificados en sus lecturas. Su presencia no significa que se hayan recalculado.

Esta integración proporciona las lecturas y sus equivalencias, no promete que todo programa histórico se ejecute sin adaptación: algunos conservan rutas absolutas o presuponen la disposición privada anterior. El mapa `LEY9/ARBOL_ESTRUCTURAL_NUCLEO.json` cuenta con un verificador que admite `--package-root`; otros programas requerirían un adaptador explícito. `mpmath` es una dependencia de entorno de determinados controles. No se han ejecutado campañas ni reconstrucciones para preparar este plan.

Tampoco se presenta el subconjunto de propietarios como un nuevo manuscrito LaTeX compilable ni como el cierre transitivo de toda cita del corpus. Se conserva la fuente precisa requerida por la lectura focal, con su identidad y su alcance; los tratados completos se entregan en su unidad propia.

## Integridad y límites documentales

El plan enumera cada origen, destino relativo, tamaño, SHA-256, motivo de incorporación y, cuando existe, miembro idéntico del ZIP principal. Sus referencias no seleccionadas se conservan como inventario: «no seleccionado» no significa «inexistente» ni «desarrollo ausente». Los vínculos históricos no se reescriben dentro de los originales; el índice de equivalencias es la capa de acceso portátil.

El plan de procedencia se conserva en `PROCEDENCIA/PLAN_INCLUSION_RESERVORIO.json`. El inventario efectivo de esta copia y sus hashes se encuentran en `MANIFEST.json`; su comprobación está indicada en `LEER_PRIMERO.md`.
