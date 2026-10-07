import RegionalSynchronizationSignature
import RegionalW24

/-!
The integer capacity used by the regional synchronization signature is the
publication clock of the enriched regional development. Its first pause is
the same event that selects the W24 descriptor. All calculations use the
certified regional publications. No terminal K repertoire is supplied here.
-/

namespace HMT.RegionalClockComposition

open HMT.N69RegionalSignature HMT.I.GeneratedN69Rows
open HMT.RegionalSynchronizationSignature HMT.I.RegionalW24

set_option maxHeartbeats 0
set_option maxRecDepth 100000

theorem radix_power_identity (t : Nat) :
    3 ^ ternaryDepth t = 729 ^ (t + 1) := by
  rw [ternaryDepth, pow_mul]
  norm_num

theorem capacity_eq_publicationClock (t : Nat) (ht : t < 23) :
    capacity t = publicationClock t := by
  have h := capacity_power_characterization t (List.mem_range.mpr ht)
  symm
  apply publicationClock_unique
  · rw [radix_power_identity]
    exact h.1
  · rw [radix_power_identity]
    exact h.2

theorem first_pause_is_same_clock_event :
    capacity firstPause = capacity (firstPause + 1) := by
  rw [firstPause_eq_twenty]
  rw [capacity_eq_publicationClock 20 (by omega),
    capacity_eq_publicationClock 21 (by omega)]
  exact distinct_times_same_clock.2

theorem no_earlier_capacity_pause :
    ∀ t < firstPause, capacity t ≠ capacity (t + 1) := by
  intro t ht
  have htwenty : t < 20 := by simpa [firstPause_eq_twenty] using ht
  rw [capacity_eq_publicationClock t (by omega),
    capacity_eq_publicationClock (t + 1) (by omega)]
  exact no_earlier_pause ⟨t, htwenty⟩

theorem reopening_follows_descriptor_epoch :
    counts regionalPrefixes firstPause = (2, 2, 2) ∧
    counts regionalPrefixes (firstPause + 1) = (611, 527, 723) ∧
    counts regionalPrefixes (firstPause + 2) = (421, 242, 483) := by
  rw [firstPause_eq_twenty]
  exact ⟨regional_counts.2.2.2.1,
    regional_counts.2.2.2.2.1, regional_counts.2.2.2.2.2⟩

theorem common_regional_evaluation :
    descriptorFromPrefixes regionalPrefixes firstPause = 66241910521 ∧
    synchronizationMatrix regionalPrefixes = [85, 112, 41, 52] ∧
    normalizedDefect regionalPrefixes = 4 := by
  exact ⟨regionalW24_value, synchronization_matrix_evaluates,
    normalized_defect_evaluates⟩

end HMT.RegionalClockComposition

#print axioms HMT.RegionalClockComposition.radix_power_identity
#print axioms HMT.RegionalClockComposition.capacity_eq_publicationClock
#print axioms HMT.RegionalClockComposition.first_pause_is_same_clock_event
#print axioms HMT.RegionalClockComposition.no_earlier_capacity_pause
#print axioms HMT.RegionalClockComposition.reopening_follows_descriptor_epoch
#print axioms HMT.RegionalClockComposition.common_regional_evaluation
