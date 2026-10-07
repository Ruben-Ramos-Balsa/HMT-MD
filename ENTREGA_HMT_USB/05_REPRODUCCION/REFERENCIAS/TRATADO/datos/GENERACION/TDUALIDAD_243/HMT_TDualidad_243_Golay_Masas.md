# Dualidad de lectura HMT: T-dualidad, bloque 243, Golay ternario y rutas de masa

**Documento de trabajo tecnico**  
**Holografia Modular Triadica / Mecanica Dimensional**

## Resumen

Este documento formula la dualidad T de cuerdas como una proyeccion continua de una dualidad HMT mas primaria: el intercambio entre valor visible y memoria de frontera. En HMT, todo entero se lee como `n = 9Q + r`, donde `r` es valor visible en la rueda nonadica y `Q` es memoria de cruce de borde. La misma estructura aparece en la APP levantada, en la descomposicion `1215 = 54 + 9*129`, en la unidad dimensional estratificada `1000 = 729 + 243 + 27 + 1`, y en la lectura de masa como ruta con avance visible y enrollamiento contraangular. El documento conecta esta dualidad con el bloque `243`, la bola ternaria perfecta `V_3(11,2)=243`, el codigo ternario puncturado de Golay `[11,6,5]_3`, los canales `pi,e,phi,alpha`, la bisagra `744`, la dimension `11=6+5=3+8`, y la forma HMT de la T-dualidad: `(r,Q;R) -> (Q,r;1/R)`.

La tesis central queda fijada asi:

```
T-dualidad = intercambio de lectura entre residuo visible y memoria de frontera.
```

En lenguaje de cuerdas, el residuo visible se proyecta como modo de vibracion o momento, mientras que la memoria de frontera se proyecta como winding. En Mecanica Dimensional, esos dos modos aparecen como `n_A A_rad` y `(s_C/6) C*_rad`, es decir, avance visible y memoria contraangular.

---

## 1. Objeto y programa

La HMT no toma el continuo como objeto primario. Parte de una celula discreta con memoria de frontera. La recta real, Moonshine y la fisica dimensional aparecen como lecturas distintas de esa celula.

El presente documento desarrolla un modulo especifico:

```
APP levantada -> valor/memoria -> T-dualidad HMT -> 243/Golay -> rutas de masa.
```

El objetivo no es importar la dualidad T desde la teoria de cuerdas, sino mostrar que la estructura de la dualidad T ya existe en HMT antes de su geometrizacion continua.

La definicion operativa es:

```
n = 9Q + r,
```

con `r` como lectura visible y `Q` como memoria de borde. Esta pareja `(r,Q)` es la semilla de la dualidad visible/enrollada.

---

## 2. Lectura visible y memoria de frontera

Para todo entero positivo `n`, definimos la lectura nonadica HMT:

```
r_9(n) = 1 + ((n-1) mod 9),
Q_9(n) = (n - r_9(n))/9.
```

Entonces:

```
n = 9 Q_9(n) + r_9(n).
```

La lectura visible es `r_9(n)`. La memoria de frontera es `Q_9(n)`. La lectura ordinaria conserva el resto. HMT conserva el par completo:

```
n -> (r,Q).
```

Este par contiene la estructura minima de una lectura compacta: algo aparece dentro de la rueda y algo queda como memoria de cuantas veces se cruzo el borde.

### Principio 2.1 - Dualidad visible/memoria

La celula HMT admite dos lecturas conjugadas:

```
lectura visible: r,
lectura de frontera: Q.
```

La primera se proyecta como fase, valor o vibracion. La segunda se proyecta como memoria, enrollamiento o winding.

---

## 3. Modelo minimo de T-dualidad HMT

Sea `R` una escala positiva. Definimos el funcional de cierre:

```
E_R(r,Q) = r^2/R^2 + Q^2 R^2.
```

Entonces:

```
E_R(r,Q) = E_{1/R}(Q,r).
```

### Prueba

```
E_{1/R}(Q,r) = Q^2/(1/R)^2 + r^2(1/R)^2
             = Q^2 R^2 + r^2/R^2
             = E_R(r,Q).
```

Por tanto:

```
(r,Q;R) <-> (Q,r;1/R).
```

Esta es la forma HMT de la dualidad T. En la teoria de cuerdas, la formula continua usual contiene terminos de la forma:

```
n^2/R^2 + w^2 R^2/alpha'^2.
```

HMT da la estructura antes de la cuerda continua:

```
residuo visible + memoria de frontera + inversion de escala.
```

La dualidad T aparece como la proyeccion continua de esta involucion de lectura.

---

## 4. APP levantada: vibracion y winding de suma/producto

En APP se tienen dos operaciones sobre el mismo soporte: suma y producto. La version visible usa restos. La version HMT completa conserva restos y memorias.

Para la suma:

```
i + j = 9 Q^+_{ij} + R^+_{ij}.
```

Para el producto:

```
ij = 9 Q^x_{ij} + R^x_{ij}.
```

La APP levantada es:

```
A_9^# = (R^+,Q^+ ; R^x,Q^x).
```

Aqui `R^+, R^x` son modos visibles y `Q^+, Q^x` son modos de memoria o winding aritmetico.

La discrepancia completa es:

```
ij - (i+j) = (R^x_{ij} - R^+_{ij}) + 9(Q^x_{ij} - Q^+_{ij}).
```

Al sumar toda la celula `1 <= i,j <= 9`:

```
sum R^+ = 405,
sum R^x = 459,
sum Q^+ = 45,
sum Q^x = 174.
```

Por tanto:

```
Delta_visible = 459 - 405 = 54,
Delta_memoria = 174 - 45 = 129.
```

La diferencia bruta total es:

```
sum ij - sum(i+j) = 2025 - 810 = 1215.
```

Y la descomposicion HMT es:

```
1215 = 54 + 9*129.
```

Normalizando por la rueda:

```
1215/9 = 135.
```

Ademas:

```
135 = 6 + 129 = 120 + 15.
```

Lectura:

```
54  = defecto visible,
129 = defecto de memoria/winding,
135 = defecto total normalizado,
120 = canal octadico/constitutivo,
15  = par interno de hexada.
```

La APP ya separa el modo vibracional y el modo de enrollamiento. La teoria de cuerdas geometriza despues esta separacion.

---

## 5. EMRH estratificada: 1000 = 729 + 243 + 27 + 1

La Extrema y Media Razon Holografica se escribe en su forma cubica:

```
10^3 = 9^3 + 3*9^2 + 3*9 + 1.
```

Es decir:

```
1000 = 729 + 243 + 27 + 1.
```

Aqui:

```
729 = 9^3       = bulk tridimensional,
243 = 3*9^2     = borde de codimension uno,
27  = 3*9       = borde de codimension dos,
1   = retorno de codimension tres.
```

La corona activa se refina como:

```
270 = 243 + 27 = 3*9^2 + 3*9.
```

La unidad HMT se entiende como cubo discreto dirigido:

```
unidad = interior + borde activo estratificado + retorno.
```

El paso `9 -> 10` abre una capa dimensional completa. La frontera de un nivel se convierte en canal de propagacion del siguiente nivel de lectura.

---

## 6. Certificado 243: borde dimensional y bola ternaria perfecta

El bloque `243` aparece tambien como bola de Hamming ternaria de radio `2` en longitud `11`:

```
V_3(11,2) = sum_{k=0}^2 binom(11,k) 2^k
          = 1 + 22 + 220
          = 243.
```

El codigo ternario perfecto puncturado de Golay tiene parametros:

```
G_11 = [11,6,5]_3.
```

Su cardinal es:

```
|G_11| = 3^6 = 729.
```

Y:

```
729 * 243 = 3^11.
```

Lectura:

```
G_11 tesela F_3^11 con bolas ternarias de radio 2.
```

El mismo `243` es, simultaneamente:

```
3*9^2                      = borde codimensional de la unidad HMT,
V_3(11,2)                  = bola perfecta de correccion ternaria,
3^5                        = profundidad de correccion,
1 + 22 + 220               = centro + primer cascaron + segundo cascaron.
```

Esto conecta borde dimensional, correccion perfecta, dimension `11`, Witt/Golay y la lectura de teoria M.

---

## 7. Descomposicion HMT de 243

La bola `243` admite la descomposicion:

```
243 = 1 + 22 + 90 + 120 + 10.
```

Lectura:

```
1   = centro / retorno,
22  = primer cascaron Hamming = 2*11,
90  = 6*binom(6,2)  = canal hexadico,
120 = 8*binom(6,2)  = canal octadico,
10  = 9 + 1         = monodromia de puerta 10 -> 1.
```

El bloque `243` contiene en una sola capa:

```
retorno, electron 22, hexada 90, octada 120 y monodromia 10.
```

Esta identidad situa `22`, `90`, `120` y `10` dentro de la misma bola perfecta de Hamming.

---

## 8. Canales de constantes desde 243

Sea:

```
B = 243.
```

Entonces los canales principales se escriben como:

```
C_alpha = 3B             = 729,
C_e     = B + 27 + 1     = 271,
C_pi    = B + 72         = 315,
C_phi   = B - 81 - 1     = 161.
```

Lectura:

```
alpha = triple bloque 243,
e     = bloque 243 + kappa_27 + retorno,
pi    = bloque 243 + canal 72,
phi   = bloque 243 - subcuadrado 81 - retorno.
```

La bisagra `744` se recupera:

```
C_pi + C_e + C_phi - 3 = 315 + 271 + 161 - 3 = 744.
```

Y:

```
744 = 729 + 15.
```

Por tanto:

```
traza reducida(pi,e,phi) = triple bloque 243 + par hexadico.
```

---

## 9. Dimension 11: dos lecturas compatibles

El codigo ternario perfecto puncturado da:

```
11 = 6 + 5.
```

Donde:

```
6 = dimension del codigo G_11,
5 = profundidad de correccion, 3^5 = 243.
```

Tambien HMT usa:

```
11 = 3 + 8.
```

Donde:

```
3 = TRIT,
8 = octada interna.
```

Luego:

```
11 = 6 + 5 = 3 + 8.
```

Y:

```
12 = 11 + 1.
```

Lectura:

```
M-theory 11 <-> [11,6,5]_3 <-> 729*243 = 3^11 <-> TRIT + octada.
```

La dimension 11 se lee como codigo mas correccion y como trit mas octada.

---

## 10. T-dualidad y Mecánica Dimensional

En Mecánica Dimensional, la accion de ruta local se escribe:

```
E_0(P) = n_A(P) A_rad + (s_C(P)/6) C*_rad.
```

Lectura:

```
n_A(P) A_rad        = modo de avance / vibracion visible,
(s_C(P)/6) C*_rad   = modo de frontera / winding contraangular.
```

La masa local:

```
m_HMT(P) = m_e exp(E_0(P)).
```

La torre refinada anade memoria de frontera:

```
E(P) = E_0(P) + k(P) Delta_4 + nu_120(P) s_120 + nu_270(P) zeta_270.
```

Donde:

```
Delta_4    = torsion minima,
s_120      = selector hexada-octada,
zeta_270   = 135 Delta_4^2 = memoria cuadratica de corona.
```

La dualidad abstracta de ruta se escribe:

```
E_{A,C}(n,w) = n A_rad + w C*_rad,
E_{A,C}(n,w) = E_{C,A}(w,n)
```

como identidad de intercambio de los dos modos de lectura. En el sector fisico, `A` y `C*` estan polarizados; la dualidad aparece seleccionada por el ledger.

La masa se interpreta como:

```
masa = exponencial de una ruta de cierre con avance visible, winding de frontera y torsion.
```

---

## 11. Level matching como cierre de ledger

En cuerdas cerradas, la consistencia entre modos izquierdo y derecho se escribe esquematicamente como:

```
N_L - N_R = n w.
```

Lectura HMT:

```
desbalance entre hojas = producto de fase visible por memoria de frontera.
```

El lado izquierdo mide diferencia de excitacion entre hojas. El lado derecho mide acoplamiento entre vibracion y winding.

Por tanto:

```
level matching = cierre de ledger two-way.
```

Esto conecta con CP/T/CPT en HMT: una asimetria de orientacion debe compensarse por inversion two-way para cerrar el ledger.

---

## 12. T-dualidad, modularidad y funcion J

La dualidad T tambien toca la modularidad. En el toro complejo:

```
q = exp(2 pi i tau).
```

Las transformaciones modulares incluyen:

```
tau -> -1/tau.
```

Esta inversion intercambia ciclos del toro. En cuerdas, T-dualidad intercambia radio grande y radio pequeno. En HMT, ambas son lecturas de:

```
intercambio entre ciclo visible y ciclo de frontera.
```

La funcion `J` modular se lee como cierre externo. La accion de Sommerfeld se lee como cierre fisico. La T-dualidad se lee como intercambio de dos periodos. HMT contiene la estructura primaria: frontera con memoria.

---

## 13. Consecuencias fisicas

### 13.1 Fotón

El foton observable corresponde al modo central del TPK:

```
L_TPK = 3(I - P_0),
Spec(L_TPK) = {0,3,3}.
```

El modo cero se lee como propagacion nula extendida:

```
gamma = modo central sin memoria compactificada propia.
```

### 13.2 Electrón

El electron aparece como cierre compacto de dos modos nulos conjugados:

```
e^- = cierre compacto de P_+ + P_-.
```

Es winding fisico minimo: frontera con memoria estable.

### 13.3 Masa

La masa mide el coste de estabilizar esa memoria compacta:

```
masa = accion de ruta estabilizada por memoria de borde.
```

### 13.4 Pauli

Pauli se lee como saturacion de ledger:

```
dos fermiones iguales no ocupan la misma frontera porque el cierre de winding ya esta saturado.
```

### 13.5 Bosones

Los bosones se leen como modos compartibles de memoria desplegada:

```
boson = modo de memoria desplegada,
fermion = memoria compactificada.
```

---

## 14. Certificados computacionales incluidos

El paquete adjunto incluye un certificado Python que verifica:

1. `1000 = 729 + 243 + 27 + 1`.
2. `V_3(11,2) = 1 + 22 + 220 = 243`.
3. `729 * 243 = 3^11`.
4. `243 = 1 + 22 + 90 + 120 + 10`.
5. Canales desde `243`: `729,271,315,161`.
6. Bisagra `315+271+161-3=744`.
7. APP levantada: `1215 = 54 + 9*129`.
8. Dualidad minima: `E_R(r,Q)=E_{1/R}(Q,r)`.
9. Lecturas dimensionales: `11=6+5=3+8`, `12=11+1`, `26=2+24`, `10=2+8`.

---

## 15. Conclusiones

La dualidad T de cuerdas se entiende en HMT como una sombra continua de una dualidad mas primaria:

```
residuo visible <-> memoria de frontera.
```

El winding no aparece primero como una propiedad exotica de una cuerda en una dimension compacta. Aparece antes como cociente de frontera en la lectura:

```
n = 9Q + r.
```

La vibracion lee `r`. El enrollamiento lee `Q`. La inversion de escala intercambia esos dos lectores.

El bloque `243` une esta dualidad con Golay ternario, dimension `11`, `90/120`, canales de constantes, masa de ruta y teoria M:

```
243 = 3*9^2 = V_3(11,2) = 1+22+90+120+10.
```

Desde el mismo bloque salen:

```
C_alpha = 3*243 = 729,
C_e     = 243 + 27 + 1 = 271,
C_pi    = 243 + 72 = 315,
C_phi   = 243 - 81 - 1 = 161.
```

El documento fija asi una tesis:

```
T-dualidad = resto/cociente visto en geometria compacta.
```

Y una forma mas general:

```
HMT lee la masa, la cuerda y la dimension como modos de una misma frontera con memoria.
```
