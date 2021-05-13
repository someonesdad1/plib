'''Miscellaneous routines in python:

AlmostEqual           Returns True when two floats are nearly equal
Ampacity              Returns NEC ampacity of copper wire
AWG                   Returns wire diameter in inches for AWG gauge number
base2int              Convert string is base x to base 10 integer
Batch                 Generate to pick n items at a time from a sequence
Binary                Converts an integer to a binary string (see int2bin)
bin2gray              Convert binary integer to Gray code
bitlength             Return number of bits needed to represent an integer
bitvector             Convenience class to get the binary bits of an integer
Cfg                   Execute a sequence of text lines for config use
CommonPrefix          Find common prefix in a list of strings
CommonSuffix          Find common suffix in a list of strings
ConvertToNumber       Convert a string to a number
CountBits             Return the number of bits set in an integer
cw2mc                 Convert cap-words naming to mixed-case
cw2us                 Convert cap-words naming to underscore
Debug                 A class that helps with debugging
DecimalToBase         Convert a decimal integer to a base between 2 and 36
Dispatch              Class to aid polymorphism
eng                   Convenience function for engineering format
EditData              Edit a str or bytes object with vim
Engineering           Represent a number in engineering notation
FindDiff              Find the index where two strings first differ.
FindSubstring         Return tuple of indexes where substr is in string
Flatten               Flattens nested sequences to a sequence of scalars
GetChoice             Return a unique string if possible from set of choices
GetString             Return a string from a set by prompting the user
gray2bin              Convert Gray code to binary integer
GroupByN              Group items from a sequence by n items at a time
grouper               Function to group data
HeatIndex             Effect of temperature and humidity
Height                Predict a child's adult height
hyphen_range          Returns list of integers specified as ranges
IdealGas              Calculate ideal gas P, v, T (v is specific volume)
Int                   Convert a string to an integer
int2base              Convert an integer to a specified base
int2bin               Converts int to specified number of binary digits
InterpretFraction     Interprets string as proper or improper fraction
IsBinaryFile          Heuristic to see if a file is a binary file
IsConvexPolygon       Is seq of 2-D points a convex polygon?
IsCygwinSymlink       Returns True if a file is a cygwin symlink
IsIterable            Determines if you can iterate over an object
IsTextFile            Heuristic to see if a file is a text file
ItemCount             Summarize a sequence with counts of each item
Keep                  Keep only specified characters in a string
KeepFilter            Return a function that keeps specified characters
KeepOnlyLetters       Change everything in a string not a letter to spaces
ListInColumns         Returns a list of strings listing a seq in columns
mantissa              Return the mantissa of the base 10 log of a number
mc2cw                 Convert mixed-case naming to cap-words
mc2us                 Convert mixed-case naming to underscore
MultipleReplace       Replace multiple patterns in a string
partition             Generate a list of the partitions of an iterable
Paste                 Return sequence of pasted sequences
Percentile            Returns the percentile of a sorted sequence
ProgressBar           Prints a progress bar to stdout
ProperFraction        Converts a Fraction object to proper form
randq                 Simple, fast random number generator
randr                 Random numbers on [0,1) using randq
ReadVariables         Read variables from a file
Remove                Remove a specified set of characters from a string
RemoveComment         Remove a # style comment
RemoveFilter          Return a function that removes specified characters
RemoveIndent          Remove leading spaces from a multi-line string
significand           Return the significand of x
SignificantFigures    Rounds to specified num of sig figs (returns float)
SignificantFiguresS   Rounds to specified num of sig figs (returns string)
SignSignificandExponent  Returns tuple of sign, significand, exponent
signum                Signum function
Singleton             Mix-in class to create the singleton pattern
soundex               Returns a string characterizing a word's sound
SoundSimilar          Returns True if two words sound similar
SpeedOfSound          Calculate the speed of sound as func of temperature
SpellCheck            Checks that a list of words is in a dictionary
Spinner               Console spinner to show activity
SplitOnNewlines       Splits a string on newlines for PC, Mac, Unix
StringSplit           Split a string on fixed fields or cut at columns
StringToNumbers       Convert a string to a sequence of numbers
TempConvert           Convert a temperature
Time                  Returns a string giving local time and date
TranslateSymlink      Returns what a cygwin symlink is pointing to
Unique                Return the unique items in a sequence
us2cw                 Convert underscore naming to cap-words naming
us2mc                 Convert underscore naming to mixed-case
US_states             Dictionary of states indexed by e.g. "ID"
VisualCount           Return a list representing a histogram of a sequence
Walker                Generator to recursively return files or directories
WindChillInDegF       Calculate wind chill given OAT & wind speed
WireGauge             Get diameter or number of wire gauge sizes
WordID                Generate nonsense words that are somewhat prounounceable
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from collections import deque, defaultdict, OrderedDict
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from heapq import nlargest
from itertools import chain, combinations, islice, groupby
from itertools import filterfalse, cycle
from itertools import zip_longest
from operator import itemgetter
from random import randint, seed
from sig import sig
from string import ascii_letters, digits as DIGITS, punctuation
import cmath
import glob
import math
import os
import pathlib
import re
import struct
import subprocess
import sys
import tempfile
import time

from pdb import set_trace as xx
import debug
if 0:
    debug.SetDebugger()

P = pathlib.Path
nl = "\n"

# Note:  this choice of a small floating point number may be
# wrong on a system that doesn't use IEEE floating point numbers.
eps = 1e-15

def KeepOnlyLetters(s, underscore=False, digits=True):
    '''Replace all non-word characters with spaces.  If underscore is
    True, keep underscores too (e.g., typical for programming language
    identifiers).  If digits is True, keep digits too.
    '''
    allowed = ascii_letters + "_" if underscore else ascii_letters
    allowed += DIGITS if digits is True else ""
    c = [chr(i) for i in range(256)]
    t = ''.join([i if i in allowed else " " for i in c])
    return s.translate(t)

def StringSplit(fields, string, remainder=True, strict=True):
    '''Pick out the specified fields of the string and return them as
    a tuple of strings.  fields can be either a format string or a
    list/tuple of numbers.
 
    Field numbering starts at 0.  If strict is True, then the indicated
    number of fields must be returned or a ValueError exception will be
    raised.
 
    fields is a format string
        A format string is used to get particular columns of the
        string.  For example, the format string "5s 3x 8s 8s" means to
        pick out the first five characters of the string, skip three
        spaces, get the next 8 characters, then the next 8 characters.
        If remainder is False, this is all that's returned; if
        remainder is True, then whatever is left over will also be
        returned.  Thus, if remainder is False, you'll have a 3-tuple
        of strings returned; if True, a 4-tuple.
 
    fields is a sequence of numbers
        The numbers specify cutting the string at the indicated
        columns (numbering is 0-based).  Example:  for the input string
        "hello there", using the fields of [3, 7] will return the tuple
        of strings ("hel", "lo t", "here").
            "hello there"
             01234567890
 
    Derived from code by Alex Martelli at
    http://code.activestate.com/recipes/65224-accessing-substrings/
    Downloaded Sun 27 Jul 2014 07:52:44 AM
    '''
    if isinstance(fields, str):
        left_over = len(string) - struct.calcsize(fields)
        if left_over < 0:
            raise ValueError("string is shorter than requested format")
        format = "%s %ds" % (fields, left_over)
        s = bytes(string.encode("ascii"))
        result = list(struct.unpack(format, s))
        return result if remainder else result[:-1]
    else:
        pieces = [string[i:j] for i, j in zip([0] + fields, fields)]
        if remainder:
            pieces.append(string[fields[-1]:])
        num_expected = len(fields) + 1
        if num_expected != len(pieces) and strict:
            raise ValueError("Expected %d pieces; got %d" % (num_expected,
                             len(pieces)))
        return pieces

def Percentile(seq, fraction):
    '''Return the indicated fraction of a sequence seq of sorted
    values.  fraction will be converted to be in [0, 1].
 
    The method is recommended by NIST at
    https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm.  
    
    The algorithm is:
 
        Suppose you have N numbers Y_[1] to Y_[N].  For the pth percentile,
        let x = p*(N + 1) and
      
          k = int(x)      [Integer part of x], d >= 0
          d = x - k       [Fractional part of x], d in [0, 1)
      
        Then calculate
      
          1.  For 0 < k < N, Y_(p) = Y_[k] + d*(Y_[k+1] - Y_[k]).
          2.  For k = 0, Y_[p] = Y[1].  Note that any p <= 1/(N+1) will be
              set to the minimum value.
          3.  For k >= N, Y_(p) = = Y_[N].  Note that any p > N/(N+1) will
              be set to the maximum value.
      
          Note the array indexing is 1-based, so python code will need to
          take this into account.
  
    Example:  A gauge study resulted in 12 measurements:
  
         i  Measurements   Sorted       Ranks
        --- ------------   -------      -----
         1     95.1772     95.0610        9
         2     95.1567     95.0925        6
         3     95.1937     95.1065       10
         4     95.1959     95.1195       11
         5     95.1442     95.1442        5
         6     95.0610     95.1567        1
         7     95.1591     95.1591        7
         8     95.1195     95.1682        4
         9     95.1065     95.1772        3
        10     95.0925     95.1937        2
        11     95.1990     95.1959       12
        12     95.1682     95.1990        8
  
    To find the 90th percentile, we have p*(N+1) = 0.9*13 = 11.7.  Then 
    k = 11 and d = 0.7.  From step 1 above, we estimate Y_(90) as
  
        Y_(90) = Y[11] + 0.7*(95.1990 - 95.1959) = 95.1981
  
    Note this algorithm will work for N > 1.
 
    http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    gives another algorithm, but it doesn't give the same results as the
    NIST algorithm.
    '''
    if not seq:
        return None
    N = len(seq)
    if N == 1:
        raise ValueError("Sequence must have at least 2 elements")
    fraction = max(min(fraction, 1), 0)
    x = fraction*(N + 1)
    k = int(x)      # Integer part of x
    d = x - k       # Fractional part of x
    if 0 < k < N:
        yk = seq[k - 1]
        y = yk + d*(seq[k] - yk)
    elif k >= N:
        y = seq[-1]
    else:
        y = seq[0]
    return y

def ItemCount(seq, n=None):
    '''Return a sorted list of the items and their counts in the iterable
    seq, with the largest count first in the tuple.  If n is given, only
    return the largest n counts.  The items in seq must be hashable.
 
    Example:
      If a = (1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
      returns [(5, 5), (1, 3), (4, 2), (2, 1), (3, 1)].
 
      If a = (1.0, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
      returns [(5, 5), (1.0, 3), (4, 2), (2, 1), (3, 1)].
 
    Note that 1, 1.0, and Fraction(1, 1) hash to the same value; since a
    dictionary is used as the counting container, these are considered to
    be the same items.  Thus, you can get syntactically different results
    that are semantically the same.
    '''
    items = defaultdict(int)
    for item in seq:
        items[item] += 1
    s = sorted(items.items(), key=itemgetter(1), reverse=True)
    return s if n is None else s[:n]

def VisualCount(seq, n=None, char="*", width=None, indent=0):
    '''Return a list of strings representing a histogram of the items in
    the iterable seq.  If the values in the sequence can be sorted, the
    histogram will be shown by increasing item value; otherwise, the items
    will be shown sorted by frequency.
 
    n       Return the n largest items if n is not None.
    char    String to build the histogram element.
    width   Fit each element into this width.  If none, use the value of
            the COLUMNS environment variable or 79 if it isn't defined.
    indent  Indent each line by this amount.
 
    Note:  the width calculations are only correct if the length of the
    char string is 1.

    Example:  
        for i in VisualCount([1,1,1,1,1,8,8,8,9,9,9,9,9,9,9,9,9,9,9], 
                             width=40, indent=8):
            print(i)
    prints
        1 *************
        8 ********
        9 ******************************
    '''
    counts = ItemCount(seq, n=n)
    try:
        counts = sorted(counts)     # Sort by item values if possible
    except TypeError:
        pass
    max_obj_len = max([len(str(i[0])) for i in counts])
    max_count = max([i[1] for i in counts])
    if width is None:
        width = int(os.environ.setdefault("COLUMNS", 80)) - 1
    max_hist_len = width - indent - 1 - max_obj_len
    assert(max_hist_len > 0)
    # Scale counts to fit on screen
    counts = [(i, int(j/max_count*max_hist_len)) for i, j in counts]
    # Construct the output list
    output = []
    for item, count in counts:
        s = "{}{:{}s} ".format(" "*indent, str(item), max_obj_len)
        output.append(s + char*count)
    return output

def cw2us(x):
    '''Convert cap-words naming to underscore naming.
    "Python Cookbook", pg 91.

    Example:  ALotOfFuss --> a_lot_of_fuss
    '''
    return re.sub(r"(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])",
                  r"_\g<0>", x).lower()

def cw2mc(x):
    '''Convert cap-words naming to mixed-case naming.
    "Python Cookbook", pg 91.

    Example:  ALotOfFuss --> aLotOfFuss
    '''
    return x[0].lower() + x[1:]

def us2mc(x):
    '''Convert underscore naming to mixed-case.
    "Python Cookbook", pg 91.

    Example:  a_lot_of_fuss --> aLotOfFuss
    '''
    return re.sub(r"_([a-z])", lambda m: (m.group(1).upper()), x)

def us2cw(x):
    '''Convert underscore naming to cap-words naming.
    "Python Cookbook", pg 91.

    Example:  a_lot_of_fuss --> ALotOfFuss
    '''
    s = us2mc(x)
    return s[0].upper() + s[1:]

def mc2us(x):
    '''Convert mixed-case naming to underscore naming.
    "Python Cookbook", pg 91.

    Example:  aLotOfFuss --> a_lot_of_fuss
    '''
    return cw2us(x)

def mc2cw(x):
    '''Convert mixed-case naming to cap-words naming.
    "Python Cookbook", pg 91.

    Example:  aLotOfFuss --> ALotOfFuss
    '''
    return x[0].upper() + x[1:]

def MultipleReplace(text, patterns, flags=0):
    '''Replace multiple patterns in the string text.  patterns is a
    dictionary whose keys are the regular expressions and values are the
    replacement text.  The flags keyword variable is the same as that used
    by the re.compile function.
    
    From page 88 of Python Cookbook.
    '''
    # Make a compound regular expression from all the keys
    r = re.compile("|".join(map(re.escape, patterns.keys())), flags)
    # For each match, look up the corresponding value in the dictionary
    return r.sub(lambda match: patterns[match.group(0)], text)
    
class Singleton(object):
    '''Mix-in class to make an object a singleton.  From 'Python in a
    Nutshell', p 84.
    '''
    _singletons = {}
    def __new__(cls, *args, **kw):
        if cls not in cls._singletons:
            cls._singletons[cls] = object.__new__(cls)
        return cls._singletons[cls]

def signum(x, ret_type=int):
    '''Return a number -1, 0, or 1 representing the sign of x.
    '''
    if x < 0:
        return ret_type(-1)
    elif x > 0:
        return ret_type(1)
    return ret_type(0)

def InterpretFraction(s):
    '''Interprets the string s as a fraction.  The following are
    equivalent forms:  '5/4', '1 1/4', '1-1/4', or '1+1/4'.  The
    fractional part in a proper fraction can be improper:  thus,
    '1 5/4' is returned as Fraction(9, 4).
    '''
    if "/" not in s:
        raise ValueError("'%s' must contain '/'" % s)
    t = s.strip()
    # First, try to convert the string to a Fraction object
    try:
        return Fraction(t)
    except ValueError:
        pass
    # Assume it's of the form 'm[ +-]n/d' where m, n, d are
    # integers.
    msg = "'%s' is not of the correct form" % s
    neg = True if t[0] == "-" else False
    fields = t.replace("+", " ").replace("-", " ").strip().split()
    if len(fields) != 2:
        raise ValueError(msg)
    try:
        ip = abs(int(fields[0]))
        fp = abs(Fraction(fields[1]))
        return -(ip + fp) if neg else ip + fp
    except ValueError:
        raise ValueError(msg)

def ProperFraction(fraction, separator=" "):
    '''Return the Fraction object fraction in a proper fraction string
    form.
 
    Example:  Fraction(-5, 4) returns '-1 1/4'.
    '''
    if not isinstance(fraction, Fraction):
        raise ValueError("frac must be a Fraction object")
    sgn = "-" if fraction < 0 else ""
    n, d = abs(fraction.numerator), abs(fraction.denominator)
    ip, numerator = divmod(n, d)
    return "{}{}{}{}/{}".format(sgn, ip, separator, numerator, d)

def RemoveIndent(s, numspaces=4):
    '''Given a multi-line string s, remove the indicated number of
    spaces from the beginning each line.  If that number of space
    characters aren't present, then leave the line alone.
    '''
    if numspaces < 0:
        raise ValueError("numspaces must be >= 0")
    lines = s.split(nl)
    for i, line in enumerate(lines):
        if line.startswith(" "*numspaces):
            lines[i] = lines[i][numspaces:]
    return nl.join(lines)

def Batch(iterable, size):
    '''Generator that gives you batches from an iterable in manageable
    sizes.  Slightly adapted from Raymond Hettinger's entry in the
    comments to
    http://code.activestate.com/recipes/303279-getting-items-in-batches/
 
    Example:
        for n in (3, 4, 5, 6):
            s = tuple(tuple(i) for i in Batch(range(n), 3))
            print(s)
    gives
        ((0, 1, 2),)
        ((0, 1, 2), (3,))
        ((0, 1, 2), (3, 4))
        ((0, 1, 2), (3, 4, 5))
 
    Another way of doing this is with slicing (but you'll need to have
    the whole iterable in memory to do this):
        def Pick(iterable, size):
            i = 0
            while True:
                s = iterable[i:i + size]
                if not s:
                    break
                yield s
                i += size
    '''
    def counter(x):
        counter.n += 1
        return counter.n//size
    counter.n = -1
    for k, g in groupby(iterable, counter):
        yield g

def GroupByN(seq, n, fill=False):
    '''Return an iterator that gives groups of n items from the
    sequence.  If fill is True, return None for any missing items.  In
    other words, if fill is False, groups without the full number of
    elements are discarded.
 
    Example:
        print("fill = False:")
        for i in GroupByN(range(7), 3, fill=False):
            print("  ", i)
        print("fill = True:")
        for i in GroupByN(range(7), 3, fill=True):
            print("  ", i)
    prints
        fill = False:
           (0, 1, 2)
           (3, 4, 5)
        fill = True:
           (0, 1, 2)
           (3, 4, 5)
           (6, None, None)
    '''
    # Inspired by
    # http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/
    if fill:
        return zip_longest(*([iter(seq)]*n), fillvalue=None)
    else:
        return zip(*([iter(seq)]*n))

def Unique(seq):
    '''Given a sequence seq, returns a sequence with the unique
    items in seq.
    '''
    return list(OrderedDict.fromkeys(seq))

def soundex(s):
    '''Return the 4-character soundex value to a string argument.  The
    string s must be one word formed with ASCII characters and with no
    punctuation or spaces.  The returned soundex string can be used to
    compare the sounds of words; from US patents 1261167(1918) and
    1435663(1922) by Odell and Russell.
 
    The algorithm is from Knuth, "The Art of Computer Programming",
    volume 3, "Sorting and Searching", pg. 392:
 
        1. Retain first letter of name and drop all occurrences
           of a, e, h, i, o, u, w, y in other positions.
        2. Assign the following numbers to the remaining letters
           after the first:
            1:  b, f, p, v
            2:  c, g, j, k, q, s, x, z
            3:  d, t
            4:  l
            5:  m, n
            6:  r
        3. If two or more letters with the same code were adjacent in
           the original name (before step 1), omit all but the first.
        4. Convert to the form "letter, digit, digit, digit" by adding
           trailing zeroes (if there are less than three digits), or
           by dropping rightmost digits (if there are more than
           three).
    '''
    if not s:
        raise ValueError("Argument s must not be empty string")
    if set(s) - set(ascii_letters):
        raise ValueError("String s must contain only ASCII letters")
    if not hasattr(soundex, "m"):
        soundex.m = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                             "01230120022455012623010202"))
    # Function to map lower-case letters to soundex number
    getnum = lambda x: [soundex.m[i] for i in x]
    t = s.upper()
    num, keep = getnum(t), []
    # Step 0 (and step 3):  keep only those letters that don't map to
    # the same number as the previous letter.
    for i, code in enumerate(num):
        if not i:
            keep.append(t[0])   # Always keep first letter
        else:
            if code != num[i - 1]:
                keep.append(t[i])
    # Step 1:  remove vowels, etc.
    first_letter = keep[0]
    ignore, process = set("AEHIOUWY"), []
    process += [i for i in keep[1:] if i not in ignore]
    # Step 2:  assign numbers for remaining letters
    code = first_letter + ''.join(getnum(''.join(process)))
    # Step 3:  same as step 0
    # Step 4:  adjust length
    if len(code) > 4:
        code = code[:4]
    while len(code) < 4:
        code += "0"
    return code

def SoundSimilar(s, t):
    '''Returns True if the strings s and t sound similar.
    '''
    return True if soundex(s) == soundex(t) else False

def Cfg(lines, lvars=OrderedDict(), gvars=OrderedDict()):
    '''Allow use of sequences of text strings to be used for
    general-purpose configuration information.  Each string must be
    valid python code.
 
    Each line in lines is executed with the local variables in lvars
    and global variables in gvars.  The lvars dictionary is returned,
    which will contain each of the defined variables and functions.
 
    Any common leading indentation is removed before processing; this
    allows you to indent your configuration lines as desired.
 
    Example:
        lines = """
                from math import sqrt
                a = 44
                b = "A string"
                def X(a):
                    return a/2
                c = a*sqrt(2)
                d = X(a)
            """[1:-1].split("\n")
 
    The code
        d = Cfg(lines)
        for i in d.keys():
            print(i + " = " + str(d[i]))
 
    results in
        sqrt = <built-in function sqrt>
        a = 44
        b = A string
        X = <function X at 0x00B9C9B0>
        c = 62.2253967444
        d = 22.0
    '''
    # Remove any common indent
    indent = os.path.commonprefix(lines)
    if indent:
        lines = [i.replace(indent, "", 1) for i in lines]
    # Put lines into a temporary file so execfile can be used.  I
    # would have used NamedTemporaryFile(), but it doesn't work
    # correctly on Windows XP, so I used the deprecated mktemp.
    exec(nl.join(lines), gvars, lvars)
    # The things defined in the configuration lines are now in the
    # dictionary lvars.
    return lvars

def RemoveComment(line, code=False):
    '''Remove the largest string starting with '#' from the string
    line.  If code is True, then the resulting line will be compiled
    and an exception will occur if the modified line won't compile.
    This typically happens if '#' is inside of a comment.
    '''
    orig = line
    loc = line.find("#")
    if loc != -1:
        line = line[:loc]
    if code:
        try:
            compile(line, "", "single")
        except Exception:
            msg = "Line with comment removed won't compile:\n  '%s'" % orig
            raise ValueError(msg)
    return line

def bitlength(n):
    '''This emulates the n.bit_count() function of integers in python 2.7
    and 3.  This returns the number of bits needed to represent the
    integer n; n can be any integer.
 
    A naive implementation is to take the base two logarithm of the
    integer, but this will fail if abs(n) is larger than the largest
    floating point number.
    '''
    try:
        return n.bit_count()
    except Exception:
        return len(bin(abs(n))) - 2

def CountBits(num):
    '''Return (n_on, n_off), the number of 'on' and 'off' bits in the 
    integer num.
    '''
    if not isinstance(num, int):
        raise ValueError("num must be an integer")
    s = list(bin(num)[2:])
    on  = sum([i == "1" for i in s])
    off = sum([i == "0" for i in s])
    return (on, off)

def ReadVariables(file, ignore_errors=False):
    '''Given a file of lines of python code, this function reads in
    each line and executes it.  If the lines of the file are
    assignments to variables, then this results in a defined variable
    in the local namespace.  Return the dictionary containing these
    variables.
 
    file can be a name of a file, a file-like object, a string, or a
    multiline string.
 
    Note that this function will not execute any line that doesn't
    contain an '=' character to cut down on the chance that some
    unforeseen error can occur (but, of course, this protection can
    rather easily be subverted).
 
    This function is intended to be used to allow you to have an
    easy-to-use configuration file for a program.  For example, a user
    could write the configuration file
 
        # This is a comment
        ProcessMean              = 37.2
        ProcessStandardDeviation = 12.1
        NumberOfParts            = 180
 
    When this function returned, you'd have a dictionary with four
    variables in it.
 
    If any line in the input file causes an exception, the offending
    line will be printed to stderr and the program will exit unless
    ignore_errors is True.
    '''
    try:
        lines = file.readlines()
    except AttributeError:
        try:
            lines = open(file).readlines()
        except FileNotFoundError:
            # Assume it's a multiline string
            lines = file.strip().split("\n")
    for i, line in enumerate(lines):
        if "=" not in line:
            continue
        try:
            exec(line)
        except Exception:
            sys.stderr.write("Line %d of file '%s' bad:\n  '%s'\n" %
                             (i+1, file, line.rstrip()))
            if not ignore_errors:
                exit(1)
    d = locals()
    for i in "line lines i file ignore_errors".split():
        del d[i]
    return d

def FindSubstring(string, substring):
    '''Return a tuple of the indexes of where the substring t is found
    in the string s.
    '''
    if not isinstance(string, str):
        raise TypeError("s needs to be a string")
    if not isinstance(substring, str):
        raise TypeError("t needs to be a string")
    d, ls, lsub = [], len(string), len(substring)
    if not ls or not lsub or lsub > ls:
        return tuple(d)
    start = string.find(substring)
    while start != -1 and ls - start >= lsub:
        d.append(start)
        start = string.find(substring, start + 1)
    return tuple(d)

def randq(seed=-1):
    '''The simple random number generator in the section "An Even
    Quicker Generator" from "Numerical Recipes in C", page 284,
    chapter 7, 2nd ed, 1997 reprinting (found on the web in PDF form).
 
    If seed is not -1, it is used to initialize the sequence; it can
    be any hashable value.
    '''
    # The multiplicative constant 1664525 was recommended by Knuth and
    # the additive constant 1013904223 came from Lewis.
    a, c = 1664525, 1013904223
    if seed != -1:
        randq.idum = abs(hash(seed))
    randq.idum = (randq.a*randq.idum + randq.c) % randq.maxidum
    return randq.idum

# State variables for randq
randq.a = 1664525
randq.c = 1013904223
randq.idum = 0
randq.maxidum = 2**32

def randr(seed=-1):
    '''Uses randq to return a floating point number on [0, 1).
    '''
    n = randq(seed=seed) if seed != -1 else randq()
    return n/float(randq.maxidum)

def IsCygwinSymlink(file):
    '''Return True if file is a cygwin symbolic link.
    '''
    s = open(file).read(20)
    if len(s) > 10:
        if s[2:9] == "symlink":
            return True
    return False

def TranslateSymlink(file):
    '''For a cygwin symlink, return a string of what it's pointing to.
    '''
    return open(file).read()[12:].replace("\x00", "")

def GetString(prompt_msg, default, allowed_values, ignore_case=True):
    '''Get a string from a user and compare it to a sequence of
    allowed values.  If the response is in the allowed values, return
    it.  Otherwise, print an error message and ask again.  The letter
    'q' or 'Q' will let the user quit the program.  The returned
    string will have no leading or trailing whitespace.
    '''
    if ignore_case:
        allowed_values = [i.lower() for i in allowed_values]
    while True:
        msg = prompt_msg + " [" + default + "]:  "
        response = input(msg)
        s = response.strip()
        if not s:
            return default
        if s.lower() == "q":
            exit(0)
        s = s.lower() if ignore_case else s
        if s in allowed_values:
            return s
        print("'%s' is not a valid response" % response.strip())

def GetChoice(name, names):
    '''name is a string and names is a set or dict of strings.  Find
    if name uniquely identifies a string in names; if so, return it.
    If it isn't unique, return a list of the matches.  Otherwise
    return None.  The objective is to allow name to be the minimum
    length string necessary to uniquely identify the choice.
    '''
    # See self tests below for an example of use
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(names, (set, dict)):
        raise ValueError("names must be a set or dictionary")
    d, n = defaultdict(list), len(name)
    for i in names:
        d[i[:len(name)]] += [i]
    if name in d:
        if len(d[name]) == 1:
            return d[name][0]
        else:
            return d[name]
    return None

def Int(s):
    '''Convert the string x to an integer.  Allowed forms are:
    Plain base 10 string
    0b binary
    0o octal
    0x hex
    '''
    neg = 1
    if s[0] == "-":
        neg = -1
        s = s[1:]
    if s.startswith("0b"):
        return neg*int(s, 2)
    elif s.startswith("0o"):
        return neg*int(s, 8)
    elif s.startswith("0x"):
        return neg*int(s, 16)
    else:
        return neg*int(s, 10)

def int2base(x, base):
    '''Converts the integer x to a string representation in a given
    base.  base may be from 2 to 94.
 
    Method by Alex Martelli
    http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
    Modified slightly by DP.
    '''
    if not (2 <= base <= len(int2base.digits)):
        msg = "base must be between 2 and %d inclusive" % len(int2base.digits)
        raise ValueError(msg)
    if not isinstance(x, (int, str)):
        raise ValueError("Argument x must be an integer or string")
    if isinstance(x, str):
        x = int(x)
    sgn = 1
    if x < 0:
        sgn = -1
    elif not x:
        return '0'
    x, answer = abs(x), []
    while x:
        answer.append(int2base.digits[x % base])
        x //= base
    if sgn < 0:
        answer.append('-')
    answer.reverse()
    return ''.join(answer)

int2base.digits = DIGITS + ascii_letters + punctuation

def base2int(x, base):
    '''Inverse of int2base.  Converts a string x in the indicated base
    to a base 10 integer.  base may be from 2 to 94.
    '''
    if not (2 <= base <= len(base2int.digits)):
        msg = "base must be between 2 and %d inclusive" % len(base2int.digits)
        raise ValueError(msg)
    if not isinstance(x, str):
        raise ValueError("Argument x must be a string")
    y = list(reversed(x))
    n = 0
    for i, c in enumerate(list(reversed(x))):
        try:
            val = base2int.digits.index(c)
        except Exception:
            msg = "'%c' not a valid character for base %d" % (c, base)
            raise ValueError(msg)
        n += val*(base**i)
    return n

base2int.digits = DIGITS + ascii_letters + punctuation

def IsTextFile(file, num_bytes=100):
    '''Heuristic to classify a file as text or binary.  The algorithm
    is to read num_bytes from the beginning of the file; if there are
    any characters other than the "typical" ones found in plain text
    files, the file is classified as binary.

    This won't work on a file that contains Unicode characters but is
    otherwise plain text.  Here, "text" means plain ASCII.
 
    Note:  if file is a string, it is assumed to be a file name and
    opened.  Otherwise it is assumed to be an open stream.
    '''
    text_chars = set([ord(i) for i in "\n\r\b\t\v"] + list(range(32, 127)))
    if isinstance(file, str):
        s = open(file, "rb").read(num_bytes)
    else:
        s = file.read(num_bytes)
    for c in s:
        if ord(c) not in text_chars:
            return False
    return True

def IsBinaryFile(file, num_bytes=100):
    'Heuristic that returns True if a file is a binary file'
    return not IsTextFile(file, num_bytes)

class Dispatch:
    '''The Dispatch class allows different functions to be called
    depending on the argument types.  Thus, there can be one function
    name regardless of the argument type.  Due to David Ascher.
 
    Example:  the following lets us define a function ss which will
    calculate the sum of squares of the contents of an array, whether
    the array is a python sequence or a NumPy array.
    ss = Dispatch((list_ss, (ListType, TupleType)),
                            (array_ss, (numpy.ArrayType)))
    '''
    def __init__(self, *tuples):
        self._dispatch = {}
        for func, types in tuples:
            for t in types:
                if t in self._dispatch.keys():
                    raise ValueError("Can't have two dispatches on " + str(t))
                self._dispatch[t] = func
        self._types = self._dispatch.keys()
    def __call__(self, arg1, *args, **kw):
        if type(arg1) not in self._types:
            raise TypeError("Don't know how to dispatch %s arguments" %
                            type(arg1))
        return apply(self._dispatch[type(arg1)], (arg1,) + args, kw)

def IsIterable(x, exclude_strings=False):
    '''Return True if x is an iterable.  You can exclude strings from the
    things that can be iterated on if you wish.
 
    Note:  if you don't care whether x is a string or not, a simpler way
    is:
        try:
            iter(x)
            return True
        except TypeError:
            return False
    '''
    if exclude_strings and isinstance(x, str):
        return False
    return True if isinstance(x, Iterable) else False

def ListInColumns(alist, col_width=0, num_columns=0, space_betw=0, truncate=0):
    '''Returns a list of strings with the elements of alist (if
    components are not strings, they will be converted to strings
    using str) printed in columnar format.  Elements of alist that
    won't fit in a column either generate an exception if truncate is
    0 or get truncated if truncate is nonzero.  The number of spaces
    between columns is space_betw.
 
    If col_width and num_columns are 0, then the program will set them
    by reading the COLUMNS environment variable.  If COLUMNS doesn't
    exist, col_width will default to 80.  num_columns will be chosen
    by finding the length of the largest element so that it is not
    truncated.
 
    Caveat:  if there are a small number of elements in the list, you
    may not get what you expect.  For example, try a list size of 1 to
    10 with num_columns equal to 4:  for lists of 1, 2, 3, 5, 6, and 9,
    you'll get fewer than four columns.
 
    This function is obsolete; instead, use Columnize in columnize.py.
    '''
    # Make all integers
    col_width = int(col_width)
    num_columns = int(num_columns)
    space_betw = int(space_betw)
    truncate = int(truncate)
    lines = []
    N = len(alist)
    if not N:
        return [""]
    # Get the length of the longest line in the alist
    maxlen = max([len(str(i)) for i in alist])
    if not maxlen:
        return [""]
    if not col_width:
        if "COLUMNS" in os.environ:
            columns = int(os.environ["COLUMNS"]) - 1
        else:
            columns = 80 - 1
        col_width = maxlen
    if not num_columns:
        try:
            num_columns = int(columns//maxlen)
        except Exception:
            return [""]
        if num_columns < 1:
            raise ValueError("A line is too long to display")
        space_betw = 1
    if not col_width or not num_columns or space_betw < 0:
        raise ValueError("Error: invalid parameters")
    num_rows = int(N//num_columns + (N % num_columns != 0))
    for row in range(num_rows):
        s = ""
        for column in range(num_columns):
            i = int(num_rows*column + row)
            if 0 <= i <= (N-1):
                if len(str(alist[i])) > col_width:
                    if truncate:
                        s += str(alist[i])[:col_width] + " "*space_betw
                    else:
                        raise ValueError("Error:  element %d too long" % i)
                else:
                    s += (str(alist[i]) + " " * (col_width -
                          len(str(alist[i]))) + " " * space_betw)
        lines.append(s)
    assert(len(lines) == num_rows)
    return lines

def SpeedOfSound(T):
    '''Returns speed of sound in air in m/s as a function of temperature
    T in K.  Assumes sea level pressure.
    '''
    assert(T > 0)
    return 331.4*math.sqrt(T/273.15)

def WindChillInDegF(wind_speed_in_mph, air_temp_deg_F):
    '''Wind Chill for exposed human skin, expressed as a function of
    wind speed in miles per hour and temperature in degrees Fahrenheit.
 
    http://en.wikipedia.org/wiki/Wind_chill.
    '''
    if wind_speed_in_mph <= 3:
        raise ValueError("Wind speed must be > 3 mph")
    if air_temp_deg_F > 50:
        raise ValueError("Air temperature must be < 50 deg F")
    return (35.74 + 0.6215*air_temp_deg_F - 35.75*wind_speed_in_mph**0.16 +
            0.4275*air_temp_deg_F*wind_speed_in_mph**0.16)

def Height(current_height_inches, age_years, sex):
    '''Returns the predicted adult height in inches of a child.
    Unattributed, but found in the C code files of Glenn Rhoads' old
    website http://remus.rutgers.edu/~rhoads/Code/code.html, but which
    was defunct in 2010.
    '''
    if not (0 < current_height_inches < 72):
        raise ValueError("current_height_inches must be between 0 and 72")
    if not (0 < age_years < 20):
        raise ValueError("age_years must be between 0 and 20")
    if sex.lower() not in "mf":
        raise ValueError("sex must be 'm' or 'f'")
    a, h = age_years, current_height_inches
    if sex.lower() == "m":
        return h/(((0.00011*a - 0.0032)*a + 0.0604)*a + 0.3796)
    else:
        return h/(((0.00028*a - 0.0071)*a + 0.0926)*a + 0.3524)

def HeatIndex(air_temp_deg_F, relative_humidity_percent):
    '''From http://www.weather.gov/forecasts/graphical/sectors/idaho.php#tabs.
    See also http://www.crh.noaa.gov/pub/heat.php.
 
    Heat Index combines the effects of heat and humidity. When heat and
    humidity combine to reduce the amount of evaporation of sweat from the
    body, outdoor exercise becomes dangerous even for those in good shape.
 
    Example:  for 90 deg F and 50% RH, the heat index is 94.6.
 
    The equation used is a multiple regression fit to a complicated set of
    equations that must be solved iteratively.  The uncertainty with a
    prediction is given at 1.3 deg F.  See
    http://www.srh.noaa.gov/ffc/html/studies/ta_htindx.PDF for details.
 
    If heat index is:
 
        80-90 degF:  Caution:  fatigue possible with prolonged exposure or
                     activity.
        90-105:      Extreme caution:  sunstroke, muscle cramps and/or heat
                     exhaustion possible with prolonged exposure and/or
                     physical activity.
        105-129:     Danger:  sunstroke, muscle cramps and/or heat exhaustion
                     likely.  Heatstroke possible with prolonged exposure
                     and/or physical activity.
        >= 130       Extreme danger:  Heat stroke or sunstroke likely.
    '''
    RH, Tf = relative_humidity_percent, air_temp_deg_F
    HI = (-42.379 + 2.04901523*Tf + 10.14333127*RH - 0.22475541*Tf*RH -
          6.83783e-3*Tf*Tf - 5.481717e-2*RH*RH + 1.22874e-3*Tf*Tf*RH +
          8.5282e-4*Tf*RH*RH - 1.99e-6*Tf*Tf*RH*RH)
    return HI

def SpellCheck(input, Words, ignore_case=True):
    '''input is a sequence of word strings; Words is a dictionary or set
    of correct spellings.  Return the set of any words in input that are not
    in Words.
    '''
    misspelled = set()
    if not input:
        return []
    if not Words:
        raise ValueError("Words parameter is empty")
    for word in input:
        if ignore_case:
            word = word.lower()
        if word not in Words:
            misspelled.add(word)
    return misspelled

def Keep(s, keep):
    '''Return a list (or a string if s is a string) of the items in s that
    are in keep.
    '''
    k = set(keep)
    if 0:
        f = lambda x: x not in k
        ret = filterfalse(f, s)
    f = lambda x: x in k
    ret = filter(f, s)
    return ''.join(ret) if isinstance(s, str) else list(ret)

def KeepFilter(keep):
    '''Return a function that takes a string and returns a string
    containing only those characters that are in keep.
    '''
    def func(s):
        return Keep(s, keep)
    return func

def Remove(s, remove):
    '''Return a list (or a string if s is a string) of the items in s that
    are not in remove.
    '''
    r = set(remove)
    f = lambda x: x in r
    ret = filterfalse(f, s)
    return ''.join(ret) if isinstance(s, str) else list(ret)

def RemoveFilter(remove):
    '''Return a function that takes a string and returns a string
    containing only those characters that are not in remove.
    '''
    def func(s):
        return Remove(s, remove)
    return func

class Debug:
    '''Implements a debug class that can be useful in printing debugging
    information.

    dbg = Debug()
    dbg.print("Message")
        Will print '+ Message' to stderr
    Turn off printing with 'dbg.on = False'.
    '''
    def __init__(self, stream=sys.stderr, add_nl=True, prefix="+ "):
        self.stream = stream
        self.on = True
        self.add_nl = add_nl
        self.prefix = prefix
    def print(self, s):
        if self.on:
            s = self.prefix + s
            if self.add_nl:
                s += nl
            self.stream.write(s)

def Time():
    '''Returns the current time in the following format:
        Mon Oct 25 22:05:00 2010
    '''
    t, f = time.localtime(), lambda x: x[1:] if x[0] == "0" else x
    day = f(time.strftime("%a", t))
    date = f(time.strftime("%d%b%Y", t))
    clock = f(time.strftime("%I:%M", t))
    ampm = time.strftime("%p", t).lower()
    return ' '.join((date, clock, ampm, day))

def AWG(n):
    '''Returns the wire diameter in inches given the AWG (American Wire
    Gauge) number (also known as the Brown and Sharpe gauge).  Use negative
    numbers as follows:
 
        00    -1
        000   -2
        0000  -3
 
    Reference:  the units.dat file with version 1.80 of the GNU units
    program gives the following statement:
 
        American Wire Gauge (AWG) or Brown & Sharpe Gauge appears to be the
        most important gauge. ASTM B-258 specifies that this gauge is based
        on geometric interpolation between gauge 0000, which is 0.46 inches
        exactly, and gauge 36 which is 0.005 inches exactly.  Therefore,
        the diameter in inches of a wire is given by the formula
                1|200 92^((36-g)/39).
        Note that 92^(1/39) is close to 2^(1/6), so diameter is
        approximately halved for every 6 gauges.  For the repeated zero
        values, use negative numbers in the formula.  The same document
        also specifies rounding rules which seem to be ignored by makers of
        tables.  Gauges up to 44 are to be specified with up to 4
        significant figures, but no closer than 0.0001 inch.  Gauges from
        44 to 56 are to be rounded to the nearest 0.00001 inch.
 
    An equivalent formula is 0.32487/1.12294049**n where n is the
    gauge number (works for n >= 0).
    '''
    if n < -3 or n > 56:
        raise ValueError("AWG argument out of range")
    diameter = 92.**((36 - n)/39)/200
    if n <= 44:
        return round(diameter, 4)
    return round(diameter, 5)

def WireGauge(num, mm=False):
    '''If num is an integer between 1 and 80, this function will return the
    diameter of the indicated wire gauge size in inches (or mm if the mm
    keyword is True).  This gauge is used for number-sized drills in the
    US.
 
    If num is a floating point number, this function will return an
    integer representing the nearest wire gauge size.  It will throw
    an exception if the floating point number is greater than the
    diameter of #1 or less than #80.
    '''
    # Index number in sizes is wire gauge number.  units is the number of
    # inches for each integral wire gauge size.
    units, sizes = 1e-4, (
        0, 2280, 2210, 2130, 2090, 2055, 2040, 2010, 1990, 1960, 1935,
        1910, 1890, 1850, 1820, 1800, 1770, 1730, 1695, 1660, 1610,
        1590, 1570, 1540, 1520, 1495, 1470, 1440, 1405, 1360, 1285,
        1200, 1160, 1130, 1110, 1100, 1065, 1040, 1015,  995,  980, 960,
        935,  890,  860,  820,  810,  785,  760, 730,  700,  670,  635,
        595,  550,  520,  465, 430,  420,  410,  400,  390,  380,  370,
        360, 350,  330,  320,  310,  293,  280,  260,  250, 240,  225,
        210,  200,  180,  160,  145,  135)
    if isinstance(num, int):
        if num < 1 or num > 80:
            raise ValueError("num must be between 1 and 80 inclusive")
        return units*sizes[num]*25.4 if mm else units*sizes[num]
    elif isinstance(num, float):
        if mm:
            num /= 25.4  # Convert to inches
        # Note sizes is from largest to smallest
        if num > units*sizes[1] or num < units*sizes[80]:
            raise ValueError("num diameter is outside wire gauge range")
        # Create units list with the differences from the target value.
        # Note we've deleted the 0 element.
        s = list(map(lambda x: abs(x - num/units), sizes[1:]))
        t = [(s[i], i) for i in range(len(s))]    # Combine with array position
        t.sort()  # Sort to put minimum diff first in list
        return t[0][1] + 1  # Add 1 because we deleted the first element
    else:
        raise ValueError("num is an unexpected type")

def SignSignificandExponent(x, digits=15):
    '''Returns a tuple (sign, significand, exponent) of a floating point
    number x.
    '''
    s = ("%%.%de" % digits) % abs(float(x))
    return (1 - 2*(x < 0), float(s[0:digits + 2]), int(s[digits + 3:]))

def significand(x, digits=6):
    '''Return the significand of x rounded to the indicated number of
    digits.
    '''
    s = SignSignificandExponent(x)[1]
    return round(s, digits - 1)

def mantissa(x, digits=6):
    '''Return the mantissa of the base 10 logarithm of x rounded to the
    indicated number of digits.
    '''
    return round(math.log10(significand(x, digits=digits)), digits)

def SignificantFiguresS(value, digits=3, exp_compress=True):
    '''Returns a string representing the number value rounded to
    a specified number of significant figures.  The number is
    converted to a string, then rounded and returned as a string.
    If you want it back as a number, use float() on the string.
    If exp_compress is true, the exponent has leading zeros
    removed.
 
    The following types of printouts can be gotten using this function
    and native python formats:
 
           A              B               C               D
       3.14e-12       3.14e-012       3.14e-012       3.14e-012
       3.14e-11       3.14e-011       3.14e-011       3.14e-011
       3.14e-10       3.14e-010       3.14e-010       3.14e-010
        3.14e-9       3.14e-009       3.14e-009       3.14e-009
        3.14e-8       3.14e-008       3.14e-008       3.14e-008
        3.14e-7       3.14e-007       3.14e-007       3.14e-007
        3.14e-6       3.14e-006       3.14e-006       3.14e-006
        3.14e-5       3.14e-005       3.14e-005       3.14e-005
        3.14e-4       3.14e-004        0.000314        0.000314
        3.14e-3       3.14e-003         0.00314         0.00314
        3.14e-2       3.14e-002          0.0314          0.0314
        3.14e-1       3.14e-001           0.314           0.314
        3.14e+0       3.14e+000            3.14            3.14
        3.14e+1       3.14e+001            31.4            31.4
        3.14e+2       3.14e+002             314           314.0
        3.14e+3       3.14e+003       3.14e+003          3140.0
        3.14e+4       3.14e+004       3.14e+004         31400.0
        3.14e+5       3.14e+005       3.14e+005        314000.0
        3.14e+6       3.14e+006       3.14e+006       3140000.0
        3.14e+7       3.14e+007       3.14e+007      31400000.0
        3.14e+8       3.14e+008       3.14e+008     314000000.0
        3.14e+9       3.14e+009       3.14e+009    3140000000.0
       3.14e+10       3.14e+010       3.14e+010   31400000000.0
       3.14e+11       3.14e+011       3.14e+011  314000000000.0
       3.14e+12       3.14e+012       3.14e+012       3.14e+012
 
    A:  SignificantFiguresS(x, 3)
    B:  SignificantFiguresS(x, 3, 0)
    C:  "%.3g" % x
    D:  float(SignificantFiguresS(x, 3))
    '''
    if digits < 1 or digits > 15:
        msg = "Number of significant figures must be >= 1 and <= 15"
        raise ValueError(msg)
    sign, significand, exponent = SignSignificandExponent(float(value))
    fmt = "%%.%df" % (digits-1)
    neg = "-" if sign < 0 else ""
    e = "e%+d" % exponent if exp_compress else "e%+04d" % exponent
    return neg + (fmt % significand) + e

def SignificantFigures(value, figures=3):
    '''Rounds a value to specified number of significant figures.
    Returns a float.
    '''
    return float(SignificantFiguresS(value, figures))

def EditData(data, binary=False):
    'Edit a str or bytes object using vim'
    if not isinstance(data, (str, bytes)):
        raise TypeError("data must be a str or bytes object")
    if binary and isinstance(data, str):
        raise TypeError("data must be a bytes object")
    if not binary and isinstance(data, bytes):
        raise TypeError("data must be a str")
    vi = "vim"
    with tempfile.NamedTemporaryFile() as temp:
        file = P(temp.name)
        if binary:
            file.write_bytes(data)
            cmd = [vi, "-b", str(file)]
        else:
            file.write_text(data)
            cmd = [vi, str(file)]
        subprocess.call(cmd)
        if binary:
            data = file.read_bytes()
        else:
            data = file.read_text()
    return data

def Engineering(value, digits=3):
    '''Return a tuple (m, e, s) representing a number in engineering
    notation.  m is the significand.  e is the exponent in the form of
    an integer; it is adjusted to be a multiple of 3.  s is the SI
    symbol for the exponent; for "e+003" it would be "k".  s is empty
    if there is no SI symbol.
 
    Engineering(1.2345678901234567890e-88, 4) --> ('123.5', -90, '')
    Engineering(1.2345678901234567890e-8, 4)  --> ('12.35', -9, 'n')
    Engineering(1.2345678901234567890e8, 4)   --> ('123.5', 6, 'M')
    Examples:
    '''
    suffixes = {
        -8: "y", -7: "z", -6: "a", -5: "f", -4: "p", -3: "n",
        -2: "u", -1: "m", 0: "", 1: "k", 2: "M", 3: "G", 4: "T",
        5: "P", 6: "E", 7: "Z", 8: "Y"}
    if digits < 1 or digits > 15:
        raise ValueError("Number of significant digits must be >= 1 and <= 15")
    sign, significand, exponent = SignSignificandExponent(float(value))
    s = suffixes[exponent//3] if exponent//3 in suffixes else ""
    m = sign*(("%%.%dg" % digits) % (significand*10**(exponent % 3)))
    if m.find("e") != -1:
        # digits = 1 or 2 can cause e.g. 3e+001, so the following
        # eliminates the exponential notation
        m = str(int(float(m)))
    return m, 3*(exponent//3), s

def eng(value, digits=3, unit=None, width=0):
    '''Convenience function for engineering representation.  If unit is
    given, then the number of digits is displayed in value with the
    prefix prepended to unit.  Otherwise, "xey" notation is used, except if
    y == 0, no exponent portion is given.  Returns a string for printing.
    If width is nonzero, then returns a string right-justified to that
    width.
    '''
    m, e, p = Engineering(value, digits)
    if unit:
        s = m + " " + p + unit
    else:
        s = m if e == 0 else "%se%d" % (m, e)
    if width:
        if len(s) < width:
            p = (" " * (width - len(s)))
            s = p + s
    return s

def IdealGas(P=0, v=0, T=0, MW=28.9):
    '''Given two of the three variables P, v, and T, calculates the
    third for the indicated gas.  The variable that is unknown should
    have a value of zero.
        P = pressure in Pa
        v = specific volume in m^3/kg
        T = absolute temperature in K
        MW = molecular weight = molar mass in g/mol (defaults to air)
             Note you can also supply a string; if the lower-case
             version of this string is in the dictionary of gas_molar_mass
             below, the molar mass for that gas will be used.
    The tuple (P, v, T) will be returned.
 
    WARNING:  Note that v is the specific volume, not the volume!
 
    The equation used is P*v = R*T where R is the gas constant for this
    particular gas.  It is the universal gas constant divided by the
    molecular weight of the gas.
 
    The ideal gas law is an approximation, but a good one for high
    temperatures and low pressures.  Here, high and low are relative
    to the critical temperature and pressure of the gas; these can be
    found in numerous handbooks, such as the CRC Handbook of Chemistry
    and Physics, the Smithsonian Critical Tables, etc.
 
    Some molar masses and critical values for common gases are:
 
                    Tc       Pc     MW
        air        133.3   37.69   28.9
        ammonia    405.6  113.14   17.03
        argon      151.0   48.00   39.95
        co2        304.2   73.82   44.0099
        helium       5.2    2.25    4.003
        hydrogen    33.3   12.97    2.01594
        methane    190.6   46.04   16.04298
        nitrogen   126.1   33.94   28.0134
        oxygen     154.6   50.43   31.9988
        propane    369.8   42.49   26.03814
        water      647.3  221.2    18.01534
        xenon      289.8   58.00  131.30
 
    Tc is the critical temperature in K, Pc is the critical pressure
    in bar (multiply by 1e5 to get Pa), and MW is the molecular
    weight in daltons (1 Da = 1 g/mol).
    '''
    gas_molar_mass = {
        "air"      : 28.9,
        "ammonia"  : 17.03,
        "argon"    : 39.95,
        "co2"      : 44.0099,
        "helium"   : 4.003,
        "hydrogen" : 2.01594,
        "methane"  : 16.04298,
        "nitrogen" : 28.0134,
        "oxygen"   : 31.9988,
        "propane"  : 26.03814,
        "water"    : 18.01534,
        "xenon"    : 131.30,
    }
    if isinstance(MW, str):
        MW = gas_molar_mass[MW.lower()]
    else:
        assert(P >= 0 and v >= 0 and T >= 0 and MW >= 0)
    molar_gas_constant = 8.3145         # J/(mol*K)
    R = molar_gas_constant/(float(MW)/1000)   # 1000 converts g to kg
    if sum([i == 0 for i in (P, v, T)]) != 1:
        raise ValueError("One and only one of P, v, T must be zero")
    if not P:
        return R*T/v
    elif not v:
        return R*T/P
    else:
        return P*v/R

def AlmostEqual(a, b, rel_err=2e-15, abs_err=5e-323):
    '''Determine whether floating-point values a and b are equal to
    within a (small) rounding error; return True if almost equal and
    False otherwise.  The default values for rel_err and abs_err are
    chosen to be suitable for platforms where a float is represented
    by an IEEE 754 double.  They allow an error of between 9 and 19
    ulps.
 
    This routine comes from the Lib/test/test_cmath.py in the python
    distribution; the function was called almostEqualF.
    '''
    # Special values testing
    if math.isnan(a):
        return math.isnan(b)
    if math.isinf(a):
        return a == b
    # If both a and b are zero, check whether they have the same sign
    # (in theory there are examples where it would be legitimate for a
    # and b to have opposite signs; in practice these hardly ever
    # occur).
    if not a and not b:
        return math.copysign(1., a) == math.copysign(1., b)
    # If a-b overflows, or b is infinite, return False.  Again, in
    # theory there are examples where a is within a few ulps of the
    # max representable float, and then b could legitimately be
    # infinite.  In practice these examples are rare.
    try:
        absolute_error = abs(b-a)
    except OverflowError:
        return False
    else:
        return absolute_error <= max(abs_err, rel_err*abs(a))

def Flatten(L, max_depth=None, ltypes=(list, tuple)):
    ''' Flatten every sequence in L whose type is contained in
    "ltypes" to "max_depth" levels down the tree.  The sequence
    returned has the same type as the input sequence.
 
    Written by Kevin L. Sitze on 2010-11-25.  From
    http://code.activestate.com/recipes/577470-fast-flatten-with-depth-control-and-oversight-over/?in=lang-python
    This code may be used pursuant to the MIT License.
 
    Note:  itertools has a flatten() recipe that flattens one level:
 
        def flatten(listOfLists):
            'Flatten one level of nesting'
            return chain.from_iterable(listOfLists)
 
    but every element encountered needs to be an iterable.  This
    Flatten() function works more generally.
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

def CommonPrefix(seq):
    '''Return the largest string that is a prefix of all the strings in
    seq.
    '''
    return os.path.commonprefix(seq)

def CommonSuffix(seq):
    '''Return the largest string that is a suffix of all the strings in
    seq.
    '''
    # Method:  reverse each string in seq, find their common prefix, then
    # reverse the result.
    f = lambda lst:  ''.join(lst)   # Convert the list back to a string
    def rev(s):     # Reverse the string s
        return f([f(list(i)) for i in reversed(s)])
    return rev(CommonPrefix([rev(i) for i in seq]))

def TempConvert(t, in_unit, to_unit):
    '''Convert the temperature in t in the unit specified in in_unit to the
    unit specified by to_unit.
    '''
    allowed, k, r, a, b = "cfkr", 273.15, 459.67, 1.8, 32
    def check(unit, orig):
        if len(unit) != 1 and unit not in allowed:
            raise ValueError("'%s' is a bad temperature unit" % orig)
    inu, tou = [i.lower() for i in (in_unit, to_unit)]
    check(inu, in_unit)
    check(tou, to_unit)
    if inu == tou:
        return t
    d = {
        "cf" : lambda t: a*t + b,
        "ck" : lambda t: t + k,
        "cr" : lambda t: a*(t + k),
        "fc" : lambda t: (t - b)/a,
        "fk" : lambda t: (t - b)/a + k,
        "fr" : lambda t: t + r,
        "kc" : lambda t: t - k,
        "kf" : lambda t: a*(t - k) + b,
        "kr" : lambda t: a*t,
        "rc" : lambda t: (t - r - b)/a,
        "rf" : lambda t: t - r,
        "rk" : lambda t: t/a,
    }
    T = d[inu + tou](t)
    e = ValueError("Converted temperature is too low")
    if ((tou in "kr" and T < 0) or (tou == "c" and T < -k) or
            (tou == "f" and T < -r)):
        raise e
    return T

def SplitOnNewlines(s):
    ''' Splits s on all of the three newline sequences: "\r\n", "\r", or
    "\n".  Returns a list of the strings.
 
    Copyright (c) 2002-2009 Zooko Wilcox-O'Hearn, who put it under the GPL.
    '''
    cr = "\r"
    res = []
    for x in s.split(cr + nl):
        for y in x.split(cr):
            res.extend(y.split(nl))
    return res

def DecimalToBase(num, base, check_result=False):
    '''Convert a decimal integer num to a string in base base.  Tested with
    random integers from 10 to 10,000 digits in bases 2 to 36 inclusive.
    Set check_result to True to assure that the integer was converted
    properly.
    '''
    if not 2 <= base <= 36:
        raise ValueError('Base must be between 2 and 36.')
    if num == 0:
        return "0"
    s, sign, n = "0123456789abcdefghijklmnopqrstuvwxyz", "", abs(num)
    if num < 0:
        sign, num = "-", abs(num)
    d, in_base = dict(zip(range(len(s)), list(s))), ""
    while num:
        num, rem = divmod(num, base)
        in_base = d[rem] + in_base
    if check_result and int(in_base, base) != n:
        raise ArithmeticError("Base conversion failed for %d to base %d" %
                              (num, base))
    return sign + in_base

def ConvertToNumber(s, handle_i=True):
    '''This is a general-purpose routine that will return a python number
    for a string if it is possible.  The basic logic is:
        * If it contains 'j' or 'J', it's complex
        * If it contains '/', it's a fraction
        * If it contains '.', 'E', or 'e', it's a float
        * Otherwise it's interpreted to be an integer
    Since I prefer to use 'i' for complex numbers, we'll also allow an 'i'
    in the number unless handle_i is False.
    '''
    s = s.lower()
    if handle_i:
        s = s.replace("i", "j")
    if 'j' in s:
        return complex(s)
    elif '.' in s or 'e' in s:
        return float(s)
    elif '/' in s:
        return Fraction(s)
    else:
        return int(s)

def StringToNumbers(s, sep=" ", handle_i=True):
    '''s is a string; return the sequence (tuple) of numbers it
    represents; number strings are separated by the string sep.  The
    numbers returned are integers, fractions, floats, or complex.  If
    handle_i is True, 'i' or 'I' are allowed as the imaginary unit.
    '''
    seq = []
    for line in s.strip().split(nl):
        if sep is None:
            seq.extend(line.split(sep))
        else:
            seq.extend(line.split())
    return tuple([ConvertToNumber(i, handle_i=handle_i) for i in seq])

class bitvector(int):
    '''This convenience class is an integer that lets you get its bit
    values using indexing or slices.
 
    Examples:
        x = bitvector(9)
        x[3] returns 1
        x[2] returns 0
        x[2:3] returns 2
        x[123] returns 0    # Arbitrary bits can be addressed
        x[-1] raises an IndexError
 
    Suggested from python 2 code given by Ross Rogers at
    (http://stackoverflow.com/questions/147713/how-do-i-manipulate-bits-in-python)
    dated 29 Sep 2008.
    '''
    def __repr__(self):
        return "bitvector({})".format(self)
    def _validate_slice(self, slice):
        '''Check the slice object for valid values; raises an IndexError if
        it's improper.  Return (start, stop) where the values are valid
        indices into the binary value.  Note that start and stop values can
        be any integers >= 0 as long as start is less than or equal to
        stop.
        '''
        start, stop, step = slice.start, slice.stop, slice.step
        # Check start
        if start is None:
            start = 0
        elif start < 0:
            raise IndexError("Slice start cannot be < 0")
        # Check stop
        if stop is None:
            stop = int(math.log(self)/math.log(2))
        elif stop < 0:
            raise IndexError("Slice stop cannot be < 0")
        if step is not None:
            raise IndexError("Slice step must be None")
        if start > stop:
            raise IndexError("Slice start must be <= stop")
        return start, stop
    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = self._validate_slice(key)
            return bitvector((self >> start) & (2**(stop - start + 1) - 1))
        else:
            try:
                index = int(key)
            except Exception:
                raise IndexError("'{}' is an invalid index".format(key))
            if index < 0:
                raise ValueError("Negative bit index not allowed")
            return bitvector((self & 2**index) >> index)

def hyphen_range(s, sorted=False, unique=False):
    '''Takes a set of range specifications of the form "a-b" and returns a
    list of integers between a and b inclusive.  Also accepts comma
    separated ranges like "a-b,c-d,f".  Numbers from a to b, a to d and f.
    If sorted is True, the returned list will be sorted.  If unique is
    True, only unique numbers are kept and the list is automatically
    sorted.  In "a-b", a can be larger than b, in which case the
    sequence will decrease until b is reached.
 
    Adapted from routine at
    http://code.activestate.com/recipes/577279-generate-list-of-numbers-from-hyphenated-and-comma/?in=lang-python
    '''
    s = "".join(s.split())    # Removes white space
    r = []
    for x in s.split(','):
        t = [int(i) for i in x.split('-')]
        if len(t) not in (1, 2):
            raise ValueError("'%s' is bad range specifier" % s)
        if len(t) == 1:
            r.append(t[0])
        else:
            if t[0] < t[1]:
                r.extend(range(t[0], t[1] + 1))
            else:
                r.extend(range(t[0], t[1] - 1, -1))
    if sorted:
        r.sort()
    elif unique:
        r = list(set(r))
        r.sort()
    return r

US_states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

def Binary(n):
    '''convert an integer n to a binary string.  Example:  Binary(11549)
    gives '10110100011101'.
    '''
    if 0:
        # from http://www.daniweb.com/software-development/python/code/216539
        s, m = "", abs(n)
        if not n:
            return "0"
        while m > 0:
            s = str(m % 2) + s
            m >>= 1
        return "-" + s if n < 0 else s
    else:
        # Use built-in bin()
        return "-" + bin(n)[3:] if n < 0 else bin(n)[2:]

def int2bin(n, numbits=32):
    '''Returns the binary of integer n, using numbits number of
    digits.  Note this is a two's-complement representation.
    From http://www.daniweb.com/software-development/python/code/216539
    '''
    return "".join([str((n >> y) & 1) for y in range(numbits - 1, -1, -1)])

def grouper(data, mapper, reducer=None):
    '''Simple map/reduce for data analysis.
 
    Each data element is passed to a *mapper* function.
    The mapper returns key/value pairs
    or None for data elements to be skipped.
 
    Returns a dict with the data grouped into lists.
    If a *reducer* is specified, it aggregates each list.
 
    >>> def even_odd(elem):                     # sample mapper
    ...     if 10 <= elem <= 20:                # skip elems outside the range
    ...         key = elem % 2                  # group into evens and odds
    ...         return key, elem
 
    >>> grouper(range(30), even_odd)         # show group members
    {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}
 
    >>> grouper(range(30), even_odd, sum)    # sum each group
    {0: 90, 1: 75}
 
    Note:  from
    http://code.activestate.com/recipes/577676-dirt-simple-mapreduce/?in=lang-python
    I renamed the function to grouper.
    '''
    d = {}
    for elem in data:
        r = mapper(elem)
        if r is not None:
            key, value = r
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    if reducer is not None:
        for key, group in d.items():
            d[key] = reducer(group)
    return d

def FindDiff(s1, s2, ignore_empty=False, equal_length=False):
    '''Returns the integer index of where the strings s1 and s2 first
    differ.  The number returned is the index where the first
    difference was found.  If the strings are equal, then -1 is
    returned, implying one string is a substring of the other (or they
    are the same string).  If ignore_empty is True, an exception is
    raised if one of the strings is empty.  If equal_length is True,
    then the strings must be of equal length or a ValueError exception
    is raised.
    '''
    if not isinstance(s1, str) or not isinstance(s2, str):
        raise TypeError("Arguments must be strings")
    if (not s1 or not s2) and not ignore_empty:
        raise ValueError("String cannot be empty")
    ls1, ls2 = len(s1), len(s2)
    if equal_length and ls1 != ls2:
        raise ValueError("Strings must be equal lengths")
    n = min(len(s1), len(s2))
    if not n:
        return 0
    for i in range(n):
        if s1[i] != s2[i]:
            return i
    # If we get here, every character matched up to the end of the
    # shorter string.
    return -1

class Walker(object):
    '''Defines a class that operates as a generator for recursively getting
    files or directories from a starting directory.  The default is to
    return files; if you want directories, set the dir attribute to True.
    The ignore option to the constructor defines directories to ignore.
 
    An example of use to show all the files in the current directory tree:
 
        w = Walker()
        for i in w("."):
            print(i)
     
    Note:  the functionality here is obsolete because
    pathlib.glob("**/*") can do these things.
    '''
    def __init__(self, ignore=".bzr .git .hg .rcs __pycache__".split(),
                 dir=False):
        self.dir = dir
        self._ignore = ignore
    def __str__(self):
        return "util.Walker(ignore={}, dir={})".format(self._ignore, self.dir)
    def __repr__(self):
        return str(self)
    def _ignore_this(self, dir):
        for i in dir.split("/"):
            if i in self._ignore:
                return True
        return False
    def __call__(self, location):
        '''Walk the directory tree starting at location.  This is a
        generator that returns each file or directory found.
        '''
        if not os.path.isdir(location):
            raise ValueError("location must be a directory")
        for root, dirs, files in os.walk(location):
            if self._ignore_this(root):
                continue
            if self.dir:
                for dir in dirs:
                    if self._ignore_this(dir):
                        continue
                    p = os.path.join(root, dir)
                    if os.path.isdir(p):
                        yield p
            else:
                for file in files:
                    p = os.path.join(root, file)
                    if os.path.isfile(p):
                        yield p

def IsConvexPolygon(*p):
    '''Return True if the sequence p of two-dimensional points
    constitutes a convex polygon.  Ref:
    http://stackoverflow.com/questions/471962/how-do-determine-if-a-polygon-is-complex-convex-nonconvex#
 
    The assumption is that the sequence p of points traverses consecutive
    points of the polygon.
 
    The algorithm is to look at the triples of points and calculate the
    sign of the z component of their cross product.  The polygon is
    convex if the signs are either all negative or all positive.
 
    Examples:
        ((0, 0), (1, 0), (1, 1), (1, 0)) will return True.
        ((0, 0), (1, 0), (1, 1), (0.5,         0.5)) will return False.
        ((0, 0), (1, 0), (1, 1), (0.5 - 1e-10, 0.5)) will return True.
    '''
    n = len(p)
    if n < 3:
        raise ValueError("Need at least three points")
    cross_product_signs = []
    for index in range(n + 3):
        # Generate indices of the needed points
        i = index % n
        j = (index + 1) % n
        k = (index + 2) % n
        p1, p2, p3 = p[i], p[j], p[k]
        dx1 = p2[0] - p1[0]
        dy1 = p2[1] - p1[1]
        dx2 = p3[0] - p2[0]
        dy2 = p3[1] - p2[1]
        cross_product_signs.append(signum(dx1*dy2 - dy1*dx2))
    assert(len(cross_product_signs) == n + 3)
    if cross_product_signs[0] and len(set(cross_product_signs)) == 1:
        return True
    return False

def BraceExpansion(s, glob=False):
    '''Generator to perform brace expansion on the string s.  If glob
    is True, then also glob each pattern in the current directory.
     
    Examples:
    
        - list(BraceExpansion("a.{a, b}")) returns ['a.a', 'a. b'].
 
        - list(BraceExpansion("pictures/*.{jpg, png}")) returns a list of
          all the JPG and PNG files in the pictures directory under the
          current directory.
    '''
    # Algorithm from http://rosettacode.org/wiki/Brace_expansion#Python
    def getitem(s, depth=0):
        out = [""]
        while s:
            c = s[0]
            if depth and (c == ',' or c == '}'):
                return out, s
            if c == '{':
                x = getgroup(s[1:], depth+1)
                if x:
                    out, s = [a+b for a in out for b in x[0]], x[1]
                    continue
            if c == '\\' and len(s) > 1:
                s, c = s[1:], c + s[1]
            out, s = [a + c for a in out], s[1:]
        return out, s
    def getgroup(s, depth):
        out, comma = [], False
        while s:
            g, s = getitem(s, depth)
            if not s:
                break
            out += g
            if s[0] == '}':
                if comma:
                    return out, s[1:]
                return ['{' + a + '}' for a in out], s[1:]
            if s[0] == ',':
                comma, s = True, s[1:]
        return None
    if glob:
        for i in getitem(s)[0]:
            for j in glob.glob(i):
                yield j
    else:
        for i in getitem(s)[0]:
            yield i

def bin2gray(bits):
    '''bits will be a string representing a binary number with the most
    significant bit at index 0; for example, the integer 13 would be
    represented by the string '1101'.  Return a string representing a Gray
    code of this number.
 
    Example:  If bits = '1011' (binary of the integer 13), this function
    returns '1011'.
    '''
    # Algorithm from http://rosettacode.org/wiki/Gray_code#Python
    b = [int(i) for i in bits]
    g = b[:1] + [i ^ ishift for i, ishift in zip(b[:-1], b[1:])]
    return ''.join([str(i) for i in g])

def gray2bin(bits):
    '''bits will be a string representing a Gray-encoded binary number.
    Return a string representing a binary number with the most significant
    bit at index 0.
 
    Example:  If bits = '1101', this function returns '1101', the binary
    form of the integer 13.
    '''
    # Algorithm from http://rosettacode.org/wiki/Gray_code#Python
    Bits = [int(i) for i in bits]
    b = [Bits[0]]
    for nextb in Bits[1:]:
        b.append(b[-1] ^ nextb)
    return ''.join([str(i) for i in b])

def WordID(half_length=3, unique=None, num_tries=100):
    '''Return an ID string that is (somewhat) pronounceable.  The
    returned number of characters will be twice the half_length.  If
    unique is not None, it must be a container that can be used to
    determine if the ID is unique.  You are responsible for adding the
    returned word to the container.
 
    The method is to choose a consonant from 'bdfghklmnprstvw' and append a
    vowel; do this half_length number of times.
 
    Interestingly, the words often look like they came from Japanese or
    Hawaiian.
    '''
    # Derived from http://code.activestate.com/recipes/576858
    # downloaded Tue 12 Aug 2014 12:38:54 PM.  Original recipe by
    # Robin Parmar on 8 Aug 2007 under PSF license.
    from random import choice
    v, c, r, count = 'aeiou', 'bdfghklmnprstvw', range(half_length), 0
    while count < num_tries:
        word = ''.join([choice(c) + choice(v) for i in r])
        if not unique or (unique and word not in unique):
            return word
        count += 1
    raise RuntimeError("Couldn't generate unique word")
 
    '''Here's some driver code that prints out lists of these words.
 
    from columnize import Columnize
    from words import words_ic
    num_words = 100
    for n in range(2, 6):
        print("{} letters:".format(2*n))
        uniq = set()
        for i in range(num_words):
            is_word = True
            while is_word:
                w = WordID(n, unique=uniq)
                is_word = w in words_ic
                if not is_word:
                    uniq.add(w)
        s = sorted(list(uniq))
        for line in Columnize(s, col_width=2*n+2, indent=" "*2):
            print(line)
        print()
    '''

# TODO:  Convert to a class so the instance is thread-safe

def Spinner(chars=r"-\|/-\|/", delay=0.1):
    '''Show a spinner to indicate that processing is still taking place.
    Set Spinner.stop to True to cause it to exit.  Note this is not
    thread-safe.
 
    Here's some example code that demonstrates how it could be used:
 
        from threading import Thread
        def T():
            Spinner()
            if Spinner.stop:
                return
        t = Thread(target=T)
        t.start()
        time.sleep(2)
        Spinner.stop = True
    '''
    # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
    for frame in cycle(chars):
        print('\r', frame, sep='', end='', flush=True)
        time.sleep(delay)
        if Spinner.stop:
            print()
            return
Spinner.stop = False

def ProgressBar(frac=0, width=40, char="#"):
    '''Prints a progress bar to stdout.  frac must be a number on the
    closed interval [0, 1].
 
    Here's an example of use:
        n = 100
        for i in range(n + 1):
            ProgressBar(i/n)
            time.sleep(0.01)
        print()
    '''
    # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
    assert(len(char) == 1)
    left = int(width*frac)
    right = width - left
    percent = int(100*frac)
    print("\r[", char*left, " "*right, "]", " {}%".format(percent),
          sep="", end="", flush=True)

def Paste(*seq, missing="", sep="\t"):
    '''Return a list whose elements are each corresponding element of the
    sequences in *seq, separated by the string sep.  If a sequence is too
    short, the missing string will be substituted.  All sequence elements
    will be converted to strings using str().
 
    Example:
        Paste([1, 2, "a"], ["3 4", 5], missing="X")
    will return
        ['1\t3 4', '2\t5', 'a\tX']
    '''
    result = list(zip_longest(*seq, fillvalue=missing))
    for i, item in enumerate(result):   # Convert all elements to strings
        result[i] = [str(j) for j in result[i]]
    return [sep.join(i) for i in result]

def EBCDIC():
    '''Returns two byte-translation tables to use with
    bytes.translate().  The first converts ASCII bytes to EBCDIC and the
    second converts EBCDIC bytes to ASCII.
    '''
    a2e = [
        0, 1, 2, 3, 55, 45, 46, 47, 22, 5, 37, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 60, 61, 50, 38, 24, 25, 63, 39, 28, 29, 30, 31, 64,
        79,127,123, 91,108, 80,125, 77, 93, 92, 78,107, 96, 75, 97,
        240,241,242,243,244,245,246,247,248,249,122, 94, 76,126,110,111,
        124,193,194,195,196,197,198,199,200,201,209,210,211,212,213,214,
        215,216,217,226,227,228,229,230,231,232,233, 74,224, 90, 95,109,
        121,129,130,131,132,133,134,135,136,137,145,146,147,148,149,150,
        151,152,153,162,163,164,165,166,167,168,169,192,106,208,161, 7,
        32, 33, 34, 35, 36, 21, 6, 23, 40, 41, 42, 43, 44, 9, 10, 27,
        48, 49, 26, 51, 52, 53, 54, 8, 56, 57, 58, 59, 4, 20, 62,225,
        65, 66, 67, 68, 69, 70, 71, 72, 73, 81, 82, 83, 84, 85, 86, 87,
        88, 89, 98, 99,100,101,102,103,104,105,112,113,114,115,116,117,
        118,119,120,128,138,139,140,141,142,143,144,154,155,156,157,158,
        159,160,170,171,172,173,174,175,176,177,178,179,180,181,182,183,
        184,185,186,187,188,189,190,191,202,203,204,205,206,207,218,219,
        220,221,222,223,234,235,236,237,238,239,250,251,252,253,254,255
    ]
    e2a = [
        0, 1, 2, 3,156, 9,134,127,151,141,142, 11, 12, 13, 14, 15, 16,
        17, 18, 19,157,133, 8,135, 24, 25,146,143, 28, 29, 30, 31,
        128,129,130,131,132, 10, 23, 27,136,137,138,139,140, 5, 6, 7,
        144,145, 22,147,148,149,150, 4,152,153,154,155, 20, 21,158, 26,
        32,160,161,162,163,164,165,166,167,168, 91, 46, 60, 40, 43, 33,
        38,169,170,171,172,173,174,175,176,177, 93, 36, 42, 41, 59, 94,
        45, 47,178,179,180,181,182,183,184,185,124, 44, 37, 95, 62, 63,
        186,187,188,189,190,191,192,193,194, 96, 58, 35, 64, 39, 61, 34,
        195, 97, 98, 99,100,101,102,103,104,105,196,197,198,199,200,201,
        202,106,107,108,109,110,111,112,113,114,203,204,205,206,207,208,
        209,126,115,116,117,118,119,120,121,122,210,211,212,213,214,215,
        216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,
        123, 65, 66, 67, 68, 69, 70, 71, 72, 73,232,233,234,235,236,237,
        125, 74, 75, 76, 77, 78, 79, 80, 81, 82,238,239,240,241,242,243,
        92,159, 83, 84, 85, 86, 87, 88, 89, 90,244,245,246,247,248,249,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57,250,251,252,253,254,255
    ]
    s, t = bytearray(a2e), bytearray(e2a)
    return s.maketrans(s, t), s.maketrans(t, s)

def Ampacity(dia_mm, insul_degC=60, ambient_degC=30):
    '''Return the NEC-allowed current in a copper conductor at the
    indicated ambient temperature and with the indicated insulation
    temperature rating.  
 
    The data from table 310-16 in the 1998 NEC was fitted to cubic
    polynomials, so the table data won't be reproduced exactly.  Thus,
    the intended use is to estimate safe currents for a given wire size,
    particularly smaller wires than are in the table.  To get the
    ampacity of a smaller wire, the constant term of the regression was
    set to zero.
 
    The data and regressions are in /elec/projects/current_capacity.
    '''
    def AmbientCorrection(ambient_degC, insul_degC):
        if insul_degC not in (60, 75, 90):
            raise ValueError("insul_degC must be 60, 75, or 90 °C")
        if insul_degC == 60:
            i = 0
        elif insul_degC == 75:
            i = 1
        elif insul_degC == 90:
            i = 2
        T = int(ambient_degC)
        if not (21 <= T <= 80):
            raise ValueError("ambient_degC must be between 21 and 80 °C")
        if 21 <= T <= 25:
            return (1.08, 1.05, 1.04)[i]
        elif 26 <= T <= 30:
            return 1
        elif 31 <= T <= 35:
            return (0.91, 0.94, 0.96)[i]
        elif 36 <= T <= 40:
            return (0.82, 0.88, 0.91)[i]
        elif 41 <= T <= 45:
            return (0.71, 0.82, 0.87)[i]
        elif 46 <= T <= 50:
            return (0.58, 0.75, 0.82)[i]
        elif 51 <= T <= 55:
            return (0.41, 0.67, 0.76)[i]
        elif 56 <= T <= 60:
            return (0, 0.58, 0.71)[i]
        elif 61 <= T <= 70:
            return (0, 0.33, 0.58)[i]
        elif 71 <= T <= 80:
            return (0, 0, 0.41)[i]
    max_dia_mm = 11.68
    if not (0 < dia_mm <= max_dia_mm):
        raise ValueError("dia_mm must be in (0, 11.68 mm]")
    if insul_degC not in (60, 75, 90):
        raise ValueError("insul_degC must be 60, 75, or 90 °C")
    constants = {
        60: (10.6841, 0.667284, -0.014032),
        75: (11.0919, 1.25111, -0.0445333),
        90: (12.9412, 1.30463, -0.0441503),
    }
    b1, b2, b3 = constants[insul_degC]
    correction = AmbientCorrection(ambient_degC, insul_degC)
    if correction:
        return correction*(b1*dia_mm + b2*dia_mm**2 + b3*dia_mm**3)
    else:
        raise ValueError("ambient_degC out of range")
