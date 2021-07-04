# Written by Kevin L. Sitze on 2010-11-25.  From
# http://code.activestate.com/recipes/577470-fast-flatten-with-depth-control-and-oversight-over/?in=lang-python
# This code may be used pursuant to the MIT License.

'''This module contains four flatten() functions for generating either
a sequence or an iterator.  The goal is to "flatten" a tree (typically
comprised of lists and tuples) by slicing the elements in each
contained subtree over the subtree element itself.  For example:

    ([a, b], [c, (d, e)]) => (a, b, c, d, e)

The functions available via this module are

    flatten    ( sequence[, max_depth[, ltypes]] ) => sequence
    xflatten   ( sequence[, max_depth[, ltypes]] ) => iterator
    flatten_it ( iterable[, max_depth[, ltypes]] ) => sequence
    xflatten_it( iterable[, max_depth[, ltypes]] ) => iterator

Each function takes as its only required argument the tree to flatten.
The first two functions (flatten() and xflatten()) require their first
argument to be a valid Python sequence object.  The '_it' functions
(flatten_it() and xflatten_it()) accept any iterable object.

The return type for the flatten() and xflatten_it functions is the
same type as the input sequence, when possible, otherwise the type
will be 'list'.

Wall clock speed of these functions increase from the top of the list
down (i.e., where possible prefer the flatten() function to any other
if speed is a concern).

The "max_depth" argument is either a non-negative integer indicating
the maximum tree depth to flatten; or "None" to flatten the entire
tree.  The required "sequence" argument has a 'depth' of zero; a list
element of the sequence would be flattened if "max_depth" is greater
than or equal to one (1).  A negative depth is treated the same as a
depth of zero.

The "ltypes" argument indicates which elements are subtrees.  It may
be either a collection of sequence types or a predicate function.  If
"ltypes" is a collection a subtree is expanded if its type is in the
collection.  If "ltypes" is a predicate function a subtree is expanded
if the predicate function returns "True" for that subtree.

The implementation of flatten here runs in O(N) time where N is the
number of elements in the traversed tree.  It uses O(N+D) space
where D is the maximum depth of the traversed tree.
'''

import sys

_py3 = True if sys.version_info[0] == 3 else False

def flatten(L, max_depth=None, ltypes=(list, tuple)):
    '''flatten(sequence[, max_depth[, ltypes]]) => sequence
 
    Flatten every sequence in "L" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.
 
    The sequence returned has the same type as the input sequence.
    '''
    if max_depth is None:
        make_flat = lambda x: True
    else:
        make_flat = lambda x: max_depth > len(x)
    if callable(ltypes):
        is_sequence = ltypes
    else:
        is_sequence = lambda x: isinstance(x, ltypes)
    r, s = [], []
    s.append((0, L))
    while s:
        i, L = s.pop()
        while i < len(L):
            while is_sequence(L[i]):
                if not L[i]:
                    break
                elif make_flat(s):
                    s.append((i + 1, L))
                    L = L[i]
                    i = 0
                else:
                    r.append(L[i])
                    break
            else:
                r.append(L[i])
            i += 1
    try:
        return type(L)(r)
    except TypeError:
        return r

def xflatten(L, max_depth=None, ltypes=(list, tuple)):
    '''xflatten(sequence[, max_depth[, ltypes]]) => iterable
 
    Flatten every sequence in "L" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.
 
    This is the iterator version of the flatten function.
    '''
    if max_depth is None:
        make_flat = lambda x: True
    else:
        make_flat = lambda x: max_depth > len(x)
    if callable(ltypes):
        is_sequence = ltypes
    else:
        is_sequence = lambda x: isinstance(x, ltypes)
    r, s = [], []
    s.append((0, L))
    while s:
        i, L = s.pop()
        while i < len(L):
            while is_sequence(L[i]):
                if not L[i]:
                    break
                elif make_flat(s):
                    s.append((i + 1, L))
                    L = L[i]
                    i = 0
                else:
                    yield L[i]
                    break
            else:
                yield L[i]
            i += 1

def flatten_it(L, max_depth=None, ltypes=(list, tuple)):
    '''flatten_it(iterator[, max_depth[, ltypes]]) => sequence
 
    Flatten every sequence in "L" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.
 
    The sequence returned has the same type as the input sequence.
    '''
    if max_depth is None:
        make_flat = lambda x: True
    else:
        make_flat = lambda x: max_depth > len(x)
    if callable(ltypes):
        is_iterable = ltypes
    else:
        is_iterable = lambda x: isinstance(x, ltypes)
    r, s = [], []
    s.append((iter(L)))
    while s:
        i = s.pop()
        try:
            while True:
                e = i.next() if not _py3 else i.__next__()
                if is_iterable(e):
                    if make_flat(s):
                        s.append((i))
                        i = iter(e)
                    else:
                        r.append(e)
                else:
                    r.append(e)
        except StopIteration:
            pass
    try:
        return type(L)(r)
    except TypeError:
        return r

def xflatten_it(L, max_depth=None, ltypes=(list, tuple)):
    '''xflatten_it(iterator[, max_depth[, ltypes]]) => iterator
 
    Flatten every sequence in "L" whose type is contained in "ltypes"
    to "max_depth" levels down the tree.  See the module documentation
    for a complete description of this function.
 
    This is the iterator version of the flatten_it function.
    '''
    if max_depth is None:
        make_flat = lambda x: True
    else:
        make_flat = lambda x: max_depth > len(x)
    if callable(ltypes):
        is_iterable = ltypes
    else:
        is_iterable = lambda x: isinstance(x, ltypes)
    r, s = [], []
    s.append((iter(L)))
    while s:
        i = s.pop()
        try:
            while True:
                e = i.next() if not _py3 else i.__next__()
                if is_iterable(e):
                    if make_flat(s):
                        s.append((i))
                        i = iter(e)
                    else:
                        yield e
                else:
                    yield e
        except StopIteration:
            pass

if __name__ == '__main__':
    import sys
    import traceback
    from lwtest import run, assert_equal
    def Test():
        def test(exp, got, depth=None):
            assert_equal(exp, flatten(got, depth))
            assert_equal(exp, tuple(xflatten(got, depth)))
            assert_equal(exp, flatten_it(got, depth))
            assert_equal(exp, tuple(xflatten_it(got, depth)))
        test((),      ())
        test((),      (()))
        test((),      ((),()))
        test((),      ((),((),()),()))
        test((1,),    ((1,),((),()),()))
        test((1,),    ((),1,((),()),()))
        test((1,),    ((),(1,(),()),()))
        test((1,),    ((),((1,),()),()))
        test((1,),    ((),((),1,()),()))
        test((1,),    ((),((),(1,)),()))
        test((1,),    ((),((),(),1),()))
        test((1,),    ((),((),()),1,()))
        test((1,),    ((),((),()),(1,)))
        test((1,),    ((),((),()),(),1))
        test((1,),    ((),1,()))
        test((1,2,3), (1,2,3))
        test((1,2,3), ((1,2),3))
        test((1,2,3), (1,(2,3)))
        test((1,2,3), ((1,),(2,),3))
        test(((((((((((0,),1),2),3),4),5),6),7),8),9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 0)
        test((((((((((0,),1),2),3),4),5),6),7),8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 1)
        test(((((((((0,),1),2),3),4),5),6),7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 2)
        test((((((((0,),1),2),3),4),5),6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 3)
        test(((((((0,),1),2),3),4),5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 4)
        test((((((0,),1),2),3),4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 5)
        test(((((0,),1),2),3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 6)
        test((((0,),1),2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 7)
        test(((0,),1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 8)
        test((0,1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 9)
        test((0,1,2,3,4,5,6,7,8,9), ((((((((((0,),1),2),3),4),5),6),7),8),9), 10)
        test(({1:2},3,4,set([5,6])), ({1:2},(3,4),set([5,6])))
        # Build a tree n elements deep
        n, L = int(1e4), (1,)
        for i in range(n):
            L = (L, 2)
        # Expected value is a 1 followed by n 2's
        exp = (1,) + (2,)*n
        got = flatten(L)
        assert(exp == got)
        got = tuple(xflatten(L))
        assert(exp == got)
        got = flatten_it(L)
        assert(exp == got)
        got = tuple(xflatten_it(L))
        assert(exp == got)
    run(globals(), halt=1)
