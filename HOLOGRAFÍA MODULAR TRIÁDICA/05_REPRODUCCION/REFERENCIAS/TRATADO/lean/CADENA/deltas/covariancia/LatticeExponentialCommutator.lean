import LatticeCreationExponential
import LatticeAnnihilationExponential

/-!
Mixed annihilation/creation-exponential commutators for the actual lattice
oscillators. The proof differentiates the constructed finite coefficient
expansion. Neither a BCH formula nor locality is supplied as an assumption.
-/

noncomputable section
namespace HMT.IV.LatticeExponentialCommutator

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeCreationExponential HMT.IV.LatticeAnnihilationExponential
open HMT.FockTransport.Symmetric
open PowerSeries
open scoped BigOperators

variable {A : Type*} [CommRing A] [Algebra ℂ A]

def seriesDerivation (D : Derivation ℂ A A) :
    Derivation ℂ (PowerSeries A) (PowerSeries A) where
  toLinearMap :=
    { toFun := fun f => PowerSeries.mk fun d => D (coeff A d f)
      map_add' := by intros; ext d; simp
      map_smul' := by intros; ext d; simp }
  map_one_eq_zero' := by
    ext d
    simp only [LinearMap.coe_mk, AddHom.coe_mk, coeff_mk, coeff_one, map_zero]
    split_ifs <;> simp
  leibniz' f g := by
    ext d
    simp only [LinearMap.coe_mk, AddHom.coe_mk, coeff_mk, smul_eq_mul,
      map_add, coeff_mul, map_sum, Derivation.leibniz, Finset.sum_add_distrib]
    congr 1
    exact (Finset.Nat.sum_antidiagonal_swap
      (n := d) (f := fun p => coeff A p.1 g * D (coeff A p.2 f)))

theorem seriesDerivation_coefficient (D : Derivation ℂ A A)
    (f : PowerSeries A) (d : ℕ) :
    coeff A d (seriesDerivation D f) = D (coeff A d f) := by
  change coeff A d (PowerSeries.mk fun n => D (coeff A n f)) = _
  exact coeff_mk _ _

theorem derivative_power_coefficient (D : Derivation ℂ A A)
    (f : PowerSeries A) (k d : ℕ) :
    D (coeff A d (f^(k+1))) =
      (k+1 : ℂ) • coeff A d (f^k * seriesDerivation D f) := by
  rw [← seriesDerivation_coefficient, Derivation.leibniz_pow]
  simp only [Nat.add_sub_cancel, smul_eq_mul, nsmul_eq_mul]
  rw [← nsmul_eq_mul, map_nsmul]
  simpa only [Nat.cast_add, Nat.cast_one] using
    (Nat.cast_smul_eq_nsmul ℂ (k+1)
      (coeff A d (f^k * seriesDerivation D f))).symm

theorem derivation_sum_apply {ι : Type*} (s : Finset ι)
    (D : ι → Derivation ℂ A A) (v : A) : (∑ i ∈ s, D i) v = ∑ i ∈ s, D i v := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih => simp [Finset.sum_insert ha, Derivation.add_apply, ih]

def chargedDerivation (o : Fin 12) (x : Lattice o) (n : ℕ) :
    Derivation ℂ (Fock o) (Fock o) :=
  ∑ i : Fin (BasisSize o), ((latticeBasis o).repr x i : ℂ) •
    annihilation (modeCovector o n i)

theorem chargedDerivation_apply (o : Fin 12) (x : Lattice o) (n : ℕ)
    (v : Fock o) : chargedDerivation o x n v = chargeAnnihilation o x n v := by
  simp [chargedDerivation, chargeAnnihilation, annihilate, derivation_sum_apply,
    Derivation.smul_apply]

/-- The pairing coefficient is evaluated in the inherited integral basis. -/
def coordinatePair (o : Fin 12) (x y : Lattice o) : ℂ :=
  ∑ i : Fin (BasisSize o), ∑ j : Fin (BasisSize o),
    ((latticeBasis o).repr x i : ℂ) * ((latticeBasis o).repr y j : ℂ) * gram o i j

theorem integerPair_sum_right (o : Fin 12) (x : Lattice o) {ι : Type*}
    (s : Finset ι) (y : ι → Lattice o) :
    integerPair o x (∑ i ∈ s, y i) = ∑ i ∈ s, integerPair o x (y i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [integerPair_zero_right]
  | @insert a s ha ih => simp [Finset.sum_insert ha, integerPair_add_right, ih]

theorem integerPair_sum_left (o : Fin 12) (y : Lattice o) {ι : Type*}
    (s : Finset ι) (x : ι → Lattice o) :
    integerPair o (∑ i ∈ s, x i) y = ∑ i ∈ s, integerPair o (x i) y := by
  rw [integerPair_comm, integerPair_sum_right]
  exact Finset.sum_congr rfl fun i _ => integerPair_comm o y (x i)

theorem coordinatePair_eq_integerPair (o : Fin 12) (x y : Lattice o) :
    coordinatePair o x y = (integerPair o x y : ℂ) := by
  have h : integerPair o x y =
      ∑ i : Fin (BasisSize o), ∑ j : Fin (BasisSize o),
        (latticeBasis o).repr x i * (latticeBasis o).repr y j *
          integerPair o (latticeBasis o i) (latticeBasis o j) := by
    conv_lhs => rw [← (latticeBasis o).sum_repr x, ← (latticeBasis o).sum_repr y]
    simp only [integerPair_sum_left, integerPair_sum_right,
      integerPair_smul_left, integerPair_smul_right, smul_eq_mul, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  unfold coordinatePair gram
  exact_mod_cast h.symm

theorem chargedDerivation_creationState (o : Fin 12) (x y : Lattice o) (n m : ℕ) :
    chargedDerivation o x n (chargeCreationState o y m) =
      if n=m then ((n+1 : ℂ) * coordinatePair o x y) • (1 : Fock o) else 0 := by
  unfold chargedDerivation
  rw [derivation_sum_apply]
  simp only [Derivation.smul_apply, chargeCreationState, chargeModeVector,
    map_sum, map_smul, Derivation.map_smul, annihilation_generator,
    modeCovector_modeVector, Finset.smul_sum]
  by_cases h : n=m
  · subst m
    simp only [if_pos rfl, coordinatePair, Finset.mul_sum, Finset.sum_smul,
      Algebra.algebraMap_eq_smul_one, smul_smul]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    congr 1
    simp only [if_true]
    ring
  · simp [h]

theorem derivative_creationPotential (o : Fin 12) (x y : Lattice o) (n : ℕ) :
    seriesDerivation (chargedDerivation o x n) (creationPotential o y) =
      coordinatePair o x y • (X^(n+1) : PowerSeries (Fock o)) := by
  ext d
  rw [seriesDerivation_coefficient, coeff_smul, coeff_X_pow]
  cases d with
  | zero =>
    rw [coeff_zero_eq_constantCoeff_apply, creationPotential_constant, map_zero]
    simp
  | succ m =>
    rw [creationPotential_coefficient_succ, Derivation.map_smul,
      chargedDerivation_creationState]
    by_cases h : n=m
    · subst m
      simp only [Nat.succ.injEq, if_true, smul_smul]
      have hn : (n+1 : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
      congr 1
      field_simp
    · have hm : m+1 ≠ n+1 := by omega
      simp [h, Ne.symm h, hm]

theorem derivative_creationPower_coefficient (o : Fin 12) (x y : Lattice o)
    (n k d : ℕ) :
    chargedDerivation o x n (coeff (Fock o) d (creationPotential o y ^ (k+1))) =
      if n+1 ≤ d then
        ((k+1 : ℂ) * coordinatePair o x y) •
          coeff (Fock o) (d-(n+1)) (creationPotential o y ^ k)
      else 0 := by
  rw [derivative_power_coefficient, derivative_creationPotential,
    mul_smul_comm, coeff_smul, coeff_mul_X_pow']
  split_ifs <;> simp [smul_smul]

theorem exp_coefficient_succ_mul (k : ℕ) :
    coeff ℂ (k+1) (PowerSeries.exp ℂ) * (k+1 : ℂ) =
      coeff ℂ k (PowerSeries.exp ℂ) := by
  simp only [coeff_exp, map_div₀, map_one, map_natCast, Nat.factorial_succ,
    Nat.cast_mul, Nat.cast_add, Nat.cast_one]
  have hk : (k+1 : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero k
  have hf : (k.factorial : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
  field_simp

theorem creationExponential_coefficient_extended (o : Fin 12) (y : Lattice o)
    (d N : ℕ) (hN : d ≤ N) :
    coeff (Fock o) d (creationExponential o y) =
      ∑ k ∈ Finset.range (N+1), coeff ℂ k (PowerSeries.exp ℂ) •
        coeff (Fock o) d (creationPotential o y ^ k) := by
  rw [creationExponential_coefficient]
  apply Finset.sum_subset (Finset.range_mono (by omega))
  intro k _ hk
  have hdk : d < k := by simp only [Finset.mem_range] at hk; omega
  rw [HMT.IV.LatticeCreationExponential.potential_power_coefficient_zero o y d k hdk,
    smul_zero]

theorem annihilation_creationExponential_coefficient (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) :
    chargeAnnihilation o x n (coeff (Fock o) d (creationExponential o y)) =
      if n+1 ≤ d then coordinatePair o x y •
        coeff (Fock o) (d-(n+1)) (creationExponential o y) else 0 := by
  rw [← chargedDerivation_apply]
  cases d with
  | zero => rw [creationExponential_constant]; simp
  | succ d =>
    rw [creationExponential_coefficient, map_sum, Finset.sum_range_succ']
    simp only [pow_zero, coeff_one, Nat.succ_ne_zero, if_false,
      smul_zero, map_zero, add_zero]
    by_cases hd : n+1 ≤ d+1
    · rw [if_pos hd, creationExponential_coefficient_extended o y _ d (by omega),
        Finset.smul_sum]
      apply Finset.sum_congr rfl
      intro k _
      rw [Derivation.map_smul, derivative_creationPower_coefficient, if_pos hd,
        smul_smul, ← mul_assoc, exp_coefficient_succ_mul, smul_smul, mul_comm]
    · rw [if_neg hd]
      apply Finset.sum_eq_zero
      intro k _
      rw [Derivation.map_smul, derivative_creationPower_coefficient, if_neg hd, smul_zero]

theorem mixed_exponential_commutator (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) (v : Fock o) :
    chargeAnnihilation o x n (creationExponentialMode o y d v) -
      creationExponentialMode o y d (chargeAnnihilation o x n v) =
      if n+1 ≤ d then coordinatePair o x y •
        creationExponentialMode o y (d-(n+1)) v else 0 := by
  change chargeAnnihilation o x n (coeff (Fock o) d (creationExponential o y) * v) -
    coeff (Fock o) d (creationExponential o y) * chargeAnnihilation o x n v = _
  rw [← chargedDerivation_apply, Derivation.leibniz]
  simp only [smul_eq_mul, chargedDerivation_apply]
  rw [annihilation_creationExponential_coefficient]
  split_ifs <;> simp [creationExponentialMode, smul_eq_mul, Algebra.smul_def, mul_comm,
    mul_left_comm, mul_assoc]

/-- Mixed commutator with the inherited integral lattice pairing, on every
Fock vector and for every mode and coefficient degree. -/
theorem mixed_exponential_commutator_pairing (o : Fin 12) (x y : Lattice o)
    (n d : ℕ) (v : Fock o) :
    chargeAnnihilation o x n (creationExponentialMode o y d v) -
      creationExponentialMode o y d (chargeAnnihilation o x n v) =
      if n+1 ≤ d then (integerPair o x y : ℂ) •
        creationExponentialMode o y (d-(n+1)) v else 0 := by
  rw [mixed_exponential_commutator, coordinatePair_eq_integerPair]

end HMT.IV.LatticeExponentialCommutator
end

#print axioms HMT.IV.LatticeExponentialCommutator.derivative_power_coefficient
#print axioms HMT.IV.LatticeExponentialCommutator.chargedDerivation_creationState
#print axioms HMT.IV.LatticeExponentialCommutator.derivative_creationPotential
#print axioms HMT.IV.LatticeExponentialCommutator.derivative_creationPower_coefficient
#print axioms HMT.IV.LatticeExponentialCommutator.annihilation_creationExponential_coefficient
#print axioms HMT.IV.LatticeExponentialCommutator.mixed_exponential_commutator
#print axioms HMT.IV.LatticeExponentialCommutator.coordinatePair_eq_integerPair
#print axioms HMT.IV.LatticeExponentialCommutator.mixed_exponential_commutator_pairing
