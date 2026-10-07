import LatticeDongBinomial
import LatticeOrderedConvolution

/-!
Ordered convolution on three-variable coefficient arrays, on a fixed
input vector. All exchanges with finite polynomial shifts are justified
by one-sided bounds; no unsupported product of arbitrary distributions
is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeTripleConvolution

open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeOrderedConvolution
open HMT.IV.LatticeDongBinomial

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def FirstAdmissible (F : TriCoefficients V) : Prop :=
  ∀ c, FirstBounded (fun a b => F a b c)

def SecondAdmissible (F : TriCoefficients V) : Prop :=
  ∀ c, SecondBounded (fun a b => F a b c)

def shift (x y z : ℤ) (F : TriCoefficients V) : TriCoefficients V :=
  fun a b c => F (a-x) (b-y) (c-z)

def leftConv (p : ℤ) (F : TriCoefficients V) : TriCoefficients V :=
  fun a b c => leftProduct p (fun i j => F i j c) a b

def rightConv (p : ℤ) (F : TriCoefficients V) : TriCoefficients V :=
  fun a b c => rightProduct p (fun i j => F i j c) a b

omit [Module ℂ V] in
theorem firstAdmissible_shift (x y z : ℤ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : FirstAdmissible (shift x y z F) := by
  intro c
  obtain ⟨l,hl⟩ := hF (c-z)
  exact ⟨l+x, fun a b ha => hl (a-x) (b-y) (by omega)⟩

omit [Module ℂ V] in
theorem secondAdmissible_shift (x y z : ℤ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : SecondAdmissible (shift x y z F) := by
  intro c
  obtain ⟨u,hu⟩ := hF (c-z)
  exact ⟨u+y, fun a b hb => hu (a-x) (b-y) (by omega)⟩

omit [Module ℂ V] in
theorem firstAdmissible_sub {F G : TriCoefficients V}
    (hF : FirstAdmissible F) (hG : FirstAdmissible G) : FirstAdmissible (F-G) := by
  intro c
  obtain ⟨l,hl⟩ := hF c
  obtain ⟨u,hu⟩ := hG c
  dsimp only at hl hu
  refine ⟨min l u, fun a b ha => ?_⟩
  change F a b c - G a b c = 0
  rw [hl _ _ (lt_of_lt_of_le ha (min_le_left _ _)),
    hu _ _ (lt_of_lt_of_le ha (min_le_right _ _)), sub_self]

omit [Module ℂ V] in
theorem secondAdmissible_sub {F G : TriCoefficients V}
    (hF : SecondAdmissible F) (hG : SecondAdmissible G) : SecondAdmissible (F-G) := by
  intro c
  obtain ⟨l,hl⟩ := hF c
  obtain ⟨u,hu⟩ := hG c
  dsimp only at hl hu
  refine ⟨min l u, fun a b hb => ?_⟩
  change F a b c - G a b c = 0
  rw [hl _ _ (lt_of_lt_of_le hb (min_le_left _ _)),
    hu _ _ (lt_of_lt_of_le hb (min_le_right _ _)), sub_self]

theorem leftConv_shift (p x y z : ℤ) (F : TriCoefficients V) :
    leftConv p (shift x y z F) = shift x y z (leftConv p F) := by
  funext a b c
  unfold leftConv leftProduct convolution shift
  apply finsum_congr
  intro j
  dsimp only
  rw [show a-p+j-x = (a-x)-p+j by omega,
    show b-j-y = (b-y)-j by omega]

theorem rightConv_shift (p x y z : ℤ) (F : TriCoefficients V) :
    rightConv p (shift x y z F) = shift x y z (rightConv p F) := by
  funext a b c
  unfold rightConv rightProduct convolution shift
  apply finsum_congr
  intro j
  dsimp only
  rw [show a-p+j-x = (a-x)-p+j by omega,
    show b-j-y = (b-y)-j by omega]

theorem leftConv_sub (p : ℤ) {F G : TriCoefficients V}
    (hF : SecondAdmissible F) (hG : SecondAdmissible G) :
    leftConv p (F-G) = leftConv p F - leftConv p G := by
  funext a b c
  simp only [leftConv, leftProduct, convolution, Pi.sub_apply, smul_sub]
  exact finsum_sub_distrib
    (convolution_finite_second p _ _ ⟨0,leftKernel_support p⟩ (hF c) a b)
    (convolution_finite_second p _ _ ⟨0,leftKernel_support p⟩ (hG c) a b)

theorem rightConv_sub (p : ℤ) {F G : TriCoefficients V}
    (hF : FirstAdmissible F) (hG : FirstAdmissible G) :
    rightConv p (F-G) = rightConv p F - rightConv p G := by
  funext a b c
  simp only [rightConv, rightProduct, convolution, Pi.sub_apply, smul_sub]
  exact finsum_sub_distrib
    (convolution_finite_first p _ _ ⟨p,rightKernel_support p⟩ (hF c) a b)
    (convolution_finite_first p _ _ ⟨p,rightKernel_support p⟩ (hG c) a b)

theorem leftConv_zero (p : ℤ) : leftConv p (0 : TriCoefficients V) = 0 := by
  funext a b c
  simp [leftConv, leftProduct, convolution]

theorem rightConv_zero (p : ℤ) : rightConv p (0 : TriCoefficients V) = 0 := by
  funext a b c
  simp [rightConv, rightProduct, convolution]

theorem firstThird_as_shift (F : TriCoefficients V) :
    firstThird F = shift 1 0 0 F - shift 0 0 1 F := by
  funext a b c
  simp [firstThird, shift]

theorem firstSecond_as_shift (F : TriCoefficients V) :
    firstSecond F = shift 1 0 0 F - shift 0 1 0 F := by
  funext a b c
  simp [firstSecond, shift]

theorem secondThird_as_shift (F : TriCoefficients V) :
    secondThird F = shift 0 1 0 F - shift 0 0 1 F := by
  funext a b c
  simp [secondThird, shift]

theorem secondAdmissible_firstThird {F : TriCoefficients V}
    (hF : SecondAdmissible F) : SecondAdmissible (firstThird F) := by
  rw [firstThird_as_shift]
  exact secondAdmissible_sub (secondAdmissible_shift _ _ _ hF)
    (secondAdmissible_shift _ _ _ hF)

theorem secondAdmissible_secondThird {F : TriCoefficients V}
    (hF : SecondAdmissible F) : SecondAdmissible (secondThird F) := by
  rw [secondThird_as_shift]
  exact secondAdmissible_sub (secondAdmissible_shift _ _ _ hF)
    (secondAdmissible_shift _ _ _ hF)

theorem firstAdmissible_firstThird {F : TriCoefficients V}
    (hF : FirstAdmissible F) : FirstAdmissible (firstThird F) := by
  rw [firstThird_as_shift]
  exact firstAdmissible_sub (firstAdmissible_shift _ _ _ hF)
    (firstAdmissible_shift _ _ _ hF)

theorem firstAdmissible_secondThird {F : TriCoefficients V}
    (hF : FirstAdmissible F) : FirstAdmissible (secondThird F) := by
  rw [secondThird_as_shift]
  exact firstAdmissible_sub (firstAdmissible_shift _ _ _ hF)
    (firstAdmissible_shift _ _ _ hF)

theorem leftConv_firstThird (p : ℤ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : leftConv p (firstThird F) = firstThird (leftConv p F) := by
  rw [firstThird_as_shift, leftConv_sub p (secondAdmissible_shift _ _ _ hF)
    (secondAdmissible_shift _ _ _ hF), leftConv_shift, leftConv_shift,
    firstThird_as_shift]

theorem leftConv_secondThird (p : ℤ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : leftConv p (secondThird F) = secondThird (leftConv p F) := by
  rw [secondThird_as_shift, leftConv_sub p (secondAdmissible_shift _ _ _ hF)
    (secondAdmissible_shift _ _ _ hF), leftConv_shift, leftConv_shift,
    secondThird_as_shift]

theorem rightConv_firstThird (p : ℤ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : rightConv p (firstThird F) = firstThird (rightConv p F) := by
  rw [firstThird_as_shift, rightConv_sub p (firstAdmissible_shift _ _ _ hF)
    (firstAdmissible_shift _ _ _ hF), rightConv_shift, rightConv_shift,
    firstThird_as_shift]

theorem rightConv_secondThird (p : ℤ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : rightConv p (secondThird F) = secondThird (rightConv p F) := by
  rw [secondThird_as_shift, rightConv_sub p (firstAdmissible_shift _ _ _ hF)
    (firstAdmissible_shift _ _ _ hF), rightConv_shift, rightConv_shift,
    secondThird_as_shift]

theorem firstSecond_leftConv (p : ℤ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : firstSecond (leftConv p F) = leftConv (p+1) F := by
  funext a b c
  exact congrFun (congrFun (LatticeOrderedConvolution.crossing_leftProduct p
    (fun i j => F i j c) (hF c)) a) b

theorem firstSecond_rightConv (p : ℤ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : firstSecond (rightConv p F) = rightConv (p+1) F := by
  funext a b c
  exact congrFun (congrFun (LatticeOrderedConvolution.crossing_rightProduct p
    (fun i j => F i j c) (hF c)) a) b

theorem firstSecond_pow_leftConv (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : (firstSecond^N) (leftConv p F) = leftConv (p+N) F := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, ih, firstSecond_leftConv _ hF]
    push_cast
    ring

theorem firstSecond_pow_rightConv (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : (firstSecond^N) (rightConv p F) = rightConv (p+N) F := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, ih, firstSecond_rightConv _ hF]
    push_cast
    ring

theorem leftConv_pow (p : ℤ) (T : Module.End ℂ (TriCoefficients V))
    (hT : ∀ F, SecondAdmissible F → SecondAdmissible (T F))
    (hcomm : ∀ F, SecondAdmissible F → leftConv p (T F) = T (leftConv p F))
    (N : ℕ) {F : TriCoefficients V} (hF : SecondAdmissible F) :
    leftConv p ((T^N) F) = (T^N) (leftConv p F) := by
  have hadm : ∀ n : ℕ, SecondAdmissible ((T^n) F) := by
    intro n
    induction n with
    | zero => simpa using hF
    | succ n ih => rw [pow_succ', Module.End.mul_apply]; exact hT _ ih
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, hcomm _ (hadm N), ih]
    rfl

theorem rightConv_pow (p : ℤ) (T : Module.End ℂ (TriCoefficients V))
    (hT : ∀ F, FirstAdmissible F → FirstAdmissible (T F))
    (hcomm : ∀ F, FirstAdmissible F → rightConv p (T F) = T (rightConv p F))
    (N : ℕ) {F : TriCoefficients V} (hF : FirstAdmissible F) :
    rightConv p ((T^N) F) = (T^N) (rightConv p F) := by
  have hadm : ∀ n : ℕ, FirstAdmissible ((T^n) F) := by
    intro n
    induction n with
    | zero => simpa using hF
    | succ n ih => rw [pow_succ', Module.End.mul_apply]; exact hT _ ih
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [pow_succ', Module.End.mul_apply, hcomm _ (hadm N), ih]
    rfl

theorem secondAdmissible_secondThird_pow (N : ℕ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : SecondAdmissible ((secondThird^N) F) := by
  induction N with
  | zero => simpa using hF
  | succ N ih => rw [pow_succ', Module.End.mul_apply]; exact secondAdmissible_secondThird ih

theorem firstAdmissible_secondThird_pow (N : ℕ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : FirstAdmissible ((secondThird^N) F) := by
  induction N with
  | zero => simpa using hF
  | succ N ih => rw [pow_succ', Module.End.mul_apply]; exact firstAdmissible_secondThird ih

theorem leftConv_firstThird_pow (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) :
    leftConv p ((firstThird^N) F) = (firstThird^N) (leftConv p F) :=
  leftConv_pow p firstThird (fun _ => secondAdmissible_firstThird)
    (fun _ => leftConv_firstThird p) N hF

theorem leftConv_secondThird_pow (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) :
    leftConv p ((secondThird^N) F) = (secondThird^N) (leftConv p F) :=
  leftConv_pow p secondThird (fun _ => secondAdmissible_secondThird)
    (fun _ => leftConv_secondThird p) N hF

theorem rightConv_firstThird_pow (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) :
    rightConv p ((firstThird^N) F) = (firstThird^N) (rightConv p F) :=
  rightConv_pow p firstThird (fun _ => firstAdmissible_firstThird)
    (fun _ => rightConv_firstThird p) N hF

theorem rightConv_secondThird_pow (p : ℤ) (N : ℕ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) :
    rightConv p ((secondThird^N) F) = (secondThird^N) (rightConv p F) :=
  rightConv_pow p secondThird (fun _ => firstAdmissible_secondThird)
    (fun _ => rightConv_secondThird p) N hF

theorem leftKernel_zero (j : ℤ) : leftKernel 0 j = if j=0 then 1 else 0 := by
  by_cases hj : j=0
  · simp [hj, leftKernel, LatticeTwoRegionFactor.leftExpansion]
  · by_cases hpos : 0 ≤ j
    · have hnat : j.toNat ≠ 0 := by omega
      simp [leftKernel, LatticeTwoRegionFactor.leftExpansion,
        LatticeContractionPascal.contraction_zero_pairing, hj, hnat]
    · simp [leftKernel, LatticeTwoRegionFactor.leftExpansion, hpos, hj]

theorem leftConv_zero_power (F : TriCoefficients V) : leftConv 0 F = F := by
  funext a b c
  simp only [leftConv, leftProduct, convolution, leftKernel_zero]
  rw [finsum_eq_single _ 0]
  · simp
  · intro j hj
    simp [hj]

theorem rightConv_zero_power (F : TriCoefficients V) : rightConv 0 F = F := by
  have he : rightConv 0 F = leftConv 0 F := by
    funext a b c
    exact congrFun (congrFun (zero_products_equal (fun i j => F i j c)).symm a) b
  rw [he, leftConv_zero_power]

theorem leftConv_nonnegative (N : ℕ) {F : TriCoefficients V}
    (hF : SecondAdmissible F) : leftConv (N : ℤ) F = (firstSecond^N) F := by
  have h := firstSecond_pow_leftConv 0 N hF
  simpa only [leftConv_zero_power, zero_add] using h.symm

theorem rightConv_nonnegative (N : ℕ) {F : TriCoefficients V}
    (hF : FirstAdmissible F) : rightConv (N : ℤ) F = (firstSecond^N) F := by
  have h := firstSecond_pow_rightConv 0 N hF
  simpa only [rightConv_zero_power, zero_add] using h.symm

end HMT.IV.LatticeTripleConvolution
end

#print axioms HMT.IV.LatticeTripleConvolution.leftConv_sub
#print axioms HMT.IV.LatticeTripleConvolution.rightConv_sub
#print axioms HMT.IV.LatticeTripleConvolution.leftConv_firstThird
#print axioms HMT.IV.LatticeTripleConvolution.leftConv_secondThird
#print axioms HMT.IV.LatticeTripleConvolution.rightConv_firstThird
#print axioms HMT.IV.LatticeTripleConvolution.rightConv_secondThird
#print axioms HMT.IV.LatticeTripleConvolution.firstSecond_pow_leftConv
#print axioms HMT.IV.LatticeTripleConvolution.firstSecond_pow_rightConv
