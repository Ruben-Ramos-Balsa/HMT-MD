# Artículo II: composición sobre el registro seleccionado

Estas dos entradas consumen el mismo `SelectedAction.alpha/phi/pi` del Artículo I. Su dominio analítico ya está demostrado en `SelectedAction.action_domain`. No se reconstruye un `Ledger` a partir de las cifras deseadas ni se introduce una nueva premisa `PublishedRegister`.

## CKM

`SelectedCKMPublication.lean` reúne las reglas sectoriales declaradas, las coordenadas angulares de acción y torsión, la inversión del lector, la matriz unitaria, la positividad de su cuarteto de Jarlskog y el transporte espectral. También demuestra la obstrucción a una refase real y el determinante del conmutador. Las masas son lectores posteriores arbitrarios; su no degeneración sólo se exige para la conclusión de determinante no nulo.

La unicidad corresponde al sistema de reglas sectoriales escrito en el manuscrito, no a cualquier regla imaginable con los mismos seis cardinales. Se reutilizan las demostraciones matriciales y espectrales anteriores.

Terminal: `HMT.II.CKM.SelectedPublication.selected_ckm_principal_chain`.
Recibo: `CKM_VERIFICATION.json`.

## Acción, realización circular y transducción térmica

`SelectedActionGravityThermal.lean` aplica la misma acción seleccionada a la familia gravitatoria circular y a la lectura térmica. Se obtiene el selector `(54/pi)^2` por la igualdad de radios `G*m/c^2`; también la unicidad del transductor que satisface `b*Theta*log(3)=E_ciclo`, su transporte entre orientaciones y la identidad de área compartida.

Las bases positivas de acción, velocidad y tiempo, y la sección térmica positiva, permanecen explícitas. No se deducen de una cifra SI introducida como dato.

Terminal: `HMT.II.SelectedActionGravityThermal.selected_action_gravity_thermal_chain`.
Recibo: `verification_action_gravity_thermal/VERIFICATION.json`.

El consumidor térmico de V utiliza `thermalCoefficient` y `thermalCoefficient_pos` de esta entrada; no necesita postular otra constante de Boltzmann.

## Reproducción y continuidad

Los dos scripts locales reproducen estas entradas contra la entrega preservada del primer artículo y Lean 4.21.0/Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`. La entrega acumulativa añade el reproductor portátil con rutas relativas. Los archivos y recibos históricos quedan intactos; los registros actuales distinguen los objetos reutilizados y las fuentes recompiladas.

Los terminales heredan `Lean.ofReduceBool` del selector regional y los axiomas ordinarios declarados en sus salidas de compilación. No incorporan axiomas científicos nuevos ni una premisa que afirme el registro final.

La discrepancia histórica del verificador de arranque es exclusivamente la actualización autoral de `AGENTS.md` del 21 de septiembre sobre los enlaces a petición. Se conserva su `FAIL` y la conciliación documental existente; no se presenta como un nuevo `PASS` global.
