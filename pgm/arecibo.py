'''
This is a binary message sent via the Arecibo radio telescope in Puerto
Rico in 1961.  The signal was aimed at M13, which is 24 kly away, so an
answer will take 48 kyears, which would have been 2009.  I don't know if
anyone deliberately did any listening for an answer.

https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cryptologic-spectrum/communications_with_extraterrestrial.pdf
Downloaded Sun 17 Dec 2023 04:08:12 PM

Page 6 states Barney Oliver made this message in 1961 and it has 1271
(product of two prime factors 31 and 41) binary digits.

I got the data by screen scraping the above PDF in Chrome's PDF viewer.  It
actually did fairly well (particularly when you know that getting text
lines from a PDF is nontrivial) and it wasn't hard to correct the few
errors.

The script will print out the binary data in an array of 41 dots per line
and 31 lines.

Sklovskii & Sagan, "Intelligent Live in the Universe", Delta, 1966
    Page 423 gives a similar binary message created by F. Drake to simulate
    a hypothetical message received on Earth.  It is 551 bits and has
    content very similar to Oliver's message.
'''
from wrap import dedent
from lwtest import Assert
from collections import deque
if 1:
    import debug
    debug.SetDebugger()

Oliver = '''
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 1 1 1 Q 0 0 0 0 0 0 o.o 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 ~ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0
1 1 0 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 1 0 1 1 0 0 1 0 1 1 0 0 1 0 0 1 0 0
1 0 0 1 0 0 1 0 0 1 0 1 0 1 0 0 1 0 0 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 1 0 1 1 0 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 1 1 0 0 1 0 1 0 1 1 1 0 0 1 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 0 0 0 0 1 0 1 0 1 0 0 0
0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 1 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0
1 0 0 0 1 0 0 0 1 0 0 1 1 0 1 1 0 0 1 1 1 0 1 1 0 1 1 0 1 0 0 0 0 0 1 0 0 0 1 0
0 0 1 0 1 0 1 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1
0 0 0 1 0 0 1 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 1 l l 0 0 0 0 0 0 0 l l l l l 0 1 0 0 0 0 0 l 0 1
0 1 0 0 0 0 0 1 0 1 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 1 0 0 0 l 0 0 0 l 0 0 0 1 0 0 0 0 0 l 0 0 0 0 0 1 l 0 0 0 1 1 0 0 0 0 l
0 0 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 1 1 0 1 1 0 0 0 1 1 0 1 1 0 0 0 0 0 1 1 0 0 1 1 1 
'''[1:-1]
Drake = '''
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
'''[1:-1]
def GetOliver():
    '''The set of non-whitespace characters in the screen-scraped message
    is '.01Qlo~'.  I would make the following substitutions:
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
    s = Oliver
    if 0:   # Show characters in raw data
        print(''.join(sorted(set(s))))
    if 0:   # Print with ruler and numbered rows
        print(dedent('''
        1-based line number starts each line
                    1         2         3         4    
           ····+····|····+····|····+····|····+····|····+
        '''))
    
        for i, line in enumerate(data2.split("\n")):
            print(f"{i+1:2d} {line.strip().replace(' ', '')}")
    if 1:   # Fix the data
        # Remove spaces and newlines
        s = s.replace(" ", "").replace("\n", "")
        # Remove the '.'
        s = s.replace(".", "")
        Assert(len(s) == 1271)
        # Other fixes
        s = s.replace("l", "1")
        s = s.replace("Q", "0")
        s = s.replace("o", "0")
        s = s.replace("~", "0")
        # Should be only 0 and 1
        Assert(set(s) == set("01"))
    return s
def PrintRows(s, nrows, one="1", zero="0", double=False):
    ncols = len(s)//nrows
    # Print a header to get column number
    if double:
        print("  ", end="")
        for i in range(1, (ncols + 1)//10):
            print(f"{i:20d}", end="")
        print()
        print("   ", end="")
        for i in range(ncols):
            print(f"{(i + 1) % 10} ", end="")
    else:
        print("  ", end="")
        for i in range(1, (ncols + 1)//10):
            print(f"{i:10d}", end="")
        print()
        print("   ", end="")
        for i in range(ncols):
            print(f"{(i + 1) % 10}", end="")
    # Print the data rows
    for i, c in enumerate(s):
        if i % ncols == 0:
            print(f"\n{i//ncols + 1:2d} ", end="")
        char = one + one if double else one
        if c == "0":
            char = zero + zero if double else zero
        print(char, end="")
    print()
def GetDrake():
    s = Drake.replace("\n", "")
    Assert(len(s) == 551)
    return s

action = 2
if action == 0:     # Print the Oliver raster pattern
    oliver = GetOliver()
    if 1:
        # Print 31 rows
        one = "●"
        one = "█"
        zero = " "
        zero = "‥"
        zero = "․"
        PrintRows(oliver, nrows=31, one=one, zero=zero, double=True)
    else:
        # Print 41 rows
        PrintRows(oliver, nrows=41, one="█", zero="‥")
elif action == 1:
    # Encode the Oliver message in hex
    oliver = RecoverData(Oliver)
    bits = 8
    msg = []
    src = oliver
    while src:
        m = src[:bits]
        src = src[bits:]
        if len(m) != 8:
            breakpoint() #xx
        val = int(m, 2)
        u = f"{val:02x}"
        msg.append(f"{u:2s}")
    for i, u in enumerate(msg):
        if i and i % 25 == 0:
            print()
        print(f"{u} ", end="")
    print()
    if 1:   # Recover the binary; prove it by printing the picture
        o = []
        for i in msg:
            u = f"{int(i, 16):08b}"
            o.append(u)
            print(o)
        new_s = ''.join(o)
        Assert(oliver == new_s)
elif action == 2:
    # Plot the Drake data
    drake = GetDrake()
    # Factors of len(drake) == 551 are 19 and 29
    if 1:
        # Print 29 rows
        one = "●"
        one = "█"
        zero = "․"
        PrintRows(drake, nrows=29, one=one, zero=zero, double=True)
    else:
        # Print 41 rows
        PrintRows(drake, nrows=19, one=one, zero=zero, double=False)
