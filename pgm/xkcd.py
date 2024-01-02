'''
Show favorite xkcd links
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Show favorite xkcd links
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        data = '''

            131 Clicking fans
            135 Substitute (velociraptors, matter of life & death)
            356 Nerd sniping
            409 Double comic
            414 Mistranslations of the Kama Sutra
            418 Health plot with bacon event
            530 Bizarre solutions to getting in, forgetting doorbell
            552 Correlation & causation
            572 Scavenger hunt
            601 AI analyzes love
            674 Natural parenting
            685 G-spot
            712 Single ladies
            735 Pretending the floor is lava
            788 Grand Theft Auto, Emily Dickinson edition
            793 Obnoxious physicists:  why does your field need a journal?
            841 Audiophiles
            896 Marie Curie, Noether
            962 Can't focus on calculus
            967 Amber waves of grain --> particles when observed
            972 Tongue awareness month (perfect for Sa)
            974 Why software development is problematic
            979 One link when googling an error
            999 Cougars:  good parenting
            1077 Home organization:  just give up
            1082 Erotic geology
            1094 Interview:  black hat says "opening has been filled"
            1125 Hubble's car
            1235 Quietly settled some big issues with cameras
            1356 Fan & kite
            1356 Kerbal & orbital mechanics
            1381 Proof in a margin (parodies Fermat's comment)
            1462 Limitations of blind trials
            1542 National scheduling conflict championships canceled
            1574 Trouble for science
            1594 Human subjects
            1597 Git
            1649 Fluid flows
            1680 Black hole bringing room together
            1693 Oxidizing car
            1713 50 ccs
            1726 Unicode ==> trying to steer a river with signs
            1728 You're move cron
            1750 Game player's life goals
            1770 UI change == getting old
            1985 Pure math meteorologist
            1994 How well something works after I've fixed it

        '''
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] keyword
          Show xkcd links with keyword.  Show all with none.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    def GetDict():
        di = {}
        for line in data.split("\n"):
            line = line.strip()
            if not line:
                continue
            f = line.split(" ", maxsplit=1)
            di[int(f[0])] = f[1]
        return di
    def PrintItem(i):
        s = f"{p}{i!s}"
        print(f"{s:21s} {di[i]}")
    def PrintResults(keyword):
        breakpoint() #xx

if __name__ == "__main__":
    d = {}      # Options dictionary
    di = GetDict()
    keywords = ParseCommandLine(d)
    results, p = [], "https://xkcd.com/"
    if keywords:
        for keyword in keywords:
            for i in di:
                if keyword.lower() in di[i].lower():
                    PrintItem(i)
    else:
        for i in di:
            PrintItem(i)
