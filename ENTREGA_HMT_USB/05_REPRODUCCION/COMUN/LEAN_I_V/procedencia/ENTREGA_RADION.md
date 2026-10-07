# Composición acumulativa de los resultados de II, III y V

Esta entrega reutiliza la selección regional y el dominio de acción del
artículo I. Conserva la genealogía APP → TRIT → TPK → estado enriquecido →
estructura discreta conjunta del continuo. Las coordenadas aritméticas,
angulares y constitutivas son resultados del origen compartido; los teoremas
clásicos intervienen como lenguaje de prueba o reconocimiento posterior.

## Resultados materializados

| Resultado del manuscrito | Composición Lean añadida | Alcance del resultado |
| --- | --- | --- |
| Vacío constitutivo y constantes eléctricas de III | `III/SelectedConstitutivePublication.lean` | Especializa el dominio angular de I, demuestra positividad y unicidad del operador constitutivo, recupera los ángulos y la elipse, conserva la velocidad por refinamiento y obtiene la carga positiva única y las identidades eléctricas sobre la misma acción. |
| Área e información de frontera de II | `II/SectorialAreaInformation.lean` | Construye las 36 aristas orientadas y el estado de los dos sectores de 18 enlaces; demuestra normalización, purificación, reducción diagonal, recuperación de ocupaciones y la relación exacta entre logaritmo del estado, áreas y entropía. |
| Parámetro de Barbero–Immirzi en ese estado | `II/SelectedAreaInformation.lean` | Evalúa el funcional sobre la cámara angular generada, demuestra su positividad y conserva sus recuperaciones constitutivas y por trazas. También construye el factor areal a0 desde el carácter angular y el contraángulo generado. El terminal recibe únicamente el parámetro del estado reducido, sin gamma ni a0 libres. |
| Escala gravitatoria del área | `II/SelectedGravitationalArea.lean` | La combinación de la misma acción, gravedad circular y velocidad constitutiva produce la escala Gℏ/c³ y demuestra su igualdad con el radio al cuadrado. La identidad modular conserva su forma al pasar de las áreas normalizadas a las áreas dimensionales. |
| Portador tensorial de cinco componentes de II | `II_TENSOR/PentadicTensorCarrier.lean` y `II_TENSOR/SelectedPentadicTensor.lean` | Construye el proyector antipodal y el marco tensorial explícito. Sus dos inversas identifican su imagen con matrices simétricas de traza nula. La especialización utiliza la coordenada de autoescala de I, con reconocimiento posterior de su expresión radical. La reducción transversal tiene imagen explícita de dos componentes. |
| Ocupación y radiación de V | `V/SelectedThermalPublication.lean` | Aplica los teoremas existentes a dos polarizaciones ortonormales concretas, acción retornada y velocidad constitutiva; incluye ocupación, sumabilidad, integrabilidad y límite periódico de los tres observables térmicos. |
| Transductor térmico de II en la radiación de V | `V/SelectedBoltzmannRadiation.lean` | Demuestra igualdad de la acción utilizada, conservación del transductor al retorno y unicidad de su valor dentro de la sección térmica declarada. La ocupación y el flujo de Stefan reciben ese mismo transductor, en lugar de un valor de Boltzmann independiente. |

Los resultados de CKM y de la composición acción–gravedad–temperatura se
encuentran en `II_CENTRAL/SelectedCKMPublication.lean` y
`II_CENTRAL/SelectedActionGravityThermal.lean`, desarrollados por el integrador
en esta misma entrega. El segundo ya es una dependencia efectiva de
`SelectedBoltzmannRadiation`, no una remisión editorial.

Los parámetros positivos de unidades de acción, velocidad y reloj, la sección
térmica y la temperatura del estado permanecen declarados con sus tipos.
El parámetro de la distribución de frontera identifica el estado reducido.
Ninguno de ellos se utiliza para seleccionar retrospectivamente el registro.

## Reutilización y separación de las pruebas

La base I permanece intacta en
`../PAQUETE_ARTICULO_I_PUBLICACION_PRINCIPAL_20260922`.
Los objetos clásicos ya formalizados se importan: álgebra matricial, operadores
de ocupación, sumas de Gibbs, límites periódicos y teoremas de radiación.
La aportación de estos módulos consiste en realizar sus hipótesis sobre los
objetos concretos del corpus y demostrar las identidades de composición.
La aplicación bibliográfica de clasificación de Leech y FLM conserva el
estatuto documentado en la entrega de I; no se convierte en una nueva campaña
de formalización de toda esa teoría clásica.

El revisor ha terminado IV: `ArticleIVSelectedScreens.article_IV_selected_screens`
compone la dirección concreta `P3 P11 K`, su norma exacta, el proyector de
imagen diez-dimensional, la pantalla que conserva once dimensiones, el
cociente lorentziano 26→25→24, el radio seleccionado y la dualidad. Los dos
objetos reales de dimensiones diez y once conservan su distinción matemática.
La entrega reside en
`/Users/ruben/Documents/ChatGPT/jueces y controles/ENTREGA_ARTICULO_IV_PANTALLAS_SELECCIONADAS_20260922`.
Su recibo final, consultado, es `PASS_ARTICLE_IV_SELECTED_SCREENS`, situado en
`/Users/ruben/Documents/ChatGPT/jueces y controles/VERIFICACION_ARTICULO_IV_PANTALLAS_20260922/VERIFICATION.json`.
La procedencia de la suma de caracteres A5 mantiene su certificado aritmético
exacto; las identidades de la matriz concreta P3 se comprueban en Lean.

## Los dos censos de selección

El certificado de 7.567.952 combinaciones regionales y el selector de 19.446
registros distintos se conservan como dominios diferentes. El primero mantiene
su certificado computacional y sus fuentes; el segundo conserva su teorema
Lean de unicidad excepcional–temporal. Esta entrega no transforma ambos
censos en una sola sucesión ni sustituye uno por el otro. Reutiliza la salida
seleccionada que el artículo I ya entrega a sus consumidores.

## Comprobaciones reproducibles

Los recibos adjuntos fijan fuente, objeto compilado, versión de Lean y axiomas
de las declaraciones comprobadas. Las composiciones seleccionadas heredan
`Lean.ofReduceBool` allí donde lo emplea la selección antecedente; los nuevos
módulos no añaden axiomas ni pruebas con `sorry`.

- III: `III/VERIFICATION.json`, reproducible con `bash III/reproducir.sh`.
- Área: `II/VERIFICATION.json` y `II/VERIFICATION_SELECTED.json`.
- Escala gravitatoria del área: `II/VERIFICATION_GRAVITATIONAL.json`.
- Tensor: recibos y reproducción en `II_TENSOR/`.
- V: `V/VERIFICATION_COMPACT.json`, reproducible con `python3 -I -S V/verify.py`.
- Composición térmica II–V: `V/VERIFICATION_BOLTZMANN.json`, reproducible con
  `python3 -I -S V/verify_boltzmann.py`.

Los comandos se ejecutan desde este directorio con los antecedentes presentes.
La comprobación causal está separada de la compilación Lean. El recibo de cada
módulo acredita sus enunciados concretos; la entrega acumulativa final reúne
estos consumidores con los resultados y las aplicaciones bibliográficas de
los cinco artículos. No se modifican los manuscritos ni los paquetes sellados.
