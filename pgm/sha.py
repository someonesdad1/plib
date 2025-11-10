'''
Print out the SHA hashes for files on the command line.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Print hashes for files on the command line
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from pathlib import Path as P
        import getopt
        import hashlib
        import os
        import re
        import sys
        import zlib
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
    if 1:  # Global variables
        t.trunc = t.brnl
if 1:  # Utility
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Calculate the hash of the given files.  Use '-' for stdin.  If a
          command line argument is a directory, it's silently ignored.
        Options:                        Bits in hash
            -1      SHA-1                      160
            -2      SHA-224                    224
            -3      SHA-256 (default)          256
            -4      SHA-384                    384
            -5      SHA-512                    512
            -6      MD5                        128
            -7      CRC32                       32
            -8      ADLER32                     32
            -a      Show hash for each of the different methods
            -c n    Truncate hash to n characters
            -t      Truncate all hashes to 16 characters
            -w      Open as UTF8 text file, read, remove all whitespace,
                    encode to bytes, then calculate hash
            ''')
        )
        exit(status)
    def ParseCommandLine():
        d["-a"] = False  # Use all hash methods
        d["-h"] = False  # Help
        d["-n"] = None   # Truncate hash to n characters
        d["-t"] = False  # Truncate hash to 16 characters
        d["-w"] = False  # Remove whitespace from each file
        d["-1"] = False  # SHA1
        d["-2"] = False  # SHA224
        d["-3"] = False  # SHA256
        d["-4"] = False  # SHA384
        d["-5"] = False  # SHA512
        d["-6"] = False  # MD5
        d["-7"] = False  # CRC32
        d["-8"] = False  # ADLER32
        d["method"] = {
            "-1": (hashlib.sha1, "SHA1"),
            "-2": (hashlib.sha224, "SHA224"),
            "-3": (hashlib.sha256, "SHA256"),
            "-4": (hashlib.sha384, "SHA384"),
            "-5": (hashlib.sha512, "SHA512"),
            "-6": (hashlib.md5, "MD5"),
            "-7": (zlib.crc32, "CRC32"),
            "-8": (zlib.adler32, "ADLER32"),
        }
        try:
            opts, files = getopt.getopt(sys.argv[1:], "12345678ahn:tw")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        L = d["L"] = "-1 -2 -3 -4 -5 -6 -7 -8".split()
        for o, a in opts:
            if o in L + ["-a", "-t", "-w"]:
                d[o] = not d[o]
            elif o == "-n":
                d[o] = int(a)
                if d[o] <= 0:
                    Error("-n option must be > 0")
        if d["-t"]:
            d["-n"] = 32
        if d["-a"]:
            for i in L:
                d[i] = True
        if not files or d["-h"]:
            Usage()
        num = sum([d[i] for i in L])
        if not num:
            d["-3"] = True  # Use SHA256 by default
        d["more_than_one"] = num > 1
        return files
if 1:  # Core functionality
    def GetHash(Bytes, method):
        'Return (h, t) where h is hash and t is True if truncated'
        truncated = False
        if method == zlib.crc32:
            i = zlib.crc32(Bytes)
            h = f"{i:08x}"
        elif method == zlib.adler32:
            i = zlib.adler32(Bytes)
            h = f"{i:08x}"
        else:
            h = eval("method()")
            h.update(Bytes)
            h = h.hexdigest()
        if d["-n"] is not None:
            old = h
            new = h[:d["-n"]]
            truncated = True if old != new else False
            h = new
        return (h, truncated)
    def GetBytes(file):
        "Read file in binary as a bytes object"
        if file == "-":
            # Method to read stdin as binary
            b = sys.stdin.buffer.read()
        else:
            p = P(file)
            if p.is_dir():
                return None
            try:
                b = p.open("rb").read()
            except Exception:
                print(f"Couldn't read {file!r}", file=sys.stderr)
                return None
        assert type(b) == bytes
        return b
    def GetTextFile(file):
        'Read as UTF8 text, remove whitespace, return bytes'
        if file == "-":
            b = sys.stdin.read()
        else:
            p = P(file)
            if p.is_dir():
                return None
            try:
                b = p.open("r").read()
            except Exception:
                print(f"Couldn't read {file!r}", file=sys.stderr)
                return None
        # Remove whitespace
        b = re.sub(r"\s+", "", b)
        # Convert to binary
        b = b.encode()
        return b

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine()
    show_color_message = False
    for file in files:
        if d["-w"]:
            b = GetTextFile(file)
        else:
            b = GetBytes(file)
        if b is None:
            continue
        if d["more_than_one"]:
            print(file)
            for i in d["L"]:
                if d[i]:
                    method, name = d["method"][i]
                    h, truncated = GetHash(b, method)
                    if truncated:
                        t.print(f"{t.trunc}  {name:7s} {h}")
                        show_color_message = True
                    else:
                        print(f"  {name:7s} {h}")
        else:
            for i in d["L"]:
                if d[i]:
                    method, name = d["method"][i]
                    h, truncated = GetHash(b, method)
                    if truncated:
                        t.print(f"{t.trunc}{h} {'<stdin>' if file == '-' else file}")
                        show_color_message = True
                    else:
                        print(f"{h} {'<stdin>' if file == '-' else file}")
    if show_color_message:
        print(f"A hash in {t.trunc}this color{t.n} means it was truncated")
