import AnnularRiemann
import LatticeShells

noncomputable section
open Set Filter MeasureTheory
open scoped Topology Pointwise

namespace HMT.V.ThermodynamicLimit

def scaledLatticePoint (n : ℕ) (ν : Lattice) : CoordinateSpace :=
  fun i => (ν i : ℝ) / n

lemma scaledLatticePoint_injective {n : ℕ} (hn : n ≠ 0) :
    Function.Injective (scaledLatticePoint n) := by
  intro ν μ heq
  funext i
  have h := congrFun heq i
  dsimp [scaledLatticePoint] at h
  exact_mod_cast (div_left_inj' (by exact_mod_cast hn : (n : ℝ) ≠ 0)).1 h

lemma scaledLatticePoint_mem_lattice {n : ℕ} (hn : n ≠ 0) (ν : Lattice) :
    scaledLatticePoint n ν ∈ (n : ℝ)⁻¹ • (standardIntegerLattice : Set CoordinateSpace) := by
  letI : NeZero n := ⟨hn⟩
  apply (BoxIntegral.unitPartition.mem_smul_span_iff (n := n)).2
  intro i
  refine ⟨ν i, ?_⟩
  simp [scaledLatticePoint, mul_div_cancel₀, hn]

lemma exists_scaledLatticePoint {n : ℕ} (hn : n ≠ 0) {x : CoordinateSpace}
    (hx : x ∈ (n : ℝ)⁻¹ • (standardIntegerLattice : Set CoordinateSpace)) :
    ∃ ν : Lattice, scaledLatticePoint n ν = x := by
  letI : NeZero n := ⟨hn⟩
  have hi := (BoxIntegral.unitPartition.mem_smul_span_iff (n := n)).1 hx
  choose ν hν using hi
  refine ⟨ν, ?_⟩
  funext i
  dsimp [scaledLatticePoint]
  have hni : (n : ℝ) ≠ 0 := by exact_mod_cast hn
  exact (div_eq_iff hni).2 (by simpa [mul_comm] using hν i)

def annularIndexEquiv (δ R : ℝ) {n : ℕ} (hn : n ≠ 0) :
    {ν : Lattice // scaledLatticePoint n ν ∈ cubicAnnulus δ R} ≃
    ↑(cubicAnnulus δ R ∩ (n : ℝ)⁻¹ • (standardIntegerLattice : Set CoordinateSpace)) :=
  Equiv.ofBijective (fun ν => ⟨scaledLatticePoint n ν, ν.property,
    scaledLatticePoint_mem_lattice hn ν⟩) (by
      constructor
      · intro ν μ h
        apply Subtype.ext
        exact scaledLatticePoint_injective hn (congrArg Subtype.val h)
      · intro x
        obtain ⟨ν, hν⟩ := exists_scaledLatticePoint hn x.property.2
        exact ⟨⟨ν, hν ▸ x.property.1⟩, Subtype.ext hν⟩)

lemma scaledLatticePoint_radius (n : ℕ) (ν : Lattice) :
    euclideanRadius (scaledLatticePoint n ν) = radius ν / n := by
  have heq : WithLp.toLp 2 (scaledLatticePoint n ν) = (n : ℝ)⁻¹ • latticePoint ν := by
    ext i
    simp [scaledLatticePoint, latticePoint, div_eq_mul_inv, mul_comm]
  rw [euclideanRadius, heq, norm_smul, Real.norm_eq_abs, abs_of_nonneg (inv_nonneg.2 (Nat.cast_nonneg n))]
  simp [radius, div_eq_mul_inv, mul_comm]

lemma lattice_coordinate_norm (ν : Lattice) :
    ‖(fun i => (ν i : ℝ))‖ = (supRadius ν : ℝ) := by
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (Nat.cast_nonneg _)).2
    intro i
    rw [Real.norm_eq_abs, ← natAbs_real]
    exact_mod_cast (supRadius_le_iff ν (supRadius ν)).1 le_rfl i
  · simp only [supRadius, Nat.cast_max, max_le_iff, natAbs_real]
    exact ⟨norm_le_pi_norm (fun i => (ν i : ℝ)) 0,
      norm_le_pi_norm (fun i => (ν i : ℝ)) 1,
      norm_le_pi_norm (fun i => (ν i : ℝ)) 2⟩

lemma scaledLatticePoint_norm (n : ℕ) (ν : Lattice) :
    ‖scaledLatticePoint n ν‖ = (supRadius ν : ℝ) / n := by
  have heq : scaledLatticePoint n ν = (n : ℝ)⁻¹ • (fun i => (ν i : ℝ)) := by
    funext i
    simp [scaledLatticePoint, div_eq_mul_inv, mul_comm]
  rw [heq, norm_smul, Real.norm_eq_abs,
    abs_of_nonneg (inv_nonneg.2 (Nat.cast_nonneg n)), lattice_coordinate_norm]
  ring

lemma scaledLatticePoint_mem_annulus (n : ℕ) (ν : Lattice) (δ R : ℝ) :
    scaledLatticePoint n ν ∈ cubicAnnulus δ R ↔
      δ ≤ (supRadius ν : ℝ) / n ∧ (supRadius ν : ℝ) / n ≤ R := by
  rw [mem_cubicAnnulus, scaledLatticePoint_norm]

def annularDiscreteSum (F : ℝ → ℝ) (δ R : ℝ) (n : ℕ) : ℝ :=
  (∑' ν : {ν : Lattice // scaledLatticePoint n ν ∈ cubicAnnulus δ R},
    F (radius ν / n)) / (n : ℝ)^3

theorem annularDiscreteSum_eq {n : ℕ} (hn : n ≠ 0) (F : ℝ → ℝ) (δ R : ℝ) :
    annularDiscreteSum F δ R n = annularLatticeIntegral F δ R n := by
  unfold annularDiscreteSum annularLatticeIntegral
  congr 1
  rw [← (annularIndexEquiv δ R hn).tsum_eq]
  apply tsum_congr
  intro ν
  exact congrArg F (scaledLatticePoint_radius n ν).symm

theorem annular_discrete_tendsto {F : ℝ → ℝ} (hF : ContinuousOn F (Ioi 0))
    {δ : ℝ} (hδ : 0 < δ) (R : ℝ) :
    Tendsto (annularDiscreteSum F δ R) atTop
      (𝓝 (∫ x in cubicAnnulus δ R, F (euclideanRadius x))) := by
  apply (annular_lattice_tendsto hF hδ R).congr'
  filter_upwards [eventually_ne_atTop (0 : ℕ)] with n hn
  exact (annularDiscreteSum_eq hn F δ R).symm

#print axioms annularIndexEquiv
#print axioms annularDiscreteSum_eq
#print axioms annular_discrete_tendsto

end HMT.V.ThermodynamicLimit
