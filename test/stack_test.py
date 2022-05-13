import sys
from stack import Stack
from lwtest import run, raises
from pdb import set_trace as xx 

n = 5

def init():
    'Make a stack with n integers'
    st = Stack()
    for i in range(n):
        st.push(i)
    return st

def TestLen():
    st = init()
    assert(len(st) == n)

def TestPop():
    st = init()
    R = list(st)
    for i in R:
        assert(st.pop() == i)
    assert(len(st) == 0)
    assert(not st)
    with raises(IndexError):
        st.pop()

def TestPush():
    st = Stack()
    r = list(range(n))
    R = list(reversed(r))
    for i in r:
        st.push(i)
    assert(list(st) == R)
    for i in R:
        assert(st.pop() == i)
    assert(len(st) == 0)
    assert(not st)

def TestCopy():
    'The copy() method appeared in python 3.5.'
    v = sys.version_info
    if v[0] < 3 or (v[0] == 3 and v[1] < 5):
        return
    st = init()
    s = st.copy()
    assert(st == s)
    assert(id(st) != id(s))

def TestClear():
    st = init()
    assert(len(st) == n)
    st.clear()
    assert(len(st) == 0)

def TestHomogeneity():
    st = Stack(['a', 'b'], homogeneous='a')
    assert(st.homogeneous and st.homogeneous == type('a'))
    raises(TypeError, st.push, 1)
    st.push("b")
    # Non-homogeneous allows homogeneity
    st = init()
    st.push("a")

def TestMaxlen():
    st = Stack([1, 2], maxlen=2)
    st.push(3)
    assert(list(st) == [3, 1])
    assert(st.maxlen == 2)

if __name__ == "__main__":
    exit(run(globals())[0])
