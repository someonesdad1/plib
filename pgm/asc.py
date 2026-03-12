'''
Prints out ASCII characters
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Prints out ASCII characters oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2009, 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
            
            - ∞∞3 Just below https://en.wikipedia.org/wiki/UTF-8#Error_handling, there's
              a colorized byte map that would be handy to print to the terminal
            
        oo>
    '''
    if 1:  # Standard imports
        import getopt
        import sys
        from textwrap import dedent
    if 1:  # Custom imports
        import trm
        from columnize import Columnize
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        if 1:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        t = trm.Trm()
        class Global:
            pass
        g = Global()
        if 0:
            g.dbg = True
        else:
            g.dbg = False
        g.decimal = False
        g.octal = False
        g.binary = False
        g.Binary = False
        g.offset = 0
        g.column_width = 9
        g.number_of_columns = 8
        g.c = True  # Colorize
        g.symbols = False   # If true, print g.decorations
if 1:  # Utility
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = t.cyn
        t.err = t.red
        t.dec = t.skyl
        t.hex = t.wht
        t.oct = t.pur
        t.bin = t.orn
        t.chr = t.wht
        t.N = t.n
        if not g.c:
            t.on = False
    def Dbg(*p, **kw):
        if g.dbg:
            if 0:
                print(f"{t.dbg}", end="", file=Dbg.file)
                k = kw.copy()
                k["file"] = Dbg.file
                print(*p, **k)
                print(f"{t.N}", end="", file=Dbg.file)
            else:
                print(f"{t.dbg}", end="")
                k = kw.copy()
                print(*p, **k)
                t.print(f"", end="")
    Dbg.file = sys.stdout
    def Error(msg, status=1):
        print(msg)
        exit(status)
    def Usage():
        name = sys.argv[0]
        print(dedent(f'''
        Usage: {name} [options] [offset [numchars]]
          Prints the ASCII/Unicode character set starting at the indicated offset 
          for the indicated number of characters (default 0x100).
           
          offset and numchars can be expressions.  Prefix hex numbers with
          '0x', octal numbers with '0o', and binary numbers with '0b'.
           
          The character 0x7f is printed as a red block, as it typically
          won't display as a single character.
        Options
          -B    Print the 256 binary characters, one per line
          -b    Print a binary listing
          -c    Don't colorize
          -d    Print in decimal
          -h    Print this help
          -l    Print the lower 128 characters
          -o    Print octal characters
          -s    Show symbols & names for 0x0 to 0x20
          -u    Print the upper 128 characters
          -x    Print in hex (default)
        Example
            {name} 0x10a8*2
          will print a table of Unicode characters starting at 0x2150.
          These are Unicode fractions symbols such as 1/7, 1/9, 1/10, etc.
          and a variety of arrows and math symbols.'''[1:]
            )
        )
        exit(1)
    def ParseCommandLine():
        lower_upper = False
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "Bbcdhlosux")
        except getopt.GetoptError as e:
            print(f"{sys.argv[0]}:  {e}")
            sys.exit(1)
        lower, upper = 0, 256
        for o, a in optlist:
            if o == "-B":
                g.Binary = True
            elif o == "-b":
                g.binary = True
            elif o == "-c":
                g.c = not g.c
            elif o == "-d":
                g.decimal = True
            elif o == "-h":
                Usage()
            elif o == "-l":
                lower_upper = True
                lower, upper = 0, 128
            elif o == "-o":
                g.octal = True
            elif o == "-s":
                g.symbols = True
            elif o == "-u":
                lower_upper = True
                lower, upper = 128, 256
            elif o == "-x":
                g.Binary = g.binary = g.decimal = g.octal = False
        GetColors()
        Dbg("Debugging turned on")
        # Get Unicode start and number of characters if present
        if args:
            Dbg(f"args = {args}")
            offset = args[0]
            numchars = None
            if len(args) > 2:
                Usage(status=1)
            if len(args) == 2:
                numchars = args[1]
            try:
                i = eval(offset)  # This handles "0x3", "0o3", "0b11", "3"
                if i < 0:
                    raise ValueError()
                g.offset = min(max(0, i), 0x10FFFF)
            except Exception:
                Error(f"'{offset}' is not a valid integer for offset (must be >= 0)")
            try:
                if numchars is None:
                    g.numchars = 256
                else:
                    g.numchars = int(numchars)
                    if g.numchars < 1:
                        raise ValueError()
            except Exception:
                Error(f"'{numchars}' is not a valid integer for numchars (must be > 0)")
        else:
            g.offset = 0
            g.numchars = 256
        if 1:  # Debug print input stuff
            Dbg(f"g.offset   = {g.offset}")
            Dbg(f"g.numchars = {g.numchars}")
            Dbg(f"Settings:")
            for i in dir(g):
                if i.startswith("_"):
                    continue
                Dbg(f"  g.{i} = {eval(f'g.{i}')}")
        if lower_upper:
            return lower, upper
        return g.offset, g.offset + g.numchars
if 1:  # Core functionality
    def ColorCoding():
        t.print(f"{t.whtl}Colors: {t.dec}dec {t.hex}hex {t.oct}oct {t.bin}bin")
    def Integer(s):
        '''Convert the string s to an integer.  Allow prefixes such as 0x,
        0b, 0o.
        '''
        s, base = s.lower(), 10
        if s.startswith("0b"):
            base = 2
        elif s.startswith("0o"):
            base = 8
        elif s.startswith("0x"):
            base = 16
        return int(s, base)
    def PrintBinary():
        for i in range(lower, upper):
            c = i + g.offset
            s = " "*4  # Spacing to make things easier to read
            print(
                f"{t.dec}{c:3d}{t.N}{s}"
                f"{t.hex}0x{c:02x}{t.N}{s}"
                f"{t.oct}0o{c:03o}{t.N}{s}"
                f"{t.bin}0b{c:08b}{t.N}{s}"
                f"{t.chr}{chr(c)}{t.N}"
            )
        ColorCoding()
    def PrintBinaryListing():
        for i in range(0x100):
            c = i + g.offset
            print(chr(c))
        print()
    def PrintTable(lower, upper):
        ctrl = '''
                nul soh stx etx eot enq ack bel bs ht nl vt ff cr so si dle dc1
                dc2 dc3 dc4 nak syn etb can em sub esc fs gs rs us sp
        '''.split()
        out = []
        for i in range(lower, upper):
            c = ctrl[i] if i <= ord(" ") else chr(i)
            # Handle the special case of char == 0xf7, which doesn't print correctly.  We
            # replace it with a space with a red background.
            c = f"{t('redl', 'redl')} {t.N}" if i == 0x7F else c
            if g.decimal:
                out.append(f"{t.dec}{i:3d}{t.N} {t.chr}{c:3s}{t.N}")
            elif g.octal:
                out.append(f"{t.oct}{i:03o}{t.N} {t.chr}{c:3s}{t.N}")
            else:
                out.append(f"{t.hex}{i:02x}{t.N} {t.chr}{c:3s}{t.N}")
        for i in Columnize(out, col_width=g.column_width, columns=g.number_of_columns):
            print(i)
    def PrintSymbols():
        bl = t.blul
        c  = t.cynl
        m  = t.magl
        o  = t.ornl
        O  = t.n
        p  = t.lipl
        r  = t.redl
        s  = t.sky
        w  = t.whtl
        y  = t.yell
        print(dedent(f'''
            {bl}00 nul   ␀   U+2400  null{O}
            01 soh   ␁   U+2401  start of heading
            02 stx   ␂   U+2402  start of text
            03 etx   ␃   U+2403  end of text
            04 eot   ␄   U+2404  end of transmission
            05 enq   ␅   U+2405  enquiry
            06 ack   ␆   U+2406  acknowledge
            07 bel   ␇   U+2407  bell                   {c}\\a{w}
            08 bs    ␈   U+2408  backspace              {c}\\b{p}
            09 ht    ␉   U+2409  horizontal tab         {c}\\t{m}  *{r}
            0a nl    ␤   U+240A  newline                {c}\\n{m}  *{p}
            0b vt    ␋   U+240B  vertical tab           {c}\\v{m}  *{p}
            0c ff    ␌   U+240C  form feed              {c}\\f{m}  *{o}
            0d cr    ␍   U+240D  carriage return{O}        {c}\\r{m}  *{O}
            0e so    ␎   U+240E  shift out
            0f si    ␏   U+240F  shift in
            10 dle   ␐   U+2410  data link escape
            11 dc1   ␑   U+2411  device control one
            12 dc2   ␒   U+2412  device control two
            13 dc3   ␓   U+2413  device control three
            14 dc4   ␔   U+2414  device control four
            15 nak   ␕   U+2415  negative acknowledge
            16 syn   ␖   U+2416  synchronous idle
            17 etb   ␗   U+2417  end of transmission block
            18 can   ␘   U+2418  cancel
            19 em    ␙   U+2419  end of medium
            1a sub   ␚   U+241A  substitute{y}
            1b esc   ␛   U+241B  escape{O}
            1c fs    ␜   U+241C  file separator
            1d gs    ␝   U+241D  group separator
            1e rs    ␞   U+241E  record separator
            1f us    ␟   U+241F  unit separator{s}
            20 spc   ␠   U+2420  space{O}
            7f del   ␡   U+2421  delete
            {m}*{O} indicates whitespace in python
        '''))
    def PrintByteMap():
        '''This table shows the detailed meaning of each byte in a UTF-8 stream
        https://en.wikipedia.org/wiki/UTF-8#Error_handling
        '''
        # Define the colors for the blocks
        t.hdr  = t.ygr
        t.ctrl = t("blk", "skyl")
        t.asc  = t("blk", "wht")
        t.cont = t("blk", "brn")
        t.byt1 = t("blk", "purl")
        t.nota = t("blk", "lip")
        t.unus = t("blk", "yel")
        def out(x):
            print(x, end="")
        def C(n):
            assert 0 <= n < 16
            return f"{n:X}"
        def Item(char):
            '''Print a table entry with 3 characters width & proper color.  char is an
            integer <= 0xff.
            '''
            if char <= 0x1f or char == 0x7f:    # Control character
                out(t.ctrl)
                out(f" {chr(0x2421)} ") if char == 0x7f else out(f" {chr(char + 0x2400)} ")
                out(t.n)
            elif 0x1f < char < 0x7f:            # Plain ASCII character
                out(t.asc)
                out(f" {chr(char)} ")
                out(t.n)
            elif 0x80 <= char < 0xc0:
                out(t.cont)
                out(f"   ")
                out(t.n)
            elif 0xc0 <= char < 0xe0:
                out(t.unus) if 0xc0 <= char <= 0xc1 else out(t.byt1)
                out(f" 2 ")
                out(t.n)
            elif 0xe0 <= char < 0xf0:
                out(t.nota) if char == 0xe0 or char == 0xed else out(t.byt1)
                out(f" 3 ")
                out(t.n)
            elif 0xf0 <= char < 0xf8:
                if char == 0xf0 or char == 0xf4:
                    out(t.nota)
                elif 0xf1 <= char <= 0xf3:
                    out(t.byt1)
                else:
                    out(t.unus)
                out(f" 4 ")
                out(t.n)
            elif 0xf8 <= char < 0xfc:
                out(t.unus)
                out(f" 5 ")
                out(t.n)
            elif 0xfc <= char < 0xfe:
                out(t.unus)
                out(f" 6 ")
                out(t.n)
            else:
                out(t.unus)
                out(f"   ")
                out(t.n)
        t.print(f"{' '*6}{t(attr='ul')}Meaning of each byte in a UTF-8 stream")
        print()
        R, s = range(16), " "*3
        if 1:   # Print column headers
            out(s)
            for i in R:
                out(f" {t.hdr}{C(i)}{t.n} ")
            print()
        for row in R:
            out(f" {t.hdr}{C(row)}{t.n} ")    # Row header
            if 0 and row == 2:
                breakpoint() # ∞∞ 
            for col in R:
                char = 16*row + col
                Item(char)
            print()
        # Print legend
        s = " "*3
        print(f"{t.ctrl}{s}{t.n} ASCII control character")
        print(f"{t.asc}{s}{t.n} ASCII character")
        print(f"{t.cont}{s}{t.n} Continuation byte")
        print(f"{t.byt1}{s}{t.n} First byte of an N-byte code sequence")
        print(f"{t.nota}{s}{t.n} Not all continuation bytes are allowed")
        print(f"{t.unus}{s}{t.n} Unused")
                
if __name__ == "__main__" and len(sys.argv) == 1:  
    PrintByteMap()
    exit() 

if __name__ == "__main__":
    lower, upper = ParseCommandLine()
    if g.binary:
        PrintBinary()
    elif g.Binary:
        PrintBinaryListing()
    elif g.symbols:
        PrintSymbols()
    else:
        PrintTable(lower, upper)
