# Cadena vigente G9

Esta carpeta añade los eslabones N68–N70 que faltaban en el paquete anterior
y separa los fundamentos N62/N64 de la cadena rectora.

## Núcleo vigente

- `N68_CILINDRO_INTERVALAR/`: corrige la poda por extremo inferior y usa
  intersección exacta de cilindros.
- `N69_CALENDARIO_TRANSICION/`: fija el calendario mecánico, los stutters y el
  estatuto del axioma de transición.
- `N70_TRANSICION_EXACTA/`: formula la transición de cilindros una vez dado el
  estado.
- `../G9_N57_N71/`: contiene N71.
- `../G9_N72_N75/`: contiene N72, N73 y N74.
- `../G9_MONODROMIA/verificar_g9_monodromia.py`: control rector con índices
  normalizados.

## Fundamentos condicionados

- `N62_FUNDAMENTO_CONDICIONAL/`: identidades algebraicas de la firma desde
  `B4`; sus conteos históricos no prevalecen sobre N68.
- `N64_FUNDAMENTO_CONDICIONAL/`: órbita y unidad Witt-dual; la neutralidad
  general sigue siendo una ley declarada.

## Fuentes originales

`fuentes_originales/` conserva los cinco ZIP sin alterar. Las carpetas
adyacentes son su extracción legible. No hay scripts ejecutables originales
dentro de esos ZIP; contienen CSV, JSON, LaTeX, informes y PDF.
