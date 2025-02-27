"""
Make a project periodically:  execute 'make -q'; if it returns nonzero,
execute 'make'.  All command line arguments are passed to make.
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
    # Execute make periodically to keep a project updated
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import os
    import sys
    import time
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] target1 [target2 ...]
      Make the indicated targets on the command line using make(1).  Delay,
      then remake the targets.  The intended use case is e.g. making an HTML
      file that is updated in your browser when the source code is.  Except
      for -E and -T. the command line targets are passed to make.
    
      To execute the default target, call '{sys.argv[0]} ""'.
    Options:
      -E    Don't exit on a make error [{d["-E"]}]
      -T t  Delay t seconds before launching another make [{d["-T"]} s]
    """)
    )
    exit(status)


def Loc(item, seq):
    try:
        return seq.index(item)
    except ValueError:
        return -1


def ParseCommandLine(d):
    d["-E"] = False  # Don't exit on make error
    d["-T"] = 1  # Sleep time in s
    targets = sys.argv[1:]
    if not targets:
        Usage(d)
    # Find our options on the command line; the remainder will be passed
    # to make.
    loc = Loc("-E", targets)
    if loc != -1:
        d["-E"] = True
        del targets[loc]
    loc = Loc("-T", targets)
    if loc != -1:
        try:
            tm = targets[loc + 1]
            d["-T"] = float(tm)
            if d["-T"] <= 0:
                Error('d["-T"] option must be > 0')
        except ValueError:
            Error("'{}' is not a float".format(tm))
        except IndexError:
            Error("Argument missing for -T option")
        del targets[loc + 1]
        del targets[loc]
    if not targets:
        Usage(d)
    return targets


def Make(targets, d):
    make = "/usr/bin/make"
    make_cmd = "{} {{}} {}".format(make, " ".join(targets))
    while True:
        try:
            not_up_to_date = os.system(make_cmd.format("-q"))
            if not_up_to_date:
                mc = make_cmd.format("")
                status = os.system(mc)
                if status and not d["-E"]:
                    raise Exception("make returned nonzero")
        except Exception as e:
            print(f"Error in {sys.argv[0]}:  {e}", file=sys.stderr)
            print(f"Make command was '{mc}'", file=sys.stderr)
            exit(1)
        time.sleep(d["-T"])


if __name__ == "__main__":
    d = {}  # Options dictionary
    targets = ParseCommandLine(d)
    Make(targets, d)
