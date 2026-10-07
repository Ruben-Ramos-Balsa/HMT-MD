import IncidenceChain
import Mathlib

/-!
# The Article II finite boundary-sector instance

This module formalizes the already written 18+18 tritic boundary construction.
The sector eigenvalues are the cardinalities of the previously constructed
hexad and octad flag spaces. They are downstream labels, not generator inputs.
The reduced state and its diagonal Schmidt purification are actual finite
functions on all 36 links. General entropy/relative-entropy theorems are not
re-proved here.
-/

noncomputable section
open scoped BigOperators

namespace HMT.II.SectorialAreaInformation

abbrev Sector := Fin 2
abbrev Link := Sector × Fin 18
abbrev Occupation := Link → Fin 3

def incidenceLabel (s : Sector) : ℕ :=
  if s = 0 then Fintype.card HMT.OrientedReturn.HexadFlags
  else Fintype.card HMT.OrientedReturn.OctadFlags

@[simp] theorem incidenceLabel_zero : incidenceLabel 0 = 90 := by
  unfold incidenceLabel
  rw [if_pos rfl]
  exact HMT.OrientedReturn.hexadFlags_cardinal

@[simp] theorem incidenceLabel_one : incidenceLabel 1 = 120 := by
  unfold incidenceLabel
  rw [if_neg (by decide)]
  exact HMT.OrientedReturn.octadFlags_cardinal

theorem link_cardinality : Fintype.card Link = 36 := by decide

/-- The actual oriented boundary edges of the 9 by 9 block in the 27-torus.
Indices 0,...,8 encode the incoming side and 9,...,17 the outgoing side. -/
def boundaryEdge (l : Link) : ((ZMod 27 × ZMod 27) × (ZMod 27 × ZMod 27)) :=
  let j : ZMod 27 := ((l.2.val % 9 : ℕ) : ZMod 27)
  if l.1 = 0 then
    if l.2.val < 9 then ((-1, j), (0, j)) else ((8, j), (9, j))
  else
    if l.2.val < 9 then ((j, -1), (j, 0)) else ((j, 8), (j, 9))

set_option maxRecDepth 10000 in
set_option maxHeartbeats 2000000 in
theorem boundaryEdge_injective : Function.Injective boundaryEdge := by decide

theorem boundary_edges_cardinality :
    (Finset.univ.image boundaryEdge).card = 36 := by
  rw [Finset.card_image_of_injective _ boundaryEdge_injective]
  exact link_cardinality

def sectorNumber (s : Sector) (v : Occupation) : ℝ :=
  ∑ i : Fin 18, ((v (s, i)).val : ℝ)

def totalNumber (v : Occupation) : ℝ := sectorNumber 0 v + sectorNumber 1 v

def incidenceNumber (v : Occupation) : ℝ :=
  incidenceLabel 0 * sectorNumber 0 v + incidenceLabel 1 * sectorNumber 1 v

theorem recover_sector_zero (v : Occupation) :
    sectorNumber 0 v = 4 * totalNumber v - incidenceNumber v / 30 := by
  simp only [totalNumber, incidenceNumber, incidenceLabel_zero, incidenceLabel_one]
  push_cast
  ring

theorem recover_sector_one (v : Occupation) :
    sectorNumber 1 v = incidenceNumber v / 30 - 3 * totalNumber v := by
  simp only [totalNumber, incidenceNumber, incidenceLabel_zero, incidenceLabel_one]
  push_cast
  ring

theorem sector_recovery_unique (v : Occupation) (a b : ℝ)
    (hN : a + b = totalNumber v)
    (hD : 90 * a + 120 * b = incidenceNumber v) :
    a = sectorNumber 0 v ∧ b = sectorNumber 1 v := by
  have h0 := recover_sector_zero v
  have h1 := recover_sector_one v
  constructor <;> linarith

def reverseOccupation (v : Occupation) : Occupation := fun l => ⟨2 - (v l).val, by omega⟩

theorem reverseOccupation_involutive : Function.Involutive reverseOccupation := by
  intro v
  funext l
  apply Fin.ext
  simp only [reverseOccupation]
  have h := (v l).isLt
  omega

theorem sectorNumber_reverse (s : Sector) (v : Occupation) :
    sectorNumber s (reverseOccupation v) = 36 - sectorNumber s v := by
  unfold sectorNumber
  have hlocal (i : Fin 18) :
      ((reverseOccupation v (s, i)).val : ℝ) = 2 - ((v (s, i)).val : ℝ) := by
    simp only [reverseOccupation]
    rw [Nat.cast_sub (by have := (v (s, i)).isLt; omega)]
    norm_num
  simp_rw [hlocal]
  norm_num [Finset.sum_sub_distrib]

theorem totalNumber_reverse (v : Occupation) :
    totalNumber (reverseOccupation v) = 72 - totalNumber v := by
  simp only [totalNumber, sectorNumber_reverse]
  ring

theorem incidenceNumber_reverse (v : Occupation) :
    incidenceNumber (reverseOccupation v) = 7560 - incidenceNumber v := by
  simp only [incidenceNumber, sectorNumber_reverse,
    incidenceLabel_zero, incidenceLabel_one]
  push_cast
  ring

def localPartition (x : ℝ) : ℝ := 1 + x + x ^ 2

def localProbability (x : ℝ) (n : Fin 3) : ℝ := x ^ n.val / localPartition x

theorem localPartition_pos (x : ℝ) (hx : 0 < x) : 0 < localPartition x := by
  unfold localPartition
  positivity

theorem localProbability_pos (x : ℝ) (hx : 0 < x) (n : Fin 3) :
    0 < localProbability x n :=
  div_pos (pow_pos hx _) (localPartition_pos x hx)

theorem localProbability_sum (x : ℝ) (hx : 0 < x) :
    ∑ n : Fin 3, localProbability x n = 1 := by
  simp [Fin.sum_univ_succ, localProbability]
  have hz := ne_of_gt (localPartition_pos x hx)
  unfold localPartition at *
  field_simp
  ring

theorem local_first_moment (x : ℝ) :
    ∑ n : Fin 3, (n.val : ℝ) * localProbability x n =
      (x + 2 * x ^ 2) / localPartition x := by
  simp [Fin.sum_univ_succ, localProbability]
  ring

theorem local_second_moment (x : ℝ) :
    ∑ n : Fin 3, (n.val : ℝ) ^ 2 * localProbability x n =
      (x + 4 * x ^ 2) / localPartition x := by
  simp [Fin.sum_univ_succ, localProbability]
  ring

def sectorWeight (delta : ℝ) (s : Sector) : ℝ :=
  Real.exp (-(incidenceLabel s : ℝ) * delta)

theorem sectorWeight_pos (delta : ℝ) (s : Sector) : 0 < sectorWeight delta s :=
  Real.exp_pos _

def probability (delta : ℝ) (v : Occupation) : ℝ :=
  ∏ l : Link, localProbability (sectorWeight delta l.1) (v l)

theorem probability_pos (delta : ℝ) (v : Occupation) : 0 < probability delta v := by
  exact Finset.prod_pos (fun l _ => localProbability_pos _ (sectorWeight_pos _ _) _)

theorem probability_sum (delta : ℝ) : ∑ v : Occupation, probability delta v = 1 := by
  unfold probability
  rw [← Fintype.prod_sum]
  simp_rw [localProbability_sum _ (sectorWeight_pos _ _)]
  simp

theorem local_log_probability (delta : ℝ) (s : Sector) (n : Fin 3) :
    Real.log (localProbability (sectorWeight delta s) n) =
      (-(incidenceLabel s : ℝ) * delta) * n.val -
        Real.log (localPartition (sectorWeight delta s)) := by
  rw [localProbability, Real.log_div
    (ne_of_gt (pow_pos (sectorWeight_pos delta s) n.val))
    (ne_of_gt (localPartition_pos _ (sectorWeight_pos delta s))), Real.log_pow]
  simp only [sectorWeight, Real.log_exp]
  ring

def logPartition (delta : ℝ) : ℝ :=
  18 * Real.log (localPartition (sectorWeight delta 0)) +
    18 * Real.log (localPartition (sectorWeight delta 1))

theorem sector_log_sum (delta : ℝ) (s : Sector) (v : Occupation) :
    (∑ i : Fin 18, Real.log (localProbability (sectorWeight delta s) (v (s, i)))) =
      (-(incidenceLabel s : ℝ) * delta) * sectorNumber s v -
        18 * Real.log (localPartition (sectorWeight delta s)) := by
  simp_rw [local_log_probability]
  rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
  simp [sectorNumber]

/-- The scalar spectrum of -log rho for the actual normalized state above. -/
theorem negative_log_probability (delta : ℝ) (v : Occupation) :
    -Real.log (probability delta v) = logPartition delta + delta * incidenceNumber v := by
  have hp : Real.log (probability delta v) =
      ∑ l : Link, Real.log (localProbability (sectorWeight delta l.1) (v l)) := by
    unfold probability
    exact Real.log_prod _ _ (fun l _ => ne_of_gt (localProbability_pos _
      (sectorWeight_pos delta l.1) (v l)))
  rw [hp, Fintype.sum_prod_type]
  simp only [Fin.sum_univ_two]
  rw [sector_log_sum delta 0 v, sector_log_sum delta 1 v]
  simp only [incidenceNumber, logPartition, incidenceLabel_zero, incidenceLabel_one]
  push_cast
  ring

def entropy (delta : ℝ) : ℝ :=
  ∑ v : Occupation, probability delta v * (-Real.log (probability delta v))

def expectedIncidence (delta : ℝ) : ℝ :=
  ∑ v : Occupation, probability delta v * incidenceNumber v

theorem entropy_state_equation (delta : ℝ) :
    entropy delta = logPartition delta + delta * expectedIncidence delta := by
  unfold entropy
  simp_rw [negative_log_probability, mul_add]
  rw [Finset.sum_add_distrib, ← Finset.sum_mul, probability_sum]
  simp only [one_mul]
  apply congrArg (fun z : ℝ => logPartition delta + z)
  unfold expectedIncidence
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro v _
  ring

/-- Coordinates of the diagonal Schmidt vector in the real subspace of the
complex bipartite space. Its complexification has the same reduced density. -/
def purification (delta : ℝ) (v w : Occupation) : ℝ :=
  if v = w then Real.sqrt (probability delta v) else 0

def reducedDensity (delta : ℝ) (v w : Occupation) : ℝ :=
  ∑ u : Occupation, purification delta v u * purification delta w u

theorem reducedDensity_diagonal (delta : ℝ) (v w : Occupation) :
    reducedDensity delta v w = if v = w then probability delta v else 0 := by
  classical
  unfold reducedDensity purification
  by_cases hvw : v = w
  · subst w
    simp only [if_true]
    rw [Finset.sum_eq_single v]
    · simp only [if_true]
      exact Real.mul_self_sqrt (le_of_lt (probability_pos delta v))
    · intro b _ hb
      simp [Ne.symm hb]
    · simp
  · simp only [hvw, if_false]
    apply Finset.sum_eq_zero
    intro u _
    by_cases hvu : v = u
    · have hwu : w ≠ u := fun h => hvw (hvu.trans h.symm)
      simp only [if_pos hvu, if_neg hwu, mul_zero]
    · simp only [if_neg hvu, zero_mul]

theorem reducedDensity_trace (delta : ℝ) :
    ∑ v : Occupation, reducedDensity delta v v = 1 := by
  simp only [reducedDensity_diagonal, if_true]
  exact probability_sum delta

theorem purification_normalized (delta : ℝ) :
    ∑ v : Occupation, ∑ w : Occupation, purification delta v w ^ 2 = 1 := by
  have h (v : Occupation) :
      (∑ w : Occupation, purification delta v w ^ 2) = reducedDensity delta v v := by
    simp [reducedDensity, pow_two]
  simp_rw [h]
  exact reducedDensity_trace delta

def normalizedArea (gamma a0 : ℝ) (v : Occupation) : ℝ :=
  gamma * a0 * totalNumber v

def normalizedSectorArea (gamma a0 : ℝ) (s : Sector) (v : Occupation) : ℝ :=
  gamma * a0 * sectorNumber s v

def modularCoefficient (gamma a0 delta : ℝ) (s : Sector) : ℝ :=
  (incidenceLabel s : ℝ) * delta / (gamma * a0)

theorem modularCoefficient_ratio (gamma a0 delta : ℝ) :
    modularCoefficient gamma a0 delta 1 =
      (4 / 3 : ℝ) * modularCoefficient gamma a0 delta 0 := by
  simp only [modularCoefficient, incidenceLabel_zero, incidenceLabel_one]
  push_cast
  ring

theorem modular_area_identity (gamma a0 delta : ℝ) (hg : gamma ≠ 0) (ha : a0 ≠ 0)
    (v : Occupation) :
    modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v =
      delta * incidenceNumber v := by
  simp only [modularCoefficient, normalizedSectorArea, incidenceNumber]
  field_simp
  ring

theorem modular_area_of_reduced_state (gamma a0 delta : ℝ) (hg : gamma ≠ 0)
    (ha : a0 ≠ 0) (v : Occupation) :
    -Real.log (reducedDensity delta v v) = logPartition delta +
      modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v := by
  rw [reducedDensity_diagonal]
  simp only [if_true]
  rw [negative_log_probability]
  rw [← modular_area_identity gamma a0 delta hg ha v]
  ring

theorem area_complement (gamma a0 : ℝ) (v : Occupation) :
    normalizedArea gamma a0 (reverseOccupation v) + normalizedArea gamma a0 v =
      72 * gamma * a0 := by
  simp only [normalizedArea, totalNumber_reverse]
  ring

theorem sectorial_boundary_instance (delta gamma a0 : ℝ) (hg : gamma ≠ 0)
    (ha : a0 ≠ 0) :
    Fintype.card Link = 36 ∧
    (∀ v, sectorNumber 0 v = 4 * totalNumber v - incidenceNumber v / 30) ∧
    (∀ v, sectorNumber 1 v = incidenceNumber v / 30 - 3 * totalNumber v) ∧
    (∑ v : Occupation, probability delta v = 1) ∧
    (∀ v w, reducedDensity delta v w = if v = w then probability delta v else 0) ∧
    (∑ v : Occupation, ∑ w : Occupation, purification delta v w ^ 2 = 1) ∧
    (∀ v, modularCoefficient gamma a0 delta 0 * normalizedSectorArea gamma a0 0 v +
      modularCoefficient gamma a0 delta 1 * normalizedSectorArea gamma a0 1 v =
        delta * incidenceNumber v) := by
  exact ⟨link_cardinality, recover_sector_zero, recover_sector_one,
    probability_sum delta, reducedDensity_diagonal delta, purification_normalized delta,
    modular_area_identity gamma a0 delta hg ha⟩

#print axioms sectorial_boundary_instance
#print axioms reverseOccupation_involutive
#print axioms area_complement
#print axioms boundaryEdge_injective
#print axioms negative_log_probability
#print axioms entropy_state_equation
#print axioms modular_area_of_reduced_state

end HMT.II.SectorialAreaInformation
