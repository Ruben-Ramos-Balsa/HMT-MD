import LatticeFockMonomialParity
import Mathlib.Algebra.Module.ZLattice.Basic

/-!
The existing order-three isometry of the marked neighbour is lifted in its
own integral basis, first to every oscillator frequency and then to the
actual symmetric Fock algebra. No independently chosen 24 by 24 matrix is
used. Its ambient orientation is wittOrientation (one C, eleven C-inverse).
The six-plus-six presentation of APPFockIndex needs a separate conjugating
chart; no literal equality with that presentation or trace is claimed here.
-/

noncomputable section
namespace HMT.IV.LatticeCoxeterFock

open HMT.IV.LatticeCocycle HMT.IV.CoxeterNeighbor
open HMT.IV.LatticeOscillatorFock HMT.IV.LatticeFockMonomialParity
open HMT.FockTransport.Symmetric
open scoped BigOperators

def latticeAction (o : Fin 12) : Lattice o →ₗ[ℤ] Lattice o :=
  AddMonoidHom.toIntLinearMap {
    toFun := fun x => ⟨action wittOrientation (x : Space 12),
      (witt_neighbor_invariant o (x : Space 12)).mpr x.property⟩
    map_zero' := by
      apply Subtype.ext
      exact (action_fixed_iff wittOrientation 0).mpr rfl
    map_add' := by
      intro x y
      apply Subtype.ext
      exact action_add wittOrientation (x : Space 12) (y : Space 12) }

theorem latticeAction_cube (o : Fin 12) (x : Lattice o) :
    latticeAction o (latticeAction o (latticeAction o x)) = x := by
  apply Subtype.ext
  exact action_cube wittOrientation (x : Space 12)

theorem latticeAction_pairing (o : Fin 12) (x y : Lattice o) :
    integerPair o (latticeAction o x) (latticeAction o y) = integerPair o x y := by
  apply Int.cast_injective (α := ℚ)
  rw [cast_integerPair, cast_integerPair]
  exact action_pairing wittOrientation (x : Space 12) (y : Space 12)

/-- Complex oscillator vector obtained from an actual lattice vector at
frequency n+1, in the already chosen integral basis. -/
def modeLift (o : Fin 12) (n : ℕ) : Lattice o →ₗ[ℤ] Oscillators o :=
  AddMonoidHom.toIntLinearMap {
    toFun := fun x => ∑ j : Fin (BasisSize o),
      ((latticeBasis o).repr x j : ℂ) • modeVector o n j
    map_zero' := by simp
    map_add' := by
      intro x y
      simp only [map_add, Finsupp.add_apply, Int.cast_add, add_smul,
        Finset.sum_add_distrib] }

@[simp] theorem modeLift_basis (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    modeLift o n (latticeBasis o i) = modeVector o n i := by
  change (∑ j : Fin (BasisSize o),
    ((latticeBasis o).repr (latticeBasis o i) j : ℂ) • modeVector o n j) = _
  simp [Finsupp.single_apply]

theorem modeLift_apply (o : Fin 12) (n : ℕ) (x : Lattice o)
    (i : Fin (BasisSize o)) :
    modeLift o n x (n,i) = ((latticeBasis o).repr x i : ℂ) := by
  simp [modeLift, modeVector, Finsupp.single_apply]

theorem modeLift_injective (o : Fin 12) (n : ℕ) :
    Function.Injective (modeLift o n) := by
  intro x y h
  apply (latticeBasis o).repr.injective
  ext i
  apply Int.cast_injective (α := ℂ)
  have hi := congrArg (fun v : Oscillators o => v (n,i)) h
  simpa only [modeLift_apply] using hi

def oscillatorAction (o : Fin 12) : Oscillators o →ₗ[ℂ] Oscillators o :=
  (oscillatorBasis o).constr ℂ (fun p =>
    modeLift o p.1 (latticeAction o (latticeBasis o p.2)))

@[simp] theorem oscillatorAction_basis (o : Fin 12) (p : Mode o) :
    oscillatorAction o (oscillatorBasis o p) =
      modeLift o p.1 (latticeAction o (latticeBasis o p.2)) :=
  Basis.constr_basis _ _ _ _

theorem oscillatorAction_intertwines (o : Fin 12) (n : ℕ) :
    ((oscillatorAction o).restrictScalars ℤ).comp (modeLift o n) =
      (modeLift o n).comp (latticeAction o) := by
  apply (latticeBasis o).ext
  intro i
  simp only [LinearMap.comp_apply, LinearMap.restrictScalars_apply, modeLift_basis]
  exact oscillatorAction_basis o (n,i)

theorem oscillatorAction_modeLift (o : Fin 12) (n : ℕ) (x : Lattice o) :
    oscillatorAction o (modeLift o n x) = modeLift o n (latticeAction o x) :=
  LinearMap.congr_fun (oscillatorAction_intertwines o n) x

theorem oscillatorAction_cube (o : Fin 12) (v : Oscillators o) :
    oscillatorAction o (oscillatorAction o (oscillatorAction o v)) = v := by
  have he : (oscillatorAction o).comp ((oscillatorAction o).comp (oscillatorAction o)) =
      (LinearMap.id : Oscillators o →ₗ[ℂ] Oscillators o) := by
    apply (oscillatorBasis o).ext
    intro p
    simp only [LinearMap.comp_apply, LinearMap.id_apply, oscillatorAction_basis,
      oscillatorAction_modeLift, latticeAction_cube, modeLift_basis]
    rfl
  exact LinearMap.congr_fun he v

def oscillatorEquiv (o : Fin 12) : Oscillators o ≃ₗ[ℂ] Oscillators o where
  toLinearMap := oscillatorAction o
  invFun := fun v => oscillatorAction o (oscillatorAction o v)
  left_inv := oscillatorAction_cube o
  right_inv := oscillatorAction_cube o

def fockAction (o : Fin 12) : Fock o →ₐ[ℂ] Fock o := gamma (oscillatorAction o)

@[simp] theorem fockAction_generator (o : Fin 12) (v : Oscillators o) :
    fockAction o (SymmetricAlgebra.ι ℂ (Oscillators o) v) =
      SymmetricAlgebra.ι ℂ (Oscillators o) (oscillatorAction o v) :=
  gamma_generator _ _

theorem fockAction_cube (o : Fin 12) (v : Fock o) :
    fockAction o (fockAction o (fockAction o v)) = v := by
  have he : (fockAction o).comp ((fockAction o).comp (fockAction o)) =
      AlgHom.id ℂ (Fock o) := by
    apply SymmetricAlgebra.algHom_ext
    apply LinearMap.ext
    intro x
    change fockAction o (fockAction o (fockAction o
      (SymmetricAlgebra.ι ℂ (Oscillators o) x))) = SymmetricAlgebra.ι ℂ (Oscillators o) x
    rw [fockAction_generator, fockAction_generator, fockAction_generator,
      oscillatorAction_cube]
  exact AlgHom.congr_fun he v

def fockEquiv (o : Fin 12) : Fock o ≃ₐ[ℂ] Fock o :=
  AlgEquiv.ofAlgHom (fockAction o) ((fockAction o).comp (fockAction o))
    (by apply AlgHom.ext; intro v; exact fockAction_cube o v)
    (by apply AlgHom.ext; intro v; exact fockAction_cube o v)

theorem generator_injective (o : Fin 12) :
    Function.Injective (SymmetricAlgebra.ι ℂ (Oscillators o)) := by
  intro x y h
  ext p
  have hc := congrArg (annihilation (Finsupp.lapply p :
    Oscillators o →ₗ[ℂ] ℂ)) h
  simp only [annihilation_generator, Finsupp.lapply_apply] at hc
  exact (SymmetricAlgebra.algebraMap_leftInverse (Oscillators o)).injective hc

theorem fockEquiv_ne_one (o : Fin 12) : fockEquiv o ≠ 1 := by
  intro h
  let x : Lattice o := ⟨rootDifference o,
    rootDifference o, rootDifference_mem_kernel wittCode o, 0, by simp⟩
  have he := congrArg (fun e : Fock o ≃ₐ[ℂ] Fock o =>
    e (SymmetricAlgebra.ι ℂ (Oscillators o) (modeLift o 0 x))) h
  change fockAction o (SymmetricAlgebra.ι ℂ (Oscillators o) (modeLift o 0 x)) =
    SymmetricAlgebra.ι ℂ (Oscillators o) (modeLift o 0 x) at he
  rw [fockAction_generator, oscillatorAction_modeLift] at he
  have hx := modeLift_injective o 0 (generator_injective o he)
  have hval := congrArg (fun z : Lattice o => (z : Space 12)) hx
  change action wittOrientation (rootDifference o) = rootDifference o at hval
  exact rootDifference_ne_zero o ((action_fixed_iff _ _).mp hval)

theorem fockEquiv_order (o : Fin 12) : orderOf (fockEquiv o) = 3 := by
  apply orderOf_eq_prime
  · apply AlgEquiv.ext
    intro v
    exact fockAction_cube o v
  · exact fockEquiv_ne_one o

@[simp] theorem fockAction_vacuum (o : Fin 12) : fockAction o 1 = 1 := map_one _

theorem fockAction_creation (o : Fin 12) (n : ℕ)
    (i : Fin (BasisSize o)) (v : Fock o) :
    fockAction o (create o n i v) =
      creation (modeLift o n (latticeAction o (latticeBasis o i)))
        (fockAction o v) := by
  have h := creation_naturality (oscillatorAction o) (modeVector o n i) v
  change fockAction o (create o n i v) =
    creation (oscillatorAction o (modeVector o n i)) (fockAction o v) at h
  rw [show oscillatorAction o (modeVector o n i) =
    modeLift o n (latticeAction o (latticeBasis o i)) from oscillatorAction_basis o (n,i)] at h
  exact h

end HMT.IV.LatticeCoxeterFock
end

#print axioms HMT.IV.LatticeCoxeterFock.latticeAction_cube
#print axioms HMT.IV.LatticeCoxeterFock.latticeAction_pairing
#print axioms HMT.IV.LatticeCoxeterFock.modeLift_basis
#print axioms HMT.IV.LatticeCoxeterFock.modeLift_injective
#print axioms HMT.IV.LatticeCoxeterFock.oscillatorAction_intertwines
#print axioms HMT.IV.LatticeCoxeterFock.oscillatorAction_cube
#print axioms HMT.IV.LatticeCoxeterFock.oscillatorEquiv
#print axioms HMT.IV.LatticeCoxeterFock.fockAction_cube
#print axioms HMT.IV.LatticeCoxeterFock.fockEquiv
#print axioms HMT.IV.LatticeCoxeterFock.fockEquiv_order
#print axioms HMT.IV.LatticeCoxeterFock.fockAction_vacuum
#print axioms HMT.IV.LatticeCoxeterFock.fockAction_creation
