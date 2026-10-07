import CKMSpectral
import CKMComplex

noncomputable section
open Matrix Complex
namespace HMT.CKM.Spectral
open HMT.CKM.ComplexRealization

def massTransport (a b c δ : ℝ) (m : Fin 3 → ℝ) : Mat3 :=
  CKM a b c δ * diagonal (fun i => (m i : ℂ)) * (CKM a b c δ)ᴴ

theorem massTransport_hermitian (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    (massTransport a b c δ m).IsHermitian := by
  apply unitary_transport_hermitian
  ext i j
  by_cases hij : i = j
  · subst j; simp
  · simp [Matrix.diagonal_apply, hij, Ne.symm hij]

theorem massTransport_charpoly (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    (massTransport a b c δ m).charpoly =
      (diagonal (fun i => (m i : ℂ))).charpoly :=
  inverse_transport_charpoly _ _ _ (CKM_right_unitary a b c δ)

theorem massTransport_spectrum (a b c δ : ℝ) (m : Fin 3 → ℝ) :
    spectrum ℂ (massTransport a b c δ m) =
      spectrum ℂ (diagonal (fun i => (m i : ℂ))) := by
  exact unitary_transport_spectrum ⟨CKM a b c δ, CKM_mem_unitary a b c δ⟩ _

theorem massTransport_commutator (a b c δ : ℝ) (u d : Fin 3 → ℝ) :
    (commutator (diagonal (fun i => (u i : ℂ))) (massTransport a b c δ d)).det =
      2 * I * ((u 0 - u 1) * (u 1 - u 2) * (u 2 - u 0) : ℝ) *
        ((massTransport a b c δ d) 0 1 * (massTransport a b c δ d) 1 2 *
          (massTransport a b c δ d) 2 0).im :=
  hermitian_commutator_det u _ (massTransport_hermitian a b c δ d)

#print axioms massTransport_hermitian
#print axioms massTransport_charpoly
#print axioms massTransport_spectrum
#print axioms massTransport_commutator
end HMT.CKM.Spectral
