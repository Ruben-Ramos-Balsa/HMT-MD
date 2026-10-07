import Mathlib.Algebra.Vertex.VertexOperator

/-!
# Assembly of four heterogeneous vertex-operator blocks

The inputs are already Laurent fields, linear in the state.  Their four blocks
assemble into a Laurent field on `E × T`.  This construction asserts neither
locality nor the existence of any particular orbifold input blocks.
-/

noncomputable section

namespace HMT.IV.VertexBlockAssembly

variable (R E T : Type*) [CommRing R]
  [AddCommGroup E] [Module R E] [AddCommGroup T] [Module R T]

/-- Four fields with the parity-compatible input and output types. -/
structure Blocks where
  ee : E →ₗ[R] HVertexOperator ℤ R E E
  et : E →ₗ[R] HVertexOperator ℤ R T T
  te : T →ₗ[R] HVertexOperator ℤ R E T
  tt : T →ₗ[R] HVertexOperator ℤ R T E

variable {R E T}

/-- The coefficient matrix acting on the product of the two sectors. -/
def coefficient (B : Blocks R E T) (u : E × T) (k : ℤ) :
    Module.End R (E × T) where
  toFun v :=
    (HVertexOperator.coeff (B.ee u.1) k v.1 +
      HVertexOperator.coeff (B.tt u.2) k v.2,
     HVertexOperator.coeff (B.et u.1) k v.2 +
      HVertexOperator.coeff (B.te u.2) k v.1)
  map_add' v w := by
    ext <;> simp [add_assoc, add_left_comm, add_comm]
  map_smul' r v := by
    ext <;> simp [smul_add]

@[simp]
theorem coefficient_apply (B : Blocks R E T) (u v : E × T) (k : ℤ) :
    coefficient B u k v =
      (HVertexOperator.coeff (B.ee u.1) k v.1 +
        HVertexOperator.coeff (B.tt u.2) k v.2,
       HVertexOperator.coeff (B.et u.1) k v.2 +
        HVertexOperator.coeff (B.te u.2) k v.1) := rfl

/-- A common lower bound is the minimum of the four pointwise Laurent bounds.
It may depend on both the state and the vector on which the field acts. -/
theorem coefficient_bounded_pole (B : Blocks R E T) (u : E × T) :
    ∀ v : E × T, ∃ n : ℤ, ∀ k : ℤ, k < n → coefficient B u k v = 0 := by
  intro v
  let a := HahnSeries.order ((HahnModule.of R).symm (B.ee u.1 v.1))
  let b := HahnSeries.order ((HahnModule.of R).symm (B.tt u.2 v.2))
  let c := HahnSeries.order ((HahnModule.of R).symm (B.et u.1 v.2))
  let d := HahnSeries.order ((HahnModule.of R).symm (B.te u.2 v.1))
  refine ⟨min (min a b) (min c d), ?_⟩
  intro k hk
  have ha : HVertexOperator.coeff (B.ee u.1) k v.1 = 0 :=
    HahnSeries.coeff_eq_zero_of_lt_order
      (lt_of_lt_of_le hk (le_trans (min_le_left _ _) (min_le_left _ _)))
  have hb : HVertexOperator.coeff (B.tt u.2) k v.2 = 0 :=
    HahnSeries.coeff_eq_zero_of_lt_order
      (lt_of_lt_of_le hk (le_trans (min_le_left _ _) (min_le_right _ _)))
  have hc : HVertexOperator.coeff (B.et u.1) k v.2 = 0 :=
    HahnSeries.coeff_eq_zero_of_lt_order
      (lt_of_lt_of_le hk (le_trans (min_le_right _ _) (min_le_left _ _)))
  have hd : HVertexOperator.coeff (B.te u.2) k v.1 = 0 :=
    HahnSeries.coeff_eq_zero_of_lt_order
      (lt_of_lt_of_le hk (le_trans (min_le_right _ _) (min_le_right _ _)))
  simp only [coefficient_apply, ha, hb, hc, hd, zero_add, Prod.zero_eq_mk]

/-- The assembled coefficient matrix defines a genuine Laurent field. -/
def field (B : Blocks R E T) (u : E × T) : VertexOperator R (E × T) :=
  VertexOperator.of_coeff (coefficient B u) (coefficient_bounded_pole B u)

@[simp]
theorem field_coefficient (B : Blocks R E T) (u : E × T) (k : ℤ) :
    HVertexOperator.coeff (field B u) k = coefficient B u k := by
  rfl

theorem coefficient_add (B : Blocks R E T) (u v : E × T) (k : ℤ) :
    coefficient B (u + v) k = coefficient B u k + coefficient B v k := by
  apply LinearMap.ext
  intro w
  change
    (HVertexOperator.coeff (B.ee (u.1 + v.1)) k w.1 +
       HVertexOperator.coeff (B.tt (u.2 + v.2)) k w.2,
     HVertexOperator.coeff (B.et (u.1 + v.1)) k w.2 +
       HVertexOperator.coeff (B.te (u.2 + v.2)) k w.1) =
    ((HVertexOperator.coeff (B.ee u.1) k w.1 +
       HVertexOperator.coeff (B.tt u.2) k w.2) +
      (HVertexOperator.coeff (B.ee v.1) k w.1 +
       HVertexOperator.coeff (B.tt v.2) k w.2),
     (HVertexOperator.coeff (B.et u.1) k w.2 +
       HVertexOperator.coeff (B.te u.2) k w.1) +
      (HVertexOperator.coeff (B.et v.1) k w.2 +
       HVertexOperator.coeff (B.te v.2) k w.1))
  simp only [map_add, HVertexOperator.coeff_add, Pi.add_apply, LinearMap.add_apply]
  exact Prod.ext (add_add_add_comm _ _ _ _) (add_add_add_comm _ _ _ _)

theorem coefficient_smul (B : Blocks R E T) (r : R) (u : E × T) (k : ℤ) :
    coefficient B (r • u) k = r • coefficient B u k := by
  ext w <;> simp [coefficient, HVertexOperator.coeff_smul, smul_add]

/-- The assembled field is linear in its state. -/
def fieldMap (B : Blocks R E T) : (E × T) →ₗ[R] VertexOperator R (E × T) where
  toFun := field B
  map_add' u v := by
    apply HVertexOperator.coeff_inj
    funext k
    simp only [field_coefficient, HVertexOperator.coeff_add, Pi.add_apply,
      coefficient_add]
  map_smul' r u := by
    apply HVertexOperator.coeff_inj
    funext k
    simp only [field_coefficient, HVertexOperator.coeff_smul, Pi.smul_apply,
      coefficient_smul, RingHom.id_apply]

@[simp]
theorem fieldMap_apply (B : Blocks R E T) (u : E × T) :
    fieldMap B u = field B u := rfl

@[simp]
theorem coefficient_even_even (B : Blocks R E T) (e v : E) (k : ℤ) :
    coefficient B (e, 0) k (v, 0) =
      (HVertexOperator.coeff (B.ee e) k v, 0) := by
  simp [coefficient, HVertexOperator.coeff]

@[simp]
theorem coefficient_even_twisted (B : Blocks R E T) (e : E) (t : T) (k : ℤ) :
    coefficient B (e, 0) k (0, t) =
      (0, HVertexOperator.coeff (B.et e) k t) := by
  simp [coefficient, HVertexOperator.coeff]

@[simp]
theorem coefficient_twisted_even (B : Blocks R E T) (t : T) (e : E) (k : ℤ) :
    coefficient B (0, t) k (e, 0) =
      (0, HVertexOperator.coeff (B.te t) k e) := by
  simp [coefficient, HVertexOperator.coeff]

@[simp]
theorem coefficient_twisted_twisted (B : Blocks R E T) (t v : T) (k : ℤ) :
    coefficient B (0, t) k (0, v) =
      (HVertexOperator.coeff (B.tt t) k v, 0) := by
  simp [coefficient, HVertexOperator.coeff]

@[simp]
theorem field_even_even (B : Blocks R E T) (e v : E) (k : ℤ) :
    HVertexOperator.coeff (field B (e, 0)) k (v, 0) =
      (HVertexOperator.coeff (B.ee e) k v, 0) := by
  rw [field_coefficient]
  exact coefficient_even_even B e v k

@[simp]
theorem field_even_twisted (B : Blocks R E T) (e : E) (t : T) (k : ℤ) :
    HVertexOperator.coeff (field B (e, 0)) k (0, t) =
      (0, HVertexOperator.coeff (B.et e) k t) := by
  rw [field_coefficient]
  exact coefficient_even_twisted B e t k

@[simp]
theorem field_twisted_even (B : Blocks R E T) (t : T) (e : E) (k : ℤ) :
    HVertexOperator.coeff (field B (0, t)) k (e, 0) =
      (0, HVertexOperator.coeff (B.te t) k e) := by
  rw [field_coefficient]
  exact coefficient_twisted_even B t e k

@[simp]
theorem field_twisted_twisted (B : Blocks R E T) (t v : T) (k : ℤ) :
    HVertexOperator.coeff (field B (0, t)) k (0, v) =
      (HVertexOperator.coeff (B.tt t) k v, 0) := by
  rw [field_coefficient]
  exact coefficient_twisted_twisted B t v k

end HMT.IV.VertexBlockAssembly

