# Delta Artículo VI — rigidez longitudinal, masa y gravedad

Fecha: 26 de septiembre de 2026. Idioma: ES.

## Alcance aplicado

- La incidencia marcada fija \(N=5760\), \(r_N=5759/23040\) y
  \(L_\alpha=\alpha_{\rm HMT}^{16}r_NL_\star\) antes del reloj.
- Después se construyen \(t_0=\pi_{\rm HMT}L_\alpha/(54c_{\rm int})\),
  \(R_{108}=L_\alpha\), \(Q_L=\hbar_{\rm ret}c_{\rm int}/L_\alpha\),
  \(m_{\rm clk}=Q_L/c_{\rm int}^2\) y \(b_e=E_e^{(0)}/Q_L\).
- Se publica la cotransformación independiente de longitud y acción:
  \(Q_L,m_{\rm clk}\mapsto(\mu/\lambda)(Q_L,m_{\rm clk})\) y
  \(b_e\mapsto(\lambda/\mu)b_e\). El operador de masa permanece
  invariante.
- En la sección retornada común se prueban R01,
  \(H\Lambda=\hbar c_{\rm int}I\), y R02,
  \(\mathcal R_g\Lambda=L_\alpha^2I\). Para secciones distintas se
  conserva explícitamente
  \(r_g^{(a)}\bar\lambda=(\hbar_{\rm ret}/\hbar_a)L_\alpha^2\).
- La identificación radial posterior fuerza de manera única
  \(G=c_{\rm int}^3L_\alpha^2/\hbar\). La fórmula circular se conserva
  como corolario. La pseudoinversa y la proyección sobre
  \((\ker X)^\perp\) preservan el sector semidefinido; el sector nulo no
  se invierte.
- \(Q_{L,a}=E_{P,a}\) se declara sólo dentro de la misma sección de acción.
  \(G\) no antecede al operador de masa y no se introduce ninguna
  corrección \(10^{-34}\) dependiente de la especie.

## Archivos modificados

- `ampliacion_20260922.tex`
- `sections/00_resumen.tex`
- `sections/01_introduccion.tex`
- `sections/90_conclusiones.tex`
- `technical/verificar_rigidez_gravitatoria_masas_vi.py`

## Preservación y exclusiones

Las secciones 05, 07, 09, 11 y 12 coinciden byte a byte con la base exacta.
No se editó `main_catalogo.tex`, ni `sections/10a_dependencia_activa_l_g.tex`,
ni las secciones 11/12 reservadas al editor del anexo. Las tablas de masas
y contraste permanecen intactas.

## Control

`python3 -I -S technical/verificar_rigidez_gravitatoria_masas_vi.py`

Salida: `PASS_RIGIDEZ_G_MASAS_VI_PORTABLE`.

El control usa aritmética racional exacta, una fibra masiva matricial no
diagonal y dos variaciones independientes: sección longitudinal (7/3)
y sección de acción (11/5). La precompilación queda pendiente por
instrucción expresa.
