"""
TODO
    - This is a candidate to move to /plib
        - Generalize the functions with keyword arguments
        - GetWords is a routine that belongs in a library like dpstr.py
    - Write a test routine for each function

Finding anagrams
    The primary method is GetAnagrams(), which returns a list of lines with
    space-separated words that are anagrams.

    The algorithm is to use collections.Counter to characterize the letters
    in a word and find all words that produce the same Counter object;
    these are anagrams.

Other algorithm ideas

    https://stackoverflow.com/questions/7896694/how-to-find-find-anagrams-among-words-which-are-given-in-a-file
    https://stackoverflow.com/questions/12477339/finding-anagrams-for-a-given-word

- Prime integers
    - Assign each letter a prime number and compute the product for each
      string; if they match, they are anagrams.  For spaces and
      punctuation, you can use 1 to ignore them.  The method is based on
      the fundamental theorem of arithmetic that all non-prime numbers have
      unique factorizations.
- Multisets
    - Convert the strings to multisets; if the multisets are equal, the
      strings are anagrams.  Note the collections.Counter object is similar
      to a multiset.
- Sorted strings
    - Sort the letters of the strings; if they match, they are an anagram.
    - Sort the letters of the strings.  Use the sorted letters as a key to
      a dict with a list of all other words with the same sorted letters.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # GetAnagrams() and other functions handy to getting anagrams of
        # words from strings
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import collections
        import string
if 1:  # Core functionality

    def IsValidWord(word):
        """Return True if word is considered a valid word.  Here, valid
        means it only contains ASCII letters.

        If you want to have letters other than ASCII, construct a custom
        IsValidWord.rm_invalid translation mapping before calling
        GetWords().

        The algorithm is to use the string translation table to remove all
        non-ASCII characters.  The word is considered valid if the
        resulting string length is zero.
        """
        if not hasattr(IsValidWord, "rm_invalid"):
            lc = string.ascii_lowercase
            IsValidWord.rm_invalid = "".maketrans(lc, " " * len(lc))
        s = word.lower().translate(IsValidWord.rm_invalid).replace(" ", "")
        return not bool(len(s))

    def GetWords(mystring):
        """Given a string, return a set of the words in this string.  The
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
        """
        if isinstance(mystring, list):
            mystring = mystring[0]
        if not hasattr(GetWords, "remove"):
            # Construct a set of characters to change to spaces
            u = string.punctuation.replace("'", "") + string.digits
            replace = " " * len(u)
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
        """Return a list strings such that each element is a string of
        space-separated anagrams of the words in mystring.  If sortlist is
        True, the list is sorted by the number of words with the 2-word
        elements first.
        """
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
        if sortlist:  # Sort by number of words
            # Decorate with number of words for sorting
            p = [(len(i), i) for i in di.values()]
            p = list(sorted(p))
            o = [" ".join(b) for a, b in sorted(p)]
        else:
            # Get a list of space-separated anagrams
            o = [" ".join(i) for i in di.values()]
        return o


if __name__ == "__main__":
    from lwtest import run, Assert

    def Test_IsValidWord():
        Assert(IsValidWord(""))
        Assert(IsValidWord("Assert"))
        Assert(not IsValidWord("\n"))
        Assert(not IsValidWord("Ass∞ert"))
        Assert(not IsValidWord("Ass-ert"))
        Assert(not IsValidWord("Ass?ert"))
        Assert(not IsValidWord("Ass.ert"))

    def Test_GetWords():
        l = "If you wish to handle non-ASCII Unicode punctuation characters,"
        e = "if you wish to handle non ASCII Unicode punctuation characters"
        got = GetWords(l)
        expected = set(e.lower().split())
        Assert(got == expected)

    def Test_GetAnagrams():
        s = "Able was I ere I saw Elba."
        a = GetAnagrams(s)
        # Note the set order is not constant, so we have to compare sets of
        # words.
        expected1 = list(sorted(["saw", "was"]))
        expected2 = list(sorted(["able", "elba"]))
        got1 = list(sorted(a[0].split()))
        got2 = list(sorted(a[1].split()))
        if expected1 == got1:
            Assert(got2 == expected2)
        else:
            Assert(got1 == expected2)
            Assert(got2 == expected1)

    exit(run(globals(), halt=True)[0])
