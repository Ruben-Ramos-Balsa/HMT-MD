import Mathlib

/-!
Finite algebraic support for the normal-product commutation obligation.
This module does not identify Laurent sums or prove field-level locality.
The central editor retains that lifting and the existing selected origin.
-/

namespace HMT.NormalProductAlgebra

variable {R : Type*} [Ring R]

/-- Creation on the left and annihilation on the right. -/
def normalStep (aMinus aPlus x : R) : R := aMinus * x + x * aPlus

/-- The mixed terms cancel without imposing mixed-sign commutation. -/
theorem normalStep_commutator (aMinus aPlus bMinus bPlus x : R) :
    normalStep aMinus aPlus (normalStep bMinus bPlus x) -
      normalStep bMinus bPlus (normalStep aMinus aPlus x) =
    (aMinus * bMinus - bMinus * aMinus) * x +
      x * (bPlus * aPlus - aPlus * bPlus) := by
  unfold normalStep
  noncomm_ring

theorem normalStep_commute (aMinus aPlus bMinus bPlus : R)
    (hm : Commute aMinus bMinus) (hp : Commute aPlus bPlus) (x : R) :
    normalStep aMinus aPlus (normalStep bMinus bPlus x) =
      normalStep bMinus bPlus (normalStep aMinus aPlus x) := by
  apply sub_eq_zero.mp
  rw [normalStep_commutator, hm.eq, hp.eq]
  simp

/-- For left-only steps, the hypothesis cannot be dropped uniformly. -/
theorem left_only_commute_iff (a b : R) :
    (∀ x : R, normalStep a 0 (normalStep b 0 x) =
      normalStep b 0 (normalStep a 0 x)) ↔ Commute a b := by
  constructor
  · intro h
    show a * b = b * a
    simpa [normalStep] using h 1
  · intro h x
    exact normalStep_commute a 0 b 0 h (Commute.refl 0) x

/-- Right-only steps have the same necessary condition (reversed order). -/
theorem right_only_commute_iff (a b : R) :
    (∀ x : R, normalStep 0 a (normalStep 0 b x) =
      normalStep 0 b (normalStep 0 a x)) ↔ Commute a b := by
  constructor
  · intro h
    show a * b = b * a
    simpa [normalStep] using (h 1).symm
  · intro h x
    exact normalStep_commute 0 a 0 b (Commute.refl 0) h x

def e12 : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 0, 0]
def e21 : Matrix (Fin 2) (Fin 2) ℤ := !![0, 0; 1, 0]

/-- A concrete falsifier for unrestricted normal-step commutativity. -/
theorem noncommuting_left_counterexample :
    ¬ (∀ x : Matrix (Fin 2) (Fin 2) ℤ,
      normalStep e12 0 (normalStep e21 0 x) =
      normalStep e21 0 (normalStep e12 0 x)) := by
  rw [left_only_commute_iff]
  intro h
  have hc := congrArg (fun m : Matrix (Fin 2) (Fin 2) ℤ => m 0 0) h.eq
  norm_num [e12, e21, Matrix.mul_apply, Fin.sum_univ_two] at hc

end HMT.NormalProductAlgebra

#print axioms HMT.NormalProductAlgebra.normalStep_commutator
#print axioms HMT.NormalProductAlgebra.normalStep_commute
#print axioms HMT.NormalProductAlgebra.left_only_commute_iff
#print axioms HMT.NormalProductAlgebra.right_only_commute_iff
#print axioms HMT.NormalProductAlgebra.noncommuting_left_counterexample
