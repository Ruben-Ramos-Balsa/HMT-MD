import LatticeConformalEnergy

/-! Commutation of the constructed quadratic conformal modes with the
actual Heisenberg modes. The calculation uses the inherited CCR and the
pointwise finite normal-ordered sums, not a Virasoro relation as input. -/
noncomputable section
namespace HMT.IV.LatticeConformalHeisenberg
open LatticeCocycle LatticeOscillatorFock LatticeHeisenbergModes
open LatticeHeisenbergField LatticeNormalOrderedField LatticeConformalState
open LatticeConformalCoefficient LatticeGramDual LatticeGramSymmetry
open scoped BigOperators

theorem creationTerm_heisenberg (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) :
    creationTerm o i 0 (heisenbergField o j) (-m-2) a =
      (hmode o i (-(a:ℤ)-1)).comp (hmode o j (m+a+1)) := by
  simp only [creationTerm, Nat.add_zero, Nat.choose_zero_right, Nat.cast_one, one_smul]
  have hneg : -(a:ℤ)-1=Int.negSucc a := by omega
  rw [hneg, hmode_negSucc]
  change (onCarrier o (create o a i)).comp (hmode o j (-(-m-2-a)-1)) = _
  congr 2
  omega

theorem annihilationTerm_heisenberg (o : Fin 12) (i j : Fin (BasisSize o))
    (m : ℤ) (a : ℕ) :
    annihilationTerm o i 0 (heisenbergField o j) (-m-2) a =
      (hmode o j (m-a)).comp (hmode o i (a:ℤ)) := by
  simp only [annihilationTerm, Nat.add_zero, Nat.choose_zero_right, Nat.cast_one,
    pow_zero, one_mul, one_smul, Nat.cast_zero, add_zero]
  change (hmode o j (-(-m-2+a+1)-1)).comp (hmode o i (a:ℤ)) = _
  congr 2
  omega

theorem product_commutator (o : Fin 12) (i j t : Fin (BasisSize o))
    (a b n : ℤ) (v : LatticeCarrier o) :
    hmode o i a (hmode o j b (hmode o t n v)) -
      hmode o t n (hmode o i a (hmode o j b v)) =
    (if b+n=0 then (b:ℂ)*gram o j t else 0) • hmode o i a v +
      (if a+n=0 then (a:ℂ)*gram o i t else 0) • hmode o j b v := by
  have h1 := congrArg (hmode o i a) (heisenberg_relation_apply o j t b n v)
  simp only [map_sub, map_smul] at h1
  have h2 := heisenberg_relation_apply o i t a n (hmode o j b v)
  rw [← h1, ← h2]
  abel

theorem finsum_integer_delta {V : Type*} [AddCommGroup V] (r : ℤ) (v : V) :
    (∑ᶠ a : ℕ, if (a:ℤ)=r then v else 0) = if 0≤r then v else 0 := by
  classical
  by_cases hr : 0≤r
  · rw [if_pos hr]
    have heq (a : ℕ) : ((a:ℤ)=r) ↔ a=r.toNat := by omega
    simp_rw [heq]
    rw [finsum_eq_single _ r.toNat (by intro a ha; simp [ha])]
    simp
  · rw [if_neg hr]
    have hz (a : ℕ) : ¬(a:ℤ)=r := by omega
    simp [hz]

theorem integer_delta_finite {V : Type*} [Zero V] (r : ℤ) (v : V) :
    (Function.support (fun a : ℕ => if (a:ℤ)=r then v else 0)).Finite := by
  apply (Set.finite_singleton r.toNat).subset
  intro a ha
  have h : (a:ℤ)=r := by
    by_contra h
    exact ha (if_neg h)
  simp only [Set.mem_singleton_iff]
  omega

theorem creation_commutator_delta (o : Fin 12) (i j t : Fin (BasisSize o))
    (m n : ℤ) (a : ℕ) (v : LatticeCarrier o) :
    creationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v) -
      hmode o t n (creationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
    (if (a:ℤ)=-m-n-1 then (((-n:ℤ):ℂ)*gram o j t) • hmode o i (m+n) v else 0) +
    (if (a:ℤ)=n-1 then (((-n:ℤ):ℂ)*gram o i t) • hmode o j (m+n) v else 0) := by
  rw [creationTerm_heisenberg]
  simp only [LinearMap.comp_apply]
  rw [product_commutator]
  apply congrArg₂ (fun u w : LatticeCarrier o => u+w)
  · by_cases h : m+(a:ℤ)+1+n=0
    · have ha : (a:ℤ)=-m-n-1 := by omega
      rw [if_pos h, if_pos ha, show m+(a:ℤ)+1 = -n by omega,
        show -(a:ℤ)-1=m+n by omega]
    · have ha : ¬(a:ℤ)=-m-n-1 := by omega
      simp only [if_neg h, if_neg ha, zero_smul]
  · by_cases h : -(a:ℤ)-1+n=0
    · have ha : (a:ℤ)=n-1 := by omega
      rw [if_pos h, if_pos ha, show -(a:ℤ)-1 = -n by omega,
        show m+(a:ℤ)+1=m+n by omega]
    · have ha : ¬(a:ℤ)=n-1 := by omega
      simp only [if_neg h, if_neg ha, zero_smul]

theorem annihilation_commutator_delta (o : Fin 12) (i j t : Fin (BasisSize o))
    (m n : ℤ) (a : ℕ) (v : LatticeCarrier o) :
    annihilationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v) -
      hmode o t n (annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v) =
    (if (a:ℤ)=-n then (((-n:ℤ):ℂ)*gram o i t) • hmode o j (m+n) v else 0) +
    (if (a:ℤ)=m+n then (((-n:ℤ):ℂ)*gram o j t) • hmode o i (m+n) v else 0) := by
  rw [annihilationTerm_heisenberg]
  simp only [LinearMap.comp_apply]
  rw [product_commutator]
  apply congrArg₂ (fun u w : LatticeCarrier o => u+w)
  · by_cases h : (a:ℤ)+n=0
    · have ha : (a:ℤ)=-n := by omega
      rw [if_pos h, if_pos ha, ha, show m-(-n)=m+n by omega]
    · have ha : ¬(a:ℤ)=-n := by omega
      simp only [if_neg h, if_neg ha, zero_smul]
  · by_cases h : m-(a:ℤ)+n=0
    · have ha : (a:ℤ)=m+n := by omega
      rw [if_pos h, if_pos ha, show m-(a:ℤ)=-n by omega, ha]
    · have ha : ¬(a:ℤ)=m+n := by omega
      simp only [if_neg h, if_neg ha, zero_smul]

theorem finsum_commutator {V : Type*} [AddCommGroup V] [Module ℂ V]
    (f : ℕ → Module.End ℂ V)
    (hf : ∀ v, (Function.support (fun a => f a v)).Finite)
    (T : Module.End ℂ V) (v : V) :
    (∑ᶠ a, f a (T v)) - T (∑ᶠ a, f a v) =
      ∑ᶠ a, (f a (T v) - T (f a v)) := by
  have hT : (Function.support (fun a => T (f a v))).Finite := by
    apply (hf v).subset
    intro a ha
    intro hz
    change f a v=0 at hz
    exact ha (by change T (f a v)=0; rw [hz, map_zero])
  rw [finsum_sub_distrib (hf (T v)) hT]
  have hm : T (∑ᶠ a, f a v) = ∑ᶠ a, T (f a v) :=
    T.toAddMonoidHom.map_finsum (hf v)
  rw [hm]

theorem normalCoefficient_heisenberg_commutator (o : Fin 12)
    (i j t : Fin (BasisSize o)) (m n : ℤ) (v : LatticeCarrier o) :
    normalCoefficient o i 0 (heisenbergField o j) (-m-2) (hmode o t n v) -
      hmode o t n (normalCoefficient o i 0 (heisenbergField o j) (-m-2) v) =
      (((-n:ℤ):ℂ)*gram o j t) • hmode o i (m+n) v +
      (((-n:ℤ):ℂ)*gram o i t) • hmode o j (m+n) v := by
  rw [normalCoefficient_apply, normalCoefficient_apply, map_add]
  rw [show (∑ᶠ a, creationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v)) +
       (∑ᶠ a, annihilationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v)) -
       ((hmode o t n) (∑ᶠ a, creationTerm o i 0 (heisenbergField o j) (-m-2) a v) +
        (hmode o t n) (∑ᶠ a, annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v)) =
       ((∑ᶠ a, creationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v)) -
        (hmode o t n) (∑ᶠ a, creationTerm o i 0 (heisenbergField o j) (-m-2) a v)) +
       ((∑ᶠ a, annihilationTerm o i 0 (heisenbergField o j) (-m-2) a (hmode o t n v)) -
        (hmode o t n) (∑ᶠ a, annihilationTerm o i 0 (heisenbergField o j) (-m-2) a v)) by abel]
  rw [finsum_commutator _ (creationTerm_finite o i 0 (heisenbergField o j) (-m-2)),
    finsum_commutator _ (annihilationTerm_finite o i 0 (heisenbergField o j) (-m-2))]
  simp_rw [creation_commutator_delta, annihilation_commutator_delta]
  rw [finsum_add_distrib (integer_delta_finite _ _) (integer_delta_finite _ _),
    finsum_add_distrib (integer_delta_finite _ _) (integer_delta_finite _ _)]
  simp_rw [finsum_integer_delta]
  split_ifs <;> first | omega | abel

theorem gram_contract_modes (o : Fin 12) (t : Fin (BasisSize o))
    (c : ℂ) (w : Fin (BasisSize o) → LatticeCarrier o) :
    (∑ i, ∑ j, gramInv o i j • ((c*gram o j t) • w i)) = c • w t := by
  classical
  simp only [smul_smul]
  have inner (i : Fin (BasisSize o)) :
      (∑ j, (gramInv o i j * (c*gram o j t)) • w i) =
      (c*(if i=t then 1 else 0)) • w i := by
    rw [← Finset.sum_smul]
    congr 1
    calc
      _ = c * ∑ j, gramInv o i j * gram o j t := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intros
        ring
      _ = _ := by rw [gramInv_pairing]
  simp_rw [inner]
  simp

theorem gram_contract_modes_swapped (o : Fin 12) (t : Fin (BasisSize o))
    (c : ℂ) (w : Fin (BasisSize o) → LatticeCarrier o) :
    (∑ i, ∑ j, gramInv o i j • ((c*gram o i t) • w j)) = c • w t := by
  rw [Finset.sum_comm]
  have h : (∑ j, ∑ i, gramInv o i j • ((c*gram o i t) • w j)) =
      ∑ j, ∑ i, gramInv o j i • ((c*gram o i t) • w j) := by
    apply Finset.sum_congr rfl
    intro j _
    apply Finset.sum_congr rfl
    intro i _
    rw [gramInv_symmetric o i j]
  rw [h, gram_contract_modes]

theorem conformalMode_heisenberg_commutator_apply (o : Fin 12)
    (t : Fin (BasisSize o)) (m n : ℤ) (v : LatticeCarrier o) :
    conformalMode o m (hmode o t n v) - hmode o t n (conformalMode o m v) =
      ((-n:ℤ):ℂ) • hmode o t (m+n) v := by
  classical
  rw [conformalMode_normal_sum_apply, conformalMode_normal_sum_apply]
  have combine :
      (2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j •
        normalCoefficient o i 0 (heisenbergField o j) (-m-2) (hmode o t n v)) -
      hmode o t n ((2:ℂ)⁻¹ • (∑ i, ∑ j, gramInv o i j •
        normalCoefficient o i 0 (heisenbergField o j) (-m-2) v)) =
      (2:ℂ)⁻¹ • ∑ i, ∑ j, gramInv o i j •
        (normalCoefficient o i 0 (heisenbergField o j) (-m-2) (hmode o t n v) -
         hmode o t n (normalCoefficient o i 0 (heisenbergField o j) (-m-2) v)) := by
    simp only [map_smul, map_sum, smul_sub, Finset.sum_sub_distrib]
  rw [combine]
  simp_rw [normalCoefficient_heisenberg_commutator, smul_add, Finset.sum_add_distrib]
  rw [gram_contract_modes, gram_contract_modes_swapped]
  module

theorem conformalMode_heisenberg_commutator (o : Fin 12)
    (t : Fin (BasisSize o)) (m n : ℤ) :
    (conformalMode o m).comp (hmode o t n) - (hmode o t n).comp (conformalMode o m) =
      ((-n:ℤ):ℂ) • hmode o t (m+n) := by
  apply LinearMap.ext
  intro v
  exact conformalMode_heisenberg_commutator_apply o t m n v

end HMT.IV.LatticeConformalHeisenberg
end
#print axioms HMT.IV.LatticeConformalHeisenberg.creationTerm_heisenberg
#print axioms HMT.IV.LatticeConformalHeisenberg.annihilationTerm_heisenberg
#print axioms HMT.IV.LatticeConformalHeisenberg.product_commutator
#print axioms HMT.IV.LatticeConformalHeisenberg.finsum_integer_delta
#print axioms HMT.IV.LatticeConformalHeisenberg.integer_delta_finite
#print axioms HMT.IV.LatticeConformalHeisenberg.creation_commutator_delta
#print axioms HMT.IV.LatticeConformalHeisenberg.annihilation_commutator_delta
#print axioms HMT.IV.LatticeConformalHeisenberg.finsum_commutator
#print axioms HMT.IV.LatticeConformalHeisenberg.normalCoefficient_heisenberg_commutator
#print axioms HMT.IV.LatticeConformalHeisenberg.gram_contract_modes
#print axioms HMT.IV.LatticeConformalHeisenberg.gram_contract_modes_swapped
#print axioms HMT.IV.LatticeConformalHeisenberg.conformalMode_heisenberg_commutator_apply
#print axioms HMT.IV.LatticeConformalHeisenberg.conformalMode_heisenberg_commutator
