import sys
from lwtest import run, assert_equal, raises
from iterutil import *
import itertools as it
from frange import frange
from pdb import set_trace as xx

n, m = 20, 5

def Range(*p):
    return list(range(*p))
def TestTake():
    assert(take(range(n), m) == Range(m))
def TestTabulate():
    items = Range(n)
    X = tabulate(lambda x: x*x, iterable=items)
    for i, item in enumerate(items):
        assert(next(X) == i*i)
    # tabulate with floats
    start, stop, step = "1.5", "10.5", "0.75"
    float_list = list(frange(start, stop, step))
    fl = frange(start, stop, step)
    X = tabulate(lambda x: x*x, iterable=fl)
    for i in float_list:
        assert(next(X) == i*i)
def TestConsume():
    x = iter(Range(n))
    consume(x, m)
    assert(list(x) == Range(m, n))
    x = iter(Range(n))
    consume(x)
    assert(not list(x))
def TestNth():
    assert(nth(Range(n), m) == m)
    assert(nth(Range(n), n) is None)
    assert(nth(Range(n), n, -n*m) == -n*m)
def TestQuantify():
    assert(quantify(Range(n), lambda x: x % 2 == 0) == n//2)
    assert(quantify(Range(n), lambda x: x % (n*n) == 0) == 1)
def TestPadnone():
    x = padnone(Range(n))
    consume(x, n - 1)
    assert(next(x) == n - 1)
    for i in Range(m):
        assert(next(x) is None)
def TestNcycles():
    assert(list(ncycles(Range(m), m)) == Range(m)*m)
def TestDotProduct():
    assert(dotproduct(Range(n), Range(n)) == sum(i*i for i in Range(n)))
def TestFlatten():
    l = ["ABC", "DEF"]
    lst = list(flatten(l))
    assert_equal(lst, list("ABCDEF"))
def TestRepeatFunc():
    def f(n):
        return n + 1
    n = 5
    assert(list(repeatfunc(f, n, 1)) == [2]*n)
def TestPairwise():
    x, y = Range(m), Range(1, m+1)
    assert(list(pairwise(Range(m))) == list(zip(x, y))[:-1])
    x, y = Range(m), Range(2, m+2)
    assert(list(pairwise(Range(m), 2)) == list(zip(x, y))[:-2])
def TestGrouper():
    assert(list(grouper(3, Range(5), -1)) == [(0, 1, 2), (3, 4, -1)])
def TestRoundRobin():
    assert(list(roundrobin('ABC', 'D', 'EF')) == "A D E B F C".split())
def Test_combinations_with_replacement():
    s = []
    for i in combinations_with_replacement('ABC', 2):
        s.append(''.join(i))
    assert(' '.join(s) == "AA AB AC BB BC CC")
def TestPowerset():
    assert(list(powerset([1, 2, 3])) == [(), (1,), (2,), (3,), (1, 2), (1, 3),
                                         (2, 3), (1, 2, 3)])
def Test_unique_everseen():
    assert(list(unique_everseen('AAAABBBCCDAABBB')) == "A B C D".split())
    assert(list(unique_everseen('ABBCcAD', str.lower)) == "A B C D".split())
def Test_unique_justseen():
    assert(list(unique_justseen('AAAABBBCCDAABBB')) == "A B C D A B".split())
    assert(list(unique_justseen('ABBCcAD', str.lower)) == "A B C A D".split())
def Test_iter_except():
    def f(x=[0]):
        x[0] += 1
        if x[0] > m:
            raise Exception()
        return x[0] - 1
    assert(list(iter_except(f, Exception)) == Range(m))

if __name__ == "__main__":
    exit(run(globals(), halt=1, dbg=0)[0])
