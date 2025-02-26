"""

This script uses the cmudict from the nltk.corpus to generate a python
module that lets you look up the number of syllables in a word.  The
word must be all lowercase.

To use this script, you must first install nltk (the Natural Language
Toolkit):

    pip install nltk

You can learn more about nltk from
https://en.wikipedia.org/wiki/Natural_Language_Toolkit.  The authors
wrote a book published by O'Reilley (see http://nltk.org/book_1ed/).
You can also see an on-line version at http://www.nltk.org/book/.

The first time you run the script, you'll get an exception because the
cmudict data structure isn't present.  The backtrace will give you
instructions on how to download it (it's two simple instructions at a
python prompt).  After downloading, this script should then run.

Note:  It does not make sense to pickle the two dictionaries and load them
into a python module, as this save neither time nor space (found by an
experiment).

This script produces the same dictionaries when run under python 3.7.4
and 2.7.16, though they won't be in the same order when printed to the
file words_syllables.py.  The words_syllables.py file should be usable by
any python version.
"""

from __future__ import print_function
import sys
import time
from nltk.corpus import cmudict


def Syllables(word):
    """For the given word, returns the number of syllables in the word.
    The returned value will either be an integer or a tuple of integers.
    """
    t = [len(list(y for y in x if y[-1].isdigit())) for x in d[word]]
    syls = tuple(sorted(set(t)))
    return syls[0] if len(syls) == 1 else syls


# Construct two dictionaries.  The first, syllables, contains a unique
# mapping of the word in lower case letters to number of syllables.  The
# second, multiple_syllables, maps to a tuple of integers because the
# word has more than one pronounciation.  Examples:  'resume' returns
# (2, 3), but 'maps' returns 1.
syllables, multiple_syllables = {}, {}
d = cmudict.dict()
words = list(d.keys())
n = max([len(i) for i in words])
for w in words:
    t = Syllables(w)
    if isinstance(t, tuple):
        multiple_syllables[w] = t
    else:
        syllables[w] = t

# Items to ignore
ignore = set(
    (
        "!exclamation-point",
        "#sharp-sign",
        "%percent",
        "&ampersand",
        "'end-inner-quote",
        "'end-quote",
        "'inner-quote",
        "'quote",
        "'single-quote",
        "(begin-parens",
        "(in-parentheses",
        "(left-paren",
        "(open-parentheses",
        "(paren",
        "(parens",
        "(parentheses",
        ")close-paren",
        ")close-parentheses",
        ")end-paren",
        ")end-parens",
        ")end-parentheses",
        ")end-the-paren",
        ")paren",
        ")parens",
        ")right-paren",
        ")un-parentheses",
        ",comma",
        "-dash",
        "-hyphen",
        "...ellipsis",
        ".decimal",
        ".dot",
        ".full-stop",
        ".period",
        ".point",
        "/slash",
        ";semi-colon",
        "?question-mark",
        "a",
        "a's",
        "a.",
        "a.",
        "a.'s",
        "a.s",
        "a42128",
        "a42128",
        "aaa",
        "{brace",
        "{left-brace",
        "}close-brace",
        "}right-brace",
        '"close-quote',
        '"double-quote',
        '"end-of-quote',
        '"end-quote',
        '"in-quotes',
        '"quote',
        '"unquote',
    )
)

description = """'''
This module provides two dictionaries that give the number of syllables
in a word.  Convert a word to lowercase, then see if it is in the
syllables dictionary; if it is, then the number of syllables is
returned.  If not, then check in multiple_syllables; if it is, a tuple
of integers is returned.  

Examples:
    syllable["aardvark"] returns 2.
    multiple_syllables["babbling"] returns (2, 3).

This file was constructed by the {name} script on 
{date}.

The data came from the cmudict dictionary in the nltk.corpus module.  You
can install nltk with

    pip install nltk

The first time you run the script, you'll get an exception because the
cmudict data structure isn't present.  The backtrace will give you
instructions on how to download it (it's two simple instructions at a
python prompt).  After downloading, this script should then run.

Note:  the CMU dictionary from the nltk.corpus contains 123455 word
entries, but some of them are foreign words, acronyms, or abbreviations.
While they could be encountered in everyday speech (particularly the
acronyms), you might not want them to be in the two dictionaries.  
If so, call the module function Restrict(True); call Restrict(False) to
restore to the full dictionaries.

'''"""

if __name__ == "__main__":
    module_name = "words_syllables.py"
    name = sys.argv[0]
    date = time.asctime()
    # Save the module
    f = open(module_name, "w")
    print(description.format(**globals()), file=f)
    print("syllables = {", file=f)
    for i in syllables:
        if i in ignore:
            continue
        s = '    "{}": {},'.format(i, syllables[i])
        print(s, file=f)
    print("}", file=f)
    print(file=f)
    print("multiple_syllables = {", file=f)
    for i in multiple_syllables:
        s = '    "{}": {},'.format(i, multiple_syllables[i])
        print(s, file=f)
    print("}", file=f)
