# Python Unicode Identifiers for Unicode 4.1, taken from
# https://www.dcl.hpi.uni-potsdam.de/home/loewis/table-3131.html.  See
# https://www.python.org/dev/peps/pep-3131/, which states the above link is a
# non-normative (i.e., not officially sanctioned by python) listing of all
# valid identifiers.

# Note you can use the unicodedata module to look up the numerical
# equivalent and description string of a Unicode character.

import pickle

# The following set _identifiers contains the decimal integers that
# represent a Unicode character that is a valid python identifier.
_identifiers = pickle.load(open("identifiers.pickled", "rb"))

def IsIdentifier(c):
    '''Given an integer c, returns True if the integer represents a Unicode
    character that is a valid python 3 identifier; otherwise returns False.
    '''
    return c in _identifiers

