'''

ToDo
    - Rename all the functions
    - Start typing each function; get to pass with mypy
    - Reasoning:  this is a good first pass with typing to prepare me for the dp*.py
      files

Utility recipes from the itertools documentation:
    TakeFirstNItems
    TabulateAFunction
    ConsumeIterator
    ReturnNthItem
    HowManyTimesIsPredicateTrue
    PadNone
    ReturnSequencElementsNTimes
    DotProduct
    FlattenOneLevelOfNesting
    RepeatCallsToFunction
    IteratePairwise
    GroupByN
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

    Note:  Instead of using this module, it probably makes more sense to install the
    https://pypi.org/project/more-itertools/ module or the
    https://github.com/pytoolz/toolz module.

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Utility itertools recipes oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import collections
        import itertools
        import operator
        import random
        #import typing as ty
    if 1:  # Custom imports
        pass
    if 1:  # Type aliases
        pass
        #Iterable = ty.Iterable
        #Callable = ty.Callable
        #Sequence = ty.Sequence
        #Any = ty.Any
        # T represents 'Any type', but it will stay consistent within a function
        #T = ty.TypeVar('T')

    #def Func(function: ty.Callable[[int], ty.Any], x: int) -> ty.Any:
    #    return function(x)

if 0:  # Core functionality
    # Original function signatures in comments from itertools doc
    # def take(iterable, n):
    def TakeFirstNItems(iterable: ty.Iterable[ty.Any], n: int) -> list[ty.Any]:
        'Return first n items of the iterable as a list'
        return list(itertools.islice(iterable, n))
    # def tabulate(function, start=0):
    def TabulateAFunction(function: ty.Callable[[ty.Any], ty.Any],
                          start: int=0, 
                          iterable: ty.Iterable[ty.Any] | None=None) -> ty.Iterable[ty.Any]:
        '''Return an iterator that evaluates function(0), function(1), ...
        or at the arguments returned by iterable.
        '''
        if iterable:
            return map(function, iterable)
        else:
            return map(function, itertools.count(start))
    def ConsumeIterator(iterator: ty.Iterable[ty.Any], n: int|None =None) -> None:
        "Advance the iterator n-steps ahead. If n is None, consume entirely."
        # Use functions that consume iterators at C speed
        if n is None:
            # Feed the entire iterator into a zero-length deque
            collections.deque(iterator, maxlen=0)
        else:
            # Advance to the empty slice starting at position n
            next(itertools.islice(iterator, n, n), None)
    def ReturnNthItem(iterator: ty.Iterable[ty.Any], n: int, default: ty.Any|None=None) -> ty.Any:
        "Returns the nth item or a default value"
        return next(itertools.islice(iterator, n, None), default)
    def HowManyTimesIsPredicateTrue(iterable: ty.Iterable[ty.Any], 
                                    predicate: ty.Callable[[ty.Any], ty.Any]=bool) -> int:
        "Count how many times the predicate is true"
        return sum(map(predicate, iterable))
    def PadNone(iterable: ty.Iterable[ty.Any]) -> ty.Any | None:
        '''Returns the sequence elements and then returns None indefinitely.
        Useful for emulating the behavior of the built-in map() function.
        '''
        return iter(itertools.chain(iterable, itertools.repeat(None)))
    def ReturnSequencElementsNTimes(iterable: ty.Iterable[ty.Any], n: int) -> ty.Iterable[ty.Any]:
        "Returns the sequence elements n times"
        return itertools.chain.from_iterable(itertools.repeat(tuple(iterable), n))
    def DotProduct(vec1, vec2):
        return sum(map(operator.mul, vec1, vec2))
    def FlattenOneLevelOfNesting(iterable: ty.Iterable[ty.Any]) -> ty.Iterable[ty.Any]:
        "Flatten one level of nesting"
        return itertools.chain.from_iterable(iterable)
    def RepeatCallsToFunction(func: ty.Callable[..., ty.Any],
                              times: int | None = None,
                              *args: ty.Any) -> ty.Any:
        """Repeat calls to func with specified arguments."""
        if times is None:
            return itertools.starmap(func, itertools.repeat(args))
        return itertools.starmap(func, itertools.repeat(args, times))
    def IteratePairwise(iterable: ty.Iterable[ty.Any], offset: int=1) -> ty.Iterator[tuple[T, T]]:
        '''s -> (s0,s1), (s1,s2), (s2, s3), ... if offset is 1.  If offset is
        n, returns (s0,sn), (s1,s_n+1), (s2, s_n+2), ...
        '''
        assert offset > 0 and isinstance(offset, int)
        a, b = itertools.tee(iterable)
        for i in range(offset):
            next(b, None)
        return zip(a, b)
    def GroupByN(iterable: ty.Iterable[ty.Any], n: int, fillvalue: str|None=None) -> ty.Iterable[ty.Any]:
        "GroupByN(3, 'ABCDEFG', 'z') -> ABC DEF Gzz"
        args = [iter(iterable)]*n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    def roundrobin(*iterables):
        "roundrobin('ABC', 'D', 'EF') -> A D E B F C"
        # Recipe credited to George Sakkis
        pending = len(iterables)
        nexts = itertools.cycle(iter(it).__next__ for it in iterables)
        while pending:
            try:
                for next in nexts:
                    yield next()
            except StopIteration:
                pending -= 1
                nexts = itertools.cycle(itertools.islice(nexts, pending))

    def combinations_with_replacement(iterable, r):
        "Combinations_with_replacement('ABC', 2) -> AA AB AC BB BC CC"
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
        "powerset([1,2,3]) -> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

    def unique_everseen(iterable, key=None):
        "List unique elements, preserving order. Remember all elements ever seen."
        # unique_everseen('AAAABBBCCDAABBB') -> A B C D
        # unique_everseen('ABBCcAD', str.lower) -> A B C D
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in itertools.filterfalse(seen.__contains__, iterable):
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
        # unique_justseen('AAAABBBCCDAABBB') -> A B C D A B
        # unique_justseen('ABBCcAD', str.lower) -> A B C A D
        return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))

    def iter_except(func, exception, first=None):
        '''Call a function repeatedly until an exception is raised.
        
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
        pools = map(tuple, args) * kwds.get("repeat", 1)
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

if 1:   # I asked Gemini to type annotate the following and here are the results.  It
        # did it in the blink of an eye.
    import collections
    import itertools
    from itertools import islice, count, chain, repeat, starmap, zip_longest, product, combinations, cycle
    try:
        from itertools import batched # type: ignore # Python 3.12+
    except ImportError:
        # Minimal stub if you're on 3.11 but using 3.12 recipes
        def batched(iterable, n): ...

    import operator
    import typing as ty

    # --- Types & Generics ---
    T = ty.TypeVar('T')
    U = ty.TypeVar('U')

    # We use ty.Callable[..., ty.Any] as our "Safe Path" for variadic functions
    # but we can be more specific where the inputs are known.

    def take(n: int, iterable: ty.Iterable[T]) -> list[T]:
        return list(islice(iterable, n))

    def tabulate(function: ty.Callable[[int], T], start: int = 0) -> ty.Iterator[T]:
        return map(function, count(start))

    def consume(iterator: ty.Iterator[ty.Any], n: int | None = None) -> None:
        if n is None:
            collections.deque(iterator, maxlen=0)
        else:
            next(islice(iterator, n, n), None)

    def nth(iterable: ty.Iterable[T], n: int, default: T | None = None) -> T | None:
        return next(islice(iterable, n, None), default)

    def quantify(iterable: ty.Iterable[T], pred: ty.Callable[[T], bool] = bool) -> int:
        return sum(map(pred, iterable))

    def ncycles(iterable: ty.Iterable[T], n: int) -> ty.Iterator[T]:
        return chain.from_iterable(repeat(tuple(iterable), n))

    def grouper(
        iterable: ty.Iterable[T],
        n: int,
        *,
        incomplete: ty.Literal['fill', 'strict', 'ignore'] = 'fill',
        fillvalue: T | None = None
    ) -> ty.Iterator[ty.Any]: # Resulting tuples vary based on fillvalue
        args = [iter(iterable)] * n
        if incomplete == 'fill':
            return zip_longest(*args, fillvalue=fillvalue)
        if incomplete == 'strict':
            return zip(*args, strict=True)
        if incomplete == 'ignore':
            return zip(*args)
        else:
            raise ValueError('Expected fill, strict, or ignore')

    #def sumprod(vec1: ty.Iterable[float], vec2: ty.Iterable[float]) -> float:
    #    return sum(starmap(operator.mul, zip(vec1, vec2, strict=True)))

    def transpose(it: ty.Iterable[ty.Iterable[T]]) -> ty.Iterator[tuple[T, ...]]:
        return zip(*it, strict=True)

    #def matmul(m1: list[list[float]], m2: list[list[float]]) -> ty.Iterator[ty.Any]:
    #    # transpose(m2) returns an iterator of columns
    #    n = len(m2[0])
    #    return batched(starmap(sumprod, product(m1, transpose(m2))), n)

    #def convolve(signal: ty.Iterable[float], kernel: ty.Iterable[float]) -> ty.Iterator[float]:
    #    kernel_tuple = tuple(kernel)[::-1]
    #    n = len(kernel_tuple)
    #    window = collections.deque([0.0], maxlen=n)
    #    # Filling the window for the initial state
    #    for _ in range(n): window.append(0.0)
    #
    #   for x in chain(signal, repeat(0, n-1)):
    #       window.append(x)
    #       yield sumprod(kernel_tuple, window)

    def repeatfunc(func: ty.Callable[..., T], times: int | None = None, *args: ty.Any) -> ty.Iterator[T]:
        if times is None:
            return starmap(func, repeat(args))
        return starmap(func, repeat(args, times))

    def roundrobin(*iterables: ty.Iterable[T]) -> ty.Iterator[T]:
        num_active = len(iterables)
        nexts = cycle(iter(it).__next__ for it in iterables)
        while num_active:
            try:
                for next_item in nexts:
                    yield next_item()
            except StopIteration:
                num_active -= 1
                nexts = cycle(islice(nexts, num_active))

    def powerset(iterable: ty.Iterable[T]) -> ty.Iterator[tuple[T, ...]]:
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

if __name__ == "__main__":
    import dpseq
    import lwtest as lw
    n, m = 20, 5
    def Range(*p):
        return list(range(*p))
    def TestTakeFirstNItems():
        lw.Assert(TakeFirstNItems(range(n), m) == Range(m))
    def TestTabulate():
        items = Range(n)
        X = TabulateAFunction(lambda x: x * x, iterable=items)
        for i, item in enumerate(items):
            lw.Assert(next(X) == i * i)
        # Tabulate with floats
        start, stop, step = "1.5", "10.5", "0.75"
        float_list = list(dpseq.frange(start, stop, step))
        fl = dpseq.frange(start, stop, step)
        X = TabulateAFunction(lambda x: x * x, iterable=fl)
        for i in float_list:
            lw.Assert(next(X) == i * i)
    def TestConsume():
        x = iter(Range(n))
        ConsumeIterator(x, m)
        lw.Assert(list(x) == Range(m, n))
        x = iter(Range(n))
        ConsumeIterator(x)
        lw.Assert(not list(x))
    def TestReturnNthItem():
        lw.Assert(ReturnNthItem(Range(n), m) == m)
        lw.Assert(ReturnNthItem(Range(n), n) is None)
        lw.Assert(ReturnNthItem(Range(n), n, -n * m) == -n * m)
    def TestQuantify():
        lw.Assert(HowManyTimesIsPredicateTrue(Range(n), lambda x: x % 2 == 0) == n // 2)
        lw.Assert(HowManyTimesIsPredicateTrue(Range(n), lambda x: x % (n * n) == 0) == 1)
    def TestPadNone():
        x = PadNone(Range(n))
        ConsumeIterator(x, n - 1)
        lw.Assert(next(x) == n - 1)
        for i in Range(m):
            lw.Assert(next(x) is None)
    def TestNcycles():
        lw.Assert(list(ReturnSequencElementsNTimes(Range(m), m)) == Range(m) * m)
    def TestDotProduct():
        lw.Assert(DotProduct(Range(n), Range(n)) == sum(i * i for i in Range(n)))
    def TestFlattenOneLevelOfNesting():
        L = ["ABC", "DEF"]
        lst = list(FlattenOneLevelOfNesting(L))
        lw.assert_equal(lst, list("ABCDEF"))
    def TestRepeatFunc():
        def f(n):
            return n + 1
        n = 5
        lw.Assert(list(RepeatCallsToFunction(f, n, 1)) == [2] * n)
    def TestPairwise():
        x, y = Range(m), Range(1, m + 1)
        lw.Assert(list(IteratePairwise(Range(m))) == list(zip(x, y))[:-1])
        x, y = Range(m), Range(2, m + 2)
        lw.Assert(list(IteratePairwise(Range(m), 2)) == list(zip(x, y))[:-2])
    def TestGrouper():
        lw.Assert(list(GroupByN(3, Range(5), -1)) == [(0, 1, 2), (3, 4, -1)])
    def TestRoundRobin():
        lw.Assert(list(roundrobin("ABC", "D", "EF")) == "A D E B F C".split())
    def Test_combinations_with_replacement():
        s = []
        for i in combinations_with_replacement("ABC", 2):
            s.append("".join(i))
        lw.Assert(" ".join(s) == "AA AB AC BB BC CC")
    def TestPowerset():
        lw.Assert(list(powerset([1, 2, 3]))
            == [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)])
    def Test_unique_everseen():
        lw.Assert(list(unique_everseen("AAAABBBCCDAABBB")) == "A B C D".split())
        lw.Assert(list(unique_everseen("ABBCcAD", str.lower)) == "A B C D".split())
    def Test_unique_justseen():
        lw.Assert(list(unique_justseen("AAAABBBCCDAABBB")) == "A B C D A B".split())
        lw.Assert(list(unique_justseen("ABBCcAD", str.lower)) == "A B C A D".split())
    def Test_iter_except():
        def f(x=[0]):
            x[0] += 1
            if x[0] > m:
                raise Exception()
            return x[0] - 1
        lw.Assert(list(iter_except(f, Exception)) == Range(m))
    exit(lw.run(globals(), halt=1)[0])

