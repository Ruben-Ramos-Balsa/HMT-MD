import CoxeterNeighbor

/-! Exact finite certification for the displayed Paley–Witt encoder.
The source message space has 3^6 elements. No external weight table is assumed.
-/

namespace HMT.IV.CoxeterNeighbor

set_option maxHeartbeats 0
set_option maxRecDepth 1000000

def hammingWeight {n : ℕ} (c : Fin n → ZMod 3) : ℕ :=
  ∑ i, if c i = 0 then 0 else 1

theorem encoded_weight_zero_or_at_least_six :
    ∀ w : Fin 6 → ZMod 3, encode w = 0 ∨ 6 ≤ hammingWeight (encode w) := by
  decide

theorem witt_nonzero_weight_ge_six {c : Fin 12 → ZMod 3}
    (hc : c ∈ wittCode) (hne : c ≠ 0) : 6 ≤ hammingWeight c := by
  obtain ⟨w, rfl⟩ := hc
  exact (encoded_weight_zero_or_at_least_six w).resolve_left hne

def weightSixWord : Fin 12 → ZMod 3 :=
  encode (fun i => if i = 0 then 1 else 0)

theorem weightSixWord_mem : weightSixWord ∈ wittCode :=
  ⟨_, rfl⟩

theorem weightSixWord_weight : hammingWeight weightSixWord = 6 := by
  decide

theorem weightSixWord_ne_zero : weightSixWord ≠ 0 := by
  decide

theorem witt_minimum_weight_exactly_six :
    (∀ c ∈ wittCode, c ≠ 0 → 6 ≤ hammingWeight c) ∧
      ∃ c ∈ wittCode, c ≠ 0 ∧ hammingWeight c = 6 := by
  exact ⟨fun _ hc hn => witt_nonzero_weight_ge_six hc hn,
    weightSixWord, weightSixWord_mem, weightSixWord_ne_zero, weightSixWord_weight⟩

#print axioms encoded_weight_zero_or_at_least_six
#print axioms witt_nonzero_weight_ge_six
#print axioms weightSixWord_mem
#print axioms weightSixWord_weight
#print axioms weightSixWord_ne_zero
#print axioms witt_minimum_weight_exactly_six

end HMT.IV.CoxeterNeighbor
