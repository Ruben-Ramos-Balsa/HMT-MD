import LatticeFieldLocality
import LatticeChargedLocalityFull
import LatticeMixedLocality
import LatticeHeisenbergField

/-! The three existing generator-locality proofs, expressed with one
coefficientwise locality predicate on the same actual Laurent fields. -/
noncomputable section
namespace HMT.IV.LatticeGeneratorLocality
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFieldLocality HMT.IV.LatticeFactorConvolution
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeHeisenbergField

theorem charged_coefficient (o : Fin 12) (x : Lattice o) (k : ℤ) :
    HVertexOperator.coeff (chargedField o x) k =
      HMT.IV.LatticeChargedVertexField.fieldCoefficient o x k := rfl

theorem heisenberg_coefficient (o : Fin 12) (i : Fin (BasisSize o)) (k : ℤ) :
    HVertexOperator.coeff (heisenbergField o i) k =
      HMT.IV.LatticeHeisenbergModes.hmode o i (-k-1) := rfl

theorem charged_local (o : Fin 12) (x y : Lattice o) :
    Local (chargedField o x) (chargedField o y) := by
  exact HMT.IV.LatticeChargedLocalityFull.charged_fields_locality o x y

theorem heisenberg_charged_localAt (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) :
    LocalAt 1 (heisenbergField o i) (chargedField o y) := by
  simpa only [LocalAt, pow_one] using
    HMT.IV.LatticeMixedLocality.heisenberg_charged_locality o i y

theorem heisenberg_charged_local (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) :
    Local (heisenbergField o i) (chargedField o y) :=
  ⟨1, heisenberg_charged_localAt o i y⟩

theorem heisenberg_localAt (o : Fin 12) (i j : Fin (BasisSize o)) :
    LocalAt 2 (heisenbergField o i) (heisenbergField o j) := by
  unfold LocalAt
  simp only [pow_succ, pow_zero, mul_one, Module.End.mul_apply, Module.End.one_apply]
  funext k l
  simp only [crossing, LinearMap.coe_mk, AddHom.coe_mk, forward, backward,
    heisenberg_coefficient]
  have h := heisenbergField_locality_order_two o i j (-k-1) (-l-1)
  unfold orderTwoLocalityCoefficient at h
  have a : -(k-1-1)-1=(-k-1)+2 := by omega
  have b : -(k-1)-1=(-k-1)+1 := by omega
  have c : -(l-1-1)-1=(-l-1)+2 := by omega
  have d : -(l-1)-1=(-l-1)+1 := by omega
  rw [a,b,c,d]
  simp only [Module.End.mul_eq_comp]
  apply sub_eq_zero.mp
  convert h using 1
  simp only [two_smul]
  abel

theorem heisenberg_local (o : Fin 12) (i j : Fin (BasisSize o)) :
    Local (heisenbergField o i) (heisenbergField o j) :=
  ⟨2, heisenberg_localAt o i j⟩

end HMT.IV.LatticeGeneratorLocality
end

#print axioms HMT.IV.LatticeGeneratorLocality.charged_local
#print axioms HMT.IV.LatticeGeneratorLocality.heisenberg_charged_localAt
#print axioms HMT.IV.LatticeGeneratorLocality.heisenberg_localAt
