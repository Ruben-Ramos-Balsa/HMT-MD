import SectorIncidenceData
import IncidenceRegister

/-!
Recovered article-I incidence selector, in the exact Paley chart of
`excepcional.tex`. No point is chosen by fiat: the singleton is proved from
the four published regional words, the register high-block support and the
unique hexad satisfying the source incidence rule. Fin coordinates are 0-based.

The antecedent identification of the terminal ledger is explicit. The four
regional words are the published finite words at this cut, not decimal or
metrological selectors. Their earlier TPK selection is not proved here.
-/
namespace HMT.I.KMarkedIncidence

open HMT.IV.CoxeterNeighbor HMT.IncidenceRegister
open HMT.II.CKM.Incidence

set_option maxHeartbeats 8000000
set_option maxRecDepth 8000

def autoscaleWord : Fin 6 → ZMod 3 := ![1, 2, 1, 2, 0, 0]
def appWord : Fin 6 → ZMod 3 := ![0, 2, 2, 0, 2, 0]
def autoscaleSupport := wordSupport autoscaleWord
def appSupport := wordSupport appWord

theorem autoscale_support_exact :
    autoscaleSupport = {0, 1, 2, 3, 6, 8} := by decide +kernel
theorem app_support_exact :
    appSupport = {1, 2, 4, 9, 10, 11} := by decide +kernel

def registerHighSupport (l : Ledger) : Finset (Fin 12) :=
  Finset.univ.filter fun i => 729 ≤ (register l).digits[i.val]!

theorem register_high_support (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    registerHighSupport l = markedFace := by
  unfold registerHighSupport
  rw [hl, marked_face_exact]
  decide +kernel

def alphaHexad : Finset (Fin 12) := {3, 4, 5, 6, 8, 9}

def incidenceRule (h : Finset (Fin 12)) : Prop :=
  h.card = 6 ∧ markedFace ⊆ h ∧ h ⊆ closureSupport ∧
    (h ∩ hexadSupport).card = 4 ∧
    (h ∩ autoscaleSupport).card = 3 ∧ (h ∩ appSupport).card = 2

instance (h : Finset (Fin 12)) : Decidable (incidenceRule h) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

theorem alpha_incidence_rule : incidenceRule alphaHexad := by decide +kernel

/-- This finite theorem checks precisely the encoder image, not all anonymous
six-element subsets. It is the two-selector theorem of the manuscript. -/
theorem selected_hexad_unique :
    ∀ w : Fin 6 → ZMod 3, incidenceRule (wordSupport w) →
      wordSupport w = alphaHexad := by decide +kernel

theorem selected_hexad_exists :
    ∃ w : Fin 6 → ZMod 3, wordSupport w = alphaHexad := by decide +kernel

theorem selected_hexad_existsUnique :
    ∃! h : Finset (Fin 12), (∃ w, wordSupport w = h) ∧ incidenceRule h := by
  refine ⟨alphaHexad, ⟨selected_hexad_exists, alpha_incidence_rule⟩, ?_⟩
  rintro h ⟨⟨w, rfl⟩, hh⟩
  exact selected_hexad_unique w hh

def preCarry : Fin 12 → ℤ :=
  ![7, 297, 353, -430, -715, -1199, -3, 286, -894, -528, 380, 663]
def negativeSupport : Finset (Fin 12) := Finset.univ.filter fun i => preCarry i < 0

theorem signed_support_exact : negativeSupport = alphaHexad := by decide +kernel

/-- The mark is an incidence output. The display coordinate 1 is index 0. -/
def originSupport : Finset (Fin 12) :=
  (hexadSupport ∩ autoscaleSupport) \ (alphaHexad ∪ appSupport)

theorem origin_support_exact : originSupport = {0} := by decide +kernel

def origin : Fin 12 := originSupport.min' (by rw [origin_support_exact]; simp)

theorem origin_eq_zero : origin = 0 := by
  have h := Finset.min'_mem originSupport
    (show originSupport.Nonempty by rw [origin_support_exact]; simp)
  change origin ∈ originSupport at h
  rw [origin_support_exact] at h
  exact Finset.mem_singleton.mp h

theorem origin_displayed : origin.val + 1 = 1 := by rw [origin_eq_zero]; rfl

theorem selected_origin_from_register (l : Ledger)
    (hl : (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]) :
    registerHighSupport l = markedFace ∧
    incidenceRule alphaHexad ∧ negativeSupport = alphaHexad ∧
    originSupport = {origin} := by
  exact ⟨register_high_support l hl, alpha_incidence_rule, signed_support_exact,
    by rw [origin_eq_zero, origin_support_exact]⟩

/-- Incidence selection commutes with relabeling: a bijection transports the
selected singleton, not the literal numeral used by its original chart. -/
theorem origin_relabel (g : Equiv.Perm (Fin 12)) :
    originSupport.image g = {g origin} := by
  rw [origin_support_exact, origin_eq_zero, Finset.image_singleton]

#print axioms autoscale_support_exact
#print axioms app_support_exact
#print axioms register_high_support
#print axioms alpha_incidence_rule
#print axioms selected_hexad_unique
#print axioms selected_hexad_exists
#print axioms selected_hexad_existsUnique
#print axioms signed_support_exact
#print axioms origin_support_exact
#print axioms origin_eq_zero
#print axioms selected_origin_from_register
#print axioms origin_relabel

end HMT.I.KMarkedIncidence
