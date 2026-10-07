import LatticeDongLocality
import LatticeGeneratorLocality
import LatticeStateFieldCoherence

/-!
Mutual locality on the entire previously constructed lattice carrier.
The three inductions use the actual normal-product closure: first against
Heisenberg generators, then against charged fields, and finally between
arbitrary oscillator descendants. Linear extension uses the existing
carrier basis and does not impose any finite energy cutoff.
-/

noncomputable section
namespace HMT.IV.LatticeDescendantLocality

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeFockMonomialParity HMT.IV.LatticeDescendantFields
open HMT.IV.LatticeFieldLocality HMT.IV.LatticeGeneratorLocality
open HMT.IV.LatticeHeisenbergField HMT.IV.LatticeChargedVertexField
open HMT.IV.LatticeDongLocality HMT.IV.LatticeStateFieldMap

theorem heisenberg_descendant_local (o : Fin 12) (x : Lattice o)
    (w : List (Mode o)) : ∀ i : Fin (BasisSize o),
      Local (heisenbergField o i) (descendantField o x w) := by
  induction w with
  | nil => exact fun i => heisenberg_charged_local o i x
  | cons m w ih =>
    intro i
    apply local_symm
    exact normalField_local o m.2 m.1 _ _
      (heisenberg_local o m.2 i) (local_symm (ih i)) (ih m.2)

theorem charged_descendant_local (o : Fin 12) (x y : Lattice o)
    (w : List (Mode o)) : Local (chargedField o x) (descendantField o y w) := by
  induction w with
  | nil => exact charged_local o x y
  | cons m w ih =>
    apply local_symm
    exact normalField_local o m.2 m.1 _ _
      (heisenberg_charged_local o m.2 x) (local_symm ih)
      (heisenberg_descendant_local o y w m.2)

theorem descendant_fields_local (o : Fin 12) (x y : Lattice o)
    (u v : List (Mode o)) : Local (descendantField o x u) (descendantField o y v) := by
  induction u with
  | nil => exact charged_descendant_local o x y v
  | cons m u ih =>
    exact normalField_local o m.2 m.1 _ _
      (heisenberg_descendant_local o y v m.2) ih
      (heisenberg_descendant_local o x u m.2)

/-- Linearity extends locality from a basis, because each vector has a
finite basis expansion. Different pairs may have different locality orders. -/
theorem local_linear_extension {W V ι : Type*}
    [AddCommGroup W] [Module ℂ W] [AddCommGroup V] [Module ℂ V]
    (b : Basis ι ℂ W) (Y : W →ₗ[ℂ] VertexOperator ℂ V)
    (C : VertexOperator ℂ V) (h : ∀ i, Local (Y (b i)) C) (w : W) :
    Local (Y w) C := by
  let S : Submodule ℂ W :=
    { carrier := {v | Local (Y v) C}
      zero_mem' := by
        change Local (Y 0) C
        simpa only [map_zero] using local_zero_left C
      add_mem' := by
        intro v u hv hu
        change Local (Y (v+u)) C
        simpa only [map_add] using local_add_left hv hu
      smul_mem' := by
        intro c v hv
        change Local (Y (c • v)) C
        simpa only [map_smul] using local_smul_left c hv }
  have hrange : Set.range b ⊆ S := by
    rintro _ ⟨i,rfl⟩
    exact h i
  have hspan : Submodule.span ℂ (Set.range b) ≤ S := Submodule.span_le.mpr hrange
  rw [b.span_eq] at hspan
  exact hspan (Submodule.mem_top)

theorem stateField_basis_local (o : Fin 12)
    (a b : Occupation o) (x y : Lattice o) :
    Local (stateField o (carrierBasis o (a,x)))
      (stateField o (carrierBasis o (b,y))) := by
  rw [stateField_basis, stateField_basis]
  exact descendant_fields_local o x y _ _

/-- Mutual locality of the constructed state-field map on every pair
of states of M(1) tensor C_epsilon[Lambda]. The result follows from the
original generator localities and the proved residue construction. -/
theorem stateField_local (o : Fin 12) (u v : LatticeCarrier o) :
    Local (stateField o u) (stateField o v) := by
  apply local_linear_extension (carrierBasis o) (stateField o) (stateField o v) _ u
  rintro ⟨a,x⟩
  apply local_symm
  apply local_linear_extension (carrierBasis o) (stateField o)
    (stateField o (carrierBasis o (a,x))) _ v
  rintro ⟨b,y⟩
  exact stateField_basis_local o b a y x

end HMT.IV.LatticeDescendantLocality
end

#print axioms HMT.IV.LatticeDescendantLocality.heisenberg_descendant_local
#print axioms HMT.IV.LatticeDescendantLocality.charged_descendant_local
#print axioms HMT.IV.LatticeDescendantLocality.descendant_fields_local
#print axioms HMT.IV.LatticeDescendantLocality.local_linear_extension
#print axioms HMT.IV.LatticeDescendantLocality.stateField_basis_local
#print axioms HMT.IV.LatticeDescendantLocality.stateField_local
