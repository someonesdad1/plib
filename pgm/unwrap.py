"""

Todo
    - No args means print -h output
    - Use '-' to read from stdin

Convert a text file to word processor form
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Convert text file to word processor form
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import re
    import sys
    from io import StringIO
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent

    # Global variables
    ii = isinstance

    class G:
        pass

    g = G()
    g.nl = "\n"
    # The following string is used to flag locations of verbatim text
    # in the processed data.  It must not appear in regular text when
    # followed by the string representation of an integer.
    g.key_start = "\x00key"
    # Abbreviations and titles need one space after them.
    g.abbreviations = """
            a acad acc acct ad addr adj adv al alt approx apr assn asst at
            attn aug ave b betw bros c ca cal cca cent cf ch chas chem cit
            cm co conc corp cp ct ctrl cu cwt d dec dept devt diff dist div
            dwt e ea ed edn encl eng esp esq est et etc ex exc f feb fem ff
            fig fl flor ft fwd g gal govt grad h hr hrs ht i ibid id impt
            in inc info inv irreg j jan jr jul jun k l lat lb lib litt long
            loq m mar masc mass max may meas mech med min misc movt mts n
            nat naut no nov o obj oct op orig oz p para pc pcs phys pl pop
            poss pp ppl prep prob pron prox pseud pt pub q qtr r rd ref
            refl reg rev s sc scil sec sep sept seq ser sic sing so sp sq
            sr st stat syn t tbsp tem temp thos tsp u ult univ unkn v var
            vb viz vol vols vs vt vulg w wk wm wt x y yd yr yrs z
        """
    g.titles = """
            capt col comdr cpl dr gen gov hon lt maj mme mr mrs ms mt prof
            pvt sgt ste
        """
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        name = sys.argv[0]
        colon = d["-k"]
        bl = d["-p"]
        ns = d["-s"]
        on, off = d["verbatim_begin"].strip(), d["verbatim_end"].strip()
        print(
            dedent(
                f"""
        Usage:  {name} [options] [file1 [file2]]
          Removes hard line breaks from input text so that paragraphs are
          indicated by one newline.  The use case is to change text into a
          form suitable for importing into a word processor.  file 1 is the
          input text file and file2 is the output text file.  Read from
          stdin if no input file is given and send the results to stdout.
        
          A hyphenated word at the end of a line will be joined with the
          first word on the following line and the hyphen removed except if
          the word on the following line is capitalized (e.g., in a
          hyphenated name).
        
          Use {on} and {off} on their own lines to indicate a block of text
          that shouldn't be reformatted.
        
          Multiple spaces will be changed into one space character.
        Options:
            -h      Print this help message.
            -k n    Number of spaces after a colon. [{colon}]
            -n      Don't remove trailing newlines.
            -p n    Number of newlines after a paragraph. [{bl}]
            -s n    Number of spaces between sentences. [{ns}]
        """[1:-1]
            )
        )
        exit(status)

    def ParseCommandLine(d):
        d["-k"] = 2  # Number of spaces after colon
        d["-n"] = True  # Remove any trailing newlines
        d["-p"] = 0  # Newlines after paragraph
        d["-s"] = 2  # Number of spaces after sentence
        d["verbatim"] = {}
        d["verbatim_begin"] = "{{" + g.nl
        d["verbatim_end"] = "}}" + g.nl
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hk:np:s:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o == "-h":
                Usage(status=0)
            elif o in ("-k", "-p", "-s"):
                d[o] = int(a)
            elif o == "-n":
                d["-n"] = False
        # Set up input & output streams
        d["in"] = sys.stdin
        d["out"] = sys.stdout
        if not args:
            Usage()
        if len(args) == 1:
            if args[0] == "-":
                d["in"] = sys.stdin
            else:
                d["in"] = open(args[0], "r")
            d["out"] = sys.stdout
        elif len(args) == 2:
            d["in"] = open(args[0], "r")
            d["out"] = open(args[1], "w")
        # Build the set of abbreviations and titles
        d["abbreviations"] = set(g.abbreviations.split())
        d["titles"] = set(g.titles.split())
        return args


if 0:

    def GetStringFromClipboard():  # Input from clipboard
        if have_gtk:
            cb = gtk.clipboard_get()
            s = cb.wait_for_text()
        elif have_windows:
            win32clipboard.OpenClipboard()
            s = win32clipboard.GetClipboardData(win32con.CF_TEXT)
            win32clipboard.CloseClipboard()
        else:
            Error("No clipboard connection")
        return s

    def SendStringToClipboard(s):
        if have_gtk:
            clipboard = gtk.clipboard_get()
            clipboard.set_text(s)
            clipboard.store()
        elif have_windows:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(s)
            win32clipboard.CloseClipboard()


if 1:  # Core functionality

    def CheckVerbatimBlockMarks(d):
        """Verify there's an equal number of beginning and ending block
        marks.
        """
        s, b, e = d["text"], d["verbatim_begin"], d["verbatim_end"]
        n_begin = s.count(b)
        n_end = s.count(e)
        if n_begin != n_end:
            b, e = b.strip(), e.strip()
            msg = "Unmatched verbatim block markers '{b}' and '{e}'"
            Error(msg.format(**locals()))

    def RemoveVerbatimBlocks(d):
        """Remove the verbatim blocks from the input string and replace
        them with tokens that we can use to put them back in later.
        """
        CheckVerbatimBlockMarks(d)
        d["verbatim"] = {}
        # Make a regular expression that can be used to remove the blocks.
        b, e = d["verbatim_begin"], d["verbatim_end"]
        r = re.compile(
            r"""
            {0}     # Match the verbatim_begin string
            (.*?)   # Non-greedy match of everything; put in group
            {1}     # Match the verbatim_end string
        """.format(b, e),
            re.S | re.X,
        )
        count = 0
        while True:
            count += 1
            key = "{0}{1}".format(g.key_start, count)
            mo = r.search(d["text"])
            if mo:
                s, e = mo.start(), mo.end()
                assert len(mo.groups()) == 1
                d["verbatim"][key] = mo.groups()[0]
                # Remove the found string and replace it with the key.
                # Note we make sure that the verbatim string is a separate
                # paragraph by surrounding it with multiple newlines.
                t = [d["text"][:s], 2 * g.nl, key, 2 * g.nl, d["text"][e:]]
                d["text"] = "".join(t)
            else:
                break

    def EndsInHyphen(word):
        """This function is present to allow you to use other characters to
        indicate hyphenation.  For example, the Unicode code points U+2010
        and U+2011 might be considered hyphens also.
        """
        return word[-1] in "-"

    def EndsInColon(word):
        return word[-1] == ":"

    def IsEndOfSentence(word):
        return word[-1] == "."

    def IsAbbreviationOrTitle(word, next_word, d):
        """word ends in '.'; return True if it's an abbreviation or title
        and, thus, doesn't require an extra space after it because it's not
        the end of a sentence.
        """
        assert word[-1] == "."
        w = word[:-1].lower()
        is_capital = ord("A") <= ord(next_word[0]) <= ord("Z")
        # Handle a.m. and p.m. specially
        if w in ("a.m.", "p.m."):
            return not is_capital
        if w in d["abbreviations"]:
            return True
        if w in d["titles"]:
            return is_capital
        return False

    def ProcessParagraph(p):
        """Convert a paragraph p to a sequence of words and join by spaces.
        Unhyphenate words that end in a hyphen character.
        """
        words, q = p.replace(g.nl, " ").split(), []
        n = len(words)
        had_hyphen = False
        for i, word in enumerate(words):
            if had_hyphen:
                # This word was processed already because the previous word
                # was hyphenated.
                had_hyphen = False
                continue
            if EndsInHyphen(word) and i < n - 1:
                had_hyphen = True
                next_word = words[i + 1]
                first_char = next_word[0]
                if ord("A") <= ord(first_char) <= ord("Z"):
                    # Next word is capitalized, so leave hyphen in place.
                    q.append(word + next_word)
                else:
                    # Remove the hyphen and join the next word.
                    q.append(word[:-1] + next_word)
            elif EndsInColon(word):
                # We subtract one space because of the space character
                # which will be inserted at the end of this function.
                q.append(word + " " * (d["-k"] - 1))
            elif IsEndOfSentence(word):
                # We only need to do further processing if the -s option is
                # not 1 space.
                if d["-s"] != 1:
                    # This can either be a true end of sentence or an
                    # abbreviation/title.
                    if i < n - 1:  # Next word exists
                        next_word = words[i + 1]
                        if IsAbbreviationOrTitle(word, next_word, d):
                            q.append(word)
                        else:
                            # We subtract one space because of the space
                            # character which will be inserted at the end
                            # of this function.
                            q.append(word + " " * (d["-s"] - 1))
                    else:
                        q.append(word)
                else:
                    q.append(word)
            else:
                q.append(word)
        return " ".join(q)

    def GetText():
        "Read input stream's data"
        d["text"] = d["in"].read()

    def GetParagraphs(d):
        "Generator to split the input text into paragraphs"
        r = re.compile(r"\n\n+", re.S)
        for i in r.split(d["text"]):
            yield i


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    GetText()
    RemoveVerbatimBlocks(d)
    paragraphs = []
    for paragraph in GetParagraphs(d):
        p = ProcessParagraph(paragraph)
        # Replace with verbatim text if appropriate
        key = p.strip()
        if key in d["verbatim"]:
            p = d["verbatim"][key].strip(g.nl)
        paragraphs.append(p)
    # Join the paragraphs into a single string
    n = max(1, d["-p"])
    s = (g.nl * n).join(paragraphs)
    # Remove trailing newlines
    if d["-n"]:
        s = s.rstrip(g.nl)
    # Send to the output stream
    print(s, file=d["out"])
