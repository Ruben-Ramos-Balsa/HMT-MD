import LatticeTwistedCarrier
import LatticeChargedFieldParity

/-! Parity on the actual half-integer oscillator space tensor the constructed
finite irreducible module. The sign is chosen so that the ground space is odd.
The involution, complementary projectors, oscillator sign and commutation with
the actual charge and conformal operators are proved. No twisted vertex product
or orbifold multiplication is supplied or assumed. -/

noncomputable section
namespace HMT.IV.LatticeTwistedParity
open TensorProduct
open LatticeCocycle LatticeOscillatorFock LatticeFiniteIrreducible
open LatticeParityCarrier LatticeTwistedCarrier LatticeTwistedOscillatorTensor
open LatticeHalfIntegerHeisenberg hiding halfMode
open LatticeHalfConformalModes LatticeHalfConformalVacuum LatticeHalfConformalCentralizer

def liftedTheta (o : Fin 12) : Module.End ℂ (Carrier o) :=
  -((fockTheta o).toLinearMap.rTensor (FiniteSpace o))

theorem liftedTheta_tmul (o : Fin 12) (v : HalfFock o) (t : FiniteSpace o) :
    liftedTheta o (v ⊗ₜ[ℂ] t) = -(fockTheta o v ⊗ₜ[ℂ] t) := by
  simp [liftedTheta]

theorem liftedTheta_square (o : Fin 12) (v : Carrier o) :
    liftedTheta o (liftedTheta o v) = v := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v t => simp [liftedTheta_tmul, map_neg, fockTheta_square]
  | add a b ha hb => simp only [map_add, ha, hb]

def evenProjector (o : Fin 12) : Module.End ℂ (Carrier o) :=
  (2:ℂ)⁻¹ • (LinearMap.id + liftedTheta o)

def oddProjector (o : Fin 12) : Module.End ℂ (Carrier o) :=
  (2:ℂ)⁻¹ • (LinearMap.id - liftedTheta o)

theorem even_fixed (o : Fin 12) (v : Carrier o) :
    liftedTheta o (evenProjector o v) = evenProjector o v := by
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply, map_smul, map_add, liftedTheta_square]
  rw [add_comm]

theorem odd_negated (o : Fin 12) (v : Carrier o) :
    liftedTheta o (oddProjector o v) = -oddProjector o v := by
  simp only [oddProjector, LinearMap.smul_apply, LinearMap.sub_apply,
    LinearMap.id_apply, map_smul, map_sub, liftedTheta_square]
  module

theorem parity_decomposition (o : Fin 12) (v : Carrier o) :
    evenProjector o v + oddProjector o v = v := by
  simp only [evenProjector, oddProjector, LinearMap.smul_apply,
    LinearMap.add_apply, LinearMap.sub_apply, LinearMap.id_apply]
  module

theorem even_idempotent (o : Fin 12) (v : Carrier o) :
    evenProjector o (evenProjector o v) = evenProjector o v := by
  change (2:ℂ)⁻¹ • (evenProjector o v + liftedTheta o (evenProjector o v)) = _
  rw [even_fixed]
  module

theorem odd_idempotent (o : Fin 12) (v : Carrier o) :
    oddProjector o (oddProjector o v) = oddProjector o v := by
  change (2:ℂ)⁻¹ • (oddProjector o v - liftedTheta o (oddProjector o v)) = _
  rw [odd_negated]
  module

theorem even_odd_zero (o : Fin 12) (v : Carrier o) :
    evenProjector o (oddProjector o v) = 0 := by
  change (2:ℂ)⁻¹ • (oddProjector o v + liftedTheta o (oddProjector o v)) = 0
  rw [odd_negated]
  simp

theorem odd_even_zero (o : Fin 12) (v : Carrier o) :
    oddProjector o (evenProjector o v) = 0 := by
  change (2:ℂ)⁻¹ • (evenProjector o v - liftedTheta o (evenProjector o v)) = 0
  rw [even_fixed]
  simp

theorem liftedTheta_ground (o : Fin 12) (t : FiniteSpace o) :
    liftedTheta o (groundEmbedding o t) = -groundEmbedding o t := by
  simp [groundEmbedding, liftedTheta_tmul]

theorem even_ground_zero (o : Fin 12) (t : FiniteSpace o) :
    evenProjector o (groundEmbedding o t) = 0 := by
  change (2:ℂ)⁻¹ • (groundEmbedding o t + liftedTheta o (groundEmbedding o t)) = 0
  rw [liftedTheta_ground]
  simp

theorem odd_ground_identity (o : Fin 12) (t : FiniteSpace o) :
    oddProjector o (groundEmbedding o t) = groundEmbedding o t := by
  have h := parity_decomposition o (groundEmbedding o t)
  simpa only [even_ground_zero, zero_add] using h

theorem theta_create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) (v : HalfFock o) :
    fockTheta o (create o n i v) = -create o n i (fockTheta o v) := by
  change fockTheta o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeVector o n i) * v) = _
  rw [map_mul, fockTheta_generator]
  simp only [neg_mul]
  rfl

theorem theta_halfAnnihilate (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o))
    (v : HalfFock o) :
    fockTheta o (halfAnnihilate o n i v) = -halfAnnihilate o n i (fockTheta o v) := by
  simp only [halfAnnihilate, LinearMap.smul_apply, map_smul,
    LatticeChargedFieldParity.theta_annihilate, smul_neg]

theorem theta_halfMode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ)
    (v : HalfFock o) :
    fockTheta o (LatticeHalfIntegerHeisenberg.halfMode o i m v) =
      -LatticeHalfIntegerHeisenberg.halfMode o i m (fockTheta o v) := by
  cases m with
  | ofNat n => exact theta_halfAnnihilate o n i v
  | negSucc n => exact theta_create o n i v

theorem liftedTheta_halfMode (o : Fin 12) (i : Fin (BasisSize o)) (m : ℤ)
    (v : Carrier o) :
    liftedTheta o (halfMode o i m v) = -halfMode o i m (liftedTheta o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    simp only [halfMode, halfModeTensor_tmul, liftedTheta_tmul, theta_halfMode,
      TensorProduct.neg_tmul, map_neg, neg_neg]
  | add a b ha hb => simp only [map_add, ha, hb, neg_add]

theorem first_oscillator_positive (o : Fin 12) (i : Fin (BasisSize o))
    (t : FiniteSpace o) :
    liftedTheta o (halfMode o i (-1) (groundEmbedding o t)) =
      halfMode o i (-1) (groundEmbedding o t) := by
  rw [liftedTheta_halfMode, liftedTheta_ground, map_neg, neg_neg]

theorem even_first_oscillator_identity (o : Fin 12) (i : Fin (BasisSize o))
    (t : FiniteSpace o) :
    evenProjector o (halfMode o i (-1) (groundEmbedding o t)) =
      halfMode o i (-1) (groundEmbedding o t) := by
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply]
  rw [first_oscillator_positive]
  module

theorem liftedTheta_comm_charge (o : Fin 12) (x : Lattice o) :
    liftedTheta o * chargeOperator o x = chargeOperator o x * liftedTheta o := by
  change (-((fockTheta o).toLinearMap.rTensor (FiniteSpace o))) *
    secondFactorOperator (FiniteSpace o) o _ =
      secondFactorOperator (FiniteSpace o) o _ *
        (-((fockTheta o).toLinearMap.rTensor (FiniteSpace o)))
  apply LinearMap.ext
  intro v
  have h := LinearMap.congr_fun
    (tensor_factors_commute (FiniteSpace o) o (fockTheta o).toLinearMap
      (LatticeFiniteGroundState.latticeOperator o x)) v
  simp only [Module.End.mul_apply, LinearMap.neg_apply, map_neg] at h ⊢
  exact congrArg Neg.neg h

theorem theta_creationHalfTerm (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) (v : HalfFock o) :
    fockTheta o (creationHalfTerm o i j m a v) =
      creationHalfTerm o i j m a (fockTheta o v) := by
  simp only [creationHalfTerm, LinearMap.comp_apply, theta_create,
    theta_halfMode, map_neg, neg_neg]

theorem theta_annihilationHalfTerm (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) (v : HalfFock o) :
    fockTheta o (annihilationHalfTerm o i j m a v) =
      annihilationHalfTerm o i j m a (fockTheta o v) := by
  simp only [annihilationHalfTerm, LinearMap.comp_apply, theta_halfMode,
    theta_halfAnnihilate, map_neg, neg_neg]

theorem theta_halfNormalMode (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (v : HalfFock o) :
    fockTheta o (halfNormalMode o i j m v) =
      halfNormalMode o i j m (fockTheta o v) := by
  simp only [halfNormalMode_apply, map_add]
  have hc : fockTheta o (∑ᶠ a, creationHalfTerm o i j m a v) =
      ∑ᶠ a, fockTheta o (creationHalfTerm o i j m a v) :=
    (fockTheta o).toAddMonoidHom.map_finsum (creationHalfTerm_finite o i j m v)
  have ha : fockTheta o (∑ᶠ a, annihilationHalfTerm o i j m a v) =
      ∑ᶠ a, fockTheta o (annihilationHalfTerm o i j m a v) :=
    (fockTheta o).toAddMonoidHom.map_finsum (annihilationHalfTerm_finite o i j m v)
  rw [hc, ha]
  simp_rw [theta_creationHalfTerm, theta_annihilationHalfTerm]

theorem theta_quadraticMode (o : Fin 12) (m : ℤ) (v : HalfFock o) :
    fockTheta o (quadraticMode o m v) = quadraticMode o m (fockTheta o v) := by
  simp only [quadraticMode_apply, map_smul, map_sum, theta_halfNormalMode]

theorem theta_shiftedModes (o : Fin 12) (m : ℤ) (v : HalfFock o) :
    fockTheta o (shiftedModes o m v) = shiftedModes o m (fockTheta o v) := by
  by_cases hm : m = 0
  · simp only [shiftedModes, shiftedQuadraticMode, if_pos hm, LinearMap.add_apply,
      LinearMap.smul_apply, LinearMap.id_apply, map_add, map_smul, theta_quadraticMode]
  · simp only [shiftedModes, shiftedQuadraticMode, if_neg hm, add_zero, theta_quadraticMode]

theorem liftedTheta_comm_conformal_apply (o : Fin 12) (m : ℤ) (v : Carrier o) :
    liftedTheta o (conformalMode o m v) = conformalMode o m (liftedTheta o v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v t =>
    simp only [conformalMode, conformalModeTensor_tmul, liftedTheta_tmul,
      theta_shiftedModes, map_neg]
  | add a b ha hb => simp only [map_add, ha, hb]

theorem liftedTheta_comm_conformal (o : Fin 12) (m : ℤ) :
    liftedTheta o * conformalMode o m = conformalMode o m * liftedTheta o := by
  apply LinearMap.ext
  exact liftedTheta_comm_conformal_apply o m

end HMT.IV.LatticeTwistedParity
end
