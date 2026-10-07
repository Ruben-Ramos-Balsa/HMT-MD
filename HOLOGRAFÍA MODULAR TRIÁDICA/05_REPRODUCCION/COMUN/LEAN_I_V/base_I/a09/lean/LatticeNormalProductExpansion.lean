import LatticeNormalProductTerms
import LatticeFiniteDoubleSums

/-! Expansion of nested normal products using pointwise finite sums. -/
noncomputable section
namespace HMT.IV.LatticeNormalProductExpansion
open HMT.IV.LatticeCocycle HMT.IV.LatticeOscillatorFock
open HMT.IV.LatticeHeisenbergModes HMT.IV.LatticeNormalOrderedField
open HMT.IV.LatticeNormalProductTerms HMT.IV.LatticeFiniteDoubleSums
open scoped BigOperators

theorem creationTerm_normalField (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ)
    (v : LatticeCarrier o) (a : ℕ) :
    creationTerm o i n (normalField o j m B) k a v =
      (∑ᶠ b, cc o i j n m B k v a b) +
      ∑ᶠ b, ca o i j n m B k v a b := by
  let L : Module.End ℂ (LatticeCarrier o) :=
    (Nat.choose (a+n) n : ℂ) • onCarrier o (create o (a+n) i)
  have hc : L (∑ᶠ b, creationTerm o j m B (k-a) b v) =
      ∑ᶠ b, L (creationTerm o j m B (k-a) b v) :=
    L.toAddMonoidHom.map_finsum (creationTerm_finite o j m B (k-a) v)
  have ha : L (∑ᶠ b, annihilationTerm o j m B (k-a) b v) =
      ∑ᶠ b, L (annihilationTerm o j m B (k-a) b v) :=
    L.toAddMonoidHom.map_finsum (annihilationTerm_finite o j m B (k-a) v)
  change L (normalCoefficient o j m B (k-a) v) = _
  rw [normalCoefficient_apply, map_add, hc, ha]
  rfl

theorem annihilationTerm_normalField (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (LatticeCarrier o)) (k : ℤ)
    (v : LatticeCarrier o) (a : ℕ) :
    annihilationTerm o i n (normalField o j m B) k a v =
      (∑ᶠ b, ac o i j n m B k v a b) +
      ∑ᶠ b, aa o i j n m B k v a b := by
  change ((-1 : ℂ)^n * (Nat.choose (a+n) n : ℂ)) •
    normalCoefficient o j m B (k+a+n+1) (hmode o i (a : ℤ) v) = _
  rw [normalCoefficient_apply, smul_add]
  rw [smul_finsum' _ (creationTerm_finite o j m B (k+a+n+1) _),
    smul_finsum' _ (annihilationTerm_finite o j m B (k+a+n+1) _)]
  rfl

end HMT.IV.LatticeNormalProductExpansion
end

#print axioms HMT.IV.LatticeNormalProductExpansion.creationTerm_normalField
#print axioms HMT.IV.LatticeNormalProductExpansion.annihilationTerm_normalField
