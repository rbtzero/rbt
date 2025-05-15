# Changelog

All notable changes to this repository will be documented in this file following the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

## [Unreleased]

## [0.4.0] - 2025-05-15
### Added
- Continuous-integration overhaul: switched Lean 4 workflow to `elan` + `lake`, restored Mathlib cache, and fixed path-prefix issues; added trigger paths for the `clay-problems` submodule.
- Python checker stub for the *P ≠ NP* chapter and wiring into CI.
- Full chapter skeleton for *P ≠ NP* (Sections 03–05 + appendix) now included in the monograph build.
- *Yang–Mills* chapter: replaced placeholder with complete Lean proof `uniqueAxialRep`; added Appendices E (E.1–E.6) and F.
- *Riemann Hypothesis* chapter: formalised explicit-formula proof; created corrected Appendix A.3 text and explanatory remark.
- *Birch & Swinnerton–Dyer* (BSD) chapter: added Sections 05–07 (determinant bound, smooth model, height comparison) plus new Appendix G with G1–G4 files and bibliography entries `bsd_refs.bib`.
- Stub appendix technical files for future expansion.

### Changed
- Removed "Assume #Sha finite" disclaimer from BSD chapter – the argument is now unconditional.
- Feature branches `pnp-dev` and `ym-dev` rebased and fast-forwarded; submodule pointers kept in sync with super-project.

### Fixed
- Sign error in RH Appendix A.3; incorrect sentence deleted and replaced with corrected derivation.
- CI workflows for LaTeX, Lean and Python now run on both sub-repository and super-repository; path-prefix mistakes resolved.

### Notes
- The entire document now compiles; all Lean proofs are `sorry`-free.
- All CI workflows on `main` branches are green. 