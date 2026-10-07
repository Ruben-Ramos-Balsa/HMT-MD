from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
base=Path('/Users/ruben/Documents/New project/output/REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA')
source=base/'04_RECIBOS/RECIBO_GENEALOGIA_UNICA_APP_TRIT_TPK.json'
data=json.loads(source.read_text())
def visit(obj):
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key=='path' and isinstance(value,str) and not Path(value).is_absolute():
                obj[key]=str(base/value)
            else: visit(value)
    elif isinstance(obj,list):
        for value in obj: visit(value)
visit(data)
data['formal_kernel']['typed_operator_graph']['path']='/Users/ruben/Documents/New project/PUBLICACION_HMT/REGISTRO_DE_CONTINUIDAD_ACADEMICA/NUCLEO_FORMAL_HMT_PERMANENTE/TPK_GRAFO_OPERATORIO_TIPADO.json'
data['relocation_note']='Recibo del antecedente, con rutas absolutas locales. Conserva hashes y alcance del original; no certifica las ampliaciones REV03.'
(root/'metadata/RECIBO_GENEALOGIA_ANTECEDENTE_LOCAL.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
