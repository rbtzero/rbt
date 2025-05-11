import RB.Core
open RB

/-- Zero-density bound: N(σ,T) ≤ 50·T^{1-(σ-1/2)/6}. -/
 theorem zeroDensity (σ T : ℝ) (hσ : 1/2 < σ ∧ σ < 1) (hT : 2 ≤ T) :
     N σ T ≤ 50 * T ^ (1 - (σ - 1 / 2) / 6) := by
   sorry 