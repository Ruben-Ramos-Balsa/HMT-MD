import LatticeChargedVertexField
import LatticeParityCarrier

/-!
The order-two parity operator on the constructed carrier intertwines the
actual charged fields, not only their graded dimensions. The sign cocycle
and the integral pairing are the same as in the marked lattice construction.
-/

noncomputable section
namespace HMT.IV.LatticeChargedFieldParity

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeParityCarrier
open HMT.IV.LatticeFockMonomialParity HMT.FockTransport.Symmetric
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeChargedVertexField
open PowerSeries
open scoped TensorProduct BigOperators

theorem chargeCreationState_neg (o : Fin 12) (x : Lattice o) (n : ℕ) :
    chargeCreationState o (-x) n = -chargeCreationState o x n := by
  simp only [chargeCreationState, chargeModeVector, map_neg, Finsupp.neg_apply, Int.cast_neg,
    neg_smul, Finset.sum_neg_distrib]

theorem theta_creationPotential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    fockTheta o (coeff (Fock o) d (creationPotential o x)) =
      coeff (Fock o) d (creationPotential o (-x)) := by
  cases d with
  | zero => simp [coeff_zero_eq_constantCoeff_apply, creationPotential_constant]
  | succ n =>
    rw [creationPotential_coefficient_succ, creationPotential_coefficient_succ,
      map_smul, chargeCreationState_neg]
    simp only [chargeCreationState, fockTheta_generator]

theorem theta_creationPotential_series (o : Fin 12) (x : Lattice o) :
    PowerSeries.map (fockTheta o).toRingHom (creationPotential o x) =
      creationPotential o (-x) := by
  ext d
  exact theta_creationPotential_coefficient o x d

theorem theta_creationExponential_coefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    fockTheta o (coeff (Fock o) d (creationExponential o x)) =
      coeff (Fock o) d (creationExponential o (-x)) := by
  rw [creationExponential_coefficient, creationExponential_coefficient,
    map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [map_smul]
  congr 1
  change (fockTheta o).toRingHom (coeff (Fock o) d (creationPotential o x ^ k)) = _
  rw [← coeff_map, map_pow, theta_creationPotential_series]

theorem theta_creationMode (o : Fin 12) (x : Lattice o) (d : ℕ) (v : Fock o) :
    fockTheta o (creationExponentialMode o x d v) =
      creationExponentialMode o (-x) d (fockTheta o v) := by
  change fockTheta o (coeff (Fock o) d (creationExponential o x) * v) = _
  rw [map_mul, theta_creationExponential_coefficient]
  rfl

theorem theta_annihilate (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) (v : Fock o) :
    fockTheta o (annihilate o n i v) = -annihilate o n i (fockTheta o v) := by
  change fockTheta o (annihilation (modeCovector o n i) v) =
    -annihilation (modeCovector o n i) (fockTheta o v)
  induction v using SymmetricAlgebra.induction with
  | algebraMap r => simp
  | ι h => simp
  | mul a b ha hb =>
    simp only [annihilation_product, map_add, map_mul, ha, hb]
    ring
  | add a b ha hb =>
    simp only [map_add, ha, hb]
    abel

theorem theta_chargeAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ) (v : Fock o) :
    fockTheta o (chargeAnnihilation o x n v) =
      chargeAnnihilation o (-x) n (fockTheta o v) := by
  rw [chargeAnnihilation_apply, chargeAnnihilation_apply, map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_smul, theta_annihilate]
  simp only [map_neg, Finsupp.neg_apply, Int.cast_neg, neg_smul, smul_neg]

theorem theta_annihilationPotential_coefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) (v : Fock o) :
    fockTheta o (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x) v) =
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o (-x)) (fockTheta o v) := by
  cases d with
  | zero => simp [annihilationPotential_constant]
  | succ n =>
    rw [annihilationPotential_coefficient_succ,
      annihilationPotential_coefficient_succ, LinearMap.smul_apply,
      LinearMap.smul_apply, map_smul, theta_chargeAnnihilation]

theorem theta_annihilationPotential_power (o : Fin 12) (x : Lattice o)
    (k d : ℕ) (v : Fock o) :
    fockTheta o (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k) v) =
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o (-x) ^ k) (fockTheta o v) := by
  induction k generalizing d v with
  | zero =>
    by_cases hd : d = 0 <;> simp [coeff_one, hd]
  | succ k ih =>
    rw [pow_succ, pow_succ, coeff_mul, coeff_mul,
      LinearMap.sum_apply, LinearMap.sum_apply, map_sum]
    apply Finset.sum_congr rfl
    intro p _
    change fockTheta o ((coeff (Module.End ℂ (Fock o)) p.1 (annihilationPotential o x ^ k))
      ((coeff (Module.End ℂ (Fock o)) p.2 (annihilationPotential o x)) v)) = _
    rw [ih, theta_annihilationPotential_coefficient]
    rfl

theorem theta_annihilationCoefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) (v : Fock o) :
    fockTheta o (exponentialCoefficient o x d v) =
      exponentialCoefficient o (-x) d (fockTheta o v) := by
  rw [exponentialCoefficient, exponentialCoefficient,
    LinearMap.sum_apply, LinearMap.sum_apply, map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [LinearMap.smul_apply, LinearMap.smul_apply, map_smul,
    theta_annihilationPotential_power]

theorem theta_basisCoefficient (o : Fin 12) (x y : Lattice o)
    (a : Occupation o) (k : ℤ) :
    carrierTheta o (basisCoefficient o x k a y) =
      (-1 : ℂ) ^ occupationLength o a • basisCoefficient o (-x) k a (-y) := by
  unfold basisCoefficient basisCoefficientCutoff
  rw [map_smul, map_sum]
  rw [WittNegationLift.epsilon_neg_neg, HMT.IV.LatticeWeightShells.integerPair_neg_neg]
  conv_rhs => rw [smul_comm]
  congr 1
  rw [Finset.smul_sum]
  apply Finset.sum_congr rfl
  intro j _
  split_ifs
  · rw [carrierTheta_pure, theta_creationMode, theta_annihilationCoefficient,
      fockTheta_monomial, map_smul, map_smul, WittNegationLift.theta_basis,
      TensorProduct.smul_tmul']
    congr 2
    abel
  · simp

theorem theta_fieldCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (carrierTheta o).comp (fieldCoefficient o x k) =
      (fieldCoefficient o (-x) k).comp (carrierTheta o) := by
  apply (carrierBasis o).ext
  rintro ⟨a,y⟩
  change carrierTheta o (fieldCoefficient o x k (carrierBasis o (a,y))) =
    fieldCoefficient o (-x) k (carrierTheta o (carrierBasis o (a,y)))
  rw [fieldCoefficient_basis, theta_basisCoefficient, carrierTheta_basis,
    map_smul, fieldCoefficient_basis]

theorem theta_conjugates_field (o : Fin 12) (x : Lattice o) (k : ℤ)
    (v : LatticeCarrier o) :
    carrierTheta o (fieldCoefficient o x k (carrierTheta o v)) =
      fieldCoefficient o (-x) k v := by
  have h := LinearMap.congr_fun (theta_fieldCoefficient o x k) (carrierTheta o v)
  simpa only [LinearMap.comp_apply, carrierTheta_square] using h

theorem symmetric_field_preserves_fixed (o : Fin 12) (x : Lattice o) (k : ℤ)
    (v : LatticeCarrier o) (hv : carrierTheta o v = v) :
    carrierTheta o (fieldCoefficient o x k v + fieldCoefficient o (-x) k v) =
      fieldCoefficient o x k v + fieldCoefficient o (-x) k v := by
  have hx := LinearMap.congr_fun (theta_fieldCoefficient o x k) v
  have hn := LinearMap.congr_fun (theta_fieldCoefficient o (-x) k) v
  simp only [LinearMap.comp_apply, hv, neg_neg] at hx hn
  rw [map_add, hx, hn, add_comm]

theorem antisymmetric_field_changes_parity (o : Fin 12) (x : Lattice o) (k : ℤ)
    (v : LatticeCarrier o) (hv : carrierTheta o v = v) :
    carrierTheta o (fieldCoefficient o x k v - fieldCoefficient o (-x) k v) =
      -(fieldCoefficient o x k v - fieldCoefficient o (-x) k v) := by
  have hx := LinearMap.congr_fun (theta_fieldCoefficient o x k) v
  have hn := LinearMap.congr_fun (theta_fieldCoefficient o (-x) k) v
  simp only [LinearMap.comp_apply, hv, neg_neg] at hx hn
  rw [map_sub, hx, hn]
  abel

end HMT.IV.LatticeChargedFieldParity
end

#print axioms HMT.IV.LatticeChargedFieldParity.chargeCreationState_neg
#print axioms HMT.IV.LatticeChargedFieldParity.theta_creationExponential_coefficient
#print axioms HMT.IV.LatticeChargedFieldParity.theta_creationMode
#print axioms HMT.IV.LatticeChargedFieldParity.theta_annihilate
#print axioms HMT.IV.LatticeChargedFieldParity.theta_chargeAnnihilation
#print axioms HMT.IV.LatticeChargedFieldParity.theta_annihilationCoefficient
#print axioms HMT.IV.LatticeChargedFieldParity.theta_basisCoefficient
#print axioms HMT.IV.LatticeChargedFieldParity.theta_fieldCoefficient
#print axioms HMT.IV.LatticeChargedFieldParity.theta_conjugates_field
#print axioms HMT.IV.LatticeChargedFieldParity.symmetric_field_preserves_fixed
#print axioms HMT.IV.LatticeChargedFieldParity.antisymmetric_field_changes_parity
