import LatticeFiniteIrreducible
import LatticeFiniteDimension

/-! The finite ground-state factor of the negation-twisted construction.
It is a constituent of the inherited twisted regular action. Its dimension
and uniqueness follow from that action and the proved nondegenerate pairing.
The lattice operators retain the original cocycle and parity projection. -/

noncomputable section
namespace HMT.IV.LatticeFiniteGroundState
open CoxeterNeighbor LatticeCocycle LatticeTwistedFiniteQuotient
open LatticeFiniteRepresentation LatticeFiniteIrreducible
open LatticeFiniteCharacter LatticeFiniteDimension
open TwistedGroupAlgebra WittNegationLift CategoryTheory

theorem finiteSpace_dimension (o : Fin 12) :
    Module.finrank ℂ (FiniteSpace o) = 4096 :=
  irreducible_dimension o (finiteFDRep o) (constituent_central_involution_negative o)

theorem finiteSpace_unique (o : Fin 12) (W : FDRep ℂ (FiniteExtension o))
    [CategoryTheory.Simple W] (hW : W.ρ (1,0) = -1) :
    Nonempty (finiteFDRep o ≅ W) :=
  irreducible_unique o (finiteFDRep o) W
    (constituent_central_involution_negative o) hW

def parityOperator (o : Fin 12) (v : ParityVector o) :
    Module.End ℂ (FiniteSpace o) := constituentRepresentation o (parityLift o v)

theorem parityOperator_zero (o : Fin 12) : parityOperator o 0 = 1 := by
  change constituentRepresentation o 1 = 1
  exact map_one _

theorem parityOperator_product (o : Fin 12) (v w : ParityVector o) :
    parityOperator o v * parityOperator o w =
      complexSign (TC.tau (parityGram o) v w) • parityOperator o (v+w) := by
  have hg : parityLift o v * parityLift o w =
      centralElement o (TC.tau (parityGram o) v w) * parityLift o (v+w) := by
    apply Prod.ext
    · change 0+0+TC.tau (parityGram o) v w =
        TC.tau (parityGram o) v w + 0 + TC.tau (parityGram o) 0 (v+w)
      simp [TC.tau_zero_left]
    · change v+w=0+(v+w)
      exact (zero_add _).symm
  unfold parityOperator
  rw [← map_mul, hg, map_mul]
  have hz := constituent_center o (TC.tau (parityGram o) v w)
  change constituentRepresentation o (centralElement o (TC.tau (parityGram o) v w)) = _ at hz
  rw [hz, smul_mul_assoc, one_mul]

def latticeOperator (o : Fin 12) (x : Lattice o) :
    Module.End ℂ (FiniteSpace o) := parityOperator o (parityCoordinates o x)

theorem latticeOperator_product (o : Fin 12) (x y : Lattice o) :
    latticeOperator o x * latticeOperator o y =
      (wittSign o x y : ℂ) • latticeOperator o (x+y) := by
  simpa only [latticeOperator, parityCoordinates_add, complexSign, wittSign, wittCocycle]
    using parityOperator_product o (parityCoordinates o x) (parityCoordinates o y)

theorem latticeOperator_neg (o : Fin 12) (x : Lattice o) :
    latticeOperator o (-x) = latticeOperator o x := by
  unfold latticeOperator
  rw [parityCoordinates_neg]

theorem latticeOperator_zero (o : Fin 12) : latticeOperator o 0 = 1 := by
  rw [latticeOperator, parityCoordinates_zero, parityOperator_zero]

theorem latticeOperator_two_periodic (o : Fin 12) (x y : Lattice o) :
    latticeOperator o (x+(2:ℤ) • y) = latticeOperator o x := by
  unfold latticeOperator
  rw [parityCoordinates_add]
  have h := (parityCoordinates_zero_iff_double o ((2:ℤ) • y)).mpr ⟨y,rfl⟩
  rw [h, add_zero]

def extensionRepresentation (o : Fin 12) :
    Representation ℂ (Extension o) (FiniteSpace o) :=
  (constituentRepresentation o).comp (parityProjection o)

theorem extensionRepresentation_theta (o : Fin 12) (a : Extension o) :
    extensionRepresentation o (extensionTheta o a) = extensionRepresentation o a := by
  change constituentRepresentation o (a.1, parityCoordinates o (-a.2)) =
    constituentRepresentation o (a.1, parityCoordinates o a.2)
  rw [parityCoordinates_neg]

theorem displacement_acts_trivially (o : Fin 12) (a : Extension o) :
    extensionRepresentation o (extensionTheta o a * a⁻¹) = 1 := by
  have hk := (parityProjection_kernel o (extensionTheta o a * a⁻¹)).mpr ⟨a,rfl⟩
  change parityProjection o (extensionTheta o a * a⁻¹)=1 at hk
  change constituentRepresentation o (parityProjection o (extensionTheta o a * a⁻¹))=1
  rw [hk, map_one]

end HMT.IV.LatticeFiniteGroundState
end
