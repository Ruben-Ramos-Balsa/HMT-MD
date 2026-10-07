import Mathlib

/-!
# Explicit envelopes for the three thermal observables

Source: the complete `71_limite_termodinamico.tex` in the sealed
`SNAPSHOT_III_V_X_EXTENSION_20260916_01`, especially `v:eq:envolventes-termicas`.
This module proves the local estimates from the literal real functions.
It does not claim the periodic Riemann-sum limit from these estimates alone.
The positive parameters are posterior readings, not generator inputs.
-/

noncomputable section

namespace HMT.V.ThermodynamicLimit

open Set

def FN (a r : ℝ) : ℝ := 1 / (Real.exp (a * r) - 1)

def FE (a b r : ℝ) : ℝ := b * r / (Real.exp (a * r) - 1)

def FZ (a r : ℝ) : ℝ := -Real.log (1 - Real.exp (-a * r))

theorem exp_denominator_pos {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    0 < Real.exp (a * r) - 1 := by
  have := Real.one_lt_exp_iff.mpr (mul_pos ha hr)
  linarith

theorem decay_denominator_pos {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    0 < 1 - Real.exp (-a * r) := by
  have := Real.exp_lt_one_iff.mpr (mul_neg_of_neg_of_pos (neg_neg_of_pos ha) hr)
  linarith

theorem FN_pos {a r : ℝ} (ha : 0 < a) (hr : 0 < r) : 0 < FN a r :=
  div_pos (by norm_num) (exp_denominator_pos ha hr)

theorem FE_pos {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) : 0 < FE a b r :=
  div_pos (mul_pos hb hr) (exp_denominator_pos ha hr)

theorem FZ_pos {a r : ℝ} (ha : 0 < a) (hr : 0 < r) : 0 < FZ a r := by
  apply neg_pos.mpr
  exact Real.log_neg (decay_denominator_pos ha hr) (by linarith [Real.exp_pos (-a * r)])

theorem FN_continuousOn {a : ℝ} (ha : 0 < a) : ContinuousOn (FN a) (Ioi 0) := by
  apply continuousOn_const.div
    ((Real.continuous_exp.comp (continuous_const.mul continuous_id)).sub continuous_const).continuousOn
  intro r hr
  exact ne_of_gt (exp_denominator_pos ha hr)

theorem FE_continuousOn {a b : ℝ} (ha : 0 < a) : ContinuousOn (FE a b) (Ioi 0) := by
  apply (continuous_const.mul continuous_id).continuousOn.div
    ((Real.continuous_exp.comp (continuous_const.mul continuous_id)).sub continuous_const).continuousOn
  intro r hr
  exact ne_of_gt (exp_denominator_pos ha hr)

theorem FZ_continuousOn {a : ℝ} (ha : 0 < a) : ContinuousOn (FZ a) (Ioi 0) := by
  apply ContinuousOn.neg
  apply ContinuousOn.log
    (continuous_const.sub (Real.continuous_exp.comp (continuous_const.mul continuous_id))).continuousOn
  intro r hr
  exact ne_of_gt (decay_denominator_pos ha hr)

theorem FE_eq_FN (a b r : ℝ) : FE a b r = b * r * FN a r := by
  unfold FE FN
  ring

/-- The reciprocal exponential is proved, not assumed as an occupation field. -/
theorem FN_eq_decay {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    FN a r = Real.exp (-a * r) / (1 - Real.exp (-a * r)) := by
  have he : Real.exp (a * r) * Real.exp (-a * r) = 1 := by
    rw [← Real.exp_add]
    convert Real.exp_zero using 1
    ring
  unfold FN
  apply (div_eq_div_iff (ne_of_gt (exp_denominator_pos ha hr))
    (ne_of_gt (decay_denominator_pos ha hr))).mpr
  nlinarith

/-- The source's logarithmic identity, on the full positive ray. -/
theorem FZ_eq_log_one_add_FN {a r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    FZ a r = Real.log (1 + FN a r) := by
  rw [FN_eq_decay ha hr]
  have he : 1 + Real.exp (-a * r) / (1 - Real.exp (-a * r)) =
      (1 - Real.exp (-a * r))⁻¹ := by
    calc
      _ = (1 - Real.exp (-a * r)) / (1 - Real.exp (-a * r)) +
          Real.exp (-a * r) / (1 - Real.exp (-a * r)) := by
        rw [div_self (ne_of_gt (decay_denominator_pos ha hr))]
      _ = 1 / (1 - Real.exp (-a * r)) := by
        rw [← add_div]
        congr 1
        ring
      _ = _ := one_div _
  rw [he, Real.log_inv]
  rfl

theorem FZ_le_FN {a r : ℝ} (ha : 0 < a) (hr : 0 < r) : FZ a r ≤ FN a r := by
  rw [FZ_eq_log_one_add_FN ha hr]
  have := Real.log_le_sub_one_of_pos (show 0 < 1 + FN a r by linarith [FN_pos ha hr])
  linarith

theorem FN_strictAntiOn {a : ℝ} (ha : 0 < a) : StrictAntiOn (FN a) (Ioi 0) := by
  intro x hx y _ hxy
  apply one_div_lt_one_div_of_lt (exp_denominator_pos ha hx)
  have := Real.exp_lt_exp.mpr (mul_lt_mul_of_pos_left hxy ha)
  linarith

theorem FZ_strictAntiOn {a : ℝ} (ha : 0 < a) : StrictAntiOn (FZ a) (Ioi 0) := by
  intro x hx y hy hxy
  rw [FZ_eq_log_one_add_FN ha hy, FZ_eq_log_one_add_FN ha hx]
  apply Real.log_lt_log (by linarith [FN_pos ha hy])
  linarith [FN_strictAntiOn ha hx hy hxy]

theorem FE_hasDerivAt {a b r : ℝ} (ha : 0 < a) (hr : 0 < r) :
    HasDerivAt (FE a b)
      ((b * (Real.exp (a * r) - 1) - b * r * (Real.exp (a * r) * a)) /
        (Real.exp (a * r) - 1) ^ 2) r := by
  simpa [FE] using ((hasDerivAt_id r).const_mul b).div
    (((hasDerivAt_id r).const_mul a).exp.sub_const 1)
    (ne_of_gt (exp_denominator_pos ha hr))

theorem FE_deriv_neg {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) :
    deriv (FE a b) r < 0 := by
  rw [(FE_hasDerivAt ha hr).deriv]
  have hlin : -a * r + 1 < Real.exp (-a * r) :=
    Real.add_one_lt_exp (ne_of_lt (mul_neg_of_neg_of_pos (neg_neg_of_pos ha) hr))
  have he : Real.exp (a * r) * Real.exp (-a * r) = 1 := by
    rw [← Real.exp_add, show a * r + -a * r = 0 by ring, Real.exp_zero]
  have hprod : Real.exp (a * r) * (1 - a * r) < 1 := by
    have := mul_lt_mul_of_pos_left hlin (Real.exp_pos (a * r))
    rw [he] at this
    nlinarith
  apply div_neg_of_neg_of_pos _ (pow_pos (exp_denominator_pos ha hr) 2)
  rw [show b * (Real.exp (a * r) - 1) - b * r * (Real.exp (a * r) * a) =
    b * (Real.exp (a * r) * (1 - a * r) - 1) by ring]
  exact mul_neg_of_pos_of_neg hb (sub_neg.mpr hprod)

theorem FE_strictAntiOn {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    StrictAntiOn (FE a b) (Ioi 0) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioi _) (FE_continuousOn ha)
  intro r hr
  exact FE_deriv_neg ha hb (by simpa only [interior_Ioi, mem_Ioi] using hr)

theorem FN_le_inv_ar {a r : ℝ} (ha : 0 < a) (hr : 0 < r) : FN a r ≤ 1 / (a * r) := by
  unfold FN
  apply div_le_div₀ (by norm_num) le_rfl (mul_pos ha hr)
  linarith [Real.add_one_le_exp (a * r)]

theorem FE_le_b_div_a {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) :
    FE a b r ≤ b / a := by
  rw [FE_eq_FN]
  calc
    b * r * FN a r ≤ b * r * (1 / (a * r)) :=
      mul_le_mul_of_nonneg_left (FN_le_inv_ar ha hr) (mul_pos hb hr).le
    _ = b / a := by field_simp; ring

def originConstant (a b : ℝ) : ℝ := (1 + b) / a

def decayRate (a : ℝ) : ℝ := a / 2

def tailConstant (a b : ℝ) : ℝ := (1 + 2 * b / a) / (1 - Real.exp (-a))

theorem originConstant_pos {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    0 < originConstant a b := by unfold originConstant; positivity

theorem decayRate_pos {a : ℝ} (ha : 0 < a) : 0 < decayRate a := div_pos ha (by norm_num)

theorem tailConstant_pos {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    0 < tailConstant a b := by
  apply div_pos (by positivity)
  simpa using decay_denominator_pos ha (show (0 : ℝ) < 1 by norm_num)

theorem FN_origin {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) :
    FN a r ≤ originConstant a b / r := by
  calc
    FN a r ≤ 1 / (a * r) := FN_le_inv_ar ha hr
    _ ≤ (1 + b) / (a * r) :=
      div_le_div_of_nonneg_right (by linarith) (mul_pos ha hr).le
    _ = originConstant a b / r := by unfold originConstant; ring

theorem FE_origin {a b r : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hr : 0 < r) (hr1 : r ≤ 1) : FE a b r ≤ originConstant a b / r := by
  have hba : 0 < b / a := div_pos hb ha
  have hc : b / a ≤ originConstant a b := by
    unfold originConstant
    apply div_le_div_of_nonneg_right (by linarith) ha.le
  calc
    FE a b r ≤ b / a := FE_le_b_div_a ha hb hr
    _ ≤ (b / a) / r := by
      apply (le_div_iff₀ hr).mpr
      nlinarith
    _ ≤ originConstant a b / r := div_le_div_of_nonneg_right hc hr.le

theorem FZ_origin {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r) :
    FZ a r ≤ originConstant a b / r := (FZ_le_FN ha hr).trans (FN_origin ha hb hr)

theorem FN_tail_fast {a r : ℝ} (ha : 0 < a) (hr : 1 ≤ r) :
    FN a r ≤ (1 / (1 - Real.exp (-a))) * Real.exp (-a * r) := by
  have hrpos : 0 < r := lt_of_lt_of_le (by norm_num) hr
  rw [FN_eq_decay ha hrpos]
  have hden : 0 < 1 - Real.exp (-a) := by
    simpa using decay_denominator_pos ha (show (0 : ℝ) < 1 by norm_num)
  have hexp : Real.exp (-a * r) ≤ Real.exp (-a) := by
    apply Real.exp_le_exp.mpr
    nlinarith
  calc
    Real.exp (-a * r) / (1 - Real.exp (-a * r)) ≤
        Real.exp (-a * r) / (1 - Real.exp (-a)) :=
      div_le_div₀ (Real.exp_pos _).le le_rfl hden (by linarith)
    _ = (1 / (1 - Real.exp (-a))) * Real.exp (-a * r) := by ring

/-- A fully explicit absorption estimate, with half of the original decay rate. -/
theorem absorb_linear_factor {a r : ℝ} (ha : 0 < a) :
    r * Real.exp (-a * r) ≤ (2 / a) * Real.exp (-(a / 2) * r) := by
  have ht : (a / 2) * r ≤ Real.exp ((a / 2) * r) := by
    linarith [Real.add_one_le_exp ((a / 2) * r)]
  have hr : r ≤ (2 / a) * Real.exp ((a / 2) * r) := by
    calc
      r ≤ (2 * Real.exp ((a / 2) * r)) / a := (le_div_iff₀ ha).mpr (by nlinarith)
      _ = _ := by ring
  calc
    r * Real.exp (-a * r) ≤ ((2 / a) * Real.exp ((a / 2) * r)) * Real.exp (-a * r) :=
      mul_le_mul_of_nonneg_right hr (Real.exp_pos _).le
    _ = (2 / a) * Real.exp (-(a / 2) * r) := by
      rw [mul_assoc, ← Real.exp_add]
      congr 2
      ring

theorem FE_tail_fast {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 1 ≤ r) :
    FE a b r ≤ (2 * b / a) / (1 - Real.exp (-a)) * Real.exp (-(a / 2) * r) := by
  have hrpos : 0 < r := lt_of_lt_of_le (by norm_num) hr
  have hden : 0 < 1 - Real.exp (-a) := by
    simpa using decay_denominator_pos ha (show (0 : ℝ) < 1 by norm_num)
  rw [FE_eq_FN]
  calc
    b * r * FN a r ≤ b * r * ((1 / (1 - Real.exp (-a))) * Real.exp (-a * r)) :=
      mul_le_mul_of_nonneg_left (FN_tail_fast ha hr) (mul_pos hb hrpos).le
    _ = (b / (1 - Real.exp (-a))) * (r * Real.exp (-a * r)) := by ring
    _ ≤ (b / (1 - Real.exp (-a))) * ((2 / a) * Real.exp (-(a / 2) * r)) :=
      mul_le_mul_of_nonneg_left (absorb_linear_factor ha) (div_pos hb hden).le
    _ = _ := by ring

theorem FN_tail {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 1 ≤ r) :
    FN a r ≤ tailConstant a b * Real.exp (-decayRate a * r) := by
  have hden : 0 < 1 - Real.exp (-a) := by
    simpa using decay_denominator_pos ha (show (0 : ℝ) < 1 by norm_num)
  have hcoeff : 1 / (1 - Real.exp (-a)) ≤ tailConstant a b := by
    unfold tailConstant
    apply div_le_div_of_nonneg_right _ hden.le
    have := div_pos (mul_pos (by norm_num : (0 : ℝ) < 2) hb) ha
    linarith
  have hexp : Real.exp (-a * r) ≤ Real.exp (-decayRate a * r) := by
    apply Real.exp_le_exp.mpr
    unfold decayRate
    nlinarith
  exact (FN_tail_fast ha hr).trans (mul_le_mul hcoeff hexp (Real.exp_pos _).le
    (tailConstant_pos ha hb).le)

theorem FE_tail {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 1 ≤ r) :
    FE a b r ≤ tailConstant a b * Real.exp (-decayRate a * r) := by
  have hden : 0 < 1 - Real.exp (-a) := by
    simpa using decay_denominator_pos ha (show (0 : ℝ) < 1 by norm_num)
  have hcoeff : (2 * b / a) / (1 - Real.exp (-a)) ≤ tailConstant a b := by
    unfold tailConstant
    exact div_le_div_of_nonneg_right (by linarith) hden.le
  exact (FE_tail_fast ha hb hr).trans (mul_le_mul_of_nonneg_right hcoeff (Real.exp_pos _).le)

theorem FZ_tail {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 1 ≤ r) :
    FZ a r ≤ tailConstant a b * Real.exp (-decayRate a * r) :=
  (FZ_le_FN ha (lt_of_lt_of_le (by norm_num) hr)).trans (FN_tail ha hb hr)

/-- Exactly the three source observables; no envelope fields are stored in this type. -/
inductive ThermalKind where
  | number
  | energy
  | partition

def thermalObservable (a b : ℝ) : ThermalKind → ℝ → ℝ
  | .number => FN a
  | .energy => FE a b
  | .partition => FZ a

theorem thermal_continuousOn {a b : ℝ} (ha : 0 < a) (kind : ThermalKind) :
    ContinuousOn (thermalObservable a b kind) (Ioi 0) := by
  cases kind
  · exact FN_continuousOn ha
  · exact FE_continuousOn ha
  · exact FZ_continuousOn ha

theorem thermal_pos {a b r : ℝ} (ha : 0 < a) (hb : 0 < b) (hr : 0 < r)
    (kind : ThermalKind) : 0 < thermalObservable a b kind r := by
  cases kind
  · exact FN_pos ha hr
  · exact FE_pos ha hb hr
  · exact FZ_pos ha hr

theorem thermal_strictAntiOn {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (kind : ThermalKind) :
    StrictAntiOn (thermalObservable a b kind) (Ioi 0) := by
  cases kind
  · exact FN_strictAntiOn ha
  · exact FE_strictAntiOn ha hb
  · exact FZ_strictAntiOn ha

theorem thermal_antitoneOn {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (kind : ThermalKind) :
    AntitoneOn (thermalObservable a b kind) (Ioi 0) := (thermal_strictAntiOn ha hb kind).antitoneOn

theorem thermal_origin {a b r : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hr : 0 < r) (hr1 : r ≤ 1) (kind : ThermalKind) :
    thermalObservable a b kind r ≤ originConstant a b / r := by
  cases kind
  · exact FN_origin ha hb hr
  · exact FE_origin ha hb hr hr1
  · exact FZ_origin ha hb hr

theorem thermal_tail {a b r : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hr : 1 ≤ r) (kind : ThermalKind) :
    thermalObservable a b kind r ≤ tailConstant a b * Real.exp (-decayRate a * r) := by
  cases kind
  · exact FN_tail ha hb hr
  · exact FE_tail ha hb hr
  · exact FZ_tail ha hb hr

/-- Explicit common constants, uniform in the radius and independent of any lattice mesh. -/
theorem thermal_envelopes {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    0 < originConstant a b ∧ 0 < tailConstant a b ∧ 0 < decayRate a ∧
    ∀ kind : ThermalKind,
      ContinuousOn (thermalObservable a b kind) (Ioi 0) ∧
      (∀ r : ℝ, 0 < r → 0 < thermalObservable a b kind r) ∧
      (∀ r : ℝ, 0 < r → r ≤ 1 → thermalObservable a b kind r ≤ originConstant a b / r) ∧
      (∀ r : ℝ, 1 ≤ r → thermalObservable a b kind r ≤
        tailConstant a b * Real.exp (-decayRate a * r)) := by
  refine ⟨originConstant_pos ha hb, tailConstant_pos ha hb, decayRate_pos ha, ?_⟩
  intro kind
  exact ⟨thermal_continuousOn ha kind, fun _ hr => thermal_pos ha hb hr kind,
    fun _ hr hr1 => thermal_origin ha hb hr hr1 kind, fun _ hr => thermal_tail ha hb hr kind⟩

#print axioms FN_continuousOn
#print axioms FE_continuousOn
#print axioms FZ_continuousOn
#print axioms FZ_eq_log_one_add_FN
#print axioms FZ_le_FN
#print axioms FE_deriv_neg
#print axioms thermal_strictAntiOn
#print axioms thermal_antitoneOn
#print axioms FN_le_inv_ar
#print axioms absorb_linear_factor
#print axioms thermal_origin
#print axioms thermal_tail
#print axioms thermal_envelopes

end HMT.V.ThermodynamicLimit
