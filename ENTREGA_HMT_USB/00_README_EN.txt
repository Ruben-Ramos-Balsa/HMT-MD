HMT–MD SCIENTIFIC LIBRARY

OPEN FIRST: 00_START_HERE.html
Español: 00_EMPEZAR_AQUI.html
Français: 00_COMMENCER_ICI.html

01_PDF_ESPANOL     Spanish PDFs.
02_PDF_ENGLISH     English PDFs.
03_PDF_FRANCAIS    French PDFs.
04_FUENTES_LATEX   Editable sources by language and work; guide sources are Python/JSON.
05_REPRODUCCION    Programs, data, Lean proofs, certificates and shared libraries.
06_VERIFICACION    File inventories, hashes and copy verification.

Each reading index starts with the 20-page guide, then four reference works,
twelve monographs and the mass appendix. The 2,249-page integral is available
in Spanish and is shared by all three collections; no translation is supplied.
There are 52 distinct reading PDFs. They can be read offline on Mac, Windows
or Linux. Inserting the USB does not launch any program.

Keep the complete folder together for reproduction. All catalogue links are
relative. Individual PDFs may be copied separately for reading or printing.
Use 05_REPRODUCCION/INDEX.html for the corresponding programs and instructions.
Scientific code and data serve all language editions.

Install the execution software appropriate to your operating system: Python,
a TeX distribution to rebuild manuscripts, and Lean 4.21.0 for the formal proofs.
The exact Mathlib revision and eight dependencies are included as source, with
licences and Git identities. See 05_REPRODUCCION/DEPENDENCIAS/mathlib4/LEER_MATHLIB_FUENTES.md
for the library build and ProofWidgets requirements. Guide fonts and dependencies
are described in 04_FUENTES_LATEX/GUIA/README.txt.
Copy ENTREGA_HMT_USB directly to the USB drive root, for example,
E:\ENTREGA_HMT_USB. All paths then fit the classic Windows path limit without
a special copy tool. Avoid adding long parent folder names. Native Windows
scientific execution has not been tested in this delivery.

CHECK THE COPY WITHOUT SCIENTIFIC RECOMPUTATION
macOS/Linux: python3 06_VERIFICACION/verificar_integridad.py
Windows:     py -3 06_VERIFICACION/verificar_integridad.py

These checks verify file integrity and paths, not mathematical validity.
Each scientific unit retains the scope of its proofs and recorded certificates.
The PDFs and LaTeX/Lean sources were retained without recompilation.
Only the exact Fricke identity check was rerun to replace a truncated receipt;
see 06_VERIFICACION/REPRODUCCION_RECIBO_FRICKE.json for its program and scope.
See 05_REPRODUCCION/MAPA_CIENTIFICO.html for work-to-file correspondence and
05_REPRODUCCION/LEER_DEPENDENCIAS.txt for updated reproduction instructions.
