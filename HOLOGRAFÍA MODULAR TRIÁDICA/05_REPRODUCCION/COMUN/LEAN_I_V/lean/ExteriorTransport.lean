import Mathlib.LinearAlgebra.ExteriorAlgebra.Basic
import Mathlib.LinearAlgebra.CliffordAlgebra.Contraction
import Mathlib.Analysis.InnerProductSpace.Adjoint

/-!
Article V, 20_completaciones_cuanticas.tex:94-134 and
30_fock_gibbs.tex:51-101. The algebraic finite-particle exterior domain is
constructed as ExteriorAlgebra, with arbitrary one-particle module and degree.
Creation is wedge multiplication; annihilation is the canonical contraction.
The algebraic transport is defined by the induced exterior-algebra map.
No CAR, naturality, or Pauli identity is assumed as a premise.
The Hilbert norm on exterior powers is a separate analytic construction.
-/

noncomputable section

namespace HMT.FockTransport.Exterior

variable {R M N P : Type*} [CommRing R]
  [AddCommGroup M] [Module R M]
  [AddCommGroup N] [Module R N]
  [AddCommGroup P] [Module R P]

abbrev Domain (R M : Type*) [CommRing R] [AddCommGroup M] [Module R M] :=
  ExteriorAlgebra R M

def creation (f : M) : Domain R M →ₗ[R] Domain R M where
  toFun x := ExteriorAlgebra.ι R f * x
  map_add' := mul_add _
  map_smul' c x := by simp only [RingHom.id_apply, mul_smul_comm]

abbrev annihilation (d : Module.Dual R M) : Domain R M →ₗ[R] Domain R M :=
  CliffordAlgebra.contractLeft (Q := (0 : QuadraticForm R M)) d

abbrev transport (T : M →ₗ[R] N) : Domain R M →ₐ[R] Domain R N :=
  ExteriorAlgebra.map T

def occupation (f : M) (d : Module.Dual R M) : Domain R M →ₗ[R] Domain R M :=
  (creation f).comp (annihilation d)

@[simp] theorem creation_apply (f : M) (x : Domain R M) :
    creation f x = ExteriorAlgebra.ι R f * x := rfl

theorem creation_square_zero (f : M) (x : Domain R M) :
    creation f (creation f x) = 0 := by
  simp only [creation_apply, ← mul_assoc, ExteriorAlgebra.ι_sq_zero, zero_mul]

theorem creation_anticommute (f g : M) (x : Domain R M) :
    creation f (creation g x) + creation g (creation f x) = 0 := by
  simp only [creation_apply, ← mul_assoc, ← add_mul]
  rw [ExteriorAlgebra.ι_add_mul_swap, zero_mul]

theorem annihilation_square_zero (d : Module.Dual R M) (x : Domain R M) :
    annihilation d (annihilation d x) = 0 :=
  CliffordAlgebra.contractLeft_contractLeft d x

theorem annihilation_anticommute (d e : Module.Dual R M) (x : Domain R M) :
    annihilation d (annihilation e x) + annihilation e (annihilation d x) = 0 := by
  rw [CliffordAlgebra.contractLeft_comm, neg_add_cancel]

theorem canonical_anticommutation (d : Module.Dual R M) (f : M)
    (x : Domain R M) :
    annihilation d (creation f x) + creation f (annihilation d x) = d f • x := by
  simp only [creation_apply, CliffordAlgebra.contractLeft_ι_mul, sub_add_cancel]

theorem pauli_idempotence (f : M) (d : Module.Dual R M) (h : d f = 1)
    (x : Domain R M) : occupation f d (occupation f d x) = occupation f d x := by
  simp only [occupation, LinearMap.comp_apply, creation_apply,
    CliffordAlgebra.contractLeft_ι_mul, h, one_smul,
    CliffordAlgebra.contractLeft_contractLeft, mul_zero, sub_zero]

theorem vacuum_unoccupied (f : M) (d : Module.Dual R M) :
    occupation f d (1 : Domain R M) = 0 := by
  simp [occupation, creation]

theorem one_particle_occupied (f : M) (d : Module.Dual R M) (h : d f = 1) :
    occupation f d (ExteriorAlgebra.ι R f) = ExteriorAlgebra.ι R f := by
  simp [occupation, creation, h]

theorem transport_identity (x : Domain R M) : transport (LinearMap.id : M →ₗ[R] M) x = x := by
  simp [transport, ExteriorAlgebra.map_id]

theorem transport_composition (T : M →ₗ[R] N) (S : N →ₗ[R] P)
    (x : Domain R M) : transport S (transport T x) = transport (S.comp T) x := by
  exact DFunLike.congr_fun (ExteriorAlgebra.map_comp_map T S) x

theorem transport_creation (T : M →ₗ[R] N) (f : M) (x : Domain R M) :
    transport T (creation f x) = creation (T f) (transport T x) := by
  simp only [creation_apply, map_mul, ExteriorAlgebra.map_apply_ι]

/-- Naturality of contraction for every linear map, not only isometries. -/
theorem transport_annihilation (T : M →ₗ[R] N) (d : Module.Dual R N)
    (x : Domain R M) :
    annihilation d (transport T x) = transport T (annihilation (d.comp T) x) := by
  induction x using CliffordAlgebra.left_induction with
  | algebraMap r => simp
  | add x y hx hy => simp only [map_add, hx, hy]
  | ι_mul f x hx =>
    simp only [map_mul, ExteriorAlgebra.map_apply_ι,
      CliffordAlgebra.contractLeft_ι_mul, map_sub, map_smul,
      LinearMap.comp_apply, hx]

theorem transport_occupation (T : M →ₗ[R] N) (f : M) (d : Module.Dual R N)
    (x : Domain R M) :
    occupation (T f) d (transport T x) = transport T (occupation f (d.comp T) x) := by
  simp only [occupation, LinearMap.comp_apply, transport_annihilation,
    transport_creation]

section HilbertOneParticle

variable {𝕜 E F : Type*} [RCLike 𝕜]
  [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [NormedAddCommGroup F] [InnerProductSpace 𝕜 F]

def innerDual (g : E) : Module.Dual 𝕜 E :=
  (innerSL 𝕜 g).toLinearMap

@[simp] theorem innerDual_apply (g x : E) : innerDual g x = inner 𝕜 g x := rfl

theorem isometry_dual (T : E →ₗᵢ[𝕜] F) (f : E) :
    (innerDual (T f)).comp T.toLinearMap = innerDual f := by
  ext x
  exact T.inner_map_map f x

theorem isometry_transports_occupation (T : E →ₗᵢ[𝕜] F) (f : E)
    (x : Domain 𝕜 E) :
    occupation (T f) (innerDual (T f)) (transport T.toLinearMap x) =
      transport T.toLinearMap (occupation f (innerDual f) x) := by
  simpa only [isometry_dual] using
    transport_occupation T.toLinearMap f (innerDual (T f)) x

theorem normalized_mode_pauli (f : E) (h : ‖f‖ = 1) (x : Domain 𝕜 E) :
    occupation f (innerDual f) (occupation f (innerDual f) x) =
      occupation f (innerDual f) x := by
  apply pauli_idempotence
  simp [innerDual_apply, inner_self_eq_norm_sq_to_K, h]

variable [CompleteSpace E] [CompleteSpace F]

theorem adjoint_dual (T : E →L[𝕜] F) (g : F) :
    (innerDual g).comp T.toLinearMap = innerDual (T.adjoint g) := by
  ext x
  exact (T.adjoint_inner_left x g).symm

theorem adjoint_transports_annihilation (T : E →L[𝕜] F) (g : F)
    (x : Domain 𝕜 E) :
    annihilation (innerDual g) (transport T.toLinearMap x) =
      transport T.toLinearMap (annihilation (innerDual (T.adjoint g)) x) := by
  rw [transport_annihilation, adjoint_dual]

end HilbertOneParticle

#print axioms canonical_anticommutation
#print axioms creation_anticommute
#print axioms annihilation_anticommute
#print axioms pauli_idempotence
#print axioms transport_composition
#print axioms transport_annihilation
#print axioms isometry_transports_occupation
#print axioms normalized_mode_pauli
#print axioms adjoint_transports_annihilation

end HMT.FockTransport.Exterior
