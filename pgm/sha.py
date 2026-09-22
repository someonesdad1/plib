'''
Print out the hashes for files on the command line
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Print out hashes of files oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞1 -t working, but need some careful tests on some prepared files to know that
              it's working correctly

        oo>
    '''
    if 1:  # Standard imports
        from pathlib import Path as P
        import getopt
        import hashlib
        import re
        import sys
        import zlib
    if 1:  # Custom imports
        from wrap import dedent
        import trm
        t = trm.TrmDP()
        import dpstr
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:    # Global variable container
            pass
        g = G()
        # Colors
        t.d = t.sky
        t.trunc = t.sky
        t.err = t.redl
        t.name = t.ornl
        t.hshname = t.purl
        # Hash method numbers to the method's constructor
        g.hash_methods = {
            0:  (hashlib.sha256, "SHA256"),
            1:  (hashlib.md5, "MD5"),
            2:  (hashlib.sha1, "SHA1"),
            3:  (hashlib.sha224, "SHA224"),
            4:  (hashlib.sha384, "SHA384"),
            5:  (hashlib.sha512, "SHA512"),
            6:  (zlib.crc32, "CRC32"),
            7:  (zlib.adler32, "ADLER32"),
        }
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
        
          A   Convert Unicode characters to rough ASCII equivalents{n}
          B   Remove characters under 0x20
          b   Remove characters under 0x20 except newline
          d   Remove characters that are ASCII digits (∈ string.digits)
          h   Remove characters that are hex digits (∈ string.hexdigits)
          l   Remove lower case letters (∈ string.ascii_lowercase)
          n   Remove punctuation (∈ string.punctuation)
          o   Remove characters that are octal digits (∈ string.octdigits)
          p   Remove non-printable characters (∉ string.printable)
          u   Remove upper case letters (∈ string.ascii_uppercase)
          W   Remove whitespace (∈ string.whitespace)
          w   Remove whitespace except newlines
          7   Remove characters above 0x7f (i.e., keep only 7-bit characters)
          8   Remove characters above 0xff (i.e., keep only 8-bit characters)
        
        The A conversion is idiosyncratic and doesn't convert all Unicode characters
        (mostly ones that look like Latin characters); it may even increase the size
        because strings like '∞' will be replaced by 'oo'.


        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Calculate the SHA-256 hash of the given files.  Use '-' for stdin.
        Options:                          Bytes in hash
            -a      Show hash for each of the different methods
            -H      Show manpage
            -l      Convert to lower case (only works with -t; outranks -u)
            -m n    Select other hash method
            -n n    Truncate hash to n bytes
            -s      Print hash name in color to stderr
            -t n    Process text files in special ways.  See -H manpage.
            -u      Convert to upper case (only works with -t)
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
        d["-l"] = False  # Convert to lowercase
        d["-m"] = 0      # Hash method to use
        d["-n"] = None   # Truncate hash to n bytes
        d["-s"] = False  # Print hash name in color to stderr
        d["-t"] = []     # Process text file specially
        d["-u"] = False  # Convert to uppercase
        try:
            opts, files = getopt.getopt(sys.argv[1:], "aHhlm:n:st:u")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in opts:
            if o[1] in "alsu":
                d[o] = not d[o]
            elif o == "-H":     # Show manpage
                Manpage()
            elif o == "-m":     # Select hash method
                d[o] = int(a)
                if d[o] not in g.hash_methods:
                    must = ', '.join(str(i) for i in g.hash_methods.keys())
                    Error(f"-m option must in {must}")
            elif o == "-n":     # Truncate hash to n bytes
                d[o] = int(a)
                if d[o] <= 0:
                    Error("-n option must be > 0")
            elif o == "-t":     # Process text file
                letters = "AaBbdhloPpWwu8"
                if a not in set(letters):
                    Error("{a!r} not in valid -t letters of {letters!r}")
                d[o].append(a)
        if not files or d["-h"]:
            Usage()
        return files
if 1:  # Core functionality
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
    def GetHash(b, hash_method):
        'Return the hexdigest; b are the bytes, hash_method is the hashlib method'
        try:
            hsh = hash_method()
            hsh.update(b)
            hexdigest = hsh.hexdigest()
        except TypeError:
            # CRC32 or ADLER32
            hsh = hash_method(b)
            hexdigest = f"{hsh:08x}"
        return hexdigest
    def ProcessText(b, file, keys):
        '''These bytes are converted to Unicode (assumed to be UTF-8 encoded), processed
        as indicated by the -t option (in keys), then converted back to bytes.
        '''
        s = b.decode()
        try:
            u = dpstr.RemoveCharClass(s, keys=keys)
        except Exception as e:
            Error(f"Special -t processing for {file!r} failed:\n  {e}")
        if d["-u"] and d["-t"]:
            u = u.upper()
        if d["-l"] and d["-t"]:
            u = u.lower()
        return u.encode()
    def ProcessFile(file):
        p = P(file)
        if p.is_dir():
            t.print(f"{t.err}{file!r} is a directory", file=sys.stderr)
            return
        # Get the relevant bytes in the file
        B = GetBytes(file)
        # Special processing if -t option used
        b = ProcessText(B, file, d["-t"])
        if d["-a"]:     # Show for all hash methods
            t.print(f"{t.name}{file}")
            # Get longest hash method name
            w = 0
            for i in g.hash_methods:
                w = max(w, len(g.hash_methods[i][1]))
            for i in g.hash_methods:
                hash_method, name = g.hash_methods[i]
                hexdigest = GetHash(b, hash_method)
                if d["-n"]:     # Truncate hash to n bytes
                    newdigest = hexdigest[:2*d['-n']]
                    if len(newdigest) != len(hexdigest):
                        t.print(f"   {t.hshname}{name:{w}s}{t.n} {t.trunc}{newdigest}")
                    else:
                        print(f"   {t.hshname}{name:{w}s}{t.n} {newdigest}")
                else:
                    print(f"   {t.hshname}{name:{w}s}{t.n} {hexdigest}")
            return
        else:
            hash_method, name = g.hash_methods[d["-m"]]
            hexdigest = GetHash(b, hash_method)
        if d["-n"]:     # Truncate hash to n bytes
            newdigest = hexdigest[:2*d["-n"]]
            if len(newdigest) != len(hexdigest):
                t.print(f"   {t.hshname}{name}{t.n} {t.trunc}{newdigest}")
            else:
                print(f"   {t.hshname}{name}{t.n} {newdigest}")
        else:
            print(hexdigest, file)

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine()
    for file in files:
        ProcessFile(file)
    if d["-n"]:     # Truncate hash to n bytes
        t.print(f"Hashes in this {t.trunc}color{t.n} are truncated to {d['-n']} bytes", file=sys.stderr)
    if d["-s"]:     # Print hash name in color to stderr
        _, name = g.hash_methods[d["-m"]]
        t.print(f"Hash used is {t.name}{name}", file=sys.stderr)

