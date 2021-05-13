from laser_dist import DistAcrossRiver, CrownMoulding
from lwtest import run, assert_equal
from sig import sig
from pdb import set_trace as xx 

try:
    from uncertainties import ufloat, UFloat
    from uncertainties.umath import cos, acos, sin, asin, tan, atan
    from uncertainties.umath import sqrt, pi
except ImportError:
    pass

def TestDistAcrossRiver():
    # Should give result of 9 units for CD
    AB, BD, AC, BC, AD = 5, 7.28, 5.96, 8.98, 9.84
    x = DistAcrossRiver(AB, BD, AC, BC, AD)
    assert(abs(x[0] - 9) < 0.01)
    x_no_unc = x[0]
    # Same test, but with uncertainties
    unc = 0.05
    AB = ufloat(5, unc)
    BD = ufloat(7.28, unc)
    AC = ufloat(5.96, unc)
    BC = ufloat(8.98, unc)
    AD = ufloat(9.84, unc)
    x = DistAcrossRiver(AB, BD, AC, BC, AD)
    assert(abs(x_no_unc - x[0]) < 0.01)
    assert(abs(x[0] - 9) < 0.01)
    assert(sig(x[0]) == "9.0(2)")
def TestCrownMoulding():
    # The easiest test case is where crown angle is zero and where the wall
    # angle is a right angle.
    miter, bevel = CrownMoulding(90, 0)
    eps = 1e-15
    assert_equal(miter, 0, reltol=eps)
    assert_equal(bevel, 45, reltol=eps)
    # http://www.installcrown.com/Crown_angle_generator.html
    miter, bevel = CrownMoulding(90, 45)
    assert_equal(miter, 35.264389682754654, reltol=eps)
    assert_equal(bevel, 30, reltol=eps)
    # Some oddball numbers using above calculator
    miter, bevel = CrownMoulding(68.37, 33.77)
    assert_equal(miter, 39.29636516267699, reltol=eps)
    assert_equal(bevel, 43.444706297407485, reltol=eps)

if __name__ == "__main__":
    run(globals())
