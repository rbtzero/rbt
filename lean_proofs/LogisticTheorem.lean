import Mathlib.Analysis.Calculus.IteratedDeriv
open Topology
theorem LogisticTheorem :
    Continuous fun μ : ℝ => (fun x : ℝ => μ*x*(1-x))^[100] 0.5 := by
  simpa using continuous_const.iterate 