import LatticeTranslationCommutators
import LatticePositiveMixedFields
import LatticeHeisenbergField

/-!
Translation covariance of every integral Heisenberg mode, for the actual
translation operator (oscillator derivation plus incoming lattice charge).
The crossing from mode one to mode zero is inherited from the proved
charge commutator; it is not inferred from an oscillator-only formula.
-/

noncomputable section
set_option maxHeartbeats 1000000
namespace HMT.IV.LatticeHeisenbergTranslation

open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeTranslationCommutators LatticePositiveMixedFields

local notation "T" => LatticeTranslationOperator.translation

theorem translation_create (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    (T o).comp (onCarrier o (create o n i)) -
      (onCarrier o (create o n i)).comp (T o) =
      (n+1 : ℂ) • onCarrier o (create o (n+1) i) := by
  simpa only [chargeCreation_basis] using translation_chargeCreate o (latticeBasis o i) n

theorem translation_annihilate_succ (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    (T o).comp (onCarrier o (annihilate o (n+1) i)) -
      (onCarrier o (annihilate o (n+1) i)).comp (T o) =
      (-(n+2 : ℂ)) • onCarrier o (annihilate o n i) := by
  simpa only [chargeAnnihilation_basis] using
    translation_chargeAnnihilate_succ o (latticeBasis o i) n

theorem translation_annihilate_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    (T o).comp (onCarrier o (annihilate o 0 i)) -
      (onCarrier o (annihilate o 0 i)).comp (T o) = -hmode o i 0 := by
  simpa only [chargeAnnihilation_basis, hmode_zero] using
    translation_chargeAnnihilate_zero o (latticeBasis o i)

/-- `[T,h_m]=-m h_(m-1)` for every integer, including the zero mode and
the frequency-one-to-charge transition. -/
theorem translation_hmode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ) :
    (T o).comp (hmode o i m) - (hmode o i m).comp (T o) =
      (-(m : ℂ)) • hmode o i (m-1) := by
  cases m with
  | ofNat n =>
    change (T o).comp (hmode o i (n : ℤ)) - (hmode o i (n : ℤ)).comp (T o) =
      (-(n : ℂ)) • hmode o i ((n : ℤ)-1)
    cases n with
    | zero =>
      simp only [Nat.cast_zero, neg_zero, zero_smul, hmode_zero]
      exact sub_eq_zero.mpr (translation_zeroMode o (latticeBasis o i))
    | succ n =>
      cases n with
      | zero =>
        simp only [Nat.cast_add, Nat.cast_zero, Nat.cast_one, zero_add, sub_self]
        rw [show hmode o i (1 : ℤ) = onCarrier o (annihilate o 0 i) from hmode_natSucc o i 0]
        apply LinearMap.ext
        intro v
        have h := LinearMap.congr_fun (translation_annihilate_zero o i) v
        simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.neg_apply] at h
        simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply]
        rw [h]
        norm_num
      | succ n =>
        have he : ((n+1+1 : ℕ) : ℤ)-1 = ((n+1 : ℕ) : ℤ) := by omega
        rw [he, hmode_castSucc, hmode_castSucc]
        convert translation_annihilate_succ o i n using 1
        push_cast
        ring
  | negSucc n =>
    have he : Int.negSucc n - 1 = Int.negSucc (n+1) := by omega
    rw [he, hmode_negSucc, hmode_negSucc]
    convert translation_create o i n using 1
    push_cast
    ring

/-- Exponent-index form of differential covariance for the actual
Heisenberg field: `[T,H_k]=(k+1) H_(k+1)`. -/
theorem translation_heisenberg_coefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    (T o).comp (HVertexOperator.coeff (LatticeHeisenbergField.heisenbergField o i) k) -
      (HVertexOperator.coeff (LatticeHeisenbergField.heisenbergField o i) k).comp (T o) =
      ((k : ℂ)+1) •
        HVertexOperator.coeff (LatticeHeisenbergField.heisenbergField o i) (k+1) := by
  change (T o).comp (hmode o i (-k-1)) - (hmode o i (-k-1)).comp (T o) =
    ((k : ℂ)+1) • hmode o i (-(k+1)-1)
  have h := translation_hmode o i (-k-1)
  rw [show -k-1-1 = -(k+1)-1 by omega] at h
  convert h using 1
  push_cast
  ring

end HMT.IV.LatticeHeisenbergTranslation
end

#print axioms HMT.IV.LatticeHeisenbergTranslation.translation_create
#print axioms HMT.IV.LatticeHeisenbergTranslation.translation_annihilate_succ
#print axioms HMT.IV.LatticeHeisenbergTranslation.translation_annihilate_zero
#print axioms HMT.IV.LatticeHeisenbergTranslation.translation_hmode
#print axioms HMT.IV.LatticeHeisenbergTranslation.translation_heisenberg_coefficient
