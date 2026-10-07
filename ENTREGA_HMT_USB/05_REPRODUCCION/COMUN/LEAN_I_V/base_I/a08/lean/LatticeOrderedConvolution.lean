import LatticeFieldLocality
import LatticeResidueProducts

/-!
Convolution in the correct ordered expansion region. A(t)B(z)v has a
lower bound in z, and B(z)A(t)v has one in t. Neither is assumed to have
both bounds before locality is applied. The one-sided kernel support
is enough for every convolution below to be pointwise finite.
-/

noncomputable section
namespace HMT.IV.LatticeOrderedConvolution

open HMT.IV.LatticeFactorConvolution
open HMT.IV.LatticeFieldLocality

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def FirstBounded (h : BiStates V) : Prop :=
  ∃ l : ℤ, ∀ a b, a < l → h a b = 0

def SecondBounded (h : BiStates V) : Prop :=
  ∃ u : ℤ, ∀ a b, b < u → h a b = 0

theorem convolution_finite_second (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hk : ∃ l : ℤ, ∀ j < l, k j = 0) (hh : SecondBounded h) (a b : ℤ) :
    (Function.support (fun j : ℤ => k j • h (a-p+j) (b-j))).Finite := by
  obtain ⟨l,hl⟩ := hk
  obtain ⟨u,hu⟩ := hh
  apply (Set.finite_Icc l (b-u)).subset
  intro j hj
  change k j • h (a-p+j) (b-j) ≠ 0 at hj
  simp only [Set.mem_Icc]
  by_contra hn
  by_cases hjl : j < l
  · exact hj (by rw [hl j hjl, zero_smul])
  · exact hj (by rw [hu _ _ (by omega), smul_zero])

theorem convolution_finite_first (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hk : ∃ u : ℤ, ∀ j, u < j → k j = 0) (hh : FirstBounded h) (a b : ℤ) :
    (Function.support (fun j : ℤ => k j • h (a-p+j) (b-j))).Finite := by
  obtain ⟨u,hu⟩ := hk
  obtain ⟨l,hl⟩ := hh
  apply (Set.finite_Icc (l-a+p) u).subset
  intro j hj
  change k j • h (a-p+j) (b-j) ≠ 0 at hj
  simp only [Set.mem_Icc]
  by_contra hn
  by_cases hju : u < j
  · exact hj (by rw [hu j hju, zero_smul])
  · exact hj (by rw [hl _ _ (by omega), smul_zero])

theorem crossing_convolution_second (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hk : ∃ l : ℤ, ∀ j < l, k j = 0) (hh : SecondBounded h) :
    crossing (convolution p k h) = convolution (p+1) (raiseKernel k) h := by
  funext a b
  change ((∑ᶠ j : ℤ, k j • h (a-1-p+j) (b-j)) -
    ∑ᶠ j : ℤ, k j • h (a-p+j) (b-1-j)) =
      ∑ᶠ j : ℤ, (k j-k (j-1)) • h (a-(p+1)+j) (b-j)
  rw [convolution_reindex_one]
  have harg : ∀ j : ℤ, a-1-p+j=a-(p+1)+j := by omega
  simp only [harg, sub_smul]
  have hshift : ∃ l : ℤ, ∀ j < l, k (j-1) = 0 := by
    obtain ⟨l,hl⟩ := hk
    exact ⟨l+1, fun j hj => hl _ (by omega)⟩
  exact (finsum_sub_distrib (convolution_finite_second (p+1) k h hk hh a b)
    (convolution_finite_second (p+1) (fun j => k (j-1)) h hshift hh a b)).symm

theorem crossing_convolution_first (p : ℤ) (k : ℤ → ℂ) (h : BiStates V)
    (hk : ∃ u : ℤ, ∀ j, u < j → k j = 0) (hh : FirstBounded h) :
    crossing (convolution p k h) = convolution (p+1) (raiseKernel k) h := by
  funext a b
  change ((∑ᶠ j : ℤ, k j • h (a-1-p+j) (b-j)) -
    ∑ᶠ j : ℤ, k j • h (a-p+j) (b-1-j)) =
      ∑ᶠ j : ℤ, (k j-k (j-1)) • h (a-(p+1)+j) (b-j)
  rw [convolution_reindex_one]
  have harg : ∀ j : ℤ, a-1-p+j=a-(p+1)+j := by omega
  simp only [harg, sub_smul]
  have hshift : ∃ u : ℤ, ∀ j, u < j → k (j-1) = 0 := by
    obtain ⟨u,hu⟩ := hk
    exact ⟨u+1, fun j hj => hu _ (by omega)⟩
  exact (finsum_sub_distrib (convolution_finite_first (p+1) k h hk hh a b)
    (convolution_finite_first (p+1) (fun j => k (j-1)) h hshift hh a b)).symm

theorem leftKernel_support (p : ℤ) : ∀ j < 0, leftKernel p j = 0 := by
  intro j hj
  simp [leftKernel, LatticeTwoRegionFactor.leftExpansion, show ¬0 ≤ j by omega]

theorem rightKernel_support (p : ℤ) : ∀ j, p < j → rightKernel p j = 0 := by
  intro j hj
  rw [rightKernel, LatticeTwoRegionFactor.rightExpansion,
    LatticeTwoRegionFactor.leftExpansion, if_neg (by omega), mul_zero]

theorem crossing_leftProduct (p : ℤ) (h : BiStates V) (hh : SecondBounded h) :
    crossing (leftProduct p h) = leftProduct (p+1) h := by
  rw [leftProduct, crossing_convolution_second p _ _ ⟨0,leftKernel_support p⟩ hh,
    raise_leftKernel]
  rfl

theorem crossing_rightProduct (p : ℤ) (h : BiStates V) (hh : FirstBounded h) :
    crossing (rightProduct p h) = rightProduct (p+1) h := by
  rw [rightProduct, crossing_convolution_first p _ _ ⟨p,rightKernel_support p⟩ hh,
    raise_rightKernel]
  rfl

theorem crossing_leftProduct_iterate (p : ℤ) (n : ℕ) (h : BiStates V)
    (hh : SecondBounded h) :
    (crossing^n) (leftProduct p h) = leftProduct (p+n) h := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply, ih, crossing_leftProduct _ _ hh]
    push_cast
    ring

theorem crossing_rightProduct_iterate (p : ℤ) (n : ℕ) (h : BiStates V)
    (hh : FirstBounded h) :
    (crossing^n) (rightProduct p h) = rightProduct (p+n) h := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply, ih, crossing_rightProduct _ _ hh]
    push_cast
    ring

theorem firstBounded_crossing (h : BiStates V) (hh : FirstBounded h) :
    FirstBounded (crossing h) := by
  obtain ⟨l,hl⟩ := hh
  refine ⟨l, fun a b ha => ?_⟩
  change h (a-1) b - h a (b-1) = 0
  rw [hl _ _ (by omega), hl _ _ ha, sub_self]

theorem secondBounded_crossing (h : BiStates V) (hh : SecondBounded h) :
    SecondBounded (crossing h) := by
  obtain ⟨u,hu⟩ := hh
  refine ⟨u, fun a b hb => ?_⟩
  change h (a-1) b - h a (b-1) = 0
  rw [hu _ _ hb, hu _ _ (by omega), sub_self]

theorem firstBounded_crossing_pow (h : BiStates V) (hh : FirstBounded h) (n : ℕ) :
    FirstBounded ((crossing^n) h) := by
  induction n with
  | zero => simpa using hh
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply]
    exact firstBounded_crossing _ ih

theorem secondBounded_crossing_pow (h : BiStates V) (hh : SecondBounded h) (n : ℕ) :
    SecondBounded ((crossing^n) h) := by
  induction n with
  | zero => simpa using hh
  | succ n ih =>
    rw [pow_succ', Module.End.mul_apply]
    exact secondBounded_crossing _ ih

omit [Module ℂ V] in
theorem lowerBounded_of_both {h : BiStates V}
    (h₁ : FirstBounded h) (h₂ : SecondBounded h) : LowerBounded h := by
  obtain ⟨l,hl⟩ := h₁
  obtain ⟨u,hu⟩ := h₂
  refine ⟨l,u,fun a b hab => ?_⟩
  rcases hab with ha | hb
  · exact hl a b ha
  · exact hu a b hb

def forwardState (A B : VertexOperator ℂ V) (v : V) : BiStates V :=
  fun a b => HVertexOperator.coeff A a (HVertexOperator.coeff B b v)

def backwardState (A B : VertexOperator ℂ V) (v : V) : BiStates V :=
  fun a b => HVertexOperator.coeff B b (HVertexOperator.coeff A a v)

theorem forwardState_secondBounded (A B : VertexOperator ℂ V) (v : V) :
    SecondBounded (forwardState A B v) := by
  obtain ⟨b,hb⟩ := LatticeResidueProducts.field_lower_bound B v
  refine ⟨b,fun a k hk => ?_⟩
  simp only [forwardState, hb k hk, map_zero]

theorem backwardState_firstBounded (A B : VertexOperator ℂ V) (v : V) :
    FirstBounded (backwardState A B v) := by
  obtain ⟨a,ha⟩ := LatticeResidueProducts.field_lower_bound A v
  refine ⟨a,fun k b hk => ?_⟩
  simp only [backwardState, ha k hk, map_zero]

theorem crossing_pow_evaluate (f : BiStates (Module.End ℂ V)) (n : ℕ) (v : V) :
    (fun a b => ((crossing^n) f a b) v) =
      (crossing^n) (fun a b => f a b v) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    funext a b
    rw [pow_succ', Module.End.mul_apply]
    change ((crossing^n) f (a-1) b) v - ((crossing^n) f a (b-1)) v = _
    rw [congrFun (congrFun ih (a-1)) b, congrFun (congrFun ih a) (b-1)]
    rw [pow_succ', Module.End.mul_apply]
    rfl

/-- Locality produces a common product with both lower bounds. It is not
an extra boundedness hypothesis imposed on an unprocessed ordered product. -/
theorem local_cleared_product_lowerBounded {A B : VertexOperator ℂ V} {N : ℕ}
    (h : LocalAt N A B) (v : V) : LowerBounded ((crossing^N) (forwardState A B v)) := by
  have he : (crossing^N) (forwardState A B v) =
      (crossing^N) (backwardState A B v) := by
    have hv := congrArg (fun f : BiStates (Module.End ℂ V) => fun a b => f a b v) h
    simpa only [crossing_pow_evaluate, forward, backward, Module.End.mul_apply,
      forwardState, backwardState] using hv
  apply lowerBounded_of_both
  · rw [he]
    exact firstBounded_crossing_pow _ (backwardState_firstBounded A B v) N
  · exact secondBounded_crossing_pow _ (forwardState_secondBounded A B v) N

end HMT.IV.LatticeOrderedConvolution
end

#print axioms HMT.IV.LatticeOrderedConvolution.convolution_finite_second
#print axioms HMT.IV.LatticeOrderedConvolution.convolution_finite_first
#print axioms HMT.IV.LatticeOrderedConvolution.crossing_leftProduct_iterate
#print axioms HMT.IV.LatticeOrderedConvolution.crossing_rightProduct_iterate
#print axioms HMT.IV.LatticeOrderedConvolution.local_cleared_product_lowerBounded
