import AlphaCanonicalSection
import AlphaAnalyticChart

/-!
The two posterior publications of one supplied upstream state agree at every
dodecaphase depth. The analytic chart does not independently select that state.
All source enclosures on the periodic coordinate, precoordinate and link remain
explicit. The carry boundary is the constructed canonical boundary, not zero.
-/
noncomputable section

namespace AlphaPublications

def publication (register : RadixRecovery.K12) (n : Nat) :=
  AlphaCarry.close
    ((AlphaPositionalBridge.publishedBlocks register n).map AlphaCarry.InputBlock.balance)
    (AlphaCanonicalSection.registeredBoundary register n)

theorem root_publication (register : RadixRecovery.K12) (delta x : ℝ)
    (hk : AlphaCanonicalSection.InUnit (AlphaCarryLimit.Periodic.periodicValue register))
    (ha0 : 0 < AlphaAnalyticChart.precoordinate register)
    (ha1 : AlphaAnalyticChart.precoordinate register < AlphaAnalyticChart.radius)
    (hlambda : |AlphaAnalyticChart.stateLink register delta| ≤ AlphaAnalyticChart.lambdaBound)
    (hx : x ∈ Set.Ioo 0 AlphaAnalyticChart.radius)
    (hroot : AlphaAnalyticChart.stateChart register delta x = 0) (n : Nat) :
    (publication register n).outgoing = 0 ∧
      (publication register n).digits =
        (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat := by
  have hxa := (AlphaAnalyticChart.state_chart_root_iff register delta x
    ha0 ha1 hlambda hx).mp hroot
  have hav : AlphaCanonicalSection.InUnit (AlphaCarryLimit.value register) := by
    rw [← AlphaAnalyticChart.precoordinate_eq_carry_value]
    exact ⟨ha0.le,ha1.trans (by norm_num [AlphaAnalyticChart.radius])⟩
  have h := AlphaCanonicalSection.registered_canonical_closure register hk hav n
  simpa only [publication,hxa,AlphaAnalyticChart.precoordinate_eq_carry_value] using h

theorem root_publications_compatible (register : RadixRecovery.K12) (delta x : ℝ)
    (hk : AlphaCanonicalSection.InUnit (AlphaCarryLimit.Periodic.periodicValue register))
    (ha0 : 0 < AlphaAnalyticChart.precoordinate register)
    (ha1 : AlphaAnalyticChart.precoordinate register < AlphaAnalyticChart.radius)
    (hlambda : |AlphaAnalyticChart.stateLink register delta| ≤ AlphaAnalyticChart.lambdaBound)
    (hx : x ∈ Set.Ioo 0 AlphaAnalyticChart.radius)
    (hroot : AlphaAnalyticChart.stateChart register delta x = 0) (n m : Nat) :
    ((publication register (n+m)).digits).take (12*n) = (publication register n).digits := by
  rw [(root_publication register delta x hk ha0 ha1 hlambda hx hroot (n+m)).2,
    (root_publication register delta x hk ha0 ha1 hlambda hx hroot n).2,
    ← List.map_take,Nat.mul_add,AlphaCanonicalSection.digits_compatible]

/-- One and the same root carries all canonical dodecaphase publications. -/
theorem unique_root_with_all_publications (register : RadixRecovery.K12) (delta : ℝ)
    (hk : AlphaCanonicalSection.InUnit (AlphaCarryLimit.Periodic.periodicValue register))
    (ha0 : 0 < AlphaAnalyticChart.precoordinate register)
    (ha1 : AlphaAnalyticChart.precoordinate register < AlphaAnalyticChart.radius)
    (hlambda : |AlphaAnalyticChart.stateLink register delta| ≤ AlphaAnalyticChart.lambdaBound) :
    ∃! x : ℝ, x ∈ Set.Ioo 0 AlphaAnalyticChart.radius ∧
      AlphaAnalyticChart.stateChart register delta x = 0 ∧
      (∀ n : Nat, (publication register n).outgoing = 0 ∧
        (publication register n).digits =
          (AlphaCanonicalSection.digits x (12*n)).map Int.ofNat) := by
  have hx : AlphaAnalyticChart.precoordinate register ∈ Set.Ioo 0 AlphaAnalyticChart.radius :=
    ⟨ha0,ha1⟩
  have hroot := (AlphaAnalyticChart.state_chart_simple_root register delta ha0 ha1 hlambda).1
  refine ⟨AlphaAnalyticChart.precoordinate register,⟨hx,hroot,?_⟩,?_⟩
  · intro n
    exact root_publication register delta _ hk ha0 ha1 hlambda hx hroot n
  · intro x h
    exact (AlphaAnalyticChart.state_chart_root_iff register delta x ha0 ha1 hlambda h.1).mp h.2.1

end AlphaPublications
end

#print axioms AlphaPublications.root_publication
#print axioms AlphaPublications.root_publications_compatible
#print axioms AlphaPublications.unique_root_with_all_publications
