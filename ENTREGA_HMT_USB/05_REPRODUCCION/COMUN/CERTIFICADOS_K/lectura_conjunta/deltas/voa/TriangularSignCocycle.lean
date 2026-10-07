import Mathlib

/-! The upper-triangular cocycle is derived from its explicit finite sum.
Symmetry and zero diagonal are used only in the commutator identity.
No cocycle identity is an input. -/
namespace HMT.IV.TriangularCocycle

abbrev Vec (n : ℕ) := Fin n → ZMod 2

def bilinear {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x y : Vec n) : ZMod 2 :=
  ∑ i, ∑ j, x i * G i j * y j

def triangle {n : ℕ} (G : Fin n → Fin n → ZMod 2) (i j : Fin n) : ZMod 2 :=
  if i < j then G i j else 0

def tau {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x y : Vec n) : ZMod 2 :=
  bilinear (triangle G) x y

theorem tau_zero_left {n : ℕ} (G : Fin n → Fin n → ZMod 2) (y : Vec n) :
    tau G 0 y = 0 := by
  simp [tau, bilinear]

theorem tau_zero_right {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x : Vec n) :
    tau G x 0 = 0 := by
  simp [tau, bilinear]

theorem tau_add_left {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x y z : Vec n) :
    tau G (x + y) z = tau G x z + tau G y z := by
  simp [tau, bilinear, add_mul, Finset.sum_add_distrib]

theorem tau_add_right {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x y z : Vec n) :
    tau G x (y + z) = tau G x y + tau G x z := by
  simp [tau, bilinear, mul_add, Finset.sum_add_distrib]

theorem tau_cocycle {n : ℕ} (G : Fin n → Fin n → ZMod 2) (x y z : Vec n) :
    tau G x y + tau G (x + y) z = tau G y z + tau G x (y + z) := by
  rw [tau_add_left, tau_add_right]
  ring

theorem triangle_transpose_sum {n : ℕ} (G : Fin n → Fin n → ZMod 2)
    (hG : ∀ i j, G i j = G j i) (hdiag : ∀ i, G i i = 0) (i j : Fin n) :
    triangle G i j + triangle G j i = G i j := by
  by_cases h : i = j
  · subst j
    simp [triangle, hdiag]
  · rcases lt_or_gt_of_ne h with hlt | hgt
    · simp [triangle, hlt, not_lt_of_ge hlt.le]
    · simp [triangle, hgt, not_lt_of_ge hgt.le, hG j i]

theorem tau_commutator {n : ℕ} (G : Fin n → Fin n → ZMod 2)
    (hG : ∀ i j, G i j = G j i) (hdiag : ∀ i, G i i = 0) (x y : Vec n) :
    tau G x y + tau G y x = bilinear G x y := by
  have flip : tau G y x = ∑ i, ∑ j, x i * triangle G j i * y j := by
    unfold tau bilinear
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    apply Finset.sum_congr rfl
    intro j _
    ring
  rw [flip]
  unfold tau bilinear
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  calc
    x i * triangle G i j * y j + x i * triangle G j i * y j =
        x i * (triangle G i j + triangle G j i) * y j := by ring
    _ = x i * G i j * y j := by rw [triangle_transpose_sum G hG hdiag]

def sign (z : ZMod 2) : ℤ := if z = 0 then 1 else -1

theorem sign_zero : sign 0 = 1 := by decide

theorem sign_add (a b : ZMod 2) : sign (a+b) = sign a * sign b := by
  fin_cases a <;> fin_cases b <;> decide

theorem sign_sq (a : ZMod 2) : sign a * sign a = 1 := by
  fin_cases a <;> decide

#print axioms tau_zero_left
#print axioms tau_zero_right
#print axioms tau_add_left
#print axioms tau_add_right
#print axioms tau_cocycle
#print axioms triangle_transpose_sum
#print axioms tau_commutator
#print axioms sign_zero
#print axioms sign_add
#print axioms sign_sq

end HMT.IV.TriangularCocycle
