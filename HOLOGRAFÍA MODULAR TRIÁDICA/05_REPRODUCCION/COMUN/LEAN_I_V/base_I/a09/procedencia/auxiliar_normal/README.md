# Auxiliar algebraico del producto normal

Se han compilado cinco teoremas en Lean 4.21.0. La prueba es algebraica finita y se entrega al editor central para el levantamiento a los campos de Laurent existentes. No modifica K ni ningún PDF, paquete sellado o fuente central.

Para un anillo R, sea N(a,b)(X)=aX+Xb. El teorema principal demuestra

\[
N(a,b)(N(c,d)(X))-N(c,d)(N(a,b)(X))
=(ac-ca)X+X(db-bd).
\]

Por tanto, ac=ca y bd=db implican conmutación de los pasos normales. Los términos mixtos se cancelan por asociatividad; no se exige que creadores y aniquiladores conmuten entre sí.

Además se demuestra que, para pasos exclusivamente izquierdos o exclusivamente derechos, la conmutación uniforme es equivalente a la conmutación de sus coeficientes. El ejemplo matricial E12/E21 constituye un falsador de la afirmación sin hipótesis: sobre la identidad, el defecto es diag(1,-1).

## Aplicación pendiente en la fuente central

En `LatticeNormalOrderedField.lean`, la suma es finita después de actuar sobre cada vector, no una suma finita uniforme de endomorfismos. El editor central conserva el paso adicional:

1. Fijar coeficiente k y estado v.
2. Probar soporte finito conjunto en N×N de las cuatro contribuciones CC, CA, AC y AA.
3. Distribuir las aplicaciones lineales e intercambiar sumas finitas.
4. Aplicar conmutación de los modos del mismo signo y cerrar por extensionalidad.
5. Deducir invariancia por intercambios adyacentes y por `List.Perm`.

Los límites inferiores Laurent y los límites de modos no negativos existentes permiten construir esas cotas. Este auxiliar no afirma que esos cinco pasos ya estén integrados.

## Reproducción

Ejecutar `bash reproduce.sh` desde cualquier directorio. Se usa el entorno Mathlib autenticado del proyecto y se recompila únicamente este módulo. Los cinco `#print axioms` quedan en la salida estándar. El recibo conserva la compilación realizada en esta entrega; el script no sobrescribe ese recibo.

Procedencia: FORMALIZACION_NUEVA como auxiliar finito del siguiente paso registrado en CONTINUIDAD_I.md. El resultado no es una nueva prueba de selección de K ni una formalización completa de Moonshine.
