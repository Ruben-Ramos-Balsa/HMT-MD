# Bibliografía del Artículo VI: verificación y procedencia

Fecha de revisión bibliográfica: 10 de septiembre de 2026.
Alcance: metadatos bibliográficos y fuentes de los datos congelados. No se han
actualizado valores ni se ha emitido una certificación matemática del artículo.
La fuente entregada es `sections/99_bibliografia.tex`; no se ha modificado el
ensamblaje `main.tex` ni se ha compilado.

## Fuentes primarias externas

1. **Musto–Vicary, 2016**, clave `mustovicary`. El editor confirma autores,
   título, volumen 16, números 15–16, páginas 1318–1332 y DOI.
   https://www.rintonpress.com/journals/doi/QIC16.15-16-4.html
   DOI: https://doi.org/10.26421/QIC16.15-16-4
2. **De las Cuevas–Drescher–Netzer, 2020**, clave `delascuevas2020`.
   La ficha de la prepublicación remitida por los autores confirma autores,
   título, referencia publicada `J. Math. Phys. 61, 111704 (2020)` y DOI.
   https://arxiv.org/abs/1912.07332
   DOI: https://doi.org/10.1063/5.0022344
   El acceso directo al editor devolvió HTTP 403; se utilizó la fuente primaria
   de los autores, no una cita bibliográfica de terceros.
3. **De las Cuevas–Netzer–Valentiner-Branth, 2023**, clave `delascuevas2023`.
   La ficha de los autores confirma el nombre Inga Valentiner-Branth, el volumen
   64, el número de artículo 022201, el año 2023 y el DOI.
   https://arxiv.org/abs/2209.10230
   DOI: https://doi.org/10.1063/5.0127393
   El editor devolvió HTTP 403; la comprobación se hizo en la prepublicación.
4. **CODATA 2018**, clave `codata2018`. NIST confirma autores, ajuste 2018,
   publicación de 2021 y referencia `Rev. Mod. Phys. 93, 025010`.
   https://physics.nist.gov/cuu/Constants/archive2018.html
   Texto original alojado en NIST:
   https://physics.nist.gov/cuu/pdf/RevModPhys.93.025010.pdf
   Tabla archivada:
   https://physics.nist.gov/cuu/Constants/ArchiveASCII/allascii_2018.txt
   DOI: https://doi.org/10.1103/RevModPhys.93.025010
5. **CODATA 2022**, clave `codata2022`. La página específica de NIST y la
   publicación de APS confirman autores, ajuste 2022 y publicación de 2025,
   `Rev. Mod. Phys. 97, 025002`.
   https://physics.nist.gov/cuu/Constants/article2022.html
   DOI: https://doi.org/10.1103/RevModPhys.97.025002
   No se ha supuesto la existencia de un archivo `archive2022.html`: la URL
   incorporada es la página explícita del ajuste 2022. La página general de
   NIST muestra valores 2022 al consultarla, pero no se utiliza como selector
   de una edición futura ni como sustituto de las tablas congeladas.
6. **PDG 2026**, clave `pdg2026`. La página oficial confirma la referencia
   `F. Takahashi et al. (Particle Data Group), Int. J. Mod. Phys. A 41,
   2630011 (2026)` y enlaza el DOI. La página oficial de acceso programático
   identifica expresamente la edición 2026 y sus bases de datos.
   https://pdg.lbl.gov/2026/
   https://pdg.lbl.gov/2026/api/index.html
   DOI enlazado por PDG: https://doi.org/10.1142/S0217751X26300115
   El destino editorial directo no pudo abrirse mediante el navegador; los
   metadatos se acreditan en la propia página oficial del Particle Data Group.

Las tres primeras claves son las únicas referencias externas citadas mediante
`\cite` en `sections/nucleo.tex` en el corte revisado. CODATA y PDG se añaden
como fuentes del contraste descrito en la sección 07 y del catálogo. No se
han trasladado las restantes referencias del Artículo I sin uso efectivo en VI.

## Identidad de los datos metrológicos conservados

Se leyó `technical/catalogo_manifiesto.json` junto con
`technical/catalogo_observables.json`. El catálogo de observables conserva
855 registros: 471 de masa y 384 de anchura. Sus campos documentales dicen:

- `source_edition`: `2026`.
- `source_cutoff`: `2026-01-15`.
- Consulta consignada en el propietario del integral: `2026-07-26`.
- `source_snapshot_sha256`:
  `40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe`.

La existencia de una edición oficial 2026 se verificó en PDG. Eso no demuestra
identidad byte a byte entre la instantánea local y una descarga actual. No se
ha descargado una base de datos nueva ni reemplazado la conservada. El corte y
la fecha de consulta anteriores son metadatos del corpus local, no fechas
atribuidas retrospectivamente al lanzamiento de la edición pública. Se conservan
los tipos, límites, incertidumbres y estados de cada registro sin promoverlos
a predicciones internas.

## Antecedentes internos citados

Autores: Oumar Haidara Fall y Rubén Ramos Balsa. Todas las entradas se describen
como manuscritos de trabajo inéditos. Los localizadores de versión no cambian
el título literal del artículo ni sustituyen una prueba.

- `hmtintegral`: *El cierre holográfico del infinito: la estructura discreta
  del continuo y el origen de las constantes fundamentales*, 2.249 páginas,
  revisión editorial del 5 de septiembre de 2026. Título contrastado con la
  bibliografía del Artículo I y versión contrastada con `CORPUS_ACTIVO.md`.
  `/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/02_PDF/INTEGRAL/main_paquete_union_demostrativa_20260904.pdf`
- `hmtmasasrev2`: *Teoría holográfica integral de la masa*, REV.2, 20 de agosto
  de 2026, 479 páginas. Título confirmado por `pdftitle` y cabeceras de la fuente
  `tmp/pdfs/hmt_masas_rev2/teoria_holografica_integral_masa_rev2.tex`.
  `/Users/ruben/Documents/New project/PUBLICACION_HMT/TEORIA_HOLOGRAFICA_INTEGRAL_MASA_HMT_MD_REV2_2026-08-20/output/pdf/TEORIA_HOLOGRAFICA_INTEGRAL_DE_LA_MASA_HMT_MD_REV2_2026-08-20.pdf`
  SHA-256 de referencia: `b56bb38d10b9a4f4d0de47b7da8010fb31a6e8e8684a3bfd4237e37d7a3dddfa`.
- `hmtarticuloI`: título científico conservado; revisión de representación
  espinorial y helicidad del 10 de septiembre de 2026, 127 páginas.
  `/Users/ruben/Documents/New project/output/CANTERA_ARTICULO_PI_PHI_E_ALPHA_ELECTRON_20260906/ARTICULO_HELICIDAD_ELECTRON_20260910/output/pdf/ARTICULO_I_HELICIDAD_ELECTRON.pdf`
  SHA-256 de referencia: `3008c548303b423f5ae359ce8ab0b87d37e63857a1fd1891bcdbb34f82608045`.
- `hmtarticuloII`: título contrastado con `manuscrito/main.tex`, revisión 09,
  208 páginas. Se distingue la entrega del 10 de septiembre de la fecha impresa
  conservada en la portada.
  `/Users/ruben/Documents/New project/output/ARTICULO_II_REV09_ENTREGA_20260910/output/pdf/ARTICULO_II_REVISION_09.pdf`
  SHA-256 de referencia: `45f9fe37e50753601671e35375022e3c5666158692fb3cb3ca3ce0945c3992a8`.
- `hmtarticuloIII`: *Estructura constitutiva del vacío electromagnético*,
  revisión 03, 149 páginas.
  `/Users/ruben/Documents/New project/output/ARTICULO_III_VACIO_ELECTROMAGNETICO_20260910_REV03/output/pdf/ARTICULO_III_ESTRUCTURA_CONSTITUTIVA_VACIO_ELECTROMAGNETICO.pdf`
  SHA-256 de referencia: `bdb315b76011df805433307085a9477e0a290a8e0e64e8e4223d56edae5c0164`.
- `hmtarticuloIV`: *Moonshine, dualidad T y teoría M desde la estructura
  discreta del continuo*, borrador del 10 de septiembre de 2026, 116 páginas.
  Título contrastado con `main.tex`.
  `/Users/ruben/Documents/New project/output/ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M_20260910/output/pdf/ARTICULO_IV_MOONSHINE_DUALIDAD_TEORIA_M.pdf`
  SHA-256 de referencia: `76e59c3051ba2048041b6ae83a89eb35ac4a7e7ba8eb5f20fc71403142897dfc`.
- `hmtarticuloV`: *Estadística cuántica y radiación. Estados genealógicos,
  evolución unitaria y distribuciones de ocupación*, título provisional,
  borrador del 10 de septiembre de 2026, 142 páginas. Ambas líneas del título
  se verificaron en `manuscrito/preambulo.tex` y su inclusión en la portada.
  `/Users/ruben/Documents/New project/output/ARTICULO_V_ESTADISTICA_CUANTICA_RADIACION_20260910/output/pdf/ARTICULO_V_ESTADISTICA_CUANTICA_RADIACION.pdf`
  SHA-256 de referencia: `a931b4f11dfb53b82b644f53aad80452b57601e85fabaea492568c55f9ecf4e4`.

Las huellas anteriores son las referencias de versión del corpus vigente; la
presente tarea bibliográfica no las presenta como una nueva revisión integral
de esos PDFs. No se han alterado los índices compartidos ni las fuentes anteriores.

## Control estático de la entrega

Se ejecutaron `inspect_file` y `aggregate` del verificador reproducible
`technical/verificar_fuentes_vi.py` sobre la bibliografía y todas las secciones.
Resultado: 13 entradas bibliográficas, claves únicas, ningún hallazgo de sintaxis
en el archivo nuevo y ninguna cita sin `bibitem` entre las secciones disponibles.
El resultado no afirma que `main.tex` haya incorporado todavía la bibliografía:
esa integración corresponde al editor principal. No se ha realizado compilación
ni revisión visual dentro de esta subtarea.
