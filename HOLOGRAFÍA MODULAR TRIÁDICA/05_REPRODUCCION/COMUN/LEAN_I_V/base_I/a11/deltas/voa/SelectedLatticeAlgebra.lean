import SharedArticleIBase
import WittComplexAlgebra

/-!
The cocycle, central extension and twisted complex group algebra are attached
to the same marked origin already selected by the Article I incidence reader.
The seven algebra modules are reused unchanged. No new register, incidence
flag, cocycle, associativity law, or FLM theorem is accepted as an input.

This is the lattice/group-algebra portion of the vertex construction. It does
not identify that associative algebra with the full vertex operator algebra.
The upstream S8 input and native finite selector retain their recorded scope.
-/

noncomputable section
namespace HMT.I.SelectedLatticeAlgebra

open HMT.I.SelectedRegionalIncidence
open HMT.IV.CoxeterNeighbor
open HMT.IV.LatticeCocycle
open HMT.IV.TwistedGroupAlgebra

/-- The carrier is definitionally the marked lattice in the common entry. -/
abbrev SelectedLattice := Lattice selectedOrigin

abbrev SelectedCentralExtension := Extension selectedOrigin

abbrev SelectedTwistedAlgebra := TwistedAlgebra selectedOrigin

theorem selected_lattice_is_same_carrier :
    SelectedLattice = neighborSubgroup wittCode selectedRadial := rfl

/-- The marked point is recovered from the register/incidence construction. -/
theorem selected_origin_is_registered :
    selectedOriginSupport = {selectedOrigin} :=
  selected_incidence_lattice_properties.2.2.1

theorem selected_cocycle_commutator (x y : SelectedLattice) :
    wittSign selectedOrigin x y * wittSign selectedOrigin y x =
      HMT.IV.TriangularCocycle.sign (integerPair selectedOrigin x y : ZMod 2) :=
  wittSign_commutator selectedOrigin x y

theorem selected_central_extension :
    Function.Injective (centralEmbedding selectedOrigin) ∧
    Function.Surjective (latticeProjection selectedOrigin) ∧
    (∀ a : SelectedCentralExtension,
      latticeProjection selectedOrigin a = 1 ↔
        ∃ s, a = centralEmbedding selectedOrigin s) ∧
    (∀ (s : Multiplicative (ZMod 2)) (a : SelectedCentralExtension),
      centralEmbedding selectedOrigin s * a = a * centralEmbedding selectedOrigin s) :=
  ⟨centralEmbedding_injective selectedOrigin,
    latticeProjection_surjective selectedOrigin,
    latticeProjection_kernel selectedOrigin,
    centralEmbedding_commutes selectedOrigin⟩

theorem selected_algebra_product (x y : SelectedLattice) :
    basisElement selectedOrigin x * basisElement selectedOrigin y =
      epsilon selectedOrigin x y • basisElement selectedOrigin (x+y) :=
  twisted_basis_product selectedOrigin x y

theorem selected_algebra_laws :
    (∀ a b c : SelectedTwistedAlgebra, (a*b)*c = a*(b*c)) ∧
    (∀ a : SelectedTwistedAlgebra, 1*a = a ∧ a*1 = a) ∧
    (∀ x y : SelectedLattice,
      basisElement selectedOrigin x * basisElement selectedOrigin y =
        epsilon selectedOrigin x y • basisElement selectedOrigin (x+y)) :=
  ⟨fun a b c => mul_assoc a b c,
    fun a => ⟨one_mul a, mul_one a⟩, selected_algebra_product⟩

/-- The selected reticular endpoint and its algebraic continuation coexist
on exactly the same origin. The register is not supplied a second time. -/
theorem selected_incidence_central_extension_algebra :
    HMT.Shared.ArticleI.IncidenceLatticePublication ∧
    Function.Injective (centralEmbedding selectedOrigin) ∧
    Function.Surjective (latticeProjection selectedOrigin) ∧
    (∀ a : SelectedCentralExtension,
      latticeProjection selectedOrigin a = 1 ↔
        ∃ s, a = centralEmbedding selectedOrigin s) ∧
    (∀ x y : SelectedLattice,
      basisElement selectedOrigin x * basisElement selectedOrigin y =
        epsilon selectedOrigin x y • basisElement selectedOrigin (x+y)) ∧
    (∀ a b c : SelectedTwistedAlgebra, (a*b)*c = a*(b*c)) :=
  ⟨selected_incidence_lattice_properties,
    selected_central_extension.1, selected_central_extension.2.1,
    selected_central_extension.2.2.1, selected_algebra_product,
    selected_algebra_laws.1⟩

end HMT.I.SelectedLatticeAlgebra
end

#print axioms HMT.I.SelectedLatticeAlgebra.selected_lattice_is_same_carrier
#print axioms HMT.I.SelectedLatticeAlgebra.selected_origin_is_registered
#print axioms HMT.I.SelectedLatticeAlgebra.selected_cocycle_commutator
#print axioms HMT.I.SelectedLatticeAlgebra.selected_central_extension
#print axioms HMT.I.SelectedLatticeAlgebra.selected_algebra_product
#print axioms HMT.I.SelectedLatticeAlgebra.selected_algebra_laws
#print axioms HMT.I.SelectedLatticeAlgebra.selected_incidence_central_extension_algebra
