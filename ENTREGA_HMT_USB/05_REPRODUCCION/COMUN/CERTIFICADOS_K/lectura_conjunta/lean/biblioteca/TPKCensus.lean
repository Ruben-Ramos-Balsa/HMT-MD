import TPKFiniteCursor

/-!
Exhaustive finite image of the source emitter, starting from the complete
9 × 9 × 4 cursor domain.  Signatures are computed from TPKFiniteCursor;
no catalogue, target constant, or expected output word is an input.
Source: extension.tex, initial conditions and injective emission factorization.
-/
namespace TPKCensus

open TPKTransport TPKFiniteCursor

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

theorem mem_eraseDups {α : Type} [BEq α] [LawfulBEq α]
    (x : α) (xs : List α) : x ∈ xs.eraseDups ↔ x ∈ xs := by
  match xs with
  | [] => simp
  | a :: tail =>
    rw [List.eraseDups_cons, List.mem_cons,
      mem_eraseDups x (tail.filter (fun b => !b == a))]
    by_cases h : x = a <;> simp [List.mem_filter, h]
termination_by xs.length
decreasing_by
  exact Nat.lt_succ_of_le (List.length_filter_le _ _)

def directions : List Direction := [.north, .east, .south, .west]

def seeds : List FiniteCursor :=
  (List.finRange 9).flatMap fun x =>
    (List.finRange 9).flatMap fun y =>
      directions.map fun d => ⟨x, y, d⟩

theorem directions_complete (d : Direction) : d ∈ directions := by
  cases d <;> decide

theorem fin9_complete : ∀ i : Fin 9, i ∈ List.finRange 9 := by decide +kernel

theorem seeds_complete (c : FiniteCursor) : c ∈ seeds := by
  rcases c with ⟨x, y, d⟩
  simp only [seeds, List.mem_flatMap, List.mem_map]
  exact ⟨x, fin9_complete x, y, fin9_complete y,
    d, directions_complete d, rfl⟩

theorem seeds_nodup : seeds.Nodup := by decide +kernel

theorem seeds_cardinality : seeds.length = 324 := by decide +kernel

theorem paired_seed_cardinality : seeds.length * seeds.length = 104976 := by
  rw [seeds_cardinality]

def signatures (sheet : Sheet) : List (List Nat) :=
  seeds.map (signatureFast sheet)

def signatureImage (sheet : Sheet) : List (List Nat) :=
  (signatures sheet).eraseDups

theorem signatureImage_exact (sheet : Sheet) (s : List Nat) :
    s ∈ signatureImage sheet ↔ ∃ c : FiniteCursor, signature sheet c = s := by
  rw [signatureImage, mem_eraseDups]
  simp only [signatures, List.mem_map]
  constructor
  · intro ⟨c, _, h⟩
    exact ⟨c, by simpa only [signatureFast_eq] using h⟩
  · intro ⟨c, h⟩
    exact ⟨c, seeds_complete c, by simpa only [signatureFast_eq] using h⟩

def multiplicity (sheet : Sheet) (sig : List Nat) : Nat :=
  ((signatures sheet).filter (fun s => s == sig)).length

def multiplicityCount (sheet : Sheet) (n : Nat) : Nat :=
  ((signatureImage sheet).filter (fun s => multiplicity sheet s == n)).length

def coupleDigit (a b : Nat) : Nat :=
  (EmissionCode.encode (EmissionCode.ofNat a) (EmissionCode.ofNat b)).val

def couple (a b : List Nat) : List Nat := List.zipWith coupleDigit a b

theorem ofNat_val (d : EmissionCode.Digit) : EmissionCode.ofNat d.val = d := by
  apply Fin.ext
  exact Nat.mod_eq_of_lt d.isLt

theorem couple_is_TPK_word (p t : FiniteCursor) :
    couple (signature .additive p) (signature .multiplicative t) =
      (List.finRange 6).map (fun j => (TPKEmission.word (seedObservable p t) j).val) := by
  rw [(signatures_two_cursor p t).1, (signatures_two_cursor p t).2]
  unfold couple
  rw [List.zipWith_map, List.zipWith_self, TPKEmission.word_as_encodeWord]
  simp only [coupleDigit, ofNat_val, EmissionCode.encodeWord]

def emitted : List (List Nat) :=
  (signatureImage .additive).flatMap fun a =>
    (signatureImage .multiplicative).map fun b => couple a b

theorem emitted_exact (u : List Nat) :
    u ∈ emitted ↔ ∃ p t : FiniteCursor,
      couple (signature .additive p) (signature .multiplicative t) = u := by
  simp only [emitted, List.mem_flatMap, List.mem_map, signatureImage_exact]
  constructor
  · intro ⟨a, ⟨p, hp⟩, b, ⟨t, ht⟩, h⟩
    exact ⟨p, t, by rw [hp, ht]; exact h⟩
  · intro ⟨p, t, h⟩
    exact ⟨signature .additive p, ⟨p, rfl⟩,
      signature .multiplicative t, ⟨t, rfl⟩, h⟩

theorem emitted_full_TPK_image (u : List Nat) :
    u ∈ emitted ↔ ∃ p t : FiniteCursor,
      (List.finRange 6).map (fun j => (TPKEmission.word (seedObservable p t) j).val) = u := by
  rw [emitted_exact]
  simp only [couple_is_TPK_word]

def ternary (u : List Nat) : List Nat :=
  u.map fun a => (3 - a % 3) % 3

def ternaryImage : List (List Nat) := (emitted.map ternary).eraseDups

theorem ternaryImage_exact (w : List Nat) :
    w ∈ ternaryImage ↔ ∃ p t : FiniteCursor,
      ternary (couple (signature .additive p) (signature .multiplicative t)) = w := by
  rw [ternaryImage, mem_eraseDups]
  simp only [List.mem_map, emitted_exact]
  constructor
  · intro ⟨u, ⟨p, t, h⟩, hw⟩
    exact ⟨p, t, by rw [h]; exact hw⟩
  · intro ⟨p, t, h⟩
    exact ⟨couple (signature .additive p) (signature .multiplicative t),
      ⟨p, t, rfl⟩, h⟩

theorem ternary_full_TPK_image (w : List Nat) :
    w ∈ ternaryImage ↔ ∃ p t : FiniteCursor,
      ternary ((List.finRange 6).map
        (fun j => (TPKEmission.word (seedObservable p t) j).val)) = w := by
  rw [ternaryImage_exact]
  simp only [couple_is_TPK_word]

def ternaryMultiplicity (w : List Nat) : Nat :=
  ((emitted.map ternary).filter (fun t => t == w)).length

def ternaryMultiplicityCount (n : Nat) : Nat :=
  (ternaryImage.filter (fun w => ternaryMultiplicity w == n)).length

/- Checked output witnesses for normalization efficiency; not generator inputs. -/
def additiveRows : List (List Nat) := [
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [8, 8, 9, 6, 5, 4],
  [6, 5, 4, 8, 8, 9],
  [6, 5, 4, 8, 8, 9],
  [8, 8, 9, 6, 5, 4],
  [2, 1, 2, 9, 8, 8],
  [9, 8, 8, 2, 1, 2],
  [9, 8, 8, 2, 1, 2],
  [2, 1, 2, 9, 8, 8],
  [6, 4, 5, 2, 1, 2],
  [2, 1, 2, 6, 4, 5],
  [2, 1, 2, 6, 4, 5],
  [6, 4, 5, 2, 1, 2],
  [9, 8, 8, 5, 4, 6],
  [5, 4, 6, 9, 8, 8],
  [5, 4, 6, 9, 8, 8],
  [9, 8, 8, 5, 4, 6],
  [2, 2, 1, 8, 8, 9],
  [8, 8, 9, 2, 2, 1],
  [8, 8, 9, 2, 2, 1],
  [2, 2, 1, 8, 8, 9],
  [5, 6, 4, 1, 2, 2],
  [1, 2, 2, 5, 6, 4],
  [1, 2, 2, 5, 6, 4],
  [5, 6, 4, 1, 2, 2],
  [8, 9, 8, 4, 6, 5],
  [4, 6, 5, 8, 9, 8],
  [4, 6, 5, 8, 9, 8],
  [8, 9, 8, 4, 6, 5],
  [1, 2, 2, 8, 9, 8],
  [8, 9, 8, 1, 2, 2],
  [8, 9, 8, 1, 2, 2],
  [1, 2, 2, 8, 9, 8],
  [4, 5, 6, 2, 2, 1],
  [2, 2, 1, 4, 5, 6],
  [2, 2, 1, 4, 5, 6],
  [4, 5, 6, 2, 2, 1]
]

def multiplicativeRows : List (List Nat) := [
  [3, 9, 3, 1, 7, 7],
  [1, 7, 7, 3, 9, 3],
  [1, 7, 7, 3, 9, 3],
  [3, 9, 3, 1, 7, 7],
  [5, 5, 5, 3, 3, 9],
  [3, 9, 3, 1, 7, 7],
  [3, 3, 9, 5, 5, 5],
  [1, 7, 7, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [7, 1, 7, 5, 5, 5],
  [7, 7, 1, 3, 3, 9],
  [5, 5, 5, 7, 1, 7],
  [3, 3, 9, 7, 7, 1],
  [7, 7, 1, 5, 5, 5],
  [9, 3, 3, 7, 1, 7],
  [5, 5, 5, 7, 7, 1],
  [7, 1, 7, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [5, 5, 5, 9, 3, 3],
  [7, 1, 7, 9, 3, 3],
  [9, 3, 3, 5, 5, 5],
  [9, 3, 3, 7, 1, 7],
  [3, 3, 9, 7, 7, 1],
  [3, 3, 9, 7, 7, 1],
  [7, 7, 1, 3, 3, 9],
  [7, 7, 1, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [1, 7, 7, 3, 9, 3],
  [3, 3, 9, 5, 5, 5],
  [3, 9, 3, 1, 7, 7],
  [5, 5, 5, 3, 3, 9],
  [3, 9, 3, 5, 5, 5],
  [5, 5, 5, 3, 9, 3],
  [5, 5, 5, 3, 9, 3],
  [3, 9, 3, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [5, 5, 5, 7, 1, 7],
  [3, 9, 3, 5, 5, 5],
  [7, 1, 7, 5, 5, 5],
  [5, 5, 5, 3, 9, 3],
  [5, 5, 5, 1, 7, 7],
  [5, 5, 5, 3, 3, 9],
  [1, 7, 7, 5, 5, 5],
  [3, 3, 9, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [9, 3, 3, 5, 5, 5],
  [9, 3, 3, 5, 5, 5],
  [5, 5, 5, 9, 3, 3],
  [5, 5, 5, 9, 3, 3],
  [7, 1, 7, 9, 3, 3],
  [5, 5, 5, 9, 3, 3],
  [9, 3, 3, 7, 1, 7],
  [9, 3, 3, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 7, 7, 1],
  [5, 5, 5, 7, 1, 7],
  [7, 7, 1, 3, 3, 9],
  [7, 1, 7, 5, 5, 5],
  [5, 5, 5, 3, 9, 3],
  [7, 1, 7, 5, 5, 5],
  [3, 9, 3, 5, 5, 5],
  [5, 5, 5, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [7, 7, 1, 5, 5, 5],
  [5, 5, 5, 7, 7, 1],
  [5, 5, 5, 7, 7, 1],
  [7, 7, 1, 5, 5, 5],
  [1, 7, 7, 5, 5, 5],
  [1, 7, 7, 5, 5, 5],
  [5, 5, 5, 1, 7, 7],
  [5, 5, 5, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [5, 5, 5, 3, 3, 9],
  [5, 5, 5, 1, 7, 7],
  [3, 3, 9, 5, 5, 5],
  [1, 7, 7, 5, 5, 5],
  [9, 3, 3, 7, 1, 7],
  [7, 7, 1, 5, 5, 5],
  [7, 1, 7, 9, 3, 3],
  [5, 5, 5, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [7, 1, 7, 9, 3, 3],
  [5, 5, 5, 7, 7, 1],
  [9, 3, 3, 7, 1, 7],
  [7, 7, 1, 5, 5, 5],
  [3, 3, 9, 5, 5, 5],
  [1, 7, 7, 5, 5, 5],
  [5, 5, 5, 3, 3, 9],
  [5, 5, 5, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [5, 5, 5, 1, 7, 7],
  [5, 5, 5, 1, 7, 7],
  [1, 7, 7, 5, 5, 5],
  [1, 7, 7, 5, 5, 5],
  [5, 5, 5, 7, 7, 1],
  [7, 7, 1, 5, 5, 5],
  [7, 7, 1, 5, 5, 5],
  [5, 5, 5, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [3, 9, 3, 5, 5, 5],
  [5, 5, 5, 7, 1, 7],
  [5, 5, 5, 3, 9, 3],
  [7, 1, 7, 5, 5, 5],
  [7, 7, 1, 3, 3, 9],
  [7, 1, 7, 5, 5, 5],
  [3, 3, 9, 7, 7, 1],
  [5, 5, 5, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 7, 1, 7],
  [9, 3, 3, 5, 5, 5],
  [7, 1, 7, 9, 3, 3],
  [5, 5, 5, 9, 3, 3],
  [5, 5, 5, 9, 3, 3],
  [5, 5, 5, 9, 3, 3],
  [9, 3, 3, 5, 5, 5],
  [9, 3, 3, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [1, 7, 7, 5, 5, 5],
  [3, 3, 9, 5, 5, 5],
  [5, 5, 5, 1, 7, 7],
  [5, 5, 5, 3, 3, 9],
  [7, 1, 7, 5, 5, 5],
  [5, 5, 5, 3, 9, 3],
  [5, 5, 5, 7, 1, 7],
  [3, 9, 3, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [3, 9, 3, 3, 9, 3],
  [5, 5, 5, 3, 9, 3],
  [3, 9, 3, 5, 5, 5],
  [3, 9, 3, 5, 5, 5],
  [5, 5, 5, 3, 9, 3],
  [3, 9, 3, 1, 7, 7],
  [5, 5, 5, 3, 3, 9],
  [1, 7, 7, 3, 9, 3],
  [3, 3, 9, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [7, 7, 1, 3, 3, 9],
  [7, 7, 1, 3, 3, 9],
  [3, 3, 9, 7, 7, 1],
  [3, 3, 9, 7, 7, 1],
  [9, 3, 3, 5, 5, 5],
  [9, 3, 3, 7, 1, 7],
  [5, 5, 5, 9, 3, 3],
  [7, 1, 7, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [0, 0, 0, 0, 0, 0],
  [7, 1, 7, 7, 1, 7],
  [5, 5, 5, 7, 7, 1],
  [7, 1, 7, 9, 3, 3],
  [7, 7, 1, 5, 5, 5],
  [9, 3, 3, 7, 1, 7],
  [5, 5, 5, 7, 1, 7],
  [3, 3, 9, 7, 7, 1],
  [7, 1, 7, 5, 5, 5],
  [7, 7, 1, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [3, 3, 9, 5, 5, 5],
  [1, 7, 7, 3, 9, 3],
  [5, 5, 5, 3, 3, 9],
  [3, 9, 3, 1, 7, 7],
  [1, 7, 7, 3, 9, 3],
  [3, 9, 3, 1, 7, 7],
  [3, 9, 3, 1, 7, 7],
  [1, 7, 7, 3, 9, 3],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [5, 5, 5, 5, 5, 5],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [3, 3, 9, 9, 3, 3],
  [0, 0, 0, 0, 0, 0],
  [9, 3, 3, 3, 3, 9],
  [0, 0, 0, 0, 0, 0],
  [1, 7, 7, 7, 7, 1],
  [0, 0, 0, 0, 0, 0],
  [7, 7, 1, 1, 7, 7],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0]
]

theorem signatures_additive_checked : signatures .additive = additiveRows := by decide +kernel

theorem signatures_multiplicative_checked : signatures .multiplicative = multiplicativeRows := by decide +kernel


-- These are conclusions of the finite computation, not structure fields.
theorem additive_image_cardinality : (signatureImage .additive).length = 18 := by
  rw [signatureImage, signatures_additive_checked]
  decide +kernel

theorem multiplicative_image_cardinality : (signatureImage .multiplicative).length = 26 := by
  rw [signatureImage, signatures_multiplicative_checked]
  decide +kernel

theorem additive_fibre_profile :
    multiplicityCount .additive 18 = 18 := by
  simp only [multiplicityCount, multiplicity, signatureImage, signatures_additive_checked]
  decide +kernel

theorem multiplicative_fibre_profile :
    multiplicityCount .multiplicative 8 = 24 ∧
    multiplicityCount .multiplicative 24 = 1 ∧
    multiplicityCount .multiplicative 108 = 1 := by
  simp only [multiplicityCount, multiplicity, signatureImage, signatures_multiplicative_checked]
  decide +kernel

theorem emitted_cardinality : emitted.length = 468 := by
  simp only [emitted, signatureImage, signatures_additive_checked, signatures_multiplicative_checked]
  decide +kernel

theorem emitted_nodup : emitted.Nodup := by
  simp only [emitted, signatureImage, signatures_additive_checked, signatures_multiplicative_checked]
  decide +kernel

theorem ternary_image_cardinality : ternaryImage.length = 243 := by
  simp only [ternaryImage, emitted, signatureImage, signatures_additive_checked, signatures_multiplicative_checked]
  decide +kernel

theorem ternary_fibre_profile :
    ternaryMultiplicityCount 1 = 132 ∧
    ternaryMultiplicityCount 2 = 66 ∧
    ternaryMultiplicityCount 3 = 18 ∧
    ternaryMultiplicityCount 4 = 3 ∧
    ternaryMultiplicityCount 5 = 6 ∧
    ternaryMultiplicityCount 6 = 18 := by
  simp only [ternaryMultiplicityCount, ternaryMultiplicity, ternaryImage,
    emitted, signatureImage, signatures_additive_checked, signatures_multiplicative_checked]
  decide +kernel

end TPKCensus

#print axioms TPKCensus.directions_complete
#print axioms TPKCensus.mem_eraseDups
#print axioms TPKCensus.fin9_complete
#print axioms TPKCensus.seeds_complete
#print axioms TPKCensus.seeds_nodup
#print axioms TPKCensus.seeds_cardinality
#print axioms TPKCensus.paired_seed_cardinality
#print axioms TPKCensus.signatureImage_exact
#print axioms TPKCensus.ofNat_val
#print axioms TPKCensus.couple_is_TPK_word
#print axioms TPKCensus.emitted_exact
#print axioms TPKCensus.emitted_full_TPK_image
#print axioms TPKCensus.ternaryImage_exact
#print axioms TPKCensus.ternary_full_TPK_image
#print axioms TPKCensus.signatures_additive_checked
#print axioms TPKCensus.signatures_multiplicative_checked
#print axioms TPKCensus.additive_image_cardinality
#print axioms TPKCensus.multiplicative_image_cardinality
#print axioms TPKCensus.additive_fibre_profile
#print axioms TPKCensus.multiplicative_fibre_profile
#print axioms TPKCensus.emitted_cardinality
#print axioms TPKCensus.emitted_nodup
#print axioms TPKCensus.ternary_image_cardinality
#print axioms TPKCensus.ternary_fibre_profile
