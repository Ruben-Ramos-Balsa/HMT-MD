# N73 - Teorema de puerta de orientación

## Resultado principal

En todas las fronteras ambiguas auditadas t=5..25:

- phi queda fijo;
- pi+e queda fijo;
- la ambigüedad local vive solo en el reparto de pi/e.

Esto significa que la ambigüedad no es de escala ni de carga total. Es de orientación.

## Teorema local exacto

Si q y a están fijos, entonces:
u^phi = 2(q-a)
y
u^pi + u^e = q - u^phi

Luego cualquier ambigüedad residual solo puede vivir en la descomposición de pi/e.

## Auditoría finita

Valores ambiguos:
[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 23, 24, 25]

Todas las ambiguas cumplen:
all_phi_fixed = True
all_pi_plus_e_fixed = True

Resolución máxima por supervivencia coinductiva:
max_resolution_depth = 3

## Novena zona

t=8 y t=9 son puertas de orientación muy visibles, pero no únicas. La novena puerta confirma la pauta; no la inaugura.
