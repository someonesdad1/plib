from odict import odict
from lwtest import run, assert_equal

def testInitialization():
    d0 = {"one":1, "two":2}
    # Can be initialized with nothing
    d = odict()
    assert_equal(len(d), 0)
    # Can be initialized with an existing dict
    d = odict(d0)
    assert_equal(d, d0)
    # Can be initialized with sequence of (key, value) pairs
    d = odict((("one", 1), ("two", 2)))
    assert_equal(d, d0)
    # Can be initialized with sequence of keys
    d = odict(["one", "two"])
    assert_equal(d, {"one":None, "two":None})
    # Can be initialized with existing odict
    d1 = odict(d0)
    d = odict(d1)
    assert_equal(d, d0)
    # Can be initialized with two sequences of key/value pairs
    d = odict(("one", "two"), (1, 2))
    assert_equal(d, d0)
    # Can be initialized with keyword arguments
    d = odict(one=1, two=2)
    assert_equal(d, d0)
    # Example of using odict for physical units
    if 0:
        u = odict((
            ("mm", 1/1000),
            ("in", 1/39.37),
            ("cm", 1/100),
            ("ft", 0.3048),
            ("m", 1),
        ))
        print(u)

def init():
    d = odict()
    d["one"] = 1
    d["two"] = 2
    return d

def AssertSameDict(a, b):
    assert len(a) == len(b)
    assert set(a) == set(b)
    assert set(a.values()) == set(b.values())
    for i in a:
        assert a[i] == b[i]

def testClear():
    d = init()
    assert_equal(len(d), 2)
    d.clear()
    assert_equal(len(d), 0)

def testCopy():
    d = init()
    d1 = d.copy()
    AssertSameDict(d, d1)
    d1["three"] = 3
    assert d != d1

def testItems():
    d = init()
    items = list(d.items())
    assert_equal(len(items), 2)
    assert_equal(items[0], ("one", 1))
    assert_equal(items[1], ("two", 2))

def testDelItem():
    # Also tests __setitem__
    d = init()
    del d["one"]
    d1 = odict()
    d1["two"] = 2
    AssertSameDict(d, d1)

def testIter():
    # Same as testItervalues
    d = init()
    k = ("one", "two")
    for i, key in enumerate(d.iter()):
        assert_equal(key, k[i])

def testIteritems():
    d = init()
    k = (("one", 1), ("two", 2))
    for i, j in zip(d.iteritems(), k):
        assert_equal(i, j)

def testIterkeys():
    d = init()
    k = ("one", "two")
    for i, key in enumerate(d.iter()):
        assert_equal(key, k[i])

def testItervalues():
    # Same as testIter
    d = init()
    k = ("one", "two")
    for i, key in enumerate(d.iter()):
        assert_equal(key, k[i])

def testKeys():
    d = init()
    assert_equal(d.keys(), ["one", "two"])

def testPop():
    d = init()
    k = d.pop("one")
    assert_equal(k, 1)
    assert_equal(len(d), 1)
    AssertSameDict(d, {"two":2})

def testPopitem():
    d = init()
    k = d.popitem()
    assert_equal(k, ("two", 2))
    assert_equal(d, {"one":1})

def testSetdefault():
    d = init()
    value = d.setdefault("one")
    assert_equal(value, 1)
    value = d.setdefault("three")
    assert_equal(value, None)
    value = d.setdefault("four", 4)
    assert_equal(value, 4)

def testUpdate():
    d1 = odict((("one", 1), ("two", 2), ("three", 3)))
    # Update from a dict
    d = init()
    d.update({"three":3})
    AssertSameDict(d, d1)
    # Update from a odict
    d = init()
    d.update(odict((("three", 3),)))
    AssertSameDict(d, d1)
    # Update from key:value pairs
    d = init()
    d.update((("three", 3),))
    AssertSameDict(d, d1)
    # Update from keyword arguments
    d = init()
    d.update(three=3)
    AssertSameDict(d, d1)

def testValues():
    d = init()
    values = d.values()
    assert_equal(values, [1, 2])

def testRepr():
    d = odict()
    assert_equal(str(d), "odict{}")
    assert_equal(repr(d), "odict{}")

if __name__ == "__main__":
    exit(run(globals())[0])
