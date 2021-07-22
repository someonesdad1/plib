'''
Generate a series of random numbers
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2003 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generate a series of random numbers
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import re
    import getopt
    import random
    import statistics
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from f import flt
def Percentile(seq, fraction):
    '''Return the indicated fraction of a sequence seq of sorted
    values.  fraction will be forced to be in [0, 1].
 
    The method is recommended by NIST at
    https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm.
    '''
    if not seq:
        return None
    N = len(seq)
    if N == 1:
        raise ValueError("Sequence must have at least 2 elements")
    fraction = max(min(fraction, 1), 0)     # Clamp to [0, 1]
    x = fraction*(N + 1)
    k = int(x)      # Integer part of x
    d = x - k       # Fractional part of x
    if 0 < k < N:
        yk = seq[k - 1]
        y = yk + d*(seq[k] - yk)
    elif k >= N:
        y = seq[-1]
    else:
        y = seq[0]
    return y
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dist N [other_parameters]
      Generate N random numbers from the following distributions:
                 Parameters         Constraints [defaults]
        beta     N a b              a > 0, b > 0 [a = 1, b = 1]
        binomial N p m              p in [0, 1], m > 0 [m = 1, p = 0.5]
        bsample  N m                Sample m items with replacement from 1..N
        expon    N mu               mu = 1/(desired mean).  Range = [0, inf) if
                                    mu > 0, (-inf, 0] if mu < 0 [mu = 1]
        gamma    N a b              a > 0, b > 0 [a = 1, b = 1]
        logn     N mu sigma         sigma > 0 (lognormal distribution)
                                    [mu = 1, sigma = 1]
        normal   N mu sigma         sigma > 0 [mu = 0, sigma = 1]
        pareto   N a                [a = 1]
        poisson  N mu               mu > 0 [mu = 1]
        rand     N                  Real from [0, 1)
        sample   N m                Select a random sample of m integers from 
                                    1..N without replacement
        shuffle  N M                Shuffle the integers from 1 to N (or N to M
                                    inclusive if M is given)
        tri      N low hi infl      Triangular on [low, hi] with infl inflection.
                                    [low = 0, hi = 1, infl = (low + hi)/2]
        uint     N a b              Integers on [a, b] [a = 1, b = a + 1]
        uniform  N a b              Reals on [a, b] [0, 1]
        weibull  N a b              a > 0, b > 0 (b is shape parameter) [1, 1]
      Parameters may be python expressions.
    Options:
      -c    Don't output in columns; print one number per line 
      -d n  Specify number of significant digits for output [{d["-d"]}]
      -h    Show some examples of use
      -i    Force output to be integers
      -n    Put all the numbers on one line
      -o    Sort the output from low to high.  
      -q    Don't print the random numbers generated
      -s s  Specify the seed for the random number generator
      -v    Print parameters used and sample statistics of the random
            variates produced
      -V    Same as -v except produce percentiles every 1%
    '''))
    exit(status)
def Examples(d):
    name = sys.argv[0]
    print(dedent(f'''
                      Examples of use of the {name} script
    
    These examples use a seed of 0.  Note you only have to type enough
    letters of the distribution name to identify it.
     
    * Estimate the CDF
        The cumulative distribution function of a distribution is a useful
        quantity to have.  You can estimate it for the distributions
        supplied by using the -v and -V options to print out the sample
        statistics, which includes a table of percentiles.  The -v option
        prints percentiles every 5% and the -V option every 1%.

        Here's an example of the standard normal distribution:
            python {name} -s 0 -Vq norm 1e5 0 1
            
        Normal distribution
            Mean = 0.0
            Standard deviation = 1.0
            Seed = 0
            Number of points = 100000
        Sample statistics:
            n      100000
            mean   -0.00508
            median -0.00706
            mode   undefined
            sdev   0.999
            min    -4.05
            max    4.67
            range  8.72   [±4.36 standard deviations]
            Percentiles:
              0  -4.05    21  -0.812   41  -0.235    61  0.274    81  0.873
              1  -2.32    22  -0.778   42  -0.208    62  0.299    82  0.910
              2  -2.05    23  -0.744   43  -0.182    63  0.327    83  0.951
              3  -1.88    24  -0.713   44  -0.157    64  0.353    84  0.994
              4  -1.75    25  -0.681   45  -0.132    65  0.382    85  1.04
              5  -1.65    26  -0.650   46  -0.108    66  0.409    86  1.08
              6  -1.56    27  -0.621   47  -0.0836   67  0.437    87  1.12
              7  -1.48    28  -0.591   48  -0.0583   68  0.465    88  1.17
              8  -1.41    29  -0.560   49  -0.0328   69  0.492    89  1.22
              9  -1.35    30  -0.531   50  -0.00706  70  0.520    90  1.28
             10  -1.29    31  -0.503   51  0.0182    71  0.549    91  1.33
             11  -1.23    32  -0.474   52  0.0435    72  0.581    92  1.40
             12  -1.18    33  -0.444   53  0.0682    73  0.611    93  1.47
             13  -1.13    34  -0.418   54  0.0952    74  0.640    94  1.55
             14  -1.09    35  -0.391   55  0.120     75  0.671    95  1.64
             15  -1.04    36  -0.364   56  0.146     76  0.702    96  1.74
             16  -1.00    37  -0.338   57  0.172     77  0.735    97  1.87
             17  -0.960   38  -0.312   58  0.198     78  0.768    98  2.04
             18  -0.921   39  -0.287   59  0.223     79  0.802    99  2.33
             19  -0.885   40  -0.261   60  0.247     80  0.836   100  4.67
             20  -0.848

        You can linearly interpolate to find that the percentile at 1
        standard deviation is 84 + (1 - 0.994)/(1.04 - 0.994) or 84.13.
        This is correct to 4 significant figures.  For 2 standard
        deviations, the percentile is 97.765; a table gives 97.725, off
        by 0.04%.

    * Simulate 10 tosses of a fair coin
        python {name} -s 0 binomial 10 0.5 1
            --> 1 0 1 0 1 1 1 1 1 1
        The 0's could represent heads and the 1's could represent tails.
     
    * You have a group of 72 objects and you want a random sample of 8 of them,
      drawn without replacement (they'll be numbered from 1 to 72):
        python {name} -s 0 sample 72 8
            --> 30 20 3  46 44 43 27 5
     
        To print the output in sorted order use -o:
            python {name} -s 0 -o sample 72 8
                --> 3  5  20 27 30 43 44 46
        
        For a sample of 8 of the 72 objects taken with replacement:
            python {name} -s 0 -o bsample 72 8
                --> 3  8  18 27 27 28 66 69
            Note 27 was drawn twice; it's easier to see duplicates if you sort
            the output with the -o option.
     
    * You have designed an experiment with 12 distinct treatments.  Good
      experimental protocol suggests randomizing the order in which these
      treatments are applied:
        python {name} -s 0 shuffle 12
            --> 3  10 8  11 9  7  1  4  12 5  2  6
     
    * A radioactive source with a half life of millions of years has a count
      rate of 235 counts per minute.  Suppose we make 50 sequential five minute
      counts; print out a simulation of the actual counts that would be gotten,
      assuming a Poisson process and include the basic counting statistics
      using the -v option:
        python {name} -v -s 0 -d 4 poi 50 '235*5'
      results in
        Poisson distribution
            mu = 1175.0 (single event exponential distribution parameter)
            Seed = 0
            Number of points = 50
        1170 1155 1242 1130 1122 1206 1126 1096 1214 1182 1258 1184 1149 1120
        1129 1181 1182 1182 1105 1239 1253 1130 1151 1176 1198 1200 1235 1151
        1214 1153 1244 1155 1179 1178 1211 1166 1150 1176 1173 1231 1169 1164
        1158 1158 1172 1195 1200 1149 1152 1215
            Sample statistics:
                n      50
                mean   1177.
                median 1174.
                mode   1182
                sdev   38.77
                min    1096
                max    1258
                range  162   [+/- 2.089 standard deviations]
            Percentiles:
                  0  1096                      55  1178.
                  5  1113.                     60  1182.
                 10  1126.                     65  1182.
                 15  1130.                     70  1197.
                 20  1149.                     75  1202.
                 25  1151.                     80  1213.
                 30  1154.                     85  1221.
                 35  1158.                     90  1239.
                 40  1165.                     95  1248.
                 45  1170.                    100  1258
                 50  1174.
    
      The standard deviation is about the square root of the number of counts
      per counting interval, as would be expected.  Note we used the -d option
      to get 4 significant figures for the percentiles table (3 figures is not
      quite enough).
     
    * There are 365 objects in a set.  Randomly draw 23 of these objects and
      repeat.  How often do you get two or more of the same objects in the
      sample?  Here's a shell script that would generate a simulation of 50
      repeats (the seq script outputs a sequence of numbers, one number per
      line):
     
          rm -f results
          for i in $(seq 1 50); do
            python {name} -n -o bsample 365 23 >>results
          done
     
      The following python script
     
          import sys
          for line in sys.stdin.readlines():
              items = line.strip().split()
              if len(items) != len(set(items)):
                  print(line.strip())
     
      can then show you the lines in the result file that have duplicate
      numbers.  If you run these tests a few times, you should find that about
      half of the lines have duplicate numbers.  This is a demonstration of
      what's called the birthday paradox.  If you have 23 people in a room,
      there's about a 50% probability that two or more people in the room have
      the same birthday.
      
      Explanation:  Select two people at random.  The probability that the
      second person has the same birthday as the first is 1/365.  The
      probability that the two people have a different birthday is 1 - 1/365 or
      364/365.  
     
      Now we ask what the probability is for all of the 23 pairs of people in
      the room to have a different birthday.  There are 23 choose 2 or
      23!/(2!*(23 - 2)!) = 23*11 = 230 + 11 = 253 distinct pairs of people.
      For none of the pairs to have the same birthday, we must have (pair one
      different) AND (pair two different) AND (...) etc. because each of these
      occurrences is (presumably) independent in a statistical sense.  Thus, we
      multiply the probability 364/365 together 253 times.  If you do this,
      you'll find the probability of no shared birthdays to be about 1/2.  But
      that also means that about half of the time two people in the room share
      a birthday.
    
    * Distribution of run sizes in flipping a coin.  While a special script
      could be written to simulate this, it's pretty easy to get an estimate
      using the {name} script.  The method will be to generate a large sample,
      have the script print out the results on one line and save the results to
      a file.  Then we massage the output with a text editor and use a simple
      python script to print out a count of the run sizes.  First, we use the
      command to get a million 0's and 1's:

        python {name} -s 0 binomial 1e6 0.5 1 >results
    
      This results in a file with one long line of 0's and 1's.  Then the
      following python script is used to print out the counts and frequencies
      of the run lengths:
    
            import sys
            from collections import defaultdict
    
            counts = defaultdict(int)
            line = open("results").readline()
            while "1 1" in line:
                line = line.replace("1 1", "11")
            # Line is now '1 0 1 0 1111111 0 0 0 11111 0 ...'.  Replace all '0'
            # characters with a space.
            line = line.replace("0", " ")
            # Split the line and record the length of the runs.
            s = line.split()
            for run in s:
                counts[len(run)] += 1
            # Print count information
            total_counts = len(s)
            print("""
             Run
            length     Count    Percentage"""[1:])
            for runlength, count in sorted(counts.items()):
                print("{{:3d}} {{:12d}}       {{:.2g}}%".format(runlength, count,
                                                    100*count/total_counts))
            print("Total count of runs =", total_counts)
    
      which prints
    
             Run
            length     Count    Percentage
              1       125106       50%
              2        62544       25%
              3        31263       12%
              4        15725       6.3%
              5         7810       3.1%
              6         3896       1.6%
              7         1865       0.75%
              8          986       0.39%
              9          493       0.2%
             10          268       0.11%
             11          130       0.052%
             12           66       0.026%
             13           38       0.015%
             14           19       0.0076%
             15            9       0.0036%
             16            2       0.0008%
             18            1       0.0004%
             20            1       0.0004%
             21            1       0.0004%
            Total count of runs = 250223
    
      The expected number of runs are the probability of (k - 1) 1's and one 0,
      which is given by
            p*(1 - p)**(k - 1) = 1/2**k because p = 0.5.
      For run length = k = 9, you'd expect a percentage of 100/2**9 or 0.19%;
      the table's 0.2% is close.
    '''))
    exit(0)
def sig(x, digits=None):
    '''Returns a string representing the float x to a specified number
    of significant digits.  x can also be an integer, complex number,
    sequence of numbers, or any object or sequence of objects that can
    be converted to a float.  If the digits parameter is None, the
    sig.digits setting is used.  Integers are returned with their full
    number of digits.  Warning: extended precision numbers like
    decimal.Decimal or mpmath.mpf types may lose precision when
    converted to floats.
 
    Function attributes:
 
    sig.low         Use scientific notation if x < low
    sig.high        Use scientific notation if x > high
    sig.digits      Default number of significant digits
    sig.dp          String to use for decimal point
    sig.rdp         Remove ending decimal point if True
    sig.imagunit    Imaginary unit string
    sig.rtz         Remove trailing zeroes if True
    sig.rlz         Remove leading 0 before decimal point if True
    '''
    sig.low = sig.__dict__.get("low", 1e-5)
    sig.high = sig.__dict__.get("high", 1e6)
    sig.digits = sig.__dict__.get("digits", 3)
    sig.dp = sig.__dict__.get("dp", ".")
    sig.rdp = sig.__dict__.get("rdp", False)
    sig.imagunit = sig.__dict__.get("imagunit", "i")
    sig.rtz = sig.__dict__.get("rtz", False)
    sig.rlz = sig.__dict__.get("rlz", False)
    def rtz(s):
        if not sig.rtz:
            return s
        t = list(s)
        while t[-1] == "0":
            del t[-1]
        return ''.join(t)
    if sig.low > sig.high:
        raise ValueError("sig.low > sig.high")
    msg = "{}digits = {} is out of range"
    if not (1 <= sig.digits <= 15):
        raise ValueError(msg.format("sig.", sig.digits))
    if digits is not None and not (1 <= digits <= 15):
        raise ValueError(msg.format("", digits))
    try:    # If x is an iterable, iterate over it
        iter(x)
        T = tuple if isinstance(x, tuple) else list
        return T(sig(i, digits=digits) for i in x)
    except TypeError:
        pass
    if isinstance(x, int):      # Return integers with all their digits
        return str(x)
    elif isinstance(x, complex):
        r = sig(x.real, digits=digits)
        i = sig(abs(x.imag), digits=digits)
        sgn = "-" if x.imag < 0 else "+"
        return "{}{}{}{}".format(r, sgn, i, sig.imagunit)
    elif not isinstance(x, float):
        x = float(x)
    ndig = sig.digits - 1 if digits is None else digits - 1
    if x and (abs(x) < sig.low or abs(x) > sig.high):
        xs = "{:.{}e}".format(x, ndig)      # Use scientific notation
        st, e = xs.split("e")
        t = "{}e{}".format(rtz(st), int(e))
        return t.replace(".", sig.dp)
    # xs = list of significant digits with decimal point removed
    # e = integer exponent
    xs, e = "{:.{}e}".format(abs(x), ndig).replace(".", "").split("e")
    xs, e = list(xs), int(e)
    sgn = "-" if x < 0 else ""
    if not e:
        t = "{:.{}e}".format(abs(x), ndig).split("e")[0]
        u = t.replace(".", sig.dp)
        v = rtz(u)
        if sig.rdp and v[-1] == sig.dp:
            v = v[:-1]
        return sgn + v
    elif e < 0:
        e = abs(e) - 1
        xs.reverse()
        while e:
            xs.append("0")
            e -= 1
        xs.append(sig.dp)
        if not sig.rlz:
            xs.append("0")
        xs.reverse()
    else:
        n = len(xs)
        if e >= n:
            e -= n - 1
            while e:
                xs.append("0")
                e -= 1
            xs.append(sig.dp)
        else:
            xs.insert(e + 1, sig.dp)
    t = rtz(''.join(xs))
    if sig.rdp and t[-1] == sig.dp:
        t = t[:-1]
    return sgn + t
def ParseCommandLine(d):
    d["-c"] = False     # Don't output in columns
    d["-d"] = 3         # Number of significant digits
    d["-i"] = False     # Force output to be integers
    d["-n"] = False     # Put all numbers on one line
    d["-o"] = False     # Sort the output from low to high
    d["-q"] = False     # Don't print the random numbers in the report
    d["-s"] = None      # Random number seed
    d["-V"] = False     # Same as -v but percentiles every 1%
    d["-v"] = False     # Show sample statistics & parameters
    d["discrete"] = False   # Flags a discrete distribution
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cd:hinoqs:vV")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "cinoqVv":
            d[o] = not d[o]
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise Exception()
                #sig.digits = d["-d"]
            except Exception:
                Error("'{}' is improper integer for -d option".format(a))
        elif o in ("-h",):
            Examples(d)
        elif o in ("-s",):
            d["-s"] = a
    if len(args) < 2:
        Usage(d)
    try:
        args[1] = int(round(eval(args[1]), 0))
    except Exception:
        Error("'{}' is improper integer expression for N".format(args[1]))
    if d["-s"]:
        random.seed(d["-s"])
    flt(0).n = d["-d"]
    if d["-c"] and d["-n"]:
        Error("-c and -n options can't be used together")
    if d["-V"]:
        d["-v"] = True
    return args
def GetParams(params, number, errmsg):
    '''Return a list of the number of needed parameters if len(params) <=
    number; missing parameters are returned as empty strings.  If there are
    too many parameters, print errmsg and exit.
    '''
    params = list(params)
    missing = number - len(params)
    if missing >= 0:
        params.extend([""]*missing)
        return params
    else:
        Error(errmsg)
class RV(object):
    'Base class of a random variable object.'
    def __init__(self, *params, **kw):
        # The derived classes will set the self.params attribute.
        self.n = n = kw.setdefault("n", 1)
        self.d = d = kw.setdefault("d", {})
        self.seed = d["-s"]
        if self.n <= 0 and not isinstance(self.n, int):
            raise ValueError("n must be an integer > 0")
        if not self.d or not isinstance(self.d, dict):
            raise ValueError("d must be a dictionary of options")
        self.check_parameters()
        self.report()
    def check_parameters(self):
        '''Check the parameters and set any missing ones to default
        values.'''
        raise Exception("Abstract base class")
    def get_numbers(self):
        'Return a list of n random variates.'
        raise Exception("Abstract base class")
    def report(self):
        '''Print a report to stdout for self.n numbers with the options
        given in the dictionary self.d.
        '''
        def F(x):
            if 0:   # Old method
                'Format the number with sig and a leading space if it is >= 0'
                if self.d["discrete"] or self.d["-i"]:
                    return str(x)
                else:
                    fmt = " {}" if x >= 0 else "{}"
                    return fmt.format(sig(x), self.d["-d"])
            else:   # New method with flt
                return str(x)
        if self.d["-v"]:
            print(self)
        nums = list(self.get_numbers(self.n))
        if self.d["-o"]:    # Sort the numbers
            nums.sort()
        if self.d["-i"]:    # Force output to be integers
            nums = [int(i) for i in nums]
        if not self.d["-q"]:    # If not quiet
            if self.d["-c"] or self.d["-n"]:
                end = "\n" if self.d["-c"] else " "
                for i in nums:
                    print(F(i), end=end)
                if end == " ":
                    print()
            else:
                for i in Columnize([F(i) for i in nums], horiz=True):
                    print(i)
        if self.d["-v"]:
            self.print_statistics(nums)
            self.print_percentiles(nums)
    def print_statistics(self, nums):
        n = len(nums)
        mean = sum(nums)/n
        var = sum([(i - mean)**2 for i in nums])/(n - 1)
        sdev = var**0.5
        if self.d["discrete"]:
            maximum, minimum = max(nums), min(nums)
            range = srange = maximum - minimum
        else:
            maximum, minimum = max(nums), min(nums)
            range = max(nums) - min(nums)
        # 0xb1 is the plus/minus symbol
        ci = range/(2*sdev)
        median = statistics.median(nums)
        try:
            mode = statistics.mode(nums)
        except statistics.StatisticsError:
            mode = "undefined"
        print(dedent(f'''
        Sample statistics:
            n      {n}
            mean   {mean}
            median {median}
            mode   {mode}
            sdev   {sdev}
            min    {minimum}
            max    {maximum}
            range  {range}   [±{ci} standard deviations]'''))
    def print_percentiles(self, nums):
        if len(nums) < 2:
            Error("Must have at least 2 elements for percentiles")
        s, seq = [], sorted(nums)
        print("    Percentiles:")
        for i in range(0, 101, 1 if d["-V"] else 5):
            y = Percentile(seq, i/100)
            s.append(f"{i:3d}  {y}")
        for i in Columnize(s, indent=" "*4):
            print(i)
class Normal(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Normal needs 2 parameters")
        super(Normal, self).__init__(*params, **kw)
    def check_parameters(self):
        mu, sigma = self.params
        try:
            self.mu = float(eval(mu))
        except Exception:
            if mu:
                Error("'{}' is not a valid mean".format(mu))
            else:
                self.mu = 0
        try:
            self.sigma = float(eval(sigma))
            if self.sigma < 0:
                raise Exception()
        except Exception:
            if sigma:
                Error("'{}' is not a valid standard deviation".format(sigma))
            else:
                self.sigma = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.gauss(self.mu, self.sigma)))
        return nums
    def __str__(self):
        return '''Normal distribution
    Mean = {0.mu}
    Standard deviation = {0.sigma}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Exponential(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 1, "Exponential needs 1 parameter")
        super(Exponential, self).__init__(*params, **kw)
    def check_parameters(self):
        mu = self.params[0]
        try:
            self.mu = float(eval(mu))
            if not self.mu:
                Error("Exponential parameter can't be 0")
        except Exception:
            if mu:
                Error("'{}' is not a valid mean".format(mu))
            else:
                self.mu = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.expovariate(self.mu)))
        return nums
    def __str__(self):
        return '''Exponential distribution
    mu = {0.mu}
    Number of points = {0.n}'''.format(self)
class Beta(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Beta needs 2 parameters")
        super(Beta, self).__init__(*params, **kw)
    def check_parameters(self):
        a, b = self.params
        try:
            self.a = float(eval(a))
            if self.a <= 0:
                Error("Parameter a must be > 0".format(a))
        except Exception:
            if a:
                Error("'{}' is not a valid a parameter".format(a))
            else:
                self.a = 1
        try:
            self.b = float(eval(b))
            if self.a <= 0:
                Error("Parameter b must be > 0".format(a))
        except Exception:
            if b:
                Error("'{}' is not a valid b parameter".format(b))
            else:
                self.b = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.betavariate(self.a, self.b)))
        return nums
    def __str__(self):
        return '''Beta distribution
    a = {0.a}
    b = {0.b}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Gamma(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Gamma needs 2 parameters")
        super(Gamma, self).__init__(*params, **kw)
    def check_parameters(self):
        a, b = self.params
        try:
            self.a = float(eval(a))
            if self.a <= 0:
                Error("Parameter a must be > 0".format(a))
        except Exception:
            if a:
                Error("'{}' is not a valid a parameter".format(a))
            else:
                self.a = 1
        try:
            self.b = float(eval(b))
            if self.a <= 0:
                Error("Parameter b must be > 0".format(a))
        except Exception:
            if b:
                Error("'{}' is not a valid b parameter".format(b))
            else:
                self.b = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.gammavariate(self.a, self.b)))
        return nums
    def __str__(self):
        return '''Gamma distribution
    a = {0.a}
    b = {0.b}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Binomial(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Binomial needs 2 parameters")
        self.d = kw.setdefault("d", {})
        self.d["discrete"] = True
        super(Binomial, self).__init__(*params, **kw)
    def check_parameters(self):
        p, m = self.params
        try:
            self.p = float(eval(p))
            if not (0 <= self.p <= 1):
                Error("Parameter p must be between 0 and 1 inclusive".format(p))
        except Exception:
            if p:
                Error("'{}' is not a valid a parameter".format(p))
            else:
                self.p = 0.5
        try:
            self.m = int(eval(m))
            if self.m < 1:
                Error("Parameter m must be an integer > 0".format(m))
        except Exception:
            if m:
                Error("'{}' is not a valid integer".format(m))
            else:
                self.m = 1
    def get_numbers(self, n):
        # http://heather.cs.ucdavis.edu/~matloff/SimCourse/PLN/RandNumGen.pdf
        nums = []
        for i in range(n):
            count = 0
            for j in range(self.m):
                u = random.random()
                if u < self.p:
                    count += 1
            nums.append(count)
        return nums
    def __str__(self):
        return '''Binomial distribution
    p = {0.p} (fraction of population with characteristic)
    m = {0.m} (number of items in sample drawn with replacement)
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Poisson(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 1, "Poisson needs 1 parameter")
        self.d = kw.setdefault("d", {})
        self.d["discrete"] = True
        super(Poisson, self).__init__(*params, **kw)
    def check_parameters(self):
        mu = self.params[0]
        try:
            self.mu = float(eval(mu))
            if self.mu <= 0:
                Error("Parameter mu must be > 0".format(mu))
        except Exception:
            if mu:
                Error("'{}' is not a valid a parameter".format(mu))
            else:
                self.mu = 1
    def get_numbers(self, n):
        # http://heather.cs.ucdavis.edu/~matloff/SimCourse/PLN/RandNumGen.pdf
        nums = []
        for i in range(n):
            count, sum = 0, 0
            while True:
                count += 1
                sum += random.expovariate(self.mu)
                if sum > 1:
                    break
            nums.append(count - 1)
        return nums
    def __str__(self):
        return '''Poisson distribution
    mu = {0.mu} (single event exponential distribution parameter)
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Lognormal(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Lognormal needs 2 parameters")
        super(Lognormal, self).__init__(*params, **kw)
    def check_parameters(self):
        mu, sigma = self.params
        try:
            self.mu = float(eval(mu))
        except Exception:
            if mu:
                Error("'{}' is not a valid mu".format(mu))
            else:
                self.mu = 0
        try:
            self.sigma = float(eval(sigma))
            if self.sigma < 0:
                raise Exception()
        except Exception:
            if sigma:
                Error("'{}' is not a valid sigma".format(sigma))
            else:
                self.sigma = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.lognormvariate(self.mu, self.sigma)))
        return nums
    def __str__(self):
        return '''Lognormal distribution
    mu = {0.mu}
    sigma = {0.sigma}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Pareto(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 1, "Pareto needs 1 parameter")
        super(Pareto, self).__init__(*params, **kw)
    def check_parameters(self):
        alpha = self.params[0]
        try:
            self.alpha = float(eval(alpha))
        except Exception:
            if alpha:
                Error("'{}' is not a valid alpha".format(alpha))
            else:
                self.alpha = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.paretovariate(self.alpha)))
        return nums
    def __str__(self):
        return '''Pareto distribution
    alpha = {0.alpha}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Rand(RV):
    def __init__(self, *params, **kw):
        super(Rand, self).__init__(*params, **kw)
    def check_parameters(self):
        return
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.random()))
        return nums
    def __str__(self):
        return '''Rand distribution (uniform on [0, 1))
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Triangular(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 3, "Triangular needs 3 parameters")
        super(Triangular, self).__init__(*params, **kw)
    def check_parameters(self):
        low, high, infl = self.params
        try:
            self.low = float(eval(low))
        except Exception:
            if low:
                Error("'{}' is not a valid low".format(low))
            else:
                self.low = 0
        try:
            self.high = float(eval(high))
        except Exception:
            if high:
                Error("'{}' is not a valid high".format(high))
            else:
                self.high = 1
        try:
            self.infl = float(eval(infl))
        except Exception:
            if infl:
                Error("'{}' is not a valid infl".format(infl))
            else:
                self.infl = (self.low + self.high)/2
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.triangular(self.low, self.high, self.infl)))
        return nums
    def __str__(self):
        return '''Triangular distribution
    low = {0.low}
    high = {0.high}
    infl = {0.infl}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Uint(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Uint needs 2 parameters")
        self.d = kw.setdefault("d", {})
        self.d["discrete"] = True
        super(Uint, self).__init__(*params, **kw)
    def check_parameters(self):
        a, b = self.params
        try:
            self.a = int(eval(a))
        except Exception:
            if a:
                Error("'{}' is not a valid a".format(a))
            else:
                self.a = 0
        try:
            self.b = int(eval(b))
        except Exception:
            if b:
                Error("'{}' is not a valid b".format(b))
            else:
                self.b = self.a + 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.randint(self.a, self.b)))
        return nums
    def __str__(self):
        return '''Uniform distribution
    a = {0.a}
    b = {0.b}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Uniform(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Uniform needs 2 parameters")
        super(Uniform, self).__init__(*params, **kw)
    def check_parameters(self):
        a, b = self.params
        try:
            self.a = float(eval(a))
        except Exception:
            if a:
                Error("'{}' is not a valid a".format(a))
            else:
                self.a = 0
        try:
            self.b = float(eval(b))
        except Exception:
            if b:
                Error("'{}' is not a valid b".format(b))
            else:
                self.b = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.uniform(self.a, self.b)))
        return nums
    def __str__(self):
        return '''Uniform distribution
    a = {0.a}
    b = {0.b}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
class Weibull(RV):
    def __init__(self, *params, **kw):
        self.params = GetParams(params, 2, "Weibull needs 2 parameters")
        super(Weibull, self).__init__(*params, **kw)
    def check_parameters(self):
        alpha, beta = self.params
        try:
            self.alpha = float(eval(alpha))
        except Exception:
            if alpha:
                Error("'{}' is not a valid alpha".format(alpha))
            else:
                self.alpha = 0
        try:
            self.beta = float(eval(beta))
        except Exception:
            if beta:
                Error("'{}' is not a valid b".format(beta))
            else:
                self.beta = 1
    def get_numbers(self, n):
        nums = []
        for i in range(n):
            nums.append(flt(random.weibullvariate(self.alpha, self.beta)))
        return nums
    def __str__(self):
        return '''Weibull distribution
    alpha = {0.alpha}
    beta = {0.beta}
    Seed = {0.seed}
    Number of points = {0.n}'''.format(self)
def Shuffle(params, n=None, d=None):
    if len(params) not in (0, 1):
        Error("Shuffle needs one or two parameters")
    try:
        N = int(n)
    except Exception:
        Error("'{}' for N is not an integer".format(n))
    if N < 1:
        Error("N must be > 0")
    if len(params) == 1:
        try:
            M = int(params[0])
        except Exception:
            Error("'{}' for M is not an integer".format(params[0]))
        if M < 1:
            Error("M must be > 0")
        if M < N:
            N, M = M, N
    else:
        N, M = 1, N
    s = list(range(N, M + 1))
    random.shuffle(s)
    if d["-o"]:
        s = sorted(s)
    for i in Columnize([str(j) for j in s]):
        print(i)
    if d["-v"]:
        print("Seed =", d["-s"])
def Sample(params, n=None, d=None):
    if len(params) != 1:
        Error("Sample needs two parameters")
    m = params[0]
    try:
        N = int(n)
        if N < 1:
            Error("N must be > 0")
    except Exception:
        Error("{} is not an integer".format(n))
    try:
        m = int(m)
        if m < 1 or m > N:
            Error("m must be between 1 and {}".format(N))
    except Exception:
        Error("{} is not an integer".format(n))
    s = list(range(1, N + 1))
    random.shuffle(s)
    s = s[:m]
    if d["-o"]:
        s = sorted(s)
    for i in Columnize([str(j) for j in s]):
        print(i)
    if d["-v"]:
        print("Seed =", d["-s"])
def SampleWithReplacement(params, n=None, d=None):
    if len(params) != 1:
        Error("bsample needs two parameters")
    m = params[0]
    try:
        N = int(n)
        if N < 1:
            Error("N must be > 0")
    except Exception:
        Error("{} is not an integer".format(n))
    try:
        m = int(m)
        if m < 1 or m > N:
            Error("m must be between 1 and {}".format(N))
    except Exception:
        Error("{} is not an integer".format(n))
    s = range(1, N + 1)
    t = random.choices(s, k=m)
    if d["-o"]:
        t = sorted(t)
    if d["-n"]:
        print(' '.join([str(i) for i in t]))
    else:
        for i in Columnize([str(j) for j in t]):
            print(i)
    if d["-v"]:
        print("Seed =", d["-s"])
def Process(dist, args, d):
    '''Generate the random numbers to stdout.  
 
    dist    Abbreviation for the distribution.  
    args    Sequence of the command line arguments.
    d       Dictionary of options.
    '''
    s = dist.lower().strip()
    n, params = args[0], args[1:]
    if s.startswith("n"):
        Normal(*params, n=n, d=d)
    elif s.startswith("bi"):
        Binomial(*params, n=n, d=d)
    elif s.startswith("be"):
        Beta(*params, n=n, d=d)
    elif s.startswith("bs"):
        SampleWithReplacement(params, n=n, d=d)
    elif s.startswith("e"):
        Exponential(*params, n=n, d=d)
    elif s.startswith("g"):
        Gamma(*params, n=n, d=d)
    elif s.startswith("l"):
        Lognormal(*params, n=n, d=d)
    elif s.startswith("pa"):
        Pareto(*params, n=n, d=d)
    elif s.startswith("po"):
        Poisson(*params, n=n, d=d)
    elif s.startswith("r"):
        Rand(*params, n=n, d=d)
    elif s.startswith("sa"):
        Sample(params, n=n, d=d)
    elif s.startswith("sh"):
        Shuffle(params, n=n, d=d)
    elif s.startswith("t"):
        Triangular(*params, n=n, d=d)
    elif s.startswith("un"):
        Uniform(*params, n=n, d=d)
    elif s.startswith("ui"):
        Uint(*params, n=n, d=d)
    elif s.startswith("w"):
        Weibull(*params, n=n, d=d)
    else:
        Error(f"'{dist}' is not a recognized distribution")
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    Process(args[0], args[1:], d)
