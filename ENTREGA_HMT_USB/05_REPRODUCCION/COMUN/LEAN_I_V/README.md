# Fuentes Lean I–V / Lean I–V sources / Sources Lean I–V

ES — La entrada oficial de esta unidad es `reproducir.py`. El registro mantiene
542 módulos con sus importaciones, objetos y entradas por artículo. Las carpetas
`base_I/a01`…`base_I/a11` sustituyen las cadenas repetidas de directorios. Los
archivos científicos conservan todos sus bytes; `INDICE_RUTAS.json` relaciona
cada ruta de origen con su ubicación actual y huella SHA-256. Los demás scripts
se conservan como fuentes auxiliares y no son entradas vigentes de esta unidad.

EN — Use `reproducir.py` as the official entrypoint. The registry retains 542
modules, their imports, objects and article targets. `base_I/a01`…`base_I/a11`
replace repeated directory chains. Scientific files are byte-identical;
`INDICE_RUTAS.json` maps every original path to its current path and SHA-256.
Other preserved scripts are auxiliary sources, not current package entrypoints.

FR — L’entrée officielle est `reproducir.py`. Le registre conserve 542 modules,
leurs importations, objets et entrées par article. `base_I/a01`…`base_I/a11`
remplacent les chaînes répétées de dossiers. Les fichiers scientifiques restent
identiques octet par octet ; `INDICE_RUTAS.json` associe les anciens chemins aux
chemins actuels et aux empreintes SHA-256. Les autres scripts sont des sources
auxiliaires, non des points d’entrée actuels.

## Comprobar / Check / Vérifier

Desde esta carpeta, con una carpeta de informes nueva fuera de ella / From this
folder, choose a new report folder outside it / Depuis ce dossier, choisir un
nouveau dossier de rapports à l’extérieur :

```text
python3 -I -S reproducir.py --verify-only --report-dir /ruta/nueva/integridad
```

Windows (PowerShell):

```text
py -3 -I -S reproducir.py --verify-only --report-dir C:/HMT/resultados_nuevos
```

ES — Este comando verifica archivos y registro sin invocar Lean. Para reconstruir,
use las opciones de `python3 -I -S reproducir.py --help`. Se conservan Lean 4.21.0,
Mathlib `308445d7985027f538e281e18df29ca16ede2ba3` y todos los controles originales.
En otra plataforma, la reconstrucción completa usa `--from-sources
--portable-toolchain`. El cambio de rutas no recompila ni amplía la formalización.

EN — This checks files and registry without invoking Lean. For rebuilding, see
`python3 -I -S reproducir.py --help`. Lean 4.21.0, Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3` and every original check are retained.
On another platform, full rebuilding uses `--from-sources --portable-toolchain`.
Path relocation neither recompiles nor extends the formalization.

FR — Cette commande vérifie les fichiers et le registre sans appeler Lean. Pour
reconstruire, voir `python3 -I -S reproducir.py --help`. Lean 4.21.0, Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3` et tous les contrôles restent inchangés.
Sur une autre plateforme, utiliser `--from-sources --portable-toolchain` pour une
reconstruction complète. Le déplacement ne recompile ni n’élargit la formalisation.

ES — Recibos, certificados, módulos adicionales y datos se conservan íntegros.
Los documentos que citan rutas anteriores se consultan con el índice. La lectura
científica original completa está en `indice/lectura_original.md`.
EN — All receipts, certificates, additional modules and data are preserved.
Resolve earlier path references through the index. The full original scientific
reading guide is at `indice/lectura_original.md`.
FR — Reçus, certificats, modules supplémentaires et données sont intégralement
conservés. L’index permet de résoudre les anciennes références. Le guide de
lecture scientifique original est dans `indice/lectura_original.md`.
