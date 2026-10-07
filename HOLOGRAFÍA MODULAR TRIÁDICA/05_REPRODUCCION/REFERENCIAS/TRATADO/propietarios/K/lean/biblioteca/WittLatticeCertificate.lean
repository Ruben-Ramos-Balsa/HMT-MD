import MarkedNeighborSelfDual
import MarkedNeighborMinimum
import MarkedNeighborRank

/-!
The explicit ternary code and marked neighbour now supply the lattice
properties used in the manuscript before its classification step. Every
conjunct below is discharged by the construction; none is an input field.
This endpoint does not formalize lattice classification or FLM/Moonshine.
-/
namespace HMT.IV.WittLatticeCertificate

open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum
open HMT.IV.NeighborRank

theorem pairing_positive_on_nonzero (x : Space 12) (hx : x ≠ 0) :
    0 < pairing x x :=
  lt_of_le_of_ne (pairing_self_nonneg x)
    (Ne.symm (fun h => hx ((pairing_self_eq_zero_iff x).mp h)))

/-- A complete conjunction of the lattice properties at every marked origin,
before any isometry classification or vertex-operator construction. -/
theorem explicit_marked_lattice_properties (o : Fin 12) :
    Module.Finite ℤ (neighborSubgroup wittCode (radial (marked o))) ∧
    Module.Free ℤ (neighborSubgroup wittCode (radial (marked o))) ∧
    Module.finrank ℤ (neighborSubgroup wittCode (radial (marked o))) = 24 ∧
    Module.finrank ℚ
      (Submodule.span ℚ (neighbor wittCode (radial (marked o)))) = 24 ∧
    (∀ x : Space 12, x ≠ 0 → 0 < pairing x x) ∧
    EvenNeighbor wittCode (radial (marked o)) ∧
    IntegralNeighbor wittCode (radial (marked o)) ∧
    integralDual (neighborSubgroup wittCode (radial (marked o))) =
      neighbor wittCode (radial (marked o)) ∧
    (∀ x ∈ neighbor wittCode (radial (marked o)), x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode (radial (marked o)), pairing x x = 4) :=
  ⟨witt_marked_module_finite o, witt_marked_module_free o,
    witt_marked_integer_rank o,
    witt_marked_rational_dimension o, pairing_positive_on_nonzero,
    witt_marked_neighbor_even o, witt_marked_neighbor_integral o,
    witt_marked_neighbor_selfDual o,
    witt_marked_norm_ge_four o, witt_marked_has_norm_four o⟩

/-- The inherited oriented ternary action remains on that same neighbour. -/
theorem explicit_marked_lattice_symmetry (o : Fin 12) (x : Space 12) :
    (action wittOrientation x ∈ neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o))) ∧
    action wittOrientation (action wittOrientation (action wittOrientation x)) = x ∧
    (action wittOrientation x = x ↔ x = 0) ∧
    pairing (action wittOrientation x) (action wittOrientation x) = pairing x x :=
  ⟨(witt_marked_neighbor_symmetry o).2.2.2 x, action_cube _ _,
    action_fixed_iff _ _, action_pairing _ _ _⟩

#print axioms pairing_positive_on_nonzero
#print axioms explicit_marked_lattice_properties
#print axioms explicit_marked_lattice_symmetry

end HMT.IV.WittLatticeCertificate
