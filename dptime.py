'''
This is a module with functions to return the date and time as I like to see them 
and handy time formatting stuff.
'''
if 1:  # Header
    if 1:  # Standard imports
        import datetime
        import decimal
        import fractions
        import time
    if 1:  # Custom imports
        import dptypes
        import f
        import u
        if 0:
            import debug
            debug.SetDebugger()
        try:
            import mpmath
            _have_mpmath = True
        except ImportError:
            _have_mpmath = False
    if 1:  # Global variables
        # Bi-directional mappings between month number and 3-letter string name
        Num2Month = dptypes.Bidict({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})
        # The following uses upper case letters
        Num2Month_uc = dptypes.Bidict({1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN",
                7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"})
        # The following uses lower case letters
        Num2Month_lc = dptypes.Bidict({1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
                7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec" })
        Month2Num = Num2Month.invert()
        Month2Num_lc = Num2Month_lc.invert()
        Month2Num_uc = Num2Month_uc.invert()
if 1:  # Functions
    def dpdate():
        "Return the date in a format like '1 Jan 2025'"
        s = time.strftime("%d %b %Y")
        if s[0] == "0":
            s = s[1:]
        return s
    def dptime():
        "Return the time in a format like '7:14:16 am'"
        ampm = time.strftime("%p").lower()
        s = time.strftime(f"%I:%M:%S {ampm}")
        if s[0] == "0":
            s = s[1:]
        return s
    def dpdatetime():
        return dpdate() + " " + dptime()
    def NiceET(seconds, digits=4):
        '''Return an elapsed time in seconds in friendly units so that scientific 
        display is not needed.  The used units will be ns, μs, ms, s, min, hr, day,
        month, yr.  Longer intervals will be in yr with an SI prefix.
        '''
        sec = f.flt(seconds)
        with sec:
            sec.N = digits
            if sec < 1:
                return f"{sec.engsi}s"
            elif sec < u.u("minute"):
                return f"{sec} s"
            elif sec < u.u("hour"):
                use = "min"
                return f"{sec/u.u(use)} {use}"
            elif sec < u.u("day"):
                use = "hr"
                return f"{sec/u.u(use)} {use}"
            elif sec < u.u("month"):
                use = "days"
                return f"{sec/u.u(use)} {use}"
            elif sec < u.u("year"):
                use = "months"
                return f"{sec/u.u(use)} {use}"
            else:
                use = "yr"
                y = sec/u.u(use)
                if y < 1000:
                    return f"{y} {use}"
                else:
                    return f"{y.engsi}{use}"
    def Time():
        'Returns the current time in the following format: "7Jun2021 7:24 am Mon"'
        t, f = time.localtime(), lambda x: x[1:] if x[0] == "0" else x
        day = f(time.strftime("%a", t))
        date = f(time.strftime("%d%b%Y", t))
        clock = f(time.strftime("%I:%M", t))
        ampm = time.strftime("%p", t).lower()
        return ' '.join((date, clock, ampm, day))
    def GetET(seconds, units="", digits=3, eng=False):
        '''Return a string with the elapsed time in seconds given in familiar units.  Examples:
                                                Returns
            GetET(86399)                        '24 hr'
            GetET(86399 + 1)                    '1 day'
            GetET(time.time(), units="yr")      '54.1 years'
            
        The last example is the current time since 1 Jan 1970 and will depend on the time it's
        run.
        
        If you pass the units keyword, that will be used.  You can specify the number of digits in
        the output.  If eng is given, then engineering format will be used with either seconds or
        the units you specified.
        
        If units is None, then appropriate units will be chosen.  For seconds less than 1, ms, us,
        etc. will be used.  For seconds greater than 1, minutes, hours, days, weeks, months,
        years, centuries, and millenia will be used.
        '''
        # seconds must be an integer, float, Fraction, Decimal, or mpmath.mpf
        if _have_mpmath:
            if not isinstance(seconds, (int, float, fractions.Fraction, decimal.Decimal, mpmath.mpf)):
                raise TypeError(
                    "seconds must be int, float, Fraction, Decimal, mpmath.mpf"
                )
        else:
            if not isinstance(seconds, (int, float, fractions.Fraction, decimal.Decimal)):
                raise TypeError("seconds must be int, float, Fraction, Decimal")
        # Convert to a float
        sign = -1 if seconds < 0 else 1
        seconds = abs(f.flt(seconds))
        with seconds:
            seconds.N = digits
            factor = u.u(units) if units else 1
            if abs(seconds) < 1:
                if units:
                    return f"{(sign * factor / seconds).engsi}{units}"
                else:
                    return f"{sign * seconds.engsi}s"
            if units:
                return f"{(seconds / factor).engsi}{units}"
            else:
                if seconds < u.u("minute"):
                    return f"{sign * seconds} s"
                elif seconds < u.u("hr"):
                    return f"{sign * seconds / u.u('minutes')} min"
                elif seconds < u.u("day"):
                    return f"{sign * seconds / u.u('hours')} hr"
                elif seconds < u.u("week"):
                    return f"{sign * seconds / u.u('days')} day"
                elif seconds < u.u("month"):
                    return f"{sign * seconds / u.u('weeks')} wk"
                elif seconds < u.u("year"):
                    return f"{sign * seconds / u.u('months')} mo"
                elif seconds < u.u("century"):
                    return f"{sign * seconds / u.u('years')} yr"
                elif seconds < u.u("millenia"):
                    return f"{sign * seconds / u.u('centuries')} century"
                else:
                    x = seconds / u.u("millenia")
                    if x <= 1e4:
                        return f"{sign * seconds / u.u('millenia')} millenia"
                    else:
                        return f"{(sign * seconds / u.u('millenia')).sci} millenia"
    def AdjustTimeUnits(seconds, digits=3, sci=False):
        '''Convert a time in seconds to an easier to understand string.  If seconds is
        less than 1, then the returned string will be in s with an SI prefix.  If
        seconds is > 1, then it will be converted to one of the larger time units:
            minutes hours days weeks months years
        If sci is true, use scientific notation instead (helpful for big SI prefixes you can't
        remember).
        '''
        def P(time, units, sci):
            return f"{s.engsi}{units} = {s.sci} {units}" if sci else f"{s.engsi}{units}"
        x = f.flt(0)
        with x:
            x.N = digits
            x.u = sci
            if seconds < 1:
                s = f.flt(seconds)
                return f"{s.engsi}s"
            else:
                if seconds / u.u("years") >= 1:
                    s = f.flt(seconds / u.u("years"))
                    return P(s, "years", sci=sci)
                elif seconds / u.u("months") >= 1:
                    s = f.flt(seconds / u.u("months"))
                    return P(s, "months", sci=sci)
                elif seconds / u.u("weeks") >= 1:
                    s = f.flt(seconds / u.u("weeks"))
                    return P(s, "weeks", sci=sci)
                elif seconds / u.u("days") >= 1:
                    s = f.flt(seconds / u.u("days"))
                    return P(s, "days", sci=sci)
                elif seconds / u.u("hours") >= 1:
                    s = f.flt(seconds / u.u("hours"))
                    return P(s, "hours", sci=sci)
                elif seconds / u.u("minutes") >= 1:
                    s = f.flt(seconds / u.u("minutes"))
                    return P(s, "minutes", sci=sci)
                else:
                    s = f.flt(seconds)
                    return P(s, "seconds", sci=sci)
    def DaysPerMonth(month, leap_year=False):
        days_per_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31}
        if isinstance(month, str):
            n = Num2Month_lc(month[:3].lower())
        elif isinstance(month, int):
            n = month
        return days_per_month[n] + bool(leap_year)
    def GetDate(s):
        'Return a date.Date object given the string s in the form 11Feb2023'
        u = s.replace(" ", "")
        u = "0" + u if len(u) == 8 else u
        day = int(u[:2])
        month = Month2Num_lc(u[2:5].lower())
        year = int(u[5:])
        return datetime.date(year, month, day)
if 1:  # Timer stuff
    class Timer:
        '''Use an instance of this object to time events in code.  Note this design is inherently
        not thread-safe.  Usage patterns:
        
        Object:
            t = Timer()
            t.start     # Starts/resets the timer
            ...do stuff...
            t.stop      # Turn timer off but retain state
            elapsed_time_in_seconds = t.et  # Elapsed time from t.start, a flt
            # Do stuff not related to what you're timing
            t.cont      # Continue timing
            ...do more stuff...
            t.stop
            cumulative_elapsed_time_in_seconds = t.et   # A flt
        Context manager:
            with Timer() as t:
                <do stuff>
            elapsed_time_in_seconds = t.et
            
        Decorator:
            @Timer()
            def myfunc():
                <do stuff>
                
            This will cause an elapsed time to be printed to stdout after the function exits.
            
        The u attribute is set to 1 to indicate time units of 1 second.  Set it to a different
        value to change the default time units.  Example: set u to 1000 to set the time units to
        ms.
        
        Internally, a Decimal instance is used so that long times don't have resolution problems.
        For convenience, the elapsed time property returns a flt so that you don't have to see a
        large number of floating point digits.
        
        The lists _start and _stop are used internally to keep track of start and stop times in
        Decimals.  These lists aren't exposed by the interface, but if you need them they provide
        a record of when the timer was started and stopped.
        
        Ideas from
            https://realpython.com/python-timer/
            https://realpython.com/python-with-statement/#measuring-execution-time
        '''
        # The following function returns time in ns and avoids resolution
        # problems of floating point numbers.
        ns = time.perf_counter_ns
        def __init__(self):
            self.clear()
            self._u = decimal.Decimal(1)
            # The timer has the following states in self._state:
            #   "init"  Waiting to be started
            #   "run"   Start has been called
            #   "stop"  Stop was called; can be continued
        def clear(self):
            'Set the timer to the initialized state'
            self._start, self._stop = [], []
            self._state = "init"
        # Decorator functionality
        def __call__(self, func):
            'Return execution time in engineering notation for seconds'
            def f(*args, **kw):
                self.start  # noqa
                retval = func(*args, **kw)
                self.stop   # noqa
                print(f"{str(func)} time = {self.et.engsi}s")
                return retval
            return f
        # Context manager functionality
        def __enter__(self):
            self.start  # noqa
            return self
        def __exit__(self, exc_type, exc_value, exc_tb):
            self.stop   # noqa
        # Properties
        @property
        def cont(self):
            'Continue a stopped timer and return the time in s of continuation'
            if self._state != "stop":
                raise ValueError("Timer is not stopped")
            t = self.time
            self._start.append(t)
            self._state = "run"
        @property
        def ET(self):
            'Returns elapsed time in s as a Decimal'
            if self._state != "stop":
                raise ValueError("Timer not stopped")
            # Check the invariants
            n = len(self._start)
            assert len(self._stop) == n
            if not n:
                raise ValueError("No accumulated data")
            # Calculate elapsed time by subtracting stop/start times.  self._start and self._stop
            # are lists of start and stop times as Decimal instances.
            T = zip(self._stop, self._start, strict=True)
            t = [stop - start for stop, start in T]
            assert all(i >= 0 for i in t)
            # Sum the interval durations (a Decimal result)
            return sum(t)
        @property
        def et(self):
            'Returns elapsed time in s as a flt'
            return f.flt(self.ET)
        @property
        def start(self):
            'Resets timer and returns start time in s'
            self.clear()
            t = self.time
            # Update list of start times
            self._start.append(t)
            self._state = "run"
            return t
        @property
        def stop(self):
            'Returns stop time in s'
            if self._state != "run":
                raise ValueError("Timer not running")
            t = self.time
            # Update list of start times
            self._stop.append(t)
            self._state = "stop"
            return t
        @property
        def time(self):
            'Return current time as a Decimal in current time units'
            # By default, Decimal objects use 28 digits.  Since time.perf_counter_ns() returns an
            # integer number of ns, our nominal resolution is 1e28*1e-9 or 1e19 s which is over
            # 1e11 years, so there should be no resolution problems in timing code.
            # ns,
            return decimal.Decimal(Timer.ns())/decimal.Decimal("1e9")*self.u
        @property
        def u(self):
            'Set/return the time unit factor (1 = s, 1000 = ms, etc.)'
            return self._u
        @u.setter
        def u(self, value):
            'Set the default time unit (seconds is default)'
            if self._state != "init":
                raise ValueError("Use self.clear() before setting u")
            self._u = decimal.Decimal(value)
    class Stopwatch:
        '''Timer that returns a flt of the elapsed time in seconds from when it was started.
        Example usage:
            sw = Stopwatch()
            ...
            t = sw()    # How many seconds (a flt) have elapsed since starting
            sw.reset()  # Start the timer over again
        '''
        def __init__(self):
            self._start = None
            self.reset()
        def __call__(self):
            "Returns the elapsed time in s as a flt"
            return f.flt(time.time() - self._start)
        def reset(self):
            "Start the timer over; handy so an instance can be reused"
            self._start = time.time()
    class FilenameTime:
        def __init__(self):
            pass
        def __call__(self, short=False):
            '''Return a string containing the time now that is suitable for a filename.
            The string will contain the time to the nearest microsecond, so will almost
            certainly be unique but long.  Set short to True to get a short string like
            '5Jun'.  Examples:
                long form = 20260304_120549.115350
                short form = 4Mar
            '''
            d = datetime.datetime.now()
            if short:
                s = f"{d.day}{Num2Month[d.month]}"
            else:
                s = (
                    f"{d.year:04d}{d.month:02d}{d.day:02d}_"
                    f"{d.hour:02d}{d.minute:02d}{d.second:02d}."
                    f"{d.microsecond:06d}"
                )
            return s
if 1:  # ISO class:  gives current date and time in standard ISO format
    class ISO:
        def __init__(self, zulu=False, rm_zero=True):
            "Initialize with now.  If zulu is True, use GMT."
            self._tm = time.gmtime() if zulu else time.localtime()
            self._rm0 = rm_zero
        def __str__(self):
            return time.strftime("%Y%m%d-%H:%M:%S", self._tm)
        def set(self, tm):
            "Set to a new struct_time"
            if not isinstance(tm, time.struct_time):
                raise TypeError("tm must be a time.struct_time instance")
            self._tm = tm
        @property
        def date(self):
            '''This returns the date in the form I use the most; e.g.
            '12 Aug 2019'.
            '''
            s = time.strftime("%d %b %Y", self._tm)
            if self._rm0 and s[0] == "0":
                s = s[1:]
            return s
        @property
        def dt(self):
            return self.d + " " + self.t
        @property
        def d(self):
            s = time.strftime("%d %b %Y %a", self._tm)
            if self._rm0 and s[0] == "0":
                s = s[1:]
            return s
        @property
        def t(self):
            h = time.strftime("%I", self._tm)
            if h[0] == "0":
                h = h[1:]
            return h + time.strftime(":%M:%S %p", self._tm).lower()
if 1:  # Convenience class instances
    timer = Timer()
    fnt = FilenameTime()
    sw = Stopwatch()

if __name__ == "__main__":
    import lwtest
    Assert = lwtest.Assert
    def Test_GetET():
        s = GetET(2e-9)
        Assert(s == "2 ns")
        s = GetET(0.1)
        Assert(s == "100 ms")
        s = GetET(50)
        Assert(s == "50 s")
        s = GetET(u.u("minute"))
        Assert(s == "1 min")
        s = GetET(u.u("hr"))
        Assert(s == "1 hr")
        s = GetET(u.u("day"))
        Assert(s == "1 day")
        s = GetET(u.u("week"))
        Assert(s == "1 wk")
        s = GetET(u.u("month"))
        Assert(s == "1 mo")
        s = GetET(u.u("yr"))
        Assert(s == "1 yr")
        s = GetET(u.u("century"))
        Assert(s == "1 century")
        s = GetET(u.u("millenia"))
        Assert(s == "1 millenia")
    def Test_AdjustTimeUnits():
        for un in "years months weeks days hours minutes".split():
            Assert(AdjustTimeUnits(1 * u.u(un)) == f"1 {un}")
    exit(lwtest.run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

def GetGist():
    g = {}
    g["gist"] = "Time-related routines"
    g["copy"] = "Copyright © 2024 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "time"
    g["todo"] = '''
    
    -
    
    '''
    return g
