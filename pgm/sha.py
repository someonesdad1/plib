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
        import re
        import sys
        import zlib
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:    # Global variable container
            pass
        g = G()
        # Colors
        t.d = t.sky
        t.trunc = t.brnl
        t.err = t.redl
        t.name = t.ornl
        # Hash method numbers to the method's constructor
        g.hash_method = {
            0:  hashlib.sha256,
            1:  hashlib.md5,
            2:  hashlib.sha1,
            3:  hashlib.sha224,
            4:  hashlib.sha384,
            5:  hashlib.sha512,
            6:  zlib.crc32,
            7:  zlib.adler32}
        # This is set to True if -t or -n option used
        g.show_color_message = False
if 1:  # Utility
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Manpage():
        print(dedent(f'''

        The -t option is intended to help compare text files.  The letters in the -t
        option determine the processing done on the file:

            a   'ASCIIFY' the file by converting Unicode characters to rough ASCII
                equivalents.  This transliteration is idiomatic because it was done
                by my judgment [see /plib/asciify.py].  It also won't convert any 
                Unicode characters that don't look similar to Latin letters.
            b   Remove characters under 0x20
            s   Remove all whitespace
            p   Remove all punctuation
            l   Convert to lower case
            u   Convert to upper case
            a   Remove all non-ASCII characters

        For example, if you used '-t spal', the resulting file that is hashed would only
        have 

        '''))
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Calculate the SHA-256 hash of the given files.  Use '-' for stdin.
        Options:                          Bytes in hash
            -a      Show hash for each of the different methods
            -H      Show manpage
            -m n    Select other hash method
            -n n    Truncate hash to n bytes
            -s      Print hash name in color to stderr
            -t n    Process text files in special ways.  See -H manpage.
            -w      Open as UTF8 text file, read, remove all whitespace,
                    encode to bytes, then calculate hash
        Other hash methods                Bytes in hash{t.d}
            0       SHA-256 (default)           32{t.n}
            1       MD5                         16
            2       SHA-1                       20
            3       SHA-224                     28
            4       SHA-384                     48
            5       SHA-512                     64
            6       CRC32                        4
            7       ADLER32                      4
        '''))
        exit(status)
    def ParseCommandLine():
        d["-a"] = False  # Use all hash methods
        d["-h"] = False  # Help
        d["-m"] = 0      # Hash method to use
        d["-n"] = None   # Truncate hash to n bytes
        d["-s"] = False  # Print hash name in color to stderr
        d["-t"] = None   # Process text file specially
        d["-w"] = False  # Remove whitespace from each file
        try:
            opts, files = getopt.getopt(sys.argv[1:], "aHhm:n:stw")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in opts:
            if o[1] in "astw":
                d[o] = not d[o]
            elif o == "-H":     # Show manpage
                Manpage()
            elif o == "-m":     # Select hash method
                d[o] = int(a)
                if d[o] not in g.hash_method:
                    must = ', '.join(str(i) for i in g.hash_method.keys())
                    Error(f"-m option must in {must}")
            elif o == "-n":     # Truncate hash to n bytes
                d[o] = int(a)
                if d[o] <= 0:
                    Error("-n option must be > 0")
            elif o == "-t":     # Process text file
                d[o] = int(a)
                if d[o] <= 0:
                    Error("-t option must be > 0")
        if not files or d["-h"]:
            Usage()
        return files
if 1:  # Core functionality
    def GetHash(Bytes, method):
        '''Return (h, t) where h is hash and t is True if truncated.
        Bytes  = string of bytes to hash
        method = integer indicating the hash method to use in g.method
        '''
        if method not in g.hash_method:
            raise ValueError(f"{method!r} is bad hash method number")
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
        if d["-n"] is not None:     # Truncate hash to n bytes
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
            try:
                b = p.open("rb").read()
            except Exception:
                t.print(f"{t.err}Couldn't read {file!r}", file=sys.stderr)
                return None
        assert type(b) is bytes
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
    def ProcessFile(file):
        p = P(file)
        if p.is_dir():
            t.print(f"{t.err}{file!r} is a directory", file=sys.stderr)
            return
        # Get the relevant bytes in the file
        b = GetTextFile(file) if d["-w"] else GetBytes(file)
        if b is None:
            return
        if d["-a"]:     # Show for all hash methods
            breakpoint() # ∞∞ 
        else:
            hash_method = g.hash_method[d["-m"]]
            try:
                hsh = hash_method()
                hsh.update(b)
                hexdigest = hsh.hexdigest()
                print("digest", hexdigest)
            except TypeError:
                # CRC32 or ADLER32
                hsh = hash_method(b)
                hexdigest = f"{hsh:08x}"
        if d["-n"]:     # Truncate hash to n bytes
            hexdigest = hexdigest[:2*d["-n"]]
        print(hexdigest)
        exit() # ∞∞ 


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine()
    for file in files:
        ProcessFile(file)

    if 0:   # Old code
        if d["-w"]:
            b = GetTextFile(file)
        else:
            b = GetBytes(file)
        if b is None:
            pass
            #continue
        if d["more_than_one"]:
            print(file)
            for i in d["L"]:
                if d[i]:
                    method, name = d["method"][i]
                    h, truncated = GetHash(b, method)
                    if truncated:
                        t.print(f"{t.trunc}  {name:7s} {h}")
                        g.show_color_message = True
                    else:
                        print(f"  {name:7s} {h}")
        else:
            for i in d["L"]:
                if d[i]:
                    method, name = d["method"][i]
                    h, truncated = GetHash(b, method)
                    if truncated:
                        t.print(f"{t.trunc}{h} {'<stdin>' if file == '-' else file}")
                        g.show_color_message = True
                    else:
                        print(f"{h} {'<stdin>' if file == '-' else file}")
    if g.show_color_message:
        print(f"A hash in {t.trunc}this color{t.n} means it was truncated")
