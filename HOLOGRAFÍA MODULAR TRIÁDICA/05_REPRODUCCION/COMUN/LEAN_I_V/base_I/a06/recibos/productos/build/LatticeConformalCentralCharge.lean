import LatticeConformalCentralizer
import LatticeFieldGeneration

/-! The central scalar is calculated on every charged ground state from the
actual finite normal-product sums and CCR. Its extension to the carrier uses
the already proved Heisenberg centralizer, not a Virasoro or VOA Jacobi axiom. -/

noncomputable section
namespace HMT.IV.LatticeConformalCentralCharge
open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeHeisenbergField LatticeNormalOrderedField LatticeConformalState
open LatticeConformalCoefficient LatticeConformalHeisenberg
open LatticeConformalCentralizer LatticeConformalEnergy LatticeGramDual
open TwistedGroupAlgebra
open scoped BigOperators TensorProduct

abbrev chargedGround (o : Fin 12) (x : Lattice o) : LatticeCarrier o :=
  (1 : Fock o) ⊗ₜ[ℂ] basisElement o x

theorem hmode_positive_ground (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℤ) (hn : 0<n) (x : Lattice o) : hmode o i n (chargedGround o x)=0 := by
  obtain ⟨a, ha⟩ : ∃ a : ℕ, n=((a+1 : ℕ):ℤ) := ⟨n.toNat-1, by omega⟩
  rw [ha, hmode_castSucc]
  simp only [chargedGround, onCarrier_pure, annihilate_vacuum, TensorProduct.zero_tmul]

theorem hmode_zero_ground (o : Fin 12) (i : Fin (BasisSize o)) (x : Lattice o) :
    hmode o i 0 (chargedGround o x) =
      (integerPair o (latticeBasis o i) x : ℂ) • chargedGround o x := by
  simp only [chargedGround, hmode_zero, onLattice_pure,
    LatticeZeroModes.zeroMode_basis, TensorProduct.tmul_smul]

theorem normal_ground (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (x : Lattice o) :
    normalCoefficient o i 0 (heisenbergField o j) (-m-2) (chargedGround o x) =
      (∑ a ∈ Finset.range (-m).toNat,
        hmode o i (-(a:ℤ)-1) (hmode o j (m+a+1) (chargedGround o x))) +
      (integerPair o (latticeBasis o i) x : ℂ) •
        hmode o j m (chargedGround o x) := by
  classical
  have hC : Function.support
      (fun a => creationTerm o i 0 (heisenbergField o j) (-m-2) a (chargedGround o x))
      ⊆ (Finset.range (-m).toNat : Set ℕ) := by
    intro a ha
    simp only [Finset.mem_coe, Finset.mem_range]
    by_contra hn
    apply ha
    change creationTerm o i 0 (heisenbergField o j) (-m-2) a (chargedGround o x)=0
    rw [creationTerm_heisenberg, LinearMap.comp_apply,
      hmode_positive_ground o j _ (by omega), map_zero]
  have hA (a : ℕ) (ha : a≠0) :
      annihilationTerm o i 0 (heisenbergField o j) (-m-2) a (chargedGround o x)=0 := by
    rw [annihilationTerm_heisenberg, LinearMap.comp_apply,
      hmode_positive_ground o i _ (by exact_mod_cast Nat.pos_of_ne_zero ha), map_zero]
  rw [normalCoefficient_apply, finsum_eq_sum_of_support_subset _ hC,
    finsum_eq_single _ 0 hA]
  simp only [creationTerm_heisenberg, annihilationTerm_heisenberg,
    LinearMap.comp_apply, Nat.cast_zero, sub_zero, hmode_zero_ground, map_smul]

theorem conformal_two_ground (o : Fin 12) (x : Lattice o) :
    conformalMode o 2 (chargedGround o x)=0 := by
  rw [conformalMode_normal_sum_apply]
  simp only [normal_ground, show (- (2:ℤ)).toNat=0 by decide,
    Finset.range_zero, Finset.sum_empty, hmode_positive_ground o _ 2 (by omega),
    smul_zero, zero_add, Finset.sum_const_zero]

theorem conformal_zero_ground (o : Fin 12) (x : Lattice o) :
    conformalMode o 0 (chargedGround o x) =
      (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j •
        ((integerPair o (latticeBasis o i) x : ℂ) •
          ((integerPair o (latticeBasis o j) x : ℂ) • chargedGround o x))) := by
  rw [conformalMode_normal_sum_apply]
  simp_rw [normal_ground o _ _ 0 x]
  simp only [neg_zero, Int.toNat_zero, Finset.range_zero,
    Finset.sum_empty, zero_add, hmode_zero_ground]

theorem conformal_neg_two_ground (o : Fin 12) (x : Lattice o) :
    conformalMode o (-2) (chargedGround o x) =
      (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j •
        (hmode o i (-1) (hmode o j (-1) (chargedGround o x)) +
          (integerPair o (latticeBasis o j) x : ℂ) • hmode o i (-2) (chargedGround o x) +
          (integerPair o (latticeBasis o i) x : ℂ) • hmode o j (-2) (chargedGround o x))) := by
  rw [conformalMode_normal_sum_apply]
  simp only [normal_ground]
  rw [show (-(-2:ℤ)).toNat=2 by rfl]
  norm_num [Finset.sum_range_succ, hmode_zero_ground, map_smul]

theorem conformal_two_single (o : Fin 12) (i : Fin (BasisSize o)) (x : Lattice o) :
    conformalMode o 2 (hmode o i (-2) (chargedGround o x)) =
      (2:ℂ) • ((integerPair o (latticeBasis o i) x : ℂ) • chargedGround o x) := by
  have h := conformalMode_heisenberg_commutator_apply o i 2 (-2) (chargedGround o x)
  simpa only [conformal_two_ground, map_zero, sub_zero, Int.reduceNeg,
    Int.cast_ofNat, Int.reduceAdd, hmode_zero_ground] using h

theorem conformal_two_double (o : Fin 12) (i j : Fin (BasisSize o)) (x : Lattice o) :
    conformalMode o 2 (hmode o i (-1) (hmode o j (-1) (chargedGround o x))) =
      gram o i j • chargedGround o x := by
  have hj := conformalMode_heisenberg_commutator_apply o j 2 (-1) (chargedGround o x)
  have hz : conformalMode o 2 (hmode o j (-1) (chargedGround o x))=0 := by
    simpa only [conformal_two_ground, map_zero, sub_zero, Int.reduceNeg,
      Int.cast_ofNat, Int.reduceAdd, one_smul,
      hmode_positive_ground o j 1 (by omega)] using hj
  have hi := conformalMode_heisenberg_commutator_apply o i 2 (-1)
    (hmode o j (-1) (chargedGround o x))
  have hc := heisenberg_relation_apply o i j 1 (-1) (chargedGround o x)
  simp only [hmode_positive_ground o i 1 (by omega), map_zero, sub_zero,
    Int.reduceAdd, if_pos rfl, Int.cast_one, one_mul] at hc
  simpa only [hz, map_zero, sub_zero, Int.reduceNeg, Int.cast_ofNat,
    Int.reduceAdd, Nat.cast_one, Int.cast_one, one_smul, hc, ite_true] using hi

theorem gram_trace (o : Fin 12) :
    (∑ i, ∑ j, gramInv o i j * gram o i j) = (BasisSize o : ℂ) := by
  have hi (i : Fin (BasisSize o)) : (∑ j, gramInv o i j * gram o i j) = 1 := by
    simp_rw [gram_symmetric o i]
    simpa only [if_pos rfl] using gramInv_pairing o i i
  simp only [hi, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, mul_one]

theorem defect_two_neg_two_ground (o : Fin 12) (x : Lattice o) :
    defect o 2 (-2) (chargedGround o x) =
      ((BasisSize o : ℂ)/2) • chargedGround o x := by
  simp only [defect, LatticeConformalCentralizer.comm, LinearMap.sub_apply, Module.End.mul_apply,
    LinearMap.smul_apply, conformal_two_ground, map_zero, sub_zero,
    Int.reduceSub, Int.reduceAdd, Int.cast_ofNat]
  rw [conformal_neg_two_ground, conformal_zero_ground]
  simp only [map_smul, map_sum, map_add, conformal_two_double, conformal_two_single]
  have hs (i j : Fin (BasisSize o)) :
      gramInv o i j •
        (gram o i j • chargedGround o x +
          (integerPair o (latticeBasis o j) x : ℂ) •
            ((2:ℂ) • ((integerPair o (latticeBasis o i) x : ℂ) • chargedGround o x)) +
          (integerPair o (latticeBasis o i) x : ℂ) •
            ((2:ℂ) • ((integerPair o (latticeBasis o j) x : ℂ) • chargedGround o x))) =
      (gramInv o i j * gram o i j) • chargedGround o x +
        (4:ℂ) • (gramInv o i j •
          ((integerPair o (latticeBasis o i) x : ℂ) •
            ((integerPair o (latticeBasis o j) x : ℂ) • chargedGround o x))) := by
    module
  simp_rw [hs]
  simp only [Finset.sum_add_distrib]
  simp only [← Finset.smul_sum, ← Finset.sum_smul]
  rw [gram_trace]
  module

theorem defect_two_neg_two (o : Fin 12) :
    defect o 2 (-2) = ((BasisSize o : ℂ)/2) • LinearMap.id := by
  let D := defect o 2 (-2)
  let c : ℂ := (BasisSize o : ℂ)/2
  let S := LinearMap.ker (D-c • LinearMap.id)
  have htop : S=⊤ := by
    apply LatticeFieldGeneration.carrier_generated_by_ground_states o
    · intro x
      exact sub_eq_zero.mpr (defect_two_neg_two_ground o x)
    · intro n i v hv
      have hv' : D v=c • v := sub_eq_zero.mp hv
      have h := LinearMap.congr_fun
        (sub_eq_zero.mp (defect_comm_heisenberg o i 2 (-2) (Int.negSucc n))) v
      simp only [Module.End.mul_apply, hmode_negSucc] at h
      change D (onCarrier o (create o n i) v) - c • onCarrier o (create o n i) v=0
      rw [show D (onCarrier o (create o n i) v) =
        onCarrier o (create o n i) (D v) from h, hv', map_smul, sub_self]
  apply LinearMap.ext
  intro v
  have hv : v ∈ S := by rw [htop]; trivial
  exact sub_eq_zero.mp hv

end HMT.IV.LatticeConformalCentralCharge
end

#print axioms HMT.IV.LatticeConformalCentralCharge.chargedGround
#print axioms HMT.IV.LatticeConformalCentralCharge.hmode_positive_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.hmode_zero_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.normal_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.conformal_two_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.conformal_zero_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.conformal_neg_two_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.conformal_two_single
#print axioms HMT.IV.LatticeConformalCentralCharge.conformal_two_double
#print axioms HMT.IV.LatticeConformalCentralCharge.gram_trace
#print axioms HMT.IV.LatticeConformalCentralCharge.defect_two_neg_two_ground
#print axioms HMT.IV.LatticeConformalCentralCharge.defect_two_neg_two
