import ReturnSeries
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.Powerset

/-! Marked hexad/octad flags and the oriented twelve-sector chain.
The multiplicities are read from the chain before computing its pole. -/
noncomputable section
namespace HMT.OrientedReturn
open Filter Set
open scoped Topology BigOperators

abbrev MarkedPair := {s : Finset (Fin 6) // s.card = 2}
abbrev HexadFlags := Fin 6 × MarkedPair
abbrev OctadFlags := Fin 8 × MarkedPair

theorem markedPair_cardinal : Fintype.card MarkedPair = 15 := by decide
theorem hexadFlags_cardinal : Fintype.card HexadFlags = 90 := by
  simp only [HexadFlags, Fintype.card_prod, Fintype.card_fin, markedPair_cardinal]
theorem octadFlags_cardinal : Fintype.card OctadFlags = 120 := by
  simp only [OctadFlags, Fintype.card_prod, Fintype.card_fin, markedPair_cardinal]

def flagInclusion (p : HexadFlags) : OctadFlags := (p.1.castLE (by decide), p.2)

theorem flagInclusion_injective : Function.Injective flagInclusion := by
  intro p q h
  apply Prod.ext
  · apply Fin.ext
    exact congrArg (fun x : OctadFlags => x.1.val) h
  · exact congrArg (fun x : OctadFlags => x.2) h

theorem normalized_incidence_defect :
    ((Fintype.card HexadFlags : ℝ) - Fintype.card OctadFlags) /
      (24 * Fintype.card MarkedPair) = -(1 : ℝ) / 12 := by
  rw [hexadFlags_cardinal, octadFlags_cardinal, markedPair_cardinal]
  norm_num

abbrev Event := Sum (Fin 12) Unit
abbrev Chain := Event → ℤ

def fundamentalChain : Chain := Sum.elim (fun _ => 1) (fun _ => -1)

theorem fundamentalChain_generators :
    fundamentalChain = (∑ j : Fin 12, Pi.single (Sum.inl j) (1 : ℤ)) -
      Pi.single (Sum.inr ()) 1 := by
  funext e
  cases e with
  | inl j => simp [fundamentalChain, Pi.single_apply]
  | inr u => cases u; simp [fundamentalChain, Pi.single_apply]

def chainReader (q : ℝ) (c : Chain) : ℝ :=
  (∑ j : Fin 12, (c (.inl j) : ℝ) * returnSeries 90 q) +
    (c (.inr ()) : ℝ) * returnSeries 120 q

theorem chainReader_add (q : ℝ) (c d : Chain) :
    chainReader q (c + d) = chainReader q c + chainReader q d := by
  simp only [chainReader, Pi.add_apply, Int.cast_add, add_mul, Finset.sum_add_distrib]
  ring

theorem chainReader_neg (q : ℝ) (c : Chain) :
    chainReader q (-c) = -chainReader q c := by
  simp only [chainReader, Pi.neg_apply, Int.cast_neg, neg_mul, Finset.sum_neg_distrib]
  ring

theorem chainReader_fundamental (q : ℝ) :
    chainReader q fundamentalChain = fundamentalReturn q := by
  simp [chainReader, fundamentalChain, fundamentalReturn]
  ring

theorem chainReader_fundamental_pole :
    Tendsto (fun q : ℝ => (1 - q) * chainReader q fundamentalChain)
      (𝓝[<] 1) (𝓝 ((1 : ℝ) / 24)) := by
  simpa only [chainReader_fundamental] using fundamentalReturn_pole

#print axioms markedPair_cardinal
#print axioms flagInclusion_injective
#print axioms normalized_incidence_defect
#print axioms fundamentalChain_generators
#print axioms chainReader_fundamental
#print axioms chainReader_fundamental_pole
end HMT.OrientedReturn
