import ElectronComposition
import VacancyDeltaBounds

/-!
The regional electronic torsion and the logarithmic vacancy are distinct
readers. A rational separator prevents substituting the latter in the
electronic composition. All inputs are the existing generated regional
readers; no new numerical interval is assumed.
-/

noncomputable section

namespace HMT.I.ElectronTorsionSeparation

theorem regional_full_lt_one_thirtieth :
    ElectronComposition.regionalFull < (1 : ℝ) / 30 := by
  have hp := AlphaPositionalBridge.closure_integer_part
  have he := AlphaPositionalBridge.propagation_integer_part
  have hl : 0 < Real.log ClosureAnalytic.value :=
    Real.log_pos (by linarith)
  have hem : 0 < PropagationLimit.value * Real.log ClosureAnalytic.value :=
    mul_pos (by linarith) hl
  have hr : ElectronComposition.regionalReduced < (4 : ℝ) / 270 := by
    unfold ElectronComposition.regionalReduced ElectronComposition.reducedTorsion
    exact (div_lt_div_iff_of_pos_right (by norm_num : (0 : ℝ) < 270)).2
      (by linarith)
  have hs : 1 + ClosureAnalytic.value / 729 < (2 : ℝ) := by linarith
  have hs0 : 0 < 1 + ClosureAnalytic.value / 729 := by linarith
  calc
    ElectronComposition.regionalFull =
        ElectronComposition.regionalReduced * (1 + ClosureAnalytic.value / 729) := rfl
    _ < (4 / 270 : ℝ) * 2 :=
      mul_lt_mul hr hs.le hs0 (by norm_num)
    _ < (1 : ℝ) / 30 := by norm_num

theorem one_thirtieth_lt_vacancy :
    (1 : ℝ) / 30 < VacancyDeltaBounds.vacancyDelta := by
  exact lt_trans (by norm_num [AlphaStateLinkBound.deltaLower])
    VacancyDeltaBounds.vacancyDelta_enclosure.1

theorem regional_torsion_lt_vacancy :
    ElectronComposition.regionalFull < VacancyDeltaBounds.vacancyDelta :=
  lt_trans regional_full_lt_one_thirtieth one_thirtieth_lt_vacancy

theorem regional_torsion_ne_vacancy :
    ElectronComposition.regionalFull ≠ VacancyDeltaBounds.vacancyDelta :=
  ne_of_lt regional_torsion_lt_vacancy

end HMT.I.ElectronTorsionSeparation

#print axioms HMT.I.ElectronTorsionSeparation.regional_full_lt_one_thirtieth
#print axioms HMT.I.ElectronTorsionSeparation.one_thirtieth_lt_vacancy
#print axioms HMT.I.ElectronTorsionSeparation.regional_torsion_lt_vacancy
#print axioms HMT.I.ElectronTorsionSeparation.regional_torsion_ne_vacancy
