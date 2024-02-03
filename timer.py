'''
Todo
    - The timing tool of choice is probably time.perf_counter_ns()
        - You must subtract two calls to get a valid time
        - It includes sleep times
    - Add split() method to Timer.  Or let et() be allow to be called when
      running.

Time-related tools:
    Stopwatch class:  For elapsed times
    Timer class:  Tool that works as a context manager and decorator
    FNTime class:  Get a filename with a time in it
    BasicTime():  Display a time in s, minutes, hr, day, weeks, months, years
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Provides objects that help with program timing.  Run as
        # a script to see example output.
        #∞what∞#
        #∞test∞# ignore #∞test∞#
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
if 1:   # Classes 
    class Stopwatch(object):
        '''Timer that returns a flt of the elapsed time in seconds from
        when it was started.  Example usage:
            sw = Stopwatch()
            ...
            t = sw()    # How many seconds have elapsed since starting
            sw.reset()  # Start the timer over again
        The timer's resolution is ns because it uses time.perf_counter_ns()
        but resolution will be limited for long times because of the limited
        resolution of floats.
        '''
        def __init__(self):
            self.reset()
        def __call__(self):
            et = time.perf_counter_ns() - self.start
            return flt(et/1e9)
        def reset(self):
            'Start the timer over; handy so an instance can be reused'
            self.start = time.perf_counter_ns()
    class Timer(object):
        '''Use an instance of this object to time events in code.  
        Usage patterns are:
    
            Object:
                t = Timer()
                t.start
                ...do stuff...
                t.stop
                elapsed_time_in_seconds = t.et
                # Do stuff not related to what you're timing
                t.cont     # Continue timing
                ...do more stuff...
                t.stop
                cumulative_elapsed_time_in_seconds = t.et
            
            Context manager:
                with Timer() as t:
                    <do stuff>
                elapsed_time_in_seconds = t.et
        
            Decorator:
                @Timer()
                def myfunc():
                    <do stuff>
        
                This will cause an elapsed time to be printed to stdout after
                the function exits.
    
        The u attribute is set to 1 to indicate time units of 1 second.  Set 
        it to a different value to change the default time units.  Example:
        set u to 1000 to set the time units to ms.
 
        Ideas from
            https://realpython.com/python-timer/ and 
            https://realpython.com/python-with-statement/#measuring-execution-time
        '''
        # The following function returns time in ns and avoids resolution
        # problems of floating point numbers.
        ns = time.perf_counter_ns
        def __init__(self):
            self.clear()
            self._u = decimal.Decimal(1)
            # The timer has the following states:
            #   "init"  Waiting to be started
            #   "run"   Start has been called
            #   "stop"  Stop was called; can be continued
        def clear(self):
            'Set the timer to the initialized state'
            self._start, self._stop = [], []
            self._state = "init"
        # Decorator functionality
        def __call__(self, func):
            def f(*args, **kw):
                self.start
                func(*args, **kw)
                self.stop
                print(f"{str(func)} time = {self.et} s")
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
            'Continue a stopped timer.  Returns time of continuation.'
            if self._state != "stop":
                raise ValueError("Timer is not stopped")
            t = self.time
            self._start.append(t)
            self._state = "run"
        @property
        def et(self):
            'Returns elapsed time'
            if self._state != "stop":
                raise ValueError("Timer not stopped")
            # Check the invariants
            n = len(self._start)
            assert(len(self._stop) == n)
            if not n:
                raise ValueError("No accumulated data")
            # Calculate elapsed time by subtracting stop/start times
            T = zip(self._stop, self._start)
            t = [stop - start for stop, start in T]
            assert(all([i >= 0 for i in t]))
            return flt(sum(t))
        @property
        def start(self):
            'Starts timer and returns start time'
            self.clear()
            t = self.time
            self._start.append(t)
            self._state = "run"
            return t
        @property
        def stop(self):
            'Returns stop time'
            if self._state != "run":
                raise ValueError("Timer not running")
            t = self.time
            self._stop.append(t)
            self._state = "stop"
            return t
        @property
        def time(self):
            'Return current time in current time units'
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
                s = (f"{d.year:04d}{d.month:02d}{d.day:02d}_"
                    f"{d.hour:02d}{d.minute:02d}{d.second:02d}."
                    f"{d.microsecond:06d}")
            return s
if 1:   # Functions
    def BasicTime(seconds, units="", digits=3, eng=False):
        '''Return a string with the time given in familiar units.  If you
        pass the units keyword, that will be used.  You can specify the
        number of digits in the output.  If eng is given, then engineering
        format will be used with either seconds or the units you specified.
 
        If units is None, then appropriate units will be chosen.  For
        seconds less than 1, ms, us, etc. will be used.  For seconds
        greater than 1, minutes, hours, days, weeks, months, years,
        centuries, and millenia will be used.
        '''
        # seconds must be an integer, float, Fraction, Decimal, or
        # mpmath.mpf
        if have_mpmath:
            if not ii(seconds, (int, float, Fraction, Decimal, mpmath.mpf)): 
                raise TypeError("seconds must be int, float, Fraction, Decimal, mpmath.mpf")
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
                    return f"{(sign*factor/seconds).engsi}{units}"
                else:
                    return f"{sign*seconds.engsi}s"
            if units:
                return f"{(seconds/factor).engsi}{units}"
            else:
                if seconds < u("minute"):
                    return f"{sign*seconds} s"
                elif seconds < u("hr"):
                    return f"{sign*seconds/u('minutes')} min"
                elif seconds < u("day"):
                    return f"{sign*seconds/u('hours')} hr"
                elif seconds < u("week"):
                    return f"{sign*seconds/u('days')} day"
                elif seconds < u("month"):
                    return f"{sign*seconds/u('weeks')} wk"
                elif seconds < u("year"):
                    return f"{sign*seconds/u('months')} mo"
                elif seconds < u("decades"):
                    return f"{sign*seconds/u('years')} yr"
                elif seconds < u("century"):
                    return f"{sign*seconds/u('decades')} decade"
                elif seconds < u("millenia"):
                    return f"{sign*seconds/u('centuries')} century"
                else:
                    x = seconds/u('millenia')
                    if x <= 1e4:
                        return f"{sign*seconds/u('millenia')} millenia"
                    else:
                        return f"{(sign*seconds/u('millenia')).sci} millenia"
            
if 1:   # Convenience instances
    timer = Timer()
    fnt = FNTime()
    sw = Stopwatch()

if __name__ == "__main__": 
    import re
    from fmt import fmt
    from color import t
    from f import sqrt
    from lwtest import run, Assert
    from textwrap import dedent
    n = 100
    def stats(seq):
        'Return (mean, stddev) for sequence of Decimal numbers'
        n = len(seq)
        mean = sum(seq)/n
        deviations = [(i - mean)**2 for i in seq]
        variance = sum(deviations)/(n - 1)
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
        'Timer that shows time.sleep() time is counted too'
        t = Timer()
        t.start
        time.sleep(1)
        t.stop
        print(f"Time with 1 s sleep = {t.et} s")
    def D_Context_manager_example():
        'Time a loop a bunch of times'
        print("Context manager use:")
        r, m = [], 1e5
        for i in range(n):
            with Timer() as t:
                for i in range(int(m)):
                    pass
            r.append(t.et)
        mean, sdev = stats(r)
        print(f"  Repeated {int(n*m)} times")
        rsd = 100*sdev/mean
        print(f"  relative std dev = {fmt(rsd)}%")
    def E_Timer_decorator_example():
        print("Using Timer as a decorator:")
        @Timer()
        def Demo():
            for i in range(n):
                time.sleep(0.001)
        Demo()
    def F_min_resolution_example():
        'Estimate the minimum timer resolution'
        r, n, D = [], int(1e5), decimal.Decimal
        to_ns = D(1e9)
        for i in range(n):
            t1, t2 = Timer.ns(), Timer.ns()
            r.append(D(t2 - t1)/to_ns)
        mean, sdev = stats(r)
        print(f"Estimate of time.perf_counter_ns practical resolution:")
        print(f"  Sample size = {n}")
        print(f"  Mean = {fmt(mean*to_ns, n=2)} ns")
        print(f"  Std dev = {fmt(sdev*to_ns, n=2)} ns")
        print(f"  Relative std dev = {fmt(100*sdev/mean, n=2)}%")
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
            time.sleep(2*st)  # Don't count this one
        print(f"  Expected elapsed time = {n*st} s")
        print(f"  Actual elapsed time   = {t.et} s")
    def H_Discuss_example():
        N = decimal.getcontext().prec
        t1, t2 = Timer.ns(), Timer.ns()
        print("\nDiscussion:\n")
        print(dedent(f'''
        Timer objects use Decimal numbers to keep track of time.  The default
        Decimal context uses {N} significant figures, so you will see numerous
        meaningless figures in typical output. 
        
        Timing is done using the time.perf_counter_ns function.  Two
        sequential calls to this resulted in the times {t1} and 
        {t2}.  Their difference is {t2 - t1} ns, which will be different each
        time you try it.
        
        Timing things on computers with software has been notoriously poor
        over the decades and you need to be aware of the pitfalls.  If my
        memory serves, trying to get decent timing on early MSDOS systems was
        tough because clock resolutions were on the order of a second or so.
        UNIX systems in the 1980's might have had resolutions of an order of
        magnitude or two better, but still pretty crummy.  Things are also
        more problematic on operating systems that can suspend your process,
        which means almost everything you'd use today.
        
        Python will use tools available to it from the operating system, so
        your results will depend on your hardware and software.  The best
        advice is to be aware of the many sources of timing variability and
        use multiple measurements to estimate the mean and the spread in the
        results.
        
        When you get the elapsed time of a Timer object (et attribute), it
        will be a flt instance from f.py.  This will cause the elapsed time to
        be printed to 3 digits, the default.  Change Timer.et.n to a larger
        number for more digits.
 
        The Stopwatch class is a convenience for routine timing tasks in a
        script.  You can use the timer.sw convenience instance by starting
        it with sw.reset(), but be aware that it is not thread-safe.  It's
        handy because the returned type of flt means you don't see a lot of
        useless digits.
        '''[1:].rstrip()))
    # Testing
    def Test():
        s = BasicTime(2e-9)
        Assert(s == "2 ns")
        s = BasicTime(0.1)
        Assert(s == "100 ms")
        s = BasicTime(50)
        Assert(s == "50 s")
        s = BasicTime(u("minute"))
        Assert(s == "1 min")
        s = BasicTime(u("hr"))
        Assert(s == "1 hr")
        s = BasicTime(u("day"))
        Assert(s == "1 day")
        s = BasicTime(u("week"))
        Assert(s == "1 wk")
        s = BasicTime(u("month"))
        Assert(s == "1 mo")
        s = BasicTime(u("yr"))
        Assert(s == "1 yr")
        s = BasicTime(u("decade"))
        Assert(s == "1 decade")
        s = BasicTime(u("century"))
        Assert(s == "1 century")
        s = BasicTime(u("millenia"))
        Assert(s == "1 millenia")
    retvalue, s = run(globals(), quiet=True, halt=False)
    if retvalue:
        t.print(f"{t('ornl')}Self tests failed")
        print(s.strip())
        exit(1)
    with Timer() as T:
        run(globals(), regexp="example$", quiet=True)
        #run(globals(), regexp="example$", verbose=True)
        #run(globals(), regexp="example$")
    print(f"Total time for examples = {fmt(T.et, n=2)} s")
