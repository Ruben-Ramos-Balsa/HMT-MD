import LatticePositiveMixedFields
import LatticeNegativeMixedFields

/-! The mixed Heisenberg/charged-field commutator in every integer mode.
The positive, zero and negative cases are proved on the original fields and
are combined here; no commutator identity is an assumption of the theorem. -/
noncomputable section
namespace HMT.IV.LatticeAllMixedFields

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeCocycle
open HMT.IV.LatticeChargedVertexField HMT.IV.LatticeHeisenbergModes
open HMT.IV.LatticePositiveMixedFields HMT.IV.LatticeNegativeMixedFields

theorem heisenberg_field_commutator (o : Fin 12)
    (i : Fin (BasisSize o)) (y : Lattice o) (m k : ℤ) :
    hmode o i m * fieldCoefficient o y k -
      fieldCoefficient o y k * hmode o i m =
        (integerPair o (latticeBasis o i) y : ℂ) • fieldCoefficient o y (k-m) := by
  cases m with
  | ofNat n =>
    cases n with
    | zero => simpa using zero_heisenberg_field_commutator o i y k
    | succ n => simpa using positive_heisenberg_field_commutator o i y n k
  | negSucc n =>
    have hk : k-Int.negSucc n = k+((n+1:ℕ):ℤ) := by omega
    rw [hk, hmode_negSucc]
    simpa only [chargeCreation_basis] using
      negative_mode_field_commutator o (latticeBasis o i) y n k

end HMT.IV.LatticeAllMixedFields
end

#print axioms HMT.IV.LatticeAllMixedFields.heisenberg_field_commutator
