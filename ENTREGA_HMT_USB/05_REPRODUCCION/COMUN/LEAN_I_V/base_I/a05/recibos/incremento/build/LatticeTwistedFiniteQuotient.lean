import WittCentralExtension
import WittNegationLift
import MarkedNeighborRank

/-! The finite quotient required by the negation-twisted construction.
It is obtained from the same integral basis and triangular cocycle. The
kernel is proved to be exactly the theta-displacement subgroup. This is
the finite group, not an assumed irreducible module or orbifold product. -/

noncomputable section
namespace HMT.IV.LatticeTwistedFiniteQuotient

open LatticeCocycle TwistedGroupAlgebra WittNegationLift

abbrev ParityVector (o : Fin 12) := Fin (BasisSize o) → ZMod 2
def FiniteExtension (o : Fin 12) := ZMod 2 × ParityVector o

instance finiteExtensionFintype (o : Fin 12) : Fintype (FiniteExtension o) :=
  inferInstanceAs (Fintype (ZMod 2 × ParityVector o))

def finiteMul (o : Fin 12) (a b : FiniteExtension o) : FiniteExtension o :=
  (a.1+b.1+TC.tau (parityGram o) a.2 b.2, a.2+b.2)

def finiteInv (o : Fin 12) (a : FiniteExtension o) : FiniteExtension o :=
  (-a.1-TC.tau (parityGram o) a.2 (-a.2), -a.2)

private theorem finiteMul_assoc (o : Fin 12) (a b c : FiniteExtension o) :
    finiteMul o (finiteMul o a b) c = finiteMul o a (finiteMul o b c) := by
  apply Prod.ext
  · dsimp [finiteMul]
    have h := TC.tau_cocycle (parityGram o) a.2 b.2 c.2
    linear_combination h
  · exact add_assoc _ _ _

private theorem finiteMul_one_left (o : Fin 12) (a : FiniteExtension o) :
    finiteMul o (0,0) a = a := by
  apply Prod.ext <;> simp [finiteMul, TC.tau_zero_left]

private theorem finiteMul_one_right (o : Fin 12) (a : FiniteExtension o) :
    finiteMul o a (0,0) = a := by
  apply Prod.ext <;> simp [finiteMul, TC.tau_zero_right]

private theorem finiteInv_mul (o : Fin 12) (a : FiniteExtension o) :
    finiteMul o (finiteInv o a) a = (0,0) := by
  have hn : -a.2 = a.2 := by funext i; exact ZMod.neg_eq_self_mod_two _
  apply Prod.ext
  · dsimp [finiteMul, finiteInv]
    rw [hn]
    ring
  · simp [finiteMul, finiteInv]

instance finiteExtensionGroup (o : Fin 12) : Group (FiniteExtension o) where
  mul := finiteMul o
  one := (0,0)
  inv := finiteInv o
  mul_assoc := finiteMul_assoc o
  one_mul := finiteMul_one_left o
  mul_one := finiteMul_one_right o
  inv_mul_cancel := finiteInv_mul o

def parityProjection (o : Fin 12) : Extension o →* FiniteExtension o where
  toFun a := (a.1, parityCoordinates o a.2)
  map_one' := by
    change (0,parityCoordinates o 0) = (0,0)
    rw [parityCoordinates_zero]
  map_mul' a b := by
    change (a.1+b.1+wittCocycle o a.2 b.2, parityCoordinates o (a.2+b.2)) =
      (a.1+b.1+TC.tau (parityGram o) (parityCoordinates o a.2)
        (parityCoordinates o b.2), parityCoordinates o a.2+parityCoordinates o b.2)
    rw [parityCoordinates_add]
    rfl

theorem parityCoordinates_surjective (o : Fin 12) :
    Function.Surjective (parityCoordinates o) := by
  intro v
  let x : Lattice o := (latticeBasis o).equivFun.symm (fun i => ((v i).val : ℤ))
  refine ⟨x, ?_⟩
  funext i
  have h : (latticeBasis o).repr x i = ((v i).val : ℤ) := by
    change (latticeBasis o).equivFun x i = _
    rw [LinearEquiv.apply_symm_apply]
  change ((latticeBasis o).repr x i : ZMod 2) = v i
  rw [h, Int.cast_natCast, ZMod.natCast_zmod_val]

theorem parityProjection_surjective (o : Fin 12) :
    Function.Surjective (parityProjection o) := by
  rintro ⟨s,v⟩
  obtain ⟨x,hx⟩ := parityCoordinates_surjective o v
  exact ⟨(s,x), Prod.ext rfl hx⟩

theorem parityCoordinates_zero_iff_double (o : Fin 12) (x : Lattice o) :
    parityCoordinates o x=0 ↔ ∃ y : Lattice o, x=(2:ℤ) • y := by
  constructor
  · intro hx
    have hd (i : Fin (BasisSize o)) : (2:ℤ) ∣ (latticeBasis o).repr x i := by
      apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).mp
      exact congrFun hx i
    let y : Lattice o := (latticeBasis o).equivFun.symm
      (fun i => (latticeBasis o).repr x i / 2)
    refine ⟨y, ?_⟩
    apply (latticeBasis o).equivFun.injective
    funext i
    change (latticeBasis o).repr x i =
      ((latticeBasis o).equivFun ((2:ℤ) • y)) i
    rw [map_smul, Pi.smul_apply]
    have hy : (latticeBasis o).equivFun y i = (latticeBasis o).repr x i / 2 := by
      rw [LinearEquiv.apply_symm_apply]
    rw [hy]
    change _ = 2 * (_ / 2)
    exact (Int.mul_ediv_cancel' (hd i)).symm
  · rintro ⟨y,rfl⟩
    funext i
    change (((latticeBasis o).repr ((2:ℤ) • y) i : ℤ) : ZMod 2)=0
    rw [map_smul]
    change ((2*((latticeBasis o).repr y i) : ℤ) : ZMod 2)=0
    have h2 : ((2:ℤ):ZMod 2)=0 :=
      (ZMod.intCast_zmod_eq_zero_iff_dvd 2 2).mpr (dvd_refl _)
    rw [Int.cast_mul, h2, zero_mul]

def extensionTheta (o : Fin 12) : Extension o ≃* Extension o where
  toFun a := (a.1,-a.2)
  invFun a := (a.1,-a.2)
  left_inv a := by apply Prod.ext <;> simp
  right_inv a := by apply Prod.ext <;> simp
  map_mul' a b := by
    change (a.1+b.1+wittCocycle o a.2 b.2, -(a.2+b.2)) =
      (a.1+b.1+wittCocycle o (-a.2) (-b.2), -a.2 + -b.2)
    rw [wittCocycle_neg_neg, neg_add]

theorem theta_displacement (o : Fin 12) (a : Extension o) :
    extensionTheta o a * a⁻¹ = (0, -(2:ℤ) • a.2) := by
  have hp := parityCoordinates_neg o a.2
  change (a.1+(-a.1-wittCocycle o a.2 (-a.2))+
    wittCocycle o (-a.2) (-a.2), -a.2 + -a.2) = _
  apply Prod.ext
  · simp only [wittCocycle, hp]
    ring
  · module

theorem parityProjection_kernel (o : Fin 12) (a : Extension o) :
    a ∈ (parityProjection o).ker ↔ ∃ b : Extension o, a=extensionTheta o b*b⁻¹ := by
  change (a.1,parityCoordinates o a.2) = (0,0) ↔ _
  constructor
  · intro ha
    have hs := congrArg Prod.fst ha
    obtain ⟨y,hy⟩ := (parityCoordinates_zero_iff_double o a.2).mp (congrArg Prod.snd ha)
    refine ⟨(0,-y), ?_⟩
    rw [theta_displacement]
    apply Prod.ext
    · exact hs
    · simpa using hy
  · rintro ⟨b,rfl⟩
    rw [theta_displacement]
    change (0,parityCoordinates o (-(2:ℤ) • b.2)) = (0,0)
    apply Prod.ext (show (0 : ZMod 2)=0 from rfl)
    apply (parityCoordinates_zero_iff_double o _).mpr
    exact ⟨-b.2, by module⟩

/-- The quotient uses its proved theta-displacement kernel. -/
def thetaQuotientEquiv (o : Fin 12) :
    Extension o ⧸ (parityProjection o).ker ≃* FiniteExtension o :=
  QuotientGroup.quotientKerEquivOfSurjective (parityProjection o) (parityProjection_surjective o)

theorem finiteExtension_card (o : Fin 12) :
    Fintype.card (FiniteExtension o) = 2^(BasisSize o+1) := by
  change Fintype.card (ZMod 2 × (Fin (BasisSize o) → ZMod 2)) = _
  simp only [Fintype.card_prod, Fintype.card_fun, ZMod.card, Fintype.card_fin]
  rw [pow_succ, mul_comm]

theorem finiteExtension_card_rank24 (o : Fin 12) :
    Fintype.card (FiniteExtension o)=2^25 := by
  have hr : BasisSize o=24 := NeighborRank.witt_marked_integer_rank o
  rw [finiteExtension_card, hr]

end HMT.IV.LatticeTwistedFiniteQuotient
end

#print axioms HMT.IV.LatticeTwistedFiniteQuotient.finiteExtensionGroup
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.parityProjection
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.parityCoordinates_surjective
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.parityProjection_surjective
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.parityCoordinates_zero_iff_double
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.extensionTheta
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.theta_displacement
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.parityProjection_kernel
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.thetaQuotientEquiv
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.finiteExtension_card
#print axioms HMT.IV.LatticeTwistedFiniteQuotient.finiteExtension_card_rank24
