'''
Time-related tools:
    Stopwatch class:  For elapsed times
    Timer class:  Tool that works as a context manager and decorator
    FTime class:  Get a filename with a time in it
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
        import datetime
        import time
        import decimal
        from textwrap import dedent
        from pdb import set_trace as xx 
    # Custom imports
        from f import flt
if 1:   # Classes 
    class Stopwatch(object):
        '''Timer that returns the elapsed time in seconds from when it was
        started.  Example usage:
            sw = Stopwatch()
            ...
            t = sw()    # How many seconds have elapsed since starting
        '''
        def __init__(self):
            self.start = flt(time.time())
        def __call__(self):
            return flt(time.time() - self.start)
    class Timer(object):
        '''Use an instance of this object to time events in code.  
        Ideas from https://realpython.com/python-timer/ and 
        https://realpython.com/python-with-statement/#measuring-execution-time
    
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
        '''
        ns = time.perf_counter_ns
        def __init__(self):
            self.clear()
            self._u = decimal.Decimal(1)
            ## The timer has the following states:
            ##   "init"  Waiting to be started
            ##   "run"   Start has been called
            ##   "stop"  Stop was called; can be continued
        def clear(self):
            'Set the timer to the initialized state'
            self._start, self._stop = [], []
            self._state = "init"
        ## Decorator functionality
        def __call__(self, func):
            def f(*args, **kw):
                self.start
                func(*args, **kw)
                self.stop
                print(f"{str(func)} time = {self.et} s")
            return f
        ## Context manager functionality
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
        def __call__(self):
            '''Return a string containing the time now that is suitable
            for a filename.
            '''
            d = datetime.datetime.now()
            s = (f"{d.year:04d}{d.month:02d}{d.day:02d}_"
                 f"{d.hour:02d}{d.minute:02d}{d.second:02d}."
                 f"{d.microsecond:06d}")
            return s
if 1:   # Convenience instances
    timer = Timer()
    fnt = FNTime()

if __name__ == "__main__": 
    import re
    from fmt import fmt
    from f import sqrt
    from lwtest import run
    from textwrap import dedent
    n = 100
    def stats(seq):
        'Return (mean, stddev) for sequence of Decimal numbers'
        n = len(seq)
        mean = sum(seq)/n
        deviations = [(i - mean)**2 for i in seq]
        variance = sum(deviations)/(n - 1)
        return mean, sqrt(variance)
    ## The functions are named with leading letters to control the
    ## execution order because lwtest.run() alphabetizes the names.
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
        '''[1:].rstrip()))
    with Timer() as T:
        run(globals(), regexp="example$", quiet=True)
        #run(globals(), regexp="example$", verbose=True)
        #run(globals(), regexp="example$")
    print(f"Total time for examples = {fmt(T.et, n=2)} s")
