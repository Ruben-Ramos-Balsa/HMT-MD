import RegionalResidualCylinderBridge
import SurvivalCylinderSelection
import JointCylinderSignature

/-!
Composition of the source's residual dynamics after R36 with the survival
criterion and the shared signature reader. Compatibility is supplied by the
proved residual trajectory, not by an extra equality-to-output assumption.
The result remains about this real-coordinate realization after R36.
-/

noncomputable section
namespace HMT.I.ResidualSurvivalSelection

open HMT.I.RegionalPublicationComposition HMT.I.RegionalCylinderTransition
open HMT.I.RegionalResidualDynamics HMT.I.RegionalResidualCylinderBridge
open HMT.I.SurvivalCylinderSelection HMT.I.JointCylinderSignature
open HMT.I.JointRegionalFrontier HMT.I.GeneratedN69Rows

theorem residual_history_survives (c : Channel) (n : Nat) :
    SurvivesAllDecimals c (6 + n) (residualPrefix c n).toNat := by
  intro k
  exact residual_cylinder_compatible c n k

theorem residual_prefix_is_unique_survivor (c : Channel) (n N : Nat) :
    SurvivesAllDecimals c (6 + n) N ↔ N = (residualPrefix c n).toNat := by
  have hr := survival_selects_publication c (6 + n) _ (residual_history_survives c n)
  rw [survival_iff_publication, hr]

def residualChild (c : Channel) (n : Nat) : Fin 729 :=
  let s := run n (r36RealCoordinate c)
  ⟨(nextDigit s).toNat, by have h := digit_bounds s; omega⟩

theorem residual_child_eq_generated (c : Channel) (n : Nat) :
    residualChild c n = nextTernary c (6 + n) := by
  apply Fin.ext
  change (nextDigit (run n (r36RealCoordinate c))).toNat = _
  rw [(r36_forward_publication c n).2]
  rfl

theorem residual_child_is_admissible (c : Channel) (n : Nat) :
    ChildAdmissible c (6 + n) (residualChild c n) :=
  (child_admissible_iff c (6 + n) _).2 (residual_child_eq_generated c n)

def residualJointChildren (n : Nat) (i : Fin 3) : Fin 729 :=
  residualChild (channelOfIndex i) n

theorem residual_joint_is_admissible (n : Nat) :
    JointAdmissible (6 + n) (residualJointChildren n) := by
  intro i
  exact residual_child_is_admissible (channelOfIndex i) n

theorem residual_joint_produces_same_signature (n : Nat) :
    signatureFromChildren (residualJointChildren n) = signatureGenerated (6 + n) :=
  signature_of_admissible_children (6 + n) _ (residual_joint_is_admissible n)

theorem residual_joint_refines_same_cylinders (n k : Nat) (i : Fin 3) :
    jointStep (generated (channelOfIndex i) (6 + n) k) (residualJointChildren n i)
        (nextDecimal (channelOfIndex i) k) =
      generated (channelOfIndex i) (6 + n + 1) (k + 1) :=
  admissible_children_refine_same_cylinders (6 + n) k _ (residual_joint_is_admissible n) i

end HMT.I.ResidualSurvivalSelection
end

#print axioms HMT.I.ResidualSurvivalSelection.residual_history_survives
#print axioms HMT.I.ResidualSurvivalSelection.residual_prefix_is_unique_survivor
#print axioms HMT.I.ResidualSurvivalSelection.residual_child_eq_generated
#print axioms HMT.I.ResidualSurvivalSelection.residual_child_is_admissible
#print axioms HMT.I.ResidualSurvivalSelection.residual_joint_is_admissible
#print axioms HMT.I.ResidualSurvivalSelection.residual_joint_produces_same_signature
#print axioms HMT.I.ResidualSurvivalSelection.residual_joint_refines_same_cylinders
