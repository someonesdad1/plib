'''
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Transliterate ASCII letters to Unicode oo>
        <oo desc ∞ 

            This allows you to have text that is reasonably readable but would be
            difficult to search for.  This provides a modicum of textual security in
            that the only way the material could be found in a large file is by a
            tedious search, unless the person knows the algorithm of this script.

        oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ 
            MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ text oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 
            
            - ∞∞2 Useful utility for shrouding ASCII text
            - The selection of characters is random (os.urandom()) unless a seed is
              provided.  This means you'll essentially never get the same encoding
              twice.
            - asciify.test has a good selection of some Unicode characters to use
                - Example:  the digit 0 has four different good choices (at least they
                  look good on the WSL Windows Terminal screen font).  The character A
                  has '𝐀ḀȂȀĂĀ𝘈ȦÅ𝐴𝔸𝘼𝑨𝙰𝖠ẠẢẤẦẨẪẬẮẰẲẴẶÀÁÂÃÄÅǍ𝗔ǞǠǺ', a wide variety of
                  choices.  

        oo>
    '''
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Transliteration data
    if 0:
        # /plib/asciify.test is the primary source of these data.  Note the primary
        # character (the key) is separated from its values by a tab character.  I have
        # manually edited the data to only include values that I feel look reasonable in the
        # WSL Windows Terminal font I use.
        g.data = '''
            '	❛ʼʽˊ′ʹ‵‘’‛❜ʻ
            "	🙷“〞”‟❞˝ˮ″‶🙶ʺ
            (	⦅⟮❨﹙❪
            )	⟯⦆❩﹚❫
            <	˂﹤≺＜
            >	˃﹥≻＞
            [	⦋【〔〘〚⟦⟬
            ]	⦌】〕〙〛⟧⟭
            {	﹛⦃❴
            }	﹜⦄❵
            ,	⹁⸲⸴
            -	⁃┄┅⹃┈┉₋⑉╌╍‐‑‒–—⁓−﹘˗­
            .	⸼․
            ;	︔﹔⸵⁏
            :	⦂꞉ː∶˸
            ?	❓❔︖
            !	ǃ❕︕
            /	⁄⧸∕⫻🙼⫽
            \	⧵∖⧹⑊﹨🙽
            |	∣⏐⸾⍿
            $	﹩💲
            &	﹠🙴🙵
            *	∗🞯🞰✱✲🞱🞲🞳🞴🞵🞶✻✼✽🞷🞸🞹🞺🞻❃🞼🞽🞾🞿❉❊❋⁎
            +	＋➕✚✛🞡🞢🞣🞤🞥🞦🞧⨥﹢᛭
            =	⊜﹦꞊₌⁼＝
            _	ˍ
            ~	∾∽∼∿
            0	𝟢𝟬𝟎𝟶𝟘
            1	𝟣𝟭𝟏𝟷𝟙
            2	𝟐𝟚𝟤𝟮𝟸
            3	𝟑𝟛𝟥𝟯𝟹
            4	𝟦𝟰𝟒𝟺𝟜
            5	𝟧𝟱𝟓𝟻𝟝
            6	𝟨𝟲𝟔𝟼𝟞
            7	𝟩𝟳𝟕𝟽𝟟
            8	𝟠𝟪𝟴𝟖𝟾
            9	𝟡𝟫𝟵𝟗𝟿
            A	𝐀ḀȂȀĂĀ𝘈ȦÅ𝐴𝔸𝘼𝑨𝖠ẠẢẤẦẨẪẬẮẰẲẴẶÀÁÂÃÄÅǍ𝗔ǞǠǺ
            a	ḁȁȃăā𝐚𝘢ȧ𝑎𝕒𝙖𝒂𝖆𝚊ᶏẚạảấầẩẫậắằẳẵ𝒶ặ𝖺ǎǟàǡâäåãá𝓪𝗮ǻ
            B	ƁɃ𝐁ḆḄḂ𝘉𝓑𝗕Ꞗ𝖡𝑩ℬ𝙱𝐵𝔹𝘽
            b	ƀᶀ𝒃ḅḃḇ𝚋𝑏𝕓𝙗𝐛𝔟𝘣𝓫ᵬ𝗯𝒷𝖻
            C	𝐂ℂĆƇḈĈ𝘊ĊČÇ𝓒𝗖𝒞𝖢𝑪Ⅽ𝙲𝐶𝘾
            c	𝒄ćƈḉċ𝚌čĉ𝑐𝕔𝙘𝖼𝐜𝔠𝘤ç𝓬𝗰𝒸ⅽ
            D	𝐃ⅅ𝔇Ɗ𝘋ḌḎḊĐḐḒ𝓓Ď𝗗𝒟𝖣𝑫Ⅾ𝕯𝙳𝐷𝘿
            d	ᶁ𝒅ḋ𝚍ḍḏďđḓḑ𝐝ȡ𝘥𝒹𝖽ⅆ𝑑𝕕ɗ𝙙ᵭ𝓭𝗱ⅾ
            E	𝐄ȄȆ𝘌ĒḔĔḖĖḘḚĚḜ𝖤Ȩℰ𝐸ẸẺ𝔼ẼẾ𝙀ỀỂỄỆÈÉÊË𝓔𝗘𝑬𝙴
            e	ȅȇēḕĕḗėḙḛěḝ𝐞𝘦ȩℯꬲꬴɇⅇ𝑒𝕖𝙚𝒆𝚎ᶒẹẻẽ𝖾ếềểễệèéêë𝓮𝗲
            F	𝐅𝘍ƑꞘḞ𝖥ℱ𝐹𝔽𝙁𝓕𝗙𝑭𝙵
            f	ᶂ𝒇𝚏ƒꞙḟ𝐟𝘧𝒻𝖿𝑓𝕗𝙛𝓯𝗳
            G	𝙂𝐆𝘎Ɠ𝓖𝗚ĜĞḠ𝒢ĢǤĠ𝖦Ǧ𝑮Ǵ𝙶𝐺𝔾
            g	ᶃℊ𝖌𝚐ĝğ𝐠ḡģ𝔤ġ𝘨𝗀𝑔𝕘𝙜ǥǧ𝓰𝗴ǵ
            H	𝙃𝐇ℍ𝘏𝗛ȞḤĤⱧ𝖧ḨꞪḪḦ𝑯𝙷𝐻
            h	𝗁𝒉ℎ𝚑ꞕ𝕙ẖ𝙝ȟ𝐡ḣħⱨ𝘩ḩḫḧḥĥ𝓱𝗵𝒽
            I	𝐈ȈȊ𝘐𝖨ĨĪḬĬḮİ𝐼𝕀𝙄ỈỊÌÍÎǏÏ𝗜Ⅰ𝙸ꟾ
            i	ȉ𝒊ȋ𝖎𝚒ᶖ𝐢𝔦ĩ𝘪īḭĭḯ𝒾𝗂ⅈỉịǐ𝑖𝕚𝙞ɨìíîïⅰ𝓲𝗶
            J	𝐉𝘑𝒥𝖩Ĵ𝐽𝕁𝙅𝓙𝗝𝙹
            j	𝒋𝚓ʝ𝐣𝔧𝘫ĵ𝒿𝗃ɉⅉ𝑗𝕛𝙟ǰ𝓳𝗷ⱼ
            K	𝐊𝘒Ƙ𝒦K𝖪ḰḲḴĶ𝐾ꝀꝂ𝕂Ꝅ𝙆𝓚𝗞ǨⱩ𝙺
            k	ᶄ𝒌𝚔ƙꞣ𝐤𝘬ḱḳḵķꝁꝃ𝗄ꝅ𝑘𝕜𝙠ǩⱪ𝗸
            L	𝐋ℒ𝘓𝙻Ĺ𝖫ꞭḶḸḺḼȽĽ𝐿ĿŁ𝕃Ļ𝙇Ꝉ𝓛𝗟ⱢⅬ
            l	ᶅ𝒍ꞎ𝖑ℓ𝚕ƚ𝐥𝘭ȴḹḻḷḽľļŀ𝓁łĺ𝗅ꝉ𝑙𝕝𝙡ɫɬɭ𝓵𝗹ⅼ
            M	𝐌𝘔𝙼𝖬Ḿ𝑀Ṁ𝕄𝙈𝓜𝗠ⱮⅯ
            m	ṁ𝓂ṃᶆ𝗆𝒎𝖒𝚖𝑚𝕞𝙢𝐦𝔪ḿ𝘮ᵯ𝓶𝗺ꬺⅿ
            N	𝑁ṄŅṆŇṈ𝙉ṊŃ𝐍ꞐÑ𝘕ℕ𝓝𝗡Ꞥ𝒩𝖭Ǹ𝙽
            n	ᶇ𝒏ꞑ𝖓𝚗ƞꞥ𝐧𝔫𝘯ȵ𝓃ńṅņ𝗇ṇṉŉṋň𝑛𝕟𝙣ᵰñ𝓷ǹ𝗻
            O	ŌŎŐƠÒÓ𝙾Ô𝕆ỌỎỐỒỔỖØỘỚÖỜÕỠỞỢ
            o	ōȍȏ𝒐ŏ𝚘őơ𝐨ȫ𝔬ȭȯ𝘰ȱℴ𝗈ꝍọỏṏốṑồổṓỗộǒớ𝑜ờởøỡợ𝙤òóṍõöô𝓸ⱺ𝗼ǿ
            P	𝐏𝘗ℙƤ𝒫𝖯𝑃𝙋ꝐꝒṔṖ𝓟Ᵽ𝗣𝑷𝙿
            p	ᶈ𝒑𝖕𝚙𝐩𝔭𝘱𝓅𝗉ꝑꝓꝕṕṗ𝑝𝕡𝙥ᵱ𝓹𝗽
            Q	𝐐𝘘ℚ𝒬𝖰𝑄𝙌Ꝗ𝓠𝗤𝑸
            q	𝕢𝙦𝓆𝗊ɋ𝓺𝐪𝔮𝘲𝒒𝑞𝖖ꝗꝙ𝚚𝗾
            R	𝚁Ř𝑅Ɍ𝙍Ȑ𝐑ȒŔŖṘ𝘙ℛℜℝṞṜṚ𝓡Ɽ𝗥Ꞧ𝖱𝑹𝕽
            r	ᶉȑ𝒓ȓ𝖗𝚛ꞧ𝐫𝔯𝘳ꭇ𝓇𝗋ɍŕŗṙřṛṝ𝑟ṟ𝕣𝙧ᵲᵳ𝓻ɼɽɾ𝗿
            S	𝐒Ș𝘚Ꞩ𝒮𝖲𝑆𝕊𝙎ⱾŚŜŞṠŠ𝓢ṤṢ𝗦ṦṨ𝑺
            s	𝘀ʂᶊ𝗌ś𝒔𝖘ș𝚜ŝş𝑠ṡ𝕤ṥṣṧ𝙨ꞩṩ𝐬𝔰šᵴ𝘴ȿ
            T	𝚃𝑇𝕋𝙏𝐓Ț𝘛ŢŤŦ𝗧ṪƬṬƮ𝒯ṰṮ𝖳𝑻
            t	𝘁ʈ𝒕ẗ𝖙ț𝚝ƫƭ𝐭𝔱𝘵ȶ𝓉𝗍𝑡ţ𝕥ⱦŧť𝙩ṫṭṯṱᵵ𝓽
            U	𝚄𝐔ȔȖŨ𝘜Ư𝒰𝖴𝑈𝕌𝙐ǓǕǗǙÚǛÜÛÙỦỤỨỪŪỬŬỮŮỰŰṲṴṶṸṺ
            u	𝘂ȕȗ𝐮𝔲𝘶ꭎꭒ𝑢𝕦ũ𝙪ūŭůűṳṵṷṹṻ𝒖ᶙ𝖚𝚞ư𝓊𝗎ǔǖǘǚǜụủứừửữựùúûü𝓾
            V	𝐕𝘝𝒱𝖵𝑉𝕍𝙑Ꝟ𝗩Ṽ𝑽Ṿ
            v	𝘃˅𝓋𝗏𝒗𝚟ꝟ𝑣𝕧𝙫𝐯ṿⱱⅴ𝘷ṽ𝓿
            W	ẀẂẄ𝚆ᵂ𝕎Ŵ
            w	𝔀𝘄ẇẉẘ𝒘𝖜𝚠𝐰𝔴𝘸𝓌𝗐𝑤ⓦ𝕨𝙬ⱳŵ
            X	𝚇ẊẌ𝐗𝔛𝘟𝖷𝑋𝕏𝗫𝑿
            x	𝔁𝘅ẋ⛌ᶍ𝓍𝗑ẍꭖꭗꭘꭙ𝒙𝖝⊠𝚡𝑥𝕩ⅹ⤫⤬𝙭⨯𝐱𝔵𝘹
            Y	𝒀𝑌Ɏ𝕐ỸẎ𝙔𝐘Ý𝘠Ÿ𝗬ỲƳỴỶȲ𝖸Ŷ
            y	𝔂ÿ𝘆ẏẙ𝒚𝚢𝐲ȳƴ𝘺𝓎ɏ𝗒ꭚŷ𝑦𝕪𝙮ỳỵỷỹýỿ
            Z	𝒁𝚉𝑍ẐẒẔ𝙕𝐙𝘡ȤℤⱫŹ𝗭Ƶ𝖹ŻŽⱿ
            z	𝔃𝘇ᶎʐʑẑẓẕ𝒛𝚣ȥ𝐳ƶ𝘻ɀ𝓏𝗓𝑧𝕫ⱬ𝙯ᵶźżž
        '''
        # Choices dictionary (transliteration dict built from this)
        g.choices = {}
        for line in g.data.split("\n"):
            line = line.strip()
            if not line:
                continue
            key, value = line.split("\t")
            assert " " not in value
            g.choices[key] = value
        # Print dict to stdout
        s = " "*4   # For indent
        print(f"{s}g.choices = {{")
        for i in g.choices:
            if i == '"':
                print(f"{s}{s}'{i}': '{g.choices[i]},'")
            else:
                print(f'{s}{s}"{i}": "{g.choices[i]}",')
        print(f"{s}}}")
        exit() #∞∞ 

if 1:   # Utility
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
          -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Get transliteration dict
    def GetTransliterationDict(seed=None):
        '''Return a dictionary that will translate an ASCII string to a Unicode string
        that looks similar.  If you include a seed argument (it must be hashable), it
        will be used to get the same dictionary each time.
        '''

    # Dictionary of allowed translations from ASCII to Unicode
    GetTransliterationDict.choices = {
        "'": "❛ʼʽˊ′ʹ‵‘’‛❜ʻ",
        '"': '🙷“〞”‟❞˝ˮ″‶🙶ʺ',
        "(": "⦅⟮₍❨﹙❪",
        ")": "₎⟯⦆❩﹚❫",
        "<": "˂﹤≪≮≺",
        ">": "˃﹥≫≯≻",
        "[": "⦋【〔⦗〘〚﹝⟦⟬",
        "]": "⦌】〕⦘〙〛﹞⟧⟭",
        "{": "﹛⦃❴",
        "}": "⦄❵﹜",
        ",": "⹁⸲⸴",
        "-": "⁃┄┅⹃┈┉₋⑉╌╍‐‑‒–—⁓−﹘˗­",
        ".": "⸼․",
        ";": "︔﹔⸵⁏",
        ":": "⦂꞉ː︓∶˸",
        "?": "❓❔︖",
        "!": "ǃ❕︕",
        "/": "⁄⧸∕⫻🙼⫽",
        "\\": "⧵∖⧹⑊﹨🙽",
        "|": "∣⏐⸾⍿",
        "$": "﹩💲",
        "&": "﹠🙴🙵",
        "*": "∗🞯🞰✱✲🞱🞲🞳🞴🞵🞶✻✼✽🞷🞸🞹🞺🞻❃🞼🞽🞾🞿❉❊❋⁎",
        "+": "＋➕✚✛🞡🞢🞣🞤🞥🞦🞧⨥﹢᛭",
        "=": "⊜﹦꞊₌⁼＝",
        "_": "ˍ",
        "~": "∾∽∼∿",
        "0": "𝟢𝟬𝟎𝟶𝟘",
        "1": "𝟣𝟭𝟏𝟷𝟙",
        "2": "𝟐𝟚𝟤𝟮𝟸",
        "3": "𝟑𝟛𝟥𝟯𝟹",
        "4": "𝟦𝟰𝟒𝟺𝟜",
        "5": "𝟧𝟱𝟓𝟻𝟝",
        "6": "𝟨𝟲𝟔𝟼𝟞",
        "7": "𝟩𝟳𝟕𝟽𝟟",
        "8": "𝟠𝟪𝟴𝟖𝟾",
        "9": "𝟡𝟫𝟵𝟗𝟿",
        "A": "𝐀ḀȂȀĂĀ𝘈ȦÅ𝐴𝔸𝘼𝑨𝖠ẠẢẤẦẨẪẬẮẰẲẴẶÀÁÂÃÄÅǍ𝗔ǞǠǺ",
        "a": "ḁȁȃăā𝐚𝘢ȧ𝑎𝕒𝙖𝒂𝖆𝚊ᶏẚạảấầẩẫậắằẳẵ𝒶ặ𝖺ǎǟàǡâäåãá𝓪𝗮ǻ",
        "B": "ƁɃ𝐁ḆḄḂ𝘉𝓑𝗕Ꞗ𝖡𝑩ℬ𝙱𝐵𝔹𝘽",
        "b": "ƀᶀ𝒃ḅḃḇ𝚋𝑏𝕓𝙗𝐛𝔟𝘣𝓫ᵬ𝗯𝒷𝖻",
        "C": "𝐂ℂĆƇḈĈ𝘊ĊČÇ𝓒𝗖𝒞𝖢𝑪Ⅽ𝙲𝐶𝘾",
        "c": "𝒄ćƈḉċ𝚌čĉ𝑐𝕔𝙘𝖼𝐜𝔠𝘤ç𝓬𝗰𝒸ⅽ",
        "D": "𝐃ⅅ𝔇Ɗ𝘋ḌḎḊĐḐḒ𝓓Ď𝗗𝒟𝖣𝑫Ⅾ𝕯𝙳𝐷𝘿",
        "d": "ᶁ𝒅ḋ𝚍ḍḏďđḓḑ𝐝ȡ𝘥𝒹𝖽ⅆ𝑑𝕕ɗ𝙙ᵭ𝓭𝗱ⅾ",
        "E": "𝐄ȄȆ𝘌ĒḔĔḖĖḘḚĚḜ𝖤Ȩℰ𝐸ẸẺ𝔼ẼẾ𝙀ỀỂỄỆÈÉÊË𝓔𝗘𝑬𝙴",
        "e": "ȅȇēḕĕḗėḙḛěḝ𝐞𝘦ȩℯꬲꬴɇⅇ𝑒𝕖𝙚𝒆𝚎ᶒẹẻẽ𝖾ếềểễệèéêë𝓮𝗲",
        "F": "𝐅𝘍ƑꞘḞ𝖥ℱ𝐹𝔽𝙁𝓕𝗙𝑭𝙵",
        "f": "ᶂ𝒇𝚏ƒꞙḟ𝐟𝘧𝒻𝖿𝑓𝕗𝙛𝓯𝗳",
        "G": "𝙂𝐆𝘎Ɠ𝓖𝗚ĜĞḠ𝒢ĢǤĠ𝖦Ǧ𝑮Ǵ𝙶𝐺𝔾",
        "g": "ᶃℊ𝖌𝚐ĝğ𝐠ḡģ𝔤ġ𝘨𝗀𝑔𝕘𝙜ǥǧ𝓰𝗴ǵ",
        "H": "𝙃𝐇ℍ𝘏𝗛ȞḤĤⱧ𝖧ḨꞪḪḦ𝑯𝙷𝐻",
        "h": "𝗁𝒉ℎ𝚑ꞕ𝕙ẖ𝙝ȟ𝐡ḣħⱨ𝘩ḩḫḧḥĥ𝓱𝗵𝒽",
        "I": "𝐈ȈȊ𝘐𝖨ĨĪḬĬḮİ𝐼𝕀𝙄ỈỊÌÍÎǏÏ𝗜Ⅰ𝙸ꟾ",
        "i": "ȉ𝒊ȋ𝖎𝚒ᶖ𝐢𝔦ĩ𝘪īḭĭḯ𝒾𝗂ⅈỉịǐ𝑖𝕚𝙞ɨìíîïⅰ𝓲𝗶",
        "J": "𝐉𝘑𝒥𝖩Ĵ𝐽𝕁𝙅𝓙𝗝𝙹",
        "j": "𝒋𝚓ʝ𝐣𝔧𝘫ĵ𝒿𝗃ɉⅉ𝑗𝕛𝙟ǰ𝓳𝗷ⱼ",
        "K": "𝐊𝘒Ƙ𝒦K𝖪ḰḲḴĶ𝐾ꝀꝂ𝕂Ꝅ𝙆𝓚𝗞ǨⱩ𝙺",
        "k": "ᶄ𝒌𝚔ƙꞣ𝐤𝘬ḱḳḵķꝁꝃ𝗄ꝅ𝑘𝕜𝙠ǩⱪ𝗸",
        "L": "𝐋ℒ𝘓𝙻Ĺ𝖫ꞭḶḸḺḼȽĽ𝐿ĿŁ𝕃Ļ𝙇Ꝉ𝓛𝗟ⱢⅬ",
        "l": "ᶅ𝒍ꞎ𝖑ℓ𝚕ƚ𝐥𝘭ȴḹḻḷḽľļŀ𝓁łĺ𝗅ꝉ𝑙𝕝𝙡ɫɬɭ𝓵𝗹ⅼ",
        "M": "𝐌𝘔𝙼𝖬Ḿ𝑀Ṁ𝕄𝙈𝓜𝗠ⱮⅯ",
        "m": "ṁ𝓂ṃᶆ𝗆𝒎𝖒𝚖𝑚𝕞𝙢𝐦𝔪ḿ𝘮ᵯ𝓶𝗺ꬺⅿ",
        "N": "𝑁ṄŅṆŇṈ𝙉ṊŃ𝐍ꞐÑ𝘕ℕ𝓝𝗡Ꞥ𝒩𝖭Ǹ𝙽",
        "n": "ᶇ𝒏ꞑ𝖓𝚗ƞꞥ𝐧𝔫𝘯ȵ𝓃ńṅņ𝗇ṇṉŉṋň𝑛𝕟𝙣ᵰñ𝓷ǹ𝗻",
        "O": "ŌŎŐƠÒÓ𝙾Ô𝕆ỌỎỐỒỔỖØỘỚÖỜÕỠỞỢ",
        "o": "ōȍȏ𝒐ŏ𝚘őơ𝐨ȫ𝔬ȭȯ𝘰ȱℴ𝗈ꝍọỏṏốṑồổṓỗộǒớ𝑜ờởøỡợ𝙤òóṍõöô𝓸ⱺ𝗼ǿ",
        "P": "𝐏𝘗ℙƤ𝒫𝖯𝑃𝙋ꝐꝒṔṖ𝓟Ᵽ𝗣𝑷𝙿",
        "p": "ᶈ𝒑𝖕𝚙𝐩𝔭𝘱𝓅𝗉ꝑꝓꝕṕṗ𝑝𝕡𝙥ᵱ𝓹𝗽",
        "Q": "𝐐𝘘ℚ𝒬𝖰𝑄𝙌Ꝗ𝓠𝗤𝑸",
        "q": "𝕢𝙦𝓆𝗊ɋ𝓺𝐪𝔮𝘲𝒒𝑞𝖖ꝗꝙ𝚚𝗾",
        "R": "𝚁Ř𝑅Ɍ𝙍Ȑ𝐑ȒŔŖṘ𝘙ℛℜℝṞṜṚ𝓡Ɽ𝗥Ꞧ𝖱𝑹𝕽",
        "r": "ᶉȑ𝒓ȓ𝖗𝚛ꞧ𝐫𝔯𝘳ꭇ𝓇𝗋ɍŕŗṙřṛṝ𝑟ṟ𝕣𝙧ᵲᵳ𝓻ɼɽɾ𝗿",
        "S": "𝐒Ș𝘚Ꞩ𝒮𝖲𝑆𝕊𝙎ⱾŚŜŞṠŠ𝓢ṤṢ𝗦ṦṨ𝑺",
        "s": "𝘀ʂᶊ𝗌ś𝒔𝖘ș𝚜ŝş𝑠ṡ𝕤ṥṣṧ𝙨ꞩṩ𝐬𝔰šᵴ𝘴ȿ",
        "T": "𝚃𝑇𝕋𝙏𝐓Ț𝘛ŢŤŦ𝗧ṪƬṬƮ𝒯ṰṮ𝖳𝑻",
        "t": "𝘁ʈ𝒕ẗ𝖙ț𝚝ƫƭ𝐭𝔱𝘵ȶ𝓉𝗍𝑡ţ𝕥ⱦŧť𝙩ṫṭṯṱᵵ𝓽",
        "U": "𝚄𝐔ȔȖŨ𝘜Ư𝒰𝖴𝑈𝕌𝙐ǓǕǗǙÚǛÜÛÙỦỤỨỪŪỬŬỮŮỰŰṲṴṶṸṺ",
        "u": "𝘂ȕȗ𝐮𝔲𝘶ꭎꭒ𝑢𝕦ũ𝙪ūŭůűṳṵṷṹṻ𝒖ᶙ𝖚𝚞ư𝓊𝗎ǔǖǘǚǜụủứừửữựùúûü𝓾",
        "V": "𝐕𝘝𝒱𝖵𝑉𝕍𝙑Ꝟ𝗩Ṽ𝑽Ṿ",
        "v": "𝘃˅𝓋𝗏𝒗𝚟ꝟ𝑣𝕧𝙫𝐯ṿⱱⅴ𝘷ṽ𝓿",
        "W": "ẀẂẄ𝚆ᵂ𝕎Ŵ",
        "w": "𝔀𝘄ẇẉẘ𝒘𝖜𝚠𝐰𝔴𝘸𝓌𝗐𝑤ⓦ𝕨𝙬ⱳŵ",
        "X": "𝚇ẊẌ𝐗𝔛𝘟𝖷𝑋𝕏𝗫𝑿",
        "x": "𝔁𝘅ẋ⛌ᶍ𝓍𝗑ẍꭖꭗꭘꭙ𝒙𝖝⊠𝚡𝑥𝕩ⅹ⤫⤬𝙭⨯𝐱𝔵𝘹",
        "Y": "𝒀𝑌Ɏ𝕐ỸẎ𝙔𝐘Ý𝘠Ÿ𝗬ỲƳỴỶȲ𝖸Ŷ",
        "y": "𝔂ÿ𝘆ẏẙ𝒚𝚢𝐲ȳƴ𝘺𝓎ɏ𝗒ꭚŷ𝑦𝕪𝙮ỳỵỷỹýỿ",
        "Z": "𝒁𝚉𝑍ẐẒẔ𝙕𝐙𝘡ȤℤⱫŹ𝗭Ƶ𝖹ŻŽⱿ",
        "z": "𝔃𝘇ᶎʐʑẑẓẕ𝒛𝚣ȥ𝐳ƶ𝘻ɀ𝓏𝗓𝑧𝕫ⱬ𝙯ᵶźżž",
    }
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
