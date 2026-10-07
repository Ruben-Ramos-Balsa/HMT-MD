import APPGlobalPrefactor
import ElectronSpin

/-!
# The actual APP principal plane underlying the electronic block

The TRIT phase mode selects the 1/4 eigenvector of the already computed APP
Gram operator. Its additive-fibre lift and the orthogonal part of its
multiplicative projection construct an orthonormal principal plane. The two
actual APP projections act on this plane by the unchanged matrices P and Q
of ElectronSpin. No principal-plane identification is assumed, and the
previous global commutator-norm theorem is not reproved here.

Source: active Article I electron.tex, principal-plane and local electronic
block paragraphs; helicidad_electron.tex, the inherited real principal plane.
-/

noncomputable section
open Matrix

namespace HMT.I.APPSpinBridge

open APPFiberCensus APPFiberOperators APPGramSpectrum APPGlobalCommutator

attribute [local irreducible] sigmaColumn sigmaProjection piProjection

abbrev Ambient := EuclideanSpace ℝ Triple
abbrev LocalPlane := EuclideanSpace ℝ (Fin 2)

/-- The normalized column corresponding to the already identified TRIT mode. -/
def phaseVector : EuclideanSpace ℝ Digit :=
  WithLp.toLp 2 (fun a => orthogonalEigenvectors a 1)

theorem phaseVector_trit (a : Digit) :
    phaseVector a = (APPPhaseMode.phaseMode a : ℝ) / Real.sqrt 6 := by
  change orthogonalEigenvectors a 1 = _
  rw [orthogonalEigenvectors, normalization, Matrix.mul_diagonal]
  simp only [realEigenvectors, Matrix.map_apply, realSquaredLengths, squaredLengths,
    Matrix.cons_val, Fin.reduceFinMk]
  rw [APPPhaseMode.phase_mode_is_eigenvector_column]
  rfl

theorem phaseVector_inner : inner ℝ phaseVector phaseVector = 1 := by
  have h := congrArg (fun A : RealMat => A 1 1) orthogonalEigenvectors_transpose_mul
  simpa only [phaseVector, PiLp.inner_apply, WithLp.ofLp_toLp, RCLike.inner_apply,
    conj_trivial, Matrix.mul_apply, Matrix.transpose_apply, Matrix.one_apply,
    if_pos rfl] using h

theorem gram_phaseVector : gramOperator phaseVector = (1 / 4 : ℝ) • phaseVector := by
  ext a
  have h := congrArg (fun A : RealMat => A a 1) orthogonal_gram_intertwining
  change (generatedGramReal *ᵥ (fun i => orthogonalEigenvectors i 1)) a =
    (1 / 4 : ℝ) * orthogonalEigenvectors a 1
  rw [APPGlobalPrefactor.generated_gram_identification]
  simpa [Matrix.mul_apply, Matrix.mulVec, dotProduct, realEigenvalues, eigenvalues,
    Matrix.diagonal, mul_comm] using h

def firstVector : Ambient := sigmaColumn phaseVector

theorem compressed_first : sigmaColumn.adjoint (piProjection firstVector) =
    (1 / 4 : ℝ) • phaseVector := by
  have h := congrArg (fun A => A phaseVector) compressed_pi_eq_gramOperator
  change sigmaColumn.adjoint (piProjection firstVector) = gramOperator phaseVector at h
  exact h.trans gram_phaseVector

theorem sigma_first : sigmaProjection firstVector = firstVector := by
  rw [sigmaProjection_eq_column]
  change sigmaColumn (sigmaColumn.adjoint (sigmaColumn phaseVector)) = firstVector
  have h := congrArg (fun A => A phaseVector) sigmaColumn_isometry
  change sigmaColumn.adjoint (sigmaColumn phaseVector) = phaseVector at h
  rw [h]
  rfl

theorem sigma_pi_first : sigmaProjection (piProjection firstVector) =
    (1 / 4 : ℝ) • firstVector := by
  rw [sigmaProjection_eq_column]
  change sigmaColumn (sigmaColumn.adjoint (piProjection firstVector)) = _
  rw [compressed_first, map_smul]
  rfl

theorem idempotent_apply {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (P : E →L[ℝ] E) (h : P * P = P) (v : E) : P (P v) = P v := by
  exact congrArg (fun A : E →L[ℝ] E => A v) h

theorem pi_pi_first : piProjection (piProjection firstVector) = piProjection firstVector :=
  idempotent_apply piProjection piProjection_idempotent firstVector

theorem first_inner : inner ℝ firstVector firstVector = 1 := by
  have h := sigmaColumn.inner_map_map_iff_adjoint_comp_self.mpr sigmaColumn_isometry
  exact (h phaseVector phaseVector).trans phaseVector_inner

theorem first_pi_inner : inner ℝ firstVector (piProjection firstVector) = 1 / 4 := by
  change inner ℝ (sigmaColumn phaseVector) (piProjection firstVector) = _
  rw [← sigmaColumn.adjoint_inner_right, compressed_first, real_inner_smul_right,
    phaseVector_inner]
  ring

theorem pi_first_inner : inner ℝ (piProjection firstVector) (piProjection firstVector) = 1 / 4 := by
  have hAdj : piProjection.adjoint = piProjection := piProjection_selfAdjoint
  rw [← piProjection.adjoint_inner_right, hAdj, pi_pi_first, first_pi_inner]

/-- The orthogonal component, with the positive normalization fixing the local orientation. -/
def secondVector : Ambient :=
  (4 / Real.sqrt 3 : ℝ) • (piProjection firstVector - (1 / 4 : ℝ) • firstVector)

theorem sigma_second : sigmaProjection secondVector = 0 := by
  simp only [secondVector, map_smul, map_sub, sigma_pi_first, sigma_first, sub_self,
    smul_zero]

theorem pi_first : piProjection firstVector =
    (1 / 4 : ℝ) • firstVector + (Real.sqrt 3 / 4 : ℝ) • secondVector := by
  have hs : Real.sqrt 3 ≠ 0 := ElectronSpin.sqrt_three_nonzero
  simp only [secondVector, smul_smul]
  rw [show (Real.sqrt 3 / 4) * (4 / Real.sqrt 3) = (1 : ℝ) by field_simp]
  module

theorem pi_second : piProjection secondVector =
    (Real.sqrt 3 / 4 : ℝ) • firstVector + (3 / 4 : ℝ) • secondVector := by
  have hs : Real.sqrt 3 ≠ 0 := ElectronSpin.sqrt_three_nonzero
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = (3 : ℝ) := Real.mul_self_sqrt (by norm_num)
  simp only [secondVector, map_smul, map_sub, pi_pi_first]
  have hc : (Real.sqrt 3 / 4 : ℝ) = (4 / Real.sqrt 3) * (3 / 16) := by
    field_simp
    nlinarith
  rw [hc]
  module

theorem first_second_inner : inner ℝ firstVector secondVector = 0 := by
  simp only [secondVector, real_inner_smul_right, inner_sub_right,
    first_pi_inner, first_inner]
  ring

theorem second_inner : inner ℝ secondVector secondVector = 1 := by
  have hs : Real.sqrt 3 ≠ 0 := ElectronSpin.sqrt_three_nonzero
  have hs2 : Real.sqrt 3 * Real.sqrt 3 = (3 : ℝ) := Real.mul_self_sqrt (by norm_num)
  have hcross : inner ℝ (piProjection firstVector) firstVector = 1 / 4 := by
    rw [real_inner_comm, first_pi_inner]
  simp only [secondVector, real_inner_smul_left, real_inner_smul_right,
    inner_sub_left, inner_sub_right, pi_first_inner, first_pi_inner, hcross, first_inner]
  field_simp
  nlinarith

def planeLinear : LocalPlane →ₗ[ℝ] Ambient where
  toFun v := v 0 • firstVector + v 1 • secondVector
  map_add' v w := by
    simp only [PiLp.add_apply, add_smul]
    module
  map_smul' c v := by
    simp only [PiLp.smul_apply, smul_eq_mul, smul_add, smul_smul, RingHom.id_apply]

theorem planeLinear_inner (v w : LocalPlane) :
    inner ℝ (planeLinear v) (planeLinear w) = inner ℝ v w := by
  have hrev : inner ℝ secondVector firstVector = 0 := by
    rw [real_inner_comm, first_second_inner]
  simp only [planeLinear, LinearMap.coe_mk, AddHom.coe_mk, inner_add_left,
    inner_add_right, real_inner_smul_left, real_inner_smul_right,
    first_inner, second_inner, first_second_inner, hrev]
  simp [PiLp.inner_apply, Fin.sum_univ_two, real_inner_comm, mul_comm]

/-- The inherited counting-Hilbert metric on the actual APP principal plane. -/
def planeEmbedding : LocalPlane →ₗᵢ[ℝ] Ambient where
  toLinearMap := planeLinear
  norm_map' v := by
    apply (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
    simpa only [real_inner_self_eq_norm_sq] using planeLinear_inner v v

theorem planeEmbedding_apply (v : LocalPlane) :
    planeEmbedding v = v 0 • firstVector + v 1 • secondVector := rfl

theorem localMatrix_apply (A : ElectronSpin.MatR) (v : LocalPlane) (i : Fin 2) :
    (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) A v) i =
      (A *ᵥ (fun j => v j)) i := rfl

theorem sigma_intertwining (v : LocalPlane) :
    sigmaProjection (planeEmbedding v) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P v) := by
  rw [planeEmbedding_apply, map_add, map_smul, map_smul, sigma_first, sigma_second,
    planeEmbedding_apply]
  simp [ElectronSpin.P, localMatrix_apply, Matrix.mulVec,
    dotProduct, Fin.sum_univ_two]

theorem pi_intertwining (v : LocalPlane) :
    piProjection (planeEmbedding v) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q v) := by
  rw [planeEmbedding_apply, map_add, map_smul, map_smul, pi_first, pi_second,
    planeEmbedding_apply]
  simp [ElectronSpin.Q, localMatrix_apply, Matrix.mulVec,
    dotProduct, Fin.sum_univ_two]
  module

theorem localMatrix_mul_apply (A B : ElectronSpin.MatR) (v : LocalPlane) :
    Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) (A * B) v =
      Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) A
        (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) B v) := by
  exact congrArg (fun T : LocalPlane →L[ℝ] LocalPlane => T v)
    (map_mul (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ)) A B)

theorem localMatrix_sub_apply (A B : ElectronSpin.MatR) (v : LocalPlane) :
    Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) (A - B) v =
      Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) A v -
        Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) B v := by
  exact congrArg (fun T : LocalPlane →L[ℝ] LocalPlane => T v)
    (map_sub (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ)) A B)

theorem generic_clm_commutator_intertwining
    {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    (f : E →ₗ[ℝ] F) (A B : F →L[ℝ] F) (P Q : E →ₗ[ℝ] E)
    (hA : ∀ v, A (f v) = f (P v)) (hB : ∀ v, B (f v) = f (Q v)) (v : E) :
    (A * B - B * A) (f v) = f (P (Q v) - Q (P v)) := by
  simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.mul_apply]
  rw [hB, hA, hA, hB, map_sub]

theorem commutator_intertwining (v : LocalPlane) :
    APPGlobalPrefactor.incompatibility (planeEmbedding v) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ)
        (ElectronSpin.commutator ElectronSpin.P ElectronSpin.Q) v) := by
  have h := generic_clm_commutator_intertwining planeEmbedding.toLinearMap
    sigmaProjection piProjection
    (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P).toLinearMap
    (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q).toLinearMap
    sigma_intertwining pi_intertwining v
  exact h.trans (congrArg planeEmbedding (by
    rw [ElectronSpin.commutator, localMatrix_sub_apply, localMatrix_mul_apply,
      localMatrix_mul_apply]
    rfl))

theorem S_intertwining (v : LocalPlane) :
    (2 : ℝ) • sigmaProjection (planeEmbedding v) - planeEmbedding v =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.S v) := by
  rw [sigma_intertwining, ← map_smul, ← map_sub]
  congr 1
  simp only [ElectronSpin.S, map_sub, map_smul, map_one, ContinuousLinearMap.sub_apply,
    ContinuousLinearMap.smul_apply, ContinuousLinearMap.one_apply]

theorem J_intertwining (v : LocalPlane) :
    (4 / Real.sqrt 3 : ℝ) • APPGlobalPrefactor.incompatibility (planeEmbedding v) =
      planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.J v) := by
  rw [commutator_intertwining, ← map_smul]
  congr 1
  simp only [ElectronSpin.J, map_smul, ContinuousLinearMap.smul_apply]

/-- The manuscript's uniform measure divides the counting vector norm by 27.
Multiplying this basis by 27 gives exactly the same local Hilbert coordinates. -/
def uniformPlaneLinear : LocalPlane →ₗ[ℝ] Ambient := (27 : ℝ) • planeLinear

theorem uniformPlane_norm (v : LocalPlane) :
    ‖uniformPlaneLinear v‖ / 27 = ‖v‖ := by
  change ‖(27 : ℝ) • planeEmbedding v‖ / 27 = ‖v‖
  rw [norm_smul, planeEmbedding.norm_map]
  norm_num

theorem uniform_sigma_intertwining (v : LocalPlane) :
    sigmaProjection (uniformPlaneLinear v) =
      uniformPlaneLinear (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P v) := by
  change sigmaProjection ((27 : ℝ) • planeEmbedding v) =
    (27 : ℝ) • planeEmbedding _
  rw [map_smul, sigma_intertwining]

theorem uniform_pi_intertwining (v : LocalPlane) :
    piProjection (uniformPlaneLinear v) =
      uniformPlaneLinear (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q v) := by
  change piProjection ((27 : ℝ) • planeEmbedding v) =
    (27 : ℝ) • planeEmbedding _
  rw [map_smul, pi_intertwining]

def principalPlane : Submodule ℝ Ambient := LinearMap.range planeEmbedding.toLinearMap

theorem sigma_invariant {z : Ambient} (hz : z ∈ principalPlane) :
    sigmaProjection z ∈ principalPlane := by
  obtain ⟨v, rfl⟩ := hz
  exact ⟨Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P v,
    (sigma_intertwining v).symm⟩

theorem pi_invariant {z : Ambient} (hz : z ∈ principalPlane) :
    piProjection z ∈ principalPlane := by
  obtain ⟨v, rfl⟩ := hz
  exact ⟨Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q v,
    (pi_intertwining v).symm⟩

/-- Concrete identification with the unchanged local electronic block. -/
theorem actual_APP_local_block (v : LocalPlane) :
    ‖planeEmbedding v‖ = ‖v‖ ∧
      sigmaProjection (planeEmbedding v) =
        planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.P v) ∧
      piProjection (planeEmbedding v) =
        planeEmbedding (Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) ElectronSpin.Q v) :=
  ⟨planeEmbedding.norm_map v, sigma_intertwining v, pi_intertwining v⟩

end HMT.I.APPSpinBridge

#print axioms HMT.I.APPSpinBridge.phaseVector_trit
#print axioms HMT.I.APPSpinBridge.gram_phaseVector
#print axioms HMT.I.APPSpinBridge.first_inner
#print axioms HMT.I.APPSpinBridge.first_second_inner
#print axioms HMT.I.APPSpinBridge.second_inner
#print axioms HMT.I.APPSpinBridge.sigma_first
#print axioms HMT.I.APPSpinBridge.sigma_second
#print axioms HMT.I.APPSpinBridge.pi_first
#print axioms HMT.I.APPSpinBridge.pi_second
#print axioms HMT.I.APPSpinBridge.planeLinear_inner
#print axioms HMT.I.APPSpinBridge.planeEmbedding
#print axioms HMT.I.APPSpinBridge.sigma_intertwining
#print axioms HMT.I.APPSpinBridge.pi_intertwining
#print axioms HMT.I.APPSpinBridge.commutator_intertwining
#print axioms HMT.I.APPSpinBridge.S_intertwining
#print axioms HMT.I.APPSpinBridge.J_intertwining
#print axioms HMT.I.APPSpinBridge.uniformPlane_norm
#print axioms HMT.I.APPSpinBridge.uniform_sigma_intertwining
#print axioms HMT.I.APPSpinBridge.uniform_pi_intertwining
#print axioms HMT.I.APPSpinBridge.sigma_invariant
#print axioms HMT.I.APPSpinBridge.pi_invariant
#print axioms HMT.I.APPSpinBridge.actual_APP_local_block
