import PaleyCharacterConstruction

/-!
Algebraic change of frame for the already constructed Paley--Witt encoder.

Source: the 775-page monograph, main_autosuficiente.tex:33950--34240,
especially the row-vector covariance identity and the calibrated atlas.
This auxiliary supplies only the algebraic terms requested by the unique
integrator. The history-dependent frames and their application to actualWord
are instantiated in that integrator's module, not postulated here.

No K, S8, target expansion, new axiom, or selection hypothesis occurs in this
file. These lemmas transport an existing generated encoding; they do not
select the terminal arithmetic register.
-/

namespace HMT.I.CalibratedPaleyTransport

set_option maxRecDepth 10000
set_option maxHeartbeats 1000000

abbrev Mat := Matrix (Fin 6) (Fin 6) (ZMod 3)
abbrev Frame := Matˣ
abbrev Word := Fin 6 → ZMod 3

def gamma (A : Mat) (w : Word) : Word × Word :=
  (w, Matrix.vecMul w A)

def conjugate (f : Frame) (A : Mat) : Mat :=
  (f : Mat) * A * ((f⁻¹ : Frame) : Mat)

def rowChange (f : Frame) (w : Word) : Word :=
  Matrix.vecMul w ((f⁻¹ : Frame) : Mat)

def pairedChange (f : Frame) (v : Word × Word) : Word × Word :=
  (rowChange f v.1, rowChange f v.2)

@[simp] theorem gamma_fst (A : Mat) (w : Word) :
    (gamma A w).1 = w := rfl

@[simp] theorem gamma_snd (A : Mat) (w : Word) :
    (gamma A w).2 = Matrix.vecMul w A := rfl

theorem gamma_left_inverse (A : Mat) :
    Function.LeftInverse Prod.fst (gamma A) := by
  intro w
  rfl

theorem gamma_injective (A : Mat) : Function.Injective (gamma A) :=
  (gamma_left_inverse A).injective

@[simp] theorem rowChange_inverse (f : Frame) (w : Word) :
    rowChange f⁻¹ (rowChange f w) = w := by
  simp only [rowChange, inv_inv, Matrix.vecMul_vecMul, Units.inv_mul,
    Matrix.vecMul_one]

theorem rowChange_injective (f : Frame) : Function.Injective (rowChange f) := by
  intro u v h
  have h' := congrArg (rowChange f⁻¹) h
  simpa only [rowChange_inverse] using h'

@[simp] theorem pairedChange_inverse (f : Frame) (v : Word × Word) :
    pairedChange f⁻¹ (pairedChange f v) = v := by
  rcases v with ⟨u, w⟩
  simp [pairedChange]

theorem pairedChange_injective (f : Frame) :
    Function.Injective (pairedChange f) := by
  intro u v h
  have h' := congrArg (pairedChange f⁻¹) h
  simpa only [pairedChange_inverse] using h'

theorem conjugate_mul (f : Frame) (A B : Mat) :
    conjugate f (A * B) = conjugate f A * conjugate f B := by
  simp only [conjugate, mul_assoc, Units.inv_mul_cancel_left]

@[simp] theorem conjugate_neg_one (f : Frame) :
    conjugate f (-1) = -1 := by
  simp only [conjugate, mul_neg, mul_one, neg_mul, Units.mul_inv]

theorem conjugate_square (f : Frame) (A : Mat) (hA : A * A = -1) :
    conjugate f A * conjugate f A = -1 := by
  rw [← conjugate_mul, hA, conjugate_neg_one]

/-- Row-vector covariance: both halves change by the same inverse frame. -/
theorem gamma_covariant (f : Frame) (A : Mat) (w : Word) :
    gamma (conjugate f A) (rowChange f w) =
      pairedChange f (gamma A w) := by
  apply Prod.ext
  · rfl
  · simp only [gamma, rowChange, pairedChange, conjugate,
      Matrix.vecMul_vecMul, ← mul_assoc, Units.inv_mul, one_mul]

theorem calibrated_gamma_injective (f : Frame) (A : Mat) :
    Function.Injective (fun w => gamma (conjugate f A) (rowChange f w)) :=
  (gamma_injective (conjugate f A)).comp (rowChange_injective f)

open HMT.I.PaleyCharacterConstruction HMT.PaleyWittDuality

/-- Link to the existing encoder, without reconstructing the Paley matrix. -/
theorem generated_pair (w : Word) :
    gamma reducedConference w =
      (head (generatedEncode w), tail (generatedEncode w)) := by
  rw [generated_encode_eq, head_encode, tail_encode, reduced_conference_eq]
  rfl

theorem generated_pair_covariant (f : Frame) (w : Word) :
    gamma (conjugate f reducedConference) (rowChange f w) =
      pairedChange f (head (generatedEncode w), tail (generatedEncode w)) := by
  rw [gamma_covariant, generated_pair]

theorem generated_square_preserved (f : Frame) :
    conjugate f reducedConference * conjugate f reducedConference = -1 :=
  conjugate_square f reducedConference reduced_conference_square

theorem generated_word_recovered (f : Frame) (w : Word) :
    rowChange f⁻¹
      (gamma (conjugate f reducedConference) (rowChange f w)).1 = w := by
  simp only [gamma_fst, rowChange_inverse]

#print axioms gamma_left_inverse
#print axioms gamma_injective
#print axioms rowChange_inverse
#print axioms rowChange_injective
#print axioms pairedChange_inverse
#print axioms pairedChange_injective
#print axioms conjugate_mul
#print axioms conjugate_neg_one
#print axioms conjugate_square
#print axioms gamma_covariant
#print axioms calibrated_gamma_injective
#print axioms generated_pair
#print axioms generated_pair_covariant
#print axioms generated_square_preserved
#print axioms generated_word_recovered

end HMT.I.CalibratedPaleyTransport
