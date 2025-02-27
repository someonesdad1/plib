"""
Print out valid C/C++ symbols in files
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print out valid C/C++ symbols in source files
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import sys
    import re

    # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t

    # Global variables
    ii = isinstance

    class g:
        pass

    g.symbols = {}
    nl = "\n"
    # Regular expressions
    g.valid_symbol = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
    g.c_comment = re.compile(r"/\*.*?\*/", re.S)
    g.cpp_comment = re.compile(r"//.*?\n", re.S)
    g.string = re.compile(r"\"[^\n]*\"")
    g.punctuation = r"~!@#\$%^&*()-+={}[]:;'<>,.?/|"
    # From Harbison and Steele; ANSI C only.
    c_keywords = (
        "ifdef",
        "ifndef",
        "define",
        "endif",
        "include",
        "auto",
        "break",
        "case",
        "char",
        "const",
        "continue",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extern",
        "float",
        "for",
        "goto",
        "if",
        "int",
        "long",
        "register",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "struct",
        "switch",
        "typedef",
        "union",
        "unsigned",
        "void",
        "volatile",
        "while",
    )
    # From Stroustrup
    cpp_keywords = (
        "ifdef",
        "ifndef",
        "endif",
        "define",
        "include",
        "and",
        "and_eq",
        "asm",
        "auto",
        "bitand",
        "bitor",
        "bool",
        "break",
        "case",
        "catch",
        "char",
        "class",
        "compl",
        "const",
        "const_cast",
        "continue",
        "default",
        "delete",
        "do",
        "double",
        "dynamic_cast",
        "else",
        "enum",
        "explicit",
        "export",
        "extern",
        "false",
        "float",
        "for",
        "friend",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "mutable",
        "namespace",
        "new",
        "not",
        "not_eq",
        "operator",
        "or",
        "or_eq",
        "private",
        "protected",
        "public",
        "register",
        "reinterpret_cast",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "static_cast",
        "struct",
        "switch",
        "template",
        "this",
        "throw",
        "true",
        "try",
        "typedef",
        "typeid",
        "typename",
        "union",
        "unsigned",
        "using",
        "virtual",
        "void",
        "volatile",
        "wchar_t",
        "while",
        "xor",
        "xor_eq",
    )
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 [file2 ...]
            Prints C/C++ symbols found in the indicated files.
        Options:
            -c    Treat all files as C files
            -k    Don't remove keywords
            -n    Don't report symbols by file
        """)
        )
        exit(status)

    def ParseCommandLine():
        d["-c"] = False  # Treat as C file
        d["-k"] = False  # Do not remove keywords
        d["-n"] = False  # Do not order by file
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "ckn")
        except getopt.error as str:
            print("getopt error:  %s\n" % str)
            exit(1)
        for o, a in optlist:
            if o[1] in "ckn":
                d[o] = not d[o]
        if not args:
            Usage()
        return args


if 1:  # Core functionality

    def ReadFile(file):
        """Read in the file as a whole string and remove all comments.
        Return the resulting string.
        """
        ifp = open(file)
        str = ifp.read()
        ifp.close()
        while g.c_comment.search(str):
            str = g.c_comment.sub("", str)
        while g.cpp_comment.search(str):
            str = g.cpp_comment.sub("\n", str)
        while g.string.search(str):
            str = g.string.sub("\n", str)
        newstr = ""
        for i in range(len(str)):
            if str[i] in g.punctuation:
                newstr += " "
            else:
                newstr += str[i]
        return newstr

    def ProcessFile(file):
        str = ReadFile(file)
        if str == "":
            print("Couldn't read file '%s'\n" % file, file=sys.stderr)
            return
        tokens = re.split(" +|\t+", str.replace("\n", " "))
        dict = {}
        keyword_list = cpp_keywords
        if file[-2] == "." and (file[-1] == "C" or file[-1] == "c"):
            keyword_list = c_keywords
        if d["-c"]:
            keyword_list = c_keywords
        if d["-k"]:
            keyword_list = []
        for token in tokens:
            if token not in keyword_list and token != "":
                if g.valid_symbol.match(token):
                    dict[token] = 0
        k = dict.keys()
        g.symbols[file] = list(sorted(k))

    def Conglomerate():
        lst = []
        for key in g.symbols.keys():
            lst += g.symbols[key]
        for item in sorted(lst):
            print(item)

    def PrintResults():
        if d["-n"]:
            Conglomerate()
            return
        filelist = g.symbols.keys()
        for file in sorted(filelist):
            print(file + ":")
            for token in g.symbols[file]:
                print("  " + token)


if __name__ == "__main__":
    d = {}
    args = ParseCommandLine()
    for file in args:
        ProcessFile(file)
    PrintResults()
