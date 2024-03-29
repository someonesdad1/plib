'''
Various binary messages for extraterrestrial communication

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
        # Gives various binary messages for extraterrestrial communication
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import hashlib
        import os
        from pathlib import Path as P
        import sys
        from textwrap import dedent
        from collections import deque
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        if 0:   # Drops into debugger on exception
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        ii = isinstance
        # Screen dimensions
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def GetColors():
        t.dbg = t("lill")
        t.ruler = t("sky")
        t.N = t.n
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        This script grew out of my interest in seeing both the content and bitmap
        interpretation of these old messages put forward as examples to communicate
        with extraterrestrial beings.
 
        Oliver (hypothetical, never sent)
 
            Page 5 of [1] gives a 1271 bit = 31*41 message in Figure 1, which I
            screen scraped from the PDF (using the SumatraPDF viewer).  Barney Oliver
            constructed this message in 1961 after a conference in Green Bank.  The
            decrypted message is shown on pg 6.  Page 7 contains the interpretation.
            As far as I know, this message was never sent, but it provided many of
            the ideas for Drake's 1974 Arecibo message.
 
        Drake (hypothetical, never sent)
 
            This message is given in binary form on page 423 of [2], but it appears
            to have errors when compared to the decoding given in figure 30-2 on page
            425 (in particular, the carbon atom is wrong).
 
        Arecibo (Arecibo message 16 Nov 1974) See [3, 5, 6].
 
            This is a binary message of 1679 bits (73*23) sent via the Arecibo radio
            telescope in Puerto Rico on 16 Nov 1974 (see [3]).  The signal was aimed
            at M13, which is 25 kly away, so an answer will take 50 thousand years.
            A copy is at [4], which is used for the binary string in this script.
 
            The message was at 2.38 GHz, was frequency modulated, and had a bandwidth
            of 10 Hz, resulting in about 10 bits/second.  It took less than 3 minutes
            to send and was sent only once.  The Arecibo telescope was 305 m in
            diameter and the broadcast power was on the order of 1 MW.  The purpose
            was to demonstrate the revised Arecibo radio telescope, not to try to
            communicate with anyone.

        Even with the explanations of these bitmaps, they can be a bit hard to follow
        or see without careful studying.  I got interested in these messages after
        reading [7] again, which I consider an excellent book because of the careful
        and thoughtful contributions of the confererence's attendees (many were
        amongst the top scientists at the time).  I loaned the book to a friend, both
        because I thought he might be interested in some of the discussions and some
        of the ideas/topics might make for interesting discussions/projects amongst
        his students.  I was wondering if it could help make good term or research
        projects for students.  Since his students are computer science students, I
        wondered if software could be written that would extract some of the messages
        within the bitmap.

        References
        ----------
            URLs downloaded about 17 Dec 2023
            
        [1] https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cryptologic-spectrum/communications_extraterrestrial_intelligence.pdf
            "Communication with Extraterrestrial Intelligence", DOCID 3052333, author
            Lambros D. Callimahos.  No date given, but probably 1975 because it
            refers to the Arecibo message of 1974 as "last November".
        [2] Sklovskii & Sagan, "Intelligent Live in the Universe", Delta, 1966
        [3] https://en.wikipedia.org/wiki/Arecibo_message
        [4] https://pages.uoregon.edu/jimbrau/astr123/Notes/ch28/73by23.html
        [5] https://www.universetoday.com/153920/what-is-the-arecibo-message/
        [6] https://www.seti.org/seti-institute/project/details/arecibo-message
        [7] Sagan (ed.), "Communication with Extraterrestrial Intelligence", MIT
            Press, 1975
        [8] https://en.wikipedia.org/wiki/Lincos_language
        [9] https://math.dartmouth.edu/~carlp/PDF/extraterrestrial.pdf
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] action
          Actions:
            1   Plot the Barney Oliver 1961 data
            2   Plot the Arecibo 1974 data
            3   Plot the Drake data from 1966 or before
            4   Print the Oliver data
            5   Print the Arecibo data
            6   Print the Drake data
        Options:
            -0 c    Character for 0's
            -1 c    Character for 1's
            -2      Double the number of horizontal bits in plot
            -d      Turn on debug printing
            -h      Show manpage
            -r      Flip rows & columns when printing to see "other" bitmap
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-0"] = " "       # Character for 0 (others:  ․ ‥)
        d["-1"] = "X"       # Character for 1 (others:  ● █ ■ ⛝)
        d["-2"] = False     # Double horizontal bits in plot
        d["-2"] = False     # Double horizontal bits in plot
        d["-d"] = False     # Turn on debug printing
        d["-r"] = False     # Flip bitmap
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0:1:2dhr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("2dr"):
                d[o] = not d[o]
            elif o in ("-0", "-1"):
                d[o] = a
            elif o == "-1":
                d[o] = a
            elif o == "-h":
                Manpage()
        g.zero = d["-0"]
        g.one = d["-1"]
        if d["-d"]:
            g.dbg = True
        return args
    def Assert(cond, debug=False, msg=""):
        '''Similar to assert, but you'll be dropped into the debugger on an
        exception if debug is True, Assert.debug is True, or 'Assert' is
        a nonempty environment string.  If msg is not empty, it's printed
        out.
        '''
        if not cond:
            if debug or Assert.debug or os.environ.get("Assert", ""):
                if msg:
                    print(msg, file=sys.stderr)
                print("Type 'up' to go to line that failed", file=sys.stderr)
                breakpoint()
            else:
                raise AssertionError(msg)
    Assert.debug = False
if 1:   # Core functionality
    def GetOliver():
        'Return the 1271 bit Oliver message'
        # Screen-scraped from PDF of pg 5 of ref [1]
        s = '''
            1000000000000000000000000000000000000000
            1000011100000000001000001000000100000100
            0000010001000000000000000000000000000000
            0000001000100001000000100000000000010000
            0000000100010000010000001000000001000100
            010000000111Q000000o.o0000010000000000001
            0000000000000000000000000000000000000000
            000000000000~000000000001000001000000100
            0001000011000100000000001100000000000000
            0000000000000000000110000110000110000110
            1101101101001100001100101100101100100100
            1001001001010100100100001100001100001100
            0011000011000000000100000000000111110100
            0000000000000000000100000000000100000100
            0000000001011011100100000000000001111101
            0000000000000000000000000000100000000000
            0000001000100111000000000000101000000000
            0000001010010000110010101110010100000000
            0000000101001000010000000000100100000000
            0000000001001000001000000000001111100000
            0000000011111000000111010100000010101000
            0000000010101000000010000000000010001010
            0000000010100010000000000000000001000100
            1000100010011011001110110110100000100010
            0010101010001000100000000000000000010001
            0001001001000100010000001000000000000111
            0000011111000001ll0000000lllll0100000l01
            0100000101000001000100000010000000000100
            0001000011100001000001000001000000000010
            00001000l000l000100000l000001l000110000l
            0000010001000100010000010000011000000001
            1000001101100011011000001100111
        '''
        s = s.replace("\n", "").replace(" ", "")
        Assert(len(s) == 1271 + 1)  # The '.' is an extra character
        if 1: # Fix the data
            '''The set of non-whitespace characters in the data is '.01Qlo~'.
            I would make the following substitutions:

                            Row Col
                .   ' '      6   21  Length of line indicates it's spurious
                0   None    
                1   None    
                Q   '0'      6   13
                l   '1'     various  Easy to see why confused with 1
                o   '0'      6   20
                ~   '0'      8   13  Gotten by counting in figure 2  
            It's supposed to be 41 columns and 31 rows.  However, return the string
            of 1271 characters.
            '''
            # Remove spaces and newlines
            s = s.replace(" ", "").replace("\n", "")
            # Remove the '.'
            s = s.replace(".", "")
            # Other fixes
            s = s.replace("l", "1")
            s = s.replace("Q", "0")
            s = s.replace("o", "0")
            s = s.replace("~", "0")
        Assert(len(s) == 1271)
        return s
    def GetDrake():
        'Return the 551 bit Drake message'
        # From Shklovskii & Sagan [2] pg 423 
        s = '''
        11110000101001000011001000000010000010100
        10000011001011001111000001100001101000000
        00100000100001000010000101010000100000000
        00000000001000100000000001011000000000000
        00000001000111011010110101000000000000000
        00001001000011101010101000000000101010101
        00000000011101010101110101100000001000000
        00000000000100000000000001000100111111000
        00111010000010110000011100000001000000000
        10000000010000000111110000001011000101110
        10000000110010111110101111100010011111001
        00000000000111110000001011000111111100000
        10000011000001100001000011000000011000101
        001000111100101111
        '''
        s = s.replace("\n", "").replace(" ", "")
        Assert(len(s) == 551)
        return s
    def GetArecibo():
        'Return the 1679 bit Arecibo message'
        # From https://pages.uoregon.edu/jimbrau/astr123/Notes/ch28/73by23.html
        s = '''
            00000010101010000000000 00101000001010000000100
            10001000100010010110010 10101010101010100100100
            00000000000000000000000 00000000000011000000000
            00000000001101000000000 00000000001101000000000
            00000000010101000000000 00000000011111000000000
            00000000000000000000000 11000011100011000011000
            10000000000000110010000 11010001100011000011010
            11111011111011111011111 00000000000000000000000
            00010000000000000000010 00000000000000000000000
            00001000000000000000001 11111000000000000011111
            00000000000000000000000 11000011000011100011000
            10000000100000000010000 11010000110001110011010
            11111011111011111011111 00000000000000000000000
            00010000001100000000010 00000000001100000000000
            00001000001100000000001 11111000001100000011111
            00000000001100000000000 00100000000100000000100
            00010000001100000001000 00001100001100000010000
            00000011000100001100000 00000000001100110000000
            00000011000100001100000 00001100001100000010000
            00010000001000000001000 00100000001100000000100
            01000000001100000000100 01000000000100000001000
            00100000001000000010000 00010000000000001100000
            00001100000000110000000 00100011101011000000000
            00100000001000000000000 00100000111110000000000
            00100001011101001011011 00000010011100100111111
            10111000011100000110111 00000000010100000111011
            00100000010100000111111 00100000010100000110000
            00100000110110000000000 00000000000000000000000
            00111000001000000000000 00111010100010101010101
            00111000000000101010100 00000000000000101000000
            00000000111110000000000 00000011111111100000000
            00001110000000111000000 00011000000000001100000
            00110100000000010110000 01100110000000110011000
            01000101000001010001000 01000100100010010001000
            00000100010100010000000 00000100001000010000000
            00000100000000010000000 00000001001010000000000
            01111001111101001111000
        '''
        s = s.replace("\n", "").replace(" ", "")
        Assert(len(s) == 1679)
        return s
    def PlotRows(s, nrows, one="1", zero="0", double=False):
        '''Given the binary string s, print out the 1's and 0's with the
        indicated characters.  If double is True, then print two characters
        for each bit, as this can help with the anisotropic nature of a
        terminal screen.  Print the date in the indicated number of rows.
        The number of columns is gotten from the number of bits in s.
        '''
        Assert(set(s) == set("01"))
        ncols = len(s)//nrows
        Dbg(f"PlotRows:  {len(s)} bits, {nrows} rows, {ncols} columns")
        if ncols*nrows != len(s):
            Dbg(f"  Warning:  ncols*nrows != len(s)")
        # Print a header to get column numbering
        tens = (ncols + 1)//10 + 1
        if double:
            print("  ", end="")
            for i in range(1, tens):
                print(f"{i:20d}", end="")
            print()
            print("   ", end="")
            for i in range(ncols):
                print(f"{(i + 1) % 10} ", end="")
        else:
            print("   ", end="")
            for i in range(1, tens):
                print(f"{i:10d}", end="")
            print()
            print("   ", end="")
            for i in range(ncols):
                print(f"{(i + 1) % 10}", end="")
        # Print the data rows with a leading row number
        for i, c in enumerate(s):
            if i % ncols == 0:
                print(f"\n{i//ncols + 1:2d} ", end="")
            char = one*2 if double else one
            if c == "0":
                char = zero + zero if double else zero
            print(char, end="")
        print()
    def PlotOliver():
        s = GetOliver()
        print("Barney Oliver message from 1961\n")
        # 1271 bits = 31*41
        rows = 41 if d["-r"] else 31
        PlotRows(s, nrows=rows, one=g.one, zero=g.zero, double=d["-2"])
    def PrintOliver():
        s = GetOliver()
        print("Barney Oliver message from 1961")
        PrintSummary(s)
    def PlotArecibo():
        s = GetArecibo()
        print("Arecibo message from 1974\n")
        # 1679 bits = 23*73
        rows = 23 if d["-r"] else 73
        PlotRows(s, nrows=rows, one=g.one, zero=g.zero, double=d["-2"])
    def PrintArecibo():
        s = GetArecibo()
        print("Arecibo message from 1974")
        PrintSummary(s)
    def PlotDrake():
        s = GetDrake()
        print("Drake message from Shklovskii & Sagan pg 423 \n")
        # 551 bits = 19*29
        rows = 19 if d["-r"] else 29
        PlotRows(s, nrows=rows, one=g.one, zero=g.zero, double=d["-2"])
    def PrintDrake():
        s = GetDrake()
        print("Drake message from Shklovskii & Sagan pg 423")
        PrintSummary(s)
        print(dedent('''
        
        Note:  I suspect there are errors in the table on page 423 because the carbon
        atom picture is wrong.'''))
    def PrintSummary(s):
        'Print a summary of the message string s'
        bits = len(s)
        cksum = sum(int(i) for i in s)
        md5 = hashlib.md5()
        md5.update(s.encode())
        print(f"  {len(s)} bits:  {cksum} 1's, {bits - cksum} 0's")
        print(f"  MD5 hash of binary string:  {md5.hexdigest()}")
        PrintBinaryString(s)
    def PrintBinaryString(s):
        '''Fit the string s to the screen and use a number of columns that
        is divisible by 10.  Also use rulers to help see rows and columns.
        '''
        n = g.W
        while n % 10:
            n -= 1
        m = 0   # Keep track of number of characters printed
        # Divide into rows
        rows = []
        for i in range(0, len(s) + 1, n):
            row = s[i:i + n]
            rows.append(row)
            m += len(row)
        Assert(m == len(s))
        # Print the header
        w = len(str(len(rows)))
        m = n//10
        print(f"{' '*w} {t.ruler}", end="")
        for i in range(m):
            s = str(i + 1)
            u = " "*(10 - len(s))
            print(f"{u}{s}", end="")
        t.print()
        # Print the rows
        t.print(f"{' '*w} {t.ruler}{'1234567890'*m}")
        for i, row in enumerate(rows):
            print(f"{t.ruler}{i + 1:{w}d}{t.n} {row}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    GetColors()
    action = int(args[0])
    if action == 1:
        PlotOliver()
    elif action == 2:
        PlotArecibo()
    elif action == 3:
        PlotDrake()
    elif action == 4:
        PrintOliver()
    elif action == 5:
        PrintArecibo()
    elif action == 6:
        PrintDrake()
    else:
        Error(f"{action} is an illegal action")
