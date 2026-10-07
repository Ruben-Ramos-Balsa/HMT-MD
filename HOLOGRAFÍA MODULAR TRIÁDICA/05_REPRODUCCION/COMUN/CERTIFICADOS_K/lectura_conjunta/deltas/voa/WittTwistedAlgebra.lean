import WittCentralExtension

namespace HMT.IV.TwistedGroupAlgebra

open HMT.IV.LatticeCocycle

abbrev AlgebraSpace (o : Fin 12) := Lattice o →₀ ℂ

noncomputable def epsilon (o : Fin 12) (x y : Lattice o) : ℂ := wittSign o x y

theorem epsilon_zero_left (o : Fin 12) (x : Lattice o) : epsilon o 0 x = 1 := by
  simp [epsilon, wittSign_zero_left]

theorem epsilon_zero_right (o : Fin 12) (x : Lattice o) : epsilon o x 0 = 1 := by
  simp [epsilon, wittSign_zero_right]

theorem epsilon_cocycle (o : Fin 12) (x y z : Lattice o) :
    epsilon o x y * epsilon o (x+y) z = epsilon o y z * epsilon o x (y+z) := by
  dsimp [epsilon]
  exact_mod_cast wittSign_cocycle o x y z

theorem epsilon_square (o : Fin 12) (x y : Lattice o) :
    epsilon o x y * epsilon o x y = 1 := by
  dsimp [epsilon]
  exact_mod_cast wittSign_square o x y

noncomputable def twistedBilinear (o : Fin 12) :
    AlgebraSpace o →ₗ[ℂ] AlgebraSpace o →ₗ[ℂ] AlgebraSpace o :=
  Finsupp.linearCombination ℂ fun x =>
    Finsupp.linearCombination ℂ fun y => Finsupp.single (x+y) (epsilon o x y)

noncomputable def twistedMul (o : Fin 12) (f g : AlgebraSpace o) : AlgebraSpace o :=
  twistedBilinear o f g

noncomputable def twistedOne (o : Fin 12) : AlgebraSpace o := Finsupp.single 0 1

theorem twistedMul_single (o : Fin 12) (x y : Lattice o) (a b : ℂ) :
    twistedMul o (Finsupp.single x a) (Finsupp.single y b) =
      Finsupp.single (x+y) (a*b*epsilon o x y) := by
  simp only [twistedMul, twistedBilinear, Finsupp.linearCombination_single,
    LinearMap.smul_apply, smul_smul, Finsupp.smul_single, smul_eq_mul, mul_assoc]

theorem twistedMul_zero_left (o : Fin 12) (f : AlgebraSpace o) : twistedMul o 0 f = 0 := by
  simp [twistedMul]

theorem twistedMul_zero_right (o : Fin 12) (f : AlgebraSpace o) : twistedMul o f 0 = 0 := by
  simp [twistedMul]

theorem twistedMul_add_left (o : Fin 12) (f g h : AlgebraSpace o) :
    twistedMul o (f+g) h = twistedMul o f h + twistedMul o g h := by
  simp [twistedMul]

theorem twistedMul_add_right (o : Fin 12) (f g h : AlgebraSpace o) :
    twistedMul o f (g+h) = twistedMul o f g + twistedMul o f h := by
  simp [twistedMul]

theorem twistedMul_smul_left (o : Fin 12) (a : ℂ) (f g : AlgebraSpace o) :
    twistedMul o (a • f) g = a • twistedMul o f g := by
  simp [twistedMul]

theorem twistedMul_smul_right (o : Fin 12) (a : ℂ) (f g : AlgebraSpace o) :
    twistedMul o f (a • g) = a • twistedMul o f g := by
  simp [twistedMul]

theorem twistedMul_assoc (o : Fin 12) (f g h : AlgebraSpace o) :
    twistedMul o (twistedMul o f g) h = twistedMul o f (twistedMul o g h) := by
  induction f using Finsupp.induction_linear with
  | zero => simp [twistedMul_zero_left]
  | add f₁ f₂ ih₁ ih₂ => simp [twistedMul_add_left, ih₁, ih₂]
  | single x a =>
    induction g using Finsupp.induction_linear with
    | zero => simp [twistedMul_zero_left, twistedMul_zero_right]
    | add g₁ g₂ ih₁ ih₂ => simp [twistedMul_add_left, twistedMul_add_right, ih₁, ih₂]
    | single y b =>
      induction h using Finsupp.induction_linear with
      | zero => simp [twistedMul_zero_right]
      | add h₁ h₂ ih₁ ih₂ => simp [twistedMul_add_left, twistedMul_add_right, ih₁, ih₂]
      | single z c =>
        simp only [twistedMul_single, add_assoc]
        congr 1
        have hc := epsilon_cocycle o x y z
        linear_combination a*b*c*hc

theorem twistedMul_one_left (o : Fin 12) (f : AlgebraSpace o) :
    twistedMul o (twistedOne o) f = f := by
  induction f using Finsupp.induction_linear with
  | zero => exact twistedMul_zero_right _ _
  | add f g hf hg => rw [twistedMul_add_right, hf, hg]
  | single x a => simp [twistedOne, twistedMul_single, epsilon_zero_left]

theorem twistedMul_one_right (o : Fin 12) (f : AlgebraSpace o) :
    twistedMul o f (twistedOne o) = f := by
  induction f using Finsupp.induction_linear with
  | zero => exact twistedMul_zero_left _ _
  | add f g hf hg => rw [twistedMul_add_left, hf, hg]
  | single x a => simp [twistedOne, twistedMul_single, epsilon_zero_right]

theorem twistedMul_scalar_left (o : Fin 12) (a : ℂ) (f : AlgebraSpace o) :
    twistedMul o (Finsupp.single 0 a) f = a • f := by
  have h : Finsupp.single 0 a = a • twistedOne o := by
    simp [twistedOne]
  rw [h, twistedMul_smul_left, twistedMul_one_left]

theorem twistedMul_scalar_right (o : Fin 12) (a : ℂ) (f : AlgebraSpace o) :
    twistedMul o f (Finsupp.single 0 a) = a • f := by
  have h : Finsupp.single 0 a = a • twistedOne o := by
    simp [twistedOne]
  rw [h, twistedMul_smul_right, twistedMul_one_right]

#print axioms epsilon_cocycle
#print axioms epsilon_square
#print axioms twistedMul_single
#print axioms twistedMul_zero_left
#print axioms twistedMul_zero_right
#print axioms twistedMul_add_left
#print axioms twistedMul_add_right
#print axioms twistedMul_smul_left
#print axioms twistedMul_smul_right
#print axioms twistedMul_assoc
#print axioms twistedMul_one_left
#print axioms twistedMul_one_right
#print axioms twistedMul_scalar_left
#print axioms twistedMul_scalar_right

end HMT.IV.TwistedGroupAlgebra
