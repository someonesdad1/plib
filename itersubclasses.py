# ∞test∞# ignore #∞test∞#
def IterSubclasses(cls, seen=None):
    """Iterator over all subclasses of a given class, in depth first
    order.  If not None, seen should be a set that will contain the
    class names already seen.
    """
    # From http://code.activestate.com/recipes/576949
    # Downloaded Tue 12 Aug 2014 12:32:03 PM
    if not isinstance(cls, type):
        msg = "IterSubclasses must be called with new-style classes"
        raise TypeError(msg)
    if seen is None:
        seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:  # Fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in seen:
            seen.add(sub)
            yield sub
            for sub in IterSubclasses(sub, seen):
                yield sub
