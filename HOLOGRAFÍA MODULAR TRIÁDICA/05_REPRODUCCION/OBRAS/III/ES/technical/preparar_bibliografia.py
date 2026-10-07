#!/usr/bin/env python3
"""Conserva la bibliografía anterior y registra el corte autoral vigente."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'base_articulo_I/sections/bibliografia.tex').read_text()
s=s.replace('edición rectora de 2\\,084 páginas, revisión del 1 de septiembre de 2026, y desarrollos especializados posteriores identificados en el registro de procedencia.',
            'testigo histórico de 2\\,084 páginas, revisión del 1 de septiembre de 2026. La consulta activa de esta serie utiliza la compilación integral de 2\\,249 páginas del 5 de septiembre de 2026, indicada en la referencia de edición integral.')
extra=(ROOT/'base_articulo_II/BIBITEMS_ADICIONALES_II.tex').read_text()
s=s.replace('\\end{thebibliography}',extra+'\n'+r'\bibitem{hmtconfluencia} O. Haidara Fall y R. Ramos Balsa, \emph{Transporte orientado, respuesta del vacío y funcional de Barbero--Immirzi}. Desarrollo del 7 de septiembre de 2026, con los propietarios \emph{Red de lectores, momentos y sustituciones}, sección 9, y el capítulo de residuos de vacío y Barbero. Manuscritos de trabajo conservados en el paquete de reproducción.'+'\n'+r'\end{thebibliography}')
(ROOT/'manuscrito/bibliografia.tex').write_text(s)
print('Bibliografía reunida; original conservado.')
