# Certificado NEWSO / CT108–243

Este directorio separa y verifica tres construcciones que en borradores
históricos podían confundirse por el uso de las mismas letras cardinales:

1. **NEWSO espacial:** rutas sobre el toro APP de 9 por 9, con hoja suma o
   producto, realimentación ternaria y puertas en los ticks 3, 6 y 9.
2. **D108 dodecafásico:** rotor de 108 entradas inducido por
   `beta(b)=4b mod 12`; recorre los doce sectores durante nueve bloques.
3. **NSEO aritmético:** corrientes de triadas `E=pi`, `N=e`, `O=phi` y
   `S=K`, con acarreo/préstamo base 1000 de derecha a izquierda.

`verificar_newso_ct108.py` recibe las palabras objetivo y reconstruye por
programación dinámica sus rutas de coste mínimo a 108 y 243 ticks; comprueba los
trits emitidos en cada puerta; lee doce triadas estables a partir de 81 trits;
construye el observable firmado con tres bloques Hadamard; y ejecuta el cierre
NSEO que produce las doce triadas de alfa.

La reauditoría detectó que una nota histórica prolongaba correctamente los
prefijos sólo hasta el trit 36, pero imprimía después cadenas incompatibles con
las palabras objetivo de 81 trits. Este certificado usa esas palabras como
entrada de control. Con semilla fijada y desempate determinista NEWSO se
obtienen costes `15/18/17` a 108 ticks y `35/37/40` a 243 ticks para pi/e/phi.
Los últimos reemplazan la anotación `35/40/45`. La lectura corregida produce
exactamente las doce triadas declaradas y conserva el cierre de alfa.

Las rutas largas son certificados condicionados de realización y minimalidad
de los prefijos declarados; no seleccionan las cifras. La lectura rectora de
doce triadas usa 78 trits de la rama G9 publicada y la ventana de 81 actúa como
control adicional. N32/N33 tampoco aportan todavía un selector libre de
objetivos para las ramas largas.

Salidas:

- `rutas_newso_108_243.csv`: cada tick, dirección, posición, hoja y puerta;
- `rotor_dodecafasico_D108.csv`: los 108 sectores del rotor;
- `acarreo_NSEO_alpha.csv`: operación y acarreo de cada sector;
- `certificado_newso_ct108_243.json`: resumen verificable.
