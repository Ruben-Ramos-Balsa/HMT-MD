"""Archivo de mensajes públicos de dos conversaciones expresamente autorizadas.

No extrae razonamiento, herramientas, mensajes de agentes ni instrucciones del sistema.
La copia conserva el texto; el visor de consola puede ocultar colas bibliográficas.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'REV04_RELECTURA_Y_JERARQUIA' / 'conversaciones'
SOURCES = {
    'radion': Path('/Users/ruben/.codex/sessions/2026/07/31/rollout-2026-07-31T02-06-41-019fb435-03c2-78c1-a31f-2e3fb909ac07.jsonl'),
    'revisar_tesis': Path('/Users/ruben/.codex/sessions/2026/09/04/rollout-2026-09-04T22-31-36-01a06cd5-0aca-7de0-a2f7-c730b928c4d0.jsonl'),
}

def save_new(path, text):
    raw = text.encode('utf-8')
    if path.exists():
        if path.read_bytes() != raw:
            raise RuntimeError(f'No se sobrescribe la captura: {path}')
    else:
        path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'scope': '10 últimas intervenciones de usuario y mensajes públicos posteriores disponibles en la captura', 'threads': []}
    for name, path in SOURCES.items():
        messages = []
        raw = path.read_bytes()
        for line in raw.splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            p = item.get('payload', {})
            if item.get('type') != 'response_item' or p.get('type') != 'message':
                continue
            if p.get('role') not in ('user', 'assistant') or p.get('channel') == 'analysis':
                continue
            text = ''.join(c.get('text', '') for c in p.get('content', []) if c.get('type') in ('input_text', 'output_text', 'text'))
            if not text:
                continue
            if p['role'] == 'user' and text.lstrip().startswith(('<environment_context>', '<recommended_plugins>', '# AGENTS.md instructions', '<permissions instructions>')):
                continue
            messages.append({'timestamp': item.get('timestamp'), 'role': p['role'], 'phase': p.get('phase'), 'message_id': p.get('id'), 'turn_id': p.get('internal_chat_message_metadata_passthrough', {}).get('turn_id'), 'text': text})
        users = [i for i, m in enumerate(messages) if m['role'] == 'user']
        selected = messages[users[-10]:]
        data = {'name': name, 'source': str(path), 'source_bytes_at_snapshot': len(raw), 'source_sha256_at_snapshot': hashlib.sha256(raw).hexdigest(), 'messages': selected}
        sha = save_new(OUT / f'{name}_10_intervenciones_autorales.json', json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        lines = [f'# {name}: diez intervenciones recientes y sus respuestas disponibles\n', 'Copia de mensajes públicos. Se excluyen herramientas, razonamiento e instrucciones internas. La conversación puede seguir activa después de esta captura.\n']
        n = 0
        attachments = []
        for m in selected:
            if m['role'] == 'user':
                n += 1
            lines.extend([f'## Intervención {n} · {m["role"]} · {m["phase"] or "mensaje"} · {m["timestamp"]}\n', m['text'], '\n'])
            if m['role'] == 'user':
                for s in re.findall(r'/Users/ruben/\.codex/attachments/[^\s<>"`)]+/pasted-text\.txt', m['text']):
                    if s not in attachments:
                        attachments.append(s)
        for s in attachments:
            source = Path(s)
            if source.is_file():
                content = source.read_text()
                lines.extend([f'## Texto adjunto íntegro · {s}\n', content, '\n'])
        md_sha = save_new(OUT / f'{name}_10_intervenciones_autorales.md', '\n'.join(lines))
        manifest['threads'].append({'name': name, 'user_messages': n, 'public_messages': len(selected), 'first_timestamp': selected[0]['timestamp'], 'last_timestamp': selected[-1]['timestamp'], 'json_sha256': sha, 'markdown_sha256': md_sha, 'attachments': attachments, 'is_mathematical_verification': False})
    save_new(OUT / 'MANIFIESTO_CAPTURA_AUTORAL.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
