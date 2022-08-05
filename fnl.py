'''
Some higher-order functions useful for text processing.  Reference:
D. Mertz, "Text Processing in Python" (see http://gnosis.cx/TPiP/).

A higher-order function is a function that returns another function or
takes functions as arguments.

This module redefines Mertz's one-liners to become regular functions
with a bit of documentation.  This helped me understand what they were
intended to do.

When run as a script, examples will be printed to stdout showing
functionality.

Example from Mertz's book (search for '#*------ Boolean algebra of
composed functions ------#'):

    Suppose you had four functions that process a line of text:  f1, f2,
    f3, and f4.  These functions return Boolean values.  You want each
    line x of your input text to have (f1(x) or f2(x) be true along with
    (f3(x) or f4(x)) also true.  This could be done as follows:
        satisfied = all(any_f(f1, f2), any_f(f3, f4))
        selected = filter(satisfied, lines)
    or the last line could be the more readable
        selected = [line in lines if satisfied(line)]
'''
if 1:  # License
    # These "trigger strings" can be managed with trigger.py
    #∞license∞#
    # Note:  David Mertz's site https://gnosis.cx/TPiP/ appears to state
    # (downloaded on 10 Jun 2021) that the book's copyright is owned by
    # Addison-Wesley, but the code samples are released into the public
    # domain.  Because of this, the following license text is deemed
    # appropriate.
    #
    # This is free and unencumbered software released into the public
    # domain.
    #
    # Anyone is free to copy, modify, publish, use, compile, sell, or
    # distribute this software, either in source code form or as a
    # compiled binary, for any purpose, commercial or non-commercial,
    # and by any means.
    #
    # In jurisdictions that recognize copyright laws, the author or
    # authors of this software dedicate any and all copyright interest
    # in the software to the public domain.  We make this dedication for
    # the benefit of the public at large and to the detriment of our
    # heirs and successors.  We intend this dedication to be an overt
    # act of relinquishment in perpetuity of all present and future
    # rights to this software under copyright law.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    # MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    # NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY
    # CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
    # CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    # WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    #∞license∞#
    #∞what∞#
    # <programming> Functional programming examples from D. Mertz, "Text
    # Processing in Python" (see http://gnosis.cx/TPiP).
    #∞what∞#
    #∞test∞# ignore #∞test∞#
    pass
if 1:   # Imports
    import sys
    from operator import mul, add
    from functools import reduce
    from pdb import set_trace as xx
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
''' The reduce function as used here can be written as
def reduce(function, seq):
    it = iter(seq)
    value = next(it)
    for element in it:
        value = function(value, element)
    return value
'''
def apply(f, p, kw={}):
    '''apply() was a function in python 2; it's not in python 3.
    apply(f, (a, b, c)) returns f(a, b, c).  In python 3, you use
    the asterisk notation on f directly.
    '''
    return f(*p, **kw)
def apply_each(functions, x=[]):
    '''Apply a sequence of univariate functions to an argument x and
    return the list [f0(x), f1(x), ...].  Note the functions can take no
    argument.
    '''
    return list(map(apply, functions, [x]*len(functions)))
def bools(seq):
    '''Return a list of True or False elements corresponding to each
    element of seq.
    '''
    return [bool(i) for i in seq]
def bool_each(functions, x=[]):
    '''Return a list of True or False elements corresponding to each
    application of the sequence of functions called with the argument
    x.
    '''
    return bools(apply_each(functions, x))
def all_f(functions, x=[]):
    '''Return True if all of the univariate functions evaluated at x
    return True; return False otherwise.  Note x must be a sequence
    (this is needed because of the ultimate call to apply_each).
    '''
    if not functions:
        return False
    return all(bool_each(functions, x))
def any_f(functions, x=[]):
    '''Return True if any of the univariate functions evaluated at x
    return True; return False otherwise.  Note x must be a sequence
    (this is needed because of the ultimate call to apply_each).
    '''
    return any(bool_each(functions, x))
def compose(*functions):
    '''For a sequence of univariate functions <f0, f1, ...>, return
    the function composition ...f2(f1(f0(x))).
    '''
    compose2 = lambda f0, f1: lambda x: f0(f1(x))
    return reduce(compose2, functions)
def and_f(functions, x):
    '''Same as all_f except short-circuit evaluation is used:
    returns f0(x) and f1(x) and f2(x) and ...  Short-circuit
    evaluation means the function will return as soon as a False
    function value is detected.
 
    This function is to be preferred over all_f() when the functions in
    functions do not have any side effects, because execution will
    generally be faster.  Use all_f when you want all of the functions
    to be evaluated (e.g., they have some desired side effect).
    '''
    if not functions:
        return lambda y: False
    flag = True
    for f in functions:
        flag &= bool(f(x))
        if not flag:
            return lambda y: False
    return lambda y: True
def or_f(functions, x):
    '''Same as any_f except short-circuit evaluation is used:
    returns f0(x) or f1(x) or f2(x) or ...  Short-circuit evaluation
    means the function will return as soon as a True function value
    is detected.
 
    This function is to be preferred over any_f() when the functions in
    functions do not have any side effects, because execution will
    generally be faster.  Use any_f when you want all of the functions
    to be evaluated (e.g., they have some desired side effect).
    '''
    rv = False
    for f in functions:
        rv |= bool(f(x))
        if rv:
            return True
    return False
def ident(x):
    '''Identity function; returns its argument.
    '''
    return x
def Test_apply_each():
    def A(a, b, c):
        return a + b + c
    def B(a, b, c):
        return a * b * c
    a = range(5, 8)
    result = list(apply_each((A, B), a))
    print('''apply_each(function_list, argument_list):
    This higher-order function returns a function that applies each
    of a list of functions to a set of arguments; each function must
    take the same number of arguments.  Here, we'll define two
    functions:  A sums the arguments and B returns their product:
        def A(a, b, c): return a + b + c
        def B(a, b, c): return a * b * c
    Then
        a = range(5, 8)
        print(list(apply_each((A, B), a)))
        returns {result} because 5 + 6 + 7 = 18 and 5*6*7 = 210.
    '''[:-4].format(**locals()))
def Test_bools():
    a = (0, 1, 2)
    result = bools(a)
    print('''bools(seq):
    Returns a list of True or False elements for the sequence seq; is
    equivalent to [bool(i) for i in seq].
        bools({a})
    returns {result}.
    '''[:-4].format(**locals()))
def Test_bool_each():
    def A(a, b, c):
        return a + b + c
    def B(a, b, c):
        return a * b * c
    a = range(5, 8)
    result = bool_each((A, B), a)
    print('''bool_each(function_list, argument_list):
    Return a list of True or False elements that result from applying
    bool() to the return of each function call with the indicated
    parameters.  Using the results of the apply_each example, we get
    {result}.
    '''[:-4].format(**locals()))
def Test_compose():
    def square(x):
        return x*x
    def add3(x):
        return x + 3
    f, x = compose(add3, square), 2
    result = f(2)
    print('''compose(*functions):
    Returns a function representing the function composition of the
    functions in the sequence functions.  If functions is the sequence
    <f0, f1, f2, ...>, the returned function is
        f(x) = ...f2(f1(f0(x)))
    Here, the function f0 squares its argument and f1 adds 3 to its
    argument.  We thus get f(x) = x*x + 3 and the numerical result for
    x = {x} is {result}.
    '''[:-4].format(**locals()))
def Test_all_f():
    has_a = lambda x:  "a" in x
    has_b = lambda x:  "b" in x
    result = all_f((has_a, has_b), ["abc"])
    print('''all_f(functions, arguments=[]):
    Returns True or False, representing the Boolean product of each
    function call.  If functions is the sequence
    <f0, f1, f2, ...>, the returned value is
        f(x) = bool(f0(arguments))*bool(f1(arguments))*...
    Suppose we have the two functions
        has_a = lambda x:  "a" in x
        has_b = lambda x:  "b" in x
    Then all_f((has_a, has_b), ["abc"]) returns {result} because 'a'
    and 'b' are both in the string argument.
    '''[:-4].format(**locals()))
def Test_any_f():
    has_a = lambda x:  "a" in x
    has_d = lambda x:  "d" in x
    result = any_f((has_a, has_d), ["abc"])
    print('''any_f(functions, arguments=[]):
    Returns True or False, representing the Boolean product of each
    function call.  If functions is the sequence
    <f0, f1, f2, ...>, the returned value is
        f(x) = bool(f0(arguments))*bool(f1(arguments))*...
    Suppose we have the two functions
        has_a = lambda x:  "a" in x
        has_d = lambda x:  "d" in x
    Then any_f((has_a, has_d), ["abc"]) returns {result} because 'a'
    and 'b' are both in the string argument.
    '''[:-4].format(**locals()))
def Test_and_f():
    has_a = lambda x:  "a" in x
    has_b = lambda x:  "b" in x
    result = and_F((has_a, has_b), ["abc"])
    print('''and_F(functions, arguments=[]):
    Same as all_f except short-circuit evaluation is used.
    Returns True or False, representing the Boolean product of each
    function call.  If functions is the sequence
    <f0, f1, f2, ...>, the returned value is
        f(x) = bool(f0(arguments))*bool(f1(arguments))*...
    Suppose we have the two functions
        has_a = lambda x:  "a" in x
        has_b = lambda x:  "b" in x
    Then conjoin((has_a, has_b), ["abc"]) returns {result} because 'a'
    and 'b' are both in the string argument.
    '''[:-4].format(**locals()))
def Test_or_f():
    has_a = lambda x:  "a" in x
    has_d = lambda x:  "d" in x
    result = or_f((has_a, has_d), set("abc"))
    print('''or_f(functions, arguments=[]):
    Same as any_f except short-circuit evaluation is used.
    Returns True or False, representing the Boolean sum of each
    function call.  If functions is the sequence
    <f0, f1, f2, ...>, the returned value is
        f(x) = bool(f0(arguments))*bool(f1(arguments))*...
    Suppose we have the two functions
        has_a = lambda x:  "a" in x
        has_d = lambda x:  "d" in x
    Then or_f((has_a, has_d), set("abc")) returns {result} because 'a'
    is in the string argument.
    '''[:-4].format(**locals()))
if __name__ == "__main__": 
    lines = ["{}".format(i) for i in range(20)]
    f1 = lambda x:  int(x) % 2 == 0
    f2 = lambda x:  int(x) % 3 == 0
    f3 = lambda x:  int(x) % 4 == 0
    f4 = lambda x:  int(x) % 5 == 0
    if 0:
        satisfied = all(any_f(f1, f2), any_f(f3, f4))
        selected = [line for line in lines if satisfied(line)]
        for i in selected:
            print(i)
    elif 0:
        '''
        From pg 12 of mertz.odt.  Boolean higher order functions.
        '''
        s = list(range(1, 6))
        ##print("s =", s)
        def apply(f, p, kw={}):
            '''Apply the function with the arguments of p and keywords in kw.
            '''
            return f(*p, **kw)
        def apply_each(fns, args=[]):
            '''Return the result of applying the functions in fns each on the
            arguments in args.

            Example:
                f = lambda x, y: x*y
                g = lambda x, y: x+y
                t = list(apply_each((f, g), [3, 4]))
                print(t)
            prints
                [12, 7]
            '''
            return map(apply, fns, [args]*len(fns))

        def Bool(seq):
            '''Equivalent to [bool(i) for i in seq] except you'll get a map
            object returned.

            Example:
                list(Bool([0, 1, 2])) returns [False, True, True].
            '''
            return map(bool, seq)
        def bool_each(fns, args=[]):
            '''Return the result of applying the functions in fns each on the
            arguments in args and calling Bool on the resulting sequence.

            Example:
                f = lambda x, y: x*y
                g = lambda x, y: x+y
                t = list(bool_each((f, g), [3, 4]))
                print(t)
            prints
                [True, True]
            '''
            return Bool(apply_each(fns, args))

        def conjoin(fns, args=[]):
            return reduce(mul, bool_each(fns, args))

        f = lambda x, y: x*y
        g = lambda x, y: x+y
        print(list(conjoin((f, g), [3, 4])))
        exit()

        conjoin = lambda fns, args=[]: reduce(mul, bool_each(fns, args))
        all_ = lambda fns: lambda arg, fns=fns: conjoin(fns, (arg,))
        both = lambda f, g: all_((f, g))
        all3 = lambda f, g, h: all_((f, g, h))
        and_ = lambda f, g: lambda x, f=f, g=g: f(x) and g(x)
        disjoin = lambda fns, args=[]: reduce(add, bool_each(fns, args))
        some = lambda fns: lambda arg, fns=fns: disjoin(fns, (arg,))
        either = lambda f, g: some((f, g))
        anyof3 = lambda f, g, h: some((f, g, h))
        compose = lambda f, g: lambda x, f=f, g=g: f(g(x))
        compose3 = lambda f, g, h: lambda x, f=f, g=g, h=h: f(g(h(x)))
        ident = lambda x: x
        satisfied = both(either(f1, f2), either(f3, f4))
        if 0:
            # The satisfied function should select numbers that are (divisible
            # by 2 or 3) and (divisible by 4 or 5).
            #
            # The first set is (2, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18).  The
            # second set is (4, 5, 8, 10, 12, 15, 16).  Their intersection is
            # (
            selected = [line for line in lines if satisfied(line)]
            a = set((0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18))
            b = set((0, 4, 5, 8, 10, 12, 15, 16))
            print("first set  =", a)
            print("second set =", b)
            print("intersection =", list(a & b))
            print("Answer       =", [int(i) for i in selected])
    elif 0:
        # Develop a groupby-type function like Toolz's
        from toolz import groupby
        from collections import defaultdict
        def Dictify(f, lst):
            d = defaultdict(list)
            for i in lst:
                d[f(i)].append(i)
            return dict(d.items())
        A = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
        print(Dictify(len, A))
        print(groupby(len, A))
        print()
        iseven = lambda n: n % 2 == 0
        B = range(1, 8)
        print(Dictify(iseven, B))
        print(groupby(iseven, B))
    elif 1:
        # Demo toolz.itertoolz.iterate
        # Calculates iterated value for cosine, which should converge to 0.7390851332151607
        from toolz import iterate
        from math import cos
        for i, val in enumerate(iterate(cos, 1)):
            print(i, val)
            if i > 100:
                break
