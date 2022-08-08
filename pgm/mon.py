'''
Simple serial port monitor
    It prompts you with '> ' for a string that ends with a newline, sends
    it to the serial port, then reads the string sent back and prints it in
    color as a byte array (the leading "b'" and trailing "'" are removed).
    I use this for development with an Arduino on my desktop computer under
    cygwin.
 
    Needed library:
        pySerial (pySerial https://pypi.org/project/pyserial/)
        Use 'pip install pyserial' if you have pip.
 
    Optional:  Get color.py from
        https://someonesdad1.github.io/hobbyutil/util/color.py to get
        colored output in an ANSI terminal.
 
    You can test that this script works with the following Arduino code:
        void loop(void) {
            Serial.begin(9600);
            while (! Serial) {};
            String msg;
            while (true) {
                if (Serial.available()) {
                    msg = Serial.readStringUntil('\n');
                    Serial.println(msg);
                }
            }
        }
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import serial
    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import color as C
        have_color = True
    except ImportError:
        class Dummy:    # Make a dummy color object to swallow function calls
            def fg(self, *p, **kw):
                pass
            def normal(self, *p, **kw):
                pass
            def __getattr__(self, name):
                pass
        C = Dummy()
        have_color = False
if 1:   # Global variables
    # Colors used
    c_ascii = C.lgreen        # For what came back from serial port
    c_input = C.white         # User's input
    c_quit = C.lmagenta      # When monitor exits
    c_count = C.white         # Character count returned
    # Other constants
    timeout_default = 1
def Lines(input_file):
    '''Generator that returns the text lines of the input_file with
    attached newlines.
    '''
    for line in open(input_file).readlines():
        yield line
def StripByteStuff(b):
    '''b is a byte array.  Convert to a string using repr() and strip off
    the leading "b'" and trailing "'".
    '''
    t = repr(b)
    return t[2:-1]
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] 
      Serial port monitor
        Press 'ctrl-D' to quit.
        Input your data at the '>' prompt.
        The bytes data returned by the port are printed in color.
        Use -h for options help.
    Options (defaults in square brackets):
      -h          Show help message
      -p port     Set the serial port [{d["-p"]}]
      -t seconds  Set the serial port read timeout [{d["-t"]}]
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-p"] = "/dev/ttyS2"      # Serial port to use
    d["-t"] = timeout_default   # Serial port read timeout in s
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-p",):
            d[o] = a
        elif o in ("-t",):
            d[o] = max(0, int(a))
            if not d[0]:
                d[0] = timeout_default
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args
def GetUserString():
    '''Return the string typed by user and include the newline.
    '''
    try:
        C.fg(c_input)
        t = input("> ")
        C.normal()
    except EOFError:
        C.fg(c_quit)
        print("Exit serial port monitor")
        C.normal()
        exit(0)
    return t + "\n"
def PrintGot(got):
    n = len(got)
    C.fg(c_ascii)
    print(StripByteStuff(got), end=" ")
    C.normal()
    C.fg(c_count)
    print("[{}]".format(n))
    C.normal()
def ASCII(d):
    while True:
        s = GetUserString()
        u = s.encode("UTF8")
        SP.write(u)
        got = SP.read_until(terminator=b'\n')
        PrintGot(got)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    try:
        SP = serial.Serial(d["-p"], timeout=1)
    except Exception:
        print("Unable to connect to serial port '{}'".format(d["-p"]))
        exit(1)
    ASCII(d)
