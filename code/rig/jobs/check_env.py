import sys
try:
    import numpy, scipy, numba, matplotlib, sequence_jacobian, torch
except Exception as ex:
    print('ENV CHECK FAILED:', ex); sys.exit(1)
print(f"env OK  numpy {numpy.__version__}  numba {numba.__version__}  torch {torch.__version__}  cuda {torch.cuda.is_available()}  gpus {torch.cuda.device_count()}")
