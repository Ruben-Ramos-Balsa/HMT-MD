import WittComplexAlgebra

/-!
Negation lift for the actual parity-coordinate cocycle. The sign has been
constructed rather than postulated; its invariance under simultaneous
negation follows from parity coordinates. The resulting complex algebra
automorphism has square one. This statement does not impose the additional
half-norm diagonal normalization used by some lattice-VOA conventions.
-/

noncomputable section
namespace HMT.IV.WittNegationLift

open HMT.IV.LatticeCocycle HMT.IV.TwistedGroupAlgebra

theorem parityCoordinates_neg (o : Fin 12) (x : Lattice o) :
    parityCoordinates o (-x) = parityCoordinates o x := by
  funext i
  simp [parityCoordinates, ZMod.neg_eq_self_mod_two]

theorem wittCocycle_neg_neg (o : Fin 12) (x y : Lattice o) :
    wittCocycle o (-x) (-y) = wittCocycle o x y := by
  simp only [wittCocycle, parityCoordinates_neg]

theorem epsilon_neg_neg (o : Fin 12) (x y : Lattice o) :
    epsilon o (-x) (-y) = epsilon o x y := by
  simp only [epsilon, wittSign, wittCocycle_neg_neg]

def negationEquiv (o : Fin 12) : Lattice o ≃ Lattice o where
  toFun := Neg.neg
  invFun := Neg.neg
  left_inv := neg_neg
  right_inv := neg_neg

def thetaLinear (o : Fin 12) : TwistedAlgebra o ≃ₗ[ℂ] TwistedAlgebra o :=
  Finsupp.domLCongr (negationEquiv o)

theorem theta_single (o : Fin 12) (x : Lattice o) (a : ℂ) :
    thetaLinear o (Finsupp.single x a) = Finsupp.single (-x) a :=
  Finsupp.domLCongr_single (negationEquiv o) x a

theorem theta_square (o : Fin 12) (f : TwistedAlgebra o) :
    thetaLinear o (thetaLinear o f) = f := by
  induction f using Finsupp.induction_linear with
  | zero => simp
  | add f g hf hg => simp [hf, hg]
  | single x a => simp only [theta_single, neg_neg]

theorem theta_one (o : Fin 12) : thetaLinear o 1 = 1 := by
  change thetaLinear o (Finsupp.single 0 1) = Finsupp.single 0 1
  rw [theta_single, neg_zero]

theorem theta_mul (o : Fin 12) (f g : TwistedAlgebra o) :
    thetaLinear o (f*g) = thetaLinear o f * thetaLinear o g := by
  change thetaLinear o (twistedMul o f g) =
    twistedMul o (thetaLinear o f) (thetaLinear o g)
  induction f using Finsupp.induction_linear with
  | zero => simp [twistedMul_zero_left]
  | add f h hf hh =>
      simp only [twistedMul_add_left, map_add, hf, hh]
      exact (twistedMul_add_left o (thetaLinear o f) (thetaLinear o h)
        (thetaLinear o g)).symm
  | single x a =>
    induction g using Finsupp.induction_linear with
    | zero => simp [twistedMul_zero_right]
    | add g h hg hh =>
        simp only [twistedMul_add_right, map_add, hg, hh]
        exact (twistedMul_add_right o (thetaLinear o (Finsupp.single x a))
          (thetaLinear o g) (thetaLinear o h)).symm
    | single y b =>
      simp only [twistedMul_single, theta_single, neg_add_rev,
        epsilon_neg_neg, add_comm]

def theta (o : Fin 12) : TwistedAlgebra o ≃ₐ[ℂ] TwistedAlgebra o :=
  AlgEquiv.ofLinearEquiv (thetaLinear o) (theta_one o) (theta_mul o)

theorem theta_basis (o : Fin 12) (x : Lattice o) :
    theta o (basisElement o x) = basisElement o (-x) :=
  theta_single o x 1

theorem theta_involutive (o : Fin 12) : Function.Involutive (theta o) :=
  theta_square o

end HMT.IV.WittNegationLift
end

#print axioms HMT.IV.WittNegationLift.parityCoordinates_neg
#print axioms HMT.IV.WittNegationLift.wittCocycle_neg_neg
#print axioms HMT.IV.WittNegationLift.epsilon_neg_neg
#print axioms HMT.IV.WittNegationLift.theta_square
#print axioms HMT.IV.WittNegationLift.theta_one
#print axioms HMT.IV.WittNegationLift.theta_mul
#print axioms HMT.IV.WittNegationLift.theta
#print axioms HMT.IV.WittNegationLift.theta_basis
#print axioms HMT.IV.WittNegationLift.theta_involutive
