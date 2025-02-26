"""
Show system and python information
"""

import f
import platform
import multiprocessing as mp
import sys
from color import t
from textwrap import wrap

t.hl = t("grnl")
t.ti = t("ornl")
cores = mp.cpu_count()

# System info
print(
    f"""
Device name     DON-PC
Processor       Intel Core i5-7600 CPU @ 3.5 GHz
    {t.hl}Cores       {cores}{t.n}
    L1 cache    256 kB
    L2 cache      1 MB
    L3 cache      6 MB
{t.hl}Installed RAM   8 GB{t.n}
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
"""[1:-1]
)

# Python info
ver = sys.version.replace("\n", "")
contsz = f"{f.log(sys.maxsize) / f.log(2)}"
impl = f"{platform.python_implementation()}"
w = 34
flg = wrap(str(sys.flags), initial_indent=" " * 16, subsequent_indent=" " * w)
flags = "\n".join(flg)
print(
    f"""
{t.ti}Python information{t.n}
    {t.hl}Python version  {ver}{t.n}
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
"""[1:-1]
)
