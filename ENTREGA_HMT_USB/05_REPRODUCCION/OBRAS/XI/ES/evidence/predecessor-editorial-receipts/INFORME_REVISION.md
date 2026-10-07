# Informe final de corrección y verificación de la revisión exhaustiva XIV

Fecha: 14 de septiembre de 2026  
Edición: `REVISION_EXHAUSTIVA_14`

## Resultado

La REV14 es una edición sucesora separada de la REV13; REV04--REV13 permanecen
intactas como antecedentes. El enunciado y la demostración cardinal se conservan
sin rebaja. El delta de esta edición es editorial y tipográfico: define `h`
antes de usarlo, precisa la dirección de las dos inyecciones, formula
positivamente la integridad del estado HMT, depura encabezados y mantiene juntas
las unidades matemáticas y figuras señaladas. La generación dodecafásica
completa de `alpha_HMT` y su certificado intervalar no se modifican.

## Contenido causal conservado de las revisiones XI y XII

La unidad `U016_registro_dodecafasico_hadamard_k.tex`, con SHA-256
`40449cd4913dc6867b7784f7338afc63706ea4a5467c6efdad97b6d7d365de96`,
tipa el libro dodecafásico orientado como componente del estado TPK pleno y
contiene las cartas internas exactas

```text
TPKFullState → SignedDodecaphaseState
  ↔ CanonicalSealK ↔ (D3K,D4K,Q_TPK).
```

La fuente local hace explícito que una factorización de esa carta a través de
`CT108RawProjection` no se presupone: requeriría demostrar constancia sobre sus
fibras. No se usa esa proyección cruda como dominio del teorema interno ni de
la prueba cardinal. También identifica sin ambigüedad
`S12=R_sgn=Pi_H∘E108∘R12` sobre la subred compatible y desarrolla la
sustitución

```text
C_term=(b90,b120,Q_TPK) → Pi_H →
B=(972,-1073,101) → s=(2378,1406,2479) →
U^(1),U^(2),U^(3) → S12(X_term)=U_term.
```

Los doce componentes se obtienen por operaciones enteras impresas. Después,
la carta de Hadamard y el extractor transversal prueban el retorno
`U_term↔K↔C_term`. No se emplean el testigo histórico `S8`, `W24`, una criba
de candidatos ni una constante objetivo.

## Delta heredado de la REV08

La REV08 corrigió el alcance del argumento de signos sin alterar el lector
intervalar ya verificado. Para un truncamiento finito, el resto geométrico se
escribe exactamente y se demuestra que, en la raíz positiva y con
`lambda<0`, el truncamiento tiene signo positivo. Por tanto, los signos
débiles de los extremos se atribuyen a la función completa, o al truncamiento
acompañado de su resto certificado, y no al truncamiento aislado. La regresión
`technical/verificar_resto_geometrico.py` comprueba la identidad y su falsador
en 72 casos racionales, tanto en modo normal como optimizado.

La cadena recuperada se compone con el tramo posterior conservado y comprobado
exactamente:

```text
(b90,b120,Q_TPK) → Pi_H → U_term
  → H4^{-1} → K → Dig10 → residuos → (D3,D4,Q) → estado archivado.
```

La recuperación pertenece a una publicación correlacionada del mismo estado y
confirma, sin modificar, la fuente y la prueba del teorema cardinal del
artículo.

## Comprobación de las correcciones

| Punto | Corrección realizada | Localización material | Comprobación |
|---|---|---|---|
| 1. Carta terminal — **TIPADA Y CERRADA EN EL ESTADO PLENO** | Se identifica `S12=R_sgn=Pi_H∘E108∘R12`; las doce ventanas particionan los 108 pasos, los canales se expresan como sumas finitas de todas sus visitas y trazas, se evalúa `S12(X_term)=U_term` y se conserva el cierre exacto `U_term↔K↔(D3K,D4K,Q)`. | `sections/registro_incidencias.tex`, `sections/tpk_desarrollo_integrado.tex`, `sections/registro_k.tex`, `evidence/U016_registro_dodecafasico_hadamard_k.tex` | Composición operatoria completa, sustitución entera y retorno exacto. La tabla fila por fila es una serialización opcional de las mismas sumas; el auxiliar desde `C_term` es un control suplementario y no una frontera causal. |
| 2. Certificado numérico de alfa — **CUMPLIDO** | Los prefijos nonádicos se interpretan como cilindros semiabiertos y se propagan con cola `10^-1000` a `a`, `lambda`, evaluaciones y cilindros. Se conservan las cotas logarítmicas, se imprimen las cotas racionales de `a` y se añaden cinco controles negativos. | `technical/verificar_lector_analitico_alpha.py`, `metadata/certificado-lector-analitico-alpha.json`, `sections/alpha_lector_analitico_completo_rev08.tex` (pp. 125--129) | `PASS_LECTOR_ANALITICO_ALPHA_COMPLETO`; 24 niveles, aritmética racional dirigida y cinco rechazos negativos, tanto en modo normal como optimizado. |
| 3. Desarrollo analítico — **CUMPLIDO** | Se fija `d_M=12+3M`; el rescate usa `E'≥6`, recinto de anchura `≤6w/4` e intersección con `[m-w/4,m+w/4]`; el diámetro queda acotado por `w/2`, también cuando la raíz coincide con el punto medio. Para cada cilindro semiabierto se distinguen el ínfimo `ell_N` y el supremo excluido `u_N`, usando el cierre exterior sólo para el certificado intervalar. | `sections/alpha_lector_analitico_completo_rev08.tex` (pp. 125--129), `technical/verificar_lector_analitico_alpha.py` | Prueba simbólica impresa y control ejecutable normal/optimizado; la igualdad exacta con cero no se usa como decisión algorítmica. |
| 4. Lenguaje, autonomía y guía — **CUMPLIDO** | Se sincronizan los títulos de las publicaciones dodecafásica y analítica correlacionada, el dominio como subconjunto de la subred de integralidad, la frontera analítica, el orden de reproducción y el estatuto de las dependencias. | PDF, pp. 98, 103--112 y 122--130; `sections/alpha_dos_vias_cierre_vigente.tex`, `sections/alpha_dependencias.tex`, `sections/revision_alpha_frontera.tex`, `README.md`, `metadata/source-map.json` | Búsqueda textual, compilación reproducible y control visual integral sobre las 154 páginas. |

Las páginas modificadas se consignan también en `metadata/visual-qa.json`; los
archivos fuente siguen siendo los localizadores causales estables.

## Preservación de la demostración cardinal

El teorema principal conserva su forma y sus inferencias: dentro de la clausura
genealógica construida por APP--TRIT--TPK, la recta HMT y todos sus
subconjuntos internos se cuantifican en una misma semántica; las inyecciones se
construyen en ambos sentidos y Cantor--Bernstein cierra la igualdad cardinal.
Desde la REV12, `Sigma_HMT` contiene expresamente los grafos generados de los
lectores de `pi_HMT`, `phi_HMT`, `e_HMT` y `alpha_HMT`, y declara sus
coordenadas finitas en la historia del estado. No se usan sus valores
convencionales para seleccionar una rama. La representación posterior
`L[h,m_∞]` reconoce la clausura obtenida y no interviene como generador.

## Alfa: identidad simbólica y certificado finito

La publicación dodecafásica y la representación analítica son publicaciones
correlacionadas de la misma coordenada, no dos selectores causalmente
independientes. Para

```text
a(s)=pi_HMT+e_HMT-phi_HMT-4-kappa_per(s),  q=1/729,
lambda(s)=-E9,s(a(s))·(1-q a(s)^3)/a(s)^10,
```

la recurrencia calcula

```text
b_(10+3n)=lambda(s)/729^n,
b_(11+3n)=b_(12+3n)=0.
```

La recurrencia conserva los exponentes `10+3n`, `11+3n` y `12+3n`. La
corrección `d_M=12+3M` fija el grado máximo del truncamiento y garantiza que
cada etapa contiene íntegramente los tres grados de su último bloque.

La sustitución de `lambda(s)` prueba simbólicamente la identidad de raíz. El
certificado finito no confunde esa identidad con una igualdad obtenida al
tratar prefijos como números exactos: encierra las tres coordenadas generadas,
propaga sus colas y demuestra la inclusión de sus cierres exteriores en los
24 cilindros publicados.

## Reproducibilidad

La puerta de construcción aplica una lista cerrada de auxiliares LaTeX,
rechaza PDF o texto reutilizado como entrada, exige ausencia inicial de los
productos regenerables y protege la etapa interna mediante una capacidad de
un solo uso transmitida por tubería. El hash inicial de `SHA256SUMS` queda
congelado y se revalida durante la etapa, en el recibo y antes de la
publicación exterior.

Los auxiliares Python del registro terminal reejecutan exactamente

```text
C_term → Pi_H → U_term → H4^{-1} → K → Dig10
       → residuos → (D3,D4,Q_TPK) → retorno a C_term.
```

No reconstruyen visita por visita una carta firmada después de proyectar el
estado a CT108 y olvidar el ledger. Ese es el alcance del ejecutable
empaquetado, no una reserva sobre la prueba cardinal. El control ejecutable
acompaña las biyecciones internas impresas; no convierte la proyección cruda
en generador ni en dominio del teorema HMT-full.

La única salida terminal aceptada para las dos reconstrucciones independientes
y la reproducción desde el ZIP extraído en un directorio vacío es
`PASS_REPRODUCCION_CH_HMT_REV14`.

## Estatuto final

- Correcciones 1, 2, 3 y 4: cerradas y verificadas.
- Tipado `TPKFullState→SignedDodecaphaseState`: explícito y separado de
  `CT108RawProjection`.
- Cadena terminal posterior a `C_term`: exacta y reproducible por los
  auxiliares empaquetados.
- Demostración cardinal: conservada sin modificación ni condición adicional.
- Generación completa de `alpha_HMT`: conservada sin rebaja; el certificado
  intervalar mantiene su función de comprobación correlacionada.
