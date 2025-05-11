import Mathlib.Data.Complex.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Pow
import Mathlib.Tactic

/-
  Core ledger objects shared by every RB formal proof.
  Δ-glitch → depth n, branch tag s, amplitude Ψₙ(s).
-/

namespace RB

/-- Depth index n (ℕ). -/
abbrev Depth := Nat

/-- Branch tag at depth n is a bitstring of length n. -/
def Tag (n : Depth) := Fin (Nat.pow 2 n)

open Complex Real

/-- Complex amplitude carried by a tag.  Defined by the quarter-turn recursion. -/
noncomputable def ψ : {n : Depth} → Tag n → ℂ
| 0, _ => 1
| n+1, t =>
  let parent : Tag n := ⟨t / 2, by
    have : (t / 2) < 2 ^ (n) := 
      Nat.div_lt_pow_two _ (Nat.succ_pos _)
    simpa using this⟩
  let phase : ℂ := Complex.I ^ (t % 2) / Real.sqrt 2
  phase * ψ parent

/-- RB ζ-function ≔ sum over branch phases / depth^s. -/
noncomputable def zetaRB (s : ℂ) : ℂ :=
  ∑ n : ℕ, (∑ t : Tag n, ψ t) / (n.succ : ℂ) ^ s

end RB 