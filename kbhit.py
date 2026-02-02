if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Get the next character typed at the keyboard oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2010 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞2 Move to util.py
            - Add in extra functionality to decode all the common keys that can be
              pressed on the keyboard:  regular keys, function keys, control keys, etc.
        
        oo>
    '''
    if 1:  # Standard imports
        import fcntl
        import os
        import sys
        import termios
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def kbhit(block=True):
        '''Get the next character typed at the keyboard.  If block is True,
        then wait for the key to be pressed, otherwise return immediately.
        This is for Linux; under Windows, use
            from msvcrt import kbhit
        for similar functionality.
        
        -----------------------------------------------------------------
        WARNING:  this only returns the first byte in the keyboard buffer
        and, thus, will probably not give you what you want if you want to
        detect function keys, arrow keys, etc.
        -----------------------------------------------------------------
        '''
        # From
        # http://stackoverflow.com/questions/9882985/capture-keystrokes-for-a-game-python
        fd = sys.stdin.fileno()
        oldattr = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        if block:
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        else:
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        try:
            while True:
                try:
                    c = sys.stdin.read(1)
                    return c
                except IOError:
                    return None
        finally:
            # This code is executed before returning:  Reset to old terminal
            # characteristics.
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldattr)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
if __name__ == "__main__":
    # Run as a script for a demonstration
    print("Type 'q' to exit")
    while True:
        c = kbhit()
        if c == "q":
            break
        o = ord(c)
        s = c if o >= ord(" ") else ""
        print(f"char = '{s}'  ord(char) = {o:3d} (0x{o:02x})")
