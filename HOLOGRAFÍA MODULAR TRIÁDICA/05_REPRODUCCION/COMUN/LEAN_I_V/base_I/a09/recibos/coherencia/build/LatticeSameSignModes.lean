import LatticeHeisenbergModes

/-!
Operator forms of the same-sign commutation laws already proved on the
generated marked-lattice carrier.  The nonnegative statement includes the
lattice zero mode; its vanishing commutator follows from the full CCR.
These identities are used to reorder the two same-sign factors in normal
products. No new lattice, pairing or commutation axiom is introduced.
-/

noncomputable section
namespace HMT.IV.LatticeSameSignModes

open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes

theorem creations_commute_operators (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) :
    (onCarrier o (create o n i)).comp (onCarrier o (create o m j)) =
      (onCarrier o (create o m j)).comp (onCarrier o (create o n i)) := by
  apply LinearMap.ext
  intro v
  exact carrier_creations_commute o n m i j v

theorem nonnegative_hmodes_commute (o : Fin 12)
    (i j : Fin (BasisSize o)) (a b : ℕ) :
    (hmode o i (a : ℤ)).comp (hmode o j (b : ℤ)) =
      (hmode o j (b : ℤ)).comp (hmode o i (a : ℤ)) := by
  apply sub_eq_zero.mp
  rw [heisenberg_relation]
  by_cases h : (a : ℤ)+(b : ℤ)=0
  · have ha : a = 0 := by omega
    simp [h, ha]
  · simp [h]

theorem creations_commute_before (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (B : Module.End ℂ (LatticeCarrier o)) :
    (onCarrier o (create o n i)).comp ((onCarrier o (create o m j)).comp B) =
      (onCarrier o (create o m j)).comp ((onCarrier o (create o n i)).comp B) := by
  rw [← LinearMap.comp_assoc, creations_commute_operators, LinearMap.comp_assoc]

theorem nonnegative_hmodes_commute_after (o : Fin 12)
    (i j : Fin (BasisSize o)) (a b : ℕ) (B : Module.End ℂ (LatticeCarrier o)) :
    B.comp ((hmode o i (a : ℤ)).comp (hmode o j (b : ℤ))) =
      B.comp ((hmode o j (b : ℤ)).comp (hmode o i (a : ℤ))) := by
  rw [nonnegative_hmodes_commute]

end HMT.IV.LatticeSameSignModes
end

#print axioms HMT.IV.LatticeSameSignModes.creations_commute_operators
#print axioms HMT.IV.LatticeSameSignModes.nonnegative_hmodes_commute
#print axioms HMT.IV.LatticeSameSignModes.creations_commute_before
#print axioms HMT.IV.LatticeSameSignModes.nonnegative_hmodes_commute_after
