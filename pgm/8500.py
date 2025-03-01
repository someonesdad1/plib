'''
<∞ desc 

Operation of B&K 8500 DC load

∞>

<∞ Copyright © 2025 Don Peterson ∞>
<∞ category elec ∞>
<∞ test none ∞>

'''
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.title = t("denl")
        t.cmd = t("purl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] cmd1 [cmd2...]
          B&K 8500 DC load help info.  cmd values are
            all     Show all
            cc      Constant current operation
            tm      Timer operation
            bat     Battery test
            rs      Remote sense
            brk     DC circuit breaker
            short   Short emulator
            save    Save/recall settings to/from registers
        '''))
        exit(status)
    def ParseCommandLine(d):
        #d["-a"] = False     # Need description
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
        GetColors()
        return args
if 1:   # Core functionality
    def CC():
        t.print(dedent(f'''
        {t.title}Constant current testing{t.n}
            Use I-set to choose the desired current level.  Press On-Off to turn the load on and
            off.  Press the ↑ or ↓ keys to see the operating power level.
        '''))
    def TM():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Timer mode:  stay on for indicated time, then turn off{t.n}
            shift + menu        {on}:CONFIG{off}
            ↑ or ↓              {on}:LOAD ON TIMER{off}
            enter               {on}:TIMER STATE{off}
            ↓                   {on}:TIMER SET{off}
            enter               {on}:TIMER=XXXXXS{off}   Enter 1 to 6000 s
            enter               {on}:TIMER SET{off}
            esc esc
            Now when load is turned on, its duration will be timed.  To turn off, enter the menu
            {on}:CONFIG:LOAD ON TIMER:TIMER STATE{off} and set to {on}:OFF{off}.
        '''))
    def BAT():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Battery test: Measures time it takes for battery to drop to a specified voltage at
            constant current.  At test end, display shows A*hr (charge) drawn from battery.{t.n}
            Set desired constant current level
            shift + Battery     {on}MIN VOLT = 0.10V{off}    Voltage level to end test
            Enter voltage   
            enter               Starts test; CC on
            ↑ or ↓              Show power level and accumulated A*hr
            OFF shows           Test finished
            ↑ or ↓              Display total charge in A*hr
            shift + Battery     Turn battery test mode off
        '''))
    def RS():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Remote sensing:  Terminals in 4-clamp connector on back.  Remote sensing has
            to be turned on to be functional.  The power displayed by the load will
            still include the power dissipated by the lead's connections.{t.n}
            shift + Menu        {on}:CONFIG{off}
            enter               {on}:INTIAL CONFIG{off}
            ↓ 8 times           {on}:REMOTE SENSE{off}
            enter               {on}:OFF|DEFAULT{off}
            ↓                   {on}:ON{off}
            enter               {on}:REMOTE SENSE{off} and annunciator shows Sense
            esc esc             Exit menu
        '''))
    def BRK():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Act as a DC circuit breaker{t.n}
            - This needs to be tested.  Uses voltage threshold operation and remote
              sensing terminals on back.  
            - Set up a shunt to measure current with an op amp to condition the signal
              to desired voltage levels.  This signal is input to the remote sense
              terminals.
            - Put the DC load in series with the supply voltage
            - Enable remote sense
            - Set {on}SYSTEM SET:VOLTAGE OFF SET{off} to the desired shunt voltage to turn off
            - Set {on}SYSTEM SET:VOLTAGE ON SET{off} to 0 V
            - Now the current should be shut off if the 

        '''))
    def SHORT():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Short emulation{t.n}
            CC, CR, CV:  shift-Short simulates a short and draws maximum current.
                         shift-Short to turn off.
            CP:  Same, put you must press On-Off to turn off the load.

        '''))
    def SAVE():
        on, off = t.cmd, t.n
        t.print(dedent(f'''
        {t.title}Save/recall settings to/from registers{t.n}
            There are 25 registers.  To save, use shift-Store; press 1 to 25 and then
            press enter.  Use shift-Recall to restore the settings.

        '''))
    def Dispatch(args):
        dispatch = {
            "cc": CC,
            "tm": TM,
            "bat": BAT,
            "rs": RS,
            "brk": BRK,
            "short": SHORT,
            "save": SAVE,
        }
        if "all" in args:
            for cmd in dispatch:
                dispatch[cmd]()
        else:
            for cmd in args:
                if cmd in dispatch:
                    dispatch[cmd]()
                else:
                    print(f"{cmd!r} not recognized")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Dispatch(args)
