import SelectedRegionalIncidence
import SelectedRadiusTDuality
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
The isotropic Lorentz screen of Article IV uses the same selected radial
lattice as Article I. Its integral hyperbolic plane is displayed explicitly:
orthogonal restriction removes the e-minus coordinate, and the subsequent
quotient removes the e-plus coordinate. This is not the rank-ten projection.
The coordinated product preserves its middle factor, hence intertwines its
duality. No FLM theorem or physical identification is postulated here.
-/

noncomputable section
namespace HMT.IV.LorentzScreen

set_option synthInstance.maxHeartbeats 200000

open HMT.I.SelectedRegionalIncidence HMT.I.PaleyCharacterConstruction
open HMT.IV.CoxeterNeighbor HMT.IV.NeighborLattice

abbrev SelectedLattice := neighborSubgroup wittCode selectedRadial

instance selected_finite : Module.Finite ℤ SelectedLattice := by
  rcases selected_incidence_lattice_properties with ⟨_, _, _, _, h, _⟩
  exact h

instance selected_free : Module.Free ℤ SelectedLattice := by
  rcases selected_incidence_lattice_properties with ⟨_, _, _, _, _, h, _⟩
  exact h

theorem selected_rank : Module.finrank ℤ SelectedLattice = 24 := by
  rcases selected_incidence_lattice_properties with ⟨_, _, _, _, _, _, h, _⟩
  exact h

abbrev LorentzLattice := SelectedLattice × (ℤ × ℤ)
abbrev OrthogonalCoordinates := SelectedLattice × ℤ

def ePlus : LorentzLattice := (0, 1, 0)
def eMinus : LorentzLattice := (0, 0, 1)

def lorentzPair (x y : LorentzLattice) : ℚ :=
  pairing x.1.val y.1.val + (x.2.1 : ℚ) * y.2.2 + (x.2.2 : ℚ) * y.2.1

@[simp] theorem pairing_ePlus (x : LorentzLattice) :
    lorentzPair x ePlus = (x.2.2 : ℚ) := by
  simp [lorentzPair, ePlus, pairing, localPair]

@[simp] theorem pairing_eMinus (x : LorentzLattice) :
    lorentzPair x eMinus = (x.2.1 : ℚ) := by
  simp [lorentzPair, eMinus, pairing, localPair]

theorem hyperbolic_plane : lorentzPair ePlus ePlus = 0 ∧
    lorentzPair eMinus eMinus = 0 ∧ lorentzPair ePlus eMinus = 1 ∧
    lorentzPair eMinus ePlus = 1 := by
  simp [lorentzPair, ePlus, eMinus, pairing, localPair]

def minusCoordinate : LorentzLattice →ₗ[ℤ] ℤ :=
  (LinearMap.snd ℤ ℤ ℤ).comp (LinearMap.snd ℤ SelectedLattice (ℤ × ℤ))

def orthogonalHyperplane : Submodule ℤ LorentzLattice := LinearMap.ker minusCoordinate

theorem mem_orthogonalHyperplane (x : LorentzLattice) :
    x ∈ orthogonalHyperplane ↔ lorentzPair x ePlus = 0 := by
  simp [orthogonalHyperplane, minusCoordinate, LinearMap.mem_ker]

def orthogonalCoordinates : OrthogonalCoordinates ≃ₗ[ℤ] orthogonalHyperplane where
  toFun x := ⟨(x.1, x.2, 0), by simp [orthogonalHyperplane, minusCoordinate]⟩
  invFun y := (y.val.1, y.val.2.1)
  left_inv x := rfl
  right_inv y := by
    apply Subtype.ext
    have h : y.val.2.2 = 0 := y.property
    exact Prod.ext rfl (Prod.ext rfl h.symm)
  map_add' x y := rfl
  map_smul' a x := by
    apply Subtype.ext
    simp

def q24 : OrthogonalCoordinates →ₗ[ℤ] SelectedLattice := LinearMap.fst ℤ _ _

theorem q24_surjective : Function.Surjective q24 := fun x => ⟨(x, 0), rfl⟩

theorem q24_kernel (x : OrthogonalCoordinates) :
    x ∈ LinearMap.ker q24 ↔ ∃ a : ℤ, x = (0, a) := by
  constructor
  · intro h
    exact ⟨x.2, Prod.ext h rfl⟩
  · rintro ⟨a, rfl⟩
    rfl

def isotropicLine : Submodule ℤ OrthogonalCoordinates := LinearMap.ker q24

abbrev LorentzQuotient := OrthogonalCoordinates ⧸ isotropicLine

def quotientEquiv : LorentzQuotient ≃ₗ[ℤ] SelectedLattice :=
  q24.quotKerEquivOfSurjective q24_surjective

@[simp] theorem quotientEquiv_mk (x : OrthogonalCoordinates) :
    quotientEquiv (Submodule.Quotient.mk x) = x.1 := rfl

theorem screen_ranks : Module.finrank ℤ LorentzLattice = 26 ∧
    Module.finrank ℤ orthogonalHyperplane = 25 ∧
    Module.finrank ℤ LorentzQuotient = 24 := by
  constructor
  · simp [LorentzLattice, Module.finrank_prod, selected_rank]
  constructor
  · rw [← orthogonalCoordinates.finrank_eq]
    simp [OrthogonalCoordinates, Module.finrank_prod, selected_rank]
  · rw [quotientEquiv.finrank_eq, selected_rank]

def q24Orthogonal : orthogonalHyperplane →ₗ[ℤ] SelectedLattice :=
  q24.comp orthogonalCoordinates.symm.toLinearMap

theorem q24Orthogonal_surjective : Function.Surjective q24Orthogonal := by
  intro x
  exact ⟨orthogonalCoordinates (x, 0), by simp [q24Orthogonal, q24]⟩

theorem q24Orthogonal_kernel (x : orthogonalHyperplane) :
    x ∈ LinearMap.ker q24Orthogonal ↔ ∃ a : ℤ, x.val = a • ePlus := by
  constructor
  · intro h
    have hx : x.val.1 = 0 := h
    have hz : x.val.2.2 = 0 := x.property
    refine ⟨x.val.2.1, ?_⟩
    simp only [ePlus, Prod.smul_mk, smul_zero, zsmul_eq_mul, mul_one]
    exact Prod.ext hx (Prod.ext rfl hz)
  · rintro ⟨a, h⟩
    change x.val.1 = 0
    rw [h]
    simp [ePlus]

def actualQuotientEquiv :
    (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal) ≃ₗ[ℤ] SelectedLattice :=
  q24Orthogonal.quotKerEquivOfSurjective q24Orthogonal_surjective

@[simp] theorem actualQuotientEquiv_mk (x : orthogonalHyperplane) :
    actualQuotientEquiv (Submodule.Quotient.mk x) = x.val.1 := rfl

abbrev ScalarDomain := {r : ℝ // 0 < r} × (ℤ × ℤ)

def scalarDuality (d : ScalarDomain) : ScalarDomain :=
  (⟨d.1.val⁻¹, inv_pos.mpr d.1.property⟩, d.2.swap)

theorem scalarDuality_involutive : Function.Involutive scalarDuality := by
  intro d
  apply Prod.ext
  · exact Subtype.ext (inv_inv d.1.val)
  · exact Prod.swap_swap d.2

theorem scalarDuality_energy (d : ScalarDomain) :
    FiniteWeyl.Duality.energyAt (scalarDuality d).1.val (scalarDuality d).2 =
      FiniteWeyl.Duality.energyAt d.1.val d.2 :=
  FiniteWeyl.Duality.energyAt_swap_inv d.1.val d.2

def EllipticDomain := {d : ScalarDomain //
  d.1.val = SelectedRadiusTDuality.radius ∨ d.1.val = SelectedRadiusTDuality.radius⁻¹}

def ellipticDuality (d : EllipticDomain) : EllipticDomain :=
  ⟨scalarDuality d.val, by
    rcases d.property with h | h
    · exact Or.inr (congrArg Inv.inv h)
    · exact Or.inl ((congrArg Inv.inv h).trans (inv_inv _))⟩

theorem ellipticDuality_involutive : Function.Involutive ellipticDuality := by
  intro d
  exact Subtype.ext (scalarDuality_involutive d.val)

theorem ellipticDuality_energy (d : EllipticDomain) :
    FiniteWeyl.Duality.energyAt (ellipticDuality d).val.1.val
      (ellipticDuality d).val.2 =
        FiniteWeyl.Duality.energyAt d.val.1.val d.val.2 := scalarDuality_energy d.val

/-- The first factor is supplied by the separately proved K-directed graph
screen. The selected integral lattice quotient is discharged here. -/
def productScreenEquiv {Q G D : Type*} (first : Q ≃ G) :
    (Q × D × LorentzQuotient) ≃ (G × D × SelectedLattice) :=
  first.prodCongr ((Equiv.refl D).prodCongr quotientEquiv.toEquiv)

def actualProductScreenEquiv {Q G D : Type*} (first : Q ≃ G) :
    (Q × D × (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal)) ≃
      (G × D × SelectedLattice) :=
  first.prodCongr ((Equiv.refl D).prodCongr actualQuotientEquiv.toEquiv)

def middleAction {Q D L : Type*} (T : D → D) (x : Q × D × L) : Q × D × L :=
  (x.1, T x.2.1, x.2.2)

theorem productScreen_intertwines {Q G D : Type*} (first : Q ≃ G)
    (T : D → D) (x : Q × D × LorentzQuotient) :
    productScreenEquiv first (middleAction T x) =
      middleAction T (productScreenEquiv first x) := rfl

theorem productScreen_preserves_middle {Q G D : Type*} (first : Q ≃ G)
    (x : Q × D × LorentzQuotient) :
    (productScreenEquiv first x).2.1 = x.2.1 := rfl

theorem actualProductScreen_intertwines {Q G D : Type*} (first : Q ≃ G)
    (T : D → D)
    (x : Q × D × (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal)) :
    actualProductScreenEquiv first (middleAction T x) =
      middleAction T (actualProductScreenEquiv first x) := rfl

theorem elliptic_screen_intertwines {Q G : Type*} (first : Q ≃ G)
    (x : Q × EllipticDomain ×
      (orthogonalHyperplane ⧸ LinearMap.ker q24Orthogonal)) :
    actualProductScreenEquiv first (middleAction ellipticDuality x) =
      middleAction ellipticDuality (actualProductScreenEquiv first x) ∧
    FiniteWeyl.Duality.energyAt (ellipticDuality x.2.1).val.1.val
      (ellipticDuality x.2.1).val.2 =
        FiniteWeyl.Duality.energyAt x.2.1.val.1.val x.2.1.val.2 :=
  ⟨rfl, ellipticDuality_energy x.2.1⟩

/-- The elliptic radius and its energy transport are the existing selected
register realization, not a new unrestricted radius assumption. -/
theorem selected_radius_screen_energy {Q G : Type*} (first : Q ≃ G)
    (x : Q × (ℤ × ℤ) × LorentzQuotient) :
    FiniteWeyl.Duality.energyAt SelectedRadiusTDuality.radius⁻¹
        (productScreenEquiv first (middleAction Prod.swap x)).2.1 =
      FiniteWeyl.Duality.energyAt SelectedRadiusTDuality.radius x.2.1 := by
  exact SelectedRadiusTDuality.selected_energy_duality x.2.1

end HMT.IV.LorentzScreen
end

#print axioms HMT.IV.LorentzScreen.screen_ranks
#print axioms HMT.IV.LorentzScreen.quotientEquiv_mk
#print axioms HMT.IV.LorentzScreen.productScreen_intertwines
#print axioms HMT.IV.LorentzScreen.selected_radius_screen_energy
#print axioms HMT.IV.LorentzScreen.q24Orthogonal_kernel
#print axioms HMT.IV.LorentzScreen.actualQuotientEquiv_mk
#print axioms HMT.IV.LorentzScreen.ellipticDuality_energy
#print axioms HMT.IV.LorentzScreen.elliptic_screen_intertwines
