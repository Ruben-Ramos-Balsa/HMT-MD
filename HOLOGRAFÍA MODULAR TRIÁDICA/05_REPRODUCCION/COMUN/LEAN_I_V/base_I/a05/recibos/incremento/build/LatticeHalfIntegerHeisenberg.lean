import LatticeOscillatorFock
import LatticeFieldTruncation

/-! Half-integer oscillators on the same symmetric algebra and marked-lattice
pairing. The natural oscillator label n now has frequency n+1/2. Creation is
unchanged; annihilation is the scalar transport of the existing derivation.
This is only the oscillator factor, not the finite central-extension module T,
the complete twisted lattice state-field map, or an orbifold construction. -/

noncomputable section
namespace HMT.IV.LatticeHalfIntegerHeisenberg
open LatticeCocycle LatticeOscillatorFock LatticeFieldTruncation

/-- An integer labels the actual half-integer frequency m+1/2. -/
def frequency (m : ℤ) : ℚ := (m:ℚ)+1/2

def opposite (m : ℤ) : ℤ := -m-1

theorem frequency_opposite (m : ℤ) : frequency (opposite m) = -frequency m := by
  simp only [frequency, opposite, Int.cast_sub, Int.cast_neg, Int.cast_one]
  ring

theorem frequency_sum_zero (m n : ℤ) :
    frequency m + frequency n=0 ↔ m+n+1=0 := by
  dsimp [frequency]
  constructor
  · intro h
    have h' : ((m+n+1:ℤ):ℚ)=0 := by push_cast; linarith
    exact_mod_cast h'
  · intro h
    have h' : ((m+n+1:ℤ):ℚ)=0 := by exact_mod_cast h
    push_cast at h'
    linarith

theorem frequency_ne_zero (m : ℤ) : frequency m ≠ 0 := by
  intro h
  have h' : ((2*m+1:ℤ):ℚ)=0 := by dsimp [frequency] at h; push_cast; linarith
  have hi : 2*m+1=0 := by exact_mod_cast h'
  omega

/-- No oscillator variables or lattice pairings are replaced. -/
abbrev HalfFock (o : Fin 12) := Fock o

def annihilationScale (n : ℕ) : ℂ := ((n:ℂ)+1/2)/((n:ℂ)+1)

def halfAnnihilate (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    Module.End ℂ (HalfFock o) := annihilationScale n • annihilate o n i

theorem annihilationScale_cancel (n : ℕ) :
    annihilationScale n * ((n:ℂ)+1) = (n:ℂ)+1/2 := by
  have hn : (n:ℂ)+1 ≠ 0 := by exact_mod_cast (Nat.succ_ne_zero n)
  exact div_mul_cancel₀ _ hn

theorem halfAnnihilate_vacuum (o : Fin 12) (n : ℕ) (i : Fin (BasisSize o)) :
    halfAnnihilate o n i 1=0 := by
  simp only [halfAnnihilate, LinearMap.smul_apply, annihilate_vacuum, smul_zero]

theorem half_mode_ccr_apply (o : Fin 12) (n m : ℕ) (i j : Fin (BasisSize o))
    (v : HalfFock o) :
    halfAnnihilate o n i (create o m j v) -
      create o m j (halfAnnihilate o n i v) =
      (if n=m then ((n:ℂ)+1/2)*gram o i j else 0) • v := by
  have h := LinearMap.congr_fun (mode_ccr o n m i j) v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    LinearMap.id_apply] at h
  simp only [halfAnnihilate, LinearMap.smul_apply, map_smul, ← smul_sub, h, smul_smul]
  by_cases hnm : n=m
  · simp only [if_pos hnm, ← mul_assoc, annihilationScale_cancel]
  · simp only [if_neg hnm, mul_zero]

theorem half_annihilations_commute (o : Fin 12) (n m : ℕ)
    (i j : Fin (BasisSize o)) (v : HalfFock o) :
    halfAnnihilate o n i (halfAnnihilate o m j v) =
      halfAnnihilate o m j (halfAnnihilate o n i v) := by
  simp only [halfAnnihilate, LinearMap.smul_apply, map_smul]
  rw [annihilations_commute_all_modes, smul_comm]

/-- There is no zero-frequency case: ofNat n is n+1/2 and negSucc n
is -(n+1/2), acting on the same nth oscillator generator. -/
def halfMode (o : Fin 12) (i : Fin (BasisSize o)) : ℤ → Module.End ℂ (HalfFock o)
  | Int.ofNat n => halfAnnihilate o n i
  | Int.negSucc n => create o n i

theorem halfMode_ofNat (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    halfMode o i (n:ℤ)=halfAnnihilate o n i := rfl

theorem halfMode_negSucc (o : Fin 12) (i : Fin (BasisSize o)) (n : ℕ) :
    halfMode o i (Int.negSucc n)=create o n i := rfl

theorem half_heisenberg_relation_apply (o : Fin 12) (i j : Fin (BasisSize o))
    (m n : ℤ) (v : HalfFock o) :
    halfMode o i m (halfMode o j n v) - halfMode o j n (halfMode o i m v) =
      (if m+n+1=0 then (((m:ℂ)+1/2)*gram o i j) else 0) • v := by
  cases m with
  | ofNat a =>
    cases n with
    | ofNat b =>
      have hne : Int.ofNat a+Int.ofNat b+1 ≠ 0 := by
        simp only [Int.ofNat_eq_coe]
        omega
      simp only [halfMode, half_annihilations_commute, sub_self, if_neg hne, zero_smul]
    | negSucc b =>
      have heq : Int.ofNat a+Int.negSucc b+1=0 ↔ a=b := by
        simp only [Int.ofNat_eq_coe]
        omega
      simpa only [halfMode, heq, Int.cast_natCast] using half_mode_ccr_apply o a b i j v
  | negSucc a =>
    cases n with
    | ofNat b =>
      have heq : Int.negSucc a+Int.ofNat b+1=0 ↔ b=a := by
        simp only [Int.ofNat_eq_coe]
        omega
      simp only [halfMode, heq]
      rw [← neg_sub, half_mode_ccr_apply]
      by_cases hba : b=a
      · subst b
        simp only [if_pos rfl, gram_symmetric o j i, ← neg_smul]
        congr 1
        push_cast
        ring
      · simp only [if_neg hba, zero_smul, neg_zero]
    | negSucc b =>
      have hne : Int.negSucc a+Int.negSucc b+1 ≠ 0 := by omega
      simp only [halfMode, creations_commute_all_modes, sub_self, if_neg hne, zero_smul]

theorem half_heisenberg_relation (o : Fin 12) (i j : Fin (BasisSize o)) (m n : ℤ) :
    (halfMode o i m).comp (halfMode o j n) - (halfMode o j n).comp (halfMode o i m) =
      (if frequency m+frequency n=0 then ((frequency m:ℂ)*gram o i j) else 0) •
        (LinearMap.id : Module.End ℂ (HalfFock o)) := by
  apply LinearMap.ext
  intro v
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.smul_apply,
    LinearMap.id_apply, frequency_sum_zero]
  rw [half_heisenberg_relation_apply]
  simp only [frequency, Rat.cast_add, Rat.cast_intCast, Rat.cast_div,
    Rat.cast_one, Rat.cast_ofNat]

theorem halfMode_annihilation_bound (o : Fin 12) (v : HalfFock o) :
    ∃ N : ℕ, ∀ n ≥ N, ∀ i : Fin (BasisSize o), halfMode o i (n:ℤ) v=0 := by
  obtain ⟨N,hN⟩ := exists_annihilation_bound o v
  refine ⟨N, ?_⟩
  intro n hn i
  simp only [halfMode_ofNat, halfAnnihilate, LinearMap.smul_apply, hN n hn i, smul_zero]

end HMT.IV.LatticeHalfIntegerHeisenberg
end

#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.frequency
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.opposite
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.frequency_opposite
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.frequency_sum_zero
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.frequency_ne_zero
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.HalfFock
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.annihilationScale
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfAnnihilate
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.annihilationScale_cancel
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfAnnihilate_vacuum
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.half_mode_ccr_apply
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.half_annihilations_commute
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfMode
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfMode_ofNat
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfMode_negSucc
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.half_heisenberg_relation_apply
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.half_heisenberg_relation
#print axioms HMT.IV.LatticeHalfIntegerHeisenberg.halfMode_annihilation_bound
