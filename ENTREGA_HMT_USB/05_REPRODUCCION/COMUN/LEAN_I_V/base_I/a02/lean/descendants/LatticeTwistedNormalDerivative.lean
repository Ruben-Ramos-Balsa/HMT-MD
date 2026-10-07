import LatticeTwistedNormalProduct

/-!
Divided z derivatives of the half-Heisenberg field, in the coordinate z=t²,
and their normal products with arbitrary Laurent fields on the same carrier.
A mode with t exponent e receives binom(e/2,n) and exponent e-2n.
Creation and annihilation retain the inherited oscillator-mode split at every
order. All sums are pointwise finite, not finite truncations of the modes.
No Jacobi, twisted state-field axiom or complete ET is assumed here.
-/

noncomputable section
namespace HMT.IV.LatticeTwistedNormalDerivative

open LatticeCocycle LatticeOscillatorFock LatticeTwistedCarrier
open LatticeTwistedTensorField
open LatticeNormalOrderedField (locallyFiniteSum)
open scoped BigOperators

local notation "NP" => LatticeTwistedNormalProduct.normalCoefficient

/-- The generalized binomial binom(e/2,n), with the falling-product convention. -/
def dividedFactor (e : ℤ) (n : ℕ) : ℂ :=
  (∏ j ∈ Finset.range n, ((e : ℂ)/2-(j : ℂ))) / (n.factorial : ℂ)

theorem dividedFactor_zero (e : ℤ) : dividedFactor e 0 = 1 := by
  simp [dividedFactor]

theorem dividedFactor_succ (e : ℤ) (n : ℕ) :
    ((n+1 : ℕ) : ℂ) * dividedFactor e (n+1) =
      ((e : ℂ)/2-(n : ℂ)) * dividedFactor e n := by
  have hn : ((n+1 : ℕ) : ℂ) ≠ 0 := by exact_mod_cast Nat.succ_ne_zero n
  unfold dividedFactor
  rw [Finset.prod_range_succ, Nat.factorial_succ, Nat.cast_mul]
  calc
    _ = (((n+1 : ℕ) : ℂ) * (((n+1 : ℕ) : ℂ))⁻¹) *
        (((e : ℂ)/2-(n : ℂ)) *
          ((∏ j ∈ Finset.range n, ((e : ℂ)/2-(j : ℂ))) / (n.factorial : ℂ))) := by
      simp only [div_eq_mul_inv, mul_inv_rev]
      ring
    _ = _ := by rw [mul_inv_cancel₀ hn, one_mul]

def derivativeCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) (k : ℤ) :
    Module.End ℂ (Carrier o) :=
  dividedFactor (k+2*n) n • tensorHalfFieldCoefficient o i (k+2*n)

theorem derivativeCoefficient_at_exponent (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (e : ℤ) :
    derivativeCoefficient o i n (e-2*n) =
      dividedFactor e n • tensorHalfFieldCoefficient o i e := by
  unfold derivativeCoefficient
  rw [show e-2*(n:ℤ)+2*n = e by omega]

/-- The coefficient recurrence for (1/n!)(d/dz)^n, where z=t². -/
theorem derivativeCoefficient_succ (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    ((n+1 : ℕ) : ℂ) • derivativeCoefficient o i (n+1) k =
      ((k : ℂ)/2+1) • derivativeCoefficient o i n (k+2) := by
  unfold derivativeCoefficient
  rw [show k+2*((n+1 : ℕ):ℤ) = k+2+2*(n:ℤ) by omega]
  simp only [smul_smul]
  rw [dividedFactor_succ]
  have hs : (((k+2+2*(n:ℤ) : ℤ) : ℂ)/2-(n:ℂ)) = (k:ℂ)/2+1 := by
    push_cast
    ring
  rw [hs]

theorem derivativeCoefficient_bounded (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, derivativeCoefficient o i n k v = 0 := by
  obtain ⟨b, hb⟩ := tensorHalfFieldCoefficient_bounded_pole o i v
  refine ⟨b-2*n, ?_⟩
  intro k hk
  have hz := hb (k+2*n) (by omega)
  simp only [derivativeCoefficient, LinearMap.smul_apply, hz, smul_zero]

def derivativeField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (derivativeCoefficient o i n) (derivativeCoefficient_bounded o i n)

theorem derivativeField_coefficient (o : Fin 12) (i : Fin (BasisSize o))
    (n : ℕ) (k : ℤ) :
    HVertexOperator.coeff (derivativeField o i n) k = derivativeCoefficient o i n k := rfl

def creationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (Carrier o) :=
  dividedFactor (2*(a:ℤ)-1) n •
    LatticeTwistedNormalProduct.creationTerm o i B (k+2*n) a

def annihilationTerm (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    Module.End ℂ (Carrier o) :=
  dividedFactor (-2*(a:ℤ)-3) n •
    LatticeTwistedNormalProduct.annihilationTerm o i B (k+2*n) a

theorem creationTerm_eq_derivative (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    creationTerm o i n B k a =
      (derivativeCoefficient o i n (2*(a:ℤ)-1-2*n)).comp
        (HVertexOperator.coeff B (k-(2*(a:ℤ)-1-2*n))) := by
  rw [derivativeCoefficient_at_exponent]
  unfold creationTerm
  rw [LatticeTwistedNormalProduct.creationTerm_eq_field_coefficient,
    twistedHalfHeisenbergField_coefficient, LinearMap.smul_comp]
  rw [show k+2*(n:ℤ)-(2*(a:ℤ)-1) = k-(2*(a:ℤ)-1-2*n) by omega]

theorem annihilationTerm_eq_derivative (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (a : ℕ) :
    annihilationTerm o i n B k a =
      (HVertexOperator.coeff B (k-(-2*(a:ℤ)-3-2*n))).comp
        (derivativeCoefficient o i n (-2*(a:ℤ)-3-2*n)) := by
  rw [derivativeCoefficient_at_exponent]
  unfold annihilationTerm
  rw [LatticeTwistedNormalProduct.annihilationTerm_eq_field_coefficient,
    twistedHalfHeisenbergField_coefficient, LinearMap.comp_smul]
  rw [show k+2*(n:ℤ)-(-2*(a:ℤ)-3) = k-(-2*(a:ℤ)-3-2*n) by omega]

theorem creationTerm_finite (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    (Function.support (fun a => creationTerm o i n B k a v)).Finite := by
  apply (LatticeTwistedNormalProduct.creationTerm_finite o i B (k+2*n) v).subset
  intro a ha hz
  apply ha
  simp only [creationTerm, LinearMap.smul_apply, hz, smul_zero]

theorem annihilationTerm_finite (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    (Function.support (fun a => annihilationTerm o i n B k a v)).Finite := by
  apply (LatticeTwistedNormalProduct.annihilationTerm_finite o i B (k+2*n) v).subset
  intro a ha hz
  apply ha
  simp only [annihilationTerm, LinearMap.smul_apply, hz, smul_zero]

private theorem normalTerms_bounded (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, ∀ a : ℕ,
      LatticeTwistedNormalProduct.creationTerm o i B k a v = 0 ∧
      LatticeTwistedNormalProduct.annihilationTerm o i B k a v = 0 := by
  classical
  obtain ⟨b, hb⟩ := LatticeTwistedNormalProduct.field_has_bound o B v
  obtain ⟨N, hN⟩ := LatticeTwistedNormalProduct.nonnegative_modes_bounded o i v
  have hfinite : ∀ a : Fin N, ∃ c : ℤ, ∀ k < c,
      HVertexOperator.coeff B k (halfMode o i (a : ℕ) v) = 0 :=
    fun _ => LatticeTwistedNormalProduct.field_has_bound o B _
  choose c hc using hfinite
  let d : ℤ := min (b-1) (-(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
    (fun a => (-(c a - 2*(a : ℕ) - 3)).toNat))))
  refine ⟨d, ?_⟩
  intro k hk a
  have hkb : k < b-1 := lt_of_lt_of_le hk (min_le_left _ _)
  constructor
  · simp only [LatticeTwistedNormalProduct.creationTerm, LinearMap.comp_apply,
      hb (k-2*a+1) (by omega), map_zero]
  · by_cases ha : a < N
    · let a' : Fin N := ⟨a,ha⟩
      have hsup : (-(c a' - 2*(a : ℤ) - 3)).toNat ≤
          (Finset.univ : Finset (Fin N)).sup
            (fun q => (-(c q - 2*(q : ℕ) - 3)).toNat) :=
        Finset.le_sup (f := fun q : Fin N => (-(c q - 2*(q : ℕ) - 3)).toNat)
          (Finset.mem_univ a')
      have hkd : k < -(Int.ofNat ((Finset.univ : Finset (Fin N)).sup
          (fun q => (-(c q - 2*(q : ℕ) - 3)).toNat))) :=
        lt_of_lt_of_le hk (min_le_right (b-1) _)
      simp only [Int.ofNat_eq_coe] at hkd
      have hlow : k+2*(a : ℤ)+3 < c a' := by omega
      have hzero : HVertexOperator.coeff B (k+2*(a : ℤ)+3)
          (halfMode o i (a : ℤ) v) = 0 := hc a' _ hlow
      simp only [LatticeTwistedNormalProduct.annihilationTerm, LinearMap.comp_apply, hzero]
    · simp only [LatticeTwistedNormalProduct.annihilationTerm, LinearMap.comp_apply,
        hN a (by omega), map_zero]

def normalCoefficient (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) : Module.End ℂ (Carrier o) :=
  locallyFiniteSum (creationTerm o i n B k) (creationTerm_finite o i n B k) +
  locallyFiniteSum (annihilationTerm o i n B k) (annihilationTerm_finite o i n B k)

theorem normalCoefficient_apply (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) (v : Carrier o) :
    normalCoefficient o i n B k v =
      (∑ᶠ a, creationTerm o i n B k a v) +
      ∑ᶠ a, annihilationTerm o i n B k a v := rfl

theorem normalCoefficient_bounded (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (v : Carrier o) :
    ∃ b : ℤ, ∀ k < b, normalCoefficient o i n B k v = 0 := by
  obtain ⟨b, hb⟩ := normalTerms_bounded o i B v
  refine ⟨b-2*n, ?_⟩
  intro k hk
  have hz := hb (k+2*n) (by omega)
  rw [normalCoefficient_apply]
  simp only [creationTerm, annihilationTerm, LinearMap.smul_apply,
    fun a => (hz a).1, fun a => (hz a).2, smul_zero, finsum_zero, add_zero]

def derivativeNormalField (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) : VertexOperator ℂ (Carrier o) :=
  VertexOperator.of_coeff (normalCoefficient o i n B) (normalCoefficient_bounded o i n B)

theorem derivativeNormalField_coefficient (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ)
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) :
    HVertexOperator.coeff (derivativeNormalField o i n B) k = normalCoefficient o i n B k := rfl

theorem normalCoefficient_zero (o : Fin 12) (i : Fin (BasisSize o))
    (B : VertexOperator ℂ (Carrier o)) (k : ℤ) :
    normalCoefficient o i 0 B k = NP o i B k := by
  apply LinearMap.ext
  intro v
  rw [normalCoefficient_apply, LatticeTwistedNormalProduct.normalCoefficient_apply]
  simp only [creationTerm, annihilationTerm, dividedFactor_zero,
    Nat.cast_zero, mul_zero, add_zero, one_smul]

end HMT.IV.LatticeTwistedNormalDerivative
end

#print axioms HMT.IV.LatticeTwistedNormalDerivative.dividedFactor
#print axioms HMT.IV.LatticeTwistedNormalDerivative.dividedFactor_zero
#print axioms HMT.IV.LatticeTwistedNormalDerivative.dividedFactor_succ
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeCoefficient
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeCoefficient_at_exponent
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeCoefficient_succ
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeField
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeField_coefficient
#print axioms HMT.IV.LatticeTwistedNormalDerivative.creationTerm
#print axioms HMT.IV.LatticeTwistedNormalDerivative.annihilationTerm
#print axioms HMT.IV.LatticeTwistedNormalDerivative.creationTerm_eq_derivative
#print axioms HMT.IV.LatticeTwistedNormalDerivative.annihilationTerm_eq_derivative
#print axioms HMT.IV.LatticeTwistedNormalDerivative.creationTerm_finite
#print axioms HMT.IV.LatticeTwistedNormalDerivative.annihilationTerm_finite
#print axioms HMT.IV.LatticeTwistedNormalDerivative.normalCoefficient
#print axioms HMT.IV.LatticeTwistedNormalDerivative.normalCoefficient_apply
#print axioms HMT.IV.LatticeTwistedNormalDerivative.normalCoefficient_bounded
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeNormalField
#print axioms HMT.IV.LatticeTwistedNormalDerivative.derivativeNormalField_coefficient
#print axioms HMT.IV.LatticeTwistedNormalDerivative.normalCoefficient_zero
