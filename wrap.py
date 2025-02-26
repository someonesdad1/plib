"""
TODO
    - Use abbreviations.py instead of class Abbr.
    - Bug:  Wrapping 'which is equal to (x - 1)!  if x is an integer.' will
      result in two spaces after the '!'.  Look at the next letter of the
      sentence and don't double space if it's not a capital.
    - Use the -H string from /plib/pgm/goto.py as an example of the typical
      help string found in a script.
        - Develop a mini-language for formatting things; these get stripped
          out of the output.
            - Look at mp.py and ts.py and see what of them can be put into
              a text processing module.
            - Commands (column numbering is 1-based)
                - If you want a line to begin with a period, escape it with
                  a backslash.
                - .exec s:  Execute this python line of code
                - .{ and .}  Defines a python code block
                - .default:  Set the default state
                - .fmt on/off:  Turn formatted output on/off.  If it is
                  off, the lines are output verbatim.
                - .output on/off:  Turn output on/off.  If it is off, no
                  lines are output until the next '.output on' is seen.
                - .push:  Save the current state
                - .pop:  Use the previously saved state
                - .save x:  Save the current state to variable x
                - .restore x:  Restore the current state from variable x
                - .lm n:  Set left margin.  Set to 0 or 1 to have text
                  start at column 1.
                - .rm n:  Set right margin.  Set to 0 to make it be
                  determined by the .width command.
                - .width n:  0 means wrap to width from COLUMNS.  'n' means
                  to wrap to int(n) columns.
                - .indent n:  How many spaces to indent if n is an integer.
                  Otherwise, n is interpreted as the indent string (it must
                  be a valid python string usable by eval()).
                - .empty n:  A line with no whitespace is replaced by one
                  with n space characters.
                - .#:  Delete this line up to and including the newline.
                - .|   No justification or centering
                - .< [n]:  Left justify the following n lines (if n isn't
                  present, the setting is sticky)
                - .> [n]:  Right justify the next n lines (sticky if n not
                  given)
                - .^ [n]:  Center the next n lines (sticky if n not given)
        - Template strings:  a = string.Template(s) is used to replace things
          like $name by another string defined in a dict.  Then
          a.substitute(dict) gets the replacements.
    - For use with Usage strings in a script, in dedent, remove the first
      and last lines with newlines if they are whitespace only.  Then
      include an option that's True to let empty lines with no space be
      ignored in the analysis of the number of common spaces on the line.
    - Sometimes you want to wrap a set of things like numbers, but you want
      a specified spacing between the numbers.  For example, consider the
      Renard5 numbers 1 1.6 2.5 4 6.3.  I might want these to be printed
      with the format {i:^6s}.  Add a method that allows the wrapping of
      sequences like this such as wrap_seq(seq, format_string, width).

Wrap class: make text fit into a desired width with a specified indent.
    Basic usage is

        w = Wrap()
        print(w(s))

    where s is a string you'd like to wrap.  The width is automatically
    taken from the COLUMNS environment variable or is 79 if COLUMNS doesn't
    exist.  You can define it by setting the w.width attribute.

    Instance attributes

        ends        Tuple of strings that can end a sentence
        i           String to prepend before each line
        ls          Line separator
        opp         Output paragraph separator
        pp          Paragraph separator for parsing input
        ss          Sentence spacing ("" for one space after previous)
        width       Maximum width of a line

    The basic use case is to let you write multiline program output strings
    without regard for their appearance.  Before printing an output string
    to stdout, you'd run it through the Wrap instance to get it looking the
    way you want.

    Run the module as a script to see some examples.  Use the --test option
    to run the unit tests.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # <programming> Provides the Wrap class, which can be used to make
    # text fit into a desired width with a specified indent.  Can also
    # indent and dedent like the textwrap module.  Handles common
    # English abbreviations also.
    # ∞what∞#
    # ∞test∞# --test #∞test∞#
    pass
if 1:  # Imports
    from collections import deque
    import os
if 1:  # Global variables
    all = """Abbr Wrap dedent indent wrap""".split()


class Abbr:
    "Used to identify common abbreviations in English"

    def __init__(self):
        # This list came from searching hundreds of texts with a script
        self.abbr = set(
            """
            a.c. a.d. a.k.a. abr. abstr. acad. acc. acct. addr. adj.
            adm.  adv. advb. anon. app. appl. assoc. attrib. auth. ave.
            b. b.c.  b.c.e. b.o. b.t.u. betw. bk. bur. c. c.e. c.o.d.
            c.p.u. cent.  cert. cf. ch. chas. co. colloq. conf. conv.
            corresp. ct. d.a.  d.c. d.o.a. dat. def. dep. dept. descr.
            e. e.s.p. ed. edw.  emph. eng. equip. esp. etym. etymol.
            euphem. exc. f. fr. fut.  geo. gov. govt. h.p. handbk. hist.
            i.d. i.u.d. illustr. inc.  intro. jr. jrnl. jurisd. jurispr.
            lat. lbf. lett. ltd. ln. m.  masc. mass. meas. med. mil.
            misc. mt. n. n.b. n.e. n.s.w. n.w.  n.y. n.z. nom. nucl.
            o.d. o.e.d. o.k. obj. orig. oz. p. p.a.  p.e. p.m. p.o.
            ph.d. phil. phys. pl. publ. q. q.v. r.a.f.  r.c. r.n. ref.
            rep. rev. s. s.e. st. s.t.p. s.u.v. s.w. sat.  sci. soc. sp.
            sr. st. subj. subord. t.b. techn. technol. tr.  trans. u.k.
            u.s. u.s.s.r. univ. unkn. unoffic. usu. v. v.p.  var. vet.
            vic. viz. vol. vols. vulg. w. w.c. w.v. w.m.d. wk.  yr. yrs.
    
            u.s.a. u.s.n. u.s.a.f. u.s.c.g.
            g.i. pvt. cpl. corp. sgt. lt. capt. maj. cmdr. col. gen.
    
            e.g. et.al. etc. q.e.d. i.e. ibid. ib.
            a.m. p.m.
    
            mr. mrs. ms. mss. messrs. mssrs. dr. prof.
            jan. feb. mar. apr. jun. jul. aug. sep. sept. oct. nov. dec.
            mon. tue. wed. thu. fri. sat. sun.
    
            add. admin. ann. bull. conn. dim. fig. math. mod.
            no. pa. pop. sing. west. 
        """.split()
        )

    def is_abbreviation(self, s):
        return s.strip().lower() in self.abbr


class Wrap(Abbr):
    def __init__(self, indent="", width=None, rmargin=0):
        super().__init__()
        self._indent = str(indent)
        self._width = width
        self._rmargin = int(rmargin)
        self.ls = "\n" * 1
        self.pp = "\n" * 2  # Paragraph separator
        self.opp = "\n" * 2  # Paragraph separator for output
        # The following is the sentence separator string.  If this entry
        # is the empty string, all sentences are separated by one space.
        # Thus, if you want two spaces between sentences, make it " ".
        self.ss = " "
        if width is None:
            key = "COLUMNS"
            if key in os.environ:
                self._width = int(os.environ[key])
            else:
                self._width = 79
        # The following strings can end a sentence.
        self.ends = (".", "!", "?", '."', '?"', '!"')

    def __call__(self, *args):
        "Process each string in args and return the wrapped result"
        r = []
        for s in args:
            t = self.process(s)
            r.extend(t)
        return self.opp.join(r).rstrip()

    def indent(self, s, indent=""):
        "Insert the indent string at the beginning of each line in s"
        o, d = [], deque(s.split("\n"))
        while d:
            t = d.popleft()
            o.append(indent + t)
        return "\n".join(o)

    def is_sentence_end(self, token):
        if not token.endswith(self.ends):
            return False
        if token.endswith("."):
            if self.is_abbreviation(token):
                return False
        return True

    def normalize(self, s):
        """Remove the indent from the string s, lstrip leading whitespace,
        and put the indent back.  This handles some corner cases.
        """
        t = s[len(self._indent) :].lstrip()
        return self._indent + t

    def process(self, s):
        r = []
        for paragraph in s.split(self.pp):
            r.append(self.process_paragraph(paragraph))
        return r

    def process_paragraph(self, p):
        assert self.pp not in p
        p = p.strip()
        # Separate into lines by the linefeeds
        lines = p.split("\n")
        # Remove leading space characters
        lines = [i.lstrip(" ") for i in lines]
        # Append space to each line and join to a single string
        s = " ".join(lines)
        # Tokenize at whitespace characters
        tokens = deque(s.split())
        results = deque()
        # Look for sentence ends.  We use unusual Unicode characters as
        # a sentinel character that is unlikely to be in any English
        # text.
        sentinels = deque([0x204B, 0x2188, 0x2187, 0xBEEF, 0x2588])
        sentinel = chr(sentinels.pop())
        while sentinel in p:
            sentinel = chr(sentinels.pop())
        if not sentinels:
            raise RuntimeError("All sentinels used")
        while tokens:
            token = tokens.popleft()
            results.append(token)
            if self.is_sentence_end(token):
                results.append(sentinel)
        # results contains the paragraph's tokens with sentence ending
        # markers, so we can now construct the wrapped paragraph.
        lines, line, space = [], deque(), " "

        def Len(x):
            return len("".join(x))

        W = self._width - self._rmargin
        while results:
            token = results.popleft()
            if not line:
                line.append(self._indent)
            if token == sentinel:
                line.append(self.ss)
            else:
                line.append(token)
                if token.endswith(":"):
                    line.append(space)
                line.append(space)
            next_token_length = len(results[0]) if results else 0
            if Len(line) + next_token_length >= W:
                # Remove the indent, lstrip whitespace, and put the
                # indent back.  This handles some corner cases.
                lines.append(self.normalize("".join(line)))
                line.clear()
        # Don't forget last portion
        if line:
            lines.append(self.normalize("".join(line)))
        q = self.ls.join(lines).rstrip()
        return q

    def seq(self, seq, fmt):
        """Given a sequence of objects in seq and a string interpolation
        formatting string fmt, wrap this sequence's string
        representation into the desired width.  The basic use case is a
        sequence of numbers that you want to have a specified set of
        space characters around them.  The __call__ method will strip
        all the spaces off the individual "words".
        """
        # Put the needed strings into a deque
        tokens, lines, line = deque(), [], deque()
        for i in seq:
            s = fmt.format(i)
            tokens.append(s)

        # Construct the individual lines
        def Len(x):
            return len("".join(x))

        W = self._width - self._rmargin
        while tokens:
            token = tokens.popleft()
            if not line:
                line.append(self._indent)
            line.append(token)
            next_token_length = len(tokens[0]) if tokens else 0
            if Len(line) + next_token_length >= W:
                lines.append("".join(line))
                line.clear()
        # Don't forget last portion
        if line:
            lines.append("".join(line))
        q = self.ls.join(lines).rstrip()
        return q

    @property
    def i(self):
        return self._indent

    @i.setter
    def i(self, value):
        self._indent = str(value)

    @property
    def rmargin(self):
        return self._rmargin

    @rmargin.setter
    def rmargin(self, value):
        self._rmargin = int(value)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = int(value)


def HangingIndent(s, indent="", first_line_indent=""):
    """Return the string s wrapped so that the first line has the indicated
    indent with the remaining lines indented uniformly.
    """
    w = Wrap(indent=first_line_indent)
    out = []
    lines = w(s).split("\n")
    out.append(lines[0])
    lines.pop(0)
    if len(lines):
        t = "\n".join(lines)
        w = Wrap(indent=indent)
        out.extend(w(t).split("\n"))
    return "\n".join(out)


def indent(s: str, sindent=""):
    "Convenience function to indent"
    if not hasattr(indent, "wrap"):
        indent.wrap = Wrap()
    return indent.wrap.indent(s, sindent)


def Dedent(
    s,
    empty=True,
    leading=True,
    trailing=True,
    trim=False,
    ltrim=False,
    rtrim=False,
    n=None,
):
    '''For the multiline string s, remove the common leading space
    characters and return the modified string.

    empty       Consider empty lines to have an infinite number of spaces.
                They will be empty lines in the output string.
    leading     Remove first line if it is only space characters.
    trailing    Remove last line if it is only space characters.
    ltrim       Remove all leading lines that are blank or whitespace.
    rtrim       Remove all trailing lines that are blank or whitespace.
    trim        Remove all trailing whitespace.
    n           If not None, remove this number of leading space characters

    The keywords default to the values most useful in help strings for
    scripts.  Typical use is
        s = """
        Line 1
          Line 2
        """
    and dedent(s) will return the string 'Line 1\n  Line 2'.
    '''
    if not s.strip():
        return ""
    if trim:
        s = s.rstrip()
    lines = deque(s.split("\n"))
    if len(lines) == 1:
        return s.lstrip()
    if ltrim:
        while lines and IsBlankOrSpaces(lines[0]):
            lines.popleft()
    if rtrim:
        while lines and IsBlankOrSpaces(lines[-1]):
            lines.pop()
    if not trim and trailing:
        if set(lines[-1]) == set(" "):
            del lines[-1]
    if len(lines) > 1 and leading:
        a = set(lines[0])
        if not a or a == set(" "):
            del lines[0]
    # Get sequence of the number of beginning spaces on each line
    o = [LeadingSpaces(i) for i in lines]
    if empty:
        # Fix the empty lines
        m = max(o)
        o = [i if i else m + 1 for i in o]
    n = min(o) if n is None else n
    if n:
        lines = [i[n:] for i in lines]
    return "\n".join(lines)


def IsBlankOrSpaces(s):
    "For string s, return True if it's empty or contains only spaces"
    empty, only_spaces = set(), set(" ")
    return set(s) == empty or set(s) == only_spaces


def LeadingSpaces(s):
    "Return the number of space characters at the beginning of string s"
    if not s:
        return 0
    dq, count = deque(s), 0
    while dq:
        c = dq.popleft()
        if c == " ":
            count += 1
        else:
            break
    return count


def dedent(s):
    '''For the multiline string s, remove common leading space characters.  The use case is for
    help strings in scripts, allowing arbitrary leading and trailing newlines that are removed.
    Example:  dedent(s) for
        s = """

        Line 1
          Line 2

        """
    will return 'Line 1\n  Line 2'.
    '''
    # If s is the empty string, return the empty string
    if not s.strip():
        return ""
    # If s has no newlines, return s.strip()
    if "\n" not in s:
        return s.strip()
    lines = deque(s.split("\n"))
    # Remove leading blank lines or lines with only spaces
    while lines:
        if not IsBlankOrSpaces(lines[0]):
            break
        lines.popleft()
    # Remove trailing blank lines or lines with only spaces
    while lines:
        if not IsBlankOrSpaces(lines[-1]):
            break
        lines.pop()
    # Get sequence of the number of leading spaces on each line
    numspaces = [LeadingSpaces(i) for i in lines]
    # Bare newlines are considered to have infinite spaces.  The following emulates this by making
    # them appear to have max(numspaces) + 1 spaces.
    m = max(numspaces)
    numspaces = [i if i else m + 1 for i in numspaces]
    # Find n = the number of common beginning spaces on each line
    n = min(numspaces)
    # If n is zero, then there are no lines with leading spaces, so just return s
    if not n:
        return s
    else:
        # Trim off n spaces from each line
        lines = [i[n:] for i in lines]
    # Return the dedented string
    return "\n".join(lines)


if 0:  # xx
    s = """
    Line 1
   Line 2
    """
    result = dedent(s)
    print(f"orig:\n{s}")
    print()
    print(f"result:\n{result}")
    exit()

wrap = Wrap()  # Convenience instance

if __name__ == "__main__":
    # Run the selftests
    from lwtest import run, Assert
    import sys

    def Dump(s):
        "Print a multiline string to stdout"
        for i in s.split("\n"):
            print(repr(i))

    def W():
        return Wrap()

    def TestBasic():
        s = """One two.          Three four.

        Five
        six.
        Seven
                eight."""
        # Default behavior
        w = W()
        t = w(s)
        u = ["One two.  Three four.", "", "Five six.  Seven eight."]
        Assert(t == "\n".join(u))
        # One space after sentence
        w.ss = ""
        t = w(s)
        u = ["One two. Three four.", "", "Five six. Seven eight."]
        Assert(t == "\n".join(u))
        # Triple newline
        w.opp = "\n" * 4
        t = w(s)
        u = ["One two. Three four.", "", "", "", "Five six. Seven eight."]
        Assert(t == "\n".join(u))

    def TestDoubleLineSpacing():
        s = """
        Mr. Bennet missed his second daughter exceedingly; his affection
        for her drew him oftener from home than anything else could do. 
        """
        w = W()
        w.ls = "\n" * 2
        w.width = 60
        t = w(s)
        u = (
            "Mr. Bennet missed his second daughter exceedingly; his \n"
            "\n"
            "affection for her drew him oftener from home than anything \n"
            "\n"
            "else could do."
        )
        Assert(u == t)

    def Test_dedent():
        # Simplest cases:  no newline in string
        Assert(dedent("") == "")
        Assert(dedent(" ") == "")
        Assert(dedent("x") == "x")
        Assert(dedent(" x") == "x")
        Assert(dedent("  x") == "x")
        Assert(dedent("  x  ") == "x")
        # Canonical use cases
        x = """
        a
        b
        """
        Assert(dedent(x) == "a\nb")
        x = """
        
        a
        b
        
        """
        Assert(dedent(x) == "a\nb")
        # Make sure an embedded blank line is retained, but leading and trailing empty lines are
        # deleted.
        x = """

        
        
        
        a

        b
        
        
        

        """
        Assert(dedent(x) == "a\n\nb")

    def TestDedent():
        Assert(Dedent(" x") == "x")
        s = """        a
        b"""
        s = "        a\n        b"
        Assert(Dedent(s) == "a\nb")
        s = "\n        a\n        b\n          c\n        "
        Assert(Dedent(s) == "a\nb\n  c")
        # Test main use case:  script help strings
        s = """   
        Line 1
          Line 2
        
        """
        t = "Line 1\n  Line 2\n"
        Assert(Dedent(s) == t)
        # Blank line with empty False
        s = """   
        Line 1
          Line 2

        
        """
        t = "        Line 1\n          Line 2\n\n        "
        Assert(Dedent(s, empty=False) == t)
        t = "Line 1\n  Line 2\n\n"
        Assert(Dedent(s, empty=True) == t)
        # Most common use case
        s = """
        Line 1
          Line 2
        """
        t = "Line 1\n  Line 2"
        Assert(Dedent(s) == t)

    def TestIndent():
        f, spc = wrap.indent, " "
        Assert(f(" x", spc) == "  x")
        s = "        a\n        b"
        t = "         a\n         b"
        Assert(f(s, spc) == t)
        s = "\n        a\n        b\n          c\n        "
        t = " \n         a\n         b\n           c\n         "
        Assert(f(s, spc) == t)

    def TestTwoSpacesAfterColon():
        s = "This is a:     test."
        w = W()
        w.ls = "\n"
        w.width = 60
        t = w(s)
        u = "This is a:  test."
        Assert(u == t)

    # Run the demos
    def Demos():
        s = """
            It is a truth universally acknowledged, that a single man in
            possession of a good fortune, must be in want of a wife.
            However little known the feelings or views of such a man may be
            on his first entering a neighbourhood, this truth is so well
            fixed in the minds of the surrounding families, that he is
            considered the rightful property of some one or other of their
            daughters.
    
            "My dear Mr. Bennet," said his lady to him one day, "have you
            heard that Netherfield Park is let at last?" Mr. Bennet replied
            that he had not.  "But it is," returned she; "for Mrs. Long has
            just been here, and she told me all about it." "Oh!  Single, my
            dear, to be sure!  A single man of large fortune; four or five
            thousand a year.  What a fine thing for our girls!"  Mr. Bennet
            was quiet."""[1:]

        def Sep():
            print("-" * (wrap.width - 1))

        def Example1():
            print("Original text:")
            print(s)

        def Example2():
            Sep()
            w = Wrap()
            print("Wrapped to screen width with no indent:")
            print(w(s))

        def Example3():
            Sep()
            w = Wrap()
            print("Wrapped to width 50 with an indent of 10 (text width = 40):")
            w.indent = " " * (10 - 1)
            w.width = 50
            print(
                """
            1         2         3         4         5         6         7 
    ....+....|....+....|....+....|....+....|....+....|....+....|....+....|....+....
    """[1:].rstrip()
            )
            print(w(s))

        def Example4():
            Sep()
            w = Wrap()
            print("Single space between sentences:")
            w.indent = " " * 2
            w.ss = ""
            w.opp = "\n" * 4
            print(w(s))

        def Example5():
            Sep()
            w = Wrap()
            print("Double line spacing, quadruple space between paragraphs:")
            w.indent = " " * 2
            w.opp = "\n" * 5
            w.ls = "\n" * 2
            print(w(s))

        Example1()
        Example2()
        Example3()
        Example4()
        Example5()

    # Run self tests, then show demo stuff if successful
    status = run(globals())[0]
    if status:
        exit(status)
    Demos()
