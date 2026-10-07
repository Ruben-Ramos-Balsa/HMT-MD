import LatticeHeisenbergField
import Mathlib.Algebra.BigOperators.Finprod

/-!
Normal ordered Heisenberg descendants on the existing marked-lattice carrier.
The operator is the divided derivative : (∂^n h_i / n!) B :.
Both sums are proved locally finite. No vacuum, locality, Jacobi or FLM
identity is assumed in order to construct this genuine Laurent field.
Source: Article I, sections/excepcional.tex, construction M(1) ⊗ Cε[Λ].
-/

noncomputable section
namespace HMT.IV.LatticeNormalOrderedField

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeFieldTruncation
open scoped BigOperators

private theorem finite_support_of_bound {V : Type*} [Zero V]
    (f : ℕ → V) (N : ℕ) (h : ∀ a ≥ N, f a = 0) :
    (Function.support f).Finite := by
  apply (Finset.range N).finite_toSet.subset
  intro a ha
  simp only [Finset.mem_coe, Finset.mem_range]
  by_contra hn
  exact ha (h a (by omega))

/-- Sum of endomorphisms whose values, not necessarily the operators,
have finite support. This distinction retains every frequency. -/
def locallyFiniteSum {V : Type*} [AddCommGroup V] [Module ℂ V]
    (f : ℕ → Module.End ℂ V)
    (hf : ∀ v, (Function.support (fun a => f a v)).Finite) : Module.End ℂ V where
  toFun v := ∑ᶠ a, f a v
  map_add' v w := by
    simp only [map_add]
    exact finsum_add_distrib (hf v) (hf w)
  map_smul' c v := by
    simp only [map_smul]
    exact (smul_finsum c (fun a => f a v)).symm

def creationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (LatticeCarrier o) :=
  (Nat.choose (a+n) n : ℂ) •
    (onCarrier o (create o (a+n) i)).comp (HVertexOperator.coeff B (k-a))

def annihilationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (LatticeCarrier o) :=
  ((-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ)) •
    (HVertexOperator.coeff B (k+a+n+1)).comp (hmode o i (a : ℤ))

theorem field_has_bound (o : Fin 12) (B : VertexOperator ℂ (LatticeCarrier o))
    (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff B k v = 0 := by
  refine ⟨HahnSeries.order ((HahnModule.of ℂ).symm (B v)), ?_⟩
  intro k hk
  exact VertexOperator.coeff_eq_zero_of_lt_order B k v hk

theorem nonnegative_modes_bounded (o : Fin 12) (v : LatticeCarrier o) :
    ∃ N : ℕ, ∀ a ≥ N, ∀ i : Fin (BasisSize o), hmode o i (a : ℤ) v = 0 := by
  obtain ⟨N, hN⟩ := exists_carrier_annihilation_bound o v
  refine ⟨N+1, ?_⟩
  intro a ha i
  cases a with
  | zero => omega
  | succ a =>
    rw [hmode_castSucc]
    exact hN a (by omega) i

theorem creationTerm_finite (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    (Function.support (fun a => creationTerm o i n B k a v)).Finite := by
  obtain ⟨b, hb⟩ := field_has_bound o B v
  apply finite_support_of_bound _ ((k-b).toNat+1)
  intro a ha
  have hk : k-(a : ℤ) < b := by omega
  simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    hb _ hk, map_zero, smul_zero]

theorem annihilationTerm_finite (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    (Function.support (fun a => annihilationTerm o i n B k a v)).Finite := by
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o v
  apply finite_support_of_bound _ N
  intro a ha
  simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    hN a ha i, map_zero, smul_zero]

def normalCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  locallyFiniteSum (creationTerm o i n B k) (creationTerm_finite o i n B k) +
  locallyFiniteSum (annihilationTerm o i n B k) (annihilationTerm_finite o i n B k)

theorem normalCoefficient_apply (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) (v : LatticeCarrier o) :
    normalCoefficient o i n B k v =
      (∑ᶠ a, creationTerm o i n B k a v) +
      ∑ᶠ a, annihilationTerm o i n B k a v := rfl

/-- A single lower Laurent bound controls all terms of the normal product.
Only finitely many nonnegative modes of the input state can contribute. -/
theorem normalCoefficient_bounded (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (v : LatticeCarrier o) :
    ∃ b : ℤ, ∀ k < b, normalCoefficient o i n B k v = 0 := by
  classical
  obtain ⟨b, hb⟩ := field_has_bound o B v
  obtain ⟨N, hN⟩ := nonnegative_modes_bounded o v
  have hfinite : ∀ a : Fin N, ∃ c : ℤ, ∀ k < c,
      HVertexOperator.coeff B k (hmode o i (a : ℕ) v) = 0 :=
    fun a => field_has_bound o B _
  choose c hc using hfinite
  -- Use a minimum with an explicit default so the empty-mode case is included.
  let d : ℤ := min b (-(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
    (fun a => (-(c a - (a : ℕ) - n - 1)).toNat))))
  refine ⟨d, ?_⟩
  intro k hk
  have hkb : k < b := lt_of_lt_of_le hk (min_le_left _ _)
  rw [normalCoefficient_apply]
  have hfirst : (∑ᶠ a, creationTerm o i n B k a v) = 0 := by
    have hz : ∀ a, creationTerm o i n B k a v = 0 := by
      intro a
      simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
        hb (k-a) (by omega), map_zero, smul_zero]
    simp only [hz, finsum_zero]
  have hsecond : (∑ᶠ a, annihilationTerm o i n B k a v) = 0 := by
    have hz : ∀ a, annihilationTerm o i n B k a v = 0 := by
      intro a
      by_cases ha : a < N
      · let a' : Fin N := ⟨a,ha⟩
        have hsup : (-(c a' - (a : ℤ) - n - 1)).toNat ≤
            (Finset.univ : Finset (Fin N)).sup
              (fun q => (-(c q - (q : ℕ) - n - 1)).toNat) :=
          Finset.le_sup (f := fun q : Fin N => (-(c q - (q : ℕ) - n - 1)).toNat)
            (Finset.mem_univ a')
        have hkd : k < -(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
            (fun q => (-(c q - (q : ℕ) - n - 1)).toNat))) :=
          lt_of_lt_of_le hk (min_le_right b _)
        simp only [Int.ofNat_eq_coe] at hkd
        have hlow : k+(a : ℤ)+n+1 < c a' := by omega
        have hzero : HVertexOperator.coeff B (k+(a : ℤ)+n+1)
            (hmode o i (a : ℤ) v) = 0 := hc a' _ hlow
        simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
          hzero, smul_zero]
      · simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
          hN a (by omega) i, map_zero, smul_zero]
    simp only [hz, finsum_zero]
  rw [hfirst, hsecond, add_zero]

def normalField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) : VertexOperator ℂ (LatticeCarrier o) :=
  VertexOperator.of_coeff (normalCoefficient o i n B) (normalCoefficient_bounded o i n B)

theorem normalField_coefficient (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ) :
    HVertexOperator.coeff (normalField o i n B) k = normalCoefficient o i n B k := rfl

end HMT.IV.LatticeNormalOrderedField
end

#print axioms HMT.IV.LatticeNormalOrderedField.creationTerm_finite
#print axioms HMT.IV.LatticeNormalOrderedField.annihilationTerm_finite
#print axioms HMT.IV.LatticeNormalOrderedField.normalCoefficient_bounded
#print axioms HMT.IV.LatticeNormalOrderedField.normalField_coefficient
