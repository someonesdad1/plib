'''

ToDo
    - Estimate number of bits in each set of words

Script to generate easier-to-remember passwords than modern "recommendations"

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Questions to help generate a password
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        import getopt
        import math
        import os
        import random
        import secrets
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t 
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Global variables as attributes to this instance
        g.words = (
            P("/words/words.ef.3000"),
            P("/words/words.beale.2of12inf"),
            P("/words/words.ngsl.experimental"),
            P("/words/words.univ"),
        )
        g.wordlist = None
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''

        Thoughts
            - Also see /plib/pgm/random_phrase.py.  This can build phrases easier to remember
              because you can e.g. specify 'ad v a n' on the command line, saying you want an
              adverb followed by a verb followed by an adjective followed by a noun.  
                - Example output:
                    - unblushingly dado secretory sickroom
                    - forever twiddle famished Phyllostachys
                    - disgustingly shoulder hunched rink
                    - seaward gun dissipated megasporangium
                    - wrongheadedly teethe entitled convulsion
                - This uses words from Wordnet 3.1, which is a fairly large set of words.  Such
                  things can result in words the average person won't recognize, such as
                  'Phyllostachys' or 'megasporangium'.

            - An attacker won't know the number of symbols used nor the length of the password.
              Since these passwords are composed of English words, their number of bits is far
              smaller than e.g. random bytes or even the 95 usual ASCII characters.
                - https://en.wikipedia.org/wiki/Rainbow_table#Example states that using a PC to
                  crack an 8 character password in lowercase letters is completely feasible(1e12
                  hashes), but a 16 character password in lowercase letters is completely
                  inveasible (1e25 hashes).
                    - Precomputed rainbow tables:  For older Unix passwords which used a 12-bit
                      salt this would require 4096 tables, a significant increase in cost for the
                      attacker, but not impractical with terabyte hard drives. The SHA2-crypt and
                      bcrypt methods—used in Linux, BSD Unixes, and Solaris—have salts of 128
                      bits.[4] These larger salt values make precomputation attacks against these
                      systems infeasible for almost any length of a password. Even if the attacker
                      could generate a million tables per second, they would still need billions of
                      years to generate tables for all possible salts.

            - The number of symbols in the wordlists vary:  -0:47, -1:26, -2:29, -3:63.  These will
              strongly impact the assessed number of bits in the passwords.
            - The default wordlist is -0 and I recommend this for passwords that more easily
              remembered.  The remaining wordlists contain more complex words.  The -3 option will
              probably have many unfamiliar words.
            - I recommend using a password safe to store your passwords.  Then you only have to
              memorize one good password to open up the password safe.  
            - For important stuff (e.g. banking, retirement account, etc.) use high-strength
              passwords generated by your password generator.
            - For passwords that you need to remember for things you can't easily keep on your
              computer, the sets of words generated by this script might be useful.  I wouldn't
              hesitate to permute the words to make the thing easier to remember.
            - Another technique is to shift your hands up one row on the keyboard.  This makes the
              word "randomly selected" come out as "4qhe9joy w3o3d53e".
            - I recommend you stick with the -0 word list, as you'll get more familiar words that
              should be easier to remember.
            - I had a friend in the 1980's who had the initials GE, so he used the phrase "we bring
              good things to life", which was (and might still be) an advertising slogan from GE.
              He told me he then used the first letters of the words to get "wbgttl" for a short
              password that was easy to remember.  Of course, telling me his password wasn't a very
              good security practice. :^)
                - You can make up a memorable word phrase and do the same thing, then putting some
                  characters like comma, colon, semicolon, etc. into the abbreviation.  For
                  example, in the old days some coffee company used the phrase "Jim never has a
                  second cup of coffee" (it might have been Folgers).  This would abbeviate to
                  'jnhascoc'.  Take your birthday and insert its factors.  Example:  my mother's
                  birthday was 2/22/1926.  Change this to the integer 22226 and factor it to get
                  2*11113, then just remember there are only two factors, so you can factor it in
                  your head because it's even.  Then you could have the password '2*11113jnhascoc',
                  a fairly good password.

        The cartoon https://xkcd.com/936/ pokes fun at humans' attempt to make secure passwords.
        As computers keep getting faster, they can more easily be used to crack passwords on
        systems by brute force searching.  Just as problematic, humans are often lax at password
        security, even if they have good passwords.  A good example is the secretary who can't
        remember the password he/she needs, so writes it on a Post-It note and puts it on the
        computer monitor.

        The trouble is caused by our inability to remember secure passwords like
        'fw2Sn,ZBzxYNdAH2KASPRkKl0jKelO0m', a random password of 32 characters generated by the
        password manager I use, which labeled this password as having 180 bits.  This problem is
        compounded by the large number of passwords we need today.

        One technique is to generate a set of words that you can remember.  This script does this
        for you, selecting from various lists of words.  



        '''))
        exit()
    def Usage():
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] numwords [numlines [maxchars [minchars]]]
          Print line(s) containing numwords randomly selected from a wordlist.  Optional arguments:
            numlines = number of lines to print
            maxchars = maximum number of characters allowed in words
            minchars = minimum number of characters allowed in words
          If you want to constrain only the minimum number of characters, set maxchars to '-' and
          set minchars appropriately.  The output is random and not repeatable unless you use the
          -s option.
        Options:
            -0      Simple wordlist (3000 words) [default]
            -1      Moderately-sized wordlist (16378 words)
            -2      Large list of words from Alan Beale (81882 words)
            -3      Complex wordlist (302618 words)
            -h      Print a manpage
            -s st   Define seed string st to use repeatable pseudorandom generator
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-s"] = None      # Random number seed; implies pseudorandom number generator
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0123hs:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o[1] in list("0123"):
                g.wordlist = int(o[1])
            elif o == "-h":
                Manpage()
            elif o in ("-s",):
                d["-s"] = a
        if g.wordlist is None:
            g.wordlist = 0
        return args
if 1:   # Core functionality
    def CheckParameters(numwords, numlines, maxchars, minchars):
        if numwords < 1:
            Error("numwords must be an integer > 0")
        if numlines < 1:
            Error("numlines must be an integer > 0")
        if minchars < 1:
            Error("minchars must be an integer > 0")
        if maxchars < minchars:
            Error("maxchars must be an integer > 0 and be larger than minchars")
    def GetBits(passwd: list, numsymbols: str):
        '''Estimate the number of bits in the list of words.  This will be int(log2(N**P)) where 
            N = number of possible symbols (numsymbols)
            P =  number of characters in ''.join(passwd)
        One can quibble about this calculation, as I've used the set of the actual characters in
        the password, not the population set that the actual set was drawn from.  I consider this
        reasonable, as the randomly selected items are from a word list, not randomly drawn from a
        large set of characters.  To be more correct, I could let N be the number of words in the
        wordlist.

        The basic purpose of this script is to produce passwords using groups of English words with
        the intent that such a password is probably easier for the average human to remember than
        something like 'QlN<^y;_[1416D]$NwSx?CKGou5v)vC}', produced by my password management
        software and labeled as having 191 bits, a very strong password.  

        I'd use the output of this script for things like a password for my NAS box or a wifi
        password at home.  I'd never use this output for something like a bank or financial
        account.  In fact, for such things I insist on two factor authorization.
        '''
        n = flt(numsymbols**len(''.join(passwd)))
        bits = int(round(math.log2(n), 0))
        if bits > 9999:
            bits = 9999
        elif bits < 1:
            bits = 1
        return bits
    def Calculate(numwords, numlines, maxchars, minchars):
        '''Print the indicated numbers of words
        numwords = number of words per line
        numlines = number of lines to print
        maxchars = maximum number of characters per word
        minchars = minimum number of characters per word
        '''
        # Get the word list
        file = g.words[g.wordlist]
        assert file.exists()
        with open(file) as f:
            words = [word.strip() for word in f]
            # Only keep words with lengths between minchars and maxchars
            words = [i for i in words if minchars <= len(i) <= maxchars]
        numsymbols = len(set(''.join(words)))   # Does not include the space character
        if d["-s"] is None:
            # Random selection, cannot be repeated
            for i in range(numlines):
                passwd = [secrets.choice(words) for i in range(numwords)]
                bits = GetBits(passwd, numsymbols)
                print(f"{t('lill')}[{bits:4d}]{t.n} {' '.join(passwd)}")
        else:
            # Pseudorandom number generator, same output for same seed
            random.seed(d["-s"])
            for linenum in range(numlines):
                passwd = []
                for i in range(numwords):
                    k = random.randint(0, len(words) - 1)
                    passwd.append(words[k])
                bits = GetBits(passwd, numsymbols)
                print(f"{t('lill')}[{bits:4d}]{t.n} {' '.join(passwd)}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    maxchars = 1000  # Much large number of characters than any word in wordlists
    args = ParseCommandLine(d)
    numwords = int(args[0])
    numlines = int(args[1]) if len(args) > 1 else 1
    if len(args) > 2 and args[2] != "-":
        maxchars = int(args[2])
    minchars = int(args[3]) if len(args) > 3 else 1
    CheckParameters(numwords, numlines, maxchars, minchars)
    Calculate(numwords, numlines, maxchars, minchars)
