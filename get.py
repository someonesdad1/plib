'''
TODO:  
    - See if GetLines and GetLines1 can be combined
    - Add number kw to GetLines which then causes a list of tuples
      (linenum, str) to be returned
    - Add Zn to GetNumbers
    - Change GetFraction to also handle integers

Module for a) getting data from files, strings, and streams, b) getting
numbers interactively from user.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Module for getting data from files, strings, and
        # streams.  An example is reading a text file, getting all the lines
        # except for those that match a sequency of regular expressions.
        # Other examples are getting all the words (tokens) from a file or a
        # set of numbers.  Handles a number of common programming tasks.
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        import locale
        import pathlib
        import re
        import string
        import sys
        from collections import defaultdict, deque
        from collections.abc import Iterable
        from io import StringIO
        from fractions import Fraction
    # Custom imports
        import u
        from f import flt
        from asciify import Asciify
        try:
            from uncertainties import ufloat, ufloat_fromstr, UFloat
            have_unc = True
        except ImportError:
            have_unc = False
        try:
            from f import flt, cpx
            have_f = True
        except ImportError:
            have_f = False
        try:
            from mpmath import mpf, mpc
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    # Global variables
        P = pathlib.Path
        ii = isinstance
        # For Tokenize
        letters = set(string.ascii_letters)
        others = set(
            "žŽżŻźŹŸŷŶŵŴųŲűŰůŮŭŬūŪũŨŧŦťŤţŢšŠşŞŝŜśŚřŘŗŖŕŔőŐŏŎōŌŋŊŉňŇņŅńŃ"
            "łŁŀĿľĽļĻĺĹĸķĶĵĴıİįĮĭĬīĪĩĨħĦĥĤģĢġĠğĞĝĜěĚęĘėĖĕĔēĒđĐďĎčČċĊĉĈć"
            "ĆąĄăĂāĀÿþýüûúùøöõôóòñðïîíìëêéèçæåäãâáàßÞÝÜÛÚÙØÖÕÔÓÒÑÐÏÎÍÌË"
            "ÊÉÈÇÆÅÄÃÂÁÀ")
        __all__ = '''
            GetText GetLines1 GetLines GetTextLines GetLine GetNumberedLines GetBinary
            GetNumber GetNumber GetNumberArray GetFraction ParseUnit ParseUnitString GetComplex
            GetChoice
            GetWords GetTokens GetWordlist wrd pnc Tokenize
            IsPunctuation GetWireDiameter GetFileSize
        '''.split()
if 1:   # Getting text, lines, bytes
    def GetText(thing, enc=None):
        '''Return text from thing, which is
            string      It's a file name.  If read exception, then use string
                        itself for the text. "-" means to read stdin.
            bytes       
            stream
        If enc is not None, then it's the encoding to read the file and it is
        read as binary.  enc is ignored for stdin.
        '''
        if ii(thing, bytes):            # Bytes
            s = thing.decode(encoding="UTF-8" if enc is None else enc)
        elif ii(thing, pathlib.Path):   # It's a path, so read its text
            s = thing.read_text(encoding=enc) if enc else thing.read_text()
        elif ii(thing, str):            # It's a file name or string
            try:
                if thing == "-":
                    s = sys.stdin.read()    # enc is ignored
                else:
                    p = pathlib.Path(thing)
                    s = p.read_text(encoding=enc) if enc else p.read_text()
            except Exception:
                s = thing               # It's a string
        elif hasattr(thing, "read"):    # It's a stream
            s = thing.read()
        else:
            raise TypeError("Type of 'thing' not recognized")
        return s
    if 0:   # Phase out if nothing breaks
        def GetLines1(thing, enc=None, ignore=None, script=False, ignore_empty=False, strip=False, nonl=False):
            r'''Return text from thing, which is
                string      It's a file name.  If get a read exception, then
                            use string itself for the text.
                bytes       
                stream
             If enc is not None, then it's the encoding to read the file and it is
             read as binary.  Keywords are (for bool (b), action is if True):
            
                nonl          b If True, remove trailing newline
                script        b If True, ignore comment lines
                strip         b If True, strip off whitespace from each line.  If
                              strip is True, it also implies nonl is True, even if
                              it is set False.
                ignore_empty  b If True, ignore empty (whitespace only) lines
            
                ignore          Either None or a sequence of strings that are 
                                compiled to regular expressions and are lines
                                that are to be ignored.
            
                If you want to use strip or script as True, then you must also set
                ignore to the empty list.
        
                Example:
                    s = """# Comment
                    ## Another comment
                    Line 1
                        Line 2
                    """
                    r = [r"^\s*#"]
                    lines = GetLines(s, ignore=r)
                    print(f"lines {list(lines)}")
                outputs 
                    lines ['Line 1', '    Line 2', '']
                The call GetLines(s, script=True) does the same thing.
            '''
            def Filter(line):
                if ignore is None:
                    return True
                for r in ignore:
                    if re.search(r, line):
                        return False     # Don't keep this line
                return True     # Keep this line
            if (ignore is not None and (ii(ignore, str) or 
                not ii(ignore, Iterable))):
                raise TypeError("ignore must be an iterable")
            if script and ignore is not None:
                ignore.append(r"^\s*#")
            if ignore_empty and ignore is not None:
                ignore.append(r"^\s*$")
            got = GetText(thing, enc=enc)
            if ii(got, bytes):
                if enc:
                    lines = got.decode(enc).split("\n")
                else:
                    lines = got.decode().split("\n")
            elif ii(got, str):
                lines = got.split("\n")
            else:
                raise TypeError("GetText() didn't return bytes or string")
            if not nonl:
                lines = [i + "\n" for i in lines]   # Add back newlines to each line
            lines = list(filter(Filter, lines))
            if strip:
                lines = [i.strip() for i in lines]
            return lines
    def GetLines(thing, enc=None, ignore=[], script=False, ignore_empty=False, strip=False, nonl=False):
        r'''Return text from thing, which is
            string      It's a file name.  If get a read exception, then
                        use string itself for the text.  "-" means stdin.
            bytes       
            stream
         If enc is not None, then it's the encoding to read the file and it is
         read as binary.  Keywords are (for bool (b), action is if True):
        
            nonl          b If True, remove trailing newline
            script        b If True, ignore comment lines
            strip         b If True, strip off whitespace from each line.  If
                            strip is True, it also implies nonl is True, even if
                            it is set False.
            ignore_empty  b If True, ignore empty (whitespace only) lines
        
            ignore          A list of strings that are compiled to regular
                            expressions and are lines that are to be ignored.
        
            Example:
                s = """# Comment
                ## Another comment
                Line 1
                    Line 2
                """
                r = [r"^\s*#"]
                lines = GetLines(s, ignore=r)
                print(f"lines {list(lines)}")
            outputs 
                lines ['Line 1', '    Line 2', '']
            The call GetLines(s, script=True) does the same thing.
        '''
        def Filter(line):
            if not ignore:
                return True
            for r in ignore:
                if re.search(r, line):
                    return False     # Don't keep this line
            return True     # Keep this line
        if not ii(ignore, (list, tuple)):
            raise TypeError("ignore must be a list or tuple")
        if script:
            ignore.append(r"^\s*#")
        if ignore_empty:
            ignore.append(r"^\s*$")
        got = GetText(thing, enc=enc)
        if ii(got, bytes):
            if enc:
                lines = got.decode(enc).split("\n")
            else:
                lines = got.decode().split("\n")
        elif ii(got, str):
            lines = got.split("\n")
        else:
            raise TypeError("GetText() didn't return bytes or string")
        if not nonl:
            lines = [i + "\n" for i in lines]   # Add back newlines to each line
        lines = list(filter(Filter, lines))
        if strip:
            lines = [i.strip() for i in lines]
        return lines
    def GetTextLines(thing):
        '''This is a convenience instance of GetLines with the keywords:
            script = True
            ignore_empty = True
            strip = True
            nonl = True
        This is because a common use case in a script is a multi-line string
        containing a data table that's e.g. tab-separated.
        '''
        return GetLines(thing, script=True, ignore_empty=True, strip=True,
                        nonl=True)
    def GetLine(thing, enc=None):
        '''Similar to GetLines, but is a generator so it gets a line at a time.
        thing can be a string, bytes, or a stream.  If it is a string, it's
        assumed to be a file name; if trying to read the file generates an
        exception, the string itself is used as the text.
    
        If it is a bytes object, then the indicated encoding is used to
        decode it, then it's read a line at a time.
        '''
        if ii(thing, bytes):  # Bytes
            s = thing.decode(encoding="UTF-8" if enc is None else enc)
            stream = StringIO(s)
        elif ii(thing, (str, pathlib.Path)):  # File name
            p = pathlib.Path(thing)
            try:
                stream = open(p)
            except Exception:
                stream = StringIO(thing)
        elif hasattr(thing, "read"):  # Stream
            stream = thing
        else:
            raise TypeError("Type of 'thing' not recognized")
        line = stream.readline()
        while line:
            yield line
            line = stream.readline()
    def GetNumberedLines(thing, enc=None):
        '''Return a tuple of (linenum, line_string) tuples where linenum is
        the line number in the file.  See GetText for details on the enc
        argument.
        '''
        lines = GetText(thing, enc=enc).split("\n")
        return tuple((i + 1, j) for i, j in enumerate(lines))
    def GetBinary(thing, encoded=False):
        '''Read in thing as binary (thing is a stream or filename).  Bytes
        will be returned.
        
        If encoded is True, then try to decode it by using a number of 
        encodings.  A string will be returned if it can be decoded.
        '''
        # See ConstructEncodingData in /pylib/enc.py, as it gives the
        # frequency of these encodings found on web pages.
        encodings = '''
            utf_8 latin_1 cp1251 cp1252 shift_jis gb2312 euc_kr euc_jp
            iso8859_2 gbk cp1250 big5 iso8859_9 iso8859_15
        '''.split()
        if encoded:
            try:
                s = thing.read()
            except AttributeError:
                s = open(thing, "rb").read()
            if ii(s, str):
                return s
            # Got bytes; try to decode them
            for encoding in encodings:
                try:
                    return s.decode(encoding)
                except UnicodeDecodeError:
                    pass
            raise ValueError("'thing' could not be decoded")
        else:
            try:
                return thing.read()
            except AttributeError:
                return open(thing, "rb").read()
if 1:   # Getting numbers
    def GetNumber(prompt_msg, **kw):
        '''General-purpose routine to get a number from the user with the
        prompt msg.  These are the things that can be returned:
            
            number                      use_unit is False
            (number, unit_string)       use_unit is True
            True or False               inspect is True
            None                        default = None and allow_none = True
    
        The returned number type will be numtype.  Examples:
    
            a_float = GetNumber(prompt_msg)
            an_integer = GetNumber(prompt_msg, numtype=int)
            a_flt = GetNumber(prompt_msg, numtype=flt)
            a_UFloat = GetNumber(prompt_msg, use_unc=True)
    
        The user can utilize python expressions in the input; the math 
        library's functions are in scope.
    
        If you wish to restrict the allowed values of the number, use the
        following keyword arguments (default values are in square brackets):
    
            numtype     Number type [flt].  Use int if you want the number to
                        be an integer.  You can use a number type as long as it
                        obeys the required ordering semantics and the
                        constructor returns a number object that raises a
                        ValueError if the initializing string is of improper
                        form.  For an example, see the use of mpmath's mpf
                        numbers in the unit tests.
    
            default     Default value.  This value will be returned if
                        the user just presses the return key when prompted.
                        Note the default value of None will cause an exception
                        unless the keyword allow_none is True.  [None]
 
            allow_none  If True, allows None to be returned as the default.
                        [False]
    
            low         Lowest allowed value.  [None]
    
            high        Highest allowed value.  [None]
    
            low_open    Boolean; if True, then the low end of the acceptance
                        interval is open.  [False]
    
            high_open   Boolean; if True, then the high end of the acceptance
                        interval is open.  [False]
    
            invert      If true, the value must be in the complement interval.
                        This is used to allow numbers except those in a
                        particular range.  See note below.
    
            outstream   Stream to print messages to.  [stdout]
    
            instream    Stream to get input from (intended for unit tests).
    
            prefix      Prefix string for error messages
                            ["Error:  must have "]
    
            use_unc     If true, lets you use number strings that can be
                        interpreted by the python uncertainties library.
                        If use_unit is true, then all units must be
                        separated from the uncertain number string by one or
                        more spaces (i.e., no cuddled units).  Note:  if you
                        use a number string like '9 m' and use_unc is True,
                        then the returned number will be 9+/-1, which is the
                        default interpretive behavior of the uncertainties
                        library's ufloat_fromstr() function.  The following
                        strings mean the same number and uncertainty:
                        "4.2+/-0.4", "4.2+-0.4", "4.2(4)".  [False]
    
            use_unit    If true, allows a unit to be included in the string.
                        The return value will be a tuple of (number,
                        unit_string).  [False]
    
            allow_quit  If true, "Q" or "q" quits the program.  [True]
    
            inspect     If not None, it's a string that should be
                        inspected to see if it meets the requirements.  If
                        it does, True will be returned; otherwise, False
                        is returned.
    
            vars        Dictionary to use as locals to evaluate expressions.
    
        Note:  if you call
    
            GetNumber("", low=a, high=b)
    
        the number returned will be the number in the closed interval [a, b].
        If you make the same call but with invert set to True
    
            GetNumber("", low=a, high=b, invert=True)
    
        then the returned number must lie in the union of the open intervals
        (-inf, a) and (b, inf); this set of numbers is the complement of the
        previous call's.  If you make the call
    
            GetNumber("", low=a, high=b, low_open=True, high_open=True)
    
        the number returned will be in the open interval (a, b).  If this is
        inverted by setting invert to True as in
    
            GetNumber("", low=a, high=b, low_open=True,
                    high_open=True, invert=True)
    
        then you'll get a number returned in the union of the half-closed
        intervals (-inf, a] and [b, inf).  A programmer might be confused
        by the fact that the intervals were half-closed, even though the
        settings low_open and high_open were used, implying the programmer
        wanted open intervals.  The way to look at this is to realize that
        if invert is True, it changes an open half-interval to a closed
        half-interval.  I chose to make the function behave this way
        because it's technically correct.  However, if this behavior is
        not to your liking, it's easy to change by changing the
        conditional statements in the conditionals dictionary.  (I debated
        as to whether I should make this function an object instead; then
        this could be done by subclassing rather than changing the
        function.  But the convenience of a simple function won out.)
        '''
        outstream = kw.get("outstream", sys.stdout)
        instream = kw.get("instream", None)
        numtype = kw.get("numtype", flt)
        default = kw.get("default", None)
        low = kw.get("low", None)
        high = kw.get("high", None)
        low_open = kw.get("low_open", False)
        high_open = kw.get("high_open", False)
        inspect = kw.get("inspect", None)
        invert = kw.get("invert", False)
        prefix = kw.get("prefix", "Error:  must have ")
        use_unc = kw.get("use_unc", False)
        use_unit = kw.get("use_unit", False)
        allow_quit = kw.get("allow_quit", True)
        allow_none = kw.get("allow_none", False)
        vars = kw.get("vars", {})
        Debug = kw.get("Debug", None)
        # If the variable Debug is defined and True, then we
        # automatically return the default value.
        if Debug:
            return default
        if (low is not None) and (high is not None):
            if low > high:
                raise ValueError("low must be <= high")
            if default is not None and not (low <= numtype(default) <= high):
                raise ValueError("default must be between low and high")
        if invert and low is None and high is None:
            raise ValueError("low and high must be defined to use invert")
        if inspect is not None and not isinstance(inspect, str):
            raise ValueError("inspect must be a string")
        out = outstream.write
        # The following dictionary is used to get conditionals for testing the
        # values entered by the user.  If a set of keywords is not in this
        # dictionary's keys, then it is considered a syntax error by the
        # programmer making a call to this function.  This dictionary is used
        # to both check the conditions as well as provide an error message back
        # to the user.
        conditionals = {
            # low     high   low_open  high_open  invert
            (True, False, False, False, False): "x >= low",
            (True, False, True, False, False): "x > low",
            (True, False, False, False, True): "x < low",
            (True, False, True, False, True): "x <= low",
            (False, True, False, False, False): "x <= high",
            (False, True, False, True, False): "x < high",
            (False, True, False, False, True): "x > high",
            (False, True, False, True, True): "x >= high",
            (True, True, False, False, False): "low <= x <= high",
            (True, True, True, False, False): "low < x <= high",
            (True, True, False, True, False): "low <= x < high",
            (True, True, True, True, False): "low < x < high",
            (True, True, False, False, True): "x < low or x > high",
            (True, True, True, False, True): "x <= low or x > high",
            (True, True, False, True, True): "x < low or x >= high",
            (True, True, True, True, True): "x <= low or x >= high",
        }
        unit_string = ""
        while True:
            if inspect is None:
                msg = f"{prompt_msg}"
                msg += f" [{default}] " if default is not None else ""
                if outstream != sys.stdout:
                    out(msg)
                if instream is not None:
                    s = instream.readline()
                    if not s:
                        if default is None:
                            if allow_none:
                                return None
                            else:
                                # This should only be seen during testing.
                                raise RuntimeError("Empty input!")
                        else:
                            if use_unit:
                                return (numtype(default), "")
                            else:
                                return numtype(default)
                else:
                    # This form allows you to use readline:  execute 
                    # 'readline.set_startup_hook(input)' and the following
                    # input call will use readline's facilities.
                    s = input(msg).strip()
            else:
                s = inspect
            if not s:
                if default is None:
                    if allow_none:
                        return None
                    else:
                        raise ValueError("Default value not defined")
                else:
                    if inspect is not None:
                        return True
                    if use_unit:
                        return (numtype(default), "")
                    else:
                        return numtype(default)
            if len(s) == 1 and s in "qQ" and allow_quit:
                exit(0)
            if use_unc and "+-" in s:  # Change 8+-1 to 8+/-1
                if not have_unc:
                    raise ValueError("Uncertainties library not available")
                s = s.replace("+-", "+/-")
            # Check to see if number contains a unit
            if use_unit:
                number_string, unit_string = u.ParseUnit(s, allow_unc=use_unc)
                s = number_string
            try:
                if use_unc:
                    if ii(s, str):
                        x = ufloat_fromstr(s)
                    else:
                        x = s   # It's already a uncertainties.core.Variable
                else:
                    # Note the use of eval lets the user type expressions in.
                    # The math module's symbols are in scope.
                    x = numtype(eval(s, globals(), vars))
            except ValueError:
                if inspect is not None:
                    return False
                if numtype == int:
                    out("'%s' is not a valid integer\n" % s)
                else:
                    out("'%s' is not a valid number\n" % s)
            else:
                if low is None and high is None:
                    if inspect is not None:
                        return True
                    if use_unit:
                        return (x, unit_string)
                    else:
                        return x
                # Check if this number meets the specified conditions; if it
                # does, return it.  Otherwise, print an error message on the
                # output stream and re-prompt the user.
                c = (low is not None, high is not None, low_open, 
                    high_open, invert)
                if c not in conditionals:
                    # Programmer mistake
                    raise ValueError('''Bad set of parameters to GetNumber:
        low       = {low}
        high      = {high}
        low_open  = {low_open}
        high_open = {high_open}
        invert    = {invert}
    
        For example, low and high must not be None.'''.format(**locals()))
                condition = conditionals[c]
                if not eval(condition):
                    if inspect is not None:
                        return False
                    # Test failed, so send error message to user
                    condition = condition.replace("x", "number")
                    condition = prefix + condition
                    condition = condition.replace("high", "{high}")
                    condition = condition.replace("low", "{low}")
                    out(condition.format(**locals()) + "\n")
                    # If instream is defined, we're testing, so just return.
                    if instream is not None:
                        return
                    continue
                # Got a good number, so return it
                if inspect is not None:
                    return True
                if use_unit:
                    return (x, unit_string)
                else:
                    return x
    def GetNumbers(thing, numtype=None, enc=None):
        '''Uses GetText() to get a string, then recognizes integers, floats,
        fractions, complex, and uncertain numbers in the string separated by
        whitespace and returns a list of these numbers.  If numtype is
        given, all found strings are converted to that type.
    
        If flt and cpx types are available (have_f is True), then floats
        and complex types are converted to these over float and complex, 
        respectively.
    
        If the uncertainties library is present, the ufloat type can be
        recognized.
        '''
        lst, dp = [], locale.localeconv()["decimal_point"]
        for s in GetText(thing, enc=enc).split():
            if numtype:
                lst.append(numtype(s))
            else:
                if have_unc and "+-" in s:
                    s = s.replace("+-", "+/-")
                if have_unc and ("+/-" in s or "(" in s or "±" in s):
                    x = ufloat_fromstr(s)
                elif "/" in s:
                    x = Fraction(s)
                elif "j" in s.lower():
                    x = cpx(s) if have_f else complex(s)
                elif dp in s or "e" in s.lower():
                    x = flt(s) if have_f else float(s)
                else:
                    x = int(s)
                lst.append(x)
        return lst
    def GetNumberArray(string, row=False, numtype=float):
        r'''Return a list of vectors gotten from the indicated multiline string.
        The numbers are separated on each line by whitespace.  If row is
        True, then the vectors are row vectors.  Lines in string matching
        the regular expression with '^\s*#' are ignored.  If string is empty or
        only whitespace, then [[]] is returned.  ValueError will be raised if a
        row contains a different number of elements than the others.
    
        Example:  
            If the string is 
                s = """
                1 2 3
                4 5 6
                """
            then GetNumberArray(s) returns [[1, 4], [2, 5], [3, 6]].
            GetNumberArray(s, row=True) returns [[1, 2, 3], [4, 5, 6]].
        '''
        if not string.strip():
            return [[]]
        strings = []
        # Put valid lines into strings
        for line in string.strip().split("\n"):
            if line.strip()[0] == "#":
                continue
            strings.append(line)
        nrows = len(strings)
        # Get number of columns and verify all rows have the same number of
        # columns
        cols = [i.split() for i in strings]
        ncols = len(cols[0])
        if not all([len(i) == ncols for i in cols]):
            raise ValueError(f"Not all rows have {ncols} elements")
        # Get number array
        A = []
        for myrow in strings:
            a = [numtype(i) for i in myrow.split()]
            A.append(a)
        if row:
            return A    # Return row vectors
        if ncols == 1 or nrows == 1:
            return A    # Special case of one column or row vector
        # Use transpose to return column vectors
        return [list(i) for i in zip(*A)]
    def GetFraction(s):
        '''Return a Fraction object if string s contains a '/' and can be
        interpreted as an improper or proper fraction or if it can be
        interpreted as an integer.  Otherwise return None.  The following
        forms are allowed:
    
            A   5/4     +5/4    -5/4
            B   1 1/4   +1 1/4  -1 1/4
            C   1-1/4   +1-1/4  -1-1/4
            D   1+1/4   +1+1/4  -1+1/4
        '''
        if "/" not in s:
            try:
                i = int(s)
                return Fraction(i, 1)
            except Exception:
                return None
        s = s.strip()
        try:
            neg = 1
            if s[0] == "+":
                s = s[1:]
            elif s[0] == "-":
                s = s[1:]
                neg = -neg
            s = s.replace("+", " ").replace("-", " ")
            ip = 0
            if " " in s:
                ip, s = s.split()
                ip = int(ip)
            n, d = s.split("/")
            return neg*(ip + Fraction(int(n), int(d)))
        except Exception:
            return None
    def ParseUnit(s):
        '''Assume the string s has a unit and possible SI prefix appended
        to the end, such as '123Pa', '123 Pa', or '1.23e4 Pa'.  Remove the
        unit and prefix and return the tuple (num, unit).  Note that two
        methods are used.  First, if the string contains one or more space
        characters, the string is split on the space and the two parts are
        returned immediately; an exception is raised if there are more
        than two portions.  The other method covers the case where the
        unit may be cuddled against the number.
        '''
        if " " in s:
            f = tuple(i.strip() for i in s.split())
            if len(f) != 2:
                raise ValueError("'%s' must have only two fields" % s)
            return f
        # The second method reverses the string and looks for unit
        # characters until a character that must be in the number is found.
        # This means that digit characters cannot be in the unit, so a unit
        # like "mmH2O" is not allowed.
        unit, num, num_chars, done = [], [], set("1234567890."), False
        for i in reversed(s):
            if done:
                num.append(i)
                continue
            if i in num_chars:
                num.append(i)
                done = True
            else:
                unit.append(i)
        return (''.join(reversed(num)), (''.join(reversed(unit))).strip())
    def ParseUnitString(x, allowed_units, strict=True):
        '''This routine will take a string x and return a tuple (prefix,
        unit) where prefix is a power of ten gotten from the SI prefix
        found in x and unit is one of the allowed_units strings.
        allowed_units must be an iterable container.  Note things are
        case-sensitive.  prefix will either be a float or an integer.
 
        Example:
            u = ["m", "in", "ft"]
            s = "mm"
            Then ParseUnitString(s, u) returns (0.001, "m").
    
        The typical use case is where ParseUnit() has been used to separate
        a number and unit.  Then ParseUnitString() can be used to parse the
        returned unit string to get the SI prefix actual unit string.
        Parsing of composite units (such as m/s) must take place outside
        this function.
    
        If strict is True, then one of the strings in allowed_units must
        be anchored at the right end of x.  If strict is False, then the
        strings in allowed_units do not have to be present in x; in this
        case, (1, "") will be returned.
        '''
        # Define the allowed SI prefixes
        si = {"y": -24, "z": -21, "a": -18, "f": -15, "p": -12, "n": -9,
            "u": -6, "μ": -6, "m": -3, "c": -2, "d": -1, "": 0, "da": 1, "h": 2,
            "k": 3, "M": 6, "G": 9, "T": 12, "P": 15, "E": 18, "Z": 21,
            "Y": 24}
        s = x.strip()  # Remove any leading/trailing whitespace
        # See if s ends with one of the strings in allowed_units
        unit = ""
        for u in allowed_units:
            u = u.strip()
            # The following can be used if a unit _must_ be supplied.
            # However, it's convenient to allow for a default unit, which
            # is handled by the empty string for the unit.
            #if not u:
            #    raise ValueError("Bad unit (empty or all spaces)")
            if u and s.endswith(u):
                unit = u
                break
        if not unit:
            if strict:
                raise ValueError(f"'{x}' did not contain an allowed unit")
            else:
                return (1, "")
        else:
            # Get right index of unit string
            index = s.rfind(unit)
            if index == -1:
                raise Exception("Bug in ParseUnitString() routine")
            prefix = s[:index]
            if prefix not in si:
                raise ValueError(f"'{prefix}' is not an SI prefix")
            return (10**si[prefix], unit)
    def GetComplex(s, typ=complex):
        '''Return a complex number from the string s.  If s does not
        represent a complex number, None is returned.  You can change the
        returned number type with typ.  The allowed forms of s are:
            1. i, +i, -i
            2. X+i, X-i
            3. Xi
            4. XYi
        where
            X is an integer or float with an optional leading sign
            Y is an integer or float with a mandatory leading sign
        '''
        if not ii(s, str):
            raise TypeError("Parameter s must be a string")
        u = s.lower().replace("j", "i")
        u = re.sub("\s*", "", u)    # Remove all whitespace
        if not u:
            return None
        if not u.endswith("i"):
            return None
        # Case 1.  i, +i, -i forms
        if u == "i" or u == "+i":
            return typ(0, 1)
        elif u == "-i":
            return typ(0, -1)
        # Case 2.  X+i, X-i forms
        if u.endswith("-i") or u.endswith("+i"):
            im = "-1j" if u.endswith("-i") else "+1j"
            u = u[:-2]
            assert(u)
            if have_mpmath and typ == mpc:
                return typ(u, im.replace("j", ""))
            else:
                return typ(u + im)
        # Remove the trailing 'i'
        u = u[:-1]
        # Get leading - sign
        minus = 1
        if u.startswith("+"):
            u = u[1:]
        elif u.startswith("-"):
            u = u[1:]
            minus = -1
        if not u:
            return None
        # Case 3 and 4 forms with no trailing i
        # 
        # u is now one or two numbers.  These numbers will be separated
        # by '+' or '-'.  Replace "e-" by "em" and "e+" by "e".  Remaining
        # string can then have only one "+" or "-"; split on it to get
        # real and imaginary parts.
        assert(u and u[0] not in "+-")
        u = u.replace("e-", "em")
        u = u.replace("e+", "e")
        p = u.count("+")
        m = u.count("-")
        if p > 1 or m > 1:
            return None
        # 3. Xi form 
        sgn = "-" if minus == -1 else "+"
        if not p and not m:
            u = u.replace("em", "e-")
            if have_mpmath and typ == mpc:
                return typ("0", f"{sgn}{u}")
            else:
                return typ(f"0{sgn}{u}j")
        assert((p and not m) or (not p and m))
        sp = "+" if p else "-"  # Character to split on
        r, i = u.split(sp)
        r = r.replace("em", "e-")
        i = i.replace("em", "e-")
        r = r if r else 0
        i = i if i else 0
        iminus = -1 if sp == "-" else 1
        z = f"{sgn}{r}{sp}{i}j"
        if have_mpmath and typ == mpc:
            return typ(f"{sgn}{r}", f"{sp}{i}")
        else:
            return typ(z)
if 1:   # Getting choices
    def GetChoice(seq, default=1, indent=None, col=False, instream=None,
                  outstream=None):
        '''Display the choices in seq with numbers and prompt the user for his
        choice.  Note the numbers are 1-based as displayed to the user, but the
        returned value of choice will be 0-based.  Return the choice_number.
 
        default     Default choice
        indent      String to indent printed choices
        col         If True, use Columnize to print the choices
 
        instream and outstream are used for testing and are passed to
        GetNumber().
        '''
        if not seq:
            raise ValueError("seq can't be empty")
        items, n = [], len(seq)
        for i, item in enumerate(seq):
            items.append("{}) {}".format(i + 1, str(item)))
        if col:
            for i in Columnize(items, indent=indent, sep=" "*3):
                print(i, file=outstream)
        else:
            s = "" if indent is None else indent
            for i in items:
                print(s, i, sep="", file=outstream)
        choice = GetNumber("Choice? ", numtype=int, default=default, 
                        low=1, high=n, instream=instream,
                        outstream=outstream)
        if choice is None:
            return (None, "")
        choice = int(choice) - 1
        return (choice, seq[choice])
if 1:   # Tokenizing
    def GetWords(thing, sep=None, enc=None, ignore=[]):
        '''Return a list of words separated by the string sep from the thing (see details for
        GetLines).  If sep is None, then the data are split on whitespace; otherwise, the newlines
        are replaced by sep, then the data are split on sep.  
 
        ignore is a sequence of regular expressions that indicate the lines to ignore.
        '''
        lines = GetLines(thing, ignore=ignore, nonl=True)
        if sep is not None:
            s = sep.join(lines)
            return sep.join(lines).split(sep)
        else:
            return ' '.join(lines).split()
    def GetTokens(*things, sep=None, enc=None):
        '''Similar to GetWords(), but this is a generator so that arbitrarily large sets of files
        or streams can be processed.
        '''
        for thing in things:
            for line in GetLine(thing, enc=enc):
                for token in line.split() if sep is None else line.split(sep):
                    yield token
    def GetWordlist(*files, case=None):
        '''The arguments can be a stream, filename, or string to parse.  Return a set of all the
        words in these files.
    
        This function is aimed at reading wordlists I use on my computer.  These will have comment
        lines beginning with '#' after stripping whitespace.  Then words are separated by
        whitespace and can be gotten at once on the whole file's string with strip().
    
        If case is None, do nothing with the words.  If it is "lower", change them to lower case;
        upper with "upper".
        '''
        words = set()
        for file in files:
            try:
                # See if it's a stream
                s = file.read()
            except Exception:
                try:
                    s = open(file).read()   # It's a file
                except FileNotFoundError:
                    s = file    # It's a string
            lines = []
            for line in s.split("\n"):
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                lines.append(line)
            s = ' '.join(lines)
            if case == "upper":
                s = s.upper()
            elif case == "lower":
                s = s.lower()
            words.update(set(s.split()))
        return words
    class wrd(str):
        def __new__(cls, value):
            return super(wrd, cls).__new__(cls, value)
    class pnc(str):
        def __new__(cls, value):
            return super(pnc, cls).__new__(cls, value)
    def Tokenize(s, wordchars=letters, otherchars=others, check=True, wordtype=wrd, punctype=pnc):
        '''Return a deque t that contains all the word tokens in the string s.  The tokenizing
        process is such that ''.join(t) is the same string as s (this is verified if check is
        True).  wordchars and otherchars must be sequences of letters (sets preferred) so that "in"
        works on detecting whether a letter is in the sequence.
    
        The returned deque is made up of non-empty strings of a) words with letters and b)
        non-letters.  These strings will be wordtype and punctype, respectively, which are derived
        from str.
    
        Example:  Tokenize("To be, or not to be:") returns
 
            deque(['To', ' ', 'be', ', ', 'or', ' ', 'not', ' ', 'to', ' ', 'be', ':'])
 
        The word tokens have isinstance(token, wrd) return True and the punctuation strings have
        isinstance(token, pnc) return True.
        '''
        def Handle(c, seq1, seq2, seq2type):
            seq1.append(c)
            if seq2:
                p = ''.join(seq2)
                if p:
                    out.append(seq2type(p))
                seq2.clear()
        inp, out, word, punc = deque(s), deque(), deque(), deque()
        while inp:
            c = inp.popleft()
            if c in letters or c in otherchars:
                Handle(c, word, punc, punctype)
            else:
                Handle(c, punc, word, wordtype)
        if word:
            out.append(wordtype(''.join(word)))
        if punc:
            out.append(punctype(''.join(punc)))
        if check:
            t = ''.join(out)
            if t != s:
                print(f"Orig:  {repr(s)}")
                print(f"New :  {repr(t)}")
                print("Tokenize's invariant failed")
        return out
if __name__ == "__main__":  
    # xx Testing of Tokenize
    s = '''
This is a sentence; it's a compound-sentence!
"There's a reasonable amt of punc."'''[1:]
    tk = Tokenize(s)
    #print(tk)
    print(list(i for i in tk if ii(i, wrd)))
    exit()

if 1:   # Miscellaneous
    def IsPunctuation(seq):
        'Return True if all characters in iterable seq are punctuation'
        if not hasattr(IsPunctuation, "punc"):
            # Get punctuation characters
            other_punc = ''.join([chr(i) for i in 
                (0x00ab, 0x00bb, 0x2012, 0x2013, 0x2014, 0x2015, 0x2018,
                0x2019, 0x201a, 0x201b, 0x201c, 0x201d, 0x201e, 0x201f,
                0x2039, 0x203a, 0x2053, 0x229d, 0x2448, 0x2449, 0x2504,
                0x2505, 0x2508, 0x2509, 0x254c, 0x254d, 0x275b, 0x275c,
                0x275d, 0x275e, 0x275f, 0x2760, 0x276e, 0x276f, 0x2e3a,
                0x2e3b, 0x301c, 0x301d, 0x301e, 0x301f, 0x3030, 0xff02)])
            IsPunctuation.punc = set(string.punctuation + other_punc)
        return set(seq) <= IsPunctuation.punc
    def GetWireDiameter(default_unit="mm"):
        '''Returns (s, d) where d is a wire diameter in the indicated units and
        s is the string the user input.  The user is prompted for the value,
        which can use an optional length unit (must be separated from the value
        by one or more spaces) or ' ga' to denote AWG.  The number portion of
        the input can be a valid python expression.
        '''
        def AWG(n):
            if n < -3 or n > 56:
                raise ValueError("AWG argument out of range")
            diameter = 92**((36 - n)/39)/200
            if n <= 44:
                return round(diameter, 4)
            return round(diameter, 5)
        msg = "Enter wire diameter (use 'ga' suffix for AWG): "
        while True:
            if GetWireDiameter.input is not None:
                # This is a StringIO stream used for testing
                s = GetWireDiameter.input.readline()
            else:
                s = input(msg).strip()
            if s == "q":
                exit(0)
            # See if it's AWG
            if s.endswith("ga"):
                t = s[:-2].strip()
                try:
                    dia_inches = AWG(int(t))
                except ValueError:
                    print("'{}' is not a valid AWG number".format(t))
                    continue
                return s, dia_inches*u("inches")/u(default_unit)
            else:
                x, unit = ParseUnit(s)
                try:
                    value = float(eval(x))
                except Exception:
                    print("Expression '{}' not valid".format(x))
                    continue
                if value <= 0:
                    print("The value must be > 0")
                    continue
                if u.dim(unit) == u.dim("m"):
                    return s, value*u(unit)/u(default_unit)
                elif not unit:
                    return s, value
    GetWireDiameter.input = None    # Used for self tests
    def GetFileSize(file):
        p = pathlib.Path(file)
        s = p.stat()
        return s.st_size
    def GetIndent(line):
        if not ii(line, str):
            raise TypeError("Argument must be a string")
        if not line:
            return 0
        count = 0
        dq = deque(line)
        while dq and dq[0] == " ":
            count += 1
            dq.popleft()
        return count

if __name__ == "__main__": 
    # Regression tests
    if 1:   # Initialization
        from collections import deque
        from wrap import dedent
        from lwtest import run, raises, Assert
        from io import StringIO
        text_file, S = None, None
        def SetUp():
            global text_file, S
            text_file = P("get.test")
            S = "Some\ntext\n"
            text_file.write_text(S)
        def TearDown():
            if text_file.exists():
                text_file.unlink()
        def sio(*s):
            'Allows StringIO to be used for input or output'
            if not s:
                return StringIO()
            return StringIO(s[0])
    if 1:   # Getting text, tokens, lines, bytes
        def TestGetText():
            sio = StringIO(S)
            t = GetText(sio)
            Assert(t == S)
            t = GetText(S)
            Assert(t == S)
            t = GetText(text_file)
            Assert(t == S)
            # Test with bytes
            b = b"Some\ntext\n"
            t = GetText(b)
            Assert(t == S)
            t = GetText(b, enc="ISO-8859-1")
            Assert(t == S)
            t = GetText(b"\xb5", enc="ISO-8859-1")
            Assert(t == "µ")
            # Test with regexp
            s = dedent('''
            # Comment
            ## Another comment
            Line 1
              Line 2''')
            r = ("^ *#",)
            lines = GetLines(s, ignore=r, nonl=True)
            Assert(lines == ['Line 1', '  Line 2'])
        def TestGetLines():
            # Test with stream
            sio = StringIO(S)
            L = S.split() + [""]
            t = GetLines(sio, nonl=True)
            Assert(t == L)
            sio = StringIO(S)
            t = GetLines(sio, nonl=False)
            m = [i + "\n" for i in L]
            Assert(t == m)
            # Test with string
            t = GetLines(S, nonl=True)
            Assert(t == L)
            # Test with file
            t = GetLines(text_file, nonl=True)
            Assert(t == L)
            # Test 'script' keyword
            s = "# xyz\n    # xyz\nabc"
            sio = StringIO(s)
            t = GetLines(sio, script=False, nonl=True)
            Assert(t == ['# xyz', '    # xyz', 'abc'])
            sio = StringIO(s)
            t = GetLines(sio, ignore=[], script=True, nonl=True)
            Assert(t == ['abc'])
            # Test docstring example
            s = """# Comment
            ## Another comment
            Line 1
                Line 2
            """
            r = [r"^\s*#"]
            lines = GetLines(s, ignore=r, nonl=True)
            if 0:
                print("Got:")
                for i in lines:
                    print(repr(i))
            expected = ['            Line 1', '                Line 2', '            ']
            if 0:
                print("Expected:")
                for i in expected:
                    print(repr(i))
            Assert(lines == expected)
            lines = GetLines(s, ignore=[], script=True, nonl=True)
            Assert(lines == expected)
        def TestGetLine():
            # Test with stream
            sio = StringIO(S)
            lines = ["Some\n", "text\n"]
            for i, line in enumerate(GetLine(sio)):
                Assert(line == lines[i])
            # Test with string
            for i, line in enumerate(GetLine(S)):
                Assert(line == lines[i])
            # Test with file
            for i, line in enumerate(GetLine(text_file)):
                Assert(line == lines[i])
        def TestGetNumberedLines():
            expected = ((1, "Some"), (2, "text"), (3, ""))
            sio = StringIO(S)
            t = GetNumberedLines(sio)
            Assert(t == expected)
            t = GetNumberedLines(S)
            Assert(t == expected)
            t = GetNumberedLines(text_file)
            Assert(t == expected)
        def TestGetBinary():
            enc = "iso-8859-1"
            open(text_file, "wb").write(S.encode(enc))
            t = GetBinary(text_file)
            Assert(t == S.encode("ascii"))
    if 1:   # Getting numbers
        def TestGetNumber():
            msg = "Error:  must have "
            # Note:  the test case comment is a picture of the allowed interval;
            # '(' and ')' mean open, '[' and ']' mean closed.
            #
            # [----...
            s_out = sio()
            GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("4"))
            Assert(s_out.getvalue() == msg + "number >= 5\n")
            s_out = sio()
            n = GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("5"))
            Assert(n == 5 and isinstance(n, int))
            s_out = sio()  # Test we can get a float like this too
            GetNumber("", numtype=float, low=5, outstream=s_out, instream=sio("4"))
            Assert(s_out.getvalue() == msg + "number >= 5\n")
            n = GetNumber("", numtype=float, low=5, outstream=sio(), instream=sio("5"))
            Assert(n == 5 and isinstance(n, float))
            # The remaining tests will be done implicitly with floats
            # (----...
            s_out = sio()
            GetNumber("", low=5, low_open=True, outstream=s_out,
                instream=sio("4"))
            Assert(s_out.getvalue() == msg + "number > 5\n")
            s_out = sio()
            n = GetNumber("", low=5, low_open=True, outstream=s_out,
                    instream=sio("6"))
            Assert(n == 6 and isinstance(n, float))
            Assert(n == 6 and isinstance(n, flt))
            # ...----]
            s_out = sio()
            GetNumber("", high=5, outstream=s_out, instream=sio("6"))
            Assert(s_out.getvalue() == msg + "number <= 5\n")
            s_out = sio()
            n = GetNumber("", high=5, outstream=s_out, instream=sio("5"))
            Assert(n == 5 and isinstance(n, float))
            Assert(n == 5 and isinstance(n, flt))
            # ...----)
            s_out = sio()
            GetNumber("", high=5, high_open=True, outstream=s_out,
                instream=sio("5"))
            Assert(s_out.getvalue() == msg + "number < 5\n")
            s_out = sio()
            n = GetNumber("", high=5, high_open=True, outstream=s_out,
                    instream=sio("4"))
            Assert(n == 4 and isinstance(n, float))
            Assert(n == 4 and isinstance(n, flt))
            # [----]
            s_out = sio()
            GetNumber("", low=2, high=5, outstream=s_out, instream=sio("6"))
            Assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
            s_out = sio()
            GetNumber("", low=2, high=5, outstream=s_out, instream=sio("1"))
            Assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
            # Also test at boundaries because this is probably the most important
            # case.
            s_out = sio()
            n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("5"))
            Assert(n == 5 and isinstance(n, float))
            Assert(n == 5 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("2"))
            Assert(n == 2 and isinstance(n, float))
            Assert(n == 2 and isinstance(n, flt))
            # [----)
            s_out = sio()
            GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
                instream=sio("5"))
            Assert(s_out.getvalue() == msg + "2 <= number < 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
                    instream=sio("4.999999999999"))
            Assert(n == 4.999999999999)
            s_out = sio()
            GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
                instream=sio("1"))
            Assert(s_out.getvalue() == msg + "2 <= number < 5\n")
            # (----]
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
                instream=sio("2"))
            Assert(s_out.getvalue() == msg + "2 < number <= 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
                    instream=sio("2.0000000000001"))
            Assert(n == 2.0000000000001)
            # (----)
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, high_open=True,
                outstream=s_out, instream=sio("5"))
            Assert(s_out.getvalue() == msg + "2 < number < 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
                    outstream=s_out, instream=sio("4.999999999999"))
            Assert(n == 4.999999999999)
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, high_open=True,
                outstream=s_out, instream=sio("2"))
            Assert(s_out.getvalue() == msg + "2 < number < 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
                    outstream=s_out, instream=sio("2.0000000000001"))
            Assert(n == 2.0000000000001)
            # ...---[  ]---...
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                outstream=s_out, instream=sio("2.0000000000001"))
            Assert(s_out.getvalue() == msg + "number <= 2 or number >= 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                outstream=s_out, instream=sio("2"))
            Assert(n == 2 and isinstance(n, float))
            Assert(n == 2 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                outstream=s_out, instream=sio("5"))
            Assert(n == 5 and isinstance(n, float))
            Assert(n == 5 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                    outstream=s_out, instream=sio("1"))
            Assert(n == 1 and isinstance(n, float))
            Assert(n == 1 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
                    outstream=s_out, instream=sio("6"))
            Assert(n == 6 and isinstance(n, float))
            Assert(n == 6 and isinstance(n, flt))
            # ...---[  )---...
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, invert=True,
                outstream=s_out, instream=sio("5"))
            Assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
            s_out = sio()
            GetNumber("", low=2, high=5, low_open=True, invert=True,
                outstream=s_out, instream=sio("4"))
            Assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, invert=True,
                outstream=s_out, instream=sio("2"))
            Assert(n == 2 and isinstance(n, float))
            Assert(n == 2 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, low_open=True, invert=True,
                outstream=s_out, instream=sio("1"))
            Assert(n == 1 and isinstance(n, flt))
            # ...---(  ]---...
            s_out = sio()
            GetNumber("", low=2, high=5, high_open=True, invert=True,
                outstream=s_out, instream=sio("2"))
            Assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
            s_out = sio()
            GetNumber("", low=2, high=5, high_open=True, invert=True,
                outstream=s_out, instream=sio("4"))
            Assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, high_open=True, invert=True,
                outstream=s_out, instream=sio("1.999999"))
            Assert(n == 1.999999 and isinstance(n, float))
            Assert(n == 1.999999 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, high_open=True, invert=True,
                outstream=s_out, instream=sio("5"))
            Assert(n == 5 and isinstance(n, float))
            Assert(n == 5 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, high_open=True, invert=True,
                outstream=s_out, instream=sio("6"))
            Assert(n == 6 and isinstance(n, float))
            Assert(n == 6 and isinstance(n, flt))
            # ...---(  )---...
            s_out = sio()
            GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("2"))
            Assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
            s_out = sio()
            GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("5"))
            Assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
            s_out = sio()
            GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("3"))
            Assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
            s_out = sio()
            n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("1"))
            Assert(n == 1 and isinstance(n, float))
            Assert(n == 1 and isinstance(n, flt))
            s_out = sio()
            n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("6"))
            Assert(n == 6 and isinstance(n, float))
            Assert(n == 6 and isinstance(n, flt))
            # Show that we can evaluate things with a variables dictionary.
            from math import sin, pi
            v = {"sin": sin, "pi": pi}
            s_out = sio()
            n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
                instream=sio("sin(pi/6)"), vars=v)
            Assert(n == sin(pi/6) and isinstance(n, float))
            Assert(n == sin(pi/6) and isinstance(n, flt))
        def TestGetNumberExceptionalCases():
            # low > high
            raises(ValueError, GetNumber, "", low=1, high=0, instream=sio("0"))
            # Invert True without low or high
            raises(ValueError, GetNumber, "", invert=True, instream=sio("0"))
        def TestGetNumber_mpmath():
            # Import mpmath and use for testing if available.
            # Demonstrates that GetNumber works with ordered number types
            # other than int and float.
            try:
                import mpmath
            except ImportError:
                print("** mpmath not tested in getnumber_test.py", file=err)
            else:
                # [----
                n = GetNumber("", numtype=mpmath.mpf, low=2, outstream=sio(),
                        instream=sio("4"))
                Assert(n == 4 and isinstance(n, mpmath.mpf))
        def TestGetNumberDefaultValue():
            # See that we get an exception when the default is not between low
            # and high.
            with raises(ValueError):
                GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                        default=1, instream=sio(""))
            # Test default value with int
            default = 2
            num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                        numtype=int, default=default, instream=sio(""))
            Assert(num == default)
            Assert(isinstance(num, int))
            # Test default value with float
            default = 3.77
            num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                        default=default, instream=sio(""))
            Assert(num == default)
            Assert(isinstance(num, float))
            Assert(isinstance(num, flt))
            # Test default of None:  exception if allow_none is False and
            # returns None if allow_none is True.
            with raises(RuntimeError):
                GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                        default=None, instream=sio(""))
            n = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                        default=None, instream=sio(""), allow_none=True)
            Assert(n is None)
        def TestGetNumberNumberWithUnit():
            # Show that we can return numbers with units
            # 5 with no unit string
            n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5"),
                use_unit=True)
            Assert(n == (5, "") and isinstance(n[0], float))
            Assert(n == (5, "") and isinstance(n[0], flt))
            # 5 meters, cuddled
            n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5m"),
                use_unit=True)
            Assert(n == (5, "m") and isinstance(n[0], float))
            Assert(n == (5, "m") and isinstance(n[0], flt))
            # 5 meters
            n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5 m"),
                use_unit=True)
            Assert(n == (5, "m") and isinstance(n[0], float))
            Assert(n == (5, "m") and isinstance(n[0], flt))
            # millimeters, cuddled
            n = GetNumber("", low=0, high=1e100, outstream=sio(),
                instream=sio("123.456e7mm"), use_unit=True)
            Assert(n == (123.456e7, "mm") and isinstance(n[0], float))
            Assert(n == (123.456e7, "mm") and isinstance(n[0], flt))
            # millimeters
            n = GetNumber("", low=0, high=1e100, outstream=sio(),
                instream=sio("123.456e7   mm"), use_unit=True)
            Assert(n == (123.456e7, "mm") and isinstance(n[0], float))
            Assert(n == (123.456e7, "mm") and isinstance(n[0], flt))
            # millimeters, negative number
            n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
                instream=sio("-123.456e7   mm"), use_unit=True)
            Assert(n == (-123.456e7, "mm") and isinstance(n[0], float))
            Assert(n == (-123.456e7, "mm") and isinstance(n[0], flt))
            #--------------------
            # Uncertainties
            #--------------------
            for t in ("8 mm", "8+-1 mm", "8+/-1 mm", "8(1) mm"):
                n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
                            instream=sio(t), use_unit=True, use_unc=True)
                Assert(isinstance(n[0], UFloat))
                Assert(n[0].nominal_value == 8)
                Assert(n[0].std_dev == 1)
                Assert(n[1] == "mm")
        def TestGetNumberInspect():
            # Test that 2 isn't in the first interval, but is in the second.
            Assert(not GetNumber("", low=0, high=1, inspect="2"))
            Assert(GetNumber("", low=0, high=3, inspect="2"))
            # If inspect is not a string, get exception
            raises(ValueError, GetNumber, "", inspect=1)
        def TestGetNumbers():
            # Check general python numerical types
            s = "1 1.2 3/4 3+1j"
            L = GetNumbers(s)
            Assert(L == [1, 1.2, Fraction(3, 4), (3+1j)])
            # Check f.py types flt and cpx
            if have_f:
                s = "1.2 3+1j"
                x, z = GetNumbers(s)
                Assert(ii(x, flt) and ii(z, cpx))
                Assert(x == flt(1.2))
                Assert(z == cpx(3+1j))
            # Check uncertainties library forms
            if have_unc:
                s = "3±4 3+-4 3+/-4 3(4)"
                for u in GetNumbers(s):
                    Assert(u.nominal_value == 3)
                    Assert(u.std_dev == 4)
            # Test with a float type
            s = "1 1.2"
            L = GetNumbers(s, numtype=float)
            Assert(L == [1.0, 1.2])
            Assert(all([ii(i, float) for i in L]))
            L = GetNumbers(s, numtype=flt)
            Assert(L == [flt(1.0), flt(1.2)])
            Assert(all([ii(i, flt) for i in L]))
            # Test with a complex type
            s = "1 1.2 3+4j"
            L = GetNumbers(s, numtype=complex)
            Assert(L == [1+0j, 1.2+0j, 3+4j])
            L = GetNumbers(s, numtype=cpx)
            Assert(all([ii(i, cpx) for i in L]))
            Assert(L == [cpx(1+0j), cpx(1.2+0j), cpx(3+4j)])
            # Test Fraction
            s = "3/8 7/16 1/2"
            L = GetNumbers(s)
            Assert(all([ii(i, Fraction) for i in L]))
            Assert(L == [Fraction(3, 8), Fraction(7, 16), Fraction(1, 2)])
        def TestGetNumberArray():
            s = '''
                1 2 3
                4 5 6
            '''
            # Empty string
            a = GetNumberArray("")
            Assert(a == [[]])
            a = GetNumberArray(" \t\n \v\r")
            Assert(a == [[]])
            # Simple string
            t = "1"
            a = GetNumberArray(t)
            Assert(a == [[1.0]])
            Assert(isinstance(a[0][0], float))
            a = GetNumberArray(t, numtype=int)
            Assert(a == [[1]])
            Assert(isinstance(a[0][0], int))
            # Single column vector
            t = '''
                1
                2
            '''
            a = GetNumberArray(t)
            Assert(a == [[1.0], [2.0]])
            # Single row vector
            t = "1 2"
            a = GetNumberArray(t)
            Assert(a == [[1.0, 2.0]])
            # Default gets column vector of floats
            a = GetNumberArray(s)
            Assert(a == [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]])
            Assert(isinstance(a[0][0], float))
            # Gets column vector of ints
            a = GetNumberArray(s, numtype=int)
            Assert(a == [[1, 4], [2, 5], [3, 6]])
            Assert(isinstance(a[0][0], int))
            # Get row vector of ints
            a = GetNumberArray(s, row=True, numtype=int)
            Assert(a == [[1, 2, 3], [4, 5, 6]])
            # Bad data gets exception
            s = '''
                1 2 3
                4 5  
            '''
            with raises(ValueError):
                a = GetNumberArray(s)
        def TestGetFraction():
            e = Fraction(5, 4)
            for i in ("5/4", "+5/4", " -5/4", "1   1/4", "+1 1/4", "  -1 1/4",
                "1-1/4", "+1-1/4", "-1-1/4", "1+1/4", "+1+1/4", "-1+1/4"):
                i = i.strip()
                neg = -1 if i[0] == "-" else 1
                Assert(GetFraction(i) == neg*e)
            Assert(GetFraction("1") == Fraction(1, 1))
        def TestParseUnitString():
            u = ["m", "in", "ft"]
            s = "mm"
            a, b = ParseUnitString(s, u)
            Assert(a == 0.001 and b == "m")
            s = "ym"
            a, b = ParseUnitString(s, u)
            Assert(a == 1e-24 and b == "m")
            # Missing an allowed string
            raises(ValueError, ParseUnitString, "yd", u)
            # Incorrect SI prefix
            raises(ValueError, ParseUnitString, "qm", u)
            # strict is False
            a, b = ParseUnitString("", [], strict=False)
            Assert(a == 1 and b == "")
            a, b = ParseUnitString("μ", [], strict=False)
            Assert(a == 1 and b == "")
        def TestGetComplex():
            em, ep = "1.23e-77", "1.23e+77"
            cases = (
                # Case 1
                ("i", "0+1j"),
                ("+i", "0+1j"),
                ("-i", "0-1j"),
                # Case 2
                ("2+i", "2+1j"),
                ("2-i", "2-1j"),
                # Case 3
                ("3i", "0+3j"),
                ("+3i", "0+3j"),
                ("-3i", "0-3j"),
                (f" {em}i", f"0+{em}j"),
                (f"+{em}i", f"0+{em}j"),
                (f"-{em}i", f"0-{em}j"),
                (f" {ep}i", f"0+{ep}j"),
                (f"+{ep}i", f"0+{ep}j"),
                (f"-{ep}i", f"0-{ep}j"),
                # Case 4
                (f" {ep}+{em}i", f"{ep}+{em}j"),
                (f"+{ep}+{em}i", f"{ep}+{em}j"),
                (f"-{ep}+{em}i", f"-{ep}+{em}j"),
                (f" {ep}-{em}i", f"{ep}-{em}j"),
                (f"+{ep}-{em}i", f"{ep}-{em}j"),
                (f"-{ep}-{em}i", f"-{ep}-{em}j"),
                (f" {em}+{ep}i", f"{em}+{ep}j"),
                (f"+{em}+{ep}i", f"{em}+{ep}j"),
                (f"-{em}+{ep}i", f"-{em}+{ep}j"),
                (f" {em}-{ep}i", f"{em}-{ep}j"),
                (f"+{em}-{ep}i", f"{em}-{ep}j"),
                (f"-{em}-{ep}i", f"-{em}-{ep}j"),
                #
                (f" {ep}+{ep}i", f"{ep}+{ep}j"),
                (f"+{ep}+{ep}i", f"{ep}+{ep}j"),
                (f"-{ep}+{ep}i", f"-{ep}+{ep}j"),
                (f" {ep}-{ep}i", f"{ep}-{ep}j"),
                (f"+{ep}-{ep}i", f"{ep}-{ep}j"),
                (f"-{ep}-{ep}i", f"-{ep}-{ep}j"),
                (f" {em}+{em}i", f"{em}+{em}j"),
                (f"+{em}+{em}i", f"{em}+{em}j"),
                (f"-{em}+{em}i", f"-{em}+{em}j"),
                (f" {em}-{em}i", f"{em}-{em}j"),
                (f"+{em}-{em}i", f"{em}-{em}j"),
                (f"-{em}-{em}i", f"-{em}-{em}j"),
            )
            for i, j in cases:
                z = GetComplex(i)
                expected = complex(j)
                Assert(z == expected)
                if have_f:
                    z = GetComplex(i, typ=cpx)
                    Assert(z == expected)
                if have_mpmath:
                    z = GetComplex(i, typ=mpc)
                    Assert(z == expected)
    if 1:   # Getting choices
        def TestGetChoice():
            seq = ["a", "b", "c"]
            i, o = sio("1"), sio()
            n, choice = GetChoice(seq, instream=i, outstream=o)
            Assert(n == 0 and choice == "a")
            i, o = sio("2"), sio()
            n, choice = GetChoice(seq, instream=i, outstream=o)
            Assert(n == 1 and choice == "b")
            # Get None for out-of-band choice
            i, o = sio("88"), sio()
            n, choice = GetChoice(seq, instream=i, outstream=o)
            Assert(n is None and choice == "")
    if 1:   # Tokenizing
        def TestGetWords():
            sio = StringIO(S)
            L = S.split()
            t = GetWords(sio)
            Assert(t == L)
            t = GetWords(S)
            Assert(t == L)
            t = GetWords(text_file)
            Assert(t == L)
        def TestGetTokens():
            s = "1 2 3\n4 5 6\n"
            L = list(GetTokens(s))
            Assert(L == "1 2 3 4 5 6".split())
        def TestGetWordlist():
            t = "Aa Bb cC"
            s = f'''# Comment
            # Another comment
            {t}
                        {t}
    
            '''
            wl = GetWordlist(s, case=None)
            Assert(wl == set(t.split()))
            wl = GetWordlist(s, case="lower")
            Assert(wl == set(t.lower().split()))
            wl = GetWordlist(s, case="upper")
            Assert(wl == set(t.upper().split()))
        def TestTokenize():
            s = "To be, or not to be:"
            t = list(Tokenize(s))
            Assert(t == ['To', ' ', 'be', ', ', 'or', ' ', 'not', ' ', 'to', ' ',
            'be', ':'])
            for i in (0, 2, 4, 6, 8, 10):
                Assert(ii(t[i], wrd))
                Assert(ii(t[i + 1], pnc))
            # Handles empty string
            s = ""
            t = Tokenize(s)
            Assert(t == deque())
            # Handles string of spaces
            s, a = "   ", "a"
            t = Tokenize(s + a + s)
            Assert(t == deque([s, a, s]))
    if 1:   # Miscellaneous
        def TestIsPunctuation():
            other_punc = ''.join([chr(i) for i in 
                (0x00ab, 0x00bb, 0x2012, 0x2013, 0x2014, 0x2015, 0x2018,
                0x2019, 0x201a, 0x201b, 0x201c, 0x201d, 0x201e, 0x201f,
                0x2039, 0x203a, 0x2053, 0x229d, 0x2448, 0x2449, 0x2504,
                0x2505, 0x2508, 0x2509, 0x254c, 0x254d, 0x275b, 0x275c,
                0x275d, 0x275e, 0x275f, 0x2760, 0x276e, 0x276f, 0x2e3a,
                0x2e3b, 0x301c, 0x301d, 0x301e, 0x301f, 0x3030, 0xff02)])
            s = set(string.punctuation + other_punc)
            Assert(IsPunctuation(s))
            s.add("s")
            Assert(not IsPunctuation(s))
        def TestGetIndent():
            raises(TypeError, GetIndent, None)
            raises(TypeError, GetIndent, 1)
            raises(TypeError, GetIndent, 1.0)
            raises(TypeError, GetIndent, b'a')
            Assert(GetIndent("") == 0)
            Assert(GetIndent(" ") == 1)
            Assert(GetIndent("  ") == 2)
            Assert(GetIndent("  This is a test") == 2)
            Assert(GetIndent("\t  This is a test") == 0)
    SetUp()
    status = run(globals(), halt=True)[0]
    TearDown()
    exit(status)
