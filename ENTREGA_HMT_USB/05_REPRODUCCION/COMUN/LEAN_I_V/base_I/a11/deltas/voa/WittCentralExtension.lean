import WittLatticeCocycle

namespace HMT.IV.TwistedGroupAlgebra

open HMT.IV.LatticeCocycle

def Extension (o : Fin 12) := ZMod 2 × Lattice o

noncomputable instance extensionGroup (o : Fin 12) : Group (Extension o) where
  mul := extensionMul o
  one := (0, 0)
  inv := extensionInv o
  mul_assoc := extensionMul_assoc o
  one_mul := extensionMul_zero_left o
  mul_one := extensionMul_zero_right o
  inv_mul_cancel := extensionMul_inv_left o

noncomputable def latticeProjection (o : Fin 12) :
    Extension o →* Multiplicative (Lattice o) where
  toFun a := Multiplicative.ofAdd a.2
  map_one' := rfl
  map_mul' _ _ := rfl

noncomputable def centralEmbedding (o : Fin 12) :
    Multiplicative (ZMod 2) →* Extension o where
  toFun s := (s.toAdd, 0)
  map_one' := rfl
  map_mul' a b := by
    change (a.toAdd + b.toAdd, (0 : Lattice o)) = extensionMul o (a.toAdd, 0) (b.toAdd, 0)
    simp [extensionMul, wittCocycle_zero_left]

theorem centralEmbedding_injective (o : Fin 12) :
    Function.Injective (centralEmbedding o) := by
  intro a b h
  exact congrArg Prod.fst h

theorem latticeProjection_surjective (o : Fin 12) :
    Function.Surjective (latticeProjection o) := by
  intro x
  exact ⟨(0, x.toAdd), rfl⟩

theorem latticeProjection_kernel (o : Fin 12) (a : Extension o) :
    latticeProjection o a = 1 ↔ ∃ s, a = centralEmbedding o s := by
  change a.2 = 0 ↔ ∃ s : ZMod 2, a = (s, 0)
  constructor
  · intro h
    exact ⟨a.1, Prod.ext rfl h⟩
  · rintro ⟨s, rfl⟩
    rfl

theorem centralEmbedding_commutes (o : Fin 12) (s : Multiplicative (ZMod 2))
    (a : Extension o) : centralEmbedding o s * a = a * centralEmbedding o s :=
  extension_kernel_central o s.toAdd a

#print axioms extensionGroup
#print axioms latticeProjection
#print axioms centralEmbedding
#print axioms centralEmbedding_injective
#print axioms latticeProjection_surjective
#print axioms latticeProjection_kernel
#print axioms centralEmbedding_commutes

end HMT.IV.TwistedGroupAlgebra
