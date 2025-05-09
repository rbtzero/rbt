import Lake
open Lake DSL

package rb_lean where
  moreLeanArgs := #["-O2"]

lean_lib RBProofs where
  globs := #[`AxiomUniqueness, `NumberTower, `BornRule,
            `GaugeStack, `MassFormula, `LogisticTheorem] 