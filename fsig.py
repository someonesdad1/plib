def fsig(x, digits=None):
    """Returns a string representing the float x to a specified number
    of digits.  x can also be an integer, in which case it is converted to
    a float.  Similar to the 'g' string formatting spec, but you can
    control the points where fixed point interpolation switches to
    scientific notation.
    
    The fsig function attributes control other behaviors:
    
    fsig.low         Use scientific notation if x < low
    fsig.high        Use scientific notation if x >= high
    fsig.digits      Default number of significant digits
    fsig.dp          String to use for decimal point
    fsig.rdp         Remove ending decimal point if True
    fsig.rtz         Remove trailing zeroes if True
    fsig.rlz         Remove leading 0 before decimal point if True
    """
    fsig.low = fsig.__dict__.get("low", 1e-5)
    fsig.high = fsig.__dict__.get("high", 1e6)
    fsig.digits = fsig.__dict__.get("digits", 3)
    fsig.dp = fsig.__dict__.get("dp", ".")
    fsig.rdp = fsig.__dict__.get("rdp", False)
    fsig.rtz = fsig.__dict__.get("rtz", False)
    fsig.rlz = fsig.__dict__.get("rlz", False)
    def rtz(s):
        if not fsig.rtz:
            return s
        t = list(s)
        while t and t[-1] == "0":
            del t[-1]
        return "".join(t)
    if fsig.low > fsig.high:
        raise ValueError("fsig.low > fsig.high")
    msg = "{}digits = {} is out of range"
    if not (1 <= fsig.digits <= 15):
        raise ValueError(msg.format("fsig.", fsig.digits))
    if digits is not None and not (1 <= digits <= 15):
        raise ValueError(msg.format("", digits))
    if not isinstance(x, (float, int)):
        raise TypeError("x must be a float or integer")
    if isinstance(x, int):
        x = float(x)
    ndig = fsig.digits - 1 if digits is None else digits - 1
    if x and (abs(x) < fsig.low or abs(x) > fsig.high):
        xs = "{:.{}e}".format(x, ndig)  # Use scientific notation
        st, e = xs.split("e")
        t = "{}e{}".format(rtz(st), int(e))
        return t.replace(".", fsig.dp)
    # xs = list of significant digits with decimal point removed
    # e = integer exponent
    xs, e = "{:.{}e}".format(abs(x), ndig).replace(".", "").split("e")
    xs, e = list(xs), int(e)
    sgn = "-" if x < 0 else ""
    if not e:
        t = "{:.{}e}".format(abs(x), ndig).split("e")[0]
        u = t.replace(".", fsig.dp)
        v = rtz(u)
        if fsig.rdp and v[-1] == fsig.dp:
            v = v[:-1]
        return sgn + v
    elif e < 0:
        e = abs(e) - 1
        xs.reverse()
        while e:
            xs.append("0")
            e -= 1
        xs.append(fsig.dp)
        if not fsig.rlz:
            xs.append("0")
        xs.reverse()
    else:
        n = len(xs)
        if e >= n:
            e -= n - 1
            while e:
                xs.append("0")
                e -= 1
            xs.append(fsig.dp)
        else:
            xs.insert(e + 1, fsig.dp)
    t = rtz("".join(xs))
    if fsig.rdp and t[-1] == fsig.dp:
        t = t[:-1]
    return sgn + t

if __name__ == "__main__":
    # A few test cases
    fsig.digits = 2
    fsig.rtz = True
    fsig.rlz = True
    u = 1.23456789
    for x, s in (
        (u, "1.2"),
        (u * 10, "12."),
        (u * 100, "120."),
        (u * 1e5, "120000."),
        (u * 1e6, "1.2e6"),
        (u / 10, ".12"),
        (u / 100, ".012"),
        (u / 1e5, ".000012"),
        (u / 1e6, "1.2e-6"),
    ):
        assert fsig(x) == s, "fsig({}) != {}".format(x, s)
        assert fsig(-x) == "-" + s, "fsig({}) != {}".format(x, "-" + s)
