import LatticeTwistedNormalBounds

/-! Order independence of iterated divided half-normal products. Each double
sum has a proved pointwise finite rectangle before the order is exchanged.
The conclusion is an equality of the actual Laurent fields on Carrier,
not an assumed identity of a formal state-field map. -/
noncomputable section
namespace HMT.IV.LatticeTwistedNormalCommutation
open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedNormalDerivative LatticeTwistedNormalTerms
open LatticeTwistedNormalBounds LatticeFiniteDoubleSums
open scoped BigOperators

theorem creationTerm_normalField (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ)
    (v : Carrier o) (a : ℕ) :
    creationTerm o i n (derivativeNormalField o j m B) k a v =
      (∑ᶠ b, cc o i j n m B k v a b) +
      ∑ᶠ b, ca o i j n m B k v a b := by
  let L := creator o i n a
  have hc : L (∑ᶠ b, creationTerm o j m B (k+2*n-2*a+1) b v) =
      ∑ᶠ b, L (creationTerm o j m B (k+2*n-2*a+1) b v) :=
    L.toAddMonoidHom.map_finsum (creationTerm_finite o j m B (k+2*n-2*a+1) v)
  have ha : L (∑ᶠ b, annihilationTerm o j m B (k+2*n-2*a+1) b v) =
      ∑ᶠ b, L (annihilationTerm o j m B (k+2*n-2*a+1) b v) :=
    L.toAddMonoidHom.map_finsum (annihilationTerm_finite o j m B (k+2*n-2*a+1) v)
  rw [creationTerm_apply, derivativeNormalField_coefficient]
  change L (normalCoefficient o j m B (k+2*n-2*a+1) v) = _
  rw [normalCoefficient_apply, map_add, hc, ha]
  rfl

theorem annihilationTerm_normalField (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ)
    (v : Carrier o) (a : ℕ) :
    annihilationTerm o i n (derivativeNormalField o j m B) k a v =
      (∑ᶠ b, ac o i j n m B k v a b) +
      ∑ᶠ b, aa o i j n m B k v a b := by
  rw [annihilationTerm_apply, derivativeNormalField_coefficient, normalCoefficient_apply]
  rfl

theorem normalCoefficient_four_terms (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    normalCoefficient o i n (derivativeNormalField o j m B) k v =
      ((∑ᶠ a, ∑ᶠ b, cc o i j n m B k v a b) +
       ∑ᶠ a, ∑ᶠ b, ca o i j n m B k v a b) +
      ((∑ᶠ a, ∑ᶠ b, ac o i j n m B k v a b) +
       ∑ᶠ a, ∑ᶠ b, aa o i j n m B k v a b) := by
  obtain ⟨Nc, Mc, hcc, _⟩ := cc_rectangle o i j n m B k v
  obtain ⟨Na, Ma, hca, _⟩ := ca_rectangle o i j n m B k v
  obtain ⟨Nb, Mb, hac, _⟩ := ac_rectangle o i j n m B k v
  obtain ⟨Nd, Md, haa, _⟩ := aa_rectangle o i j n m B k v
  rw [normalCoefficient_apply]
  simp only [creationTerm_normalField, annihilationTerm_normalField]
  rw [finsum_add_distrib (finite_support_row_sums _ Nc hcc)
      (finite_support_row_sums _ Na hca),
    finsum_add_distrib (finite_support_row_sums _ Nb hac)
      (finite_support_row_sums _ Nd haa)]

theorem normalCoefficient_commute (o : Fin 12) (i j : Fin (BasisSize o))
    (n m : ℕ) (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    normalCoefficient o i n (derivativeNormalField o j m B) k v =
      normalCoefficient o j m (derivativeNormalField o i n B) k v := by
  rw [normalCoefficient_four_terms, normalCoefficient_four_terms]
  obtain ⟨Nc, Mc, hcc, hcc'⟩ := cc_rectangle o i j n m B k v
  obtain ⟨Na, Ma, hca, hca'⟩ := ca_rectangle o i j n m B k v
  obtain ⟨Nb, Mb, hac, hac'⟩ := ac_rectangle o i j n m B k v
  obtain ⟨Nd, Md, haa, haa'⟩ := aa_rectangle o i j n m B k v
  rw [finsum_comm_of_rectangle _ Nc Mc hcc hcc',
    finsum_comm_of_rectangle _ Na Ma hca hca',
    finsum_comm_of_rectangle _ Nb Mb hac hac',
    finsum_comm_of_rectangle _ Nd Md haa haa']
  simp only [cc_swap o i j n m B k v, ca_swap o i j n m B k v,
    ac_swap o i j n m B k v, aa_swap o i j n m B k v]
  abel

theorem derivativeNormalField_commute (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (j : Fin (BasisSize o)) (m : ℕ) (B : VertexOperator ℂ (Carrier o)) :
    derivativeNormalField o i n (derivativeNormalField o j m B) =
      derivativeNormalField o j m (derivativeNormalField o i n B) := by
  apply VertexOperator.ext
  intro v
  apply (HahnModule.of ℂ).symm.injective
  apply HahnSeries.ext
  funext k
  change normalCoefficient o i n (derivativeNormalField o j m B) k v =
    normalCoefficient o j m (derivativeNormalField o i n B) k v
  exact normalCoefficient_commute o i j n m B k v

end HMT.IV.LatticeTwistedNormalCommutation
end

#print axioms HMT.IV.LatticeTwistedNormalCommutation.creationTerm_normalField
#print axioms HMT.IV.LatticeTwistedNormalCommutation.annihilationTerm_normalField
#print axioms HMT.IV.LatticeTwistedNormalCommutation.normalCoefficient_four_terms
#print axioms HMT.IV.LatticeTwistedNormalCommutation.normalCoefficient_commute
#print axioms HMT.IV.LatticeTwistedNormalCommutation.derivativeNormalField_commute
