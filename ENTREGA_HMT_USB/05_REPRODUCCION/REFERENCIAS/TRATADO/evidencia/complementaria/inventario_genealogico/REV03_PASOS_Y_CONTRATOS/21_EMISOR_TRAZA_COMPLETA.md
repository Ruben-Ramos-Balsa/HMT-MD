# Emisor finito APP–TRIT–TPK: traza íntegra de cincuenta y cuatro transiciones

## Alcance de esta ampliación

Este bloque despliega un caso completo del emisor documentado en el artículo X vigente y una regla paramétrica aplicable a todas sus condiciones iniciales. Es un aporte parcial al árbol global del integral, el reservorio, la serie, la narración y los desarrollos especializados. No convierte el índice de la cantera histórica en arquitectura global ni sustituye las entregas REV01 y REV02.

El corte causal se sitúa en

\[
\mathrm{APP}\longrightarrow\text{lectura de fase TRIT}
\longrightarrow\text{emisión finita TPK con registro}
\longrightarrow U_6\longrightarrow\Psi(U_6).
\]

La prolongación posterior \(w_6\to w_{12}\to w_{18}\to w_{24}\to w_{30}\to R_{36}\to G_9\), sus lectores y la estructura discreta conjunta del continuo conservan su lugar en el árbol. Aquí no se evalúan constantes ni se seleccionan semillas por valores objetivo. Las constantes correlacionadas \((\pi,\varphi,e,\alpha)\) pertenecen a publicaciones coinductivas posteriores dentro de esa genealogía; ninguna interviene como entrada en esta traza.

**Estatuto:** `RESULTADO_RECUPERADO` para la recurrencia y su factorización, que ya están en el artículo; `CERTIFICADO_NUEVO` para la traza tabulada, sus archivos de datos y su cotejo focal reproducible. No se atribuye novedad a la emisión original.

## 21.1. Procedencia y correspondencia con el árbol conservado

La fuente primaria es la edición sucesora del artículo X, no el documento antiguo U007.

| Operación desplegada | Identificadores previos | Fuente primaria |
|---|---|---|
| Dos cursores orientados y enumeración de condiciones | SR-001–SR-003; LRG.1.1–LRG.1.5 | X, `extension.tex`, líneas 8–18 |
| Lectura de fase, lectura anterior al movimiento e inversión | SR-004; LRG.2.1.1, LRG.2.3–LRG.2.6 | X, `extension.tex`, línea 20 |
| Logaritmo discreto y registro del sector radical | SR-005; LRG.2.1.2–LRG.2.1.3 | X, `extension.tex`, líneas 22–27 |
| Acumulación por ventana y seis emisiones | SR-006–SR-007; LRG.2.2, LRG.2.7–LRG.2.8 | X, `extension.tex`, líneas 29–37 |
| Factorización y recuperación de firmas | SR-008; LRG.3.2 | X, `extension.tex`, líneas 39–43, 51–64 |
| Fibras de condiciones y reducción ternaria | SR-009–SR-011; LRG.3.3–LRG.3.4 | X, `extension.tex`, líneas 44–64 |
| Registro entero, proyección finita y recuperación | SR-012; LRG.1.5 | `TPKTransport.lean`, líneas 75–122; `CommonComposition.lean`, líneas 43–86 |

Rutas absolutas:

- Fuente matemática: [extension.tex](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/extension.tex:8>).
- Implementación propietaria: [verificar_catalogo_app.py](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/supplement/emission/verificar_catalogo_app.py:18>).
- Cotejo por firmas del propietario: [verify_signatures.py](</Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/supplement/emission/verify_signatures.py>).
- Árbol anterior intacto: [12_LECTURA_RAPIDA_Y_GENERACION.md](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV02_ARBOL/12_LECTURA_RAPIDA_Y_GENERACION.md>).
- Fichas anteriores intactas: [02_SEMILLAS_REGIONES_R36.md](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/02_SEMILLAS_REGIONES_R36.md>).
- Cantera histórica complementaria, ya leída en REV02: [U007_semillas_emisor_54.tex](</Users/ruben/Documents/excelencia academica/MONOGRAFIA_INTEGRA_APP_TRIT_TPK_CONSTANTES_2026-08-19/manuscrito/unidades/U007_semillas_emisor_54.tex:109>). Conserva la misma sucesión de lectura, movimiento, acumulación e inversión; su contador neutral \(T_r\) corresponde al \(Z_m\) de la fuente actual. No reemplaza la fuente sucesora.

## 21.2. Contrato paramétrico del emisor

### 21.2.1. Estado inicial y coordenadas

Un cursor finito pertenece a

\[
\mathcal S=\{0,\ldots,8\}^2\times\{N,E,S,O\},\qquad|\mathcal S|=324.
\]

El emisor recibe una pareja ordenada de cursores, uno por hoja: \(\mathcal S_+\times\mathcal S_\times\). Las direcciones tienen los vectores

\[
v_N=(-1,0),\quad v_E=(0,1),\quad v_S=(1,0),\quad v_O=(0,-1).
\]

Para registrar el cruce de frontera se mantiene un levantamiento entero \((x,y;d)\in\mathbb Z^2\times\{N,E,S,O\}\). Su carta finita es \((i,j)=([x]_9,[y]_9)\), y las etiquetas positivas son \((a,b)=(i+1,j+1)\). También se conservan las vueltas

\[
x=9\left\lfloor x/9\right\rfloor+[x]_9,\qquad
y=9\left\lfloor y/9\right\rfloor+[y]_9.
\]

El cociente espacial de esta igualdad y el cociente aritmético de una evaluación APP son registros diferentes. Se denominan `winding_x/winding_y` y `quotient` respectivamente en los datos.

### 21.2.2. Lecturas APP y sector multiplicativo

Sobre cada carta positiva se calculan antes de mover los cursores:

\[
A_+(a,b)=a+b,\qquad A_\times(a,b)=ab,
\]

\[
\rho_9(n)=1+[(n-1)]_9,\qquad q_9(n)=\left\lfloor\frac{n-1}{9}\right\rfloor,
\qquad n=\rho_9(n)+9q_9(n).
\]

El registro conserva el bruto \(n\), el residuo positivo y el cociente. El emisor aditivo lee \(\rho_9(A_+)\). El multiplicativo lee el observable

\[
\ell_9(1,2,4,8,7,5)=(0,1,2,3,4,5),\qquad
\ell_9(3)=\ell_9(6)=\ell_9(9)=0.
\]

La segunda igualdad extiende el observable fuera del grupo de unidades. El valor cero de ese observable no identifica el residuo \(1\) con \(3,6,9\): el residuo original, la hoja y el indicador de pertenencia al grupo de unidades siguen presentes. En esta traza, por ejemplo, el paso 3 registra residuo multiplicativo 9 y el paso 1 registra residuo 1; ambos tienen lectura \(\ell_9=0\).

### 21.2.3. Orden de cada transición

Se comienza en fase cero del calendario \(C_{108}\). Para \(t=1,\ldots,54\),

\[
g_t=1+[(t-1)]_9,\qquad
\epsilon_t=
\begin{cases}
+1,&g_t\in\{1,4,7\},\\
-1,&g_t\in\{2,5,8\},\\
0,&g_t\in\{3,6,9\}.
\end{cases}
\]

Cada transición ejecuta, en este orden:

1. Conservar el estado previo de los dos cursores y su fase.
2. Evaluar ambas lecturas APP en esas posiciones previas.
3. Añadir a los acumuladores sólo la lectura activa: residuo aditivo si \(\epsilon_t=+1\), exponente multiplicativo si \(\epsilon_t=-1\), o una unidad al contador neutral si \(\epsilon_t=0\).
4. Desplazar solamente el cursor activo; el evento neutral no desplaza ninguno.
5. Si \(t=27\) o \(54\), invertir ambas orientaciones cardinales.
6. Avanzar la fase y añadir el registro de esta transición al archivo.
7. Al completar nueve transiciones, emitir un bloque; al comenzar la ventana siguiente, reiniciar únicamente los tres acumuladores locales, no posiciones, orientaciones, fase ni archivo.

Al escribir \(c=(z,d)\), con \(z\in\mathbb Z^2\), \(a\in\{0,1\}\) indicador de activación y \(b\in\{0,1\}\) indicador de inversión, la regla es

\[
F_{a,b}(z,d)=\bigl(z+a\,v_d,\operatorname{opp}^{\,b}(d)\bigr).
\]

La fase previa determina \(a,b\); no se recuperan estos indicadores desde una cifra emitida.

### 21.2.4. Acumuladores y emisión

En la ventana \(m\), de pasos \(9m-8,\ldots,9m\), se inicializan \(S=E=Z=0\). Cada ventana contiene tres eventos de cada régimen, por lo que \(Z_m=3\). El bloque decimal es

\[
\begin{aligned}
d_{m,1}&=[S_m]_{10},\\
d_{m,2}&=[S_m+E_m]_{10},\\
d_{m,3}&=[3S_m+5E_m+7Z_m]_{10},\\
U_m&=100d_{m,1}+10d_{m,2}+d_{m,3}.
\end{aligned}
\]

Los pesos \(3,5,7\), el calendario de 9 y 54 transiciones y la tabla \(\ell_9\) son los datos explícitos de la ley propietaria aquí reproducida. Este bloque no inventa una derivación nueva de esos coeficientes ni los ajusta a una constante. Su procedencia inmediata queda fijada en la fuente y en los propietarios.

## 21.3. Condición inicial seleccionada antes de ejecutar

Se ordenan las semillas por

\[
\nu(i,j,d)=4(9i+j)+\operatorname{ind}(d),\qquad
\operatorname{ind}(N,E,S,O)=(0,1,2,3).
\]

La pareja se enumera mediante \(324\nu_++\nu_\times\). Elegimos su primer elemento:

\[
\nu_+=\nu_\times=0,\qquad
c_{+,0}=c_{\times,0}=(0,0;N),\qquad p_0=0,\qquad \mathcal M_0=\varnothing.
\]

La carta positiva de ambos cursores es \((1,1)\). No se eligió una región numérica reconocida, una órbita asociada a una constante ni un valor metrológico.

## 21.4. Traza íntegra de transporte

En las tablas \((x,y;d)\) son coordenadas enteras levantadas, no índices ya reducidos. La fase previa es \(t-1\), la posterior \(t\); la longitud del archivo al terminar cada fila es exactamente \(t\). Las 54 filas conservan ambas posiciones antes y después. Las inversiones se aplican al finalizar las filas 27 y 54.

| Paso | Ventana | Régimen | Cursor + anterior | Cursor × anterior | Cursor + posterior | Cursor × posterior | Inversión final |
|---:|---:|:---:|---|---|---|---|:---:|
| 1 | 1 | + | (0,0;N) | (0,0;N) | (-1,0;N) | (0,0;N) | — |
| 2 | 1 | - | (-1,0;N) | (0,0;N) | (-1,0;N) | (-1,0;N) | — |
| 3 | 1 | 0 | (-1,0;N) | (-1,0;N) | (-1,0;N) | (-1,0;N) | — |
| 4 | 1 | + | (-1,0;N) | (-1,0;N) | (-2,0;N) | (-1,0;N) | — |
| 5 | 1 | - | (-2,0;N) | (-1,0;N) | (-2,0;N) | (-2,0;N) | — |
| 6 | 1 | 0 | (-2,0;N) | (-2,0;N) | (-2,0;N) | (-2,0;N) | — |
| 7 | 1 | + | (-2,0;N) | (-2,0;N) | (-3,0;N) | (-2,0;N) | — |
| 8 | 1 | - | (-3,0;N) | (-2,0;N) | (-3,0;N) | (-3,0;N) | — |
| 9 | 1 | 0 | (-3,0;N) | (-3,0;N) | (-3,0;N) | (-3,0;N) | — |
| 10 | 2 | + | (-3,0;N) | (-3,0;N) | (-4,0;N) | (-3,0;N) | — |
| 11 | 2 | - | (-4,0;N) | (-3,0;N) | (-4,0;N) | (-4,0;N) | — |
| 12 | 2 | 0 | (-4,0;N) | (-4,0;N) | (-4,0;N) | (-4,0;N) | — |
| 13 | 2 | + | (-4,0;N) | (-4,0;N) | (-5,0;N) | (-4,0;N) | — |
| 14 | 2 | - | (-5,0;N) | (-4,0;N) | (-5,0;N) | (-5,0;N) | — |
| 15 | 2 | 0 | (-5,0;N) | (-5,0;N) | (-5,0;N) | (-5,0;N) | — |
| 16 | 2 | + | (-5,0;N) | (-5,0;N) | (-6,0;N) | (-5,0;N) | — |
| 17 | 2 | - | (-6,0;N) | (-5,0;N) | (-6,0;N) | (-6,0;N) | — |
| 18 | 2 | 0 | (-6,0;N) | (-6,0;N) | (-6,0;N) | (-6,0;N) | — |
| 19 | 3 | + | (-6,0;N) | (-6,0;N) | (-7,0;N) | (-6,0;N) | — |
| 20 | 3 | - | (-7,0;N) | (-6,0;N) | (-7,0;N) | (-7,0;N) | — |
| 21 | 3 | 0 | (-7,0;N) | (-7,0;N) | (-7,0;N) | (-7,0;N) | — |
| 22 | 3 | + | (-7,0;N) | (-7,0;N) | (-8,0;N) | (-7,0;N) | — |
| 23 | 3 | - | (-8,0;N) | (-7,0;N) | (-8,0;N) | (-8,0;N) | — |
| 24 | 3 | 0 | (-8,0;N) | (-8,0;N) | (-8,0;N) | (-8,0;N) | — |
| 25 | 3 | + | (-8,0;N) | (-8,0;N) | (-9,0;N) | (-8,0;N) | — |
| 26 | 3 | - | (-9,0;N) | (-8,0;N) | (-9,0;N) | (-9,0;N) | — |
| 27 | 3 | 0 | (-9,0;N) | (-9,0;N) | (-9,0;S) | (-9,0;S) | sí |
| 28 | 4 | + | (-9,0;S) | (-9,0;S) | (-8,0;S) | (-9,0;S) | — |
| 29 | 4 | - | (-8,0;S) | (-9,0;S) | (-8,0;S) | (-8,0;S) | — |
| 30 | 4 | 0 | (-8,0;S) | (-8,0;S) | (-8,0;S) | (-8,0;S) | — |
| 31 | 4 | + | (-8,0;S) | (-8,0;S) | (-7,0;S) | (-8,0;S) | — |
| 32 | 4 | - | (-7,0;S) | (-8,0;S) | (-7,0;S) | (-7,0;S) | — |
| 33 | 4 | 0 | (-7,0;S) | (-7,0;S) | (-7,0;S) | (-7,0;S) | — |
| 34 | 4 | + | (-7,0;S) | (-7,0;S) | (-6,0;S) | (-7,0;S) | — |
| 35 | 4 | - | (-6,0;S) | (-7,0;S) | (-6,0;S) | (-6,0;S) | — |
| 36 | 4 | 0 | (-6,0;S) | (-6,0;S) | (-6,0;S) | (-6,0;S) | — |
| 37 | 5 | + | (-6,0;S) | (-6,0;S) | (-5,0;S) | (-6,0;S) | — |
| 38 | 5 | - | (-5,0;S) | (-6,0;S) | (-5,0;S) | (-5,0;S) | — |
| 39 | 5 | 0 | (-5,0;S) | (-5,0;S) | (-5,0;S) | (-5,0;S) | — |
| 40 | 5 | + | (-5,0;S) | (-5,0;S) | (-4,0;S) | (-5,0;S) | — |
| 41 | 5 | - | (-4,0;S) | (-5,0;S) | (-4,0;S) | (-4,0;S) | — |
| 42 | 5 | 0 | (-4,0;S) | (-4,0;S) | (-4,0;S) | (-4,0;S) | — |
| 43 | 5 | + | (-4,0;S) | (-4,0;S) | (-3,0;S) | (-4,0;S) | — |
| 44 | 5 | - | (-3,0;S) | (-4,0;S) | (-3,0;S) | (-3,0;S) | — |
| 45 | 5 | 0 | (-3,0;S) | (-3,0;S) | (-3,0;S) | (-3,0;S) | — |
| 46 | 6 | + | (-3,0;S) | (-3,0;S) | (-2,0;S) | (-3,0;S) | — |
| 47 | 6 | - | (-2,0;S) | (-3,0;S) | (-2,0;S) | (-2,0;S) | — |
| 48 | 6 | 0 | (-2,0;S) | (-2,0;S) | (-2,0;S) | (-2,0;S) | — |
| 49 | 6 | + | (-2,0;S) | (-2,0;S) | (-1,0;S) | (-2,0;S) | — |
| 50 | 6 | - | (-1,0;S) | (-2,0;S) | (-1,0;S) | (-1,0;S) | — |
| 51 | 6 | 0 | (-1,0;S) | (-1,0;S) | (-1,0;S) | (-1,0;S) | — |
| 52 | 6 | + | (-1,0;S) | (-1,0;S) | (0,0;S) | (-1,0;S) | — |
| 53 | 6 | - | (0,0;S) | (-1,0;S) | (0,0;S) | (0,0;S) | — |
| 54 | 6 | 0 | (0,0;S) | (0,0;S) | (0,0;N) | (0,0;N) | sí |

A los 27 pasos los cursores están en \((-9,0;S)\), cuya proyección finita es \((0,0;S)\), y la fase es 27. A los 54 vuelven a \((0,0;N)\), pero la fase es 54 y el archivo tiene 54 registros. La igualdad de posiciones y orientaciones con el inicio no es igualdad del estado enriquecido registrado.

## 21.5. Traza íntegra de lecturas y acumulación

En cada columna de lectura se escribe `bruto; residuo positivo; cociente aritmético`. Todas las lecturas son anteriores al movimiento, incluidas las del cursor inactivo. La columna de incremento muestra cuál interviene efectivamente. El acumulador previo \((0,0,0)\) de los pasos 10, 19, 28, 37 y 46 sólo inaugura una nueva ventana local.

| Paso | Lectura +: bruto; residuo; cociente | Lectura ×: bruto; residuo; cociente | ℓ₉ de × | Incremento (S,E,Z) | Acumuladores previos | Acumuladores posteriores |
|---:|---|---|---:|---|---|---|
| 1 | 2;2;0 | 1;1;0 | 0 | (2,0,0) | (0,0,0) | (2,0,0) |
| 2 | 10;1;1 | 1;1;0 | 0 | (0,0,0) | (2,0,0) | (2,0,0) |
| 3 | 10;1;1 | 9;9;0 | 0 | (0,0,1) | (2,0,0) | (2,0,1) |
| 4 | 10;1;1 | 9;9;0 | 0 | (1,0,0) | (2,0,1) | (3,0,1) |
| 5 | 9;9;0 | 9;9;0 | 0 | (0,0,0) | (3,0,1) | (3,0,1) |
| 6 | 9;9;0 | 8;8;0 | 3 | (0,0,1) | (3,0,1) | (3,0,2) |
| 7 | 9;9;0 | 8;8;0 | 3 | (9,0,0) | (3,0,2) | (12,0,2) |
| 8 | 8;8;0 | 8;8;0 | 3 | (0,3,0) | (12,0,2) | (12,3,2) |
| 9 | 8;8;0 | 7;7;0 | 4 | (0,0,1) | (12,3,2) | (12,3,3) |
| 10 | 8;8;0 | 7;7;0 | 4 | (8,0,0) | (0,0,0) | (8,0,0) |
| 11 | 7;7;0 | 7;7;0 | 4 | (0,4,0) | (8,0,0) | (8,4,0) |
| 12 | 7;7;0 | 6;6;0 | 0 | (0,0,1) | (8,4,0) | (8,4,1) |
| 13 | 7;7;0 | 6;6;0 | 0 | (7,0,0) | (8,4,1) | (15,4,1) |
| 14 | 6;6;0 | 6;6;0 | 0 | (0,0,0) | (15,4,1) | (15,4,1) |
| 15 | 6;6;0 | 5;5;0 | 5 | (0,0,1) | (15,4,1) | (15,4,2) |
| 16 | 6;6;0 | 5;5;0 | 5 | (6,0,0) | (15,4,2) | (21,4,2) |
| 17 | 5;5;0 | 5;5;0 | 5 | (0,5,0) | (21,4,2) | (21,9,2) |
| 18 | 5;5;0 | 4;4;0 | 2 | (0,0,1) | (21,9,2) | (21,9,3) |
| 19 | 5;5;0 | 4;4;0 | 2 | (5,0,0) | (0,0,0) | (5,0,0) |
| 20 | 4;4;0 | 4;4;0 | 2 | (0,2,0) | (5,0,0) | (5,2,0) |
| 21 | 4;4;0 | 3;3;0 | 0 | (0,0,1) | (5,2,0) | (5,2,1) |
| 22 | 4;4;0 | 3;3;0 | 0 | (4,0,0) | (5,2,1) | (9,2,1) |
| 23 | 3;3;0 | 3;3;0 | 0 | (0,0,0) | (9,2,1) | (9,2,1) |
| 24 | 3;3;0 | 2;2;0 | 1 | (0,0,1) | (9,2,1) | (9,2,2) |
| 25 | 3;3;0 | 2;2;0 | 1 | (3,0,0) | (9,2,2) | (12,2,2) |
| 26 | 2;2;0 | 2;2;0 | 1 | (0,1,0) | (12,2,2) | (12,3,2) |
| 27 | 2;2;0 | 1;1;0 | 0 | (0,0,1) | (12,3,2) | (12,3,3) |
| 28 | 2;2;0 | 1;1;0 | 0 | (2,0,0) | (0,0,0) | (2,0,0) |
| 29 | 3;3;0 | 1;1;0 | 0 | (0,0,0) | (2,0,0) | (2,0,0) |
| 30 | 3;3;0 | 2;2;0 | 1 | (0,0,1) | (2,0,0) | (2,0,1) |
| 31 | 3;3;0 | 2;2;0 | 1 | (3,0,0) | (2,0,1) | (5,0,1) |
| 32 | 4;4;0 | 2;2;0 | 1 | (0,1,0) | (5,0,1) | (5,1,1) |
| 33 | 4;4;0 | 3;3;0 | 0 | (0,0,1) | (5,1,1) | (5,1,2) |
| 34 | 4;4;0 | 3;3;0 | 0 | (4,0,0) | (5,1,2) | (9,1,2) |
| 35 | 5;5;0 | 3;3;0 | 0 | (0,0,0) | (9,1,2) | (9,1,2) |
| 36 | 5;5;0 | 4;4;0 | 2 | (0,0,1) | (9,1,2) | (9,1,3) |
| 37 | 5;5;0 | 4;4;0 | 2 | (5,0,0) | (0,0,0) | (5,0,0) |
| 38 | 6;6;0 | 4;4;0 | 2 | (0,2,0) | (5,0,0) | (5,2,0) |
| 39 | 6;6;0 | 5;5;0 | 5 | (0,0,1) | (5,2,0) | (5,2,1) |
| 40 | 6;6;0 | 5;5;0 | 5 | (6,0,0) | (5,2,1) | (11,2,1) |
| 41 | 7;7;0 | 5;5;0 | 5 | (0,5,0) | (11,2,1) | (11,7,1) |
| 42 | 7;7;0 | 6;6;0 | 0 | (0,0,1) | (11,7,1) | (11,7,2) |
| 43 | 7;7;0 | 6;6;0 | 0 | (7,0,0) | (11,7,2) | (18,7,2) |
| 44 | 8;8;0 | 6;6;0 | 0 | (0,0,0) | (18,7,2) | (18,7,2) |
| 45 | 8;8;0 | 7;7;0 | 4 | (0,0,1) | (18,7,2) | (18,7,3) |
| 46 | 8;8;0 | 7;7;0 | 4 | (8,0,0) | (0,0,0) | (8,0,0) |
| 47 | 9;9;0 | 7;7;0 | 4 | (0,4,0) | (8,0,0) | (8,4,0) |
| 48 | 9;9;0 | 8;8;0 | 3 | (0,0,1) | (8,4,0) | (8,4,1) |
| 49 | 9;9;0 | 8;8;0 | 3 | (9,0,0) | (8,4,1) | (17,4,1) |
| 50 | 10;1;1 | 8;8;0 | 3 | (0,3,0) | (17,4,1) | (17,7,1) |
| 51 | 10;1;1 | 9;9;0 | 0 | (0,0,1) | (17,7,1) | (17,7,2) |
| 52 | 10;1;1 | 9;9;0 | 0 | (1,0,0) | (17,7,2) | (18,7,2) |
| 53 | 2;2;0 | 9;9;0 | 0 | (0,0,0) | (18,7,2) | (18,7,2) |
| 54 | 2;2;0 | 1;1;0 | 0 | (0,0,1) | (18,7,2) | (18,7,3) |

Ejemplo del cruce y del cociente: antes del paso 4 el cursor aditivo está en \((-1,0;N)\), cuya carta positiva es \((9,1)\). El bruto aditivo es \(10=1+9\cdot1\). Se añade 1 al acumulador, no 10; ambos enteros y el cociente permanecen registrados. Después se mueve a \((-2,0;N)\). El cociente espacial antes de mover es \(\lfloor-1/9\rfloor=-1\), distinto del cociente aritmético 1 de la lectura.

## 21.6. Las seis emisiones, sin cifras prefijadas

| Ventana | Pasos | S | E | Z | s | e | Tres cifras | U | Ψ(U) |
|---:|---|---:|---:|---:|---:|---:|---|---:|---:|
| 1 | 1–9 | 12 | 3 | 3 | 2 | 3 | 2,5,2 | 252 | 0 |
| 2 | 10–18 | 21 | 9 | 3 | 1 | 9 | 1,0,9 | 109 | 2 |
| 3 | 19–27 | 12 | 3 | 3 | 2 | 3 | 2,5,2 | 252 | 0 |
| 4 | 28–36 | 9 | 1 | 3 | 9 | 1 | 9,0,3 | 903 | 0 |
| 5 | 37–45 | 18 | 7 | 3 | 8 | 7 | 8,5,0 | 850 | 2 |
| 6 | 46–54 | 18 | 7 | 3 | 8 | 7 | 8,5,0 | 850 | 2 |

La salida calculada es

\[
U_6=(252,109,252,903,850,850),
\]

\[
s=(2,1,2,9,8,8),\qquad e_{\rm sig}=(3,9,3,1,7,7).
\]

El símbolo \(e_{\rm sig}\) es aquí una firma de exponentes discretos; no es la constante exponencial. Se distingue de ella en este documento para evitar una colisión de nombres.

## 21.7. Factorización, recuperación y fibras exactas

### 21.7.1. Qué recupera el sexteto emitido

Como \(Z_m=3\), \(7Z_m\equiv1\pmod{10}\). Por tanto

\[
G(s,e)=100s+10[s+e]_{10}+[3s+5e+1]_{10}
\]

produce el bloque desde las dos firmas reducidas. Si \(U=100a+10b+c\) está en su imagen,

\[
s=a,\qquad e=[b-a]_{10},\qquad c=[3s+5e+1]_{10}.
\]

Esto prueba que \(G\) es inyectivo en los pares de firmas. No prueba que el mapa de condiciones iniciales a firmas sea inyectivo ni recupera los totales no reducidos \(S_m,E_m\) sin registro adicional.

En la primera ventana, por ejemplo, \(S_1=12\) y la centena de \(252\) recupera \(s_1=2\), no 12. El total exacto se obtiene sumando las lecturas archivadas.

### 21.7.2. Fibra de la emisión elegida

Aplicar el emisor propietario a las 324 semillas de cada hoja produce 18 firmas aditivas y 26 multiplicativas. Para la emisión calculada, las preimágenes individuales son exactamente:

\[
\begin{aligned}
F_+={}&\{0,3,68,71,100,103,132,135,164,167,\\
&196,199,228,231,260,263,292,295\},\\
F_\times={}&\{0,3,5,38,244,279,281,282\}.
\end{aligned}
\]

La fibra completa es el producto cartesiano \(F_+\times F_\times\), de cardinal \(18\cdot8=144\). No es una mera cota: cada uno de los 144 pares se ha vuelto a ejecutar con la implementación conjunta propietaria y produce el sexteto elegido. La inyectividad de \(G\) y la enumeración íntegra de cada hoja excluyen cualquier otra preimagen.

El JSON y el TSV de fibra enumeran individualmente esos 144 pares y su identificador \(324\nu_++\nu_\times\). La fórmula cartesiana conserva también la lista completa sin perder elementos.

### 21.7.3. Censo finito por factorización

La comprobación focal enumera 648 trayectorias de un cursor, no una campaña nueva de las 104976 trayectorias conjuntas. Después compone las \(18\cdot26\) parejas de firmas. El histograma es

\[
18\text{ fibras aditivas de }18;
\quad24\text{ fibras multiplicativas de }8,\quad
1\text{ de }24,\quad1\text{ de }108.
\]

Se obtienen 468 emisiones distintas, con

\[
432\text{ fibras de }144,\quad18\text{ de }432,\quad18\text{ de }1944,
\]

\[
432\cdot144+18\cdot432+18\cdot1944=104976.
\]

La fuente propietaria contiene además una campaña exhaustiva conjunta; no se declara repetida en esta iteración. Lo ejecutado aquí es el cotejo del caso completo, las 144 condiciones de su fibra y el censo por firmas.

## 21.8. La reducción ternaria es una lectura adicional

El mapa orientado se aplica componente a componente:

\[
\Psi:\mathcal U_6\longrightarrow\mathbb F_3^6,\qquad
\Psi(U_6)=([-U_1]_3,\ldots,[-U_6]_3).
\]

No convierte un entero decimal de dieciocho cifras en su expansión de base tres. Lee por separado los seis bloques. Para el caso calculado,

\[
\Psi(252,109,252,903,850,850)=(0,2,0,0,2,2).
\]

La identificación balanceada posterior \(0\mapsto0,1\mapsto+1,2\mapsto-1\) da \((0,-1,0,0,-1,-1)\). Esta lectura no debe confundirse con el calendario \((+1,-1,0)^3\) que gobernó los movimientos.

En el catálogo de 468 emisiones, la fibra de la palabra concreta \(020022\) contiene un solo sexteto: el elegido. Por ello sería falso afirmar que en este ejemplo \(\Psi\) identifica dos sextetos distintos. Sí hay 144 condiciones iniciales detrás de él.

Globalmente, \(\Psi\) tiene 243 imágenes en el ambiente de \(3^6=729\) palabras y no es inyectiva. Un testigo reproducible, elegido después de generar el catálogo por ser la primera palabra lexicográfica con al menos dos emisiones, es

\[
\begin{aligned}
U&=(498,501,614,252,252,109),\\
U'&=(870,810,923,252,252,109),\\
U&\ne U',\qquad \Psi(U)=\Psi(U')=(0,0,1,0,0,2).
\end{aligned}
\]

Cada uno de esos sextetos tiene multiplicidad 144. Este testigo no altera la condición inicial de la traza de 54 pasos ni introduce otra selección por una constante.

La cadena de mapas es, con sus tipos,

\[
\Omega_{\rm seed}\xrightarrow{(s,e_{\rm sig})}
\mathcal S_{\rm sig}\times\mathcal E_{\rm sig}
\xrightarrow[\text{inyectivo}]{G^{\times6}}
\mathcal U_6
\xrightarrow{\Psi}\operatorname{im}\Psi\subset\mathbb F_3^6.
\]

El registro ordenado se conserva en el estado emisor y sus ejecuciones; no se atribuye a \(\Psi(U)\) la información eliminada por las proyecciones anteriores. Mantener \(U_6\) como publicación adicional tampoco identifica \(U_6\) con todo el archivo.

## 21.9. Recuperación local y conservación del archivo

### Proposición 21-A. Inversión del transporte local

Para indicadores conocidos \(a,b\), la inversa de \(F_{a,b}\) es

\[
F_{a,b}^{-1}(z',d')
=\bigl(z'-a\,v_{\operatorname{opp}^{\,b}(d')},
       \operatorname{opp}^{\,b}(d')\bigr).
\]

**Demostración.** La oposición aplicada dos veces devuelve la orientación inicial. Por ello se recupera primero la dirección anterior a la inversión, y se sustrae exactamente el vector que se había añadido. La fase anterior se obtiene desde la posterior por la operación inversa del calendario. No se necesita deducir la dirección desde el residuo de una lectura. El script comprueba ambas recuperaciones cursor a cursor en las 54 transiciones. Los teoremas paramétricos propietarios ya están en Lean.

### Proposición 21-B. Proyección finita compatible

Reducir las coordenadas del transporte entero módulo nueve da el transporte finito del emisor. En efecto,

\[
[z+a\,v_d]_9=[[z]_9+a\,v_d]_9.
\]

La inversión afecta a la dirección y conmuta con la reducción espacial. Las lecturas APP usan precisamente la carta positiva de esa reducción. En consecuencia, la traza entera y la recurrencia finita producen las mismas lecturas activas y las mismas emisiones; la primera conserva además las vueltas espaciales.

### Proposición 21-C. Archivo y concatenación

Sea \(\mathsf{Sample}(q)\) el estado previo y sus evaluaciones tipadas. La ejecución registrada aplica

\[
(q,\mathcal M)\longmapsto
(Fq,\mathcal M\,\Vert\,\mathsf{Sample}(q)).
\]

Por inducción en \(n\),

\[
\mathcal M_n=\mathcal M_0\,\Vert\,
\bigl(\mathsf{Sample}(q_0),\ldots,\mathsf{Sample}(q_{n-1})\bigr),
\qquad|\mathcal M_n|=|\mathcal M_0|+n.
\]

La recurrencia determinista genera los estados intermedios y sus lecturas. El archivo se obtiene ejecutando esa recurrencia, no suponiendo una lista arbitraria que deba recuperarse. Los acumuladores son pliegues sobre segmentos de nueve registros: reiniciarlos para el siguiente segmento no borra los segmentos anteriores. La suma sobre una concatenación es la suma de sus dos segmentos; de ahí se recuperan los totales exactos, las firmas y los bloques en el orden correspondiente.

El contrato archivístico especifica qué conserva la implementación; por sí solo no pretende convertir una proyección no inyectiva en una codificación sin pérdida de todo el estado.

## 21.10. Contratos para la transcripción LaTeX y Lean

La futura transcripción no necesita reinventar las operaciones ya formalizadas. Los siguientes son nombres existentes, leídos en sus fuentes; esta iteración no recompila Lean ni presenta el script Python como prueba Lean.

| Contrato | Propietario y localizador | Estado |
|---|---|---|
| Evaluación positiva = residuo + nueve veces cociente | `APPArithmetic.reconstruct`, línea 40; `reconstruct_sum/product`, 115–125 | Teoremas existentes |
| Carta positiva de una coordenada entera | `CommonComposition.cursor_positive_chart`, 47; `cursor_mark_periodic`, 53 | Teoremas existentes |
| Recuperación de las evaluaciones de cada visita | `CommonComposition.every_visit_reconstructs`, 83 | Teorema existente |
| Transporte e inversa de cursores | `TPKTransport.cursor_unstep_step`, 91; `cursor_step_unstep`, 97 | Teoremas existentes |
| Transporte e inversa del estado observable | `TPKTransport.unstep_step/step_unstep`, 118–125 | Teoremas existentes |
| Lectura anterior al movimiento | `TPKEmission.emitStep_reads_before`, 98 | Teorema existente |
| Tres eventos de cada clase por ventana | `TPKEmission.every_nine_window`, 204 | Teorema existente |
| Fórmula decimal y recuperación de firmas | `TPKEmission.block_source_formula`, 243; `block_recovers_signatures`, 256 | Teoremas existentes |
| Palabra de seis bloques = codificación de las dos firmas | `TPKEmission.word_as_encodeWord`, 271 | Teorema existente |
| Recuperación de firmas desde la palabra | `TPKEmission.word_recovers_signatures`, 276 | Teorema existente |
| Concatenación de memoria | `TPKEmission.execution_concatenates`, 151 | Teorema existente |
| Seis ventanas son 54 pasos y conservan 54 muestras | `TPKEmission.six_windows_fiftyfour`, 352; `six_windows_memory`, 358 | Teoremas existentes |
| Igualdad computada de este caso con \(252,109,252,903,850,850\) | `21_verificar_emisor_traza.py`, función `main` | Comprobación exacta Python; especialización Lean aún no añadida |
| Fibra exacta de 144 condiciones y testigo de no inyectividad de \(\Psi\) | JSON/TSV y comparación propietaria | Comprobación finita exacta; no nueva formalización Lean |

Fuentes Lean:

- [APPArithmetic.lean](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/APPArithmetic.lean:24>).
- [CommonComposition.lean](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/CommonComposition.lean:43>).
- [TPKTransport.lean](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKTransport.lean:81>).
- [TPKEmission.lean](</Users/ruben/Documents/New project/output/AMPLIACION_FORMAL_LEAN_SERIE_20260916/formalization/TPKEmission.lean:95>).

Para trasladar el caso se deben declarar los dos cursores enteros, sus direcciones y la fase cero; especializar la ejecución de 54 muestras; demostrar la lista concreta de bloques; y sólo después aplicar la definición de \(\Psi\). No se debe reemplazar la ejecución por una lista literal usada como supuesto.

## 21.11. Reproducción y controles de alteración

Ejecutar:

```bash
python3 -I -S "/Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/21_verificar_emisor_traza.py"
```

El programa importa únicamente las definiciones del propietario y llama a `direct_u6`, `channel_signature`, `combine`, `recover_signatures` y `w6`. No ejecuta `owner.main()`, no abre el catálogo arquimediano y no lee su etiqueta de región para elegir el ejemplo.

Comprueba:

1. Cincuenta y cuatro transiciones enlazadas y archivo de longitud 54.
2. Tres eventos por régimen en cada ventana; inversiones exactamente en 27 y 54.
3. Reconstrucción de las evaluaciones brutas desde residuo y cociente.
4. Inversión de cada transición de cada cursor.
5. Coincidencia del caso con la ejecución conjunta propietaria.
6. Coincidencia independiente con las dos firmas y su acoplamiento.
7. Recuperación de las firmas desde el sexteto.
8. Enumeración de las firmas de cada hoja y de sus fibras.
9. Reejecución directa de las 144 condiciones de la fibra seleccionada.
10. Reducción ternaria, fibra concreta y testigo global de no inyectividad.

Dos controles negativos introducen alteraciones explícitas en copias de cálculo, sin cambiar el propietario:

\[
\text{lectura después de mover}\ \longmapsto\
(850,850,903,252,109,252),
\]

\[
\text{signo positivo en lugar de negativo para }\Psi
\ \longmapsto\ 010011\ne020022.
\]

Son pruebas de sensibilidad a esas dos alteraciones, no una batería exhaustiva de todos los errores posibles. En particular, como los pasos 27 y 54 son neutrales, desplazar una inversión dentro de ese mismo paso exige comparar el registro orientado; no se presupone que necesariamente cambien los seis bloques.

## 21.12. Archivos y límites de lectura

- [Script focal](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/21_verificar_emisor_traza.py>).
- [JSON íntegro de la traza, las seis ventanas, las fibras y los controles](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/21_TRAZA_EMISOR_54.json>).
- [TSV de las 54 transiciones, con cartas, vueltas, evaluaciones y acumuladores](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/21_TRAZA_EMISOR_54.tsv>).
- [TSV de los 144 pares de condiciones iniciales](</Users/ruben/Documents/New project/output/INVENTARIO_GENEALOGICO_HMT_20260919/REV03_PASOS_Y_CONTRATOS/21_FIBRA_144_CONDICIONES.tsv>).

Lecturas materiales focales de esta iteración:

- `extension.tex`: íntegro, 188 líneas; el tramo utilizado para este emisor es 8–64.
- `verificar_catalogo_app.py`: íntegro; se emplean las funciones de emisión, no su selección posterior de regiones.
- `verify_signatures.py`: íntegro, como cotejo de la estructura de la verificación propietaria.
- `APPArithmetic.lean`: líneas 1–180 leídas; los nombres posteriores se localizaron, pero no se presentan como lectura íntegra.
- `TPKTransport.lean`: líneas 1–150 leídas; localizadores posteriores consultados sin nueva lectura completa.
- `TPKEmission.lean`: líneas 1–160 y 170–380 leídas; esta iteración no declara lectura íntegra ni recompilación.
- `CommonComposition.lean`: íntegro.
- U007: lectura íntegra conservada de REV02; en REV03 no se ha repetido una lectura integral de la cantera.

El integral completo, las otras canteras, las cinco regiones, los lifts \(L_0/L_1\), el selector \(R_{36}\) y los lectores coinductivos mantienen sus nodos en el inventario global. No se vuelven a desarrollar en este bloque focal ni se declaran ausentes por ello. Tampoco se modificaron REV01, REV02, fuentes de la serie o PDF.

