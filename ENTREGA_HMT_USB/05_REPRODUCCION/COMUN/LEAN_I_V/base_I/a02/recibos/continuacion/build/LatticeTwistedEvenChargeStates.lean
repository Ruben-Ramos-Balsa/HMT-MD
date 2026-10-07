import LatticeTwistedChargeNormalization
import LatticeEvenVertexFields

/-! A linear field map on the genuine even exponential-state subspace of the
untwisted lattice carrier. Its generators are the averages
(1 tensor e^x + 1 tensor e^(-x))/2 inside the existing evenSpace; the zero charge
is therefore the existing vacuum. The map is constructed by the Fock-vacuum
projection and the actual twisted-group-algebra basis. It is not a state-field
map on oscillator descendants and asserts no twisted Jacobi identity. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeTwistedEvenChargeStates
open TensorProduct
open LatticeCocycle LatticeOscillatorFock TwistedGroupAlgebra
open LatticeFockMonomialParity LatticeParityCarrier LatticeEvenVertexFields
open LatticeTwistedPositiveSector LatticeTwistedPositiveKernel
open LatticeTwistedKernelParity LatticeTwistedChargeNormalization

theorem positiveCoefficient_neg_charge (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    positiveCoefficient o (-x) s k = positiveCoefficient o x s k := by
  apply LinearMap.ext
  intro v
  apply Subtype.ext
  change descendedCoefficient o (-x) s k v.val = descendedCoefficient o x s k v.val
  simp only [descendedCoefficient, evenKernelCoefficient, neg_neg, add_comm]

theorem chargeField_neg (o : Fin 12) (x : Lattice o) : chargeField o (-x) = chargeField o x := by
  apply HVertexOperator.coeff_inj
  funext k
  rw [chargeField_coefficient, chargeField_coefficient]
  simp only [chargeCoefficient, normScalar_neg, LatticeWeightShells.halfnormNat_neg,
    positiveCoefficient_neg_charge]

def latticeEmbedding (o : Fin 12) : TwistedAlgebra o →ₗ[ℂ] LatticeCarrier o :=
  TensorProduct.mk ℂ (Fock o) (TwistedAlgebra o) 1

def latticeProjection (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] TwistedAlgebra o :=
  (TensorProduct.lid ℂ (TwistedAlgebra o)).toLinearMap.comp
    ((SymmetricAlgebra.lift (0 : Oscillators o →ₗ[ℂ] ℂ)).toLinearMap.rTensor (TwistedAlgebra o))

theorem latticeProjection_embedding (o : Fin 12) (a : TwistedAlgebra o) :
    latticeProjection o (latticeEmbedding o a) = a := by
  simp [latticeProjection, latticeEmbedding]

theorem latticeEmbedding_injective (o : Fin 12) : Function.Injective (latticeEmbedding o) :=
  Function.LeftInverse.injective (latticeProjection_embedding o)

def exponentialState (o : Fin 12) (x : Lattice o) : LatticeCarrier o :=
  latticeEmbedding o (basisElement o x)

theorem exponentialState_eq_carrierBasis (o : Fin 12) (x : Lattice o) :
    exponentialState o x = carrierBasis o (0,x) := by
  simp [exponentialState, latticeEmbedding, carrierBasis, Basis.tensorProduct_apply,
    monomialBasis_product, latticeBasisComplex, basisElement, Finsupp.coe_basisSingleOne]
  rfl

theorem theta_exponentialState (o : Fin 12) (x : Lattice o) :
    carrierTheta o (exponentialState o x) = exponentialState o (-x) := by
  simp [exponentialState, latticeEmbedding, WittNegationLift.theta_basis]

theorem exponentialState_zero (o : Fin 12) : exponentialState o 0 = vacuum o := by
  rw [exponentialState_eq_carrierBasis, vacuum_is_empty_monomial]

def evenExponentialState (o : Fin 12) (x : Lattice o) : evenSpace o :=
  ⟨LatticeParityCarrier.evenProjector o (exponentialState o x), evenProjector_mem o _⟩

theorem evenExponentialState_coe (o : Fin 12) (x : Lattice o) :
    (evenExponentialState o x).val =
      (2:ℂ)⁻¹ • (exponentialState o x + exponentialState o (-x)) := by
  change (2:ℂ)⁻¹ • (exponentialState o x + carrierTheta o (exponentialState o x)) = _
  rw [theta_exponentialState]

theorem evenExponentialState_neg (o : Fin 12) (x : Lattice o) :
    evenExponentialState o (-x) = evenExponentialState o x := by
  apply Subtype.ext
  simp only [evenExponentialState_coe, neg_neg, add_comm]

theorem evenExponentialState_zero (o : Fin 12) : evenExponentialState o 0 = evenVacuum o := by
  apply Subtype.ext
  rw [evenExponentialState_coe, neg_zero, exponentialState_zero]
  change (2:ℂ)⁻¹ • (vacuum o + vacuum o) = vacuum o
  module

def evenExponentialStates (o : Fin 12) : Submodule ℂ (evenSpace o) :=
  Submodule.span ℂ (Set.range (evenExponentialState o))

def exponentialGenerator (o : Fin 12) (x : Lattice o) : evenExponentialStates o :=
  ⟨evenExponentialState o x, Submodule.subset_span ⟨x,rfl⟩⟩

def evenExponentialInclusion (o : Fin 12) : evenExponentialStates o →ₗ[ℂ] evenSpace o :=
  (evenExponentialStates o).subtype

theorem evenExponentialInclusion_injective (o : Fin 12) :
    Function.Injective (evenExponentialInclusion o) := Subtype.val_injective

theorem evenExponentialInclusion_generator (o : Fin 12) (x : Lattice o) :
    evenExponentialInclusion o (exponentialGenerator o x) = evenExponentialState o x := rfl

def latticeFieldLinear (o : Fin 12) :
    TwistedAlgebra o →ₗ[ℂ] VertexOperator ℂ (positiveSector o) :=
  (latticeBasisComplex o).constr ℂ (chargeField o)

theorem latticeFieldLinear_basis (o : Fin 12) (x : Lattice o) :
    latticeFieldLinear o (basisElement o x) = chargeField o x :=
  Basis.constr_basis (latticeBasisComplex o) ℂ (chargeField o) x

theorem latticeFieldLinear_theta (o : Fin 12) (a : TwistedAlgebra o) :
    latticeFieldLinear o (WittNegationLift.theta o a) = latticeFieldLinear o a := by
  have h : (latticeFieldLinear o).comp (WittNegationLift.theta o).toLinearMap =
      latticeFieldLinear o := by
    apply (latticeBasisComplex o).ext
    intro x
    change latticeFieldLinear o (WittNegationLift.theta o (basisElement o x)) =
      latticeFieldLinear o (basisElement o x)
    rw [WittNegationLift.theta_basis, latticeFieldLinear_basis, latticeFieldLinear_basis,
      chargeField_neg]
  exact LinearMap.congr_fun h a

def evenExponentialField (o : Fin 12) :
    evenExponentialStates o →ₗ[ℂ] VertexOperator ℂ (positiveSector o) :=
  (latticeFieldLinear o).comp ((latticeProjection o).comp
    ((evenSpace o).subtype.comp (evenExponentialInclusion o)))

theorem evenExponentialField_generator (o : Fin 12) (x : Lattice o) :
    evenExponentialField o (exponentialGenerator o x) = chargeField o x := by
  change latticeFieldLinear o (latticeProjection o (evenExponentialState o x).val) = _
  rw [evenExponentialState_coe]
  simp only [map_smul, map_add, exponentialState, latticeProjection_embedding,
    latticeFieldLinear_basis, chargeField_neg]
  module

theorem evenExponentialField_inversion (o : Fin 12) (x : Lattice o) :
    evenExponentialField o (exponentialGenerator o (-x)) =
      evenExponentialField o (exponentialGenerator o x) := by
  rw [evenExponentialField_generator, evenExponentialField_generator, chargeField_neg]

theorem evenVacuum_mem_exponentialStates (o : Fin 12) :
    evenVacuum o ∈ evenExponentialStates o := by
  rw [← evenExponentialState_zero]
  exact Submodule.subset_span ⟨0,rfl⟩

def exponentialVacuum (o : Fin 12) : evenExponentialStates o :=
  ⟨evenVacuum o, evenVacuum_mem_exponentialStates o⟩

theorem exponentialVacuum_eq_generator (o : Fin 12) :
    exponentialVacuum o = exponentialGenerator o 0 := by
  apply Subtype.ext
  exact (evenExponentialState_zero o).symm

theorem evenExponentialField_vacuum (o : Fin 12) :
    evenExponentialField o (exponentialVacuum o) = chargeField o 0 := by
  rw [exponentialVacuum_eq_generator, evenExponentialField_generator]

theorem evenExponentialField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (evenExponentialField o (exponentialVacuum o)) k =
      if k=0 then (1 : Module.End ℂ (positiveSector o)) else 0 := by
  rw [evenExponentialField_vacuum, chargeField_zero_charge]

end HMT.IV.LatticeTwistedEvenChargeStates
end

#print axioms HMT.IV.LatticeTwistedEvenChargeStates.positiveCoefficient_neg_charge
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.chargeField_neg
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeEmbedding
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeProjection
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeProjection_embedding
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeEmbedding_injective
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialState
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialState_eq_carrierBasis
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.theta_exponentialState
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialState_zero
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialState
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialState_coe
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialState_neg
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialState_zero
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialStates
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialGenerator
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialInclusion
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialInclusion_injective
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialInclusion_generator
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeFieldLinear
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeFieldLinear_basis
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.latticeFieldLinear_theta
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialField
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialField_generator
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialField_inversion
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenVacuum_mem_exponentialStates
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialVacuum
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.exponentialVacuum_eq_generator
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialField_vacuum
#print axioms HMT.IV.LatticeTwistedEvenChargeStates.evenExponentialField_vacuum_coefficient
