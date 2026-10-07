import MarkedNeighborSpan

/-! Finite generation over the integers of the constructed marked neighbour.
The integral-coordinate embedding is derived from the denominator-three theorem.
This is finite generation of a module, not finiteness of its underlying set. -/
namespace HMT.IV.NeighborLattice

open HMT.IV.CoxeterNeighbor HMT.IV.NeighborSpan

abbrev NeighborModule {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) := neighborSubgroup C (radial t)

noncomputable def coordinateA {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) (x : NeighborModule C t) : Fin n → ℤ :=
  Classical.choose (neighbor_coordinates_thirds C t x.property)

noncomputable def coordinateB {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) (x : NeighborModule C t) : Fin n → ℤ :=
  Classical.choose (Classical.choose_spec (neighbor_coordinates_thirds C t x.property))

theorem coordinate_spec {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) (x : NeighborModule C t) (i : Fin n) :
    (x : Space n) i = ((coordinateA C t x i : ℚ)/3,
      (coordinateB C t x i : ℚ)/3) :=
  Classical.choose_spec (Classical.choose_spec (neighbor_coordinates_thirds C t x.property)) i

theorem coordinateA_cast {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) (x : NeighborModule C t) (i : Fin n) :
    (coordinateA C t x i : ℚ) = 3 * ((x : Space n) i).1 := by
  have h := congrArg Prod.fst (coordinate_spec C t x i)
  dsimp only at h
  linarith

theorem coordinateB_cast {n : ℕ} (C : AddSubgroup (Fin n → ZMod 3))
    (t : Fin n → ℤ) (x : NeighborModule C t) (i : Fin n) :
    (coordinateB C t x i : ℚ) = 3 * ((x : Space n) i).2 := by
  have h := congrArg Prod.snd (coordinate_spec C t x i)
  dsimp only at h
  linarith

noncomputable def integralCoordinateMap {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    NeighborModule C t →ₗ[ℤ] (Fin n → ℤ × ℤ) where
  toFun := fun x i => (coordinateA C t x i, coordinateB C t x i)
  map_add' := by
    intro x y
    funext i
    apply Prod.ext
    · apply Int.cast_injective (α := ℚ)
      change (coordinateA C t (x+y) i : ℚ) =
        ((coordinateA C t x i + coordinateA C t y i : ℤ):ℚ)
      rw [Int.cast_add, coordinateA_cast, coordinateA_cast, coordinateA_cast]
      simp
      ring
    · apply Int.cast_injective (α := ℚ)
      change (coordinateB C t (x+y) i : ℚ) =
        ((coordinateB C t x i + coordinateB C t y i : ℤ):ℚ)
      rw [Int.cast_add, coordinateB_cast, coordinateB_cast, coordinateB_cast]
      simp
      ring
  map_smul' := by
    intro k x
    funext i
    apply Prod.ext
    · apply Int.cast_injective (α := ℚ)
      change (coordinateA C t (k • x) i : ℚ) = ((k * coordinateA C t x i : ℤ):ℚ)
      rw [Int.cast_mul, coordinateA_cast, coordinateA_cast]
      simp
      ring
    · apply Int.cast_injective (α := ℚ)
      change (coordinateB C t (k • x) i : ℚ) = ((k * coordinateB C t x i : ℤ):ℚ)
      rw [Int.cast_mul, coordinateB_cast, coordinateB_cast]
      simp
      ring

theorem integralCoordinateMap_injective {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    Function.Injective (integralCoordinateMap C t) := by
  intro x y h
  apply Subtype.ext
  funext i
  apply Prod.ext
  · have hi := congrArg (fun f : Fin n → ℤ × ℤ => (f i).1) h
    change coordinateA C t x i = coordinateA C t y i at hi
    have hq := congrArg (fun a : ℤ => (a:ℚ)) hi
    dsimp only at hq
    rw [coordinateA_cast, coordinateA_cast] at hq
    linarith
  · have hi := congrArg (fun f : Fin n → ℤ × ℤ => (f i).2) h
    change coordinateB C t x i = coordinateB C t y i at hi
    have hq := congrArg (fun a : ℤ => (a:ℚ)) hi
    dsimp only at hq
    rw [coordinateB_cast, coordinateB_cast] at hq
    linarith

theorem neighbor_module_finite {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    Module.Finite ℤ (NeighborModule C t) :=
  Module.Finite.of_injective (integralCoordinateMap C t)
    (integralCoordinateMap_injective C t)

theorem witt_marked_module_finite (o : Fin 12) :
    Module.Finite ℤ (neighborSubgroup wittCode (radial (marked o))) :=
  neighbor_module_finite wittCode (marked o)

theorem neighbor_no_zero_smul_divisors {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    NoZeroSMulDivisors ℤ (NeighborModule C t) :=
  Function.Injective.noZeroSMulDivisors (integralCoordinateMap C t)
    (integralCoordinateMap_injective C t) (map_zero _)
    (fun k x => map_smul (integralCoordinateMap C t) k x)

theorem neighbor_module_free {n : ℕ}
    (C : AddSubgroup (Fin n → ZMod 3)) (t : Fin n → ℤ) :
    Module.Free ℤ (NeighborModule C t) := by
  letI := neighbor_module_finite C t
  letI := neighbor_no_zero_smul_divisors C t
  exact Module.free_of_finite_type_torsion_free'

theorem witt_marked_module_free (o : Fin 12) :
    Module.Free ℤ (neighborSubgroup wittCode (radial (marked o))) :=
  neighbor_module_free wittCode (marked o)

#print axioms coordinate_spec
#print axioms coordinateA_cast
#print axioms coordinateB_cast
#print axioms integralCoordinateMap
#print axioms integralCoordinateMap_injective
#print axioms neighbor_module_finite
#print axioms witt_marked_module_finite
#print axioms neighbor_no_zero_smul_divisors
#print axioms neighbor_module_free
#print axioms witt_marked_module_free

end HMT.IV.NeighborLattice
