"""
TODO

- Need two spaces after ., : and end of quoted sentences like ?",
  .", !", etc.  Need to handle abbreviations for these cases too.

- PNP shows numerous sentence endings or places that would be good for
  an extra space:
    ?"    ."    !"    ,"    .'"    ,'    ;"    :"


Comments:  the algorithm works, but I think I'd rather see random
location of the extra spaces rather than starting at the beginning of
the line.  Justify PNP to 79 spaces and you'll see why.

"""

# ∞test∞# ignore #∞test∞#
if 1:
    from abbreviations import IsAbbreviation
    from dpstr import KeepFilter
    import string

    punctuation = set(string.punctuation)
    letters = set(string.ascii_letters)
    letters.update(set("_-"))
    ii = isinstance


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
    """Block justify the paragraphs in string s and return them.  The
    paragraphs are separated by the string brk.
    """
    paragraphs = [JustifyParagraph(i, width) for i in s.split(brk)]
    return brk.join(paragraphs)


if 1:
    s = open("pnp").read()
    print(Justify(s, 79), end="")
    exit()

if 0:
    keep = KeepFilter(punctuation)
    s = open("big.txt").read()
    TokenEnds(s)
    exit()
