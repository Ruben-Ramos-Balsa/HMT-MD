import DodecaphaseLinear

/-! The material harmonic reader Pi_H from U016, equations
lector-armonico-a-desde-ledger and lector-armonico-bloque-desde-ledger.
This module proves its universal concordance with the existing H12 operator.
It does not supply or assume a particular terminal channel value. -/
namespace HMT.TerminalChannels

open DodecaphaseLinear

structure Channels where
  b90 : Vector12
  b120 : Vector12
  charge : Int

def extract (z : Vector12) : Channels := ⟨D3 z, D4 z, Q z⟩

def orbitSum (v : Vector12) (r : Fin 3) : Int :=
  v (orbitIndex r 0) + v (orbitIndex r 1) +
  v (orbitIndex r 2) + v (orbitIndex r 3)

def firstSum (c : Channels) : Int :=
  (c.charge + 2 * orbitSum c.b120 0 + orbitSum c.b120 1) / 3

def scalarSum (c : Channels) (r : Fin 3) : Int :=
  match r.val with
  | 0 => firstSum c
  | 1 => firstSum c - orbitSum c.b120 0
  | _ => firstSum c - orbitSum c.b120 0 - orbitSum c.b120 1

def harmonic (c : Channels) : Vector12 := fun i =>
  let r : Fin 3 := ⟨i.val % 3, Nat.mod_lt _ (by decide)⟩
  match i.val / 3 with
  | 0 => scalarSum c r
  | 1 => c.b90 (orbitIndex r 1) - c.b90 (orbitIndex r 3)
  | 2 => c.b90 (orbitIndex r 0) + c.b90 (orbitIndex r 2)
  | _ => c.b90 (orbitIndex r 0) - c.b90 (orbitIndex r 2)

theorem firstSum_extract (z : Vector12) :
    firstSum (extract z) = orbitSum z 0 := by
  change (z 0 + z 1 + z 2 + z 3 + z 4 + z 5 + z 6 + z 7 + z 8 + z 9 + z 10 + z 11 +
    2 * (z 0 - z 4 + (z 3 - z 7) + (z 6 - z 10) + (z 9 - z 1)) +
    (z 1 - z 5 + (z 4 - z 8) + (z 7 - z 11) + (z 10 - z 2))) / 3 =
    z 0 + z 3 + z 6 + z 9
  omega

theorem harmonic_extract (z : Vector12) : harmonic (extract z) = H12 z := by
  funext i
  have hs := firstSum_extract z
  rcases fin12_cases i with h | h | h | h | h | h | h | h | h | h | h | h
  all_goals subst i
  all_goals simp [harmonic, scalarSum, extract, orbitSum, orbitIndex,
    D3, D4, shift, H12, Fin.ofNat, Fin.instOfNat] at *
  all_goals dsimp only [OfNat.ofNat, Fin.ofNat, Fin.instOfNat] at *
  all_goals simp only [Nat.reduceMod, Nat.reduceMul, Nat.reduceAdd] at *
  all_goals omega

def inverseH (u : Vector12) : Vector12 := fun i => H12 u i / 4

theorem inverseH_H12 (z : Vector12) : inverseH (H12 z) = z := by
  funext i
  simp only [inverseH, H12_square_pointwise]
  omega

def recover (c : Channels) : Vector12 := inverseH (harmonic c)

theorem recover_extract (z : Vector12) : recover (extract z) = z := by
  rw [recover, harmonic_extract, inverseH_H12]

theorem extract_injective (u v : Vector12) (h : extract u = extract v) : u = v := by
  have e := congrArg recover h
  simpa only [recover_extract] using e

theorem recover_unique (c : Channels) (z : Vector12) (h : extract z = c) :
    recover c = z := by
  rw [← h, recover_extract]

/-- Compatibility is stated as the actual image condition, not asserted for
every tuple of 25 integers. Later ledger extraction proves image membership. -/
def Compatible (c : Channels) : Prop := ∃ z : Vector12, extract z = c

theorem return_compatible (c : Channels) (hc : Compatible c) :
    extract (recover c) = c := by
  obtain ⟨z, hz⟩ := hc
  rw [recover_unique c z hz]
  exact hz

theorem integral_hadamard (c : Channels) (hc : Compatible c) :
    H12 (recover c) = harmonic c := by
  obtain ⟨z, hz⟩ := hc
  rw [← hz, recover_extract, harmonic_extract]

theorem same_channels_same_harmonic (u v : Vector12)
    (h : extract u = extract v) : H12 u = H12 v := by
  rw [← harmonic_extract, ← harmonic_extract, h]

theorem compatible_integral_equation (c : Channels) (hc : Compatible c) :
    scale 4 (recover c) = H12 (harmonic c) :=
  (inverse_equation _ _).mp (integral_hadamard c hc)

#print axioms firstSum_extract
#print axioms harmonic_extract
#print axioms inverseH_H12
#print axioms recover_extract
#print axioms extract_injective
#print axioms recover_unique
#print axioms return_compatible
#print axioms integral_hadamard
#print axioms same_channels_same_harmonic
#print axioms compatible_integral_equation

end HMT.TerminalChannels
