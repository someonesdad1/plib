'''
Construct a skeleton of a LaTeX project file set.
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
        # Construct a skeleton of a LaTeX project file set
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
        t.title = t("ornl")
        t.mak = t("cynl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] project_name
          Construct a set of files for a LaTeX project.
        Options:
            -h      Print a manpage
            -s      Print to stdout in colored form for visual debugging
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("s"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        if len(args) != 1 and not d["-s"]:
            Usage()
        return args[0] if args else None
if 1:   # Core functionality
    def GenerateFiles(project_name):
        ProjectFile(project_name)
        MainFile(project_name)
        StyleFile(project_name)
        Makefile(project_name)
    def ProjectFile(pn):
        print(dedent(f'''
        '''))
    def MainFile(pn):
        print(dedent(f'''
        '''))
    def StyleFile(pn):
        print(dedent(f'''
        '''))
    def Makefile(pn):
        '''A characteristic of this makefile is that the tp.exe tool is
        used to allow quick commenting out of code when desired.
        '''
        tb = "\t"
        s = dedent(f'''
        # vim: noet
        #   $@      file name of target rule
        #   $^      all dependencies with a space between them
        #   $?      all dependencies newer than target
        #   $<      first dependency

        p = pdflatex -halt-on-error
        o = t   # Name of output file
        .PHONY: $o.pdf

        $o.pdf: {pn}_.tex
        {tb}tp {pn}_.tex > {pn}.tex
        {tb}$p {pn}.tex

        {pn}_.tex: {pn}.tex
        {tb}tp {pn}.tex {pn}_.tex
        clean:
        {tb}rm -f *.aux *.idx *.log *.toc *.nav *.out *.snm $o.tex
        realclean: clean
        {tb}rm -f t.pdf
        ''')
        if d["-s"]:
            t.print(f"{t.title}makefile")
            t.print(f"{t.mak}" + s)
        else:
            print(s, file=open("makefile", "w"))

if __name__ == "__main__":
    d = {}      # Options dictionary
    project_name = ParseCommandLine(d)
    GenerateFiles(project_name)
