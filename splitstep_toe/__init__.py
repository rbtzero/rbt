# Alias package to point notebooks to existing code in ToE
import importlib, types, sys

alias = types.ModuleType(__name__)
try:
    alias.core = importlib.import_module('ToE.core')
except ModuleNotFoundError:
    # provide minimal stub so import works
    import types, numpy as np
    core_stub = types.ModuleType('core')
    def laplacian_fft(field,*args,**kwargs):
        return np.zeros_like(field)
    def laplacian_2d(field,*args,**kwargs):
        return np.zeros_like(field)
    core_stub.fft = types.ModuleType('fft')
    core_stub.laplacian = types.ModuleType('laplacian')
    core_stub.fft.laplacian_fft = laplacian_fft
    core_stub.laplacian_2d = laplacian_2d
    alias.core = core_stub
sys.modules[__name__] = alias 