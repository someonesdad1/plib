'''
Sends a python dictionary top stdout that maps a file extension to one or
more descriptions.

- Provide a dictionary for file extensions and their type(s)
- Add feature to pgm/ext.py to use this dict to annotate the
    extensions that are printed
- Good links to check
    - https://en.wikipedia.org/wiki/List_of_file_formats
    - https://www.webopedia.com/reference/data-formats-and-file-extensions/
        - https://www.webopedia.com/reference/data-formats-and-file-extensions/
        - https://www.webopedia.com/reference/fileextensionsnumber/
        - https://www.webopedia.com/reference/fileextensionssymbol/
- Others
    - https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89
    - https://www.computerhope.com/issues/ch001789.htm
    - https://en.wikipedia.org/wiki/List_of_file_signatures

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
        # Create an extensions dictionary mapping an extension to a
        # description.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import shutil
        import subprocess
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from util import GetHash
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
        d["-a"] = False
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
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def Mk(python_script):
        if not hasattr(Mk, "data"):
            Mk.data = []
        cmd = [sys.executable, python_script]
        r = subprocess.run(cmd, capture_output=True)
        r.check_returncode()
        lines = [i for i in r.stdout.decode().split("\n") if i]
        for line in lines:
            Mk.data.append(f"    {line}")
    def MakeModule():
        'Construct /plib/extensions.py'
        dest = P("/plib/extensions.py")
        local = P("extensions.py")
        with open(local, "w") as fp:
            fp.write("extensions_dict = {\n")
            for i in Mk.data:
                fp.write(i + "\n")
            fp.write("}\n")
        # Check hash to see if need to overwrite /plib file
        old = GetHash(dest)
        new = GetHash(local)
        if old != new:
            shutil.copyfile(local, dest)

if __name__ == "__main__":
    d = {}      # Options dictionary
    #args = ParseCommandLine(d)
    files = [
        P("webopedia.py"),
        P("wp.py"),
    ]
    for file in files:
        Mk(file)
    MakeModule()
    # Print dict to stdout
    print("extensions_dict = {")
    for i in Mk.data:
        print(i)
    print("}")
