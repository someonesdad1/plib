'''
Time-related tools to:
    - Measure elapsed times (Timer or Stopwatch class)
        - Timing in your software like a stopwatch
        - Act as a context manager
        - Function decorator to measure the time it takes for a function to complete
    - Get a file name with a time in it (FNTime class)
    - Convert a time in seconds to minutes, hr, day, weeks, months, years (GetET())

Timing events in code (not thread-safe)
    Use a Timer instance:
        t = Timer()
        t.start     # Starts the timer running and resets it to 0 s
            <do stuff>
        t.stop      # Stop timer running and retain state
        elapsed_time_in_seconds = t.et  # Elapsed time in s from t.start, a flt
            # Do stuff not related to what you're timing
        t.cont      # Resume running of the timer
            <do more stuff>
        t.stop
        cumulative_elapsed_time_in_seconds = t.et   # A flt
    Use Timer as a context manager:
        with Timer() as t:
            <do stuff>
        elapsed_time_in_seconds = t.et
    Use Timer as a function decorator
        @Timer()
        def myfunc():
            <do stuff>
        This will cause an elapsed time to be printed to stdout after the function exits.
    Use a stopwatch
        sw = Stopwatch()
            <do stuff>
        t = sw()    # How many seconds (a flt) have elapsed since starting
        sw.reset()  # Start the timer over again

File name with a time in it (FNTime class)
    t = timer.FNTime()
    print(t()) --> '20250308_163445.960344'
    print(t(short=True)) --> '8Mar'

GetET():  convert a time in s to a familiar unit
                                        Returns
    GetET(86399)                        '24 hr'
    GetET(86399 + 1)                    '1 day' (86400 s is 24 hours == 1 day)
    GetET(time.time(), units="yr")      '54.1 years'
'''
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> Provides objects that help with program timing.  Run as
    # a script to see example output.
    ##∞what∞#
    ##∞test∞# ignore #∞test∞#
    # Standard imports
    from decimal import Decimal
    from fractions import Fraction
    import datetime
    import time
    import decimal
    from textwrap import dedent
    from pdb import set_trace as xx
    # Custom imports
    from f import flt
    from u import u
    try:
        import mpmath
        have_mpmath = True
    except ImportError:
        have_mpmath = False
    # Global variables
    ii = isinstance
    __all__ = "Stopwatch Timer FNTime GetET timer fnt sw".split()
if 1:  # Classes
    class Timer(object):
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
            # The timer has the following states in self.state:
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
                self.start
                retval = func(*args, **kw)
                self.stop
                print(f"{str(func)} time = {self.et.engsi}s")
                return retval
            return f
        # Context manager functionality
        def __enter__(self):
            self.start
            return self
        def __exit__(self, exc_type, exc_value, exc_tb):
            self.stop
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
            T = zip(self._stop, self._start)
            t = [stop - start for stop, start in T]
            assert all(i >= 0 for i in t)
            # Sum the interval durations (a Decimal result)
            return sum(t)
        @property
        def et(self):
            'Returns elapsed time in s as a flt'
            return flt(self.ET)
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
    class Stopwatch(object):
        '''Timer that returns a flt of the elapsed time in seconds from when it was started.
        Example usage:
            sw = Stopwatch()
            ...
            t = sw()    # How many seconds (a flt) have elapsed since starting
            sw.reset()  # Start the timer over again
        '''
        def __init__(self):
            self.timer = Timer()
            self.reset()
        def __call__(self):
            "Returns the elapsed time in s as a flt"
            return self.timer.et
        def reset(self):
            "Start the timer over; handy so an instance can be reused"
            self.timer.start
    class FNTime(object):
        def __init__(self):
            pass
        def __call__(self, short=False):
            '''Return a string containing the time now that is suitable
            for a filename.  The string will contain the time to the
            nearest microsecond, so will almost certainly be unique but
            long.  Set short to True to get a short string like '5Jun'.
            '''
            d = datetime.datetime.now()
            if short:
                from months import months
                m = months[d.month]
                s = f"{d.day}{months[d.month]}"
            else:
                s = (
                    f"{d.year:04d}{d.month:02d}{d.day:02d}_"
                    f"{d.hour:02d}{d.minute:02d}{d.second:02d}."
                    f"{d.microsecond:06d}"
                )
            return s
if 1:  # Functions
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
        if have_mpmath:
            if not ii(seconds, (int, float, Fraction, Decimal, mpmath.mpf)):
                raise TypeError(
                    "seconds must be int, float, Fraction, Decimal, mpmath.mpf"
                )
        else:
            if not ii(seconds, (int, float, Fraction, Decimal)):
                raise TypeError("seconds must be int, float, Fraction, Decimal")
        # Convert to a float
        sign = -1 if seconds < 0 else 1
        seconds = abs(flt(seconds))
        with seconds:
            seconds.N = digits
            factor = u(units) if units else 1
            if abs(seconds) < 1:
                if units:
                    return f"{(sign * factor / seconds).engsi}{units}"
                else:
                    return f"{sign * seconds.engsi}s"
            if units:
                return f"{(seconds / factor).engsi}{units}"
            else:
                if seconds < u("minute"):
                    return f"{sign * seconds} s"
                elif seconds < u("hr"):
                    return f"{sign * seconds / u('minutes')} min"
                elif seconds < u("day"):
                    return f"{sign * seconds / u('hours')} hr"
                elif seconds < u("week"):
                    return f"{sign * seconds / u('days')} day"
                elif seconds < u("month"):
                    return f"{sign * seconds / u('weeks')} wk"
                elif seconds < u("year"):
                    return f"{sign * seconds / u('months')} mo"
                elif seconds < u("century"):
                    return f"{sign * seconds / u('years')} yr"
                elif seconds < u("millenia"):
                    return f"{sign * seconds / u('centuries')} century"
                else:
                    x = seconds / u("millenia")
                    if x <= 1e4:
                        return f"{sign * seconds / u('millenia')} millenia"
                    else:
                        return f"{(sign * seconds / u('millenia')).sci} millenia"
    def AdjustTimeUnits(seconds, digits=3, un=False):
        '''Convert a time in seconds to an easier to understand string.  If seconds is < 1, then
        the returned string will be in s with an SI prefix.  If seconds is > 1, then it will be
        converted to one of the larger time units:
            minutes hours days weeks months years
        If un is true, use scientific notation instead (helpful for big SI prefixes you can't
        remember).
        '''
        def P(time, units, un):
            return f"{s.engsi}{units} = {s.sci} {units}" if un else f"{s.engsi}{units}"
        x = flt(0)
        with x:
            x.N = digits
            x.u = un
            if seconds < 1:
                s = flt(seconds)
                return f"{s.engsi}s"
            else:
                if seconds / u("years") >= 1:
                    s = flt(seconds / u("years"))
                    return P(s, "years", un=un)
                elif seconds / u("months") >= 1:
                    s = flt(seconds / u("months"))
                    return P(s, "months", un=un)
                elif seconds / u("weeks") >= 1:
                    s = flt(seconds / u("weeks"))
                    return P(s, "weeks", un=un)
                elif seconds / u("days") >= 1:
                    s = flt(seconds / u("days"))
                    return P(s, "days", un=un)
                elif seconds / u("hours") >= 1:
                    s = flt(seconds / u("hours"))
                    return P(s, "hours", un=un)
                elif seconds / u("minutes") >= 1:
                    s = flt(seconds / u("minutes"))
                    return P(s, "minutes", un=un)
                else:
                    s = flt(seconds)
                    return P(s, "seconds", un=un)
if 1:  # Convenience instances
    timer = Timer()
    fnt = FNTime()
    sw = Stopwatch()
if __name__ == "__main__":
    import re
    from fmt import fmt
    from color import t as C
    from f import sqrt
    from lwtest import run, Assert
    from textwrap import dedent
    n = 100
    def stats(seq):
        "Return (mean, stddev) for sequence of Decimal numbers"
        n = len(seq)
        mean = sum(seq) / n
        deviations = [(i - mean) ** 2 for i in seq]
        variance = sum(deviations) / (n - 1)
        return mean, sqrt(variance)
    # The functions are named with leading letters to control the
    # execution order because lwtest.run() alphabetizes the names.
    def A_Timer1_example():
        title = "Timer using seconds"
        units, multiplier = "s", 1
        t = Timer()
        t.u = multiplier
        print(title)
        print(f"  t.start = {t.start} {units}")
        for i in range(n):
            pass
        print(f"  t.stop  = {t.stop} {units}")
        print(f"  elapsed = {t.et} {units}")
    def B_Timer2_example():
        title = "Timer using μs"
        units, multiplier = "μs", 1e6
        t = Timer()
        t.u = multiplier
        print(title)
        print(f"  t.start = {t.start} {units}")
        for i in range(n):
            pass
        print(f"  t.stop  = {t.stop} {units}")
        print(f"  elapsed = {t.et} {units}")
    def C_Timer_with_sleep_example():
        "Timer that shows time.sleep() time is counted too"
        t = Timer()
        t.start
        time.sleep(1)
        t.stop
        print(f"Time with 1 s sleep = {t.et} s")
    def D_Context_manager_example():
        "Time a loop a bunch of times"
        print("Context manager use:")
        r, m = [], 1e5
        for i in range(n):
            with Timer() as t:
                for i in range(int(m)):
                    pass
            r.append(t.et)
        mean, sdev = stats(r)
        print(f"  Repeated {int(n * m)} times")
        rsd = 100 * sdev / mean
        print(f"  relative std dev = {fmt(rsd)}%")
    def E_Timer_decorator_example():
        print("Using Timer as a decorator:")
        @Timer()
        def Demo():
            for i in range(n):
                time.sleep(0.001)
        Demo()
    def F_min_resolution_example():
        "Estimate the minimum timer resolution"
        r, n, D = [], int(1e5), decimal.Decimal
        to_ns = D(1e9)
        for i in range(n):
            t1, t2 = Timer.ns(), Timer.ns()
            r.append(D(t2 - t1) / to_ns)
        mean, sdev = stats(r)
        print(f"Estimate of time.perf_counter_ns practical resolution:")
        print(f"  Sample size = {n}")
        print(f"  Mean = {fmt(mean * to_ns, n=2)} ns")
        print(f"  Std dev = {fmt(sdev * to_ns, n=2)} ns")
        print(f"  Relative std dev = {fmt(100 * sdev / mean, n=2)}%")
    def G_accumulation_example():
        print("Show accumulation of intervals works")
        t, st, n = Timer(), 0.05, 5
        t.start
        t.stop
        # Remove this small offset
        t._stop[0] = t._start[0]
        for i in range(n):
            t.cont
            time.sleep(st)  # Count this one
            t.stop
            time.sleep(2 * st)  # Don't count this one
        print(f"  Expected elapsed time = {n * st} s")
        print(f"  Actual elapsed time   = {t.et} s")
    def H_Discuss_example():
        N = decimal.getcontext().prec
        t1, t2 = Timer.ns(), Timer.ns()
        print("\nDiscussion:\n")
        print(dedent(f'''
        Timer objects use Decimal numbers to keep track of time.  The default Decimal context uses
        {N} significant figures, so you will see numerous meaningless figures in typical output. 
        
        Timing is done using the time.perf_counter_ns function.  Two sequential calls to this
        resulted in the times {t1} and {t2}.  Their difference is {t2 - t1} ns,
        which will be different each time you try it.
        
        Timing things on computers with software has been notoriously poor over the decades and
        you need to be aware of the pitfalls.  If my memory serves, trying to get decent timing on
        early MSDOS systems was tough because clock resolutions were on the order of a second or
        so.  UNIX systems in the 1980's might have had resolutions of an order of magnitude or two
        better, but still pretty crummy.  Things are also more problematic on operating systems
        that can suspend your process, which means almost everything you'd use today.
        
        Python will use tools available to it from the operating system, so your results will
        depend on your hardware and software.  The best advice is to be aware of the many sources
        of timing variability and use multiple measurements to estimate the mean and the spread in
        the results.
        
        When you get the elapsed time of a Timer object (et attribute), it will be a flt instance
        from f.py.  This will cause the elapsed time to be printed to 3 digits, the default.
        Change Timer.et.N to a larger number for more digits.
 
        The Stopwatch class is a convenience for routine timing tasks in a script.  You can use
        the timer.sw convenience instance by starting it with sw.reset(), but be aware that it is
        not thread-safe.  It's handy because the returned type of flt means you don't see a lot of
        useless digits.
 
        The GetET function will return the argument in seconds in a time unit that is easier to
        interpret:
                                                Returns
            GetET(86399)                        '24 hr'
            GetET(86399 + 1)                    '1 day'
            GetET(time.time(), units="yr")      '54.1 years'
        '''[1:].rstrip()))
    if 1:  # Run self tests
        def Test():
            s = GetET(2e-9)
            Assert(s == "2 ns")
            s = GetET(0.1)
            Assert(s == "100 ms")
            s = GetET(50)
            Assert(s == "50 s")
            s = GetET(u("minute"))
            Assert(s == "1 min")
            s = GetET(u("hr"))
            Assert(s == "1 hr")
            s = GetET(u("day"))
            Assert(s == "1 day")
            s = GetET(u("week"))
            Assert(s == "1 wk")
            s = GetET(u("month"))
            Assert(s == "1 mo")
            s = GetET(u("yr"))
            Assert(s == "1 yr")
            s = GetET(u("century"))
            Assert(s == "1 century")
            s = GetET(u("millenia"))
            Assert(s == "1 millenia")
            # AdjustTimeUnits()
            for un in "years months weeks days hours minutes".split():
                Assert(AdjustTimeUnits(1 * u(un)) == f"1 {un}")
        retvalue, s = run(globals(), quiet=True, halt=False)
        if retvalue:
            C.print(f"{C.ornl}Self tests failed")
            print(s.strip())
            exit(1)
        else:
            C.print(f"{C.grnl}Tests passed")
    # Run a demo
    with Timer() as T:
        run(globals(), regexp="example$")
    print(f"Total time for examples = {fmt(T.et, n=2)} s")
