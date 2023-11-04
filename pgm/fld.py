'''
Manipulate fields in the stdin stream
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 1995, 2009, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Manipulate fields in the stdin stream
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from io import StringIO
    from pdb import set_trace as xx
    import functools
    import getopt
    import re
    import sys
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    debug = False
    testing = False
    nl = "\n"
    dash = "-"
    split_re = None
    class TestingException(Exception):
        pass

    status_ok = 0
    status_fail = 1
    status_bad_command_line = 2

    manual = dedent('''
    NAME
        fld -- manipulate fields of stdin
    SYNOPSIS
        fld [options] [X1 [X2 ...]]
    DESCRIPTION
        This program will print selected fields from an input text stream.
        The fields' order can be rearranged from the original stream's
        order and the fields can be duplicated.  Both delimited and fixed-
        width streams can be input or output.

        The X's are the field specifiers and have the following format.  All
        integers n and m are base 10; field numbering is 1-based.

        n     Specifies field n
        n-m   Specifies field n to m inclusive
        -n    Specifies fields 1 to n
        n-    Specifies field n to the end of the line

        If m is less than n in an n-m expression, it means print the fields
        from m to n in reverse order.

        The output is to stdout.  The specified fields are separated by tab
        characters (or the specified string if the -o option is used).  If
        there are no specified fields on the command line, the whole line is
        printed to stdout; in this case all whitespace is collapsed to one
        output separator character.

        The fields are printed in the order given on the command line, which
        allows for rearranging and/or duplication of the stream's data.

        Any referenced fields that are not present are ignored.

        Note that the default field separator is whitespace.  This means a
        line such as

            "This    \\t   is  \\t a line"

        will be parsed into the fields

            ["This", "is", "a", "line"]

        If that is not the behavior you want, then you'll want to use the -i
        option to specify a python regular expression to use to delimit the
        fields.
    OPTIONS
        -i regexp
            Specifies an input field separator regular expression that
            overrides the default of whitespace("[ \t]+").  The regular
            expression syntax is that of python's re module.
        -I
            Make the -i option's regular expressions case-insensitive.
        -l string
            Trims any characters in string from the left side of each field.
        -n string
            Fields are fixed-width and string contains a list of the
            starting column numbers (1-based).  Any non-numeric characters
            can separate the column numbers.  This can be used to change a
            fixed-width data file to a string-separated form.  Trailing
            whitespace will be stripped from the fields.  The field numbers
            will be sorted, so they can be supplied in any order.
        -m string
            The output will be in fixed-width form; the field widths are
            given in the same format as in the column numbers in the -n
            option.  If you don't specify enough field widths, the
            remaining fields will not be printed, even though they were
            specified on the command line.  If a field won't fit into the
            stated space, it will be truncated; if you want to know about
            this condition, use the -t option.  Fields that are shorter
            than the corresponding length will be padded with space
            characters.
        -M
            The output will be in fixed-width form; the field widths will be
            determined by the largest fields.
        -o string
            Specifies the output field separator string.  The default is the
            tab character.
        -r string
            Trims any characters in string from the right side of each field.
        -R
            Reverses the sense of all fields printed.
        -s
            Cause a fatal error if all the input records are not of the same
            length (i.e., the length of field 1 doesn't need to match field 2,
            but the first field on all lines must be the same length).
        -t
            If the -m option was used and any fields needed to be truncated,
            print the line numbers that were truncated to stderr when finished.
        -w
            Strips whitespace from both ends of each line read before parsing.
    EXAMPLES
        * Delimited files
            Suppose you have the single input line
            1 2 3 4 5 6 7 8 9 10 11 12
            If you type
            fld -3 2 5-3 4-6 8-
            you'll get the following output fields, separated by tabs:
            1 2 3 2 5 4 3 4 5 6 8 9 10 11 12
            If you typed the same as above, but with a -R:
            fld -R -3 2 5-3 4-6 8-
            you'd get
            12 11 10 9 8 6 5 4 3 4 5 2 3 2 1
        * Fixed-width fields
            Suppose you have the single input line (double quotes not
            included in line)
            "f1 f2   f3"
            If you type
                fld -n "1,4 9" 3 2
            you'd get the following output
                'f3\\tf2'
            To show the example of using fixed-width output fields, if
            you typed
                fld -n "1,4 9" -m "8,8" 3 2 1
            you'd get
                'f3      f2      \\n'
            Note that the last specified field #1 would not be printed.  If
            this is not what you want, read the comments in PrintOutputLine
            and comment out the line that does the truncation.
    DIAGNOSTICS
        0  Successful completion.
        1  Failure.
        2  Failure due to an invalid command line option.''')
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def dbg(s):
    if debug:
        print("+", s, file=sys.stderr)
def Usage(status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] field-specifiers
      Pick out 1-based number fields of a stream.  Example:
        fld -f - 3 1 
      gets fields 3 and 1 from stdin and sends them to stdout.
      Fields are split by default on python's re whitespace.
      -f is to specify the file to read; '-' means stdin.  Use
      -i to specifiy a regexp to split the fields.
      Use -h to get a more detailed manual.
      '''))
    exit(status)
def GetFieldWidthNumbers(field_width_specs):
    def f(s):   # Change a non-numeric character into a space
        from string import digits
        if s in digits:
            return s
        return " "
    fn = ''.join(map(f, list(field_width_specs)))  # Keep only digits
    fn = [int(i) for i in fn.split()]
    return fn
def GetFixedFieldNumbers(field_number_specs):
    def f(s):   # Change a non-numeric character into a space
        from string import digits
        if s in digits:
            return s
        return " "
    fn = ''.join(map(f, list(field_number_specs)))  # Keep only digits
    # Convert to 0-based indexing and sort the numbers
    fn = list(sorted([int(i) - 1 for i in fn.split()]))
    return fn
def ProcessFieldSpecs(specs, settings):
    '''Turn the field specifications into a tuple of field numbers.
    Reverse if so indicated.  Note at this point, all field numbers are
    1-based.
    '''
    if debug:
        dbg("Field specs from command line = " + str(specs))
    fields = []
    if len(specs) == 0:
        fields.append(-1)
        if debug:
            dbg("No fields on command line; set to [-1] to get everything")
    for spec in specs:
        try:
            if dash in spec:
                # It's of the form '-n', 'n-m', or 'n-'.  We'll encode the
                # third form by using a negative number.
                if spec[0] == dash:
                    for i in range(1, int(spec[1:]) + 1):
                        fields.append(i)
                elif spec[-1] == dash:
                    fields.append(-int(spec[:-1]))
                else:
                    n, m = [int(i) for i in spec.split(dash)]
                    if n > m:
                        # A decreasing range
                        for i in range(n, m - 1, -1):
                            fields.append(i)
                    else:
                        # An increasing range
                        for i in range(n, m + 1):
                            fields.append(i)
            else:
                # It must be a simple number
                fields.append(int(spec))
        except ValueError:
            Error("'%s' is an improper field specification" % spec,
                  status_bad_command_line)
    settings["fields to get"] = fields
    if debug:
        dbg("Fields specified list (1-based):  ", str(fields))
def PrintOutputLine(line, settings):
    def pad(s, width, settings=settings):
        # Pad s with spaces if it's less than width long.  If longer,
        # truncate it and indicate the line number in settings.
        n = len(s)
        if n == width:
            return s
        if n < width:
            return s + " "*(width - n)
        if n > width:
            # Truncation condition
            settings["truncated lines"][settings["line number"]] = 0
            return s[:width]
    # Note line is a list of field strings
    if settings["output fixed width"]:
        widths = settings["output fixed width"]
        n = len(widths)
        for i, field in enumerate(line):
            if i >= n:
                # We have more fields than we have width fields.  There are
                # two choices of what we could do here:  truncate the
                # output or just leave the line alone and leave the
                # remaining fields alone.  I've chosen truncation, as it
                # (in my mind) most closely gives the user what he asked
                # for.  If you'd rather have the remaining fields included,
                # just comment out the following line.
                del line[i:]
                break
            line[i] = pad(field, widths[i])
        print(''.join(line))
    elif settings["output fixed max width"]:
        # The settings will contain the max column widths of the output
        # fields.  Note the output will have a space character between
        # each field to make it a bit easier to read.
        d = settings["max field widths"]
        for i, field in enumerate(line):
            line[i] = pad(field, d[i])
        print(' '.join(line))
    else:
        print(settings["output separator"].join(line))
def ProcessFields(fields, settings):
    '''Remove any indicated characters from the right and left of each
    field.
    '''
    L = settings["trim left"]
    if L:
        fields = [i.lstrip(L) for i in fields]
    R = settings["trim right"]
    if R:
        fields = [i.rstrip(R) for i in fields]
    return fields
def SplitFixedWidth(line, columns, line_number):
    fields = []
    n = len(columns)
    try:
        for i, column in enumerate(columns):
            if i == n - 1:
                fields.append(line[column:].rstrip())
            else:
                fields.append(line[column:columns[i+1]].rstrip())
    except IndexError:
        Error(f"Parsing error in line {line_number}\n"
              f"{column} or {columns[i+1]} is a bad column number",
              status_fail)
    return fields
def ProcessLine(line, output, settings):
    settings["line number"] += 1
    if debug:
        dbg("Line #", str(settings["line number"]) + ": " + repr(line))
    if settings["strip whitespace"]:
        line = line.strip()
    if settings["fixed width"]:
        columns, line_number = settings["fixed width"], settings["line number"]
        fields = SplitFixedWidth(line, columns, line_number)
    else:
        fields = settings["split_re"].split(line)
    n = len(fields)
    if settings["same size records"]:
        if settings["record size"] == 0:
            # This is the first record we've seen
            if n == 0:
                # It was an empty line
                return
            else:
                # All records must now have this length
                settings["record size"] = n
        else:
            if n != settings["record size"]:
                msg = ("Fatal error:  line number %d does not have %d fields"
                       % (settings["line number"], settings["record size"]))
                if not testing:
                    Error(msg, status_fail)
    output = []
    for i in settings["fields to get"]:
        try:
            # Note we convert to 0-based indexing
            if i < 0:
                for j in range(abs(i), len(fields) + 1):
                    output.append(fields[j - 1])
            else:
                output.append(fields[i - 1])
        except IndexError:
            pass
    if settings["reverse sense"]:
        output.reverse()
    output = ProcessFields(output, settings)
    # Save the maximum field widths in settings
    d = settings["max field widths"]
    for i, field in enumerate(output):
        n = len(field)
        d.setdefault(i, n)
        d[i] = max(n, d[i])
    return output
def PrintTruncation(settings):
    m = "Lines with truncated fields:  "
    lines = list(settings["truncated lines"].keys())
    if settings["show truncated lines"] and lines and not testing:
        print(m, file=sys.stderr, end="")
        for line in sorted(lines):
            print(line, " ", file=sys.stderr, end="")
        print()
def ParseCommandLine(settings):
    '''Because we will allow field specifications such as '-3', we need
    to collect all field specs on the command line and not pass them to
    getopt.  Thus, build two lists; one contains the field specs and the
    other contains the options.
    '''
    require_arg = "filmnor"
    no_require_arg = "dhIMRstwz"
    fs = re.compile(r"^-\d+$|^\d+-\d+$|^\d+-$")
    field_specs, options = [], []
    need_option_argument = False
    for arg in sys.argv[1:]:
        if need_option_argument:
            options.append(arg)
            need_option_argument = False
            continue
        elif arg[0] == dash:
            if len(arg) < 2:
                Error("'-' is not allowed", status_bad_command_line)
            next_char = arg[1]
            if next_char in require_arg:
                options.append(arg)
                need_option_argument = True
                continue
            elif next_char in no_require_arg:
                options.append(arg)
            else:
                # It has to be a field spec
                field_specs.append(arg)
        else:
            # It has to be a field spec
            field_specs.append(arg)
    global debug
    if debug:
        dbg("Options     =" + str(options))
        dbg("Field specs =" + str(field_specs))
    try:
        optlist, args = getopt.getopt(options, "df:hi:Il:m:n:Mo:r:Rstwz")
    except getopt.GetoptError as e:
        msg, option = e
        Error(msg, 1)
    for o, a in optlist:
        if o == "-d":
            debug = True
        elif o == "-f":
            settings["file"] = a
        elif o == "-h":
            print(manual)
            exit(0)
        elif o == "-i":
            settings["input regexp"] = a
            try:
                settings["split_re"] = re.compile(a)
            except re.error as e:
                Error("Bad -i regular expression: " + str(e),
                      status_bad_command_line)
        elif o == "-I":
            settings["case sensitivity"] = False
        elif o == "-l":
            settings["trim left"] = a
        elif o == "-r":
            settings["trim right"] = a
        elif o == "-n":
            settings["fixed width"] = GetFixedFieldNumbers(a)
        elif o == "-m":
            settings["output fixed width"] = GetFieldWidthNumbers(a)
        elif o == "-M":
            settings["output fixed max width"] = True
        elif o == "-o":
            settings["output separator"] = a
        elif o == "-R":
            settings["reverse sense"] = True
        elif o == "-s":
            settings["same size records"] = True
        elif o == "-t":
            settings["show truncated lines"] = True
        elif o == "-w":
            settings["strip whitespace"] = True
    # We compile the input regexp again because the ignore case flag could
    # have been set.
    try:
        r = settings["input regexp"]
        if settings["case sensitivity"]:
            settings["split_re"] = re.compile(r)
        else:
            settings["split_re"] = re.compile(r, re.I)
    except re.error as e:
        Error("Bad -i or -I regular expression: " + str(e),
              status_bad_command_line)
    if not field_specs:
        Usage()
    if debug:
        dbg("Settings:")
        for i in settings:
            if i == "split_re":
                s = settings[i]
                dbg(f"  {i:20d} = {s.pattern!r} (pattern from regexp)")
            else:
                dbg(f"  {i:20d} = {s!r}")
        dbg(f"Command line args = {args}")
    return field_specs
def GetLines(settings):
    file = settings["file"]
    if file == "-":
        lines = sys.stdin.readlines()
    else:
        lines = open(file).readlines()
    return lines
if __name__ == "__main__": 
    settings = {
        "file": "-",                            # -f
        "input regexp": "[ \t]+",               # -i
        "case sensitivity": True,               # -I
        "trim left": "",                        # -l
        "trim right": "",                       # -r
        "fixed width": None,                    # -n
        "output fixed width": None,             # -m
        "output fixed max width": False,        # -M
        "max field widths": {},
        "output separator": "\t",               # -o
        "reverse sense": False,                 # -R
        "same size records": False,             # -s
        "record size": 0,                       # -s
        "show truncated lines": False,          # -t
        "truncated lines": {},
        "strip whitespace": False,              # -w
        "line number": 0,
    }
    args = ParseCommandLine(settings)
    ProcessFieldSpecs(args, settings)
    lines = GetLines(settings)
    lines = [i.rstrip("\n") for i in lines]     # Remove newlines
    output = []
    for line in lines:
        output.append(ProcessLine(line, output, settings))
    for line in output:
        PrintOutputLine(line, settings)
    PrintTruncation(settings)
    D
