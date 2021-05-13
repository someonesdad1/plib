from homoglist import HomogenousList
from lwtest import run, assert_equal, raises

def Test():
    # Construct empty list
    h = HomogenousList()
    h.append(0)
    h.append(1)
    raises(ValueError, h.append, "2")
    h1 = HomogenousList(range(2))    # Construct list with sequence
    raises(ValueError, h1.append, "2")
    assert_equal(h, list(range(2)))
    assert_equal(h1, list(range(2)))
    h.extend([2, 3])
    assert_equal(h, list(range(4)))
    raises(ValueError, h.extend, ["2"])
    h.insert(0, -1)
    assert_equal(h, [-1] + list(range(4)))
    # Show two lists with different types can't be concatenated
    g = HomogenousList(["0"])
    with raises(ValueError):
        h + g

if __name__ == "__main__":
    run(globals())
