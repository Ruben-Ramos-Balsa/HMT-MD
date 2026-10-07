# Continuación Lean del artículo I: traza graduada del retículo seleccionado

Este README es la entrada vigente. La entrada anterior permanece íntegra en
`versiones_previas/README_VOA_SELLADO.md`; las pruebas previas no se reinician.

## Ejecutar la cadena completa

```sh
python3 -I -S reproducir_traza.py --mathlib /ruta/mathlib4 --lean /ruta/lean
```

Se requieren Python3, Lean4.21.0 y Mathlib en el commit
`308445d7985027f538e281e18df29ca16ede2ba3`. Lean y Mathlib son dependencias
externas declaradas. Todas las fuentes HMT de la clausura están en esta carpeta
y en su ZIP. No se depende de otro directorio privado de HMT.

El ejecutor conserva la clausura anterior y añade la continuación en
`deltas/traza`. Comprueba huellas e imports, compila o reutiliza objetos sólo
si coinciden sus fuentes, compilador y dependencias, y consulta los axiomas
de cada declaración principal registrada. No reconstruye Mathlib.
La compilación no es una revisión humana del manuscrito ni una certificación
de afirmaciones distintas de los enunciados efectivamente comprobados.

## Entrada matemática

`deltas/traza/SelectedFullGradedTrace.lean`

Teorema:
`HMT.I.SelectedFullGradedTrace.shared_action_electron_fields_and_full_trace`.

El recorrido conserva el mismo origen seleccionado y sus condiciones:

`APP → TRIT → TPK → estado enriquecido → publicaciones regionales → registro
seleccionado → incidencia → retículo → álgebra torcida → osciladores → campos
de Heisenberg → piezas de peso finitas → traza graduada`.

No se repiten la inversión de K ni sus lectores. La composición de acción,
electrón e incidencia se importa sin modificar sus dominios e hipótesis.
Las constantes de llegada y los coeficientes de la serie no se suministran
como nuevas entradas de esta continuación.

## Resultado añadido

En cada peso d, la restricción de la involución real del portador
`M(1) ⊗ Cε[Λ]` tiene traza igual al coeficiente d del producto formal
`∏(n≥1) (1+X^n)^(-24)`.

- La base es la del álgebra simétrica y del álgebra reticular ya construidas.
- Las ocupaciones de peso d son finitas por codificación explícita; los modos
  del espacio ambiente no están acotados.
- Las capas de norma del retículo son finitas por cotas de sus coordenadas
  enteras; esa finitud no se recibe como premisa.
- La involución restringida coincide con `carrierTheta`, sobre cada vector.
- La carga cero es la única fija; las otras no contribuyen a la traza.
- El24 procede del rango demostrado del mismo retículo seleccionado.
- Todos los coeficientes y truncamientos son compatibles a profundidad
  arbitraria; no se certifica solamente una lista de coeficientes.

## Alcance preciso y continuación

La graduación probada es frecuencia oscilatoria más la mitad de la norma
cuadrática reticular.
Esta entrega no la identifica todavía con un operador de Virasoro L0 ni
incorpora el desplazamiento conforme q^(-c/24). No llama J a esta serie.
La traza de orden dos aquí comprobada es distinta del índice54 de la acción
de orden tres ya preservada en `APPFockIndex`.

El LaTeX conservado aplica FLM al retículo construido. Esta continuación no
convierte esa cita en un axioma de Lean: los campos exponenciales completos,
el sector torcido, el producto de orbifold y la identificación del grupo
de automorfismos con el Monstruo no son conclusiones de este paquete.
Por ello no se presenta como formalización final de Moonshine.

No se usan `sorry`, `admit` ni axiomas HMT añadidos. El uso heredado de
`Lean.ofReduceBool` en el selector finito sigue registrado; las pruebas nuevas
generales de traza sólo emplean los axiomas estándar de Mathlib.

La ejecución conjunta congelada se conserva en
`recibos/traza/LEAN_CONJUNTO.json`. Las ejecuciones posteriores escriben
`resultados/lean_unificado/VERIFICATION.json`. El manifiesto permite comprobar
la conservación íntegra del predecesor, incluida su entrada histórica.

No se han modificado los PDFs. Las fuentes LaTeX de la traza y de su posterior
reconocimiento modular se guardan como procedencia, no como pruebas Lean.
