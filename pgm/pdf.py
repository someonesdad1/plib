'''
Helper for Xpdf command line utilities
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
        import subprocess
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        t.err = t("redl")
        t.msg = t("ornl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1.pdf [file2.pdf...]]
          Run pdftotext on each file and outputting the text to file1.txt,
          etc.
        PDF tools from Xpdf version 4.04:
          0 pdftotext     Convert to plain text
          1 pdftops       Convert to PostScript
          2 pdftohtml     Convert to HTML
          3 pdfinfo       Dump info dictionary
          4 pdffonts      List fonts used
          5 pdfdetach     List or extract attachments
          6 pdftoppm      Convert to PPM/PGM/PBM bitmaps
          7 pdftopng      Convert to a series of PNG image files
          8 pdfimages     Extracts images
        Options
          -t n      Selection tool number n (0 is default)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-t"] = 0         # Tool number to run
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (0 <= d["-d"] <= 8):
                        raise ValueError()
                except ValueError:
                    msg = "-t option's argument must be an integer between 0 and 8"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def ToText(*files):
        for file in files:
            pdf = P(file)
            txt = P(pdf.stem + ".txt")
            cmd = ["pdftotext", 
                   "-enc UTF-8",
                   str(pdf),
                   str(txt)
                  ]
            s = ' '.join(cmd)
            r = subprocess.run(s, shell=True, capture_output=True)
            if r.returncode:
                t.print(f"{t.err}{s!r} failed:", file=sys.stderr)
                t.print(f"  {t.msg}{r.stderr.strip().decode()!r}", file=sys.stderr)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if d["-t"] == 0:
        ToText(*files)
