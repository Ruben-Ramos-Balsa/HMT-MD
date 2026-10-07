import Mathlib

/-! Finite tensor carrier of article II. The domain consists of actual
3 by 3 symmetric trace-free matrices. Five coordinates are introduced only
through an explicit matrix chart and its inverse. -/

namespace HMT.ArticleII.PentadicTensor

open scoped BigOperators Matrix
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option linter.unnecessarySeqFocus false
set_option linter.unreachableTactic false
set_option linter.unusedTactic false
noncomputable section

def antipode : Fin 12 → Fin 12 := ![3,2,1,0,7,6,5,4,11,10,9,8]
def signedPosition : Fin 12 → Fin 6 := ![0,1,1,0,2,4,4,2,3,5,5,3]
def orientation : Fin 12 → ℚ := ![1,-1,1,-1,-1,1,-1,1,-1,1,-1,1]

theorem antipode_involution : ∀ p, antipode (antipode p) = p := by decide +kernel
theorem antipode_fixed_free : ∀ p, antipode p ≠ p := by decide +kernel
theorem signed_table_antipodal : ∀ p,
    signedPosition (antipode p) = signedPosition p ∧
    orientation (antipode p) = -orientation p := by decide +kernel

def clock (b : Fin 12) (r : Fin 9) (n : ℕ) : Fin 12 × Fin 9 :=
  (⟨(b.val + (r.val+n)/9)%12, Nat.mod_lt _ (by decide)⟩,
   ⟨(r.val+n)%9, Nat.mod_lt _ (by decide)⟩)

theorem clock_nine : ∀ b r,
    clock b r 9 = (⟨(b.val+1)%12, Nat.mod_lt _ (by decide)⟩,r) := by
  decide +kernel

theorem clock_108 : ∀ b r, clock b r 108 = (b,r) := by decide +kernel

theorem carry_composition (r n m : ℕ) :
    (r+n+m)/9 = (r+n)/9 + ((r+n)%9+m)/9 := by omega

def P5 : Matrix (Fin 12) (Fin 12) ℚ := fun p q =>
  (if p=q then 1/2 else 0) + (if p=antipode q then 1/2 else 0) - 1/12

theorem P5_symmetric : P5.transpose = P5 := by decide +kernel
theorem P5_idempotent : P5 * P5 = P5 := by decide +kernel
theorem P5_trace : Matrix.trace P5 = 5 := by decide +kernel
theorem P5_constant_kernel : P5.mulVec (fun _ => 1) = 0 := by decide +kernel
theorem P5_antipodal_rows : ∀ p q, P5 (antipode p) q = P5 p q := by
  decide +kernel

abbrev Mat3 := Matrix (Fin 3) (Fin 3) ℝ
def IsSTF (Q : Mat3) : Prop := Q.transpose = Q ∧ Matrix.trace Q = 0
abbrev STF := { Q : Mat3 // IsSTF Q }

def tensorChart (a b c d e : ℝ) : Mat3 :=
  !![a,b,c; b,d,e; c,e,-a-d]

theorem tensorChart_STF (a b c d e : ℝ) : IsSTF (tensorChart a b c d e) := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;> simp [tensorChart, Matrix.transpose_apply]
  · simp [Matrix.trace, Fin.sum_univ_succ, tensorChart]

theorem STF_chart_exhaustive (Q : Mat3) (h : IsSTF Q) :
    Q = tensorChart (Q 0 0) (Q 0 1) (Q 0 2) (Q 1 1) (Q 1 2) := by
  have hs (i j : Fin 3) : Q j i = Q i j := congrFun (congrFun h.1 i) j
  have ht : Q 0 0 + Q 1 1 + Q 2 2 = 0 := by
    simpa [Matrix.trace, Fin.sum_univ_succ, add_assoc] using h.2
  ext i j
  fin_cases i <;> fin_cases j <;> simp [tensorChart]
  · exact hs 0 1
  · exact hs 0 2
  · exact hs 1 2
  · linarith

def frobenius (Q R : Mat3) : ℝ := ∑ i, ∑ j, Q i j * R i j

def transverse (Q : Mat3) : Mat3 :=
  tensorChart ((Q 0 0-Q 1 1)/2) ((Q 0 1+Q 1 0)/2) 0
    ((Q 1 1-Q 0 0)/2) 0

theorem transverse_STF (Q : Mat3) : IsSTF (transverse Q) :=
  tensorChart_STF _ _ _ _ _

theorem transverse_idempotent (Q : Mat3) : transverse (transverse Q) = transverse Q := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [transverse,tensorChart] <;> ring

theorem transverse_axis_kernel (Q : Mat3) : ∀ i, transverse Q i 2 = 0 := by
  intro i
  fin_cases i <;> simp [transverse,tensorChart] <;> ring

theorem transverse_self_adjoint (Q R : Mat3) :
    frobenius (transverse Q) R = frobenius Q (transverse R) := by
  simp [frobenius, Fin.sum_univ_succ, transverse, tensorChart]
  ring

theorem transverse_on_chart (a b c d e : ℝ) :
    transverse (tensorChart a b c d e) =
    tensorChart ((a-d)/2) b 0 ((d-a)/2) 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [transverse,tensorChart] <;> ring

theorem transverse_image_exact (Q : Mat3) :
    (∃ R, transverse R = Q) ↔ ∃ a b, Q = tensorChart a b 0 (-a) 0 := by
  constructor
  · rintro ⟨R,rfl⟩
    refine ⟨(R 0 0-R 1 1)/2,(R 0 1+R 1 0)/2,?_⟩
    ext i j
    fin_cases i <;> fin_cases j <;> simp [transverse,tensorChart] <;> ring
  · rintro ⟨a,b,rfl⟩
    refine ⟨tensorChart a b 0 (-a) 0,?_⟩
    rw [transverse_on_chart]
    congr 1 <;> ring

def rawVertex (t : ℝ) : Fin 6 → Fin 3 → ℝ :=
  ![![0,-1,-t],![-1,-t,0],![-t,0,-1],![0,1,-t],![t,0,-1],![1,-t,0]]

def Qsix (t : ℝ) (u : Fin 6) : Mat3 := fun i j =>
  rawVertex t u i * rawVertex t u j / (t+2) - if i=j then 1/3 else 0

def Qposition (t : ℝ) (p : Fin 12) : Mat3 := Qsix t (signedPosition p)

theorem Qposition_antipodal (t : ℝ) (p : Fin 12) :
    Qposition t (antipode p) = Qposition t p := by
  simp only [Qposition, (signed_table_antipodal p).1]

theorem Qsix_STF (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0) (u : Fin 6) :
    IsSTF (Qsix t u) := by
  constructor
  · ext i j
    simp only [Matrix.transpose_apply, Qsix]
    rw [mul_comm]
    congr 1
    simp [eq_comm]
  · fin_cases u <;> simp [Matrix.trace,Fin.sum_univ_succ,Qsix,rawVertex]
      <;> field_simp [hd] <;> nlinarith [ht]

def Qclosed (t : ℝ) : Fin 6 → Mat3 :=
  let a := (4-3*t)/15
  let b := (2*t-1)/5
  let c := (3*t+1)/15
  ![!![-1/3,0,0; 0,a,b; 0,b,c],
    !![a,b,0; b,c,0; 0,0,-1/3],
    !![c,0,b; 0,-1/3,0; b,0,a],
    !![-1/3,0,0; 0,a,-b; 0,-b,c],
    !![c,0,-b; 0,-1/3,0; -b,0,a],
    !![a,-b,0; -b,c,0; 0,0,-1/3]]

theorem Qsix_eq_closed (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0) :
    Qsix t = Qclosed t := by
  funext u i j
  fin_cases u <;> fin_cases i <;> fin_cases j <;>
    simp [Qsix,rawVertex,Qclosed] <;> field_simp [hd] <;> nlinarith [ht]

theorem Qsix_gram (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0) :
    ∀ u v, frobenius (Qsix t u) (Qsix t v) =
       if u=v then 2/3 else -2/15 := by
  intro u v
  rw [Qsix_eq_closed t ht hd]
  fin_cases u <;> fin_cases v <;>
    simp [frobenius,Fin.sum_univ_succ,Qclosed] <;>
    nlinarith [ht]

theorem position_tensor_gram (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (p q : Fin 12) :
    frobenius (Qposition t p) (Qposition t q) = (8/5:ℝ) * (P5 p q : ℝ) := by
  unfold Qposition
  rw [Qsix_gram t ht hd]
  have h : ∀ p q, (if signedPosition p = signedPosition q then (2/3:ℚ) else -2/15)
      = (8/5:ℚ) * P5 p q := by decide +kernel
  have hh := congrArg (fun z : ℚ => (z : ℝ)) (h p q)
  push_cast at hh
  by_cases he : signedPosition p = signedPosition q <;> simpa [he] using hh

def Gamma0 (t : ℝ) (x : Fin 12 → ℝ) : Mat3 :=
  fun i j => ∑ p, x p * Qposition t p i j

def Gamma0Adj (t : ℝ) (Q : Mat3) : Fin 12 → ℝ :=
  fun p => frobenius (Qposition t p) Q

theorem Gamma0_tight_frame (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (Q : Mat3) (hQ : IsSTF Q) :
    Gamma0 t (Gamma0Adj t Q) = (8/5:ℝ) • Q := by
  rw [STF_chart_exhaustive Q hQ]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Gamma0,Gamma0Adj,Qposition,Qsix_eq_closed t ht hd,
      signedPosition,frobenius,Fin.sum_univ_succ,Qclosed,tensorChart] <;>
    ring_nf <;> simp only [ht] <;> ring

def Gamma5 (t : ℝ) (x : Fin 12 → ℝ) : Mat3 :=
  Real.sqrt (5/8) • Gamma0 t x

def Gamma5Adj (t : ℝ) (Q : Mat3) : Fin 12 → ℝ :=
  fun p => Real.sqrt (5/8) * Gamma0Adj t Q p

theorem Gamma0_smul (t c : ℝ) (x : Fin 12 → ℝ) :
    Gamma0 t (fun p => c * x p) = c • Gamma0 t x := by
  ext i j
  simp [Gamma0, Finset.mul_sum, mul_assoc]

theorem frobenius_Gamma0 (t : ℝ) (Q : Mat3) (x : Fin 12 → ℝ) :
    frobenius Q (Gamma0 t x) = ∑ p, x p * frobenius Q (Qposition t p) := by
  unfold frobenius Gamma0
  simp only [Finset.mul_sum]
  calc
    (∑ i, ∑ j, ∑ p, Q i j * (x p * Qposition t p i j)) =
        ∑ i, ∑ p, ∑ j, Q i j * (x p * Qposition t p i j) := by
      apply Finset.sum_congr rfl
      intro i _
      exact Finset.sum_comm
    _ = ∑ p, ∑ i, ∑ j, Q i j * (x p * Qposition t p i j) := Finset.sum_comm
    _ = ∑ p, ∑ i, ∑ j, x p * (Q i j * Qposition t p i j) := by
      apply Finset.sum_congr rfl
      intro p _
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      ring

theorem Gamma0_left_gram (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (x : Fin 12 → ℝ) (p : Fin 12) :
    Gamma0Adj t (Gamma0 t x) p = (8/5:ℝ) * ∑ q, (P5 p q:ℝ) * x q := by
  unfold Gamma0Adj
  rw [frobenius_Gamma0]
  simp only [position_tensor_gram t ht hd]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro q _
  ring

theorem frobenius_smul_right (Q R : Mat3) (c : ℝ) :
    frobenius Q (c • R) = c * frobenius Q R := by
  simp [frobenius,Finset.mul_sum,mul_left_comm,mul_assoc]

def IsV5 (x : Fin 12 → ℝ) : Prop :=
  ∀ p, ∑ q, (P5 p q:ℝ) * x q = x p

theorem Gamma5_left_projector (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (x : Fin 12 → ℝ) (p : Fin 12) :
    Gamma5Adj t (Gamma5 t x) p = ∑ q, (P5 p q:ℝ) * x q := by
  unfold Gamma5Adj Gamma5
  simp only [Gamma0Adj,frobenius_smul_right]
  have h := Gamma0_left_gram t ht hd x p
  unfold Gamma0Adj at h
  rw [h]
  have hs : Real.sqrt (5/8) * Real.sqrt (5/8) = (5/8:ℝ) :=
    Real.mul_self_sqrt (by norm_num)
  calc
    _ = (Real.sqrt (5/8) * Real.sqrt (5/8)) * (8/5) *
        (∑ q, (P5 p q:ℝ) * x q) := by ring
    _ = _ := by rw [hs]; ring

theorem Gamma5_left_inverse_on_V5 (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (x : Fin 12 → ℝ) (hx : IsV5 x) : Gamma5Adj t (Gamma5 t x) = x := by
  funext p
  rw [Gamma5_left_projector t ht hd x p]
  exact hx p

theorem Gamma5_right_inverse (t : ℝ) (ht : t^2=t+1) (hd : t+2 ≠ 0)
    (Q : Mat3) (hQ : IsSTF Q) :
    Gamma5 t (Gamma5Adj t Q) = Q := by
  unfold Gamma5 Gamma5Adj
  rw [Gamma0_smul,Gamma0_tight_frame t ht hd Q hQ]
  have hs : Real.sqrt (5/8) * Real.sqrt (5/8) = (5/8:ℝ) := by
    exact Real.mul_self_sqrt (by norm_num)
  rw [smul_smul,smul_smul,hs]
  norm_num

def phiRealization : ℝ := (1+Real.sqrt 5)/2

theorem phiRealization_relation : phiRealization^2=phiRealization+1 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ 5 by norm_num)
  unfold phiRealization
  nlinarith

theorem phiRealization_denominator : phiRealization+2 ≠ 0 := by
  have h := Real.sqrt_nonneg (5:ℝ)
  unfold phiRealization
  linarith

theorem concrete_tensor_frame_reconstruction (Q : Mat3) (hQ : IsSTF Q) :
    Gamma5 phiRealization (Gamma5Adj phiRealization Q) = Q :=
  Gamma5_right_inverse phiRealization phiRealization_relation
    phiRealization_denominator Q hQ

#print axioms antipode_involution
#print axioms clock_108
#print axioms P5_idempotent
#print axioms STF_chart_exhaustive
#print axioms transverse_image_exact
#print axioms Qsix_gram
#print axioms position_tensor_gram
#print axioms concrete_tensor_frame_reconstruction
#print axioms Gamma5_left_inverse_on_V5

end

end HMT.ArticleII.PentadicTensor
