"""
Prints information about the python installation
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014, 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Prints information about the python installation
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    # Uncomment the following, move up, and it should work for python 2
    # from __future__ import print_function, division
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import dedent
if 1:  # Global variables
    py3 = True if sys.version_info[0] > 2 else False


def Python2():
    def P(s, val):
        print(s)
        print("  " + val)

    def PL(s, val, size=30):
        fmt = "%%-%ds %%s" % size
        print(fmt % (s, val))

    def Numbers():
        size = 35
        print("Number information:")
        PL("  Max int", sys.maxint, size)
        PL("  Largest negative int", -sys.maxint - 1, size)
        print("  Floating point info:")
        s = sys.float_info
        PL("    Number of digits", s.dig, size)
        PL("    Maximum floating point number", s.max, size)
        PL("    Minimum floating point number", s.min, size)
        PL("    (First number > 1) - 1", s.epsilon, size)
        print("")

    def Path():
        print("Path:")
        for i in sys.path:
            print(" " + i)
        print("")

    def Version():
        print("Version info:\n  " + sys.version)
        PL("  Version info", sys.version_info)
        PL("  Hex version", hex(sys.hexversion))
        try:
            PL("  Subversion info", sys.subversion)
        except Exception:
            pass
        PL("  API version", sys.api_version)
        try:
            PL("  Windows version", sys.getwindowsversion())
            PL("  winver", sys.winver)
        except Exception:
            pass
        print("")

    def Other():
        print("Other info:")
        PL("  Interpreter's check interval", sys.getcheckinterval())
        PL("  Default Unicode encoding", sys.getdefaultencoding())
        PL("  Byte order", sys.byteorder)
        # PL("  DLL handle", hex(sys.dllhandle))
        PL("  Exec prefix", sys.exec_prefix)
        PL("  Executable", sys.executable)
        PL("  File system encoding", sys.getfilesystemencoding())
        PL("  Recursion limit", sys.getrecursionlimit())
        PL("  Max size", hex(sys.maxsize))
        PL("  Max Unicode", hex(sys.maxunicode))
        PL("  Platform", sys.platform)
        PL("  Prefix", sys.prefix)
        PL("  stdin", sys.stdin)
        PL("  stdout", sys.stdout)
        PL("  stderr", sys.stderr)

    print("Python Information")
    print("------------------")
    print("")
    Version()
    Numbers()
    Path()
    Other()


def Python3():
    def Version():
        v = sys.version.replace("\n", " ")
        print("Version info:  " + v)
        print("  API version", sys.api_version)
        try:
            print("  Windows version", sys.getwindowsversion())
            print("  winver", sys.winver)
        except Exception:
            pass
        print("Implementation:  ")
        im, ind = sys.implementation, " " * 4
        print(f"{ind}_multiarch:  {im._multiarch}")
        print(f"{ind}cache_tag :  {im.cache_tag}")
        print(f"{ind}hexversion:  {im.hexversion} = 0x{im.hexversion:x}")
        print(f"{ind}name      :  {im.name}")
        print(f"Byte order = {sys.byteorder}")
        print(f"Built-in module names:")
        # for line in Columnize(sys.builtin_module_names, indent=" "*4,
        #                      width=14):
        for line in Columnize(sys.builtin_module_names, columns=5):
            print(ind, line)
        c = sys.copyright.replace("All Rights Reserved.", "")
        print(f"Copyright")
        for i in c.split("\n"):
            i = i.strip()
            if i:
                print(ind, i)
        try:
            print(f"DLL handle = {sys.dllhandle}")
        except Exception:
            pass
        print(f"Don't write bytecode = {sys.dont_write_bytecode}")
        print(f"exec_prefix = {sys.exec_prefix}")
        print(f"executable = {sys.executable}")
        f = sys.flags
        print(f"Command line flags:")
        for i in """debug inspect interactive optimize dont_write_bytecode
            no_user_site no_site ignore_environment verbose bytes_warning
            quiet hash_randomization isolated dev_mode utf8_mode""".split():
            try:
                s = eval(f"bool(f.{i})")
                print(f"{ind}{i:19s} = {s}")
            except Exception:
                pass
        print(f"Float information:")
        f = sys.float_info
        for i in """max max_exp max_10_exp min min_exp min_10_exp
                dig mant_dig epsilon radix rounds""".split():
            s = eval(f"f.{i}")
            print(f"{ind}{i:19s} = {s}")
        print(f"float_repr_style = {sys.float_repr_style}")
        print(f"getallocatedblocks = {sys.getallocatedblocks()}")
        print(f"getdefaultencoding = {sys.getdefaultencoding()}")
        try:
            print(f"getdlopenflags = {sys.getdlopenflags()}")
        except Exception:
            pass
        print(f"getfilesystemencoding = {sys.getfilesystemencoding()}")
        print(f"getfilesystemencodeerrors = {sys.getfilesystemencodeerrors()}")
        print(f"getrecursionlimit = {sys.getrecursionlimit()}")
        print(f"getswitchinterval = {sys.getswitchinterval()} s")
        print(f"getprofile = {sys.getprofile()}")
        print(f"gettrace = {sys.gettrace()}")
        try:
            print(f"getwindowsversion = {sys.getwindowsversion()}")
        except Exception:
            pass
        print(f"get_asyncgen_hooks = {sys.get_asyncgen_hooks()}")
        try:
            print(
                f"get_coroutine_origin_tracking_depth = {sys.get_coroutine_origin_tracking_depth()}"
            )
        except Exception:
            pass
        try:
            print(f"get_coroutine_wrapper = {sys.get_coroutine_wrapper()}")
        except Exception:
            pass
        f = sys.hash_info
        print(f"Hash information:")
        for i in """
            width modulus inf nan imag algorithm hash_bits seed_bits cutoff
            """.split():
            s = eval(f"f.{i}")
            print(f"{ind}{i:9s} = {s}")
        print(f"int information: {sys.int_info}")
        print(f"maxsize: {sys.maxsize}")
        print(f"maxunicode: {sys.maxunicode} = 0x{sys.maxunicode:x}")
        print(f"meta_path: {sys.meta_path}")
        print(f"Modules:")
        for line in Columnize(sys.modules, columns=2):
            print(ind, line)
        print(f"Path:")
        for i in sys.path:
            print(f"{ind}{i}")
        print(f"path_hooks:")
        for i in sys.path_hooks:
            print(f"{ind}{i}")
        print(f"platform: {sys.platform}")
        print(f"prefix: {sys.prefix}")
        print(f"thread_info: {sys.thread_info}")
        try:
            print(f"tracebacklimit: {sys.tracebacklimit}")
        except Exception:
            pass
        print(f"warnoptions: {sys.warnoptions}")
        try:
            print(f"winver: {sys.winver}")
        except Exception:
            pass
        print(f"_xoptions: {sys._xoptions}")

    print("Python Information")
    print("------------------")
    print("")
    Version()


if __name__ == "__main__":
    Python3() if py3 else Python2()
