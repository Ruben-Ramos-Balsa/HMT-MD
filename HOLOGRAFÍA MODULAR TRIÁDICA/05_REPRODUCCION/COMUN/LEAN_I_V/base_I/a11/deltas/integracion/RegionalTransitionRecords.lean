import GeneratedN69Rows

/-!
The published transition records are recovered from the already verified
regional readers, rather than supplied to this constructor as four tables.
This is a posterior reading of the three regional publications. It is not
an identification of that reading with nine iterations of the full enriched
Sel/Tra/Upd dynamics. The latter statement has a different domain.

APP → TRIT → TPK → enriched state → joint discrete continuum is the inherited
genealogy of the regional readers. No conventional real constant, X/Y table,
lift matrix, K register, or target decimal expansion is a constructor input.
-/

namespace HMT.I.RegionalTransitionRecords

open TPKOrbits TPKLifts HMT.I.GeneratedN69Rows

set_option maxRecDepth 30000
set_option maxHeartbeats 10000000

def wordFromPrefix (p time : Nat) : Word :=
  let b := bandFromWord (blockFromPrefix p time)
  ⟨(b 0).val, (b 1).val, (b 2).val, (b 3).val, (b 4).val, (b 5).val⟩

/-- Exactly the row ordering printed in the source's construction of X_a. -/
def recordAt (prefixes : Fin 3 → Nat) (time : Nat) : Matrix :=
  ⟨wordFromPrefix (prefixes 0) time,
   wordFromPrefix (prefixes 0) (time + 1),
   wordFromPrefix (prefixes 1) time,
   wordFromPrefix (prefixes 1) (time + 1),
   wordFromPrefix (prefixes 2) time,
   wordFromPrefix (prefixes 2) (time + 1)⟩

noncomputable def regionalX0 : Matrix := recordAt regionalPrefixes 0
noncomputable def regionalY0 : Matrix := recordAt regionalPrefixes 1
noncomputable def regionalX1 : Matrix := recordAt regionalPrefixes 2
noncomputable def regionalY1 : Matrix := recordAt regionalPrefixes 3

/-- Integer evaluation is checked by the kernel; these targets are not inputs. -/
theorem evaluated_records :
    recordAt prefixInputs 0 = X0 ∧ recordAt prefixInputs 1 = Y0 ∧
    recordAt prefixInputs 2 = X1 ∧ recordAt prefixInputs 3 = Y1 := by
  decide +kernel

theorem regional_records_identified :
    regionalX0 = X0 ∧ regionalY0 = Y0 ∧
    regionalX1 = X1 ∧ regionalY1 = Y1 := by
  unfold regionalX0 regionalY0 regionalX1 regionalY1
  rw [regionalPrefixes_eq_inputs]
  exact evaluated_records

theorem regional_first_blocks_are_selected_seeds :
    [wordFromPrefix (regionalPrefixes 0) 0,
     wordFromPrefix (regionalPrefixes 1) 0,
     wordFromPrefix (regionalPrefixes 2) 0] = selectedSeeds := by
  rw [regionalPrefixes_eq_inputs, selected_seeds_checked]
  decide +kernel

noncomputable def regionalLift0 : Matrix := solveMatrix regionalX0 regionalY0
noncomputable def regionalLift1 : Matrix := solveMatrix regionalX1 regionalY1

theorem regional_lifts_identified : regionalLift0 = L0 ∧ regionalLift1 = L1 := by
  obtain ⟨h0, h1, h2, h3⟩ := regional_records_identified
  simp only [regionalLift0, regionalLift1, h0, h1, h2, h3, L0, L1, and_self]

theorem regional_transition_equations :
    mul regionalX0 regionalLift0 = regionalY0 ∧
    mul regionalX1 regionalLift1 = regionalY1 := by
  obtain ⟨h0, h1, h2, h3⟩ := regional_records_identified
  obtain ⟨h4, h5⟩ := regional_lifts_identified
  rw [h0, h1, h2, h3, h4, h5]
  exact transition_equations

theorem regional_lifts_unique (M0 M1 : Matrix)
    (hm0 : TernaryMatrix M0) (hm1 : TernaryMatrix M1)
    (h0 : mul regionalX0 M0 = regionalY0)
    (h1 : mul regionalX1 M1 = regionalY1) :
    M0 = regionalLift0 ∧ M1 = regionalLift1 := by
  obtain ⟨hx0, hy0, hx1, hy1⟩ := regional_records_identified
  obtain ⟨hl0, hl1⟩ := regional_lifts_identified
  rw [hx0, hy0] at h0
  rw [hx1, hy1] at h1
  exact ⟨(L0_unique M0 hm0 h0).trans hl0.symm,
    (L1_unique M1 hm1 h1).trans hl1.symm⟩

/-- Absolute existence and uniqueness for the records constructed above. -/
theorem regional_lifts_existUnique :
    ∃! lifts : Matrix × Matrix,
      TernaryMatrix lifts.1 ∧ TernaryMatrix lifts.2 ∧
      mul regionalX0 lifts.1 = regionalY0 ∧
      mul regionalX1 lifts.2 = regionalY1 := by
  obtain ⟨hl0, hl1⟩ := regional_lifts_identified
  refine ⟨(regionalLift0, regionalLift1), ?_, ?_⟩
  · refine ⟨?_, ?_, regional_transition_equations.1,
      regional_transition_equations.2⟩
    · change TernaryMatrix regionalLift0
      rw [hl0]
      exact reconstructed_lifts_ternary.1
    · change TernaryMatrix regionalLift1
      rw [hl1]
      exact reconstructed_lifts_ternary.2
  · intro lifts h
    obtain ⟨h0, h1⟩ := regional_lifts_unique lifts.1 lifts.2 h.1 h.2.1 h.2.2.1 h.2.2.2
    exact Prod.ext h0 h1

end HMT.I.RegionalTransitionRecords

#print axioms HMT.I.RegionalTransitionRecords.evaluated_records
#print axioms HMT.I.RegionalTransitionRecords.regional_records_identified
#print axioms HMT.I.RegionalTransitionRecords.regional_first_blocks_are_selected_seeds
#print axioms HMT.I.RegionalTransitionRecords.regional_lifts_identified
#print axioms HMT.I.RegionalTransitionRecords.regional_transition_equations
#print axioms HMT.I.RegionalTransitionRecords.regional_lifts_unique
#print axioms HMT.I.RegionalTransitionRecords.regional_lifts_existUnique
