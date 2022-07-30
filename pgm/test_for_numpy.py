'''
This script will print whether numpy, matplotlib, scipy are available
'''
from color import t
import sys
v = sys.version_info
ver = f"{v.major}.{v.minor}.{v.micro}"
t.numpy = t("grnl")
t.matplotlib = t("ornl")
t.scipy = t("purl")
t.nope = t("redl")
print(f"python version {ver}")
try:
    import numpy
    t.print(f"{t.numpy}Have numpy")
except ImportError:
    t.print(f"{t.nope}numpy not available")
try:
    import matplotlib
    t.print(f"{t.matplotlib}Have matplotlib")
except ImportError:
    t.print(f"{t.nope}matplotlib not available")
try:
    import scipy
    t.print(f"{t.scipy}Have scipy")
except ImportError:
    t.print(f"{t.nope}scipy not available")
