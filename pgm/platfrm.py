if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print out platform information
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import platform
    import pathlib
    import sys
    from pdb import set_trace as xx

    if 1:
        import debug

        debug.SetDebugger()
if 1:  # Custom imports
    from wrap import dedent, wrap
if 1:  # Global variables
    ii = isinstance
    n = 25
    fmt = "{{:{}}} {{}}".format(n)
    wrap.i = " " * 4


def W(s):
    if 0:
        tw = textwrap.wrap(
            str(s), width=76 - n, initial_indent="", subsequent_indent=" " * (n + 3)
        )
        for i in tw:
            print(i)
    else:
        print(wrap(s))


def Platform():
    cmds = """
        Architecture, architecture(), 0
        Machine, architecture(), 0
        Platform, platform(), 0
        Processor, processor(), 0
        Python build, python_build(), 0
        Python compiler, python_compiler(), 0
        Python version, python_version(), 0
        Release, release(), 0
        System, system(), 0
        Version, version(), 0
        Uname, uname(), 1
        Win32 version, win32_ver(), 0
    """.strip().split("\n")
    for cmd in cmds:
        f, c, newline = [i.strip() for i in cmd.split(",")]
        newline = bool(int(newline))
        s = eval("platform.{}".format(c))
        if f in ("Uname",):
            print(fmt.format(f, ""), end="")
            if newline:
                print()
            W(str(s))
        else:
            if ii(s, (list, tuple)):
                print(fmt.format(f, " ".join(s)))
            else:
                print(fmt.format(f, s))
    print("-" * 70)


def Other():
    print(fmt.format("Python executable ", sys.executable))
    print(fmt.format("Allocated memory blocks", sys.getallocatedblocks()))
    print(fmt.format("File system encoding", sys.getfilesystemencoding()))
    print(fmt.format("Recursion limit", sys.getrecursionlimit()))
    print(fmt.format("Implementation", ""))
    W(wrap(str(sys.implementation)))
    print(fmt.format("Bytes per integer digit", sys.int_info.sizeof_digit))
    print(fmt.format("Largest Unicode codepoint (hex)", hex(sys.maxunicode)))
    # Module search path
    s = ", ".join(sys.path)
    print(fmt.format("Module search path", ""))
    W(s)
    #
    print(fmt.format("Python files location", sys.prefix))
    print(fmt.format("Thread info:", ""))
    print(fmt.format("  Implementation", sys.thread_info.name))
    print(fmt.format("  Lock", sys.thread_info.lock))
    print(fmt.format("  Version", sys.thread_info.version))
    print(fmt.format("API version", sys.api_version))
    print(fmt.format("Warning options", sys.warnoptions))

    print(fmt.format("Version info", ""))
    print(wrap(str(sys.version_info)))
    fi = sys.float_info
    print("Float information:")
    print(fmt.format("  Size of float (bytes)", sys.getsizeof(1.0)))
    print(fmt.format("  epsilon (fp step)", fi.epsilon))
    print(fmt.format("  Decimal digits", fi.dig))
    print(fmt.format("  Significand digits", fi.mant_dig))
    print(fmt.format("  Maximum float", fi.max))
    print(fmt.format("  Minimum float", fi.min))
    print(fmt.format("  Max base 10 exponent", fi.max_10_exp))
    print(fmt.format("  Min base 10 exponent", fi.min_10_exp))
    print(fmt.format("  Rounding mode", fi.rounds))
    print(fmt.format("  Float representation style", sys.float_repr_style))


if __name__ == "__main__":
    p = pathlib.Path(sys.argv[0]).resolve()
    print(f"Script:  {p}")
    Platform()
    Other()
