import EvenCoxeterNeighbor

/-!
The marked neighbour is an additive subgroup, and its bilinear form is
integer-valued. These are consequences of the constructed kernel and radial
norm. No recognition as the Leech lattice or any VOA is asserted here.
-/
namespace HMT.IV.CoxeterNeighbor

def kernelSubgroup {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (v : Space n) : AddSubgroup (Space n) where
  carrier := kernel C v
  zero_mem' := by
    refine ⟨(glue C).zero_mem, 0, ?_⟩
    simp [pairing, localPair]
  add_mem' := by
    rintro x y ⟨hx, a, ha⟩ ⟨hy, b, hb⟩
    refine ⟨(glue C).add_mem hx hy, a + b, ?_⟩
    rw [pairing_add_left, ha, hb]
    push_cast
    ring
  neg_mem' := by
    rintro x ⟨hx, a, ha⟩
    refine ⟨(glue C).neg_mem hx, -a, ?_⟩
    have hneg : -x = (-1 : ℚ) • x := by simp
    rw [hneg, pairing_smul_left, ha]
    push_cast
    ring

/-- The neighbour uses arbitrary integral multiples of the marked third.
Its subgroup laws do not require recognition by a classical lattice name. -/
def neighborSubgroup {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (v : Space n) : AddSubgroup (Space n) where
  carrier := neighbor C v
  zero_mem' := by
    refine ⟨0, (kernelSubgroup C v).zero_mem, 0, ?_⟩
    simp
  add_mem' := by
    rintro x y ⟨a, ha, k, rfl⟩ ⟨b, hb, l, rfl⟩
    refine ⟨a + b, (kernelSubgroup C v).add_mem ha hb, k + l, ?_⟩
    push_cast
    rw [add_smul]
    abel
  neg_mem' := by
    rintro x ⟨a, ha, k, rfl⟩
    refine ⟨-a, (kernelSubgroup C v).neg_mem ha, -k, ?_⟩
    push_cast
    rw [neg_smul]
    abel

theorem neighbor_subgroup_carrier {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) :
    (neighborSubgroup C v : Set (Space n)) = neighbor C v := rfl

def IntegralNeighbor {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (v : Space n) : Prop :=
  ∀ x ∈ neighbor C v, ∀ y ∈ neighbor C v, ∃ k : ℤ, pairing x y = k

theorem neighbor_pairing_formula {n : ℕ} (x y v : Space n) (k l : ℤ) :
    pairing (x + (k : ℚ) • ((1 / 3 : ℚ) • v))
      (y + (l : ℚ) • ((1 / 3 : ℚ) • v)) =
      pairing x y + ((l : ℚ) / 3) * pairing x v +
      ((k : ℚ) / 3) * pairing y v +
      (((k : ℚ) * (l : ℚ)) / 9) * pairing v v := by
  rw [pairing_add_left, pairing_add_right, pairing_add_right]
  simp only [pairing_smul_left, pairing_smul_right, pairing_comm v y]
  ring

/-- Integrality uses the whole source glue and the kernel congruences. -/
theorem integralNeighbor_of_integralGlue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n)
    (hC : IntegralGlue C) (hv : ∃ q : ℤ, pairing v v = 9 * (q : ℚ)) :
    IntegralNeighbor C v := by
  rintro x ⟨a, ha, k, rfl⟩ y ⟨b, hb, l, rfl⟩
  obtain ⟨r, hr⟩ := hC a ha.1 b hb.1
  obtain ⟨i, hi⟩ := ha.2
  obtain ⟨j, hj⟩ := hb.2
  obtain ⟨q, hq⟩ := hv
  refine ⟨r + l * i + k * j + k * l * q, ?_⟩
  rw [neighbor_pairing_formula, hr, hi, hj, hq]
  push_cast
  ring

theorem witt_marked_neighbor_integral (o : Fin 12) :
    IntegralNeighbor wittCode (radial (marked o)) := by
  apply integralNeighbor_of_integralGlue wittCode _
    (integralGlue_of_selfOrthogonal wittCode wittCode_selfOrthogonal)
  exact ⟨6, by rw [marked_radial_norm]; norm_num⟩

/-- The stated even, integral additive realization, at any marked origin. -/
theorem witt_marked_even_integral_group (o : Fin 12) :
    (neighborSubgroup wittCode (radial (marked o)) : Set (Space 12)) =
      neighbor wittCode (radial (marked o)) ∧
    EvenNeighbor wittCode (radial (marked o)) ∧
    IntegralNeighbor wittCode (radial (marked o)) :=
  ⟨rfl, witt_marked_neighbor_even o, witt_marked_neighbor_integral o⟩

#print axioms kernelSubgroup
#print axioms neighborSubgroup
#print axioms neighbor_subgroup_carrier
#print axioms neighbor_pairing_formula
#print axioms integralNeighbor_of_integralGlue
#print axioms witt_marked_neighbor_integral
#print axioms witt_marked_even_integral_group

end HMT.IV.CoxeterNeighbor
