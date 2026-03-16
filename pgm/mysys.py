'''
Show system and python information
'''
if 1:   # Header
    if 1:   # Standard modules
        import platform
        import multiprocessing as mp
        import sys
        import textwrap
    if 1:   # Standard modules
        import columnize
        import dputil
        import f
        import trm
        import wrap
    if 1:   # Global variables
        t = trm.Trm()
        sp = " "
        nl = "\n"
if 1:   # Core functionality
    def SystemInfo():
        print(wrap.dedent(f'''
        Device name     DON-PC
        Processor       Intel Core i5-7600 CPU @ 3.5 GHz
            {t.hl}Cores       {mp.cpu_count()}{t.n}
            L1 cache    256 kB
            L2 cache      1 MB
            L3 cache      6 MB
        {t.hl}Installed RAM   8 GB{t.n}
        Device ID       BA964BA2-04C0-4C34-9D7B-811C7E92CFB8
        Product ID      00329-10180-00000-AA897
        System type     64-bit operating system, x64-based processor
        Pen and touch   No pen or touch input is available for this display
        Byte order      {sys.byteorder} endian
        
        Windows information
            Edition         Windows 10 Enterprise
            Version         21H2
            Installed on    15-Oct-22
            OS build        19044.3803
            Experience      Windows Feature Experience Pack 1000.19053.1000.0
        '''))
    def PythonInfo():
        impl = f"{platform.python_implementation()}"
        if 0:   # Flag information
            flg = textwrap.wrap(str(sys.flags), initial_indent=sp*8,
                    subsequent_indent=sp*16)
            flags = nl.join(flg)

            items = str(sys.flags).replace("sys.flags(", "").replace(")", "").split(", ")
            for i in columnize.Columnize(items, indent=sp*8):
                t.print(f"{t.flags}{i}")

        # Print the information
        print(wrap.dedent(f'''
        {t.ti}Python information {dputil.PyVer()}{t.n}
            {t.hl}Python version  {sys.version.replace(nl, "")}{t.n}
            {t.pnkl}Flags:'''))
        # Print flag information
        items = str(sys.flags).replace("sys.flags(", "").replace(")", "").split(", ")
        for i in columnize.Columnize(items, indent=sp*8):
            t.print(f"{t.flags}{i}")
        # Remainder of the information
        print(wrap.dedent(f'''
            API version     {sys.api_version}
            log2(max container size) = {f.log(sys.maxsize)/f.log(2)}
        {t.fp}Python floating point information{t.n}
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
    def Platform():
        p = platform
        print(wrap.dedent(f'''
        {t.pf}Python platform information{t.n}
            machine                 {p.machine()}
            node                    {p.node()}
            platform                {p.platform()}
            processor               {p.processor()}
            python_build            {p.python_build()}
            python_compiler         {p.python_compiler()}
            python_branch           {p.python_branch()}
            python_implementation   {p.python_implementation()}
            python_revision         {p.python_revision()}
            python_version          {p.python_version()}
            python_version_tuple    {p.python_version_tuple()}
            release                 {p.release()}
            system                  {p.system()}
            version                 {p.version()}
            uname                   {p.uname()}
        '''))

if __name__ == "__main__":
    # Set up our colors
    t.hl = t.skyl       # Highlight the python version
    t.ti = t.orn        # Title
    t.flags = t.trq1
    t.fp = t.viol       # Floating point stuff
    t.pf = t.ygr        # Platform
    SystemInfo()
    PythonInfo()
    Platform()
