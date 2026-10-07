# Insuficiencia de la ventana coinductiva finita para seleccionar los ocho bloques

## 1. Planteamiento

Sea

\[
\mathcal S_8=
\{002001,020111,200110,121012,010122,001001,221110,222110\}
\subset\mathbb F_3^6.
\]

El problema no consiste en comprobar que estas ocho palabras aparecen en los
registros. Consiste en determinar si las reglas publicadas de frontera,
calendario nonádico y supervivencia las seleccionan como conjunto antes de
leer la palabra dodecafásica o el sello decimal.

El verificador define primero, sin consultar \(\mathcal S_8\), todas las
familias sometidas a prueba. Sólo después introduce las ocho palabras como
contraste. No abre \(W_{72}\), \(K\), \(U_{12}\), \(\alpha\) ni CODATA.

## 2. Cobertura N69

Para cada una de las cien fronteras N69 se consideran las tres bandas
\(B_{t,1},B_{t,2},B_{t,3}\), la fase

\[
p_t=t-1\pmod3,
\]

y las cargas visible y Witt--dual. La familia comparativa asigna a cada banda
el coeficiente \(+1\) o \(-1\) según coincida su carga con
\(p_t+\delta\), para las tres traslaciones \(\delta\in\mathbb F_3\) y las dos
orientaciones. Sus cardinales son

\[
\#\mathcal C_{mathrm{vis}}=330,
\qquad
\#\mathcal C_{mathrm{W}}=318,
\qquad
\#(\mathcal C_{mathrm{vis}}\cup\mathcal C_{mathrm{W}})=410.
\]

La extensión afín Witt--dual

\[
c_i=\rho_{W,i}+p_t\pmod3
\]

produce \(91\) palabras. La unión total contiene

\[
\#\mathcal O_{69}=442
\]

palabras distintas.

Las ocho palabras de \(\mathcal S_8\) pertenecen a \(\mathcal O_{69}\). Siete
pertenecen ya a la familia comparativa; la única excepción es
\(001001\), obtenida por la extensión afín en \(t=30\). Por tanto, N69
contiene el alfabeto necesario, pero la pertenencia no constituye una
selección. Sin una regla adicional quedan

\[
\binom{442}{8}=33,899,151,336,985,935
\]

subconjuntos de ocho elementos. Esta cuenta no pretende medir la complejidad
de una futura ley natural; demuestra únicamente que el censo de incidencias
no determina por sí solo \(\mathcal S_8\).

## 3. Teorema de imposibilidad para N72

La ventana N72 contiene las puertas

\[
t=5,\ldots,25.
\]

La convención de índices se verifica fila por fila: la salida de la puerta
\(t\) coincide exactamente con la frontera \(B_{t+1}\) de N69. Sobre toda la
ventana, sin aplicar ningún filtro, se obtienen:

\[
\begin{array}{c|c}
\text{fuente}&\text{palabras distintas}\\
\hline
\text{bandas de la rama superviviente}&61\\
\text{lectores comparativos}&114\\
\text{extensión afín Witt--dual}&21\\
\text{unión total}&172
\end{array}
\]

La unión total sólo contiene cuatro palabras de \(\mathcal S_8\):

\[
\mathcal S_8\cap\mathcal O_{72}
=\{010122,020111,221110,222110\}.
\]

Faltan en toda la imagen:

\[
\boxed{
\{001001,002001,121012,200110\}.
}
\]

### Teorema

Ningún selector que opere únicamente restringiendo tiempos, fases,
profundidades de resolución o ramas de la ventana N72 publicada puede
seleccionar \(\mathcal S_8\).

### Demostración

La imagen de cualquier restricción de la ventana es un subconjunto de
\(\mathcal O_{72}\). Las cuatro palabras anteriores no pertenecen a
\(\mathcal O_{72}\). Por tanto ninguna restricción de esa ventana puede tener
imagen \(\mathcal S_8\). \(\square\)

Este resultado no niega el teorema finito de supervivencia N72. N72 sigue
demostrando que las ambigüedades de su dominio se resuelven en profundidad a
lo sumo tres y que la rama distinguida permanece estable hasta nueve
fronteras. Lo que demuestra el teorema anterior es que esa ventana no posee
el dominio suficiente para construir los ocho bloques.

## 4. Por qué el retorno nonádico no completa la ventana

Podría intentarse extender N72 repitiendo su perfil según la fase módulo
nueve. N74 impide exactamente esa operación. En los nueve pares publicados

\[
t\longmapsto t+9
\]

retorna la fase, pero cambian tanto el eje \(\varphi\) como la suma
\(\pi+e\). Así,

\[
g(t+9)=g(t),
\qquad
\mathcal B_{t+9}\ne\mathcal B_t.
\]

La fase no determina la frontera. El retorno conserva una memoria de
acarreo, hoja y orientación. En consecuencia, prolongar N72 por periodicidad
eliminaría precisamente la información que la monodromía conserva.

## 5. El panel de los tres lectores

Los tres lectores coinductivos publican, en sus tres primeras posiciones, un
panel de nueve entradas y ocho palabras distintas:

\[
\begin{aligned}
&010211,012222,010211,\\
&201101,121221,102011,\\
&121200,112202,121020.
\end{aligned}
\]

El panel tiene rango seis sobre \(\mathbb F_3\); por tanto su envolvente
lineal es todo \(\mathbb F_3^6\), de cardinal \(729\). No contiene ninguna
palabra de \(\mathcal S_8\). Su órbita por las seis rotaciones cíclicas sólo
contiene \(020111\); la órbita Witt no contiene ninguna, y la órbita conjunta
rotación--Witt vuelve a contener sólo \(020111\).

El panel es indispensable para cerrar el cilindro decimal posterior, pero no
es un selector del conjunto previo de ocho bloques. Además, la cara
excepcional y el bosque (90/120) actúan sobre posiciones dodecafásicas. Un
conjunto de palabras sin mapa de incidencia no puede acoplarse a esos objetos
posicionales.

## 6. Objeto adicional mínimo

El dato ausente no es otra cifra, un escalar ni una corrección decimal. Es una
sección coinductiva sensible a la monodromía,

\[
\Sigma:
\mathcal X_{mathrm{TPK}}^{\mathrm{enr}}
\longrightarrow
\mathcal I_{69},
\]

donde el dominio conserva frontera, fase, acarreo, hoja y orientación, y
\(\mathcal I_{69}\) es el conjunto de incidencias indexadas de los lectores
N69. La sección debe satisfacer cuatro condiciones:

1. prolongar la supervivencia más allá de \(t=25\);
2. distinguir estados con igual fase y distinta memoria de retorno;
3. seleccionar ocho incidencias sin consultar \(W_{72}\), \(K\) ni sus
   cifras;
4. conservar la posición de cada incidencia para el ensamblaje
   dodecafásico.

Una vez suministrado este objeto, el selector global documentado en
`15_SELECTOR_GLOBAL_DOBLE_LECTURA` ya elige de forma única la regla
\((c,a)\) y el sello decimal. Esa unicidad es exacta respecto del conjunto de
ocho bloques. El presente teorema localiza, sin desplazarla, la única
dependencia anterior de ese resultado.

## 7. Fuerza probatoria y procedencia

- Los cardinales N69 son `EXACTO_INTERNO` respecto del registro publicado.
- La imposibilidad de N72 es `EXACTO_INTERNO` respecto de su dominio
  \(t=5,\ldots,25\).
- La no periodicidad es `EXACTO_INTERNO` para los nueve retornos N74.
- La arquitectura de supervivencia y monodromía es
  `ARQUITECTURA_AUTORAL_PREEXISTENTE`.
- La formulación de la obstrucción de dominio es `FORMALIZACION_NUEVA`.
- Los conteos exhaustivos constituyen `CERTIFICADO_NUEVO`.

No se declara que la sección \(\Sigma\) haya quedado construida. Se demuestra
qué datos ya existen, por qué N71--N74 no bastan para seleccionarlos y qué
tipo de aplicación debe completar el paso.

## 8. Reproducción

```bash
python3 verificar_no_go_s8_n71_n72.py --check-certificate
python3 -O verificar_no_go_s8_n71_n72.py --check-certificate
```

El programa utiliza exclusivamente la biblioteca estándar, no contiene
`assert` y produce el mismo certificado en ejecución normal y optimizada.
