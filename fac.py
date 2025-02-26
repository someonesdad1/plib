"""
Use /usr/bin/factor to provide the prime factorization of integers
    Factor(3141596, u=True) produces 2²·37·21227
    Factor(3141596) produces 2^2*37*21227
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Provide Factor(x), which factors integers using /usr/bin/factor
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque, defaultdict
        import subprocess
    if 1:  # Global variables
        ii = isinstance
if 1:  # Core functionality

    def Factor(x, u=False):
        """Return the string representing the prime factorization of
        integer x.  If u is True, use Unicode to represent the
        factorization.  Return None if something goes wrong.
        """
        e = dict(zip(list(range(10)), "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        if not (ii(x, int)):
            raise TypeError("x must be an integer")
        cmd = ["/usr/bin/factor", str(x)]
        try:
            r = subprocess.run(cmd, capture_output=True)
        except Exception:
            return None
        # Get list of prime factors
        s = r.stdout.decode("UTF-8").strip().split(":")[1].strip().split()
        factors = deque(int(i) for i in s)
        d = defaultdict(int)
        while factors:
            n = factors.popleft()
            d[n] += 1
        o = []
        # Generate ASCII form to check calculation
        for i in d:
            if d[i] > 1:
                o.append(f"{i}**{d[i]}")
            else:
                o.append(str(i))
        r = "*".join(o)
        assert eval(r) == x
        r = r.replace("**", "^")
        # Return the needed value
        if u:
            # Unicode form
            o = []
            for i in d:
                if d[i] > 1:
                    s = ""
                    for k in str(d[i]):
                        s += e[int(k)]
                    o.append(str(i) + s)
                else:
                    o.append(str(i))
            return "·".join(o)
        else:
            return r


if __name__ == "__main__":
    from lwtest import run, Assert
    from math import factorial

    def Test_Factor():
        x = factorial(100)
        s = (
            "2^97*3^48*5^24*7^16*11^9*13^7*17^5*19^5*23^4*29^3*31^3*"
            "37^2*41^2*43^2*47^2*53*59*61*67*71*73*79*83*89*97"
        )
        Assert(Factor(x, u=False) == s)
        s = (
            "2⁹⁷·3⁴⁸·5²⁴·7¹⁶·11⁹·13⁷·17⁵·19⁵·23⁴·29³·31³·37²·41²·"
            "43²·47²·53·59·61·67·71·73·79·83·89·97"
        )
        Assert(Factor(x, u=True) == s)

    exit(run(globals(), halt=True)[0])
