# Continuación por fases del sello dodecafásico

Este directorio contiene cuatro resultados finitos exactos. El carácter
fase--dual de la rama superviviente \(t=10\) produce \(021101\) sin consultar
el sello, y su concatenación con el rombo N72/N74 fuerza la celda decimal
(234\mid543\mid140). Además, la lectura íntegra del registro direccional
N/E/S/O demuestra que su proyección visible posee período \(54\), o seis
ventanas nonádicas, y por ello no puede generar por sí sola un estado
dodecafásico no periódico.
El calibre de Witt estratifica además, palabra por palabra, los doce bloques
del sello en profundidades mínimas \(5+2+5\), conservando expresamente que se
trata de un reconocimiento posterior y no de un generador.
El barrido completo de los caracteres fase--carga localiza un único bloque
ausente, construye ese bloque mediante el carácter afín \(\rho_W+p\), y
demuestra que nueve diferencias orientadas sobre un bosque de pasos \(3/4\)
constituyen la interfaz lineal mínima entre \(W_{24}\) y el sello
dodecafásico completo.

La continuación vigente refina además la elección del bosque mediante las
cuatro órbitas del paso \(+4\). Las nueve diferencias residuales de esta carta
pertenecen al atlas N69--Witt. Ningún lector uniforme de las familias naturales
de fase, carga, calendario, orientación y rotación de Witt selecciona las
nueve. Una vez suministrados sus residuos, la cara excepcional
\(H_e\cap P_\pi\) reduce por sí sola las \(64\) elevaciones a un único sello,
sin imponer \(Q=6263\).

Un resultado posterior sustituye esa selección local por un selector global:
dado el conjunto no ordenado de ocho bloques, la regla N69 estratificada y la
cara excepcional seleccionan conjuntamente un único sello. La dependencia
anterior queda así desplazada a una cuestión más precisa. N69 contiene los
ocho bloques, pero N71--N72 no los seleccionan: cuatro ni siquiera pertenecen
a la imagen total de su ventana publicada. N74 impide completar la ventana por
periodicidad, pues retorna la fase y cambia la frontera. El dato mínimo es una
sección coinductiva sensible a la memoria que seleccione incidencias y
posiciones, no una lista adicional de cifras.

Archivos:

- `TEOREMA_CARACTER_FASE_DUAL_Y_TERCER_BLOQUE.md`: demostración y alcance;
- `verificar_caracter_fase_dual.py`: reproducción con aritmética exacta;
- `RESULTADO_CARACTER_FASE_DUAL.json`: certificado congelado;
- `TEOREMA_OBSTRUCCION_REGISTRO_DIRECCIONAL_108.md`: teorema de periodicidad y
  delimitación exacta de la proyección direccional;
- `analizar_registro_direccional_108.py`: lectura OOXML y verificador;
- `RESULTADO_REGISTRO_DIRECCIONAL_108.json`: certificado congelado;
- `TEOREMA_ESTRATIFICACION_WITT_DEL_SELLO.md`: teorema de primera entrada en
  el catálogo N33 bajo \(J=A_W\);
- `verificar_estratificacion_witt_sello.py`: verificador exhaustivo sobre
  \(\mathbb F_3^6\);
- `RESULTADO_ESTRATIFICACION_WITT_SELLO.json`: certificado congelado;
- `TEOREMA_OBSTRUCCION_Y_DATO_MINIMO_W72.md`: obstrucción exacta de los
  lectores locales, carácter afín de cierre de cobertura e interfaz mínima;
- `verificar_obstruccion_y_dato_minimo_w72.py`: barrido N69 y certificado
  unimodular de reconstrucción;
- `RESULTADO_OBSTRUCCION_Y_DATO_MINIMO_W72.json`: certificado congelado;
- `TEOREMA_COCICLOS_N69_Y_SECCION_DIRECCIONAL.md`: bosque orbital, incidencia
  de los nueve cociclos, imposibilidad de los lectores uniformes y unicidad
  de la elevación por la cara excepcional;
- `verificar_cociclos_n69_y_seccion_direccional.py`: barridos exhaustivos y
  reproducción exacta;
- `RESULTADO_COCICLOS_N69_Y_SECCION_DIRECCIONAL.json`: certificado congelado;
- `TEOREMA_NO_GO_S8_N71_N72.md`: insuficiencia exacta de la ventana
  coinductiva para seleccionar los ocho bloques y tipo del dato mínimo;
- `verificar_no_go_s8_n71_n72.py`: verificador de N69, N72, N74 y del panel
  de los tres lectores;
- `RESULTADO_NO_GO_S8_N71_N72.json`: certificado congelado;
- `SHA256SUMS`: integridad de todos los artefactos.

Reproducción:

```bash
python3 verificar_caracter_fase_dual.py --check-certificate
python3 -O verificar_caracter_fase_dual.py --check-certificate
python3 analizar_registro_direccional_108.py --check-certificate
python3 -O analizar_registro_direccional_108.py --check-certificate
python3 verificar_estratificacion_witt_sello.py --check-certificate
python3 -O verificar_estratificacion_witt_sello.py --check-certificate
python3 verificar_obstruccion_y_dato_minimo_w72.py --check-certificate
python3 -O verificar_obstruccion_y_dato_minimo_w72.py --check-certificate
python3 verificar_cociclos_n69_y_seccion_direccional.py --check-certificate
python3 -O verificar_cociclos_n69_y_seccion_direccional.py --check-certificate
python3 verificar_no_go_s8_n71_n72.py --check-certificate
python3 -O verificar_no_go_s8_n71_n72.py --check-certificate
```

La formalización es canónica respecto de los axiomas publicados en el teorema
—coincidencia fase--carga, orientación y naturalidad—. La extensión afín
cierra la cobertura de los bloques, pero no se declara que esa cobertura
ordene por sí sola los doce bloques ternarios de \(K\).
La obstrucción direccional explica por qué: la memoria que rompe el período
seis no está en la proyección visible de 108 pasos y debe conservarse en el
estado TPK enriquecido. El selector global evita la elección arista por
arista, pero no elimina la necesidad de seleccionar intrínsecamente las ocho
incidencias anteriores.
La elección orbital sustituye únicamente el bosque concreto del primer
certificado; conserva su teorema de minimalidad y toda la cobertura N69.
