# Supervivencia, registros y evolución residual

Este desarrollo conserva la cadena APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo como la arquitectura del manuscrito.
El objetivo local es enlazar sus pruebas de supervivencia con los lectores y
la evolución residual ya formalizados. No sustituye el estado enriquecido
completo por su coordenada real ni redefine retrospectivamente su dinámica.

## Cadena comprobada

1. `SurvivalCylinderSelection.lean`: el solapamiento, definido por las dos
   desigualdades enteras del cilindro, con todos los prefijos decimales
   producidos selecciona exactamente un prefijo ternario. Un candidato
   diferente resulta rechazado a alguna profundidad finita.
2. `CofinalCylinderSurvival.lean`: basta comprobar profundidades cofinales;
   no se exige que se visiten consecutivamente ni en orden creciente.
3. `SurvivingTransitionHistory.lean`: una historia se construye mediante
   `N_(n+1) = 729 N_n + u_n`. La supervivencia de sus prefijos fuerza una
   única historia de bloques. De ella se obtienen los mismos registros,
   las elevaciones `L0,L1` y la firma regional previamente comprobados.
   La igualdad a esos bloques o registros no es premisa de supervivencia.
4. `RegionalResidualDynamics.lean`: la recurrencia del propietario 06e
   lee el residuo actual: `d = floor(729 epsilon)`,
   `epsilon' = 729 epsilon - d`, `N' = 729 N + d`. Se prueban el balance,
   las iteraciones y la unicidad de la historia desde su estado inicial.
5. `RegionalResidualCylinderBridge.lean`: la trayectoria residual desde
   la coordenada real a profundidad seis produce prefijos compatibles con
   todos los prefijos decimales regionales; la compatibilidad es conclusión.
6. `ResidualSurvivalSelection.lean`: compone los pasos anteriores. El
   prefijo producido es el único superviviente; sus hijos satisfacen el
   criterio de admisibilidad y alimentan la misma firma y los mismos cilindros.

Los caracteres regionales se reciben del productor interno anterior.
Ningún constructor de este desarrollo recibe los bloques publicados como
objetivos, ni valores metrológicos. La matemática de Lean y Mathlib actúa
como lenguaje de prueba y reconocimiento posterior.

## Ejecución y resultado

Se requiere Python 3, Lean 4.21.0 y la base autenticada de 251 módulos
`../PAQUETE_ARTICULO_I_INTEGRACION_ESTADO_CAMPOS_20260919`.

```sh
python3 -I -S verify_survival_chain.py
```

El verificador autentica las fuentes y objetos de la base, conserva copias
exactas de los dos módulos del revisor, recompila los seis módulos en orden
y examina las 48 consultas de axiomas. El resultado se conserva en
`survival_chain_build/VERIFICATION.json`. Se admiten únicamente `propext`,
`Classical.choice` y `Quot.sound`; no se admiten `sorryAx` ni axiomas locales.
El paquete anterior permanece intacto.

## Punto de enlace que este desarrollo no sustituye

El primer artículo, `generacion.tex`, presenta las cinco palabras regionales
como lecturas de nueve actualizaciones consecutivas sobre el estado completo.
El integral 06e imprime esa composición y sus registros. La reconstrucción
de las matrices a partir de los registros y la selección por supervivencia
están ahora conectadas, pero no se afirma que una proyección escalar por sí
sola pruebe la acción de cada componente del operador enriquecido histórico.

La recurrencia residual de 06e se declara después de `R36`. No se la ha
renombrado como productor anterior de las matrices. Tampoco se identifica
el reloj de capacidad del bloque ternario con el momento en que queda
determinado un prefijo decimal concreto. La instancia pre-R36 debe conservar
el calendario y las acciones de las fibras fijadas en las fuentes; no puede
obtenerse copiando las tablas objetivo en la definición de la actualización.

Este límite se refiere al enlace entre implementaciones. No altera el texto
de los PDF ni declara inexistente una construcción en todo el corpus.

## Procedencia

La arquitectura y la supervivencia pertenecen al corpus autoral. Estas
pruebas Lean son un certificado nuevo de ese criterio y de su composición.
Fuentes leídas: integral 06e (generación monodrómica), capítulo 20
(arquitectura operatoria: cilindros y supervivencia), U006F (componentes
tipados de actualización), y los capítulos `generacion.tex` y
`tpk_desarrollo_integrado.tex` del primer artículo activo. Los dos módulos
residuales proceden de la tarea «Revisar tesis HMT desde cero» y sus huellas
se autentican antes de la incorporación.

Un falsador concreto es una historia con un bloque diferente: el teorema
`different_block_has_finite_rejection` demuestra que algún prefijo suyo
falla una desigualdad de compatibilidad a profundidad finita.
