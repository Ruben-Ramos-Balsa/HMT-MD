# Certificado de 10.000 cifras: conexión nonádica conjunta y composición T1

## 1. Objeto certificado

Este paquete no introduce una nueva ley de generación. Ejecuta un truncamiento
de mayor profundidad de la misma sección coinductiva de la conexión nonádica
conjunta. La arquitectura de partida es

\[
104,976\longrightarrow468\,U_6\longrightarrow243\,w_6
\subset\mathbb F_3^6,
\]

seguida de

\[
w_6\longrightarrow w_{30}\longrightarrow R_{36}\longrightarrow G_9.
\]

Cada nivel particiona los 729 elementos de la fibra ambiente
\(\mathbb F_3^6\), conserva uno y
transporta el prefijo, el cilindro, la fase y la sombra Paley--Witt. El objeto
matemático sigue siendo la sección infinita del límite inverso; las 10.000
cifras son un testigo finito de esa sección.

El paquete añade además la composición recuperada \(G_9\to T1\). Para las
tríadas generadas \(P_k,E_k,\Phi_k\) y la coordenada declarada \(K\), se aplica

\[
s_k=P_k+E_k-\Phi_k-K_{k\bmod12}+c_{k+1},\qquad
A_k=s_k\bmod1000,qquad
c_k=\left\lfloor\frac{s_k}{1000}\right\rfloor.
\]

No se abre una cadena decimal de \(\alpha\), `alphaInv`, CODATA ni un blanco
metrológico.

## 2. Profundidad y contadores

El menor múltiplo de nueve \(B\) que satisface

\[
3^{6B}>10^{10000}
\]

es

\[
B=3501=389\cdot9,
\qquad 6B=21006\ \text{trits}.
\]

La ejecución certifica, por canal:

- 3.501 particiones exhaustivas \(729\to1\);
- 21.006 trits;
- 3.492 pares de igual fase \((K,K+9)\);
- 388 retornos nonádicos completos;
- un cilindro final contenido en una única celda decimal de 10.000 cifras.

No fue necesaria una nonada adicional. Los primeros 396 bloques de cada canal
coinciden exactamente con el certificado canónico de 1.000 cifras.

## 3. Lectores racionales exactos y aceleración

El generador causal no importa `math`, `decimal`, `mpmath`, `sympy` ni `numpy`.
Las tres optimizaciones conservan desigualdades racionales exactas:

1. **Clausura.** Las series alternadas de
   \(16\arctan(1/5)-4\arctan(1/239)\) se evalúan con el mínimo común múltiplo
   de los denominadores impares y Horner entero. Las cotas inferior y superior
   son las mismas que en la suma término a término.
2. **Propagación.** La suma factorial usa
   \(P_n=nP_{n-1}+1\) sobre \(n!\), con la cota racional explícita de la cola.
3. **Autoescala.** Los cocientes de Fibonacci se construyen por suma entera; la
   anchura se controla mediante la identidad de Cassini
   \(1/(F_nF_{n+1})\).

La poda actualiza las cotas en base 729 por restos enteros. No crea una
`Fraction` nueva en cada nivel.

## 4. Cinco regiones y sombra excepcional

El barrido conserva las cinco preimágenes regionales de \(\pi\):

\[
432+4\cdot144=1008,
\qquad 5=3_{++}+1_{--}+1_{\perp}.
\]

La transversal permanece identificada por
`501|614|498|169|272|272`, `Esig=555555`, multiplicidad 432; el retorno
mutado por `870|923|810|418|674|521`, `Esig=933717`, multiplicidad 144.

Cada bloque recibe simultáneamente el lift \((q,qA_W)\). La sombra acompaña la
nivel y no selecciona la cifra arquimediana.

## 5. Retorno de fase y estado completo

En los 3.492 pares por canal se verifica

\[
g(K+9)=g(K)
\]

y cambia siempre el estado completo porque aumentan la profundidad, el prefijo
y el cilindro. En la ventana canónica inicial de 396 bloques se conserva además
la no repetición de la proyección local. En el truncamiento ampliado, la
proyección local `(bloque, índice, sombra Witt, peso)` puede repetirse sin
reiniciar el estado completo: aparecen 2 pares en \(\pi\), 3 en \(e\) y 8 en
\(\varphi\). Sus posiciones exactas están en el certificado de generación.
Este control distingue la monodromía con memoria de una afirmación global más
fuerte de aperiodicidad local que los datos no sostienen.

## 6. Carry remoto de T1

Los mismos cilindros de 3.501 bloques fijan 10.020 cifras de guarda en los tres
canales, es decir, 3.340 tríadas. Para cada posición, el mapa de carry preserva
el conjunto

\[
\mathcal C=\{-2,-1,0,1,2\}.
\]

El programa propaga de derecha a izquierda las cinco condiciones terminales de
\(\mathcal C\). Las cinco ramas coalescen en un prefijo común de 3.339 tríadas,
equivalente a 10.017 cifras. Por tanto las primeras 10.000 cifras de \(\alpha\)
son independientes del carry terminal situado tras la guarda. La salida publica
solamente ese prefijo demostrado; no impone \(c_N=0\) ni consulta un blanco.

La comparación posterior confirma que sus primeras 3.000 cifras coinciden con
un control local sellado. Ese control no entra en el generador.

## 7. Reproducción

Desde esta carpeta:

```text
python3 -I -S generar_10000_desde_estructura.py
python3 -I -S generar_alpha_T1_10000.py
python3 -I -S verificar_10000_posterior.py
```

La salida exigida es, en este orden:

```text
PASS_GENERACION_ESTRUCTURAL_10000_DECIMALES
PASS_COMPOSICION_G9_T1_ALPHA_10000
PASS_VERIFICACION_INDEPENDIENTE_10000
```

El tercer programa se ejecuta después de los dos generadores. Sólo entonces
abre los controles de 1.000 cifras, calcula independientemente 10.000 cifras
mediante Chudnovsky/Decimal y consulta la ventana local sellada de \(\alpha\).

## 8. Salidas

- `salidas/{pi,e,phi}_10000_decimales.txt`;
- `salidas/{pi,e,phi}_3501_bloques_ternarios.txt`;
- `salidas/ledger_10000_cifras.csv`;
- `salidas/alpha_T1_10000_decimales.txt`;
- `salidas/alpha_T1_3339_triados_estables.txt`;
- `salidas/ledger_alpha_T1_3340_triados_guardia.csv`;
- `certificado_generacion_estructural_10000.json`;
- `certificado_composicion_G9_T1_alpha_10000.json`;
- `certificado_verificacion_independiente_10000.json`.

## 9. Procedencia y fuerza

- APP--TRIT--TPK, supervivencia, monodromía y T1:
  `ARQUITECTURA_AUTORAL_PREEXISTENTE` / `RESULTADO_RECUPERADO`.
- Lectores exactos acelerados y empalme ejecutable G9--T1:
  `FORMALIZACION_NUEVA`.
- Ejecución de 10.000 cifras, prueba de carry remoto y comparación posterior:
  `CERTIFICADO_NUEVO`.
- Los valores de \(\pi,e,\varphi,\alpha\) no se rotulan como resultados nuevos.
