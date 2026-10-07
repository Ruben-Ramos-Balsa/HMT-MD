import AdjointTransport
import BosonOccupations
import BosonGibbsMean
import Mathlib.Analysis.InnerProductSpace.Orthonormal

/-!
# Arbitrary bosonic occupations in the algebraic symmetric Fock domain

Every state in the existing `BosonStates n` is represented by a symmetric
monomial. Occupations are arbitrary natural numbers, without a degree cutoff.
Biorthogonal modes make the creation-annihilation number operators read
exactly the occupation variable already used in the convergent BE state sum.
This identifies algebraic readings and statistical variables, not a Hilbert
trace or a completed Fock-space realization of the probability measure.
-/

noncomputable section

namespace HMT.FockTransport.Symmetric

open QuantumOccupations
open scoped BigOperators

variable {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]

/-- The existing countable occupation state space, with no occupation cutoff. -/
def configurationVector : {n : ℕ} → (Fin n → M) → BosonStates n → SymmetricAlgebra R M
  | 0, _, _ => 1
  | _n + 1, v, s =>
      SymmetricAlgebra.ι R M (v 0) ^ s.1 * configurationVector (fun i => v i.succ) s.2

theorem annihilation_zero_of_modes {n : ℕ} (d : Module.Dual R M)
    (v : Fin n → M) (h : ∀ i, d (v i) = 0) (s : BosonStates n) :
    annihilation d (configurationVector v s) = 0 := by
  induction n with
  | zero => simp [configurationVector]
  | succ n ih =>
      have ht := ih (fun i => v i.succ) (fun i => h i.succ) s.2
      simp [configurationVector, annihilation_product, Derivation.leibniz_pow, h, ht]

theorem occupation_power_same (f : M) (d : Module.Dual R M) (h : d f = 1)
    (k : ℕ) (x : SymmetricAlgebra R M) (hx : annihilation d x = 0) :
    occupation f d (SymmetricAlgebra.ι R M f ^ k * x) =
      (k : R) • (SymmetricAlgebra.ι R M f ^ k * x) := by
  cases k with
  | zero => simp [occupation, hx]
  | succ k =>
      rw [occupation_apply, creation_apply, annihilation_product,
        hx, mul_zero, zero_add, Derivation.leibniz_pow, annihilation_generator, h, map_one]
      simp only [Nat.add_sub_cancel, Nat.cast_smul_eq_nsmul, smul_eq_mul,
        nsmul_eq_mul, mul_one, pow_succ]
      ring

theorem occupation_power_other (f g : M) (d : Module.Dual R M) (h : d g = 0)
    (k : ℕ) (x : SymmetricAlgebra R M) :
    occupation f d (SymmetricAlgebra.ι R M g ^ k * x) =
      SymmetricAlgebra.ι R M g ^ k * occupation f d x := by
  simp only [occupation_apply, creation_apply, annihilation_product,
    Derivation.leibniz_pow, annihilation_generator, h, map_zero, smul_zero, mul_zero,
    add_zero]
  ring

/-- In all degrees, the number operator reads the existing BE occupation variable. -/
theorem configuration_number_eigenvector {n : ℕ} (v : Fin n → M)
    (d : Fin n → Module.Dual R M)
    (h : ∀ i j, d i (v j) = if i = j then 1 else 0)
    (i : Fin n) (s : BosonStates n) :
    occupation (v i) (d i) (configurationVector v s) =
      (bosonStateOccupation n i s : R) • configurationVector v s := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
      have ht : ∀ i j : Fin n, d i.succ (v j.succ) = if i = j then 1 else 0 := by
        intro i j
        simpa only [Fin.succ_inj] using h i.succ j.succ
      refine Fin.cases ?_ (fun j => ?_) i
      · have hd : d 0 (v 0) = 1 := by simpa using h 0 0
        have hz : ∀ j : Fin n, d 0 (v j.succ) = 0 := by
          intro j
          simpa using h 0 j.succ
        simp only [configurationVector, bosonStateOccupation, Fin.cases_zero]
        exact occupation_power_same _ _ hd _ _ (annihilation_zero_of_modes _ _ hz _)
      · have hz : d j.succ (v 0) = 0 := by simpa using h j.succ 0
        have hi := ih (fun k => v k.succ) (fun k => d k.succ) ht j s.2
        simp only [configurationVector, bosonStateOccupation, Fin.cases_succ]
        rw [occupation_power_other _ _ _ hz, hi, mul_smul_comm]

theorem configuration_evaluation {n : ℕ} (v : Fin n → M)
    (l : Module.Dual R M) (hl : ∀ i, l (v i) = 1) (s : BosonStates n) :
    SymmetricAlgebra.lift l (configurationVector (R := R) v s) = 1 := by
  induction n with
  | zero => simp [configurationVector]
  | succ n ih =>
      have ht := ih (fun i => v i.succ) (fun i => hl i.succ) s.2
      simp [configurationVector, hl, ht]

/-- Biorthogonality prevents the occupation words from being zero vectors. -/
theorem configuration_ne_zero [Nontrivial R] {n : ℕ} (v : Fin n → M)
    (d : Fin n → Module.Dual R M)
    (h : ∀ i j, d i (v j) = if i = j then 1 else 0) (s : BosonStates n) :
    configurationVector (R := R) v s ≠ 0 := by
  have he := configuration_evaluation v (∑ i, d i) (by
    intro j
    simp [h]) s
  intro hz
  rw [hz, map_zero] at he
  exact zero_ne_one he

section ComplexModes

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- The modal covector is definitionally the one used by adjoint transport. -/
theorem innerDual_eq_inner (f : E) : Exterior.innerDual (𝕜 := ℂ) f = innerₛₗ ℂ f := rfl

theorem orthonormal_configuration_eigenvector {n : ℕ} (v : Fin n → E)
    (hv : Orthonormal ℂ v) (i : Fin n) (s : BosonStates n) :
    occupation (v i) (innerₛₗ ℂ (v i)) (configurationVector (R := ℂ) v s) =
      (bosonStateOccupation n i s : ℂ) • configurationVector (R := ℂ) v s := by
  exact configuration_number_eigenvector v (fun i => innerₛₗ ℂ (v i))
    (orthonormal_iff_ite.mp hv) i s

theorem orthonormal_configuration_ne_zero {n : ℕ} (v : Fin n → E)
    (hv : Orthonormal ℂ v) (s : BosonStates n) :
    configurationVector (R := ℂ) v s ≠ 0 :=
  configuration_ne_zero v (fun i => innerₛₗ ℂ (v i)) (orthonormal_iff_ite.mp hv) s

/-- The algebraic operator readings and the BE coordinate expectation share
the same unrestricted occupation states and the same occupation variable. -/
theorem symmetric_be_occupation {us : List ℝ} (hu : BosonAdmissible us)
    (v : Fin us.length → E) (hv : Orthonormal ℂ v) (i : Fin us.length) :
    (∀ s : BosonStates us.length,
      configurationVector (R := ℂ) v s ≠ 0 ∧
      occupation (v i) (innerₛₗ ℂ (v i)) (configurationVector (R := ℂ) v s) =
        (bosonStateOccupation us.length i s : ℂ) • configurationVector (R := ℂ) v s) ∧
      bosonCoordinateMean us i = bosonMean (us.get i) :=
  ⟨fun s => ⟨orthonormal_configuration_ne_zero v hv s,
    orthonormal_configuration_eigenvector v hv i s⟩, bosonCoordinate_mean_eq hu i⟩

/-- The number readings over all modes accompany the existing Gibbs-sum BE law;
no trace-class or completion assertion is used in this connection. -/
theorem symmetric_gibbs_total_occupation {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E)
    (v : Fin energies.length → E) (hv : Orthonormal ℂ v) :
    (∀ (i : Fin energies.length) (s : BosonStates energies.length),
      occupation (v i) (innerₛₗ ℂ (v i)) (configurationVector (R := ℂ) v s) =
        (bosonStateOccupation energies.length i s : ℂ) •
          configurationVector (R := ℂ) v s) ∧
      bosonGibbsMeanNumber β μ energies =
        (energies.map (fun E => 1 / (Real.exp (β * (E - μ)) - 1))).sum :=
  ⟨fun i s => orthonormal_configuration_eigenvector v hv i s,
    bosonGibbsMeanNumber_exponential hβ hμ⟩

end ComplexModes

#print axioms annihilation_zero_of_modes
#print axioms occupation_power_same
#print axioms occupation_power_other
#print axioms configuration_number_eigenvector
#print axioms configuration_evaluation
#print axioms configuration_ne_zero
#print axioms innerDual_eq_inner
#print axioms orthonormal_configuration_eigenvector
#print axioms orthonormal_configuration_ne_zero
#print axioms symmetric_be_occupation
#print axioms symmetric_gibbs_total_occupation

end HMT.FockTransport.Symmetric
