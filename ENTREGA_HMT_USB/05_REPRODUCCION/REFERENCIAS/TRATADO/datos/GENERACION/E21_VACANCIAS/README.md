
# HMT E21/22 CELLULAR 01

## Datos exactos

rho = log_1000(729) = log_10(9)
epsilon = 1 - rho = log_10(10/9)

rho = 0.95424250943932487459005580651023061840025772838139
epsilon = 0.045757490560675125409944193489769381599742271618608
1/epsilon = 21.854345326782832562577351508746968935114554971886

## Huecos primarios

Las posiciones p_n=floor(n/epsilon) tienen huecos {21,22}.
Primeras posiciones:
[0, 21, 43, 65, 87, 109, 131, 152, 174, 196, 218, 240, 262, 284, 305, 327, 349, 371, 393, 415]

Primeros huecos:
[21, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 21, 22, 22]

## Segunda escala 6/7

Los huecos cortos 21 aparecen en índices:
[0, 6, 13, 20, 27, 34, 41, 48, 54, 61, 68, 75, 82, 89, 96, 102, 109, 116, 123, 130, 137, 144, 151, 157, 164]

Sus retornos son:
[6, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7]

La frecuencia de hueco corto es beta = 22 - 1/epsilon = 0.14565467321716743742264849125303106488544502811417.
1/beta = 6.8655538329966609969381012073988490390325374219294.
Por tanto, los retornos secundarios son 6 o 7.

## Ventanas HMT

[
  {
    "N": 22,
    "N_epsilon": "1.006664792334852759018772256774926395194",
    "floor": 1,
    "ceil": 2,
    "advances_floorcase": 21,
    "advances_ceilcase": 20
  },
  {
    "N": 132,
    "N_epsilon": "6.039988754009116554112633540649558371166",
    "floor": 6,
    "ceil": 7,
    "advances_floorcase": 126,
    "advances_ceilcase": 125
  },
  {
    "N": 1000,
    "N_epsilon": "45.75749056067512540994419348976938159974",
    "floor": 45,
    "ceil": 46,
    "advances_floorcase": 955,
    "advances_ceilcase": 954
  },
  {
    "N": 729,
    "N_epsilon": "33.35721061873216642384931705404187918621",
    "floor": 33,
    "ceil": 34,
    "advances_floorcase": 696,
    "advances_ceilcase": 695
  },
  {
    "N": 131,
    "N_epsilon": "5.994231263448441428702689347159788989566",
    "floor": 5,
    "ceil": 6,
    "advances_floorcase": 126,
    "advances_ceilcase": 125
  },
  {
    "N": 153,
    "N_epsilon": "7.000896055783294187721461603934715384761",
    "floor": 7,
    "ceil": 8,
    "advances_floorcase": 146,
    "advances_ceilcase": 145
  },
  {
    "N": 1049,
    "N_epsilon": "47.99960759814820655503145897076808129813",
    "floor": 47,
    "ceil": 48,
    "advances_floorcase": 1002,
    "advances_ceilcase": 1001
  },
  {
    "N": 2251,
    "N_epsilon": "103.000111252079707297784379545470877981",
    "floor": 103,
    "ceil": 104,
    "advances_floorcase": 2148,
    "advances_ceilcase": 2147
  }
]

## Alfa por vacancia

alpha0 = epsilon/(2*pi) = 0.0072825308062121875851522897685332436539019191054637

Con alpha_HMT = 0.007297352569283800997285105472380663

Residuo 5 términos:
0.000000000000003291726190804839398023566794746390350558289856398

Residuo 6 términos con -alpha^6/46:
9.0038886279943083176441665410322626955924107843718e-18

Raíz inversa 5 términos:
137.03599908400987825838677450195817559796993365685

Raíz inversa 6 términos:
137.03599908400002702009012825987492484805160851508

Diferencia raíz inversa 6 términos contra alpha_HMT^-1:
0.00000000000002702009012825987491418217154187073822886160076704
