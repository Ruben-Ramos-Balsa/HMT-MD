import RegionalPublicationComposition

/-!
Exact joint ternary/decimal refinement from the existing regional producer.

Source: 20_arquitectura_operatoria_tpk_actualizada.tex, the cylinder
recurrences A=N*1000^k-D*3^L, with L=6*n.  This is the cylinder component
of the enriched state, not a replacement for its transport, history or phase.
The constructors use the rational publication procedure, not target digits,
X/Y records, L0/L1, K or conventional real constants.
-/

noncomputable section
namespace HMT.I.RegionalCylinderTransition

open RegionalPublicationComposition

structure CylinderState where
  ternaryDepth : Nat
  decimalDepth : Nat
  ternaryPrefix : Nat
  decimalPrefix : Nat
  deriving DecidableEq

def lowerDefect (s : CylinderState) : Int :=
  s.ternaryPrefix * (1000 : Int)^s.decimalDepth -
    s.decimalPrefix * (729 : Int)^s.ternaryDepth

def upperDefect (s : CylinderState) : Int :=
  (s.ternaryPrefix + 1 : Int) * (1000 : Int)^s.decimalDepth -
    s.decimalPrefix * (729 : Int)^s.ternaryDepth

def Compatible (s : CylinderState) : Prop :=
  lowerDefect s < (729 : Int)^s.ternaryDepth ∧ 0 < upperDefect s

def ternaryStep (s : CylinderState) (u : Fin 729) : CylinderState :=
  ⟨s.ternaryDepth + 1, s.decimalDepth,
    729 * s.ternaryPrefix + u.val, s.decimalPrefix⟩

def jointStep (s : CylinderState) (u : Fin 729) (d : Fin 1000) : CylinderState :=
  ⟨s.ternaryDepth + 1, s.decimalDepth + 1,
    729 * s.ternaryPrefix + u.val, 1000 * s.decimalPrefix + d.val⟩

theorem upper_lower_gap (s : CylinderState) :
    upperDefect s = lowerDefect s + (1000 : Int)^s.decimalDepth := by
  simp only [upperDefect, lowerDefect]
  ring

theorem ternary_defect_update (s : CylinderState) (u : Fin 729) :
    lowerDefect (ternaryStep s u) =
      729 * lowerDefect s + u.val * (1000 : Int)^s.decimalDepth := by
  simp only [lowerDefect, ternaryStep, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat,
    pow_succ]
  ring

theorem joint_defect_update (s : CylinderState) (u : Fin 729) (d : Fin 1000) :
    lowerDefect (jointStep s u d) =
      729000 * lowerDefect s + u.val * (1000 : Int)^(s.decimalDepth + 1) -
        d.val * 729 * (729 : Int)^s.ternaryDepth := by
  simp only [lowerDefect, jointStep, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat,
    pow_succ]
  ring

def generated (c : Channel) (n k : Nat) : CylinderState :=
  ⟨n, k, publish c 729 (by decide) n, publish c 1000 (by decide) k⟩

def nextTernary (c : Channel) (n : Nat) : Fin 729 :=
  ⟨publish c 729 (by decide) (n + 1) % 729, Nat.mod_lt _ (by decide)⟩

def nextDecimal (c : Channel) (k : Nat) : Fin 1000 :=
  ⟨publish c 1000 (by decide) (k + 1) % 1000, Nat.mod_lt _ (by decide)⟩

/-- A candidate is tested against the rational enclosure reached by the proved
terminating search. No target word is part of this test. -/
def ChildAdmissible (c : Channel) (n : Nat) (u : Fin 729) : Prop :=
  let scale := 729^(n + 1)
  let j := searchDepth c scale (by positivity)
  let candidate : Int := 729 * publish c 729 (by decide) n + u.val
  RadixCellSelection.first (lower c j) scale ≤ candidate ∧
    candidate ≤ RadixCellSelection.last (upper c j) scale

private theorem search_bounds_published (c : Channel) (base : Nat)
    (hb : 0 < base) (n : Nat) :
    let scale := base^n
    let j := searchDepth c scale (pow_pos hb n)
    RadixCellSelection.first (lower c j) scale = (publish c base hb n : Int) ∧
      RadixCellSelection.last (upper c j) scale = (publish c base hb n : Int) := by
  dsimp only
  have hs := Nat.find_spec (search_terminates c (base^n) (pow_pos hb n))
  have hf : RadixCellSelection.first
      (lower c (searchDepth c (base^n) (pow_pos hb n))) (base^n) =
      (publish c base hb n : Int) := by
    rw [stopped_cell_correct c (base^n) (searchDepth c (base^n) (pow_pos hb n))
      (pow_pos hb n) hs,
      publish_eq_prefix]
    exact (RadixCellSelection.prefix_as_cell _ (value_nonnegative c) base n).symm
  exact ⟨hf, hs.symm.trans hf⟩

theorem child_admissible_iff (c : Channel) (n : Nat) (u : Fin 729) :
    ChildAdmissible c n u ↔ u = nextTernary c n := by
  obtain ⟨hf, hl⟩ := search_bounds_published c 729 (by decide) (n + 1)
  unfold ChildAdmissible
  dsimp only
  rw [hf, hl]
  have he := publication_step c 729 (by decide) n
  constructor
  · intro hu
    apply Fin.ext
    dsimp [nextTernary]
    omega
  · intro hu
    subst u
    dsimp [nextTernary]
    constructor <;> omega

theorem unique_generated_child (c : Channel) (n : Nat) :
    ∃! u : Fin 729, ChildAdmissible c n u := by
  refine ⟨nextTernary c n, (child_admissible_iff c n _).2 rfl, ?_⟩
  intro u hu
  exact (child_admissible_iff c n u).1 hu

theorem generated_ternary_step (c : Channel) (n k : Nat) :
    generated c (n + 1) k = ternaryStep (generated c n k) (nextTernary c n) := by
  exact congrArg (fun p => CylinderState.mk (n + 1) k p
    (publish c 1000 (by decide) k)) (publication_step c 729 (by decide) n)

theorem generated_joint_step (c : Channel) (n k : Nat) :
    generated c (n + 1) (k + 1) =
      jointStep (generated c n k) (nextTernary c n) (nextDecimal c k) := by
  exact congrArg₂ (fun p q => CylinderState.mk (n + 1) (k + 1) p q)
    (publication_step c 729 (by decide) n)
    (publication_step c 1000 (by decide) k)

theorem generated_truncation (c : Channel) (n k a b : Nat) :
    (generated c (n + a) (k + b)).ternaryPrefix / 729^a =
      (generated c n k).ternaryPrefix ∧
    (generated c (n + a) (k + b)).decimalPrefix / 1000^b =
      (generated c n k).decimalPrefix := by
  exact ⟨publications_compatible c 729 (by decide) n a,
    publications_compatible c 1000 (by decide) k b⟩

private theorem published_cell_bounds (c : Channel) (base n : Nat) (hb : 0 < base) :
    (publish c base hb n : ℝ) ≤ value c * (base : ℝ)^n ∧
      value c * (base : ℝ)^n < (publish c base hb n : ℝ) + 1 := by
  rw [publish_eq_prefix]
  unfold RadixCellSelection.positionalPrefix
  exact ⟨Nat.floor_le (mul_nonneg (value_nonnegative c) (by positivity)),
    Nat.lt_floor_add_one _⟩

/-- Both finite cylinders contain the same produced regional value.  The value
is used to prove compatibility, not as an input to either prefix constructor. -/
theorem generated_compatible (c : Channel) (n k : Nat) :
    Compatible (generated c n k) := by
  obtain ⟨htl, htu⟩ := published_cell_bounds c 729 n (by decide)
  obtain ⟨hdl, hdu⟩ := published_cell_bounds c 1000 k (by decide)
  norm_num only [Nat.cast_ofNat] at htl htu hdl hdu
  have ht : (0 : ℝ) < 729^n := by positivity
  have hd : (0 : ℝ) < 1000^k := by positivity
  have h1 := mul_le_mul_of_nonneg_right htl hd.le
  have h2 := mul_lt_mul_of_pos_right hdu ht
  have h3 := mul_lt_mul_of_pos_right htu hd
  have h4 := mul_le_mul_of_nonneg_right hdl ht.le
  have hA : (publish c 729 (by decide) n : ℝ) * (1000 : ℝ)^k -
      (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n < (729 : ℝ)^n := by
    nlinarith only [h1, h2]
  have hB : (0 : ℝ) < ((publish c 729 (by decide) n : ℝ) + 1) * (1000 : ℝ)^k -
      (publish c 1000 (by decide) k : ℝ) * (729 : ℝ)^n := by
    nlinarith only [h3, h4]
  constructor
  · unfold lowerDefect generated
    exact_mod_cast hA
  · unfold upperDefect generated
    exact_mod_cast hB

/-- The complete published cylinder component has a lawful next state at every
depth, with both prefixes retained and the exact mixed-radix carry update. -/
theorem generated_refinement (c : Channel) (n k : Nat) :
    let s := generated c n k
    let t := jointStep s (nextTernary c n) (nextDecimal c k)
    t = generated c (n + 1) (k + 1) ∧ Compatible t ∧
      t.ternaryPrefix / 729 = s.ternaryPrefix ∧
      t.decimalPrefix / 1000 = s.decimalPrefix ∧
      lowerDefect t = 729000 * lowerDefect s +
        (nextTernary c n).val * (1000 : Int)^(k + 1) -
        (nextDecimal c k).val * 729 * (729 : Int)^n := by
  dsimp only
  have he := generated_joint_step c n k
  refine ⟨he.symm, ?_, ?_, ?_, joint_defect_update _ _ _⟩
  · rw [← he]
    exact generated_compatible c (n + 1) (k + 1)
  · rw [← he]
    simpa using (generated_truncation c n k 1 1).1
  · rw [← he]
    simpa using (generated_truncation c n k 1 1).2

end HMT.I.RegionalCylinderTransition
end

#print axioms HMT.I.RegionalCylinderTransition.upper_lower_gap
#print axioms HMT.I.RegionalCylinderTransition.ternary_defect_update
#print axioms HMT.I.RegionalCylinderTransition.joint_defect_update
#print axioms HMT.I.RegionalCylinderTransition.child_admissible_iff
#print axioms HMT.I.RegionalCylinderTransition.unique_generated_child
#print axioms HMT.I.RegionalCylinderTransition.generated_ternary_step
#print axioms HMT.I.RegionalCylinderTransition.generated_joint_step
#print axioms HMT.I.RegionalCylinderTransition.generated_truncation
#print axioms HMT.I.RegionalCylinderTransition.generated_compatible
#print axioms HMT.I.RegionalCylinderTransition.generated_refinement
