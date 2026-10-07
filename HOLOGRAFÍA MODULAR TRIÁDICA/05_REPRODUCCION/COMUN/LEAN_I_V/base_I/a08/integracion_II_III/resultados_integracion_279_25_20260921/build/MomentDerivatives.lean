import OrientedSeries
import ConstitutiveResponse
import Mathlib.Analysis.Calculus.SmoothSeries
import Mathlib.Analysis.SpecialFunctions.Complex.Arctan
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv

/-! Local uniform summation of actual term derivatives, followed by recognition
of the already constructed sum as arctan. -/

noncomputable section

open Filter Set
open scoped Topology

namespace HMT.III.OrientedMoment

def derivativeTerm (n : ℕ) (s : ℝ) : ℝ :=
  (-1) ^ n * s ^ (2 * n) / ((2 * n + 1 : ℕ) : ℝ)

def euler (f : ℝ → ℝ) (s : ℝ) : ℝ := s * deriv f s

theorem term_hasDerivAt (n : ℕ) (s : ℝ) : HasDerivAt (term n) (derivativeTerm n s) s := by
  have hn : ((2 * n + 1 : ℕ) : ℝ) ≠ 0 := by positivity
  convert (((hasDerivAt_id s).pow (2 * n + 1)).const_mul ((-1 : ℝ) ^ n)).div_const
    (((2 * n + 1 : ℕ) : ℝ) ^ 2) using 1
  unfold derivativeTerm
  simp only [Nat.add_sub_cancel, mul_one]
  field_simp [hn]
  ring

theorem derivativeTerm_norm (n : ℕ) (s : ℝ) :
    ‖derivativeTerm n s‖ = ‖s‖ ^ (2 * n) / ((2 * n + 1 : ℕ) : ℝ) := by
  simp [derivativeTerm, norm_div, norm_mul, norm_pow,
    abs_of_nonneg (by positivity : 0 ≤ 2 * (n : ℝ) + 1)]

theorem derivativeTerm_bound (n : ℕ) {s r : ℝ} (hs : ‖s‖ ≤ r) :
    ‖derivativeTerm n s‖ ≤ r ^ (2 * n) := by
  rw [derivativeTerm_norm]
  apply le_trans (div_le_self (pow_nonneg (norm_nonneg s) _) ?_)
    (pow_le_pow_left₀ (norm_nonneg s) hs _)
  have hn : (1 : ℕ) ≤ 2 * n + 1 := by omega
  exact_mod_cast hn

theorem derivativeMajorant_summable {r : ℝ} (hr0 : 0 ≤ r) (hr1 : r < 1) :
    Summable (fun n : ℕ => r ^ (2 * n)) := by
  simpa only [pow_mul] using summable_geometric_of_lt_one (sq_nonneg r)
    (pow_lt_one₀ hr0 hr1 (by decide : (2 : ℕ) ≠ 0))

theorem derivativeSeries_uniform {r : ℝ} (hr0 : 0 < r) (hr1 : r < 1) :
    TendstoUniformlyOn (fun N : ℕ => fun s => ∑ n ∈ Finset.range N, derivativeTerm n s)
      (fun s => ∑' n, derivativeTerm n s) atTop (Icc (-r) r) := by
  apply tendstoUniformlyOn_tsum_nat (derivativeMajorant_summable hr0.le hr1)
  intro n s hs
  exact derivativeTerm_bound n (by simpa only [Real.norm_eq_abs] using abs_le.mpr hs)

theorem moment_hasDerivAt {s : ℝ} (hs : ‖s‖ < 1) :
    HasDerivAt moment (∑' n, derivativeTerm n s) s := by
  let r : ℝ := (1 + ‖s‖) / 2
  have hsabs : |s| < 1 := by simpa only [Real.norm_eq_abs] using hs
  have hr0 : 0 < r := by dsimp [r]; positivity
  have hr1 : r < 1 := by dsimp [r]; linarith
  have hsr : ‖s‖ < r := by dsimp [r]; linarith
  apply hasDerivAt_tsum_of_isPreconnected (derivativeMajorant_summable hr0.le hr1)
    isOpen_Ioo (convex_Ioo (-r) r).isPreconnected
    (fun n t _ => term_hasDerivAt n t)
    (fun n t ht => derivativeTerm_bound n (by simpa only [Real.norm_eq_abs] using (abs_lt.mpr ht).le))
    (show (0 : ℝ) ∈ Ioo (-r) r by constructor <;> linarith)
    (moment_summable (s := 0) (by norm_num))
  exact abs_lt.mp (by simpa only [Real.norm_eq_abs] using hsr)

theorem derivativeSeries_summable {s : ℝ} (hs : ‖s‖ < 1) :
    Summable (fun n => derivativeTerm n s) :=
  Summable.of_norm_bounded (derivativeMajorant_summable (norm_nonneg s) hs)
    (fun n => derivativeTerm_bound n le_rfl)

theorem weighted_derivativeSeries {s : ℝ} (hs : ‖s‖ < 1) :
    s * (∑' n, derivativeTerm n s) = Real.arctan s := by
  have ha : HasSum (fun n => s * derivativeTerm n s) (Real.arctan s) := by
    apply (Real.hasSum_arctan hs).congr
    intro n
    simp only [derivativeTerm, pow_succ]
    ring
  exact ((derivativeSeries_summable hs).hasSum.mul_left s).unique ha

theorem euler_moment {s : ℝ} (hs : ‖s‖ < 1) : euler moment s = Real.arctan s := by
  rw [euler, (moment_hasDerivAt hs).deriv]
  exact weighted_derivativeSeries hs

theorem euler_moment_eventually {s : ℝ} (hs : ‖s‖ < 1) :
    euler moment =ᶠ[𝓝 s] Real.arctan := by
  have hmem : s ∈ Ioo (-1 : ℝ) 1 := abs_lt.mp (by simpa only [Real.norm_eq_abs] using hs)
  filter_upwards [isOpen_Ioo.mem_nhds hmem] with t ht
  exact euler_moment (by simpa only [Real.norm_eq_abs] using abs_lt.mpr ht)

theorem euler_moment_hasDerivAt {s : ℝ} (hs : ‖s‖ < 1) :
    HasDerivAt (euler moment) (1 / (1 + s ^ 2)) s :=
  (Real.hasDerivAt_arctan s).congr_of_eventuallyEq (euler_moment_eventually hs)

theorem second_euler_moment {s : ℝ} (hs : ‖s‖ < 1) :
    euler (euler moment) s = kernel s := by
  rw [euler, (euler_moment_hasDerivAt hs).deriv]
  simp [kernel, div_eq_mul_inv]

theorem euler_origin_limit : Tendsto (euler moment) (𝓝 (0 : ℝ)) (𝓝 0) := by
  have h := (Real.continuous_arctan.tendsto 0).congr' (euler_moment_eventually (s := 0) (by norm_num)).symm
  simpa using h

theorem euler_right_origin_limit : Tendsto (euler moment) (𝓝[>] (0 : ℝ)) (𝓝 0) :=
  euler_origin_limit.mono_left nhdsWithin_le_nhds

theorem moment_endpoint_limit : Tendsto moment (𝓝[Icc (0 : ℝ) 1] 1) (𝓝 catalan) :=
  moment_continuousOn 1 (by constructor <;> norm_num)

theorem constitutive_relation {s : ℝ} (hs0 : 0 < s) (hs1 : s < 1) :
    (1 + s + s ^ 2) / (1 + s + s ^ 2 + s ^ 3) =
      ((1 + s + s ^ 2) / (s * (1 + s))) * euler (euler moment) s := by
  rw [second_euler_moment (by simpa only [Real.norm_eq_abs, abs_of_pos hs0] using hs1)]
  unfold kernel
  have hfactor : 1 + s + s ^ 2 + s ^ 3 = (1 + s) * (1 + s ^ 2) := by ring
  rw [hfactor]
  field_simp [ne_of_gt hs0, ne_of_gt (by positivity : 0 < 1 + s),
    ne_of_gt (by positivity : 0 < 1 + s ^ 2)]
  ring

theorem existing_response_relation {s : ℝ} (hs0 : 0 < s) (hs1 : s < 1) :
    HMT.III.Constitutive.response s =
      ((1 + s + s ^ 2) / (s * (1 + s))) * euler (euler moment) s :=
  constitutive_relation hs0 hs1

#print axioms derivativeSeries_uniform
#print axioms moment_hasDerivAt
#print axioms euler_moment
#print axioms second_euler_moment
#print axioms euler_right_origin_limit
#print axioms moment_endpoint_limit
#print axioms constitutive_relation
#print axioms existing_response_relation

end HMT.III.OrientedMoment
