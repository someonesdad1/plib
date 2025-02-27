"""

Module to get the text content of the mathematical equations in an Open
Document file.

---------------------------------------------------------------------------

This script is intended to parse the content.xml file that came from
unzipping the AnalyticGeometry.odt document (which resides in this
directory).  The goal is to print out all the math equations (in OO's
dialect) in the order they are encountered in the document.  This will be
my backup method of converting AG to LaTeX in case Henrik is not able to do
the conversion.

'Object 1437' is a known math equation.

Plan
    - Read the top level contents.xml file that has been converted to
      multiple line format by vim.
        - Find the lines that contain "Object d" where d is an integer.
          These are the possible directories in '.' that contain math
          equations (not all of them will).
    - Open the Object\ d/content.xml file for each object.  Look for XML
      elements of the form '<annotation encoding = "StarMath
      5.0".*</annotation>'.  This contains the equation's text after
      stripping off the beginning '<annotation encoding = "StarMath
      5.0"' and the trailing '</annotation>'
    - For each equation
        - Remove 'align.' from beginning
        - Change e.g. %theta to \theta and %THETA to \Theta
        - Change +- to \pm and -+ to \mp
        - Change '`=`' and '`=' to '='
    - Print the resulting lines out
    - Once this works, do it all from the zipped .odt file

"""

if 1:  # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Module to get the text content of the mathematical equations in an Open
        # Document file.
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    # Standard imports
    if 1:
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
        from zipfile import ZipFile
    # Custom imports
    if 1:
        from wrap import dedent
        from color import Color, TRM as t

        if 0:
            import debug

            debug.SetDebugger()
    # Global variables
    if 1:
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.docname = t("grnl")
        t.hyphens = t("yell")
        t.objname = t("ornl")
        t.noeqns = t("magl")
if 1:  # Core functionality

    def GetObjects(file):
        """Return a list of the object directories we'll need to search.  These
        are the objects as they are encountered in the document.

        The assumption is that file is the unmodified content.xml file from an
        OO Writer document.  It contains two lines and the second line is
        searched with a regular expression.  file can be a filename or stream.
        """
        r = re.compile(r"(Object \d+)")
        # Get the XML data
        if ii(file, str):  # It's a file name
            data = open(file).read()
        else:  # It's a stream
            data = file.read()
        # Convert it to a string
        data = data.decode()
        # Get the matches from the file
        o = re.findall(r"Object \d+", data)
        # Keep only one copy of each Object
        objects = []
        found = set()
        for i in o:
            if i not in found:
                found.add(i)
                objects.append(i)
        return objects

    def GetEquation(file, zf=None):
        """file is the name of the 'Object d/content.xml' where d is an
        integer.  Read the data, searching for the 'StarMath 5.0' regular
        expression.  If zf is None, file is a regular file; otherwise, it's in
        a ZipFile instance.
        """
        a = "annotation"
        if zf:
            stream = zf.open(file)
        else:
            stream = open(file, "rb")
        data = stream.read().decode()
        look_for = '<annotation encoding="StarMath 5.0">'
        loc = data.find(look_for)
        if loc == -1:
            return None
        data = data[loc + len(look_for) :]
        look_for = "</annotation>"
        loc = data.find(look_for)
        if loc == -1:
            return None
        eq = data[0:loc]
        return eq

    def FixUnicode(eq):
        """Standard LaTeX doesn't work with Unicode very well because it was written
        before Unicode appeared.  This function, however, will substitute strings
        that will get the same result inside the math environment.

        NOTE:  You'll probably want to modify this mapping to fit your needs, as I only
        put in enough to get the results I wanted on the document I was processing.
        """
        di = {
            "Γ": r" \Gamma ",
            "Δ": r" \Delta ",
            "α": r" \alpha ",
            "β": r" \beta ",
            "γ": r" \gamma ",
            "θ": r" \theta ",
            "μ": r" \mu ",
            "π": r" \pi ",
            "ψ": r" \psi ",
            "ϕ": r" \phi ",
            "‡": r" \ddag ",
            "∈": r" \in ",
            "∉": r" \notin ",
            "∩": r" \cap ",
            "∪": r" \cup ",
            "≜": r" \stackrel{\text{def}}{=} ",
            "≤": r" \le ",
            "≥": r" \ge ",
            "∞": r" \infty ",
            "ℕ": r" \textbb{N} ",
        }
        for i in di:
            eq = eq.replace(i, di[i])
        return eq

    def AdjustEquation(eq):
        "Make a number of adjustments to make it easier to convert to LaTeX"
        greek = """alpha beta chi delta epsilon eta gamma iota kappa lambda mu nu
                omega phi pi psi rho sigma tau theta upsilon xi zeta""".split()
        # Change Greek letters to LaTeX form
        for i in greek:
            j = f"%{i}"
            if j in eq:
                eq = eq.replace(j, rf"\{i}")
            if j.upper() in eq:
                eq = eq.replace(j.upper(), rf"\{i.capitalize()}")
        # Special function conversion
        trig = "sin cos tan csc sec cot log ln".split()
        for i in trig:
            j = f" {i} "
            if j in eq:
                eq = eq.replace(j.strip(), rf"\{j.strip()} ")
        # Fix equal sign spacing
        eq = eq.replace("`=`", "=")  # Remove "= spacing hack"
        eq = eq.replace("`=", "=")  # Remove "= spacing hack"
        eq = eq.replace("`", "")  # Remove backticks
        # +- and -+
        eq = eq.replace("+-", r"\pm ")
        eq = eq.replace("-+", r"\mp ")
        # Make it easy to find where \frac is needed
        eq = eq.replace("over", "__OVER__")  # Makes it easy to see & search for
        # < and >
        eq = eq.replace("&lt;", " < ")
        eq = eq.replace("&gt;", " > ")
        eq = eq.replace("&le;", r" \le ")
        eq = eq.replace("&ge;", r" \ge ")
        eq = FixUnicode(eq)
        return eq


if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Help():
        print(
            dedent(
                rf"""
        The script's purpose
        --------------------

        This script is used to print the text in equation objects in Open Document files.
        
        My primary use case for this script is to help me convert Open Document files to LaTeX.
        The text conversion is straightforward (save the OO document as a .txt file with UTF-8
        encoding), but the math syntax needs to be converted from OO's syntax to LaTeX syntax.  The
        default behavior of the script is to just print out each equation's text content.  For
        conversion to LaTeX, use the -a option, which means to adjust the equations' text.  Here,
        "adjust" means make some conversions to LaTeX that are easy enough to make without having
        to write a full parser.  For example, if the OO math text contains the string "+-", this is
        converted to \pm, which is LaTeX's equivalent.

        This script's input files must be Open Document format file(s).  In addition, they must use
        the "StarMath 5.0" annotation in the XML.  I have tested this script on files produced by
        Open Office version 4.1.6.  I tested it on documents from Writer (word processor), Calc
        (spreadsheet), Impress (presentations), and Draw (drawing program).  I'll call these types
        of documents OO documents.

        I wrote this script to convert a reference document I wrote a few decades ago to LaTeX.
        This document contained 1113 equations (and about 500 other OLE objects) and the task would
        have been a daunting amount of labor to type the new equations into a *.tex file from
        scratch.  It was still a lot of work, but not as much as doing it from scratch because OO's
        math syntax has similarities to LaTeX -- and once you're fluent in both it's pretty easy to
        translate the equation text in your text editor.  This script did a lot of the work.

        NOTE:  It's likely you'll have to hack on this script to get it to work on your own files.
        FixUnicode() is probably one function you'll want to look at. 

        Algorithm
        ---------

        While I haven't read the Open Document specification, I long ago did a hex dump of an OO
        file and noted that the first two characters were PK, meaning it used zip compression.
        Unzipping the file, you'll see a standard structure.  The only things that concern us here
        are the top-level content.xml file and each ObjectX directory, where X is an integer.

        If you peruse https://en.wikipedia.org/wiki/OpenDocument_technical_specification, it states
        that formulas (i.e., equations) are represented as MathML.  If you read
        https://en.wikipedia.org/wiki/MathML#Example_and_comparison_to_other_formats, you'll see
        how the <annotation> XML tag can be used to utilize other non-XML equation formats, such as
        Star Office 5.0.  

        This python script is purely heuristic, based on the text I found in the OO documents I
        unzipped.  Thus, it may not work for you -- but it shouldn't be too hard to look at the
        differences/exceptions and figure out how to get things to work.

        Here are the steps:

            - Open the document as a zipfile using zipfile.ZipFile
            - Get a list of the object directories in the zipfile.  These match the regexp
              r"Object\d+"; keep only one copy of this name.  Note these are in the order they are
              encountered in the OO file.  I'll call these ObjectX.
            - For each of the ObjectX directories, read the content.xml file in that directory.
                - If there's a "StarMath 5.0" equation object, get its text.
            - Return a list of (a, b) objects where a is the ObjectX string and b is the equation's
              text.

        If you run this file as a script, the above list of objects is printed out in a
        easy-to-consume form with ANSI color coding to show the file name and ObjectX string.

        Finding the ObjectX directories used a simple regular expression; finding the equation's
        text used simple string manipulations.

        Dependencies
        ------------

        If you want to run this script, it is dependent on a few files from
        https://github.com/someonesdad1/plib.   These are in the section near the top of the file
        labeled '# Custom imports'.  If you don't want to use these features, they can be removed:

            - In the global variables section, add the line 'class t: pass' after the line with '#
              Color'.
            - Remove 'dedent' from print statements (you'll want to manually adjust the argument
              string to fit your screen).
            - Under the '# Color' lines, change the t("...") function calls to be empty strings.
            - Change lines with t.print() to print().
            - Change the line 'lines = GetLines(file)' to 'open(file).read().split("\n")' if file
              is a string or 'file.read().split("\n")' if file is a stream.

        Notes
        -----

        In 2014 I contacted Henrik Just, the author of Writer2LaTeX.  Henrik used my reference
        document as a test case for his tool and commented that it helped him find a number of
        errors.  I wasn't able to use it to get LaTeX output at the time.  In Sep 2022, I decided
        to revisit this problem again, as I was put out with Open Office's poor equation formatting
        and problems that made me spend far more time fiddling with formatting than editing the
        content.  Since I've long been a believer in separating content from presentation (e.g.,
        the MVC pattern), I've always wanted the document in LaTeX, but was gun-shy of the amount
        of manual work it would take for conversion.  

        It turns out the process wasn't as daunting as I thought it would be.  I used the following
        process

            - Save the file as a UTF-8-encoded text file to get the document's text.
            - Using a text editor, format this text into paragraphs suitable for LaTeX.

        """.rstrip()
            )
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] odfile1 [odfile2...]
            Print out the equations' text in the Open Document files.
        Options:
            -a      Adjust the text for conversion to LaTeX
            -h      Details on how the script works
            -r      Print repr() form of equations rather than str()
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Adjust the equations for LaTeX
        d["-h"] = False  # Print detailed help
        d["-r"] = False  # Use repr() instead of str() for equations
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "ahr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ahr"):
                d[o] = not d[o]
        if d["-h"]:
            Help()
        return files

    def PrintDocumentObjects(document):
        try:
            hyphens = "-" * (W - 2)
            with ZipFile(document) as zf:
                o = GetObjects(zf.open("content.xml"))
                equations = []
                # Get the equations' text
                for i in o:
                    obj = i.replace(" ", "")
                    file = f"{i}/content.xml"
                    eq = GetEquation(file, zf)
                    if eq:
                        equations.append((i, eq))
            # Print results
            t.print(f"{t.docname}{document}")
            if not equations:
                t.print(f"    {t.noeqns}No equations")
            else:
                for object, eq in equations:
                    if d["-a"]:
                        eq = AdjustEquation(eq)
                    t.print(f"{t.objname}{obj}")
                    print()
                    if d["-r"]:
                        print(f"{eq!r}")
                    else:
                        print(f"{eq!s}")
                    # Print line of hyphens
                    if d["-a"]:
                        # Add '%' so it's a LaTeX comment
                        print(f"%{hyphens}")
                    else:
                        print(f"{hyphens}")
        except Exception as e:
            print(f"{document}:  Error:  {e}", file=sys.stderr)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        PrintDocumentObjects(file)

if 0:  # Generate a list of Objects in document order
    o = GetObjects("content.xml")
    # print(f"Found {len(o)} candidates")
    for i in o:
        obj = i.replace(" ", "")
        eq = GetEquation(i.lower())
        if eq:
            print(obj)
            print()
            print(eq)
            print("%" + "-" * 50)
    print(eq)
