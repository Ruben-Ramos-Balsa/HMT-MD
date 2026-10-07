# Reproducción y naturaleza de la evidencia

## 1. Conservación de ejecuciones válidas

Los 24 archivos del expediente del 29/09 se copian íntegros a `archivo_integro/`. La tabla de procedencia del manifiesto compara SHA-256 de origen y copia. Esta entrega reutiliza esas ejecuciones: no se ha vuelto a ejecutar una campaña de raíces, entrada, cobertura intermedia o primera salida. El traslado editorial conserva familia, precisión, dominios, programas y certificados.

Las reservas finitas impresas en algunos JSON describen correctamente lo que prueba ese programa por sí solo. La conclusión infinita pertenece a la composición de dichos certificados con las pruebas escritas; no se modifica retrospectivamente el alcance de cada ejecución.

## 2. Tres niveles de evidencia

| Nivel | Contenido | Función |
|---|---|---|
| Demostraciones generales | Perfil y normalización; Schwarziana; factorización holomorfa; inversas con memoria; lectores de profundidad; palabra infinita; intervalos restrictivos; transporte del orden y mínimos; clasificación; existencia de todas las primeras raíces; continuidad de signos; hoja estable; primera salida; transferencia métrica | Justifican los cuantificadores sobre toda profundidad y la identidad de la sucesión seleccionada. |
| Certificados racionales finitos | Ocho raíces; continuación finita; entrada y tangente; 374 hojas del puente; 64 bandas de primera salida; controles exactos de momentos, Jacobi y sensibilidad | Acreditan desigualdades y coberturas concretas utilizadas por las demostraciones generales. |
| Teoremas analíticos importados | Hiperbolicidad de renormalización, transversalidad del blanco superestable, universalidad local, realización cuadrática semejante y holonomía de clases híbridas | Se aplican a la familia HMT ya generada, con las hipótesis comprobadas en el cuerpo. Sus valores no seleccionan el perfil ni sus raíces. |

Los recibos causales comprueban genealogía, roles y localizadores. El manifiesto comprueba identidad material. Estas comprobaciones tienen funciones distintas de la demostración matemática.

## 3. Orden de reproducción

Los comandos siguientes documentan la reproducción, **no una campaña nueva ejecutada para esta entrega**. Usan Python 3 y biblioteca estándar. Para conservar los testigos originales, ejecútense en una copia de trabajo del paquete y guárdense las salidas nuevas con nombres diferentes. Desde la raíz de esa copia:

### 3.1. Ocho raíces y cocientes finitos

```sh
python3 -I -S archivo_integro/certificar_raices.py --seeds datos/vacancias_criticidad.json --max-level 8 --digits 100 --radius-exp 42 --output RAICES_REPRODUCIDAS.json
```

El único miembro de las semillas leído por el programa es `dodecaphase_quadratic_criticality.undeformed_eta_zero.superstable_parameters`. Las aproximaciones proponen cajas; los signos, las derivadas intervalares y la exclusión de períodos divisores las certifican. Los valores históricos de Feigenbaum presentes en otros miembros del archivo de semillas no se leen como entradas.

Salida del testigo: `PASS_LOCAL_FINITE_ROOTS_AND_RATIOS`.

### 3.2. Continuación finita del selector

```sh
python3 -I -S archivo_integro/certificar_continuacion_finita.py --certificate archivo_integro/CERTIFICADO_RAICES_INTERVALOS.json --levels 2 3 4 5 6 7 8 --upper 1.874039 --terms 32 --self-test --seconds 3600 --max-boxes 20000 --output CONTINUACION_REPRODUCIDA.json
```

El presupuesto temporal controla cuánto trabajo se permite a la ejecución; el resultado válido exige cobertura completa. La campaña conservada contiene 650 cajas procesadas y 332 hojas de cobertura. Salida del testigo: `PASS_FINITE_ROOT_CONTINUATION`.

### 3.3. Entrada, tangente y cruce estable

```sh
python3 -I -S archivo_integro/certificar_entrada_renormalizacion.py --lower 1.874038 --upper 1.874039 --levels 4 --order 32 --pieces 16 --output ENTRADA_REPRODUCIDA.json
```

Se conservan las dieciséis cajas, los cuatro retornos, las colas de función y tangente, la admisibilidad real y los márgenes del cruce. El certificado guarda los resultados de cada nivel; la construcción de la hoja y su contracción aparecen en la prueba legible.

### 3.4. Puente entre la octava raíz y la caja local

```sh
python3 -I -S archivo_integro/certificar_puente_itinerario.py --upper 1.874038 --max-iteration 2048 --max-boxes 20000 --seconds 3600 --output PUENTE_REPRODUCIDO.json
```

Si una ejecución termina por presupuesto, el mismo comando con `--resume` continúa el archivo de salida. Se acepta únicamente la cobertura completa. El testigo conservado guarda también la primera ejecución y su reanudación: 374 intervalos exactamente adyacentes, con 331 exclusiones por signo y 43 por retorno de igual signo. Salida: `PASS_EXCLUSION_LAMBDA_TAU_ON_FULL_BRIDGE`.

### 3.5. Exclusión de toda la región de primera salida

```sh
python3 -I -S archivo_integro/certificar_caps_kneading.py --first-exit-cover --receipt CAP_REPRODUCIDA.json
```

El modo indicado fija la región utilizada en la prueba, incluida la sobrepasada máxima del umbral y la correlación del residuo estable. Cubre exactamente 64 bandas: 54 por signo y diez por contracción. Salida: `PASS_NEGATIVE_FIRST_EXIT_CAP_EXCLUSION`.

### 3.6. Comprobaciones exactas del expediente

`verificar_prolongacion.py` y `verificar_escalado_local.py` conservan sus versiones originales. Ejecutarlos directamente regenera sus controles y recibos junto a los scripts; hágase sólo en una copia de trabajo. El segundo comprueba las huellas, el teselado y los testigos almacenados, además de identidades racionales y falsadores; no regenera por sí solo todas las trayectorias de las campañas 3.1–3.5.

La prueba de profundidad infinita se lee en los fragmentos de clasificación, aislamiento e identificación analítica. Ningún número de cajas finitas reemplaza esas inducciones y argumentos uniformes.

## 4. Teoremas analíticos empleados

1. **Lanford: hiperbolicidad del operador de duplicación.** Se emplea la existencia del punto fijo, una dirección inestable y las cotas de los bloques diferenciales en la carta declarada. [Prepublicación original](https://repo-archives.ihes.fr/A_GARDER/20180409/Test/I_Prepublications/LANFORD/1968-2013/P_81_17/P_81_17_web.pdf).
2. **Hertling–Spandl, §2, lema 2.1 y tabla 2.** Fija la carta \(u/10\), el polinomio central, la cota del error y el precondicionador que proporciona la cota superior transversal. [Artículo](https://arxiv.org/pdf/1410.3277).
3. **Eckmann–Wittwer.** Se utiliza el cruce transversal de la variedad inestable con el blanco superestable de período dos en la normalización par. [Artículo original](https://link.springer.com/article/10.1007/BF01013368).
4. **Collet–Eckmann–Lanford, §6, proposición 6.1 y teoremas 6.2–6.3.** Se aplica el escalado local a la curva transversal y al blanco superestable. [Artículo original](https://people.math.harvard.edu/~knill/history/lanford/papers/ColletEckmannLanford.pdf).
5. **de Faria–de Melo–Pinto, teorema 2.1 y lema 3.2.** Proporciona la realización de grado dos en una vecindad común tras un número finito de retornos. [Artículo original, Annals 164](https://annals.math.princeton.edu/wp-content/uploads/annals-v164-n3-p01.pdf).
6. **Lyubich, teoremas 5.6, 6.1 y 7.4; lema 7.3.** Cotas a priori; identificación entre clase híbrida y variedad estable; unicidad de centros sobre una transversal en una vecindad fija; regularidad \(C^{1+\beta}\) de la holonomía. [Artículo original, Annals 149](https://www.maths.tcd.ie/EMIS/journals/Annals/149_2/lyubich.pdf).

Las hipótesis y su aplicación concreta se explican en los fragmentos 05–07. La exposición acredita una construcción HMT del lector y una demostración de su escalado mediante esas dependencias. No atribuye al expediente una reproducción independiente de todas las pruebas originales de hiperbolicidad.

## 5. Precisión y alcance

El error de evaluación de \(\delta_{F,8}\), la tasa operatorial \(0.83996\) y el resto paramétrico \(M\theta^n\) tienen variables diferentes. La prueba del límite y de su resto de potencia es completa con cuantificadores existenciales para \(C,M,\theta,n_0\). La evaluación decimal de la distancia del octavo cociente a ese límite no forma parte del enunciado entregado.

La corrección editorial preserva el dominio uniforme \(\eta=0\), el selector original y los dos desplazamientos de índice: \(d\), preparación cuadrática semejante, y \(s\), índice del blanco superestable. La identidad eventual se establece igualando períodos físicos.

## 6. Instrucciones de inclusión

Los archivos `latex/*.tex` son fragmentos, no documentos autónomos. El anfitrión debe disponer de `amsmath`, `amsthm` (entornos `proposition`, `lemma`, `proof`), `booktabs`, `longtable` e `hyperref`; para los alfabetos matemáticos se emplea `amssymb,mathrsfs` o `unicode-math`. La raíz se pasa en `\HMTFGRoot`; el archivo `INSERCION_FEIGENBAUM.tex` respeta esa variable y fija localmente los alias operatorios.

No se ha compilado el libro ni estos fragmentos. La integración final deberá conservar el preámbulo y el entorno de numeración del editor, aplicar los localizadores del mapa y comprobar el resultado compuesto. Esta comprobación editorial del PDF integrado es distinta del cierre matemático entregado.
