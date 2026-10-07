import IteratedCylinderSelector
import JointCylinderSignature

/-!
The blocks returned by the recursive rational selector are used once, both
to refine the two cylinder prefixes and to read the joint signature. No
signature, carry, future prefix or transition record is a constructor input.

This composes the cylinder and incidence components of the enriched state;
it does not substitute them for its other fibers or identify block refinements
with nine microscopic updates.
-/

namespace HMT.I.SelectedCylinderSignature

open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition
open HMT.I.GeneratedN69Rows HMT.I.JointRegionalFrontier
open HMT.I.JointCylinderSignature HMT.N69RegionalSignature

noncomputable section

abbrev SelectedStep := CylinderState × Fin 729

/-- The emitted digit is passed unchanged to the cylinder update and returned
for the joint signature reader. Both parent prefixes were computed recursively. -/
def step (c : Channel) (n k : Nat) : Option SelectedStep := do
  let p ← IteratedCylinderSelector.run c 729 (by decide) n
  let q ← IteratedCylinderSelector.run c 1000 (by decide) k
  let u ← IteratedCylinderSelector.next c 729 (by decide) n p
  let d ← IteratedCylinderSelector.next c 1000 (by decide) k q
  pure (jointStep ⟨n, k, p, q⟩ u d, u)

theorem step_correct (c : Channel) (n k : Nat) :
    step c n k = some (generated c (n + 1) (k + 1), nextTernary c n) := by
  simp only [step, IteratedCylinderSelector.run_correct, Bind.bind, Option.bind,
    IteratedCylinderSelector.next_correct, Pure.pure]
  change some (jointStep (generated c n k) (nextTernary c n) (nextDecimal c k),
    nextTernary c n) = _
  rw [← generated_joint_step]

structure JointOutput where
  cylinders : Fin 3 → CylinderState
  children : Fin 3 → Fin 729
  signature : Signature

/-- All signature fields are read from the exact digits used by the refinements. -/
def assemble (x y z : SelectedStep) : JointOutput :=
  let u := ![x.2, y.2, z.2]
  ⟨![x.1, y.1, z.1], u, signatureFromChildren u⟩

def produce (n k : Nat) : Option JointOutput := do
  let x ← step (channelOfIndex 0) n k
  let y ← step (channelOfIndex 1) n k
  let z ← step (channelOfIndex 2) n k
  pure (assemble x y z)

def generatedOutput (n k : Nat) : JointOutput :=
  ⟨fun i => generated (channelOfIndex i) (n + 1) (k + 1),
   jointChild n, signatureGenerated n⟩

theorem produce_correct (n k : Nat) : produce n k = some (generatedOutput n k) := by
  simp only [produce, step_correct, Bind.bind, Option.bind, Pure.pure]
  congr 1
  have hu : ![nextTernary (channelOfIndex 0) n,
      nextTernary (channelOfIndex 1) n, nextTernary (channelOfIndex 2) n] =
      jointChild n := by
    funext i
    fin_cases i <;> rfl
  have hs : ![generated (channelOfIndex 0) (n + 1) (k + 1),
      generated (channelOfIndex 1) (n + 1) (k + 1),
      generated (channelOfIndex 2) (n + 1) (k + 1)] =
      (fun i => generated (channelOfIndex i) (n + 1) (k + 1)) := by
    funext i
    fin_cases i <;> rfl
  simp only [assemble, generatedOutput, hu, hs]
  rfl

theorem produce_never_fails (n k : Nat) :
    ∃ out, produce n k = some out := ⟨generatedOutput n k, produce_correct n k⟩

theorem selected_fields (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) :
    (∀ i, out.cylinders i = generated (channelOfIndex i) (n + 1) (k + 1)) ∧
    out.children = jointChild n ∧ out.signature = signatureGenerated n := by
  have he := Option.some.inj ((produce_correct n k).symm.trans hout)
  subst out
  exact ⟨fun _ => rfl, rfl, rfl⟩

/-- Every produced cylinder retains its actual two previous prefixes. -/
theorem selected_prefix_recovery (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) (i : Fin 3) :
    Compatible (out.cylinders i) ∧
    (out.cylinders i).ternaryPrefix / 729 = publish (channelOfIndex i) 729 (by decide) n ∧
    (out.cylinders i).decimalPrefix / 1000 = publish (channelOfIndex i) 1000 (by decide) k := by
  rw [(selected_fields n k out hout).1 i]
  refine ⟨generated_compatible _ _ _, ?_, ?_⟩
  · simpa using (generated_truncation (channelOfIndex i) n k 1 1).1
  · simpa using (generated_truncation (channelOfIndex i) n k 1 1).2

theorem selected_column_carry (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) (j : Fin 6) :
    out.signature.q j + 3 * out.signature.c j = columnTotal (bandsGenerated n) j := by
  rw [(selected_fields n k out hout).2.2]
  exact generated_column_reconstruction n j

theorem selected_axis (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) (j : Fin 6) :
    (bandsGenerated n 2 j).val =
      (2 * (out.signature.q j + 3 - out.signature.a j)) % 3 := by
  rw [(selected_fields n k out hout).2.2]
  exact generated_axis_reconstruction n j

theorem selected_witt_charge (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) (i : Fin 3) :
    out.signature.wittDual i =
      (∑ j : Fin 6, wittResidue (bandsGenerated n) i j) % 3 := by
  rw [(selected_fields n k out hout).2.2]
  exact generated_dual_charge n i

/-- The same selected step obeys the full integer mixed-radix defect identity. -/
theorem selected_defect_update (n k : Nat) (out : JointOutput)
    (hout : produce n k = some out) (i : Fin 3) :
    lowerDefect (out.cylinders i) =
      729000 * lowerDefect (generated (channelOfIndex i) n k) +
      (out.children i).val * (1000 : Int)^(k + 1) -
      (nextDecimal (channelOfIndex i) k).val * 729 * (729 : Int)^n := by
  obtain ⟨hs, hu, _⟩ := selected_fields n k out hout
  rw [hs i, hu, generated_joint_step]
  exact joint_defect_update _ _ _

end
end HMT.I.SelectedCylinderSignature

#print axioms HMT.I.SelectedCylinderSignature.step_correct
#print axioms HMT.I.SelectedCylinderSignature.produce_correct
#print axioms HMT.I.SelectedCylinderSignature.produce_never_fails
#print axioms HMT.I.SelectedCylinderSignature.selected_fields
#print axioms HMT.I.SelectedCylinderSignature.selected_prefix_recovery
#print axioms HMT.I.SelectedCylinderSignature.selected_column_carry
#print axioms HMT.I.SelectedCylinderSignature.selected_axis
#print axioms HMT.I.SelectedCylinderSignature.selected_witt_charge
#print axioms HMT.I.SelectedCylinderSignature.selected_defect_update
