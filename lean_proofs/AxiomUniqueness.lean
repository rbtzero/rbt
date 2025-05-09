import Mathlib.Topology.Basic
theorem AxiomUniqueness : ¬ ∃ f : Bool → Bool, Function.LeftInverse f Bool.not := by
  intro h; cases h with | intro f hf => exact Bool.noConfusion (hf rfl) 