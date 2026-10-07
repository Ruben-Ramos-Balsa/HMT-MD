import LatticeDongKernel
import LatticeNormalOrderedField

/-!
Residue products of the actual Laurent fields. The two expansion regions
are retained in the definition, with their order of composition and minus
sign. Every coefficient sum is locally finite on each input vector; no
uniform truncation of the carrier or its frequencies is introduced.

The negative residue of the generated Heisenberg field is then identified
with the existing normalField coefficient, rather than replacing that
field by an unrelated abstract normal product.
-/

noncomputable section
namespace HMT.IV.LatticeResidueProducts

open HMT.IV.LatticeTwoRegionFactor HMT.IV.LatticeDongKernel
open HMT.IV.LatticeNormalOrderedField

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

theorem field_lower_bound (A : VertexOperator ℂ V) (v : V) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff A k v = 0 := by
  refine ⟨HahnSeries.order ((HahnModule.of ℂ).symm (A v)), ?_⟩
  intro k hk
  exact VertexOperator.coeff_eq_zero_of_lt_order A k v hk

omit [Module ℂ V] in
private theorem finite_support_of_bound (f : ℕ → V) (N : ℕ)
    (h : ∀ a ≥ N, f a = 0) : (Function.support f).Finite := by
  apply (Finset.range N).finite_toSet.subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

/-- Residue in the expansion region with nonnegative powers of the second
variable. Its first field coefficient has exponent `a-p-1`. -/
def leftTerm (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) (a : ℕ) :
    Module.End ℂ V :=
  leftExpansion p (p-a) a •
    (HVertexOperator.coeff A (a-p-1)).comp (HVertexOperator.coeff B (k-a))

/-- The opposite expansion region retains the opposite composition order.
The minus sign belongs to residueCoefficient, not this individual term. -/
def rightTerm (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) (a : ℕ) :
    Module.End ℂ V :=
  rightExpansion p a (p-a) •
    (HVertexOperator.coeff B (k-p+a)).comp (HVertexOperator.coeff A (-a-1))

theorem leftTerm_finite (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) (v : V) :
    (Function.support (fun a => leftTerm p A B k a v)).Finite := by
  obtain ⟨b, hb⟩ := field_lower_bound B v
  apply finite_support_of_bound _ ((k-b).toNat+1)
  intro a ha
  simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    hb (k-a) (by omega), map_zero, smul_zero]

theorem rightTerm_finite (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) (v : V) :
    (Function.support (fun a => rightTerm p A B k a v)).Finite := by
  obtain ⟨b, hb⟩ := field_lower_bound A v
  apply finite_support_of_bound _ ((-b).toNat+1)
  intro a ha
  simp only [rightTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    hb (-a-1) (by omega), map_zero, smul_zero]

/-- Coefficient of `Res_t (ι(t-z)^p A(t)B(z) − ι'(t-z)^p B(z)A(t))`.
The nonnegative indices are exactly the supports of the two expansion
regions, not a cutoff on the residue or on the Laurent field. -/
def residueCoefficient (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) :
    Module.End ℂ V :=
  locallyFiniteSum (leftTerm p A B k) (leftTerm_finite p A B k) -
    locallyFiniteSum (rightTerm p A B k) (rightTerm_finite p A B k)

theorem residueCoefficient_apply (p : ℤ) (A B : VertexOperator ℂ V)
    (k : ℤ) (v : V) :
    residueCoefficient p A B k v =
      (∑ᶠ a, leftTerm p A B k a v) - ∑ᶠ a, rightTerm p A B k a v := rfl

/-- The residue coefficients have a lower Laurent bound on every input
vector. The bound is constructed from B on that vector and on the finitely
many nonzero nonnegative modes of A acting on it. -/
theorem residueCoefficient_bounded (p : ℤ) (A B : VertexOperator ℂ V) (v : V) :
    ∃ b : ℤ, ∀ k < b, residueCoefficient p A B k v = 0 := by
  classical
  obtain ⟨b, hb⟩ := field_lower_bound B v
  obtain ⟨a₀, ha₀⟩ := field_lower_bound A v
  let N : ℕ := (-a₀).toNat+1
  have hA (a : ℕ) (ha : N ≤ a) : HVertexOperator.coeff A (-a-1) v = 0 :=
    ha₀ _ (by dsimp [N] at ha; omega)
  have hfinite : ∀ a : Fin N, ∃ c : ℤ, ∀ k < c,
      HVertexOperator.coeff B k (HVertexOperator.coeff A (-(a : ℕ)-1) v) = 0 :=
    fun _ => field_lower_bound B _
  choose c hc using hfinite
  let d : ℤ := min b (-(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
    (fun a => (-(c a + p - (a : ℕ))).toNat))))
  refine ⟨d, ?_⟩
  intro k hk
  have hkb : k < b := lt_of_lt_of_le hk (min_le_left _ _)
  rw [residueCoefficient_apply]
  have hleft : (∑ᶠ a, leftTerm p A B k a v) = 0 := by
    have hz (a : ℕ) : leftTerm p A B k a v = 0 := by
      simp only [leftTerm, LinearMap.smul_apply, LinearMap.comp_apply,
        hb (k-a) (by omega), map_zero, smul_zero]
    simp only [hz, finsum_zero]
  have hright : (∑ᶠ a, rightTerm p A B k a v) = 0 := by
    have hz (a : ℕ) : rightTerm p A B k a v = 0 := by
      by_cases ha : a < N
      · let a' : Fin N := ⟨a,ha⟩
        have hsup : (-(c a' + p - (a : ℤ))).toNat ≤
            (Finset.univ : Finset (Fin N)).sup
              (fun q => (-(c q + p - (q : ℕ))).toNat) :=
          Finset.le_sup (f := fun q : Fin N => (-(c q + p - (q : ℕ))).toNat)
            (Finset.mem_univ a')
        have hkd : k < -(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
            (fun q => (-(c q + p - (q : ℕ))).toNat))) :=
          lt_of_lt_of_le hk (min_le_right b _)
        simp only [Int.ofNat_eq_coe] at hkd
        have hlow : k-p+(a : ℤ) < c a' := by omega
        have hzero : HVertexOperator.coeff B (k-p+(a : ℤ))
            (HVertexOperator.coeff A (-(a : ℤ)-1) v) = 0 := hc a' _ hlow
        simp only [rightTerm, LinearMap.smul_apply, LinearMap.comp_apply,
          hzero, smul_zero]
      · simp only [rightTerm, LinearMap.smul_apply, LinearMap.comp_apply,
          hA a (by omega), map_zero, smul_zero]
    simp only [hz, finsum_zero]
  rw [hleft, hright, sub_self]

def residueField (p : ℤ) (A B : VertexOperator ℂ V) : VertexOperator ℂ V :=
  VertexOperator.of_coeff (residueCoefficient p A B) (residueCoefficient_bounded p A B)

theorem residueField_coefficient (p : ℤ) (A B : VertexOperator ℂ V) (k : ℤ) :
    HVertexOperator.coeff (residueField p A B) k = residueCoefficient p A B k := rfl

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeHeisenbergField

theorem heisenberg_leftTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    leftTerm (-(n : ℤ)-1) (heisenbergField o i) B k a =
      creationTerm o i n B k a := by
  rw [leftTerm, left_residue_coefficient]
  have he : (a : ℤ)-(-(n : ℤ)-1)-1 = ((a+n : ℕ) : ℤ) := by omega
  rw [he]
  have hc : HVertexOperator.coeff (heisenbergField o i) ((a+n : ℕ) : ℤ) =
      onCarrier o (create o (a+n) i) := by
    change hmode o i (-((a+n : ℕ) : ℤ)-1) = _
    rw [show -((a+n : ℕ) : ℤ)-1 = Int.negSucc (a+n) by omega, hmode_negSucc]
  rw [hc]
  rfl

theorem heisenberg_neg_rightTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    -rightTerm (-(n : ℤ)-1) (heisenbergField o i) B k a =
      annihilationTerm o i n B k a := by
  apply LinearMap.ext
  intro v
  simp only [rightTerm, LinearMap.neg_apply, LinearMap.smul_apply, LinearMap.comp_apply]
  rw [← neg_smul, negative_right_residue_coefficient]
  have he : k-(-(n : ℤ)-1)+(a : ℤ) = k+a+n+1 := by omega
  rw [he]
  have hc : HVertexOperator.coeff (heisenbergField o i) (-(a : ℤ)-1) =
      hmode o i (a : ℤ) := by
    change hmode o i (-(-(a : ℤ)-1)-1) = _
    congr 1
    omega
  rw [hc]
  rfl

theorem heisenberg_residue_eq_normalCoefficient (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
    residueCoefficient (-(n : ℤ)-1) (heisenbergField o i) B k =
      normalCoefficient o i n B k := by
  apply LinearMap.ext
  intro v
  rw [residueCoefficient_apply, normalCoefficient_apply, sub_eq_add_neg, ← finsum_neg_distrib]
  congr 1
  · apply finsum_congr
    intro a
    rw [heisenberg_leftTerm]
  · apply finsum_congr
    intro a
    exact congrArg (fun F : Module.End ℂ (LatticeCarrier o) => F v)
      (heisenberg_neg_rightTerm o i n B k a)

theorem heisenberg_residue_eq_normalField (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
    residueCoefficient (-(n : ℤ)-1) (heisenbergField o i) B k =
      HVertexOperator.coeff (normalField o i n B) k :=
  heisenberg_residue_eq_normalCoefficient o i n B k

/-- Equality of the genuine Laurent fields, not only a vacuum matrix
element or an equality in a finite frequency window. -/
theorem heisenberg_residueField (o : Fin 12)
    (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) :
    residueField (-(n : ℤ)-1) (heisenbergField o i) B = normalField o i n B := by
  apply VertexOperator.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  exact congrArg (fun F : Module.End ℂ (LatticeCarrier o) => F v)
    (heisenberg_residue_eq_normalField o i n B k)

end HMT.IV.LatticeResidueProducts
end

#print axioms HMT.IV.LatticeResidueProducts.field_lower_bound
#print axioms HMT.IV.LatticeResidueProducts.leftTerm_finite
#print axioms HMT.IV.LatticeResidueProducts.rightTerm_finite
#print axioms HMT.IV.LatticeResidueProducts.residueCoefficient_apply
#print axioms HMT.IV.LatticeResidueProducts.residueCoefficient_bounded
#print axioms HMT.IV.LatticeResidueProducts.residueField_coefficient
#print axioms HMT.IV.LatticeResidueProducts.heisenberg_leftTerm
#print axioms HMT.IV.LatticeResidueProducts.heisenberg_neg_rightTerm
#print axioms HMT.IV.LatticeResidueProducts.heisenberg_residue_eq_normalCoefficient
#print axioms HMT.IV.LatticeResidueProducts.heisenberg_residue_eq_normalField
#print axioms HMT.IV.LatticeResidueProducts.heisenberg_residueField
