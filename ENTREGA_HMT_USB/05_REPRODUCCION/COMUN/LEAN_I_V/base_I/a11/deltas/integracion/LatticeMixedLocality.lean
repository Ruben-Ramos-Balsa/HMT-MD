import LatticeMixedLocalityCriterion
import LatticeAllMixedFields

/-!
Mixed locality for the actual Heisenberg and charged fields of the previously
constructed lattice realization. The integer-mode relation is a proved
theorem on these fields, not an axiom or an input to the result below.
The lattice, pairing, charge, basis and Fock carrier are unchanged.
-/
noncomputable section
namespace HMT.IV.LatticeMixedLocality

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticeFactorConvolution HMT.IV.LatticeMixedLocalityCriterion

theorem heisenberg_charged_locality (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) :
    crossing (mixedForward (hmode o i) (fieldCoefficient o y)) =
      crossing (mixedBackward (hmode o i) (fieldCoefficient o y)) := by
  exact mixed_locality_of_mode_relation (hmode o i) (fieldCoefficient o y)
    (integerPair o (latticeBasis o i) y : ℂ)
    (HMT.IV.LatticeAllMixedFields.heisenberg_field_commutator o i y)

end HMT.IV.LatticeMixedLocality
end

#print axioms HMT.IV.LatticeMixedLocality.heisenberg_charged_locality
