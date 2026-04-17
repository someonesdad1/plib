import typing as ty
import re
import fractions
import mpmath
from enum import Enum

class NumType(Enum):
    Int = 1
    Rat = 2
    Flt = 3
    Cpx = 4
    Unc = 5

class ParsedPayload(ty.NamedTuple):
    type: NumType
    real: mpmath.mpf
    imag: mpmath.mpf = mpmath.mpf("0")
    numer: int = 0
    denom: int = 1
    re_unc: mpmath.mpf = mpmath.mpf("0")
    im_unc: mpmath.mpf = mpmath.mpf("0")
    unit: str = ""

class StringParser:
    '''Engine to dichotomize numeric strings and units with recursive precision.'''
    
    @staticmethod
    def parse(s: str, passed_unit: str = "") -> ParsedPayload:
        s = s.strip()
        if not s:
            return ParsedPayload(NumType.Int, mpmath.mpf("0"), unit=passed_unit)

        num_part, found_unit = StringParser._extract_unit(s)
        final_unit = (found_unit if not passed_unit 
                      else f"({found_unit})*({passed_unit})").strip()

        # Tier A: Complex Uncertainty - Manual Top-Level Split
        # Handles: -9.81(2) - 9.81e4(20)j
        if "(" in num_part and ("j" in num_part.lower() or "i" in num_part.lower()):
            clean = num_part.lower().replace("i", "j")
            
            # Find the hinge: the last +/- that is NOT inside parentheses
            hinge_idx = -1
            paren_depth = 0
            for i, char in enumerate(clean):
                if char == '(': paren_depth += 1
                elif char == ')': paren_depth -= 1
                elif char in ('+', '-') and paren_depth == 0:
                    # Don't pick a sign at the very beginning (unary)
                    if i > 0:
                        hinge_idx = i
            
            if hinge_idx != -1:
                re_s = clean[:hinge_idx].strip()
                sign = clean[hinge_idx]
                im_s = clean[hinge_idx+1:].strip().replace("j", "")
                
                re_p = StringParser.parse(re_s)
                im_p = StringParser.parse(im_s)
                
                return ParsedPayload(
                    NumType.Unc, 
                    re_p.real, 
                    imag=(im_p.real if sign == "+" else -im_p.real),
                    re_unc=re_p.re_unc,
                    im_unc=im_p.re_unc,
                    unit=final_unit
                )

        # Tier B: Standard Uncertainty 1.23(45)
        if "(" in num_part and not num_part.startswith("("):
            idx = num_part.find("(")
            if idx > 0 and num_part[idx-1].isdigit():
                try:
                    main_s = num_part[:idx]
                    unc_s = num_part[idx+1:].rstrip(")")
                    real_val = mpmath.mpf(main_s)
                    dec_idx = main_s.find(".")
                    prec = len(main_s) - dec_idx - 1 if dec_idx != -1 else 0
                    re_unc = mpmath.mpf(unc_s) * mpmath.power(10, -prec)
                    return ParsedPayload(NumType.Unc, real_val, re_unc=re_unc, unit=final_unit)
                except: pass

        # Tier C: Complex (Manual Split for Precision)
        clean_num = num_part.lower().replace("i", "j").replace(" ", "")
        if "j" in clean_num:
            try:
                match = re.match(r'^(.*?)([+-])?([^+-]*j)$', clean_num)
                if match:
                    r_s, sign, i_s = match.groups()
                    i_s = i_s.replace('j', '')
                    if not i_s: i_s = "1"
                    if sign == "-": i_s = "-" + i_s
                    return ParsedPayload(NumType.Cpx, mpmath.mpf(r_s or "0"), 
                                         imag=mpmath.mpf(i_s), unit=final_unit)
            except: pass

        # Tier D: Rational
        if "/" in num_part:
            try:
                f = fractions.Fraction(num_part)
                return ParsedPayload(NumType.Rat, mpmath.mpf("0"), numer=f.numerator, denom=f.denominator, unit=final_unit)
            except: pass

        # Tier E: Integer/Float
        if re.fullmatch(r"[-+]?\d+", num_part):
            return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=int(num_part), unit=final_unit)
        try:
            return ParsedPayload(NumType.Flt, mpmath.mpf(num_part), unit=final_unit)
        except:
            return ParsedPayload(NumType.Int, mpmath.mpf("0"), numer=1, unit=s)

    @staticmethod
    def _extract_unit(s: str) -> ty.Tuple[str, str]:
        if " " not in s:
            if any(c.isdigit() for c in s) or any(c.lower() in 'ji' for c in s):
                return s, ""
            return "1", s

        # For strings with multiple spaces like "-9.81(2) - 9.81e4(20)j m/s^2"
        # The unit is the very last block.
        parts = s.rsplit(" ", 1)
        left, right = parts[0].strip(), parts[1].strip()
        
        # If right block starts with a letter/paren and isn't i/j
        if re.match(r'^[a-zA-Z(]', right) and right.lower() not in ('i', 'j'):
            # Ignore scientific notation "e-3"
            if not (right.lower().startswith('e') and any(c.isdigit() for c in right)):
                return left, right
        
        return s, ""

def Assert(condition, message="Assertion failed", got=None, expected=None):
    if not condition:
        out = f"[FAIL] {message}"
        if got is not None or expected is not None:
            out += f" | Got: {got} | Expected: {expected}"
        print(out)
        return False
    return True

def Run_Tests():
    print(f"--- Starting StringParser Spec Tests (dps={mpmath.mp.dps}) ---")
    test_cases = [
        ("1", NumType.Int, 0, ""),
        ("-5", NumType.Int, 0, ""),
        ("1/2", NumType.Rat, 0, ""),
        ("-3/4", NumType.Rat, 0, ""),
        ("1.2", NumType.Flt, 1.2, ""),
        ("-1.2e-3", NumType.Flt, -0.0012, ""),
        ("1+2j", NumType.Cpx, 1.0, ""),
        ("-1 - 2.5i", NumType.Cpx, -1.0, ""),
        ("0 + 0j", NumType.Cpx, 0.0, ""),
        ("-j", NumType.Cpx, 0.0, ""),
        ("1.2e-3 kg", NumType.Flt, 0.0012, "kg"),
        ("3+4j (V)*(A)", NumType.Cpx, 3.0, "(V)*(A)"),
        ("-10 m/s", NumType.Int, 0, "m/s"),
        ("1.23(45)", NumType.Unc, 1.23, ""),
        ("-9.81(2) m/s^2", NumType.Unc, -9.81, "m/s^2"),
        ("-9.81(2) - 9.81e4(20)j m/s^2", NumType.Unc, -9.81, "m/s^2"),
        ("ft", NumType.Int, 0, "ft"),
        ("", NumType.Int, 0, ""),
        ("1.00000000000000000000000000000000000000000000000001", NumType.Flt, 1.0, ""),
    ]

    passed = 0
    for s, exp_type, exp_val, exp_unit in test_cases:
        try:
            p = StringParser.parse(s)
            t_ok = Assert(p.type == exp_type, f"Type mismatch '{s}'", f"{p.type.name}", f"{exp_type.name}")
            u_ok = Assert(p.unit == exp_unit, f"Unit mismatch '{s}'", f"'{p.unit}'", f"'{exp_unit}'")
            if t_ok and u_ok:
                print(f"[OK]   '{s}' -> {p.type.name}")
                passed += 1
        except Exception as e:
            print(f"[CRASH] '{s}' exploded: {e}")

    print(f"--- Result: {passed}/{len(test_cases)} Passed ---")

if __name__ == "__main__":
    Run_Tests()
