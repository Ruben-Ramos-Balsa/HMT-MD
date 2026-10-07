import LatticeTwistedTensorField
import LatticeNormalOrderedField

/-!
Normal ordering of the inherited half-Heisenberg field with an arbitrary
Laurent field on the actual twisted carrier. The variable is t, with z=t².
The split is by oscillator mode, not by the sign of the t exponent:
the creator indexed by a=0 has exponent -1. Both sums are pointwise finite,
and their sum has a Laurent lower bound on every vector. This module treats
the undifferentiated product only; it assumes no Jacobi or state-field axiom.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalProduct

open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeHalfIntegerField LatticeTwistedTensorField
open LatticeNormalOrderedField (locallyFiniteSum)
open scoped BigOperators

private theorem finite_support_of_bound {V : Type*} [Zero V]
    (f : ℕ → V) (N : ℕ) (h : ∀ a ≥ N, f a = 0) :
    (Function.support f).Finite := by
  apply (Finset.range N).finite_toSet.subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

theorem field_has_bound (o : Fin 12) (B : VertexOperator ℂ (Carrier o))
    (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff B k v = 0 := by
  refine ⟨HahnSeries.order ((HahnModule.of ℂ).symm (B v)), ?_⟩
  intro k hk
  exact VertexOperator.coeff_eq_zero_of_lt_order B k v hk

theorem nonnegative_modes_bounded (o : Fin 12) (i : Fin (BasisSize o))
    (v : Carrier o) :
    ∃ N : ℕ, ∀ a ≥ N, halfMode o i (a : ℤ) v = 0 := by
  obtain ⟨b, hb⟩ := tensorHalfFieldCoefficient_bounded_pole o i v
  refine ⟨(-b).toNat + 1, ?_⟩
  intro a ha
  have hk : ramifiedExponent (a : ℤ) < b := by
    unfold ramifiedExponent
    omega
  rw [← tensorHalfFieldCoefficient_mode]
  exact hb _ hk

def creationTerm (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (Carrier o) :=
  (halfMode o i (Int.negSucc a)).comp (HVertexOperator.coeff B (k-2*a+1))

def annihilationTerm (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (Carrier o) :=
  (HVertexOperator.coeff B (k+2*a+3)).comp (halfMode o i (a : ℤ))

theorem creationTerm_eq_field_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i B k a =
      (HVertexOperator.coeff (twistedHalfHeisenbergField o i) (2*(a:ℤ)-1)).comp
        (HVertexOperator.coeff B (k-(2*(a:ℤ)-1))) := by
  have he : 2*(a:ℤ)-1 = ramifiedExponent (Int.negSucc a) := by
    simp only [ramifiedExponent, Int.negSucc_eq]
    omega
  have hk : k-2*(a:ℤ)+1 = k-(2*(a:ℤ)-1) := by omega
  unfold creationTerm
  rw [hk, he, twistedHalfHeisenbergField_mode]

theorem annihilationTerm_eq_field_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i B k a =
      (HVertexOperator.coeff B (k-(-2*(a:ℤ)-3))).comp
        (HVertexOperator.coeff (twistedHalfHeisenbergField o i) (-2*(a:ℤ)-3)) := by
  change annihilationTerm o i B k a =
    (HVertexOperator.coeff B (k-(-2*(a:ℤ)-3))).comp
      (HVertexOperator.coeff (twistedHalfHeisenbergField o i) (ramifiedExponent (a:ℤ)))
  rw [twistedHalfHeisenbergField_mode]
  unfold annihilationTerm
  congr 2
  omega

theorem creationTerm_finite (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    (Function.support (fun a => creationTerm o i B k a v)).Finite := by
  obtain ⟨b, hb⟩ := field_has_bound o B v
  apply finite_support_of_bound _ ((k-b+1).toNat+1)
  intro a ha
  have hk : k-2*(a:ℤ)+1 < b := by omega
  simp only [creationTerm, LinearMap.comp_apply, hb _ hk, map_zero]

theorem annihilationTerm_finite (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    (Function.support (fun a => annihilationTerm o i B k a v)).Finite := by
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o i v
  apply finite_support_of_bound _ N
  intro a ha
  simp only [annihilationTerm, LinearMap.comp_apply, hN a ha, map_zero]

def normalCoefficient (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) : Module.End ℂ (Carrier o) :=
  locallyFiniteSum (creationTerm o i B k) (creationTerm_finite o i B k) +
  locallyFiniteSum (annihilationTerm o i B k) (annihilationTerm_finite o i B k)

theorem normalCoefficient_apply (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    normalCoefficient o i B k v =
      (∑ᶠ a, creationTerm o i B k a v) +
      ∑ᶠ a, annihilationTerm o i B k a v := rfl

theorem normalCoefficient_bounded (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, normalCoefficient o i B k v = 0 := by
  classical
  obtain ⟨b, hb⟩ := field_has_bound o B v
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o i v
  have hfinite : ∀ a : Fin N, ∃ c : ℤ, ∀ k < c,
      HVertexOperator.coeff B k (halfMode o i (a : ℕ) v) = 0 :=
    fun _ => field_has_bound o B _
  choose c hc using hfinite
  let d : ℤ := min (b-1) (-(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
    (fun a => (-(c a - 2*(a : ℕ) - 3)).toNat))))
  refine ⟨d, ?_⟩
  intro k hk
  have hkb : k < b-1 := lt_of_lt_of_le hk (min_le_left _ _)
  rw [normalCoefficient_apply]
  have hfirst : (∑ᶠ a, creationTerm o i B k a v) = 0 := by
    have hz : ∀ a, creationTerm o i B k a v = 0 := by
      intro a
      simp only [creationTerm, LinearMap.comp_apply,
        hb (k-2*a+1) (by omega), map_zero]
    simp only [hz, finsum_zero]
  have hsecond : (∑ᶠ a, annihilationTerm o i B k a v) = 0 := by
    have hz : ∀ a, annihilationTerm o i B k a v = 0 := by
      intro a
      by_cases ha : a < N
      · let a' : Fin N := ⟨a,ha⟩
        have hsup : (-(c a' - 2*(a : ℤ) - 3)).toNat ≤
            (Finset.univ : Finset (Fin N)).sup
              (fun q => (-(c q - 2*(q : ℕ) - 3)).toNat) :=
          Finset.le_sup (f := fun q : Fin N => (-(c q - 2*(q : ℕ) - 3)).toNat)
            (Finset.mem_univ a')
        have hkd : k < -(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
            (fun q => (-(c q - 2*(q : ℕ) - 3)).toNat))) :=
          lt_of_lt_of_le hk (min_le_right (b-1) _)
        simp only [Int.ofNat_eq_coe] at hkd
        have hlow : k+2*(a : ℤ)+3 < c a' := by omega
        have hzero : HVertexOperator.coeff B (k+2*(a : ℤ)+3)
            (halfMode o i (a : ℤ) v) = 0 := hc a' _ hlow
        simp only [annihilationTerm, LinearMap.comp_apply, hzero]
      · simp only [annihilationTerm, LinearMap.comp_apply,
          hN a (by omega), map_zero]
    simp only [hz, finsum_zero]
  rw [hfirst, hsecond, add_zero]

def normalField (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) : VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (normalCoefficient o i B) (normalCoefficient_bounded o i B)

theorem normalField_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) :
    HVertexOperator.coeff (normalField o i B) k = normalCoefficient o i B k := rfl

end HMT.IV.LatticeTwistedNormalProduct
end

#print axioms HMT.IV.LatticeTwistedNormalProduct.field_has_bound
#print axioms HMT.IV.LatticeTwistedNormalProduct.nonnegative_modes_bounded
#print axioms HMT.IV.LatticeTwistedNormalProduct.creationTerm
#print axioms HMT.IV.LatticeTwistedNormalProduct.annihilationTerm
#print axioms HMT.IV.LatticeTwistedNormalProduct.creationTerm_eq_field_coefficient
#print axioms HMT.IV.LatticeTwistedNormalProduct.annihilationTerm_eq_field_coefficient
#print axioms HMT.IV.LatticeTwistedNormalProduct.creationTerm_finite
#print axioms HMT.IV.LatticeTwistedNormalProduct.annihilationTerm_finite
#print axioms HMT.IV.LatticeTwistedNormalProduct.normalCoefficient
#print axioms HMT.IV.LatticeTwistedNormalProduct.normalCoefficient_apply
#print axioms HMT.IV.LatticeTwistedNormalProduct.normalCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedNormalProduct.normalField
#print axioms HMT.IV.LatticeTwistedNormalProduct.normalField_coefficient
