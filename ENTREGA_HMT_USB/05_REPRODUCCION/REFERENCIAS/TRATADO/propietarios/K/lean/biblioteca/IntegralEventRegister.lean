import ChannelReconstruction

/-! Exact integral image and prospective event accumulation from
registro_imagen_integral.tex, img09:imagen and img09:acumulacion.
The event rules are supplied before evaluation. This theorem does not select
the canonical terminal family and does not use its expected twelve blocks. -/
namespace HMT.IntegralEventRegister

open DodecaphaseLinear HMT.TerminalChannels

def adjacent (z : Vector12) : Vector12 := fun i => z i - z (shift 1 i)

def prefixSum (w : Vector12) : Nat → Int
  | 0 => 0
  | n + 1 => prefixSum w n + w ⟨n % 12, Nat.mod_lt _ (by decide)⟩

def totalPrefix (w : Vector12) : Int := Q (fun i => prefixSum w i.val)

def admissible (w : Vector12) (q : Int) : Prop :=
  Q w = 0 ∧ (q + totalPrefix w) % 12 = 0

def reconstruct (w : Vector12) (q : Int) : Vector12 :=
  fun i => (q + totalPrefix w) / 12 - prefixSum w i.val

def sum3 (w : Vector12) : Vector12 :=
  fun i => w i + w (shift 1 i) + w (shift 2 i)

def sum4 (w : Vector12) : Vector12 :=
  fun i => sum3 w i + w (shift 3 i)

def delta (c : Channels) : Vector12 :=
  fun i => c.b120 i - c.b90 (shift 1 i)

theorem adjacent_sum_zero (z : Vector12) : Q (adjacent z) = 0 := by
  simp only [Q, adjacent, shift]
  dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat]
  simp only [Nat.reduceMod, Nat.reduceAdd, Int.ofNat_eq_coe, Int.ofNat_zero]
  omega

theorem prefix_adjacent (z : Vector12) (i : Fin 12) :
    prefixSum (adjacent z) i.val = z 0 - z i := by
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp only [prefixSum, adjacent, shift]
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat]
  all_goals simp only [Nat.reduceMod, Nat.reduceAdd, prefixSum, Int.ofNat_eq_coe, Int.ofNat_zero]
  all_goals omega

theorem totalPrefix_adjacent (z : Vector12) :
    totalPrefix (adjacent z) = 12 * z 0 - Q z := by
  unfold totalPrefix
  have hp : (fun i : Fin 12 => prefixSum (adjacent z) i.val) =
      (fun i => z 0 - z i) := funext (prefix_adjacent z)
  rw [hp]
  simp only [Q]
  omega

theorem adjacent_admissible (z : Vector12) : admissible (adjacent z) (Q z) := by
  constructor
  · exact adjacent_sum_zero z
  · rw [totalPrefix_adjacent]
    omega

theorem reconstruct_adjacent (z : Vector12) : reconstruct (adjacent z) (Q z) = z := by
  funext i
  simp only [reconstruct, totalPrefix_adjacent, prefix_adjacent]
  omega

theorem delta_extract (z : Vector12) : delta (extract z) = adjacent z := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp only [delta, extract, D3, D4, adjacent, shift]
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat]
  all_goals simp only [Nat.reduceMod, Nat.reduceAdd]
  all_goals omega

theorem D3_eq_sum3_adjacent (z : Vector12) : D3 z = sum3 (adjacent z) := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp only [D3, sum3, adjacent, shift]
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat]
  all_goals simp only [Nat.reduceMod, Nat.reduceAdd]
  all_goals omega

theorem D4_eq_sum4_adjacent (z : Vector12) : D4 z = sum4 (adjacent z) := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp only [D4, sum4, sum3, adjacent, shift]
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat]
  all_goals simp only [Nat.reduceMod, Nat.reduceAdd]
  all_goals omega

theorem adjacent_reconstruct (w : Vector12) (q : Int) (hw : Q w = 0) :
    adjacent (reconstruct w q) = w := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; simp [adjacent, reconstruct, shift, prefixSum, Fin.ofNat, Fin.instOfNat]
  all_goals simp only [Q] at hw; omega

theorem charge_reconstruct (w : Vector12) (q : Int)
    (hq : (q + totalPrefix w) % 12 = 0) : Q (reconstruct w q) = q := by
  have ht : Q (reconstruct w q) = 12 * ((q + totalPrefix w) / 12) -
      totalPrefix w := by
    simp only [Q, reconstruct, totalPrefix]
    omega
  rw [ht]
  omega

theorem extract_reconstruct (w : Vector12) (q : Int) (h : admissible w q) :
    extract (reconstruct w q) = ⟨sum3 w, sum4 w, q⟩ := by
  cases h with
  | intro hw hq =>
    unfold extract
    rw [D3_eq_sum3_adjacent, D4_eq_sum4_adjacent, adjacent_reconstruct w q hw,
      charge_reconstruct w q hq]

theorem delta_relations (c : Channels) (hb : c.b90 = sum3 (delta c)) :
    c.b120 = sum4 (delta c) := by
  funext i
  have hj := congrArg (fun v : Vector12 => v (shift 1 i)) hb
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp only [sum4, sum3, delta, shift] at hj ⊢
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat] at hj ⊢
  all_goals simp only [Nat.reduceMod, Nat.reduceAdd] at hj ⊢
  all_goals omega

theorem compatible_iff_integral_conditions (c : Channels) :
    Compatible c ↔ c.b90 = sum3 (delta c) ∧ admissible (delta c) c.charge := by
  constructor
  · rintro ⟨z, rfl⟩
    rw [delta_extract]
    exact ⟨D3_eq_sum3_adjacent z, adjacent_admissible z⟩
  · rintro ⟨hb, hw⟩
    refine ⟨reconstruct (delta c) c.charge, ?_⟩
    rw [extract_reconstruct _ _ hw]
    have hc := delta_relations c hb
    rw [← hb, ← hc]

theorem recover_eq_reconstruct (c : Channels) (hc : Compatible c) :
    recover c = reconstruct (delta c) c.charge := by
  obtain ⟨z, rfl⟩ := hc
  rw [recover_extract, delta_extract]
  exact (reconstruct_adjacent z).symm

theorem prefix_add (u v : Vector12) (n : Nat) :
    prefixSum (fun i => u i + v i) n = prefixSum u n + prefixSum v n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [prefixSum, ih]; omega

theorem totalPrefix_add (u v : Vector12) :
    totalPrefix (fun i => u i + v i) = totalPrefix u + totalPrefix v := by
  simp only [totalPrefix, Q, prefix_add]
  omega

theorem admissible_add (u v : Vector12) (q r : Int)
    (hu : admissible u q) (hv : admissible v r) :
    admissible (fun i => u i + v i) (q + r) := by
  rcases hu with ⟨hu0, hu12⟩
  rcases hv with ⟨hv0, hv12⟩
  constructor
  · simp only [Q] at *; omega
  · rw [totalPrefix_add]
    omega

theorem reconstruct_add (u v : Vector12) (q r : Int)
    (hu : admissible u q) (hv : admissible v r) :
    reconstruct (fun i => u i + v i) (q + r) =
      fun i => reconstruct u q i + reconstruct v r i := by
  funext i
  simp only [reconstruct, totalPrefix_add, prefix_add]
  have hq := hu.2
  have hr := hv.2
  omega

structure Contribution where
  increments : Vector12
  charge : Int
  compatible : admissible increments charge

def Contribution.zero : Contribution := ⟨fun _ => 0, 0, by
  constructor
  · rfl
  · decide⟩

def Contribution.add (a b : Contribution) : Contribution :=
  ⟨fun i => a.increments i + b.increments i, a.charge + b.charge,
    admissible_add _ _ _ _ a.compatible b.compatible⟩

def Contribution.register (a : Contribution) : Vector12 := reconstruct a.increments a.charge

theorem register_add (a b : Contribution) : (a.add b).register =
    fun i => a.register i + b.register i :=
  reconstruct_add _ _ _ _ a.compatible b.compatible

def accumulate : List Contribution → Contribution
  | [] => Contribution.zero
  | a :: as => a.add (accumulate as)

theorem register_zero : Contribution.zero.register = fun _ => 0 := by
  funext i
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i; rfl

theorem register_append (a b : List Contribution) : (accumulate (a ++ b)).register =
    fun i => (accumulate a).register i + (accumulate b).register i := by
  induction a with
  | nil => simp only [List.nil_append, accumulate, register_zero]; funext i; omega
  | cons x xs ih =>
    simp only [List.cons_append, accumulate, register_add, ih]
    funext i
    omega

theorem register_prefix_preserved (a b : List Contribution) :
    (accumulate ((a ++ b).take a.length)).register = (accumulate a).register := by
  rw [List.take_left]

theorem accumulated_channel_return (events : List Contribution) :
    recover (extract (accumulate events).register) = (accumulate events).register :=
  recover_extract _

theorem accumulated_register_unique (events : List Contribution) (z : Vector12)
    (h : extract z = extract (accumulate events).register) :
    z = (accumulate events).register := extract_injective _ _ h

#print axioms adjacent_sum_zero
#print axioms prefix_adjacent
#print axioms totalPrefix_adjacent
#print axioms adjacent_admissible
#print axioms reconstruct_adjacent
#print axioms delta_extract
#print axioms D3_eq_sum3_adjacent
#print axioms D4_eq_sum4_adjacent
#print axioms adjacent_reconstruct
#print axioms charge_reconstruct
#print axioms extract_reconstruct
#print axioms delta_relations
#print axioms compatible_iff_integral_conditions
#print axioms recover_eq_reconstruct
#print axioms prefix_add
#print axioms totalPrefix_add
#print axioms admissible_add
#print axioms reconstruct_add
#print axioms register_add
#print axioms register_zero
#print axioms register_append
#print axioms register_prefix_preserved
#print axioms accumulated_channel_return
#print axioms accumulated_register_unique

end HMT.IntegralEventRegister
