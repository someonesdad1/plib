import f
import platform
import sys
from wrap import dedent
from textwrap import wrap

def Python():
    ver = sys.version.replace("\n", "")
    contsz = f"{f.log(sys.maxsize)/f.log(2)}"
    impl = f"{platform.python_implementation()}"
    w = 34
    flg = wrap(str(sys.flags), initial_indent = " "*16, subsequent_indent=" "*w)
    flags = '\n'.join(flg)
    print(dedent(f'''
    Python information
        Version         {ver}
        Flags
        {flags}
        Platform        {platform.platform()}
                        {sys.platform}
        Implementation  {impl}
        API version     {sys.api_version}
        log2(max container size) = {contsz}
    Python floating point information
        Number of digits                {sys.float_info.dig}
        Mantissa binary digits          {sys.float_info.mant_dig}
        Exponent radix                  {sys.float_info.radix}
        Maximum number                  {sys.float_info.max}
        Minimum number                  {sys.float_info.min}
        Maximum exponent for radix      {sys.float_info.max_exp}
        Maximum exponent for 10         {sys.float_info.max_10_exp}
        Minimum exponent for radix      {sys.float_info.min_exp}
        Minimum exponent for 10         {sys.float_info.min_10_exp}
        (First number > 1) - 1          {sys.float_info.epsilon}
        Addition rounds                 {sys.float_info.rounds}
    '''))

print(dedent(f'''
    Device name     DON-PC
    Processor       Intel(R) Core(TM) i5-7600 CPU @ 3.50GHz   3.50 GHz
        Cores       4
        L1 cache    256 kB
        L2 cache      1 MB
        L3 cache      6 MB
    Installed RAM   8 GB
    Device ID       BA964BA2-04C0-4C34-9D7B-811C7E92CFB8
    Product ID      00329-10180-00000-AA897
    System type     64-bit operating system, x64-based processor
    Pen and touch   No pen or touch input is available for this display

    Windows information
        Edition         Windows 10 Enterprise
        Version         21H2
        Installed on    15-Oct-22
        OS build        19044.3803
        Experience      Windows Feature Experience Pack 1000.19053.1000.0
'''))
Python()
