import BosonManyModes

/-! Bosonic Gibbs weights from the additive grand-canonical energy, with exact reindexing. -/

noncomputable section

namespace QuantumOccupations

/-- The actual additive `H - μ N` eigenvalue on an occupation configuration. -/
def bosonGrandEnergy (μ : ℝ) : (energies : List ℝ) → BosonStates energies.length → ℝ
  | [], _ => 0
  | E :: energies, s => (s.1 : ℝ) * (E - μ) + bosonGrandEnergy μ energies s.2

/-- Replace the energy labels by thermal weights without changing any occupation. -/
def thermalStateEquiv (β μ : ℝ) : (energies : List ℝ) →
    BosonStates energies.length ≃ BosonStates (thermalWeights β μ energies).length
  | [] => Equiv.refl _
  | _ :: energies => Equiv.prodCongr (Equiv.refl ℕ) (thermalStateEquiv β μ energies)

/-- Product weights are proved to be the exponential of the additive grand energy. -/
theorem boson_thermal_weight_eq (β μ : ℝ) (energies : List ℝ)
    (s : BosonStates energies.length) :
    bosonStateWeight (thermalWeights β μ energies) (thermalStateEquiv β μ energies s) =
      Real.exp (-β * bosonGrandEnergy μ energies s) := by
  induction energies with
  | nil => simp [thermalWeights, thermalStateEquiv, bosonStateWeight, bosonGrandEnergy]
  | cons E energies ih =>
    rcases s with ⟨n, s⟩
    change fugacity β E μ ^ n *
      bosonStateWeight (thermalWeights β μ energies) (thermalStateEquiv β μ energies s) =
        Real.exp (-β * ((n : ℝ) * (E - μ) + bosonGrandEnergy μ energies s))
    rw [ih, fugacity, ← Real.exp_nat_mul, ← Real.exp_add]
    congr 1
    ring

def bosonGibbsPartition (β μ : ℝ) (energies : List ℝ) : ℝ :=
  ∑' s : BosonStates energies.length, Real.exp (-β * bosonGrandEnergy μ energies s)

def bosonGibbsProbability (β μ : ℝ) (energies : List ℝ)
    (s : BosonStates energies.length) : ℝ :=
  Real.exp (-β * bosonGrandEnergy μ energies s) / bosonGibbsPartition β μ energies

/-- Gibbs partition and the configuration-weight partition are equal by a bijection. -/
theorem bosonGibbs_partition_eq_many (β μ : ℝ) (energies : List ℝ) :
    bosonGibbsPartition β μ energies = bosonManyPartition (thermalWeights β μ energies) := by
  have h := (thermalStateEquiv β μ energies).tsum_eq (bosonStateWeight (thermalWeights β μ energies))
  simpa only [boson_thermal_weight_eq] using h

theorem bosonGibbs_probability_eq_many (β μ : ℝ) (energies : List ℝ)
    (s : BosonStates energies.length) :
    bosonGibbsProbability β μ energies s =
      bosonManyProbability (thermalWeights β μ energies) (thermalStateEquiv β μ energies s) := by
  unfold bosonGibbsProbability bosonManyProbability
  rw [boson_thermal_weight_eq, bosonGibbs_partition_eq_many]

/-- The Gibbs series itself converges on the stated thermodynamic domain. -/
theorem bosonGibbs_hasSum {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    HasSum (fun s : BosonStates energies.length => Real.exp (-β * bosonGrandEnergy μ energies s))
      (bosonFactors (thermalWeights β μ energies)) := by
  have h := (thermalStateEquiv β μ energies).hasSum_iff.mpr
    (bosonManyWeight_hasSum (thermalWeights_admissible hβ hμ))
  simpa only [Function.comp_def, boson_thermal_weight_eq] using h

theorem bosonGibbs_probability_hasSum {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    HasSum (bosonGibbsProbability β μ energies) 1 := by
  have h := (thermalStateEquiv β μ energies).hasSum_iff.mpr
    (bosonMany_probability_hasSum (thermalWeights_admissible hβ hμ))
  simpa only [Function.comp_def, ← bosonGibbs_probability_eq_many] using h

/-- Grand-canonical factorization starting from the exponential of `H - μ N`. -/
theorem bosonGibbs_factorization {β μ : ℝ} {energies : List ℝ}
    (hβ : 0 < β) (hμ : ∀ E ∈ energies, μ < E) :
    bosonGibbsPartition β μ energies =
      (energies.map (fun E => (1 - Real.exp (-(β * (E - μ))))⁻¹)).prod := by
  rw [bosonGibbs_partition_eq_many]
  exact boson_grandCanonical_factorization hβ hμ

#print axioms boson_thermal_weight_eq
#print axioms bosonGibbs_partition_eq_many
#print axioms bosonGibbs_probability_eq_many
#print axioms bosonGibbs_hasSum
#print axioms bosonGibbs_probability_hasSum
#print axioms bosonGibbs_factorization

end QuantumOccupations
