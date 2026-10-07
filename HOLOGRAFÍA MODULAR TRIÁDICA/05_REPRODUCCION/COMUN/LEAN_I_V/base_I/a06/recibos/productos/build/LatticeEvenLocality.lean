import LatticeEvenTranslation
import LatticeDescendantLocality

/-!
The actual field restriction to the existing fixed carrier preserves the
same finite-difference locality identity. The locality exponent is inherited
from the constructed full state-fields, not imposed on the restriction.
Linearity, vacuum and creation are transported through the same inclusion.
This is the untwisted even restriction; no twisted sector is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeEvenLocality

open LatticeOscillatorFock LatticeStateFieldMap LatticeEvenVertexFields
open LatticeEvenTranslation LatticeDescendantLocality LatticeFieldLocality
open LatticeFactorConvolution

theorem crossing_power_restrict (o : Fin 12)
    (f : BiStates (Module.End ℂ (evenSpace o)))
    (g : BiStates (Module.End ℂ (LatticeCarrier o)))
    (h : ∀ (k l : ℤ) (v : evenSpace o), (f k l v).val = g k l v.val)
    (N : ℕ) (k l : ℤ) (v : evenSpace o) :
    (((crossing^N) f k l) v).val = ((crossing^N) g k l) v.val := by
  induction N generalizing k l with
  | zero => exact h k l v
  | succ N ih =>
    rw [crossing_pow_succ_apply, crossing_pow_succ_apply]
    change (((crossing^N) f (k-1) l) v).val -
      (((crossing^N) f k (l-1)) v).val = _
    rw [ih, ih]
    rfl

theorem evenField_localAt (o : Fin 12) (u v : evenSpace o) (N : ℕ)
    (h : LocalAt N (stateField o u.val) (stateField o v.val)) :
    LocalAt N (evenField o u) (evenField o v) := by
  have hF (k l : ℤ) (w : evenSpace o) :
      (forward (evenField o u) (evenField o v) k l w).val =
        forward (stateField o u.val) (stateField o v.val) k l w.val := by
    simp only [forward, evenField_coefficient, Module.End.mul_apply, evenCoefficient_coe]
  have hB (k l : ℤ) (w : evenSpace o) :
      (backward (evenField o u) (evenField o v) k l w).val =
        backward (stateField o u.val) (stateField o v.val) k l w.val := by
    simp only [backward, evenField_coefficient, Module.End.mul_apply, evenCoefficient_coe]
  unfold LocalAt at h ⊢
  funext k l
  apply LinearMap.ext
  intro w
  apply Subtype.ext
  rw [crossing_power_restrict o _ _ hF N k l w,
      crossing_power_restrict o _ _ hB N k l w, h]

theorem evenField_local (o : Fin 12) (u v : evenSpace o) :
    Local (evenField o u) (evenField o v) := by
  obtain ⟨N, hN⟩ := stateField_local o u.val v.val
  exact ⟨N, evenField_localAt o u v N hN⟩

theorem evenField_add (o : Fin 12) (u v : evenSpace o) :
    evenField o (u+v) = evenField o u + evenField o v := by
  apply HVertexOperator.coeff_inj
  funext k
  apply LinearMap.ext
  intro w
  simp only [HVertexOperator.coeff_add, Pi.add_apply, evenField_coefficient,
    LinearMap.add_apply]
  apply Subtype.ext
  change HVertexOperator.coeff (stateField o (u.val+v.val)) k w.val =
    HVertexOperator.coeff (stateField o u.val) k w.val +
      HVertexOperator.coeff (stateField o v.val) k w.val
  simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]

theorem evenField_smul (o : Fin 12) (c : ℂ) (u : evenSpace o) :
    evenField o (c • u) = c • evenField o u := by
  apply HVertexOperator.coeff_inj
  funext k
  apply LinearMap.ext
  intro w
  simp only [HVertexOperator.coeff_smul, Pi.smul_apply, evenField_coefficient,
    LinearMap.smul_apply]
  apply Subtype.ext
  change HVertexOperator.coeff (stateField o (c • u.val)) k w.val =
    c • HVertexOperator.coeff (stateField o u.val) k w.val
  simp only [map_smul, HVertexOperator.coeff_smul, Pi.smul_apply, LinearMap.smul_apply]

def evenStateField (o : Fin 12) :
    evenSpace o →ₗ[ℂ] VertexOperator ℂ (evenSpace o) where
  toFun := evenField o
  map_add' := evenField_add o
  map_smul' c u := evenField_smul o c u

theorem evenStateField_apply (o : Fin 12) (u : evenSpace o) :
    evenStateField o u = evenField o u := rfl

theorem evenField_vacuum_coefficient (o : Fin 12) (k : ℤ) :
    HVertexOperator.coeff (evenField o (evenVacuum o)) k =
      if k=0 then (LinearMap.id : Module.End ℂ (evenSpace o)) else 0 := by
  rw [evenField_coefficient]
  exact evenCoefficient_vacuum o k

theorem evenField_creates (o : Fin 12) (u : evenSpace o) :
    (∀ k : ℤ, k < 0 → HVertexOperator.coeff (evenField o u) k (evenVacuum o) = 0) ∧
      HVertexOperator.coeff (evenField o u) 0 (evenVacuum o) = u := by
  simp only [evenField_coefficient]
  exact ⟨evenCoefficient_negative_vacuum o u, evenCoefficient_creates o u⟩

theorem evenStateField_injective (o : Fin 12) : Function.Injective (evenStateField o) := by
  intro u v h
  have hc := congrArg (fun B => HVertexOperator.coeff B 0 (evenVacuum o)) h
  simpa only [evenStateField_apply, evenField_coefficient, evenCoefficient_creates] using hc

end HMT.IV.LatticeEvenLocality
end

#print axioms HMT.IV.LatticeEvenLocality.crossing_power_restrict
#print axioms HMT.IV.LatticeEvenLocality.evenField_localAt
#print axioms HMT.IV.LatticeEvenLocality.evenField_local
#print axioms HMT.IV.LatticeEvenLocality.evenField_add
#print axioms HMT.IV.LatticeEvenLocality.evenField_smul
#print axioms HMT.IV.LatticeEvenLocality.evenStateField
#print axioms HMT.IV.LatticeEvenLocality.evenStateField_apply
#print axioms HMT.IV.LatticeEvenLocality.evenField_vacuum_coefficient
#print axioms HMT.IV.LatticeEvenLocality.evenField_creates
#print axioms HMT.IV.LatticeEvenLocality.evenStateField_injective
