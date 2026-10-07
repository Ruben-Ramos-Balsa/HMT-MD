# Article VI delta — longitudinal rigidity, mass, and gravity

Date: 26 September 2026. Language: EN.

## Applied scope

- Marked incidence fixes \(N=5760\), \(r_N=5759/23040\), and
  \(L_\alpha=\alpha_{\rm HMT}^{16}r_NL_\star\) before the clock.
- The construction then yields
  \(t_0=\pi_{\rm HMT}L_\alpha/(54c_{\rm int})\),
  \(R_{108}=L_\alpha\), \(Q_L=\hbar_{\rm ret}c_{\rm int}/L_\alpha\),
  \(m_{\rm clk}=Q_L/c_{\rm int}^2\), and \(b_e=E_e^{(0)}/Q_L\).
- Independent longitudinal and action cotransformation is published:
  \(Q_L,m_{\rm clk}\mapsto(\mu/\lambda)(Q_L,m_{\rm clk})\) and
  \(b_e\mapsto(\lambda/\mu)b_e\). The mass operator remains invariant.
- On the common returned section, R01,
  \(H\Lambda=\hbar c_{\rm int}I\), and R02,
  \(\mathcal R_g\Lambda=L_\alpha^2I\), are proved. For distinct
  sections, the text explicitly retains
  \(r_g^{(a)}\bar\lambda=(\hbar_{\rm ret}/\hbar_a)L_\alpha^2\).
- The subsequent radial identification uniquely forces
  \(G=c_{\rm int}^3L_\alpha^2/\hbar\). The circular formula is retained
  as a corollary. The pseudoinverse and projection onto
  \((\ker X)^\perp\) preserve the semidefinite sector; the null sector
  is not inverted.
- \(Q_{L,a}=E_{P,a}\) is stated only within the same action section.
  \(G\) does not precede the mass operator, and no species-dependent
  \(10^{-34}\) correction is introduced.

## Modified files

- `ampliacion_20260922.tex`
- `sections/00_resumen.tex`
- `sections/01_introduccion.tex`
- `sections/90_conclusiones.tex`
- `technical/verificar_rigidez_gravitatoria_masas_vi.py`

## Preservation and exclusions

Sections 05, 07, 09, 11, and 12 are byte-identical to the exact base.
Neither `main_catalogo.tex`, `sections/10a_dependencia_activa_l_g.tex`,
nor sections 11/12 reserved for the annex editor were edited. Mass and
comparison tables remain intact.

## Control

`python3 -I -S technical/verificar_rigidez_gravitatoria_masas_vi.py`

Output: `PASS_RIGIDEZ_G_MASAS_VI_PORTABLE`.

The control uses exact rational arithmetic, a non-diagonal massive matrix
fibre, and two independent variations: longitudinal section (7/3) and
action section (11/5). Precompilation remains pending by explicit
instruction.
