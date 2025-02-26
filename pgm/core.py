"""
List GNU core utilities
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # List GNU core utilities
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from color import t

        if 1:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Describe this option
        d["-d"] = 3  # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        return args


if 1:  # Core functionality

    def ListUtilities():
        print("             GNU core utilities")
        data = dedent("""
        Output of entire files
            cat: Concatenate and write files
            tac: Concatenate and write files in reverse
            nl: Number lines and write files
            od: Write files in octal or other formats
            base32: Transform data into printable data
            base64: Transform data into printable data
            basenc: Transform data into printable data
        Formatting file contents
            fmt: Reformat paragraph text
            pr: Paginate or columnate files for printing
            fold: Wrap input lines to fit in specified width
        Output of parts of files
            head: Output the first part of files
            tail: Output the last part of files
            split: Split a file into pieces.
            csplit: Split a file into context-determined pieces
        Summarizing files
            wc: Print newline, word, and byte counts
            sum: Print checksum and block counts
            cksum: Print and verify file checksums
            md5sum: Print or check MD5 digests
            b2sum: Print or check BLAKE2 digests
            shasum: Print or check various SHA digests
        Operating on sorted files
            sort: Sort text files
            shuf: Shuffling text
            uniq: Uniquify files
            comm: Compare two sorted files line by line
            ptx: Produce permuted indexes
            tsort: Topological sort
        Operating on fields
            cut: Print selected parts of lines
            paste: Merge lines of files
            join: Join lines on a common field
        Operating on characters
            tr: Translate, squeeze, and/or delete characters
            expand: Convert tabs to spaces
            unexpand: Convert spaces to tabs
        Directory listing
            ls: List directory contents
            dir: Briefly list directory contents
            vdir: Verbosely list directory contents
            dircolors: Color setup for ls
        Basic operations
            cp: Copy files and directories
            dd: Convert and copy a file
            install: Copy files and set attributes
            mv: Move (rename) files
            rm: Remove files or directories
            shred: Remove files more securely
        Special file types
            link: Make a hard link via the link syscall
            ln: Make links between files
            mkdir: Make directories
            mkfifo: Make FIFOs (named pipes)
            mknod: Make block or character special files
            readlink: Print value of a symlink or canonical file name
            rmdir: Remove empty directories
            unlink: Remove files via the unlink syscall
        Changing file attributes
            chown: Change file owner and group
            chgrp: Change group ownership
            chmod: Change access permissions
            touch: Change file timestamps
        File space usage
            df: Report file system space usage
            du: Estimate file space usage
            stat: Report file or file system status
            sync: Synchronize cached writes to persistent storage
            truncate: Shrink or extend the size of a file
        Printing text
            echo: Print a line of text
            printf: Format and print data
            yes: Print a string until interrupted
        Conditions
            false: Do nothing, unsuccessfully
            true: Do nothing, successfully
            test: Check file types and compare values
            expr: Evaluate expressions
        Redirection
            tee: Redirect output to multiple files or processes
        File name manipulation
            basename: Strip directory and suffix from a file name
            dirname: Strip last file name component
            pathchk: Check file name validity and portability
            mktemp: Create temporary file or directory
            realpath: Print the resolved file name.
        Working context
            pwd: Print working directory
            stty: Print or change terminal characteristics
            printenv: Print all or some environment variables
            tty: Print file name of terminal on standard input
        User information
            id: Print user identity
            logname: Print current login name
            whoami: Print effective user name
            groups: Print group names a user is in
            users: Print login names of users currently logged in
            who: Print who is currently logged in
        System context
            date: Print or set system date and time
            arch: Print machine hardware name
            nproc: Print the number of available processors
            uname: Print system information
            hostname: Print or set system name
            hostid: Print numeric host identifier
            uptime: Print system uptime and load
        SELinux context
            chcon: Change SELinux context of file
            runcon: Run a command in specified SELinux context
        Modified command invocation
            chroot: Run a command with a different root directory
            env: Run a command in a modified environment
        Environment variable expansion
            nice: Run a command with modified niceness
            nohup: Run a command immune to hangups
            stdbuf: Run a command with modified I/O stream buffering
            timeout: Run a command with a time limit
        Process control
            kill: Send a signal to processes
        Delaying
            sleep: Delay for a specified time
        Numeric operations
            factor: Print prime factors
            numfmt: Reformat numbers
            seq: Print numeric sequences
        """)
        w = 15
        for line in data.split("\n"):
            if line.startswith(" "):
                name, rem = line.strip().split(":", 1)
                print(f"{' ' * 4}{name:{w}s} {rem}")
            else:
                print(line)
        exit(0)


if __name__ == "__main__":
    d = {}  # Options dictionary
    # args = ParseCommandLine(d)
    ListUtilities()
