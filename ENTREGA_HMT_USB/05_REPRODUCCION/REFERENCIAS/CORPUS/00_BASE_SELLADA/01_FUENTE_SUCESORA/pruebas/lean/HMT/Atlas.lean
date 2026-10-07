/-!
HMT-LEAN-KERNEL-01, microcertificado del atlas cuadrático nonádico.

Este archivo usa sólo Lean 4 core. Las igualdades finitas son comprobadas por
reducción del kernel mediante `decide`; no usa `native_decide`.
-/

namespace HMT

abbrev F3 := Fin 3
abbrev I6 := Fin 6

def AW (i j : I6) : F3 :=
  match i.val, j.val with
  | 0, 0 => 0 | 0, 1 => 1 | 0, 2 => 1 | 0, 3 => 1 | 0, 4 => 1 | 0, 5 => 1
  | 1, 0 => 1 | 1, 1 => 0 | 1, 2 => 1 | 1, 3 => 2 | 1, 4 => 2 | 1, 5 => 1
  | 2, 0 => 1 | 2, 1 => 1 | 2, 2 => 0 | 2, 3 => 1 | 2, 4 => 2 | 2, 5 => 2
  | 3, 0 => 1 | 3, 1 => 2 | 3, 2 => 1 | 3, 3 => 0 | 3, 4 => 1 | 3, 5 => 2
  | 4, 0 => 1 | 4, 1 => 2 | 4, 2 => 2 | 4, 3 => 1 | 4, 4 => 0 | 4, 5 => 1
  | 5, 0 => 1 | 5, 1 => 1 | 5, 2 => 2 | 5, 3 => 2 | 5, 4 => 1 | 5, 5 => 0
  | _, _ => 0

def sum6 (f : I6 → F3) : F3 :=
  f 0 + f 1 + f 2 + f 3 + f 4 + f 5

def matMul (A B : I6 → I6 → F3) (i j : I6) : F3 :=
  sum6 (fun k => A i k * B k j)

def negIdentity (i j : I6) : F3 :=
  if i = j then 2 else 0

theorem aw_symmetric : ∀ i j : I6, AW i j = AW j i := by decide

theorem aw_square_minus_identity :
    ∀ i j : I6, matMul AW AW i j = negIdentity i j := by decide

def L1 (i j : I6) : F3 :=
  match i.val, j.val with
  | 0, 0 => 2 | 0, 1 => 1 | 0, 2 => 2 | 0, 3 => 0 | 0, 4 => 2 | 0, 5 => 2
  | 1, 0 => 1 | 1, 1 => 2 | 1, 2 => 1 | 1, 3 => 1 | 1, 4 => 2 | 1, 5 => 0
  | 2, 0 => 1 | 2, 1 => 2 | 2, 2 => 1 | 2, 3 => 1 | 2, 4 => 1 | 2, 5 => 2
  | 3, 0 => 0 | 3, 1 => 1 | 3, 2 => 0 | 3, 3 => 0 | 3, 4 => 2 | 3, 5 => 1
  | 4, 0 => 2 | 4, 1 => 0 | 4, 2 => 2 | 4, 3 => 1 | 4, 4 => 0 | 4, 5 => 1
  | 5, 0 => 0 | 5, 1 => 2 | 5, 2 => 2 | 5, 3 => 2 | 5, 4 => 1 | 5, 5 => 1
  | _, _ => 0

def rowMul (v : I6 → F3) (A : I6 → I6 → F3) (j : I6) : F3 :=
  sum6 (fun i => v i * A i j)

def u4Phi : I6 → F3
  | 0 => 0 | 1 => 1 | 2 => 0 | 3 => 2 | 4 => 0 | 5 => 0

def u008Transport : I6 → F3
  | 0 => 1 | 1 => 1 | 2 => 1 | 3 => 1 | 4 => 0 | 5 => 1

def bPlusPi : I6 → F3
  | 0 => 2 | 1 => 2 | 2 => 2 | 3 => 2 | 4 => 2 | 5 => 0

def bPlusE : I6 → F3
  | 0 => 0 | 1 => 2 | 2 => 1 | 3 => 2 | 4 => 2 | 5 => 2

def u008Aggregate (j : I6) : F3 := bPlusPi j + bPlusE j

theorem u008_phi_aw_l1_cubed :
    ∀ j : I6,
      rowMul (rowMul (rowMul (rowMul u4Phi AW) L1) L1) L1 j =
        u008Transport j := by decide

theorem u008_lateral_aggregate :
    u008Aggregate 0 = 2 ∧ u008Aggregate 1 = 1 ∧
    u008Aggregate 2 = 0 ∧ u008Aggregate 3 = 1 ∧
    u008Aggregate 4 = 1 ∧ u008Aggregate 5 = 2 := by decide

theorem u008_outputs_are_distinct : u008Aggregate ≠ u008Transport := by
  intro h
  have h0 : u008Aggregate 0 = u008Transport 0 := congrFun h 0
  have hne : u008Aggregate 0 ≠ u008Transport 0 := by decide
  exact hne h0

theorem x_sq_add_one_has_no_root :
    ∀ x : F3, x * x + 1 ≠ 0 := by decide

def dualMul (x y : F3 × F3) : F3 × F3 :=
  (x.1 * y.1, x.1 * y.2 + x.2 * y.1)

def splitMul (x y : F3 × F3) : F3 × F3 :=
  (x.1 * y.1 + x.2 * y.2, x.1 * y.2 + x.2 * y.1)

theorem dual_has_nonzero_nilpotent :
    (0, 1) ≠ (0, 0) ∧ dualMul (0, 1) (0, 1) = (0, 0) := by decide

theorem split_has_nontrivial_idempotent :
    (2, 2) ≠ (0, 0) ∧ (2, 2) ≠ (1, 0) ∧
      splitMul (2, 2) (2, 2) = (2, 2) := by decide

end HMT
