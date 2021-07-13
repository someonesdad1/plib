'''
From
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/144838
Author:  Christian Bird 14 Aug 2002
 
Modified by Don Peterson 14 Aug 2003
    Comments by DP:
 
    I use debug statements regularly in my code and often include the
    name of the function in the debug message. This is tedious and
    error prone if I copy and paste debug statements between different
    functions. In addition, I have often desired the ability to easily
    turn off debug statements without needing to use if not debug:
    print "stuff" statements everywhere.
 
    This code automatically inserts the function name, class name, and
    line number of the debug statement or error statement when it is
    printed out. This makes it easy to jump straight to that line in
    an editor. Each of the messaging methods: stdMsg, errMsg, and
    dbgMsg can be used just like a print statement in that you can
    separate an arbitrary number of arguments with commas and each one
    will be converted to a string.  e.g. dbgMsg("the value of X is",
    x)
 
    The other nice thing about this type of system is that you can
    create multiple "handler" objects by subclassing MessageHandler.
    Each registered handler gets sent each string when a program calls
    a Msg function so it's possible that one Msg call could send text
    to a log file, a gui window, and standard out.
 
Modified by Don Peterson 18 Feb 2016:  updated to work on python 3.4
'''
# messaging.py
# This is a module used for messaging.  It allows multiple classes
# to handle various types of messages.  It should work on all python
# versions >= 1.5.2

import sys
import string

# This flag determines whether debug output is sent to debug handlers
# themselves
debug = 1

def SetDebugging(debugging):
    global debug
    debug = debugging

class MessagingException(Exception):
    '''An exception class for any errors that may occur in
    a messaging function'''
    def __init__(self, args=None):
        self.args = args

class FakeException(Exception):
    '''an exception that is thrown and then caught
    to get a reference to the current execution frame'''
    pass

class MessageHandler:
    '''All message handlers should inherit this class.  Each method will
    be passed a string when the executing program passes calls a
    messaging function'''
    def HandleStdMsg(self, msg):
        '''do something with a standard message from the program'''
        pass
    def HandleErrMsg(self, msg):
        '''do something with an error message.  This will already include the
        class, method, and line of the call'''
        pass
    def HandleDbgMsg(self, msg):
        '''do something with a debug message.  This will already include the
        class, method, and line of the call'''
        pass

class DefaultMessageHandler(MessageHandler):
    '''This is a default message handler.  It simply spits all strings to
    standard out'''
    def HandleStdMsg(self, msg):
        sys.stdout.write(msg + "\n")
    def HandleErrMsg(self, msg):
        sys.stderr.write(msg + "\n")
    def HandleDbgMsg(self, msg):
        sys.stdout.write(msg + "\n")

MessageHandlers = []    # Keep track of the handlers

def RegisterMessageHandler(handler):
    'Call this with the handler to register it for receiving messages'
    # We won't check for inheritance, but we should check to make
    # sure that it has the correct methods.
    for name in ["HandleStdMsg", "HandleErrMsg", "HandleDbgMsg"]:
        try:
            getattr(handler, name)
        except:
            m = ("The class " + handler.__class__.__name__ +
                 " is missing a " + name + " method")
            raise MessagingException(m)
    MessageHandlers.append(handler)

def GetCallString(level):
    # this gets us the frame of the caller and will work
    # in python versions 1.5.2 and greater (there are better
    # ways starting in 2.1
    #xx
    import inspect
    file = inspect.stack()[level + 1][1]
    #xx
    try:
        raise FakeException("this is fake")
    except Exception as e:
        # Get the current execution frame
        f = sys.exc_info()[2].tb_frame
    # Go back as many call frames as was specified
    while level >= 0:
        f = f.f_back
        level = level-1
    # If there is a self variable in the caller's local namespace then
    # we'll make the assumption that the caller is a class method
    obj = f.f_locals.get("self", None)
    #functionName = f.f_code.co_name
    if obj:
        callstr = (obj.__class__.__name__+"::"+f.f_code.co_name +
                   " ["+file+":"+str(f.f_lineno)+"]")
    else:
        callstr = f.f_code.co_name+" ["+file+":"+str(f.f_lineno)+"]"
    return callstr
    
def StdMsg(*args):
    'Send this message to all handlers of std messages'
    s = ' '.join([str(i) for i in args])
    for handler in MessageHandlers:
        handler.HandleStdMsg(s)

def Err(*args):
    'Send this message to all handlers of error messages'
    s = ' '.join([str(i) for i in args])
    errstr = "Error in " + GetCallString(1) + ": " + s
    for handler in MessageHandlers:
        handler.HandleErrMsg(errstr)

def Dbg(*args):
    'Send this message to all handlers of debug messages'
    if not debug:
        return
    s = ' '.join([str(i) for i in args])
    errstr = GetCallString(1) + ": " + s
    for handler in MessageHandlers:
        handler.HandleDbgMsg(errstr)

RegisterMessageHandler(DefaultMessageHandler())

def TestMessage():
    'Here are some examples of this messaging code at work'
    SetDebugging(0)
    Dbg("This won't be printed")
    StdMsg("But this will")
    SetDebugging(1)
    def foo():
        Dbg("This is a debug message in", "foo")
    class bar:
        def baz(self):
            Err("This is an error message in bar")
    foo()
    b = bar()
    b.baz()

if __name__ == "__main__":
    TestMessage()
