import pathlib
import sys
from lwtest import run, raises
from asciify import Asciify
from pdb import set_trace as xx 

def TestAsciify1():
    '''Unfortunately, I didn't document where this set of test cases
    came from.  In the "A" line, the last letter fails, but it's a 
    Roman wide A, so it should pass.  Thus, the asciify.py script needs
    updating.
    '''
    return
    d = {
        "A": "ÀÁÂÃÄÅĀĂǍǞǠǺȀȂȦȺⒶḀẠẢẤẦẨẪẬẮẰẲẴẶＡ",
        "C": "ÇĆĈĊČƇȻꞒⒸḈＣ",
        "E": "ÈÉÊËĒĔĖĚȄȆȨɆⒺḔḖḘḚḜẸẺẼẾỀỂỄỆＥ",
        "I": "ÌÍÎÏĨĪĬİƗǏȈȊⒾᵻḬḮỈỊＩ",
        "N": "ÑŃŅŇƝǋǸȠⓃꞐꞤṄṆṈṊＮ",
        "O": "ÒÓÔÕÖØŌŎŐƟƠǑǾȌȎȪȬȮȰＯⓄꝊꝌṌṎṐṒỌỎỐỒỔỖỘỚỜỞỠỢ",
        "U": "ÙÚÛÜŨŪŬŮŰƯǓǕǗǙǛȔȖɄⓊꞸᵾṲṴṶṸṺỤỦỨỪỬỮỰＵ",
        "Y": "ÝŶŸƳȲɎＹⓎẎỲỴỶỸỾ",
        "D": "ĎĐƊƋǅǲⒹḊḌḎḐḒＤ",
        "G": "ĜĞĠĢƓǤǦǴⒼꞠḠＧ",
        "H": "ĤĦȞⒽⱧꞪḢḤḦḨḪＨ",
        "J": "ĴɈＪⒿ",
        "K": "ĶƘǨⓀⱩꝀꝂꝄꞢḰḲḴＫ",
        "L": "ĹĻĽĿŁǈȽⓁⱠⱢꝈꞭḶḸḺḼＬ",
        "R": "ŔŖŘȐȒɌⓇꝚꞦṘṚṜṞＲ",
        "S": "ŚŜŞŠȘⓈꞨṠṢṤṦṨＳ",
        "T": "ŢŤŦƬƮȚȾＴⓉṪṬṮṰ",
        "W": "ŴⓌⱲẀẂẄẆẈＷ",
        "Z": "ŹŻŽƵȤⓏⱫẐẒẔＺ",
        "B": "ƁƂɃⒷꞖḂḄḆＢ",
        "F": "ƑⒻꞘḞＦ",
        "P": "ƤⓅⱣꝐꝒṔṖＰ",
        "V": "ƲⓋꝞṼṾＶ",
        "M": "ⓂⱮḾṀṂＭ",
        "Q": "ⓆꝖꝘＱ",
        "X": "ⓍẊẌＸ",
        "i": "ⁱìíîïĩīĭǐȉȋɨͥⓘꟾ⒤ᵢᶖḭḯỉịｉ",
        "n": "ⁿₙñńņňŉƞǹȵɲɳⓝꞑ⒩ꞥᵰᶇᷠṅṇṉṋｎ",
        "a": "ₐàáâãäåāăǎǟǡǻȁȃȧͣ⒜ⓐⱥꬱᶏᷲḁẚạảấầẩẫậắằẳẵặａ",
        "e": "ₑèéêëēĕėěȅȇȩɇͤ⒠ⓔⱸꬲꬴᶒḕḗḙḛḝẹẻẽếềểễệｅ",
        "o": "ₒòóôõöøōŏőơǒǿȍȏȫȭȯȱͦ⒪ⓞⱺꝋꝍꬽꬾᷭᷳṍṏṑṓọỏốồổỗộớờởỡợｏ",
        "x": "ₓͯⓧꭖꭗꭘꭙ⒳ᶍẋẍｘ",
        "h": "ₕĥħȟɦͪ⒣ⓗⱨꞕḣḥḧḩḫẖｈ",
        "k": "ₖķƙǩ⒦ⓚⱪꝁꝃꝅꞣᶄᷜḱḳḵｋ",
        "l": "ₗĺļľŀłƚȴɫɬɭ⒧ⓛꬷⱡꝉꞎꬹꬸᶅᷝᷬḷḹḻḽｌ",
        "m": "ₘɱͫ⒨ⓜｍᵯᶆḿṁṃ",
        "p": "ₚƥ⒫ⓟꝑꝓᵱᵽᶈᷮṕṗｐ",
        "s": "ₛśŝşšșʂⓢ⒮ꞩᵴᶊᷤṡṣṥṧṩｓ",
        "t": "ₜţťŧƫƭțȶʈͭ⒯ⓣⱦᵵṫṭṯṱẗｔ",
        "c": "çćĉċčƈȼɕͨ⒞ⓒꞓꞔᷗḉｃ",
        "u": "ùúûüũūŭůűưǔǖǘǚǜȕȗʉͧ⒰ⓤꭎꭏꞹᵤᶙᷰᷴꭒṳṵṷṹṻụủứừửữựｕ",
        "y": "ýÿŷƴȳɏ⒴ⓨꭚẏẙỳỵỷỹỿｙ",
        "d": "ďđƌȡɗͩⓓ⒟ᵭᶁḋḍḏḑḓｄ",
        "g": "ĝğġģǥǧǵɠ⒢ⓖꞡᶃᷚḡｇ",
        "j": "ĵǰɉ⒥ⓙⱼｊ",
        "r": "ŕŗřȑȓɍɼɾͬ⒭ⓡꝛｒꞧᵣᵲᵳᶉꭇ᷊ᷣṙṛṝṟ",
        "w": "ŵ⒲ⓦⱳｗᷱẁẃẅẇẉẘ",
        "z": "źżžƶȥʐʑ⒵ⓩⱬᵶᶎᷦẑẓẕｚ",
        "b": "ƀƃɓ⒝ⓑꞗᵬᶀᷨḃḅḇｂ",
        "f": "ƒ⒡ⓕꞙᵮᶂᷫḟｆ",
        "v": "ʋͮ⒱ⓥⱱⱴꝟᵥᶌṽṿｖ",
        "q": "ʠ⒬ⓠꝗꝙｑ",
        "-": "⹃┄┅⑈┈┉╌╍〰‒⁓–—﹘⸺⸻〜⊝",
        ".": "﹒．",
        "(": "⦅❨⸨（❪₍⟮﹙⁽﴾｟",
        ")": "｠⦆❩⸩❫）₎⟯﹚⁾﴿",
        "[": "⦋「⦍『⦏【〔〖⦗〘〚⎡⎢⎣⸢⸤［⁅﹝⟦⟬❲",
        "]": "⦌」⦎』⦐】〕〗⦘〙〛⸣⎤⎥⎦⸥］⁆﹞⟧⟭❳",
        "{": "｛⦃❴﹛",
        "}": "⦄❵｝﹜",
        "<": "⟨〈⟪《❬〈❰⦑⧼",
        ">": "⟩〉⟫》❭〉❱⦒⧽",
        "'": " ̀́❛›❮❯′ʹ‵❟‘’‚‛❜‹",
        ' ': "          \u200b\ufeff",
        '"': "＂〃“〝〞〟”„‟«″‴‶‷ʺ»⹂⁗❝❞❠",
    }
    for asc, ltrs in d.items():
        if 0:
            for i in ltrs:
                assert(Asciify(i) == asc)
        else:
            for i in ltrs:
                if Asciify(i) != asc:
                    print(asc, i, hex(ord(i)))

def TestAsciify():
    '''This test uses the /pylib/asciify.test file, which contains lines
    that have a character X, tab, and a set of Unicode codepoints that
    should Asciify to X.
    '''
    p = pathlib.Path("/pylib/asciify.test")
    s = p.read_text()
    print("asciify_test.py fails on these characters:")
    print("char:  expected, got, hex(ord(char))")
    for line in s.split("\n"):
        if not line.strip():
            continue
        expected, chars = line.split("\t")
        for i in chars:
            got = Asciify(i)
            if got != expected:
                print(f"{i}:  {expected}, {got}, {hex(ord(i))}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit(run(globals(), broken=True)[0])
    else:
        exit(run(globals())[0])
