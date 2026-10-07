import LatticeTwistedNormalDerivative
import LatticeTwistedRawChargeField
import LatticeOscillatorWords

/-! Construct the uncorrected W-map on the entire existing lattice carrier.
Its basis is the inherited oscillator occupation and lattice charge, not a new
input state space. Each finite oscillator word is evaluated using the divided
z-derivatives of the actual half-integer fields, with z=t². The map is extended
linearly from the existing basis. The correction exp(Delta_z) is composed in a
separate module; no twisted Jacobi or orbifold multiplication is postulated here.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedRawStateField
open LatticeCocycle LatticeOscillatorFock LatticeFockMonomialParity
open LatticeOscillatorWords LatticeTwistedCarrier
open LatticeTwistedRawChargeField LatticeTwistedNormalDerivative
open scoped TensorProduct

def rawDescendantField (o : Fin 12) (x : Lattice o) :
    List (Mode o) → VertexOperator ℂ (Carrier o)
  | [] => rawChargeField o x
  | m :: w => derivativeNormalField o m.2 m.1 (rawDescendantField o x w)

theorem rawDescendantField_nil (o : Fin 12) (x : Lattice o) :
    rawDescendantField o x [] = rawChargeField o x := rfl

theorem rawDescendantField_cons (o : Fin 12) (x : Lattice o)
    (m : Mode o) (w : List (Mode o)) :
    rawDescendantField o x (m::w) =
      derivativeNormalField o m.2 m.1 (rawDescendantField o x w) := rfl

def rawStateField (o : Fin 12) :
    LatticeCarrier o →ₗ[ℂ] VertexOperator ℂ (Carrier o) :=
  (carrierBasis o).constr ℂ
    (fun p => rawDescendantField o p.2 (wordForOccupation o p.1))

theorem rawStateField_basis (o : Fin 12) (a : Occupation o) (x : Lattice o) :
    rawStateField o (carrierBasis o (a,x)) =
      rawDescendantField o x (wordForOccupation o a) :=
  Basis.constr_basis _ _ _ _

theorem rawStateField_pure_charge (o : Fin 12) (x : Lattice o) :
    rawStateField o (carrierBasis o (0,x)) = rawChargeField o x := by
  rw [rawStateField_basis, wordForOccupation_zero, rawDescendantField_nil]

theorem rawStateField_ground_state (o : Fin 12) (x : Lattice o) :
    rawStateField o ((1 : Fock o) ⊗ₜ[ℂ] TwistedGroupAlgebra.basisElement o x) =
      rawChargeField o x := by
  have h := stateForWord_basis o [] x
  simpa only [stateForWord, wordOccupation, rawStateField_pure_charge] using
    congrArg (rawStateField o) h

theorem rawStateField_vacuum (o : Fin 12) :
    rawStateField o (vacuum o) = rawChargeField o 0 := by
  rw [← vacuum_is_empty_monomial, rawStateField_pure_charge]

theorem rawStateField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (rawStateField o (vacuum o)) k =
      if k=0 then (1 : Module.End ℂ (Carrier o)) else 0 := by
  rw [rawStateField_vacuum, rawChargeField_zero_charge]

theorem rawStateField_laurent_bound (o : Fin 12)
    (v : LatticeCarrier o) (w : Carrier o) :
    ∃ b : ℤ, ∀ k < b, HVertexOperator.coeff (rawStateField o v) k w = 0 :=
  LatticeTwistedNormalProduct.field_has_bound o (rawStateField o v) w

theorem wordForOccupation_single (o : Fin 12) (m : Mode o) :
    wordForOccupation o (Finsupp.single m 1) = [m] := by
  simp only [wordForOccupation, Finsupp.toMultiset_single,
    one_nsmul, Multiset.toList_singleton]

theorem rawStateField_one_oscillator (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (x : Lattice o) :
    rawStateField o (carrierBasis o (Finsupp.single (n,i) 1,x)) =
      derivativeNormalField o i n (rawChargeField o x) := by
  rw [rawStateField_basis, wordForOccupation_single]
  rfl

end HMT.IV.LatticeTwistedRawStateField
end

#print axioms HMT.IV.LatticeTwistedRawStateField.rawDescendantField
#print axioms HMT.IV.LatticeTwistedRawStateField.rawDescendantField_nil
#print axioms HMT.IV.LatticeTwistedRawStateField.rawDescendantField_cons
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_basis
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_pure_charge
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_ground_state
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_vacuum
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_vacuum_coefficient
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_laurent_bound
#print axioms HMT.IV.LatticeTwistedRawStateField.wordForOccupation_single
#print axioms HMT.IV.LatticeTwistedRawStateField.rawStateField_one_oscillator
