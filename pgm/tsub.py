'''

TODO
    - Change behavior to allow the command line to have arbitrary
      whitespace in front of the '.'
        - Add -s to force strict behavior ('.' in first column)
    - Should allow multiline substitutions.  Certainly this can be done
      within a code block, but it would be nicer if multiline stuff was
      handled.
        - Special syntax of .mls symbolname/.endmls could handle this, but
          it would be better if it could be handled with regular python
          syntax.
    - Allow the syntax of {varname} to be macro expansions in text
        - This allows the architecture of reading the whole string into
          memory and then using str.format() to do the substitutions.
    - Read everything into memory at once, then process it as a string or
      bytestring.
        - Use regexps to do the key processing.
    - Switch os.path stuff to pathlib
    - .off should also have an optional [expr]
    - Check to see that defined variables really wind up in the global
      namespace or are put into a variables dict.
    - Change comment block to .[, .] to agree with ts.py?
    - Use f-strings instead of clumsy %%(name)s formatting
    - It could be nice to allow things like {F(x)} to be found and executed
      as a code short-hand.  Or use '.{F(x).}'.
    - Virtually all input text will be UTF8.  Does there need to be an
      option to handle other encodings?
    - Add -b option to change r'\\n' on a line to remove the newline.  This
      needs to be an option as it's now the default behavior and this
      screws up things like r'\\' in LaTeX tables.
    - .def var = str
        - If var is a python symbol, then put it into the localvars dict so
          it can also be used in code.
    - .undef var1 var2 ...

A text substitution tool

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2002, 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # A text substitution tool
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        import getopt
        import os
        import re
        import sys
        from pathlib import Path as P
        from pprint import PrettyPrinter
        PP = PrettyPrinter(width=180)
        pp = PP.pprint
        if 0:
            import debug
            debuSetDebugger()
    # Custom imports
        from wrap import dedent
        from color import TRM as t
    # Global variables
        class g: pass
        dbg = True  # If True, use breakpoints for debugging
        #script = os.path.split(sys.argv[0])[1]
        localvars = {}              # Dict for local variables
        cmd_char = "."              # String that denotes a command line
        output_on = 1
        current_file = ""
        current_line = 0
        in_comment_block = False    # If True, we're in a comment block
        macros = {}
        macro_names = []
        start_dir = os.getcwd()
        included_files = {}         # Which files have already been included
        # Globals to help with evaluating chunks of code
        code_mode = 0               # If true, we're in a code section
        current_code = ""           # String to hold the code lines
        code_names = {}             # Keep track of named sections of code
        # The following regular expression is used to identify lines that contain
        # formatting strings that need to be expanded with the global dictionary.
        need_global_expansion = re.compile(r"%\(([a-zA-Z][a-zA-Z_]*)\)")
if 1:  # Utility
    def ColorCoding(on=False):
        t.err = t("redl") if on else ""     # Error message
        t.ln = t("grnl") if on else ""      # Line number
        t.fn = t("yell") if on else ""      # File name
        t.log = t("trql") if on else ""     # Routine debug (-v on) message
        t.cmd = t("ornl") if on else ""     # Command line
        t.line= t("lill") if on else ""     # Non-command line from input file
        t.code = t("magl") if on else ""    # Line from code block
        t.redef = t("lipl") if on else ""   # Warning of a redefinition
        t.undef = t("viol") if on else ""   # Undefining a substitution
        t.N = t.n if on else ""             # Default normal mode
    def Manpage():
        name = P(sys.argv[0])
        sname = name.name
        print(dedent(f'''
        NAME
            {name} - Text substitution tool

        SYNOPSIS
            {sname} [options] file1 [file2...]
        
        DESCRIPTION
        
            The {sname} script is intended to make text substitutions and
            allow arbitrary python code in your text files to compute
            things needed.

            {sname} replaces strings in the input files, then prints them
            to stdout.  It knows nothing about things like identifiers or
            tokens in programming languages.  It's a dumb text substitution
            program.  For each line of input, it searches to see if a
            "macro" name occurs on that line; if it does, then the text is
            replaced.  The search starts with the longest macro names and
            goes to the shorter names.  This lets you have two macros named
            'mp_MyMacro4' and 'mp_MyMacro' and not have mp_MyMacro's value
            replaced when the macro name mp_MyMacro4 occurs in text.
            
            You'll want to make sure your macro names will not be found in
            text except where you deliberately put them in.  One way is to
            name all your macros with a prefix such as "mp_".
        
            Programmers probably expect macro names and other things to be
            processed in tokens like other macro tools such as m4.  The
            {sname} script doesn't behave this way; it uses simple text
            substitution.
        
        Options
            -h
                Prints this man page.
            -I dir
                Define an include directory.  When a file is included, it
                is first looked for in the current directory.  If it isn't
                found, directories specified with the -I option are
                searched sequentially and the first match is used.  More
                than one -I option can be given.
            -v
                Show the processing that's happening in colored text to
                stderr.  The script's normal output is in plain text.
                Different colors are used to help interpret the output.
                Escape codes for colorizing are emitted even if the output
                isn't a TTY; if you don't want this behavior, find the line
                't.always = True' in the code and make it False.

                This is a handy option to see what's happening with your
                input file.  It will show all of the input lines.
        
        Command lines
            Command lines for the macro processor have a '.' character in
            the first column and can be followed by one or more space
            characters.  You can edit the IsCommandLine() function in the
            script if you'd like to change this syntax.
        
            The general forms of a command are:
                
                .  token [token's arguments]
                .. token [token's arguments]
        
            There can be optional whitespace between the '.' character and
            the characters of the token.
        
            Note that command lines can have embedded macros expanded in them.
            This e. allows you to write
        
                .def mp_MY_FILE =abc
                .include mp_MY_FILE
        
            If you do not want macros expanded in the line, use the '..'
            form.

            A single line that only contains '.' is allowed; it behaves as a
            comment and is ignored.  It's handy to space out text in an
            input file.
        
            The allowed command tokens are:
        
            .def name = value
                Defines a text substitution.  The name string can contain
                any characters except a newline and cannot begin or end
                with a space character.  All characters after '='
                character become part of the substitution except for the
                newline.

                The definition can also be 'name='.  This shows the space
                before the '=' is optional and also shows that you can
                define a substitution to be the empty strin

                You are free to redefine a substitution name at any time,
                but if the -v option is used, a warning message will be
                printed to stderr to alert you to the redefinition.

            .undef name

                Undefine a substitution.  If name isn't defined, there's no
                error, but a warning will be printed if -v is used.
        
            .cd dir
                Set the current directory of the script to dir.  If dir is
                missing, the current directory is set to what it was at the
                start of the script.
        
            .{{ 
            .}}

                Comment block.  This is an easy way to comment out a block
                of text.  When the -v option is used, lines inside a
                comment block won't be printed.

            .( [code_section_name]
            .)

                These two tokens must each appear on a line by themselves.
                They delimit a block of lines of text that will be
                interpreted as python code.  Typically, this is used to
                define and set some global variables that are used for
                variable expansions in lines.  See the Examples section
                below for details.  However, arbitrary processing can be
                done.  Any variables that you define in your code section
                are added to the localvars dictionary, which is in the
                global namespace.

                IMPORTANT:  the code section is executed using exec() and
                any variables you define are put into the global namespace.
                To avoid namespace pollution or overwriting an existing
                variable, use names that you know are not in the global
                namespace.  
        
                If code_section_name is given, it must be encountered only
                once while processing, otherwise an error will occur and
                processing stops.  You can use this feature to avoid
                accidentally including files multiple times (if your code
                in the included file has a name, the {sname} script will
                stop executing the second time it is included).

                If an error in the code occurs, you'll get an exception.
                You'll see '[file:line_number]' in the traceback.  This
                points to the location of the '.)' line that ends the code
                block.  You can find the offending line by counting from
                the '.(' by the 'line x' message just after this file and
                line number chunk.  If you used the -v option, you'll be
                able to view the offending line on the screen by doing this
                counting.
        
            .include file [once]
                Used to include another file at this point.  The behavior is
                to read all the lines of the indicated file and insert them
                at the current location.  It is a fatal error if the file
                cannot be found.
        
                If the token 'once' is present, the file is only included
                once.  This is intended to be used where the include file
                has python code/endcode chunks that you only want executed
                once.

                Because of the way the script works, you can't include
                a file that has a space in its name.

            .sinclude file [once]
                Same as include, except it's not an error if the file cannot
                be found.
        
                If the token 'once' is present, the file is only included
                once.  This is intended to be used where the include file
                has python code/endcode chunks that you only want executed
                once.
        
            .#
                This line is a comment and is discarded.  You can omit the
                '#' and the effect is the same.
        
            .on [expr]
                Turns substitution on if expr is True.  Ignored if it is
                already on.
        
            .off
                Turns substitution off.  Ignored if it is already off.
        
        Python variables
            You may use python variable references in your text.  These references
            must be of the form '%%(varname)s', where varname is the name of a
            python variable and s is a formatting string, such as 's', 'd', 'f',
            etc.  These expressions will be evaluated with the global dictionary
            in effect at the time the code is evaluated.
        
            Typical use of this functionality is to make a counter that gets
            incremented or to define multiline strings.
        
        Example
            The following example shows a simple use of python code to
            generate serial numbers for a set of files.  The idea is that the
            serial numbers will be incremented each time they are referenced,
            allowing a set of files to have unique numbers.
        
            File 1 contains:
                .(
                sn = 100 # Starting serial number
                def IncrementSerialNumber():
                    global sn
                    sn += 1
                .)
                This is file 1.  The serial number is %%(sn)d.
                .(
                IncrementSerialNumber()
                .)
            
            File 2 contains:
                This is file 2.  The serial number is %%(sn)d.
                .(
                IncrementSerialNumber()
                .)
        
            Running the command
        
                python mp.py 1 2
                
            produces the output:
        
                This is file 1.  The serial number is 100.
                This is file 2.  The serial number is 101.
        
            Note:  any global variables and functions you define in your code
            will be put into the {sname} script's global namespace.
        '''))
    def RmNl(line):
        'Remove the newline if it has one'
        if line and line[-1] == "\n":
            return line[:-1]
        return line
    def Log(s, color=None):
        if d["-v"]:
            color = "" if color is None else color
            print(f"{color}+ {RmNl(s)}{t.N}", file=sys.stderr)
    def PrintColorCoding():
        if not d["-v"]: 
            return
        f = sys.stderr
        print("Color coding:", file=f)
        t.print(f"    {t.ln}Line number", file=f)
        t.print(f"    {t.fn}File name", file=f)
        t.print(f"    {t.log}Routine debug message", file=f)
        t.print(f"    {t.cmd}Command line", file=f)
        t.print(f"    {t.line}Non-command line from input file", file=f)
        t.print(f"    {t.code}Line from code block", file=f)
        t.print(f"    {t.redef}Warning of a redefinition", file=f)
        t.print(f"    {t.undef}Undefining a substitution", file=f)
        print(file=f)
    def Dedent(s):
        's is a code string; remove any common indenting and return it'
        def CntWS(s):
            'Return number of spaces in beginning whitespace of s'
            l = list(s)
            n = 0
            while l and l[0] == " ":
                n += 1
                l.pop(0)
            return n
        if not s:
            return s
        # Remove last newline
        if s[-1] == "\n":
            s = s[:-1]
        lines = s.split("\n")
        a = [CntWS(i) for i in lines]
        n = min([CntWS(i) for i in lines])
        if n:
            lines = [i.replace(" "*n, "", 1) for i in lines]
        q = '\n'.join(lines)
        if q[-1] != "\n":
            q += "\n"
        return q
    def Usage():
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Text substitution tool.
        Options
          -c      Turn off color coding
          -h      Print a man page
          -I dir  Define an include directory
          -v      Verbose output
        Command lines have the form (whitespace after '.' optional):
          .  command [parameters]
          .. command [parameters]       Substitutions not expanded in line
        Commands:
          .def sym = value              Define a new substitution
          .undef sym                    Undefine a substitution
          .#                            This line is a comment
          .{{                            Start a comment block
          .}}                            End a comment block
          .on [expr]                    Turn output on if expr is True
          .off [expr]                   Turn output off if expr is True
          .( [name]                     Define a [named] python code block.
                                        If named, only one such block allowed.
          .)                            End of python code block
          .include                      Insert a file; error if not found
          .sinclude                     Insert a file; no error if not found
          .cd [dir]                     Change the current directory
        '''))
    def ParseCommandLine(d):
        d["-c"] = False     # If True, no color coding for -v
        d["-I"] = []        # Directories to search for include files
        d["-v"] = False     # Verbose debugging mode
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "cI:hv", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "cv":
                d[o] = not d[o]
            elif o == "-h":
                Manpage()
            elif o == "-I":
                p = P(a)
                if not (p.exists() and p.is_file()):
                    Error(f"-I:  {a!r} doesn't exist or isn't a file")
                d["-I"].append(p)
        ColorCoding(False if d["-c"] else True)
        if d["-v"]:
            PrintColorCoding()
        return files
if 1:  # Core functionality
    def SortMacroNames():
        '''Sort the macro names so that the longest macros are first.  This
        lets macros like 'mp_MyMacro4' get substituted before 'mp_MyMacro',
        giving the behavior most of us would expect.
        '''
        global macro_names
        s = [(len(i), i) for i in macro_names]
        s.sort()
        macro_names = [i[1] for i in list(reversed(s))]
    def Error(msg):
        print(msg, file=sys.stderr)
        exit(1)
    def ProcessCommandLine(line):
        '''The line is a command line, so parse out the command and execute
        it.  If we're in code mode, the line is appended to the current_code
        strin
        '''
        global code_mode, current_code, macro_names
        original_line = line
        # Note:  we don't remove the newline, as this is needed to separate
        # code lines.
        if not line.startswith(cmd_char*2):
            line = ExpandMacros(line)
        elif line.startswith(cmd_char*2):
            # Remove one cmd_char string
            line = line.replace(cmd_char, "", 1)
        # If we're in code mode, just append the line to the current_code
        # string and return # (unless we're at the code end).
        if code_mode and not line.startswith(cmd_char):
            Log("Code line: " + line, color=t.code)
            current_code = current_code + line
            return
        # Remove the cmd_char string
        st = line.replace(cmd_char, "", 1).strip()
        if len(st) == 0:
            # We ignore a command line with no useful input
            Log(f"{t.ln}[{current_line}]{t.log} Command line with no input")
            return
        fields = st.split()
        if len(fields) == 0:
            # We ignore a command line with no useful input
            Log(f"{t.ln}[{current_line}]{t.log} Command line with no input")
            return
        # Get the command
        cmd = fields[0]
        if cmd == "def":
            # Resplit this line by first removing 'def', then splitting on
            # the '=' character
            st = st[3:].strip()
            f = st.split("=")
            if len(f) != 2:
                m = f"{original_line!r} is a bad .def line (missing '=' or too many?)"
                Error(m)
            macro_name = f[0].strip()
            macro_value = RmNl(f[1])
            if macro_name in macros and d["-v"]:
                m = [f"{t.redef}Warning:  redefining definition '%s' in line {t.ln}%d{t.redef} "
                    f"of file {t.fn}'%s'{t.redef}\n" % (macro_name, current_line, current_file)]
                m += [f"          {t.redef}Previous definition at line {t.ln}%d{t.redef} "
                      f"of file {t.fn}'%s'{t.N}" % (macros[macro_name][1], macros[macro_name][2])]
                print(''.join(m), file=sys.stderr)
            macros[macro_name] = [macro_value, current_line, current_file]
            macro_names = macros.keys()
            SortMacroNames()
            Log("Defined %s to '%s'" % (macro_name, macro_value))
        elif cmd == "(":
            # Beginning of a code section.  If it's got a name, let's make
            # sure it hasn't been executed before.
            if len(fields) > 1:
                # It's got a name
                code_name = fields[1]
                if code_name in code_names:
                    m = ["Error:  code section named '%s' at line %d of file "
                        "'%s' already defined" %
                        (code_name, curr_line, curr_file)]
                    m += ["Previous definition line %d in file '%s'" %
                        (code_names[code_name][0], code_names[code_name][1])]
                    Error('\n'.join(m))
                else:
                    # Add it to the dictionary
                    code_names[code_name] = [curr_line, curr_file]
            # Flag that we're now reading code
            code_mode = 1
        elif cmd == ")":
            # End of a code section.  Compile and execute the code.
            if not code_mode:
                Error("Error:  '.)' at line %d of file '%s' missing "
                    "a matching previous '.(' command" %
                    (curr_line, curr_file))
            code_mode = 0
            # Remove any common indent from the code lines.  This allows
            # users to indent their code to make it easier to read.
            if 0:
                print("current_code after dedent:")
                pp(current_code)
                print()
            current_code = Dedent(current_code)
            if 0:
                print("current_code after dedent:")
                pp(current_code)
                print()
            # Compile and execute.  If we get an exception, the user will
            # know about where the problem is because the file and line
            # number of the endcode statement will be in the traceback.
            loc = "[%s:%d]" % (current_file, current_line)
            try:
                co = compile(current_code, loc, "exec")
            except Exception as e:
                if dbg:
                    print(f"Got compile exception:\n  {e!r}")
                    breakpoint()
                else:
                    raise
            try:
                exec(co, globals(), localvars)
            except Exception as e:
                if dbg:
                    print(f"Got exec exception:\n  {e!r}")
                    breakpoint() 
                else:
                    raise
            current_code = ""   # Reset for next code block
            # Save our variables in the global namespace, but remove this
            # function's locals.
            code_variables = locals()
            vars = ["loc", "co", "st", "fields", "line", "cmd"]
            for var in vars:
                del code_variables[var]
            # Now add these to the global dictionary
            g = globals()
            for varname in code_variables.keys():
                g[varname] = code_variables[varname]
        elif cmd == "cd":
            if len(fields) > 1:
                os.chdir(fields[1])
                Log(f"chdir to {fields[1]!r}")
            else:
                os.chdir(start_dir)
                Log(f"chdir to {start_dir!r}")
        elif cmd[0] == "#":     # It's a comment - ignore it
            Log(f"Got a comment line")
        elif cmd[0] == "{":     # It's the start of a comment block
            in_comment_block = True
            Log(f"Entered a comment block")
        elif cmd[0] == "}":     # It's the end of a comment block
            in_comment_block = False
            Log(f"Exited a comment block")
        elif cmd == "on":
            try:
                if len(fields) > 1:  # Argument given
                    output_on = bool(eval(fields[1], globals(), localvars))
                else:
                    output_on = True
            except Exception as e:
                breakpoint()
                Error(f"Bad expression in line {current_line} of file {current_file!r}'\n  {e}")
        elif cmd == "off":
            if len(fields) > 1:  # Argument given
                output_on = not bool(eval(fields[1], globals(), localvars))
            else:
                output_on = False
        elif cmd == "include":
            if len(fields) < 2:
                Error("Bad include in line %d of file '%s':  missing file" %
                    (current_line, current_file))
            file = FindIncludeFile(fields[1])
            if len(fields) > 2:
                once = True
                if fields[2] != "once":
                    Error("Bad include in line %d of file '%s':  third "
                        "token must be 'once'" % (current_line, current_file))
            else:
                once = False
            if file == "":
                Error("Error:  include file '%s' in line %d of file '%s' "
                    "not found" % (fields[1], current_line, current_file))
            if file in included_files:
                Error("Error:  include file '%s' in line %d of file '%s' "
                    "already included" % (fields[1], current_line, current_file))
            ProcessFile(file, 0, current_line, current_file)
            included_files[file] = 0
        elif cmd == "sinclude":
            if len(fields) != 2:
                Error("Bad sinclude in line %d of file '%s'" %
                    (current_line, current_file))
            file = FindIncludeFile(fields[1])
            ProcessFile(file, 1, current_line, current_file)
        else:
            Error("Command '%s' on line %d of file '%s' not recognized" %
                (cmd, current_line, current_file))
    def FindIncludeFile(file):
        '''Search for the indicated file to include and return it; if not
        found, return None.
        '''
        p = P(file)
        if p.is_file():
            return p.resolve()
        for dir in d["-I"]:     # Search include directories
            p = P(dir)/file
            if p.is_file():
                return p.resolve()
        return None
    def IsCommandLine(line):
        'This function returns True if the line is a command line'
        # Note if we're in code mode, the line is also considered a
        # command.  Commands aren't printed to the output stream.
        return True if line[0] == cmd_char or code_mode else False
    def ExpandMacros(line):
        '''We look for any macro name matches.  Any that are found are
        replaced, then we start the search over again so we don't miss
        any macros within macros.
        '''
        done = False
        while not done:
            found = False  # Flags finding at least one macro
            for macro in macro_names:
                pos = line.find(macro)
                if pos != -1:
                    # Found a macro name in the line
                    found = True
                    old_value = macro
                    new_value = macros[macro][0]
                    line = line.replace(old_value, new_value)
                    break
            if not found:
                done = True
        # If current_code is not the null string, we've had at least one
        # code section, so evaluate using the global variables.  We'll only
        # do this if the line has at least one formatting string of the
        # form %(varname)X, where varname is the name of a global variable
        # and X is s, d, etc.
        if current_code:
            mo = need_global_expansion.search(line)
            if mo:
                line = line % globals()
        return line
    def ProcessLine(line, linenum):
        '''Determine if the line is a command line or not.  If it is, process
        it with ProcessCommandLine().  Otherwise, expand the macros in the
        line and print it to stdout.
        '''
        if IsCommandLine(line):
            Log(f"{t.ln}[{linenum}]{t.cmd} {line}", t.cmd)
            ProcessCommandLine(line)
        else:
            if output_on:
                if not in_comment_block:
                    Log(f"{t.ln}[{linenum}]{t.line} {line}", t.line)
                    Output(line)
                else:
                    Log(f"{t.ln}[{linenum}]{t.line} In comment block: {line!r}", t.line)
    def Output(line):
        '''Send the line to the output stream.  First, expand all the macros
        in the line.  Then check the character before the trailing newline:
        if it is a '\' character, remove the newline unless the character
        before that is another '\', in which case substitute '\' for the
        '\\' and keep the newline.
        '''
        line = RmNl(ExpandMacros(line))
        if len(line) < 2:
            print(line)
            return
        if line[-2] == '\\':
            # Second to last character is a backslash
            if len(line) > 2:
                # If the character before the last backslash is a backslash,
                # just output the line as is.
                if line[-3] == "\\":
                    print(line)
                else:
                    # It's an escaped backslash, so chop off the newline
                    print(line[:-2])
            else:
                # It's just a backslash and a newline.
                return
        else:
            print(line)
    def ProcessFile(file, ignore_failure_to_open=0, restore_line=0,
                    restore_file=""):
        '''Read in and process each line in the file.  The
        ignore_failure_to_open variable is used to handle the sinclude case
        when a file is missing or can't be opened.

        If present, restore_line and restore_file are used to reset the
        current_line and current_file global variables, since we're in a
        recursive call from include or sinclude commands.
        '''
        try:
            ifp = open(file)
        except Exception:
            if ignore_failure_to_open:
                return
            else:
                Error("Couldn't open file '%s' for reading" % file)
        Log(f"===== Started processing file {t.fn}{file!r}{t.N} =====")
        line = ifp.readline()
        current_file = file
        current_line = 1
        while line:
            ProcessLine(line, current_line)
            line = ifp.readline()
            current_line = current_line + 1
        ifp.close()
        if restore_line:
            current_line = restore_line
        if restore_file:
            current_file = restore_file
        Log(f"===== Finished processing file {t.fn}{file!r}{t.N} =====")
if __name__ == "__main__":
    d = {}      # Options dictionary
    ColorCoding()   # Make sure t's attributes are defined
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
