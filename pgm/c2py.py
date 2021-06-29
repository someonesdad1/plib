'''
TODO

    * Change lines with // to #

Translate C code to python
    This script will do some of the work, but you'll still be left with
    some hand translation for pointer stuff and to handle gotos (so it
    works best on C code with no gotos and few pointers).

    Here's how the script works:

    * Comments are converted to python comments.
    * All lines have the ending ';' removed.
    * It is an error if any line subsequently contains a ';' character,
      as this might indicate more than one statement per line.
    * '&&' is changed to ' and ' and '||' is changed to ' or '.
    * 'else if' --> 'elif'
    * 'else' --> 'else:'
    * An 'if ()' statement is translated into 'if():'.  Note the
      translation will be wrong if there are multiple tests inside the
      parentheses; these will cause a python error and be easy to find.

    Lines are otherwise left alone, so things like #include and #define
    statements will be in the resulting text.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Translate C code to python
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import re
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from color import C
if 1:   # Global variables
    nl = "\n"
    comment = re.compile(r"/\*(.*?)\*/", re.S)
    if_stmnt = re.compile(r"if\s*(\(.*?\))", re.S)
    elif_stmnt = re.compile(r"(else\s+if)")
    else_stmnt = re.compile(r"(else)")
    not_token = re.compile(r"![^=]")
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Commentify(s):
    '''Split on newlines and prepend '#' to each line.  Return as a
    string.'''
    out = []
    for line in s.split(nl):
        out.append("# " + line)
    return nl.join(out)
def ConvertComments(s):
    '''Convert C comments to python comments and return the string.
    '''
    mo = comment.search(s)
    while mo:
        assert len(mo.groups()) == 1
        t = Commentify(mo.groups()[0])
        i, j = mo.start(), mo.end()
        s = s[:i] + t + s[j:]
        mo = comment.search(s)
    return s
def RemoveSemicolons(s, file):
    '''Note this also removes curly braces.
    '''
    out = []
    for i, line in enumerate(s.split(nl)):
        line = line.rstrip()
        if not line or line.lstrip()[0] == "#":
            out.append(line)
            continue
        if line[-1] in ";{}":
            line = line[:-1]
            if not line.strip():
                continue
        if line.count(";") > 1 and "for" not in line:
            msg = "More than one ';' in line {0} of '{1}'"
            Error(msg.format(i + 1, file))
        if ";" in line and "for" not in line:
            line = line.replace(";", "")
        out.append(line)
    return nl.join(out)
def FixIfs(s, file):
    '''Find and translate if statements:
    !  --> not
    && --> and
    || --> or
    '''
    out = []
    mo = if_stmnt.search(s)
    while mo:
        assert len(mo.groups()) == 1
        i, j = mo.start(), mo.end()
        out.append(s[:i])
        t = s[i:j]  # The contents of the if statement's parentheses
        while not_token.search(t):
            t = not_token.sub("not ", t)
        t = t.replace("&&", " and ")
        t = t.replace("||", " or ")
        out.append(t + ":")
        s = s[j:]
        mo = if_stmnt.search(s)
    out.append(s)
    return ''.join(out)
def FixElif(s, file):
    '''Change 'else if' to 'elif' and put a colon after 'else'.
    '''
    out = []
    for line in s.split(nl):
        t = line.lstrip()
        if not t or t[0] == "#":
            out.append(line)
            continue
        mo = elif_stmnt.search(line)
        if mo:
            i, j = mo.start(), mo.end()
            line = line[:i] + "elif" + line[j:]
            out.append(line)
            continue
        mo = else_stmnt.search(line)
        if mo:
            i, j = mo.start(), mo.end()
            line = line[:i] + "else:" + line[j:]
            out.append(line)
            continue
        out.append(line)
    return nl.join(out)
def Translate(file, d):
    '''Translate the given file and write it to a new file with '.py'
    appended.
    '''
    with open(file, "r") as fp:
        s = fp.read()
    s = s.replace("&&", " and ").replace("||", " or ")
    s = ConvertComments(s)
    s = RemoveSemicolons(s, file)
    s = FixIfs(s, file)
    s = FixElif(s, file)
    with open(file + ".py", "w") as fp:
        fp.write(s)
def BugNotice():
    print(f"{C.lcyn}", end="")
    print(dedent(f'''
    Bugs in implementation:
        * Need to handle while and do{{}}while statements too
        * if () to if(): can be wrong if there are multiple tests inside
          the parentheses
        * Pointer stuff has to be handled manually
        * goto statements not handled
        * You will still have to hand-translate stuff
    '''))
    print(f"{C.norm}", end="")
if __name__ == "__main__":
    BugNotice()
    d = {}
    if len(sys.argv) < 2:
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2...]
          Translates the indicated C file(s) to python.  '.py' will be appended to
          the file's name.
        '''))
    for file in sys.argv[1:]:
        Translate(file, d)
