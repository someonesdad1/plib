"""
This module contains the function Banner() which can be used to print
a banner message like the UNIX banner(1) function.

28 Jul 2014 update:  added Raymond Hettinger's banner code.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # <utility> Print banner messages
    # ∞what∞#
    # ∞test∞# ignore #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from pdb import set_trace as xx


def Hettinger(string, char="X"):
    """Raymond Hettinger's banner code from
    http://code.activestate.com/recipes/577537
    """
    letterforms = r"""
       |       |       |       |       |       |       | |
  XXX  |  XXX  |  XXX  |   X   |       |  XXX  |  XXX  |!|
  X  X |  X  X |  X  X |       |       |       |       |"|
  X X  |  X X  |XXXXXXX|  X X  |XXXXXXX|  X X  |  X X  |#|
 XXXXX |X  X  X|X  X   | XXXXX |   X  X|X  X  X| XXXXX |$|
XXX   X|X X  X |XXX X  |   X   |  X XXX| X  X X|X   XXX|%|
  XX   | X  X  |  XX   | XXX   |X   X X|X    X | XXX  X|&|
  XXX  |  XXX  |   X   |  X    |       |       |       |'|
   XX  |  X    | X     | X     | X     |  X    |   XX  |(|
  XX   |    X  |     X |     X |     X |    X  |  XX   |)|
       | X   X |  X X  |XXXXXXX|  X X  | X   X |       |*|
       |   X   |   X   | XXXXX |   X   |   X   |       |+|
       |       |       |  XXX  |  XXX  |   X   |  X    |,|
       |       |       | XXXXX |       |       |       |-|
       |       |       |       |  XXX  |  XXX  |  XXX  |.|
      X|     X |    X  |   X   |  X    | X     |X      |/|
  XXX  | X   X |X     X|X     X|X     X| X   X |  XXX  |0|
   X   |  XX   | X X   |   X   |   X   |   X   | XXXXX |1|
 XXXXX |X     X|      X| XXXXX |X      |X      |XXXXXXX|2|
 XXXXX |X     X|      X| XXXXX |      X|X     X| XXXXX |3|
X      |X    X |X    X |X    X |XXXXXXX|     X |     X |4|
XXXXXXX|X      |X      |XXXXXX |      X|X     X| XXXXX |5|
 XXXXX |X     X|X      |XXXXXX |X     X|X     X| XXXXX |6|
XXXXXX |X    X |    X  |   X   |  X    |  X    |  X    |7|
 XXXXX |X     X|X     X| XXXXX |X     X|X     X| XXXXX |8|
 XXXXX |X     X|X     X| XXXXXX|      X|X     X| XXXXX |9|
   X   |  XXX  |   X   |       |   X   |  XXX  |   X   |:|
  XXX  |  XXX  |       |  XXX  |  XXX  |   X   |  X    |;|
    X  |   X   |  X    | X     |  X    |   X   |    X  |<|
       |       |XXXXXXX|       |XXXXXXX|       |       |=|
  X    |   X   |    X  |     X |    X  |   X   |  X    |>|
 XXXXX |X     X|      X|   XXX |   X   |       |   X   |?|
 XXXXX |X     X|X XXX X|X XXX X|X XXXX |X      | XXXXX |@|
   X   |  X X  | X   X |X     X|XXXXXXX|X     X|X     X|A|
XXXXXX |X     X|X     X|XXXXXX |X     X|X     X|XXXXXX |B|
 XXXXX |X     X|X      |X      |X      |X     X| XXXXX |C|
XXXXXX |X     X|X     X|X     X|X     X|X     X|XXXXXX |D|
XXXXXXX|X      |X      |XXXXX  |X      |X      |XXXXXXX|E|
XXXXXXX|X      |X      |XXXXX  |X      |X      |X      |F|
 XXXXX |X     X|X      |X  XXXX|X     X|X     X| XXXXX |G|
X     X|X     X|X     X|XXXXXXX|X     X|X     X|X     X|H|
  XXX  |   X   |   X   |   X   |   X   |   X   |  XXX  |I|
      X|      X|      X|      X|X     X|X     X| XXXXX |J|
X    X |X   X  |X  X   |XXX    |X  X   |X   X  |X    X |K|
X      |X      |X      |X      |X      |X      |XXXXXXX|L|
X     X|XX   XX|X X X X|X  X  X|X     X|X     X|X     X|M|
X     X|XX    X|X X   X|X  X  X|X   X X|X    XX|X     X|N|
XXXXXXX|X     X|X     X|X     X|X     X|X     X|XXXXXXX|O|
XXXXXX |X     X|X     X|XXXXXX |X      |X      |X      |P|
 XXXXX |X     X|X     X|X     X|X   X X|X    X | XXXX X|Q|
XXXXXX |X     X|X     X|XXXXXX |X   X  |X    X |X     X|R|
 XXXXX |X     X|X      | XXXXX |      X|X     X| XXXXX |S|
XXXXXXX|   X   |   X   |   X   |   X   |   X   |   X   |T|
X     X|X     X|X     X|X     X|X     X|X     X| XXXXX |U|
X     X|X     X|X     X|X     X| X   X |  X X  |   X   |V|
X     X|X  X  X|X  X  X|X  X  X|X  X  X|X  X  X| XX XX |W|
X     X| X   X |  X X  |   X   |  X X  | X   X |X     X|X|
X     X| X   X |  X X  |   X   |   X   |   X   |   X   |Y|
XXXXXXX|     X |    X  |   X   |  X    | X     |XXXXXXX|Z|
 XXXXX | X     | X     | X     | X     | X     | XXXXX |[|
X      | X     |  X    |   X   |    X  |     X |      X|\|
 XXXXX |     X |     X |     X |     X |     X | XXXXX |]|
   X   |  X X  | X   X |       |       |       |       |^|
       |       |       |       |       |       |XXXXXXX|_|
       |  XXX  |  XXX  |   X   |    X  |       |       |`|
       |   XX  |  X  X | X    X| XXXXXX| X    X| X    X|a|
       | XXXXX | X    X| XXXXX | X    X| X    X| XXXXX |b|
       |  XXXX | X    X| X     | X     | X    X|  XXXX |c|
       | XXXXX | X    X| X    X| X    X| X    X| XXXXX |d|
       | XXXXXX| X     | XXXXX | X     | X     | XXXXXX|e|
       | XXXXXX| X     | XXXXX | X     | X     | X     |f|
       |  XXXX | X    X| X     | X  XXX| X    X|  XXXX |g|
       | X    X| X    X| XXXXXX| X    X| X    X| X    X|h|
       |    X  |    X  |    X  |    X  |    X  |    X  |i|
       |      X|      X|      X|      X| X    X|  XXXX |j|
       | X    X| X   X | XXXX  | X  X  | X   X | X    X|k|
       | X     | X     | X     | X     | X     | XXXXXX|l|
       | X    X| XX  XX| X XX X| X    X| X    X| X    X|m|
       | X    X| XX   X| X X  X| X  X X| X   XX| X    X|n|
       |  XXXX | X    X| X    X| X    X| X    X|  XXXX |o|
       | XXXXX | X    X| X    X| XXXXX | X     | X     |p|
       |  XXXX | X    X| X    X| X  X X| X   X |  XXX X|q|
       | XXXXX | X    X| X    X| XXXXX | X   X | X    X|r|
       |  XXXX | X     |  XXXX |      X| X    X|  XXXX |s|
       |  XXXXX|    X  |    X  |    X  |    X  |    X  |t|
       | X    X| X    X| X    X| X    X| X    X|  XXXX |u|
       | X    X| X    X| X    X| X    X|  X  X |   XX  |v|
       | X    X| X    X| X    X| X XX X| XX  XX| X    X|w|
       | X    X|  X  X |   XX  |   XX  |  X  X | X    X|x|
       |  X   X|   X X |    X  |    X  |    X  |    X  |y|
       | XXXXXX|     X |    X  |   X   |  X    | XXXXXX|z|
  XXX  | X     | X     |XX     | X     | X     |  XXX  |{|
   X   |   X   |   X   |       |   X   |   X   |   X   |||
  XXX  |     X |     X |     XX|     X |     X |  XXX  |}|
 XX    |X  X  X|    XX |       |       |       |       |~|
""".splitlines()
    table = {}
    for form in letterforms:
        if "|" in form:
            table[form[-2]] = form[:-3].split("|")
    xx()
    ROWS = len(list(table.values())[0])

    def horizontal(string):
        for row in range(ROWS):
            for c in string:
                print(table[c][row].replace("X", char), end="")
            print()
        print()

    def vertical(string):
        for c in string:
            for row in zip(*table[c]):
                s = " ".join(reversed(row)).replace("X", char)
                print(s)
            print()

    if Hettinger.vertical:
        vertical(string)
    else:
        horizontal(string)


def Banner(string, char_to_use):
    """Prints the string using the character given in char_to_use.
    Example:  Banner("banner", "l") produces

         lll
          ll
          ll      lllll   ll lll  ll lll  lllll  ll lll
          lllll       l   lll ll  lll ll ll    l  lll ll
          ll  ll llllll   ll  ll  ll  ll lllllll  ll
          ll  ll l   ll   ll  ll  ll  ll ll       ll
         llllll  lllll l  ll  ll  ll  ll  lllll  llll
    """
    out = [[], [], [], [], [], [], [], []]  # 8 lines of data
    for ltr in range(len(string)):
        char = string[ltr]
        if ord(char) < 32 or ord(char) > 126:
            char = " "
        i = ord(char) - 32
        bytes = []
        lines = Banner.letters[i][0]
        # print("Lines = 0x%08x" % lines)
        out[0].append(((lines & (0xFF << 24)) >> 24) & 0xFF)
        out[1].append(((lines & (0xFF << 16)) >> 16) & 0xFF)
        out[2].append(((lines & (0xFF << 8)) >> 8) & 0xFF)
        out[3].append(lines & 0xFF)
        lines = Banner.letters[i][1]
        # print("Lines = 0x%08x" % lines)
        out[4].append(((lines & (0xFF << 24)) >> 24) & 0xFF)
        out[5].append(((lines & (0xFF << 16)) >> 16) & 0xFF)
        out[6].append(((lines & (0xFF << 8)) >> 8) & 0xFF)
        out[7].append(lines & 0xFF)
    for element in out:
        for byte in element:
            PrintByteLine(byte, char_to_use)
        print()
    print()


# The array Banner.letters contains the information on how to print
# each character between 32 and 126, inclusive.  There are 8 bytes for
# each character and each byte represents one line of the font.  The
# high byte of the first number is the first line of 8 bits, the next
# byte is the next line, and so on.  I got these numbers by writing a
# script that analyzed the output of somebody's banner program (this
# would have been in the early 1990's, so it was likely an HP-UX
# system).

Banner.letters = (
    (0x00000000, 0x00000000),
    (0x30303030, 0x30003000),
    (0x6C6C6C00, 0x00000000),
    (0x6C6CFE6C, 0xFE6C6C00),
    (0x187E407E, 0x027E1800),
    (0xC2C60C18, 0x3066C600),
    (0x3828387B, 0xD6CC7700),
    (0x60204000, 0x00000000),
    (0x1C70C0C0, 0xC0701C00),
    (0x701C0606, 0x061C7000),
    (0x006C38FE, 0x386C0000),
    (0x303030FC, 0x30303000),
    (0x00000000, 0x00602040),
    (0x0000007C, 0x00000000),
    (0x00000000, 0x00060600),
    (0x02060C18, 0x3060C000),
    (0x7CC6CED6, 0xE6C67C00),
    (0x10703030, 0x30307800),
    (0x78CC0C18, 0x3062FE00),
    (0x78CC0C38, 0x0CCC7800),
    (0x0C1C6CCC, 0xFE0C1E00),
    (0x7E40407C, 0x06C67C00),
    (0x3C64C0FC, 0xC6C67C00),
    (0xFE860C18, 0x18181800),
    (0x3C66663C, 0x66663C00),
    (0x7CC6C67E, 0x064C7800),
    (0x00006060, 0x00606000),
    (0x00006060, 0x00602040),
    (0x183060C0, 0x60301800),
    (0x00007C00, 0x7C000000),
    (0xC0603018, 0x3060C000),
    (0x78CC8C1C, 0x30003000),
    (0x3C46C2CE, 0xCC407800),
    (0x183C6666, 0x7E666600),
    (0xFC66667C, 0x6666FC00),
    (0x3C66C0C0, 0xC2663C00),
    (0xFC666666, 0x6666FC00),
    (0xFE626878, 0x6862FE00),
    (0xFE626878, 0x6860F000),
    (0x3C64C0C0, 0xCE663A00),
    (0xCCCCCCFC, 0xCCCCCC00),
    (0x3C181818, 0x18183C00),
    (0x3C181818, 0x98D87000),
    (0xE6666C78, 0x6C66E600),
    (0xF0606060, 0x6066FE00),
    (0xC6EEFED6, 0xC6C6C600),
    (0xC6E6F6DE, 0xCEC6C600),
    (0x7CC6C6C6, 0xC6C67C00),
    (0xFC66667C, 0x6060F000),
    (0x7CC6C6C6, 0xC6C67C06),
    (0xFC66667C, 0x6C66E600),
    (0x7EC2C07C, 0x0686FC00),
    (0x7E5A1818, 0x18183C00),
    (0x66666666, 0x66663C00),
    (0xC6C6C66C, 0x6C381000),
    (0xC6C6C6D6, 0xFEEEC600),
    (0xEE6C3810, 0x386CEE00),
    (0xC3663C18, 0x18183C00),
    (0xFE860C18, 0x3062FE00),
    (0x7C606060, 0x60607C00),
    (0xC0603018, 0x0C060200),
    (0x3E060606, 0x06063E00),
    (0x10386CC6, 0x00000000),
    (0x00000000, 0x00007C00),
    (0x0C080400, 0x00000000),
    (0x00007C04, 0xFC8CFA00),
    (0xE060607C, 0x6666FC00),
    (0x00007CC6, 0xC0C67C00),
    (0x1C0C0C7C, 0xCCCC7A00),
    (0x00007CC2, 0xFEC07C00),
    (0x386C60F8, 0x6060F000),
    (0x00007BC6, 0xC67E047C),
    (0xE060606E, 0x7666E700),
    (0x18003818, 0x18183C00),
    (0x18003C18, 0x1818D870),
    (0xE060666C, 0x706CE600),
    (0x38181818, 0x18183C00),
    (0x0000ECD6, 0xD6C6E700),
    (0x00006E76, 0x66666600),
    (0x00003C66, 0x66663C00),
    (0x0000DC66, 0x667C60F0),
    (0x000076CC, 0xCC7C0C1E),
    (0x0000DC76, 0x6060F000),
    (0x0000FEC0, 0xFE06FE00),
    (0x10307C30, 0x30361C00),
    (0x0000CECC, 0xCCCC7600),
    (0x00006666, 0x663C1800),
    (0x0000C6D6, 0xD6FE6C00),
    (0x0000C66C, 0x386CC600),
    (0x0000C6C6, 0xC67E0478),
    (0x0000FC98, 0x3064FC00),
    (0x0C181830, 0x18180C00),
    (0x10101000, 0x10101000),
    (0x60303018, 0x30306000),
    (0x66980000, 0x00000000),
)


def PrintByteLine(byte, char_to_use):
    for i in range(8):
        if byte & (1 << (8 - i)):
            print("%s" % char_to_use, end="")
        else:
            print(" ", end="")


def Example(string):
    """Prints the string to stdout with each ASCII character
    from 33 to 255.
    """
    for i in range(33, 256):
        print("Character ASCII value =", i)
        Banner(string, chr(i))


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    s = """
Usage:  {name} [-e] string
  Prints a banner message.

Options
    -a      Use Raymond Hettinger's implementation; his does both
            horizontal and vertical output.
    -c c    Use the character c for printing the banner.  c must be an
            integer; the low 7 bits are used.
    -e      Print the string in each of the ASCII characters from 33
            to 255 to let you see the effects of different character
            choices.
    -v      Vertical output (implies -a).
"""[1:-1]
    print(s.format(**locals()))
    exit(status)


def ParseCommandLine(d):
    d["-a"] = False  # Use Hettinger's implementation
    d["-c"] = "X"  # Character to use
    d["-e"] = False  # Print for all usable characters
    d["-v"] = False  # Vertical output (implies -a)
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ac:ev")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-a":
            d["-a"] = True
        if opt[0] == "-c":
            try:
                d["-c"] = chr(int(opt[1]) & 0x7F)
            except Exception:
                Error("'%s' isn't a valid character for -c" % opt[1])
        if opt[0] == "-e":
            d["-e"] = True
        if opt[0] == "-v":
            d["-a"] = d["-v"] = True
    if len(args) < 1:
        Usage(d)
    return args


if __name__ == "__main__":
    d = {}
    args = ParseCommandLine(d)
    string = " ".join(args)
    if d["-e"]:
        Example(string)
        exit(0)
    if d["-a"]:
        Hettinger.vertical = True if d["-v"] else False
        Hettinger(string, d["-c"])
    else:
        Banner(string, d["-c"])
