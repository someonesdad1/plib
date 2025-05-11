'''
Generate short hash strings for files
'''
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Generate short hash strings for files
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
    # Standard imports
    import getopt
    import hashlib
    import os
    from pathlib import Path as P
    import sys
    # Custom imports
    from wrap import wrap, dedent
    from dpstr import RemoveWhitespace
    # Global variables
    ii = isinstance
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Generate short hash strings for files.  The SHA-1 hash is used by default
          (same as git).  These hashes are intended to identify files, not provide
          cryptographic security (except for -t).
        Options:
            -1      Use MD5 hash
            -h      Print a manpage
            -n n    Print out n characters of the hash [{d["-n"]}]
            -t      Text hash:  remove whitespace and calculate SHA-256 hash
        '''))
        exit(status)
    def Manpage():
        print(dedent(f'''

        The -t option is intended to be used to identify a chunk of text and be
        cryptographically secure.  It works by reading in the text, removing all
        whitespace, converting to a UTF-8 encoded bytestring, and calculating the hash.  

        I use this in documents with a set of questions that only I would know the
        answers to.  Examples:

            - 3177 password
            - Garbage can password
            - Ted's password
            - Gray female cat
            - etc.

        These questions are ones that I will know the answers to immediately, at least
        until I become senile.  For example, the first question is a phone extension I
        had at one company for 25 years and I will never forget the password I used for
        that phone account.  The next password is associated with a memorable humorous
        event with a grandson.  A friend Ted in the 1980's told me the password he used
        and explained its derivation:  a famous large company's name was formed by his
        initials and everyone our age would recognize this company's famous advertising
        slogan; he used the first letters of that slogan's words.  A number of these
        questions will produce a "salt" in the overall hash that helps against anyone
        else forging the same hash output with different text.  Of course, the core
        assumption here is that SHA-256 remains a secure hash.

        Comment:  the protected text is e.g. printed in a document with the questions
        following and the resulting hash.  An attacker could easily forge a new document
        with suitable question answers by substituting the new hash value and printing
        it out; there's no easy defense against this except, if it's important enough, I
        can register the notarized original document with a lawyer or other professional
        and use this as legal evidence that would be hard to refute if needed to show
        that the copy was a forgery because of the registered date of my earlier
        document.

        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-1"] = False     # Use MD5
        d["-n"] = 8         # Number of hash digits
        d["-t"] = False     # Text hash
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "1hn:t")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("1t"):
                d[o] = not d[o]
            elif o in ("-n",):
                d[o] = max(abs(int(a)), 2)
            elif o in ("-h",):
                Manpage()
        return args
if 1:  # Core functionality
    def TextHash(file):
        'Return the hex form of the SHA512 hash of a text file with all whitespace removed'
        h = hashlib.sha512()
        h = hashlib.sha256()
        text = RemoveWhitespace(open(file, "r").read())
        h.update(text.encode())
        print(f"{h.hexdigest()} {file}")
    def ProcessFile(file):
        if d["-t"]:
            TextHash(file)
            return
        hash = hashlib.md5 if d["-1"] else hashlib.sha1
        h = hash()
        h.update(open(file, "rb").read())
        w = d["-n"]
        s = h.hexdigest()[:w].rstrip()
        w = min(w, len(s))
        print(f"{s:{w}s} {file}")
if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
