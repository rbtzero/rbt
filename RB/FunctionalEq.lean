import RB.Core
open RB

lemma zetaRB_sym (s : ℂ) : zetaRB s = zetaRB (1 - s) := by
  -- quarter-turn flips phase parity; regroup inner sum
  simp [zetaRB]; ring 