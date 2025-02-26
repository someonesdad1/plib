"""
OneTimePad object can be used to get a random string of bytes
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2005, 2012 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # OneTimePad object can be used to get a random string of bytes
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import binascii
    import base64
    import codecs
    import os
    import random
    import sys
    import getopt
    from io import BytesIO, StringIO
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from dpstr import Chop


class OneTimePad:
    """Generate random number sequences.  If you initialize with a seed,
    the routine will use a repeatable pseudorandom number generator.
    Otherwise, the os.urandom() generator is used.
    """

    def __init__(self, numbytes=16, seed=None):
        self.numbytes = numbytes
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def binary(self, num_bytes):
        "Return a bytes object of size num_bytes"
        if self.seed is not None:
            k = hex(random.getrandbits(8 * num_bytes))[2:]
            return bytes([int(i, 16) for i in Chop(k, 2)])
        else:
            return os.urandom(num_bytes)

    def ascii(self, num_bytes):
        """Return a string of random bytes composed of the ASCII characters
        from 0x20 to 0x7e, inclusive.  If no_equals is True, remove any
        trailing '=' characters from the returned string.
        """
        s, n = self.binary(num_bytes), 0x7F - 0x20

        def f(x):
            return chr(0x20 + (x % n))

        return "".join([f(i) for i in s])

    def hex(self, num_bytes):
        s = self.binary(num_bytes)
        t = binascii.b2a_hex(s)
        return t.decode("ascii")

    def base64(self, num_bytes, no_equals=False):
        """Return random bytes in base64 encoding.  If no_equals is True,
        remove any trailing '=' characters from the returned string.
        """
        s = self.binary(num_bytes)
        t = base64.encodebytes(s)
        u = t.decode("ascii").rstrip("\n")
        if no_equals:
            u = u.rstrip("=")
        return u


def Manpage():
    name = "python otp.py"
    print(
        dedent(f"""

    This script generates sequences of bytes that are supposedly
    cryptographically secure (unless you use the -s option).  It's up to you to
    decide whether the returned information is suitable for your needs (it uses
    the urandom() method of the os module).  Here are some examples of use:

    {name} 10 2
        f5e59a2997fbcab7d0f1
        0e0f61616f1bab4726c1
      Produces two lines of hex output with 10 bytes per line.  You will not
      get the same output twice.

    {name} -s 0 10 2
        e81d14a661b85c97bf45
        36735ce60a1f41a801a8
      Same as previous example except the pseudorandom generator of the random
      module is used and you'll get the same output if the -s option's
      argument is the same.

    {name} -s 0 -b a.out 5
      Writes 5 binary bytes to the file a.out.  A hex dump of a.out shows it
      contains the bytes 145c97bf45.  You'll get the same set of bytes with the
      command '{name} -s 0 5'.

    On my system running python 3.7.10 under cygwin one Windows, note the
    output from the following command :
        for i in 1 2 3 4 5 6 7 8 9 10 ; do {name} -s 0 $i ; done
            5c
            5c97
            5c97bf
            5c97bf45
            14 5c97bf45
            14a6 5c97bf45
            14a661 5c97bf45
            14a661b8 5c97bf45
            e8 14a661b8 5c97bf45
            e81d 14a661b8 5c97bf45
      I inserted space characters to make it easier to see the pattern.  A
      big-endian system would probably produce a different pattern.

    The -B option causes output in base64 encoding:
        for i in 1 2 3 4 5 6 7 8 9 10 ; do {name} -B -s 0 $i ; done
            XA==
            XJc=
            XJe/
            XJe/RQ==
            FFyXv0U=
            FKZcl79F
            FKZhXJe/RQ==
            FKZhuFyXv0U=
            6BSmYbhcl79F
            6B0UpmG4XJe/RQ==
      The '=' characters at the end of the encoded string are padding to make
      the number of characters output divisible by 4.  There will be 0, 1,
      or 2 '=' characters at the end of each line.  If you don't want the
      '=' characters at the end, use the -C option.

    The -a option uses all of the printable ASCII characters from 0x20 to
    0x7e, inclusive.  This gives output that is more compact than base64.

    The -l and -u options can be used to change the case of the output
    strings to lower and upper case, respectively.  For hex, this makes no
    difference, but for the -B. -C. and -a forms it changes the encoding.
    -l and -u are ignored if you use the -b option for binary output.

    Some use cases

        * You can make a pretty secure password of n characters with the
          command '{name} -a n'.  If you use the -s option with the
          argument of your birthday and remember the length n, you'll be
          able to regenerate the password when needed.

        * If you have a tool that can cyclically XOR bytes of a file with a
          one-time pad file, you can encrypt/decrypt files and be assured
          that you have strong security.  You can read about the strengths
          and weaknesses at https://en.wikipedia.org/wiki/One-time_pad.
          The weakness of the technique is the generation and management of
          the one-time keys.
    """)
    )
    exit(0)


def ParseCommandLine(d):
    d["-a"] = False  # Use ASCII characters, digits, and punctuation
    d["-B"] = False  # Output in base64
    d["-C"] = False  # Output in base64 except no trailing '='
    d["-b"] = None  # Write binary to file
    d["-l"] = False  # Change output string to lowercase
    d["-s"] = None  # Seed for pseudorandom generator
    d["-u"] = False  # Change output string to uppercase
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "aBCb:hls:u")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "aBClu":
            d[o] = not d[o]
        elif o == "-b":
            d[o] = a
        elif o == "-h":
            Manpage()
        elif o == "-s":
            d[o] = a
    if not args:
        Usage(d)
    return args


def Error(*msg):
    print(*msg, file=sys.stderr)
    exit(1)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] bytes_per_line [num_lines]
      Generate cryptographically-secure random bytes.  If seed is given
      with -s, a repeatable random sequence is generated.  Output is
      num_lines (default is 1) sets of bytes_per_line hex digits.
      On my 7 year old computer, the -b option works at over 300 MB/s.
    Options
      -a        Use ASCII characters, digits, and punctuation (0x20-0x7e)
      -B        Output in base64 instead of hex
      -C        Same as -C, except no trailing '=' characters
      -b f      Output is binary bytes written to file f
      -h        More detailed help and examples
      -s s      Seed pseudorandom generator with s
    """)
    )
    exit(1)


if __name__ == "__main__":
    d = {}
    seed, num_lines = 0, 1
    args = ParseCommandLine(d)
    if len(args) == 1:
        bytes_per_line = int(args[0])
    elif len(args) == 2:
        bytes_per_line = int(args[0])
        num_lines = int(args[1])
    else:
        Usage(d)
    if num_lines < 1:
        Error("num_lines must be an integer > 0")
    if bytes_per_line < 1:
        Error("bytes_per_line must be an integer > 0")
    o = OneTimePad(numbytes=bytes_per_line, seed=d["-s"])
    if d["-b"]:
        ofp = open(d["-b"], "wb")
        for i in range(num_lines):
            ofp.write(o.binary(bytes_per_line))
    else:
        for i in range(num_lines):
            if d["-B"]:
                s = o.base64(bytes_per_line, no_equals=False)
            elif d["-C"]:
                s = o.base64(bytes_per_line, no_equals=True)
            elif d["-a"]:
                s = o.ascii(bytes_per_line)
            else:
                s = o.hex(bytes_per_line)
            if d["-l"]:
                print(s.lower())
            elif d["-u"]:
                print(s.upper())
            else:
                print(s)
