import APPPhaseMode
import TPKCensus

/-!
Joint nonadic renewal on the complete emitted fibre, as the posterior Markov
realization in DELTA_CONEXION_NONADICA_CONJUNTA_COMPRESION_EXPRESION_2026-08-16.md.
The two finite coordinate sets are indexed by the already generated additive
and multiplicative signature images. Their cardinalities 18 and 26 are
conclusions of TPKCensus, not target digits or terminal register inputs.

The phase operators act on the WHOLE fibre. The ninefold transfer is one
joint renewal, from every starting phase, not nine independent accept/reject
tests and not a deterministic successor of one visible word. This posterior
operator is not promoted to the enriched generator Gamma9 and does not erase
or reconstruct its memory. No equality producing terminal K is assumed here.
-/

namespace HMT.I.NonadicJointRenewal

open HMT.I.APPPhaseMode

abbrev Fibre := Fin 18 × Fin 26
abbrev Observable := Fibre → ℚ
abbrev PhaseObservable := Fin 9 → Observable

def additiveSignature (a : Fin 18) : List Nat :=
  (TPKCensus.signatureImage .additive).get
    ⟨a.val, by simpa only [TPKCensus.additive_image_cardinality] using a.isLt⟩

def multiplicativeSignature (b : Fin 26) : List Nat :=
  (TPKCensus.signatureImage .multiplicative).get
    ⟨b.val, by simpa only [TPKCensus.multiplicative_image_cardinality] using b.isLt⟩

def emittedWord (u : Fibre) : List Nat :=
  TPKCensus.couple (additiveSignature u.1) (multiplicativeSignature u.2)

theorem emittedWord_mem (u : Fibre) : emittedWord u ∈ TPKCensus.emitted := by
  unfold emittedWord TPKCensus.emitted
  apply List.mem_flatMap.mpr
  refine ⟨additiveSignature u.1, List.get_mem _ _, ?_⟩
  exact List.mem_map.mpr ⟨multiplicativeSignature u.2, List.get_mem _ _, rfl⟩

/-- No part of the emitted fibre is discarded by its pair-coordinate chart. -/
theorem emittedWord_covers (w : List Nat) :
    w ∈ TPKCensus.emitted ↔ ∃ u : Fibre, emittedWord u = w := by
  constructor
  · intro hw
    obtain ⟨a, ha, hw⟩ := List.mem_flatMap.mp hw
    obtain ⟨b, hb, hab⟩ := List.mem_map.mp hw
    obtain ⟨ia, hia⟩ := List.mem_iff_get.mp ha
    obtain ⟨ib, hib⟩ := List.mem_iff_get.mp hb
    let a' : Fin 18 := ⟨ia.val, by simpa only [TPKCensus.additive_image_cardinality] using ia.isLt⟩
    let b' : Fin 26 := ⟨ib.val, by simpa only [TPKCensus.multiplicative_image_cardinality] using ib.isLt⟩
    have ha' : additiveSignature a' = a := by
      unfold additiveSignature
      dsimp only [a']
      exact hia
    have hb' : multiplicativeSignature b' = b := by
      unfold multiplicativeSignature
      dsimp only [b']
      exact hib
    exact ⟨(a',b'), by simpa only [emittedWord, ha', hb'] using hab⟩
  · rintro ⟨u, rfl⟩
    exact emittedWord_mem u

def additiveAverage (f : Observable) : Observable :=
  fun u => (∑ a : Fin 18, f (a, u.2)) / 18

def multiplicativeAverage (f : Observable) : Observable :=
  fun u => (∑ b : Fin 26, f (u.1, b)) / 26

def renewal (f : Observable) : Observable :=
  fun _ => (∑ a : Fin 18, ∑ b : Fin 26, f (a, b)) / 468

theorem additive_constant (x : ℚ) : additiveAverage (fun _ => x) = fun _ => x := by
  funext u
  simp [additiveAverage]

theorem multiplicative_constant (x : ℚ) :
    multiplicativeAverage (fun _ => x) = fun _ => x := by
  funext u
  simp [multiplicativeAverage]

theorem additive_multiplicative (f : Observable) :
    additiveAverage (multiplicativeAverage f) = renewal f := by
  funext u
  simp only [additiveAverage, multiplicativeAverage, renewal, ← Finset.sum_div]
  ring

theorem multiplicative_additive (f : Observable) :
    multiplicativeAverage (additiveAverage f) = renewal f := by
  funext u
  simp only [additiveAverage, multiplicativeAverage, renewal, ← Finset.sum_div]
  rw [Finset.sum_comm]
  ring

theorem additive_renewal (f : Observable) : additiveAverage (renewal f) = renewal f :=
  additive_constant _

theorem multiplicative_renewal (f : Observable) :
    multiplicativeAverage (renewal f) = renewal f := multiplicative_constant _

def phaseOperator (r : Fin 9) (f : Observable) : Observable :=
  if phaseMode r = 1 then additiveAverage f
  else if phaseMode r = -1 then multiplicativeAverage f else f

def nextPhase (r : Fin 9) : Fin 9 := ⟨(r.val + 1) % 9, Nat.mod_lt _ (by decide)⟩

/-- Posterior transfer of the complete field over the cyclic base. -/
def transfer (f : PhaseObservable) : PhaseObservable :=
  fun r => phaseOperator r (f (nextPhase r))

def iterate : Nat → PhaseObservable → PhaseObservable
  | 0, f => f
  | n + 1, f => transfer (iterate n f)

/-- All nine components act on the same field. Every starting phase gives
the same joint renewal rule on its own returned fibre. -/
theorem ninefold_joint_renewal (f : PhaseObservable) (r : Fin 9) :
    iterate 9 f r = renewal (f r) := by
  fin_cases r <;>
    simp [iterate, transfer, nextPhase, phaseOperator, phase_mode_values,
      show (-1 : ℚ) ≠ 1 by norm_num,
      additive_multiplicative, multiplicative_additive,
      additive_renewal, multiplicative_renewal]

def pointIndicator (v : Fibre) : Observable := fun u => if u = v then 1 else 0

theorem renewal_point_weight (v u : Fibre) : renewal (pointIndicator v) u = 1 / 468 := by
  rcases v with ⟨a,b⟩
  have h (x : Fin 18) :
      (∑ y : Fin 26, if (x,y) = (a,b) then (1 : ℚ) else 0) =
        if x = a then 1 else 0 := by
    by_cases hx : x = a
    · subst x
      simp
    · simp [Prod.mk.injEq, hx]
  simp only [renewal, pointIndicator, h]
  simp

theorem ninefold_full_support (r : Fin 9) (v u : Fibre) :
    iterate 9 (fun _ => pointIndicator v) r u = 1 / 468 := by
  rw [ninefold_joint_renewal]
  exact renewal_point_weight v u

/-- A single selected output cannot reproduce the full-fibre renewal. -/
theorem renewal_not_point_evaluation (u v : Fibre) :
    renewal (pointIndicator v) u ≠ pointIndicator v v := by
  rw [renewal_point_weight]
  norm_num [pointIndicator]

end HMT.I.NonadicJointRenewal

#print axioms HMT.I.NonadicJointRenewal.emittedWord_mem
#print axioms HMT.I.NonadicJointRenewal.ninefold_joint_renewal
#print axioms HMT.I.NonadicJointRenewal.ninefold_full_support
#print axioms HMT.I.NonadicJointRenewal.renewal_not_point_evaluation
