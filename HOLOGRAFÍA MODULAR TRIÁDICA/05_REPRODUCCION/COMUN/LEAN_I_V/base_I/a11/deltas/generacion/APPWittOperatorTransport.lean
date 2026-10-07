import APPFockIndex
import CoxeterNeighbor

/-!
# The twelve-fibre APP--Witt operator transport

CERTIFICADO_NUEVO of the pre-existing U031 construction, source
`capitulo_22_c20_lineas_2613_3270.tex`, lines 21--106,
`p12-83-c20-s8:thm:alineamiento-app-witt-u031`.

The pair/sheet/orbit labels are retained.  The chart lambda is a bijection,
and the local reflection conjugates the two actual Coxeter orientations.
The target is the existing rational root space and existing Witt action,
not a replacement operator defined from its trace.  The six-plus-six source
chart is also identified with the actual matrix in APPFockIndex.

This rational vector-space transport is not asserted to identify the two
integral glue presentations or their cocycles, and is not an FLM theorem.
-/

namespace HMT.IV.APPWittOperatorTransport

open CoxeterNeighbor

abbrev Label := Fin 3 × Fin 2 × Fin 2
abbrev Root := ℚ × ℚ
abbrev APP := Label → Root

/-- pair, sheet, cyclotomic orbit, with the fixed dodecaphase origin. -/
def lambda (a : Label) : Fin 12 :=
  ⟨4 * a.1.val + 2 * a.2.1.val + a.2.2.val, by omega⟩

theorem lambda_bijective : Function.Bijective lambda := by decide +kernel

noncomputable def labelEquiv : Label ≃ Fin 12 :=
  Equiv.ofBijective lambda lambda_bijective

@[simp] theorem labelEquiv_apply (a : Label) : labelEquiv a = lambda a := rfl

def sheet (a : Label) : Bool := decide (a.2.1.val = 1)

/-- The reflection R is the transposition of the simple-root coordinates. -/
def reflection (b : Bool) : Root ≃ₗ[ℚ] Root where
  toFun x := if b then (x.2, x.1) else x
  invFun x := if b then (x.2, x.1) else x
  left_inv x := by cases b <;> simp
  right_inv x := by cases b <;> simp
  map_add' x y := by cases b <;> rfl
  map_smul' r x := by cases b <;> rfl

theorem reflection_pairing (b : Bool) (x y : Root) :
    localPair (reflection b x) (reflection b y) = localPair x y := by
  cases b
  · rfl
  · simp [reflection, localPair]
    ring

/-- P_b R^mu in the source notation, with P_b=R^(wittOrientation b). -/
def fibreTransport (s t : Bool) : Root ≃ₗ[ℚ] Root :=
  (reflection t).trans (reflection s)

theorem fibre_intertwines (s t : Bool) (x : Root) :
    turn s (fibreTransport s t x) = fibreTransport s t (turn t x) := by
  cases s <;> cases t <;> ext <;>
    simp [fibreTransport, reflection, turn]

theorem fibre_pairing (s t : Bool) (x y : Root) :
    localPair (fibreTransport s t x) (fibreTransport s t y) = localPair x y := by
  exact (reflection_pairing s _ _).trans (reflection_pairing t x y)

def appAction (x : APP) : APP := fun a => turn (sheet a) (x a)

/-- The source labels are transported, not discarded or selected by a value. -/
noncomputable def transport : APP ≃ₗ[ℚ] Space 12 where
  toFun x b := fibreTransport (wittOrientation b) (sheet (labelEquiv.symm b))
    (x (labelEquiv.symm b))
  invFun y a := (fibreTransport (wittOrientation (labelEquiv a)) (sheet a)).symm
    (y (labelEquiv a))
  left_inv x := by
    funext a
    simp only [Equiv.symm_apply_apply, LinearEquiv.symm_apply_apply]
  right_inv y := by
    funext b
    simp only [Equiv.apply_symm_apply, LinearEquiv.apply_symm_apply]
  map_add' x y := by funext b; exact map_add _ _ _
  map_smul' r x := by
    funext b
    exact (fibreTransport (wittOrientation b) (sheet (labelEquiv.symm b))).map_smul r _

theorem transport_at_label (x : APP) (a : Label) :
    transport x (lambda a) = fibreTransport (wittOrientation (lambda a))
      (sheet a) (x a) := by
  change fibreTransport _ (sheet (labelEquiv.symm (labelEquiv a)))
    (x (labelEquiv.symm (labelEquiv a))) = _
  simp only [Equiv.symm_apply_apply]

/-- The U031 operator square, for all states, not a scalar trace comparison. -/
theorem transport_intertwines (x : APP) :
    action wittOrientation (transport x) = transport (appAction x) := by
  funext b
  exact fibre_intertwines (wittOrientation b) (sheet (labelEquiv.symm b))
    (x (labelEquiv.symm b))

def appPair (x y : APP) : ℚ := ∑ a, localPair (x a) (y a)

theorem transport_pairing (x y : APP) : pairing (transport x) (transport y) =
    appPair x y := by
  unfold pairing appPair
  have h := labelEquiv.symm.sum_comp (fun a => localPair (x a) (y a))
  rw [← h]
  apply Finset.sum_congr rfl
  intro b _
  exact fibre_pairing _ _ _ _

theorem appAction_cube (x : APP) : appAction (appAction (appAction x)) = x := by
  apply transport.injective
  rw [← transport_intertwines, ← transport_intertwines, ← transport_intertwines]
  exact action_cube wittOrientation (transport x)

/-- The APPFockIndex matrix orders the sheet first (six C, then six C^-1). -/
def matrixLabel (i : Fin 24) : Label :=
  (⟨i.val / 4 % 3, Nat.mod_lt _ (by decide)⟩,
   ⟨i.val / 12, by omega⟩, ⟨i.val / 2 % 2, Nat.mod_lt _ (by decide)⟩)

def matrixCoordinates (x : APP) (i : Fin 24) : ℚ :=
  if i.val % 2 = 0 then (x (matrixLabel i)).1 else (x (matrixLabel i)).2

def matrixIndex (a : Label) (j : Fin 2) : Fin 24 :=
  ⟨12 * a.2.1.val + 4 * a.1.val + 2 * a.2.2.val + j.val, by omega⟩

theorem matrixLabel_matrixIndex (a : Label) (j : Fin 2) :
    matrixLabel (matrixIndex a j) = a := by
  revert a j
  decide +kernel

theorem matrixIndex_parity (a : Label) (j : Fin 2) :
    (matrixIndex a j).val % 2 = j.val := by
  revert a j
  decide +kernel

theorem matrixCoordinates_injective : Function.Injective matrixCoordinates := by
  intro x y h
  funext a
  apply Prod.ext
  · have hh := congrFun h (matrixIndex a 0)
    simpa [matrixCoordinates, matrixLabel_matrixIndex, matrixIndex_parity] using hh
  · have hh := congrFun h (matrixIndex a 1)
    simpa [matrixCoordinates, matrixLabel_matrixIndex, matrixIndex_parity] using hh

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
/-- Compatibility with the imported operator that already gives the APP Fock index. -/
theorem matrixCoordinates_intertwines (x : APP) :
    Matrix.mulVec HMT.I.APPFockIndex.generator (matrixCoordinates x) =
      matrixCoordinates (appAction x) := by
  ext i
  fin_cases i <;>
    norm_num [Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
      HMT.I.APPFockIndex.generator, HMT.I.APPFockIndex.localCoordinate,
      HMT.I.APPFockIndex.coxeter, HMT.I.APPFockIndex.coxeterInverse,
      matrixCoordinates, matrixLabel, appAction, sheet, turn] <;> ring

end HMT.IV.APPWittOperatorTransport

#print axioms HMT.IV.APPWittOperatorTransport.lambda_bijective
#print axioms HMT.IV.APPWittOperatorTransport.fibre_intertwines
#print axioms HMT.IV.APPWittOperatorTransport.fibre_pairing
#print axioms HMT.IV.APPWittOperatorTransport.transport
#print axioms HMT.IV.APPWittOperatorTransport.transport_at_label
#print axioms HMT.IV.APPWittOperatorTransport.transport_intertwines
#print axioms HMT.IV.APPWittOperatorTransport.transport_pairing
#print axioms HMT.IV.APPWittOperatorTransport.appAction_cube
#print axioms HMT.IV.APPWittOperatorTransport.matrixLabel_matrixIndex
#print axioms HMT.IV.APPWittOperatorTransport.matrixIndex_parity
#print axioms HMT.IV.APPWittOperatorTransport.matrixCoordinates_injective
#print axioms HMT.IV.APPWittOperatorTransport.matrixCoordinates_intertwines
