# Reproducción independiente del campo de estrellas de Witt

`verificar_m12_witt.py` no lee el resumen JSON legado. Reconstruye desde la
matriz `A_W` publicada en el calibre del atlas (la permutación simultánea
`(1,2,3,5,6,4)` del calibre Paley):

1. las `132` hexadas de `S(5,6,12)`;
2. las `495` involuciones de estrella, una por cada 4-cara;
3. la preservación de todas las hexadas;
4. el grupo generado, de orden `95040`;
5. el estabilizador trivial del marco HMT ordenado.
6. los cuatro soportes de canal directamente desde las semillas publicadas.

El cálculo prueba que el **campo global** de estrellas genera el grupo que, por
la identificación clásica `Aut(S(5,6,12)) ≅ M12`, es `M12`. HMT selecciona la
cara `B_K={4,6,9,10}` y un marco; no se afirma que una sola estrella genere el
grupo.
