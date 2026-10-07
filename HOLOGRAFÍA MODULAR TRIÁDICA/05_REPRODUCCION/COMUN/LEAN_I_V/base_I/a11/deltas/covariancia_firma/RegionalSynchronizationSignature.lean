import GeneratedN69Rows

/-!
Exact regional synchronization data from the already certified 600-trit
publications. No N38 encoder, S8 repertoire, terminal K or target alpha is
an argument of these definitions or proofs. The finite capacity is computed
by comparing integer powers; there is no floating-point logarithm.

This file evaluates the regional antecedent of the vacancy jet. It does not
claim that the full terminal K selector has been discharged.
-/

namespace HMT.RegionalSynchronizationSignature

open HMT.I.GeneratedN69Rows

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def scale : Nat := 729 ^ 100

def fractionalPrefix (p : Nat) : Nat := p % scale

def capacity (t : Nat) : Nat :=
  (List.range (t + 2)).foldl
    (fun previous j => if 1000 ^ j ≤ 729 ^ (t + 1) then j else previous) 0

def ternaryPrefix (p t : Nat) : Nat :=
  fractionalPrefix p / 729 ^ (100 - t)

def decimalPrefix (p t : Nat) : Nat :=
  fractionalPrefix p * 1000 ^ capacity t / scale

def decimalUpper (p t : Nat) : Nat :=
  ((fractionalPrefix p + 1) * 1000 ^ capacity t - 1) / scale

def lowerLocal (p t : Nat) : Int :=
  ((decimalPrefix p t * 729 ^ (t + 1) / 1000 ^ capacity t : Nat) : Int)
    - (ternaryPrefix p t * 729 : Nat)

def upperLocal (p t : Nat) : Int :=
  ((((decimalPrefix p t + 1) * 729 ^ (t + 1) - 1) /
    1000 ^ capacity t : Nat) : Int) - (ternaryPrefix p t * 729 : Nat)

def candidateCount (p t : Nat) : Nat :=
  (min 728 (upperLocal p t) - max 0 (lowerLocal p t) + 1).toNat

def counts (prefixes : Fin 3 → Nat) (t : Nat) : Nat × Nat × Nat :=
  (candidateCount (prefixes 0) t, candidateCount (prefixes 1) t,
    candidateCount (prefixes 2) t)

def mirrorAmplitude (prefixes : Fin 3 → Nat) (t : Nat) : Nat :=
  let c := counts prefixes t
  max (Nat.dist c.1 c.2.1)
    (max (Nat.dist c.2.1 c.2.2) (Nat.dist c.2.2 c.1))

def synchronizationMatrix (prefixes : Fin 3 → Nat) : List Nat :=
  [mirrorAmplitude prefixes 4, mirrorAmplitude prefixes 5,
    mirrorAmplitude prefixes 6, mirrorAmplitude prefixes 7]

def synchronizationDeterminant (prefixes : Fin 3 → Nat) : Int :=
  (mirrorAmplitude prefixes 4 : Int) * mirrorAmplitude prefixes 7 -
    (mirrorAmplitude prefixes 5 : Int) * mirrorAmplitude prefixes 6

def normalizedDefect (prefixes : Fin 3 → Nat) : Int :=
  -synchronizationDeterminant prefixes / (counts prefixes 9).1

theorem candidate_count_is_cardinality (p t : Nat) :
    candidateCount p t =
      (Finset.Icc (max 0 (lowerLocal p t)) (min 728 (upperLocal p t))).card := by
  simp only [candidateCount, Int.card_Icc]
  congr 1
  omega

theorem capacity_power_characterization :
    ∀ t ∈ List.range 23,
      1000 ^ capacity t ≤ 729 ^ (t + 1) ∧
      729 ^ (t + 1) < 1000 ^ (capacity t + 1) := by
  decide +kernel

theorem capacity_before_reopening :
    (List.range 21).map capacity = List.range 21 := by
  decide +kernel

theorem first_reopening_capacity : capacity 21 = 20 ∧ capacity 22 = 21 := by
  decide +kernel

/-- The decimal prefix is stable throughout each finite ternary cylinder. -/
theorem prefix_stability :
    ∀ i : Fin 3, ∀ t ∈ List.range 23,
      decimalPrefix (regionalPrefixes i) t = decimalUpper (regionalPrefixes i) t := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

theorem regional_counts :
    counts regionalPrefixes 0 = (729,729,729) ∧
    counts regionalPrefixes 4 = (207,207,122) ∧
    counts regionalPrefixes 9 = (43,43,43) ∧
    counts regionalPrefixes 20 = (2,2,2) ∧
    counts regionalPrefixes 21 = (611,527,723) ∧
    counts regionalPrefixes 22 = (421,242,483) := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

theorem synchronization_matrix_evaluates :
    synchronizationMatrix regionalPrefixes = [85,112,41,52] := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

theorem determinant_evaluates :
    synchronizationDeterminant regionalPrefixes = -172 := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

theorem normalized_defect_evaluates : normalizedDefect regionalPrefixes = 4 := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

theorem reopening_boundary :
    let c := counts regionalPrefixes 21
    ((c.1 : Int) - c.2.1, (c.2.1 : Int) - c.2.2,
      (c.2.2 : Int) - c.1) = (28*3,28*(-7),28*4) := by
  rw [regionalPrefixes_eq_inputs]
  decide +kernel

end HMT.RegionalSynchronizationSignature

#print axioms HMT.RegionalSynchronizationSignature.candidate_count_is_cardinality
#print axioms HMT.RegionalSynchronizationSignature.capacity_power_characterization
#print axioms HMT.RegionalSynchronizationSignature.capacity_before_reopening
#print axioms HMT.RegionalSynchronizationSignature.first_reopening_capacity
#print axioms HMT.RegionalSynchronizationSignature.prefix_stability
#print axioms HMT.RegionalSynchronizationSignature.regional_counts
#print axioms HMT.RegionalSynchronizationSignature.synchronization_matrix_evaluates
#print axioms HMT.RegionalSynchronizationSignature.determinant_evaluates
#print axioms HMT.RegionalSynchronizationSignature.normalized_defect_evaluates
#print axioms HMT.RegionalSynchronizationSignature.reopening_boundary
