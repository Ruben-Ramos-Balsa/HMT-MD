# Certificado de estado HMT — semillas, G9 y dígitos de control

## 1. APP calculada
- Suma hoja aditiva S_+ = 405
- Suma hoja multiplicativa S_x = 459
- Defecto Delta_APP = 54
- Bloque central [4,5]x[4,5] = [[7, 2], [2, 7]]
- Red radical 3,6,9: union=297, núcleo=81, brazos=216

## 2. Catálogo TPK
- Condiciones iniciales: 81^2*4^2 = 104976
- Salidas U6: 468
- Palabras visibles w6: 243
- Fibras: 432x144 + 18x432 + 18x1944 = 104976
- Macroclases: [108, 108, 108, 36, 72, 18, 18], suma=468

## 3. Semillas y lift
w6(pi)=010211
w6(e)=201101
w6(phi)=121200

w30(pi)=010211|012222|010211|002111|110221
w30(e)=201101|121221|102011|012222|102011
w30(phi)=121200|112202|121020|010210|010200

La verificación de compatibilidad cilíndrica de w30 contra dos triadas iniciales está en `w30_cylinder_compatibility.csv`.

## 4. Dígitos de control
Los archivos `pi_1000_reference_digits.txt`, `e_1000_reference_digits.txt` y `phi_1000_reference_digits.txt` contienen los primeros 1000 decimales como referencia externa de control. No son certificados de generación autónoma G9.

## 5. Estado G9
Cerrado: semillas, lift, cilindros, Hensel/memoria, monodromía de puertas.
Frontera: generación autónoma infinita exige emisor profundo E_infty/iteradores completos.
