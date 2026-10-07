import WittComplexAlgebra
import SymmetricTransport
import WittLatticeZeroModes
import Mathlib.LinearAlgebra.TensorProduct.Basic

/-!
# Oscillators and the algebraic carrier of the selected lattice VOA

Source: Article I, `sections/excepcional.tex`, subsection `exc:voa`.
The lattice, its integral form, and the sign cocycle are imported from the
marked-neighbor construction. No lattice Gram matrix is supplied as a new
input. An integral basis is chosen only to present its complex oscillator
space; mode n means the positive frequency n+1.

The mode set is unbounded and every vector has finite support. The symmetric
algebra therefore contains every finite particle degree. The CCR below hold
on that entire algebra, and on its tensor product with the twisted group
algebra. This is the algebraic carrier M(1) tensor C_epsilon[Lambda], not yet
a claim about vertex-operator locality, the twisted module, or the FLM theorem.
-/

noncomputable section
namespace HMT.IV.LatticeOscillatorFock

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra
open HMT.FockTransport.Symmetric
open scoped TensorProduct

abbrev Mode (o : Fin 12) := ℕ × Fin (BasisSize o)
abbrev Oscillators (o : Fin 12) := Mode o →₀ ℂ
abbrev Fock (o : Fin 12) := SymmetricAlgebra ℂ (Oscillators o)
abbrev LatticeCarrier (o : Fin 12) := Fock o ⊗[ℂ] TwistedAlgebra o

/-- The complex Gram coefficient is read from the integral pairing proved
for the marked neighbor; it is not an independent matrix parameter. -/
def gram (o : Fin 12) (i j : Fin (BasisSize o)) : ℂ :=
  integerPair o (latticeBasis o i) (latticeBasis o j)

theorem gram_symmetric (o : Fin 12) (i j : Fin (BasisSize o)) :
    gram o i j = gram o j i := by
  simp only [gram, integerPair_comm]

def modeVector (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) : Oscillators o :=
  Finsupp.single (n, i) 1

def modeCovector (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    Module.Dual ℂ (Oscillators o) :=
  Finsupp.linearCombination ℂ fun p =>
    if n = p.1 then (n + 1 : ℂ) * gram o i p.2 else 0

@[simp] theorem modeCovector_modeVector (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) :
    modeCovector o n i (modeVector o m j) =
      if n = m then (n + 1 : ℂ) * gram o i j else 0 := by
  simp [modeCovector, modeVector]

def create (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    Fock o →ₗ[ℂ] Fock o := creation (modeVector o n i)

def annihilate (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    Fock o →ₗ[ℂ] Fock o := (annihilation (modeCovector o n i)).toLinearMap

theorem mode_ccr (o : Fin 12) (n m : ℕ) (i j : Fin (BasisSize o)) :
    (annihilate o n i).comp (create o m j) -
      (create o m j).comp (annihilate o n i) =
      (if n = m then (n + 1 : ℂ) * gram o i j else 0) •
        (LinearMap.id : Fock o →ₗ[ℂ] Fock o) := by
  simpa only [annihilate, create, modeCovector_modeVector] using
    ccr_linear (modeCovector o n i) (modeVector o m j)

theorem annihilate_vacuum (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    annihilate o n i 1 = 0 := annihilation_vacuum _

theorem creations_commute_all_modes (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : Fock o) :
    create o n i (create o m j v) = create o m j (create o n i v) :=
  creations_commute _ _ _

theorem annihilations_commute_all_modes (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : Fock o) :
    annihilate o n i (annihilate o m j v) =
      annihilate o m j (annihilate o n i v) :=
  annihilations_commute _ _ _

/-- All oscillator operators act on the same lattice carrier. -/
def onCarrier (o : Fin 12) (T : Fock o →ₗ[ℂ] Fock o) :
    LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
  TensorProduct.map T LinearMap.id

@[simp] theorem onCarrier_pure (o : Fin 12) (T : Fock o →ₗ[ℂ] Fock o)
    (v : Fock o) (a : TwistedAlgebra o) :
    onCarrier o T (v ⊗ₜ[ℂ] a) = T v ⊗ₜ[ℂ] a := by
  simp [onCarrier]

theorem carrier_mode_ccr (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : LatticeCarrier o) :
    onCarrier o (annihilate o n i) (onCarrier o (create o m j) v) -
      onCarrier o (create o m j) (onCarrier o (annihilate o n i) v) =
      (if n = m then (n + 1 : ℂ) * gram o i j else 0) • v := by
  have h := mode_ccr o n m i j
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [onCarrier_pure]
    rw [← TensorProduct.sub_tmul]
    have hv := LinearMap.congr_fun h v
    simp only [LinearMap.sub_apply, LinearMap.comp_apply,
      LinearMap.smul_apply, LinearMap.id_apply] at hv
    rw [hv, TensorProduct.smul_tmul']
  | add x y hx hy => simp only [map_add, smul_add]; rw [← hx, ← hy]; abel

def vacuum (o : Fin 12) : LatticeCarrier o := (1 : Fock o) ⊗ₜ[ℂ] 1

/-- The coefficient of the empty oscillator monomial and zero lattice
vector. This is a linear functional, not a character of the twisted algebra. -/
def vacuumCoefficient (o : Fin 12) : LatticeCarrier o →ₗ[ℂ] ℂ :=
  (TensorProduct.lid ℂ ℂ).toLinearMap.comp
    (TensorProduct.map
      (SymmetricAlgebra.lift (0 : Oscillators o →ₗ[ℂ] ℂ)).toLinearMap
      (Finsupp.lapply (0 : Lattice o)))

theorem vacuumCoefficient_vacuum (o : Fin 12) :
    vacuumCoefficient o (vacuum o) = 1 := by
  change (TensorProduct.lid ℂ ℂ)
    (TensorProduct.map (SymmetricAlgebra.lift (0 : Oscillators o →ₗ[ℂ] ℂ)).toLinearMap
      (Finsupp.lapply (0 : Lattice o))
      ((1 : Fock o) ⊗ₜ[ℂ] (Finsupp.single 0 1 : Lattice o →₀ ℂ))) = 1
  simp

theorem vacuum_ne_zero (o : Fin 12) : vacuum o ≠ 0 := by
  intro h
  have hc := vacuumCoefficient_vacuum o
  rw [h, map_zero] at hc
  exact zero_ne_one hc

theorem carrier_vacuum_annihilated (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) :
    onCarrier o (annihilate o n i) (vacuum o) = 0 := by
  simp [vacuum, annihilate_vacuum]

/-- Lattice operators act on the second factor, leaving the oscillator
history unchanged. -/
def onLattice (o : Fin 12) (T : TwistedAlgebra o →ₗ[ℂ] TwistedAlgebra o) :
    LatticeCarrier o →ₗ[ℂ] LatticeCarrier o :=
  TensorProduct.map LinearMap.id T

@[simp] theorem onLattice_pure (o : Fin 12)
    (T : TwistedAlgebra o →ₗ[ℂ] TwistedAlgebra o)
    (v : Fock o) (a : TwistedAlgebra o) :
    onLattice o T (v ⊗ₜ[ℂ] a) = v ⊗ₜ[ℂ] T a := by
  simp [onLattice]

theorem oscillator_lattice_commute (o : Fin 12)
    (S : Fock o →ₗ[ℂ] Fock o)
    (T : TwistedAlgebra o →ₗ[ℂ] TwistedAlgebra o) (v : LatticeCarrier o) :
    onCarrier o S (onLattice o T v) = onLattice o T (onCarrier o S v) := by
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a => simp
  | add x y hx hy => simp [map_add, hx, hy]

theorem carrier_charge_shift (o : Fin 12) (h x : Lattice o) (v : LatticeCarrier o) :
    onLattice o (LatticeZeroModes.zeroMode o h)
        (onLattice o (LatticeZeroModes.latticeShift o x) v) -
      onLattice o (LatticeZeroModes.latticeShift o x)
        (onLattice o (LatticeZeroModes.zeroMode o h) v) =
      (integerPair o h x : ℂ) • onLattice o (LatticeZeroModes.latticeShift o x) v := by
  have hcomm := LatticeZeroModes.zeroMode_latticeShift o h x
  induction v using TensorProduct.induction_on with
  | zero => simp
  | tmul v a =>
    simp only [onLattice_pure]
    rw [← TensorProduct.tmul_sub]
    have ha := LinearMap.congr_fun hcomm a
    simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply] at ha
    rw [ha, TensorProduct.tmul_smul]
  | add x y hx hy => simp only [map_add, smul_add]; rw [← hx, ← hy]; abel

end HMT.IV.LatticeOscillatorFock

#print axioms HMT.IV.LatticeOscillatorFock.mode_ccr
#print axioms HMT.IV.LatticeOscillatorFock.carrier_mode_ccr
#print axioms HMT.IV.LatticeOscillatorFock.carrier_vacuum_annihilated
#print axioms HMT.IV.LatticeOscillatorFock.vacuum_ne_zero
#print axioms HMT.IV.LatticeOscillatorFock.oscillator_lattice_commute
#print axioms HMT.IV.LatticeOscillatorFock.carrier_charge_shift

end
