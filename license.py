if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ List software licenses oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014, 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞
        
            - ∞∞3:  Move data in /pylib/licenses/analysis to /plib/data
                - Include URL & download data for the data
         
        oo>
    '''
    if 1:  # Standard imports
        import getopt
        import pathlib
        import re
        import shutil
        import sys
        import time
    if 1:  # Custom imports
        import trm
        import dptypes
        from wrap import dedent
        from license_data import licenses
    if 1:  # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        # The following are too short to warrant a separate header file
        g.short_choices = ("bsd", "mit", "pd", "wol", "rem")
        g.nl = "\n"
        with g:
            g.descr = {
                "afl3": "  Academic Free License 3.0",
                "apache2": "  Apache License 2.0",
                "bsd3": "  BSD 3-clause license",
                "ccsa4": "* Creative Commons Attribution-ShareAlike 4.0",
                "gpl2": "* GNU Public License version 2",
                "gpl3": "* GNU Public License version 3",
                "lgpl2": "- Lesser GNU Public License version 2.1",
                "lgpl3": "- Lesser GNU Public License version 3",
                "mit": "  MIT License",
                "nposl3": "* Non-Profit Open Software License 3.0",
                "osl3": "* Open Software License 3.0",
                "pd": "  Public domain release",
                "wol": "  Wide-open License",
            }
            g.analysis = dedent('''
                9 Aug 2014, updated 29 Jan 2020, updated 8 Feb 2026

                Software licenses are a confusing and complex topic.  Part of the
                complexity is the sheer number of licenses out in the wild.  I had
                never spent any time studying these licenses until in the last few
                days while I was writing this script.  I wanted to have a better
                understanding of some of the common open source licenses and make a
                more informed decision about what license(s) I should choose to
                release the free software I put on the web.

                At a high level, most of these licenses derive their "teeth" from a
                country's copyright laws.  In order for you to utilize these copyright
                laws and use a license to dictate how some copyrighted material may be
                used, you must own or control the copyrighted material.  That sounds
                pretty basic (it is), but it can get more complicated if you've e.g.
                included derivations of other people's code in your own code.

                Here are the things I decided I wanted a license to accomplish for me
                when I provide my free software and documents to the public:

                    - Let anyone use the stuff for any purpose they want.
                    - They must keep my copyright notice in the source code or document.
                    - If they modify it, they must put in a prominent message that it is
                    modified from the original so that it won't be interpreted as
                    something I wrote.
                    - I'm indemnified against damages from someone using my free stuff.
                    - Standardize on one of the standard open source licenses.

                A primary differentiator in open source software licenses is the
                notion of copyleft (also called reciprocity).  This is a
                characteristic of the license that requires the user release any
                derivations of the work under the same license as the original if they
                choose to release the source or a binary derived from it.  The basic
                intent is to keep free software free and not allow a person who makes
                a derived work to close the software's availability to others.

                    It is worth mentioning that you can change open source software
                    all you want and you're not required to include the modified
                    source code unless you distribute the modified work.  Thus, for
                    example, a large company could modify a complex open source
                    project heavily and use it internally to further their profit
                    objectives such by e.g. producing the items that they sell.
                    They're under no obligation to release that modified source code
                    unless (depending on the license) their products being sold
                    include the derived software.

                Non-copyleft licenses are sometimes called "permissive" licenses.  The
                BSD and MIT licenses are two examples of permissive licenses.

                The GNU Public License is probably the most well-known of the copyleft
                type of licenses.  You can run the script to get the usage statement
                and the copyleft licenses will be flagged.

                    The copyleft feature of a license can provide open source software
                    with significant benefits compared to proprietary software.  For
                    example, the copyleft feature can prevent a proprietary software
                    company from using the copyleft code because they don't want to
                    release their whole product under a copyleft license.  That means
                    they can't derive the benefits from the open source software.
                    This is one of the stated desires of the FSF.

                Before you decide on a license, your first task should be to formalize
                and write down exactly what you want to accomplish with a license.
                Until you know where you're going, any route can get you there;
                however, common sense says you probably want the most direct route.

                A strategic weakness of open source software comes from the
                proliferation of licenses (see
                https://opensource.org/licenses/alphabetical for a partial list).  Many
                software developers can slog through the legalese of licenses (it's
                somewhat like reading code) and determine what we like and don't like.
                Then we'll rewrite the material that isn't just as we like or has
                missing material.  It's relatively easy to do and many people have done
                it -- and they don't feel the pain that others suffer trying to use
                their software under this modified license.

                    If you think this is a non-issue, consider the following.  The web
                    page http://opensource.org/licenses/alphabetical lists 96 different
                    licenses as of 29 Jan 2020; it was 71 on 10 Aug 2014, so that's 25
                    more in six years.  This is a legal mess.  There's probably
                    lots of overlap among the different licenses.  
                    
                    But who has time to read all those thousands of lines of legal text
                    and understand it deeply (or the money to pay a lawyer to read all
                    that stuff)?  This mess can preclude the use of some software simply
                    because it's too much work for someone to figure out the conditions
                    under which they can include it in their project.  Imagine a
                    corporate project that wanted to use 15 or 20 different chunks of
                    open source software -- the corporate lawyers would be required to
                    study and proclaim the correct legal approach to using all this
                    stuff.  And if these lawyers are like the extremely good but
                    overworked lawyers I used to work with in industry, a business
                    manager might declare that it isn't worth the legal expense to
                    utilize that open source code.  Everyone loses because the
                    corporation has to develop a replacement and the open source code
                    doesn't get used.  Oh, and the customer pays a higher price for that
                    product too.

                Because of this, it makes sense to use a standard and popular license;
                see http://opensource.org/licenses for some widely-used ones.  Based on
                my reading and study, I've included in this script the licenses I
                consider to be the best ones to choose from that are both well-known and
                that might fit the needs that I have for a license.

                For small programs, the GNU folks recommend the Apache 2 license.  The
                Apache web page says the Apache 2 license is compatible with the GPL3,
                meaning that Apache2-licensed code can be included in a GPL3 project.
                However, the "reverse direction" is not true:  if you wanted to
                include a GPL project in an Apache 2 licensed project, you wouldn't be
                able to without licensing the whole thing under the GPL.

                The inherent weaknesses in all of this are that the details can be
                decided by groups of people (lawyers, judges, juries), a mistake can
                be costly (legal expenses, lost business, loss of a lawsuit), and it
                can take a lot of time and resources.  Some day we may see someone sit
                down and design a legal language like a programming language (i.e.,
                really restricted syntax and semantics) that allows better expression
                of these permissions and restrictions.  But I know I won't live long
                enough to see it.

                Releasing your software under an open source license is probably
                irrevocable, at least in a practical sense.  Some of the licenses
                state that the rights you grant users are irrevocable, so it's clear
                you can't change that.  If you did use a license that was considered
                revocable, you could issue a revocation document to the licensees that
                you know about, but remember the license allows the licensees to
                distribute the source code to others.  I'd consider it a nearly
                impossible practical task to revoke an open source license _and_
                notify all the people who have received that software, especially if
                your software is popular and has been out in the wild for a
                significant period of time.  Thus, the pragmatic view is that if you
                release your source code under an open source license, you've
                essentially done it for the life of the copyright on that material,
                regardless of whether the license is revocable or not.

                I feel an article worth reading is
                http://rosenlaw.com/OSL3.0-explained.htm.  Though it supports the OSL3
                license (which the author wrote), it is a clear exposition of various
                things about licenses.  I feel both the OSL3 and this web page are
                well-written, clear, and carefully-crafted documents.  A good legal
                document reads much like well-written software.

                Disclaimer:  I'm not a lawyer, so you can't construe the above as legal
                advice.  Further, you morally need to do your own thinking and reading
                about the various licenses and develop your own opinions of them.  I
                hope my above comments have captured the key points of some of the
                licenses, how I distinguished them, and what led me to the decision I
                made on what ones to use.  Hopefully, the above text will give you help
                in your determination of what works best for your needs.

                In 2014, my license choices were:  For a non-copyleft license, I'll use
                the AFL.  For a copyleft license, I'll use the OSL.

                2026 Thoughts
                -------------

                In 2026, I made the decision to release my code and documents under the
                MIT license (all my stuff had been using the OSL3 license).  My
                reasoning was that I was never going to try to make a living with any of
                this stuff (I retired in 2002) and I wanted people to be able to use my
                stuff however they wanted.  My only desire was that I was attributed as
                the copyright owner because I originated the material by my own thought
                and work.  I needed to decide whether I wanted "copyleft" or
                "non-copyleft".  In 2014 I decided on copyleft, but in 2026 I don't feel
                that's important to me anymore, as making my stuff non-copyleft will
                make it easier to be used by more people.  Hence the change to the MIT
                license.

                This doesn't preclude me from e.g. using the stuff I've done to help my
                kids, grandkids, or friends with some actions to help them make money
                down the road.  Since I own the copyright to this material, I can use it
                as I wish, so I could adapt it to their needs and let them use it in a
                close proprietary way if they wish.

                ''')

if 1:  # Utility
    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        choices = sorted(g.descr.keys())
        lic = []
        lic = g.nl.join(lic)
        print(dedent(f'''
        Usage:  {name} [options] [lic1 [lic2...]]
          Print text of various licenses.
        '''))
        for i in choices:
            print(f"    {i:8s} {g.descr[i]}")
        print("  where '* = copyleft' or '- = non-strong copyleft'.")
        print(dedent(f'''
        Options:
          -a      Print my thoughts on licenses
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # My thoughts
        d["missing"] = []
        if 0:
            # Get the g.analysis text, in the licenses subdirectory
            d["dir"] = GetDir()
            file = pathlib.Path("/pylib/licenses/analysis")
            with g:
                g.analysis = file.read_text().strip()
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "a")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for opt in optlist:
            if opt[0] == "-a":
                print(g.analysis)
                exit(0)
        if len(args) < 1:
            # Need at least one file
            Usage(d)
        return args
if 1:  # Core functionality
    def GetDir():
        "Return the directory of the script"
        return pathlib.Path(sys.argv[0]).resolve().parent
    def PrintLicense(choice):
        if choice not in licenses:
            Error(f"'{choice}' license not recognized")
        print(dedent(f'''
            Copyright (C) 20XX <your name>
        '''))
        print()
        print(licenses[choice].text)
if 0:
    def CheckFiles(files, d):
        '''For each file in files, ensure that it is readable and has the
        requisite string for substitution.
        '''
        bad = False
        for file in files:
            p = pathlib.Path(file)
            if not p.isfile():
                eprint(f"'{file}' is not a file")
                bad = True
                continue
            try:
                s = p.read_text()
            except Exception:
                eprint(f"Could not read '{file}'")
                bad = True
                continue
            mo = regexp.search(s)
            if not mo:
                eprint(f"'{file}' does not have the trigger string '{trigger}'")
                bad = True
                continue
        if bad:
            if not d["-n"]:
                eprint(f"{t.redl}Cannot continue because of the above problems{t.n}")
            exit(1)
    def MakeBackups(files, d):
        "For each file in files, make a backup file"
        for file in files:
            bu = pathlib.Path(file) / backup_extension
            if bu.exists() and not d["-f"]:
                eprint(
                    dedent(f'''
                Backup file '{bu}' already exists
                  Use the -f option to force overwriting of backup files.
                ''')
                )
                exit(1)
            try:
                shutil.copyfile(file, bu)
            except Exception:
                eprint(f"Copy of '{file}' to '{bu}' failed")
                exit(1)
    def ProcessFile(choice, file, d):
        if d["-s"] and choice not in g.short_choices:
            # Use license text rather than header
            s = licenses[choice]
        else:
            s = headers[choice]
        # Prepend comment string d["-c"] to each line.  Remember s is a
        # tuple of (short g.descr, license header).
        if choice == "rem":
            lines = s[1].split(g.nl)
        else:
            lines = [d["-c"] + i for i in s[1].split(g.nl)]
        try:
            u = "" if choice == "rem" else (g.nl.join(lines) + g.nl)
            t = "%s\n%s%s" % (trigger, u, trigger)
            s = open(file).read()
            open(file, "w").write(regexp.sub(t, s))
        except Exception as e:
            t.print(f"{t.redl}File {file!r} couldn't be changed:\n  {e}")
    def ChangeFiles(choice, files, d):
        for file in files:
            ProcessFile(choice, file, d)

if __name__ == "__main__":
    d: dict[object, object] = {}  # Options dictionary
    choices = ParseCommandLine(d)
    sep = t.purl + "-"*80 + t.n if len(choices) > 1 else ""
    for i, choice in enumerate(choices):
        if i and sep:
            print(sep)
        t.print(f"{t.ornl}{choice}")
        PrintLicense(choice)
