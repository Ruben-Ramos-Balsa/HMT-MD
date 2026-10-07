import KMarkedIncidence
import WittLatticeCertificate

/-! The existing universal marked-lattice theorem, applied to the mark actually
selected by the article-I incidence rule. No classification or VOA theorem is
postulated. The earlier publication contract stays visible. -/
namespace HMT.I.KSelectedLattice

open HMT.I.KMarkedIncidence HMT.IncidenceRegister
open HMT.II.CKM.Incidence
open HMT.IV.CoxeterNeighbor HMT.IV.GlueDuality
open HMT.IV.NeighborSpan HMT.IV.NeighborLattice
open HMT.IV.NeighborDuality HMT.IV.NeighborMinimum HMT.IV.NeighborRank

def selectedRadial : Space 12 := radial (marked origin)

theorem selected_radial_coordinates (i : Fin 12) :
    selectedRadial i = if i = origin then (4,4) else (1,1) := by
  by_cases h : i = origin <;> norm_num [selectedRadial, radial, marked, h]

theorem selected_radial_norm : pairing selectedRadial selectedRadial = 54 := by
  rw [show selectedRadial = radial (marked 0) by rw [selectedRadial, origin_eq_zero]]
  decide +kernel

theorem selected_lattice_properties :
    Module.Finite ℤ (neighborSubgroup wittCode selectedRadial) ∧
    Module.Free ℤ (neighborSubgroup wittCode selectedRadial) ∧
    Module.finrank ℤ (neighborSubgroup wittCode selectedRadial) = 24 ∧
    Module.finrank ℚ (Submodule.span ℚ (neighbor wittCode selectedRadial)) = 24 ∧
    (∀ x : Space 12, x ≠ 0 → 0 < pairing x x) ∧
    EvenNeighbor wittCode selectedRadial ∧
    IntegralNeighbor wittCode selectedRadial ∧
    integralDual (neighborSubgroup wittCode selectedRadial) = neighbor wittCode selectedRadial ∧
    (∀ x ∈ neighbor wittCode selectedRadial, x ≠ 0 → 4 ≤ pairing x x) ∧
    (∃ x ∈ neighbor wittCode selectedRadial, pairing x x = 4) :=
  HMT.IV.WittLatticeCertificate.explicit_marked_lattice_properties origin

theorem register_to_selected_lattice (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    registerHighSupport l = markedFace ∧
    originSupport = {origin} ∧ pairing selectedRadial selectedRadial = 54 ∧
    Module.finrank ℤ (neighborSubgroup wittCode selectedRadial) = 24 ∧
    IntegralNeighbor wittCode selectedRadial ∧
    integralDual (neighborSubgroup wittCode selectedRadial) = neighbor wittCode selectedRadial ∧
    (∀ x ∈ neighbor wittCode selectedRadial, x ≠ 0 → 4 ≤ pairing x x) := by
  exact ⟨register_high_support l hl, (selected_origin_from_register l hl).2.2.2,
    selected_radial_norm, selected_lattice_properties.2.2.1,
    selected_lattice_properties.2.2.2.2.2.2.1,
    selected_lattice_properties.2.2.2.2.2.2.2.1,
    selected_lattice_properties.2.2.2.2.2.2.2.2.1⟩

#print axioms selected_radial_coordinates
#print axioms selected_radial_norm
#print axioms selected_lattice_properties
#print axioms register_to_selected_lattice

end HMT.I.KSelectedLattice
