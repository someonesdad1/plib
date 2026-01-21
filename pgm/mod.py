'''
Finds files modified within a specified time frame

  TODO:
  
    - Use a mod_ignore file that uses regexps to define files/directories to ignore.  For example,
      I don't care to see things like files that end with `~` or have 'lock' in them, nor do I
      want to see git or hg directories.
    - The -l option should use color instead of spacing to print out the ages.  Currently, a long
      filename can cause inconveniently long lines that are hard to read.  Or add the -L option to
      use color.
    - There are numerous searches that one might like to make:
        - Find files that last changed at the date D +/- t.  Let the date be defined in various
          ways:
            - Jan8,2015-3:10:14
            - 8Jan2015-3:10:14
            - 8Jan2015-3:10:14
            - 20150108-3:10:14
            - 1/8/15-3:10:14
            - 1/8/2015-3:10:14
        - The last two forms need an option to let you use D/M/Y if you wish.
        - The above form using a hyphen might not be desired because you'd want to use it to
          indicate an interval.  For example, you could specify the time parameter as
          '8Jan2015-16Jan2015' to designate an interval.
    - Look at man stat for some other info to use.  atime is last access, mtime is last mod time,
      ctime is last owner/group/perm change on UNIX (creation time on Windows).
    - Thus there might be two searches:  modification time and access time.
    - Use -s option with letter:  a, c, or m
    
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2011, 2016 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Finds files modified within a specified time frame
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from pathlib import Path as P
        import sys
        import os
        import os.path
        import getopt
        import time
        import re
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.default_time = "1w"
if 1:  # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        name = sys.argv[0]
        short_name = os.path.split(name)[1]
        dt = g.default_time
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [age [dir [dir2...]]]
          Print out changed files younger than the given age in the indicated
          directories.  age is a number with an optional letter suffix:
              s   seconds       M   minutes         h   hours
              w   weeks         m   months          y   years
              d   days [default]                    i   infinite time in past
          age can contain a hyphen specifying a time interval to which the printed files
          must belong (example: '1y-2y' means the file changed between 1 and 2 years
          ago).
            
        Options
            -c  Include commonly-named files (.vi, *.pyc, etc.)
            -d  Turn debug printing on (see how files/directories are processed)
            -H  Show some examples of use
            -l  Decorate output with time since last change
            -m  Include ignored directories (repositories, etc.)
            -n  Show files that have not changed
            -p  Do not ignore picture files
            -r  Recurse into subdirectories
            -t  Sort the output names by age (most-recently changed last)
            -w  Make names case insensitive (for Windows)
            -x regexp    Ignore files that match regexp (more than one -x OK)
        '''))
        exit(status)
    def Examples():
        print(dedent(f'''

        Certain files and directories are ignored (see the default containers in the
        ParseCommandLine() function).  For example, common version control repository
        directories such as .hg, .git, and .bzr are ignored.  Files like object files,
        swap files, etc. are ignored.  Typical picture file extensions like .bmp, .jpg,
        etc. are ignored unless you use the -p option.

        Some examples (mydir is the mydirectory to search):

        - Find all files
            'i mydir'       Use '-t i mydir' to see most recent last
            '-r i mydir'    to recursively descend into mydir
        - Find files that changed in the last week
            '1w mydir'
        - Find files that changed between one and two weeks ago:
            '1w-2w mydir'    or    '2w-1w mydir'
        - Find files that changed more than 1 week ago:
            '1w-i mydir'    or     'i-1w mydir'
        - Find files that didn't change more than 1 week ago:
            '-n 1w-i mydir'
        '''))
    def ParseCommandLine():
        d["-c"] = False     # Include commonly-named files (.vi, *.pyc, etc.)
        d["-d"] = False     # Turn debug printing on (see how files/directories are processed)
        d["-l"] = False     # Decorate output with time since last change
        d["-m"] = False     # Include ignored directories (repositories, etc.)
        d["-n"] = False     # Show files that have not changed
        d["-p"] = True      # Do not ignore picture files
        d["-r"] = False     # Recurse into subdirectories
        d["-t"] = False     # Sort the output names by age (most-recently changed last)
        d["-w"] = False     # Make names case insensitive (for Windows)
        d["-x"] = []        # Ignore files that match regexp (more than one -x OK)
        # Edit the following containers as needed
        s = '''.hg .git .bzr .cache .mozilla __pycache__ .local tmp-donp-linux
            .ruff_cache .cache .bup .gnupg .conda .local .ssh .vimbup '''.split()
        d["directories_to_ignore"] = set(s)
        d["picture_extensions"] = set(('''
            .bmp .dib .emf .eps .gif .ipc .ipk .j2c .j2k .jif .jp2 .jpeg
            .jpg .pbm .pct .pgm .pic .png .ppm .ps .psp .pspframe .pspimage
            .pspshape .psptube .svg .tif .tiff .tub .xbm .xpm
        '''.split()))
        # Regular expressions for common files that should be ignored
        d["common_files"] = set((
                re.compile(r"^\.vi$", re.I),
                re.compile(r"^\.z$", re.I),
                re.compile(r"^.*\.swp$", re.I),
                re.compile(r"^log$", re.I),
                re.compile(r"^tags$", re.I),
                re.compile(r"^[abz]$", re.I),
                re.compile(r"^.*\.pyc$", re.I),
                re.compile(r"^.*\.pyo$", re.I),
                re.compile(r"^.*\.o$", re.I),
                re.compile(r"^.*\.obj$", re.I),
                re.compile(r"^.*cache$", re.I),
        ))
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "cdhlmnprtx:")
        except getopt.GetoptError as e:
            print(str(e))
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "cdlmnprtw":
                d[o] = not d[o]
            if o == "-h":
                Usage(0)
            elif o == "-x":
                d["-x"].append(a)
        if not args:
            if 0:
                args = [g.default_time, "."]  # Default age and directory
            else:
                # Don't allow a default so usage is seen with no args
                Usage(1)
        elif len(args) == 1:
            args.append(".")  # Default directory
        # Compile any regular expressions
        for i, r in enumerate(d["-x"]):
            try:
                d["-x"][i] = re.compile(r)
            except re.error:
                Error("'{}' is a bad regexp".format(r))
                exit(1)
        if d["-d"]:  # Debug print the settings
            g.dbg = t.dbg = True
            GetColors()
            for key in sorted("-n now -t -w -m -p -l -x -r -c".split()):
                if key == "now":
                    Dbg("  {} =".format(key), d[key], "s since 1 Jan 1970")
                else:
                    Dbg("  {} =".format(key), d[key])
        GetColors()
        return args
if 1:  # Core functionality
    def GetTime(age):
        '''age is a string representing a number (integer or floating point)
        with an optional letter suffix or a time interval separated by a
        hyphen.  Return the tuple (start, end) representing this age; if no
        hyphen is present, (start,) will be returned.  Examples:
        
            age     Returned
           ------   --------
            1s      (1,)
            1       (24*3600,)          # Default unit of days
            1d      (24*3600,)
            1d-2d   (24*3600, 2*24*3600)
            2d-1d   (24*3600, 2*24*3600)
            i       (10000000000.0,)    # Note default coefficient of 1
        'i' is intended to represent an infinite time in the past.
        '''
        digits, days_per_year, s_per_hr = "1234567890", 365.25, 3600
        s_per_day = 24 * s_per_hr
        age = age.strip()
        if not age:
            Usage(1)
        suffixes = {
            "s": 1,
            "S": 1,
            "M": 60,
            "h": s_per_hr,
            "H": s_per_hr,
            "d": s_per_day,
            "D": s_per_day,
            "w": 7 * s_per_day,
            "W": 7 * s_per_day,
            "m": days_per_year / 12 * s_per_day,
            "y": days_per_year * s_per_day,
            "Y": days_per_year * s_per_day,
            "i": inf,
            "I": inf,
        }
        fmt = "'{}' is a bad age specification"
        def Translate(a):
            '''Convert the age a to a time in seconds.  The form is [n][s]
            where n is a number (defaults to 1) and s is a character
            indicating a time unit (defaults to 'd').
            '''
            a = a.strip()
            if not a:
                Error("Empty age specification in '{}'".format(age))
            if len(a) == 1 and a[-1] in suffixes:
                a = "1" + a  # Implied 1
            if a[-1] in digits:  # No letter suffix
                a += "d"
            elif a[-1] not in suffixes:
                Error("'{}' is an illegal time suffix".format(a[-1]))
            try:
                t = float(a[:-1]) * suffixes[a[-1]]
            except ValueError:
                Error(fmt.format(a))
            return t
        # ---------------------
        if "-" in age:
            f = age.split("-")
            if len(f) != 2:
                Error(err)
            start, end = [Translate(i) for i in f]
            return (start, end) if start <= end else (end, start)
        else:
            return (Translate(age),)
    def ShouldBeIgnored(name):
        '''Check against the to-be-ignored regular expressions.'''
        for regexp in d["common_files"]:
            if regexp.match(name):
                return True
        return False
    def IgnoreThisFile(file):
        '''If the indicated file is a picture file (indicated by its extension)
        or it matches one of the -x regular expressions, return True.
        Otherwise, return False.
        '''
        # file is a pathlib.Path instance
        if not d["-c"]:     # Include common files (.vi, *.pyc, etc.)
            name = file.name.lower if d["-w"] else file.name
            if ShouldBeIgnored(name):
                return True
        if d["-x"]:         # Ignore if the file matches a regex
            for r in d["-x"]:
                if r.search(str(file)):
                    return True
        if d["-p"]:         # Don't ignore picture files
            ext = file.suffix.lower if d["-w"] else file.suffix
            if ext in d["picture_extensions"]:
                return True
        return False
    def FmtTimeDiff(td):
        '''Return s, minutes, hours, days, weeks, months, years for
        a time difference td in seconds.
        '''
        fmt, s = "{}{:.1f} {}", " " * 2
        if abs(td) < 60:
            return fmt.format(s * 0, td, "s")
        td /= 60
        if abs(td) < 60:
            return fmt.format(s * 1, td, "min")
        td /= 60
        if abs(td) < 24:
            return fmt.format(s * 2, td, "hr")
        td /= 24
        if abs(td) < 7:
            return fmt.format(s * 3, td, "days")
        td /= 7
        if abs(td) < 30:
            return fmt.format(s * 4, td, "wk")
        td /= 4
        if abs(td) < 12:
            return fmt.format(s * 5, td, "mo")
        td /= 12
        return fmt.format(s * 6, td, "yr")
    def IgnoreDirectory(*components):
        '''Return True if one of the elements of the list components is a
        directory to ignore.
        '''
        for i in components:
            if d["-w"]:
                if i.lower() in d["directories_to_ignore"]:
                    return True
            else:
                if i in d["directories_to_ignore"]:
                    return True
        return False
    def ProcessFile(file):
        'For file, determine if it has changed in the indicated age interval'
        Dbg(f"Processing file {str(file)}")
        now = d["now"]
        age0 = 0
        if len(d["age_interval"]) == 1:
            age1 = d["age_interval"][0]
        else:
            age0, age1 = d["age_interval"]
        Dbg("  age0, age1 =", age0, age1)
        if IgnoreThisFile(file):
            Dbg("  ", file, "--> ignored")
            return None
        try:
            t = last_change_time = os.stat(file).st_mtime
            age = now - t
            in_interval = age0 <= age <= age1
            if d["-n"] and not in_interval:
                Dbg("  ", file, "not in interval")
                return (age, file)
            elif not d["-n"] and in_interval:
                Dbg("  ", file, "in interval")
                return (age, file)
        except Exception:
            Dbg("  Exception on file '{}'".format(file))
            return None
    def ProcessDirectory(dir):
        'Return a list of (age_in_s, file) to process at and below dir'
        pattern = "**/*" if d["-r"] else "*"
        results = []
        for file in dir.glob(pattern):
            if IgnoreDirectory(*file.parts) and not d["-m"]:
                continue
            result = ProcessFile(file)
            if result is not None:
                results.append(result)
        return results
    def PrintReport(results):
        'results = ([age_in_s, file], ...)'
        # Each file is a pathlib.Path instance
        if d["-t"]:
            results = sorted(results, reverse=True)
        if not results:
            return
        maxlen = max([len(str(file)) for age, file in results])
        for age_s, file in results:
            if d["-l"]:
                age_str = FmtTimeDiff(age_s) if d["-l"] else ""
                n = maxlen - len(str(file))
                print(str(file), " "*n, age_str)
            else:
                print(str(file))

if __name__ == "__main__":
    nl, inf = "\n", 1e20  # inf is infinite time into the past
    d = {}  # Options dictionary
    d["now"] = time.time()
    args = ParseCommandLine()
    d["age_interval"] = GetTime(args[0])
    results = []    # Container of (age_in_s, file) items
    for dir in args[1:]:
        results.extend(ProcessDirectory(P(dir)))
    PrintReport(results)
    if d["-t"]:
        t.print(f"{t.purl}Most recent file is last", file=sys.stderr)
    else:
        t.print(f"{t.purl}File order is that encountered in tree traverse", file=sys.stderr)
