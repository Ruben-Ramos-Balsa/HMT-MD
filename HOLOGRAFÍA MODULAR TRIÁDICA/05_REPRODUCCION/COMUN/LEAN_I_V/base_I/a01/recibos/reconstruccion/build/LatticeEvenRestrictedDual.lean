import LatticeEvenPairingRepresentability

/-! Reconstruction in the actual even carrier from finitely many homogeneous
dual coordinates. The bound controls the functional, not a replacement carrier.
The contragredient consumer must prove its support bound; it is not presumed. -/

noncomputable section
namespace HMT.IV.LatticeEvenRestrictedDual
open LatticeEvenVertexFields LatticeEvenGrading LatticeEvenPairingRepresentability
open scoped BigOperators

def vanishesAbove (o : Fin 12) (N : ℕ) (f : Module.Dual ℂ (evenSpace o)) : Prop :=
  ∀ d, N ≤ d → ∀ v ∈ evenWeightSpace o d, f v = 0

def representativeBelow (o : Fin 12) (N : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) : evenSpace o :=
  ∑ d ∈ Finset.range N, homogeneousRepresentative o d f

theorem homogeneousRepresentative_pair_same (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) (v : evenSpace o)
    (hv : v ∈ evenWeightSpace o d) :
    evenPairing o (homogeneousRepresentative o d f) v = f v := by
  exact evenWeightRepresentative_pair o d
    (f.comp (evenWeightSpace o d).subtype) ⟨v,hv⟩

theorem representativeBelow_pair_weight (o : Fin 12) (N d : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) (v : evenSpace o)
    (hv : v ∈ evenWeightSpace o d) :
    evenPairing o (representativeBelow o N f) v = if d < N then f v else 0 := by
  classical
  simp only [representativeBelow, map_sum, LinearMap.sum_apply]
  by_cases hd : d < N
  · rw [if_pos hd, Finset.sum_eq_single d]
    · exact homogeneousRepresentative_pair_same o d f v hv
    · intro e _ hed
      exact evenPairing_orthogonal o e d _ v
        (homogeneousRepresentative_mem o e f) hv hed
    · intro h
      exact False.elim (h (Finset.mem_range.mpr hd))
  · rw [if_neg hd]
    apply Finset.sum_eq_zero
    intro e he
    exact evenPairing_orthogonal o e d _ v
      (homogeneousRepresentative_mem o e f) hv (by
        have heN := Finset.mem_range.mp he
        omega)

theorem representativeBelow_pair (o : Fin 12) (N : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) (hf : vanishesAbove o N f)
    (v : evenSpace o) : evenPairing o (representativeBelow o N f) v = f v := by
  have hv : v ∈ ⨆ d : ℕ, evenWeightSpace o d := by
    rw [even_weights_span o]
    trivial
  refine Submodule.iSup_induction (evenWeightSpace o)
    (motive := fun v => evenPairing o (representativeBelow o N f) v = f v)
    hv ?_ ?_ ?_
  · intro d v hd
    rw [representativeBelow_pair_weight o N d f v hd]
    split_ifs with h
    · rfl
    · exact (hf d (by omega) v hd).symm
  · simp only [map_zero]
  · intro x y hx hy
    simp only [map_add, hx, hy]

theorem representative_unique (o : Fin 12)
    (f : Module.Dual ℂ (evenSpace o)) (u v : evenSpace o)
    (hu : ∀ a, evenPairing o u a = f a)
    (hv : ∀ a, evenPairing o v a = f a) : u = v := by
  have hi : Function.Injective (evenPairing o) :=
    LinearMap.ker_eq_bot.mp (evenPairing_nondegenerate o).ker_eq_bot
  apply hi
  ext a
  exact (hu a).trans (hv a).symm

theorem representativeBelow_independent (o : Fin 12) (N M : ℕ)
    (f : Module.Dual ℂ (evenSpace o))
    (hN : vanishesAbove o N f) (hM : vanishesAbove o M f) :
    representativeBelow o N f = representativeBelow o M f :=
  representative_unique o f _ _
    (representativeBelow_pair o N f hN) (representativeBelow_pair o M f hM)

theorem vanishesAbove_mono (o : Fin 12) (N M : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) (hf : vanishesAbove o N f)
    (hNM : N ≤ M) : vanishesAbove o M f := by
  intro d hd v hv
  exact hf d (le_trans hNM hd) v hv

def boundedDual (o : Fin 12) : Submodule ℂ (Module.Dual ℂ (evenSpace o)) where
  carrier := {f | ∃ N, vanishesAbove o N f}
  zero_mem' := ⟨0, by intro d hd v hv; rfl⟩
  add_mem' := by
    rintro f g ⟨N,hf⟩ ⟨M,hg⟩
    refine ⟨max N M, ?_⟩
    intro d hd v hv
    simp only [LinearMap.add_apply, hf d (le_trans (le_max_left N M) hd) v hv,
      hg d (le_trans (le_max_right N M) hd) v hv, add_zero]
  smul_mem' := by
    rintro c f ⟨N,hf⟩
    refine ⟨N, ?_⟩
    intro d hd v hv
    simp only [LinearMap.smul_apply, hf d hd v hv, smul_zero]

def reconstruct (o : Fin 12) (f : boundedDual o) : evenSpace o :=
  representativeBelow o (Classical.choose f.property) f.val

theorem reconstruct_pair (o : Fin 12) (f : boundedDual o) (v : evenSpace o) :
    evenPairing o (reconstruct o f) v = f.val v :=
  representativeBelow_pair o _ f.val (Classical.choose_spec f.property) v

def reconstruction (o : Fin 12) : boundedDual o →ₗ[ℂ] evenSpace o where
  toFun := reconstruct o
  map_add' f g := by
    apply representative_unique o ((f+g).val)
    · exact reconstruct_pair o (f+g)
    · intro a
      simp only [map_add, LinearMap.add_apply, reconstruct_pair, Submodule.coe_add]
  map_smul' c f := by
    apply representative_unique o ((c • f).val)
    · exact reconstruct_pair o (c • f)
    · intro a
      simp only [map_smul, LinearMap.smul_apply, reconstruct_pair,
        Submodule.coe_smul, RingHom.id_apply]

theorem reconstruction_injective (o : Fin 12) : Function.Injective (reconstruction o) := by
  intro f g h
  apply Subtype.ext
  ext a
  have ha := congrArg (fun v => evenPairing o v a) h
  exact (reconstruct_pair o f a).symm.trans (ha.trans (reconstruct_pair o g a))

theorem pairing_has_bounded_weight_support (o : Fin 12) (u : evenSpace o) :
    ∃ N, vanishesAbove o N (evenPairing o u) := by
  have hu : u ∈ ⨆ d : ℕ, evenWeightSpace o d := by
    rw [even_weights_span o]
    trivial
  refine Submodule.iSup_induction (evenWeightSpace o)
    (motive := fun u => ∃ N, vanishesAbove o N (evenPairing o u)) hu ?_ ?_ ?_
  · intro d u hd
    refine ⟨d+1, ?_⟩
    intro e he v hv
    exact evenPairing_orthogonal o d e u v hd hv (by omega)
  · refine ⟨0, ?_⟩
    intro d hd v hv
    simp only [map_zero, LinearMap.zero_apply]
  · rintro x y ⟨N,hN⟩ ⟨M,hM⟩
    refine ⟨max N M, ?_⟩
    intro d hd v hv
    simp only [map_add, LinearMap.add_apply,
      hN d (le_trans (le_max_left N M) hd) v hv,
      hM d (le_trans (le_max_right N M) hd) v hv, add_zero]

def pairingEmbedding (o : Fin 12) : evenSpace o →ₗ[ℂ] boundedDual o where
  toFun u := ⟨evenPairing o u, pairing_has_bounded_weight_support o u⟩
  map_add' u v := by apply Subtype.ext; exact map_add (evenPairing o) u v
  map_smul' c u := by apply Subtype.ext; exact map_smul (evenPairing o) c u

theorem reconstruction_pairingEmbedding (o : Fin 12) (u : evenSpace o) :
    reconstruction o (pairingEmbedding o u) = u := by
  apply representative_unique o (evenPairing o u)
  · exact reconstruct_pair o (pairingEmbedding o u)
  · intro a
    rfl

theorem pairingEmbedding_reconstruction (o : Fin 12) (f : boundedDual o) :
    pairingEmbedding o (reconstruction o f) = f := by
  apply Subtype.ext
  ext a
  exact reconstruct_pair o f a

def restrictedDualEquivalence (o : Fin 12) : evenSpace o ≃ₗ[ℂ] boundedDual o where
  toFun := pairingEmbedding o
  invFun := reconstruction o
  left_inv := reconstruction_pairingEmbedding o
  right_inv := pairingEmbedding_reconstruction o
  map_add' := map_add (pairingEmbedding o)
  map_smul' := map_smul (pairingEmbedding o)

end HMT.IV.LatticeEvenRestrictedDual
end

#print axioms HMT.IV.LatticeEvenRestrictedDual.reconstruction
#print axioms HMT.IV.LatticeEvenRestrictedDual.representativeBelow_independent
#print axioms HMT.IV.LatticeEvenRestrictedDual.reconstruction_injective
#print axioms HMT.IV.LatticeEvenRestrictedDual.restrictedDualEquivalence
