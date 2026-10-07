import WittPairingParity
import Mathlib.Data.Int.Interval
import Mathlib.Tactic

/-!
Finite norm shells of the constructed marked lattice. The existing
denominator-three integral coordinate map supplies the embedding. Bounds
come from its positive definite A2 pairing; finiteness is not postulated.
-/

noncomputable section
namespace HMT.IV.LatticeWeightShells

open HMT.IV.LatticeCocycle HMT.IV.CoxeterNeighbor HMT.IV.NeighborLattice
open scoped BigOperators

theorem integerPair_self_nonneg (o : Fin 12) (x : Lattice o) :
    0 ≤ integerPair o x x := by
  have h := pairing_self_nonneg (x : Space 12)
  rw [← cast_integerPair] at h
  exact_mod_cast h

theorem integerPair_self_eq_zero_iff (o : Fin 12) (x : Lattice o) :
    integerPair o x x = 0 ↔ x = 0 := by
  constructor
  · intro h
    have hq : pairing (x : Space 12) (x : Space 12) = 0 := by
      rw [← cast_integerPair, h, Int.cast_zero]
    apply Subtype.ext
    exact (pairing_self_eq_zero_iff _).mp hq
  · rintro rfl
    exact integerPair_zero_left o 0

theorem integerPair_neg_left (o : Fin 12) (x y : Lattice o) :
    integerPair o (-x) y = -integerPair o x y := by
  have h := integerPair_add_left o x (-x) y
  rw [add_neg_cancel, integerPair_zero_left] at h
  omega

theorem integerPair_neg_neg (o : Fin 12) (x y : Lattice o) :
    integerPair o (-x) (-y) = integerPair o x y := by
  rw [integerPair_neg_left, integerPair_comm o x, integerPair_neg_left,
    neg_neg, integerPair_comm o y]

def halfnormNat (o : Fin 12) (x : Lattice o) : ℕ :=
  (integerPair o x x / 2).toNat

theorem integerPair_eq_two_halfnorm (o : Fin 12) (x : Lattice o) :
    integerPair o x x = 2 * (halfnormNat o x : ℤ) := by
  obtain ⟨k, hk⟩ := integerPair_even o x
  have hn := integerPair_self_nonneg o x
  have hk0 : 0 ≤ k := by omega
  simp [halfnormNat, hk, Int.toNat_of_nonneg hk0]

@[simp] theorem halfnormNat_neg (o : Fin 12) (x : Lattice o) :
    halfnormNat o (-x) = halfnormNat o x := by
  simp only [halfnormNat, integerPair_neg_neg]

@[simp] theorem halfnormNat_zero (o : Fin 12) : halfnormNat o 0 = 0 := by
  simp [halfnormNat, integerPair_zero_left]

theorem halfnormNat_eq_zero_iff (o : Fin 12) (x : Lattice o) :
    halfnormNat o x = 0 ↔ x = 0 := by
  constructor
  · intro h
    apply (integerPair_self_eq_zero_iff o x).mp
    rw [integerPair_eq_two_halfnorm, h]
    norm_num
  · rintro rfl
    exact halfnormNat_zero o

theorem localPair_self_nonneg (v : ℚ × ℚ) : 0 ≤ localPair v v := by
  dsimp [localPair]
  nlinarith [sq_nonneg v.1, sq_nonneg v.2, sq_nonneg (v.1-v.2)]

theorem localPair_le_pairing (x : Space 12) (i : Fin 12) :
    localPair (x i) (x i) ≤ pairing x x := by
  unfold pairing
  exact Finset.single_le_sum (f := fun j => localPair (x j) (x j))
    (fun j _ => localPair_self_nonneg (x j)) (Finset.mem_univ i)

theorem coordinateA_sq_le (o : Fin 12) (x : Lattice o) (i : Fin 12) :
    (coordinateA wittCode (marked o) x i)^2 ≤ 9 * integerPair o x x := by
  have hp := localPair_le_pairing (x : Space 12) i
  have ha := coordinateA_cast wittCode (marked o) x i
  have hs1 := sq_nonneg (((x : Space 12) i).1-((x : Space 12) i).2)
  have hs2 := sq_nonneg (((x : Space 12) i).2)
  rw [← cast_integerPair] at hp
  dsimp [localPair] at hp
  have hq : (coordinateA wittCode (marked o) x i : ℚ)^2 ≤
      9 * (integerPair o x x : ℚ) := by rw [ha]; nlinarith
  exact_mod_cast hq

theorem coordinateB_sq_le (o : Fin 12) (x : Lattice o) (i : Fin 12) :
    (coordinateB wittCode (marked o) x i)^2 ≤ 9 * integerPair o x x := by
  have hp := localPair_le_pairing (x : Space 12) i
  have hb := coordinateB_cast wittCode (marked o) x i
  have hs1 := sq_nonneg (((x : Space 12) i).1-((x : Space 12) i).2)
  have hs2 := sq_nonneg (((x : Space 12) i).1)
  rw [← cast_integerPair] at hp
  dsimp [localPair] at hp
  have hq : (coordinateB wittCode (marked o) x i : ℚ)^2 ≤
      9 * (integerPair o x x : ℚ) := by rw [hb]; nlinarith
  exact_mod_cast hq

def coordinateBound (d : ℕ) : ℤ := 18 * (d : ℤ) + 1

theorem coordinate_bounds (o : Fin 12) (d : ℕ) (x : Lattice o)
    (hx : integerPair o x x ≤ 2 * (d : ℤ)) (i : Fin 12) :
    coordinateA wittCode (marked o) x i ∈
        Set.Icc (-coordinateBound d) (coordinateBound d) ∧
    coordinateB wittCode (marked o) x i ∈
        Set.Icc (-coordinateBound d) (coordinateBound d) := by
  have ha := coordinateA_sq_le o x i
  have hb := coordinateB_sq_le o x i
  have hd : (0 : ℤ) ≤ d := Int.natCast_nonneg d
  dsimp [Set.mem_Icc, coordinateBound]
  constructor <;> constructor
  · nlinarith [sq_nonneg (coordinateA wittCode (marked o) x i + 1)]
  · nlinarith [sq_nonneg (coordinateA wittCode (marked o) x i - 1)]
  · nlinarith [sq_nonneg (coordinateB wittCode (marked o) x i + 1)]
  · nlinarith [sq_nonneg (coordinateB wittCode (marked o) x i - 1)]

abbrev NormBall (o : Fin 12) (d : ℕ) :=
  {x : Lattice o // integerPair o x x ≤ 2 * (d : ℤ)}

abbrev NormShell (o : Fin 12) (d : ℕ) :=
  {x : Lattice o // integerPair o x x = 2 * (d : ℤ)}

abbrev EnergyShell (o : Fin 12) (d : ℕ) :=
  {x : Lattice o // halfnormNat o x = d}

abbrev BoundedCoordinate (d : ℕ) :=
  {z : ℤ // z ∈ Set.Icc (-coordinateBound d) (coordinateBound d)}

def boundedEncoding (o : Fin 12) (d : ℕ) (x : NormBall o d) :
    Fin 12 → BoundedCoordinate d × BoundedCoordinate d :=
  fun i => (⟨coordinateA wittCode (marked o) x.val i,
               (coordinate_bounds o d x.val x.property i).1⟩,
            ⟨coordinateB wittCode (marked o) x.val i,
               (coordinate_bounds o d x.val x.property i).2⟩)

theorem boundedEncoding_injective (o : Fin 12) (d : ℕ) :
    Function.Injective (boundedEncoding o d) := by
  intro x y h
  apply Subtype.ext
  apply integralCoordinateMap_injective wittCode (marked o)
  funext i
  apply Prod.ext
  · exact congrArg (fun f => ((f i).1 : ℤ)) h
  · exact congrArg (fun f => ((f i).2 : ℤ)) h

noncomputable instance normBallFintype (o : Fin 12) (d : ℕ) :
    Fintype (NormBall o d) :=
  Fintype.ofInjective (boundedEncoding o d) (boundedEncoding_injective o d)

def normShellToBall (o : Fin 12) (d : ℕ) (x : NormShell o d) : NormBall o d :=
  ⟨x.val, x.property.le⟩

noncomputable instance normShellFintype (o : Fin 12) (d : ℕ) :
    Fintype (NormShell o d) :=
  Fintype.ofInjective (normShellToBall o d) (by
    intro x y h
    apply Subtype.ext
    exact congrArg (fun z : NormBall o d => z.val) h)

def energyShellEquivNormShell (o : Fin 12) (d : ℕ) :
    EnergyShell o d ≃ NormShell o d where
  toFun x := ⟨x.val, by rw [integerPair_eq_two_halfnorm, x.property]⟩
  invFun x := ⟨x.val, by
    have h := integerPair_eq_two_halfnorm o x.val
    rw [x.property] at h
    omega⟩
  left_inv _ := rfl
  right_inv _ := rfl

noncomputable instance energyShellFintype (o : Fin 12) (d : ℕ) :
    Fintype (EnergyShell o d) :=
  Fintype.ofEquiv (NormShell o d) (energyShellEquivNormShell o d).symm

def normShellNeg (o : Fin 12) (d : ℕ) : NormShell o d ≃ NormShell o d where
  toFun x := ⟨-x.val, by rw [integerPair_neg_neg]; exact x.property⟩
  invFun x := ⟨-x.val, by rw [integerPair_neg_neg]; exact x.property⟩
  left_inv x := by apply Subtype.ext; exact neg_neg x.val
  right_inv x := by apply Subtype.ext; exact neg_neg x.val

theorem normShell_zero (o : Fin 12) (x : NormShell o 0) : x.val = 0 := by
  apply (integerPair_self_eq_zero_iff o x.val).mp
  simpa using x.property

theorem energyShell_zero (o : Fin 12) (x : EnergyShell o 0) : x.val = 0 :=
  (halfnormNat_eq_zero_iff o x.val).mp x.property

end HMT.IV.LatticeWeightShells
end

#print axioms HMT.IV.LatticeWeightShells.integerPair_self_nonneg
#print axioms HMT.IV.LatticeWeightShells.integerPair_self_eq_zero_iff
#print axioms HMT.IV.LatticeWeightShells.integerPair_neg_neg
#print axioms HMT.IV.LatticeWeightShells.integerPair_eq_two_halfnorm
#print axioms HMT.IV.LatticeWeightShells.halfnormNat_eq_zero_iff
#print axioms HMT.IV.LatticeWeightShells.coordinate_bounds
#print axioms HMT.IV.LatticeWeightShells.boundedEncoding_injective
#print axioms HMT.IV.LatticeWeightShells.normBallFintype
#print axioms HMT.IV.LatticeWeightShells.normShellFintype
#print axioms HMT.IV.LatticeWeightShells.energyShellEquivNormShell
#print axioms HMT.IV.LatticeWeightShells.energyShellFintype
#print axioms HMT.IV.LatticeWeightShells.normShellNeg
#print axioms HMT.IV.LatticeWeightShells.normShell_zero
