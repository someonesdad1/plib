# Plot copper wire diameter versus chassis current

from pylab import *
from get import GetNumberArray
from f import flt

# Wire dia in mm, chassis current in A
data = '''
    11.7   380
    10.4   330
    9.27   280
    8.25   240
    6.54   180
    5.19   140
    4.11   100
    3.26    73
    2.59    55
    2.05    41
    1.63    32
    1.29    22
    1.02    16
    .813    11
    .643   7.0
    .511   3.5
    .404   2.2
    .320   1.4
    .254   0.860
'''
a = GetNumberArray(data)
dia, i = a
plot(dia, i, "b.-", label="Data")
if 0:
    # Linear approximation
    plot((3.26, 11.7), (73, 370), "r-", label="Linear approx.")
    plot((0.32, 3.26), (1.4, 73), "g-", label="Linear approx.")
if 1:
    # Quadratic approximation
    # First coefficients are from regression
    b0, b1, b2 = -7.64555, 22.6453, 0.913065
    # Second coefficients are reasonable approximations
    b0, b1, b2 = -7.6, 22.6, 0.9
    i_pred = [b0 + b1*x + b2*x**2 for x in dia]
    plot(dia, i_pred, "r-", label="Quadratic approx.")
    plot(dia, [b1*x + b2*x**2 for x in dia], "g-", label="Even simpler")
grid()
xlabel("d = diameter, mm")
ylabel("i = chassis current, A")
text(1, 325, "$i = 0.9d^2 + 22.6d - 7.6$")
title("Copper wire allowed current in air\n(Based on MIL-W-5088L) DP 20 Sep 2024")
legend(loc="lower right")
# Show residuals
resid = [flt((a - b)/b*100) for a, b in zip(i_pred, i)]
print(' '.join([str(i) for i in resid]))
exit() #xx

if 1:
    show()
else:
    savefig("cu_ampacity", dpi=200)
