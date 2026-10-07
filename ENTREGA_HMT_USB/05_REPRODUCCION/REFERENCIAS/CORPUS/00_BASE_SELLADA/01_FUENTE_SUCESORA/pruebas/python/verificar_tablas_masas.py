"""Recalcula E0--E4 desde la tabla local versionada."""
from __future__ import annotations
import csv
import json
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'datos' / 'tabla_etapas_caracter_masa.csv'

def close(a: float, b: float, rtol: float=3e-12, atol: float=1e-10) -> None:
    if not math.isclose(a, b, rel_tol=rtol, abs_tol=atol):
        raise AssertionError(f'{a!r} != {b!r}')

def rms(xs: list[float]) -> float:
    return math.sqrt(sum((x * x for x in xs)) / len(xs))

def main() -> None:
    alpha = 1.0 / 137.035999084
    A_rad = math.radians(1000 * alpha)
    C_rad = math.radians(2.123738338968646)
    D4 = (math.pi - math.e * math.log(math.pi)) / 270 * (1 + math.pi / 729)
    q_plus = math.exp(-A_rad - C_rad)
    q_minus = math.exp(-A_rad + C_rad)
    s120 = q_minus ** 120 - q_plus ** 120
    z270 = 135 * D4 ** 2
    s180 = q_minus ** 180 - q_plus ** 180
    (me_hmt, me_ext) = (0.5109989224880661, 0.51099895)
    with CSV.open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    if not len(rows) == 10:
        raise AssertionError('comprobación ejecutable fallida')
    err_hmt = {f'E{i}': [] for i in range(5)}
    err_ext = {f'E{i}': [] for i in range(5)}
    nu180 = []
    for row in rows:
        (nA, sC) = (int(row['nA']), int(row['sC']))
        (k, n120, n270, n180) = map(int, (row['k_Delta4'], row['nu120'], row['nu270_corr'], row['nu180_audit']))
        exps = [nA * A_rad + sC * C_rad / 6]
        exps.append(exps[-1] + k * D4)
        exps.append(exps[-1] + n120 * s120)
        exps.append(exps[-1] + n270 * z270)
        exps.append(exps[-1] + n180 * s180)
        ref = float(row['m_ref_calibration_MeV'])
        for (i, expv) in enumerate(exps):
            (mh, mx) = (me_hmt * math.exp(expv), me_ext * math.exp(expv))
            close(mh, float(row[f'm{i}_HMTscale_MeV']))
            close(mx, float(row[f'm{i}_EXTscale_MeV']))
            err_hmt[f'E{i}'].append(mh / ref - 1)
            err_ext[f'E{i}'].append(mx / ref - 1)
        inferred = round(math.log(ref / (me_hmt * math.exp(exps[3]))) / s180)
        if not inferred == n180:
            raise AssertionError('comprobación ejecutable fallida')
        nu180.append(n180)
    expected_hmt = [0.002224237203948622, 2.762046114809764e-05, 4.777221368999134e-06, 4.795312133659499e-07, 2.2292793901731056e-08]
    expected_ext = [0.002224232149142574, 2.761076737614547e-05, 4.765524718040763e-06, 4.7557629950193356e-07, 6.514460073013333e-08]
    for i in range(5):
        close(rms(err_hmt[f'E{i}']), expected_hmt[i], 3e-10, 2e-13)
        close(rms(err_ext[f'E{i}']), expected_ext[i], 3e-10, 2e-13)
    if not nu180 == [2, 7, -7, -1, -4, 5, -4, -5, 6, 9]:
        raise AssertionError('comprobación ejecutable fallida')
    print(json.dumps({'status': 'PASS', 'rows': len(rows), 'nu180': nu180, 'rms_hmt': {key: rms(value) for (key, value) in err_hmt.items()}, 'rms_ext': {key: rms(value) for (key, value) in err_ext.items()}, 'E4_typing': 'inverse_residual_quantization'}, sort_keys=True, indent=2))
if __name__ == '__main__':
    main()
