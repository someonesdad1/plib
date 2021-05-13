import math
from lwtest import run, assert_equal, raises
from archimedean import SpiralArcLength
from pdb import set_trace as xx

def Test():
    # a = 1, one revolution
    a, theta = 1, 2*math.pi
    A = math.sqrt(theta**2 + 1)
    exact = a/2*(theta*A + math.log(theta + A))
    formula = SpiralArcLength(a, theta)
    assert_equal(exact, formula)
    # ValueError for a < 0
    raises(ValueError, SpiralArcLength, -1, 1)
    # Approximation:  for a large diameter circle, one revolution of a
    # fine-pitch spiral should be nearly equal to the circumference.
    n_revolutions, twopi = 10000, 2*math.pi
    theta = n_revolutions*2*math.pi
    arc_len = SpiralArcLength(a, theta) - SpiralArcLength(a, theta - 2*math.pi)
    L_D = SpiralArcLength(a, n_revolutions*twopi)
    L_d = SpiralArcLength(a, (n_revolutions - 1)*twopi)
    arc_length = L_D - L_d
    pitch = a*twopi
    D = (2*n_revolutions - 1)*pitch
    circumference = D*math.pi
    assert_equal(circumference, arc_len, reltol=1e-8)

if __name__ == "__main__":
    exit(run(globals())[0])
