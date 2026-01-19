import sys
import time
from lwtest import run
from bitfield import bitfield
from pdb import set_trace as xx


def Check(size):
    start = time.time()
    err = Exception("Test failed for size %d" % size)
    a = bitfield(size)
    b = bitfield(size, init_with_ones=0)
    o = bitfield(size, init_with_ones=1)
    b.set_bit(size - 1)
    assert b.is_set(size - 1)
    b.clear_bit(size - 1)
    assert b.is_clear(size - 1)
    b.set_bit(size - 2)
    if not b.is_set(size - 2):
        raise err
    b.clear_bit(size - 2)
    if not b.is_clear(size - 2):
        raise err
    b.set_bit(0)
    if not b.is_set(0):
        raise err
    b.clear_bit(0)
    if not b.is_clear(0):
        raise err
    b.set_bit(1)
    if not b.is_set(1):
        raise err
    b.clear_bit(1)
    if not b.is_clear(1):
        raise err
    if a != b:
        raise err
    b.set_to_ones()
    if b != o:
        raise err
    b.set_to_zeros()
    if a != b:
        raise err
    finish = time.time()
    # print("Size %.1e time = %.2f sec" % (size, finish - start))


def Test():
    for size in [2, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7]:
        Check(int(size))


if __name__ == "__main__":
    run(globals())
