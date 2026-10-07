import PositiveCongruence
import RefinedCharacter

/-!
Concrete bridge from the convergent refined character to the basal operator.
The reference mass, reference signature and reference tower data remain explicit.
Already-relative tower data use the separate `relativeBasal` interface, without
a second subtraction of the reference. No scalar calibration is changed here.
-/
namespace HMT.VI.MassOperator
noncomputable section

open HMTMassCharacter

variable {Route : Type*} [Fintype Route] [DecidableEq Route]
variable {s : ℕ → ℝ}

def refinedBasal (mRef : ℝ) (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) : End Route :=
  diagonal (fun γ => refinedBasalMass mRef X (σ γ) σRef (η γ) ηRef)

theorem refinedBasal_positive {mRef : ℝ} (hmRef : 0 < mRef)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) :
    (refinedBasal mRef X σ σRef η ηRef).IsPositive :=
  diagonal_positive _ (fun γ => (refinedBasalMass_pos hmRef X (σ γ) σRef (η γ) ηRef).le)

theorem refined_corrected_positive (Ract : ℝ) {mRef : ℝ} (hmRef : 0 < mRef)
    (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) :
    (corrected Ract κ r (refinedBasal mRef X σ σRef η ηRef)).IsPositive :=
  corrected_positive Ract κ r _ (refinedBasal_positive hmRef X σ σRef η ηRef)

theorem refined_corrected_basis {Ract : ℝ} (hR : 0 < Ract) (mRef : ℝ)
    (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) (γ : Route) :
    corrected Ract κ r (refinedBasal mRef X σ σRef η ηRef) (routeBasis γ) =
      (mRef * refinedCharacter X (σ γ - σRef) ((η γ).sub ηRef) *
        Ract ^ (κ r γ) : ℝ) • routeBasis γ :=
  corrected_diagonal_basis hR κ r
    (fun δ => refinedBasalMass mRef X (σ δ) σRef (η δ) ηRef) γ

/-- Scalar output of the diagonal specialization, retaining reader and route. -/
def refinedMass (Ract mRef : ℝ) (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) (γ : Route) : ℝ :=
  refinedBasalMass mRef X (σ γ) σRef (η γ) ηRef * Ract ^ (κ r γ)

omit [Fintype Route] [DecidableEq Route] in
theorem refinedMass_pos {Ract mRef : ℝ} (hR : 0 < Ract) (hmRef : 0 < mRef)
    (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) (γ : Route) :
    0 < refinedMass Ract mRef κ r X σ σRef η ηRef γ :=
  mul_pos (refinedBasalMass_pos hmRef X (σ γ) σRef (η γ) ηRef)
    (Real.rpow_pos_of_pos hR _)

omit [Fintype Route] [DecidableEq Route] in
theorem refinedMass_ratio {Ract mRef : ℝ} (hR : 0 < Ract) (hmRef : 0 < mRef)
    (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement s) (ηRef : Refinement s) (γ δ : Route) :
    refinedMass Ract mRef κ r X σ σRef η ηRef γ /
      refinedMass Ract mRef κ r X σ σRef η ηRef δ =
      refinedCharacter X (σ γ - σ δ) ((η γ).sub (η δ)) *
        Ract ^ (κ r γ - κ r δ) := by
  rw [refinedMass, refinedMass, mul_div_mul_comm,
    refinedBasalMass_ratio hmRef, ← Real.rpow_sub hR]

/-- Towers already relative to the reference are passed directly to the character. -/
def relativeBasal (mRef : ℝ) (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (ηRelative : Route → Refinement s) : End Route :=
  calibratedBasal mRef (fun γ => refinedCharacter X (σ γ - σRef) (ηRelative γ))

theorem relativeBasal_positive {mRef : ℝ} (hmRef : 0 < mRef)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (ηRelative : Route → Refinement s) :
    (relativeBasal mRef X σ σRef ηRelative).IsPositive :=
  calibratedBasal_positive hmRef _
    (fun γ => refinedCharacter_pos X (σ γ - σRef) (ηRelative γ))

theorem relativeBasal_matches (mRef : ℝ) (X : Coordinates) (σ : Route → Signature)
    (σRef : Signature) (η : Route → Refinement s) (ηRef : Refinement s) :
    relativeBasal mRef X σ σRef (fun γ => (η γ).sub ηRef) =
      refinedBasal mRef X σ σRef η ηRef := rfl

theorem relative_corrected_basis {Ract : ℝ} (hR : 0 < Ract) (mRef : ℝ)
    (κ : Reader → Route → ℝ) (r : Reader)
    (X : Coordinates) (σ : Route → Signature) (σRef : Signature)
    (ηRelative : Route → Refinement s) (γ : Route) :
    corrected Ract κ r (relativeBasal mRef X σ σRef ηRelative) (routeBasis γ) =
      (mRef * refinedCharacter X (σ γ - σRef) (ηRelative γ) *
        Ract ^ (κ r γ) : ℝ) • routeBasis γ :=
  calibrated_corrected_basis hR κ r _ γ

/-- The source's actual two-channel moment sequence, not an arbitrary target table. -/
def internalMoments (x y : ℝ) : ℕ → ℝ := orientedMoment (qPlus x y) (qMinus x y)

def internalBasal (mRef x y delta : ℝ) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement (internalMoments x y))
    (ηRef : Refinement (internalMoments x y)) : End Route :=
  refinedBasal mRef (internalCoordinates x y delta (internalMoments x y 120)) σ σRef η ηRef

theorem internalBasal_positive {mRef : ℝ} (hmRef : 0 < mRef)
    (x y delta : ℝ) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement (internalMoments x y))
    (ηRef : Refinement (internalMoments x y)) :
    (internalBasal mRef x y delta σ σRef η ηRef).IsPositive :=
  refinedBasal_positive hmRef _ σ σRef η ηRef

theorem internal_corrected_basis {Ract : ℝ} (hR : 0 < Ract) (mRef : ℝ)
    (κ : Reader → Route → ℝ) (r : Reader)
    (x y delta : ℝ) (σ : Route → Signature) (σRef : Signature)
    (η : Route → Refinement (internalMoments x y))
    (ηRef : Refinement (internalMoments x y)) (γ : Route) :
    corrected Ract κ r (internalBasal mRef x y delta σ σRef η ηRef) (routeBasis γ) =
      (mRef * refinedCharacter (internalCoordinates x y delta (internalMoments x y 120))
        (σ γ - σRef) ((η γ).sub ηRef) * Ract ^ (κ r γ) : ℝ) • routeBasis γ :=
  refined_corrected_basis hR mRef κ r _ σ σRef η ηRef γ

#print axioms refinedBasal_positive
#print axioms refined_corrected_positive
#print axioms refined_corrected_basis
#print axioms refinedMass_pos
#print axioms refinedMass_ratio
#print axioms relativeBasal_positive
#print axioms relativeBasal_matches
#print axioms relative_corrected_basis
#print axioms internalBasal_positive
#print axioms internal_corrected_basis

end
end HMT.VI.MassOperator
