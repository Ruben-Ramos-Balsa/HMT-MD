import PaleyWittDuality

/-!
# Every full-support Paley–Witt orientation preserves every marked neighbour

Source: Article X, `sections/orientaciones_reticulares.tex`,
`paper:24-orientaciones` and `paper:robustez-orientaciones`.

This specializes the general, already proved Coxeter-neighbour certificate to
every word of full support in the constructed ternary code. The orientation
is read from that word, not from a chosen neighbour or a register K. In the
inherited convention `true` acts by C⁻¹, hence residue 1 chooses C⁻¹ and
residue 2 chooses C. No lattice classification, FLM or Moonshine is asserted.
-/

namespace HMT.I.FullSupportNeighborOrientations

open HMT.IV.CoxeterNeighbor

abbrev Word := Fin 12 → ZMod 3

/-- Full support in the ternary alphabet, before choosing an orientation. -/
def FullSupport (u : Word) : Prop := ∀ i, u i ≠ 0

/-- The frame is R on residue 1 and I on residue 2. -/
def orientation (u : Word) : Fin 12 → Bool := fun i => decide (u i = 1)

private theorem nonzero_residue_sign (a : ZMod 3) (ha : a ≠ 0) :
    ((if decide (a = 1) then (1 : ℤ) else -1) : ZMod 3) = a := by
  have h : ∀ b : ZMod 3, b ≠ 0 →
      ((if decide (b = 1) then (1 : ℤ) else -1) : ZMod 3) = b := by decide
  exact h a ha

/-- The orientation recovers the entire input codeword in the discriminant. -/
theorem signWord_mod3 (u : Word) (hfull : FullSupport u) :
    (fun i => (signWord (orientation u) i : ZMod 3)) = u := by
  funext i
  simpa [signWord, orientation] using nonzero_residue_sign (u i) (hfull i)

theorem signWord_mem (u : Word) (hu : u ∈ wittCode) (hfull : FullSupport u) :
    (fun i => (signWord (orientation u) i : ZMod 3)) ∈ wittCode := by
  rw [signWord_mod3 u hfull]
  exact hu

/-- The inverse action carries the opposite discriminant word. -/
theorem inverse_signWord_mod3 (u : Word) (hfull : FullSupport u) :
    (fun i => (signWord (fun j => !(orientation u j)) i : ZMod 3)) = -u := by
  rw [inverse_signWord]
  simpa only [Pi.neg_apply, Int.cast_neg] using
    congrArg (fun v : Word => -v) (signWord_mod3 u hfull)

theorem inverse_signWord_mem (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) :
    (fun i => (signWord (fun j => !(orientation u j)) i : ZMod 3)) ∈ wittCode := by
  rw [inverse_signWord_mod3 u hfull]
  exact wittCode.neg_mem hu

/-- Both forward and inverse displacements lie in the same marked kernel. -/
theorem both_shifts_mem_kernel (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) :
    shift (orientation u) (marked o) ∈ kernel wittCode (radial (marked o)) ∧
    shift (fun i => !(orientation u i)) (marked o) ∈
      kernel wittCode (radial (marked o)) :=
  ⟨shift_marked_mem_kernel wittCode (orientation u) o (signWord_mem u hu hfull),
    shift_marked_mem_kernel wittCode (fun i => !(orientation u i)) o
      (inverse_signWord_mem u hu hfull)⟩

/-- Explicit inverse displacement; the inverse is the square of the action. -/
theorem inverse_shift_eq (u : Word) (o : Fin 12) :
    shift (fun i => !(orientation u i)) (marked o) =
      (1 / 3 : ℚ) • (action (orientation u)
        (action (orientation u) (radial (marked o))) - radial (marked o)) := by
  simp only [shift, inverse_action]

/-- Setwise invariance of the whole neighbour, at every marked origin. -/
theorem marked_neighbor_invariant (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) (x : Space 12) :
    action (orientation u) x ∈ neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o)) :=
  action_mem_neighbor_iff wittCode (orientation u) o witt_glue_integral
    (signWord_mem u hu hfull) x

/-- The existing neighbour equivalence, now for every full-support codeword. -/
def fullSupportNeighborEquiv (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) :
    neighbor wittCode (radial (marked o)) ≃ neighbor wittCode (radial (marked o)) :=
  neighborEquiv wittCode (orientation u) o witt_glue_integral
    (signWord_mem u hu hfull)

theorem fullSupportNeighborEquiv_cube (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) :
    (fullSupportNeighborEquiv u hu hfull o) ^ 3 = 1 := by
  apply Equiv.ext
  intro x
  apply Subtype.ext
  change action (orientation u) (action (orientation u)
    (action (orientation u) x.val)) = x.val
  exact action_cube _ _

/-- Exact order three, not merely a cube identity. -/
theorem fullSupportNeighborEquiv_order (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) :
    orderOf (fullSupportNeighborEquiv u hu hfull o) = 3 := by
  apply orderOf_eq_prime
  · exact fullSupportNeighborEquiv_cube u hu hfull o
  · intro h
    let x : neighbor wittCode (radial (marked o)) :=
      ⟨rootDifference o, rootDifference o, rootDifference_mem_kernel wittCode o,
        0, by simp⟩
    have hx := congrArg (fun e => (e x : Space 12)) h
    change action (orientation u) (rootDifference o) = rootDifference o at hx
    exact rootDifference_ne_zero o ((action_fixed_iff _ _).mp hx)

/-- The universal symmetry statement on the ambient rational space. -/
theorem full_support_marked_symmetry (u : Word) (hu : u ∈ wittCode)
    (hfull : FullSupport u) (o : Fin 12) :
    orderOf (fullSupportNeighborEquiv u hu hfull o) = 3 ∧
    (∀ x y : Space 12, pairing (action (orientation u) x)
      (action (orientation u) y) = pairing x y) ∧
    (∀ x : Space 12, action (orientation u) x = x ↔ x = 0) ∧
    (∀ x : Space 12, action (orientation u) x ∈
      neighbor wittCode (radial (marked o)) ↔
      x ∈ neighbor wittCode (radial (marked o))) :=
  ⟨fullSupportNeighborEquiv_order u hu hfull o, action_pairing (orientation u),
    action_fixed_iff (orientation u), marked_neighbor_invariant u hu hfull o⟩

/-- The orientation loses no information on the full-support domain. -/
theorem orientation_injective_on_fullSupport (u v : Word)
    (hu : FullSupport u) (hv : FullSupport v) (h : orientation u = orientation v) :
    u = v := by
  rw [← signWord_mod3 u hu, ← signWord_mod3 v hv, h]

/-- Enumerate the 729 messages of the existing encoder, not arbitrary words. -/
def fullSupportMessages : Finset (Fin 6 → ZMod 3) :=
  Finset.univ.filter fun w => ∀ i : Fin 12, encode w i ≠ 0

theorem mem_fullSupportMessages (w : Fin 6 → ZMod 3) :
    w ∈ fullSupportMessages ↔ FullSupport (encode w) := by
  simp [fullSupportMessages, FullSupport]

set_option maxHeartbeats 0 in
set_option maxRecDepth 1000000 in
theorem fullSupportMessages_card : fullSupportMessages.card = 24 := by
  decide +kernel

/-- This finite set is exactly C_W^×, by `mem_fullSupportWords`. -/
def fullSupportWords : Finset Word := fullSupportMessages.image encode

theorem mem_fullSupportWords (u : Word) :
    u ∈ fullSupportWords ↔ u ∈ wittCode ∧ FullSupport u := by
  constructor
  · intro hu
    obtain ⟨w, hw, rfl⟩ := Finset.mem_image.mp hu
    exact ⟨⟨w, rfl⟩, (mem_fullSupportMessages w).mp hw⟩
  · rintro ⟨⟨w, rfl⟩, hfull⟩
    exact Finset.mem_image.mpr ⟨w, (mem_fullSupportMessages w).mpr hfull, rfl⟩

theorem fullSupportWords_card : fullSupportWords.card = 24 := by
  rw [fullSupportWords,
    Finset.card_image_of_injective _ HMT.PaleyWittDuality.encoder_injective]
  exact fullSupportMessages_card

#print axioms signWord_mod3
#print axioms both_shifts_mem_kernel
#print axioms marked_neighbor_invariant
#print axioms fullSupportNeighborEquiv_order
#print axioms full_support_marked_symmetry
#print axioms fullSupportMessages_card
#print axioms mem_fullSupportWords
#print axioms fullSupportWords_card

end HMT.I.FullSupportNeighborOrientations
