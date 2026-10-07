"""Exact focal tests and preservation checks for the IX successor.

No external libraries or network. Writes only the requested JSON receipt.
The tests supplement the proofs; they do not certify the whole HMT corpus
or compilation/visual quality of the successor PDFs.
"""
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial, prod
from pathlib import Path
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'DEPURACION_ENTREGA_HMT_MD_20260923/ENTREGA_HMT_USB/03_FUENTES_Y_REPRODUCCION/COLECCION_DOCUMENTAL/02_ARTICULOS/VIII'
ADDITIONS = ('corte_irreducibles.tex', 'composicion_lectores.tex',
             'normalizacion_stieltjes.tex', 'bendersky_glaisher.tex')
MODIFIED = ('main_lectura.tex',
            'gestion/lectura_generada/02_ORDEN_ESPECTRAL_Y_MOMENTOS.tex',
            'gestion/lectura_resumen.tex', 'gestion/lectura_conclusiones.tex')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def exact_tests():
    counts = Counter()
    for table in ((1, -1, 0), (1, 0, -1, 0), (2, -3, 1, 4)):
        q = len(table)
        for r in (F(1, 3), F(1, 2), F(2, 3)):
            polynomial = sum(F(a) * r**j for j, a in enumerate(table, 1))
            for blocks in (1, 2, 5):
                finite = sum(F(table[(n-1) % q]) * r**n
                             for n in range(1, q*blocks+1))
                require(finite == polynomial*(1-r**(q*blocks))/(1-r**q), 'heat kernel')
                counts['periodic_heat_kernel'] += 1
    a, b = (1, -1, 0), (1, 0, -1, 0)
    for limit in (6, 12, 24):
        va = lambda n: F(a[(n-1) % len(a)])
        vb = lambda n: F(b[(n-1) % len(b)])
        product_moments = (sum(va(n)/n**2 for n in range(1, limit+1)) *
                           sum(vb(n)/n**2 for n in range(1, limit+1)))
        convolution = {}
        for m in range(1, limit+1):
            for n in range(1, limit+1):
                convolution[m*n] = convolution.get(m*n, F(0)) + va(m)*vb(n)
        require(product_moments == sum(v/F(k*k) for k, v in convolution.items()), 'tensor regrouping')
        require([va(n)*vb(n) for n in range(1, limit+1)] ==
                [F(a[(n-1)%3]*b[(n-1)%4]) for n in range(1, limit+1)], 'diagonal table')
        counts['tensor_and_diagonal'] += 1
    require(F(3,4)-3*F(1,4) == 0, 'zero moment example')
    require(sum(1 for d in range(1,3) if 2%d == 0) != 1, 'diagonal is not convolution')
    counts['negative_controls'] += 2

    def transform(g, ell):
        return [sum(F(comb(n,j))*g[j]*ell**(n-j) for j in range(n+1)) -
                ell**(n+1)/F(n+1) for n in range(len(g))]
    g = [F((-1)**j*(j+2), j+3) for j in range(9)]
    for ell in (F(-2), F(0), F(2,3), F(3)):
        for m in (F(-1,2), F(0), F(5,4)):
            require(transform(transform(g, ell), m) == transform(g, ell+m), 'Stieltjes composition')
            counts['stieltjes_composition'] += 1
        require(transform(transform(g, ell), -ell) == g, 'Stieltjes inverse')
        counts['stieltjes_inverse'] += 1
        result = transform(g, ell)
        for n in range(len(g)):
            coeff = (-ell)**(n+1)/F(factorial(n+1)) + sum(
                F((-1)**j, factorial(j))*g[j]*(-ell)**(n-j)/factorial(n-j)
                for j in range(n+1))
            require(result[n] == (-1)**n*factorial(n)*coeff, 'Laurent pole coefficient')
            counts['laurent_coefficients'] += 1
    require(transform(g, F(1))[0] != g[0], 'omitting polar term must fail')
    counts['negative_controls'] += 1

    bernoulli = [F(1)]
    for n in range(1, 12):
        bernoulli.append(-sum(F(comb(n+1,j))*bernoulli[j] for j in range(n))/F(n+1))
    expected = (F(0), F(1,12), F(0), F(-11,720), F(0))
    for k, expected_value in enumerate(expected):
        harmonic = sum((F(1,j) for j in range(1,k+1)), F(0))
        require(harmonic*bernoulli[k+1]/(k+1) == expected_value, 'Bendersky normalizer')
        counts['bendersky_normalizers'] += 1
    for n in range(1, 6):
        require(bernoulli[2*n+1] == 0, 'odd Bernoulli number')
        gamma_half = prod((F(2*j-1,2) for j in range(1,n+1)), start=F(1))
        gamma_residue = F(2*(-1)**n, factorial(n))
        derivative_coefficient = gamma_half/gamma_residue
        require(derivative_coefficient == F((-1)**n*factorial(2*n), 2*4**n), 'gamma residue ratio')
        counts['even_negative_residue'] += 1
    require(bernoulli[1] != 0, 'level zero is distinct')
    counts['negative_controls'] += 1

    def prime(n):
        return n >= 2 and all(n%d for d in range(2, int(n**0.5)+1))
    for y in range(2, 33):
        for m in (y+1, y+7, y+31):
            all_product = prod((1-F(1,(n-1)**2) for n in range(y+1,m+1)), start=F(1))
            prime_product = prod((1-F(1,(n-1)**2) for n in range(y+1,m+1) if prime(n)), start=F(1))
            require(all_product == F(m*(y-1), y*(m-1)), 'product telescoping')
            require(F(y-1,y) <= all_product <= prime_product <= 1, 'prime inclusion direction')
            require(sum(F(1,2*n*(n-1)) for n in range(y+1,m+1)) == F(1,2*y)-F(1,2*m), 'sum telescoping')
            counts['prime_cut_telescoping'] += 1
    for p in range(2, 32):
        tail = sum(F(1,k*p**k) for k in range(2,40))
        require(0 < tail < F(1,2*p*(p-1)), 'log tail bound')
        counts['log_tail_bounds'] += 1
    require(1-F(1,(2-1)**2) == 0, 'excluded mode two')
    counts['negative_controls'] += 1
    return dict(counts)


def is_subsequence(old, new):
    it = iter(new)
    return all(any(line == candidate for candidate in it) for line in old)


def source_checks():
    records = {}
    for lang in ('ES', 'EN'):
        source = HERE/'IX'/lang/'source'
        base = BASE/lang/'ARCHIVOS/source'
        previous = [p for p in base.rglob('*') if p.is_file()]
        unchanged, changed = 0, []
        for old in previous:
            rel = old.relative_to(base)
            new = source/rel
            require(new.is_file(), f'Missing inherited file: {lang}/{rel}')
            if digest(old) == digest(new):
                unchanged += 1
            else:
                require(str(rel) in MODIFIED, f'Unlisted edit: {lang}/{rel}')
                require(is_subsequence(old.read_text().splitlines(), new.read_text().splitlines()),
                        f'Original line lost: {lang}/{rel}')
                changed.append(str(rel))
        all_tex = '\n'.join(p.read_text(errors='replace') for p in source.rglob('*.tex'))
        labels = set(re.findall(r'\\label\{([^}]+)\}', all_tex))
        labels.update(re.findall(r'\\HMTresultado\{[^}]*\}\{[^}]*\}\{([^}]+)\}', all_tex))
        new_labels = []
        for filename in ADDITIONS:
            path = source/'ampliacion'/filename
            value = path.read_text()
            new_labels += re.findall(r'\\label\{([^}]+)\}', value)
            new_labels += re.findall(r'\\HMTresultado\{[^}]*\}\{[^}]*\}\{([^}]+)\}', value)
            for ref in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', value):
                require(ref in labels, f'Unresolved new reference: {ref}')
            stack = []
            for kind, env in re.findall(r'\\(begin|end)\{([^}]+)\}', value):
                if kind == 'begin':
                    stack.append(env)
                else:
                    require(stack and stack.pop() == env, f'Environment mismatch: {path}')
            require(not stack, f'Unclosed environment: {path}')
        require(len(new_labels) == len(set(new_labels)), 'Duplicate new labels')
        main = (source/'main_lectura.tex').read_text()
        for filename in ADDITIONS[1:]:
            require(main.count('\\input{ampliacion/'+filename+'}') == 1, 'Missing or repeated main inclusion')
        body = (source/'gestion/lectura_generada/02_ORDEN_ESPECTRAL_Y_MOMENTOS.tex').read_text()
        require(body.count('\\input{ampliacion/corte_irreducibles.tex}') == 1, 'Missing prime cutoff inclusion')
        records[lang] = {'inherited_files': len(previous), 'unchanged_files': unchanged,
                         'additively_modified_files': changed, 'new_labels': new_labels,
                         'new_source_sha256': {n: digest(source/'ampliacion'/n) for n in ADDITIONS}}
    require(records['ES']['new_labels'] == records['EN']['new_labels'], 'Label parity ES/EN')
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--algebra-only', action='store_true',
                        help='Run the portable exact tests without requiring the historical source tree.')
    args = parser.parse_args()
    result = {'status': 'PASS_RESTITUCION_IX_FOCAL', 'exact_checks': exact_tests(),
              'source_conservation': None if args.algebra_only else source_checks(),
              'full_corpus_proof_audited': False,
              'pdf_compiled': False, 'visual_qa_completed': False,
              'scope': ('Exact local algebra checks only; no source comparison in portable mode.'
                        if args.algebra_only else
                        'Exact local checks, added-source linkage, translation label parity and preservation of every inherited file/line.')}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
