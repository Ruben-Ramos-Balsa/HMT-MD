import LatticeTwistedKernelParity
import LatticeTwistedPositiveSector

/-! Restriction of the charge-even ramified exponential kernel to the actual
positive twisted sector. Its invariance is the previously proved operator
identity, not a new hypothesis. This supplies Laurent fields on that sector;
it does not yet supply a state-field map for every even lattice state. -/

noncomputable section
namespace HMT.IV.LatticeTwistedPositiveKernel
open LatticeCocycle LatticeTwistedCarrier LatticeTwistedParity
open LatticeTwistedPositiveSector LatticeTwistedKernelParity
open LatticeTwistedExponentialKernel

theorem descendedCoefficient_mem_positive (o : Fin 12) (x : Lattice o)
    (s k : ℤ) (v : Carrier o) (hv : v ∈ positiveSector o) :
    descendedCoefficient o x s k v ∈ positiveSector o := by
  change liftedTheta o (descendedCoefficient o x s k v) = descendedCoefficient o x s k v
  have h := LinearMap.congr_fun (theta_evenKernelCoefficient o x s (2*k+s)) v
  change liftedTheta o (descendedCoefficient o x s k v) =
    descendedCoefficient o x s k (liftedTheta o v) at h
  rw [show liftedTheta o v = v from hv] at h
  exact h

def positiveCoefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    Module.End ℂ (positiveSector o) :=
  (descendedCoefficient o x s k).restrict
    (fun v hv => descendedCoefficient_mem_positive o x s k v hv)

theorem positiveCoefficient_coe (o : Fin 12) (x : Lattice o) (s k : ℤ)
    (v : positiveSector o) :
    (positiveCoefficient o x s k v).val = descendedCoefficient o x s k v.val := rfl

theorem positiveCoefficient_bounded_pole (o : Fin 12) (x : Lattice o) (s : ℤ)
    (v : positiveSector o) : ∃ b : ℤ, ∀ k < b, positiveCoefficient o x s k v = 0 := by
  obtain ⟨b,hb⟩ := descendedCoefficient_bounded_pole o x s v.val
  refine ⟨b, fun k hk => ?_⟩
  apply Subtype.ext
  exact hb k hk

def positiveKernel (o : Fin 12) (x : Lattice o) (s : ℤ) :
    VertexOperator ℂ (positiveSector o) :=
  VertexOperator.of_coeff (positiveCoefficient o x s)
    (positiveCoefficient_bounded_pole o x s)

theorem positiveKernel_coefficient (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    HVertexOperator.coeff (positiveKernel o x s) k = positiveCoefficient o x s k := by
  rfl

theorem positiveKernel_intertwines_inclusion (o : Fin 12) (x : Lattice o) (s k : ℤ) :
    (positiveSector o).subtype.comp (HVertexOperator.coeff (positiveKernel o x s) k) =
      (HVertexOperator.coeff (descendedEvenKernel o x s) k).comp (positiveSector o).subtype := by
  ext v
  rfl

theorem descendedCoefficient_shift_independent (o : Fin 12) (x : Lattice o)
    (s t k : ℤ) : descendedCoefficient o x s k = descendedCoefficient o x t k := by
  unfold descendedCoefficient
  rw [evenKernelCoefficient_even_shift, evenKernelCoefficient_even_shift]
  apply (LatticeTwistedLowWeights.twistedBasis o).ext
  rintro ⟨a,q⟩
  rw [kernelCoefficient_basis, kernelCoefficient_basis]
  simp only [basisKernelCoefficient, basisKernelCutoff, add_sub_cancel_right]

theorem positiveKernel_shift_independent (o : Fin 12) (x : Lattice o) (s t : ℤ) :
    positiveKernel o x s = positiveKernel o x t := by
  apply HVertexOperator.coeff_inj
  funext k
  rw [positiveKernel_coefficient, positiveKernel_coefficient]
  ext v
  exact LinearMap.congr_fun (descendedCoefficient_shift_independent o x s t k) v.val

end HMT.IV.LatticeTwistedPositiveKernel
end

#print axioms HMT.IV.LatticeTwistedPositiveKernel.positiveKernel_intertwines_inclusion
#print axioms HMT.IV.LatticeTwistedPositiveKernel.positiveKernel_shift_independent
