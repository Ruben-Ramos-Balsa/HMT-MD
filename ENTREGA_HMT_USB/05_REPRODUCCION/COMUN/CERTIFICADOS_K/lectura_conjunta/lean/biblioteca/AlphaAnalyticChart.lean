import AlphaCarryLimit
import Mathlib

/-!
# Correlated analytic chart of the already generated precoordinate

Source: article I, alpha_carta_analitica_completa.tex, with the corresponding
article IV alpha_lector_analitico_completo_rev08.tex.  The scalar cut begins
with the regional readers and supplied dodecaphase register.  The link
coefficient uses their precoordinate, before positional normalization.
Its root identity is a correlated representation by construction, not an
independent selection or derivation of that precoordinate.  Uniqueness of
the link is only within the declared q-geometric family.
-/

noncomputable section
open Filter Topology Finset

namespace AlphaAnalyticChart

def q : ℝ := 1 / 729
def radius : ℝ := 1 / 100
def ratioBound : ℝ := q * radius ^ 3
def lambdaBound : ℝ := 8711 / 1000000000

theorem q_pos : 0 < q := by norm_num [q]
theorem radius_pos : 0 < radius := by norm_num [radius]
theorem ratioBound_nonneg : 0 ≤ ratioBound := by norm_num [ratioBound, q, radius]
theorem ratioBound_lt_one : ratioBound < 1 := by norm_num [ratioBound, q, radius]

/-- Same inputs as the integer closure, without taking its output as input. -/
def precoordinate (register : RadixRecovery.K12) : ℝ :=
  (ClosureAnalytic.value - 3) + (PropagationLimit.value - 2) -
    (AlphaCarryLimit.autoscaleValue - 1) - AlphaCarryLimit.Periodic.periodicValue register

theorem precoordinate_eq_carry_value (register : RadixRecovery.K12) :
    precoordinate register = AlphaCarryLimit.value register := rfl

/-- The marked degree-nine jet. `p` and `delta` are prior reader coordinates. -/
def jet9 (p delta x : ℝ) : ℝ :=
  2*p*x - (7/4)*x^2 + x^3/(2*p) + x^4/20 - 2*x^5/21 - x^6/46 -
    x^7/120 + x^8/45 + 2*x^9/495 - delta

def link (E9 : ℝ → ℝ) (a : ℝ) : ℝ :=
  -(E9 a * (1 - q * a^3)) / a^10

def correction (mu x : ℝ) : ℝ := mu * x^10 / (1 - q*x^3)
def chart (E9 : ℝ → ℝ) (mu x : ℝ) : ℝ := E9 x + correction mu x
def complete (E9 : ℝ → ℝ) (a x : ℝ) : ℝ := chart E9 (link E9 a) x

def stateLink (register : RadixRecovery.K12) (delta : ℝ) : ℝ :=
  link (jet9 ClosureAnalytic.value delta) (precoordinate register)

theorem ratio_bounds {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    0 ≤ q*x^3 ∧ q*x^3 ≤ ratioBound := by
  have hq : 0 ≤ q := q_pos.le
  constructor
  · positivity
  · unfold ratioBound
    gcongr

theorem denominator_pos {x : ℝ} (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    0 < 1 - q*x^3 := by
  have h := (ratio_bounds hx0 hx1).2
  linarith [ratioBound_lt_one]

theorem link_unique (E9 : ℝ → ℝ) (a mu : ℝ) (ha : a ≠ 0)
    (hd : 1 - q*a^3 ≠ 0) : chart E9 mu a = 0 ↔ mu = link E9 a := by
  unfold chart correction link
  constructor
  · intro h
    apply (eq_div_iff (pow_ne_zero 10 ha)).2
    have hh : E9 a * (1 - q*a^3) + mu*a^10 = 0 := by
      have := (div_eq_iff hd).mp (show mu*a^10/(1-q*a^3) = -E9 a by linarith)
      nlinarith [this]
    linarith
  · intro h
    rw [h]
    field_simp
    ring

theorem complete_root (E9 : ℝ → ℝ) (a : ℝ) (ha : a ≠ 0)
    (hd : 1 - q*a^3 ≠ 0) : complete E9 a a = 0 :=
  (link_unique E9 a (link E9 a) ha hd).2 rfl

theorem complete_root_on_source_interval (E9 : ℝ → ℝ) (a : ℝ)
    (ha0 : 0 < a) (ha1 : a < radius) : complete E9 a a = 0 :=
  complete_root E9 a (ne_of_gt ha0) (ne_of_gt (denominator_pos ha0.le ha1.le))

def coefficientBlock (mu : ℝ) (n : ℕ) : Fin 3 → ℝ :=
  fun i => if i = 0 then q^n * mu else 0

def coefficientStep (v : Fin 3 → ℝ) : Fin 3 → ℝ := fun i => q * v i

theorem coefficient_block_zero (mu : ℝ) :
    coefficientBlock mu 0 = ![mu, 0, 0] := by
  funext i
  fin_cases i <;> simp [coefficientBlock]

theorem coefficient_block_succ (mu : ℝ) (n : ℕ) :
    coefficientBlock mu (n+1) = coefficientStep (coefficientBlock mu n) := by
  funext i
  by_cases hi : i = 0
  · simp [coefficientBlock, coefficientStep, hi, pow_succ, mul_comm, mul_left_comm]
  · simp [coefficientBlock, coefficientStep, hi]

theorem coefficient_block_coordinates (mu : ℝ) (n : ℕ) :
    coefficientBlock mu n 0 = q^n*mu ∧ coefficientBlock mu n 1 = 0 ∧
      coefficientBlock mu n 2 = 0 := by
  simp [coefficientBlock]

theorem coefficient_orbit_unique (mu : ℝ) (v : ℕ → Fin 3 → ℝ)
    (hzero : v 0 = coefficientBlock mu 0)
    (hstep : ∀ n, v (n+1) = coefficientStep (v n)) :
    ∀ n, v n = coefficientBlock mu n := by
  intro n
  induction n with
  | zero => exact hzero
  | succ n ih => rw [hstep, ih, coefficient_block_succ]

def term (mu x : ℝ) (n : ℕ) : ℝ := mu * q^n * x^(10+3*n)

theorem term_geometric (mu x : ℝ) (n : ℕ) :
    term mu x n = (mu*x^10) * (q*x^3)^n := by
  simp only [term, pow_add, pow_mul, mul_pow]
  ring

def truncation (E9 : ℝ → ℝ) (mu : ℝ) (M : ℕ) (x : ℝ) : ℝ :=
  E9 x + ∑ n ∈ range (M+1), term mu x n

theorem partial_succ (E9 : ℝ → ℝ) (mu : ℝ) (M : ℕ) (x : ℝ) :
    truncation E9 mu (M+1) x = truncation E9 mu M x + term mu x (M+1) := by
  simp [truncation, sum_range_succ, add_assoc]

theorem tail_hasSum (mu x : ℝ) (hx : |q*x^3| < 1) :
    HasSum (term mu x) (correction mu x) := by
  have h := (hasSum_geometric_of_abs_lt_one hx).mul_left (mu*x^10)
  change HasSum (fun n => term mu x n) (correction mu x)
  simpa only [term_geometric, correction, div_eq_mul_inv] using h

theorem tail_tsum (mu x : ℝ) (hx : |q*x^3| < 1) :
    ∑' n, term mu x n = correction mu x := (tail_hasSum mu x hx).tsum_eq

theorem remainder_exact (E9 : ℝ → ℝ) (mu x : ℝ) (M : ℕ)
    (hd : 1 - q*x^3 ≠ 0) :
    chart E9 mu x - truncation E9 mu M x =
      mu*x^10 * (q*x^3)^(M+1) / (1-q*x^3) := by
  have hsum : (∑ n ∈ range (M+1), (q*x^3)^n) =
      (1-(q*x^3)^(M+1))/(1-q*x^3) :=
    (eq_div_iff hd).2 (geom_sum_mul_neg (q*x^3) (M+1))
  simp only [chart, correction, truncation, term_geometric, ← mul_sum, hsum]
  field_simp
  ring

theorem partial_tendsto (E9 : ℝ → ℝ) (mu x : ℝ) (hx : |q*x^3| < 1) :
    Tendsto (fun M => truncation E9 mu M x) atTop (𝓝 (chart E9 mu x)) := by
  have ht := (tail_hasSum mu x hx).tendsto_sum_nat
  have hs := ht.comp (tendsto_add_atTop_nat 1)
  simpa only [truncation, chart] using hs.const_add (E9 x)

def tailBound (mu : ℝ) (M : ℕ) : ℝ :=
  |mu| * radius^10 * ratioBound^(M+1) / (1-ratioBound)

theorem remainder_bound (E9 : ℝ → ℝ) (mu x : ℝ) (M : ℕ)
    (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    |chart E9 mu x - truncation E9 mu M x| ≤ tailBound mu M := by
  have ht := ratio_bounds hx0 hx1
  have ht0 := ht.1
  have ht1 := ht.2
  have hd := denominator_pos hx0 hx1
  have hr := ratioBound_lt_one
  have hr0 := ratioBound_nonneg
  have hR := radius_pos.le
  have hrden : 0 < 1-ratioBound := sub_pos.mpr hr
  rw [remainder_exact E9 mu x M (ne_of_gt hd)]
  rw [abs_div, abs_mul, abs_mul, abs_of_nonneg (pow_nonneg hx0 10),
    abs_of_nonneg (pow_nonneg ht.1 (M+1)), abs_of_pos hd]
  unfold tailBound
  gcongr

theorem tail_bound_tendsto (mu : ℝ) :
    Tendsto (tailBound mu) atTop (𝓝 0) := by
  have h := (tendsto_pow_atTop_nhds_zero_of_lt_one
    ratioBound_nonneg ratioBound_lt_one).comp (tendsto_add_atTop_nat 1)
  simpa [tailBound] using (h.const_mul (|mu| * radius^10)).div_const (1-ratioBound)

theorem truncation_tendsto_uniformly (E9 : ℝ → ℝ) (mu : ℝ) :
    TendstoUniformlyOn (truncation E9 mu) (chart E9 mu) atTop (Set.Icc 0 radius) := by
  apply Metric.tendstoUniformlyOn_iff.mpr
  intro eps heps
  have h := (tendsto_order.mp (tail_bound_tendsto mu)).2 eps heps
  filter_upwards [h] with M hM
  intro x hx
  rw [Real.dist_eq]
  exact (remainder_bound E9 mu x M hx.1 hx.2).trans_lt hM

theorem source_remainder_bound (E9 : ℝ → ℝ) (mu x : ℝ) (M : ℕ)
    (hmu : |mu| ≤ lambdaBound) (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    |chart E9 mu x - truncation E9 mu M x| ≤
      (8711 / (10:ℝ)^29) * ratioBound^(M+1) / (1-ratioBound) := by
  apply (remainder_bound E9 mu x M hx0 hx1).trans
  have hid : lambdaBound * radius^10 = (8711 / (10:ℝ)^29) := by
    norm_num [lambdaBound, radius]
  rw [← hid]
  unfold tailBound
  have hr : 0 < 1-ratioBound := sub_pos.mpr ratioBound_lt_one
  have hR : 0 ≤ radius := radius_pos.le
  have hq := ratioBound_nonneg
  gcongr

def correctionDerivative (mu x : ℝ) : ℝ :=
  mu * (10*x^9/(1-q*x^3) + 3*q*x^12/(1-q*x^3)^2)

theorem hasDerivAt_correction (mu x : ℝ) (hd : 1-q*x^3 ≠ 0) :
    HasDerivAt (correction mu) (correctionDerivative mu x) x := by
  have hn := ((hasDerivAt_id x).pow 10).const_mul mu
  have hden := (hasDerivAt_const x (1:ℝ)).sub (((hasDerivAt_id x).pow 3).const_mul q)
  convert hn.div hden hd using 1
  dsimp [correction, correctionDerivative]
  field_simp
  ring

def derivativeBound : ℝ :=
  lambdaBound * (10*radius^9/(1-ratioBound) +
    3*q*radius^12/(1-ratioBound)^2)

theorem derivative_bound_small : derivativeBound < 8712 / (10:ℝ)^26 := by
  norm_num [derivativeBound, lambdaBound, radius, ratioBound, q]

theorem correction_derivative_bound (mu x : ℝ) (hmu : |mu| ≤ lambdaBound)
    (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    |correctionDerivative mu x| ≤ derivativeBound := by
  have hq := q_pos.le
  have hL : 0 ≤ lambdaBound := by norm_num [lambdaBound]
  have hR := radius_pos.le
  have hden := denominator_pos hx0 hx1
  have hrden : 0 < 1-ratioBound := sub_pos.mpr ratioBound_lt_one
  have hratio := (ratio_bounds hx0 hx1).2
  have hf : 0 ≤ 10*x^9/(1-q*x^3) + 3*q*x^12/(1-q*x^3)^2 := by positivity
  unfold correctionDerivative derivativeBound
  rw [abs_mul, abs_of_nonneg hf]
  gcongr

theorem chart_hasDerivAt (E9 : ℝ → ℝ) (mu x v : ℝ)
    (hE : HasDerivAt E9 v x) (hd : 1-q*x^3 ≠ 0) :
    HasDerivAt (chart E9 mu) (v+correctionDerivative mu x) x :=
  hE.add (hasDerivAt_correction mu x hd)

/-- The source's derivative margin survives the bounded geometric correction. -/
theorem chart_derivative_lower (E9 E9' : ℝ → ℝ) (mu x : ℝ)
    (hmu : |mu| ≤ lambdaBound) (hx0 : 0 ≤ x) (hx1 : x ≤ radius)
    (hE : HasDerivAt E9 (E9' x) x) (hmargin : 624/100 < E9' x) :
    6239/1000 < deriv (chart E9 mu) x := by
  rw [(chart_hasDerivAt E9 mu x (E9' x) hE
    (ne_of_gt (denominator_pos hx0 hx1))).deriv]
  have hb := correction_derivative_bound mu x hmu hx0 hx1
  have hlo := (abs_le.mp hb).1
  have hs := derivative_bound_small
  norm_num at hs ⊢
  linarith

theorem chart_strictMonoOn (E9 E9' : ℝ → ℝ) (mu : ℝ)
    (hmu : |mu| ≤ lambdaBound)
    (hE : ∀ x ∈ Set.Icc 0 radius, HasDerivAt E9 (E9' x) x)
    (hmargin : ∀ x ∈ Set.Icc 0 radius, 624/100 < E9' x) :
    StrictMonoOn (chart E9 mu) (Set.Icc 0 radius) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc 0 radius)
  · intro x hx
    exact (chart_hasDerivAt E9 mu x (E9' x) (hE x hx)
      (ne_of_gt (denominator_pos hx.1 hx.2))).continuousAt.continuousWithinAt
  · intro x hx
    have hxi : x ∈ Set.Icc 0 radius := interior_subset hx
    have h := chart_derivative_lower E9 E9' mu x hmu hxi.1 hxi.2
      (hE x hxi) (hmargin x hxi)
    linarith

/-- Unique internal root conditional on the explicit source enclosure for the link.
The known precoordinate is represented as this root; it is not selected anew. -/
theorem complete_unique_root (E9 E9' : ℝ → ℝ) (a : ℝ)
    (ha0 : 0 < a) (ha1 : a < radius) (hlambda : |link E9 a| ≤ lambdaBound)
    (hE : ∀ x ∈ Set.Icc 0 radius, HasDerivAt E9 (E9' x) x)
    (hmargin : ∀ x ∈ Set.Icc 0 radius, 624/100 < E9' x) :
    ∃! x, x ∈ Set.Ioo 0 radius ∧ complete E9 a x = 0 := by
  have hroot := complete_root_on_source_interval E9 a ha0 ha1
  refine ⟨a, ⟨⟨ha0, ha1⟩, hroot⟩, ?_⟩
  intro x hx
  apply (chart_strictMonoOn E9 E9' (link E9 a) hlambda hE hmargin).injOn
    ⟨hx.1.1.le, hx.1.2.le⟩ ⟨ha0.le, ha1.le⟩
  exact hx.2.trans hroot.symm

theorem complete_root_simple (E9 E9' : ℝ → ℝ) (a : ℝ)
    (ha0 : 0 < a) (ha1 : a < radius) (hlambda : |link E9 a| ≤ lambdaBound)
    (hE : HasDerivAt E9 (E9' a) a) (hmargin : 624/100 < E9' a) :
    complete E9 a a = 0 ∧ deriv (complete E9 a) a ≠ 0 := by
  refine ⟨complete_root_on_source_interval E9 a ha0 ha1, ?_⟩
  have h := chart_derivative_lower E9 E9' (link E9 a) a hlambda ha0.le ha1.le hE hmargin
  unfold complete
  linarith

theorem truncation_at_root (E9 : ℝ → ℝ) (a : ℝ) (M : ℕ)
    (ha0 : 0 < a) (ha1 : a < radius) :
    truncation E9 (link E9 a) M a =
      -(link E9 a)*a^10*(q*a^3)^(M+1)/(1-q*a^3) := by
  have h := remainder_exact E9 (link E9 a) a M
    (ne_of_gt (denominator_pos ha0.le ha1.le))
  have hz := complete_root_on_source_interval E9 a ha0 ha1
  change chart E9 (link E9 a) a = 0 at hz
  rw [hz] at h
  calc
    truncation E9 (link E9 a) M a =
        -(link E9 a*a^10*(q*a^3)^(M+1)/(1-q*a^3)) := by linarith
    _ = _ := by ring

theorem truncation_at_root_pos (E9 : ℝ → ℝ) (a : ℝ) (M : ℕ)
    (ha0 : 0 < a) (ha1 : a < radius) (hlink : link E9 a < 0) :
    0 < truncation E9 (link E9 a) M a := by
  rw [truncation_at_root E9 a M ha0 ha1]
  have hq := q_pos
  have hd := denominator_pos ha0.le ha1.le
  have hn : 0 < -(link E9 a) := neg_pos.mpr hlink
  positivity

def jet9Derivative (p x : ℝ) : ℝ :=
  2*p - (7/2)*x + 3*x^2/(2*p) + x^3/5 - 10*x^4/21 - 3*x^5/23 -
    7*x^6/120 + 8*x^7/45 + 2*x^8/55

theorem jet9_hasDerivAt (p delta x : ℝ) :
    HasDerivAt (jet9 p delta) (jet9Derivative p x) x := by
  have h1 := (hasDerivAt_id x).const_mul (2*p)
  have h2 := ((hasDerivAt_id x).pow 2).const_mul (7/4:ℝ)
  have h3 := ((hasDerivAt_id x).pow 3).div_const (2*p)
  have h4 := ((hasDerivAt_id x).pow 4).div_const (20:ℝ)
  have h5 := (((hasDerivAt_id x).pow 5).const_mul (2:ℝ)).div_const (21:ℝ)
  have h6 := ((hasDerivAt_id x).pow 6).div_const (46:ℝ)
  have h7 := ((hasDerivAt_id x).pow 7).div_const (120:ℝ)
  have h8 := ((hasDerivAt_id x).pow 8).div_const (45:ℝ)
  have h9 := (((hasDerivAt_id x).pow 9).const_mul (2:ℝ)).div_const (495:ℝ)
  convert ((((((((h1.sub h2).add h3).add h4).sub h5).sub h6).sub h7).add h8).add h9).sub_const delta
    using 1
  dsimp [jet9, jet9Derivative]
  ring

theorem jet9_derivative_lower (p x : ℝ) (hp : 157/50 ≤ p)
    (hx0 : 0 ≤ x) (hx1 : x ≤ radius) : 624/100 < jet9Derivative p x := by
  have hp0 : 0 < p := by linarith
  have hpos2 : 0 ≤ 3*x^2/(2*p) := by positivity
  have hpos3 : 0 ≤ x^3/5 := by positivity
  have hpos7 : 0 ≤ 8*x^7/45 := by positivity
  have hpos8 : 0 ≤ 2*x^8/55 := by positivity
  have h4 : x^4 ≤ radius^4 := by gcongr
  have h5 : x^5 ≤ radius^5 := by gcongr
  have h6 : x^6 ≤ radius^6 := by gcongr
  have hl : 157/25 - (7/2)*radius - 10*radius^4/21 - 3*radius^5/23 -
      7*radius^6/120 ≤ jet9Derivative p x := by
    unfold jet9Derivative
    nlinarith
  norm_num [radius] at hl
  linarith

theorem jet_chart_derivative_lower (p delta mu x : ℝ)
    (hp : 157/50 ≤ p) (hmu : |mu| ≤ lambdaBound)
    (hx0 : 0 ≤ x) (hx1 : x ≤ radius) :
    6239/1000 < deriv (chart (jet9 p delta) mu) x :=
  chart_derivative_lower _ _ mu x hmu hx0 hx1 (jet9_hasDerivAt p delta x)
    (jet9_derivative_lower p x hp hx0 hx1)

theorem jet_complete_unique_root (p delta a : ℝ) (hp : 157/50 ≤ p)
    (ha0 : 0 < a) (ha1 : a < radius) (hlambda : |link (jet9 p delta) a| ≤ lambdaBound) :
    ∃! x, x ∈ Set.Ioo 0 radius ∧ complete (jet9 p delta) a x = 0 := by
  apply complete_unique_root (jet9 p delta) (jet9Derivative p) a ha0 ha1 hlambda
  · intro x _
    exact jet9_hasDerivAt p delta x
  · intro x hx
    exact jet9_derivative_lower p x hp hx.1 hx.2

theorem generated_closure_lower : 157/50 ≤ ClosureAnalytic.value := by
  have h := (ClosureAnalytic.rational_brackets 1).1
  have hl : (157/50:ℝ) ≤ ClosureAnalytic.lowerQ 1 := by
    norm_num [ClosureAnalytic.lowerQ, ClosureAnalytic.quarterCount,
      ClosureAnalytic.companionCount, ClosureAnalytic.primitive_slope_value,
      ClosureAnalytic.compensator_slope_value, ClosureAnalytic.arctanPartialQ,
      ClosureAnalytic.magnitudeQ, Finset.sum_range_succ]
  exact hl.trans h

def stateChart (register : RadixRecovery.K12) (delta : ℝ) : ℝ → ℝ :=
  complete (jet9 ClosureAnalytic.value delta) (precoordinate register)

/-- The remaining hypotheses are enclosures of the upstream state coordinates,
not a root of the degree-nine jet or a prescribed decimal value of alpha. -/
theorem state_chart_unique_root (register : RadixRecovery.K12) (delta : ℝ)
    (ha0 : 0 < precoordinate register) (ha1 : precoordinate register < radius)
    (hlambda : |stateLink register delta| ≤ lambdaBound) :
    ∃! x, x ∈ Set.Ioo 0 radius ∧ stateChart register delta x = 0 :=
  jet_complete_unique_root ClosureAnalytic.value delta (precoordinate register)
    generated_closure_lower ha0 ha1 hlambda

theorem state_chart_simple_root (register : RadixRecovery.K12) (delta : ℝ)
    (ha0 : 0 < precoordinate register) (ha1 : precoordinate register < radius)
    (hlambda : |stateLink register delta| ≤ lambdaBound) :
    stateChart register delta (precoordinate register) = 0 ∧
      deriv (stateChart register delta) (precoordinate register) ≠ 0 :=
  complete_root_simple _ (jet9Derivative ClosureAnalytic.value) _ ha0 ha1 hlambda
    (jet9_hasDerivAt _ _ _)
    (jet9_derivative_lower _ _ generated_closure_lower ha0.le ha1.le)

theorem state_chart_root_iff (register : RadixRecovery.K12) (delta x : ℝ)
    (ha0 : 0 < precoordinate register) (ha1 : precoordinate register < radius)
    (hlambda : |stateLink register delta| ≤ lambdaBound) (hx : x ∈ Set.Ioo 0 radius) :
    stateChart register delta x = 0 ↔ x = precoordinate register := by
  have hz := (state_chart_simple_root register delta ha0 ha1 hlambda).1
  constructor
  · intro hroot
    have hm := chart_strictMonoOn (jet9 ClosureAnalytic.value delta)
      (jet9Derivative ClosureAnalytic.value) (stateLink register delta) hlambda
      (fun y _ => jet9_hasDerivAt _ _ y)
      (fun y hy => jet9_derivative_lower _ y generated_closure_lower hy.1 hy.2)
    exact hm.injOn ⟨hx.1.le, hx.2.le⟩ ⟨ha0.le, ha1.le⟩ (hroot.trans hz.symm)
  · rintro rfl
    exact hz

end AlphaAnalyticChart
end

#print axioms AlphaAnalyticChart.link_unique
#print axioms AlphaAnalyticChart.complete_root
#print axioms AlphaAnalyticChart.coefficient_orbit_unique
#print axioms AlphaAnalyticChart.tail_hasSum
#print axioms AlphaAnalyticChart.remainder_exact
#print axioms AlphaAnalyticChart.partial_tendsto
#print axioms AlphaAnalyticChart.remainder_bound
#print axioms AlphaAnalyticChart.truncation_tendsto_uniformly
#print axioms AlphaAnalyticChart.source_remainder_bound
#print axioms AlphaAnalyticChart.hasDerivAt_correction
#print axioms AlphaAnalyticChart.correction_derivative_bound
#print axioms AlphaAnalyticChart.chart_derivative_lower
#print axioms AlphaAnalyticChart.complete_unique_root
#print axioms AlphaAnalyticChart.complete_root_simple
#print axioms AlphaAnalyticChart.truncation_at_root_pos
#print axioms AlphaAnalyticChart.jet9_hasDerivAt
#print axioms AlphaAnalyticChart.jet9_derivative_lower
#print axioms AlphaAnalyticChart.generated_closure_lower
#print axioms AlphaAnalyticChart.state_chart_unique_root
#print axioms AlphaAnalyticChart.state_chart_simple_root
#print axioms AlphaAnalyticChart.state_chart_root_iff
#print axioms AlphaAnalyticChart.q_pos
#print axioms AlphaAnalyticChart.radius_pos
#print axioms AlphaAnalyticChart.ratioBound_nonneg
#print axioms AlphaAnalyticChart.ratioBound_lt_one
#print axioms AlphaAnalyticChart.precoordinate_eq_carry_value
#print axioms AlphaAnalyticChart.ratio_bounds
#print axioms AlphaAnalyticChart.denominator_pos
#print axioms AlphaAnalyticChart.complete_root_on_source_interval
#print axioms AlphaAnalyticChart.coefficient_block_zero
#print axioms AlphaAnalyticChart.coefficient_block_succ
#print axioms AlphaAnalyticChart.coefficient_block_coordinates
#print axioms AlphaAnalyticChart.term_geometric
#print axioms AlphaAnalyticChart.partial_succ
#print axioms AlphaAnalyticChart.tail_tsum
#print axioms AlphaAnalyticChart.tail_bound_tendsto
#print axioms AlphaAnalyticChart.derivative_bound_small
#print axioms AlphaAnalyticChart.chart_hasDerivAt
#print axioms AlphaAnalyticChart.chart_strictMonoOn
#print axioms AlphaAnalyticChart.truncation_at_root
#print axioms AlphaAnalyticChart.jet_chart_derivative_lower
#print axioms AlphaAnalyticChart.jet_complete_unique_root
