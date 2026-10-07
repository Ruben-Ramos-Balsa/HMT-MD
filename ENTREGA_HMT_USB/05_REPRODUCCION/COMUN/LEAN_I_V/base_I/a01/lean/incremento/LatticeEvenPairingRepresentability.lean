import LatticeUntwistedPairing
import GradedPairingRepresentability
import LatticeEvenGrading

/-! Nondegeneracy and homogeneous representability on the actual untwisted
fixed space. Finiteness of its homogeneous components is inherited from the
constructed lattice carrier, not assumed as self-duality of the target. -/

noncomputable section
set_option synthInstance.maxHeartbeats 200000
namespace HMT.IV.LatticeEvenPairingRepresentability
open LatticeOscillatorFock LatticeParityCarrier LatticeEvenVertexFields
open LatticeEvenGrading LatticeEvenConformal LatticeUntwistedPairing

def evenPairing (o : Fin 12) : LinearMap.BilinForm ℂ (evenSpace o) :=
  (untwistedPairing o).restrict (evenSpace o)

theorem evenPairing_apply (o : Fin 12) (u v : evenSpace o) :
    evenPairing o u v = untwistedPairing o u.val v.val := rfl

theorem evenPairing_vacuum (o : Fin 12) :
    evenPairing o (evenVacuum o) (evenVacuum o) = 1 :=
  untwistedPairing_vacuum o

theorem untwistedPairing_evenProjector (o : Fin 12) (u : evenSpace o)
    (v : LatticeCarrier o) :
    untwistedPairing o u.val (evenProjector o v) = untwistedPairing o u.val v := by
  have hu := (mem_evenSpace o u.val).mp u.property
  simp only [evenProjector, LinearMap.smul_apply, LinearMap.add_apply,
    LinearMap.id_apply, map_smul, map_add]
  rw [← untwistedPairing_theta, hu]
  module

theorem evenPairing_nondegenerate (o : Fin 12) : (evenPairing o).Nondegenerate := by
  intro u hu
  apply Subtype.ext
  apply untwistedPairing_nondegenerate o
  intro v
  have h := hu (⟨evenProjector o v, evenProjector_mem o v⟩ : evenSpace o)
  change untwistedPairing o u.val (evenProjector o v) = 0 at h
  rw [untwistedPairing_evenProjector] at h
  exact h

theorem evenPairing_energy (o : Fin 12) (u v : evenSpace o) :
    evenPairing o (evenConformalMode o 0 u) v =
      evenPairing o u (evenConformalMode o 0 v) := by
  simp only [evenPairing_apply, evenConformalMode_zero_energy]
  exact untwistedPairing_energy o u.val v.val

def evenWeightPairing (o : Fin 12) (d : ℕ) :
    LinearMap.BilinForm ℂ (evenWeightSpace o d) :=
  (evenPairing o).restrict (evenWeightSpace o d)

theorem evenWeightPairing_nondegenerate (o : Fin 12) (d : ℕ) :
    (evenWeightPairing o d).Nondegenerate := by
  exact GradedPairingRepresentability.weight_restrict_nondegenerate
    (evenPairing o) (evenConformalMode o 0) (evenPairing_nondegenerate o)
    (evenPairing_energy o) (even_weights_span o) d

def evenWeightDuality (o : Fin 12) (d : ℕ) :
    evenWeightSpace o d ≃ₗ[ℂ] Module.Dual ℂ (evenWeightSpace o d) := by
  letI : FiniteDimensional ℂ (evenWeightSpace o d) := even_weight_finite o d
  exact LinearMap.BilinForm.toDual (K := ℂ) (V := evenWeightSpace o d)
    (evenWeightPairing o d) (evenWeightPairing_nondegenerate o d)

def evenWeightRepresentative (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenWeightSpace o d)) : evenWeightSpace o d :=
  (evenWeightDuality o d).symm f

theorem evenWeightRepresentative_pair (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenWeightSpace o d)) (v : evenWeightSpace o d) :
    evenPairing o (evenWeightRepresentative o d f).val v.val = f v := by
  change (evenWeightDuality o d) ((evenWeightDuality o d).symm f) v = f v
  rw [LinearEquiv.apply_symm_apply]

theorem evenWeightRepresentative_unique (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenWeightSpace o d)) (u : evenWeightSpace o d)
    (hu : ∀ v : evenWeightSpace o d, evenPairing o u.val v.val = f v) :
    u = evenWeightRepresentative o d f := by
  apply (evenWeightDuality o d).injective
  apply LinearMap.ext
  intro v
  change evenPairing o u.val v.val =
    (evenWeightDuality o d) ((evenWeightDuality o d).symm f) v
  rw [LinearEquiv.apply_symm_apply]
  exact hu v

theorem evenPairing_orthogonal (o : Fin 12) (d e : ℕ)
    (u v : evenSpace o) (hu : u ∈ evenWeightSpace o d)
    (hv : v ∈ evenWeightSpace o e) (hde : d ≠ e) : evenPairing o u v = 0 :=
  GradedPairingRepresentability.orthogonal_weights (evenPairing o)
    (evenConformalMode o 0) (evenPairing_energy o)
    (Module.End.mem_eigenspace_iff.mp hu) (Module.End.mem_eigenspace_iff.mp hv) hde

def homogeneousRepresentative (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) : evenSpace o :=
  (evenWeightRepresentative o d (f.comp (evenWeightSpace o d).subtype)).val

theorem homogeneousRepresentative_mem (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenSpace o)) :
    homogeneousRepresentative o d f ∈ evenWeightSpace o d :=
  (evenWeightRepresentative o d (f.comp (evenWeightSpace o d).subtype)).property

theorem homogeneousRepresentative_pair (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenSpace o))
    (hf : ∀ e, e ≠ d → ∀ v ∈ evenWeightSpace o e, f v = 0)
    (v : evenSpace o) : evenPairing o (homogeneousRepresentative o d f) v = f v := by
  have hv : v ∈ ⨆ e : ℕ, evenWeightSpace o e := by
    rw [even_weights_span o]
    trivial
  refine Submodule.iSup_induction (evenWeightSpace o)
    (motive := fun v => evenPairing o (homogeneousRepresentative o d f) v = f v)
    hv ?_ ?_ ?_
  · intro e v he
    by_cases hed : e = d
    · subst e
      exact evenWeightRepresentative_pair o d
        (f.comp (evenWeightSpace o d).subtype) ⟨v,he⟩
    · rw [evenPairing_orthogonal o d e _ v (homogeneousRepresentative_mem o d f)
        he (Ne.symm hed), hf e hed v he]
  · simp only [map_zero]
  · intro x y hx hy
    simp only [map_add, hx, hy]

theorem homogeneousRepresentative_unique (o : Fin 12) (d : ℕ)
    (f : Module.Dual ℂ (evenSpace o))
    (hf : ∀ e, e ≠ d → ∀ v ∈ evenWeightSpace o e, f v = 0)
    (u : evenSpace o) (hu : ∀ v, evenPairing o u v = f v) :
    u = homogeneousRepresentative o d f := by
  have hi : Function.Injective (evenPairing o) :=
    LinearMap.ker_eq_bot.mp (evenPairing_nondegenerate o).ker_eq_bot
  apply hi
  apply LinearMap.ext
  intro v
  rw [hu v, homogeneousRepresentative_pair o d f hf v]

end HMT.IV.LatticeEvenPairingRepresentability
end
