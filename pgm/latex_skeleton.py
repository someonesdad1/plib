"""
Create skeleton of LaTeX project
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Create skeleton of LaTeX project
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] project_name
          Create a skeleton of a LaTeX project.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(status=0)
        if len(args) != 1:
            Usage()
        return args[0]


if 1:  # Core functionality

    def WriteFile(text, filename):
        with open(filename, "w") as f:
            f.write(text)

    def MakeProject(project_name):
        pn = project_name
        # makefile to produce t.pdf file
        t = dedent(f"""
        # vim: noet
        p = pdflatex -halt-on-error
        
        a: {pn}.tex
        	tp {pn}.tex >t.tex
        	$p t.tex
        clean:
        	    rm -f *.aux *.idx *.log *.toc *.nav *.out *.snm
        realclean: clean
        	    rm -f t.pdf
        """)
        WriteFile(t, "makefile")
        # Main project file
        t = dedent(r"""
        \documentclass[letterpaper]{book}
        \usepackage[hmargin={10mm, 10mm},
                    vmargin={20mm, 15mm},
                    ]{geometry}
        """)
        t += dedent(rf"""

        \usepackage{{{pn}sty}}

        """)
        t += dedent(r"""
        \begin{document}

        \begin{thebibliography}{99}
            \bibitem{tmbr1}
                G. Lautard,
                \textit{Machinist's Bedside Reader},
                volume 1,
                \href{http://www.lautard.com/}{http://www.lautard.com/}.
        \end{thebibliography}

        \end{document}
        """)
        WriteFile(t, f"{pn}.tex")


if __name__ == "__main__":
    d = {}  # Options dictionary
    project_name = ParseCommandLine(d)
    MakeProject(project_name)
