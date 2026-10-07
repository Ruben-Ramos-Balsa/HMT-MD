import ProjectionCommutatorNorm

set_option maxHeartbeats 400000

namespace HMT.I.ProjectionNorm

open ContinuousLinearMap

variable {𝕜 E F : Type*} [RCLike 𝕜]
  [NormedAddCommGroup E] [InnerProductSpace 𝕜 E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace 𝕜 F] [CompleteSpace F]

theorem isometry_column_norm_le (U : F →L[𝕜] E) (hU : (adjoint U).comp U=1) :
    ‖U‖ ≤ 1 := by
  have h := norm_adjoint_comp_self U
  rw [hU] at h
  have hi : ‖(1 : F →L[𝕜] F)‖ ≤ 1 := norm_id_le
  nlinarith [norm_nonneg U]

theorem norm_comp_three_le {A B C D : Type*}
    [NormedAddCommGroup A] [NormedSpace 𝕜 A]
    [NormedAddCommGroup B] [NormedSpace 𝕜 B]
    [NormedAddCommGroup C] [NormedSpace 𝕜 C]
    [NormedAddCommGroup D] [NormedSpace 𝕜 D]
    (L : C →L[𝕜] D) (T : B →L[𝕜] C) (R : A →L[𝕜] B)
    (hL : ‖L‖ ≤ 1) (hR : ‖R‖ ≤ 1) : ‖(L.comp T).comp R‖ ≤ ‖T‖ := by
  calc
    ‖(L.comp T).comp R‖ ≤ ‖L.comp T‖ * ‖R‖ := opNorm_comp_le _ _
    _ ≤ (‖L‖*‖T‖)*‖R‖ := mul_le_mul_of_nonneg_right (opNorm_comp_le _ _) (norm_nonneg _)
    _ ≤ (1*‖T‖)*1 := mul_le_mul
      (mul_le_mul_of_nonneg_right hL (norm_nonneg T)) hR
      (norm_nonneg R) (mul_nonneg zero_le_one (norm_nonneg T))
    _ = ‖T‖ := by ring

theorem isometry_conjugation_norm (U : F →L[𝕜] E)
    (hU : (adjoint U).comp U=1) (M : F →L[𝕜] F) :
    ‖(U.comp M).comp (adjoint U)‖ = ‖M‖ := by
  have hu : ‖U‖ ≤ 1 := isometry_column_norm_le U hU
  have hus : ‖adjoint U‖ ≤ 1 := (adjoint.norm_map U).le.trans hu
  apply le_antisymm (norm_comp_three_le U M (adjoint U) hu hus)
  have he : ((adjoint U).comp ((U.comp M).comp (adjoint U))).comp U = M := by
    have hx (x : F) : (adjoint U) (U x)=x := congrArg (fun T : F →L[𝕜] F => T x) hU
    ext x
    change (adjoint U) (U (M ((adjoint U) (U x)))) = M x
    rw [hx, hx]
  have hb := norm_comp_three_le (adjoint U) ((U.comp M).comp (adjoint U)) U hus hu
  rwa [he] at hb

theorem projection_commutator_compressed_norm_sq
    (U : F →L[𝕜] E) (hU : (adjoint U).comp U=1)
    (Q : E →L[𝕜] E) (hQ : Q*Q=Q) (hQs : star Q=Q) :
    let P := U.comp (adjoint U)
    let M := ((adjoint U).comp Q).comp U
    ‖P*Q-Q*P‖^2 = ‖M-M^2‖ := by
  dsimp only
  let P := U.comp (adjoint U)
  let M := ((adjoint U).comp Q).comp U
  have hx (x : F) : (adjoint U) (U x)=x := congrArg (fun T : F →L[𝕜] F => T x) hU
  have hP : P*P=P := by
    ext x
    simp only [P, mul_apply, comp_apply, hx]
  have hPs : star P=P := by
    change adjoint (U.comp (adjoint U))=U.comp (adjoint U)
    rw [adjoint_comp, adjoint_adjoint]
  have he : P*Q*P-(P*Q*P)^2 = (U.comp (M-M^2)).comp (adjoint U) := by
    ext x
    simp only [P, M, sub_apply, mul_apply, comp_apply, pow_two, map_sub, hx]
  change ‖P*Q-Q*P‖^2 = ‖M-M^2‖
  rw [projection_commutator_norm_sq P Q hP hQ hPs hQs, he]
  exact isometry_conjugation_norm U hU (M-M^2)

#print axioms isometry_column_norm_le
#print axioms norm_comp_three_le
#print axioms isometry_conjugation_norm
#print axioms projection_commutator_compressed_norm_sq

end HMT.I.ProjectionNorm
