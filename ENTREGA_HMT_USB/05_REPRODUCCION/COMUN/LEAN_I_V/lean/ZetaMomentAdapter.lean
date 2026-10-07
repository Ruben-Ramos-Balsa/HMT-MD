import BosonicMoment
import Mathlib.NumberTheory.LSeries.RiemannZeta

noncomputable section
open Set MeasureTheory Real

namespace HMT.V.BosonicMoments

theorem riemannZeta_real_eq_series {s : ℝ} (hs : 1 < s) :
    riemannZeta (s : ℂ) = (zetaSeries s : ℂ) := by
  rw [zeta_eq_tsum_one_div_nat_add_one_cpow (by simpa using hs), zetaSeries]
  push_cast
  apply tsum_congr
  intro n
  have hp : 0 ≤ (n + 1 : ℝ) := by positivity
  have hc : (n : ℂ) + 1 = ((n + 1 : ℝ) : ℂ) := by push_cast; rfl
  rw [hc, ← Complex.ofReal_cpow hp]
  have he : (1 / (n + 1 : ℝ)) ^ s = 1 / (n + 1 : ℝ) ^ s := by
    simpa only [one_div] using Real.inv_rpow hp s
  rw [he]
  push_cast
  rfl

theorem bosonic_moment_zeta {s : ℝ} (hs : 1 < s) :
    (∫ x in Ioi (0 : ℝ), x ^ (s - 1) * occupation x) =
      Real.Gamma s * (riemannZeta (s : ℂ)).re := by
  rw [riemannZeta_real_eq_series hs, Complex.ofReal_re, bosonic_moment hs]

#print axioms riemannZeta_real_eq_series
#print axioms bosonic_moment_zeta

end HMT.V.BosonicMoments
