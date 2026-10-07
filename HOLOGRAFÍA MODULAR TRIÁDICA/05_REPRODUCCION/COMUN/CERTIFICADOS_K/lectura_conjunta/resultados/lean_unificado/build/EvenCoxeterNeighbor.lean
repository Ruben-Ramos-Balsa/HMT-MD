import CoxeterNeighbor

/-!
# Evenness of ternary glue and the marked index-three neighbour

The existing Paley--Witt code and its proved self-orthogonality supply the
divisibility of the integral lift's squared coordinates by three. Evenness
is deduced, not supplied to the displayed-code endpoint. The marked radial
vector has squared norm 54 at every origin. This result does not identify
the neighbour with Leech or construct a VOA.
-/

namespace HMT.IV.CoxeterNeighbor

def EvenGlue {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) : Prop :=
  ∀ x ∈ glue C, ∃ k : ℤ, pairing x x = 2 * (k : ℚ)

def EvenNeighbor {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n) : Prop :=
  ∀ x ∈ neighbor C v, ∃ k : ℤ, pairing x x = 2 * (k : ℚ)

/-- Self-orthogonality controls the squared lift, independently of which
integer representative of the ternary word is chosen. -/
theorem squared_lift_divisible_by_three {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : SelfOrthogonal C)
    (c : Fin n → ℤ) (hc : (fun i => (c i : ZMod 3)) ∈ C) :
    (3 : ℤ) ∣ ∑ i, c i * c i := by
  have hz : ((∑ i, c i * c i : ℤ) : ZMod 3) = 0 := by
    simpa only [Int.cast_sum, Int.cast_mul] using hC _ hc _ hc
  exact (ZMod.intCast_zmod_eq_zero_iff_dvd _ 3).mp hz

/-- The parity of the complete glue is obtained from its actual coordinate
formula, rather than inferred from integrality alone. -/
theorem evenGlue_of_selfOrthogonal {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (hC : SelfOrthogonal C) : EvenGlue C := by
  rintro x ⟨a, b, c, hc, hx⟩
  obtain ⟨k, hk⟩ := squared_lift_divisible_by_three C hC c hc
  let r : ℤ := ∑ i, (a i * a i - a i * b i + b i * b i + a i * c i)
  have hpair : pairing x x = 2 * (r : ℚ) +
      2 * (∑ i, (c i : ℚ) * c i) / 3 := by
    simp only [pairing, r, Int.cast_sum, Int.cast_add, Int.cast_sub,
      Int.cast_mul]
    rw [Finset.mul_sum, Finset.mul_sum, Finset.sum_div, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    rw [hx]
    dsimp [localPair]
    ring
  refine ⟨r + k, ?_⟩
  have hkq := congrArg (fun z : ℤ => (z : ℚ)) hk
  push_cast at hkq ⊢
  rw [hpair, hkq]
  ring

theorem radial_norm_formula {n : ℕ} (t : Fin n → ℤ) :
    pairing (radial t) (radial t) = 2 * ∑ i, (1 + 3 * (t i : ℚ)) ^ 2 := by
  unfold pairing
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  dsimp [radial, localPair]
  ring

/-- One radial coefficient is four, the other eleven are one; the origin is arbitrary. -/
theorem marked_radial_norm (o : Fin 12) :
    pairing (radial (marked o)) (radial (marked o)) = 54 := by
  rw [radial_norm_formula]
  have hterm : (fun i : Fin 12 => (1 + 3 * ((marked o i : ℤ) : ℚ)) ^ 2) =
      fun i => 1 + if i = o then 15 else 0 := by
    funext i
    by_cases h : i = o <;> norm_num [marked, h]
  rw [hterm, Finset.sum_add_distrib]
  norm_num

theorem neighbor_norm_formula {n : ℕ} (x v : Space n) (k : ℤ) :
    pairing (x + (k : ℚ) • ((1 / 3 : ℚ) • v))
        (x + (k : ℚ) • ((1 / 3 : ℚ) • v)) =
      pairing x x + (2 * (k : ℚ) / 3) * pairing x v +
        ((k : ℚ) ^ 2 / 9) * pairing v v := by
  rw [pairing_add_left, pairing_add_right, pairing_add_right]
  simp only [pairing_smul_left, pairing_smul_right, pairing_comm v x]
  ring

/-- General index-three parity step. The norm divisibility is an explicit
premise here and is discharged by the marked vector in the terminal below. -/
theorem evenNeighbor_of_evenGlue {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (v : Space n)
    (hC : EvenGlue C) (hv : ∃ l : ℤ, pairing v v = 18 * (l : ℚ)) :
    EvenNeighbor C v := by
  rintro w ⟨x, hx, k, rfl⟩
  obtain ⟨m, hm⟩ := hC x hx.1
  obtain ⟨j, hj⟩ := hx.2
  obtain ⟨l, hl⟩ := hv
  refine ⟨m + k * j + k * k * l, ?_⟩
  rw [neighbor_norm_formula, hm, hj, hl]
  push_cast
  ring

theorem marked_neighbor_even_of_selfOrthogonal
    (C : AddSubgroup (Fin 12 → ZMod 3)) (hC : SelfOrthogonal C) (o : Fin 12) :
    EvenNeighbor C (radial (marked o)) := by
  apply evenNeighbor_of_evenGlue C _ (evenGlue_of_selfOrthogonal C hC)
  exact ⟨3, by rw [marked_radial_norm]; norm_num⟩

/-- Evenness of the explicitly displayed Paley--Witt glue, without a parity assumption. -/
theorem witt_glue_even : EvenGlue wittCode :=
  evenGlue_of_selfOrthogonal wittCode wittCode_selfOrthogonal

/-- The displayed-code neighbour is even for every marked origin. -/
theorem witt_marked_neighbor_even (o : Fin 12) :
    EvenNeighbor wittCode (radial (marked o)) :=
  marked_neighbor_even_of_selfOrthogonal wittCode wittCode_selfOrthogonal o

/-- Norm and neighbour parity are obtained together from the construction. -/
theorem witt_marked_even_construction (o : Fin 12) :
    pairing (radial (marked o)) (radial (marked o)) = 54 ∧
    EvenGlue wittCode ∧ EvenNeighbor wittCode (radial (marked o)) :=
  ⟨marked_radial_norm o, witt_glue_even, witt_marked_neighbor_even o⟩

#print axioms squared_lift_divisible_by_three
#print axioms evenGlue_of_selfOrthogonal
#print axioms radial_norm_formula
#print axioms marked_radial_norm
#print axioms neighbor_norm_formula
#print axioms evenNeighbor_of_evenGlue
#print axioms marked_neighbor_even_of_selfOrthogonal
#print axioms witt_glue_even
#print axioms witt_marked_neighbor_even
#print axioms witt_marked_even_construction

end HMT.IV.CoxeterNeighbor
