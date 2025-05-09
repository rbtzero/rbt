import Mathlib.Algebra.Algebra.Subfield
theorem MassFormula : (∀ n : ℕ, (2:ℚ) ^ (-n) ≠ 0) := by
  intro n; simp [pow_neg] 