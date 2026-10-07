import JointRegionalFrontier
import RegionalCylinderTransition

/-!
The three admissible cylinder children are exactly the blocks used by the
joint signature reader. Admissibility is the rational interval test, not an
equality imposed with a target signature. The decimal cylinder transition
and this signature therefore share the same generated ternary children.
-/
noncomputable section
namespace HMT.I.JointCylinderSignature

open HMT.I.GeneratedN69Rows HMT.I.RegionalPublicationComposition
open HMT.I.JointRegionalFrontier HMT.I.RegionalCylinderTransition
open HMT.N69RegionalSignature

def jointChild (n : Nat) (i : Fin 3) : Fin 729 :=
  nextTernary (channelOfIndex i) n

def JointAdmissible (n : Nat) (u : Fin 3 → Fin 729) : Prop :=
  ∀ i, ChildAdmissible (channelOfIndex i) n (u i)

def signatureFromChildren (u : Fin 3 → Fin 729) : Signature :=
  readSignature (fun i => bandFromWord (u i).val)

theorem joint_child_is_regional_block (n : Nat) (i : Fin 3) :
    (jointChild n i).val = blockGenerated n i := rfl

theorem joint_admissible_iff (n : Nat) (u : Fin 3 → Fin 729) :
    JointAdmissible n u ↔ u = jointChild n := by
  constructor
  · intro h
    funext i
    exact (child_admissible_iff (channelOfIndex i) n (u i)).1 (h i)
  · intro h
    subst u
    intro i
    exact (child_admissible_iff (channelOfIndex i) n _).2 rfl

theorem unique_joint_children (n : Nat) :
    ∃! u : Fin 3 → Fin 729, JointAdmissible n u := by
  refine ⟨jointChild n, (joint_admissible_iff n _).2 rfl, ?_⟩
  intro u hu
  exact (joint_admissible_iff n u).1 hu

theorem signature_of_admissible_children (n : Nat) (u : Fin 3 → Fin 729)
    (hu : JointAdmissible n u) :
    signatureFromChildren u = signatureGenerated n := by
  rw [(joint_admissible_iff n u).1 hu]
  rfl

theorem admissible_children_refine_same_cylinders
    (n k : Nat) (u : Fin 3 → Fin 729) (hu : JointAdmissible n u) (i : Fin 3) :
    jointStep (generated (channelOfIndex i) n k) (u i)
      (nextDecimal (channelOfIndex i) k) =
        generated (channelOfIndex i) (n + 1) (k + 1) := by
  rw [(joint_admissible_iff n u).1 hu]
  exact (generated_joint_step (channelOfIndex i) n k).symm

theorem admissible_children_preserve_column_carry
    (n : Nat) (u : Fin 3 → Fin 729) (hu : JointAdmissible n u) (j : Fin 6) :
    (signatureFromChildren u).q j + 3 * (signatureFromChildren u).c j =
      columnTotal (bandsGenerated n) j := by
  rw [signature_of_admissible_children n u hu]
  exact generated_column_reconstruction n j

theorem admissible_children_preserve_witt_charge
    (n : Nat) (u : Fin 3 → Fin 729) (hu : JointAdmissible n u) (i : Fin 3) :
    (signatureFromChildren u).wittDual i =
      (∑ j : Fin 6, wittResidue (bandsGenerated n) i j) % 3 := by
  rw [signature_of_admissible_children n u hu]
  exact generated_dual_charge n i

end HMT.I.JointCylinderSignature
end

#print axioms HMT.I.JointCylinderSignature.joint_child_is_regional_block
#print axioms HMT.I.JointCylinderSignature.joint_admissible_iff
#print axioms HMT.I.JointCylinderSignature.unique_joint_children
#print axioms HMT.I.JointCylinderSignature.signature_of_admissible_children
#print axioms HMT.I.JointCylinderSignature.admissible_children_refine_same_cylinders
#print axioms HMT.I.JointCylinderSignature.admissible_children_preserve_column_carry
#print axioms HMT.I.JointCylinderSignature.admissible_children_preserve_witt_charge
