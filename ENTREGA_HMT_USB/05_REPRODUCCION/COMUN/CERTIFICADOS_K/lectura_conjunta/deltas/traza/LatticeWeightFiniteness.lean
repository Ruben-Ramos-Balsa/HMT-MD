import LatticeFockMonomialParity
import WeightedOscillatorTrace

/-!
Finite weight pieces of the actual, unbounded oscillator occupation space.
Finiteness is proved by an explicit bounded encoding, not assumed. The
encoding also identifies weight and parity length with the finite trace
model. No frequency cutoff is imposed on the ambient Fock space.
-/

noncomputable section
namespace HMT.IV.LatticeWeightFiniteness

open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.IV.LatticeCocycle
open scoped BigOperators

abbrev WeightOccupation (o : Fin 12) (d : ℕ) :=
  {a : Occupation o // occupationWeight o a = d}

theorem weighted_entry_le (o : Fin 12) (a : Occupation o) (p : Mode o) :
    (p.1 + 1) * a p ≤ occupationWeight o a := by
  classical
  by_cases hp : p ∈ a.support
  · change (p.1 + 1) * a p ≤ ∑ q ∈ a.support, (q.1 + 1) * a q
    exact Finset.single_le_sum (f := fun q : Mode o => (q.1 + 1) * a q)
      (fun _ _ => Nat.zero_le _) hp
  · simp only [Finsupp.notMem_support_iff] at hp
    simp [hp]

theorem entry_le_weight (o : Fin 12) (a : Occupation o) (p : Mode o) :
    a p ≤ occupationWeight o a := by
  have h := weighted_entry_le o a p
  nlinarith

theorem entry_eq_zero_of_weight_le_mode (o : Fin 12) (d : ℕ)
    (a : WeightOccupation o d) (p : Mode o) (hp : d ≤ p.1) :
    a.val p = 0 := by
  have h := weighted_entry_le o a.val p
  rw [a.property] at h
  nlinarith

def modeEmbedding (o : Fin 12) (d : ℕ) :
    (Fin d × Fin (BasisSize o)) ↪ Mode o where
  toFun p := (p.1.val, p.2)
  inj' := by
    intro p q h
    apply Prod.ext
    · apply Fin.ext
      exact congrArg Prod.fst h
    · exact congrArg (fun x : ℕ × Fin (BasisSize o) => x.2) h

def encode (o : Fin 12) (d : ℕ) (a : WeightOccupation o d) :
    WeightedOscillatorTrace.Occupation d d (BasisSize o) :=
  fun p => ⟨a.val (modeEmbedding o d p), by
    have h := entry_le_weight o a.val (modeEmbedding o d p)
    rw [a.property] at h
    omega⟩

def decode (o : Fin 12) (d : ℕ)
    (a : WeightedOscillatorTrace.Occupation d d (BasisSize o)) : Occupation o :=
  Finsupp.embDomain (modeEmbedding o d)
    (Finsupp.equivFunOnFinite.symm (fun p => (a p).val))

@[simp] theorem decode_apply (o : Fin 12) (d : ℕ)
    (a : WeightedOscillatorTrace.Occupation d d (BasisSize o))
    (p : Fin d × Fin (BasisSize o)) :
    decode o d a (modeEmbedding o d p) = (a p).val := by
  simp [decode]

theorem decode_apply_high (o : Fin 12) (d : ℕ)
    (a : WeightedOscillatorTrace.Occupation d d (BasisSize o))
    (p : Mode o) (hp : d ≤ p.1) : decode o d a p = 0 := by
  apply Finsupp.embDomain_notin_range
  rintro ⟨q, hq⟩
  have he : q.1.val = p.1 := congrArg Prod.fst hq
  have hlt := q.1.isLt
  omega

theorem decode_encode (o : Fin 12) (d : ℕ) (a : WeightOccupation o d) :
    decode o d (encode o d a) = a.val := by
  ext p
  by_cases hp : p.1 < d
  · let q : Fin d × Fin (BasisSize o) := (⟨p.1, hp⟩, p.2)
    have hq : modeEmbedding o d q = p := by cases p; rfl
    rw [← hq, decode_apply]
    rfl
  · rw [decode_apply_high o d _ p (Nat.le_of_not_gt hp),
      entry_eq_zero_of_weight_le_mode o d a p (Nat.le_of_not_gt hp)]

theorem encode_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (encode o d) := by
  intro a b h
  apply Subtype.ext
  have hd := congrArg (decode o d) h
  simpa only [decode_encode] using hd

noncomputable instance weightOccupationFintype (o : Fin 12) (d : ℕ) :
    Fintype (WeightOccupation o d) :=
  Fintype.ofInjective (encode o d) (encode_injective o d)

theorem decode_weight (o : Fin 12) (d : ℕ)
    (a : WeightedOscillatorTrace.Occupation d d (BasisSize o)) :
    occupationWeight o (decode o d a) =
      WeightedOscillatorTrace.occupationWeight a := by
  simp [occupationWeight, decode, Finsupp.sum_embDomain,
    Finsupp.sum_fintype, modeEmbedding, WeightedOscillatorTrace.occupationWeight]

theorem decode_length (o : Fin 12) (d : ℕ)
    (a : WeightedOscillatorTrace.Occupation d d (BasisSize o)) :
    occupationLength o (decode o d a) =
      WeightedOscillatorTrace.occupationLength a := by
  simp [occupationLength, decode, Finsupp.sum_embDomain,
    Finsupp.sum_fintype, WeightedOscillatorTrace.occupationLength]

def weightEquivFinite (o : Fin 12) (d : ℕ) :
    WeightOccupation o d ≃ WeightedOscillatorTrace.WeightPiece d d (BasisSize o) where
  toFun a := ⟨encode o d a, by
    rw [← decode_weight, decode_encode]
    exact a.property⟩
  invFun a := ⟨decode o d a.val, by rw [decode_weight]; exact a.property⟩
  left_inv a := by apply Subtype.ext; exact decode_encode o d a
  right_inv a := by
    apply Subtype.ext
    funext p
    apply Fin.ext
    exact decode_apply o d a.val p

theorem occupationLength_equiv (o : Fin 12) (d : ℕ)
    (a : WeightOccupation o d) :
    occupationLength o a.val =
      WeightedOscillatorTrace.occupationLength (weightEquivFinite o d a).val := by
  change occupationLength o a.val =
    WeightedOscillatorTrace.occupationLength (encode o d a)
  rw [← decode_length, decode_encode]

end HMT.IV.LatticeWeightFiniteness
end

#print axioms HMT.IV.LatticeWeightFiniteness.weighted_entry_le
#print axioms HMT.IV.LatticeWeightFiniteness.entry_le_weight
#print axioms HMT.IV.LatticeWeightFiniteness.entry_eq_zero_of_weight_le_mode
#print axioms HMT.IV.LatticeWeightFiniteness.decode_encode
#print axioms HMT.IV.LatticeWeightFiniteness.encode_injective
#print axioms HMT.IV.LatticeWeightFiniteness.weightOccupationFintype
#print axioms HMT.IV.LatticeWeightFiniteness.decode_weight
#print axioms HMT.IV.LatticeWeightFiniteness.decode_length
#print axioms HMT.IV.LatticeWeightFiniteness.weightEquivFinite
#print axioms HMT.IV.LatticeWeightFiniteness.occupationLength_equiv
