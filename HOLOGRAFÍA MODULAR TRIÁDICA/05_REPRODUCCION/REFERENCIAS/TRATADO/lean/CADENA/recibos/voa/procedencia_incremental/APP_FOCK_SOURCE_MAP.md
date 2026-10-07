# Recuperación de APP–Fock y localizadores de Leech–VOA–Moonshine

Estatuto: `RESULTADO_RECUPERADO` en el corpus; `CERTIFICADO_NUEVO` para
los dos módulos Lean de esta carpeta. No se ha editado ningún LaTeX o PDF
de origen. No se repite aquí la inversión de K.

## Fuente U030: el enlace suma–producto no es una coincidencia escalar

Fuente íntegra:

`/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/01_FUENTES/INTEGRAL/tree/New project/output/ENSAMBLADO_CAUSAL_RESTAURADO_HMT_MD_20260905/fuente/colaboracion/partes_i_ii/source/base_residencias/capitulo_21_c20_lineas_1_2612.tex`

- 2274: comienzo de U030, acoplamiento orientado APP–Fock.
- 2291–2300: coeficiente común `c(ν)` sobre las seis clases unidades;
  los coeficientes de las clases 0, 3 y 6 no fijan ese coeficiente común.
- 2343–2370: `V_m=V_Σ,m⊕V_Π,m`, Coxeter `g_m=C^(⊕m/2)⊕(C⁻¹)^(⊕m/2)`,
  paridad `E_m=I_Σ⊕(-I_Π)`, y grado dos `V_m[2]⊕Sym²(V_m[1])`.
  El acoplamiento es `3c(ν)(0⊕Sym²(E_m))⊗o_ΣΠ`.
- 2403–2441: índice orientado `-3mc(ν)/2`, mediante
  `tr(E_m g_m)=0`, `tr((E_m g_m)²)=-m` y la traza de Sym².
- El agregado producido por las dos hojas es
  `δ=12e₀+3e₃+3e₆−3Σ_(u unidad)e_u`; por tanto `c(δ)=-3`.
  Las doce fibras son `3 pares × 2 hojas × 2 órbitas`; el índice resultante es 54.
- 2468–2520: coeficiente de Fock `F(m)=m(m−3)/2` y norma radial
  `R(m)=2(m+15)`.
- 2522–2551: `F(m)=R(m) ⇔ (m−12)(m+5)=0`; para `m>0`, únicamente `m=12`.
- 2575–2588: falsador `δ+k e₀`. Conserva el acoplamiento y el índice;
  cambia el peso digital de 54 a `54+9k`. Esto impide sustituir la
  identidad operatorial por la sola coincidencia de dos cifras.

La unicidad del acoplamiento en U030 se formula bajo sus condiciones
de linealidad, soporte de grado dos, paridad y normalización del marco
triangular. No es una afirmación de unicidad entre todos los operadores
imaginables sin esas condiciones.

## Implementación comprobada

`APPFockRigidity.lean` importa el productor APP existente (`APPArithmetic`):
construye los dos histogramas, su diferencia, el coeficiente común, el peso
digital, la perturbación, y prueba la ecuación de rigidez para todo entero
positivo `m`. Su polinomio de Fock se declara como el polinomio de grado dos;
ese módulo por sí solo no prueba una identidad de producto infinito.

`APPFockIndex.lean` añade el operador real de grado dos en el caso de doce
fibras: una matriz Coxeter orientada de 24 coordenadas, su matriz completa
de 300 tensores simétricos, la paridad de hoja y el acoplamiento producido
por el agregado APP. Demuestra:

1. `tr(g)=-12`, `tr(Eg)=0`.
2. `tr(Sym² g)=66`, `tr(Sym²(Eg))=-6`.
3. El operador graduado `g⊕Sym²(g)` tiene traza `-12+66=54`.
4. El acoplamiento `H_δ Γ₂(g)` tiene traza `3·(-3)·(-6)=54`.
5. La norma radial de la familia declarada en `m=12` también es 54.
6. `δ+e₀` deja intacto el operador de acoplamiento, pero su peso digital es 63.

La base de Sym² se realiza mediante tensores simétricos: `e_i⊗e_i` y
`e_i⊗e_j+e_j⊗e_i` para `i<j`. De ahí procede el factor dos de sus
entradas, no de un valor de traza suministrado externamente.

Los dos recibos JSON registran compilación incremental, dependencias reutilizadas,
huellas, consulta de axiomas y alcance. Son 15 consultas en cada módulo.
Las trazas finitas utilizan reducción del kernel; no `native_decide`.
Los módulos no postulan FLM, Monster o la identidad de un producto infinito.

## Artículo I: cadena reticular y prolongación clásica concreta

Raíz de secciones activa examinada:

`/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/stage18_article_I/delivery/HMT_ARTICULO_I_FUENTES_Y_PRUEBAS_ES_EN_REV04B/documentation/payload/manuscript_es/sections`

En `excepcional.tex`:

- 607–668: pegado ternario `N(C_W)` sobre `A₂¹²`; integralidad, paridad,
  unimodularidad y raíces exactamente `A₂¹²`.
- 673–707: cámara radial positiva `a_i=1+3b_i≥1`, condición congruencial,
  mínimo 54 y dirección marcada `(4,1,…,1)`. El mínimo se afirma dentro
  de esa cámara; el texto no lo afirma en toda la clase residual.
- 709–758: vecino `N_α=N_α^0+Z(v_α/3)`, donde
  `N_α^0={x∈N:〈x,v_α〉≡0 mod3}`. Integralidad, paridad,
  unimodularidad y ausencia de raíces; identificación posterior con Leech.
- 771–825: `V_Λ=M(1)⊗C_ε[Λ]`, elevación de la negación y
  `V_HMT^natural=V_Λ^+⊕(V_Λ^T)^+`, con producto orbifold, cociclo y paridad.
  El teorema `exc:moonshine` aplica FLM a ese retículo: carga central24,
  peso1 nulo, carácter `J=j−744` y automorfismos Monster. El artículo
  declara expresamente que no vuelve a demostrar el teorema FLM.
- 849–861: series `T_g=Tr(g q^(L₀−1))` y aplicación del teorema1.1
  de Borcherds para el resultado de género cero.

En `moonshine_comparacion.tex`:

- 74–123: isometría concreta de orden tres sobre el vecino marcado,
  con Coxeter, reflexión, palabra ternaria completa y las divisibilidades
  y emparejamientos que prueban la conservación del vecino.
- 130–167: carácter ciclotómico `t₃`, peso torcido `4/3` y tipo cero.
- 169–218: orbifold de orden tres y operador dual; identificación `t₃+12`
  con clase3B, mediante los teoremas de Chen–Lam–Shimakura y
  Abe–Lam–Yamada citados por el manuscrito.
- 236–270: isomorfismo entre las realizaciones de orden dos y tres que
  transporta vacío, vector conforme, grados, productos de vértices y trazas.
  El texto conserva su dependencia de elecciones de identificación.

## Artículo IV

Raíz examinada:

`/Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/04_MOONSHINE_DUALIDAD_TEORIA_M_ES/documentacion_original/payload`

`main.tex:73` incluye la sección excepcional. En `sections/excepcional.tex`
la misma cadena reticular–VOA está desplazada aproximadamente dieciséis líneas
respecto de I: vecino alrededor de693, VOA753, FLM780 y Borcherds833–842.
`moonshine_comparacion.tex` conserva el mismo mecanismo de orden tres y cita
Chen–Lam–Shimakura, teorema1.1, y Abe–Lam–Yamada, teorema4.4 y §§2–4.

El desarrollo operatorial completo U030 no está reunido en esas dos secciones
de I/IV bajo su título propio: se recuperó del propietario integral indicado.
La sección IV `acoplamiento_recuperacion.tex` trata la recuperación orbital
del registro K y sus canales; no sustituye el operador APP–Fock U030.

## Continuación formal tipada

La formalización aritmética y el grado dos del acoplamiento quedan reunidos
en los módulos anteriores. El siguiente enlace de la cadena no consiste en
postular que `54` produce una VOA: consiste en conectar la realización
simétrica de todos los modos con el álgebra torcida del mismo retículo y
construir el campo de vértices correspondiente. La aplicación FLM y el
teorema de Borcherds que usa el LaTeX siguen siendo resultados matemáticos
específicos, no se convierten en pruebas Lean por el hecho de citarlos.
