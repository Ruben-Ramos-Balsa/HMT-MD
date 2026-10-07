import OrthogonalKScreen
import SelectedKDirection
import P3ChartProjection
import SelectedLorentzScreen
import ArticleIExceptionalInterface

/-!
# The selected K-directed screen and elliptic duality

This consumer discharges the generic screen hypotheses with the actual
register already generated in Article I.  It combines the real reductions,
the isotropic quotient of the same selected lattice, and the previously
formalized radius and Hilbert-space duality.  The graph retains its first
coordinate (dimension eleven); its projected second coordinate has dimension
ten. These are different objects, not interchangeable dimension counts.

The finite A5 character-table provenance is independently reproduced by the
accompanying exact-arithmetic certificate. FLM remains a classical application
of the inherited exceptional interface, not an extra axiom of this module.
-/

noncomputable section
namespace HMT.IV.ArticleIVSelectedScreens

open scoped InnerProductSpace
open OrthogonalKScreen LorentzScreen
open HMT.I.ArticleIExceptionalInterface HMT.I.SelectedRegionalIncidence

abbrev direction := SelectedKDirection.uK

theorem direction_mem : direction ∈ V11 :=
  Submodule.mem_orthogonal_singleton_iff_inner_right.mpr
    SelectedKDirection.inner_ones_uK

theorem meanZero_is_P11 :
    SelectedKDirection.meanZeroK = P11 SelectedKDirection.selectedK := by
  ext i
  simp [SelectedKDirection.meanZeroK, P11_coordinates]

theorem direction_generated : direction = WithLp.toLp 2
    (SelectedKDirection.P3.mulVec (P11 SelectedKDirection.selectedK)) := by
  change SelectedKDirection.uK = _
  rw [SelectedKDirection.uK, meanZero_is_P11]

abbrev selectedP10 := P10 direction
abbrev RealScreen := Graph direction

def coordinatedEquiv :
    (UniformQuotient × ScalarDomain × LorentzQuotient) ≃
      (RealScreen × ScalarDomain × SelectedLattice) :=
  productScreenEquiv (realScreenEquiv direction).toEquiv

def ellipticCoordinatedEquiv :
    (UniformQuotient × EllipticDomain × LorentzQuotient) ≃
      (RealScreen × EllipticDomain × SelectedLattice) :=
  productScreenEquiv (realScreenEquiv direction).toEquiv

/-- The same isomorphism using the literal hyperplane quotient rather than
its already proved integral coordinates. -/
def actualCoordinatedEquiv :
    (UniformQuotient × EllipticDomain ×
      (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal)) ≃
      (RealScreen × EllipticDomain × SelectedLattice) :=
  actualProductScreenEquiv (realScreenEquiv direction).toEquiv

theorem actual_coordinated_formula (v : E) (d : EllipticDomain)
    (y : orthogonalHyperplane) :
    let out := actualCoordinatedEquiv
      (Submodule.Quotient.mk v, d, Submodule.Quotient.mk y)
    (out.1.val, out.2.1, out.2.2) = ((P11 v, selectedP10 v), d, y.val.1) := by
  change (((realScreenEquiv direction (Submodule.Quotient.mk v) : E × E)),
      d, actualQuotientEquiv (Submodule.Quotient.mk y)) = _
  rw [realScreenEquiv_formula direction_mem, actualQuotientEquiv_mk]

theorem actual_elliptic_duality
    (x : UniformQuotient × EllipticDomain ×
      (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal)) :
    actualCoordinatedEquiv (middleAction ellipticDuality x) =
      middleAction ellipticDuality (actualCoordinatedEquiv x) ∧
    FiniteWeyl.Duality.energyAt (ellipticDuality x.2.1).val.1.val
      (ellipticDuality x.2.1).val.2 =
        FiniteWeyl.Duality.energyAt x.2.1.val.1.val x.2.1.val.2 :=
  elliptic_screen_intertwines (realScreenEquiv direction).toEquiv x

theorem coordinated_formula (v : E) (d : ScalarDomain) (y : OrthogonalCoordinates) :
    let out := coordinatedEquiv
      (Submodule.Quotient.mk v, d, Submodule.Quotient.mk y)
    (out.1.val, out.2.1, out.2.2) = ((P11 v, selectedP10 v), d, y.1) := by
  change (((realScreenEquiv direction (Submodule.Quotient.mk v) : E × E)),
      d, quotientEquiv (Submodule.Quotient.mk y)) = _
  rw [realScreenEquiv_formula direction_mem, quotientEquiv_mk]

theorem coordinated_duality (x : UniformQuotient × ScalarDomain × LorentzQuotient) :
    coordinatedEquiv (middleAction scalarDuality x) =
      middleAction scalarDuality (coordinatedEquiv x) := rfl

theorem coordinated_energy (x : UniformQuotient × ScalarDomain × LorentzQuotient) :
    let out := coordinatedEquiv (middleAction scalarDuality x)
    FiniteWeyl.Duality.energyAt out.2.1.1.val out.2.1.2 =
      FiniteWeyl.Duality.energyAt x.2.1.1.val x.2.1.2 :=
  scalarDuality_energy x.2.1

theorem elliptic_coordinated_duality
    (x : UniformQuotient × EllipticDomain × LorentzQuotient) :
    ellipticCoordinatedEquiv (middleAction ellipticDuality x) =
      middleAction ellipticDuality (ellipticCoordinatedEquiv x) := rfl

theorem elliptic_coordinated_energy
    (x : UniformQuotient × EllipticDomain × LorentzQuotient) :
    let out := ellipticCoordinatedEquiv (middleAction ellipticDuality x)
    FiniteWeyl.Duality.energyAt out.2.1.val.1.val out.2.1.val.2 =
      FiniteWeyl.Duality.energyAt x.2.1.val.1.val x.2.1.val.2 :=
  ellipticDuality_energy x.2.1

/-- One hypothesis-free consumer for the concrete screen realization. -/
theorem article_IV_selected_screens :
    SelectedKDirection.P3.transpose = SelectedKDirection.P3 ∧
    SelectedKDirection.P3 * SelectedKDirection.P3 = SelectedKDirection.P3 ∧
    SelectedKDirection.P3.mulVec (fun _ : Fin 12 => (1 : ℝ)) = 0 ∧
    Matrix.trace SelectedKDirection.P3 = 3 ∧
    direction = WithLp.toLp 2
      (SelectedKDirection.P3.mulVec (P11 SelectedKDirection.selectedK)) ∧
    ‖direction‖ ^ 2 = (6638585 + 2275584 * Real.sqrt 5) / 20 ∧
    0 < ‖direction‖ ^ 2 ∧
    Module.finrank ℝ V11 = 11 ∧
    Module.finrank ℝ (LinearMap.range selectedP10) = 10 ∧
    Module.finrank ℝ RealScreen = 11 ∧
    (∀ v : E, selectedP10 v = P11 v -
      (⟪direction, v⟫_ℝ / ‖direction‖ ^ 2) • direction) ∧
    (∀ v : E, selectedP10 (selectedP10 v) = selectedP10 v ∧
      selectedP10 (P11 v) = selectedP10 v ∧
      ((V10 direction).orthogonalProjection v : E) = selectedP10 v) ∧
    (∀ v w : E, ⟪selectedP10 v, w⟫_ℝ = ⟪v, selectedP10 w⟫_ℝ) ∧
    selectedP10 direction = 0 ∧ selectedP10 ones = 0 ∧
    Module.finrank ℤ LorentzLattice = 26 ∧
    Module.finrank ℤ orthogonalHyperplane = 25 ∧
    Module.finrank ℤ LorentzQuotient = 24 ∧
    (∀ x : UniformQuotient × ScalarDomain × LorentzQuotient,
      coordinatedEquiv (middleAction scalarDuality x) =
        middleAction scalarDuality (coordinatedEquiv x)) ∧
    (0 < SelectedRadiusTDuality.radius ∧ SelectedRadiusTDuality.radius < 1) ∧
    SelectedRadiusTDuality.radius ^ 4 =
      (SelectedRadiusTDuality.angles.x - SelectedRadiusTDuality.angles.y) /
      (SelectedRadiusTDuality.angles.x + SelectedRadiusTDuality.angles.y) ∧
    ClassicalLeechHypotheses selectedRadial := by
  exact ⟨P3ChartProjection.P3_transpose, P3ChartProjection.P3_mul_self,
    P3ChartProjection.P3_uniform_zero, P3ChartProjection.P3_trace,
    direction_generated, SelectedKDirection.norm_sq_uK,
    SelectedKDirection.norm_sq_uK_pos, finrank_V11,
    P10_rank direction_mem SelectedKDirection.uK_ne_zero, graph_finrank direction,
    P10_formula direction,
    fun v => ⟨P10_idempotent direction_mem v, P10_P11 direction_mem v,
      P10_orthogonal_projection direction_mem v⟩,
    P10_symmetric direction, P10_kills_u direction_mem, P10_kills_ones direction_mem,
    screen_ranks.1, screen_ranks.2.1, screen_ranks.2.2, coordinated_duality,
    ⟨SelectedRadiusTDuality.radius_pos, SelectedRadiusTDuality.radius_lt_one⟩,
    SelectedRadiusTDuality.radius_fourth, selected_classical_hypotheses⟩

end HMT.IV.ArticleIVSelectedScreens
end

#print axioms HMT.IV.ArticleIVSelectedScreens.article_IV_selected_screens
#print axioms HMT.IV.ArticleIVSelectedScreens.coordinated_formula
#print axioms HMT.IV.ArticleIVSelectedScreens.elliptic_coordinated_energy
#print axioms HMT.IV.ArticleIVSelectedScreens.actual_elliptic_duality
