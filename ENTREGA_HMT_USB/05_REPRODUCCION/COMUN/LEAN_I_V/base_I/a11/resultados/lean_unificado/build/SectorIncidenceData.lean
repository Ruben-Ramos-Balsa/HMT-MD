import CoxeterNeighbor
import RationalCKMChart
import TRITCore

/-!
Finite incidence data feeding the declared N42 angular sector system.

The Paley encoder is reused from the IV formalization, in exactly the same
row-vector and coordinate convention as II, 08j:121–140. The two regional
words are the published words at this cut; their earlier TPK selection is
not replaced here by a numerical CKM target. Supports and their cardinalities
are computed from the encoder, not postulated as independent coefficients.

The other three inputs retain the types and conditions printed in 08g and
N42: a five-point determination support, an eight-point support with a
distinguished hexad inclusion, and an oriented *point coordinate* 7.
This module does not choose an octad or pivot not selected by those sources.
-/

namespace HMT.II.CKM.Incidence

open HMT.IV.CoxeterNeighbor

noncomputable section

set_option maxHeartbeats 2000000

def closureWord : Fin 6 → ZMod 3 := ![0, 1, 0, 2, 1, 1]
def propagationWord : Fin 6 → ZMod 3 := ![2, 0, 1, 1, 0, 1]

def wordSupport (w : Fin 6 → ZMod 3) : Finset (Fin 12) :=
  Finset.univ.filter fun i => encode w i ≠ 0

def closureSupport : Finset (Fin 12) := wordSupport closureWord
def hexadSupport : Finset (Fin 12) := wordSupport propagationWord
def markedFace : Finset (Fin 12) := hexadSupport ∩ closureSupport

/-- Fin indices are zero-based; the manuscript displays coordinates 1–12. -/
theorem closure_support_exact :
    closureSupport = {1, 3, 4, 5, 6, 7, 8, 9, 10} := by decide +kernel

theorem hexad_support_exact :
    hexadSupport = {0, 2, 3, 5, 8, 9} := by decide +kernel

theorem marked_face_exact : markedFace = {3, 5, 8, 9} := by decide +kernel

def displayedPositions (s : Finset (Fin 12)) : Finset ℕ :=
  s.image fun i => i.val + 1

theorem marked_face_displayed : displayedPositions markedFace = {4, 6, 9, 10} :=
  by decide +kernel

theorem closure_card : closureSupport.card = 9 := by decide +kernel
theorem hexad_card : hexadSupport.card = 6 := by decide +kernel
theorem marked_face_card : markedFace.card = 4 := by decide +kernel

theorem marked_face_subset_hexad : markedFace ⊆ hexadSupport :=
  Finset.inter_subset_left

theorem marked_face_subset_closure : markedFace ⊆ closureSupport :=
  Finset.inter_subset_right

def tritAlphabet : Finset ℤ := Finset.Icc (-1) 1

theorem trit_mem_iff (r : ℤ) : r ∈ tritAlphabet ↔ -1 ≤ r ∧ r ≤ 1 := by
  simp [tritAlphabet]

theorem every_trit_digit (r : TRITCore.Digit) : r.val ∈ tritAlphabet :=
  (trit_mem_iff r.val).mpr r.property

theorem trit_values_exact (r : ℤ) :
    r ∈ tritAlphabet ↔ ∃ d : TRITCore.Digit, d.val = r := by
  constructor
  · intro h
    exact ⟨⟨r, (trit_mem_iff r).mp h⟩, rfl⟩
  · rintro ⟨d, rfl⟩
    exact every_trit_digit d

theorem trit_card : tritAlphabet.card = 3 := by decide +kernel

/-- The remaining marked incidence data of the published sector system.
The pivot is a point, never a fictitious seven-element support. The octad
is supplied with its distinguished inclusion, not constructed by a target
coefficient. The pentad records the stated determination order. -/
structure DeclaredSectorFrame where
  pentad : Finset (Fin 12)
  pentad_card : pentad.card = 5
  octad : Finset (Fin 24)
  octad_card : octad.card = 8
  hexadInclusion : {i // i ∈ hexadSupport} → {j // j ∈ octad}
  hexadInclusion_injective : Function.Injective hexadInclusion
  phiPivot : Fin 12
  phiPivot_coordinate : phiPivot.val + 1 = 7

def sextet (s : DeclaredSectorFrame) : Fin 6 → ℝ :=
  ![(markedFace.card : ℝ), (s.pentad.card : ℝ),
    ((s.phiPivot.val + 1 : ℕ) : ℝ), (hexadSupport.card : ℝ),
    (s.octad.card : ℝ), (tritAlphabet.card : ℝ)]

theorem sextet_evaluates (s : DeclaredSectorFrame) :
    sextet s = ![4, 5, 7, 6, 8, 3] := by
  simp [sextet, marked_face_card, hexad_card, trit_card,
    s.pentad_card, s.octad_card, s.phiPivot_coordinate]

def incidenceReader (s : DeclaredSectorFrame) (x : Vec3) : Vec3 :=
  sectorRules (sextet s 0) (sextet s 1) (sextet s 2)
    (sextet s 3) (sextet s 4) (sextet s 5) x

/-- Evaluation of the complete declared system after computing its finite
support data. It does not assert uniqueness of the choice of sector rules. -/
theorem incidence_reader_is_chart (s : DeclaredSectorFrame) (x : Vec3) :
    incidenceReader s x = chart x := by
  simp only [incidenceReader, sextet_evaluates, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.cons_val_two]
  exact sector_rules_evaluate x

theorem recover_incidence_reader (s : DeclaredSectorFrame) (x : Vec3) :
    recover (incidenceReader s x) = x := by
  rw [incidence_reader_is_chart, recover_chart]

theorem incidence_reader_injective (s : DeclaredSectorFrame) :
    Function.Injective (incidenceReader s) := by
  intro x y h
  have := congrArg recover h
  simpa only [recover_incidence_reader] using this

#print axioms closure_support_exact
#print axioms hexad_support_exact
#print axioms marked_face_exact
#print axioms marked_face_displayed
#print axioms marked_face_card
#print axioms hexad_card
#print axioms every_trit_digit
#print axioms trit_values_exact
#print axioms trit_card
#print axioms sextet_evaluates
#print axioms incidence_reader_is_chart
#print axioms recover_incidence_reader
#print axioms incidence_reader_injective

end

end HMT.II.CKM.Incidence
