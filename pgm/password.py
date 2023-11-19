'''

- Script to ask a bunch of questions, concatenate your responses,
  and deliver a desired hash of the response data.
- The script will number and output the questions along with the
  hashed answer.
- With a good set of questions, it is unlikely anyone could crack
  things, especially if the answers have numerous characters in
  them.

Example:
    - Here are a set of questions with answers in double quotes:
        - Name Donald Duck's nephews
            - "Huey Dewey Louie"
        - Name of the duck that the cat loved to wipe its tail under
            - "Daddles"
        - So-and-so's phone number
            - "916-456-7890"
    - The answer strings are concatentated to get the string to be hashed:
        - "Huey Dewey LouieDaddles916-456-7890"
    - The command line options to the program are used to transform the
      input string to make it easier to tolerate input differences later
        - -i is used to ignore case
        - -p is used to remove punctuation
        - -w is used to remove whitespace
    - If all these options were used, the string to be hashed is 
        - "hueydeweylouiedaddles9164567890"
        - Even if you knew the string was 21 letters followed by 10 digits,
          you'd still be faced with 26**21*10**10 = 5e39 combinations that
          must be tried in a brute-force attack.
    - A bitcoin mining website in Nov 2023 gave a $3.2k Bitmain AntMiner
      S19 Pro's hash speed at 110 Th/s or 1e14 Hz.  Suppose you could
      afford a million of these machines ($3e9), giving you a brute force
      checking rate of 1e20 Hz.  You'd need 1e39/1e20 = 1e19 s to check all
      the possibilities, which larger than 4e17 s, the age of the universe.


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
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
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
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
