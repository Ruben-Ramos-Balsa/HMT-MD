import JointRegionalFrontier
import RegionalTransitionRecords

/-!
Transition records constructed directly from arbitrary-depth regional
publications. The 600-trit prefixes occur only in the comparison theorem;
neither they nor X/Y/lift tables are inputs to these constructors.

This composes the existing regional reader with the exact reconstruction
of its first two transition lifts. It does not identify this posterior
reading with nine complete enriched Sel/Tra/Upd updates.
-/

noncomputable section
namespace HMT.I.GeneratedTransitionRecords

open TPKOrbits TPKLifts HMT.I.GeneratedN69Rows
open HMT.I.JointRegionalFrontier HMT.I.RegionalTransitionRecords

def wordGenerated (time : Nat) (channel : Fin 3) : Word :=
  let b := bandsGenerated time channel
  ⟨(b 0).val, (b 1).val, (b 2).val, (b 3).val, (b 4).val, (b 5).val⟩

def recordGenerated (time : Nat) : Matrix :=
  ⟨wordGenerated time 0, wordGenerated (time + 1) 0,
   wordGenerated time 1, wordGenerated (time + 1) 1,
   wordGenerated time 2, wordGenerated (time + 1) 2⟩

theorem wordGenerated_eq_finite (time : Nat) (channel : Fin 3) (h : time < 100) :
    wordGenerated time channel = wordFromPrefix (regionalPrefixes channel) time := by
  unfold wordGenerated wordFromPrefix bandsGenerated
  rw [generated_block_eq_finite time channel h]

theorem recordGenerated_eq_finite (time : Nat) (h : time + 1 < 100) :
    recordGenerated time = recordAt regionalPrefixes time := by
  have ht : time < 100 := by omega
  unfold recordGenerated recordAt
  rw [wordGenerated_eq_finite time 0 ht, wordGenerated_eq_finite (time + 1) 0 h,
      wordGenerated_eq_finite time 1 ht, wordGenerated_eq_finite (time + 1) 1 h,
      wordGenerated_eq_finite time 2 ht, wordGenerated_eq_finite (time + 1) 2 h]

theorem generated_record_zero : recordGenerated 0 = regionalX0 :=
  recordGenerated_eq_finite 0 (by decide)

theorem generated_record_one : recordGenerated 1 = regionalY0 :=
  recordGenerated_eq_finite 1 (by decide)

theorem generated_record_two : recordGenerated 2 = regionalX1 :=
  recordGenerated_eq_finite 2 (by decide)

theorem generated_record_three : recordGenerated 3 = regionalY1 :=
  recordGenerated_eq_finite 3 (by decide)

theorem generated_first_blocks_are_selected_seeds :
    [wordGenerated 0 0, wordGenerated 0 1, wordGenerated 0 2] = selectedSeeds := by
  rw [wordGenerated_eq_finite 0 0 (by decide),
      wordGenerated_eq_finite 0 1 (by decide),
      wordGenerated_eq_finite 0 2 (by decide)]
  exact regional_first_blocks_are_selected_seeds

def generatedLift0 : Matrix := solveMatrix (recordGenerated 0) (recordGenerated 1)
def generatedLift1 : Matrix := solveMatrix (recordGenerated 2) (recordGenerated 3)

theorem generated_lifts_eq_regional :
    generatedLift0 = regionalLift0 ∧ generatedLift1 = regionalLift1 := by
  simp only [generatedLift0, generatedLift1, generated_record_zero,
    generated_record_one, generated_record_two, generated_record_three,
    regionalLift0, regionalLift1, and_self]

theorem generated_transition_equations :
    mul (recordGenerated 0) generatedLift0 = recordGenerated 1 ∧
    mul (recordGenerated 2) generatedLift1 = recordGenerated 3 := by
  rw [generated_record_zero, generated_record_one,
    generated_record_two, generated_record_three,
    generated_lifts_eq_regional.1, generated_lifts_eq_regional.2]
  exact regional_transition_equations

theorem generated_lifts_unique (M0 M1 : Matrix)
    (hm0 : TernaryMatrix M0) (hm1 : TernaryMatrix M1)
    (h0 : mul (recordGenerated 0) M0 = recordGenerated 1)
    (h1 : mul (recordGenerated 2) M1 = recordGenerated 3) :
    M0 = generatedLift0 ∧ M1 = generatedLift1 := by
  rw [generated_record_zero, generated_record_one] at h0
  rw [generated_record_two, generated_record_three] at h1
  obtain ⟨u0, u1⟩ := regional_lifts_unique M0 M1 hm0 hm1 h0 h1
  exact ⟨u0.trans generated_lifts_eq_regional.1.symm,
    u1.trans generated_lifts_eq_regional.2.symm⟩

theorem generated_lifts_existUnique :
    ∃! lifts : Matrix × Matrix,
      TernaryMatrix lifts.1 ∧ TernaryMatrix lifts.2 ∧
      mul (recordGenerated 0) lifts.1 = recordGenerated 1 ∧
      mul (recordGenerated 2) lifts.2 = recordGenerated 3 := by
  rw [generated_record_zero, generated_record_one,
    generated_record_two, generated_record_three]
  exact regional_lifts_existUnique

end HMT.I.GeneratedTransitionRecords
end

#print axioms HMT.I.GeneratedTransitionRecords.wordGenerated_eq_finite
#print axioms HMT.I.GeneratedTransitionRecords.recordGenerated_eq_finite
#print axioms HMT.I.GeneratedTransitionRecords.generated_record_zero
#print axioms HMT.I.GeneratedTransitionRecords.generated_record_one
#print axioms HMT.I.GeneratedTransitionRecords.generated_record_two
#print axioms HMT.I.GeneratedTransitionRecords.generated_record_three
#print axioms HMT.I.GeneratedTransitionRecords.generated_first_blocks_are_selected_seeds
#print axioms HMT.I.GeneratedTransitionRecords.generated_lifts_eq_regional
#print axioms HMT.I.GeneratedTransitionRecords.generated_transition_equations
#print axioms HMT.I.GeneratedTransitionRecords.generated_lifts_unique
#print axioms HMT.I.GeneratedTransitionRecords.generated_lifts_existUnique
