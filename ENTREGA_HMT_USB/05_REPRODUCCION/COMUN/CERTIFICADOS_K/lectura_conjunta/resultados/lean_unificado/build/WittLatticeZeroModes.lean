import WittComplexAlgebra

/-!
The zero Heisenberg mode and the lattice shift on C_epsilon[Lambda].
The charge is read from the already proved integral lattice pairing.
The commutator is proved on all finite-support vectors, not postulated.
Source: the lattice vertex construction of Article I, `exc:voa`.
-/

noncomputable section
namespace HMT.IV.LatticeZeroModes

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra

def zeroMode (o : Fin 12) (x : Lattice o) :
    TwistedAlgebra o →ₗ[ℂ] TwistedAlgebra o :=
  Finsupp.linearCombination ℂ fun y =>
    (integerPair o x y : ℂ) • basisElement o y

def latticeShift (o : Fin 12) (y : Lattice o) :
    TwistedAlgebra o →ₗ[ℂ] TwistedAlgebra o :=
  LinearMap.mulLeft ℂ (basisElement o y)

@[simp] theorem zeroMode_basis (o : Fin 12) (x y : Lattice o) :
    zeroMode o x (basisElement o y) = (integerPair o x y : ℂ) • basisElement o y := by
  change (Finsupp.linearCombination ℂ fun y : Lattice o =>
    (integerPair o x y : ℂ) • basisElement o y) (Finsupp.single y 1) = _
  rw [Finsupp.linearCombination_single, one_smul]

@[simp] theorem latticeShift_basis (o : Fin 12) (x y : Lattice o) :
    latticeShift o x (basisElement o y) = epsilon o x y • basisElement o (x+y) :=
  twisted_basis_product o x y

theorem zeroMode_latticeShift_basis (o : Fin 12) (h x y : Lattice o) :
    zeroMode o h (latticeShift o x (basisElement o y)) -
      latticeShift o x (zeroMode o h (basisElement o y)) =
      (integerPair o h x : ℂ) • latticeShift o x (basisElement o y) := by
  simp only [latticeShift_basis, map_smul, zeroMode_basis,
    integerPair_add_right, Int.cast_add, smul_smul]
  rw [← sub_smul]
  congr 1
  ring

theorem zeroMode_latticeShift (o : Fin 12) (h x : Lattice o) :
    (zeroMode o h).comp (latticeShift o x) -
      (latticeShift o x).comp (zeroMode o h) =
      (integerPair o h x : ℂ) • latticeShift o x := by
  apply Finsupp.lhom_ext'
  intro y
  apply LinearMap.ext_ring
  exact zeroMode_latticeShift_basis o h x y

theorem zeroModes_commute (o : Fin 12) (h k : Lattice o) :
    (zeroMode o h).comp (zeroMode o k) = (zeroMode o k).comp (zeroMode o h) := by
  apply Finsupp.lhom_ext'
  intro y
  apply LinearMap.ext_ring
  change zeroMode o h (zeroMode o k (basisElement o y)) =
    zeroMode o k (zeroMode o h (basisElement o y))
  simp only [zeroMode_basis, map_smul, smul_smul]
  rw [mul_comm]

theorem latticeShifts_cocycle (o : Fin 12) (x y : Lattice o) :
    (latticeShift o x).comp (latticeShift o y) =
      epsilon o x y • latticeShift o (x+y) := by
  ext v
  change basisElement o x * (basisElement o y * v) =
    epsilon o x y • (basisElement o (x+y) * v)
  rw [← mul_assoc, twisted_basis_product, smul_mul_assoc]

theorem zeroMode_vacuum (o : Fin 12) (h : Lattice o) : zeroMode o h 1 = 0 := by
  change zeroMode o h (basisElement o 0) = 0
  simp [integerPair_zero_right]

end HMT.IV.LatticeZeroModes
end

#print axioms HMT.IV.LatticeZeroModes.zeroMode_latticeShift
#print axioms HMT.IV.LatticeZeroModes.zeroModes_commute
#print axioms HMT.IV.LatticeZeroModes.latticeShifts_cocycle
#print axioms HMT.IV.LatticeZeroModes.zeroMode_vacuum
