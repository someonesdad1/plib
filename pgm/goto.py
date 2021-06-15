'''
Driver for the old shell g() function; uses _goto.py script.

#-----------------------------------------------------------------------------
# Function to allow moving around to saved directories.  Args are:
#   a       Adds current directory to list
#   e       Edits list
#   g n     Goes to the nth directory.  If n is not a number, it is a string that
#           is a shorthand description and is separated from the optional description
#           by a ! character.
#   -t      Checks each directory in the file
#   -T      Checks all directory in the file, even those commented out
#   -s      Print silent link names
#   S       Search all lines in the config file for a string
#   s       Search the active lines in the config file for a string

g()
{
    # Note this uses cygwin's python 3
    typeset dir
    typeset GOTO=_goto.py
    typeset GOTORC="$HOME/.gotorc"
    # Above works in Linux; following is for Windows
    typeset GOTORC="c:/cygwin/home/Don/.gotorc"
 
    if [ $# -eq 0 ] ; then
        # Pass the script the 0 argument to have it prompt the user
        PYTHONLIB=$PYTHONLIBcyg PYTHONPATH=$PYTHONPATHcyg
        dir="$($PYTHON3 $PLIBcyg/pgm/$GOTO $GOTORC 0)"
    else
        case $1 in
            a)  # Add the current directory to the head of the goto file
                typeset tmp=/tmp/g.$$
                echo $(pwd) >$tmp
                cat $GOTORC >>$tmp
                cp $GOTORC $HOME/.bup/goto.$$  # Make a backup copy
                mv $tmp $GOTORC
                if [ $? -ne 0 ] ; then
                    echo "Addition failed"
                    # Restore from the backup copy
                    cp $HOME/.bup/goto.$$ $GOTORC
                fi
                return
                ;;
            e)  # Edit the goto file
                $EDITOR $GOTORC
                return
                ;;
            -h) # Print a help message
                cat <<EOF
a       Add the current directory to the head of the goto file
e       Edit the goto file
g n     Go to the nth directory in the listing
S       Search active lines for a regular expression
S       Search all lines for a regular expression
-t      Check the goto file's directories exist
-T      Check all the goto file's directories exist, even those commented-out
-s      Print silent link names
 
Otherwise, the item on the command line is looked up.
EOF
                return
                ;;
            S)  # Search the whole config file for a string
                grep -i $2 $GOTORC
                return;;
            s)  # Search active lines for a string
                grep -v "^[ \t]*#" $GOTORC | grep -i $2
                return;;
            -t) # Check the directories
                PYTHONLIB=$PYTHONLIBcyg PYTHONPATH=$PYTHONPATHcyg $PYTHON3 $PYTHONPGMcyg/$GOTO -t $GOTORC
                [ $? -eq 0 ] && echo "$GOTORC directories OK"
                return
                ;;
            -T) # Check all the directories
                PYTHONLIB=$PYTHONLIBcyg PYTHONPATH=$PYTHONPATHcyg $PYTHON3 $PYTHONPGMcyg/$GOTO -T $GOTORC
                [ $? -eq 0 ] && echo "$GOTORC all directories OK"
                return
                ;;
            -s) # Print silent link names
                PYTHONLIB=$PYTHONLIBcyg PYTHONPATH=$PYTHONPATHcyg $PYTHON3 $PYTHONPGMcyg/$GOTO -s $GOTORC
                return
                ;;
            *)  # cd to the choice given on the command line
                PYTHONLIB=$PYTHONLIBcyg PYTHONPATH=$PYTHONPATHcyg dir="$($PYTHON3 $PYTHONPGMcyg/$GOTO $GOTORC $1)"
                ;;
        esac
    fi
    # The following removes any carriage returns, which can happen under
    # Windows.
    dir="$(echo $dir | tr -d '\r')"
    # cd to the desired directory; if it has a .profile file and is
    # not our home directory, source it (this is useful for project
    # aliases, etc.).
    if [ "$dir" ] ; then
        cd "$dir"  # Note 'cd -' works as expected
        typeset p=.profile
        if [ -r $p -a "$(pwd)" != "$HOME" ] ; then
            # First, make sure it's our file
            owner=$(ls -l $p | awk '{print $3}')
            if [ "$owner" = "$LOGNAME" ] ; then
                . $p
                echo "Sourced $p"
            fi
        fi
    fi
}
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
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
if 1:   # Standard imports
    import getopt
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import get
if 1:   # Global variables
    P = pathlib.Path
    class G: pass
    G.gotorc = P("c:/cygwin/home/Don/.gotorc")
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
    Usage:  {name} [options] arguments
      Function to allow moving around to saved directories.  Arguments are:
      a       Adds current directory to list
      e       Edits list
      g n     Goes to the nth directory.  If n is not a number, it is a
              string that is a shorthand description and is separated
              from the optional description by a ! character.
      -t      Checks each directory in the file
      -T      Checks all directory in the file, even those commented out
      -s      Print silent link names
      S       Search all lines in the config file for a string
      s       Search the active lines in the config file for a string
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-t"] = False
        d["-T"] = False
        d["-s"] = False
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "tTsh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("tTs"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        return args
if 1:   # Core functionality
    def GetFile(all=False):
        '''Read in the goto file.  If all is True, include the commented
        out lines.
        '''
        r = None if all else ["^ *#"]
        lines = get.GetLines(G.gotorc, regex=r)
        from pprint import pprint as pp
        pp(lines)
        exit()
    def CheckFile():
        lines = GetFile(all=True if d["-T"] else False)
    def AddCurrentDirectory():
        raise Exception("Need to implement")
    def EditFile():
        raise Exception("Need to implement")
    def GoTo(args):
        raise Exception("Need to implement")
    def SearchLines(cmd):
        raise Exception("Need to implement")
    def ExecuteCommand(cmd, args):
        if d["-t"] or d["-T"]:
            CheckFile()
        if cmd == "a":
            AddCurrentDirectory()
        elif cmd == "e":
            EditFile()
        elif cmd == "g":
            GoTo(args[1:])
        elif cmd in ("s", "S"):
            SearchLines(cmd)    
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        cmd, other = "", []
    elif len(args) == 1:
        cmd, other = args[0], []
    else:
        cmd, other = args[0], args[1:]
    ExecuteCommand(cmd, other)
