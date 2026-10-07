import WittTwistedAlgebra

namespace HMT.IV.TwistedGroupAlgebra

open HMT.IV.LatticeCocycle

def TwistedAlgebra (o : Fin 12) := AlgebraSpace o

noncomputable instance twistedMulInstance (o : Fin 12) : Mul (TwistedAlgebra o) :=
  ⟨twistedMul o⟩

noncomputable instance twistedOneInstance (o : Fin 12) : One (TwistedAlgebra o) :=
  ⟨twistedOne o⟩

noncomputable instance twistedNatCast (o : Fin 12) : NatCast (TwistedAlgebra o) :=
  ⟨fun n => Finsupp.single 0 (n : ℂ)⟩

noncomputable instance twistedIntCast (o : Fin 12) : IntCast (TwistedAlgebra o) :=
  ⟨fun z => Finsupp.single 0 (z : ℂ)⟩

noncomputable instance twistedRing (o : Fin 12) : Ring (TwistedAlgebra o) where
  __ := (inferInstance : AddCommGroup (AlgebraSpace o))
  mul := twistedMul o
  one := twistedOne o
  mul_assoc := twistedMul_assoc o
  one_mul := twistedMul_one_left o
  mul_one := twistedMul_one_right o
  left_distrib := twistedMul_add_right o
  right_distrib := twistedMul_add_left o
  zero_mul := twistedMul_zero_left o
  mul_zero := twistedMul_zero_right o
  natCast n := Finsupp.single 0 (n : ℂ)
  natCast_zero := by simp
  natCast_succ n := by
    change Finsupp.single 0 ((n+1 : ℕ) : ℂ) = Finsupp.single 0 (n : ℂ) + Finsupp.single 0 (1 : ℂ)
    simp [Finsupp.single_add]
  intCast z := Finsupp.single 0 (z : ℂ)
  intCast_ofNat n := rfl
  intCast_negSucc n := by
    change Finsupp.single 0 (Int.negSucc n : ℂ) = -Finsupp.single 0 ((n+1 : ℕ) : ℂ)
    simp

noncomputable instance twistedScalar (o : Fin 12) : SMul ℂ (TwistedAlgebra o) :=
  inferInstanceAs (SMul ℂ (AlgebraSpace o))

noncomputable def complexScalarHom (o : Fin 12) : ℂ →+* TwistedAlgebra o where
  toFun a := Finsupp.single 0 a
  map_zero' := by exact Finsupp.single_zero _
  map_one' := rfl
  map_add' a b := Finsupp.single_add _ _ _
  map_mul' a b := by
    change Finsupp.single 0 (a*b) = twistedMul o (Finsupp.single 0 a) (Finsupp.single 0 b)
    simp [twistedMul_single, epsilon_zero_left]

noncomputable instance twistedComplexAlgebra (o : Fin 12) : Algebra ℂ (TwistedAlgebra o) where
  algebraMap := complexScalarHom o
  commutes' a f := by
    change twistedMul o (Finsupp.single 0 a) f = twistedMul o f (Finsupp.single 0 a)
    rw [twistedMul_scalar_left, twistedMul_scalar_right]
  smul_def' a f := by
    change a • f = twistedMul o (Finsupp.single 0 a) f
    exact (twistedMul_scalar_left o a f).symm

noncomputable def basisElement (o : Fin 12) (x : Lattice o) : TwistedAlgebra o :=
  Finsupp.single x 1

theorem twisted_basis_product (o : Fin 12) (x y : Lattice o) :
    basisElement o x * basisElement o y = epsilon o x y • basisElement o (x+y) := by
  change twistedMul o (Finsupp.single x 1) (Finsupp.single y 1) = _
  rw [twistedMul_single]
  change Finsupp.single (x+y) (1*1*epsilon o x y) = epsilon o x y • Finsupp.single (x+y) 1
  simp

#print axioms twistedRing
#print axioms complexScalarHom
#print axioms twistedComplexAlgebra
#print axioms twisted_basis_product

end HMT.IV.TwistedGroupAlgebra
