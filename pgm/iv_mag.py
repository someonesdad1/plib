'''
Utility for magnification factors for IrfanView.
10;25;50;100;200;400;800;1600;3200;4000
'''
from f import flt
from pdb import set_trace as xx 
if 0:
    import debug
    debug.SetDebugger()

factor = flt(2**0.5)
o = [flt(1)]
# Get magnifications < 1
while o[-1] > flt(0.088):
    o.append(o[-1]/factor)
o = list(reversed(o))
# Get magnifications > 1
while o[-1] < flt(40):
    o.append(o[-1]*factor)
if o[-1] > 40:
    o[-1] = 40
flt(1).f = 1
o = [str(int(i*100)) for i in o]
print(';'.join(o))
