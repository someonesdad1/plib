'''

Anagram algorithms
    Given a string, find all anagrams that use the letters that contain
    words in a given dictionary.
    https://stackoverflow.com/questions/7896694/how-to-find-find-anagrams-among-words-which-are-given-in-a-file
    https://stackoverflow.com/questions/12477339/finding-anagrams-for-a-given-word

- Prepared data structure for a given dictionary
    - Convert string to a multiset of letters
    - Set is then key to dict of list of words with the same set
- Prime integers
    - Assign each letter a prime number and compute the product for
        each string; if they match, they are anagrams.  For spaces
        and punctuation, you can use 1 to ignore them.  The method is
        based on the fundamental theorem of arithmetic that all
        non-prime numbers have unique factorizations.
- Multisets
    - Convert the strings to multisets; if the multisets are equal,
        the strings are anagrams.
- Sorted strings
    - Sort the letters of the strings; if they match, they are an
        anagram.
    - Sort the letters of the strings.  Use the sorted letters as a
        key to a dict with all other words with the same sorted
        letters.
    - Could use a dict keyed by the length of the string for faster
        lookups.
- Counter
    - f = collections.Counter(s) for string s returns a dict
        containing the counts of each character.  Thus, if f(s1) ==
        f(s2), then s1 and s2 are anagrams.
 
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import collections
        import getopt
        import os
        from pathlib import Path as P
        import pickle
        import string
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from timer import Timer
        import get
        import dpstr
    if 1:   # Global variables
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        Here's an example.  Put the following line of text into a file
        named 'data':
            
            I was able ere I saw Elba.
 
        Run the script as 'python anagram.py data' and you'll get the
        output
 
            elba able
            saw was
 
        These are the two pairs of words in the original string that are
        anagrams of each other.  All the words are converted to lowercase.

        On my system, I use a script to get all the words from a large
        number of files, then put the output in a file named 'anagrams'.
        When I want to find an anagram of a word x, I use the command 

            grep -i '\<x\>' anagram

        and I'll get lines printed that contain the string in x.  The 
        \< and \> terms make sure we only see complete words that match x.
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          This script constructs lines of anagrams from the words in the
          given files (use '-' for stdin) and prints them to stdout.  All
          text is converted to lowercase and words are separated by
          whitespace.  There are at least two words in each line of output.
 
          Example:  give the script a dictionary file with words separated
          by whitespace and send the output to a file 'anagrams'.  Later,
          you can find anagrams for a word with the command 'grep -i <word>
          anagrams'.
        Options:
            -a      Keep only ASCII letters
            -h      Print a manpage
            -p      Don't ignore words with punctuation
            -u      Convert Unicode characters to ASCII eqivalents
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def IsValidWord(word):
        '''Return True if word is considerd a valid word.  Here, valid
        means it only contains ASCII letters.
 
        If you want to have letters other than ASCII, construct a custom
        IsValidWord.rm_invalid translation mapping before calling
        GetWords().
 
        The algorithm is to use the string translation table to remove all
        non-ASCII characters.  The word is considered valid if the
        resulting string length is zero.
        '''
        if not hasattr(IsValidWord, "rm_invalid"):
            lc = string.ascii_lowercase
            IsValidWord.rm_invalid = "".maketrans(lc, " "*len(lc))
        s = word.translate(IsValidWord.rm_invalid).replace(" ", "")
        return not bool(len(s))
    def GetWords(mystring):
        '''Given a string, return a set of the words in this string.  The
        returned words will all be lowercase.  The algorithm is:
            - Change string to lowercase
            - Change all punctuation and digits except the single quote to spaces
            - Remove single quotes
            - Split on spaces to get words
            - If word is valid, put into resultant set
        Note:  to save from making a copy of the string, pass it in as the
        only element of a list.
 
        If you wish to handle non-ASCII Unicode punctuation characters,
        construct your own GetWords.remove translation mapping before
        calling this function.
        '''
        if isinstance(mystring, list):
            mystring = mystring[0]
        if not hasattr(GetWords, "remove"):
            # Construct a set of characters to change to spaces
            u = string.punctuation.replace("'", "") + string.digits
            replace = " "*len(u)
            GetWords.remove = str.maketrans(u, replace)
        # Change punctuation to space characters.  This makes sure
        # contractions like "don't" become "dont".
        s = mystring.lower().translate(GetWords.remove)
        s = s.replace("'", "")  # Remove single quotes
        # Split to get words
        words = set()
        for word in set(s.split()):
            if IsValidWord(word):
                words.add(word)
        return words
    def GetAnagrams(mystring, sortlist=True):
        '''Return a list strings such that each element is a string of
        space-separated anagrams of the words in mystring.  If sortlist is
        True, the list is sorted by the number of words with the 2-word
        elements first.
        '''
        C = collections.Counter
        # The following dictionary uses str(Counter_instance) as key and
        # the value is a set of words with that Counter_instance, meaning
        # each word in the set is an anagram of the others.
        di = collections.defaultdict(set)
        if isinstance(mystring, list):
            mystring = mystring[0]
        # Build data structure
        words = GetWords([mystring])
        for word in words:
            counter = str(C(sorted(list(word))))
            di[counter].add(word)
        # Remove the items with only one word, as they have no
        # anagrams
        rm = []
        for i in di:
            if len(di[i]) == 1:
                rm.append(i)
        for i in rm:
            del di[i]
        if sortlist:    # Sort by number of words
            # Decorate with number of words for sorting
            p = [(len(i), i) for i in di.values()]
            p = list(sorted(p))
            o = [' '.join(b) for a, b in sorted(p)]
        else:
            # Get a list of space-separated anagrams
            o = [' '.join(i) for i in di.values()]
        return o

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    strings = []
    for file in files:
        strings.append(open(file).read())
    for i in GetAnagrams(' '.join(strings)):
        print(i)

