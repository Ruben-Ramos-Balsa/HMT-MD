import ExteriorTransport
import FermionCoordinates

/-! The exterior number operators read the binary configurations used by the
already checked finite-mode Gibbs construction, for every number of modes.
The biorthogonality data are later discharged by any orthonormal mode family.
-/

noncomputable section
namespace HMT.FockTransport.Exterior

open HMT.FockBridge

variable {R M : Type*} [CommRing R] [AddCommGroup M] [Module R M]

def configurationVector : {n : ℕ} → (Fin n → M) → Occupation n → Domain R M
  | 0, _, _ => 1
  | _n + 1, v, s =>
    if s.1 then creation (v 0) (configurationVector (fun i => v i.succ) s.2)
    else configurationVector (fun i => v i.succ) s.2

def configurationBit (R : Type*) [Zero R] [One R] :
    (n : ℕ) → Fin n → Occupation n → R
  | 0, i, _ => Fin.elim0 i
  | n + 1, i, s => Fin.cases (if s.1 then 1 else 0)
      (fun j => configurationBit R n j s.2) i

theorem contraction_zero_of_modes {n : ℕ} (d : Module.Dual R M)
    (v : Fin n → M) (h : ∀ i, d (v i) = 0) (s : Occupation n) :
    annihilation d (configurationVector v s) = 0 := by
  induction n with
  | zero => simp [configurationVector]
  | succ n ih =>
    have ht := ih (fun i => v i.succ) (fun i => h i.succ) s.2
    cases hb : s.1 <;>
      simp [configurationVector, hb, creation_apply,
        CliffordAlgebra.contractLeft_ι_mul, h, ht]

theorem configurationVector_ne_zero [Nontrivial R] {n : ℕ} (v : Fin n → M)
    (d : Fin n → Module.Dual R M)
    (h : ∀ i j, d i (v j) = if i = j then 1 else 0) (s : Occupation n) :
    configurationVector (R := R) v s ≠ 0 := by
  induction n with
  | zero => exact one_ne_zero
  | succ n ih =>
    have ht : ∀ i j : Fin n, d i.succ (v j.succ) = if i = j then 1 else 0 := by
      intro i j
      simpa only [Fin.succ_inj] using h i.succ j.succ
    have hi := ih (fun i => v i.succ) (fun i => d i.succ) ht s.2
    cases hb : s.1
    · simpa only [configurationVector, hb, Bool.false_eq_true, ↓reduceIte] using hi
    · intro hz
      have hc := congrArg (annihilation (d 0)) hz
      have hd : d 0 (v 0) = 1 := by simpa using h 0 0
      have he : ∀ j : Fin n, d 0 (v j.succ) = 0 := by
        intro j
        simpa using h 0 j.succ
      have ha := contraction_zero_of_modes (d 0) (fun j => v j.succ) he s.2
      simp only [configurationVector, hb, ↓reduceIte, creation_apply,
        CliffordAlgebra.contractLeft_ι_mul, hd, one_smul, ha, mul_zero,
        sub_zero, map_zero] at hc
      exact hi hc

theorem occupation_creation_same (f : M) (d : Module.Dual R M)
    (h : d f = 1) (x : Domain R M) :
    occupation f d (creation f x) = creation f x := by
  simp only [occupation, LinearMap.comp_apply, creation_apply,
    CliffordAlgebra.contractLeft_ι_mul, h, one_smul, mul_sub,
    ← mul_assoc, ExteriorAlgebra.ι_sq_zero, zero_mul, sub_zero]

theorem occupation_creation_other (f g : M) (d : Module.Dual R M)
    (h : d g = 0) (x : Domain R M) :
    occupation f d (creation g x) = creation g (occupation f d x) := by
  have hc := creation_anticommute f g (annihilation d x)
  have hn : creation f (creation g (annihilation d x)) =
      -(creation g (creation f (annihilation d x))) :=
    eq_neg_of_add_eq_zero_left hc
  change creation f (annihilation d (creation g x)) =
    creation g (creation f (annihilation d x))
  rw [show annihilation d (creation g x) = -(creation g (annihilation d x)) by
    simp only [creation_apply, CliffordAlgebra.contractLeft_ι_mul, h, zero_smul,
      zero_sub]]
  rw [map_neg, hn, neg_neg]

/-- The CAR number operators have exactly the binary eigenvalues of the Gibbs
configuration, on every ordered exterior word and for every finite mode count. -/
theorem configuration_number_eigenvector {n : ℕ} (v : Fin n → M)
    (d : Fin n → Module.Dual R M)
    (h : ∀ i j, d i (v j) = if i = j then 1 else 0)
    (i : Fin n) (s : Occupation n) :
    occupation (v i) (d i) (configurationVector v s) =
      configurationBit R n i s • configurationVector v s := by
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
      cases hb : s.1
      · simp only [configurationVector, hb, Bool.false_eq_true, ↓reduceIte,
          configurationBit, Fin.cases_zero, zero_smul]
        change creation (v 0) (annihilation (d 0) _) = 0
        rw [contraction_zero_of_modes (d 0) _ hz, map_zero]
      · simp only [configurationVector, hb, ↓reduceIte,
          configurationBit, Fin.cases_zero, one_smul]
        exact occupation_creation_same (v 0) (d 0) hd _
    · have hz : d j.succ (v 0) = 0 := by simpa using h j.succ 0
      have hi := ih (fun k => v k.succ) (fun k => d k.succ) ht j s.2
      cases hb : s.1
      · simpa only [configurationVector, hb, Bool.false_eq_true, ↓reduceIte,
          configurationBit, Fin.cases_succ] using hi
      · simp only [configurationVector, hb, ↓reduceIte,
          configurationBit, Fin.cases_succ]
        rw [occupation_creation_other _ _ _ hz, hi, map_smul]

theorem real_configurationBit (n : ℕ) (i : Fin n) (s : Occupation n) :
    configurationBit ℝ n i s = stateCoordinateValue n i s := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases ?_ (fun j => ?_) i
    · rfl
    · simpa only [configurationBit, stateCoordinateValue, Fin.cases_succ] using ih j s.2

section ComplexModes

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

theorem complex_configurationBit (n : ℕ) (i : Fin n) (s : Occupation n) :
    configurationBit ℂ n i s = (stateCoordinateValue n i s : ℂ) := by
  induction n with
  | zero => exact Fin.elim0 i
  | succ n ih =>
    refine Fin.cases ?_ (fun j => ?_) i
    · cases hb : s.1 <;> simp [configurationBit, stateCoordinateValue, hb]
    · simpa only [configurationBit, stateCoordinateValue, Fin.cases_succ] using ih j s.2

theorem orthonormal_configuration_eigenvector {n : ℕ} (v : Fin n → E)
    (hv : Orthonormal ℂ v) (i : Fin n) (s : Occupation n) :
    occupation (v i) (innerDual (𝕜 := ℂ) (v i)) (configurationVector (R := ℂ) v s) =
      (stateCoordinateValue n i s : ℂ) • configurationVector (R := ℂ) v s := by
  have h : ∀ i j, innerDual (𝕜 := ℂ) (v i) (v j) = if i = j then 1 else 0 := by
    intro i j
    exact (orthonormal_iff_ite.mp hv) i j
  simpa only [complex_configurationBit] using
    configuration_number_eigenvector v (fun i => innerDual (v i)) h i s

theorem orthonormal_configuration_ne_zero {n : ℕ} (v : Fin n → E)
    (hv : Orthonormal ℂ v) (s : Occupation n) :
    configurationVector (R := ℂ) v s ≠ 0 := by
  apply configurationVector_ne_zero v (fun i => innerDual (𝕜 := ℂ) (v i))
  intro i j
  exact (orthonormal_iff_ite.mp hv) i j

theorem occupation_reading_unique {n : ℕ} (v : Fin n → E)
    (hv : Orthonormal ℂ v) (i : Fin n) (s : Occupation n) (z : ℂ)
    (hz : occupation (v i) (innerDual (𝕜 := ℂ) (v i))
      (configurationVector (R := ℂ) v s) = z • configurationVector (R := ℂ) v s) :
    z = (stateCoordinateValue n i s : ℂ) := by
  have he := orthonormal_configuration_eigenvector v hv i s
  rw [hz] at he
  have hzero : (z - (stateCoordinateValue n i s : ℂ)) •
      configurationVector (R := ℂ) v s = 0 := by
    rw [sub_smul, he, sub_self]
  exact sub_eq_zero.mp ((smul_eq_zero.mp hzero).resolve_right
    (orthonormal_configuration_ne_zero v hv s))

/-- The same number-operator readings are integrated against the already
normalized many-mode Gibbs distribution; no second occupation law is defined. -/
theorem exterior_gibbs_occupation (us : List ℝ) (hu : ∀ u ∈ us, 0 ≤ u)
    (v : Fin us.length → E) (hv : Orthonormal ℂ v) (i : Fin us.length) :
    (∀ s : Occupation us.length,
      occupation (v i) (innerDual (𝕜 := ℂ) (v i)) (configurationVector (R := ℂ) v s) =
        (stateCoordinateValue us.length i s : ℂ) • configurationVector (R := ℂ) v s) ∧
      coordinateMean us i = us.get i / (1 + us.get i) :=
  ⟨fun s => orthonormal_configuration_eigenvector v hv i s,
    coordinateMean_fermi_dirac us hu i⟩

end ComplexModes

#print axioms contraction_zero_of_modes
#print axioms configurationVector_ne_zero
#print axioms occupation_creation_same
#print axioms occupation_creation_other
#print axioms configuration_number_eigenvector
#print axioms orthonormal_configuration_eigenvector
#print axioms orthonormal_configuration_ne_zero
#print axioms occupation_reading_unique
#print axioms exterior_gibbs_occupation

end HMT.FockTransport.Exterior
