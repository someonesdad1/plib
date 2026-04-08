'''
List GNU core utilities
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # List GNU core utilities
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        import trm
        t = trm.TrmDP()
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
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
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          List core GNU utilities.
        '''))
        exit(status)
    def ParseCommandLine(d):
        #d["-a"] = False  # Describe this option
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        return args
if 1:  # Core functionality
    def ListUtilities_():
        'Original list, which was unattributed or dated'
        print("             GNU core utilities")
        data = dedent('''
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
        Source:  output of 'info coreutils'
        ''')
        w = 15
        for line in data.split("\n"):
            if line.startswith(" "):
                name, rem = line.strip().split(":", 1)
                print(f"{' ' * 4}{name:{w}s} {rem}")
            else:
                print(line)
        exit(0)
    def ListUtilities():
        '''This was written 31 Jan 2026 to directly utilize the output of the 'info
        coreutils' command.
        '''
        raw_data = dedent('''
            Output of entire files

            * cat invocation::               Concatenate and write files
            * tac invocation::               Concatenate and write files in reverse
            * nl invocation::                Number lines and write files
            * od invocation::                Write files in octal or other formats
            * base32 invocation::            Transform data into printable data
            * base64 invocation::            Transform data into printable data
            * basenc invocation::            Transform data into printable data

            Formatting file contents

            * fmt invocation::               Reformat paragraph text
            * pr invocation::                Paginate or columnate files for printing
            * fold invocation::              Wrap input lines to fit in specified width

            Output of parts of files

            * head invocation::              Output the first part of files
            * tail invocation::              Output the last part of files
            * split invocation::             Split a file into fixed-size pieces
            * csplit invocation::            Split a file into context-determined pieces

            Summarizing files

            * wc invocation::                Print newline, word, and byte counts
            * sum invocation::               Print checksum and block counts
            * cksum invocation::             Print CRC checksum and byte counts
            * b2sum invocation::             Print or check BLAKE2 digests
            * md5sum invocation::            Print or check MD5 digests
            * sha1sum invocation::           Print or check SHA-1 digests
            * sha2 utilities::               Print or check SHA-2 digests

            Operating on sorted files

            * sort invocation::              Sort text files
            * shuf invocation::              Shuffle text files
            * uniq invocation::              Uniquify files
            * comm invocation::              Compare two sorted files line by line
            * ptx invocation::               Produce a permuted index of file contents
            * tsort invocation::             Topological sort

            'ptx': Produce permuted indexes

            * General options in ptx::       Options which affect general program behavior
            * Charset selection in ptx::     Underlying character set considerations
            * Input processing in ptx::      Input fields, contexts, and keyword selection
            * Output formatting in ptx::     Types of output format, and sizing the fields
            * Compatibility in ptx::         The GNU extensions to 'ptx'

            Operating on fields

            * cut invocation::               Print selected parts of lines
            * paste invocation::             Merge lines of files
            * join invocation::              Join lines on a common field

            Operating on characters

            * tr invocation::                Translate, squeeze, and/or delete characters
            * expand invocation::            Convert tabs to spaces
            * unexpand invocation::          Convert spaces to tabs

            'tr': Translate, squeeze, and/or delete characters

            * Character sets::               Specifying sets of characters
            * Translating::                  Changing one set of characters to another
            * Squeezing and deleting::       Removing characters

            Directory listing

            * ls invocation::                List directory contents
            * dir invocation::               Briefly list directory contents
            * vdir invocation::              Verbosely list directory contents
            * dircolors invocation::         Color setup for 'ls'

            'ls':  List directory contents

            * Which files are listed::       Which files are listed
            * What information is listed::   What information is listed
            * Sorting the output::           Sorting the output
            * General output formatting::    General output formatting
            * Formatting the file names::    Formatting the file names

            Basic operations

            * cp invocation::                Copy files and directories
            * dd invocation::                Convert and copy a file
            * install invocation::           Copy files and set attributes
            * mv invocation::                Move (rename) files
            * rm invocation::                Remove files or directories
            * shred invocation::             Remove files more securely

            Special file types

            * link invocation::              Make a hard link via the link syscall
            * ln invocation::                Make links between files
            * mkdir invocation::             Make directories
            * mkfifo invocation::            Make FIFOs (named pipes)
            * mknod invocation::             Make block or character special files
            * readlink invocation::          Print value of a symlink or canonical file name
            * rmdir invocation::             Remove empty directories
            * unlink invocation::            Remove files via unlink syscall

            Changing file attributes

            * chown invocation::             Change file owner and group
            * chgrp invocation::             Change group ownership
            * chmod invocation::             Change access permissions
            * touch invocation::             Change file timestamps

            Disk usage

            * df invocation::                Report file system disk space usage
            * du invocation::                Estimate file space usage
            * stat invocation::              Report file or file system status
            * sync invocation::              Synchronize cached writes to persistent storage
            * truncate invocation::          Shrink or extend the size of a file

            Printing text

            * echo invocation::              Print a line of text
            * printf invocation::            Format and print data
            * yes invocation::               Print a string until interrupted

            Conditions

            * false invocation::             Do nothing, unsuccessfully
            * true invocation::              Do nothing, successfully
            * test invocation::              Check file types and compare values
            * expr invocation::              Evaluate expressions

            'test': Check file types and compare values

            * File type tests::              File type tests
            * Access permission tests::      Access permission tests
            * File characteristic tests::    File characteristic tests
            * String tests::                 String tests
            * Numeric tests::                Numeric tests

            'expr': Evaluate expression

            * String expressions::           + : match substr index length
            * Numeric expressions::          + - * / %
            * Relations for expr::           | & < <= = == != >= >
            * Examples of expr::             Examples of using 'expr'

            Redirection

            * tee invocation::               Redirect output to multiple files or processes

            File name manipulation

            * basename invocation::          Strip directory and suffix from a file name
            * dirname invocation::           Strip last file name component
            * pathchk invocation::           Check file name validity and portability
            * mktemp invocation::            Create temporary file or directory
            * realpath invocation::          Print resolved file names

            Working context

            * pwd invocation::               Print working directory
            * stty invocation::              Print or change terminal characteristics
            * printenv invocation::          Print all or some environment variables
            * tty invocation::               Print file name of terminal on standard input

            'stty': Print or change terminal characteristics

            * Control::                      Control settings
            * Input::                        Input settings
            * Output::                       Output settings
            * Local::                        Local settings
            * Combination::                  Combination settings
            * Characters::                   Special characters
            * Special::                      Special settings

            User information

            * id invocation::                Print user identity
            * logname invocation::           Print current login name
            * whoami invocation::            Print effective user ID
            * groups invocation::            Print group names a user is in
            * users invocation::             Print login names of users currently logged in
            * who invocation::               Print who is currently logged in

            System context

            * arch invocation::              Print machine hardware name
            * date invocation::              Print or set system date and time
            * nproc invocation::             Print the number of processors
            * uname invocation::             Print system information
            * hostname invocation::          Print or set system name
            * hostid invocation::            Print numeric host identifier
            * uptime invocation::            Print system uptime and load

            'date': Print or set system date and time

            * Time conversion specifiers::   %[HIklMNpPrRsSTXzZ]
            * Date conversion specifiers::   %[aAbBcCdDeFgGhjmuUVwWxyY]
            * Literal conversion specifiers:: %[%nt]
            * Padding and other flags::      Pad with zeros, spaces, etc.
            * Setting the time::             Changing the system clock
            * Options for date::             Instead of the current time
            * Date input formats::           Specifying date strings
            * Examples of date::             Examples

            SELinux context

            * chcon invocation::             Change SELinux context of file
            * runcon invocation::            Run a command in specified SELinux context

            Modified command invocation

            * chroot invocation::            Run a command with a different root directory
            * env invocation::               Run a command in a modified environment
            * nice invocation::              Run a command with modified niceness
            * nohup invocation::             Run a command immune to hangups
            * stdbuf invocation::            Run a command with modified I/O buffering
            * timeout invocation::           Run a command with a time limit

            Process control

            * kill invocation::              Sending a signal to processes.

            Delaying

            * sleep invocation::             Delay for a specified time

            Numeric operations

            * factor invocation::            Print prime factors
            * numfmt invocation::            Reformat numbers
            * seq invocation::               Print numeric sequences

            From 'info coreutils' 31 Jan 2026 on WSL system
        ''')
        lines = [i.strip() for i in raw_data.split("\n") if i.strip()]
        if 1:   # Get rid of sections with command details
            keep = []
            while lines:
                line = lines.pop(0)
                if line[0] == "'":
                    line = lines.pop(0)
                    while line[0] == "*":
                        line = lines.pop(0)
                    # Now on next heading, so put it back in the list
                    lines.insert(0, line)
                else:
                    keep.append(line)
            lines = keep
        if 1:   # Now process remaining lines
            while lines:
                line = lines.pop(0)
                if line[0] != "*":
                    if line.startswith("From 'info coreutils'"):
                        t.print(f"{t.ornl}{line}")
                    else:
                        t.print(f"{t.sky}{line}")
                else:
                    line = line.replace("*", " ", 1)
                    s = "invocation::"
                    line = line.replace(s, " "*len(s), 1)
                    s = "::"
                    line = line.replace(s, " "*len(s), 1)
                    print(line)

if __name__ == "__main__":
    d = {}  # Options dictionary
    # args = ParseCommandLine(d)
    ListUtilities()
