import sys
from stack import Stack
from lwtest import run, raises
n = 5
def init():
    "Make a stack with n integers"
    st = Stack()
    for i in range(n):
        st.push(i)
    return st
def TestLen():
    st = init()
    assert len(st) == n
def TestPop():
    st = init()
    R = list(st)
    n = len(R)
    for i in range(n):
        item = st.pop()
        ritem = R.pop()
        assert item == ritem
    assert len(st) == 0
    assert not st
    with raises(IndexError):
        st.pop()
def TestPush():
    st = Stack()
    r = list(range(n))
    R = list(reversed(r))
    for i in r:
        st.push(i)
    assert list(st) == r
    for i in R:
        assert st.pop() == i
    assert len(st) == 0
    assert not st
def TestCopy():
    "The copy() method appeared in python 3.5."
    v = sys.version_info
    if v[0] < 3 or (v[0] == 3 and v[1] < 5):
        return
    st = init()
    s = st.copy()
    assert st == s
    assert id(st) != id(s)
def TestClear():
    st = init()
    assert len(st) == n
    st.clear()
    assert len(st) == 0
def TestHomogeneity():
    # Homogeneous means here st can only contain strings
    st = Stack(["a", "b"], homogeneous=str)
    assert st.homogeneous is str
    raises(TypeError, st.push, 1)
    st.push("b")
    assert str(st) == "Stack(['a', 'b', 'b'], homogeneous=<class 'str'>)"
    # Non-homogeneous
    st = Stack()
    st.push("a")
    st.push(1)
    assert str(st) == "Stack(['a', 1])"
def TestMaxlen():
    st = Stack([1, 2], maxlen=2)
    st.push(3)
    assert list(st) == [2, 3]
    assert st.maxlen == 2
if __name__ == "__main__":
    exit(run(globals())[0])
