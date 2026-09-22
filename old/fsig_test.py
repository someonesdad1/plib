from lwtest import run, assert_equal, raises
from fsig import fsig
from pdb import set_trace as xx


def Test_fsig():
    p = 3.141592653
    data = """-10 3.14e-10
              -9 3.14e-09
              -8 3.14e-08
              -7 3.14e-07
              -6 0.00000314
              -5 0.0000314
              -4 0.000314
              -3 0.00314
              -2 0.0314
              -1 0.314
              0 3.14
              1 31.4
              2 314
              3 3140
              4 31400
              5 314000
              6 3.14e+06
              7 3.14e+07
              8 3.14e+08
              9 3.14e+09
              10 3.14e+10"""
    for line in data.split("\n"):
        e, s = line.split()
        x = p * 10 ** (int(e))
        assert s == fsig(x)


if __name__ == "__main__":
    exit(run(globals())[0])
