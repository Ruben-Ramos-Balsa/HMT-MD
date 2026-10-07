import CoxeterChargeCovariance
import LatticeCoxeterFieldCovariance
import SelectedMixedFieldLocality

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.IV.LatticeCoxeterFock HMT.IV.LatticeCoxeterTwistedLift
open HMT.IV.LatticeZeroModes HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeChargedVertexField HMT.IV.CoxeterChargeCovariance
open HMT.IV.LatticeCoxeterFieldCovariance

example (o : Fin 12) : orderOf (carrierEquiv o) = 3 := carrierEquiv_order o

example (o : Fin 12) (x : Lattice o) (f : TwistedAlgebra o) :
    twistedEquiv o (latticeShift o x f) =
      phase o x • latticeShift o (latticeAction o x) (twistedEquiv o f) :=
  twisted_shift o x f

example (o : Fin 12) (x : Lattice o) (v : LatticeCarrier o) :
    carrierEquiv o (onCharge o (zeroMode o x) v) =
      onCharge o (zeroMode o (latticeAction o x)) (carrierEquiv o v) :=
  carrier_zeroMode o x v

example (o : Fin 12) (x : Lattice o) (k : ℤ) :
    (carrierEquiv o).toLinearMap.comp (fieldCoefficient o x k) =
      phase o x • ((fieldCoefficient o (latticeAction o x) k).comp
        (carrierEquiv o).toLinearMap) :=
  carrierEquiv_fieldCoefficient o x k

example (o : Fin 12) (x : Lattice o) (k : ℤ) (v : LatticeCarrier o) :
    carrierEquiv o (fieldCoefficient o x k ((carrierEquiv o).symm v)) =
      phase o x • fieldCoefficient o (latticeAction o x) k v :=
  carrierEquiv_conjugates_field o x k v

-- The new symmetry acts at the same selected origin as the proved mixed fields.
open HMT.I.SelectedRegionalIncidence HMT.I.SelectedMixedFieldLocality

example : SelectedMixedLocalityPublication ∧
    orderOf (carrierEquiv selectedOrigin) = 3 ∧
    ∀ (x : Lattice selectedOrigin) (k : ℤ) (v : LatticeCarrier selectedOrigin),
      carrierEquiv selectedOrigin
        (fieldCoefficient selectedOrigin x k ((carrierEquiv selectedOrigin).symm v)) =
        phase selectedOrigin x •
          fieldCoefficient selectedOrigin (latticeAction selectedOrigin x) k v :=
  ⟨selected_mixed_fields_locality, carrierEquiv_order selectedOrigin,
    carrierEquiv_conjugates_field selectedOrigin⟩
