import QuarterTurn

/-! The manuscript's normalization W = twelveEmbed / sqrt(6). Products are
explicit Euclidean coordinate products, not the product-type sup norm. -/

noncomputable section

namespace HMT.III.OrientedMoment

theorem quarter_even_iterate (n : ℕ) :
    ((quarter : Plane → Plane)^[2 * n]) (1, 0) = ((-1 : ℝ) ^ n, 0) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [show 2 * (n + 1) = 2 + 2 * n by omega, Function.iterate_add_apply, ih]
    simp [Function.iterate_succ_apply, pow_succ]

theorem quarter_odd_iterate (n : ℕ) :
    ((quarter : Plane → Plane)^[2 * n + 1]) (1, 0) = (0, (-1 : ℝ) ^ n) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [show 2 * (n + 1) + 1 = 2 + (2 * n + 1) by omega,
      Function.iterate_add_apply, ih]
    simp [Function.iterate_succ_apply, pow_succ]

theorem quarter_odd_character (n : ℕ) :
    (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 = (-1 : ℝ) ^ n := by
  rw [quarter_odd_iterate]

theorem twelveEmbed_inner (x y : Plane) :
    (∑ j : Fin 12, twelveEmbed x j * twelveEmbed y j) =
      6 * (x.1 * y.1 + x.2 * y.2) := by
  norm_num [twelveEmbed, Fin.sum_univ_succ]
  ring

def normalizedEmbed (x : Plane) (j : Fin 12) : ℝ := twelveEmbed x j / Real.sqrt 6

theorem normalizedEmbed_inner (x y : Plane) :
    (∑ j : Fin 12, normalizedEmbed x j * normalizedEmbed y j) =
      x.1 * y.1 + x.2 * y.2 := by
  simp_rw [normalizedEmbed, div_mul_div_comm]
  rw [← Finset.sum_div, twelveEmbed_inner]
  rw [← pow_two, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 6)]
  ring

theorem normalized_cycle_intertwines (x : Plane) :
    cycle12 (normalizedEmbed x) = normalizedEmbed (quarter x) := by
  funext j
  exact congrArg (fun a : ℝ => a / Real.sqrt 6) (congrFun (cycle_intertwines x) j)

theorem normalized_oriented_coefficient (s : ℝ) :
    (∑ j : Fin 12, normalizedEmbed (0, 1) j * normalizedEmbed (resolvent s (1, 0)) j) =
      kernel s := by
  rw [normalizedEmbed_inner]
  simpa only [zero_mul, one_mul, zero_add] using oriented_coefficient s

theorem normalized_reverse_coefficient (s : ℝ) :
    (∑ j : Fin 12, normalizedEmbed (0, 1) j * normalizedEmbed (resolvent (-s) (1, 0)) j) =
      -kernel s := by
  rw [normalizedEmbed_inner]
  simpa only [zero_mul, one_mul, zero_add] using reversed_coefficient s

#print axioms twelveEmbed_inner
#print axioms quarter_even_iterate
#print axioms quarter_odd_character
#print axioms normalizedEmbed_inner
#print axioms normalized_cycle_intertwines
#print axioms normalized_oriented_coefficient
#print axioms normalized_reverse_coefficient

end HMT.III.OrientedMoment
