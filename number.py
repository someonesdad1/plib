from __future__ import annotations
'''
ToDo

- Tests
    - Get some key unit tests for __add__, __radd__, and __iadd__ and friends
    - Verify infection model
    - Test formatting in detail
- Start playing with it in the REPL; it's nearly a real calculator
    - The dirt work in the back could be an excellent real-world example
    - Need some way of letting user give preferred units
        - x.preferred("ft lb"), then x.preferred() means reset to original
        - x.to("unit") should return a Num in the new unit (non-working code
          at the moment because arbiter.discover_best_unit(self.unit) isn't
          working
    - If you use an unknown unit, the server hangs
    - Changed UnitArbiter's add_primitive() to add_base() (easier to type &
      remember)
    - Any way to have a non-blocking num.check(unit) function that returns
      True if unit is known, False if not?  This would be a way to avoid the
      hang.
- Add nbs to string between number and unit in fmt.py

'''
if 1:  # Header
    if 1:   # Standard imports
        import decimal
        import enum
        import fcntl
        import fractions
        import inspect
        import operator
        import os
        import pathlib
        import re
        import shutil
        import subprocess
        import sys
        import tempfile
        import threading
        import typing as ty
    if 1:   # Custom imports
        import dpmath
        import dptypes
        import fmt
        import lwtest
        import mpmath
        import trm
        import uncertainties
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Class to contain a general number"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "math"
        __todo__      = '''These are ToDo items not to forget
            
            - Num.strict:  if on, uncertainties never compare equal.  If off, then if
              the mean and stdev match, they're equal with a warning to stderr:
              "Warning:  comparing distributions".
            - If Num.hashable is True, you might want the hash to be a tuple of the core
              values: hash((self.mytype, self.real, self.imag, self.unit)).  
            - Num.on?  Turns colorizing on/off
        
        '''
    if 1:   # Global variables
        Path = pathlib.Path
        Assert = lwtest.Assert
        t = trm.TrmDP()
        t.dbg = "#bdf6fe"
        g = dptypes.Constant()
        g.dbg = True if 0 else False
        g.X = False
    if 1:   # Types and enums
        class NumType(enum.IntEnum):
            Int = 1
            Rat = 2
            Flt = 3
            Cpx = 4
            Unc = 5
        NumericalTypes = ty.Union[
            int , float , complex , decimal.Decimal ,
            fractions.Fraction , mpmath.mpf , mpmath.mpc ,
            uncertainties.UFloat , "Num" , str , None]
    if 1:   # Utility stuff
        def Dbg(*p, **kw):
            if not hasattr(Dbg, "file"):
                Dbg.file = sys.stdout
            if g.dbg:
                if "color" in kw:
                    print(f"{t(kw['color'])}", end="", file=Dbg.file)
                    del kw["color"]
                else:
                    print(f"{t.dbg}", end="", file=Dbg.file)
                k = kw.copy()
                k["file"] = Dbg.file
                print(*p, **k)
                print(f"{t.n}", end="", file=Dbg.file)
        def get_caller_info() -> tuple[str, int]:
            'Returns (file_name, line_number) for the frame above the caller'
            # frame 0 is get_caller_info
            # frame 1 is Warn
            # frame 2 is the code that called Warn
            frame = inspect.stack()[2]
            return os.path.basename(frame.filename), frame.lineno
        def Warn(*p, **kw):
            '''Write a message to stderr in red color with location from where called.
            To minimize the number of messages, you can set single=True and the message
            will be printed only once.
            '''
            if not hasattr(Warn, "single"):
                Warn.single = False
                Warn.already_printed = set()
            fname, line = get_caller_info()
            k = kw.copy()   # Only modify a copy of kw
            k["file"] = sys.stderr
            Warn.single = bool(k.get("single", False))  # See if only print once
            if "single" in k:
                del k["single"]
            if Warn.single and p in Warn.already_printed:
                return
            Warn.already_printed.add(p)
            # Print the warning
            print(f"{t.red}[{fname}:{line}]:  ", end="", file=sys.stderr)
            print(*p, **k)
            print(f"{t.n}", end="", file=sys.stderr)
    if 0:   # Documentation
        '''Represent a general number useful for routine calculations
            
                Caution:  The internal representation uses the mpmath library, so it's
                your responsibility as the user to ensure the mpmath context has
                sufficient resolution for your problems.  Example:  'mpmath.mp.dps = 30'
                to set 30 digits of resolution; the default is 15, about the same as a
                python float.

                The Num class tries to be a container for the common numbers used
                for the problems we do in the real world.  It can deal with 
                    
                    - integers
                    - fractions
                    - floating point numbers
                    - complex numbers
                    - real and complex numbers with uncertainty
                        - Uses linear uncertainty propagation
                    - physical and logical units for these numbers
                        - GNU units program used for unit conversion fractors and
                          dimensional algebra.  Because of this, you may want to
                          familiarize yourself with its syntax and capabilities.

                The internal representation of the Num class uses 
                    
                    - Two python integers for integers and fractions
                    - Two mpmath.mpf instances for the real and imaginary components
                    - Two mpmath.mpf instances for the uncertainties in the real and
                      imaginary components
                    - One mpmath.mpf instance for the correlation coefficient between
                      the real and imaginary components

                In calculations, there's an internal type hierarchy that causes type
                promotion when needed (in the enum NumType):

                    Int < Rat < Flt < Cpx < Unc

                In binary operations, the type of the result is determined by the Num
                instance's largest NumType.

                Units are handled by letting you write them as strings.  Behind the scenes,
                the GNU units tool handles the conversion mechanics, unit definitions, and
                dimensional algebra.  

                Uncertainty is handled by using linear uncertainty propagation.  
                
                "Logical" units

                    We usually think of units as e.g. the familiar SI units.  However,
                    almost all practical calculations involve some types of units.  For
                    example, if you're measuring ut pet food mass to feed some dogs and
                    cats, you'd probably want the calculation to use the "units"
                    kg_cat_food and kg_dog_food, assuming the dogs and cats get fed
                    different foods.  This "unit orthogonality" helps keeps the animals
                    fed properly, avoiding a mistake of mixing the foods, which might
                    show up in a calculation as having units of kg_cat_food*kg_dog_food
                    or a sum of 'kg_cat_food + kg_dog_food'.  

                    It's a shame the programming tools we have don't natively support
                    both physical and logical units.  One of my goals in this Num class
                    was to provide a tool to do just this, because when the units in
                    some arithmetical calculation aren't consistent, a logical error has
                    been made.  Every scientist or engineer has learned to use such
                    dimensional errors as red flags.

                    The interesting feature of the Num class is that you can add logical
                    units dynamically, i.e., while you're doing your calculation.  This
                    is a powerful aid to doing a correct calculation, as the GNU units
                    program will tell you if the units haven't been used correctly.
                    Imagine how many bugs could be reduced in the world's programs if we
                    had this feature in our programming environments natively.
            
        '''

if 1:   # NumericMixin:  class to add dunder math methods
    class NumericMixin:
        '''Boilerplate to make Num behave like a native Python number.'''
        def __neg__(self) -> "Num":
            return self * -1
        def __pos__(self) -> "Num":
            return self * 1
        def __abs__(self) -> "Num":
            res = Num(self)
            res.numer = abs(res.numer)
            res.denom = abs(res.denom)
            res.real = abs(res.real)
            res.imag = abs(res.imag)
            return res
        def __radd__(self, other):
            return Num(other) + self
        def __rsub__(self, other):
            return Num(other) - self
        def __rmul__(self, other):
            return Num(other) * self
        def __rtruediv__(self, other):
            return Num(other) / self
        def __rfloordiv__(self, other):
            return Num(other) // self
        def __rmod__(self, other):
            return Num(other) % self
        def __rpow__(self, other):
            return Num(other) ** self
        def __iadd__(self, other):
            return self + other
        def __isub__(self, other):
            return self - other
        def __imul__(self, other):
            return self * other
        def __itruediv__(self, other):
            return self / other
        def __floordiv__(self, other):
            other_num = self._normalize(Num(other))
            return Num(self.as_mpf // other_num.as_mpf)
        def __mod__(self, other):
            other_num = self._normalize(Num(other))
            return Num(self.as_mpf % other_num.as_mpf)
        def __pow__(self, other):
            '''Note: Powers change units! (m)**2 = m^2'''
            other_val = float(Num(other).as_mpf)
            res_val = self.as_mpf ** other_val
            
            # Create the messy intermediate unit
            messy_unit = f"({self.unit})^{other_val}" if self.unit else ""
            
            # Clean it immediately
            arb = UnitArbiter()
            clean_val, clean_unit = arb.simplify(res_val, messy_unit)
            
            return Num(clean_val, unit=clean_unit)
        def __int__(self):
            return int(self.as_mpf)
        def __float__(self):
            return float(self.as_mpf)
        def __complex__(self):
            return complex(self.real, self.imag)
        def __index__(self):
            '''Allows Num to be used for slicing/bin() if it's an integer.'''
            if self.mytype in (NumType.Int, NumType.Rat):
                return int(self.as_int_or_rat)
            raise TypeError("Only integer-like Nums can be used as indices")
        def __round__(self, ndigits=0):
            return Num(mpmath.nround(self.as_mpf, ndigits), self.unit)
        def __trunc__(self):
            return Num(int(mpmath.trunc(self.as_mpf)), self.unit)
        def __floor__(self):
            return Num(int(mpmath.floor(self.as_mpf)), self.unit)
        def __ceil__(self):
            return Num(int(mpmath.ceil(self.as_mpf)), self.unit)
if 1:   # Num 
    class Num(NumericMixin):
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        flip = False  # If True, flip str() and repr() behavior
        show_color = True   # If True, strip escape sequences from str()/repr() output
        # Note:  it's easiest to set the color property of an instance to set Num.show_color
        #
        # The following dictionary lets the user select which preferred set of
        # unit he wants to use.
        systems = {
                "default": set(),
                "dirt":  set("ft lb yd".split())
        }
        active_system = "default"
        Fmt = fmt.Fmt()
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
            '''Constructor for the Num instance, an immutable number container'''
            self._doc = ""
            self.arb = UnitArbiter()    # Convenience arbiter for new units
            self.fmt = Num.Fmt          # Formatter 
            if isinstance(value, str):
                val_str, found_unit = self._extract_unit(value)
                if found_unit:
                    unit = found_unit if not unit else f"({found_unit})*({unit})"
                value = val_str
            if 1:  # Default internal state representation
                self.numer: int = 0
                self.denom: int = 1
                self.real: mpmath.mpf = mpmath.mpf("0")
                self.imag: mpmath.mpf = mpmath.mpf("0")
                self.re_unc: mpmath.mpf = mpmath.mpf("0")
                self.im_unc: mpmath.mpf = mpmath.mpf("0")
                self.correl: mpmath.mpf = mpmath.mpf("0")
                self._unit = ""
                self.mytype: NumType = NumType.Int
                if unit:
                    RegisterUnit(unit)
                self.unit = unit
                if value is None:
                    return
            if 1:  # High-Precision Conversion Logic
                if isinstance(value, Num):
                    self.numer = value.numer
                    self.denom = value.denom
                    self.real = value.real
                    self.imag = value.imag
                    self.re_unc = value.re_unc
                    self.im_unc = value.im_unc
                    self.unit = unit if unit else value.unit
                    self.mytype = value.mytype
                elif isinstance(value, int):
                    self.numer = int(value)
                    self.mytype = NumType.Int
                elif isinstance(value, float):
                    self.real = mpmath.mpf(repr(value))
                    self.mytype = NumType.Flt
                elif isinstance(value, complex):
                    self.real = mpmath.mpf(repr(value.real))
                    self.imag = mpmath.mpf(repr(value.imag))
                    self.mytype = NumType.Cpx
                elif isinstance(value, decimal.Decimal):
                    self.real = mpmath.mpf(str(value))
                    self.mytype = NumType.Flt
                elif isinstance(value, fractions.Fraction):
                    self.numer = value.numerator
                    self.denom = value.denominator
                    self.mytype = NumType.Rat
                elif hasattr(value, '_mpf_') or isinstance(value, mpmath.mpf):
                    self.real = value
                    self.mytype = NumType.Flt
                elif isinstance(value, mpmath.mpc):
                    self.real = value.real
                    self.imag = value.imag
                    self.mytype = NumType.Cpx
                elif isinstance(value, uncertainties.UFloat):
                    self.real = mpmath.mpf(str(value.nominal_value))
                    self.re_unc = mpmath.mpf(str(value.std_dev))
                    self.mytype = NumType.Unc
                elif isinstance(value, str):
                    self._parse_string(value)
                else:
                    raise TypeError(f"Type of {value!r} is not supported")
        def _parse_proper_fraction(s: str) -> float:
            # Pattern for: 1-1/3 or 1 1/3 or -2-1/2
            # Groups: 1:sign, 2:whole, 3:num, 4:den
            regex = r'^([+-])?(\d+)?(?:[- ](\d+)/(\d+))?$'
            match = re.match(regex, s.strip())
            if not match:
                raise ValueError(f"Invalid fraction format: {s}")
            sign = -1 if match.group(1) == '-' else 1
            whole = int(match.group(2)) if match.group(2) else 0
            num = int(match.group(3)) if match.group(3) else 0
            den = int(match.group(4)) if match.group(4) else 1
            return sign * (whole + (num / den))
        def _parse_string(self, value: str) -> None:
            msg = f"{value!r} not recognized as a number"
            normalized = set(value.lower().replace("i", "j").strip())
            if "-" in value and "/" in value: # Handle 1-1/3
                try:
                    whole, frac = value.split("-")
                    num, den = [int(i) for i in frac.split("/")]
                    w_val = int(whole)
                    self.numer = w_val*den + num
                    self.denom = den
                    self.mytype = NumType.Rat
                except Exception as e:
                    raise ValueError(msg) from e
            elif "/" in normalized:
                try:
                    parts = [int(i) for i in value.split("/")]
                    self.numer = parts[0]
                    self.denom = parts[1]
                    self.mytype = NumType.Rat
                except Exception as e:
                    raise ValueError(msg) from e
            elif "j" in normalized:
                re_part, im_part = dpmath.ParseComplex(value)
                self.real = mpmath.mpf(re_part)
                self.imag = mpmath.mpf(im_part)
                self.mytype = NumType.Cpx
            elif "." in normalized or "e" in normalized:
                try:
                    self.real = mpmath.mpf(value)
                    self.mytype = NumType.Flt
                except Exception as e:
                    raise ValueError(msg) from e
            else:
                try:
                    self.numer = int(value)
                    self.mytype = NumType.Int
                except Exception as e:
                    raise ValueError(msg) from e
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s:
                return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            if target_type <= NumType.Rat.value:
                result = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return Num(result)
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                a_complex = mpmath.mpc(self.real, self.imag)
                b_complex = mpmath.mpc(other.real, other.imag)
                return Num(op_func(a_complex, b_complex))
            return Num(op_func(a_val, b_val))
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            """Adjusts 'other' to match 'self.unit' if they are conformable."""
            if self.unit == other.unit:
                return Num(other)
            # Multiplication and Division are "dimension-agnostic" at this stage; 
            # we combine units in the parent method, so we just return the Num as-is.
            if operation in ('mul', 'div'):
                return Num(other)
            # For addition/subtraction, units MUST match (or both be empty).
            # This is the "Physical Reality" check.
            if operation in ('add', 'sub'):
                if bool(self.unit) != bool(other.unit):
                    raise ValueError(f"Unit Mismatch: Cannot {operation} '{self.unit}' and '{other.unit}'")
            # If we got here, we are doing a cross-unit comparison or addition (e.g., N + lbf).
            # If one is empty and the other isn't, they are fundamentally non-conformable.
            if bool(self.unit) != bool(other.unit):
                raise ValueError(f"Unit Mismatch: '{self.unit}' is not conformable with dimensionless '{other.unit}'")
            # The Arbiter handles the "Bridge" between conformable units (e.g., N vs lbf)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            # Promotion and scaling logic
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf * factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real = adjusted.real * factor
                adjusted.imag = adjusted.imag * factor
            adjusted.unit = self.unit
            return adjusted
        def __add__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num, operation='add') # Note the 'add' flag
            result = self._binary_op(adjusted, operator.add)
            
            arb = UnitArbiter()
            clean_val, clean_unit = arb.simplify(result.as_mpf, self.unit)
            return Num(clean_val, unit=clean_unit)
        def __sub__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num, operation='sub') # Note the 'sub' flag
            result = self._binary_op(adjusted, operator.sub)
            
            arb = UnitArbiter()
            clean_val, clean_unit = arb.simplify(result.as_mpf, self.unit)
            return Num(clean_val, unit=clean_unit)
        def __mul__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            result = self._binary_op(other_num, operator.mul)
            
            # Build the messy string
            if not self.unit and not other_num.unit:
                messy = ""
            elif self.unit and not other_num.unit:
                messy = self.unit
            elif not self.unit and other_num.unit:
                messy = other_num.unit
            else:
                messy = f"({self.unit})*({other_num.unit})"
            
            arb = UnitArbiter()
            clean_val, clean_unit = arb.simplify(result.as_mpf, messy)
            return Num(clean_val, unit=clean_unit)
        def __truediv__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            if other_num.as_mpf == 0:
                raise ZeroDivisionError("Tractor at 0 divisor.")
            result = self._binary_op(other_num, operator.truediv)
            
            # Build the messy string
            if not self.unit and not other_num.unit:
                messy = ""
            elif self.unit and not other_num.unit:
                messy = self.unit
            elif not self.unit and other_num.unit:
                messy = f"1/({other_num.unit})"
            else:
                messy = f"({self.unit})/({other_num.unit})"
                
            arb = UnitArbiter()
            clean_val, clean_unit = arb.simplify(result.as_mpf, messy)
            return Num(clean_val, unit=clean_unit)
        def __rmul__(self, other: ty.Any) -> "Num":
            return self.__mul__(other)
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other)/self
        def _compare(self, other: ty.Any, op_func: ty.Callable) -> bool:
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            target_type = max(self.mytype.value, adjusted.mytype.value)
            if target_type <= NumType.Rat.value:
                return op_func(self.as_int_or_rat, adjusted.as_int_or_rat)
            return bool(op_func(self.as_mpf, adjusted.as_mpf))
        def __lt__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.lt)
        def __le__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.le)
        def __gt__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.gt)
        def __ge__(self, other: ty.Any) -> bool:
            return self._compare(other, operator.ge)
        def __eq__(self, other: ty.Any) -> bool:
            other_num = Num(other)
            if self.unit != other_num.unit:
                return False
            target_type = max(self.mytype.value, other_num.mytype.value)
            if target_type <= NumType.Rat.value:
                return self.as_int_or_rat == other_num.as_int_or_rat
            return bool(self.as_mpf == other_num.as_mpf)
        def _s(self) -> str:
            '''Return the str() representation.  This will be the colorized and
            formatted version.
            '''
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                s = self.fmt(mpmath.mpc(self.real, self.imag))
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
                Warn("str() not right for Unc type")
            else:
                s = self.fmt(self.real)
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            result = f"{color}{s}{t.n}{unit_string}"
            return result
        def _r(self) -> str:
            '''Return the repr() representation.  This will be the pure string form that
            can be used as the argument to the constructor to reproduce the number.
            '''
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.real!r}+{self.imag!r}j"
                Warn("repr() not right for Unc type")
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = f"{self.real!r}"
            if self.unit.strip():
                s += f" {self.unit}"
            result = f"Num('{s}')"
            return result
        def __str__(self) -> str:
            return self._r() if Num.flip else self._s()
        def __repr__(self) -> str:
            return self._s() if Num.flip else self._r()
        def u(self, conversion_str: str) -> "Num":
            if "," not in conversion_str:
                raise ValueError("Format must be '<from> , <to>'")
            have, want = [part.strip() for part in conversion_str.split(",", 1)]
            arbiter = UnitArbiter()
            is_ok, result_str = arbiter.check_conformable(have, want)
            if is_ok:
                try:
                    return Num(result_str, want)
                except Exception as e:
                    raise ValueError(f"Could not parse units result '{result_str}': {e}")
            else:
                raise ValueError(f"GNU Units Error: {result_str}")
        def _sync_to_db(self) -> None:
            lwtest.ToDo("Num._sync_to_db needs implementation")
        def promote(self) -> "Num":
            if not self.unit:
                return self
            arbiter = UnitArbiter()
            candidate = arbiter.discover_best_unit(self.unit)
            if candidate == self.unit:
                return self
            is_ok, factor_str = arbiter.check_conformable(self.unit, candidate)
            if is_ok:
                factor = mpmath.mpf(factor_str)
                if self.round_off(factor, digits=12) == 1:
                    return self.to(candidate)
            return self
        def round_off(self, val: ty.Any, digits: int = 12) -> ty.Any:
            if isinstance(val, (int, fractions.Fraction)):
                return val
            if isinstance(val, mpmath.mpf):
                d = decimal.Decimal(mpmath.nstr(val, 17))
                with decimal.localcontext() as ctx:
                    ctx.prec = digits
                    d = +d
                return mpmath.mpf(str(d))
            return val
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit:
                return Num(self)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
            if not is_ok:
                RegisterUnit(unit)
                is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
                if not is_ok:
                    raise ValueError(f"Incompatible units: {self.unit} and {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            if res.mytype <= NumType.Rat:
                res.real = res.as_mpf*factor
                res.mytype = NumType.Flt
            else:
                res.real = res.real*factor
                res.imag = res.imag*factor
            res.unit = unit
            if auto_promote:
                return res.promote()
            return res
        def add_unit(self, definition: str) -> None:
            arb = UnitArbiter()
            arb.add_unit(definition)
        def check(self, unit_name: str, timeout: float = 0.5) -> bool:
            """
            Non-blocking check using the established GNU Units configuration.
            Returns True if the unit is valid, False otherwise.
            """
            # Replicate the command logic from _start_process
            cmd = [UnitArbiter.units_bin, "-q"]
            if UnitArbiter.main_config:
                main_p = str(Path(UnitArbiter.main_config).expanduser())
                cmd.extend(["-f", main_p])
            cmd.extend(["-f", str(UnitArbiter.dynamic_config)])
            # We use the '-t' flag (terse/check mode) which makes Units
            # exit immediately with the definition or an error.
            cmd.append("-t")
            cmd.append(unit_name)
            try:
                # run() is synchronous but we wrap it in a timeout
                # to ensure it never hangs the REPL.
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                # returncode 0 means GNU Units found the definition.
                return result.returncode == 0
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                # If it times out or crashes, it's effectively an unknown unit.
                return False
        if 1:   # Class methods
            @classmethod
            def to_global_namespace(cls, func_names: list[str]):
                # Get the caller's global namespace
                target_globals = sys._getframe(1).f_globals
                for name in func_names:
                    if not hasattr(mpmath, name):
                        print(f"Warning: mpmath has no function '{name}'")
                        continue
                    f = getattr(mpmath, name)
                    # Create the closure
                    def make_wrapper(func):
                        def wrapper(x, *args, **kwargs):
                            # If it's a Num, operate on the value but keep the unit
                            if isinstance(x, cls):
                                val = func(x.real, *args, **kwargs)
                                return cls(val, unit=x.unit)
                            return func(x, *args, **kwargs)
                        return wrapper
                    target_globals[name] = make_wrapper(f)
            @classmethod
            def define_system(cls, name: str, unit_list: list[str]):
                '''Define a named set of preferred units: e.g., Num.define_system("yard", ["ft", "lb", "truck"])'''
                cls.systems[name] = [u.strip() for u in unit_list]
            @classmethod
            def set_system(cls, name: str):
                '''Switch the active preference set'''
                if name in cls.systems:
                    cls.active_system = name
                else:
                    print(f"Warning: System '{name}' not found. Staying at '{cls.active_system}'")
            @property
            def preferred(self):
                '''Instance property to check or quickly set the system'''
                return self.systems[Num.active_system]
        if 1:   # Properties
            if 1:   # f:  exchanges the repr() and str() strings.  This is handy in the
                    # debugger, as 'p x' shows the repr() string and often you want to see the
                    # str() string.
                @property
                def f(self) -> bool:
                    return Num.flip
                @f.setter
                def f(self, value) -> None:
                    Num.flip = bool(value)
            if 1:   # unit:  gets or changes the unit attribute.
                @property
                def unit(self) -> str:
                    return self._unit.strip()
                @unit.setter
                def unit(self, new_unit: str):
                    if not hasattr(self, '_unit') or not self._unit:
                        self._unit = new_unit
                        return
                    if self._unit == new_unit:
                        return
                    arb = UnitArbiter()
                    is_ok, factor_str = arb.check_conformable(self._unit, new_unit)
                    if is_ok:
                        factor = mpmath.mpf(factor_str)
                        # Consistent Scaling across all internal types
                        if self.mytype <= NumType.Rat:
                            # Scale the rational/integer value and promote to Float
                            self.real = self.as_mpf * factor
                            self.mytype = NumType.Flt
                        else:
                            self.real *= factor
                            self.imag *= factor
                            self.re_unc *= factor
                            self.im_unc *= factor
                        self._unit = new_unit
                    else:
                        raise ValueError(f"Incompatible Units: Cannot view {self._unit} as {new_unit}")
            if 1:   # as_mpf:  return current value as an mpf
                @property
                def as_mpf(self) -> mpmath.mpf:
                    if self.mytype == NumType.Int:
                        return mpmath.mpf(str(self.numer))
                    if self.mytype == NumType.Rat:
                        return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
                    return self.real
            if 1:   # as_int_or_rat:  return current value as an int or fractions.Fraction
                @property
                def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
                    if self.mytype == NumType.Int:
                        return self.numer
                    return fractions.Fraction(self.numer, self.denom)
            if 1:   # d:  set or return the instance's documentation string, held
                    # internally in self._doc.  Note the setter method cause a logging
                    # to the database for persistence, just as if you had written in a
                    # lab notebook.
                @property
                def d(self) -> str:
                    return self._doc
                @d.setter
                def d(self, text: str) -> None:
                    self._doc = text
                    self._sync_to_db()
            if 1:   # color:  if True, allow return of escape codes
                @property
                def color(self) -> bool:
                    return Num.show_color
                @d.setter
                def color(self, value: bool) -> None:
                    Num.show_color = bool(value)
            if 1:   # num:  x/x.num returns Num("1 <x's units>")
                @property
                def num(self) -> Num:
                    y = Num(self)
                    y._unit = ""
                    return y

if 1:  # Unit arbiter
    class UnitArbiter:
        _instance = None
        # Class-level configuration defaults
        units_bin: str = "units"
        main_config: str = ""
        dynamic_config: str = "~/.units_dynamic"
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized:
                return
            # Resolve all paths to handle ~ expansion
            self.bin_path = str(Path(UnitArbiter.units_bin).expanduser())
            self.dynamic_path = Path(UnitArbiter.dynamic_config).expanduser()
            if not self.dynamic_path.exists():
                self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
        def _start_process(self) -> None:
            if self.proc:
                try:
                    self.proc.terminate()
                    self.proc.wait(timeout=0.5)
                except:
                    self.proc.kill()
            # Build command: [bin] -q [-f main] -f dynamic
            cmd = [self.bin_path, "-q"]
            if UnitArbiter.main_config:
                main_p = str(Path(UnitArbiter.main_config).expanduser())
                cmd.extend(["-f", main_p])
            cmd.extend(["-f", str(self.dynamic_path)])
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def is_known_unit(self, unit_str: str) -> bool:
            '''Checks if GNU Units recognizes the unit string.'''
            if not unit_str:
                return True
            # If we can check conformability against itself, it's a known unit
            ok, _ = self.check_conformable(unit_str, unit_str)
            return ok
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            '''Runs units -c to validate a new unit definition before committing.'''
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            cmd = [self.bin_path, "-c", "-q"]
            if UnitArbiter.main_config:
                main_p = str(Path(UnitArbiter.main_config).expanduser())
                cmd.extend(["-f", main_p])
            cmd.extend(["-f", str(self.dynamic_path), "-f", tmp_path])
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                is_ok = (result.returncode == 0)
                error_msg = result.stderr or result.stdout
            except subprocess.TimeoutExpired:
                is_ok, error_msg = False, "Circular definition detected (Check timed out)."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return is_ok, error_msg
        def add_base(self, unit_name: str) -> None:
            '''Adds a new base dimension (primitive) to the dynamic units file.'''
            self._commit_unit(f"{unit_name.strip()} !")
        def add_unit(self, definition: str) -> None:
            '''Adds a derived unit (e.g., 'mph = mile/hr') to the dynamic units file.'''
            sanitized = definition.replace("=", "").strip()
            self._commit_unit(sanitized)
        def _commit_unit(self, entry: str) -> None:
            '''Validates and appends a unit entry to the persistent dynamic file.'''
            # First, check if this exact entry already exists in the dynamic file
            if self.dynamic_path.exists():
                with open(self.dynamic_path, "r") as f:
                    if entry in f.read():
                        return
            is_ok, error = self._check_definition(entry)
            if is_ok:
                with open(self.dynamic_path, "a") as f:
                    f.write(f"{entry}\n")
                self._start_process()
                # Silencing the "learned" print to keep REPL startup clean
            else:
                # Only complain if there's an actual error
                if "not found" not in error.lower():
                    print(f"Unit Definition Error: {error.strip()}")
        def _translate_unicode(self, s: str) -> str:
                """Sanitizes exponents and common symbols for the units binary."""
                exp_map = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
                out = ""
                for char in s:
                    if char in "⁰¹²³⁴⁵⁶⁷⁸⁹":
                        out += "^" + char.translate(exp_map)
                    else:
                        out += char
                return out
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            """Queries the running units process with safety checks for empty strings."""
            if not have or not want:
                if have == want:
                    return True, "1.0"
                return False, f"Cannot conform '{have}' to '{want}'"
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            have = self._translate_unicode(have)
            want = self._translate_unicode(want)
            try:
                # We MUST use -q but AVOID -v here because -v adds extra lines of output
                # that break our synchronized readline logic.
                self.proc.stdin.write(f"{have}\n{want}\n")
                self.proc.stdin.flush()
                # Read until we find a conversion factor or an error
                # GNU Units usually outputs the * factor first, then the / factor.
                for _ in range(5):  # Safety limit to prevent infinite hang
                    line = self.proc.stdout.readline().strip()
                    if not line:
                        continue
                    if line.startswith("*"):
                        return True, line.replace("*", "").strip()
                    if line == "1" or line == "1.0":
                        return True, "1.0"
                    if "conformability error" in line.lower():
                        return False, f"Incompatible dimensions: {have} vs {want} ({line})"
                return False, "Unexpected output format from units process"
            except Exception as e:
                self._start_process()
                return False, str(e)
        def simplify(self, value: mpmath.mpf, unit_str: str) -> tuple[mpmath.mpf, str]:
                if not unit_str or unit_str == "1":
                    return value, ""
                reduced_unit_str, scale_factor = self._query_units_for_reduction(unit_str)
                current_value = value * mpmath.mpf(scale_factor)
                # Updated Step 2: Check against the Active Preferred System
                # We grab the list from the Num class registry
                preferred_units = Num.systems.get(Num.active_system, [])
                for candidate in preferred_units:
                    # Check if our messy result is conformable to a preferred unit (or power of it)
                    # We check both the unit and its common powers (unit^2, unit^3) for areas/volumes
                    for power in [1, 2, 3]:
                        test_unit = candidate if power == 1 else f"{candidate}^{power}"
                        is_ok, factor = self.check_conformable(reduced_unit_str, test_unit)
                        if is_ok:
                            return current_value * mpmath.mpf(factor), test_unit
                # Fallback to whatever messy reduction GNU Units provided
                return current_value, reduced_unit_str
        def _query_units_for_reduction(self, unit_str: str) -> tuple[str, str]:
            """
            Uses the GNU Units 'Definition' logic to flatten a unit string.
            Example: 'yard^2 inches / ft^3' -> '0.75' (dimensionless volume ratio)
            """
            # We use a one-off subprocess call with --compact to get the 'Definition'
            # without the interactive noise.
            cmd = [self.bin_path, "-q", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            # The command: units [options] "messy_unit"
            result = subprocess.run(cmd + [self._translate_unicode(unit_str)],
                                    capture_output=True, text=True)
            # GNU Units returns 'Definition: [factor] [unit]' or just '[factor] [unit]'
            # We want to split the number from the unit string.
            output = result.stdout.strip()
            # Regex to catch: "1.23 kg" or "0.75" or "1 kg/m"
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            if match:
                factor = match.group(1) or "1.0"
                remainder = match.group(2) or ""
                return remainder.strip(), factor
            return unit_str, "1.0"
        def _extract_candidate_units(self, unit_str: str) -> list[str]:
            """Helper to pull potential target units out of a messy string."""
            # Split by any non-alphanumeric characters and filter common junk
            raw_tokens = re.split(r'[^a-zA-Z]', unit_str)
            return [t for t in raw_tokens if t and len(t) > 1 and not t.isdigit()]

if 1:  # Utility functions
    def RegisterUnit(unit_name: str) -> None:
        '''
        Gatekeeper for the Num constructor. If a unit is unknown,
        it is registered as a new base (primitive) dimension.
        '''
        arb = UnitArbiter()
        if not arb.is_known_unit(unit_name):
            arb.add_base(unit_name)
    def e(n: "Num"):
        '''The "Editor" command. Spawns your $EDITOR with the Num's state.'''
        import tempfile, os, subprocess
        initial_text = f"Unit: {n.unit}\nValue: {n.real}\nDoc: {n.d}"
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='w+', delete=False) as tf:
            tf.write(initial_text)
            temp_path = tf.name
        # Fire up vi/vim/nano
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_path])
        # ... logic to read the file back and update n.d ...
        print(f"Updated {n.unit} metadata.")

if 1:   # Set up config files   ∞∞2 This needs to move out of the main code area
    UnitArbiter.main_config = "/home/don/.0rc/bin/definitions.units"
    UnitArbiter.dynamic_config = "/home/don/.units_dynamic"
    UnitArbiter.units_bin = "/home/don/.0rc/bin/units"
if 0:  # Temp experiment
    x = Num("1 step")
    x.add_unit("steps = step")
    exit()
if 1:   # Self-tests
        def Test_Constructor_With_Numbers():
            if 1:   # No input
                num = Num()
                Assert(num.real == 0 and num.imag == 0)
                Assert(num.mytype == NumType.Int)
            if 1:   # int
                if 1:   # Positive
                    x, T = 30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                if 1:   # Negative
                    x, T = -30957357, NumType.Int
                    num = Num(x)
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
                    # As string
                    num = Num(str(x))
                    Assert(num.numer == x and num.denom == 1)
                    Assert(num.mytype == T)
            if 1:   # Rational
                x, T = "-3/8", NumType.Rat
                num = Num(x)
                Assert(num.numer == -3 and num.denom == 8)
                Assert(num.mytype == T)
            if 1:   # float
                x, T = 3095.7357, NumType.Flt
                num = Num(x)
                Assert(num.real == x and num.imag == 0)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == 0)
                Assert(num.mytype == T)
            if 1:   # Decimal
                s = "3095.7357"
                x, T = decimal.Decimal(s), NumType.Flt
                num = Num(x)
                Assert(num.real == mpmath.mpf(s) and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # mpmath.mpf
                s, T = "3095.7357", NumType.Flt
                x = mpmath.mpf(s)
                num = Num(x)
                Assert(num.real == x and num.imag == zero)
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == -x and num.imag == zero)
                Assert(num.mytype == T)
            if 1:   # Complex
                x, T = -1+3j, NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # mpmath.mpc
                x, T = mpmath.mpc(-1, 3), NumType.Cpx
                num = Num(x)
                Assert(num.real == mpmath.mpf(-1) and num.imag == mpmath.mpf(3))
                Assert(num.mytype == T)
                num = Num(-x)
                Assert(num.real == mpmath.mpf(1) and num.imag == mpmath.mpf(-3))
                Assert(num.mytype == T)
            if 1:   # Rational
                pass
            if 1:   # Unc
                pass
        def Test_Constructor_Strings():
            test_cases = [("1", NumType.Int),
                          ("1/2", NumType.Rat),
                          ("1.2", NumType.Flt),
                          ("1.2e3", NumType.Flt),
                          ("1+2j", NumType.Cpx)]
            for s, typ in test_cases:
                x = Num(s)
                Assert(x.mytype == typ, got=typ, expected=x.mytype)
                # Check numerical value
                if s == "1":
                    Assert(x.numer == 1 and x.denom == 1)
                elif s == "1/2":
                    Assert(x.numer == 1 and x.denom == 2)
                elif s == "1.2":
                    Assert(x.real == mpmath.mpf("1.2") and x.imag == zero)
                elif s == "1.2e3":
                    Assert(x.real == mpmath.mpf("1.2e3") and x.imag == zero)
                elif s == "1+2j":
                    Assert(x.real == mpmath.mpf("1") and x.imag == mpmath.mpf("2"))
        def Test_Arithmetic():
            if 1:   # Test addition
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x + y
                    expected = "4.28083989501312"   # 15 digit GNU units answer
                    expected = "4.2808399000000001"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x + y
                    expected = Num("15/8", "in")
                    Assert(result == expected)
                    # See if an integer and fraction remain a fraction
                    x = Num("3/8")
                    y = Num("1")
                    result = x + y
                    expected = Num("11/8")
                    Assert(result == expected)
                    # Fraction and float should give a float
                    x = Num("3/8")
                    y = Num("1.0")
                    result = x + y
                    expected = Num("1.375") # Fractions that are powers of 2 are exact floats
                    Assert(result == expected)
            if 1:   # Test subtraction
                if 1:   # Integer & real
                    x = Num("1", "ft")
                    y = Num("1", "m")
                    result = x - y
                    expected = "-2.2808398950131199"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "ft"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x - y
                    expected = Num("-9/8", "in")   # 3/8 - 12/8 = 9/8
                    Assert(result == expected)
            if 1:   # Test multiplication
                if 1:   # Integer & real
                    x = Num("1.5", "V")
                    y = Num("2.0", "A")
                    result = x*y
                    expected = "3.0"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "(V)*(A)"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x*y
                    expected = Num("9/16", "(in)*(in)")   # 3/8*12/8 = 36/64 = 9/16
                    Assert(result == expected)
            if 1:   # Test division
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x/y
                    expected = "1.0"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "(ft)/(m)"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x/y
                    expected = Num("1/4", "(in)/(in)")   # (3/8)/(12/8) = 1/4
                    Assert(result == expected)
        def Test_Noether_Invariant():
            '''The .num component is used to normalize to a "unit vector" in the
            particular "unit" vector's direction.  This means that x/x.num returns a Num
            with unit numerical magnitude and the same units of x.  This is analogous to
            how you normalize in linear vector spaces:  a unit vector in the direction
            of v is v/|v|.
            
            I think it would be fitting to call this x/x.num the "Noether invariant";
            it's really the "unit vector" in the dimensional space described by the
            units.
            '''
            x = Num("1.23 A")
            Assert(x.real == mpmath.mpf("1.23"))
            Assert(x.unit == "A")
            y = x/x.num
            # Now y is in some sense a unit vector in the units space
            Assert(y == Num("1 A"))
            Assert(y.unit == x.unit)    # Make sure units didn't change
            Assert(x.num*y == x)        # Demonstrate the Noether invariance

        def Test_Corners():
            N = Num
            if 1:   # 0 and 1
                # Addition
                Assert(N(0) + N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1) + N(1) == N("2+0i") == N("4/2"))
                Assert(N(-1) + N(-1) == N("-2+0i") == N("-4/2"))
                # Subtraction
                Assert(N(0) - N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1) - N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(-1) - N(-1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                # Multiplication
                Assert(N(0)*N(0) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1)*N(1) == N("1+0i") == N("2/2"))
                # Division
                Assert(N(0)/N(1) == N("0+0i") == N("0/1") == N("0.-0.i"))
                Assert(N(1)/N(1) == N("1+0i") == N("2/2"))
            if 1:   # With units
                with g:
                    g.X = 1
                Assert(N("0 m") + N("0 m") == N("0 m"))
            if 1:   # "1+2i m" * "3/4 A":  hope we don't get mA
                a = N("1+2i m")
                b = N("3/4 A")
                lwtest.ToDo("Bug in '1+2i m'*'3/4 A' -> 0.00+0.00j (m)*(A)")
                breakpoint() # ∞∞ 
                Assert(a*b == N("0.75+1.5i m*A"))
if __name__ == "__main__":  
    Test_Noether_Invariant()
    print("passed")
    exit()
'''
Other tests needed:
    - '0 m' + '0 J' -> error
    - '1 m' + '1 J' -> error
    - '3 m' % '14 j' (error, units must be conformable)
    - General:  x ⚬ y OK if units are conformable, result gets units of 1st arg
    - inf and nan
        - '3 + nan i'?, should stay in ℂ?
    - Nails:  ϵ + i, 1 + ϵi
    - '1.23453094830853048309739047394739473947394739473947e4 m3' Does GNU units barf
      on this?  No, handles it fine; appears to handle unlimited digits.

'''
if __name__ == "__main__":  
    if 1:   # Standard imports
        import getopt
    if 1:   # Custom imports
        pass
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 1:   # Utility stuff for a script
        def GetScreen():
            'Return (LINES, COLUMNS)'
            return (
                int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1,
            )
        def GetColors():
            t.err = "redl"
        #def Warn(*msg, **kw):
        #    print(*msg, file=sys.stderr)
        #def Error(*msg, status=1):
        #    Warn(f"{t.err}", end="")
        #    Warn(*msg)
        #    Warn(f"{t.n}")
        #    exit(status)
        def Usage(status=1):
            print(wrap.dedent(f'''
            Usage:  {sys.argv[0]} [options] [arg1 [arg2...]]
            Describe behavior
            Options:
                -d      Turn on debug printing
                -n n    Set number of digits [15]
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-d"] = False     # Debug printing
            d["-n"] = 15        # Number of mpmath digits
            try:
                opts, args = getopt.getopt(sys.argv[1:], "dh")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("d"):
                    d[o] = not d[o]
                elif o == "-n":
                    try:
                        d[o] = int(a)
                        if d[o] < 1:
                            raise ValueError()
                    except Exception:
                        Error(f"{o!r} option must be an int >= 1")
                elif o == "-h":
                    Usage(status=0)
            GetColors()
            g.W, g.L = GetScreen()
            if d["-d"]:
                with g:
                    g.dbg = True
            return args
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    #if args:
    #    for arg in args:
    #        pass    # Do stuff
    exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
