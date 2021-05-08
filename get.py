'''
Module for getting data from files, strings, and streams.

TODO:  Add function for getting a list of numbers from a string.
    GetNumbers(thing, type=None)
        Recognizes integers, floats, fractions, complex, and uncertain
        numbers.  If type is given, all found strings are converted to
        that type.  thing can be a string, filename, or stream.

        Add flt, cpx, Zn

'''

# Copyright (C) 2019 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import locale
import pathlib
import re
from asciify import Asciify
from collections import defaultdict
from fractions import Fraction

try:
    from uncertainties import ufloat, ufloat_fromstr
    _have_unc = True
except ImportError:
    _have_unc = False

try:
    from f import flt, cpx
    _have_f = True
except ImportError:
    _have_f = False

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def GetText(thing, enc=None, xfms=[]):
    '''Return the text from thing, which can be a string, bytes,
    or stream.  If thing is a string, it's assumed to be a file name;
    if trying to read the file generates an exception, the string itself
    is used as the text.
    
    If enc is not None, then it is an encoding to decode the data and
    if thing is a str, the file will be read as binary.
 
    xfms should be a sequence of univariate functions which will transform
    the string.
    '''
    if isinstance(thing, bytes):
        # Bytes
        s = thing.decode(encoding="UTF-8" if enc is None else enc)
    elif isinstance(thing, str):
        # File name
        p = pathlib.Path(thing)
        try:
            s = p.read_text(encoding=enc) if enc else p.read_text()
        except FileNotFoundError:
            s = thing
    elif hasattr(thing, "read"):
        # Stream
        s = thing.read()
    else:
        raise TypeError("Type of 'thing' not recognized")
    if xfms:
        # Apply the transformations
        for xfm in xfms:
            s = xfm(s)
    return s

def GetLines(thing, enc=None, regex=None, xfms=None):
    '''Return either lines or (lines, meta) where lines is a list of the
    lines in thing and meta is a dictionary containing lists of lines
    that were ignored in thing that matched (with re.search) the regular
    expressions in the sequence of strings regex; the keys of meta are
    the regular expression strings.  If regex is None, then only the
    list lines is returned.  See GetText for details on arguments.
 
    If xfms is not None, then it is a sequence of univariate functions
    that will transform every line (note it is not passed on to GetText).
 
    Example:
        s = """# Comment
        ## Another comment
        Line 1
            Line 2
        """
        r = ("^ *##", "^ *#")
        lines, meta = GetLines(s, regex=r)
        print(f"lines {list(lines)}")
        print(f"meta {meta}")
 
    returns 
        lines ['Line 1', '    Line 2', '']
        meta defaultdict(<class 'list'>, {'^ *#': ['# Comment'],
            '^ *##': ['  ## Another comment']})
    '''
    if regex is not None:
        assert(isinstance(regex, (list, tuple, set)))
    meta = defaultdict(list) if regex is not None else None
    def Filter(line):
        if regex is not None:
            for r in regex:
                if re.search(r, line):
                    meta[r].append(line)
                    return None     # Don't keep this line
        return True     # Keep this line
    lines = GetText(thing, enc=enc, xfms=xfms).split("\n")
    lines = list(filter(Filter, lines))
    if xfms:
        for xfm in xfms:
            lines = [xfm(line) for line in lines]
    if regex is None:
        return lines
    return (lines, meta)

def GetNumberedLines(thing, enc=None):
    '''Return a tuple of (linenum, line_string) tuples where linenum is
    the line number in the file.  See GetText for details on the enc
    argument.
    '''
    lines = GetText(thing, enc=enc).split("\n")
    return tuple((i + 1, j) for i, j in enumerate(lines))

def GetWords(thing, sep=None, enc=None, regex=None, xfms=None):
    '''Return a list of words separated by the string sep from the thing
    (see details for GetLines).  If sep is None, then the data are split
    on whitespace; otherwise, the newlines are replaced by sep, then the
    data are split on sep.  
    '''
    if regex is None:
        lines = GetLines(thing, xfms=xfms)
    else:
        lines, meta = GetLines(thing, regex=regex, xfms=xfms)
    if sep is not None:
        s = sep.join(lines)
        return sep.join(lines).split(sep)
    else:
        return ' '.join(lines).split()

def GetBinary(thing, encoded=False):
    '''Read in thing as binary (thing is a stream or filename).  Bytes
    will be returned.
    
    If encoded is True, then try to decode it by using a number of 
    encodings.  A string will be returned if it can be decoded.
    '''
    # See ConstructEncodingData in /pylib/enc.py, as it gives the
    # frequency of these encodings found on web pages.
    encodings = '''
        utf_8 latin_1 cp1251 cp1252 shift_jis gb2312 euc_kr euc_jp
        iso8859_2 gbk cp1250 big5 iso8859_9 iso8859_15
    '''.split()
    if encoded:
        try:
            s = thing.read()
        except AttributeError:
            s = open(thing, "rb").read()
        if isinstance(s, str):
            return s
        # Got bytes; try to decode them
        for encoding in encodings:
            try:
                return s.decode(encoding)
            except UnicodeDecodeError:
                pass
        raise ValueError("'thing' could not be decoded")
    else:
        try:
            return thing.read()
        except AttributeError:
            return open(thing, "rb").read()

def GetNumbers(thing, numtype=None,  enc=None, xfms=None):
    '''Uses GetText() to get a string, then recognizes integers, floats,
    fractions, complex, and uncertain numbers in the string separated by
    whitespace and returns a list of these numbers.  If numtype is
    given, all found strings are converted to that type.
 
    If flt and cpx types are available (_have_f is True), then floats
    and complex types are converted to these over float and complex, 
    respectively.
 
    If the uncertainties library is present, the ufloat type can be
    '''
    lst, dp = [], locale.localeconv()["decimal_point"]
    for s in GetText(thing, enc=enc, xfms=xfms).split():
        if numtype:
            lst.append(numtype(s))
        else:
            if _have_unc and "+-" in s:
                s = s.replace("+-", "+/-")
            if _have_unc and ("+/-" in s or "(" in s or "±" in s):
                x = ufloat_fromstr(s)
            elif "/" in s:
                x = Fraction(s)
            elif "j" in s.lower():
                x = cpx(s) if _have_f else complex(s)
            elif dp in s or "e" in s.lower():
                x = flt(s) if _have_f else float(s)
            else:
                x = int(s)
            lst.append(x)
    return lst

if __name__ == "__main__": 
    s = '''1 1.2 3/4 3+1j 3±4 3+-4 3+/-4 3(4)'''
    print(GetNumbers(s))
