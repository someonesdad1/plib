'''
Same as textwrap.py except uses dpstr.Len to calculate string length so
that ANSI escape strings are ignored in calculating string lengths.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Same as python's textwrap module except the length of strings
        # ignores ANSI escape sequences.
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import os
        from textwrap import TextWrapper as TextWrapperOrig
        from pdb import set_trace as xx
    # Custom imports
        from dpstr import Len
        from color import Color, TRM as t
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
class TextWrapper(TextWrapperOrig):
    '''This is the same as the textwrap.TextWrapper class except the
    method with calls to len had each occurrence replaced with Len.
    '''
    def _wrap_chunks(self, chunks):
        """_wrap_chunks(chunks : [string]) -> [string]
 
        Wrap a sequence of text chunks and return a list of lines of
        length 'self.width' or less.  (If 'break_long_words' is false,
        some lines may be longer than this.)  Chunks correspond roughly
        to words and the whitespace between them: each chunk is
        indivisible (modulo 'break_long_words'), but a line break can
        come between any two chunks.  Chunks should not have internal
        whitespace; ie. a chunk is either all whitespace or a "word".
        Whitespace chunks will be removed from the beginning and end of
        lines, but apart from that whitespace is preserved.
        """
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self.max_lines is not None:
            if self.max_lines > 1:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            if Len(indent) + Len(self.placeholder.lstrip()) > self.width:
                raise ValueError("placeholder too large for max width")
        # Arrange in reverse order so items can be efficiently popped
        # from a stack of chucks.
        chunks.reverse()
        while chunks:
            # Start the list of chunks that will make up the current line.
            # cur_len is just the length of all the chunks in cur_line.
            cur_line = []
            cur_len = 0
            # Figure out which static string will prefix this line.
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            # Maximum width for this line.
            width = self.width - Len(indent)
            # First chunk on line is whitespace -- drop it, unless this
            # is the very beginning of the text (ie. no lines started yet).
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]
            while chunks:
                l = Len(chunks[-1])
                # Can at least squeeze this chunk onto the current line.
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l
                # Nope, this line is full.
                else:
                    break
            # The current line is full, and the next chunk is too big to
            # fit on *any* line (not just this one).
            if chunks and Len(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
                cur_len = sum(map(Len, cur_line))
            # If the last chunk on this line is all whitespace, drop it.
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                cur_len -= Len(cur_line[-1])
                del cur_line[-1]
            if cur_line:
                if (self.max_lines is None or
                    Len(lines) + 1 < self.max_lines or
                    (not chunks or
                     self.drop_whitespace and
                     Len(chunks) == 1 and
                     not chunks[0].strip()) and cur_len <= width):
                    # Convert current line back to a string and store it in
                    # list of all lines (return value).
                    lines.append(indent + ''.join(cur_line))
                else:
                    while cur_line:
                        if (cur_line[-1].strip() and
                            cur_len + Len(self.placeholder) <= width):
                            cur_line.append(self.placeholder)
                            lines.append(indent + ''.join(cur_line))
                            break
                        cur_len -= Len(cur_line[-1])
                        del cur_line[-1]
                    else:
                        if lines:
                            prev_line = lines[-1].rstrip()
                            if (Len(prev_line) + Len(self.placeholder) <=
                                    self.width):
                                lines[-1] = prev_line + self.placeholder
                                break
                        lines.append(indent + self.placeholder.lstrip())
                    break
        return lines


from color import TRM as t
s = f'''Wrap a sequence of text chunks and return a list of lines of length 'self.width' or less.  (If {t('yell')}'break_long_words'{t.n} is false, some lines may be longer than this.)  Chunks correspond roughly to words and the whitespace between them: each chunk is indivisible (modulo 'break_long_words'), but a line break can come between any two chunks.  Chunks should not have internal whitespace; ie. a chunk is either all whitespace or a "word".  Whitespace chunks will be removed from the beginning and end of lines, but apart from that whitespace is preserved.'''
tw = TextWrapper()
print('\n'.join(tw.wrap(s)))
