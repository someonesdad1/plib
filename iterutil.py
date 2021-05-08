'''
Utility recipes from the itertools documentation.
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
'''
 
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import division, print_function
import collections
import operator
import random
import sys
import itertools as it
from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

py3 = sys.version_info[0] == 3

Map = map if py3 else it.imap
Zip = zip if py3 else it.izip
Filterfalse = it.filterfalse if py3 else it.ifilterfalse

def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(it.islice(iterable, n))

def tabulate(function, start=0, iterable=None):
    '''Return an iterator that evaluates function(0), function(1), ...
    or at the arguments returned by iterable.
    '''
    if iterable:
        return Map(function, iterable)
    else:
        return Map(function, it.count(start))

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
    return sum(Map(predicate, iterable))

def padnone(iterable):
    '''Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.
    '''
    return iter(it.chain(iterable, it.repeat(None)))

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return it.chain.from_iterable(it.repeat(tuple(iterable), n))

def dotproduct(vec1, vec2):
    return sum(Map(operator.mul, vec1, vec2))

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
    return Zip(a, b)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'y') --> ABC DEF Gyy"
    args = [iter(iterable)]*n
    if py3:
        return it.zip_longest(*args, fillvalue=fillvalue)
    else:
        return it.izip_longest(fillvalue=fillvalue, *args)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = (it.cycle(iter(it).__next__ for it in iterables) if py3 else
             it.cycle(iter(it).next for it in iterables))
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
        for element in Filterfalse(seen.__contains__, iterable):
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
    return Map(next, Map(operator.itemgetter(1),
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

