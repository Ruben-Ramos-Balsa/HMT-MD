# Procedencia de la energía intervalar y del refinamiento

El ámbito de esta nota es el lector positivo de una partición ordenada producida a partir del registro `K`. No modifica el TPK ni los manuscritos previos. La extracción de `K`, la energía del grafo de memoria y la identidad de Schur tienen propietarios materiales anteriores. La especialización a separaciones `d_j=K_j/6263`, la interpolación armónica por esos pesos y el cuadrado que conmuta con el flujo de separaciones se presentan como **formalización añadida sobre resultados recuperados**. No se reivindica novedad histórica del principio variacional ni del complemento de Schur.

## Propietarios consultados

1. `output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source/libro/01_acoplamiento.tex`, etiquetas `lib01:cadena-registro`, `lib01:K`: extracción `x_term → R_12 → (b90,b120,Q) → U_sgn → K`, doce componentes positivas y carga 6263.
2. En la misma fuente, `libro/02_norma_ternaria.tex`, líneas 27–81, etiquetas `lib02:lectores`, `lib02:gram`, `lib02:energia-aristas`: Gram de memoria como suma ponderada de diferencias en el ciclo de doce posiciones. Sus aristas tienen pasos 1,3,4,5. Este grafo conserva su dominio; no se identifica con la red intervalar nueva.
3. `output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/delivery/USB_ES_EN_STAGE10_20260917/ES/PAQUETES/08_PRIMOS_Y_ZETA_ES/documentacion_original/payload/reference/spanish_active_tex/ampliacion/schur_y_coercividad.tex`, etiquetas `schur-add-schur-exacto`, `schur-add-eq-S2`, `schur-add-eq-S3`, `schur-add-residual`: eliminación de detalles y residual positivo para la forma completa de Weil. La identidad se reutiliza como álgebra de bloques; la forma de Weil y la energía intervalar tienen sus propios operadores y dominios.
4. `output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source/libro/memoria_reducida_20260916.tex`, etiquetas `lib04:memoria-explicita`, `lib04:schur-bilateral`: eliminación de memoria auxiliar y reconstrucción; antecedente conceptual para mantener la componente de detalle después de reducir una observación.
5. `output/EXTREMA_MEDIA_RAZON_NARRACION_Y_REVISION_20260916/ARTICULO/ES/source/sections/k_direccion_dimensional.tex`, etiqueta `eq:k-vector-direccional`: dirección exacta `u=P3 P11 K` utilizada en el flujo posterior.

La búsqueda focal se realizó con los términos energía, Dirichlet, Schur, interpolación, conductancia y resistencia en estos propietarios y en el paquete de cobertura/memoria del 17 de septiembre. No se utiliza esa búsqueda limitada para afirmar ausencia global del lector intervalar en todo el corpus.

## Fórmulas entregadas

`L_d = D* diag(1/d_j) D`; `E_d(f)=f*L_df`.

`RH=I`; `L_ref H=R* L_coarse`; `H*L_ref H=L_coarse`.

`g=H(Rg)+z`, `Rz=0`; `E_ref(g)=E_coarse(Rg)+E_ref(z)`.

`Schur_I(L_ref)=L_coarse`; reducciones sucesivas e interpolaciones componen exactamente.

`Lambda_two_ends=(sum d)^-1 [[1,-1],[-1,1]]`.

`E(g)-f*Lambda f=r*C^-1 r >=0` para el residual interior `r`.

Con hijos de fracciones fijas que heredan la velocidad de su padre, `H` local es constante y Schur conmuta con el flujo. La interpolación desde los dos extremos globales cambia con las separaciones; su operador de Dirichlet a Neumann sólo retiene la longitud total. El lector nodal completo recupera cada `d_j` desde su entrada fuera de diagonal.

## Verificación

`python3 -I -S energy/verify_energy_refinement.py` usa sólo la biblioteca estándar y aritmética racional. Comprueba matrices completas, inversas exactas, composición, residuos, el flujo con pesos positivos racionales independientes y las dos componentes de la derivada exacta en `Q(sqrt(5))`. Las pruebas generales para todas las particiones y todos los parámetros se exponen en `energia_refinamiento.tex`.
