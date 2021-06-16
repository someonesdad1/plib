'''
Contains functions to set screen color for console applications
Use sys.stdout.isatty() to determine if you should emit escape codes.

TODO:

    * The whole thing should be rewritten to be a single Color object
      that lets you define the styles to use.  Colors would be C.lred,
      C.yellow, etc., where C would be a default convenience instance.
      Functions would be C.fg(), etc.  Different instantiations could
      have different styles.

      Of course, this will mean rewriting a lot of existing code.

    * There should be a function that returns the style or color's
      escape sequence.

    * There should be a global variable that, if set, causes no escape
      codes if stdout is not a TTY (it is set by default).  This makes
      it easy for apps to support color without having escape codes in
      files or pipes.

    * A cprint() function should allow the following syntax:

        import color as C                                      
        C.cprint(C.lred, "Red text, ", C.normal, " plain text")

      which lets you easily get colored text with one line.  The C.lred
      object would be a Style object and you could easily define other
      styles.  

      Question:  would it make sense to make the Style objects derive
      from int so that older code wouldn't need to be changed?  One way
      to do this would be to make the object's str() method return the 
      desired escape code, but make fg() etc. know to get the equivalent
      integer.  Then no cprint() function is needed, as print() works as
      desired.
 
----------------------------------------------------------------------

There are 16 colors given by names:  black, blue, green, cyan, red,
magenta, brown, white, gray, lblue, lgreen, lcyan, lred, lmagenta,
yellow, and lwhite.
 
The primary function is fg(), which can be used in the following ways
to set the foreground and background colors:
 
    fg(white)
        Sets the foreground color to white and leaves the background
        unchanged.
    fg(white, black)
        Sets the foreground color to white and the background to
        black.
    fg((white, black)) or fg([white, black])
        Same as previous call.
    fg(color_byte)
        Sets the foreground and background colors by using the number
        color_byte.  The low nibble gives the foreground color and the
        high nibble gives the background color
 
The normal() function sets the foreground and background colors back
to their normal values.  Call with arguments the same as fg() to
define the normal foreground and background colors.  Set the
default_colors global variable to the default colors you use.
 
A ColorContext instance is useful as a context manager to ensure that 
you have normal colors enabled when your script exits.  See the example
at the end of the file.
 
These functions should work on both Windows and an environment that
uses ANSI escape sequences (e.g., an xterm).
 
PrintMatch()
PrintMatches()
 
    These two functions can be used to print color annotations of regular
    expression matches in strings being printed to the console.  I find
    PrintMatch() very helpful when developing a complicated regular
    expression.  Here's an example of how I'd use it in a python script:
 
    r = re.compile(r"<your regular expression here", re.S)
 
    # Colorize where the regexp r matches in the file
    s = open(file).read()
    print("-"*70)
    PrintMatch(s, r)
    print("-"*70)
    print()
    # Show the group matches
    mo = r.search(s)
    if mo:
        print("Groups:")
        for i, g in enumerate(mo.groups()):
            print("[{}]:  {}\n".format(i, g))
 
The Decorate() object is a convenience; an instance of it will return the
escape strings to set the console colors.  An example use would be
 
    dec = Decorate()
    print("Hello", dec.fg(dec.lred), " there", dec.normal(), sep="")
 
which would print the word "there" in light red.
 
The code for Windows console colors was taken from Andre Burgaud's work at
http://www.burgaud.com/bring-colors-to-the-windows-console-with-python/,
downloaded Wed 28 May 2014.
 
---------------------------------------------------------------------------
Some ANSI control codes for attributes that have an effect in xterms:
    Esc[0m  Attributes off
    Esc[1m  Bold
    Esc[3m  Italics
    Esc[4m  Underline
    Esc[5m  Blinking
    Esc[7m  Reverse video
 
---------------------------------------------------------------------------
If this module is not available, put the following in your code so that
things will still work.
 
# Try to import the color.py module; if not available, the script
# should still work (you'll just get uncolored output).
try:
    import color
    _have_color = True
except ImportError:
    # Make a dummy color object to swallow function calls
    class Dummy:
        def fg(self, *p, **kw): pass
        def normal(self, *p, **kw): pass
        def __getattr__(self, name): pass
    color = Dummy()
    _have_color = False
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
    # <programming> Module to provide ANSI color escape sequences.
    # These are useful for coloring output to a terminal.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports & globals
    import os
    import sys
    from collections.abc import Iterable
    from pdb import set_trace as xx
    # To use this under the old cygwin bash, which was derived from a Windows
    # console, you must define the environment variable BASH_IS_WIN_CONSOLE.
    # The new cygwin bash window is based on mintty and accepts ANSI escape
    # codes directly.
    bash_is_win_console = os.environ.get("BASH_IS_WIN_CONSOLE", False)
    _win = True if (sys.platform == "win32") and bash_is_win_console else False
    __all__ = '''
        black blue  green  cyan  red  magenta  brown  white 
        gray  lblue lgreen lcyan lred lmagenta yellow lwhite
        default_colors normal fg
        SetStyle Decorate Style
        PrintMatch PrintMatches
    '''.split()
    if _win:
        from ctypes import windll
    class Colors(int):
        '''Used to identify colors; shift left by 4 bits to get a
        background color.  The main reason to use a class allows the
        __call__ method to be added, which returns the escape code.
        This is a convenience for use in f-strings; for example
            print(f"{yellow()}Hello {norm()}there")
        will print 'Hello' in yellow and 'there' in the normal color.
        '''
        _DecodeColor = None
        _GetNibbles = None
        _cfg = None
        _cbg = None
        def __new__(cls, value):
            return super(Colors, cls).__new__(cls, int(value))
        def __call__(self, arg=None):
            '''Return the ASCII escape code for the color.  If arg is
            not none, return the escape code for the background color.
            '''
            val = self << 4 if arg else self
            one_byte_color = Colors._DecodeColor(val)
            cfg, cbg = Colors._GetNibbles(one_byte_color)
            f, b = Colors._cfg[cfg], Colors._cbg[cbg]
            s = "\x1b[%s;%s" % (f, b)
            return s
    # Foreground colors; shift left by 4 bits to get a background color.
    (
        black, blue,  green,  cyan,  red,  magenta,  brown,  white,
        gray,  lblue, lgreen, lcyan, lred, lmagenta, yellow, lwhite
    ) = [Colors(i) for i in range(16)]
    # Set the default_colors global variable to be the defaults for your system
    default_colors = (white, black)
    # Dictionary to translate between color numbers/names and escape sequence
    _cfg = {
        black    : "0;30",
        blue     : "0;34",
        green    : "0;32",
        cyan     : "0;36",
        red      : "0;31",
        magenta  : "0;35",
        brown    : "0;33",
        white    : "0;37",
        gray     : "1;30",
        lblue    : "1;34",
        lgreen   : "1;32",
        lcyan    : "1;36",
        lred     : "1;31",
        lmagenta : "1;35",
        yellow   : "1;33",
        lwhite   : "1;37",
    }
    _cbg = {
        black    : "40m",
        blue     : "44m",
        green    : "42m",
        cyan     : "46m",
        red      : "41m",
        magenta  : "45m",
        brown    : "43m",
        white    : "47m",
        gray     : "40m",
        lblue    : "44m",
        lgreen   : "42m",
        lcyan    : "46m",
        lred     : "41m",
        lmagenta : "45m",
        yellow   : "43m",
        lwhite   : "47m",
    }
    # Handle to call into Windows DLL
    STD_OUTPUT_HANDLE = -11
    _hstdout = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE) if _win else None

if 1:   # Utility
    def _is_iterable(x):
        '''Return True if x is an iterable that isn't a string.
        '''
        return isinstance(x, Iterable) and not isinstance(x, str)
    def _DecodeColor(*c):
        '''Return a 1-byte integer that represents the foreground and
        background color.  c can be
            * An integer
            * Two integers
            * A sequence of two integers
        '''
        if len(c) == 1:
            # It can either be a number or a tuple of two integers
            if _is_iterable(c[0]):
                if len(c[0]) != 2:
                    raise ValueError("Must be a sequence of two integers")
                color = ((c[0][1] << 4) | c[0][0]) & 0xff
            else:
                if not isinstance(c[0], int):
                    raise ValueError("Argument must be an integer")
                color = c[0] & 0xff
        elif len(c) == 2:
            color = ((c[1] << 4) | c[0]) & 0xff
        else:
            raise ValueError("Argument must be one or two integers")
        return color
    def _GetNibbles(c):
        assert 0 <= c < 256
        return (0x0f & c, (0xf0 & c) >> 4)
# Core functionality
def normal(*p, **kw):
    '''If the argument is None, set the foreground and background
    colors to their default values.  Otherwise, use the argument to
    set the default colors.
 
    If keyword 's' is True, return a string instead of printing.
    '''
    ret_string = kw.setdefault("s", False)
    global default_colors
    if p:
        one_byte_color = _DecodeColor(*p)
        default_colors = _GetNibbles(one_byte_color)
    else:
        if ret_string:
            return fg(default_colors, **kw)
        else:
            fg(default_colors, **kw)
def fg(*p, **kw):
    '''Set the color.  p can be an integer or a tuple of two
    integers.  If it is an integer that is greater than 15, then it
    also contains the background color encoded in the high nibble.
    fgcolor can be a sequence of two integers of length two also.
 
    The keyword 'style' can be:
        normal
        italic
        underline
        blink
        reverse
 
    If the keyword 's' is True, return a string containing the escape
    codes rather than printing it.  Note this won't work if _win is True.
    '''
    style = kw.setdefault("style", None)
    ret_string = kw.setdefault("s", False)
    one_byte_color = _DecodeColor(*p)
    if _win:
        windll.kernel32.SetConsoleTextAttribute(_hstdout, one_byte_color)
    else:
        # Use ANSI escape sequences
        cfg, cbg = _GetNibbles(one_byte_color)
        f, b = _cfg[cfg], _cbg[cbg]
        s = "\x1b[%s;%s" % (f, b)
        if style is not None:
            if ret_string:
                st = SetStyle(style, **kw)
                return s + st
            else:
                SetStyle(style)
                return ""
        else:
            if ret_string:
                return s
            print(s, end="")
            return ""
def SetStyle(style, **kw):
    '''If the keyword 's' is True, return a string containing the escape
    codes rather than printing it.  Note this won't work if _win is True.
    '''
    ret_string = kw.setdefault("s", False)
    if _win:
        return
    st = {
        "normal" : 0, "bold" : 1, "italic" : 3, "underline" : 4,
        "blink" : 5, "reverse" : 7,
    }[style]
    if ret_string:
        return "\x1b[%sm" % st
    else:
        print("\x1b[%sm" % st, end="")

class Decorate(object):
    '''A convenience object that will return escape code strings.
    '''
    def __init__(self):
        # Make colors an attribute
        self.black = black
        self.blue = blue
        self.green = green
        self.cyan = cyan
        self.red = red
        self.magenta = magenta
        self.brown = brown
        self.white = white
        self.gray = gray
        self.lblue = lblue
        self.lgreen = lgreen
        self.lcyan = lcyan
        self.lred = lred
        self.lmagenta = lmagenta
        self.yellow = yellow
        self.lwhite = lwhite
        self.kw = {"s": True}
    def fg(self, *p):
        return fg(*p, **self.kw)
    def normal(self, *p):
        return normal(*p, **self.kw)
    def SetStyle(self, style):
        return SetStyle(style, **self.kw)

class Style(object):
    '''Defines foreground and background colors and a particular text
    style (such as bold, italic, etc.).  The class is intended to be a
    convenience container for color information.  Note the escape codes
    are always printed to stdout; use class Decorate if you want the
    strings with the escape codes.
    '''
    def __init__(self, fg=default_colors[0], 
                 bg=default_colors[1], style="normal"):
        self.fg = fg
        self.bg = bg
        self.style = style
    def set(self):
        '''Print our escape codes to stdout.
        '''
        fg(self.fg, self.bg)
        if self.style != "normal":
            # This logic is used because the 'normal' style will undo any
            # foreground color set.
            SetStyle(self.style)
    @classmethod
    def clear(self):
        '''Print the normal style escape codes to stdout.
        '''
        normal()

class ColorContext:
    '''Context manager to ensure the screen colors are reset to desired
    values when the manager exits.  Here's an example use:
        with ColorContext():
            s = Style(fg=yellow, style="italic")
            s.set()
            print("  In yellow italics")
        print("  Back to normal")
    '''
    def __init__(self, foreground=None, background=None):
        '''If foreground and background are None, the default colors are
        used.
        '''
        self.foreground = foreground
        self.background = background
    def __enter__(self):
        pass
    def __exit__(self, type, value, traceback):
        if self.foreground is None and self.background is None:
            normal()
        if self.foreground is None:
            f = default_colors[0]
        if self.background is None:
            b = default_colors[1]
        fg(f, b)

def PrintMatch(text, regexp, style=Style(yellow, black)):
    '''Print the indicated text in normal colors if there are no
    matches to the regular expression.  If there are matches, print each
    of them in the indicated style.  text can be a multiline string.
    '''
    def out(s):
        print(s, end="")
    mo = regexp.search(text)
    if not mo:
        normal()
        print(text)
        return
    text = mo.string
    while text:
        style.clear()
        out(text[:mo.start()])      # Print non-matching start stuff
        style.set()
        out(text[mo.start():mo.end()])  # Print the match in color
        style.clear()
        # Use the remaining substring
        text = text[mo.end():]
        mo = regexp.search(text)
        if not mo:
            out(text + "\n")
            return

def PrintMatches(line, regexps):
    '''Given a line of text, search for regular expression matches
    given in the sequence of regexps, which contain pairs of regular
    expressions and Style objects, then print the line to stdout with
    the indicated styles.
    '''
    def out(s):
        print(s, end="")
    def GetShortestMatch(text):
        '''Return (start, end, style) of the earliest match or (None, None,
        None) if there were no matches.
        '''
        matches = []
        for r, style in regexps:
            mo = r.search(line)
            if mo:
                matches.append([mo.start(), mo.end(), style])
        return sorted(matches)[0] if matches else (None, None, None)
    while line:
        start, end, style = GetShortestMatch(line)
        if start is None:
            out(line)           # No matches so print remainder
            return
        style.clear()
        out(line[:start])       # Print non-matching start stuff
        style.set()
        out(line[start:end])    # Print match in chosen style
        style.clear()
        line = line[end:]       # Use the remaining substring

Colors._DecodeColor = _DecodeColor
Colors._GetNibbles = _GetNibbles
Colors._cfg = _cfg
Colors._cbg = _cbg

def norm():
    'Return the escape string for normal text'
    return normal(s=True)

class C:
    '''This is a convenience instance that holds the escape strings for
    the colors.  The color names are abbreviated with three letters
    commonly seen in resistor color codes.  Preface with 'l' to get the
    brighter color.
    '''
    blk = fg(black, s=1)
    blu = fg(blue, s=1)
    grn = fg(green, s=1)
    cyn = fg(cyan, s=1)
    red = fg(red, s=1)
    mag = fg(magenta, s=1)
    yel = fg(brown, s=1)
    wht = fg(white, s=1)
    gry = fg(gray, s=1)
    lblu = fg(lblue, s=1)
    lgrn = fg(lgreen, s=1)
    lcyn = fg(lcyan, s=1)
    lred = fg(lred, s=1)
    lmag = fg(lmagenta, s=1)
    lyel = fg(yellow, s=1)
    lwht = fg(lwhite, s=1)
    norm = normal(s=1)

if __name__ == "__main__": 
    from lwtest import run, Assert
    from wrap import dedent
    import subprocess
    def DisplayTable():
        # Display a table of the color combinations
        names = {
            black    : "black",
            blue     : "blue",
            green    : "green",
            cyan     : "cyan",
            red      : "red",
            magenta  : "magenta",
            brown    : "brown",
            gray     : "gray",
            white    : "white",
            lblue    : "lblue",
            lgreen   : "lgreen",
            lcyan    : "lcyan",
            lred     : "lred",
            lmagenta : "lmagenta",
            yellow   : "yellow",
            lwhite   : "lwhite",
        }
        low = [black, blue, green, cyan, red, magenta, brown, white]
        high = [gray, lblue, lgreen, lcyan, lred, lmagenta, yellow, lwhite]
        # Print title
        fg(yellow)
        msg = ("%s Text Colors" % __file__).center(79)
        print(msg)
        back = "Background --> "
        msg = " black   blue    green   cyan    red    magenta  brown   white"
        fg(lcyan)
        print(back + msg)
        def Table(bgcolors):
            for fgcolor in low + high:
                normal()
                s = names[fgcolor] + " (" + str(fgcolor) + ")"
                print("%-15s" % s, end="")
                for bgcolor in bgcolors:
                    fg(fgcolor, bgcolor)
                    c = (0xf0 & (bgcolor << 4)) | (0x0f & fgcolor)
                    print("wxyz %02x" % c, end="")
                    normal()
                    print(" ", end="")
                normal()
                print()
        Table(low)
        msg = " gray    lblue   lgreen  lcyan   lred  lmagenta yellow  lWhite"
        fg(lcyan)
        print("\n" + back + msg)
        Table(high)
        # Print in different styles
        print("Styles:  ", end="")
        for i in ("normal", "bold", "italic", "underline", "blink", "reverse"):
            fg(white, style=i)
            print(i, end="")
            SetStyle("normal")
            print(" ", end="")
        fg(white)
        print()
        # Using ColorContext
        print("Demo of ColorContext object:")
        with ColorContext():
            s = Style(fg=yellow, style="italic")
            s.set()
            print("  In yellow italics")
            s = Style(fg=lblue, style="underline")
            print("  ", end="")
            s.set()
            print("In blue underlined")
            normal()
            s = Style(fg=lred, style="reverse")
            print("  ", end="")
            s.set()
            print("In red reverse")
        print("  Back to normal")
        # Demo of Colors
        print("Demo of yellow(1) call to get background yellow in f-string: ", end="")
        print(f"{yellow(1)}Hi there{norm()}")
    if 1:   # Imports
        # Standard library modules
        import getopt
        import os
        import pathlib
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom modules
        from wrap import wrap, dedent, indent, Wrap
        from globalcontainer import Global, Variable, Constant
        try:
            from lwtest import run, raises, assert_equal
            _have_lwtest = True
        except ImportError:
            # Get it from
            # https://someonesdad1.github.io/hobbyutil/prog/lwtest.zip
            _have_lwtest = False
    if 1:   # Global variables
        P = pathlib.Path
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} [options] etc.
              Show color table.  Use --test option to run self tests.
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", "test")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            return args
    if 1:   # Test code 
        def Assert(cond):
            '''Same as assert, but you'll be dropped into the debugger on an
            exception if you include a command line argument.
            '''
            if not cond:
                if args:
                    print("Type 'up' to go to line that failed")
                    xx()
                else:
                    raise AssertionError
        expected_lines = dedent('''
        [1;36;40mBackground -->  black   blue    green   cyan    red    magenta  brown   white
        [0;37;40mblack (0)      [0;30;40mwxyz 00[0;37;40m [0;30;44mwxyz 10[0;37;40m [0;30;42mwxyz 20[0;37;40m [0;30;46mwxyz 30[0;37;40m [0;30;41mwxyz 40[0;37;40m [0;30;45mwxyz 50[0;37;40m [0;30;43mwxyz 60[0;37;40m [0;30;47mwxyz 70[0;37;40m [0;37;40m
        [0;37;40mblue (1)       [0;34;40mwxyz 01[0;37;40m [0;34;44mwxyz 11[0;37;40m [0;34;42mwxyz 21[0;37;40m [0;34;46mwxyz 31[0;37;40m [0;34;41mwxyz 41[0;37;40m [0;34;45mwxyz 51[0;37;40m [0;34;43mwxyz 61[0;37;40m [0;34;47mwxyz 71[0;37;40m [0;37;40m
        [0;37;40mgreen (2)      [0;32;40mwxyz 02[0;37;40m [0;32;44mwxyz 12[0;37;40m [0;32;42mwxyz 22[0;37;40m [0;32;46mwxyz 32[0;37;40m [0;32;41mwxyz 42[0;37;40m [0;32;45mwxyz 52[0;37;40m [0;32;43mwxyz 62[0;37;40m [0;32;47mwxyz 72[0;37;40m [0;37;40m
        [0;37;40mcyan (3)       [0;36;40mwxyz 03[0;37;40m [0;36;44mwxyz 13[0;37;40m [0;36;42mwxyz 23[0;37;40m [0;36;46mwxyz 33[0;37;40m [0;36;41mwxyz 43[0;37;40m [0;36;45mwxyz 53[0;37;40m [0;36;43mwxyz 63[0;37;40m [0;36;47mwxyz 73[0;37;40m [0;37;40m
        [0;37;40mred (4)        [0;31;40mwxyz 04[0;37;40m [0;31;44mwxyz 14[0;37;40m [0;31;42mwxyz 24[0;37;40m [0;31;46mwxyz 34[0;37;40m [0;31;41mwxyz 44[0;37;40m [0;31;45mwxyz 54[0;37;40m [0;31;43mwxyz 64[0;37;40m [0;31;47mwxyz 74[0;37;40m [0;37;40m
        [0;37;40mmagenta (5)    [0;35;40mwxyz 05[0;37;40m [0;35;44mwxyz 15[0;37;40m [0;35;42mwxyz 25[0;37;40m [0;35;46mwxyz 35[0;37;40m [0;35;41mwxyz 45[0;37;40m [0;35;45mwxyz 55[0;37;40m [0;35;43mwxyz 65[0;37;40m [0;35;47mwxyz 75[0;37;40m [0;37;40m
        [0;37;40mbrown (6)      [0;33;40mwxyz 06[0;37;40m [0;33;44mwxyz 16[0;37;40m [0;33;42mwxyz 26[0;37;40m [0;33;46mwxyz 36[0;37;40m [0;33;41mwxyz 46[0;37;40m [0;33;45mwxyz 56[0;37;40m [0;33;43mwxyz 66[0;37;40m [0;33;47mwxyz 76[0;37;40m [0;37;40m
        [0;37;40mwhite (7)      [0;37;40mwxyz 07[0;37;40m [0;37;44mwxyz 17[0;37;40m [0;37;42mwxyz 27[0;37;40m [0;37;46mwxyz 37[0;37;40m [0;37;41mwxyz 47[0;37;40m [0;37;45mwxyz 57[0;37;40m [0;37;43mwxyz 67[0;37;40m [0;37;47mwxyz 77[0;37;40m [0;37;40m
        [0;37;40mgray (8)       [1;30;40mwxyz 08[0;37;40m [1;30;44mwxyz 18[0;37;40m [1;30;42mwxyz 28[0;37;40m [1;30;46mwxyz 38[0;37;40m [1;30;41mwxyz 48[0;37;40m [1;30;45mwxyz 58[0;37;40m [1;30;43mwxyz 68[0;37;40m [1;30;47mwxyz 78[0;37;40m [0;37;40m
        [0;37;40mlblue (9)      [1;34;40mwxyz 09[0;37;40m [1;34;44mwxyz 19[0;37;40m [1;34;42mwxyz 29[0;37;40m [1;34;46mwxyz 39[0;37;40m [1;34;41mwxyz 49[0;37;40m [1;34;45mwxyz 59[0;37;40m [1;34;43mwxyz 69[0;37;40m [1;34;47mwxyz 79[0;37;40m [0;37;40m
        [0;37;40mlgreen (10)    [1;32;40mwxyz 0a[0;37;40m [1;32;44mwxyz 1a[0;37;40m [1;32;42mwxyz 2a[0;37;40m [1;32;46mwxyz 3a[0;37;40m [1;32;41mwxyz 4a[0;37;40m [1;32;45mwxyz 5a[0;37;40m [1;32;43mwxyz 6a[0;37;40m [1;32;47mwxyz 7a[0;37;40m [0;37;40m
        [0;37;40mlcyan (11)     [1;36;40mwxyz 0b[0;37;40m [1;36;44mwxyz 1b[0;37;40m [1;36;42mwxyz 2b[0;37;40m [1;36;46mwxyz 3b[0;37;40m [1;36;41mwxyz 4b[0;37;40m [1;36;45mwxyz 5b[0;37;40m [1;36;43mwxyz 6b[0;37;40m [1;36;47mwxyz 7b[0;37;40m [0;37;40m
        [0;37;40mlred (12)      [1;31;40mwxyz 0c[0;37;40m [1;31;44mwxyz 1c[0;37;40m [1;31;42mwxyz 2c[0;37;40m [1;31;46mwxyz 3c[0;37;40m [1;31;41mwxyz 4c[0;37;40m [1;31;45mwxyz 5c[0;37;40m [1;31;43mwxyz 6c[0;37;40m [1;31;47mwxyz 7c[0;37;40m [0;37;40m
        [0;37;40mlmagenta (13)  [1;35;40mwxyz 0d[0;37;40m [1;35;44mwxyz 1d[0;37;40m [1;35;42mwxyz 2d[0;37;40m [1;35;46mwxyz 3d[0;37;40m [1;35;41mwxyz 4d[0;37;40m [1;35;45mwxyz 5d[0;37;40m [1;35;43mwxyz 6d[0;37;40m [1;35;47mwxyz 7d[0;37;40m [0;37;40m
        [0;37;40myellow (14)    [1;33;40mwxyz 0e[0;37;40m [1;33;44mwxyz 1e[0;37;40m [1;33;42mwxyz 2e[0;37;40m [1;33;46mwxyz 3e[0;37;40m [1;33;41mwxyz 4e[0;37;40m [1;33;45mwxyz 5e[0;37;40m [1;33;43mwxyz 6e[0;37;40m [1;33;47mwxyz 7e[0;37;40m [0;37;40m
        [0;37;40mlwhite (15)    [1;37;40mwxyz 0f[0;37;40m [1;37;44mwxyz 1f[0;37;40m [1;37;42mwxyz 2f[0;37;40m [1;37;46mwxyz 3f[0;37;40m [1;37;41mwxyz 4f[0;37;40m [1;37;45mwxyz 5f[0;37;40m [1;37;43mwxyz 6f[0;37;40m [1;37;47mwxyz 7f[0;37;40m [0;37;40m
        [1;36;40m
        Background -->  gray    lblue   lgreen  lcyan   lred  lmagenta yellow  lWhite
        [0;37;40mblack (0)      [0;30;40mwxyz 80[0;37;40m [0;30;44mwxyz 90[0;37;40m [0;30;42mwxyz a0[0;37;40m [0;30;46mwxyz b0[0;37;40m [0;30;41mwxyz c0[0;37;40m [0;30;45mwxyz d0[0;37;40m [0;30;43mwxyz e0[0;37;40m [0;30;47mwxyz f0[0;37;40m [0;37;40m
        [0;37;40mblue (1)       [0;34;40mwxyz 81[0;37;40m [0;34;44mwxyz 91[0;37;40m [0;34;42mwxyz a1[0;37;40m [0;34;46mwxyz b1[0;37;40m [0;34;41mwxyz c1[0;37;40m [0;34;45mwxyz d1[0;37;40m [0;34;43mwxyz e1[0;37;40m [0;34;47mwxyz f1[0;37;40m [0;37;40m
        [0;37;40mgreen (2)      [0;32;40mwxyz 82[0;37;40m [0;32;44mwxyz 92[0;37;40m [0;32;42mwxyz a2[0;37;40m [0;32;46mwxyz b2[0;37;40m [0;32;41mwxyz c2[0;37;40m [0;32;45mwxyz d2[0;37;40m [0;32;43mwxyz e2[0;37;40m [0;32;47mwxyz f2[0;37;40m [0;37;40m
        [0;37;40mcyan (3)       [0;36;40mwxyz 83[0;37;40m [0;36;44mwxyz 93[0;37;40m [0;36;42mwxyz a3[0;37;40m [0;36;46mwxyz b3[0;37;40m [0;36;41mwxyz c3[0;37;40m [0;36;45mwxyz d3[0;37;40m [0;36;43mwxyz e3[0;37;40m [0;36;47mwxyz f3[0;37;40m [0;37;40m
        [0;37;40mred (4)        [0;31;40mwxyz 84[0;37;40m [0;31;44mwxyz 94[0;37;40m [0;31;42mwxyz a4[0;37;40m [0;31;46mwxyz b4[0;37;40m [0;31;41mwxyz c4[0;37;40m [0;31;45mwxyz d4[0;37;40m [0;31;43mwxyz e4[0;37;40m [0;31;47mwxyz f4[0;37;40m [0;37;40m
        [0;37;40mmagenta (5)    [0;35;40mwxyz 85[0;37;40m [0;35;44mwxyz 95[0;37;40m [0;35;42mwxyz a5[0;37;40m [0;35;46mwxyz b5[0;37;40m [0;35;41mwxyz c5[0;37;40m [0;35;45mwxyz d5[0;37;40m [0;35;43mwxyz e5[0;37;40m [0;35;47mwxyz f5[0;37;40m [0;37;40m
        [0;37;40mbrown (6)      [0;33;40mwxyz 86[0;37;40m [0;33;44mwxyz 96[0;37;40m [0;33;42mwxyz a6[0;37;40m [0;33;46mwxyz b6[0;37;40m [0;33;41mwxyz c6[0;37;40m [0;33;45mwxyz d6[0;37;40m [0;33;43mwxyz e6[0;37;40m [0;33;47mwxyz f6[0;37;40m [0;37;40m
        [0;37;40mwhite (7)      [0;37;40mwxyz 87[0;37;40m [0;37;44mwxyz 97[0;37;40m [0;37;42mwxyz a7[0;37;40m [0;37;46mwxyz b7[0;37;40m [0;37;41mwxyz c7[0;37;40m [0;37;45mwxyz d7[0;37;40m [0;37;43mwxyz e7[0;37;40m [0;37;47mwxyz f7[0;37;40m [0;37;40m
        [0;37;40mgray (8)       [1;30;40mwxyz 88[0;37;40m [1;30;44mwxyz 98[0;37;40m [1;30;42mwxyz a8[0;37;40m [1;30;46mwxyz b8[0;37;40m [1;30;41mwxyz c8[0;37;40m [1;30;45mwxyz d8[0;37;40m [1;30;43mwxyz e8[0;37;40m [1;30;47mwxyz f8[0;37;40m [0;37;40m
        [0;37;40mlblue (9)      [1;34;40mwxyz 89[0;37;40m [1;34;44mwxyz 99[0;37;40m [1;34;42mwxyz a9[0;37;40m [1;34;46mwxyz b9[0;37;40m [1;34;41mwxyz c9[0;37;40m [1;34;45mwxyz d9[0;37;40m [1;34;43mwxyz e9[0;37;40m [1;34;47mwxyz f9[0;37;40m [0;37;40m
        [0;37;40mlgreen (10)    [1;32;40mwxyz 8a[0;37;40m [1;32;44mwxyz 9a[0;37;40m [1;32;42mwxyz aa[0;37;40m [1;32;46mwxyz ba[0;37;40m [1;32;41mwxyz ca[0;37;40m [1;32;45mwxyz da[0;37;40m [1;32;43mwxyz ea[0;37;40m [1;32;47mwxyz fa[0;37;40m [0;37;40m
        [0;37;40mlcyan (11)     [1;36;40mwxyz 8b[0;37;40m [1;36;44mwxyz 9b[0;37;40m [1;36;42mwxyz ab[0;37;40m [1;36;46mwxyz bb[0;37;40m [1;36;41mwxyz cb[0;37;40m [1;36;45mwxyz db[0;37;40m [1;36;43mwxyz eb[0;37;40m [1;36;47mwxyz fb[0;37;40m [0;37;40m
        [0;37;40mlred (12)      [1;31;40mwxyz 8c[0;37;40m [1;31;44mwxyz 9c[0;37;40m [1;31;42mwxyz ac[0;37;40m [1;31;46mwxyz bc[0;37;40m [1;31;41mwxyz cc[0;37;40m [1;31;45mwxyz dc[0;37;40m [1;31;43mwxyz ec[0;37;40m [1;31;47mwxyz fc[0;37;40m [0;37;40m
        [0;37;40mlmagenta (13)  [1;35;40mwxyz 8d[0;37;40m [1;35;44mwxyz 9d[0;37;40m [1;35;42mwxyz ad[0;37;40m [1;35;46mwxyz bd[0;37;40m [1;35;41mwxyz cd[0;37;40m [1;35;45mwxyz dd[0;37;40m [1;35;43mwxyz ed[0;37;40m [1;35;47mwxyz fd[0;37;40m [0;37;40m
        [0;37;40myellow (14)    [1;33;40mwxyz 8e[0;37;40m [1;33;44mwxyz 9e[0;37;40m [1;33;42mwxyz ae[0;37;40m [1;33;46mwxyz be[0;37;40m [1;33;41mwxyz ce[0;37;40m [1;33;45mwxyz de[0;37;40m [1;33;43mwxyz ee[0;37;40m [1;33;47mwxyz fe[0;37;40m [0;37;40m
        [0;37;40mlwhite (15)    [1;37;40mwxyz 8f[0;37;40m [1;37;44mwxyz 9f[0;37;40m [1;37;42mwxyz af[0;37;40m [1;37;46mwxyz bf[0;37;40m [1;37;41mwxyz cf[0;37;40m [1;37;45mwxyz df[0;37;40m [1;37;43mwxyz ef[0;37;40m [1;37;47mwxyz ff[0;37;40m [0;37;40m
        Styles:  [0mnormal[0m [1mbold[0m [3mitalic[0m [4munderline[0m [5mblink[0m [7mreverse[0m [0;37;40m
        Demo of ColorContext object:
        [1;33;40m[3m  In yellow italics
          [1;34;40m[4mIn blue underlined
        [0;37;40m  [1;31;40m[7mIn red reverse
        [0;37;40m[0;37;40m  Back to normal
        Demo of yellow(1) call to get background yellow in f-string: [0;30;43mHi there[0;37;40m
        '''[1:]).split("\n")
        def TestAsScript():
            # Run the color.py module as a script and capture its output.  Compare
            # the results to the above string (remove the first line).
            cmd = os.environ["PYTHON"].split() + [os.environ["PYTHONLIB"] + "/color.py"]
            s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            lines = [i.decode("utf8") for i in s.stdout.readlines()]
            del lines[0]
            lines = [i.rstrip("\n") for i in lines]         # Remove newlines
            # Need to get rid of last line 
            del expected_lines[-1]
            Assert(len(lines) == len(expected_lines))
            Assert(lines == expected_lines)
        def TestCanReturnAsString():
            # fg
            got = fg(lred, s=True)
            expected = "[1;31;40m"
            Assert(got == expected)
            # normal
            got = normal(s=True)
            expected = "[0;37;40m"
            Assert(got == expected)
            # SetStyle
            got = SetStyle("underline", s=True)
            expected = "[4m"
            Assert(got == expected)
    # ----------------------------------------------------------------------
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals())[0])
    else:
        DisplayTable()
