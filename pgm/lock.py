'''
Encrypt/decrypt a file
    This is intended to be a practical tool for encrypting/unencrypting files.  It requires
    the PyPi 'cryptography' library that provides the Fernet object.  See
    https://cryptography.io/en/latest/fernet/#.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Encrypt/decrypt a file
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from getpass import getpass
        from pathlib import Path as P
        import base64
        import getopt
        import os
        import re
        import subprocess
        import sys
        import zlib
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        from lwtest import Assert
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
            I use this script as a utility encrypting/decrypting tool on my computers.  I use a
            shell function 'lock' to encrypt and another function 'unlock' to decrypt.

            My use cases are:
                - I want to shroud a file but make it easy to decrypt because I don't have to
                  remember a password for it
                - I want to encrypt a file with a strong password

            The first case can be gotten by using the -u option and I'm not prompted for a
            password.  Or, to get the same behavior without using -u, when prompted hit the Enter
            key twice without entering anything.

            If you use the -c option, the base64 output is compressed with python's zlib, so it
            will be roughly about the same size as the input file.

            Strong passwords with good encryption tools are how to get encrypted files others can't
            snoop.  For serious stuff, I use my password database program to both generate and
            store the password so I don't have to remember it.   

            The performance is fine for me on my 10 year-old slowly ossifying computer hardware.  A 
            10 MB file can be encrypted in about half a second.

            For a bit of added safety when encrypting a file, I have the in-memory version of the
            encrypted data decrypted and checked for equality with the input data.  This takes more
            time; if you don't want it you can switch it off by changing the line around 8 lines
            from the end of the file.
            
        '''.rstrip()))
        exit(0)
    def Usage(status=1):
        comp = "Do not use" if d["-c"] else "Use"
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] infile [outfile]
            Encrypt and decrypt files.  The default is to encrypt.  The output stream is base64
            (and it may be compressed).  outfile will be overwritten if it exists.  You'll be
            prompted for a password twice and your inputs must match before the program will
            proceed.
          Encryption
            If you use '-' for infile, stdin will be encrypted and put in outfile; if outfile
            is not present, then the information will be sent to stdout.
          Decryption
            If you use '-' for infile, stdin will be decrypted and put in outfile; if outfile
            is not present, then the information will be sent to stdout.
          Note
            If you run the program twice with the exact same inputs, you won't get the 
            same encrypted results, but the data will still decrypt to the same information.
        Options:
            -c      {comp} compression
            -d      Decrypt the file on the command line
            -h      Show more detailed help
            -v      Verbose operation (messages to stderr)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Use compression
        d["-d"] = False     # Decrypt the file
        d["-u"] = False     # Do not prompt for password
        d["-v"] = False     # Verbose output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdhuv") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cduv"):
                d[o] = not d[o]
            elif o == "-h":
                Manpage()
        if len(args) not in (1, 2):
            Usage()
        if d["-v"]:
            g.dbg = True
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def GetPassword():
        while True:
            pw1 = getpass().encode()
            pw2 = getpass().encode()
            if pw1 != pw2:
                print("Passwords differ; try again")
            else:
                return pw1
    def GetFernet(password):
        'Return the Fernet object for encrypting/decrypting'
        Assert(ii(password, bytes))
        salt = b'\xde\xc4\x9f\xb0\xc7\xa7j\x81\xca\x1a0}q\x1fB\x80'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)
    def GetData(*args):
        'Return inputdata (bytes), outstream'
        if len(args) == 1:
            if args[0] == "-":
                inputdata = sys.stdin.buffer.read()
                Dbg(f"Getting input from stdin")
            else:
                Dbg(f"Getting input from file {args[0]!r}")
                inputdata = open(args[0], "rb").read()
            outstream = sys.stdout.buffer
            Dbg("Sending output to stdout")
        else:   # Must be 2 arguments
            if args[0] == "-":
                inputdata = sys.stdin.buffer.read()
                Dbg(f"Got input from stdin")
            else:
                Dbg(f"Getting input from file {args[0]!r}")
                inputdata = open(args[0], "rb").read()
            outstream = open(args[1], "wb")
            Dbg(f"Sending output to {args[1]!r}")
        assert isinstance(inputdata, bytes)
        return inputdata, outstream

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    inputdata, outstream = GetData(*args)
    password = b'' if d["-u"] else GetPassword()
    fernet = GetFernet(password)
    if d["-d"]:     # Decrypt
        data = inputdata
        if d["-c"]:
            data = zlib.decompress(inputdata)
        output_data = fernet.decrypt(data)
    else:           # Encrypt
        output_data = fernet.encrypt(inputdata)
        if d["-c"]:
            output_data = zlib.compress(output_data)
    if 1:   # Validate when encrypting
        if not d["-d"]: 
            indata = output_data
            if d["-c"]:
                indata = zlib.decompress(output_data)
            indata = fernet.decrypt(indata)
            Assert(indata == inputdata)
    # Send data to output stream
    outstream.write(output_data)
