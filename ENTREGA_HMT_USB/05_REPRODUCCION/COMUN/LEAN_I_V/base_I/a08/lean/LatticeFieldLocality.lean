import LatticeFactorConvolution
import Mathlib.Algebra.Vertex.VertexOperator

/-!
Coefficientwise locality for genuine Laurent fields, using the same
two-variable crossing operator as the previously constructed lattice fields.
This file gives the algebraic closure under scalar multiplication and finite
addition, monotonicity of the locality order, and exchange of the two fields.
It does not assume or assert Dong's normal-product closure theorem.
-/

noncomputable section
namespace HMT.IV.LatticeFieldLocality

open HMT.IV.LatticeFactorConvolution

variable {V : Type*} [AddCommGroup V] [Module ℂ V]

def forward (A B : VertexOperator ℂ V) : BiStates (Module.End ℂ V) :=
  fun k l => HVertexOperator.coeff A k * HVertexOperator.coeff B l

def backward (A B : VertexOperator ℂ V) : BiStates (Module.End ℂ V) :=
  fun k l => HVertexOperator.coeff B l * HVertexOperator.coeff A k

def LocalAt (N : ℕ) (A B : VertexOperator ℂ V) : Prop :=
  (crossing^N) (forward A B) = (crossing^N) (backward A B)

def Local (A B : VertexOperator ℂ V) : Prop := ∃ N : ℕ, LocalAt N A B

theorem localAt_mono {m n : ℕ} {A B : VertexOperator ℂ V}
    (hmn : m ≤ n) (h : LocalAt m A B) : LocalAt n A B := by
  have hp : (crossing : Module.End ℂ (BiStates (Module.End ℂ V)))^n =
      crossing^(n-m) * crossing^m := by
    rw [← pow_add, Nat.sub_add_cancel hmn]
  unfold LocalAt at h ⊢
  rw [hp, Module.End.mul_apply, Module.End.mul_apply, h]

theorem forward_add_left (A B C : VertexOperator ℂ V) :
    forward (A+B) C = forward A C + forward B C := by
  funext k l
  simp only [forward, HVertexOperator.coeff_add, Pi.add_apply, add_mul]

theorem backward_add_left (A B C : VertexOperator ℂ V) :
    backward (A+B) C = backward A C + backward B C := by
  funext k l
  simp only [backward, HVertexOperator.coeff_add, Pi.add_apply, mul_add]

theorem forward_add_right (A B C : VertexOperator ℂ V) :
    forward A (B+C) = forward A B + forward A C := by
  funext k l
  simp only [forward, HVertexOperator.coeff_add, Pi.add_apply, mul_add]

theorem backward_add_right (A B C : VertexOperator ℂ V) :
    backward A (B+C) = backward A B + backward A C := by
  funext k l
  simp only [backward, HVertexOperator.coeff_add, Pi.add_apply, add_mul]

theorem forward_smul_left (c : ℂ) (A B : VertexOperator ℂ V) :
    forward (c • A) B = c • forward A B := by
  funext k l
  simp only [forward, HVertexOperator.coeff_smul, Pi.smul_apply, smul_mul_assoc]

theorem backward_smul_left (c : ℂ) (A B : VertexOperator ℂ V) :
    backward (c • A) B = c • backward A B := by
  funext k l
  simp only [backward, HVertexOperator.coeff_smul, Pi.smul_apply, mul_smul_comm]

theorem forward_smul_right (c : ℂ) (A B : VertexOperator ℂ V) :
    forward A (c • B) = c • forward A B := by
  funext k l
  simp only [forward, HVertexOperator.coeff_smul, Pi.smul_apply, mul_smul_comm]

theorem backward_smul_right (c : ℂ) (A B : VertexOperator ℂ V) :
    backward A (c • B) = c • backward A B := by
  funext k l
  simp only [backward, HVertexOperator.coeff_smul, Pi.smul_apply, smul_mul_assoc]

theorem localAt_add_left {N : ℕ} {A B C : VertexOperator ℂ V}
    (hA : LocalAt N A C) (hB : LocalAt N B C) : LocalAt N (A+B) C := by
  unfold LocalAt at hA hB ⊢
  rw [forward_add_left, backward_add_left, map_add, map_add, hA, hB]

theorem localAt_add_right {N : ℕ} {A B C : VertexOperator ℂ V}
    (hB : LocalAt N A B) (hC : LocalAt N A C) : LocalAt N A (B+C) := by
  unfold LocalAt at hB hC ⊢
  rw [forward_add_right, backward_add_right, map_add, map_add, hB, hC]

theorem localAt_smul_left {N : ℕ} {A B : VertexOperator ℂ V}
    (c : ℂ) (h : LocalAt N A B) : LocalAt N (c • A) B := by
  unfold LocalAt at h ⊢
  rw [forward_smul_left, backward_smul_left, map_smul, map_smul, h]

theorem localAt_smul_right {N : ℕ} {A B : VertexOperator ℂ V}
    (c : ℂ) (h : LocalAt N A B) : LocalAt N A (c • B) := by
  unfold LocalAt at h ⊢
  rw [forward_smul_right, backward_smul_right, map_smul, map_smul, h]

theorem local_add_left {A B C : VertexOperator ℂ V}
    (hA : Local A C) (hB : Local B C) : Local (A+B) C := by
  obtain ⟨m,hm⟩ := hA
  obtain ⟨n,hn⟩ := hB
  exact ⟨max m n, localAt_add_left (localAt_mono (le_max_left _ _) hm)
    (localAt_mono (le_max_right _ _) hn)⟩

theorem local_add_right {A B C : VertexOperator ℂ V}
    (hB : Local A B) (hC : Local A C) : Local A (B+C) := by
  obtain ⟨m,hm⟩ := hB
  obtain ⟨n,hn⟩ := hC
  exact ⟨max m n, localAt_add_right (localAt_mono (le_max_left _ _) hm)
    (localAt_mono (le_max_right _ _) hn)⟩

theorem local_smul_left {A B : VertexOperator ℂ V}
    (c : ℂ) (h : Local A B) : Local (c • A) B := by
  obtain ⟨N,hN⟩ := h
  exact ⟨N,localAt_smul_left c hN⟩

theorem local_smul_right {A B : VertexOperator ℂ V}
    (c : ℂ) (h : Local A B) : Local A (c • B) := by
  obtain ⟨N,hN⟩ := h
  exact ⟨N,localAt_smul_right c hN⟩

theorem local_zero_left (B : VertexOperator ℂ V) : Local 0 B := by
  refine ⟨0, ?_⟩
  unfold LocalAt
  simp only [pow_zero, Module.End.one_apply]
  funext k l
  have hz : HVertexOperator.coeff (0 : VertexOperator ℂ V) k = 0 := by
    apply LinearMap.ext
    intro v
    rfl
  simp only [forward, backward, hz, zero_mul, mul_zero]

theorem local_zero_right (A : VertexOperator ℂ V) : Local A 0 := by
  refine ⟨0, ?_⟩
  unfold LocalAt
  simp only [pow_zero, Module.End.one_apply]
  funext k l
  have hz : HVertexOperator.coeff (0 : VertexOperator ℂ V) l = 0 := by
    apply LinearMap.ext
    intro v
    rfl
  simp only [forward, backward, hz, zero_mul, mul_zero]

theorem crossing_pow_succ_apply {W : Type*} [AddCommGroup W] [Module ℂ W]
    (f : BiStates W) (N : ℕ) (k l : ℤ) :
    (crossing^(N+1)) f k l =
      (crossing^N) f (k-1) l - (crossing^N) f k (l-1) := by
  rw [pow_succ', Module.End.mul_apply]
  rfl

theorem crossing_pow_swap {W : Type*} [AddCommGroup W] [Module ℂ W]
    (f : BiStates W) (N : ℕ) (k l : ℤ) :
    (crossing^N) (fun a b => f b a) k l =
      (-1 : ℂ)^N • (crossing^N) f l k := by
  induction N generalizing k l with
  | zero => simp
  | succ N ih =>
    rw [crossing_pow_succ_apply, ih, ih, crossing_pow_succ_apply, pow_succ,
      mul_smul, neg_one_smul, smul_neg, smul_sub]
    abel

theorem localAt_symm {N : ℕ} {A B : VertexOperator ℂ V}
    (h : LocalAt N A B) : LocalAt N B A := by
  unfold LocalAt at h ⊢
  funext k l
  change (crossing^N) (fun a b => backward A B b a) k l =
    (crossing^N) (fun a b => forward A B b a) k l
  rw [crossing_pow_swap (backward A B) N k l,
    crossing_pow_swap (forward A B) N k l, h]

theorem local_symm {A B : VertexOperator ℂ V} (h : Local A B) : Local B A := by
  obtain ⟨N,hN⟩ := h
  exact ⟨N,localAt_symm hN⟩

end HMT.IV.LatticeFieldLocality
end

#print axioms HMT.IV.LatticeFieldLocality.localAt_mono
#print axioms HMT.IV.LatticeFieldLocality.local_add_left
#print axioms HMT.IV.LatticeFieldLocality.local_add_right
#print axioms HMT.IV.LatticeFieldLocality.local_smul_left
#print axioms HMT.IV.LatticeFieldLocality.local_smul_right
#print axioms HMT.IV.LatticeFieldLocality.local_zero_left
#print axioms HMT.IV.LatticeFieldLocality.local_zero_right
#print axioms HMT.IV.LatticeFieldLocality.crossing_pow_swap
#print axioms HMT.IV.LatticeFieldLocality.localAt_symm
#print axioms HMT.IV.LatticeFieldLocality.local_symm
