"""Verificador del núcleo numérico de Mecánica Dimensional.

No escribe ficheros y no usa paquetes externos. Imprime un JSON determinista.
"""
from __future__ import annotations
import json
import math
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def close(a: float, b: float, atol: float=1e-14, rtol: float=1e-12) -> None:
    if not math.isclose(a, b, abs_tol=atol, rel_tol=rtol):
        raise AssertionError(f'{a!r} != {b!r}')

def dr9(n: int) -> int:
    r = n % 9
    return 9 if r == 0 else r

def app_census() -> dict[str, int]:
    sums = {'sum_add': 0, 'sum_mul': 0, 'R_add': 0, 'R_mul': 0, 'Q_add': 0, 'Q_mul': 0}
    for i in range(1, 10):
        for j in range(1, 10):
            (ra, rm) = (dr9(i + j), dr9(i * j))
            (qa, qm) = ((i + j - ra) // 9, (i * j - rm) // 9)
            sums['sum_add'] += i + j
            sums['sum_mul'] += i * j
            sums['R_add'] += ra
            sums['R_mul'] += rm
            sums['Q_add'] += qa
            sums['Q_mul'] += qm
    if not sums == {'sum_add': 810, 'sum_mul': 2025, 'R_add': 405, 'R_mul': 459, 'Q_add': 45, 'Q_mul': 174}:
        raise AssertionError('comprobación ejecutable fallida')
    if not 2025 - 810 == 459 - 405 + 9 * (174 - 45):
        raise AssertionError('comprobación ejecutable fallida')
    return sums

def coefficient(fermion: bool) -> int:
    energies = (0, 3, 6, 9)
    degeneracies = (1, 6, 12, 8)
    dp: dict[tuple[int, int], int] = {(0, 0): 1}
    for (eps, g) in zip(energies, degeneracies):
        nxt: dict[tuple[int, int], int] = defaultdict(int)
        max_r = g if fermion else 12
        for ((n, e), count) in dp.items():
            for r in range(max_r + 1):
                if n + r > 12 or e + r * eps > 66:
                    break
                ways = math.comb(g, r) if fermion else math.comb(g + r - 1, r)
                nxt[n + r, e + r * eps] += count * ways
        dp = nxt
    return dp.get((12, 66), 0)

def microcanonical_occupancy(fermion: bool) -> tuple[int, list[float]]:
    """Enumera exactamente las ocupaciones de los cuatro niveles publicados."""
    energies = (0, 3, 6, 9)
    degeneracies = (1, 6, 12, 8)
    total = 0
    weighted = [0, 0, 0, 0]

    def visit(level: int, remaining_n: int, remaining_e: int, weight: int, occupation: list[int]) -> None:
        nonlocal total
        if level == len(energies):
            if remaining_n == 0 and remaining_e == 0:
                total += weight
                for (index, value) in enumerate(occupation):
                    weighted[index] += weight * value
            return
        (eps, degeneracy) = (energies[level], degeneracies[level])
        upper = min(remaining_n, degeneracy if fermion else remaining_n)
        for count in range(upper + 1):
            energy = count * eps
            if energy > remaining_e:
                break
            multiplicity = math.comb(degeneracy, count) if fermion else math.comb(degeneracy + count - 1, count)
            visit(level + 1, remaining_n - count, remaining_e - energy, weight * multiplicity, occupation + [count])
    visit(0, 12, 66, 1, [])
    if not total > 0:
        raise AssertionError('comprobación ejecutable fallida')
    return (total, [value / total for value in weighted])

def equilibrium_occupancy(fermion: bool) -> tuple[float, float, list[float]]:
    """Resuelve las dos restricciones por Newton amortiguado, sin dependencias."""
    energies = (0.0, 3.0, 6.0, 9.0)
    degeneracies = (1.0, 6.0, 12.0, 8.0)
    (beta, mu) = (0.15, 5.5) if fermion else (0.1, -0.5)

    def evaluate(b: float, chemical: float) -> tuple[list[float], tuple[float, float]]:
        occupations: list[float] = []
        for (eps, degeneracy) in zip(energies, degeneracies):
            exponent = math.exp(b * (eps - chemical))
            denominator = exponent + 1.0 if fermion else exponent - 1.0
            if denominator <= 0.0:
                raise ValueError('estado bosónico fuera del dominio')
            occupations.append(degeneracy / denominator)
        residual = (sum(occupations) - 12.0, sum((eps * value for (eps, value) in zip(energies, occupations))) - 66.0)
        return (occupations, residual)
    for _ in range(100):
        (occupations, residual) = evaluate(beta, mu)
        if math.hypot(*residual) < 1e-13:
            return (beta, mu, occupations)
        derivatives = []
        for (eps, degeneracy, value) in zip(energies, degeneracies, occupations):
            per_mode = value / degeneracy
            response = per_mode * (1.0 - per_mode) if fermion else per_mode * (1.0 + per_mode)
            derivatives.append((-degeneracy * (eps - mu) * response, degeneracy * beta * response))
        jacobian = ((sum((pair[0] for pair in derivatives)), sum((pair[1] for pair in derivatives))), (sum((eps * pair[0] for (eps, pair) in zip(energies, derivatives))), sum((eps * pair[1] for (eps, pair) in zip(energies, derivatives)))))
        determinant = jacobian[0][0] * jacobian[1][1] - jacobian[0][1] * jacobian[1][0]
        if not abs(determinant) > 1e-18:
            raise AssertionError('comprobación ejecutable fallida')
        step_beta = (-residual[0] * jacobian[1][1] + residual[1] * jacobian[0][1]) / determinant
        step_mu = (-jacobian[0][0] * residual[1] + jacobian[1][0] * residual[0]) / determinant
        norm = math.hypot(*residual)
        damping = 1.0
        accepted = False
        for _ in range(40):
            candidate_beta = beta + damping * step_beta
            candidate_mu = mu + damping * step_mu
            if candidate_beta <= 0.0 or (not fermion and candidate_mu >= 0.0):
                damping *= 0.5
                continue
            try:
                (_, candidate_residual) = evaluate(candidate_beta, candidate_mu)
            except (ValueError, OverflowError):
                damping *= 0.5
                continue
            if math.hypot(*candidate_residual) < norm:
                (beta, mu) = (candidate_beta, candidate_mu)
                accepted = True
                break
            damping *= 0.5
        if not accepted:
            raise AssertionError('Newton amortiguado no converge')
    raise AssertionError('Newton amortiguado excede el número de iteraciones')

def main() -> None:
    alpha = 1.0 / 137.035999084
    A = 1000.0 * alpha
    C = 2.123738338968646
    hbar_hmt = C / 2.0 - alpha
    delta4 = (math.pi - math.e * math.log(math.pi)) / 270.0 * (1.0 + math.pi / 729.0)
    (x, y) = (math.pi * A / 180.0, math.pi * C / 180.0)
    (q_plus, q_minus) = (math.exp(-x - y), math.exp(-x + y))
    close(alpha, 0.007297352569283801, 2e-18, 2e-15)
    close(hbar_hmt, 1.054571816915039, 2e-16, 2e-15)
    close(delta4, 0.00011119642269214005, 2e-19, 2e-14)
    close(q_plus, 0.8483779425764044, 2e-16, 2e-15)
    close(q_minus, 0.9136601511505573, 2e-16, 2e-15)
    xr = -0.5 * math.log(q_plus * q_minus)
    yr = 0.5 * math.log(q_minus / q_plus)
    close(xr, x)
    close(yr, y)
    c = lambda n: q_minus ** n + q_plus ** n
    s = lambda n: q_minus ** n - q_plus ** n
    for (m, n) in ((1, 1), (90, 120), (180, 240)):
        close(c(m + n), (c(m) * c(n) + s(m) * s(n)) / 2.0, 1e-15)
        close(s(m + n), (s(m) * c(n) + c(m) * s(n)) / 2.0, 1e-15)
    for n in range(0, 419):
        close(s(n + 2), c(1) * s(n + 1) - q_minus * q_plus * s(n), 2e-15, 2e-12)
    towers = {n: s(n) for n in (90, 120, 180, 210, 240, 270, 360, 420)}
    zeta270_corr = 135.0 * delta4 ** 2
    if not abs(zeta270_corr - towers[270]) > 1e-07:
        raise AssertionError('comprobación ejecutable fallida')
    close(zeta270_corr, 1.66922699663643e-06, 2e-19, 2e-13)
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    electron = math.sqrt(3.0) / 4.0 * (math.exp(phi / math.pi ** 2) - 22.0 * alpha ** 3) * (1.0 + 15.0 * delta4)
    close(electron, 0.5109989224880661, 2e-15, 2e-14)
    z0_reference = 376.730313668
    z0_candidates = {p: 120.0 * math.pi * (1.0 - (2.0 * math.pi - p / 81.0) * delta4) for p in range(21)}
    z0_errors = {p: abs(value - z0_reference) / z0_reference for (p, value) in z0_candidates.items()}
    best_p = min(z0_errors, key=z0_errors.get)
    if not best_p == 5:
        raise AssertionError('comprobación ejecutable fallida')
    if not list(sorted(z0_errors, key=z0_errors.get))[:3] == [5, 4, 6]:
        raise AssertionError('comprobación ejecutable fallida')
    if not all((z0_candidates[p + 1] > z0_candidates[p] for p in range(20))):
        raise AssertionError('comprobación ejecutable fallida')
    if not (27 - best_p == 22 and 3 * best_p == 15):
        raise AssertionError('comprobación ejecutable fallida')
    S90 = lambda q: q ** 90 / (1.0 - q ** 270)
    S120 = lambda q: q ** 120 / (1.0 - q ** 360)
    (d90, d120) = (S90(q_minus) - S90(q_plus), S120(q_minus) - S120(q_plus))
    gamma = math.pi * A * C / 180.0 + 12.0 * d90 - d120
    close(gamma, 0.2740076726944593, 2e-15, 2e-14)
    solutions = [(a, b) for a in range(1, 100) for b in range(1, 100) if 4 * a - 3 * b == 45]
    if not solutions[:5] == [(12, 1), (15, 5), (18, 9), (21, 13), (24, 17)]:
        raise AssertionError('comprobación ejecutable fallida')
    (h, Delta) = (C / 6.0, 180.0 / math.pi * delta4)
    (th12, th23, th13, dcp) = (2 * A - 5 * h + 28 * Delta, 7 * h - 12.5 * Delta, A - 20 * h - 2 * Delta / 3, 9 * A)
    close(th12, 13.003313589509013, 2e-14)
    close(th23, 2.3980561573315993, 2e-14)
    close(th13, 0.21397738224350707, 2e-14)
    if not (3857 * dcp == 9 * (1528 * th12 + 3380 * th23 + 801 * th13) or math.isclose(3857 * dcp, 9 * (1528 * th12 + 3380 * th23 + 801 * th13), rel_tol=2e-15)):
        raise AssertionError('comprobación ejecutable fallida')
    (a12, a23, a13, delta) = map(math.radians, (th12, th23, th13, dcp))
    (c12, c23, c13) = (math.cos(a12), math.cos(a23), math.cos(a13))
    (ss12, ss23, ss13) = (math.sin(a12), math.sin(a23), math.sin(a13))
    J = c12 * c23 * c13 ** 2 * ss12 * ss23 * ss13 * math.sin(delta)
    close(J, 3.118972332663311e-05, 2e-18, 2e-13)
    delta_vac = math.log10(10.0 / 9.0)
    pos = [math.floor(n / delta_vac) for n in range(1, 3000)]
    gaps = {b - a for (a, b) in zip(pos, pos[1:])}
    if not gaps == {21, 22}:
        raise AssertionError('comprobación ejecutable fallida')
    short_indices = [i for (i, g) in enumerate((b - a for (a, b) in zip(pos, pos[1:]))) if g == 21]
    return_gaps = {b - a for (a, b) in zip(short_indices, short_indices[1:])}
    if not return_gaps == {6, 7}:
        raise AssertionError('comprobación ejecutable fallida')
    (fd_count, be_count) = (coefficient(True), coefficient(False))
    if not fd_count == 2104494:
        raise AssertionError('comprobación ejecutable fallida')
    if not be_count == 259436430:
        raise AssertionError('comprobación ejecutable fallida')
    (fd_total, fd_micro) = microcanonical_occupancy(True)
    (be_total, be_micro) = microcanonical_occupancy(False)
    if not (fd_total, be_total) == (fd_count, be_count):
        raise AssertionError('comprobación ejecutable fallida')
    (beta_fd, mu_fd, fd_equilibrium) = equilibrium_occupancy(True)
    (beta_be, mu_be, be_equilibrium) = equilibrium_occupancy(False)
    fd_l1 = sum((abs(a - b) for (a, b) in zip(fd_micro, fd_equilibrium)))
    be_l1 = sum((abs(a - b) for (a, b) in zip(be_micro, be_equilibrium)))
    close(fd_l1, 0.09897380039002812, 2e-14, 2e-13)
    close(be_l1, 0.9190625715582017, 2e-14, 2e-13)
    E = math.log((1 - q_plus ** 90) * (1 - q_minus ** 90)) - math.log((1 - q_plus ** 120) * (1 - q_minus ** 120))
    B = math.log((1 - q_minus ** 90) / (1 - q_plus ** 90)) - math.log((1 - q_minus ** 120) / (1 - q_plus ** 120))
    (Zhat, chat) = (math.exp(B), math.exp(-E))
    (muhat, epshat) = (math.exp(B + E), math.exp(-B + E))
    close(math.sqrt(muhat / epshat), Zhat)
    close(1.0 / math.sqrt(muhat * epshat), chat)
    amu = alpha / (2 * math.pi) + alpha * (phi - 1) / 1000 + alpha ** 2 / (1000 * 55)
    close(amu, 0.0011659207130080142, 3e-18, 3e-14)
    amu_reference = 0.001165920705
    amu_sigma = 1.48e-10
    amu_deviation = (amu - amu_reference) / amu_sigma
    close(amu_deviation, 0.05410820387602808, 1e-14, 1e-13)
    result = {'status': 'PASS', 'app': app_census(), 'q_plus': format(q_plus, '.17g'), 'q_minus': format(q_minus, '.17g'), 'electron': format(electron, '.17g'), 'z0_best_p': best_p, 'z0_at_best_p': format(z0_candidates[best_p], '.17g'), 'z0_relative_error': format(z0_errors[best_p], '.17g'), 'gamma_6to8': format(gamma, '.17g'), 'J': format(J, '.17g'), 'fd_count': fd_count, 'be_count': be_count, 'fd_beta_mu': [format(beta_fd, '.17g'), format(mu_fd, '.17g')], 'be_beta_mu': [format(beta_be, '.17g'), format(mu_be, '.17g')], 'fd_l1': format(fd_l1, '.17g'), 'be_l1': format(be_l1, '.17g'), 'vacancy_gaps': sorted(gaps), 'short_return_gaps': sorted(return_gaps), 'typed_270_distinct': True, 'a_mu_functional': format(amu, '.17g'), 'a_mu_run1_6_deviation_sigma': format(amu_deviation, '.17g')}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
if __name__ == '__main__':
    main()
