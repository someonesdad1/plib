'''
Demonstrates and documents some functional programming tools.
'''
import toolz
import itertools
import functools
import operator
import color as C
from pprint import pprint as pp

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def FirstLine(s):
    print()
    C.fg(C.lred)
    print("-"*70)
    C.fg(C.lgreen)
    print(s)
    C.normal()

def _Accumulate():
    S = "toolz.accumulate"
    s = S.split(".")[-1]
    t = eval(S)
    l = list(range(1, 6))
    a = list(t(operator.add, l))
    f = list(t(operator.add, l, 10))
    m = list(t(operator.mul, l))
    FirstLine("{S}(binary_op, seq, initial=None)".format(**locals()))
    print('''
  Apply a binary operator to each element of a sequence, accumulating
  along the way.  The example shows using the add operator to construct
  a cumulative sum and the mul operator to construct a list of factorials.
  Contrast to stdlib's itertools.accumulate.  Is a generator.
    List = {l}
    {s}(operator.add, {l}) = {a}
    {s}(operator.mul, {l}) = {m}
  Make a cumulative sum function:
    from functools import partial
    cumsum = partial({s}, operator.add)
  {s} takes an optional second argument that is used for the first
  value.  Thus, to add 10 to the above cumulative sum:
    {s}(operator.add, {l}, 10) = {f}
'''[1:-1].format(**locals()))

def _Remove():
    f = "lambda x: x % 2 == 0"
    is_even = eval(f)
    S = "toolz.remove"
    s = S.split(".")[-1]
    t = eval(S)
    l = list(range(1, 6))
    a = list(t(is_even, l))
    FirstLine("{S}(predicate, seq)".format(**locals()))
    print('''
  Remove items from seq for which predicate is false.
    List = {l}
    {s}(is_even, {l}) = {a}
  Is constructed from itertools.filterfalse.
'''[1:-1].format(**locals()))

def _Groupby():
    f = "lambda x: x % 2 == 0"
    is_even = eval(f)
    S = "toolz.groupby"
    s = S.split(".")[-1]
    names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    t = eval(S)
    d = t(len, names)
    seq = [{"name": "Alice", "gender": "F"},
           {"name": "Bob", "gender": "M"},
           {"name": "Charlie", "gender": "M"}]
    b = t("gender", seq)
    FirstLine("{S}(keyfunc, seq)".format(**locals()))
    print('''
  Group items in sequence by the key function keyfunc; return a
  dictionary.  Non-callable keys imply grouping on a member.
    seq = {names}
    {s}(len, {names})
        = {d}
  Non-callable keys:
    seq = [{{"name": "Alice",   "gender": "F"}},
           {{"name": "Bob",     "gender": "M"}},
           {{"name": "Charlie", "gender": "M"}}]) 
    {s}("gender", seq) = 
'''[1:-1].format(**locals()))
    pp(b)

def _Partitionby():
    f = "lambda x: x > 20"
    is_large = eval(f)
    S = "toolz.partitionby"
    s = S.split(".")[-1]
    t = eval(S)
    nums = [1, 2, 1, 99, 88, 33, 99, -1, 5]
    result = list(t(is_large, nums))
    FirstLine("{S}(func, seq)".format(**locals()))
    print('''
  Partition a sequence using a function to decide where the partition's
  boundaries are.  Every time the function's output changes a new
  subsequence is created.
    seq = {nums}
    func = is_large = {f}
    result = {result}
  Another example:  determine the length of the largest run of a Bernoulli
  trial in a random sample:
'''[1:-1].format(**locals()))
    t = '''
from random import randint, seed
seed(0)
seq = []
for i in range(15):
    seq.append(randint(0, 1))
print("seq =", seq)
p = list(toolz.partitionby(lambda x: x == 1, seq))
print("Partitioned =", p)
l = list(map(len, p))
print("lengths =", l)
print("max length =", max(l))
'''
    for i in t.split("\n"):
        print(" "*3, i)
    exec(t)

def _Concat():
    S = "toolz.concat"
    s = S.split(".")[-1]
    t = eval(S)
    a, b, c = range(3), range(4), range(5)
    result = list(toolz.concat((a, b, c)))
    FirstLine("{S}(func, seq)".format(**locals()))
    print('''
  Concatenate a sequence of iterables.
    a, b, c = range(3), range(4), range(5)
    result = concat((a, b, c))
  gives
    {result}
'''[1:-1].format(**locals()))

def _Concatv():
    S = "toolz.concatv"
    s = S.split(".")[-1]
    t = eval(S)
    a, b, c = range(3), range(4), range(5)
    result = list(toolz.concatv(a, b, c))
    FirstLine("{S}(func, seq)".format(**locals()))
    print('''
  Concatenate a sequence of iterables (variadic form).
    a, b, c = range(3), range(4), range(5)
    result = concatv(a, b, c)
  gives
    {result}
'''[1:-1].format(**locals()))

if 0:
    _Concatv()
    exit()

if __name__ == "__main__": 
    # Run the functions that begin with '_' followed by a capital letter.
    f, s = [], set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pred = lambda x: not(x[0] == "_" and x[1] in s)
    f = itertools.filterfalse(pred, sorted(globals()))
    for i in f:
        exec("{}()".format(i))
