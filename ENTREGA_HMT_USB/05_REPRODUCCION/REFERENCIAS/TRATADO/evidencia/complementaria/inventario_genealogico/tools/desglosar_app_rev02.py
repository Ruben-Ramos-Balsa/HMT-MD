#!/usr/bin/env python3
"""Genera un árbol editorial verificable; no certifica todo el corpus HMT.

Los datos de desglose se redactan aquí explícitamente. Las tablas finitas se
calculan desde los enteros 1..9, sin entradas de constantes reconocidas.
REV01 y las fuentes propietarias no se modifican.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'REV02_ARBOL'
SOURCE = Path('/Users/ruben/Documents/New project/PUBLICACION_HMT/SERIE_ARTICULOS_HMT/NUCLEO_COMUN_20260910/sections/nucleo.tex')
OLD = ROOT / '01_APP_TRIT_TPK_PASOS_ELEMENTALES.md'
NODES = []

def group(parent, lines, dependencies, items):
    for index, (title, action) in enumerate(items, 1):
        NODES.append({
            'id': f'{parent}.{index:02d}', 'parent': parent,
            'title': title, 'operation_to_expose': action,
            'source': str(SOURCE), 'source_lines': lines,
            'source_role': 'DEFINICION_O_RESULTADO_BASE; SUBDIVISION_EXPOSITIVA_PROPUESTA',
            'requires': dependencies,
            'status': 'DESGLOSE_PROPUESTO_CON_FUENTE',
            'proof_complete_in_this_node': False,
        })

group('APP-001', [8,15], [], [
 ('Marcas interiores', 'Construir D9 con las nueve marcas 1,…,9; mostrar cada marca sin introducir un valor real objetivo.'),
 ('Extremos de referencia', 'Separar 0 y 10 del alfabeto interior; explicitar qué papel tiene cada extremo en la figura.'),
 ('Intervalos consecutivos', 'Enumerar [0,1],…,[9,10]; son diez intervalos y nueve marcas interiores, no dos nombres para el mismo censo.'),
 ('Orden y orientación', 'Fijar el orden de lectura sobre las marcas y describir su inversión sin cambiar la identidad de cada marca.'),
])
group('APP-002', [13,19], ['APP-001'], [
 ('Eje de filas', 'Introducir el primer ejemplar de D9 y fijar que su coordenada aumenta hacia el sur en la carta gráfica utilizada.'),
 ('Eje de columnas', 'Introducir el segundo ejemplar de D9 y fijar que su coordenada aumenta hacia el este.'),
 ('Producto de posiciones', 'Formar las 81 parejas ordenadas (i,j); conservar la distinción entre fila y columna.'),
 ('Soporte anterior a la evaluación', 'Mostrar la tabla de parejas antes de escribir sumas o productos; distinguir una celda de su valor de lectura.'),
])
group('APP-003', [16,27], ['APP-002'], [
 ('Proyección de cada eje', 'Escribir el mapa i↦[i] módulo 9 en cada coordenada.'),
 ('Carta positiva', 'Escoger 1,…,9 como representantes; mostrar explícitamente que 9 representa la clase cero.'),
 ('Identificación de fronteras', 'Describir por separado la identificación horizontal y la vertical; no sustituirla por un dibujo sin mapa.'),
 ('Posición y desplazamiento', 'Conservar el desplazamiento entero de una ruta además de su posición en el cociente; enlazar con APP-013.'),
])
group('APP-004', [20,27], ['APP-001','APP-003'], [
 ('Resto euclídeo de n−1', 'Dividir n−1 por 9 para n>0, dejando un resto entre 0 y 8.'),
 ('Representante residual positivo', 'Añadir 1 al resto para obtener ρ9(n)=1+((n−1) mod 9); comprobar dominio y rango.'),
 ('Múltiplos de nueve', 'Separar el caso n=9k: el representante positivo es 9 y el resto usual es 0.'),
 ('Congruencia con suma de cifras', 'Desarrollar 10≡1 módulo 9 y la conservación de clase al sumar cifras; esta explicación elemental amplía la definición de la fuente.'),
 ('Iteración de la raíz digital', 'Justificar la terminación de la suma iterada de cifras para n>0 y la unicidad del representante final en 1,…,9.'),
 ('Tratamiento de cero', 'Declarar aparte la convención para n=0; no extender silenciosamente una fórmula declarada para enteros positivos.'),
])
group('APP-005', [20,27], ['APP-004'], [
 ('Cálculo del cociente', 'Obtener q9(n)=(n−ρ9(n))/9 y mostrar que coincide con floor((n−1)/9).'),
 ('Integridad del cociente', 'Usar la congruencia de n y ρ9(n) para justificar que el cociente es entero.'),
 ('Reconstrucción exacta', 'Sustituir ambos datos en n=ρ9(n)+9q9(n); escribir las igualdades intermedias.'),
 ('Unicidad de la pareja', 'Si r+9q=r′+9q′ con r,r′ en 1,…,9, entonces r−r′ es múltiplo de 9 de valor absoluto ≤8; deducir r=r′ y q=q′.'),
 ('Pérdida al olvidar el cociente', 'Desarrollar 10↦(1,1) y 19↦(1,2); los residuos iguales no reconstruyen los enteros distintos.'),
])
group('APP-006', [29,34], ['APP-002'], [
 ('Evaluación individual de suma', 'Calcular S(i,j)=i+j en una posición identificada, antes de cualquier reducción.'),
 ('Tabla íntegra de sumas', 'Exponer las 81 evaluaciones; la tabla adjunta registra cada celda, no sólo totales.'),
 ('Multiplicidad de cada suma', 'Contar las parejas con suma k: k−1 para 2≤k≤10 y 19−k para 10<k≤18; justificar por límites de los índices.'),
 ('Proyección posterior de la suma', 'Aplicar ρ9 y q9 a cada suma entera, manteniendo el enlace con la celda de origen.'),
])
group('APP-007', [29,34], ['APP-002'], [
 ('Acumulación repetida', 'Escribir ij como acumulación de i repetida j veces, conforme a la explicación de la fuente.'),
 ('Evaluación individual de producto', 'Calcular P(i,j)=ij en la misma celda utilizada por la hoja aditiva.'),
 ('Tabla íntegra de productos', 'Exponer las 81 evaluaciones y mantener sus factores, aunque varios pares compartan producto.'),
 ('Proyección posterior del producto', 'Calcular residuo y cociente de cada producto, sin reducir antes los datos que necesita la reconstrucción.'),
 ('Multiplicidades de lectura', 'Identificar qué productos y residuos se repiten y qué coordenadas de origen siguen distinguiéndolos.'),
])
group('APP-008', [36,54], ['APP-005','APP-006','APP-007'], [
 ('Pareja de la hoja aditiva', 'Construir (R+,q+) para cada celda.'),
 ('Pareja de la hoja multiplicativa', 'Construir (R×,q×) sobre esa misma celda, sin intercambiar los cocientes.'),
 ('Evaluación levantada conjunta', 'Reunir ambas parejas con su origen (i,j); distinguir el dato de posición de las cuatro coordenadas de lectura.'),
 ('Recuperación de las dos evaluaciones', 'Reconstruir S y P por sus respectivos pares; este resultado no afirma que una lectura aislada recupere toda ruta.'),
 ('Ejemplo central (5,5)', 'Calcular S=10, P=25, (R+,q+)=(1,1) y (R×,q×)=(7,2).'),
 ('Ejemplo comparativo (8,2)', 'Calcular S=10, P=16, (R+,q+)=(1,1) y (R×,q×)=(7,1).'),
 ('Dato que separa ambas celdas', 'Identificar el cociente multiplicativo como diferencia que borra la pareja de residuos (1,7); no borrar tampoco las coordenadas de origen.'),
])
group('APP-009', [29,34], ['APP-008'], [
 ('Transposición del soporte', 'Definir σ(i,j)=(j,i) y verificar σ²=id.'),
 ('Celdas fijas y pares', 'Enumerar las nueve celdas i=j y las 36 parejas no fijas.'),
 ('Invariancia de las evaluaciones', 'Comprobar S∘σ=S y P∘σ=P; deducir la invariancia de sus pares residuo–cociente.'),
 ('Acción sobre direcciones', 'Transportar también N,E,S,O al intercambiar ejes; no confundir invariancia de valores con identidad de rutas.'),
])
group('APP-010', [56,67], ['APP-003'], [
 ('Paso norte', 'Aplicar (−1,0), con ejemplo interior (5,5)→(4,5) y cruce (1,5)→(9,5).'),
 ('Paso este', 'Aplicar (0,1), con ejemplo interior (5,5)→(5,6) y cruce (5,9)→(5,1).'),
 ('Paso sur', 'Aplicar (1,0), con ejemplo interior (5,5)→(6,5) y cruce (9,5)→(1,5).'),
 ('Paso oeste', 'Aplicar (0,−1), con ejemplo interior (5,5)→(5,4) y cruce (5,1)→(5,9).'),
 ('Composición inversa', 'Verificar T_N T_S=T_S T_N=id y T_E T_O=T_O T_E=id en posiciones; registrar separadamente la ruta realizada.'),
 ('Transporte y lectura', 'Mostrar qué celda se evalúa antes y después del paso cuando se active la regla TPK; el desplazamiento solo no decide la hoja.'),
])
group('APP-011', [63,67], ['APP-003','APP-010'], [
 ('Grupo aditivo subyacente', 'Precisar X9 y sus cuatro generadores; no usar aquí el producto de residuos como ley de grupo.'),
 ('Adyacencia orientada', 'Escribir las cuatro aristas salientes de cada vértice; distinguir 324 aristas dirigidas de 162 aristas no dirigidas.'),
 ('Realización toroidal', 'Construir la identificación de lados de la retícula y declarar el mapa al soporte cociente.'),
 ('Grafo y superficie', 'Separar el grafo finito de cualquier realización continua del toro; no afirmar igualdad de objetos de categorías distintas.'),
])
group('APP-012', [69,73], ['APP-010','APP-011'], [
 ('Alfabeto de direcciones', 'Fijar {N,E,S,O} y una longitud r no negativa.'),
 ('Inicialización de ruta', 'Elegir x0 entre las 81 posiciones y fijar la palabra vacía para r=0.'),
 ('Actualización prefijal', 'Obtener x_k a partir de x_(k−1) y d_k, conservando el prefijo cardinal.'),
 ('Censo de palabras con origen', 'Multiplicar 81 por cuatro posibilidades en cada uno de los r pasos; justificar 81·4^r.'),
 ('Rutas y extremos', 'Exhibir rutas diferentes con un mismo extremo; no convertir el censo de palabras en censo de puntos.'),
 ('Restricción TPK posterior', 'Distinguir todas las palabras cardinales de las rutas que satisfacen la selección y actualización TPK de la siguiente etapa.'),
])
group('APP-013', [73,78], ['APP-012'], [
 ('Desplazamiento levantado', 'Calcular (#S−#N,#E−#O) antes de reducir coordenadas.'),
 ('Condición de cierre residual', 'Mostrar que una ruta cerrada tiene ambas componentes del desplazamiento divisibles por 9.'),
 ('Índice de enrollamiento', 'Dividir ambas componentes por 9 y obtener un par de enteros.'),
 ('Inversión de la ruta', 'Invertir orden y direcciones; verificar el cambio de signo del desplazamiento y del enrollamiento.'),
 ('Vuelta y retroceso', 'Comparar E^9, de enrollamiento (0,1), con EO, de enrollamiento (0,0), aunque ambos cierren la posición.'),
])
group('APP-014', [80,100], ['APP-003','APP-005'], [
 ('Sección positiva', 'Escribir s9(a) para cada clase a y no confundir s9(0)=9 con la sección normalizada.'),
 ('Cociente de composición', 'Calcular c9(a,b)=(s9(a)+s9(b)−s9(a+b))/9 y justificar su integridad.'),
 ('Primera asociación', 'Expandir c9(a,b)+c9(a+b,c) y cancelar sólo los términos de sección que aparecen con signos opuestos.'),
 ('Segunda asociación', 'Expandir c9(b,c)+c9(a,b+c) de la misma manera.'),
 ('Identidad de cociclo', 'Comparar los numeradores resultantes; escribir la igualdad sin omitir el término −s9(a+b+c).'),
 ('Lectura composicional', 'Relacionar esta identidad con concatenación y cambio de asociación, sin identificar el cociente agregado con el registro ordenado completo.'),
])
group('APP-015', [102,107], ['APP-014'], [
 ('Valor en la identidad', 'Sustituir a=0 y calcular c9(0,b)=1, incluso si b=0.'),
 ('Sección normalizada', 'Introducir s0 en 0,…,8 y verificar s9(a)=s0(a)+9·1_(a=0).'),
 ('Corrección del cociclo', 'Sustituir las tres secciones para obtener c9=c0+1_(a=0)+1_(b=0)−1_(a+b=0).'),
 ('Casos de clase nula', 'Separar a=0, b=0, a+b=0 y el caso sin clases nulas; registrar los solapamientos.'),
 ('Datos conservados por el cambio de carta', 'Describir qué cambia numéricamente y qué identidad composicional permanece; no borrar la corrección por normalizar.'),
])
group('APP-016', [109,120], ['APP-006','APP-007','APP-008'], [
 ('Total de suma bruta', 'Sumar cada fila de S y después las nueve filas; contrastar con 9·45+9·45=810.'),
 ('Total de producto bruto', 'Sumar cada fila de P y después las nueve filas; contrastar con 45²=2025.'),
 ('Total de suma residual', 'Usar que cada fila aditiva contiene una vez 1,…,9; obtener 9·45=405.'),
 ('Total de producto residual', 'Contar por separado seis filas de unidades, las filas 3 y 6 y la fila 9; obtener 6·45+2·54+81=459.'),
 ('Total del cociente aditivo', 'Aplicar suma de S=Σ+9q+; calcular (810−405)/9=45.'),
 ('Total del cociente multiplicativo', 'Aplicar suma de P=Π+9q×; calcular (2025−459)/9=174.'),
 ('Concordancia de tabla y fórmula', 'Vincular cada total con sus 81 registros y las nueve sumas de fila, sin reemplazar esas tablas por la cifra final.'),
])
group('APP-017', [116,121], ['APP-016'], [
 ('Identidad por celda', 'Restar S=Σ+9q+ de P=Π+9q× antes de sumar sobre el soporte.'),
 ('Suma de diferencias', 'Aplicar la suma finita a cada término, manteniendo residuo y cociente como contribuciones distintas.'),
 ('Defecto visible', 'Calcular 459−405=54 y señalar su origen en las tablas residuales.'),
 ('Defecto de cociente', 'Calcular 174−45=129; multiplicar por 9 al reconstruir la diferencia entera.'),
 ('Reconstrucción del balance', 'Verificar 2025−810=1215=54+9·129; no atribuir al 54 el balance completo.'),
])
group('APP-018', [123,129], ['APP-007'], [
 ('Prueba de invertibilidad', 'Resolver ab=1 módulo 9 para cada a; obtener inversas 1↔1, 2↔5, 4↔7 y 8↔8.'),
 ('Filas aditivas', 'Demostrar que b↦a+b tiene inversa b↦b−a para cualquier fila.'),
 ('Filas multiplicativas invertibles', 'Usar la inversa de a para probar que b↦ab es una permutación exactamente cuando a es unidad.'),
 ('Fila tres', 'Enumerar 3,6,9,3,6,9,3,6,9 en la carta positiva y conservar cada multiplicidad.'),
 ('Fila seis', 'Enumerar 6,3,9,6,3,9,6,3,9 y comparar orden y multiplicidades con la fila tres.'),
 ('Fila nueve', 'Enumerar nueve representantes 9; distinguir repetición residual de los productos enteros 9,18,…,81.'),
])
group('APP-019', [125,135], ['APP-018'], [
 ('Ideal de múltiplos de tres', 'Construir m={0,3,6} como clases módulo 9.'),
 ('Nilpotencia', 'Multiplicar dos elementos 3a y 3b; su producto 9ab es cero en el cociente.'),
 ('Núcleo de multiplicación por tres', 'Resolver 3x=0 módulo 9 y obtener x en m.'),
 ('Imagen de multiplicación por tres', 'Enumerar 3x módulo 9 y obtener también m.'),
 ('Mapa inducido', 'Construir R/m→m, [x]↦3x; justificar que está bien definido, es lineal sobre F3 y biyectivo.'),
 ('Distinción de productos', 'Mostrar por qué ese isomorfismo vectorial no preserva la multiplicación de anillos: la imagen de 1 tiene cuadrado cero.'),
 ('Reducción directa de 3/6/9', 'Aplicar n↦n mod 3 a los tres enteros; obtener 0,0,0.'),
 ('Coordenada interna de 3/6/9', 'Aplicar [3k]_9↦[k]_3; obtener 1,2,0 y declarar el mapa adicional que extrae el factor tres.'),
])
group('APP-020', [137,151], ['APP-018'], [
 ('Base de realización', 'Introducir e_r en C^9 después de la construcción aritmética; es un lenguaje de realización, no una entrada generativa de constantes.'),
 ('Vector asociado a celda', 'Asignar v_ab=e_(a+b) sobre la hoja aditiva.'),
 ('Proyector de rango uno', 'Formar P_ab=v_ab v_ab* y comprobar P_ab²=P_ab.'),
 ('Resolución por fila', 'Sumar sobre b; la traslación recorre una vez la base y produce I9.'),
 ('Resolución por columna', 'Repetir la prueba sobre a, manteniendo la columna fija.'),
 ('Reconocimiento posterior', 'Nombrar la realización latina sólo después de mostrar las asignaciones y las identidades operatorias.'),
])
group('APP-021', [153,168], ['APP-019','APP-020'], [
 ('Vectores multiplicativos', 'Asignar e_(ab) sin suponer que cada fila forme una base.'),
 ('Operador de la fila tres', 'Agrupar las tres repeticiones de e0,e3,e6 y obtener 3(P0+P3+P6).'),
 ('Rango y multiplicidad', 'Separar rango tres, autovalor tres en la imagen y nulidad en el complemento.'),
 ('Contraste con la identidad', 'Comparar con I9 de la hoja aditiva; igualdad de dimensión ambiente no implica igualdad de operadores.'),
 ('Fila nueve como caso extremo', 'Obtener 9P0, de rango uno, conservando la multiplicidad de las nueve posiciones.'),
])
group('APP-022', [20,46], ['APP-005','APP-008','APP-019'], [
 ('División en base mil', 'Descomponer un entero n=1000q+r con 0≤r<1000; registrar cociente y bloque residual por separado.'),
 ('Primera tabla sin cambio por módulo mil', 'En las evaluaciones brutas de D9² se tiene 2≤S≤18 y 1≤P≤81: aplicar mod 1000 no cambia estas cifras. Distinguir esta comprobación de la emisión TPK posterior.'),
 ('Compatibilidad aritmética con módulo nueve', 'Usar 1000≡1 mod 9 para obtener n≡q+r mod 9; el bloque r solo no conserva necesariamente la clase de n.'),
 ('Ejemplo de acarreo entre bloques', 'Con n=1001, q=1,r=1: la raíz digital de n es 2 y la de r es 1; conservar q evita confundirlas.'),
 ('Ruta 3/6/9 y lector efectivo', 'Vincular el mapa concreto de emisión y lectura de la fuente propietaria con los dos mapas de APP-019; no deducir una equivalencia de rutas sólo de las congruencias.'),
])

# Tercer nivel real: la reconstrucción se descompone en igualdades, no en
# campos administrativos repetidos para inflar el inventario.
group('APP-005.03', [20,27], ['APP-004.01','APP-004.02','APP-005.01'], [
 ('División inicial', 'Escribir n−1=9q+t con 0≤t≤8.'),
 ('Cambio de representante', 'Añadir 1 y obtener n=9q+(t+1), donde 1≤t+1≤9.'),
 ('Identificación de coordenadas', 'Identificar ρ9(n)=t+1 y q9(n)=q por las definiciones anteriores.'),
 ('Restitución del entero', 'Sustituir ambas coordenadas y recuperar exactamente n, sin truncamiento ni aproximación.'),
])

# Localizadores y antecedentes específicos: la herencia de grupo no debe
# ocultar una dependencia distinta en una hoja concreta.
BY_ID = {n['id']: n for n in NODES}
for key in ('APP-006.04', 'APP-007.04'):
    BY_ID[key]['requires'] = ['APP-002','APP-004','APP-005']
BY_ID['APP-009.04']['requires'] = ['APP-008','APP-010']
BY_ID['APP-018.02']['requires'] = ['APP-003','APP-006']
for key in ('APP-002.01','APP-002.02'):
    BY_ID[key]['additional_source_lines'] = [58,63]
BY_ID['APP-003.04']['additional_source_lines'] = [69,78]
GRAPH = Path('/Users/ruben/Documents/New project/PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE/TPK_GRAFO_OPERATORIO_TIPADO.json')
GEOMETRY = Path('/Users/ruben/Documents/New project/output/EXTREMA_MEDIA_RAZON_RECIPROCIDAD_ES_EN_20260918/ARTICULO/ES/source/sections/geometria_modular.tex')
for key in ('APP-022.01','APP-022.02','APP-022.03','APP-022.04'):
    BY_ID[key]['source'] = str(GEOMETRY)
    BY_ID[key]['source_lines'] = [99,137]
    BY_ID[key]['additional_source'] = {'path': str(GRAPH), 'lines': [312,333], 'node': 'OP04_IOTA1000'}
    BY_ID[key]['source_role'] = ('REGLA_BASE_DE_LA_FUENTE' if key == 'APP-022.01'
                                 else 'CALCULO_ILUSTRATIVO_DEL_INVENTARIO_DESDE_REGLAS_CITADAS')
BY_ID['APP-022.05']['source'] = str(GRAPH)
BY_ID['APP-022.05']['source_lines'] = [542,563]
BY_ID['APP-022.05']['source_role'] = 'LOCALIZADOR_TIPADO_OP14; COTEJAR_PRODUCTOR_DE_RUTA_EN_SR_Y_CG'
BY_ID['APP-022.05']['requires'] = ['APP-019','APP-022.01']

def rho(n):
    assert isinstance(n, int) and n > 0, 'rho se restringe aquí a enteros positivos'
    return 1 + (n - 1) % 9

def encode(n):
    r = rho(n)
    return {'raw': n, 'residue_positive_mod9': r, 'quotient_positive_mod9': (n-r)//9,
            'usual_remainder_mod9': n % 9, 'remainder_mod1000': n % 1000,
            'quotient_mod1000': n // 1000}

def main():
    OUT.mkdir(exist_ok=True)
    old_text = OLD.read_text()
    parents = dict(re.findall(r'^## ((?:APP|TRIT|TPK)-\d{3}) — (.+)$', old_text, re.M))
    ids = set(parents) | {n['id'] for n in NODES}
    assert len({n['id'] for n in NODES}) == len(NODES)
    assert all(n['parent'] in ids for n in NODES)
    assert all(d in ids for n in NODES for d in n['requires'])
    rows = []
    for i in range(1,10):
        for j in range(1,10):
            item = {'cell_id': f'APP-CELDA-{i}-{j}', 'i': i, 'j': j,
                    'additive': encode(i+j), 'multiplicative': encode(i*j)}
            for key in ('additive','multiplicative'):
                e = item[key]
                assert e['raw'] == e['residue_positive_mod9'] + 9*e['quotient_positive_mod9']
                assert e['raw'] == 1000*e['quotient_mod1000'] + e['remainder_mod1000']
            rows.append(item)
    sums = {f'{sheet}_{field}': sum(r[sheet][field] for r in rows)
            for sheet in ('additive','multiplicative')
            for field in ('raw','residue_positive_mod9','quotient_positive_mod9')}
    assert list(sums.values()) == [810,405,45,2025,459,174]
    s9 = lambda a: a % 9 or 9
    c9 = lambda a,b: (s9(a)+s9(b)-s9(a+b))//9
    c0 = lambda a,b: ((a%9)+(b%9)-((a+b)%9))//9
    for a in range(9):
        for b in range(9):
            assert c9(a,b) == c0(a,b)+(a==0)+(b==0)-((a+b)%9==0)
            for c in range(9):
                assert c9(a,b)+c9(a+b,c) == c9(b,c)+c9(a,b+c)
    raw_source = SOURCE.read_bytes()
    source_hash = hashlib.sha256(raw_source).hexdigest()
    doc = {'scope': 'DESGLOSE_EDITORIAL_APP; NO_ES_EL_PERIMETRO_GLOBAL_DEL_INVENTARIO',
           'source': str(SOURCE), 'source_sha256': source_hash,
           'preserved_revision': str(ROOT/'INVENTARIO_ACUMULATIVO_REV01.md'),
           'nodes': NODES, 'table_records_are_not_distinct_theorems': True,
           'root_count_is_not_measure_of_exhaustiveness': True}
    (OUT/'11_APP_ARBOL_ELEMENTAL.json').write_text(json.dumps(doc, ensure_ascii=False, indent=2)+'\n')
    (OUT/'11_APP_CELDAS_COMPLETAS.json').write_text(json.dumps({'records':rows,'totals':sums}, ensure_ascii=False,indent=2)+'\n')
    text = [
      '# APP: árbol elemental de operaciones y pasos demostrativos\n',
      'Este desarrollo es una rama del inventario global, no su límite temático. Conserva los IDs de REV01 y añade descendientes. TRIT, TPK, semillas, prolongación, K, alfa y continuo mantienen sus fichas y sus ampliaciones propias.\n',
      f'Fuente base leída: [núcleo común](<{SOURCE}>), SHA-256 `{source_hash}`. La fuente establece las definiciones y resultados; este árbol explicita la descomposición propuesta para su exposición. Los ejemplos elementales adicionales no se atribuyen como citas literales a esa fuente.\n',
      'Las hojas siguientes son instrucciones matemáticas individualizadas para la futura redacción. `DESGLOSE_PROPUESTO_CON_FUENTE` no significa demostración ya desarrollada. Las tablas de esta entrega sí se han calculado íntegramente y se declaran al final.\n',
      'APP-022 añade la interfaz aritmética con base mil; su fuente efectiva de emisión TPK permanece enlazada en REV01 y en los árboles de generación. La congruencia elemental no sustituye aquella regla.\n',
    ]
    for parent in parents:
        children = [n for n in NODES if n['parent']==parent]
        if not children:
            continue
        text.append(f'## {parent} — {parents[parent]}\n')
        for n in children:
            locator = f"[fuente](<{n['source']}:{n['source_lines'][0]}>), líneas {n['source_lines'][0]}–{n['source_lines'][1]}"
            if n.get('additional_source_lines'):
                locator += f"; también {n['additional_source_lines'][0]}–{n['additional_source_lines'][1]}"
            if n.get('additional_source'):
                extra = n['additional_source']
                locator += f"; [{extra['node']}](<{extra['path']}:{extra['lines'][0]}>)"
            text.append(f"### {n['id']} — {n['title']}\n\n{n['operation_to_expose']}\n\nAntecedentes: {', '.join(n['requires']) or 'alfabeto declarado'}. Localizador: {locator}. Papel de la fuente: `{n['source_role']}`.\n")
            for sub in [v for v in NODES if v['parent']==n['id']]:
                text.append(f"- **{sub['id']} — {sub['title']}:** {sub['operation_to_expose']}")
            if any(v['parent']==n['id'] for v in NODES):
                text.append('')
    text += ['## Registro completo de las 81 celdas\n',
      'Cada fila conserva las dos evaluaciones enteras, sus residuos positivos y sus cocientes. La exportación JSON añade los restos usuales módulo nueve y las divisiones módulo mil. Las 81 filas son instancias de las mismas operaciones, no 81 teoremas.\n',
      '| Celda | S | Σ | q+ | P | Π | q× |',
      '|---|---:|---:|---:|---:|---:|---:|']
    for row in rows:
        a,m=row['additive'],row['multiplicative']
        text.append(f"| ({row['i']},{row['j']}) | {a['raw']} | {a['residue_positive_mod9']} | {a['quotient_positive_mod9']} | {m['raw']} | {m['residue_positive_mod9']} | {m['quotient_positive_mod9']} |")
    text += ['\n## Sumación por filas\n', '| Fila | ∑S | ∑Σ | ∑q+ | ∑P | ∑Π | ∑q× |','|---|---:|---:|---:|---:|---:|---:|']
    for i in range(1,10):
        r=[x for x in rows if x['i']==i]
        nums=[sum(x[s][f] for x in r) for s in ('additive','multiplicative') for f in ('raw','residue_positive_mod9','quotient_positive_mod9')]
        text.append('| '+str(i)+' | '+' | '.join(map(str,nums))+' |')
    text += ['| Total | 810 | 405 | 45 | 2025 | 459 | 174 |\n',
      '## Alcance del control ejecutado\n',
      'Se recorren las 81 celdas, se verifica la reconstrucción de ambas hojas, sus seis totales, la identidad del cambio de sección en las 81 parejas de clases y la identidad de cociclo en las 729 ternas. Este control aritmético no demuestra por extensión la generación de constantes, la ley nonádica completa ni los teoremas posteriores. No se ejecuta ni se anuncia una nueva prueba Lean.\n',
      f'Reproducción: `python3 -I -S "{Path(__file__).resolve()}"`.\n',
    ]
    (OUT/'11_APP_ARBOL_ELEMENTAL.md').write_text('\n'.join(text)+'\n')
    result={'status':'PASS_DESGLOSE_APP_Y_TABLAS_FINITO','nodes':len(NODES),'cells':len(rows),
            'cocycle_cases':729,'section_change_cases':81,'source_sha256':source_hash,
            'scope':'CONTROL_FOCAL_ARITMETICO_Y_DOCUMENTAL_NO_GLOBAL'}
    (OUT/'11_RECIBO_APP_FOCAL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
