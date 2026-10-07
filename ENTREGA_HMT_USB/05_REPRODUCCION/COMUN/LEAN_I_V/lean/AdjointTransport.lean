import ExteriorTransport
import SymmetricTransport

/-!
# Hilbert-adjoint transport on the algebraic symmetric Fock domain

Source: Article V, `30_fock_gibbs.tex`, equations
`v:fock:eq:transporte-creacion`, `v:fock:eq:transporte-aniquilacion`,
`v:fock:eq:transporte-ocupacion`, and `v:fock:eq:control-no-isometrico`.

The symmetric creation/annihilation operators are those already constructed
algebraically in `SymmetricTransport`. The covector is the original one-particle
inner product, via `Exterior.innerDual`; no replacement pairing is introduced.
The general annihilation identity retains `T.adjoint g`. The same-vector and
occupation identities are specialized only for a linear isometry.

No norm on the symmetric algebra, normalized occupation basis, or boundedness
of creation/annihilation on a Hilbert completion is asserted here.
-/

noncomputable section

namespace HMT.FockTransport.Symmetric

open HMT.FockTransport.Exterior (innerDual)

section AlgebraicOccupation

variable {R M N : Type*} [CommRing R]
  [AddCommGroup M] [Module R M] [AddCommGroup N] [Module R N]

/-- Mode occupation on the algebraic symmetric finite-particle domain. -/
def occupation (f : M) (d : Module.Dual R M) :
    SymmetricAlgebra R M →ₗ[R] SymmetricAlgebra R M :=
  (creation f).comp (annihilation d).toLinearMap

@[simp] theorem occupation_apply (f : M) (d : Module.Dual R M)
    (x : SymmetricAlgebra R M) :
    occupation f d x = creation f (annihilation d x) := rfl

/-- Before a metric specialization, occupation transports the pulled-back dual. -/
theorem transport_occupation (T : M →ₗ[R] N) (f : M) (d : Module.Dual R N)
    (x : SymmetricAlgebra R M) :
    occupation (T f) d (gamma T x) = gamma T (occupation f (d.comp T) x) := by
  simp only [occupation_apply, annihilation_naturality, creation_naturality]

end AlgebraicOccupation

section InnerProduct

variable {𝕜 E F : Type*} [RCLike 𝕜]
  [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
  [NormedAddCommGroup F] [InnerProductSpace 𝕜 F]

theorem hilbert_transports_creation (T : E →L[𝕜] F) (f : E)
    (x : SymmetricAlgebra 𝕜 E) :
    gamma T.toLinearMap (creation f x) =
      creation (T f) (gamma T.toLinearMap x) :=
  creation_naturality T.toLinearMap f x

/-- The same-vector annihilation identity is valid for isometries. -/
theorem isometry_transports_annihilation (T : E →ₗᵢ[𝕜] F) (f : E)
    (x : SymmetricAlgebra 𝕜 E) :
    annihilation (innerDual (T f)) (gamma T.toLinearMap x) =
      gamma T.toLinearMap (annihilation (innerDual f) x) := by
  rw [annihilation_naturality, Exterior.isometry_dual]

/-- Occupation transport uses the original inner product and no renormalization. -/
theorem isometry_transports_occupation (T : E →ₗᵢ[𝕜] F) (f : E)
    (x : SymmetricAlgebra 𝕜 E) :
    occupation (T f) (innerDual (T f)) (gamma T.toLinearMap x) =
      gamma T.toLinearMap (occupation f (innerDual f) x) := by
  simpa only [Exterior.isometry_dual] using
    transport_occupation T.toLinearMap f (innerDual (T f)) x

theorem isometry_transports_occupation_linear (T : E →ₗᵢ[𝕜] F) (f : E) :
    (occupation (T f) (innerDual (T f))).comp (gamma T.toLinearMap).toLinearMap =
      (gamma T.toLinearMap).toLinearMap.comp (occupation f (innerDual f)) := by
  ext x
  exact isometry_transports_occupation T f x

variable [CompleteSpace E] [CompleteSpace F]

/-- General transport: the adjoint acts on the target vector `g`. -/
theorem adjoint_transports_annihilation (T : E →L[𝕜] F) (g : F)
    (x : SymmetricAlgebra 𝕜 E) :
    annihilation (innerDual g) (gamma T.toLinearMap x) =
      gamma T.toLinearMap (annihilation (innerDual (T.adjoint g)) x) := by
  rw [annihilation_naturality, Exterior.adjoint_dual]

theorem adjoint_transports_annihilation_linear (T : E →L[𝕜] F) (g : F) :
    (annihilation (innerDual g)).toLinearMap.comp (gamma T.toLinearMap).toLinearMap =
      (gamma T.toLinearMap).toLinearMap.comp
        (annihilation (innerDual (T.adjoint g))).toLinearMap := by
  ext x
  exact adjoint_transports_annihilation T g x

theorem adjoint_transports_occupation (T : E →L[𝕜] F) (f : E) (g : F)
    (x : SymmetricAlgebra 𝕜 E) :
    occupation (T f) (innerDual g) (gamma T.toLinearMap x) =
      gamma T.toLinearMap (occupation f (innerDual (T.adjoint g)) x) := by
  simpa only [Exterior.adjoint_dual] using
    transport_occupation T.toLinearMap f (innerDual g) x

end InnerProduct

section NonisometricControl

/-- A one-dimensional genuine linear contraction, not a redefined pairing. -/
def scalarTransport (t : ℝ) : ℝ →L[ℝ] ℝ :=
  t • ContinuousLinearMap.id ℝ ℝ

@[simp] theorem scalarTransport_apply (t x : ℝ) : scalarTransport t x = t * x := rfl

theorem scalarTransport_contractive {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    ‖scalarTransport t‖ ≤ 1 := by
  simpa [scalarTransport, norm_smul, abs_of_nonneg ht0] using ht1

/-- The left-hand side of the source's nonisometric one-particle control. -/
theorem scalar_annihilation_after_transport (t : ℝ) :
    annihilation (innerDual (scalarTransport t 1))
      (gamma (scalarTransport t).toLinearMap (SymmetricAlgebra.ι ℝ ℝ 1)) =
        algebraMap ℝ (SymmetricAlgebra ℝ ℝ) (t ^ 2) := by
  simp [Exterior.innerDual_apply, real_inner_self_eq_norm_sq, sq]

/-- The incorrectly specialized right-hand side stays the vacuum. -/
theorem scalar_transport_after_annihilation (t : ℝ) :
    gamma (scalarTransport t).toLinearMap
      (annihilation (innerDual (1 : ℝ)) (SymmetricAlgebra.ι ℝ ℝ 1)) =
        (1 : SymmetricAlgebra ℝ ℝ) := by
  simp [Exterior.innerDual_apply]

/-- For `0 < t < 1`, deleting the adjoint really changes the result. -/
theorem scalar_nonisometric_failure {t : ℝ} (ht0 : 0 < t) (ht1 : t < 1) :
    annihilation (innerDual (scalarTransport t 1))
        (gamma (scalarTransport t).toLinearMap (SymmetricAlgebra.ι ℝ ℝ 1)) ≠
      gamma (scalarTransport t).toLinearMap
        (annihilation (innerDual (1 : ℝ)) (SymmetricAlgebra.ι ℝ ℝ 1)) := by
  rw [scalar_annihilation_after_transport, scalar_transport_after_annihilation]
  intro h
  have ht : t ^ 2 = 1 :=
    (SymmetricAlgebra.algebraMap_eq_one_iff (R := ℝ) (M := ℝ) (t ^ 2)).mp h
  nlinarith

end NonisometricControl

end HMT.FockTransport.Symmetric

#print axioms HMT.FockTransport.Symmetric.transport_occupation
#print axioms HMT.FockTransport.Symmetric.hilbert_transports_creation
#print axioms HMT.FockTransport.Symmetric.isometry_transports_annihilation
#print axioms HMT.FockTransport.Symmetric.isometry_transports_occupation
#print axioms HMT.FockTransport.Symmetric.isometry_transports_occupation_linear
#print axioms HMT.FockTransport.Symmetric.adjoint_transports_annihilation
#print axioms HMT.FockTransport.Symmetric.adjoint_transports_annihilation_linear
#print axioms HMT.FockTransport.Symmetric.adjoint_transports_occupation
#print axioms HMT.FockTransport.Symmetric.scalarTransport_contractive
#print axioms HMT.FockTransport.Symmetric.scalar_annihilation_after_transport
#print axioms HMT.FockTransport.Symmetric.scalar_transport_after_annihilation
#print axioms HMT.FockTransport.Symmetric.scalar_nonisometric_failure
