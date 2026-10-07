import EventReconstruction
import TraceEvents

/-! Exact twelve-window event extraction from a supplied 108-step route.
The finite event counter is reused from Article II; no TPK is reimplemented. -/

namespace HMT.VI.RouteEvents

open scoped BigOperators
open HMT.VI.EventReconstruction

abbrev Route108 := Fin 108 → ℤ

def windowIndex (m : Fin 12) (i : Fin 9) : Fin 108 :=
  ⟨9 * m.val + i.val, by omega⟩

/-- The one-based manuscript trace, extended by zero only outside its 108 steps. -/
def routeTrace (d : Route108) (t : ℕ) : ℤ :=
  if h : 1 ≤ t ∧ t ≤ 108 then d ⟨t - 1, by omega⟩ else 0

def calendarSign (m : ℕ) : ℤ := if m % 6 < 3 then 1 else -1

theorem calendarSign_unit (m : ℕ) : calendarSign m = 1 ∨ calendarSign m = -1 := by
  unfold calendarSign
  split <;> simp

theorem calendarSign_twelve :
    (fun m : Fin 12 => calendarSign m.val) = ![1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1] := by
  decide

theorem trace_window (d : Route108) (m : Fin 12) (i : Fin 9) :
    routeTrace d (HMT.II.Memory.TraceEvents.windowStep m.val i) = d (windowIndex m i) := by
  have hm := m.isLt
  have hi := i.isLt
  have h : 1 ≤ 9 * m.val + i.val + 1 ∧ 9 * m.val + i.val + 1 ≤ 108 := by omega
  simp only [HMT.II.Memory.TraceEvents.windowStep, routeTrace, h, dite_true]
  congr 1

def routeEvents (d : Route108) : Events :=
  fun m => HMT.II.Memory.TraceEvents.signedCoefficient (routeTrace d) calendarSign m.val

/-- Exact support and window: this does not count the separate action support
`{1,3,5,7}`, and does not identify the extractor with the tritic selector. -/
theorem routeEvents_formula (d : Route108) (m : Fin 12) :
    routeEvents d m = calendarSign m.val *
      ((∑ i : Fin 9, if d (windowIndex m i) ∈ ({2, 4, 6, 8} : Finset ℤ)
        then 1 else 0 : ℕ) : ℤ) := by
  simp only [routeEvents, HMT.II.Memory.TraceEvents.signedCoefficient,
    HMT.II.Memory.TraceEvents.eventCount, trace_window]

theorem routeEvents_abs_le_nine (d : Route108) (m : Fin 12) :
    |(routeEvents d m : ℝ)| ≤ 9 :=
  HMT.II.Memory.TraceEvents.signedCoefficient_abs_le_nine
    (routeTrace d) calendarSign calendarSign_unit m.val

theorem route_coordinates_integral (d : Route108) : IntegralImage (extract (routeEvents d)) :=
  extract_integral _

theorem route_events_reconstructed (d : Route108) :
    reconstruct (extract (routeEvents d)) = routeEvents d := reconstruct_extract _

#print axioms routeEvents_formula
#print axioms routeEvents_abs_le_nine
#print axioms route_events_reconstructed

end HMT.VI.RouteEvents
