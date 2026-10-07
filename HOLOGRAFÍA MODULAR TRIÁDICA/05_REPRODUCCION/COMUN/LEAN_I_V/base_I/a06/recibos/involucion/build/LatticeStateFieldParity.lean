import LatticeChargedFieldParity
import LatticeStateFieldCoherence

/-!
The existing order-two lattice/oscillator involution intertwines the complete
state-field map. Normal ordering is transported through its actual finite
coefficient sums. The scalar sign counts oscillator letters; lattice negation
uses the already proved cocycle lift. No orbifold or twisted-sector axiom is
introduced.
-/

noncomputable section
set_option maxHeartbeats 1200000
namespace HMT.IV.LatticeStateFieldParity

open LatticeCocycle LatticeOscillatorFock LatticeParityCarrier
open LatticeFockMonomialParity LatticeChargedFieldParity TwistedGroupAlgebra
open LatticeHeisenbergModes LatticeNormalOrderedField LatticeDescendantFields
open LatticeStateFieldMap LatticeStateFieldCoherence LatticeOscillatorWords
open LatticeNormalProductCommutation
open scoped TensorProduct BigOperators

local notation "P" => carrierTheta

theorem theta_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (v : LatticeCarrier o) :
    P o (onCarrier o (create o n i) v) = -onCarrier o (create o n i) (P o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [onCarrier_pure, carrierTheta_pure]
    change fockTheta o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i) * v)
        ⊗ₜ[ℂ] WittNegationLift.theta o a = _
    rw [map_mul, fockTheta_generator, neg_mul, TensorProduct.neg_tmul]
    rfl
  | add v w hv hw => simp only [map_add, hv, hw, neg_add_rev]; abel

theorem theta_annihilate_carrier (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (v : LatticeCarrier o) :
    P o (onCarrier o (annihilate o n i) v) =
      -onCarrier o (annihilate o n i) (P o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [onCarrier_pure, carrierTheta_pure, theta_annihilate, TensorProduct.neg_tmul]
  | add v w hv hw => simp only [map_add, hv, hw, neg_add_rev]; abel

theorem theta_zeroMode (o : Fin 12) (x : Lattice o) (a : TwistedAlgebra o) :
    WittNegationLift.theta o (LatticeZeroModes.zeroMode o x a) =
      -LatticeZeroModes.zeroMode o x (WittNegationLift.theta o a) := by
  let R := (WittNegationLift.theta o).toLinearEquiv.toLinearMap
  have he : R.comp (LatticeZeroModes.zeroMode o x) =
      -(LatticeZeroModes.zeroMode o x).comp R := by
    apply (latticeBasisComplex o).ext
    intro y
    change WittNegationLift.theta o (LatticeZeroModes.zeroMode o x (basisElement o y)) =
      -LatticeZeroModes.zeroMode o x (WittNegationLift.theta o (basisElement o y))
    have hp : integerPair o x (-y) = -integerPair o x y := by
      rw [integerPair_comm, LatticeWeightShells.integerPair_neg_left, integerPair_comm o y x]
    simp only [LatticeZeroModes.zeroMode_basis, map_smul, WittNegationLift.theta_basis,
      hp, Int.cast_neg, neg_smul, neg_neg]
  exact LinearMap.congr_fun he a

theorem theta_hmode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ)
    (v : LatticeCarrier o) : P o (hmode o i m v) = -hmode o i m (P o v) := by
  cases m with
  | negSucc n => rw [hmode_negSucc]; exact theta_create o n i v
  | ofNat n =>
    cases n with
    | succ n => rw [hmode_natSucc]; exact theta_annihilate_carrier o n i v
    | zero =>
      rw [show (Int.ofNat 0) = 0 by rfl, hmode_zero]
      induction v using TensorProduct.induction_on with
      | zero => simp
      | tmul v a =>
        simp only [onLattice_pure, carrierTheta_pure, theta_zeroMode,
          TensorProduct.tmul_neg]
      | add v w hv hw => simp only [map_add, hv, hw, neg_add_rev]; abel

theorem theta_creationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B D : VertexOperator ℂ (LatticeCarrier o)) (c : ℂ)
    (hBD : ∀ k v, P o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff D k (P o v)) (k : ℤ) (a : ℕ) (v : LatticeCarrier o) :
    P o (creationTerm o i n B k a v) = (-c) • creationTerm o i n D k a (P o v) := by
  simp only [creationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    map_smul, theta_create, hBD]
  simp only [map_smul, smul_neg, neg_smul, smul_smul]
  module

theorem theta_annihilationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B D : VertexOperator ℂ (LatticeCarrier o)) (c : ℂ)
    (hBD : ∀ k v, P o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff D k (P o v)) (k : ℤ) (a : ℕ) (v : LatticeCarrier o) :
    P o (annihilationTerm o i n B k a v) =
      (-c) • annihilationTerm o i n D k a (P o v) := by
  simp only [annihilationTerm, LinearMap.smul_apply, LinearMap.comp_apply,
    map_smul, hBD, theta_hmode, map_neg, smul_neg, neg_smul, smul_smul]
  module

theorem theta_normalField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B D : VertexOperator ℂ (LatticeCarrier o)) (c : ℂ)
    (hBD : ∀ k v, P o (HVertexOperator.coeff B k v) =
      c • HVertexOperator.coeff D k (P o v)) (k : ℤ) (v : LatticeCarrier o) :
    P o (HVertexOperator.coeff (normalField o i n B) k v) =
      (-c) • HVertexOperator.coeff (normalField o i n D) k (P o v) := by
  simp only [normalField_coefficient, normalCoefficient_apply, map_add]
  have hc : P o (∑ᶠ a, creationTerm o i n B k a v) =
      ∑ᶠ a, P o (creationTerm o i n B k a v) :=
    (P o).toAddMonoidHom.map_finsum (creationTerm_finite o i n B k v)
  have ha : P o (∑ᶠ a, annihilationTerm o i n B k a v) =
      ∑ᶠ a, P o (annihilationTerm o i n B k a v) :=
    (P o).toAddMonoidHom.map_finsum (annihilationTerm_finite o i n B k v)
  rw [hc, ha]
  simp_rw [theta_creationTerm o i n B D c hBD, theta_annihilationTerm o i n B D c hBD]
  rw [← smul_finsum' (-c) (creationTerm_finite o i n D k (P o v)),
    ← smul_finsum' (-c) (annihilationTerm_finite o i n D k (P o v)), smul_add]

theorem theta_descendantState (o : Fin 12) (x : Lattice o) (w : List (Mode o)) :
    P o (descendantState o x w) = (-1 : ℂ)^w.length • descendantState o (-x) w := by
  induction w with
  | nil => simp [descendantState, WittNegationLift.theta_basis]
  | cons m w ih =>
    simp only [descendantState, theta_create, ih, map_smul, List.length_cons, pow_succ]
    rw [mul_comm, mul_smul, neg_one_smul]

theorem theta_descendantField (o : Fin 12) (x : Lattice o) (w : List (Mode o))
    (k : ℤ) (v : LatticeCarrier o) :
    P o (HVertexOperator.coeff (descendantField o x w) k v) =
      (-1 : ℂ)^w.length • HVertexOperator.coeff (descendantField o (-x) w) k (P o v) := by
  induction w generalizing k v with
  | nil =>
    have h := LinearMap.congr_fun (theta_fieldCoefficient o x k) v
    simpa only [descendantField, List.length_nil, pow_zero, one_smul] using h
  | cons m w ih =>
    simp only [descendantField, List.length_cons]
    rw [theta_normalField o m.2 m.1 _ _ _ ih, pow_succ, mul_neg_one]

theorem theta_stateField_apply (o : Fin 12) (u : LatticeCarrier o) (k : ℤ)
    (v : LatticeCarrier o) :
    P o (HVertexOperator.coeff (stateField o u) k v) =
      HVertexOperator.coeff (stateField o (P o u)) k (P o v) := by
  let L : LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
    { toFun := fun z => P o (HVertexOperator.coeff (stateField o z) k v)
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply] }
  let R : LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
    { toFun := fun z => HVertexOperator.coeff (stateField o (P o z)) k (P o v)
      map_add' := by
        intro z t
        simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
      map_smul' := by
        intro c z
        simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply,
          LinearMap.smul_apply, RingHom.id_apply] }
  have hLR : L = R := by
    apply (carrierBasis o).ext
    rintro ⟨a,x⟩
    change P o (HVertexOperator.coeff (stateField o (carrierBasis o (a,x))) k v) =
      HVertexOperator.coeff (stateField o (P o (carrierBasis o (a,x)))) k (P o v)
    rw [← carrierBasis_wordForOccupation o a x, ← descendantState_eq_word,
      theta_descendantState, map_smul, stateField_descendant, stateField_descendant]
    simp only [HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]
    exact theta_descendantField o x (wordForOccupation o a) k v
  exact LinearMap.congr_fun hLR u

theorem theta_stateField_intertwines (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    P o * HVertexOperator.coeff (stateField o u) k =
      HVertexOperator.coeff (stateField o (P o u)) k * P o := by
  apply LinearMap.ext
  intro v
  exact theta_stateField_apply o u k v

/-- Since the existing parity satisfies `P²=1`, its inverse is itself.
This is equivariance of the entire state-field map on the actual carrier. -/
theorem theta_stateField_conjugates (o : Fin 12) (u : LatticeCarrier o) (k : ℤ) :
    P o * HVertexOperator.coeff (stateField o u) k * P o =
      HVertexOperator.coeff (stateField o (P o u)) k := by
  apply LinearMap.ext
  intro v
  change P o (HVertexOperator.coeff (stateField o u) k (P o v)) = _
  rw [theta_stateField_apply, carrierTheta_square]

end HMT.IV.LatticeStateFieldParity
end

#print axioms HMT.IV.LatticeStateFieldParity.theta_hmode
#print axioms HMT.IV.LatticeStateFieldParity.theta_normalField
#print axioms HMT.IV.LatticeStateFieldParity.theta_descendantField
#print axioms HMT.IV.LatticeStateFieldParity.theta_stateField_intertwines
#print axioms HMT.IV.LatticeStateFieldParity.theta_stateField_conjugates
