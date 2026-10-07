import MarkedNeighborFinite

namespace HMT.IV.LatticeCocycle

open HMT.IV.CoxeterNeighbor HMT.IV.NeighborLattice

abbrev Lattice (o : Fin 12) := neighborSubgroup wittCode (radial (marked o))

instance latticeFinite (o : Fin 12) : Module.Finite ℤ (Lattice o) :=
  witt_marked_module_finite o

instance latticeFree (o : Fin 12) : Module.Free ℤ (Lattice o) :=
  witt_marked_module_free o

noncomputable def integerPair (o : Fin 12) (x y : Lattice o) : ℤ :=
  Classical.choose (witt_marked_neighbor_integral o x x.property y y.property)

theorem cast_integerPair (o : Fin 12) (x y : Lattice o) :
    (integerPair o x y : ℚ) = pairing (x : Space 12) (y : Space 12) :=
  (Classical.choose_spec (witt_marked_neighbor_integral o x x.property y y.property)).symm

theorem integerPair_comm (o : Fin 12) (x y : Lattice o) :
    integerPair o x y = integerPair o y x := by
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair, cast_integerPair, pairing_comm]

theorem integerPair_add_left (o : Fin 12) (x y z : Lattice o) :
    integerPair o (x+y) z = integerPair o x z + integerPair o y z := by
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair, Int.cast_add, cast_integerPair, cast_integerPair]
  exact pairing_add_left (x : Space 12) (y : Space 12) (z : Space 12)

theorem integerPair_add_right (o : Fin 12) (x y z : Lattice o) :
    integerPair o x (y+z) = integerPair o x y + integerPair o x z := by
  rw [integerPair_comm o x, integerPair_add_left,
    integerPair_comm o y, integerPair_comm o z]

theorem integerPair_zero_left (o : Fin 12) (x : Lattice o) : integerPair o 0 x = 0 := by
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair]
  simp [pairing, localPair]

theorem integerPair_zero_right (o : Fin 12) (x : Lattice o) : integerPair o x 0 = 0 := by
  rw [integerPair_comm, integerPair_zero_left]

theorem integerPair_smul_left (o : Fin 12) (k : ℤ) (x y : Lattice o) :
    integerPair o (k • x) y = k * integerPair o x y := by
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair, Int.cast_mul, cast_integerPair]
  change pairing (k • (x : Space 12)) (y : Space 12) = _
  rw [← Int.cast_smul_eq_zsmul (R := ℚ), pairing_smul_left]

theorem integerPair_smul_right (o : Fin 12) (k : ℤ) (x y : Lattice o) :
    integerPair o x (k • y) = k * integerPair o x y := by
  rw [integerPair_comm, integerPair_smul_left, integerPair_comm o y]

theorem integerPair_even (o : Fin 12) (x : Lattice o) :
    ∃ k : ℤ, integerPair o x x = 2*k := by
  obtain ⟨k, hk⟩ := witt_marked_neighbor_even o x x.property
  refine ⟨k, ?_⟩
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair, hk]
  push_cast
  rfl

noncomputable def parityPair (o : Fin 12) (x y : Lattice o) : ZMod 2 := integerPair o x y

noncomputable def parityBilinear (o : Fin 12) :
    Lattice o →ₗ[ℤ] Lattice o →ₗ[ℤ] ZMod 2 where
  toFun := fun x => {
    toFun := parityPair o x
    map_add' := fun y z => by simp [parityPair, integerPair_add_right]
    map_smul' := fun k y => by simp [parityPair, integerPair_smul_right, zsmul_eq_mul] }
  map_add' := by
    intro x y
    ext z
    simp [parityPair, integerPair_add_left]
  map_smul' := by
    intro k x
    ext y
    simp [parityPair, integerPair_smul_left, zsmul_eq_mul]

theorem parityBilinear_apply (o : Fin 12) (x y : Lattice o) :
    parityBilinear o x y = (integerPair o x y : ZMod 2) := rfl

theorem parityPair_comm (o : Fin 12) (x y : Lattice o) :
    parityBilinear o x y = parityBilinear o y x := by
  simp only [parityBilinear_apply, integerPair_comm]

theorem parityPair_self_zero (o : Fin 12) (x : Lattice o) :
    parityBilinear o x x = 0 := by
  obtain ⟨k, hk⟩ := integerPair_even o x
  rw [parityBilinear_apply, hk]
  have h2 : (2 : ZMod 2) = 0 := by decide
  push_cast
  rw [h2, zero_mul]

#print axioms latticeFinite
#print axioms latticeFree
#print axioms cast_integerPair
#print axioms integerPair_comm
#print axioms integerPair_add_left
#print axioms integerPair_add_right
#print axioms integerPair_zero_left
#print axioms integerPair_zero_right
#print axioms integerPair_smul_left
#print axioms integerPair_smul_right
#print axioms integerPair_even
#print axioms parityBilinear
#print axioms parityBilinear_apply
#print axioms parityPair_comm
#print axioms parityPair_self_zero

end HMT.IV.LatticeCocycle
