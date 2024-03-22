'''

Script to generate hard-to-crack passwords

    Method 1:  uses secrets module and a list of words to randomly select words from the list.  You
    specify the number of words, the list of words, and the number of lines to generate.


Method 2
    - Script to ask a bunch of questions, concatenate your responses, and deliver a desired hash of
      the response data.
    - The script will number and output the questions along with the hashed answer.
    - With a good set of questions, it is unlikely anyone could crack things, especially if the
      answers have numerous characters in them.

Example of method 2:
    - Here are a set of questions with answers in double quotes:
        - Name Donald Duck's nephews
            - "Huey Dewey Louie"
        - Name of the duck that the cat loved to wipe its tail under
            - "Daddles"
        - So-and-so's phone number
            - "916-456-7890"
    - The answer strings are concatenated to get the string to be hashed:
        - "Huey Dewey LouieDaddles916-456-7890"
    - The command line options to the program are used to transform the input string to make it
      easier to tolerate input differences later
        - -i is used to ignore case
        - -p is used to remove punctuation
        - -w is used to remove whitespace
    - If all these options were used, the string to be hashed is 
        - "hueydeweylouiedaddles9164567890"
        - Even if you knew the string had 21 letters and 10 digits, you'd still be faced with
          26**21*10**10 = 5e39 combinations that must be tried in a brute-force attack.
    - A bitcoin mining website in Nov 2023 gave a $3.2k Bitmain AntMiner S19 Pro's hash speed at
      110 Th/s or 1e14 Hz.  Suppose you could afford a million of these machines ($3e9), giving you
      a brute force checking rate of 1e20 Hz.  You'd need 1e39/1e20 = 1e19 s to check all the
      possibilities, which larger than 4e17 s, the age of the universe.

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
        # Questions to help generate a password
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import random
        import secrets
        import sys
    if 1:   # Custom imports
        from wrap import dedent
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Global variables as attributes to this instance
        g.words = (
            P("/words/words.ef.3000"),
            P("/words/words.beale.2of12inf"),
            P("/words/words.ngsl.experimental"),
            P("/words/words.univ"),
        )
        g.wordlist = None
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] N [m]
          If only N is given, you will be asked for N questions followed by their answers.  The 
          password is the concatenation of the answers.
 
          If N and m are given, N words are randomly selected from a wordlist and concatenated with
          spaces between them.  m lines like this are generated.  The output is random and not
          repeatable unless you use the -s option.
        Options:
            -0      Simple wordlist /words/words.ef.3000 (3000 words).  This is the default
                    and will provide common words.
            -1      Moderately-sized wordlist /words/words.ngsl.experimental (16378 words)
            -2      Sizeable wordlist /words/words.beale.2of12inf (81882 words).  This is an
                    excellent list of words from Alan Beale.
            -3      Complex wordlist /words/words.univ (302618 words).  This can generate
                    complicated words that may be unfamiliar and hard to remember.
            -h      Print a manpage
            -i      Ignore case of words
            -l n    Limit words to n letters
            -p      Remove punctuation
            -s sd   Define seed to use repeatable pseudorandom generator
            -w      Remove whitespace
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-l"] = None      # Limit words to this length
        d["-s"] = None      # Random number seed; implies pseudorandom number generator
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0123ad:hl:s:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o[1] in list("0123"):
                g.wordlist = int(o[1])
            elif o == "-l":
                try:
                    d[o] = int(a)
                    if d[o] < 1:
                        raise ValueError()
                except ValueError:
                    Error("-l option's argument must be an integer > 0")
            elif o == "-h":
                Usage(status=0)
            elif o in ("-s",):
                d["-s"] = a
        if g.wordlist is None:
            g.wordlist = 0
        return args
if 1:   # Core functionality
    def Method1(*args):
        N, m = [int(i) for i in args]
        if N < 1:
            Error("N must be an integer > 0")
        if m < 1:
            Error("m must be an integer > 0")
        file = g.words[g.wordlist]
        assert file.exists()
        with open(file) as f:
            words = [word.strip() for word in f]
        if d["-l"]:
            # Keep words with d["-l"] letters or less
            words = [i for i in words if len(i) <= d["-l"]]
        if d["-s"] is None:
            # Random selection, cannot be repeated
            for i in range(m):
                password = ' '.join(secrets.choice(words) for i in range(N))
                print(password)
        else:
            # Pseudorandom number generator, same output for same seed
            random.seed(d["-s"])
            n = len(words)
            for linenum in range(m):
                o = []
                for i in range(N):
                    k = random.randint(0, n - 1)
                    o.append(words[k])
                print(' '.join(o))
    def Method2(args):
        pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if len(args) == 1:
        Method2(*args)
    elif len(args) == 2:
        Method1(*args)
    else:
        Usage()
