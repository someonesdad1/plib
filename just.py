if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Block justify a string oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2020 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
            
            - Comments:  the algorithm works, but I think I'd rather see random location
              of the extra spaces rather than starting at the beginning of the line.
              Justify PNP to 79 spaces and you'll see why.

            - Need two spaces after '.' and ':' and end of quoted sentences like ?", .", !",
              etc.  Need to handle abbreviations for these cases too.
            
            - PNP shows numerous sentence endings or places that would be good for an
              extra space: ?"    ."    !"    ,"    .'"    ,'    ;"    :"
            
        oo>
    '''
    if 1:  # Standard imports
        import string
    if 1:  # Custom imports
        from abbreviations import IsAbbreviation
    if 1:  # Global variables
        punctuation = set(string.punctuation)
        letters = set(string.ascii_letters)
        letters.update(set("_-"))
if 1:  # Core functionality
    def JustifyParagraph(s, width):
        "Block justify string s into width width  and return it"
        # Modified by DP; the original algorithm had a couple of bugs that
        # show up when you test at corner cases like width == 1.  Also added
        # extra stuff for end of sentence and colon.
        # From https://medium.com/@dimko1/text-justification-63f4cda29375
        def ew(x, y):
            "Return True if string x ends with string y"
            return x.endswith(y)
        out, line, num_of_letters = [], [], 0
        for w in s.split():
            if not IsAbbreviation(w) and (
                ew(w, ".") or ew(w, "!") or ew(w, "?") or ew(w, ":")
            ):
                w = w + " "
            if num_of_letters + len(w) + len(line) > width:
                spaces_to_add = max(width - num_of_letters, 0)
                # The following avoids a divide by zero when width is small
                ws_amount = max(len(line) - 1, 1)
                for i in range(spaces_to_add):
                    # When width is small, line can be empty and the
                    # mod results in an exception
                    if line:
                        line[i % ws_amount] += " "
                out.append("".join(line))
                line, num_of_letters = [], 0
            line.append(w)
            num_of_letters += len(w)
        # I want last line to not have trailing spaces
        out.append(" ".join(line))
        return "\n".join(out)
    def Justify(s, width, brk="\n\n"):
        '''Block justify the paragraphs in string s and return them.  The
        paragraphs are separated by the string brk.
        '''
        paragraphs = [JustifyParagraph(i, width) for i in s.split(brk)]
        return brk.join(paragraphs)

if __name__ == "__main__":
    s = open("pnp").read()
    print(Justify(s, 79), end="")
    exit()
