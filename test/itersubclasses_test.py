from lwtest import run
from itersubclasses import IterSubclasses

def Test():
    class A(object):
        pass
    class B(A):
        pass
    class C(A):
        pass
    class D(B, C):
        pass
    class E(D):
        pass
    r = IterSubclasses(A)
    assert ''.join([i.__name__ for i in r]) == "BDEC"

if __name__ == "__main__":
    run(globals())
