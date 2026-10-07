import Mathlib.GroupTheory.QuotientGroup.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-! Article II, eq:el-h4: the actual integral local cokernel, constructed via
an explicit residual map and its kernel. Cardinality is a theorem, not data. -/
namespace HMT.II.DeterminantalAction

abbrev IntegerFiber := Fin 4 → ℤ
abbrev ResidueFiber := ZMod 2 × ZMod 2 × ZMod 4

def H4 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 1, 1, 1; 1, 1, -1, -1; 1, -1, 1, -1; 1, -1, -1, 1]

def h4Map : IntegerFiber →+ IntegerFiber where
  toFun v := ![v 0 + v 1 + v 2 + v 3, v 0 + v 1 - v 2 - v 3,
    v 0 - v 1 + v 2 - v 3, v 0 - v 1 - v 2 + v 3]
  map_zero' := by ext i; fin_cases i <;> simp
  map_add' v w := by ext i; fin_cases i <;> simp <;> ring

theorem h4Map_eq_mulVec (v : IntegerFiber) : h4Map v = H4.mulVec v := by
  ext i
  fin_cases i <;> simp [h4Map, H4, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> ring

def residual : IntegerFiber →+ ResidueFiber where
  toFun v := (((v 1 - v 0 : ℤ) : ZMod 2),
    ((v 2 - v 0 : ℤ) : ZMod 2), ((v 0 - v 1 - v 2 + v 3 : ℤ) : ZMod 4))
  map_zero' := by simp
  map_add' v w := by ext <;> simp <;> ring

/-- Representatives of the three residues; this is a section of the residual
map, not an inverse of H4 over the integers. -/
def residueSection (a : ResidueFiber) : IntegerFiber :=
  ![0, (a.1.val : ℤ), (a.2.1.val : ℤ),
    (a.1.val : ℤ) + (a.2.1.val : ℤ) + (a.2.2.val : ℤ)]

theorem residual_section (a : ResidueFiber) : residual (residueSection a) = a := by
  rcases a with ⟨a, b, c⟩
  ext <;> simp [residual, residueSection]
  ring

theorem residual_h4Map (v : IntegerFiber) : residual (h4Map v) = 0 := by
  apply Prod.ext
  · change (((v 0 + v 1 - v 2 - v 3) - (v 0 + v 1 + v 2 + v 3) : ℤ) : ZMod 2) = 0
    apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).2
    exact ⟨-v 2 - v 3, by ring⟩
  · apply Prod.ext
    · change (((v 0 - v 1 + v 2 - v 3) - (v 0 + v 1 + v 2 + v 3) : ℤ) : ZMod 2) = 0
      apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).2
      exact ⟨-v 1 - v 3, by ring⟩
    · change (((v 0 + v 1 + v 2 + v 3) - (v 0 + v 1 - v 2 - v 3) -
        (v 0 - v 1 + v 2 - v 3) + (v 0 - v 1 - v 2 + v 3) : ℤ) : ZMod 4) = 0
      apply (ZMod.intCast_zmod_eq_zero_iff_dvd _ 4).2
      exact ⟨v 3, by ring⟩

/-- Exact integral preimage from the two divisibilities by two and one by four. -/
theorem mem_range_of_residual_zero (v : IntegerFiber) (hv : residual v = 0) :
    v ∈ h4Map.range := by
  have ha : (2 : ℤ) ∣ v 1 - v 0 :=
    (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).1 (congrArg Prod.fst hv)
  have hb : (2 : ℤ) ∣ v 2 - v 0 :=
    (ZMod.intCast_zmod_eq_zero_iff_dvd _ 2).1 (congrArg (fun a => a.2.1) hv)
  have hc : (4 : ℤ) ∣ v 0 - v 1 - v 2 + v 3 :=
    (ZMod.intCast_zmod_eq_zero_iff_dvd _ 4).1 (congrArg (fun a => a.2.2) hv)
  obtain ⟨a, ha⟩ := ha
  obtain ⟨b, hb⟩ := hb
  obtain ⟨c, hc⟩ := hc
  refine ⟨![v 0 + a + b + c, -b - c, -a - c, c], ?_⟩
  ext i
  fin_cases i <;> simp [h4Map] <;> omega

theorem residual_kernel : residual.ker = h4Map.range := by
  ext v
  constructor
  · exact mem_range_of_residual_zero v
  · rintro ⟨w, rfl⟩
    exact residual_h4Map w

/-- The quotient is by the image of the concrete H4 map, not by an unrelated
finite presentation. -/
abbrev LocalQuotient := IntegerFiber ⧸ h4Map.range

def localQuotientEquiv : LocalQuotient ≃+ ResidueFiber :=
  (QuotientAddGroup.quotientAddEquivOfEq residual_kernel.symm).trans
    (QuotientAddGroup.quotientKerEquivOfRightInverse residual residueSection residual_section)

noncomputable instance : Fintype LocalQuotient :=
  Fintype.ofEquiv ResidueFiber localQuotientEquiv.toEquiv.symm

theorem localQuotient_cardinal : Fintype.card LocalQuotient = 16 := by
  rw [Fintype.card_congr localQuotientEquiv.toEquiv]
  decide

#print axioms h4Map_eq_mulVec
#print axioms residual_section
#print axioms residual_kernel
#print axioms localQuotientEquiv
#print axioms localQuotient_cardinal

end HMT.II.DeterminantalAction
