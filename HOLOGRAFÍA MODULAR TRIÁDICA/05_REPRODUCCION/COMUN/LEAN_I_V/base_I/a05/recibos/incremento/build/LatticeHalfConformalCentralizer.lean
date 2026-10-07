import LatticeHalfConformalHeisenberg
import LatticeHalfConformalVacuum
import LatticeConformalCentralizer

/-!
Centralization of the quadratic half-integer commutator defect. The scalar
shift is the rank/16 value already forced by the vacuum calculation. The
Heisenberg commutators, associative Jacobi identity and locally finite normal
sums suffice; no Virasoro relation or scalar value of the defect is assumed.
-/

noncomputable section
namespace HMT.IV.LatticeHalfConformalCentralizer

open LatticeCocycle LatticeOscillatorFock LatticeHalfIntegerHeisenberg
open LatticeHalfConformalModes LatticeHalfConformalVacuum
open LatticeHalfConformalHeisenberg LatticeConformalCentralizer
open scoped BigOperators

def shiftedModes (o : Fin 12) (m : ℤ) : Module.End ℂ (HalfFock o) :=
  shiftedQuadraticMode o ((BasisSize o : ℂ)/16) m

theorem shifted_comm_half (o : Fin 12) (i : Fin (BasisSize o)) (m n : ℤ) :
    comm (shiftedModes o m) (halfMode o i n) =
      (-(n:ℂ)-1/2) • halfMode o i (m+n) := by
  apply LinearMap.ext
  intro v
  have h := quadraticMode_half_commutator_apply o i m n v
  change shiftedModes o m (halfMode o i n v) -
      halfMode o i n (shiftedModes o m v) = _
  by_cases hm : m=0
  · simp only [shiftedModes, shiftedQuadraticMode, if_pos hm,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply,
      map_add, map_smul]
    calc
      _ = quadraticMode o m (halfMode o i n v) -
          halfMode o i n (quadraticMode o m v) := by abel
      _ = _ := h
  · simpa only [shiftedModes, shiftedQuadraticMode, if_neg hm, add_zero,
      LinearMap.smul_apply] using h

def defect (o : Fin 12) (m n : ℤ) : Module.End ℂ (HalfFock o) :=
  comm (shiftedModes o m) (shiftedModes o n) -
    ((m-n:ℤ):ℂ) • shiftedModes o (m+n)

theorem defect_comm_half (o : Fin 12) (i : Fin (BasisSize o)) (m n k : ℤ) :
    comm (defect o m n) (halfMode o i k)=0 := by
  rw [defect, comm_sub_left, comm_jacobi_associative, comm_smul_left]
  simp only [shifted_comm_half, comm_smul_right]
  rw [show n+(m+k)=m+(n+k) by omega, show m+n+k=m+(n+k) by omega]
  push_cast
  module

theorem half_centralizer_normal (o : Fin 12) (T : Module.End ℂ (HalfFock o))
    (hT : ∀ i n, T*halfMode o i n=halfMode o i n*T)
    (i j : Fin (BasisSize o)) (m : ℤ) (v : HalfFock o) :
    T (halfNormalMode o i j m v)=halfNormalMode o i j m (T v) := by
  have ht (i : Fin (BasisSize o)) (n : ℤ) (v : HalfFock o) :
      T (halfMode o i n v)=halfMode o i n (T v) :=
    LinearMap.congr_fun (hT i n) v
  have hcreate (a : ℕ) (i : Fin (BasisSize o)) (v : HalfFock o) :
      T (create o a i v)=create o a i (T v) := by
    simpa only [halfMode_negSucc] using ht i (Int.negSucc a) v
  have hann (a : ℕ) (i : Fin (BasisSize o)) (v : HalfFock o) :
      T (halfAnnihilate o a i v)=halfAnnihilate o a i (T v) := by
    simpa only [halfMode_ofNat] using ht i (a:ℤ) v
  have hc (a : ℕ) : T (creationHalfTerm o i j m a v) =
      creationHalfTerm o i j m a (T v) := by
    simp only [creationHalfTerm, LinearMap.comp_apply, hcreate, ht]
  have ha (a : ℕ) : T (annihilationHalfTerm o i j m a v) =
      annihilationHalfTerm o i j m a (T v) := by
    simp only [annihilationHalfTerm, LinearMap.comp_apply, hann, ht]
  rw [halfNormalMode_apply, map_add, halfNormalMode_apply]
  have hsC : T (∑ᶠ a, creationHalfTerm o i j m a v) =
      ∑ᶠ a, T (creationHalfTerm o i j m a v) :=
    T.toAddMonoidHom.map_finsum (creationHalfTerm_finite o i j m v)
  have hsA : T (∑ᶠ a, annihilationHalfTerm o i j m a v) =
      ∑ᶠ a, T (annihilationHalfTerm o i j m a v) :=
    T.toAddMonoidHom.map_finsum (annihilationHalfTerm_finite o i j m v)
  rw [hsC, hsA]
  simp only [hc, ha]

theorem half_centralizer_quadratic (o : Fin 12) (T : Module.End ℂ (HalfFock o))
    (hT : ∀ i n, T*halfMode o i n=halfMode o i n*T) (m : ℤ) :
    T*quadraticMode o m=quadraticMode o m*T := by
  apply LinearMap.ext
  intro v
  change T (quadraticMode o m v)=quadraticMode o m (T v)
  rw [quadraticMode_apply, quadraticMode_apply]
  simp only [map_smul, map_sum, half_centralizer_normal o T hT]

theorem half_centralizer_shifted (o : Fin 12) (T : Module.End ℂ (HalfFock o))
    (hT : ∀ i n, T*halfMode o i n=halfMode o i n*T) (m : ℤ) :
    T*shiftedModes o m=shiftedModes o m*T := by
  apply LinearMap.ext
  intro v
  have h := LinearMap.congr_fun (half_centralizer_quadratic o T hT m) v
  change T (shiftedModes o m v)=shiftedModes o m (T v)
  by_cases hm : m=0
  · simp only [shiftedModes, shiftedQuadraticMode, if_pos hm,
      LinearMap.add_apply, LinearMap.smul_apply, LinearMap.id_apply,
      map_add, map_smul]
    exact congrArg (fun w : HalfFock o => w + ((BasisSize o : ℂ)/16) • T v) h
  · simpa only [shiftedModes, shiftedQuadraticMode, if_neg hm, add_zero] using h

theorem defect_comm_quadratic (o : Fin 12) (m n k : ℤ) :
    comm (defect o m n) (quadraticMode o k)=0 := by
  apply sub_eq_zero.mpr
  exact half_centralizer_quadratic o (defect o m n)
    (fun i a => sub_eq_zero.mp (defect_comm_half o i m n a)) k

theorem defect_comm_shifted (o : Fin 12) (m n k : ℤ) :
    comm (defect o m n) (shiftedModes o k)=0 := by
  apply sub_eq_zero.mpr
  exact half_centralizer_shifted o (defect o m n)
    (fun i a => sub_eq_zero.mp (defect_comm_half o i m n a)) k

end HMT.IV.LatticeHalfConformalCentralizer
end

#print axioms HMT.IV.LatticeHalfConformalCentralizer.shiftedModes
#print axioms HMT.IV.LatticeHalfConformalCentralizer.shifted_comm_half
#print axioms HMT.IV.LatticeHalfConformalCentralizer.defect
#print axioms HMT.IV.LatticeHalfConformalCentralizer.defect_comm_half
#print axioms HMT.IV.LatticeHalfConformalCentralizer.half_centralizer_normal
#print axioms HMT.IV.LatticeHalfConformalCentralizer.half_centralizer_quadratic
#print axioms HMT.IV.LatticeHalfConformalCentralizer.half_centralizer_shifted
#print axioms HMT.IV.LatticeHalfConformalCentralizer.defect_comm_quadratic
#print axioms HMT.IV.LatticeHalfConformalCentralizer.defect_comm_shifted
