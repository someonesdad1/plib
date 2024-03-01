'''
TODO:
    - -I:
        - Include a histogram of token lengths
        - Print the top 10 tokens by frequency
    - -T:  same as -t, but include the token counts (same output as
      /pylib/pgm/tokenize1.py).

    - Consider wrapping the long lines so that it all fits into the
      number of COLUMNS present.

    - Consider changing output to one line per token if there's only one
      file.  For neatness, this would require the spacing for the tokens
      to match the longest token, which could be problematic.
    - Total match count on token's line in parentheses

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Token cross-referencing tool
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import keyword
        import re
        import string
        import sys
        from collections import deque, Counter
    if 1:   # Custom imports
        from wrap import wrap, dedent, indent, Wrap
        from columnize import Columnize
        from globalcontainer import Global, Variable, Constant
        from color import t
        if 0:
            import debug
            debug.SetDebugger()  # Start debugger on unhandled exception
    if 1:   # Global variables
        ii = isinstance
        nl = "\n"
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        G = Global()
        G.ro = Constant()
        G.ro.default_dict = '/words/words.default'
        t.warn = t("ornl")
if 1:   # Utility
    def eprint(*p, **kw):
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def PrintManpage():
        print(dedent(f'''
        NAME
            xref.py - produce a cross reference of tokens in a set of text files
        
        SYNOPSIS
            xref.py [options] [file1 [file2...]]
        
        DESCRIPTION
            Tokens are gotten by replacing non-alphanumeric characters by
            space characters, then parsing on whitespace.  The output is
            printed to stdout and is the token on its own line followed by the
            files and line numbers that contain that token.  The -t option
            causes only the tokens to be printed out, one per line.
            
            Tab and carriage return characters will be replaced by spaces, but
            other control characters won't.  To see them, you may need to save
            the output to a file and view it with your editor.
            
            The program is also capable of spell checking the text files.  You
            may compile in the location of a default dictionary to use.  A
            dictionary is a list of tokens separated by whitespace that give
            the correct spelling of the tokens.  Letter case is ignored.
            Any misspelled tokens are printed to stdout.

            Tokens that begin with a digit are ignored unless the -N option
            is given.
            
            During spell checking, the program will parse compound tokens such
            as 'MyFunction' and 'my_function' into the tokens 'my' and
            'function', then look them up in the dictionary.  This allows
            programmers to help ensure they're using descriptive names for
            symbols in their programs.  The algorithm for splitting a compound
            token is to replace underscores by space characters, then put a
            space character before each upper case letter.  Single letters as
            tokens are ignored.  Tokens that are misspelled are printed to
            stdout.  The program includes a built-in dictionary for keywords
            in C, C++, python, and shell programming.  Tokens that begin with
            '0' are ignored, as they are likely octal or hex constants.
            Tokens that are composed of all digits are also ignored.
            
            In the source code, you can define a default dictionary to use for
            spell checking (if the string is empty, no default dictionary is
            used).  It is not an error if this file is not present.
            
            Because of the algorithm used for splitting composite tokens,
            tokens with all uppercase letters will be ignored when spell
            checking.
            
            Non-7-bit characters seen in e.g. UTF-8 encoded files will be seen
            in tokens, so this program should work on encoded files in a
            suitable terminal.  If a different encoding is used, use a
            program like /usr/bin/iconv to conver to UTF-8.
        
        CROSS-REFERENCING OPTIONS
          -@
              Get file list from stdin, one file per line.
          
          -h
              Print this man page to stdout.
          
          -I
              Print informational statistics at end of report.
          
          -i
              Do not ignore the case of tokens.  Normally, all tokens will
              be printed in lower case.
          
          -t
              Print only the tokens found in sorted order, one token per line.
        
        SPELL CHECKING OPTIONS
          -c
              Do not use the built-in keywords for C/C++, python, and Bourne
              type shell scripts when spell checking.  You can replace the
              list in the source code with your own list of words.
          
          -C 
              Remove tokens resulting from common English contractions (e.g.,
              'didn', 'hasn', etc.).
          
          -d dict
              Specify a spelling dictionary in addition to the default
              dictionary.  Use this option to add correctly spelled tokens
              that are not in the default dictionary.  You can have more
              than one -d option.  This "dictionary" should be a plain text
              file with one token per line.
          
          -D dict
              Specify a spelling dictionary that replaces the default
              dictionary.  You can have more than one -D option, but the last
              one on the command line is used.  This "dictionary" should be a
              plain text file with one token per line.
          
          -f
              Fold case when sorting tokens.  This gives the tokens like
              you'd find them in a dictionary.
          
          -g
              Do not remove digits from tokens when spell checking.  Normally,
              a token such as MyFunction4 would have the 4 removed before
              spell checking.
          
          -k
              When spell checking, split composite words such as TwoWords or
              two_words into the simple words Two and Words.  This is intended
              to allow you to spell check source code.  Many programmers feel
              variable names should be spelled correctly and use words in the
              dictionary, rather than abbreviations.
          
          -n
              Only print the properly-spelled tokens.
          
          -s
              Perform a spell check on the tokens (uses the default
              dictionary).  Any tokens not found in the dictionary will be
              printed to stdout.
        
        EXAMPLES
          xref file1
              Print a list of tokens in file1 with filename and line numbers.
          
          xref -t file1
              Print a list of tokens only in file1.
          
          xref -w file1
              Same as previous, but list the tokens in columns.
          
          xref -s -d wordlist file1
              Spell check file1 using an explicitly specified "dictionary"
              (list of words, one word per line).
        
        HISTORY
            In the late 1990's while working at HP, I was loaned to a
            group that was writing LaserJet printer drivers.  I was in a
            crunch to learn the project's code and needed to find
            symbols a lot.  There were no handy tools on the Windows NT
            system, so I wrote a python script to index the many tens of
            thousands of project files, then constructing a tags file
            for my editor.  This was likely the 1.5.2 version of python
            and it would typically take over 2 hours to do the indexing;
            a significant contributor was the network latency besides
            the processing.  I was forced to rewrite this indexing tool
            in C++ and, if I remember correctly, it got the execution
            time down to 15 minutes or so.  Back then, a rule of thumb
            was that a C++ rewrite of a python script would get you
            about an order of magnitude improvement in performance.
        
            Sometime after around 2010, I wrote a python version of the
            C++ application.  Around 2018, I compared the C++ version to
            the python application to see how long both took to generate
            a token cross-reference to the 1200 or so python files in
            the directory where I keep my python files.  Surprisingly,
            the C++ version was only about 20% faster than the python
            script.  The lesson was that I only maintain and use the
            python version.  If I was still working in industry, I'd
            probably use the C++ version for the best speed.
        
            In the early 1990's I remember some email with a person in
            Europe.  He told me that the scripting languages needed to
            be watched, as they would keep getting better and better
            over time.  He was presciently right -- the performance
            gains in python (particularly non-early versions of python
            3) have been remarkable.  A number of years ago I played
            around with mawk and was surprised at how fast it was,
            faster than C code you'd write yourself.  
        
        NOTES
            Please send bug reports/improvements to someonesdad1@gmail.com.
        '''))
    def Usage(status=1, quiet=False):
        'Print usage statement and exit'
        name = sys.argv[0]
        s = dedent(f'''
        Usage:  {name} [options] [file1 [file2...]]
        A token cross-referencing and spell checking tool.  Use '-' as a file
        argument to tokenize stdin.
            -@          Get file list from stdin, one file per line
            -f          Ignore case when sorting tokens
            -h          Print man page to stdout
            -I          Print informational statistics
            -N          Don't ignore starting digit in tokens
            -t          Print tokens only
            -u          Warn if non-7-bit characters are in tokens
            -w          Like -t, but print in columns for more compact listing
        Spell checking (-s option):
            -c          Do not use built-in keywords for C/C++, python, shell 
            -C          Remove common English contractions
            -d dict     Specify a spelling dictionary in addition to default dict
            -D dict     Specify a spelling dictionary (replaces default dictionary)
            -g          Do not remove digits from tokens when spell checking
            -i          Do not ignore case of tokens for spelling
            -k          Split composite tokens when spell checking
            -n          Negate spell check:  only print properly-spelled tokens
            -s          Perform a spell check of the tokens 
            Default dictionary = '{G.ro.default_dict}'
            
            Tokens are split in a line on python whitespace characters.
        ''')
        if not quiet:
            print(s)
            exit(status)
        # Make a list of the options to find disconnects between Usage
        # and ParseCommandLine
        Usage.s = set([i for i in s.split() if i[0] == "-" and len(i) == 2])
    def ParseCommandLine(d):
        'Parse command line and return arguments'
        d["-@"] = False     # Get file list from stdin, one per line
        d["-C"] = False     # Remove common English contractions
        d["-c"] = False     # Use common programming keywords
        d["-D"] = "/pylib/pgm/words"      # Default spelling wordlist
        d["-d"] = []        # Auxiliary spelling wordlists
        d["-f"] = False     # Ignore case when sorting tokens
        d["-g"] = False     # Do not remove digits from tokens
        d["-h"] = False     # Print manpage
        d["-I"] = False     # Show informational stats
        d["-i"] = True      # Ignore case of tokens
        d["-k"] = False     # Split composite tokens
        d["-N"] = False     # Don't ignore tokens beginning with a digit
        d["-n"] = False     # Print correctly-spelled tokens
        d["-s"] = False     # Perform spell check
        d["-t"] = False     # List tokens only
        d["-u"] = False     # Warn on non-7-bit tokens
        d["-w"] = False     # Sames as -t but in columns
        d["tokens"] = {}
        d["wordlist"] = set()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "@Ccd:D:fghIikNnstuw")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "@CcfgIikNnstuw":
                d[o] = not d[o]
            elif o in ("-d",):
                d["-d"].append(P(a))
            elif o in ("-D",):
                d["-D"] = None if a == "None" else P(a)
            elif o in ("-h", "--help"):
                PrintManpage()
                exit(0)
        # Compare the options in d to those given in Usage to find
        # disconnects.
        Usage(quiet=True)   # Puts options in Usage.s
        opts = set([i for i in d if i[0] == "-" and len(i) == 2])
        if opts != Usage.s:
            eprint(dedent(f'''
            {t.warn}xref.py has a disconnect between the options in the dict opt
            and those listed in Usage():
              In ParseCommandLine, not in Usage:  {' '.join(opts - Usage.s)}
              In Usage, not in ParseCommandLine:  {' '.join(Usage.s - opts)}{t.n}
            '''))
            exit(2)
        if not args and not d["-@"]:
            Usage()
        return args
if 1:   # Core functionality
    def GetWords(s):
        ' Return a set of words in the multiline string s'
        return set(s.split())
    def Keywords():
        ' Return a set of programming keywords'
        # C/C++/shell
        t = '''
        abs acos acosh acosl alloc amode argc argv asctime asin asinh asinl
        atan atan2 atan2l atanh atanl atexit atof atoi atol bitset bool
        boolalpha brk bsearch calloc ceil ceill cerr cgets chdir chmod cin
        clearerr cmode conio const const_iterator cosh coshl cosl cout
        cprintf cputs creat cscanf cstdlib ctime ctype difftime dup dup2
        ecvt elif endif endl erf erfc errno esac exec execl execle execlp
        execlpe execv execve execvp execvpe exp expl extern fabs fabsl
        fclose fcloseall fcntl fcvt fdopen feof ferror fflush fgetc fgetchar
        fgetpos fgets fileno fi floorl flushall fmod fmodl fopen fprint
        fprintf fputc fputchar fputs fread freopen frexp frexpl fscanf fseek
        fsetpos fstat fstream ftell func fwrite gcvt getc getch getchar
        getche getcwd getenv getline getw gmtime gsignal ifdef ifndef
        ifstream inline int ios iostream isalnum isalpha isascii isatty
        iscntrl isdigit isgraph islower isprint ispunct isspace istring
        istrstream isupper isxdigit iterator itoa labs ldexp ldexpl ldiv
        lfind localtime log10 log10l logl longjmp lsearch lseek ltoa malloc
        matherr mblen mbstowcs mbtowc memccpy memchr memcmp memcpy memicmp
        memmove memset mkdir mktemp mktime modf modfl namespace noboolalpha
        nocreate noreplace oct ofstream ostream perror pow pow10 pow10l powl
        printf putc putchar putenv putw qsort readonly realloc resetiosflags
        rmdir sbrk scanf setbase setbuf setf setfill setiosflags setjmp
        setmode setprecision setvbuf setw showbase showpoint showpos signal
        sinh sinhl sinl sizeof skipws spawnl spawnle spawnlp spawnlpe spawnv
        spawnve spawnvp spawnvpe sprintf sqrt sqrtl srand sscanf stat std
        stderr stdin stdio stdlib stdout stime stpcpy str strcat strchr
        strcmp strcmpi strcoll strcpy strcspn strdup strerror strftime
        stricmp strlen strlwr strncat strncmp strncmpi strncpy strnicmp
        strnset strpbrk strrchr strrev strset strspn strstr strstream strtod
        strtok strtol strtoul struct strupr strxfrm substr swprintf tanh
        tanhl tanl tmpfile tmpnam toascii tolower toupper trunc typedef
        typename tzset ultoa undef ungetc ungetch unitbuf unset uppercase va
        vfprintf vfscanf vprintf vscanf vsprintf vsscanf wcstombs wctomb'''
        s = GetWords(t)
        # Python
        t = '''
        and ascii bytearray bytes callable chr classmethod cmath cmp
        copysign def delattr delitem delslice dict dir divmod eq eval
        excepthook frozenset gamma getattr getitem getslice getstate globals
        hasattr hex hypot id init isinstance issubclass iter len lgamma
        locals lshift max memoryview min mul ord or radd rcmp rdiv rdivmod
        repr rlshift rmod rmul rop ror rpow rrshift rshift rsub rxor setattr
        setitem setslice setstate staticmethod tuple ufloat UFloat umath
        uncertainties vars xor xrange zip'''
        # From 3.9's keyword.kwlist:
        t += '''
            False None True and as assert async await break class continue
            def del elif else except finally for from global if import in
            is lambda nonlocal not or pass raise return try while with
            yield
        '''
        s.update(GetWords(t))
        return s
    def GetContractions():
        ''' Return a set of contraction words
        '''
        s = '''I ain aren couldn daren daresn dasn didn er finna gimme giv
            gonna gotta hadn hasn howdy isn ll ma mayn mightn mustn ne needn
            ol oughtn shan shouldn st tis twas wasn wouldn'''
        return GetWords(s)
    def GetFiles():
        'Read in the files to process from stdin, one file per line'
        files = [i.strip() for i in sys.stdin.read().split("\n") if i.strip()]
        return [i for i in files if i[0] != "#"]    # Removed 'commented' files
    def NumReferences(token: str):
        'Return the number of line references this token has'
        n = 0
        t = d["tokens"][token]
        for i in t:
            n += len(t[i])
        return n
    def RemoveDigits(token: str) -> str:
        return token if d["-g"] else token.translate(RemoveDigits.translate_dict)
    RemoveDigits.translate_dict = {}
    for i in string.digits:
        RemoveDigits.translate_dict[ord(i)] = None
    def SplitCompositeToken(token: str) -> list:
        'Return a list of the split words in token'
        # Replace each '_' with a space, then insert a space before each 
        # capital letter.
        if token.upper() == token and "_" not in token:
            return [token]
        token_chars, new = deque(RemoveDigits(token)), deque()
        while token_chars:
            char = token_chars.popleft()
            if char in SplitCompositeToken.capitals:
                new.append(" ")
            elif char == "_":
                new.append(" ")
                continue
            new.append(char)
        s = ''.join(new)
        return s.lower().split() if d["-i"] else s.split()
    SplitCompositeToken.capitals = set(string.ascii_uppercase)
    def Non7BitCharacters():
        'Return a list of any non-7bit characters in the tokens'
        all_chars = set(''.join(set(d["tokens"])))
        chars = list(sorted([i for i in all_chars if ord(i) > 0x7e]))
        return chars
    def PrintReport():
        D = d["tokens"]
        # D is dict with key of token and value of dict with keys of
        # filenames on command line and set of line numbers in that file
        # where the token occurs.
        o = []
        sortkey = str.lower if d["-f"] else None
        for token in sorted(D.keys(), key=sortkey):
            if d["-t"]:     # Only print tokens
                print(token)
            elif d["-w"]:   # Only print tokens in columns
                o.append(token)
            else:
                print(token)
                # Print location(s) in file(s)
                F = D[token]
                for file in sorted(F):
                    linenums = ' '.join([str(i) for i in sorted(list(F[file]))])
                    n = len(F[file])
                    print(f"    {file}: [{n}] {linenums}")
        if d["-w"]:     # Print only tokens in columns
            for line in Columnize(o):
                print(line)
        if d["-u"]:     # Warn on non-7-bit characters in any token
            u = Non7BitCharacters()
            if u:
                eprint(f"{t.warn}Warning:  non-7-bit character(s) in tokens:{t.n}")
                eprint(f"{t.warn}  {' '.join(u)}{t.n}")
        if d["-I"]:     # Print information statistics
            PrintStatistics()
    def PrintStatistics():
        T = d["tokens"]
        numtokens = len(T)  # Total number of tokens
        tok_one_ref = 0     # Tokens with one reference
        max_refs, max_t = 0, ""
        for t in T:
            n = 0
            for f in T[t]:
                n += len(T[t][f])
            if n > max_refs:
                max_refs = n
                max_t = t
            if len(T[t]) == 1:
                k = list(T[t].keys())[0]
                if len(T[t][k]) == 1:
                    tok_one_ref += 1
        print(dedent(f'''
        Statistics:
            Tokens with one reference    = {tok_one_ref}
            Maximum number of references = {max_refs} (token = '{max_t}')
            Total number of tokens       = {numtokens}
        '''))
        PrintHistogram()
    def PrintHistogram():
        T = set(d["tokens"])
        lengths = [len(i) for i in T]
        hist = dict(Counter(lengths))
        print(dedent('''
        Token lengths by count of number of tokens:
          Length           Count
          ------           -----'''))
        for i in range(1, max(hist) + 1):
            count = hist.get(i, 0)
            c = f"{count:>17d}" if count else ""
            print(f"{i:>7d}{c}")
        n = 10
        print("Longest tokens:")
        s = deque(sorted([(len(i), i) for i in T]), maxlen=n)
        o, w = [], Wrap()
        w.i = " "*4
        for i in reversed(s):
            o.append(i[1])
        print(w(' '.join(o)))
        print("Shortest tokens:")
        s = deque(sorted([(len(i), i) for i in T], reverse=True), maxlen=n)
        o.clear()
        for i in s:
            o.append(i[1])
        print(w(' '.join(o)))
    def GetWordlists():
        if not d["-c"]:
            d["wordlist"].update(Keywords())
        if d["-C"]:
            d["wordlist"].update(GetContractions())
        for f in d["-d"]:
            s = open(f).read()
            d["wordlist"].update(GetWords(s))
        if d["-D"] is not None:
            s = open(d["-D"]).read()
            d["wordlist"].update(GetWords(s))
        if d["-i"]:
            # Change all words to lowercase
            d["wordlist"] = set(i.lower() for i in d["wordlist"])
    def SpellCheck():
        'Print misspelled words'
        GetWordlists()
        # T is the set of tokens found in the input
        # W is the set of allowed words
        T, W = sorted(d["tokens"].keys()), d["wordlist"]
        for t in T:
            misspelled = False
            if d["-k"]:     # Split composite tokens first
                for w in SplitCompositeToken(t):
                    if w not in W:
                        misspelled = True
                        break
            else:
                tk = RemoveDigits(t.lower() if d["-i"] else t)
                misspelled = tk not in W
            if d["-n"]:
                if not misspelled:
                    print(t)
            elif misspelled:
                print(t)
    def ProcessFile(file: str) -> None:
        "Read in this file's tokens and put them into d['tokens']"
        if file == "-":
            stream, name = sys.stdin, "stdin"
        else:
            stream, name = open(file), file
        Xref(stream, name, preserve_case=d["-i"], mydict=d["tokens"])
    def Xref(stream, filename, preserve_case=True, mydict={}):
        ''' Build a dictionary of the tokens from stream, which will be read
        a line at a time.  mydict = dict(token: fdict) where fdict is
        dict(filename: set of line numbers where token was found).
        Stream is named by filename and will usually be the stream from
        open(filename), but it might be something else like the stdin stream
        which was labeled "stdin".
    
        The punctuation and control characters in the line are replaced
        with space characters, then each line is split on whitespace.  The
        tokens are inserted into the dictionary, which is returned.
        Multiple calls with a dictionary allow cross-referencing tokens in
        multiple files.
        '''
        if not hasattr(Xref, "punct"):
            # Construct a regexp that can be used to replace punctuation
            # with space characters for subsequent tokenizing.  '_' is
            # removed, as it is a valid token identifier character.
            punct = string.punctuation.replace("_", "")
            p = [re.escape(i) for i in punct]
            Xref.punct = re.compile('|'.join(p))
        def ProcessLine(line, linenum):
            line = line.rstrip("\n\r").replace("\t", " ")
            line = Xref.punct.sub(" ", line)        # Replace punct w/ space
            line = line if not preserve_case else line.lower() 
            # xx Why not use str.split(); it should do the same thing.
            words = re.split("  *", line)
            for word in words:
                if not word:
                    continue
                # Ignore any token that begins with a number
                if not d["-N"] and word[0] in string.digits:
                    continue
                if word not in mydict:
                    mydict[word] = {filename: set()}
                if filename not in mydict[word]:
                    mydict[word][filename] = set()
                if linenum not in mydict[word][filename]:
                    mydict[word][filename].add(linenum)
        # Read the lines from the stream
        linenum = 0
        line = stream.readline()
        while line:
            linenum += 1   # Line numbering is 1-based
            ProcessLine(line, linenum)
            line = stream.readline()
        return mydict 

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-@"]:
        args += GetFiles()
    for file in args:
        ProcessFile(file)
    if d["-s"]:
        SpellCheck()
    else:
        PrintReport()
