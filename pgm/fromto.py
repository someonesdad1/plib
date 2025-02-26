"""
Using regular expressions, print the lines in a file from the line that
matches regex1 to the line that matches regex2.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print the lines in files from regex1 to regex2
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import re
if 1:  # Custom imports
    from wrap import dedent


def Usage(status=1):
    print(
        dedent(f"""
    {sys.argv[0]} re1 re2 [file1 [file2...]]
      Print lines from the indicated files that match beginning at re1
      and ending at re2.  Use "-" for stdin.
    """)
    )
    exit(status)


if __name__ == "__main__":
    d = {}
    if len(sys.argv[1:]) < 3:
        Usage()
    re1, re2 = re.compile(sys.argv[1]), re.compile(sys.argv[2])
    for file in sys.argv[3:]:
        stream = sys.stdin if file == "-" else open(file)
        show = False
        for line in [i.rstrip("\n") for i in stream.readlines()]:
            if re1.search(line):
                show = True
                print(line)
                continue
            elif re2.match(line):
                if show:
                    print(line)
                break
            elif show:
                print(line)
