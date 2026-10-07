import LatticeCoxeterTwistedLift
import LatticeExponentialCommutator
import LatticeFieldBiOperators

/-!
The already constructed order-three lift acts on the actual charged fields.
The finite annihilation and creation coefficients are transported by the
inherited lattice isometry, pairing and cocycle. No covariance identity or
classification theorem is supplied as an assumption. This concerns the
existing Witt orientation, not a replacement of the selected marked lattice.
-/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeCoxeterFieldCovariance

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra HMT.IV.LatticeCoxeterFock
open HMT.IV.LatticeCoxeterTwistedLift HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.IV.LatticeExponentialCommutator HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeFieldCutoff HMT.IV.LatticeWeightFiltration
open HMT.IV.LatticeAnnihilationCommutativity HMT.IV.LatticeFieldBiOperators
open HMT.FockTransport.Symmetric
open PowerSeries
open scoped TensorProduct BigOperators

theorem fockAction_creationState (o : Fin 12) (x : Lattice o) (n : ℕ) :
    fockAction o (chargeCreationState o x n) =
      chargeCreationState o (latticeAction o x) n := by
  change fockAction o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeLift o n x)) = _
  rw [fockAction_generator, oscillatorAction_modeLift]
  rfl

theorem annihilation_creationState (o : Fin 12) (x y : Lattice o) (n m : ℕ) :
    chargeAnnihilation o x n (chargeCreationState o y m) =
      if n=m then ((n+1 : ℂ) * (integerPair o x y : ℂ)) • (1 : Fock o) else 0 := by
  rw [← chargedDerivation_apply, chargedDerivation_creationState,
    coordinatePair_eq_integerPair]

theorem annihilation_product (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v w : Fock o) :
    chargeAnnihilation o x n (v*w) =
      v * chargeAnnihilation o x n w + w * chargeAnnihilation o x n v := by
  simpa only [chargedDerivation_apply, smul_eq_mul] using
    (chargedDerivation o x n).leibniz v w

theorem fockAction_chargeAnnihilation (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : Fock o) :
    fockAction o (chargeAnnihilation o x n v) =
      chargeAnnihilation o (latticeAction o x) n (fockAction o v) := by
  have hgen :
      ((fockAction o).toLinearMap.comp (chargeAnnihilation o x n)).comp
          (SymmetricAlgebra.ι ℂ (Oscillators o)) =
        ((chargeAnnihilation o (latticeAction o x) n).comp
          (fockAction o).toLinearMap).comp (SymmetricAlgebra.ι ℂ (Oscillators o)) := by
    apply (oscillatorBasis o).ext
    rintro ⟨m,i⟩
    have hb : chargeCreationState o (latticeBasis o i) m =
        SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m i) := by
      change SymmetricAlgebra.ι ℂ (Oscillators o) (modeLift o m (latticeBasis o i)) = _
      rw [modeLift_basis]
    change fockAction o (chargeAnnihilation o x n
        (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m i))) =
      chargeAnnihilation o (latticeAction o x) n
        (fockAction o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o m i)))
    rw [← hb]
    rw [fockAction_creationState, annihilation_creationState,
      annihilation_creationState, latticeAction_pairing]
    split_ifs <;> simp
  induction v using SymmetricAlgebra.induction with
  | algebraMap r =>
    simp only [← chargedDerivation_apply]
    simp
  | ι f => exact LinearMap.congr_fun hgen f
  | mul v w hv hw =>
    simp only [annihilation_product, map_mul, map_add, hv, hw]
  | add v w hv hw => simp only [map_add, hv, hw]

theorem fockAction_creationPotential_coefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) :
    fockAction o (coeff (Fock o) d (creationPotential o x)) =
      coeff (Fock o) d (creationPotential o (latticeAction o x)) := by
  cases d with
  | zero => simp [coeff_zero_eq_constantCoeff_apply, creationPotential_constant]
  | succ n => rw [creationPotential_coefficient_succ,
      creationPotential_coefficient_succ, map_smul, fockAction_creationState]

theorem fockAction_creationPotential_series (o : Fin 12) (x : Lattice o) :
    PowerSeries.map (fockAction o).toRingHom (creationPotential o x) =
      creationPotential o (latticeAction o x) := by
  ext d
  exact fockAction_creationPotential_coefficient o x d

theorem fockAction_creationCoefficient (o : Fin 12) (x : Lattice o) (d : ℕ) :
    fockAction o (coeff (Fock o) d (creationExponential o x)) =
      coeff (Fock o) d (creationExponential o (latticeAction o x)) := by
  rw [creationExponential_coefficient, creationExponential_coefficient, map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [map_smul]
  congr 1
  change (fockAction o).toRingHom (coeff (Fock o) d (creationPotential o x ^ k)) = _
  rw [← coeff_map, map_pow, fockAction_creationPotential_series]

theorem fockAction_creationMode (o : Fin 12) (x : Lattice o) (d : ℕ) (v : Fock o) :
    fockAction o (creationExponentialMode o x d v) =
      creationExponentialMode o (latticeAction o x) d (fockAction o v) := by
  change fockAction o (coeff (Fock o) d (creationExponential o x) * v) = _
  rw [map_mul, fockAction_creationCoefficient]
  rfl

theorem fockAction_annihilationPotential_coefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) (v : Fock o) :
    fockAction o (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x) v) =
      coeff (Module.End ℂ (Fock o)) d (annihilationPotential o (latticeAction o x))
        (fockAction o v) := by
  cases d with
  | zero => simp [annihilationPotential_constant]
  | succ n =>
    rw [annihilationPotential_coefficient_succ,
      annihilationPotential_coefficient_succ, LinearMap.smul_apply,
      LinearMap.smul_apply, map_smul, fockAction_chargeAnnihilation]

theorem fockAction_annihilationPotential_power (o : Fin 12) (x : Lattice o)
    (k d : ℕ) (v : Fock o) :
    fockAction o (coeff (Module.End ℂ (Fock o)) d (annihilationPotential o x ^ k) v) =
      coeff (Module.End ℂ (Fock o)) d
        (annihilationPotential o (latticeAction o x) ^ k) (fockAction o v) := by
  induction k generalizing d v with
  | zero => by_cases hd : d = 0 <;> simp [coeff_one, hd]
  | succ k ih =>
    rw [pow_succ, pow_succ, coeff_mul, coeff_mul,
      LinearMap.sum_apply, LinearMap.sum_apply, map_sum]
    apply Finset.sum_congr rfl
    intro p _
    change fockAction o ((coeff (Module.End ℂ (Fock o)) p.1 (annihilationPotential o x ^ k))
      ((coeff (Module.End ℂ (Fock o)) p.2 (annihilationPotential o x)) v)) = _
    rw [ih, fockAction_annihilationPotential_coefficient]
    rfl

theorem fockAction_annihilationCoefficient (o : Fin 12) (x : Lattice o)
    (d : ℕ) (v : Fock o) :
    fockAction o (exponentialCoefficient o x d v) =
      exponentialCoefficient o (latticeAction o x) d (fockAction o v) := by
  rw [exponentialCoefficient, exponentialCoefficient,
    LinearMap.sum_apply, LinearMap.sum_apply, map_sum]
  apply Finset.sum_congr rfl
  intro k _
  rw [LinearMap.smul_apply, LinearMap.smul_apply, map_smul,
    fockAction_annihilationPotential_power]

theorem carrierEquiv_fieldCutoff (o : Fin 12) (x y : Lattice o)
    (k : ℤ) (N : ℕ) (v : Fock o) :
    carrierEquiv o (fieldCutoff o x y k N v) =
      (phase o x * phase o y) •
        fieldCutoff o (latticeAction o x) (latticeAction o y) k N (fockAction o v) := by
  have hterm (j : ℕ) :
      carrierEquiv o (if 0 ≤ k-integerPair o x y+(j : ℤ) then
        creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
          (exponentialCoefficient o x j v) ⊗ₜ[ℂ] basisElement o (x+y) else 0) =
      phase o (x+y) • (if 0 ≤ k-integerPair o (latticeAction o x) (latticeAction o y)+(j : ℤ) then
        creationExponentialMode o (latticeAction o x)
          ((k-integerPair o (latticeAction o x) (latticeAction o y)+(j : ℤ)).toNat)
          (exponentialCoefficient o (latticeAction o x) j (fockAction o v)) ⊗ₜ[ℂ]
            basisElement o (latticeAction o x+latticeAction o y) else 0) := by
    rw [latticeAction_pairing]
    split_ifs
    · rw [carrierEquiv_charge]
      change phase o (x+y) • (fockAction o
        (creationExponentialMode o x ((k-integerPair o x y+(j : ℤ)).toNat)
          (exponentialCoefficient o x j v)) ⊗ₜ[ℂ]
            basisElement o (latticeAction o (x+y))) = _
      rw [fockAction_creationMode, fockAction_annihilationCoefficient, map_add]
    · exact (map_zero (carrierEquiv o)).trans (smul_zero _).symm
  unfold fieldCutoff
  rw [map_smul, map_sum]
  simp_rw [hterm]
  rw [← Finset.smul_sum, smul_smul, smul_smul, phase_compatibility]

theorem carrierEquiv_fieldCoefficient_pure (o : Fin 12) (x y : Lattice o)
    (k : ℤ) (v : Fock o) :
    carrierEquiv o (fieldCoefficient o x k (v ⊗ₜ[ℂ] basisElement o y)) =
      phase o x • fieldCoefficient o (latticeAction o x) k
        (carrierEquiv o (v ⊗ₜ[ℂ] basisElement o y)) := by
  obtain ⟨N,hN⟩ := exists_weight_bound o v
  have hv : ∀ d, N < d → exponentialCoefficient o x d v = 0 :=
    fun d hd => annihilation_cutoff_on_filtration o x N d hd v hN
  have hG : ∀ d, N < d → exponentialCoefficient o (latticeAction o x) d
      (fockAction o v) = 0 := by
    intro d hd
    rw [← fockAction_annihilationCoefficient, hv d hd, map_zero]
  rw [fieldCoefficient_eq_of_annihilation_cutoff o x y k N v hv,
    carrierEquiv_fieldCutoff, carrierEquiv_charge]
  change (phase o x * phase o y) •
      fieldCutoff o (latticeAction o x) (latticeAction o y) k N (fockAction o v) =
    phase o x • fieldCoefficient o (latticeAction o x) k
      (phase o y • (fockAction o v ⊗ₜ[ℂ] basisElement o (latticeAction o y)))
  rw [map_smul, fieldCoefficient_eq_of_annihilation_cutoff o
    (latticeAction o x) (latticeAction o y) k N (fockAction o v) hG, smul_smul]

/-- Covariance of the constructed field on the whole algebraic carrier. -/
theorem carrierEquiv_fieldCoefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (carrierEquiv o).toLinearMap.comp (fieldCoefficient o x k) =
      phase o x • ((fieldCoefficient o (latticeAction o x) k).comp
        (carrierEquiv o).toLinearMap) := by
  apply end_ext_charged
  intro v y
  exact carrierEquiv_fieldCoefficient_pure o x y k v

theorem carrierEquiv_conjugates_field (o : Fin 12) (x : Lattice o) (k : ℤ)
    (v : LatticeCarrier o) :
    carrierEquiv o (fieldCoefficient o x k ((carrierEquiv o).symm v)) =
      phase o x • fieldCoefficient o (latticeAction o x) k v := by
  have h := LinearMap.congr_fun (carrierEquiv_fieldCoefficient o x k)
    ((carrierEquiv o).symm v)
  simpa only [LinearMap.comp_apply, LinearMap.smul_apply,
    LinearEquiv.coe_coe, LinearEquiv.apply_symm_apply] using h

end HMT.IV.LatticeCoxeterFieldCovariance
end

#print axioms HMT.IV.LatticeCoxeterFieldCovariance.fockAction_creationState
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.fockAction_chargeAnnihilation
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.fockAction_creationMode
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.fockAction_annihilationCoefficient
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.carrierEquiv_fieldCutoff
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.carrierEquiv_fieldCoefficient_pure
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.carrierEquiv_fieldCoefficient
#print axioms HMT.IV.LatticeCoxeterFieldCovariance.carrierEquiv_conjugates_field
