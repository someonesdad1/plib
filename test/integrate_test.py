from lwtest import run, assert_equal, raises
from integrate import Simpson, Trapezoidal

# Integrate x**2 from 0 to 3:  exact answer is 9

def f(x):
    return x**2

N = [10**i for i in range(1, 6)]
a, b, exact_answer = 0, 3, 9

def TestSimpson():
    for n in N:
        integral = Simpson(f, a, b, n)
        assert(abs(integral - exact_answer) < 1e-12)

def TestTrapezoidal():
    result = {
        10: 9.045,
        100: 9.000449999999994,
        1000: 9.000004500000005,
        10000: 9.000000045000002,
        100000: 9.000000000450042,
    }
    for n in N:
        integral = Trapezoidal(f, a, b, n)
        assert(integral == result[n])

if __name__ == "__main__":
    exit(run(globals())[0])
