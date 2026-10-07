# HMT G9 — rama continuada a 20 bloques / 12 triadas

Este paquete continúa la rama publicada usando el ledger vigente de bloques
ternarios y triadas. Los nombres pi/e/phi son etiquetas obtenidas por
comparación; el paquete no demuestra un selector autónomo.

## Rama de 20 bloques

pi:
010211|012222|010211|002111|110221|222220|111201|212121|200121|100100|101222|022212|012012|111210|121011|200220|120210|000101|022010|020111

e:
201101|121221|102011|012222|102011|021222|201202|222210|212212|020112|112221|110001|202222|112102|102010|022020|222002|012010|001112|022212

phi:
121200|112202|121020|010210|010200|102011|221021|200221|110110|010122|112002|100021|000120|211122|202200|202110|221000|100102|111122|020010

## 12 triadas emitidas

pi = 141|592|653|589|793|238|462|643|383|279|502|884
e = 718|281|828|459|045|235|360|287|471|352|662|497
phi = 618|033|988|749|894|848|204|586|834|365|638|117

## Alfa calculada condicionalmente por transporte derecha-izquierda

s_m=d_pi+d_e-d_phi-K_m+c_{m+1}; d_alpha=s_m mod 1000; c_m=(s_m-d_alpha)/1000; c_13=0

K_R = 234|543|140|729|659|824|621|058|914|794|146|601

alpha = 0.007|297|352|569|283|800|997|285|105|472|380|663

memoria_transporte c0..c12 = [0, 0, 0, -1, -1, -2, -1, 0, -1, -1, 0, 0, 0]

## Persistencia t=5..13

Cada puerta parte de 729 candidatos q,a; firma completa, cilindro intervalar y
persistencia seleccionan la candidata publicada dentro del ledger.
Ver CSV `g9_persistencia_t5_t13.csv`.
