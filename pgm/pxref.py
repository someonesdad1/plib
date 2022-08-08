'''
TODO
    - Update names to 3.9 or 3.10.

Index tokens in python files and spell check them
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Index tokens in python files and spell check them
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from keyword import kwlist as KeywordList
    import pathlib
    import token
    import tokenize
    import re
    import io
    from collections import defaultdict, deque
    from functools import partial
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from color import C
    from f import flt
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    FoldSort = partial(sorted, key=str.lower)
    underscore = "_"
    double_us = "_"*2
    digits = re.compile(r"[0-9]+")
    # Provide a container of the allowed special identifiers that begin and
    # end with double underscores.  This set came from the page
    # file:///C:/cygwin/doc/python/python-3.7.4-docs-html/genindex-_.html and a
    # script that filtered out all the relevant names.
    special_identifiers = set(["__" + i + "__" for i in '''
        abs add aenter aexit aiter all and anext annotations await bases bool
        breakpointhook bytes cached call callback cause ceil class
        class_getitem classcell closure code complex concat contains context
        copy debug deepcopy defaults del delattr delete delitem dict dir dir
        displayhook divmod doc enter eq excepthook exit file float floor
        floordiv format format fspath func future future ge get getattr getattr
        getattribute getitem getnewargs getnewargs_ex getstate globals gt hash
        iadd iand iconcat ifloordiv ilshift imatmul imod import import imul
        index init init_subclass instancecheck int interactivehook inv invert
        ior ipow irshift isub iter itruediv ixor kwdefaults le len length_hint
        loader lshift lt main main matmul missing mod module mro mul name ne
        neg new next not or package path pos pow prepare qualname radd rand
        rdivmod reduce reduce_ex repr reversed rfloordiv rlshift rmatmul rmod
        rmul ror round rpow rrshift rshift rsub rtruediv rxor self set set_name
        setattr setitem setstate slots spec stderr stdin stdout str sub
        subclasscheck subclasses subclasshook suppress_context traceback
        truediv trunc xor
        '''.split()])
    # Keywords are defined in the keyword module
    keywords = set(KeywordList)
    # See the built-in functions list in e.g.
    # file:///C:/cygwin/doc/python/python-3.7.4-docs-html/library/functions.html
    functions = set('''
        __import__ abs all any ascii bin bool breakpoint bytearray bytes
        callable chr classmethod compile complex delattr dict dir divmod
        enumerate eval exec filter float format frozenset getattr globals
        hasattr hash help hex id input int isinstance issubclass iter len
        list locals map max memoryview min next object oct open ord pow
        print property range repr reversed round set setattr slice sorted
        staticmethod str sum super tuple type vars zip'''.split())
    # This set of allowed words is specific to my needs and gets added to
    # over time.  The intent is to allow the -s option to identify the
    # possible token names that don't conform to my typical usage.
    allowed_words = set('''

        a aberration above abs abscissas absdiff absolute abspath abstol
        abstract acos acosh acquire across actual add addition adjust
        affine air algorithm align alignment all allow allowance allowed
        almost alpha altitude ampacity analysis and angle angles angular
        annotate anomaly anova anscombes ansi answer any api app apparent
        append appendleft apply approx approximation apr arange arc
        archimedian arctan are area areacode arg args arguments argv arial
        arithmetic array as ascii asctime ash asin asinh asme assert
        assertion astype atan atanh atexit atm attribute aug augment
        augmented author auto available average avg awful awg axhline axis
        axvline azimuth b back backup backups bad bag banner base based
        basename bases basestring basic batch baudrate beattie before begin
        bell below bernoulli beta betavariate between bevel bg bgcolor
        bgcolors bidict big bin binary bisect bisection bit bitfield bits
        black blocked blockquote blocksize blue body book bool bools both
        bottom bracket break brent bridgman broken brown bsearch buf buff
        bug build by byte bytearray bytes c cache cached calc calculate
        call callable candidate canned canonical capitalize card cardan
        cards case cases cat catalan catalog cdf ceil center cfg chain
        change char character chars chdir check checked chi chill chmod
        choice choices choose chr chunks chunksize circle circumference
        circumscribed class classmethod clean clear clockwise close closed
        closure cls cm cmath cmd cmds cmnt cmp cnt coalesce code codec
        codecs codepoint coef coeff coefficients coeffs coerce col collapse
        collections collinear color colors cols column columnize columns
        comb combination combinations command commands comment common
        commonprefix compass compile complement complex compose composite
        compress con condition conditionals conductivity conjoin console
        constant constants constructor consume container context continue
        continuous conv convergence conversion conversions convert cookbook
        coord coordinates copy copyfile copyright copysign corr corrcoef
        correction correl correlated correlation cos cosh could count
        counter course cov covariance covmat covmatrix cpx creator crenshaw
        croft cross crown ctm ctx cubic cuddle cumul curdir curr currdir
        current cyan cycle cygwin cyl d darcy dash data datafile date
        datetime day days dbase dbg dbm deal debug debugger debuggers dec
        decade decimal decimalmath deck decode decompose decorate decr
        dedent deepcopy def default defaultdict defaults definitions deg
        degree degrees del delattr delegator delete delimited delta
        demonstrate denom denominator density depth deque deriv destination
        det details diagonal diagonals diameter dict dictionary diff
        difference diffs dig digit digits dim dir direction directories
        directory dirname dirs discard disjoin dispatch displayable
        displayhook distance div divide divided division divisor divmod do
        doc doctest document done dot dotproduct double dow dp dpi dpmath
        draw dt dtheta dummy dump dumps duration durbin dx dy dynamic e
        each earth eccentricity echo ecliptic eight either elapsed elem
        element elements elev elif ellipe ellipk ellipse elliptic else
        email embedded empty enable encode encoding encrypted end endswith
        eng engagement engineering engsi entry enumerate environ ephemeris
        epoch eps epsilon eqn equal equality equation equatorial err errmsg
        error errors escape euclidean eval exact example examples exc
        except excepthook exception exceptions exclude exec execfile execv
        exists exit exitfunc exp expand expanduser expandvars expect
        expected exponent exponential expovariate expr ext extend extension
        extensions extra extract extreme eye f fabs factor factorial
        factors fail failed failure failures falling false farey feb fermat
        fg fgcolor fgcolors fibonacci field fields figure figures file
        filename filenum files fill filter filters finally find findall
        finder finish first fit fix fixed flags flat flatten flattening
        flesch flip fln float floor floordiv flt flush fmod fmt fn fold
        fontsize for force fork form format formatter formatting forward
        found four fourth fp fpformat frac fraction fractions frame frames
        frange freq frexp friction from frozen frozendict frozenset ft full
        func funcs function functions functools fund fwd g gamma
        gammavariate gap gas gauge gauss gcd generate generator get
        getatime getattr getcontext getctime getcwd getdefaultencoding
        getframe getmtime getnum getnumber getopt getpid getrandbits
        getrecursionlimit getrefcount getsize getstate gettext getvalue ghz
        ginitialize glob global globals gmtime gnu gohm got goto gpl
        grammage gray great green gregorian grep grid group groupby grouper
        groupindex groups gtk guts h half halflife halt hand handle hands
        harsh has hasattr hash hashlib have hd header headers heading heat
        height help helvetica hex hexdigest hexdigits hexdump hi high
        hilbert hip his histogram homogeneous horizontal hour hours hp hr
        hsl hsv html humidity hundreds hyphen hypot hz i id ideal ident
        identifier identifiers identities if ifp ignore ii im imag image
        images imaginary imp impl implementation import important improper
        in inc inches include incr increase increment indent indentation
        indeterminate index indices individual inexact inf infinite
        infinity infj info init initial initialize initialized input ins
        inscribed insert inserted insertion inspect instance int integer
        integral intercept interpolate interpolation interpret intersect
        intersection intersects interval intervals ints invalid inverse
        invert invnorm io is isabs isalnum isalpha isatty iscomplex isdigit
        isdir isfile isinf isinstance islink islower ismount isnan isprime
        isspace issubclass issubset istitle isupper it item itemgetter
        items iter iterable iteration iterations iterator iteritems
        iterkeys itertools itervalues j jan jd join jul julian jumpahead
        jun justify k kbhit kcal keep kepler kev key keys keyword keywords
        kg khz kill kinematic kinkaid km kohm kohms kw kwargs kwds kwh
        kwlist l label labels lagrange lambda landscape larger largest last
        lasts latest latitude latitudinal law lb lbf lblue lbm lcyan ldexp
        lead leap least left legend len length lengths letter letters level
        levels lexists lgreen license licenses limit line linear linenum
        lines linesep link list listdir ljust lmagenta ln lngamma local
        localcontext locale locals localtime locate location lock log log1p
        lognormvariate long longest longitude longitudinal loo lookup low
        lower lowercase lred lseek lstat lstrip lwhite lwtest m magenta
        main major make makefile manager manpage mantissa mantissas manual
        map mar mask mass match matches math matplotlib matrix max maxcnt
        maxcount maxint maxit maxlen may me mean means median meeus memoize
        memoized merge meridian messages method mg mhz middle miller
        milliohm min minimum minor missing misspelled miter mixed mkdir
        mktemp mm mo mode model modf modules mohm mol molar moments month
        months moon most motion moulding move mpc mpf mph mpmath mr msg
        msvcrt mu mul multiple multiplication multiply mv my n naive name
        names nan nanj nbs ncol ncols ncurses ndigits need needed needs neg
        negate negative new newlines newton next ng nibbles nl nm no noise
        nominal none nonzero noprint norm normal normalize normalvariate
        normcase normpath not nov novas nrow nrows nu num number numbers
        numbits numbytes numelem numer numerals numerator numpages numpy
        nums numspaces nutation o object objects obliquity oct octdigits
        odd odict of off offset offsets ofp ohm ok old omega on one ones
        only op open operation operator opname option options optlist
        optparse opts or orbit ord order ordering ordinal ordinals
        orientation orig origin osl other our out outfile output over
        overflow overlap override p packing page pager pages pair pairwise
        pal palette parallax param parameter parameters params pardir
        paretovariate parse parsed part partial partition partitions pass
        path pathlib pathsep pattern pct pdb pdf pending pep per percent
        percentage percentile performance perimeter permutation
        permutations permute phase phi phrase pi pick pickle picture
        pictures pieces pio pipe pjl places plane planet platform plot plow
        pm point points pol polar pole polyeval polynomial pool pools pop
        popen popitem popleft population portrait pos position possible
        post pound pow power powerset ppb ppm pprint pre prec precession
        precision pred prefix prefixes preserve pressure prev previous
        prime primes print printable printed probabilistic process prod
        producer product program promote prompt proper properties property
        protocol ps psi pt punctuation push putenv py pycephes pylab pyplot
        pyprimes pyver q quadratic quadrilateral quantify quarter quartet
        quartic quiet quit r rabin rad radians radius radix raise raises
        rand randint random randomize randrange range ranges raphson ratio
        rational raw raw_input rdp re read readability reader readline
        readlines real realpath rectilinear red reduce reducer ref refract
        refs regex regexp regexps register regression rel relative relaxed
        reldiff reldiffs release reload relpath reltol rem remainder remove
        rename repeat repl replace replacement report repr requested reset
        resid resids residuals response restore result results return
        retval rev reverse reversed revolutions rfind rho rhumbline ridders
        right rightmost rindex rising river rjust rmdir rnd rng rodict
        roman root roots rotate rotation rotations round rounded roundoff
        roundrobin row rows rpartition rpm rsplit rstrip rtd rtz run
        runtime rv s sales sample savefig scalar scale scaled sci scipy
        scratch screen sdev search seconds seed seek seen select selection
        selections selectors self semilogx semilogy sentinel sep separation
        separator seq sequence series set setattr setdefault
        setdefaultencoding setf setlocale setprofile setrecursionlimit
        setstate setter settrace sgn shape shapes short show shuffle
        shuffled shutil si sic sidereal sieve sig sigcomp sigfig sigma sign
        signed significand significant signum similar simple simplest
        simpson sin sine singleton singletons singular sinh site size sizes
        slice slope small softlink softlinks solidus solve some sort sorted
        sound soundex sp space spaces spc special specifiers speed spell
        sph spin spines spiral split splitdrive splitext splitlines
        splitunc spokes sq sqrt square squared squares stable stack star
        stars start starting startswith stat state states staticmethod
        statistics stats status std stddev stderr stdev stdin stdout step
        stirling stop str stream streams strerror strftime strict string
        stringio strings strip struct style sub subclasses subject subn
        subplot subprocess subs subset substring suffix suffixes suit suite
        sum sun sunday sunrise sunset super suppress surface swap swapcase
        switch sx sxx sxy sy symbol symbols symlink symmetric syntax sys
        system syy t table tabulate tag take tan tanh tau tc tee tell temp
        temperature tempfile template ten tens tenths term terms test
        testing tests text textattr texttable textwrap then thermal
        thermistor theta thing thoughts thread threading three thresh
        threshold time timeit times timezone timezones timing tin title tm
        tmp tmpfile to todo token tokeneater tokenize tokenized tokens tol
        tolerance top total tpi trace traceback tracebacklimit tracing
        trail trailing transform transformed translate transpose trapezoid
        trapezoidal trial trials triangle triangular trie trigger true
        truediv truncate truth try tuple tuples turner two twopi typ type
        typeahead types u ufloat ug um umask umath uname unc uncertainties
        uncertainty underscore unichr unicode unified uniform union unique
        unit units unittest univariate unknown unlink unpack unsigned uohm
        up update upper uppercase urandom url urllib urlopen us usage usb
        use used user util utime v val valid validate value values var
        variable variables varnames vars vec vector vel version vertical
        via virtual viscosity vmax vmin voltage vonmisesvariate vout vrms w
        wait waitpid walk wall warn warnings watch watermark watson wconio
        weaver week weibull weibullvariate westwood wheel which while white
        whitespace whole width win wind windll wire with within wobble word
        wordnum words wrap write writeline writelines writer x xbar xfm xi
        xkcd xlabel xlast xlim xref xticks xx y yaml ybar year years yellow
        yhat yield ylabel ylim yticks z zero zeros zeta zfill zip zipcode
        zipfile zlib

        spelled

    '''.split())    # End of allowed_words
def GetLatestSymbols():
    '''This function replaces the global variables
    special_identifiers, keywords, and functions with the sets gotten from the
    python 3.9.6 documentation at https://docs.python.org/3/py-modindex.html, 
    downloaded 21 Jul 2021 10:18:55 AM.  The main documentation was selected,
    then the page for "_" was chosen and put into a string s.
 
    Here's the code that generated the list for special identifiers from s:
        for i in s.strip().split("\n"):
            i = i.strip()
            if i and i.startswith("__"):
                j = i.split()[0]
                if j.endswith("__") or j.endswith("()"):
                    if j.endswith("()"):
                        j = j[:-2]
                    print(j)
 
    The only changes between 3.7.4 and 3.9.6 were the additions of 
    __unraisablehook__, __parameters__, __origin__, and __args__.
 
    Here's the code that showed this:
        # Show differences between python 3.7 and 3.9
        si7 = special_identifiers
        kw7 = keywords
        func7 = functions
        GetLatestSymbols()
        si9 = special_identifiers
        kw9 = keywords
        func9 = functions
        print(dedent(f"""
        Special identifiers:
            7, not 9:  {si7 - si9}
            9, not 7:  {si9 - si7}
        Keywords:
            7, not 9:  {kw7 - kw9}
            9, not 7:  {kw9 - kw7}
        Functions:
            7, not 9:  {func7 - func9}
            9, not 7:  {func9 - func7}
        """))
    '''
    global special_identifiers, keywords, functions 
    special_identifiers = set(["__" + i + "__" for i in '''
        abs add aenter aexit aiter all and anext annotations args await bases
        bool breakpointhook bytes cached call callback cause ceil class
        class_getitem classcell closure code complex concat contains context
        copy debug deepcopy defaults del delattr delete delitem dict dir dir
        displayhook divmod doc enter eq excepthook exit file float floor
        floordiv format format fspath func future future ge get getattr getattr
        getattribute getitem getnewargs getnewargs_ex getstate globals gt hash
        iadd iand iconcat ifloordiv ilshift imatmul imod import import imul
        index init init_subclass instancecheck int interactivehook inv invert
        ior ipow irshift isub iter itruediv ixor kwdefaults le len length_hint
        loader lshift lt main main matmul missing mod module mro mul name ne
        neg new next not or origin package parameters path pos pow prepare
        qualname radd rand rdivmod reduce reduce_ex repr reversed rfloordiv
        rlshift rmatmul rmod rmul ror round rpow rrshift rshift rsub rtruediv
        rxor self set set_name setattr setitem setstate slots spec stderr stdin
        stdout str sub subclasscheck subclasses subclasshook suppress_context
        traceback truediv trunc unraisablehook xor'''.split()])
    # Keywords copied from web page
    # https://docs.python.org/3/reference/lexical_analysis.html#keywords
    keywords = set('''
        False None True and as assert async await break class continue def del
        elif else except finally for from global if import in is lambda
        nonlocal not or pass raise return try while with yield'''.split())
    # See the built-in functions list in e.g.
    # https://docs.python.org/3/library/functions.html
    functions = set('''
        __import__ abs all any ascii bin bool breakpoint bytearray bytes
        callable chr classmethod compile complex delattr dict dir divmod
        enumerate eval exec filter float format frozenset getattr globals
        hasattr hash help hex id input int isinstance issubclass iter len list
        locals map max memoryview min next object oct open ord pow print
        property range repr reversed round set setattr slice sorted
        staticmethod str sum super tuple type vars zip'''.split())
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [pyfile1 [pyfile2...]]
      Print a cross-reference of the tokens in the indicated python source
      code files.  The text in comments and strings is ignored.
    Options
      -c          Show tokens sorted by number of occurrences
      -d dict     Specify a spelling dictionary in addition to default dict
                  (you can use more than one -d option)
      -D dict     Don't use default set of allowed words
      -e enc      Specify encoding for files [{d["-e"]}]
      -h          Print more help information
      -k chars    Specify types of tokens to display:  f = python functions,
                  r = python reserved words, s = special methods,
                  u = user tokens.  [{d["-k"]}]
      -s          Print only misspelled tokens
      -S          Same as -s, but show misspelled word in color (tells you
                  which part of a token is misspelled)
      -t          Print tokens only
      -v          Print statistics
    '''))
    exit(status)
def Manpage():
    print(dedent(f'''
    This script is useful for finding the location of tokens in a set of python
    scripts.  The default output is a list of tokens that don't occur in
    comments and strings.  Under each token is the file it appeared in and a
    list of line numbers in that file where the token appeared.  Use the -t
    option if you only want a sorted list of tokens.  Tokens are found by
    replacing punctuation characters by space characters and splitting on
    whitespace.
 
    The -s option prints out misspelled tokens.  The tokens are split on
    capital letters or underscores and the individual words are checked in
    the supplied dictionaries.  The allowed_words global variable holds the
    set of words that are spelled correctly; you'll want to tune this list
    to your own needs.  Use the -D option to disable the use of this set of
    words.  When a misspelled composite token is indicated, use the -S
    option to highlight the word portion of that token that is considered
    misspelled.

        A use case for this script is to monitor naming of symbols in a
        programming project.  On some of the projects I've worked on, we
        had the policy that all tokens needed to be correctly-spelled
        complete English words.  We had programmers from different
        countries that didn't speak English as their first language and
        abbreviated words in token names could be confusing to them.  
        A thoughtfully-chosen and correctly-spelled name helped document
        the code with little extra work.

    The -d option lets you specify files containing correctly spelled
    words.  Empty lines and lines beginning with '#' are ignored.  Note
    that all words are converted to lowercase, so case is unimportant for
    spell checking.

    '''.rstrip()))
    exit(0)
def ParseCommandLine():
    d["-c"] = False         # Sorted by number of occurrences
    d["-D"] = False         # Don't use default set of words
    d["-d"] = []            # Additional dictionaries
    d["-e"] = "UTF-8"       # Encoding of files
    d["-k"] = "frsu"        # Tokens to display
    d["-S"] = False         # Show misspelled words in color
    d["-s"] = False         # Spell check
    d["-T"] = False         # Short listing, columnized
    d["-t"] = False         # Short listing
    d["-v"] = False         # Include statistics
    # The tokens found in the input files will be stored in the
    # following dictionary.  The key is the token and the value is a
    # list of (filenum, linenum) where the token occurs.
    d["tokens"] = defaultdict(list)
    d["non-ascii"] = set()  # Tokens with non-ASCII characters
    if len(sys.argv) < 2:
        Usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cd:De:hgk:SsTtv", "help")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "cDSsTtv":
            d[o] = not d[o]
        elif o in ("-d",):
            d["-d"].append(P(a))
        elif o in ("-e",):
            d["-e"] = a
        elif o in ("-h", "--help"):
            Manpage()
        elif o in ("-k",):
            S = set(d["-k"])
            A = set(a)
            if not A.issubset(set(d["-k"])):
                Error("'{}' contains an illegal letter".format(a))
            d["-k"] = a
    if not args:
        Usage()
    if d["-S"]:
        d["-s"] = True
    if d["-s"] or d["-S"]:
        # Check any user supplied dictionaries exist
        for i in d["-d"]:
            if not i.exists():
                Error(f"Dictionary file '{i}' doesn't exist")
    args = FoldSort(args)  # Sort input files in dictionary order
    return args
def GetNameTokens(file):
    '''Generator that returns (name, linenum) tuples of tokens for a
    python source code file.
    '''
    with io.open(file, "r", encoding=d["-e"]) as f:
        try:
            for tok in tokenize.generate_tokens(f.readline):
                tok = list(tok)
                if token.tok_name[tok[0]] == "NAME":
                    name, linenum = tok[1], tok[2][0]
                    include = False
                    if "u" in d["-k"]:
                        include |= (name not in
                                    functions.union(keywords,
                                                    special_identifiers))
                    if "f" in d["-k"]:
                        include |= name in functions
                    if "r" in d["-k"]:
                        include |= name in keywords
                    if "s" in d["-k"]:
                        include |= name in special_identifiers
                    if include:
                        yield name, linenum
        except Exception as e:
            print(dedent(f'''
            Unexpected exception for file '{file}':
              {e}'''))
            exit(1)
def ProcessFile(filenum, file):
    for name, linenum in GetNameTokens(file):
        if max([ord(i) for i in name]) > 127:
            d["non-ascii"].add(name)
        d["tokens"][name].append((filenum, linenum))
def GetWords(file):
    '''Read in the words from the indicated file (words are separated
    by spaces and newlines) and return the set of the words converted
    to lower case.
    '''
    words = set()
    with open(file, "r") as f:
        for line in f:
            if not line or line.lstrip().startswith("#"):
                continue
            words.update([i.lower() for i in line.split()])
    return words
def GetDictionary():
    '''Read in the indicated dictionaries and convert each item to
    lower case.  The resulting dictionary will be a set in
    d["dictionary"].
    '''
    D = d["dictionary"] = set()
    if not d["-D"]:
        D.update(allowed_words)   # Default set of words
    for file in d["-d"]:
        D.update(GetWords(file))
def TokenSplit(token):
    '''Return a list of the token's elements split at underscores or
    capital letters.
    '''
    o, T = [], deque(token)
    while T:
        c = T.popleft()
        if c in TokenSplit.s:
            o.append(" ")
        o.append(c if c != "_" else " ")
    return [i.lower() for i in ''.join(o).split()]
TokenSplit.s = set("_ABCDEFGHIJKLMNOPQURSTUVWXYZ")
def SpelledOK(token):
    '''Return True if the string token is spelled properly.  If one or
    more underscores are present, then name is split into subtokens by
    the underscore characters.  Otherwise, the capital letters in the
    name are used to split the token into subtokens and each subtoken's
    spelling is checked.
    '''
    if not token:
        return True
    if not d["dictionary"]:
        return False
    name = digits.sub("", token)  # Remove any digits
    if name.startswith(double_us) and name.endswith(double_us):
        return name in special_identifiers
    # Remove any leading underscores
    while name.startswith(underscore):
        name = name[1:]
    for word in TokenSplit(token):
        if word not in d["dictionary"]:
            if d["-S"]:
                print(f"{C.lmag}{word}{C.norm}")
            return False
    return True
def SpellCheck():
    '''Remove any items in d["tokens"] that are spelled correctly.
    '''
    GetDictionary()
    remove = []
    for name in d["tokens"]:
        if SpelledOK(name):
            remove.append(name)
    for name in remove:
        del d["tokens"][name]
def CalculateStatistics():
    stats, T = {}, d["tokens"]
    # T is {"tokname": [(filenum, line), (filenum, line), ...], etc.}
    max_refs, name = 0, None
    # Token with the maximum number of references
    bysize = defaultdict(list)  # T find longest tokens
    mean_length = 0
    for t in T:
        mean_length += len(t)
        L = len(T[t])
        if L > max_refs:
            max_refs, name = L, t
        bysize[len(t)].append(t)
    stats["max_refs"] = name
    stats["mean_length"] = mean_length/len(T)
    stats["num_tokens"] = len(T)
    stats["longest_tokens"] = bysize[max(bysize)]
    # Tokens with only one reference
    oneref = []
    for name in T:
        if len(T[name]) == 1:
            oneref.append(name)
    stats["one_ref"] = oneref
    d["stats"] = stats
def PrintReport():
    if d["-T"]:  # Print tokens in columns
        for name in FoldSort(d["tokens"].keys()):
            print(line)
        return
    elif d["-c"]:  # Print tokens sorted by number of occurrences
        o = []  # Elements will be (count, token)
        T = d["tokens"]
        CalculateStatistics()
        w, k, spc = len(d["stats"]["longest_tokens"][0]), 12, " "*4
        for token in T:
            o.append((len(T[token]), token))
        print(f"{'Token':^{w}s}{spc}{'Count':^{k}s}")
        print(f"{'-'*w:^{w}s}{spc}{'-'*k:^{k}s}")
        for n, token in sorted(o):
            print(f"{token:{w}s}{spc}{n:^{k}d}")
        return
    for name in FoldSort(d["tokens"].keys()):
        if d["-t"]:  # Print tokens only
            print(name)
        else:
            # Group by file number
            group = {}
            for filenum, linenum in d["tokens"][name]:
                if filenum not in group:
                    group[filenum] = []
                group[filenum].append(linenum)
            print(name)
            for filenum in group:
                file = d["files"][filenum]
                s = [str(i) for i in set(group[filenum])]
                nums = " ".join([str(i) for i in FoldSort(s)])
                if group[filenum]:
                    print(f"    {file}:  {nums}")
    if d["-v"]:
        CalculateStatistics()
        s = d["stats"]
        tor = len(s["one_ref"])
        ref = s["max_refs"]
        mr = len(d["tokens"][ref])
        n = s["num_tokens"]
        ml = flt(s["mean_length"])
        print(dedent(f'''
        Summary statistics:
            Tokens with one reference    = {tor}
            Maximum number of references = {mr} ({ref})
            Total number of tokens       = {n}
            Mean token length            = {ml}
        '''))
        longest = s["longest_tokens"]
        p = "s" if len(longest) > 1 else ""
        print(f"    Longest token{p}:")
        for i in s["longest_tokens"]:
            print(f"      {i}")
    if d["non-ascii"]:
        print("Warning, non-ASCII characters are in the following tokens:",
              file=sys.stderr)
        for i in FoldSort(d["non-ascii"]):
            print(f"    {i}", file=sys.stderr)
if __name__ == "__main__":
    d = {}  # Options dictionary
    d["files"] = ParseCommandLine()
    for i, file in enumerate(d["files"]):
        ProcessFile(i, file)
    if d["-s"]:
        SpellCheck()
    PrintReport()
