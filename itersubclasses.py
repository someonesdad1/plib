def IterateOverSubclasses(cls, seen=None):
    '''Iterator over all subclasses of a given class, in depth first order.  If not
    None, seen should be a set that will contain the class names already seen.
    Downloaded Tue 12 Aug 2014 from http://code.activestate.com/recipes/576949; URL
    defunct as of 2 Feb 2026
    '''
    if not isinstance(cls, type):
        raise TypeError("IterateOverSubclasses must be called with new-style classes")
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
            for sub in IterateOverSubclasses(sub, seen):
                yield sub
