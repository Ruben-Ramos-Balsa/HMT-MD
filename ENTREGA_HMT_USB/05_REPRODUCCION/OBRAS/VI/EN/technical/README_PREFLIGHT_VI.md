# Preflight editorial propio del Artículo VI

**Actualización material del 10 de septiembre:** se ha producido una edición
completa de lectura mediante `compilar_lectura_vi.py`. Su resumen declara la
dependencia anterior a K no integrada. Esa compilación no cambia las condiciones
ni los resultados de este preflight y no emite un certificado de autonomía.
El manifiesto del ZIP de lectura comprueba archivos, no reemplaza este expediente.

Este expediente acompaña una fuente de trabajo en preparación. No compila el
artículo ni certifica su autonomía matemática, sus resultados físicos o la
ejecución de todos los productores del corpus. Tampoco hereda un PASS de los
artículos I–V. El nombre técnico del directorio y del PDF no fija el título.

## Autorización y alcance

`AUTORIZACION_AUTORAL_LITERAL_VI.json` conserva íntegro el mensaje autoral del
10 de septiembre de 2026, incluido «meteorológica». La redacción académica
empleará «metrológica». El registro identifica una autorización editorial,
no una validación científica, y conserva la prohibición de titular el artículo
«Ley general de masas».

`CONFIGURACION_PREFLIGHT_VI.json` declara las rutas propias de VI y el alcance
documental. El integral de 2.249 páginas y la monografía de masas REV.2 son
antecedentes documentales: no son una edición previa de VI ni una enumeración
completa de todas sus dependencias.

El adaptador y sus dos auxiliares son copias locales específicas de VI. No
modifican los preflights de I–V, las skills, los gates canónicos ni sus
manifiestos. La discrepancia histórica del arranque por el índice documental
se mantiene explícita; este expediente no la transforma en un PASS de arranque.

## Bloqueo material vigente

`DEPENDENCIAS_PRECOMPILACION_VI.json` conserva el estado de dependencias aún
no reunidas. Mientras tenga ese estado, dependencias abiertas o residencias
no verificables, los modos `prepare`, `verify`, `registration-patch`,
`bind-contract` y `run` se bloquean. Una nota pendiente no sustituye las
definiciones o pruebas que se necesitan incorporar.

Sólo después de reunir materialmente esos cuerpos, el editor podrá completar
`placements` con `dependency_id`, `path`, `sha256` y `locator` reales para
cada residencia; revisar el conjunto; vaciar `open_dependencies`; marcar
`reviewed_by_editor: true`; y fijar el estado
`DEPENDENCIAS_DOCUMENTALES_REUNIDAS`. No basta cambiar los indicadores: el
adaptador coteja los archivos y las huellas. El comprobador documental vuelve
a verificar las mismas residencias contra el inventario certificado.

Ese cotejo acredita identidad y presencia documental. No demuestra por sí
solo que la lista de dependencias declarada sea científicamente completa.

## Orden de ejecución

Desde la raíz de este Artículo VI, consultar el estado actual sin generar
huellas del manuscrito:

```sh
python3 -I -S -B technical/preflight_vi.py status
```

Cuando las fuentes y sus dependencias efectivas estén reunidas y revisadas:

```sh
python3 -I -S -B technical/preflight_vi.py prepare
python3 -I -S -B technical/preflight_vi.py verify
python3 -I -S -B technical/preflight_vi.py registration-patch
```

`prepare` congela un corte documental local, sus fuentes y sus antecedentes;
`verify` ejecuta los comprobadores sobre ese corte. `registration-patch`
produce únicamente una propuesta de alta para revisión del editor. No aplica
el parche a `claims.json`, `evidence.json`, `events.jsonl` ni
`causal_graph.json`. Se cotejan sus huellas antes y después de preparar esa
propuesta para detectar cambios concurrentes.

Sólo tras revisión y aplicación expresamente autorizada de la propuesta:

```sh
python3 -I -S -B technical/preflight_vi.py run
```

`run` exige el alta real y ejecuta el preflight canónico sin alterar sus
reglas. Un fallo se conserva como fallo. No se compila desde este adaptador.

## Registros y resultados

Los registros locales se escriben bajo `technical/preflight_vi_20260910/`.
`ESTADO_ULTIMO_INTENTO.json` distingue preparación, comprobación y fallo.
La prueba negativa inicial de `prepare` debe terminar con
`DEPENDENCIAS_NO_REUNIDAS`: comprueba que el bloqueo funciona y no significa
un fallo matemático del manuscrito.

No se generará un certificado de corte ni un manifiesto final de entrega
mientras las fuentes sigan en preparación. La cadena científica permanece
APP → TRIT → TPK → estado enriquecido → estructura discreta conjunta del
continuo → salida HMT–MD → reconocimiento convencional posterior. Este
control editorial preserva sus residencias declaradas; no sustituye las
pruebas ni las puertas genealógicas y científicas correspondientes.
