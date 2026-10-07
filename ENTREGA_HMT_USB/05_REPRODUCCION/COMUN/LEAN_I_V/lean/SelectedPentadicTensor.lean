import PentadicTensorCarrier
import SelectedActionDomain

/-! The geometric carrier consumes the selected autoscale coordinate of
article I. The radical realization is used only after the already proved
recognition theorem. The selected coordinate is not replaced by a new input. -/

namespace HMT.ArticleII.PentadicTensor

noncomputable section

open scoped BigOperators Matrix

theorem Gamma0_isSTF (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (x : Fin 12 → ℝ) : IsSTF (Gamma0 t x) := by
  have hQ (p : Fin 12) : IsSTF (Qposition t p) :=
    Qsix_STF t ht hd (signedPosition p)
  constructor
  · ext i j
    change (∑ p, x p * Qposition t p j i) = ∑ p, x p * Qposition t p i j
    apply Finset.sum_congr rfl
    intro p _
    rw [show Qposition t p j i = Qposition t p i j from
      congrFun (congrFun (hQ p).1 i) j]
  · change (∑ i, ∑ p, x p * Qposition t p i i) = 0
    rw [Finset.sum_comm]
    apply Finset.sum_eq_zero
    intro p _
    rw [← Finset.mul_sum]
    change x p * Matrix.trace (Qposition t p) = 0
    rw [(hQ p).2, mul_zero]

theorem STF_smul (Q : Mat3) (hQ : IsSTF Q) (c : ℝ) : IsSTF (c • Q) := by
  constructor
  · simp only [Matrix.transpose_smul, hQ.1]
  · simp only [Matrix.trace_smul, hQ.2, smul_zero]

theorem Gamma5_isSTF (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (x : Fin 12 → ℝ) : IsSTF (Gamma5 t x) :=
  STF_smul _ (Gamma0_isSTF t ht hd x) _

theorem Gamma5Adj_isV5 (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (Q : Mat3) (hQ : IsSTF Q) : IsV5 (Gamma5Adj t Q) := by
  intro p
  have h := Gamma5_left_projector t ht hd (Gamma5Adj t Q) p
  rw [Gamma5_right_inverse t ht hd Q hQ] at h
  exact h.symm

abbrev V5 := { x : Fin 12 → ℝ // IsV5 x }

def tensorEquivalence (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0) : V5 ≃ STF where
  toFun x := ⟨Gamma5 t x.val, Gamma5_isSTF t ht hd x.val⟩
  invFun Q := ⟨Gamma5Adj t Q.val, Gamma5Adj_isV5 t ht hd Q.val Q.property⟩
  left_inv x := Subtype.ext (Gamma5_left_inverse_on_V5 t ht hd x.val x.property)
  right_inv Q := Subtype.ext (Gamma5_right_inverse t ht hd Q.val Q.property)

theorem selected_phi_relation :
    HMT.I.SelectedAction.phi ^ 2 = HMT.I.SelectedAction.phi + 1 := by
  unfold HMT.I.SelectedAction.phi
  rw [_root_.AlphaCarryLimit.autoscale_recognition]
  nlinarith [_root_.AutoscaleLimit.positive_root_polynomial.2]

theorem selected_phi_denominator : HMT.I.SelectedAction.phi + 2 ≠ 0 := by
  unfold HMT.I.SelectedAction.phi
  rw [_root_.AlphaCarryLimit.autoscale_recognition]
  linarith [_root_.AutoscaleLimit.positive_root_polynomial.1]

theorem selected_phi_recognition :
    HMT.I.SelectedAction.phi = phiRealization := by
  unfold HMT.I.SelectedAction.phi phiRealization
  exact _root_.AlphaCarryLimit.autoscale_recognition

theorem selected_tensor_frame_reconstruction (Q : Mat3) (hQ : IsSTF Q) :
    Gamma5 HMT.I.SelectedAction.phi (Gamma5Adj HMT.I.SelectedAction.phi Q) = Q :=
  Gamma5_right_inverse HMT.I.SelectedAction.phi selected_phi_relation
    selected_phi_denominator Q hQ

theorem selected_tensor_frame_inverse (x : Fin 12 → ℝ) (hx : IsV5 x) :
    Gamma5Adj HMT.I.SelectedAction.phi (Gamma5 HMT.I.SelectedAction.phi x) = x :=
  Gamma5_left_inverse_on_V5 HMT.I.SelectedAction.phi selected_phi_relation
    selected_phi_denominator x hx

theorem selected_tensor_Gram (p q : Fin 12) :
    frobenius (Qposition HMT.I.SelectedAction.phi p)
      (Qposition HMT.I.SelectedAction.phi q) = (8/5:ℝ) * (P5 p q : ℝ) :=
  position_tensor_gram HMT.I.SelectedAction.phi selected_phi_relation
    selected_phi_denominator p q

def selectedTensorEquivalence : V5 ≃ STF :=
  tensorEquivalence HMT.I.SelectedAction.phi selected_phi_relation selected_phi_denominator

#print axioms selected_phi_relation
#print axioms selected_tensor_frame_reconstruction
#print axioms selected_tensor_frame_inverse
#print axioms selected_tensor_Gram
#print axioms selectedTensorEquivalence

end
end HMT.ArticleII.PentadicTensor
