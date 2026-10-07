import LatticeHeisenbergTranslation
import LatticeAllMixedFields
import LatticeFieldGeneration

/-!
Propagation of the actual charged-field translation defect through every
creation history. The defect is an explicit endomorphism, not a predicate
encoding covariance. Its vanishing on ground states is kept as the single
input to the final spanning lemma, for discharge by the independent
charged-ground calculation.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeTranslationDefect

open LatticeCocycle LatticeOscillatorFock LatticeChargedVertexField
open LatticePositiveMixedFields LatticeNegativeMixedFields
open LatticeHeisenbergTranslation LatticeFieldGeneration TwistedGroupAlgebra
open scoped TensorProduct

local notation "T" => LatticeTranslationOperator.translation

def defect (o : Fin 12) (x : Lattice o) (k : ℤ) : Module.End ℂ (LatticeCarrier o) :=
  T o * fieldCoefficient o x k - fieldCoefficient o x k * T o -
    ((k : ℂ)+1) • fieldCoefficient o x (k+1)

theorem field_creator_reverse (o : Fin 12) (x : Lattice o)
    (n : ℕ) (i : Fin (BasisSize o)) (k : ℤ) :
    fieldCoefficient o x k * onCarrier o (create o n i) -
      onCarrier o (create o n i) * fieldCoefficient o x k =
      (-(integerPair o (latticeBasis o i) x : ℂ)) •
        fieldCoefficient o x (k+((n+1 : ℕ) : ℤ)) := by
  have h := negative_mode_field_commutator o (latticeBasis o i) x n k
  rw [chargeCreation_basis] at h
  calc
    _ = -((integerPair o (latticeBasis o i) x : ℂ) •
        fieldCoefficient o x (k+((n+1 : ℕ) : ℤ))) := by
      simpa only [neg_sub] using congrArg Neg.neg h
    _ = _ := (neg_smul _ _).symm

/-- Exact recursion of the defect under a creator, using only the proved
translation/creator and creator/charged-field commutators. -/
theorem defect_creator_commutator (o : Fin 12) (x : Lattice o)
    (n : ℕ) (i : Fin (BasisSize o)) (k : ℤ) :
    defect o x k * onCarrier o (create o n i) -
      onCarrier o (create o n i) * defect o x k =
      (-(integerPair o (latticeBasis o i) x : ℂ)) •
        defect o x (k+((n+1 : ℕ) : ℤ)) := by
  let Y := fieldCoefficient o x
  let G := onCarrier o (create o n i)
  let G' := onCarrier o (create o (n+1) i)
  let q : ℂ := (integerPair o (latticeBasis o i) x : ℂ)
  let r : ℤ := ((n+1 : ℕ) : ℤ)
  have hT : T o * G - G * T o = (n+1 : ℂ) • G' := translation_create o i n
  have hY (t : ℤ) : Y t * G - G * Y t = (-q) • Y (t+r) :=
    field_creator_reverse o x n i t
  have hY' : Y k * G' - G' * Y k = (-q) • Y (k+r+1) := by
    have h := field_creator_reverse o x (n+1) i k
    simpa only [show k+((n+1+1 : ℕ) : ℤ) = k+r+1 by dsimp [r]; omega] using h
  change defect o x k * G - G * defect o x k = (-q) • defect o x (k+r)
  calc
    _ = T o * (Y k * G - G * Y k) - (Y k * G - G * Y k) * T o -
        (Y k * (T o * G - G * T o) - (T o * G - G * T o) * Y k) -
        ((k : ℂ)+1) • (Y (k+1) * G - G * Y (k+1)) := by
      dsimp only [defect, Y]
      simp only [sub_mul, mul_sub, mul_assoc, smul_mul_assoc, mul_smul_comm, smul_sub]
      abel
    _ = (-q) • (T o * Y (k+r) - Y (k+r) * T o) -
        (n+1 : ℂ) • (Y k * G' - G' * Y k) -
        ((k : ℂ)+1) • ((-q) • Y (k+1+r)) := by
      rw [hY k, hT, hY (k+1)]
      simp only [mul_smul_comm, smul_mul_assoc, smul_sub]
    _ = (-q) • defect o x (k+r) := by
      rw [hY', show k+1+r=k+r+1 by omega]
      dsimp only [defect, Y]
      simp only [smul_sub, smul_smul]
      dsimp only [r]
      push_cast
      module

def zeroDefectSpace (o : Fin 12) (x : Lattice o) : Submodule ℂ (LatticeCarrier o) :=
  ⨅ k : ℤ, LinearMap.ker (defect o x k)

theorem mem_zeroDefectSpace (o : Fin 12) (x : Lattice o) (v : LatticeCarrier o) :
    v ∈ zeroDefectSpace o x ↔ ∀ k : ℤ, defect o x k v = 0 := by
  simp only [zeroDefectSpace, Submodule.mem_iInf, LinearMap.mem_ker]

theorem creator_preserves_zeroDefectSpace (o : Fin 12) (x : Lattice o)
    (n : ℕ) (i : Fin (BasisSize o)) (v : LatticeCarrier o)
    (hv : v ∈ zeroDefectSpace o x) :
    onCarrier o (create o n i) v ∈ zeroDefectSpace o x := by
  rw [mem_zeroDefectSpace] at hv ⊢
  intro k
  have h := LinearMap.congr_fun (defect_creator_commutator o x n i k) v
  simp only [LinearMap.sub_apply, Module.End.mul_apply, LinearMap.smul_apply,
    hv, map_zero, smul_zero, sub_zero] at h
  exact h

/-- The independent ground-state calculation is the only remaining input
here. Arbitrary frequencies, occupations and charges are covered by the
already proved spanning theorem of the same carrier. -/
theorem defect_zero_of_ground (o : Fin 12) (x : Lattice o)
    (hground : ∀ (y : Lattice o) (k : ℤ),
      defect o x k ((1 : Fock o) ⊗ₜ[ℂ] basisElement o y) = 0) (k : ℤ) :
    defect o x k = 0 := by
  have htop : zeroDefectSpace o x = ⊤ := by
    apply carrier_generated_by_ground_states o
    · intro y
      exact (mem_zeroDefectSpace o x _).mpr (hground y)
    · exact creator_preserves_zeroDefectSpace o x
  apply LinearMap.ext
  intro v
  have hv : v ∈ zeroDefectSpace o x := by rw [htop]; trivial
  exact (mem_zeroDefectSpace o x v).mp hv k

end HMT.IV.LatticeTranslationDefect
end

#print axioms HMT.IV.LatticeTranslationDefect.field_creator_reverse
#print axioms HMT.IV.LatticeTranslationDefect.defect_creator_commutator
#print axioms HMT.IV.LatticeTranslationDefect.mem_zeroDefectSpace
#print axioms HMT.IV.LatticeTranslationDefect.creator_preserves_zeroDefectSpace
#print axioms HMT.IV.LatticeTranslationDefect.defect_zero_of_ground
