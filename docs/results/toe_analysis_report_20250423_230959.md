# Theory of Everything Analysis Report

Date: 2025-04-23 23:10:01

## Summary

| Simulation | Status | Time (s) |
|------------|--------|----------|
| fft_laplacian | ✅ Success | N/A |
| two_body_orbit | ✅ Success | 0.141163 |
| scale_factor | ❌ Failed | N/A |
| wave_equation | ✅ Success | 0.88368 |

## Details

### fft_laplacian

**Description**: FFT Laplacian analysis to compare spectral and finite-difference methods

**Type**: External script

**Status**: Success


### two_body_orbit

**Description**: Two-body dark matter orbit using leapfrog integration

**Type**: Direct function

**Status**: Success


**Figures**:

![two_body_orbit_20250423_231000.png](../../data/charts/two_body_orbit_20250423_231000.png)

![two_body_orbit_20250423_230942.png](../../data/charts/two_body_orbit_20250423_230942.png)


### scale_factor

**Description**: Cosmological scale factor evolution for different universe models

**Type**: Direct function

**Status**: Failed

**Error**: 'function' object has no attribute 'scale_factor'


### wave_equation

**Description**: 2D wave equation solution using the split-step method

**Type**: Direct function

**Status**: Success

**Reports**:

- [wave_equation_report_20250423_231000.md](../../data/simulations/wave_equation_report_20250423_231000.md)
- [wave_equation_report_20250423_230926.md](../../data/simulations/wave_equation_report_20250423_230926.md)

