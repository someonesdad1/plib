'''
Time integer and floating point counting

    Thu 16 Sep 2010 06:22:30 PM  Results on Intel 2.5 GHz quad core computer:
    Integer counting:
           100:  elapsed time = 0.001 s, t/pt =   9999 ns
          1000:  elapsed time = 0.000 s, t/pt =      0 ns
         10000:  elapsed time = 0.000 s, t/pt =      0 ns
        100000:  elapsed time = 0.005 s, t/pt =     49 ns
         1e+06:  elapsed time = 0.056 s, t/pt =     55 ns
         1e+07:  elapsed time = 0.556 s, t/pt =     55 ns

    Float counting:
           100:  elapsed time = 0.000 s, t/pt =      0 ns
          1000:  elapsed time = 0.000 s, t/pt =      0 ns
         10000:  elapsed time = 0.001 s, t/pt =    100 ns
        100000:  elapsed time = 0.011 s, t/pt =    109 ns
         1e+06:  elapsed time = 0.104 s, t/pt =    104 ns
         1e+07:  elapsed time = 1.035 s, t/pt =    103 ns

    Tue 06 Jul 2021 10:16:42 PM using python 3.7.10 on quad core computer
    built around 2016:
    Integer counting:
           100:  elapsed time =  0.000 s, t/pt =     64 ns
          1000:  elapsed time =  0.000 s, t/pt =     38 ns
         10000:  elapsed time =  0.000 s, t/pt =     41 ns
        100000:  elapsed time =  0.004 s, t/pt =     41 ns
         1e+06:  elapsed time =  0.045 s, t/pt =     44 ns
         1e+07:  elapsed time =  0.457 s, t/pt =     45 ns
    
    Float counting:
           100:  elapsed time =  0.000 s, t/pt =     52 ns
          1000:  elapsed time =  0.000 s, t/pt =     42 ns
         10000:  elapsed time =  0.000 s, t/pt =     42 ns
        100000:  elapsed time =  0.009 s, t/pt =     92 ns
         1e+06:  elapsed time =  0.093 s, t/pt =     93 ns
         1e+07:  elapsed time =  0.960 s, t/pt =     95 ns
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
    # Time of integer and float counting
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import time
if 1:   # Global variables
    fmt = "  %8g:  elapsed time = %6.3f s, t/pt = %6d ns"
def I(n):
    t0, count, N = time.time(), 0, int(n)
    while count < N:
        count += 1
    t = time.time() - t0
    tpp = t/n*1e9
    print(fmt % (n, t, tpp))
def F(n):
    t0, count = time.time(), 0.0
    while count < n:
        count += 1.0
    t = time.time() - t0
    tpp = t/n*1e9
    print(fmt % (n, t, tpp))
if __name__ == "__main__": 
    s = (2, 3, 4, 5, 6, 7)
    print("Integer counting:")
    for i in s:
        I(10**i)
    print("\nFloat counting:")
    for i in s:
        F(10**i)
