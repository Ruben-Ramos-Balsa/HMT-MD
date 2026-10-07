import LatticeConformalHeisenberg
import Mathlib.Tactic.NoncommRing

/-! Centralizers of the actual oscillator action and the quadratic-mode
commutator defect. This uses only the associative algebra of endomorphisms,
not a Jacobi or Virasoro axiom for a vertex algebra. -/
noncomputable section
namespace HMT.IV.LatticeConformalCentralizer
open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeHeisenbergField LatticeNormalOrderedField LatticeConformalState
open LatticeConformalCoefficient LatticeConformalHeisenberg

def comm {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B : Module.End ℂ V) : Module.End ℂ V := A*B-B*A

theorem comm_smul_left {V : Type*} [AddCommGroup V] [Module ℂ V]
    (c : ℂ) (A B : Module.End ℂ V) : comm (c•A) B = c•comm A B := by
  simp only [comm, smul_mul_assoc, mul_smul_comm, smul_sub]

theorem comm_smul_right {V : Type*} [AddCommGroup V] [Module ℂ V]
    (c : ℂ) (A B : Module.End ℂ V) : comm A (c•B) = c•comm A B := by
  simp only [comm, smul_mul_assoc, mul_smul_comm, smul_sub]

theorem comm_sub_left {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B C : Module.End ℂ V) : comm (A-B) C=comm A C-comm B C := by
  simp only [comm]
  noncomm_ring

theorem comm_jacobi_associative {V : Type*} [AddCommGroup V] [Module ℂ V]
    (A B C : Module.End ℂ V) :
    comm (comm A B) C=comm A (comm B C)-comm B (comm A C) := by
  simp only [comm]
  noncomm_ring

theorem conformal_comm_heisenberg (o : Fin 12) (i : Fin (BasisSize o)) (m n : ℤ) :
    comm (conformalMode o m) (hmode o i n) =
      ((-n:ℤ):ℂ) • hmode o i (m+n) :=
  conformalMode_heisenberg_commutator o i m n

def defect (o : Fin 12) (m n : ℤ) : Module.End ℂ (LatticeCarrier o) :=
  comm (conformalMode o m) (conformalMode o n) -
    ((m-n:ℤ):ℂ) • conformalMode o (m+n)

theorem defect_comm_heisenberg (o : Fin 12) (i : Fin (BasisSize o)) (m n k : ℤ) :
    comm (defect o m n) (hmode o i k)=0 := by
  rw [defect, comm_sub_left, comm_jacobi_associative, comm_smul_left]
  simp only [conformal_comm_heisenberg, comm_smul_right]
  rw [show n+(m+k)=m+(n+k) by omega, show m+n+k=m+(n+k) by omega]
  push_cast
  module

theorem heisenberg_centralizer_normal (o : Fin 12) (T : Module.End ℂ (LatticeCarrier o))
    (hT : ∀ i n, T*(hmode o i n)=(hmode o i n)*T)
    (i j : Fin (BasisSize o)) (m : ℤ) (v : LatticeCarrier o) :
    T (normalCoefficient o i 0 (heisenbergField o j) (-m-2) v) =
      normalCoefficient o i 0 (heisenbergField o j) (-m-2) (T v) := by
  have ht (i : Fin (BasisSize o)) (n : ℤ) (v : LatticeCarrier o) :
      T (hmode o i n v)=hmode o i n (T v) := LinearMap.congr_fun (hT i n) v
  have hc (a : ℕ) : T (creationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
      creationTerm o i 0 (heisenbergField o j) (-m-2) a (T v) := by
    rw [creationTerm_heisenberg]
    simp only [LinearMap.comp_apply, ht]
  have ha (a : ℕ) : T (annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
      annihilationTerm o i 0 (heisenbergField o j) (-m-2) a (T v) := by
    rw [annihilationTerm_heisenberg]
    simp only [LinearMap.comp_apply, ht]
  rw [normalCoefficient_apply, map_add, normalCoefficient_apply]
  have hsC : T (∑ᶠ a, creationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
      ∑ᶠ a, T (creationTerm o i 0 (heisenbergField o j) (-m-2) a v) :=
    T.toAddMonoidHom.map_finsum (creationTerm_finite o i 0 (heisenbergField o j) (-m-2) v)
  have hsA : T (∑ᶠ a, annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
      ∑ᶠ a, T (annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v) :=
    T.toAddMonoidHom.map_finsum (annihilationTerm_finite o i 0 (heisenbergField o j) (-m-2) v)
  rw [hsC, hsA]
  simp only [hc, ha]

theorem heisenberg_centralizer_conformal (o : Fin 12)
    (T : Module.End ℂ (LatticeCarrier o))
    (hT : ∀ i n, T*(hmode o i n)=(hmode o i n)*T) (m : ℤ) :
    T*conformalMode o m=conformalMode o m*T := by
  apply LinearMap.ext
  intro v
  change T (conformalMode o m v) = conformalMode o m (T v)
  rw [conformalMode_normal_sum_apply, conformalMode_normal_sum_apply]
  simp only [map_smul, map_sum, heisenberg_centralizer_normal o T hT]

theorem defect_comm_conformal (o : Fin 12) (m n k : ℤ) :
    comm (defect o m n) (conformalMode o k)=0 := by
  apply sub_eq_zero.mpr
  exact heisenberg_centralizer_conformal o (defect o m n)
    (fun i a => sub_eq_zero.mp (defect_comm_heisenberg o i m n a)) k

end HMT.IV.LatticeConformalCentralizer
end
#print axioms HMT.IV.LatticeConformalCentralizer.comm_jacobi_associative
#print axioms HMT.IV.LatticeConformalCentralizer.defect_comm_heisenberg
#print axioms HMT.IV.LatticeConformalCentralizer.heisenberg_centralizer_normal
#print axioms HMT.IV.LatticeConformalCentralizer.heisenberg_centralizer_conformal
#print axioms HMT.IV.LatticeConformalCentralizer.defect_comm_conformal
