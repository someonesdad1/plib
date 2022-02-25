'''
Script to output Mac keyboard commands in various ways
'''

 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
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
    import os
    import pathlib
    import sys
    import enum
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from color import C
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    # Ignore lines with comments
    # '.' in first column denotes a topic heading
    # ',' in first column denotes an informational heading
    # ';' in non-first column indicates modifying text for that topic
    # Indentation implies material associated with the heading
    data = dedent('''
    ,Mac keyboard shortcuts including modifier keys:
                        Mac         Windows keyboard
        Command         ⌘               Windows key
        Shift           ⇧
        Option          ⌥               Alt
        Control (or Ctrl) ⌃
        Caps Lock ⇪
        Fn
        Publication Date: January 11, 2021
    .Cut, copy, paste, and other common shortcuts
        Command-X: Cut the selected item and copy it to the Clipboard.
        Command-C: Copy the selected item to the Clipboard. This also works for files in the Finder.
        Command-V: Paste the contents of the Clipboard into the current document or app. This also works for files in the Finder.
        Command-Z: Undo the previous command. You can then press Shift-Command-Z to Redo, reversing the undo command. In some apps, you can undo and redo multiple commands.
        Command-A: Select All items.
        Command-F: Find items in a document or open a Find window.
        Command-G: Find Again: Find the next occurrence of the item previously found. To find the previous occurrence, press Shift-Command-G.
        Command-H: Hide the windows of the front app. To view the front app but hide all other apps, press Option-Command-H.
        Command-M: Minimize the front window to the Dock. To minimize all windows of the front app, press Option-Command-M.
        Command-O: Open the selected item, or open a dialog to select a file to open.
        Command-P: Print the current document.
        Command-S: Save the current document.
        Command-T: Open a new tab.
        Command-W: Close the front window. To close all windows of the app, press Option-Command-W.
        Option-Command-Esc: Force quit an app.
        Command-Space bar: Show or hide the Spotlight search field. To perform a Spotlight search from a Finder window, press Command-Option-Space bar. (If you use multiple input sources to type in different languages, these shortcuts change input sources instead of showing Spotlight. Learn how to change a conflicting keyboard shortcut.)
        Control-Command-Space bar: Show the Character Viewer, from which you can choose emoji and other symbols.
        Control-Command-F: Use the app in full screen, if supported by the app.
        Space bar: Use Quick Look to preview the selected item.
        Command-Tab: Switch to the next most recently used app among your open apps. 
        Shift-Command-5: In macOS Mojave or later, take a screenshot or make a screen recording. Or use Shift-Command-3 or Shift-Command-4 for screenshots. Learn more about screenshots.
        Shift-Command-N: Create a new folder in the Finder.
        Command-Comma (,): Open preferences for the front app.
    .Sleep, log out, and shut down shortcuts
        ;You might need to press and hold some of these shortcuts for slightly longer than other shortcuts. This helps you to avoid using them unintentionally.
        ;* Does not apply to the Touch ID sensor.
        Power button: Press to turn on your Mac or wake it from sleep. Press and hold for 1.5 seconds to put your Mac to sleep.* Continue holding to force your Mac to turn off.
        Option-Command-Power button* or Option-Command-Media Eject : Put your Mac to sleep.
        Control-Shift-Power button* or Control-Shift-Media Eject : Put your displays to sleep.
        Control-Power button* or Control-Media Eject : Display a dialog asking whether you want to restart, sleep, or shut down.
        Control-Command-Power button:* Force your Mac to restart, without prompting to save any open and unsaved documents.
        Control-Command-Media Eject : Quit all apps, then restart your Mac. If any open documents have unsaved changes, you will be asked whether you want to save them.
        Control-Option-Command-Power button* or Control-Option-Command-Media Eject : Quit all apps, then shut down your Mac. If any open documents have unsaved changes, you will be asked whether you want to save them.
        Control-Command-Q: Immediately lock your screen.
        Shift-Command-Q: Log out of your macOS user account. You will be asked to confirm. To log out immediately without confirming, press Option-Shift-Command-Q.
    .Finder and system shortcuts
        Command-D: Duplicate the selected files.
        Command-E: Eject the selected disk or volume.
        Command-F: Start a Spotlight search in the Finder window.
        Command-I: Show the Get Info window for a selected file.
        Command-R: (1) When an alias is selected in the Finder: show the original file for the selected alias. (2) In some apps, such as Calendar or Safari, refresh or reload the page. (3) In Software Update preferences, check for software updates again.
        Shift-Command-C: Open the Computer window.
        Shift-Command-D: Open the desktop folder.
        Shift-Command-F: Open the Recents window, showing all of the files you viewed or changed recently.
        Shift-Command-G: Open a Go to Folder window.
        Shift-Command-H: Open the Home folder of the current macOS user account.
        Shift-Command-I: Open iCloud Drive.
        Shift-Command-K: Open the Network window.
        Option-Command-L: Open the Downloads folder.
        Shift-Command-N: Create a new folder.
        Shift-Command-O: Open the Documents folder.
        Shift-Command-P: Show or hide the Preview pane in Finder windows.
        Shift-Command-R: Open the AirDrop window.
        Shift-Command-T: Show or hide the tab bar in Finder windows. 
        Control-Shift-Command-T: Add selected Finder item to the Dock (OS X Mavericks or later)
        Shift-Command-U: Open the Utilities folder.
        Option-Command-D: Show or hide the Dock. 
        Control-Command-T: Add the selected item to the sidebar (OS X Mavericks or later).
        Option-Command-P: Hide or show the path bar in Finder windows.
        Option-Command-S: Hide or show the Sidebar in Finder windows.
        Command-Slash (/): Hide or show the status bar in Finder windows.
        Command-J: Show View Options.
        Command-K: Open the Connect to Server window.
        Control-Command-A: Make an alias of the selected item.
        Command-N: Open a new Finder window.
        Option-Command-N: Create a new Smart Folder.
        Command-T: Show or hide the tab bar when a single tab is open in the current Finder window.
        Option-Command-T: Show or hide the toolbar when a single tab is open in the current Finder window.
        Option-Command-V: Move the files in the Clipboard from their original location to the current location.
        Command-Y: Use Quick Look to preview the selected files.
        Option-Command-Y: View a Quick Look slideshow of the selected files.
        Command-1: View the items in the Finder window as icons.
        Command-2: View the items in a Finder window as a list.
        Command-3: View the items in a Finder window in columns. 
        Command-4: View the items in a Finder window in a gallery.
        Command-Left Bracket ([): Go to the previous folder.
        Command-Right Bracket (]): Go to the next folder.
        Command-Up arrow: Open the folder that contains the current folder.
        Command-Control-Up arrow: Open the folder that contains the current folder in a new window.
        Command-Down arrow: Open the selected item.
        Right arrow: Open the selected folder. This works only when in list view.
        Left arrow: Close the selected folder. This works only when in list view.
        Command-Delete: Move the selected item to the Trash.
        Shift-Command-Delete: Empty the Trash.
        Option-Shift-Command-Delete: Empty the Trash without confirmation dialog.
        Command-Brightness Down: Turn video mirroring on or off when your Mac is connected to more than one display.
        Option-Brightness Up: Open Displays preferences. This works with either Brightness key.
        Control-Brightness Up: Change the brightness of your external display, if supported by your display.
        Control-Brightness Down: Change the brightness of your external display, if supported by your display.
        Option-Shift-Brightness Up: Adjust the display brightness in smaller steps. Add the Control key to this shortcut to make the adjustment on your external display, if supported by your display.
        Option-Shift-Brightness Down: Adjust the display brightness in smaller steps. Add the Control key to this shortcut to make the adjustment on your external display, if supported by your display.
        Option-Mission Control: Open Mission Control preferences.
        Command-Mission Control: Show the desktop. 
        Control-Down arrow: Show all windows of the front app.
        Option-Volume Up: Open Sound preferences. This works with any of the volume keys.
        Option-Shift-Volume Up: Adjust the sound volume in smaller steps.
        Option-Shift-Volume Down: Adjust the sound volume in smaller steps.
        Option-Keyboard Brightness Up: Open Keyboard preferences. This works with either Keyboard Brightness key.
        Option-Shift-Keyboard Brightness Up: Adjust the keyboard brightness in smaller steps.
        Option-Shift-Keyboard Brightness Down: Adjust the keyboard brightness in smaller steps.
       #Option key while double-clicking: Open the item in a separate window, then close the original window.
       #Command key while double-clicking: Open a folder in a separate tab or window.
       #Command key while dragging to another volume: Move the dragged item to the other volume, instead of copying it. 
       #Option key while dragging: Copy the dragged item. The pointer changes while you drag the item.
       #Option-Command while dragging: Make an alias of the dragged item. The pointer changes while you drag the item.
       #Option-click a disclosure triangle: Open all folders within the selected folder. This works only when in list view.
       #Command-click a window title: See the folders that contain the current folder.
        ;Learn how to use Command or Shift to select multiple items in the Finder. 
        ;Click the Go menu in the Finder menu bar to see shortcuts for opening many commonly used folders, such as Applications, Documents, Downloads, Utilities, and iCloud Drive.
    .Document shortcuts
        ;The behavior of these shortcuts may vary with the app you're using.
        Command-B: Boldface the selected text, or turn boldfacing on or off. 
        Command-I: Italicize the selected text, or turn italics on or off.
        Command-K: Add a web link.
        Command-U: Underline the selected text, or turn underlining on or off.
        Command-T: Show or hide the Fonts window.
        Command-D: Select the Desktop folder from within an Open dialog or Save dialog.
        Control-Command-D: Show or hide the definition of the selected word.
        Shift-Command-Colon (:): Display the Spelling and Grammar window.
        Command-Semicolon (;): Find misspelled words in the document.
        Option-Delete: Delete the word to the left of the insertion point.
        Control-H: Delete the character to the left of the insertion point. Or use Delete.
        Control-D: Delete the character to the right of the insertion point. Or use Fn-Delete.
        Fn-Delete: Forward delete on keyboards that don't have a Forward Delete   key. Or use Control-D.
        Control-K: Delete the text between the insertion point and the end of the line or paragraph.
        Fn-Up arrow: Page Up: Scroll up one page. 
        Fn-Down arrow: Page Down: Scroll down one page.
        Fn-Left arrow: Home: Scroll to the beginning of a document.
        Fn-Right arrow: End: Scroll to the end of a document.
        Command-Up arrow: Move the insertion point to the beginning of the document.
        Command-Down arrow: Move the insertion point to the end of the document.
        Command-Left arrow: Move the insertion point to the beginning of the current line.
        Command-Right arrow: Move the insertion point to the end of the current line.
        Option-Left arrow: Move the insertion point to the beginning of the previous word.
        Option-Right arrow: Move the insertion point to the end of the next word.
        Shift-Command-Up arrow: Select the text between the insertion point and the beginning of the document.
        Shift-Command-Down arrow: Select the text between the insertion point and the end of the document.
        Shift-Command-Left arrow: Select the text between the insertion point and the beginning of the current line.
        Shift-Command-Right arrow: Select the text between the insertion point and the end of the current line.
        Shift-Up arrow: Extend text selection to the nearest character at the same horizontal location on the line above.
        Shift-Down arrow: Extend text selection to the nearest character at the same horizontal location on the line below.
        Shift-Left arrow: Extend text selection one character to the left.
        Shift-Right arrow: Extend text selection one character to the right.
        Option-Shift-Up arrow: Extend text selection to the beginning of the current paragraph, then to the beginning of the following paragraph if pressed again.
        Option-Shift-Down arrow: Extend text selection to the end of the current paragraph, then to the end of the following paragraph if pressed again.
        Option-Shift-Left arrow: Extend text selection to the beginning of the current word, then to the beginning of the following word if pressed again.
        Option-Shift-Right arrow: Extend text selection to the end of the current word, then to the end of the following word if pressed again.
        Control-A: Move to the beginning of the line or paragraph.
        Control-E: Move to the end of a line or paragraph.
        Control-F: Move one character forward.
        Control-B: Move one character backward.
        Control-L: Center the cursor or selection in the visible area.
        Control-P: Move up one line.
        Control-N: Move down one line.
        Control-O: Insert a new line after the insertion point.
        Control-T: Swap the character behind the insertion point with the character in front of the insertion point.
        Command-Left Curly Bracket ({): Left align.
        Command-Right Curly Bracket (}): Right align.
        Shift-Command-Vertical bar (|): Center align.
        Option-Command-F: Go to the search field. 
        Option-Command-T: Show or hide a toolbar in the app.
        Option-Command-C: Copy Style: Copy the formatting settings of the selected item to the Clipboard.
        Option-Command-V: Paste Style: Apply the copied style to the selected item.
        Option-Shift-Command-V: Paste and Match Style: Apply the style of the surrounding content to the item pasted within that content.
        Option-Command-I: Show or hide the inspector window.
        Shift-Command-P:  Page setup: Display a window for selecting document settings.
        Shift-Command-S: Display the Save As dialog, or duplicate the current document.
        Shift-Command-Minus sign (-): Decrease the size of the selected item.
        Shift-Command-Plus sign (+): Increase the size of the selected item. Command-Equal sign (=) performs the same function.
        Shift-Command-Question mark (?): Open the Help menu.
    ,Other shortcuts
        ;For more shortcuts, check the shortcut abbreviations shown in the menus of your apps. Every app can have its own shortcuts, and shortcuts that work in one app might not work in another. 
    ''')
    # Ignore lines with comments
    # '.' in first column denotes a topic heading
    # ',' in first column denotes an informational heading
    # ';' in non-first column indicates modifying text for that topic
    # Indentation implies material associated with the heading
    if 1:   # Use this for debugging
        data = dedent('''
        ,Mac keyboard shortcuts including modifier keys:
            Command         ⌘               Windows key
            Shift           ⇧
        .Cut, copy, paste, and other common shortcuts
            Command-X: Cut the selected item and copy it to the Clipboard.
            Command-C: Copy the selected item to the Clipboard. This also works for files in the Finder.
        .Sleep, log out, and shut down shortcuts
            ;You might need to press and hold some of these shortcuts for slightly longer than other shortcuts. This helps you to avoid using them unintentionally.
            ;* Does not apply to the Touch ID sensor.
            Power button: Press to turn on your Mac or wake it from sleep. Press and hold for 1.5 seconds to put your Mac to sleep.* Continue holding to force your Mac to turn off.
            Option-Command-Power button* or Option-Command-Media Eject : Put your Mac to sleep.
        .Finder and system shortcuts
            Command-D: Duplicate the selected files.
            Shift-Command-C: Open the Computer window.
            Control-Shift-Command-T: Add selected Finder item to the Dock (OS X Mavericks or later)
        .Document shortcuts
            ;The behavior of these shortcuts may vary with the app you're using.
            Shift-Command-Down arrow: Select the text between the insertion point and the end of the document.
        ,Other shortcuts
            ;For more shortcuts, check the shortcut abbreviations shown in the menus of your apps. Every app can have its own shortcuts, and shortcuts that work in one app might not work in another. 
        ''')
if 1:   # Classes and types
    class KeyCmd:
        def __init__(self, key, descr):
            self.key = key
            self.descr = descr
            self._sym = {
                "Command": "⌘",
                "Shift": "￪",
                "Option": "⌥",
                "Control": "^",
                "Down arrow": "▼",
                "Up arrow": "▲",
                "Left arrow": "◀",
                "Right arrow": "▶",

                "Brightness Up": "Brt▲",
                "Brightness Down": "Brt▼",
                "Keyboard Brightness Up": "KbdBrt▲",
                "Keyboard Brightness Down": "KbdBrt▼",
                "Volume Up": "Vol▲",
                "Volume Down": "Vol▼",
                "Mission Control": "MisCtrl",

                "Left Bracket": "[",
                "Right Bracket": "]",
                "Left Curly Bracket": "{",
                "Right Curly Bracket": "}",
                "Colon": ":",
                "Semicolon": ";",
                "Comma": ",",
                "Vertical bar": "|",
                "Minus sign": "-",
                "Plus sign": "+",
                "Question mark": "?",
                "Delete": "Del",
                "Slash": "/",
                "Power button": "Pwr",
                "Space bar": "Spc",
            }
        def __str__(self):
            #return self.symbol()
            return self.decorate()
        def symbol(self):
            'Return the key name symbol'
            f = self.key.split("-")
            if self.key == "Shift-Command-Down Arrow": xx() #xx
            for item in f:
                i = item.strip()
                items.append(d[i] if i in d else i)
        def decorate(self):
            "Return the name with the key's symbols"
            items = [f"{self.key:40s}{' '*5}"]
            f = self.key.split("-")
            if self.key == "Shift-Command-Down Arrow": xx() #xx
            for item in f:
                i = item.strip()
                items.append(self._sym[i] if i in self._sym else i)
            return ''.join(items)
                    
    class State(enum.Enum):
        ignore = enum.auto()
        topic = enum.auto()
        modifier = enum.auto()
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def FixLine(line):
        '''Remove '(x)' where x is one of the repl characters
        '''
        repl = ",;:/[]{}+-?|"
        for i in repl:
            s = f"({i})"
            if s in line:
                line = line.replace(s, "")
        return line
    def ProcessData():
        'Return a list of the key objects'
        state = State.ignore
        keys = []
        for line in data.split("\n"):
            if line.startswith("."):
                state = State.topic
                continue
            elif line.startswith(","):
                state = State.ignore
                continue
            elif line.strip().startswith(";") or line.strip().startswith("#"):
                continue
            if state == State.ignore:
                continue
            line = FixLine(line)
            # Some keys aren't appropriate for the latest Macbook Pro
            if "Media Eject" in line:
                continue
            # Find the first ':' and split the line on it
            loc = line.find(":")
            if loc == -1:
                print(f"Bad line:  '{line.split()}'")
                exit(1)
            name = line[:loc]
            value = line[loc:]
            if "*" in name:
                continue
            key = KeyCmd(name, value)
            keys.append(key)
        return keys

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    keys = ProcessData()
    # Show some output
    for key in keys:
        print(key)
