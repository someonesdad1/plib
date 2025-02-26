from frozendict import frozendict
from collections import defaultdict, OrderedDict
from lwtest import run, assert_equal, raises

mydict = {"a": [1, 2], "b": {1: 2, 2: [3, 4]}}
d = frozendict(mydict)
hashvalue = hash(d)


def test_Hashable():
    # Check that a dict with two mutable objects can still be used
    # to construct a frozendict.
    mydict = {"a": [1, 2], "b": {1: 2, 2: [3, 4]}}
    d = frozendict(mydict)
    assert d == d
    assert d["a"] == (1, 2)
    assert d["b"] == {1: 2, 2: (3, 4)}
    assert hash(d) == hashvalue


def test_CannotBeModified():
    d = frozendict({})
    try:
        d[1] = 1
        raise SyntaxError("Modification was allowed")
    except AttributeError:
        pass
    raises(AttributeError, d.__setitem__, 1, 1)


def test_BlockedMethods():
    d = frozendict({1: 1})
    raises(AttributeError, d.__delitem__, 1)
    raises(AttributeError, d.clear)
    raises(AttributeError, d.pop)
    raises(AttributeError, d.popitem)
    raises(AttributeError, d.setdefault, 1, 1)
    raises(AttributeError, d.update, {})


def test_WithDefaultDict():
    dd = defaultdict(int)
    dd[1] += 1
    dd[2] += 1
    d = frozendict(dd)
    assert d[1] == 1
    assert d[2] == 1


def test_WithOrderedDict():
    dd = OrderedDict()
    dd[1] = 1
    dd[2] = 1
    d = frozendict(dd)
    assert d[1] == 1
    assert d[2] == 1


if __name__ == "__main__":
    exit(run(globals())[0])
