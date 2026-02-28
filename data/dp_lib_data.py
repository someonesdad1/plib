'''
Data file to hold code snippets
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import pathlib
    if 1:   # Custom imports
        import wrap
    if 1:   # Import symbols
        namedtuple = collections.namedtuple
        deque = collections.deque
        dedent = wrap.dedent
    if 1:   # Global variables
        Entry = namedtuple("Entry", "name cat lang gist code")

def GetData():
    'Returns a tuple of namedtuples of code snippets'
    # Note we return a copy of the list so that this function always returns the same
    # set of data.
    data = (
        Entry(name="bits", cat="utility", lang="python", 
            gist="Bit utility functions",
            code=dedent("""
                def get_bit(value, n):
                    return ((value >> n & 1) != 0)
                
                def set_bit(value, n):
                    return value | (1 << n)
                
                def clear_bit(value, n):
                    return value & ~(1 << n)
        """)),
        Entry(name="plot autocorrelation", cat="math", lang="python", 
            gist="Plot the autocorrelation of a sequence",
            code=dedent("""
                def PlotAutocorrelation(x, maxlag=10, color="b", plot_title=""):
                    '''Plot the autocorrelation of the sequence x.  This should give
                    similar results to the following matplotlib code:
                        acorr(x, maxlags=maxlag)
                        xlim(0, maxlag)
                    '''
                    def acf(x):
                        # Calculate autocorrelation function.  Note the different
                        # sample sizes depending on the lag.
                        results = []
                        for lag in range(1, maxlag + 1):
                            results.append(corrcoef(x[lag:], x[:-lag])[1, 0])
                        return concatenate((array([1]), array(results)))
                    if len(x) <= maxlag:
                        raise ValueError("Array must have more elements than maximum lag")
                    A, lw = acf(x), 3
                    plot(A, "bo")   # Plot the points
                    for x, r in zip(range(len(A)), A): # Draw a line to each point
                        y = 0.5 + r/2
                        if r < 0:
                            axvline(x, ymin=y, ymax=0.5, linewidth=lw, color=color)
                        else:
                            axvline(x, ymin=0.5, ymax=y, linewidth=lw, color=color)
                    axhline(y=0, linewidth=1, color="k")   # y = 0 line
                    xlabel("Lag")
                    ylabel("Autocorrelation")
                    xlim(0, 10)
                    ylim(-1, 1)
                    title(plot_title)
                    grid()
        """)),
        Entry(name="", cat="template", lang="python", 
            gist="Header for g library use",
            code=dedent("""
                # from g import *
                def SetUp(file, orientation=portrait, units=inches, wrap_in_PJL=False):
                    '''Convenience function to set up the drawing environment and return a
                    file object to the output stream.
                    '''
                    ofp = open(file, "w")
                    ginitialize(ofp, wrap_in_PJL)
                    setOrientation(orientation, units)
                    return ofp
        """)),
        Entry(name="", cat="", lang="sh", 
            gist="Shell script template",
            code=dedent("""
                #!/bin/bash
                #
                #
                #
                #----------------------------------------------------------------------
                
                main()
                {
                    Initialize "$@"
                }
                
                Initialize()
                {
                    :
                }
                
                CleanUp()
                {
                    :
                }
                
                Error()
                {
                    echo "$*" >&2
                    exit 1
                }
                
                #---------------------
                pgmname=$(basename $0)
                trap CleanUp EXIT
                main "$@"
        """)),
        Entry(name="", cat="math", lang="C", 
            gist="Simple & fast random number generator",
            code=dedent("""
                /* Simple, fast random number generator.  No function call necessary.
                Make sure X is global.  Numerical Recipes in C, ch 7, pg 284.  Include
                <limits.h> and divide X by ULONG_MAX*1.0 to get a double on [0, 1).
                
                To use:  define X as an appropriate unsigned long.  Then you can 
                pretend simp_rand is a kind of function call by assigning it to
                _another_ variable Y such as
                    
                    Y = simp_rand;
                */
                
                unsigned long X;  // Make sure this is global
                
                #define simp_rand     (X = 1664525L*X + 1013904223L)
        """)),
        Entry(name="", cat="utility", lang="sh", 
            gist="Show disk space used (du wrapper)",
            code=dedent("""
                #!/bin/sh
                
                # Script to show amount of disk space used.  Converted to Bourne shell
                # on 6 Jun 2014 from my old 1991 ksh script.
                
                Usage()
                {
                    echo "Usage:  $(basename $0) [opt] dir1 [dir2...]"
                    echo "  Shows disk space by directory"
                    echo "  Options are:"
                    echo "  -r    Recursive"
                    echo "  -l n  Only descend n levels (implies -r)"
                    exit 1
                }
                
                [ $# -eq 0 ] && Usage
                
                recursive=no
                levels=0
                
                for o in $* ; do 
                    case $o in
                        -h) Usage;;
                        -r) recursive=yes
                            shift ;;
                        -l) shift
                            recursive=yes
                            levels=${1:?-l option needs number of levels}
                            shift;;
                        --) shift
                            break;;
                    esac
                done
                
                opt="-k"
                
                if [ $recursive = "no" ] ; then
                    opt="$opt -s"  # du option -s means summarize total only
                fi
                
                if [ $levels -ne 0 ] ; then
                    opt="$opt -d $levels"   # du option -d to limit levels traversed
                fi
                
                du $opt $* | awk '
                    BEGIN{
                        total = 0
                    }
                    {
                        MB = $1/1000.
                        printf("%8.2f M %s\n", MB, $2)
                        total += MB
                    }
                    END {
                        fmt = "Total = %.3f M\n"
                        if (total > 100)
                            fmt = "Total = %d M\n"
                        else if (total > 10)
                            fmt = "Total = %.1f M\n"
                        else if (total > 1)
                            fmt = "Total = %.2f M\n"
                        printf(fmt, total)
                    }'
        """)),
        Entry(name="", cat="utility", lang="sh", 
            gist="Create a RAM disk on Linux",
            code=dedent("""
                #!/bin/bash
                
                # Script to create a RAM disk.  Downloaded from
                # http://tldp.org/LDP/abs/html/zeros.html.  Must be run as root.
                #
                # A RAM disk is a chunk of memory that is allocated and a filesystem
                # is created on it.  It gives very fast read/write access, but it is
                # volatile.  It can be used e.g. to keep a large dataset and data
                # lookups will be much faster.
                #
                #----------------------------------------------------------------------
                
                xxxxxx!  Has not been tested yet...
                
                main()
                {
                    Initialize "$@"
                    [ "$(id -nu)" != "root" ] && Error "Must be root to run $0"
                    # Make mount point
                    [ ! -d "$mountpoint" ] && mkdir $mountpoint 
                    # Zero out the bytes
                    dd if=/dev/zero of=$device count=$size bs=$blocksize 
                    # Create an ext2 file system on it
                    mke2fs $device
                    # Mount it
                    mount $device $mountpoint
                    # Let anyone read and write it
                    chmod 777 $mountpoint
                    # Success message
                    MB=$(echo $size $blocksize | awk '{printf("%.1f MB", $1*$2/1e6)}')
                    echo "\"$mountpoint\" now available for use ($MB MB)"
                    exit 0
                }
                
                Initialize()
                {
                    mountpoint=/mnt/ramdisk 
                    size=2000                      # How many blocks to create
                    blocksize=1024                 # Size of block in bytes
                    device=/dev/ram_user0
                    readonly mountpoint size blocksize device
                }
                
                Error()
                {
                    echo "$*" >&2
                    exit 1
                }
                
                #---------------------
                pgmname=$(basename $0)
                main "$@"
        """)),
        Entry(name="", cat="utility", lang="sh", 
            gist="Use getopt to get bash command-line options",
            code=dedent("""
                #!/bin/bash
                
                # An example of using the getopt(1).  This program will only work with
                # bash(1)
                
                # Example input and output (from the bash prompt):
                # ./parse.bash -a par1 'another arg' --c-long 'wow!*\?' -cmore -b " very long "
                # Option a
                # Option c, no argument
                # Option c, argument `more'
                # Option b, argument ` very long '
                # Remaining arguments:
                # --> `par1'
                # --> `another arg'
                # --> `wow!*\?'
                
                # Note that we use `"$@"' to let each command-line parameter expand to a 
                # separate word. The quotes around `$@' are essential!
                # We need TEMP as the `eval set --' would nuke the return value of getopt.
                TEMP=`getopt -o ab:c:: --long a-long,b-long:,c-long:: \
                    -n 'example.bash' -- "$@"`
                
                if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
                
                # Quotes around $TEMP are essential.
                eval set -- "$TEMP"
                
                while true ; do
                    case "$1" in
                        -a|--a-long) echo "Option a" ; shift ;;
                        -b|--b-long) echo "Option b, argument \`$2'" ; shift 2 ;;
                        -c|--c-long) 
                            # c has an optional argument. As we are in quoted mode,
                            # an empty parameter will be generated if its optional
                            # argument is not found.
                            case "$2" in
                                "") echo "Option c, no argument"; shift 2 ;;
                                *)  echo "Option c, argument \`$2'" ; shift 2 ;;
                            esac ;;
                        --) shift ; break ;;
                        *) echo "Internal error!" ; exit 1 ;;
                    esac
                done
                echo "Remaining arguments:"
                for arg do echo '--> '"\`$arg'" ; done
        """)),
        Entry(name="Compose", cat="utility", lang="python", 
            gist="Composition of a set of unary functions",
            code=dedent("""
                def compose(*funcs):
                    '''Composition of a set of unary functions.  Returns the identity function
                    for no arguments.  Handling functions that take multiple arguments is more
                    involved.
                    '''
                    idn = lambda x: x
                    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs, idn)
        """)),
        Entry(name="Group", cat="utility", lang="python", 
            gist="Class to group some related values (also see ndict)",
            code=dedent("""
                class Group:
                    '''Simple grouping of variable values.  Create different types by subclassing:
                    class Point(Group): pass
                    '''
                    # from http://code.activestate.com/recipes/52308 by Alex Martelli
                    def __init__(self, **kw):
                            self.__dict__.update(kw)
                    def __str__(self):
                        items = sorted(self.__dict__.items())
                        state = ["%s=%r" % (k, v) for k, v in items]
                        return "%s[%s]" % (self.__class__.__name__, ', '.join(state))
                x, y, threshold = 2.1, 14.3, 30
                point = Group(datum=y, squared=y*y, coord=x, name="my data")
                # Read/write the named attributes, add others, del them, etc.
                if point.squared > threshold:
                    point.isok = 1
                print(point)
                del point.coord
                print("coord deleted")
                print(point)
        """)),
        Entry(name="ndict", cat="utility", lang="python", 
            gist="Nested dictionary object",
            code=dedent("""
                class ndict(dict):
                    '''Nested dictionary object.  Syntactic sugar to support the following:
                        d = ndict()
                        d.point.x = 3
                        d.point.y = 4
                        d.distance = (d.point.x**2 + d.point.y**2)*(1/2)
                        d.other_point.x = 14
                        if "other_point.x" in d:
                            print("Has other_point.x")
                        del d.other_point.x
                    Do not use hasattr() to test whether these ndicts have an
                    attribute because hasattr() calls __getattr__() to do the
                    checking; this will add the attribute to the ndict.
                    
                    See http://code.activestate.com/recipes/578644 by Ariel Keselman
                    on 18 Aug 2013 (apparently licensed under the MIT license).
                    Adapted from a comment made by Nezar Abdennur on the above web
                    page.  Downloaded Tue 12 Aug 2014 09:04:26 AM
                    '''
                    def __str__(self):
                        return "ndict%s" % super(ndict, self).__str__()
                    def __delattr__(self, name):
                        del self[name]
                    def __getattr__(self, name):
                        return super(ndict, self).__getitem__(name)
                    def __setattr__(self, name, value):
                        super(ndict, self).__setitem__(name, value)
                    def __missing__(self, name):
                        super(ndict, self).__setitem__(name, ndict())
                        return super(ndict, self).__getitem__(name)
                    def __contains__(self, name):
                        su = super(ndict, self)
                        if '.' in name:
                            first, remaining = name.split(".", 1)
                            if first and su.__contains__(first):
                                su = super(ndict, self[first])
                                return su.__contains__(remaining)
                            else:
                                return False
                        else:
                            return su.__contains__(name)
        """)),
        Entry(name="wordid", cat="text", lang="python", 
            gist="Return an ID string that is (somewhat) pronounceable",
            code=dedent("""
                def WordID(half_length=3, unique=None, num_tries=100):
                    '''Return an ID string that is (somewhat) pronounceable.  The
                    returned number of characters will be twice the half_length.  If
                    unique is not None, it must be a container that can be used to
                    determine if the ID is unique.  You are responsible for adding the
                    returned word to the container.
                    '''
                    # Derived from http://code.activestate.com/recipes/576858
                    # downloaded Tue 12 Aug 2014 12:38:54 PM.  Original recipe by
                    # Robin Parmar on 8 Aug 2007 under PSF license.
                    from random import choice
                    v, c, r, count = 'aeiou', 'bdfghklmnprstvw', range(half_length), 0
                    while count < num_tries:
                        word = ''.join([choice(c) + choice(v) for i in r])
                        if not unique or (unique and word not in unique):
                            return word
                        count += 1
                    raise RuntimeError("Couldn't generate unique word")
        """)),
        Entry(name="", cat="utility", lang="python", 
            gist="Python coding policies",
            code=dedent("""
            
                - ∞∞1 I've deleted the original text of this item, as it seriously needs updating.
                https://realpython.com/ref/best-practices/ could be a decent place to start.
                - Goal:  make this a statement of what I consider are best practices and
                something short enough to review while finalizing a new script or module.
                
        """)),
        Entry(name="", cat="obsolete", lang="python", 
            gist="Python 2 equivalent to python 3's print()",
            code=dedent("""
                import sys
                
                class Out(object):
                    def __init__(self):
                        self.stream = sys.stdout
                        self.flush  = False
                        self.end = "\n"
                        self.sep = " "
                    def __call__(self, *v, **kw):
                        '''Sends the string representation of each element of v to the
                        stream.  Same keywords as print() in python 3, but they only
                        have an effect during the function call.  Change the
                        attributes if you want a permanent change.
                        '''
                        end    = kw.setdefault("end",    self.end)
                        sep    = kw.setdefault("sep",    self.sep)
                        stream = kw.setdefault("file",   self.stream)
                        flush  = kw.setdefault("flush",  self.flush)
                        if v and stream: # Print each parameter
                            stream.write(str(sep).join([str(i) for i in v]))
                        if end and stream:
                            stream.write(end)
                        if self.flush:
                            self.stream.flush()
                            self.flush = False
                            
                # out is a convenience instance of the Out object
                out = Out()
        """)),
        Entry(name="", cat="prog", lang="python", 
            gist="Sample profiling session",
            code=dedent("""
                import cProfile, pstats, io
                pr = cProfile.Profile()
                pr.enable()
                
                # Here's the code being profiled
                def func2(a):
                    return a//2
                def func1(a):
                    a = a + a + a + a + a + a + a + a + a + a + a + a + a + a + a 
                    a = func2(a)
                    return a + a + a + a + a + a + a + a + a + a + a + a + a + a + a
                def func(a):
                    t = 0
                    for i in range(10**5):
                        t += func1(i)
                func(1)
                # Done
                
                pr.disable()
                s = io.StringIO()
                sortby = 'cumulative'
                ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                ps.print_stats()
                print(s.getvalue())
        """)),
        Entry(name="", cat="", lang="python", 
            gist="Redirecting stdout",
            code=dedent("""
                import sys
                from io import StringIO
                if 1:   # Use your own class
                    class RedirectStdout:
                        def __init__(self, stream):
                            self.original_stream = sys.stdout
                            self.stream = stream
                        def __enter__(self):
                            sys.stdout = self.stream
                        def __exit__(self, type, value, tb):
                            sys.stdout = self.original_stream
                    out = StringIO()
                    with RedirectStdout(out):
                        print('Test')
                    print(f"StringIO contains '{out.getvalue()}'")
                else:   # Use contextlib
                    import contextlib
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        help(pow)
                    s = f.getvalue()
                    # To send the output of help() to a file:
                    with open('help.txt', 'w') as f:
                        with redirect_stdout(f):
                            help(pow)
                    # How to capture both stdout and stderr:
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        with contextlib.redirect_stderr(f):
                            help(pow)
                            print("Ouch!", file=sys.stderr)
                    s = f.getvalue()
                    print(s)
        """)),
        Entry(name="", cat="web", lang="HTML", 
            gist="HTML template",
            code=dedent("""
                <!doctype html>
                    <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <title>The Title</title>
                        <meta name="description" content="The Title">
                        <meta name="author" content="John Doe">
                        <link rel="stylesheet" href="css/styles.css?v=1.0">
                    </head>
                    <body>
                        <a href="http://www.wikipedia.com">link</a>
                    </body>
                </html>
        """)),
        Entry(name="", cat="utility", lang="python", 
            gist="Run a command & capture output",
            code=dedent("""
                # Running a command and capturing its output
                import sys
                import subprocess
                cmd = ["", "", ...]
                s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                lines = [i.decode("utf8") for i in s.stdout.readlines()]
        """)),
        Entry(name="", cat="", lang="python", 
            gist="Alternative function for assert",
            code=dedent("""
                from time import time, strftime
                check_off = False
                class CheckFailed(Exception):
                    pass
                def Check(condition, message="", log_stream=None, incl_time=False):
                    '''If condition is not true, raise an exception.
                    
                    message     Initialize the exception with this message
                    
                    log_stream  Instead of raising an exception if the condition is false,
                                just log the message to the stream.
                    
                    incl_time   If true, time stamp the message.
                    
                    Check() can be used as a substitute for assert, as it doesn't get
                    removed when the -O option is used.  It can be turned on and off
                    using the check_off variable.
                    '''
                    if check_off:
                        return
                    tm = ""
                    if incl_time:
                        tm = strftime("[%d%b%Y-%H:%M:%S] ")
                    msg = tm + message
                    if not condition:
                        if log_stream:
                            log_stream.write(msg + "\n")
                        else:
                            raise CheckFailed(msg)
        """)),
        Entry(name="ssig1", cat="math", lang="python", 
            gist="Shortened version of sig",
            code=dedent("""
                '''
                Format numbers to specified number of significant figures
                
                The ssig() function is similar to 'g' string formatting format_spec, but
                you can control the points at which the fixed point formatting is
                changed to scientific notation.
                '''
                def ssig(x, digits=None):
                    '''Returns a string representing the float x to a specified number
                    of significant digits.  x can also be an integer, complex number,
                    sequence of numbers, or any object or sequence of objects that can
                    be converted to a float.  If the digits parameter is None, the
                    ssig.digits setting is used.  Integers are returned with their full
                    number of digits.  Warning: extended precision numbers like
                    decimal.Decimal or mpmath.mpf types may lose precision when
                    converted to floats.
                
                    Function attributes:
                
                    ssig.low         Use scientific notation if x < low
                    ssig.high        Use scientific notation if x > high
                    ssig.digits      Default number of significant digits
                    ssig.dp          String to use for decimal point
                    ssig.rdp         Remove ending decimal point if True
                    ssig.imagunit    Imaginary unit string
                    ssig.rtz         Remove trailing zeroes if True
                    ssig.rlz         Remove leading 0 before decimal point if True
                    '''
                    ssig.low = ssig.__dict__.get("low", 1e-5)
                    ssig.high = ssig.__dict__.get("high", 1e6)
                    ssig.digits = ssig.__dict__.get("digits", 3)
                    ssig.dp = ssig.__dict__.get("dp", ".")
                    ssig.rdp = ssig.__dict__.get("rdp", False)
                    ssig.imagunit = ssig.__dict__.get("imagunit", "i")
                    ssig.rtz = ssig.__dict__.get("rtz", False)
                    ssig.rlz = ssig.__dict__.get("rlz", False)
                    def rtz(s):
                        if not ssig.rtz:
                            return s
                        t = list(s)
                        while t[-1] == "0":
                            del t[-1]
                        return ''.join(t)
                    if ssig.low > ssig.high:
                        raise ValueError("ssig.low > ssig.high")
                    msg = "{}digits = {} is out of range"
                    if not (1 <= ssig.digits <= 15):
                        raise ValueError(msg.format("ssig.", ssig.digits))
                    if digits is not None and not (1 <= digits <= 15):
                        raise ValueError(msg.format("", digits))
                    try:    # If x is an iterable, iterate over it
                        iter(x)
                        T = tuple if isinstance(x, tuple) else list
                        return T(ssig(i, digits=digits) for i in x)
                    except TypeError:
                        pass
                    from sys import version_info
                    Int = int if version_info[0] == 3 else (int, long)
                    if isinstance(x, Int):      # Return integers with all their digits
                        return str(x)
                    elif isinstance(x, complex):
                        r = ssig(x.real, digits=digits)
                        i = ssig(abs(x.imag), digits=digits)
                        sgn = "-" if x.imag < 0 else "+"
                        return "{}{}{}{}".format(r, sgn, i, ssig.imagunit)
                    elif not isinstance(x, float):
                        x = float(x)
                    ndig = ssig.digits - 1 if digits is None else digits - 1
                    if x and (abs(x) < ssig.low or abs(x) > ssig.high):
                        xs = "{:.{}e}".format(x, ndig)      # Use scientific notation
                        st, e = xs.split("e")
                        t = "{}e{}".format(rtz(st), int(e))
                        return t.replace(".", ssig.dp)
                    # xs = list of significant digits with decimal point removed
                    # e = integer exponent
                    xs, e = "{:.{}e}".format(abs(x), ndig).replace(".", "").split("e")
                    xs, e = list(xs), int(e)
                    sgn = "-" if x < 0 else ""
                    if not e:
                        t = "{:.{}e}".format(abs(x), ndig).split("e")[0]
                        u = t.replace(".", ssig.dp)
                        v = rtz(u)
                        if ssig.rdp and v[-1] == ssig.dp:
                            v = v[:-1]
                        return sgn + v
                    elif e < 0:
                        e = abs(e) - 1
                        xs.reverse()
                        while e:
                            xs.append("0")
                            e -= 1
                        xs.append(ssig.dp)
                        if not ssig.rlz:
                            xs.append("0")
                        xs.reverse()
                    else:
                        n = len(xs)
                        if e >= n:
                            e -= n - 1
                            while e:
                                xs.append("0")
                                e -= 1
                            xs.append(ssig.dp)
                        else:
                            xs.insert(e + 1, ssig.dp)
                    t = rtz(''.join(xs))
                    if ssig.rdp and t[-1] == ssig.dp:
                        t = t[:-1]
                    return sgn + t
                        
                if __name__ == "__main__":
                    # A few test cases
                    ssig.digits, ssig.rtz, ssig.rlz = 2, True, True
                    u = 1.23456789
                    for x, s in (
                        (u, "1.2"),
                        (u*10, "12."),
                        (u*100, "120."),
                        (u*1e5, "120000."),
                        (u*1e6, "1.2e6"),
                        (u/10, ".12"),
                        (u/100, ".012"),
                        (u/1e5, ".000012"),
                        (u/1e6, "1.2e-6"),
                        ):
                        assert ssig(x) == s, "ssig({}) != {}".format(x, s)
        """)),
        Entry(name="ssig2", cat="math", lang="python", 
            gist="Even more shortened version of sig",
            code=dedent("""
                def sig(x, digits=3):
                    '''Format numbers or sequences to a specified number of digits.  If
                    x is not a number or sequence, return str(x).
                    '''
                    if isinstance(x, (list, tuple)):
                        items = ["{:.{}g}".format(i, digits) for i in x]
                        return str(items).replace("'", "")
                    elif isinstance(x, int):
                        return str(x)
                    elif isinstance(x, float):
                        return "{:.{}g}".format(x, digits)
                    else:
                        return str(x)
        """)),
        Entry(name="", cat="template", lang="C", 
            gist="Example of using getopt in a C program",
            code=dedent("""
                #include <stdio.h>
                #include <stdlib.h>
                #include <unistd.h>
                
                void Usage(void)
                {
                    printf("xxx Usage\n");
                    exit(0);
                }
                
                // Demo of using getopt for processing command line options.  This one
                // recognizes -d, -f, and -h or -? for a Usage statement.  There can be
                // one or two variables on the command line.
                int main(int argc, char **argv)
                {
                    extern int optind;
                    char *file = "/usr/dict/words";
                    char *string;
                    int ch;
                    int d_option = 0;
                    int f_option = 0;
                    
                    while ((ch = getopt(argc, argv, "dfh?")) != -1)
                    {
                        switch(ch) {
                            case 'd':   
                                d_option = 1; 
                                break;
                            case 'f':
                                f_option = 1;
                                break;
                            case 'h':
                            case '?':
                                Usage();
                                break;
                        }
                    }
                    argc -= optind;
                    argv += optind;
                    if (argc < 1 || argc > 2) 
                        Usage();
                    string = *argv;
                    if (*++argv)
                        file = *argv;
                    printf("d_option = %d\n", d_option);
                    printf("f_option = %d\n", f_option);
                    printf("arg1 = %s\n", string);
                    printf("arg2 = %s\n", file);
                    return 0;
                }
        """)),
        Entry(name="", cat="template", lang="C++", 
            gist="C++ program template",
            code=dedent("""
                #include <iostream>
                using namespace std;
                int main(int argc, char **argv)
                {
                    return 0;
                }
        """)),
        Entry(name="", cat="template", lang="C", 
            gist="C program template",
            code=dedent("""
                #include <stdio.h>
                int main(int argc, char **argv)
                {
                    return 0;
                }
        """)),
        Entry(name="", cat="template", lang="sh", 
            gist="makefile template",
            code=dedent("""
                # vim: noet
                
                f = climits
                e = .cpp
                e = .c
                cc = g++
                cc = gcc
                o = -Wall -g
                
                .PHONY: z
                
                z: 
                    @ctags $f$e
                    $(cc) $o -o $@ $f$e
        """)),
        Entry(name="", cat="template", lang="python", 
            gist="SetUp function for g library",
            code=dedent("""
                def SetUp(file, orientation=portrait, units=inches, wrap_in_PJL=False):
                    '''Convenience function to set up the drawing environment and return a
                    file object to the output stream.
                    '''
                    ofp = open(file, "w")
                    ginitialize(ofp, wrap_in_PJL)
                    setOrientation(orientation, units)
                    return ofp
        """)),
        Entry(name="", cat="utility", lang="python", 
            gist="Calculate the transpose of a nested list",
            code=dedent("""
                How to calculate the 2D transpose of a list of lists
                Suppose A = [[1, 4], [2, 5], [3, 6]] and suppose this represents the two column
                vectors (note you read out in row-major order)
                    1   4
                    2   5
                    3   6
                The transpose is [list(i) for i in zip(*A)], which gives [[1, 2, 3], [4, 5, 6]]; in
                row-major order, this is
                    1   2   3
                    4   5   6
                These matrixes are transposes of each other.
        """)),
    )
    return data

if __name__ == "__main__":
    import collections
    import trm
    defaultdict = collections.defaultdict
    t = trm.Trm()
    di = defaultdict(list)
    for i in GetData():
        di[i.lang].append(i.gist)
    for lang in di:
        t.print(f"{t.orn}{lang}")
        for gist in sorted(di[lang]):
            print(f"  {gist}")

def GetGist():
    g = {}
    g["gist"] = "Data file to hold code snippets"
    g["copy"] = "Copyright © 2005, 2014, 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "notest"
    g["cat"] = ""
    g["todo"] = ''' '''
    return g
