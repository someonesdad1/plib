from lwtest import run, assert_equal
from kepler import Kepler, d2r
from frange import frange

def TestCases():
    '''Run a variety of test cases on the different algorithms and show
    they all produce answers essentially equal to each other.
    '''
    tol = 1e-12
    for theta in range(5, 91):
        radians = theta*d2r
        for ecc in frange("0.1", "1.0", "0.1"):
            E = []
            for alg in range(4):
                try:
                    e, n = Kepler(radians, ecc, tol, algorithm=alg)
                except ValueError:
                    print("Too many iterations {0}".format(allowed_iterations))
                    print("theta = {theta}, ecc = {ecc:.1f}".
                          format(**locals()))
                    print("algorithm =", alg)
                    exit(1)
                E.append(e)
            actual, n = Kepler(radians, ecc, tol/100, algorithm=3)
            for i, e in enumerate(E):
                if abs(e - actual) > tol:
                    print("theta = {theta}, ecc = {ecc:.1f}".
                          format(**locals()))
                    print("E =")
                    for j, k in enumerate(E):
                        print(" ", j, "    ", k)
                    print("actual =", actual)
                    print("Error for i =", i)
                    print("  E[i] - actual =", E[i] - actual)
                    exit(1)

if __name__ == "__main__":
    run(globals())
