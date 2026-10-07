"""Resuelve únicamente la discrepancia entre dos controles de Euler–Kronecker.

No vuelve a ejecutar los restantes cálculos ni escribe en el corpus.
La tabla residual procede de c33; el cociente finito procede de c34.
Es una comprobación numérica posterior, no una prueba intervalar.
"""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
VENDOR = (AUDIT.parent / "REVISION_EDITORIAL_HMT_MD_20260905/00_BASE_SELLADA/"
          "01_FUENTE_SUCESORA/pruebas/python")
sys.path.insert(0, str(VENDOR))
import mpmath as mp

SPECTRAL = AUDIT / "VALORES_ESPECTRALES_RECALCULADOS.json"
REPLAY = AUDIT / "RECOMPROBACION_CONSTANTES/REPLAY_RESULTADOS.json"


def evaluate(precision):
    with mp.workdps(precision):
        table = ((1, 1), (5, -1), (7, -1), (11, 1))
        l1 = mp.log(2 + mp.sqrt(3)) / mp.sqrt(3)
        # L(s)=12^-s sum chi(r) zeta(s,r/12). Los polos cancelan.
        # gamma_0(a)=-psi(a); d/ds de la parte regular en 1 = -gamma_1(a).
        weighted_g1 = mp.fsum(sign * mp.stieltjes(1, mp.mpf(r) / 12)
                             for r, sign in table)
        lprime = -mp.log(12) * l1 - weighted_g1 / 12
        value = mp.euler + lprime / l1
        return {"precision": precision, "L_prime_1": mp.nstr(lprime, precision - 10),
                "Euler_Kronecker_Qsqrt3": mp.nstr(value, precision - 10)}


def main():
    spectral = json.loads(SPECTRAL.read_text())
    replay = json.loads(REPLAY.read_text())
    old = next(row["result"]["Euler_Kronecker_sqrt3"]
               for row in replay["records"]
               if row["id"] == "CATALAN_BENDERSKY_ODD_ZETA_EK")
    low, high = evaluate(60), evaluate(90)
    with mp.workdps(90):
        value = mp.mpf(high["Euler_Kronecker_Qsqrt3"])
        stability = abs(value - mp.mpf(low["Euler_Kronecker_Qsqrt3"]))
        em_error = abs(value - mp.mpf(spectral["valores"]["Euler_Kronecker_Q_sqrt3"]))
        old_error = abs(value - mp.mpf(old))
        assert stability < mp.mpf("1e-48")
        assert em_error < mp.mpf("1e-40")
        assert old_error > mp.mpf("1e-11")
        result = {
            "status": "COMPROBACION_NUMERICA_RECONCILIADA",
            "method": "coeficiente de Laurent, sin diferenciacion numerica en el polo",
            "source_formula": "c34_euler_kronecker_primos.tex:12; c33_catalan_apery_euler.tex:178",
            "evaluations": [low, high],
            "difference_resolutions": mp.nstr(stability, 20),
            "difference_Euler_Maclaurin": mp.nstr(em_error, 20),
            "old_replay_value": old,
            "old_replay_discrepancy": mp.nstr(old_error, 20),
            "disposition": "Usar el valor EM concordante; no propagar el escalar discrepante del replay.",
            "scope": "comprobacion de evaluadores posteriores; no cota rigurosa de redondeo ni demostracion global",
            "evidence_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (SPECTRAL, REPLAY, Path(__file__))},
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "--write-report" in sys.argv:
        (HERE / "CONTROL_EULER_KRONECKER.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
