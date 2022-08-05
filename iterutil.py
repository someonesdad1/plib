'''
Utility recipes from the itertools documentation:
    take
    tabulate
    consume
    nth
    quantify
    padnone
    ncycles
    dotproduct
    repeatfunc
    pairwise
    grouper
    roundrobin
    combinations_with_replacement
    powerset
    unique_everseen
    unique_justseen
    iter_except
    random_product
    random_permutation
    random_combination
    random_combination_with_replacement

    Also includes IterSubclasses, which is a generator that will iterate
    over the subclasses of a class.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Python Software License.
    #   See https://docs.python.org/3/license.html
    #∞license∞#
    #∞what∞#
    # <utility> Utility itertools recipes.  These were taken from the
    # manual page for itertools.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    import collections
    import operator
    import random
    import itertools as it
    from pdb import set_trace as xx
def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(it.islice(iterable, n))
def tabulate(function, start=0, iterable=None):
    '''Return an iterator that evaluates function(0), function(1), ...
    or at the arguments returned by iterable.
    '''
    if iterable:
        return map(function, iterable)
    else:
        return map(function, it.count(start))
def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(it.islice(iterator, n, n), None)
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(it.islice(iterable, n, None), default)
def quantify(iterable, predicate=bool):
    "Count how many times the predicate is true"
    return sum(map(predicate, iterable))
def padnone(iterable):
    '''Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.
    '''
    return iter(it.chain(iterable, it.repeat(None)))
def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return it.chain.from_iterable(it.repeat(tuple(iterable), n))
def dotproduct(vec1, vec2):
    return sum(map(operator.mul, vec1, vec2))
def flatten(listOfLists):
    "Flatten one level of nesting"
    return it.chain.from_iterable(listOfLists)
def repeatfunc(func, times=None, *args):
    '''Repeat calls to func with specified arguments.
    Example:  repeatfunc(random.random)
    '''
    if times is None:
        return it.starmap(func, it.repeat(args))
    return it.starmap(func, it.repeat(args, times))
def pairwise(iterable, offset=1):
    '''s -> (s0,s1), (s1,s2), (s2, s3), ... if offset is 1.  If offset is
    n, returns (s0,sn), (s1,s_n+1), (s2, s_n+2), ...
    '''
    assert offset > 0 and isinstance(offset, int)
    a, b = it.tee(iterable)
    for i in range(offset):
        next(b, None)
    return zip(a, b)
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'y') --> ABC DEF Gyy"
    args = [iter(iterable)]*n
    return it.zip_longest(*args, fillvalue=fillvalue)
def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = it.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = it.cycle(it.islice(nexts, pending))
def combinations_with_replacement(iterable, r):
    "Combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"
    # number items returned:  (n+r-1)! / r! / (n-1)!
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for
                                  r in range(len(s)+1))
def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in it.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element
def unique_justseen(iterable, key=None):
    '''List unique elements, preserving order. Remember only the element
    just seen.
    '''
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return map(next, map(operator.itemgetter(1),
               it.groupby(iterable, key)))
def iter_except(func, exception, first=None):
    ''' Call a function repeatedly until an exception is raised.
 
    Converts a call-until-exception interface to an iterator interface.
    Like __builtin__.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.
 
    Examples:
        bsddbiter = iter_except(db.next, bsddb.error, db.first)
        heapiter = iter_except(functools.partial(heappop, h), IndexError)
        dictiter = iter_except(d.popitem, KeyError)
        dequeiter = iter_except(d.popleft, IndexError)
        queueiter = iter_except(q.get_nowait, Queue.Empty)
        setiter = iter_except(s.pop, KeyError)
    '''
    try:
        if first is not None:
            yield first()
        while True:
            yield func()
    except exception:
        pass
def random_product(*args, **kwds):
    "Random selection from itertools.product(*args, **kwds)"
    pools = map(tuple, args) * kwds.get('repeat', 1)
    return tuple(random.choice(pool) for pool in pools)
def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))
def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)
def random_combination_with_replacement(iterable, r):
    '''Random selection from
    itertools.combinations_with_replacement(iterable, r)
    '''
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)
def IterSubclasses(cls, seen=None):
    '''Iterator over all subclasses of a given class, in depth first
    order.  If not None, seen should be a set that will contain the
    class names already seen.
    '''
    # From http://code.activestate.com/recipes/576949
    # Downloaded Tue 12 Aug 2014 12:32:03 PM
    if not isinstance(cls, type):
        msg = "IterSubclasses must be called with new-style classes"
        raise TypeError(msg)
    if seen is None:
        seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:   # Fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in seen:
            seen.add(sub)
            yield sub
            for sub in IterSubclasses(sub, seen):
                yield sub
if __name__ == "__main__": 
    import sys
    from lwtest import run, assert_equal, Assert
    from frange import frange
    from pdb import set_trace as xx
    n, m = 20, 5
    def Range(*p):
        return list(range(*p))
    def TestTake():
        Assert(take(range(n), m) == Range(m))
    def TestTabulate():
        items = Range(n)
        X = tabulate(lambda x: x*x, iterable=items)
        for i, item in enumerate(items):
            Assert(next(X) == i*i)
        # tabulate with floats
        start, stop, step = "1.5", "10.5", "0.75"
        float_list = list(frange(start, stop, step))
        fl = frange(start, stop, step)
        X = tabulate(lambda x: x*x, iterable=fl)
        for i in float_list:
            Assert(next(X) == i*i)
    def TestConsume():
        x = iter(Range(n))
        consume(x, m)
        Assert(list(x) == Range(m, n))
        x = iter(Range(n))
        consume(x)
        Assert(not list(x))
    def TestNth():
        Assert(nth(Range(n), m) == m)
        Assert(nth(Range(n), n) is None)
        Assert(nth(Range(n), n, -n*m) == -n*m)
    def TestQuantify():
        Assert(quantify(Range(n), lambda x: x % 2 == 0) == n//2)
        Assert(quantify(Range(n), lambda x: x % (n*n) == 0) == 1)
    def TestPadnone():
        x = padnone(Range(n))
        consume(x, n - 1)
        Assert(next(x) == n - 1)
        for i in Range(m):
            Assert(next(x) is None)
    def TestNcycles():
        Assert(list(ncycles(Range(m), m)) == Range(m)*m)
    def TestDotProduct():
        Assert(dotproduct(Range(n), Range(n)) == sum(i*i for i in Range(n)))
    def TestFlatten():
        l = ["ABC", "DEF"]
        lst = list(flatten(l))
        assert_equal(lst, list("ABCDEF"))
    def TestRepeatFunc():
        def f(n):
            return n + 1
        n = 5
        Assert(list(repeatfunc(f, n, 1)) == [2]*n)
    def TestPairwise():
        x, y = Range(m), Range(1, m+1)
        Assert(list(pairwise(Range(m))) == list(zip(x, y))[:-1])
        x, y = Range(m), Range(2, m+2)
        Assert(list(pairwise(Range(m), 2)) == list(zip(x, y))[:-2])
    def TestGrouper():
        Assert(list(grouper(3, Range(5), -1)) == [(0, 1, 2), (3, 4, -1)])
    def TestRoundRobin():
        Assert(list(roundrobin('ABC', 'D', 'EF')) == "A D E B F C".split())
    def Test_combinations_with_replacement():
        s = []
        for i in combinations_with_replacement('ABC', 2):
            s.append(''.join(i))
        Assert(' '.join(s) == "AA AB AC BB BC CC")
    def TestPowerset():
        Assert(list(powerset([1, 2, 3])) == [(), (1,), (2,), (3,), (1, 2), (1, 3),
                                            (2, 3), (1, 2, 3)])
    def Test_unique_everseen():
        Assert(list(unique_everseen('AAAABBBCCDAABBB')) == "A B C D".split())
        Assert(list(unique_everseen('ABBCcAD', str.lower)) == "A B C D".split())
    def Test_unique_justseen():
        Assert(list(unique_justseen('AAAABBBCCDAABBB')) == "A B C D A B".split())
        Assert(list(unique_justseen('ABBCcAD', str.lower)) == "A B C A D".split())
    def Test_iter_except():
        def f(x=[0]):
            x[0] += 1
            if x[0] > m:
                raise Exception()
            return x[0] - 1
        Assert(list(iter_except(f, Exception)) == Range(m))
    def Test_IterSubclasses():
        class A(object):
            pass
        class B(A):
            pass
        class C(A):
            pass
        class D(B, C):
            pass
        class E(D):
            pass
        r = IterSubclasses(A)
        Assert(''.join([i.__name__ for i in r]) == "BDEC")
    exit(run(globals(), halt=1)[0])
