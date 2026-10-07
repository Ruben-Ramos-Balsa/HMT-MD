import RegionalResidualDynamics
import RegionalCylinderTransition

/-!
Posterior cylinder compatibility of the state-local residual trajectory.

Sources: 06e_certificado_generacion_monodromica_rev7, the forward residual
recurrence and its posterior certificate; and
20_arquitectura_operatoria_tpk_actualizada, the integer A/B cylinder test.

The ternary prefix below is read from `run`, not supplied by a decimal
target. Its nonnegativity and its identification with the existing rational
publication are proved afterwards. Pairing that prefix with any decimal
publication gives compatible cylinders without an added compatibility premise.

This is a bridge from the real coordinate at R36 depth, not an identification
with the complete historical enriched state or the pre-R36 nine-step map.
It does not turn the exact real residual into a finite-prefix algorithm, nor
assert a separate survival-to-uniqueness theorem.
-/

noncomputable section
namespace HMT.I.RegionalResidualCylinderBridge

open RegionalPublicationComposition

def residualPrefix (c : Channel) (n : Nat) : Int :=
  (RegionalResidualDynamics.run n
    (RegionalResidualDynamics.r36RealCoordinate c)).prefixValue

theorem residual_prefix_eq_publication (c : Channel) (n : Nat) :
    residualPrefix c n = (publish c 729 (by decide) (6 + n) : Int) :=
  (RegionalResidualDynamics.r36_forward_publication c n).1

theorem residual_prefix_nonnegative (c : Channel) (n : Nat) :
    0 ≤ residualPrefix c n := by
  rw [residual_prefix_eq_publication]
  exact Nat.cast_nonneg _

/-- Conversion to the natural cylinder coordinate discards no information. -/
theorem residual_prefix_toNat_exact (c : Channel) (n : Nat) :
    ((residualPrefix c n).toNat : Int) = residualPrefix c n :=
  Int.toNat_of_nonneg (residual_prefix_nonnegative c n)

def residualCylinder (c : Channel) (n k : Nat) :
    RegionalCylinderTransition.CylinderState :=
  ⟨6 + n, k, (residualPrefix c n).toNat,
    publish c 1000 (by decide) k⟩

theorem residual_cylinder_eq_generated (c : Channel) (n k : Nat) :
    residualCylinder c n k = RegionalCylinderTransition.generated c (6 + n) k := by
  unfold residualCylinder RegionalCylinderTransition.generated
  rw [residual_prefix_eq_publication]
  rfl

/-- Every decimal depth is compatible with the prefix produced by the local
residual evolution. Compatibility is a conclusion, not an input to `run`. -/
theorem residual_cylinder_compatible (c : Channel) (n k : Nat) :
    RegionalCylinderTransition.Compatible (residualCylinder c n k) := by
  rw [residual_cylinder_eq_generated]
  exact RegionalCylinderTransition.generated_compatible c (6 + n) k

theorem residual_forward_decimal_compatibility (c : Channel) (n : Nat) :
    0 ≤ residualPrefix c n ∧
      ((residualPrefix c n).toNat : Int) = residualPrefix c n ∧
      ∀ k : Nat, RegionalCylinderTransition.Compatible (residualCylinder c n k) :=
  ⟨residual_prefix_nonnegative c n, residual_prefix_toNat_exact c n,
    residual_cylinder_compatible c n⟩

end HMT.I.RegionalResidualCylinderBridge
end

#print axioms HMT.I.RegionalResidualCylinderBridge.residual_prefix_eq_publication
#print axioms HMT.I.RegionalResidualCylinderBridge.residual_prefix_nonnegative
#print axioms HMT.I.RegionalResidualCylinderBridge.residual_prefix_toNat_exact
#print axioms HMT.I.RegionalResidualCylinderBridge.residual_cylinder_eq_generated
#print axioms HMT.I.RegionalResidualCylinderBridge.residual_cylinder_compatible
#print axioms HMT.I.RegionalResidualCylinderBridge.residual_forward_decimal_compatibility
