from bidict import bidict
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

def init():
    keys, values   = ["jan", "feb"], [1, 2]
    d = dict(zip(keys, values))
    bd = bidict(d)
    Check(bd, keys, values)
    return keys, values, bd

def Check(bd, keys, values):
    assert(isinstance(bd, bidict))
    for i in bd:
        assert(i in keys)
    for i in bd.values():
        assert(i in values)
    assert(set(bd.keys()) == set(bd._inv.values()))
    assert(set(bd.values()) == set(bd._inv.keys()))

def TestLookup():
    keys, values, bd = init()
    assert(bd["jan"] == 1)
    assert(bd(1) == "jan")

def TestKeysAndValues():
    keys, values, bd = init()
    assert(set(values) == set(bd.values()))
    assert(set(keys) == set(bd.keys()))

def TestAddDeleteNewValue():
    keys, values, bd = init()
    bd["mar"] = 3
    keys.append("mar")
    values.append(3)
    Check(bd, keys, values)
    # Show we can delete it
    del bd["mar"]
    del keys[-1]
    del values[-1]
    Check(bd, keys, values)

def TestSwapDictionaries():
    keys, values, bd = init()
    rev_bd = bd.invert()
    Check(rev_bd, values, keys)

def TestMethods():
    keys, values, bd = init()
    assert(set(bd.items()) == set(zip(keys, values)))
    assert("jan" in bd)
    assert(bd.get("xyz", 88) == 88)
    assert(bd.get("jan", None) == 1)
    b2 = bd.copy()
    assert(bd == b2) # Can be tested for equality
    b2.clear()
    assert(not len(b2))
    b2 = bd.copy()
    assert(b2.setdefault("jun", 89) == 89)
    assert(b2.setdefault("jun") == 89)
    #assert(set(bd.iterkeys()) == set(bd.keys()))
    #assert(set(bd.itervalues()) == set(bd.values()))
    value = b2.pop("jun")
    assert(value == 89)
    # Get exception on empty pops
    raises(KeyError, b2.pop, "xyz")
    raises(KeyError, b2.pop, "jun")
    # Show default value for pop works
    value = b2.pop("jun", 91)
    assert(value == 91)
    key, value = b2.popitem()
    assert(len(b2) == 1)
    # Get ValueError exception for a duplicate value
    raises(ValueError, bd.__setitem__, "xyz", 2)
    # Get key error for accessing nonexistent key
    raises(KeyError, b2.__getitem__, "xyz")
    # Get key error for accessing nonexistent value
    raises(KeyError, b2, 1000)

def TestCannotUseMutableObject():
    keys, values, bd = init()
    d = dict([("jan", [1])])
    raises(TypeError, bidict, d)
    # OK to use a tuple
    d = dict([("jan", (1,))])
    bidict(d)

def TestUpdate():
    keys, values, bd = init()
    # Update with dict
    d = {"new":24}
    bd.update(d)
    assert(bd["new"] == 24)
    assert(bd(24) == "new")
    # Update with key/value pair iterable
    keys, values, bd = init()
    d = [("new", 24)]
    bd.update(d)
    assert(bd["new"] == 24)
    assert(bd(24) == "new")
    # Update with keywords
    keys, values, bd = init()
    bd.update(new=24)
    assert(bd["new"] == 24)
    assert(bd(24) == "new")
    # TypeError if update with mutable
    keys, values, bd = init()
    d = {"new" : [1, 2]}
    raises(TypeError, bd.update, d)

def TestFrozen():
    keys, values, bd = init()
    bd.frozen = True
    with raises(ValueError):
        del bd["jan"]

if __name__ == "__main__":
    exit(run(globals())[0])
