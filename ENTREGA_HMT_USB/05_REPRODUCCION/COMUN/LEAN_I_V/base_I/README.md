# Artículo I: publicaciones regionales y estructura algebraica del electrón

La entrada principal es `lean/ArticleIPrincipalPublication.lean`, declaración
`HMT.I.ArticleIPrincipalPublication.article_I_principal_publication`.
Reúne las pruebas existentes, sin volver a demostrarlas:

1. Publicaciones de las regiones de π, e y φ a cualquier profundidad finita.
2. Producción conjunta de cilindros y firma, y las dos publicaciones correlacionadas de α.
3. Escala de acción, composición electrónica y operador sobre la ruta central.
4. Entrelazamiento del plano electrónico con los proyectores efectivos de APP.
5. Relaciones algebraicas, espín, helicidad, unitariedad y retornos tras 2π y 4π.
6. El mismo origen incidencial y las propiedades reticulares para la aplicación clásica de Leech y FLM.

El punto de partida conservado es APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo → publicaciones aritmética e
incidencial. Los nombres y funciones convencionales aparecen como
reconocimiento posterior de las publicaciones regionales.

Las unidades dimensionales positivas, el refinamiento del operador de masa y
una dirección unitaria de helicidad son parámetros explícitos del teorema,
igual que en las pruebas reutilizadas. No se obtienen de una coincidencia
numérica. La carta analítica de α es correlacionada, no una segunda selección
causalmente independiente. Se conserva el dominio declarado del selector
terminal y su dependencia computacional `Lean.ofReduceBool`.

## Reproducción única

```text
python3 -I -S reproducir_principal.py --report-dir /ruta/nueva/resultados \
  --lean /ruta/lean-4.21.0/bin/lean --mathlib-root /ruta/mathlib4
```

Primero se verifica íntegro el paquete y se recompila su enlace excepcional;
después se compila la entrada principal contra los mismos objetos autenticados.
No se recompilan los 477 módulos antecedentes. Lean 4.21.0, Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`; objetos entregados para macOS arm64.
En otra plataforma deben reconstruirse los antecedentes desde sus fuentes.
Nada se ejecuta automáticamente al conectar un USB.

`APLICACION_CLASICA.md` conserva el paso bibliográfico Leech–FLM–Moonshine.
El alcance no exige volver a demostrar esos teoremas clásicos en Lean, ni
los introduce como axiomas. La compilación acredita los enunciados concretos
de las fuentes, no una certificación automática de cada frase del PDF.

## Conservación

El paquete anterior de enlace excepcional permanece intacto. Esta copia
añade la entrada principal, su reproductor y sus recibos; conserva las fuentes,
datos y pruebas anteriores. El README y manifiesto anteriores quedan en
`historia_entrega/`. Los PDF científicos no se modifican. Las pruebas
clásicas adicionales ya realizadas permanecen como antecedentes y suplementos,
sin convertirse en nuevos requisitos para aplicar los teoremas citados.
