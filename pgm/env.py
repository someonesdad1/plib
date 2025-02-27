"""
Print environment variables
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Dump environment variables
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options] [var1 [var2...]]
      Print environment variables to stdout.  If var1, ... are given on
      the command line, only dump those variables.  The output won't
      match the output of the shell's 'set' or 'printenv' commands
      because the environment variables are all uppercase in python.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-h":
            Usage(d, status=0)
    return args


def Dump(key):
    if key in os.environ:
        value = os.environ[key]
        use_repr = False
        for i in (
            " ",
            "\\",
            ";",
        ):
            if i in value:
                use_repr = True
                break
        if use_repr:
            s = repr(os.environ[key])
        else:
            s = str(os.environ[key])
        s = s.replace("\\\\", "\\")
        print(key, "=", s, sep="")
    else:
        print(f"'{key}' is not an environment variable", file=sys.stderr)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    args = args if args else sorted(os.environ.keys(), key=str.lower)
    for i in args:
        Dump(i)
