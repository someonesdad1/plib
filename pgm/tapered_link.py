from __future__ import print_function, division
from math import asin, pi
import shop_util

shop_util.debug = 0

print("Calculations for tapered, radiused-end links")
print("  All dimensions in inches\n")

inf = 1e300
r1 = shop_util.GetDouble("Small end radius?", "0.5", 0, inf)
d1 = shop_util.GetDouble("Small end hole diameter?", "0.25", 0, inf)
r2 = shop_util.GetDouble("Big end radius?", "0.75", 0, inf)
d2 = shop_util.GetDouble("Big end hole diameter?", "0.5", 0, inf)
d = shop_util.GetDouble("Distance between hole centers?", "2", 0, inf)

theta1 = asin((r2 - r1) / d) * 180 / pi
theta2 = 180 - 2 * theta1
theta3 = 180 + 2 * theta1
h = r2 - r1 + (d2 - d1) / 2

print("  Angle of tapered side       = %.2lf deg" % theta1)
print("  Included angle of small end = %.2lf deg" % theta2)
print("  Included angle of big end   = %.2lf deg" % theta3)
print("  Small end shim height       = %.4lf in" % h)

print(
    """
Instructions:
    Drill holes at both ends.  Put close-fitting pins in each hole.
    Chuck piece in milling vise with pins horizontal and resting on
    the top of a jaw.  Put indicated shim under small end and mill
    side taper.  Repeat for other side.  Use included angles to
    indicate when to stop milling.
"""[:-1]
)
