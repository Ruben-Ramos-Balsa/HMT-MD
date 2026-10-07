import LatticeOscillatorFock

/-!
# Integral-index Heisenberg modes on the generated lattice carrier

This gathers creation, annihilation and lattice zero modes into one integer
indexed family. The commutator is derived from the oscillator CCR and the
commuting tensor factors; no commutation law is added as an assumption.
The lattice Gram coefficients retain their marked-neighbor origin.
-/

noncomputable section
namespace HMT.IV.LatticeHeisenbergModes

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeOscillatorFock
open scoped TensorProduct

def hmode (o : Fin 12) (i : Fin (BasisSize o)) (n : ℤ) :
    Module.End ℂ (LatticeCarrier o) :=
  if n < 0 then onCarrier o (create o ((-n-1).toNat) i)
  else if n = 0 then onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o i))
  else onCarrier o (annihilate o ((n-1).toNat) i)

@[simp] theorem hmode_zero (o : Fin 12) (i : Fin (BasisSize o)) :
    hmode o i 0 = onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o i)) := by
  simp [hmode]

@[simp] theorem hmode_natSucc (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    hmode o i (Int.ofNat (n+1)) = onCarrier o (annihilate o n i) := by
  have hlt : ¬ (Int.ofNat (n+1) < 0) := by
    simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
  have hne : Int.ofNat (n+1) ≠ 0 := by
    simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
  have heq : (Int.ofNat (n+1) - 1).toNat = n := by
    simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
  simp only [hmode, if_neg hlt, if_neg hne, heq]

@[simp] theorem hmode_castSucc (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    hmode o i ((n+1 : ℕ) : ℤ) = onCarrier o (annihilate o n i) := by
  simpa only [Int.ofNat_eq_coe] using hmode_natSucc o i n

@[simp] theorem hmode_negSucc (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    hmode o i (Int.negSucc n) = onCarrier o (create o n i) := by
  have hlt : Int.negSucc n < 0 := by omega
  have heq : (-Int.negSucc n - 1).toNat = n := by omega
  simp only [hmode, if_pos hlt, heq]

theorem carrier_creations_commute (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : LatticeCarrier o) :
    onCarrier o (create o n i) (onCarrier o (create o m j) v) =
      onCarrier o (create o m j) (onCarrier o (create o n i) v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a => simp only [onCarrier_pure, creations_commute_all_modes]
  | add x y hx hy => simp only [map_add]; rw [hx, hy]

theorem carrier_annihilations_commute (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : LatticeCarrier o) :
    onCarrier o (annihilate o n i) (onCarrier o (annihilate o m j) v) =
      onCarrier o (annihilate o m j) (onCarrier o (annihilate o n i) v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a => simp only [onCarrier_pure, annihilations_commute_all_modes]
  | add x y hx hy => simp only [map_add]; rw [hx, hy]

theorem carrier_zeroModes_commute (o : Fin 12) (i j : Fin (BasisSize o))
    (v : LatticeCarrier o) :
    onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o i))
      (onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o j)) v) =
    onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o j))
      (onLattice o (LatticeZeroModes.zeroMode o (latticeBasis o i)) v) := by
  have h := LatticeZeroModes.zeroModes_commute o (latticeBasis o i) (latticeBasis o j)
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [onLattice_pure]
    have ha := LinearMap.congr_fun h a
    simp only [LinearMap.comp_apply] at ha
    rw [ha]
  | add x y hx hy => simp only [map_add]; rw [hx, hy]

set_option maxHeartbeats 800000 in
theorem heisenberg_relation_apply (o : Fin 12) (i j : Fin (BasisSize o))
    (m n : ℤ) (v : LatticeCarrier o) :
    hmode o i m (hmode o j n v) - hmode o j n (hmode o i m v) =
      (if m+n=0 then (m : ℂ) * gram o i j else 0) • v := by
  cases m with
  | ofNat a =>
    cases a with
    | zero =>
      cases n with
      | ofNat b =>
        cases b with
        | zero =>
          simp only [Int.ofNat_eq_coe, Nat.cast_zero, hmode_zero]
          rw [carrier_zeroModes_commute]
          simp
        | succ b =>
          simp only [Int.ofNat_eq_coe, Nat.cast_zero, hmode_zero, hmode_castSucc]
          rw [← oscillator_lattice_commute]
          simp
      | negSucc b =>
        simp only [Int.ofNat_eq_coe, Nat.cast_zero, hmode_zero, hmode_negSucc]
        rw [← oscillator_lattice_commute]
        simp
    | succ a =>
      cases n with
      | ofNat b =>
        cases b with
        | zero =>
          simp only [Int.ofNat_eq_coe, Nat.cast_zero, hmode_zero, hmode_castSucc]
          rw [oscillator_lattice_commute]
          simp
          intro h
          omega
        | succ b =>
          have hne : Int.ofNat (a+1) + Int.ofNat (b+1) ≠ 0 := by
            simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
          simp only [hmode_natSucc, if_neg hne]
          rw [carrier_annihilations_commute]
          simp
      | negSucc b =>
        simp only [hmode_natSucc, hmode_negSucc]
        rw [carrier_mode_ccr]
        have heq : Int.ofNat (a+1) + Int.negSucc b = 0 ↔ a=b := by
          simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
        simp only [heq]
        split_ifs <;> simp
  | negSucc a =>
    cases n with
    | ofNat b =>
      cases b with
      | zero =>
        simp only [Int.ofNat_eq_coe, Nat.cast_zero, hmode_negSucc, hmode_zero]
        rw [oscillator_lattice_commute]
        simp
      | succ b =>
        simp only [hmode_negSucc, hmode_natSucc]
        have h := carrier_mode_ccr o b a j i v
        have heq : Int.negSucc a + Int.ofNat (b+1) = 0 ↔ b=a := by
          simp only [Int.ofNat_eq_coe, Nat.cast_add, Nat.cast_one]; omega
        simp only [heq]
        rw [← neg_sub, h]
        by_cases hab : b=a
        · subst b
          simp only [if_pos rfl, gram_symmetric o j i]
          rw [← neg_smul]
          congr 1
          simp
          ring
        · simp [hab]
    | negSucc b =>
      have hne : Int.negSucc a + Int.negSucc b ≠ 0 := by omega
      simp only [hmode_negSucc, if_neg hne]
      rw [carrier_creations_commute]
      simp

theorem heisenberg_relation (o : Fin 12) (i j : Fin (BasisSize o)) (m n : ℤ) :
    (hmode o i m).comp (hmode o j n) - (hmode o j n).comp (hmode o i m) =
      (if m+n=0 then (m : ℂ) * gram o i j else 0) •
        (LinearMap.id : Module.End ℂ (LatticeCarrier o)) := by
  apply LinearMap.ext
  intro v
  exact heisenberg_relation_apply o i j m n v

end HMT.IV.LatticeHeisenbergModes
end

#print axioms HMT.IV.LatticeHeisenbergModes.hmode_zero
#print axioms HMT.IV.LatticeHeisenbergModes.hmode_natSucc
#print axioms HMT.IV.LatticeHeisenbergModes.hmode_castSucc
#print axioms HMT.IV.LatticeHeisenbergModes.hmode_negSucc
#print axioms HMT.IV.LatticeHeisenbergModes.carrier_creations_commute
#print axioms HMT.IV.LatticeHeisenbergModes.carrier_annihilations_commute
#print axioms HMT.IV.LatticeHeisenbergModes.carrier_zeroModes_commute
#print axioms HMT.IV.LatticeHeisenbergModes.heisenberg_relation_apply
#print axioms HMT.IV.LatticeHeisenbergModes.heisenberg_relation
