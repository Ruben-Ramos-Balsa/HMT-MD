import ArticleIIIFromSharedBase
import PellTangentTripling

/-!
Article III, recovered Catalan--Pell branch and its selected-channel composition.

The universal moment is the existing OrientedMoment.moment, constructed from
the oriented quarter-turn character, not from the selected angular constants.
NormalizedQuarterTurn realizes that character in the twelve-coordinate cycle.
OrientedSeries proves absolute/uniform convergence through the endpoint;
MomentDerivatives and MomentIntegral prove the differential/integral bridge;
PellTangentTripling proves the exact Pell evaluation without assuming it.

The selected chamber enters only through sPlus = qPlus^30 and sMinus = qMinus^30.
These are the same labelled channels as ArticleIIIFromSharedBase. No equality
between either selected argument and pellRho is asserted or assumed. The Pell
branch is a distinct evaluation of the same universal family. Its pi is written
using the already constructed HMT reader by posterior recognition only.

Owners: Article III, 05_ciclo_catalan.tex, iii:eq:quarter-intertwiner,
iii:eq:c2, iii:eq:c2-integral, iii:eq:catalan-vacuum; 06_pell_barbero.tex,
iii:eq:pell-moment-integral, iii:thm:catalan-pell. The existing tangent-tripling
proof establishes the exact terminal value; it is not a formalization of the
manuscript's entire Fourier lemma or of every result in Article III.
-/

noncomputable section
namespace HMT.Shared.ArticleIII.CatalanPell

open HMT.III.Constitutive HMT.III.OrientedMoment
open MeasureTheory
open scoped Topology

def sPlus : ℝ := channels.qPlus ^ 30
def sMinus : ℝ := channels.qMinus ^ 30

/-- The normalized marked coefficient of the existing twelve-cycle realization. -/
def orientedCoefficient (s : ℝ) : ℝ :=
  ∑ j : Fin 12, normalizedEmbed (0, 1) j *
    normalizedEmbed (resolvent s (1, 0)) j

def responseWeight (s : ℝ) : ℝ := (1 + s + s ^ 2) / (s * (1 + s))

theorem selected_arguments_mem :
    sPlus ∈ Set.Ioo 0 1 ∧ sMinus ∈ Set.Ioo 0 1 :=
  ⟨channel_power_mem channels.plus_mem, channel_power_mem channels.minus_mem⟩

/-- The existing channel response receives exactly the selected arguments. -/
theorem selected_response_arguments :
    vacuum.rPlus = response sPlus ∧ vacuum.rMinus = response sMinus :=
  ⟨channelResponse_eq channels.plus_mem, channelResponse_eq channels.minus_mem⟩

theorem selected_moment_integrals :
    moment sPlus = (∫ t in (0 : ℝ)..sPlus, Real.arctan t / t) ∧
    moment sMinus = (∫ t in (0 : ℝ)..sMinus, Real.arctan t / t) :=
  ⟨moment_integral selected_arguments_mem.1.1.le selected_arguments_mem.1.2.le,
    moment_integral selected_arguments_mem.2.1.le selected_arguments_mem.2.2.le⟩

/-- The derivative is the oriented coefficient, not merely an equal determinant. -/
theorem selected_second_euler_coefficients :
    euler (euler moment) sPlus = orientedCoefficient sPlus ∧
    euler (euler moment) sMinus = orientedCoefficient sMinus := by
  have hp : ‖sPlus‖ < 1 := by
    simpa only [Real.norm_eq_abs, abs_of_pos selected_arguments_mem.1.1]
      using selected_arguments_mem.1.2
  have hm : ‖sMinus‖ < 1 := by
    simpa only [Real.norm_eq_abs, abs_of_pos selected_arguments_mem.2.1]
      using selected_arguments_mem.2.2
  exact ⟨(second_euler_moment hp).trans (normalized_oriented_coefficient sPlus).symm,
    (second_euler_moment hm).trans (normalized_oriented_coefficient sMinus).symm⟩

theorem selected_response_from_moment :
    vacuum.rPlus = responseWeight sPlus * euler (euler moment) sPlus ∧
    vacuum.rMinus = responseWeight sMinus * euler (euler moment) sMinus :=
  ⟨selected_response_arguments.1.trans
      (existing_response_relation selected_arguments_mem.1.1 selected_arguments_mem.1.2),
    selected_response_arguments.2.trans
      (existing_response_relation selected_arguments_mem.2.1 selected_arguments_mem.2.2)⟩

theorem selected_response_from_resolvent :
    vacuum.rPlus = responseWeight sPlus * orientedCoefficient sPlus ∧
    vacuum.rMinus = responseWeight sMinus * orientedCoefficient sMinus := by
  simpa only [selected_second_euler_coefficients.1, selected_second_euler_coefficients.2]
    using selected_response_from_moment

/-- The selected evaluations retain the actual unbounded-depth character series. -/
theorem selected_series_from_character :
    (moment sPlus = ∑' n : ℕ,
      (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 *
        sPlus ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2) ∧
    (moment sMinus = ∑' n : ℕ,
      (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 *
        sMinus ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2) :=
  ⟨tsum_congr (fun n => term_from_character n sPlus),
    tsum_congr (fun n => term_from_character n sMinus)⟩

/-- Pell is a separate downstream evaluation of the universal moment. -/
theorem pell_complete_in_constructed_pi :
    moment pellRho = (2 / 3 : ℝ) * HMT.III.OrientedMoment.catalan -
      (HMT.I.SelectedAction.pi / 12) * Real.log pellLambda ∧
    euler moment pellRho = HMT.I.SelectedAction.pi / 12 ∧
    euler (euler moment) pellRho = (1 / 4 : ℝ) := by
  simpa only [constructed_pi_recognition] using catalan_pell_complete

theorem pell_integral_evaluation :
    (∫ t in (0 : ℝ)..pellRho, Real.arctan t / t) =
      (2 / 3 : ℝ) * HMT.III.OrientedMoment.catalan -
        (HMT.I.SelectedAction.pi / 12) * Real.log pellLambda :=
  pell_moment_integral.symm.trans pell_complete_in_constructed_pi.1

/-- All arguments and domain facts come from the selected base or the proved Pell unit. -/
theorem shared_catalan_pell_publication :
    (∀ x : Plane, cycle12 (normalizedEmbed x) = normalizedEmbed (quarter x)) ∧
    (vacuum.rPlus = responseWeight sPlus * orientedCoefficient sPlus ∧
      vacuum.rMinus = responseWeight sMinus * orientedCoefficient sMinus) ∧
    (moment sPlus = ∑' n : ℕ,
      (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 *
        sPlus ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2) ∧
    (moment sMinus = ∑' n : ℕ,
      (((quarter : Plane → Plane)^[2 * n + 1]) (1, 0)).2 *
        sMinus ^ (2 * n + 1) / ((2 * n + 1 : ℕ) : ℝ) ^ 2) ∧
    (moment sPlus = (∫ t in (0 : ℝ)..sPlus, Real.arctan t / t) ∧
      moment sMinus = (∫ t in (0 : ℝ)..sMinus, Real.arctan t / t)) ∧
    Filter.Tendsto moment (𝓝[Set.Icc (0 : ℝ) 1] 1)
      (𝓝 HMT.III.OrientedMoment.catalan) ∧
    (∫ t in (0 : ℝ)..pellRho, Real.arctan t / t) =
      (2 / 3 : ℝ) * HMT.III.OrientedMoment.catalan -
        (HMT.I.SelectedAction.pi / 12) * Real.log pellLambda ∧
    euler moment pellRho = HMT.I.SelectedAction.pi / 12 ∧
    euler (euler moment) pellRho = (1 / 4 : ℝ) :=
  ⟨normalized_cycle_intertwines, selected_response_from_resolvent,
    selected_series_from_character.1, selected_series_from_character.2,
    selected_moment_integrals, moment_endpoint_limit, pell_integral_evaluation,
    pell_complete_in_constructed_pi.2⟩

end HMT.Shared.ArticleIII.CatalanPell
end

#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_arguments_mem
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_response_arguments
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_moment_integrals
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_second_euler_coefficients
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_response_from_moment
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_response_from_resolvent
#print axioms HMT.Shared.ArticleIII.CatalanPell.selected_series_from_character
#print axioms HMT.Shared.ArticleIII.CatalanPell.pell_complete_in_constructed_pi
#print axioms HMT.Shared.ArticleIII.CatalanPell.pell_integral_evaluation
#print axioms HMT.Shared.ArticleIII.CatalanPell.shared_catalan_pell_publication
