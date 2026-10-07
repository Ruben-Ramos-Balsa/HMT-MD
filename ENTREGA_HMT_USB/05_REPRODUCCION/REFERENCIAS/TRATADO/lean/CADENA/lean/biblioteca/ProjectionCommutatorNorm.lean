import Mathlib

namespace HMT.I.ProjectionNorm

open scoped InnerProductSpace
open ContinuousLinearMap

variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]

theorem orthogonal_projection_decomposition
    (P : E →L[𝕜] E) (hP : P*P=P) (hPs : star P=P) (x : E) :
    ‖x‖^2 = ‖P x‖^2 + ‖x-P x‖^2 := by
  have hp : P (P x) = P x := congrArg (fun T : E →L[𝕜] E => T x) hP
  have ho : inner 𝕜 (P x) (x-P x) = 0 := by
    have h := adjoint_inner_left P (x-P x) x
    change inner 𝕜 ((star P) x) (x-P x) = inner 𝕜 x (P (x-P x)) at h
    simpa [hPs, map_sub, hp] using h
  have h := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero (P x) (x-P x) ho
  simpa only [add_sub_cancel, pow_two] using h

theorem offDiagonal_norm
    (P B : E →L[𝕜] E) (hP : P*P=P) (hPs : star P=P)
    (hPB : P*B=B) (hBP : B*P=0) : ‖B-star B‖ = ‖B‖ := by
  have hPBs : P*star B=0 := by
    have h := congrArg star hBP
    simpa only [star_mul, hPs, star_zero] using h
  have hBsP : star B*P=star B := by
    have h := congrArg star hPB
    simpa only [star_mul, hPs] using h
  have hnorm (x : E) : ‖(B-star B) x‖^2 = ‖B x‖^2 + ‖(star B) x‖^2 := by
    have h1 : P (B x)=B x := congrArg (fun T : E →L[𝕜] E => T x) hPB
    have h2 : P ((star B) x)=0 := congrArg (fun T : E →L[𝕜] E => T x) hPBs
    have ho : inner 𝕜 (B x) ((star B) x)=0 := by
      have h := adjoint_inner_left P ((star B) x) (B x)
      change inner 𝕜 ((star P) (B x)) ((star B) x) = inner 𝕜 (B x) (P ((star B) x)) at h
      simpa only [hPs, h1, h2, inner_zero_right] using h
    simpa only [ContinuousLinearMap.sub_apply, ho, map_zero, mul_zero, sub_zero]
      using (norm_sub_sq (𝕜 := 𝕜) (B x) ((star B) x))
  apply le_antisymm
  · apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
    intro x
    have hBx : B x = B (x-P x) := by
      have h : B (P x)=0 := congrArg (fun T : E →L[𝕜] E => T x) hBP
      simp only [map_sub, h, sub_zero]
    have hBsx : (star B) x = (star B) (P x) :=
      (congrArg (fun T : E →L[𝕜] E => T x) hBsP).symm
    have h1 := ContinuousLinearMap.le_opNorm B (x-P x)
    have h2 := ContinuousLinearMap.le_opNorm (star B) (P x)
    rw [_root_.norm_star B] at h2
    have h1sq : ‖B (x-P x)‖^2 ≤ ‖B‖^2 * ‖x-P x‖^2 := by
      nlinarith [norm_nonneg (B (x-P x)), mul_nonneg (norm_nonneg B) (norm_nonneg (x-P x))]
    have h2sq : ‖(star B) (P x)‖^2 ≤ ‖B‖^2 * ‖P x‖^2 := by
      nlinarith [norm_nonneg ((star B) (P x)), mul_nonneg (norm_nonneg B) (norm_nonneg (P x))]
    have hd := orthogonal_projection_decomposition P hP hPs x
    have hn := hnorm x
    rw [hBx, hBsx] at hn
    have hd' := congrArg (fun t : ℝ => ‖B‖^2*t) hd
    have hs : ‖(B-star B) x‖^2 ≤ (‖B‖*‖x‖)^2 := by
      nlinarith [hd']
    nlinarith [norm_nonneg ((B-star B) x), mul_nonneg (norm_nonneg B) (norm_nonneg x)]
  · apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _)
    intro x
    have hn := hnorm x
    have hc := ContinuousLinearMap.le_opNorm (B-star B) x
    have hb : ‖B x‖ ≤ ‖(B-star B) x‖ := by
      nlinarith [sq_nonneg ‖(star B) x‖, norm_nonneg (B x), norm_nonneg ((B-star B) x)]
    exact hb.trans hc

theorem projection_commutator_norm_sq
    (P Q : E →L[𝕜] E) (hP : P*P=P) (hQ : Q*Q=Q)
    (hPs : star P=P) (hQs : star Q=Q) :
    ‖P*Q-Q*P‖^2 = ‖P*Q*P-(P*Q*P)^2‖ := by
  let B := P*Q-P*Q*P
  have hPB : P*B=B := by
    dsimp [B]
    simp only [mul_sub, ← mul_assoc, hP]
  have hBP : B*P=0 := by
    dsimp [B]
    simp only [sub_mul, mul_assoc, hP, sub_self]
  have hBs : star B=Q*P-P*Q*P := by
    dsimp [B]
    simp only [star_sub, star_mul, hPs, hQs, mul_assoc]
  have hcomm : B-star B=P*Q-Q*P := by
    rw [hBs]
    dsimp [B]
    abel
  have hprod : B*star B=P*Q*P-(P*Q*P)^2 := by
    have hp (X : E →L[𝕜] E) : P*(P*X)=P*X := by rw [← mul_assoc, hP]
    have hq (X : E →L[𝕜] E) : Q*(Q*X)=Q*X := by rw [← mul_assoc, hQ]
    rw [hBs]
    dsimp [B]
    simp only [sub_mul, mul_sub, pow_two, mul_assoc, hp, hq]
    abel
  have hn := offDiagonal_norm P B hP hPs hPB hBP
  rw [hcomm] at hn
  rw [hn, ← hprod, CStarRing.norm_self_mul_star (x := B), pow_two]

#print axioms orthogonal_projection_decomposition
#print axioms offDiagonal_norm
#print axioms projection_commutator_norm_sq

end HMT.I.ProjectionNorm
