import IncidenceRegister
import AlphaTightBounds
import VacancyDeltaBounds

/-!
Composition from the incidence ledger to the correlated alpha publications.
The register is evaluated by IncidenceRegister.register, not supplied as an
independent numeric parameter. Generic theorems expose the vacancy enclosure;
the final corollaries discharge it from the logarithmic vacancy reader. The
identification of the particular terminal ledger remains an explicit interface.

No theorem here claims that an arbitrary ledger is the terminal TPK ledger.
The analytic chart is the correlated chart of the same state, not an
independent selection of that state. All previous proofs are imported.
-/

noncomputable section

namespace AlphaIncidencePublications

open HMT.IncidenceRegister

def PublishedRegister (l : Ledger) : Prop :=
  (register l).digits = [234,543,140,729,659,824,621,58,914,794,146,601]

theorem root_from_incidence (l : Ledger) (hl : PublishedRegister l)
    (delta : ℝ) (hdL : AlphaStateLinkBound.deltaLower < delta)
    (hdU : delta < AlphaStateLinkBound.deltaUpper) :
    ∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart (register l) delta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication (register l) n).outgoing = 0 ∧
        (AlphaPublications.publication (register l) n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat) := by
  have hk := AlphaSourceBounds.periodic_in_unit (register l) hl
  have ha := AlphaSourceBounds.precoordinate_bounds (register l) hl
  have hlink := AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
    (register l) hl delta hdL hdU
  exact AlphaPublications.unique_root_with_all_publications
    (register l) delta hk ha.1 ha.2 hlink

theorem canonical_readout_all_depths (l : Ledger) (hl : PublishedRegister l)
    (delta : ℝ) (hdL : AlphaStateLinkBound.deltaLower < delta)
    (hdU : delta < AlphaStateLinkBound.deltaUpper) (n : Nat) :
    (AlphaPublications.publication (register l) n).outgoing = 0 ∧
      (AlphaPublications.publication (register l) n).digits =
        (AlphaCanonicalSection.digits
          (AlphaAnalyticChart.precoordinate (register l)) (12*n)).map Int.ofNat := by
  have hk := AlphaSourceBounds.periodic_in_unit (register l) hl
  have ha := AlphaSourceBounds.precoordinate_bounds (register l) hl
  have hlink := AlphaTightBounds.stateLink_bound_of_vacancy_enclosure
    (register l) hl delta hdL hdU
  have hroot := (AlphaAnalyticChart.state_chart_simple_root
    (register l) delta ha.1 ha.2 hlink).1
  exact AlphaPublications.root_publication (register l) delta _ hk ha.1 ha.2
    hlink ⟨ha.1, ha.2⟩ hroot n

theorem compatible_readouts_all_depths (l : Ledger) (hl : PublishedRegister l)
    (delta : ℝ) (hdL : AlphaStateLinkBound.deltaLower < delta)
    (hdU : delta < AlphaStateLinkBound.deltaUpper) (n m : Nat) :
    ((AlphaPublications.publication (register l) (n+m)).digits).take (12*n) =
      (AlphaPublications.publication (register l) n).digits := by
  rw [(canonical_readout_all_depths l hl delta hdL hdU (n+m)).2,
      (canonical_readout_all_depths l hl delta hdL hdU n).2,
      ← List.map_take, Nat.mul_add, AlphaCanonicalSection.digits_compatible]

theorem incidence_recovery_and_root (l : Ledger) (hl : PublishedRegister l)
    (delta : ℝ) (hdL : AlphaStateLinkBound.deltaLower < delta)
    (hdU : delta < AlphaStateLinkBound.deltaUpper) :
    RadixRecovery.decode 1000 12 (register l).publish = (register l).digits ∧
    (∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart (register l) delta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication (register l) n).outgoing = 0 ∧
        (AlphaPublications.publication (register l) n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat)) :=
  ⟨register_recovery l, root_from_incidence l hl delta hdL hdU⟩

theorem root_from_vacancy_readout (l : Ledger) (hl : PublishedRegister l) :
    ∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart (register l) VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication (register l) n).outgoing = 0 ∧
        (AlphaPublications.publication (register l) n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat) :=
  root_from_incidence l hl VacancyDeltaBounds.vacancyDelta
    VacancyDeltaBounds.vacancyDelta_enclosure.1
    VacancyDeltaBounds.vacancyDelta_enclosure.2

theorem compatible_publications_from_vacancy_readout
    (l : Ledger) (hl : PublishedRegister l) (n m : Nat) :
    ((AlphaPublications.publication (register l) (n+m)).digits).take (12*n) =
      (AlphaPublications.publication (register l) n).digits :=
  compatible_readouts_all_depths l hl VacancyDeltaBounds.vacancyDelta
    VacancyDeltaBounds.vacancyDelta_enclosure.1
    VacancyDeltaBounds.vacancyDelta_enclosure.2 n m

theorem recovery_and_vacancy_root (l : Ledger) (hl : PublishedRegister l) :
    RadixRecovery.decode 1000 12 (register l).publish = (register l).digits ∧
    (∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart (register l) VacancyDeltaBounds.vacancyDelta x = 0 ∧
      (∀ n : Nat, (AlphaPublications.publication (register l) n).outgoing = 0 ∧
        (AlphaPublications.publication (register l) n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat)) :=
  ⟨register_recovery l, root_from_vacancy_readout l hl⟩

end AlphaIncidencePublications

#print axioms AlphaIncidencePublications.root_from_incidence
#print axioms AlphaIncidencePublications.canonical_readout_all_depths
#print axioms AlphaIncidencePublications.compatible_readouts_all_depths
#print axioms AlphaIncidencePublications.incidence_recovery_and_root
#print axioms AlphaIncidencePublications.root_from_vacancy_readout
#print axioms AlphaIncidencePublications.compatible_publications_from_vacancy_readout
#print axioms AlphaIncidencePublications.recovery_and_vacancy_root
