import LatticeShells
import ExponentialShellTail

/-!
# Summability and outer tails on the actual integer lattice

The partition by `supRadius` is proved from the finite shells. Positive-energy
values are cut off at the zero lattice point before any infinite sum is formed.
-/

noncomputable section
open Set Real Filter
open scoped BigOperators

namespace HMT.V.ThermodynamicLimit

set_option maxHeartbeats 800000

theorem shells_partition (nu : Lattice) :
    ∃! m : ℕ, nu ∈ (shell m : Set Lattice) := by
  refine ⟨supRadius nu, mem_shell.mpr rfl, ?_⟩
  intro m hm
  exact (mem_shell.mp hm).symm

theorem lattice_summable_iff_shells {g : Lattice → ℝ} (hg : ∀ nu, 0 ≤ g nu) :
    Summable g ↔ Summable (fun m : ℕ => ∑ nu ∈ shell m, g nu) := by
  have h := summable_partition hg shells_partition
  constructor
  · intro hs
    simpa only [tsum_fintype, Finset.sum_finset_coe] using (h.mp hs).2
  · intro hs
    apply h.mpr
    constructor
    · intro m
      exact (hasSum_fintype (fun nu : (shell m : Set Lattice) => g nu)).summable
    · simpa only [tsum_fintype, Finset.sum_finset_coe] using hs

theorem lattice_tsum_eq_shells {g : Lattice → ℝ} (hg : Summable g) :
    (∑' nu : Lattice, g nu) = ∑' m : ℕ, ∑ nu ∈ shell m, g nu := by
  let e := Set.sigmaEquiv (fun m : ℕ => (shell m : Set Lattice)) shells_partition
  have hs := e.summable_iff.mpr hg
  calc
    _ = ∑' p : Σ m : ℕ, (shell m : Set Lattice), g (e p) := (e.tsum_eq g).symm
    _ = ∑' m : ℕ, ∑' nu : (shell m : Set Lattice), g nu := hs.tsum_sigma
    _ = _ := by simp only [tsum_fintype, Finset.sum_finset_coe]

theorem lattice_summable_of_shell_majorant {g : Lattice → ℝ} {b : ℕ → ℝ}
    (hg : ∀ nu, 0 ≤ g nu) (hb : Summable b)
    (hbound : ∀ n, (∑ nu ∈ shell (n + 1), g nu) ≤ b n) : Summable g := by
  apply (lattice_summable_iff_shells hg).mpr
  apply (summable_nat_add_iff 1).mp
  exact Summable.of_nonneg_of_le (fun n => Finset.sum_nonneg (fun nu _ => hg nu)) hbound hb

theorem shell_zero_sum (g : Lattice → ℝ) : (∑ nu ∈ shell 0, g nu) = g 0 := by
  rw [shell_zero, Finset.sum_singleton]

theorem sequence_tsum_le_of_zero {a b : ℕ → ℝ} (ha : Summable a)
    (ha0 : a 0 = 0) (hb : Summable b) (hab : ∀ n, a (n + 1) ≤ b n) :
    (∑' n, a n) ≤ ∑' n, b n := by
  have hshift : Summable (fun n : ℕ => a (n + 1)) := (summable_nat_add_iff 1).mpr ha
  calc
    _ = a 0 + (∑' n : ℕ, a (n + 1)) := ha.tsum_eq_zero_add
    _ = ∑' n : ℕ, a (n + 1) := by rw [ha0, zero_add]
    _ ≤ _ := hshift.tsum_le_tsum hab hb

theorem lattice_tsum_le_shell_majorant {g : Lattice → ℝ} {b : ℕ → ℝ}
    (hg : ∀ nu, 0 ≤ g nu) (hzero : g 0 = 0) (hb : Summable b)
    (hbound : ∀ n, (∑ nu ∈ shell (n + 1), g nu) ≤ b n) :
    (∑' nu : Lattice, g nu) ≤ ∑' n : ℕ, b n := by
  have hs := lattice_summable_of_shell_majorant hg hb hbound
  have hss := (lattice_summable_iff_shells hg).mp hs
  calc
    _ = ∑' m : ℕ, ∑ nu ∈ shell m, g nu := lattice_tsum_eq_shells hs
    _ ≤ _ := sequence_tsum_le_of_zero hss ((shell_zero_sum g).trans hzero) hb hbound

/-- A pointwise radial exponential dominates the whole finite shell. -/
theorem shell_sum_le_exponential {g : Lattice → ℝ} {C c delta : ℝ}
    (hC : 0 ≤ C) (hc : 0 < c) (hdelta : 0 < delta) (n : ℕ)
    (hg : ∀ nu ∈ shell (n + 1), g nu ≤ C * Real.exp (-(c * delta * radius nu))) :
    (∑ nu ∈ shell (n + 1), g nu) ≤
      C * (shellWeight n * Real.exp (-(c * delta * (n + 1 : ℝ)))) := by
  have hpoint (nu : Lattice) (hnu : nu ∈ shell (n + 1)) :
      g nu ≤ C * Real.exp (-(c * delta * (n + 1 : ℝ))) := by
    apply (hg nu hnu).trans
    apply mul_le_mul_of_nonneg_left _ hC
    apply Real.exp_le_exp.mpr
    have hrad := (shell_radius_bounds hnu).1
    push_cast at hrad
    nlinarith [mul_le_mul_of_nonneg_left hrad (mul_pos hc hdelta).le]
  calc
    _ ≤ ∑ _nu ∈ shell (n + 1), C * Real.exp (-(c * delta * (n + 1 : ℝ))) :=
      Finset.sum_le_sum hpoint
    _ = _ := by
      simp only [Finset.sum_const, nsmul_eq_mul, card_shell_succ, Nat.cast_add,
        Nat.cast_mul, Nat.cast_pow, Nat.cast_ofNat, Nat.cast_one, shellWeight]
      ring

def excitationValue (F : ℝ → ℝ) (delta : ℝ) (nu : Lattice) : ℝ :=
  if nu = 0 then 0 else F (delta * radius nu)

theorem excitationValue_zero (F : ℝ → ℝ) (delta : ℝ) : excitationValue F delta 0 = 0 := by
  simp [excitationValue]

theorem excitationValue_nonneg {F : ℝ → ℝ} {delta : ℝ} (hdelta : 0 < delta)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r) (nu : Lattice) : 0 ≤ excitationValue F delta nu := by
  unfold excitationValue
  split_ifs with hnu
  · rfl
  · exact hF _ (mul_pos hdelta ((radius_pos_iff nu).mpr hnu))

/-- First interface: a fixed-mesh global envelope on positive excitations. -/
theorem excitation_summable_of_global_exponential {F : ℝ → ℝ} {M d delta : ℝ}
    (hM : 0 ≤ M) (hd : 0 < d) (hdelta : 0 < delta)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hbound : ∀ nu : Lattice, nu ≠ 0 →
      F (delta * radius nu) ≤ M * Real.exp (-(d * delta * radius nu))) :
    Summable (excitationValue F delta) := by
  apply lattice_summable_of_shell_majorant (excitationValue_nonneg hdelta hF)
    ((exponential_shell_summable hd hdelta).mul_left M)
  intro n
  apply shell_sum_le_exponential hM hd hdelta n
  intro nu hnu
  have hn : nu ≠ 0 := shell_nonzero (by omega) hnu
  simpa only [excitationValue, if_neg hn] using hbound nu hn

def latticeTailValue (F : ℝ → ℝ) (delta R : ℝ) (nu : Lattice) : ℝ :=
  if R < delta * radius nu then excitationValue F delta nu else 0

theorem latticeTailValue_nonneg {F : ℝ → ℝ} {delta : ℝ} (hdelta : 0 < delta)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r) (R : ℝ) (nu : Lattice) :
    0 ≤ latticeTailValue F delta R nu := by
  unfold latticeTailValue
  split_ifs
  · exact excitationValue_nonneg hdelta hF nu
  · rfl

/-- The Euclidean cutoff implies the strict shell cutoff from the source. -/
theorem shell_tail_threshold {delta R : ℝ} (hdelta : 0 < delta)
    {n : ℕ} {nu : Lattice} (hnu : nu ∈ shell (n + 1))
    (hR : R < delta * radius nu) : R / (Real.sqrt 3 * delta) < (n + 1 : ℝ) := by
  have hs : 0 < Real.sqrt (3 : ℝ) := Real.sqrt_pos.mpr (by norm_num)
  apply (div_lt_iff₀ (mul_pos hs hdelta)).mpr
  have h := (shell_radius_bounds hnu).2
  push_cast at h
  nlinarith [mul_le_mul_of_nonneg_left h hdelta.le]

theorem shell_lattice_tail_le {F : ℝ → ℝ} {C d delta R : ℝ}
    (hC : 0 ≤ C) (hd : 0 < d) (hdelta : 0 < delta) (hR : 1 ≤ R)
    (hbound : ∀ r : ℝ, 1 ≤ r → F r ≤ C * Real.exp (-(d * r))) (n : ℕ) :
    (∑ nu ∈ shell (n + 1), latticeTailValue F delta R nu) ≤
      C * exponentialShellTailTerm d delta R n := by
  unfold exponentialShellTailTerm
  split_ifs with hn
  · apply shell_sum_le_exponential hC hd hdelta n
    intro nu hnu
    unfold latticeTailValue
    split_ifs with hout
    · have hne : nu ≠ 0 := shell_nonzero (by omega) hnu
      rw [excitationValue, if_neg hne]
      simpa only [mul_assoc] using hbound (delta * radius nu) (le_trans hR hout.le)
    · exact mul_nonneg hC (Real.exp_pos _).le
  · have hzero : ∀ nu ∈ shell (n + 1), latticeTailValue F delta R nu = 0 := by
      intro nu hnu
      unfold latticeTailValue
      rw [if_neg (fun hout => hn (shell_tail_threshold hdelta hnu hout))]
    simp only [mul_zero]
    exact le_of_eq (Finset.sum_eq_zero hzero)

theorem lattice_tail_summable {F : ℝ → ℝ} {C d delta R : ℝ}
    (hC : 0 ≤ C) (hd : 0 < d) (hdelta : 0 < delta) (hR : 1 ≤ R)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hbound : ∀ r : ℝ, 1 ≤ r → F r ≤ C * Real.exp (-(d * r))) :
    Summable (latticeTailValue F delta R) :=
  lattice_summable_of_shell_majorant (latticeTailValue_nonneg hdelta hF R)
    ((exponential_tail_summable hd hdelta).mul_left C)
    (shell_lattice_tail_le hC hd hdelta hR hbound)

/-- For each fixed positive mesh, the bounded inner region contains finitely many lattice points.
No continuity or local bound is needed to absorb these finitely many real-valued terms. -/
theorem excitation_summable {F : ℝ → ℝ} {C d delta : ℝ}
    (hC : 0 ≤ C) (hd : 0 < d) (hdelta : 0 < delta)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hbound : ∀ r : ℝ, 1 ≤ r → F r ≤ C * Real.exp (-(d * r))) :
    Summable (excitationValue F delta) := by
  apply (lattice_tail_summable hC hd hdelta (R := 1) le_rfl hF hbound).congr_cofinite
  filter_upwards [(cube ⌈1 / delta⌉₊).finite_toSet.compl_mem_cofinite] with nu hnu
  have hout : 1 < delta * radius nu := by
    by_contra h
    have hr : radius nu ≤ 1 / delta := by
      apply (le_div_iff₀ hdelta).mpr
      simpa only [mul_comm] using le_of_not_gt h
    have hs : (supRadius nu : ℝ) ≤ (⌈1 / delta⌉₊ : ℕ) :=
      (supRadius_le_radius nu).trans (hr.trans (Nat.le_ceil _))
    have hmem : nu ∈ cube ⌈1 / delta⌉₊ := mem_cube.mpr (by exact_mod_cast hs)
    exact hnu hmem
  simp only [latticeTailValue, if_pos hout]

/-- The same convergence on the explicit nonzero subtype used in the source. -/
theorem excitation_subtype_summable {F : ℝ → ℝ} {C d delta : ℝ}
    (hC : 0 ≤ C) (hd : 0 < d) (hdelta : 0 < delta)
    (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hbound : ∀ r : ℝ, 1 ≤ r → F r ≤ C * Real.exp (-(d * r))) :
    Summable (fun nu : {nu : Lattice // nu ≠ 0} => F (delta * radius nu)) := by
  have hs := (excitation_summable hC hd hdelta hF hbound).subtype (fun nu => nu ≠ 0)
  apply hs.congr
  intro nu
  exact if_neg nu.property

/-- The tail is a genuine `tsum` on ℤ³, not a shell sum supplied as data. -/
theorem lattice_tail_uniform {F : ℝ → ℝ} {C d delta R : ℝ}
    (hC : 0 ≤ C) (hd : 0 < d) (hdelta : 0 < delta) (hdelta1 : delta ≤ 1)
    (hR : 1 ≤ R) (hF : ∀ r : ℝ, 0 < r → 0 ≤ F r)
    (hbound : ∀ r : ℝ, 1 ≤ r → F r ≤ C * Real.exp (-(d * r))) :
    delta ^ 3 * (∑' nu : Lattice, latticeTailValue F delta R nu) ≤
      C * shellUniformConstant (d / 2) * Real.exp (-d * R / (2 * Real.sqrt 3)) := by
  have hzero : latticeTailValue F delta R 0 = 0 := by simp [latticeTailValue, excitationValue]
  have h := lattice_tsum_le_shell_majorant (latticeTailValue_nonneg hdelta hF R) hzero
    ((exponential_tail_summable hd hdelta).mul_left C)
    (shell_lattice_tail_le hC hd hdelta hR hbound)
  rw [tsum_mul_left] at h
  change (∑' nu, latticeTailValue F delta R nu) ≤ C * exponentialShellTail d delta R at h
  calc
    _ ≤ delta ^ 3 * (C * exponentialShellTail d delta R) :=
      mul_le_mul_of_nonneg_left h (pow_nonneg hdelta.le _)
    _ = C * (delta ^ 3 * exponentialShellTail d delta R) := by ring
    _ ≤ C * (shellUniformConstant (d / 2) * Real.exp (-d * R / (2 * Real.sqrt 3))) :=
      mul_le_mul_of_nonneg_left (exponential_tail_uniform hd hdelta hdelta1) hC
    _ = _ := by ring

#print axioms lattice_summable_iff_shells
#print axioms lattice_tsum_eq_shells
#print axioms excitation_summable_of_global_exponential
#print axioms shell_tail_threshold
#print axioms lattice_tail_summable
#print axioms excitation_summable
#print axioms excitation_subtype_summable
#print axioms lattice_tail_uniform

end HMT.V.ThermodynamicLimit
