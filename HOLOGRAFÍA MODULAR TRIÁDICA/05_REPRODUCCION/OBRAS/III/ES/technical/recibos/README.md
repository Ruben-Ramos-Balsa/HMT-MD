# Recibos causales focales del artículo III

Este paquete vincula la fuente común de I/II y las secciones 03–08 con sus
operaciones, dominios, condiciones, coeficientes, datos conservados y
falsadores. No certifica autonomía matemática global, identificación física
independiente en SI, igualdad de las dos vías de alfa ni 120 cifras rigurosas.

## Reproducción

Desde cualquier directorio:

```sh
python3 -I -S technical/recibos/verificar_recibos_iii.py --build
python3 -I -S technical/recibos/verificar_recibos_iii.py --check
```

Las rutas relativas anteriores se ejecutan desde la raíz del artículo III.
`--build` escribe exclusivamente en esta carpeta. `--check` no renueva
huellas: señala cualquier cambio posterior de fuentes o datos. Ningún modo
compila, modifica capítulos, ejecuta el productor primario ni recalcula la
tabla numérica. La generación de recibos y compendios es mecánica; sus
descripciones semánticas están declaradas explícitamente en el script.

## Alcance de los controles

- El compendio incorpora íntegramente las fuentes encontradas por los
  `input` literales de ambas envolturas, las secciones 03–08 y el apéndice 11.
  Vincula también el main existente y el registro del certificado finito. No es
  un preprocesador TeX general ni acredita su inclusión material en un PDF.
- Cada fuente lleva ruta, SHA256, líneas y etiquetas; las aristas de input
  quedan en el manifiesto. Las líneas del compendio conservan el texto
  literal, sin sustituir las negaciones o condiciones para pasar el detector.
- Siete recibos 1.1 usan el auditor oficial de constantes: fuente común y
  resultados 03, 04, 05, 06, 07, 08. Verifican orden causal y esquema, no las
  demostraciones matemáticas que citan.
- El recibo v4 hereda el fundamento del recibo vigente de I. El enunciado
  se coteja con `CORE_HMT.json.canonical_chain`; sus evidencias conservan
  IDs, propietarios y huellas. No se inventan evidencias para rellenar la
  plantilla y no se declara una nueva demostración del fundamento.
- Los mapas posteriores son lecturas en dominios especificados. El carácter
  de la cubierta, la representación de hojas, el lector de profundidad y
  las secciones dimensionales siguen siendo estructuras de partida donde
  así las declaran las fuentes. El ensamblaje documental no es un mapa
  generador adicional ni una prueba por empaquetado.
- Los resultados del evaluador ya existente se comprueban como registro de
  evaluación posterior. K sigue siendo una salida heredada y los archivos
  regionales conservan sus huellas. No se presenta este script como su productor.

El fichero `RESULTADOS_PUERTAS.json` conserva salida y código de retorno de
cada puerta. Un error no se transforma en PASS mediante una dispensa local.
Las reservas heredadas sobre productores y lectores, y las propias sobre
representación y SI, permanecen explícitas incluso cuando las puertas pasan.

El primer ensayo de la puerta v4 señaló como `PLACEHOLDER` la palabra
española «todos», por contener la secuencia `TODO`. Se reformuló únicamente
esa oración del recibo, manteniendo expresamente que el evaluador no ejecuta
la genealogía primaria completa. No se cambió ninguna fuente ni reserva.

Procedencia del control: `CERTIFICADO_NUEVO` de vinculación documental. Las
construcciones y relaciones son `RESULTADO_RECUPERADO`; esta clasificación
no reclama novedad de los conceptos ni modifica el estatuto de sus pruebas.

## Estado de la flecha regional L0/L1

El apéndice 11 distingue dos resultados: el catálogo se produce mediante la
recurrencia explícita de cursores; L0/L1 se reconstruyen de forma única a
partir de las matrices X0/Y0/X1/Y1 declaradas. Esta segunda demostración
no es, por sí misma, una generación anterior de esas cuatro matrices.

La comprobación documental focal encontró en el propietario U008
`U008_orbitas_elevacion_r36.tex:193–268` las matrices L0/L1, la recurrencia
de bloques y su verificación. El propietario
`06e_certificado_generacion_monodromica_rev7.tex:60–97` declara la composición
`Pi6 ∘ (U_(9j+9)…U_(9j+1))` y reproduce las cuatro matrices;
`:99–124` prueba la reconstrucción. Son las copias literales del paquete
`technical/reproducibilidad/originales/PROPIETARIOS_NUCLEO/`.

En esta comprobación acotada no se ha identificado un desarrollo adicional
de la acción coordenada primaria que pueda incorporarse como sustituto de
esa dependencia. Esto no es una conclusión de ausencia matemática en el
corpus. Los recibos conservan la dependencia y no acreditan autonomía de
ese productor por la sola presencia de matrices, copia o inversión.
