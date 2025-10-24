'''

ToDo
    - Use a regex to remove hyperlinks, as these nearly always have misspelled words
    - Add an option to check Usage() and Manpage() functions in python scripts

Spell-checking script
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Spell-checking script
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports & globals
        import getopt
        import os
        import pathlib
        import string
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from asciify import Asciify
        import get
        import url as URL
        from columnize import Columnize
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.letters = set(string.ascii_letters)
        wordlist = {
            # This is used as my personal wordlist for stuff that shows up in my stuff
            # frequently
            "additional": "/words/words.additional",
            0: None,
            1: "/words/words.ngsl.experimental",
            2: "/words/words.beale.2of12inf",
            3: "/words/words.univ",
        }
        default_wordlist = 2
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        wl = "-" + str(default_wordlist)
        # Get names of wordlists
        def P(p):
            return pathlib.Path(p).name
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2 ...]
          Spell check the indicated files by replacing non-letters with space
          characters and tokenizing on whitespace.  Use '-' to read stdin.
          Default wordlist is {wl}.  Case is ignored by default.
        Options:
          -0    No dictionary
          -1    Basic dictionary          {P(wordlist[1])}
          -2    Medium-size dictionary    {P(wordlist[2])}
          -3    Large dictionary          {P(wordlist[3])}
          -a    Apply Asciify() to tokens
          -D    Don't remove digit characters in tokens
          -d f  Use file f as an adjunct dictionary (can have more than one)
          -h    Don't replace hyphen with space
          -i    Don't ignore case of tokens
          -k    Columnize output
          -l    Remove hypertext links before spell checking
          -n    Shows tokens in dictionary
          -s    Only print the number misspelled
          -u    Ignore tokens with non-7-bit characters
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-0"] = False
        d["-1"] = False
        d["-2"] = False
        d["-a"] = False
        d["-D"] = True
        d["-d"] = set()
        d["-h"] = False
        d["-i"] = True
        d["-k"] = False
        d["-l"] = False
        d["-n"] = False
        d["-s"] = False
        d["-u"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0123aDd:hiklnsu")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("0123aDhiklnsu"):
                d[o] = not d[o]
            elif o[1] == "d":
                d[o].add(a)
        if not d["-0"] and not d["-1"] and not d["-2"]:
            d["-" + str(default_wordlist)] = True
        if not args:
            Usage(d)
        return args
if 1:  # Core functionality
    def GetWordlists(d):
        # regex ignores comments; convert to lowercase if d["-i"] is True
        regex = r"^\s*#"
        wl = set()
        if not d["-0"]:
            wl.update(get.GetWords(wordlist["additional"], ignore=[regex]))
            for i in "-1 -2 -3".split():
                n = int(i[1:])
                wl.update(get.GetWords(wordlist[n], ignore=[regex]))
        for file in d["-d"]:
            wl.update(get.GetWords(file, ignore=[regex]))
        if d["-i"]:
            wl = set([i.lower() for i in wl])
        d["words"] = wl
    def BuildTranslate(d):
        '''Construct the d["trans"] dictionary used to translate the strings to be ready to
        tokenize.  This replaces punctuation and whitespace with spaces and deletes digits.
        Also creates the d["letters"] dictionary used to translate string to remove the
        plain ASCII letters.
        '''
        if 1:   # Make d["trans"]
            d["trans"] = u = {}
            for c in string.punctuation:
                u[ord(c)] = " "
            for c in string.whitespace:
                if c == " ":
                    continue
                u[ord(c)] = " "
            if d["-D"]:
                for c in string.digits:
                    u[ord(c)] = None
            if d["-h"]:
                del u[ord("-")]
        if 1:   # Make d["letters"]
            d["letters"] = u = {}
            for c in string.ascii_letters:
                u[ord(c)] = None
    def Non7bit(word):
        'Return False if word has non-7-bit character in it'
        return bool(word.translate(d["letters"]))
    def ProcessFile(file, d):
        s = sys.stdin.read() if file == "-" else open(file).read()
        # If -i option used, convert to lowercase
        if d["-i"]:
            s = s.lower()
        # Remove hypertext links
        if d["-l"]:
            for url in URL.GetURLs(s):
                s = s.replace(url, "")
        # Break the string into tokens
        u = s.translate(d["trans"])
        for word in u.split():
            if d["-u"] and Non7bit(word):     # Don't allow words with non-7-bit characters
                continue
            w = Asciify(word) if d["-a"] else word
            if d["-a"] and w != word:
                W = f"{w} ({word})"
            else:
                W = word
            if w in d["words"]:
                d["correct"].add(W)
            else:
                d["incorrect"].add(W)
    def Report(d):
        words = d["correct"] if d["-n"] else d["incorrect"]
        if d["-k"]:
            for i in Columnize(sorted(words)):
                print(i)
        elif d["-s"]:
            if d["-n"]:
                print(f"{len(words)} correctly spelled")
            else:
                print(f"{len(words)} misspelled")
        else:
            for i in sorted(words):
                print(i)

if 0:   # xx
    d = {"-D":0, "-h":0}
    BuildTranslate(d)
    s = "🟤🟣🟢🟡🟠🔵🔴⚫"
    print(Non7bit(s))
    exit()

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    BuildTranslate(d)
    GetWordlists(d)
    data = []
    d["correct"] = set()
    d["incorrect"] = set()
    for file in files:
        ProcessFile(file, d)
    Report(d)
