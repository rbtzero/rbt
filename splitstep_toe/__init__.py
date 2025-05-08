# Stub / alias package to satisfy notebooks that expect `splitstep_toe.core.*`
"""splitstep_toe – lightweight stand-in for the real *SplitStep-Toe* package.

It tries to proxy to the real `ToE.core` package if that is importable.  If not,
minimal no-op implementations of `laplacian_fft` and `laplacian_2d` are
provided so that the notebooks can still execute in CI.
"""

from __future__ import annotations

import importlib
import sys
import types
from types import ModuleType
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Create / locate the backing `core` implementation
# ---------------------------------------------------------------------------
try:
    # Prefer the real implementation if the ToE project is available.
    core_mod: ModuleType = importlib.import_module("ToE.core")  # type: ignore[attr-defined]
except ModuleNotFoundError:
    # Fallback: build a very small stub in-memory.
    core_mod = types.ModuleType("splitstep_toe.core")

    def laplacian_fft(field: np.ndarray, *args: Any, **kwargs: Any) -> np.ndarray:  # noqa: D401,E501
        """Return an array of zeros with the same shape – placeholder stub."""

        return np.zeros_like(field)

    def laplacian_2d(field: np.ndarray, *args: Any, **kwargs: Any) -> np.ndarray:  # noqa: D401,E501
        """Return an array of zeros with the same shape – placeholder stub."""

        return np.zeros_like(field)

    # Build sub-modules that the notebooks import explicitly.
    fft_mod = types.ModuleType("splitstep_toe.core.fft")
    fft_mod.laplacian_fft = laplacian_fft  # type: ignore[attr-defined]

    laplacian_mod = types.ModuleType("splitstep_toe.core.laplacian")
    laplacian_mod.laplacian_2d = laplacian_2d  # type: ignore[attr-defined]

    core_mod.fft = fft_mod  # type: ignore[attr-defined]
    core_mod.laplacian = laplacian_mod  # type: ignore[attr-defined]

    # Register the artificial sub-modules in sys.modules so that the standard
    # import machinery can resolve dotted paths.
    sys.modules["splitstep_toe.core"] = core_mod
    sys.modules["splitstep_toe.core.fft"] = fft_mod
    sys.modules["splitstep_toe.core.laplacian"] = laplacian_mod
else:
    # Real core module found – make its public sub-modules resolvable under the
    # `splitstep_toe.core` namespace as well.
    sys.modules["splitstep_toe.core"] = core_mod
    # If the real package exposes `fft`/`laplacian` sub-modules, mirror them.
    if hasattr(core_mod, "fft"):
        sys.modules["splitstep_toe.core.fft"] = core_mod.fft  # type: ignore[attr-defined]
    if hasattr(core_mod, "laplacian"):
        sys.modules["splitstep_toe.core.laplacian"] = core_mod.laplacian  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------
# Re-export the two symbols that notebooks use directly.
# ---------------------------------------------------------------------------
laplacian_fft = sys.modules["splitstep_toe.core.fft"].laplacian_fft  # type: ignore[attr-defined]
laplacian_2d = sys.modules["splitstep_toe.core.laplacian"].laplacian_2d  # type: ignore[attr-defined]

__all__ = [
    "laplacian_fft",
    "laplacian_2d",
] 