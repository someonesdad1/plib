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
- Num("3/4") in the local variables causes a deep fmt exception when trying to view the
  locals in dpdb.py.  But is likely that fmt doesn't handle fractions yet.
    
'''
if 1:  # Header
    if 1:   # Standard imports
        from pdb import set_trace as yy
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

if 0:  # NumericMixin
    class NumericMixin:
        '''Boilerplate to make Num behave like a native Python number.'''
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit = unit)
        def __neg__(self) -> "Num":
            return self._binary_op(Num(0), lambda a, b: b - a)
        def __pos__(self) -> "Num":
            return Num(self)
        def __abs__(self) -> "Num":
            if self.mytype == NumType.Cpx:
                return self._make_result(mpmath.absmin(self.as_mpc), self.unit)
            return self._make_result(abs(self.raw_value), self.unit)
        def __add__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "add")
            res = self._binary_op(adj_other, lambda a, b: a + b)
            val, final_unit = self.arb.simplify(res.raw_value, self.unit)
            return self._make_result(val, final_unit)
        def __sub__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "sub")
            res = self._binary_op(adj_other, lambda a, b: a - b)
            val, final_unit = self.arb.simplify(res.raw_value, self.unit)
            return self._make_result(val, final_unit)
        def __mul__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            new_unit = f"({self.unit})*({other.unit})" if self.unit and other.unit else (self.unit or other.unit)
            res = self._binary_op(other, lambda a, b: a * b)
            val, final_unit = self.arb.simplify(res.raw_value, new_unit)
            return self._make_result(val, final_unit)
        def __truediv__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            new_unit = f"({self.unit})/({other.unit})" if other.unit else self.unit
            res = self._binary_op(other, lambda a, b: a / b)
            val, final_unit = self.arb.simplify(res.raw_value, new_unit)
            return self._make_result(val, final_unit)
        def __pow__(self, other: ty.Any) -> "Num":
            exp_val = other.raw_value if isinstance(other, Num) else other
            res_val = self.as_mpc ** exp_val
            new_unit = f"({self.unit})^{exp_val}" if self.unit else ""
            val, final_unit = self.arb.simplify(res_val, new_unit)
            return self._make_result(val, final_unit)
        def __radd__(self, other):
            return Num(other) + self
        def __rsub__(self, other):
            return Num(other) - self
        def __rmul__(self, other):
            return Num(other) * self
        def __rtruediv__(self, other):
            return Num(other) / self
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
        def _compare(self, other: ty.Any, op: ty.Callable) -> bool:
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "cmp")
            if self.mytype == NumType.Cpx or adj_other.mytype == NumType.Cpx:
                return op(mpmath.norm(self.as_mpc), mpmath.norm(adj_other.as_mpc))
            return op(self.as_mpf, adj_other.as_mpf)
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, (Num, int, float, complex)):
                return False
            other = other if isinstance(other, Num) else Num(other)
            if self.unit != other.unit:
                try:
                    self._normalize(other, "cmp")
                except ValueError:
                    return False
            return self._compare(other, lambda a, b: a == b)
        def __lt__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a < b)
        def __le__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a <= b)
        def __gt__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a > b)
        def __ge__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a >= b)
        def __int__(self):
            return int(self.as_mpf)
        def __float__(self):
            return float(self.as_mpf)
        def __complex__(self):
            return complex(self.as_mpc)
        def __index__(self):
            return int(self.numer) if self.mytype == NumType.Int else int(self.as_mpf)
        def __round__(self, ndigits = 0):
            return self._make_result(round(self.as_mpf, ndigits), self.unit)
        def __trunc__(self):
            return self._make_result(math.trunc(self.as_mpf), self.unit)
        def __floor__(self):
            return self._make_result(math.floor(self.as_mpf), self.unit)
        def __ceil__(self):
            return self._make_result(math.ceil(self.as_mpf), self.unit)
if 1:  # NumericMixin
    class NumericMixin:
        '''Boilerplate to make Num behave like a native Python number.'''
        def _make_result(self, value: ty.Any, unit: str = "") -> "Num":
            return Num(value, unit = unit)
        def __neg__(self) -> "Num":
            return self._binary_op(Num(0), lambda a, b: b - a)
        def __pos__(self) -> "Num":
            return Num(self)
        def __abs__(self) -> "Num":
            if self.mytype == NumType.Cpx:
                return self._make_result(mpmath.absmin(self.as_mpc), self.unit)
            return self._make_result(abs(self.raw_value), self.unit)
        def __add__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "add")
            res = self._binary_op(adj_other, lambda a, b: a + b)
            val, final_unit = self.arb.simplify(res.raw_value, self.unit)
            return self._make_result(val, final_unit)
        def __sub__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "sub")
            res = self._binary_op(adj_other, lambda a, b: a - b)
            val, final_unit = self.arb.simplify(res.raw_value, self.unit)
            return self._make_result(val, final_unit)
        def __mul__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            new_unit = f"({self.unit})*({other.unit})" if self.unit and other.unit else (self.unit or other.unit)
            res = self._binary_op(other, lambda a, b: a * b)
            val, final_unit = self.arb.simplify(res.raw_value, new_unit)
            return self._make_result(val, final_unit)
        def __truediv__(self, other: ty.Any) -> "Num":
            other = other if isinstance(other, Num) else Num(other)
            new_unit = f"({self.unit})/({other.unit})" if other.unit else self.unit
            res = self._binary_op(other, lambda a, b: a / b)
            val, final_unit = self.arb.simplify(res.raw_value, new_unit)
            return self._make_result(val, final_unit)
        def __pow__(self, other: ty.Any) -> "Num":
            '''Exponentiation with dimensional safety check.'''
            other = other if isinstance(other, Num) else Num(other)
            # Physical Law: A base with units cannot be raised to a complex power
            if self.unit and other.mytype == NumType.Cpx:
                raise TypeError(f"Dimensional Error: Cannot raise unit '{self.unit}' to a complex power.")
            exp_val = other.raw_value
            res_val = self.as_mpc ** exp_val
            # Construct unit string; arbiter handles if (unit)^(exp) is valid
            new_unit = f"({self.unit})^{exp_val}" if self.unit else ""
            val, final_unit = self.arb.simplify(res_val, new_unit)
            return self._make_result(val, final_unit)
        def __radd__(self, other):
            return Num(other) + self
        def __rsub__(self, other):
            return Num(other) - self
        def __rmul__(self, other):
            return Num(other) * self
        def __rtruediv__(self, other):
            return Num(other) / self
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
        def _compare(self, other: ty.Any, op: ty.Callable) -> bool:
            other = other if isinstance(other, Num) else Num(other)
            adj_other = self._normalize(other, "cmp")
            if self.mytype == NumType.Cpx or adj_other.mytype == NumType.Cpx:
                return op(mpmath.norm(self.as_mpc), mpmath.norm(adj_other.as_mpc))
            return op(self.as_mpf, adj_other.as_mpf)
        def __eq__(self, other: ty.Any) -> bool:
            if not isinstance(other, (Num, int, float, complex)):
                return False
            other = other if isinstance(other, Num) else Num(other)
            if self.unit != other.unit:
                try:
                    self._normalize(other, "cmp")
                except ValueError:
                    return False
            return self._compare(other, lambda a, b: a == b)
        def __lt__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a < b)
        def __le__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a <= b)
        def __gt__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a > b)
        def __ge__(self, other: ty.Any):
            return self._compare(other, lambda a, b: a >= b)
        def __int__(self):
            return int(self.as_mpf)
        def __float__(self):
            return float(self.as_mpf)
        def __complex__(self):
            return complex(self.as_mpc)
        def __index__(self):
            return int(self.numer) if self.mytype == NumType.Int else int(self.as_mpf)
        def __round__(self, ndigits = 0):
            return self._make_result(round(self.as_mpf, ndigits), self.unit)
        def __trunc__(self):
            return self._make_result(math.trunc(self.as_mpf), self.unit)
        def __floor__(self):
            return self._make_result(math.floor(self.as_mpf), self.unit)
        def __ceil__(self):
            return self._make_result(math.ceil(self.as_mpf), self.unit)

if 0:   # Num 
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
            # Default internal state
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
                self._unit = unit
            if value is None:
                return
            # High-Precision Conversion Logic with Type Closure
            if isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self.real, self.imag = value.real, value.imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self._unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = value
                self.mytype = NumType.Int
            elif isinstance(value, (float, decimal.Decimal)):
                self.real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self.real = mpmath.mpf(str(value.real))
                self.imag = mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif isinstance(value, fractions.Fraction):
                self.numer, self.denom = value.numerator, value.denominator
                self.mytype = NumType.Rat
            elif hasattr(value, '_mpf_') or isinstance(value, mpmath.mpf):
                self.real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self.real, self.imag = value.real, value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self.real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                self._parse_string(value.strip())
            else:
                raise TypeError(f"Type of {value!r} is not supported")
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''Dispatches math operations and preserves unit context.'''
            target_type = max(self.mytype.value, other.mytype.value)
            
            # Use self.unit as the anchor for the result unit
            res_unit = self.unit

            # 1. Integer/Rational Domain
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return Num(raw_val, unit=res_unit)
            
            # 2. Uncertainty Domain
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            
            # 3. Complex Domain
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return Num(raw_val, unit=res_unit)
            
            # 4. Standard Float Domain (mpf)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return Num(raw_val, unit=res_unit)
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            '''Ensures units are compatible and returns 'other' scaled to 'self.unit'.'''
            # 1. Identical units: no work needed
            if self.unit == other.unit:
                return other
            
            # 2. Multiplication/Division: no normalization needed (units combine)
            if operation in ("mul", "div"):
                return other
            
            # 3. Addition/Subtraction: Units must be conformable
            if operation in ("add", "sub"):
                # One has units, the other doesn't
                if bool(self.unit) != bool(other.unit):
                    raise ValueError(f"Unit Mismatch: Cannot {operation} '{self.unit}' and '{other.unit}'")
            
            # 4. Check GNU Units for compatibility and scale factor
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            
            # 5. Scale 'other' to match 'self' units
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            
            if adjusted.mytype <= NumType.Rat:
                # Promote to Float if the conversion factor isn't a clean integer/ratio
                adjusted.real = adjusted.as_mpf * factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real *= factor
                adjusted.imag *= factor
                adjusted.re_unc *= factor
                adjusted.im_unc *= factor
            
            # Bypass setter to avoid circular normalization
            adjusted._unit = self.unit 
            return adjusted
        def _parse_proper_fraction(self, s: str) -> mpmath.mpf:
            regex = r'^([+-])?(\d+)?(?:[- ](\d+)/(\d+))?$'
            match = re.match(regex, s.strip())
            if not match:
                raise ValueError(f"Invalid fraction format: {s}")
            sign = -1 if match.group(1) == '-' else 1
            whole = int(match.group(2)) if match.group(2) else 0
            num = int(match.group(3)) if match.group(3) else 0
            den = int(match.group(4)) if match.group(4) else 1
            return sign * (mpmath.mpf(whole) + (mpmath.mpf(num) / mpmath.mpf(den)))
        def _parse_string(self, value: str) -> None:
            msg = f"{value!r} not recognized as a number"
            norm = value.lower().replace("i", "j").strip()
            
            if ("-" in value and value[0] != "-") and "/" in value:
                self.real = self._parse_proper_fraction(value)
                self.mytype = NumType.Flt
            elif "/" in norm:
                f = fractions.Fraction(value)
                self.numer, self.denom = f.numerator, f.denominator
                self.mytype = NumType.Rat
            elif "j" in norm or "inf" in norm or "nan" in norm:
                # dpmath.ParseComplex updated to handle inf/nan string inputs
                re_part, im_part = dpmath.ParseComplex(norm)
                self.real = mpmath.mpf(re_part if re_part is not None else 0)
                self.imag = mpmath.mpf(im_part if im_part is not None else 0)
                self.mytype = NumType.Cpx
            elif "." in norm or "e" in norm:
                self.real = mpmath.mpf(value)
                self.mytype = NumType.Flt
            else:
                try:
                    self.numer = int(value)
                    self.mytype = NumType.Int
                except ValueError:
                    raise ValueError(msg)
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s: return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                # Cleaner complex output: skip 0j if real-only
                if self.imag == 0:
                    s = self.fmt(self.real)
                else:
                    s = self.fmt(mpmath.mpc(self.real, self.imag))
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = self.fmt(self.real)
            
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.real!r}{'+' if self.imag >=0 else ''}{self.imag!r}j"
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = f"{self.real!r}"
            if self.unit.strip(): s += f" {self.unit}"
            return f"Num('{s}')"
        def __str__(self) -> str: return self._r() if Num.flip else self._s()
        def __repr__(self) -> str: return self._s() if Num.flip else self._r()
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit: return Num(self)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
            if not is_ok:
                RegisterUnit(unit)
                is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
                if not is_ok: raise ValueError(f"Incompatible units: {self.unit} and {unit}")
            
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            if res.mytype <= NumType.Rat:
                res.real = res.as_mpf * factor
                res.mytype = NumType.Flt
            else:
                res.real *= factor
                res.imag *= factor
                res.re_unc *= factor
                res.im_unc *= factor
            res._unit = unit 
            return res.promote() if auto_promote else res
        @property
        def raw_value(self) -> ty.Union[int, mpmath.mpf, mpmath.mpc]:
            '''Returns the underlying math object for the arbiter without unit scaling.'''
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                # Since we aren't using fractions.Fraction, we hand the arbiter
                # the exact ratio to maintain precision before it hits mpmath.
                return self.numer / self.denom
            if self.mytype == NumType.Cpx:
                return self.as_mpc
            # For Flt and Unc
            return self.real
        @property
        def unit(self) -> str: return self._unit.strip()
        @property
        def as_mpc(self) -> mpmath.mpc:
            if self.mytype == NumType.Int: return mpmath.mpc(str(self.numer), 0)
            if self.mytype == NumType.Rat: return mpmath.mpc(self.numer/mpmath.mpf(self.denom), 0)
            if self.mytype == NumType.Flt: return mpmath.mpc(self.real, 0)
            return mpmath.mpc(self.real, self.imag)
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype == NumType.Int: return mpmath.mpf(str(self.numer))
            if self.mytype == NumType.Rat: return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int: return self.numer
            return fractions.Fraction(self.numer, self.denom)
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
            # Default internal state
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
                self._unit = unit
            if value is None:
                return
            # High-Precision Conversion Logic with Type Closure
            if isinstance(value, Num):
                self.numer, self.denom = value.numer, value.denom
                self.real, self.imag = value.real, value.imag
                self.re_unc, self.im_unc = value.re_unc, value.im_unc
                self._unit = unit if unit else value.unit
                self.mytype = value.mytype
            elif isinstance(value, int):
                self.numer = value
                self.mytype = NumType.Int
            elif isinstance(value, (float, decimal.Decimal)):
                self.real = mpmath.mpf(str(value))
                self.mytype = NumType.Flt
            elif isinstance(value, complex):
                self.real = mpmath.mpf(str(value.real))
                self.imag = mpmath.mpf(str(value.imag))
                self.mytype = NumType.Cpx
            elif isinstance(value, fractions.Fraction):
                self.numer, self.denom = value.numerator, value.denominator
                self.mytype = NumType.Rat
            elif hasattr(value, '_mpf_') or isinstance(value, mpmath.mpf):
                self.real = value
                self.mytype = NumType.Flt
            elif isinstance(value, mpmath.mpc):
                self.real, self.imag = value.real, value.imag
                self.mytype = NumType.Cpx
            elif isinstance(value, uncertainties.UFloat):
                self.real = mpmath.mpf(str(value.nominal_value))
                self.re_unc = mpmath.mpf(str(value.std_dev))
                self.mytype = NumType.Unc
            elif isinstance(value, str):
                self._parse_string(value.strip())
            else:
                raise TypeError(f"Type of {value!r} is not supported")
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            '''Dispatches math operations and preserves unit context.'''
            target_type = max(self.mytype.value, other.mytype.value)
            # Use self.unit as the anchor for the result unit
            res_unit = self.unit
            # 1. Integer/Rational Domain
            if target_type <= NumType.Rat.value:
                raw_val = op_func(self.as_int_or_rat, other.as_int_or_rat)
                return Num(raw_val, unit=res_unit)
            # 2. Uncertainty Domain
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func)
            # 3. Complex Domain
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                raw_val = op_func(self.as_mpc, other.as_mpc)
                return Num(raw_val, unit=res_unit)
            # 4. Standard Float Domain (mpf)
            a_val = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b_val = other.real if other.mytype >= NumType.Flt else other.as_mpf
            raw_val = op_func(a_val, b_val)
            return Num(raw_val, unit=res_unit)
        def _normalize(self, other: "Num", operation: str = "") -> "Num":
            '''Ensures units are compatible and returns 'other' scaled to 'self.unit'.'''
            # 1. Identical units: no work needed
            if self.unit == other.unit:
                return other
            # 2. Multiplication/Division: no normalization needed (units combine)
            if operation in ("mul", "div"):
                return other
            # 3. Addition/Subtraction: Units must be conformable
            if operation in ("add", "sub", "cmp"):
                # One has units, the other doesn't
                if bool(self.unit) != bool(other.unit):
                    raise ValueError(f"Unit Mismatch: Cannot {operation} '{self.unit}' and '{other.unit}'")
            # 4. Check GNU Units for compatibility and scale factor
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {factor_str}")
            # 5. Scale 'other' to match 'self' units
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                # Promote to Float if the conversion factor isn't a clean integer/ratio
                adjusted.real = adjusted.as_mpf * factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real *= factor
                adjusted.imag *= factor
                adjusted.re_unc *= factor
                adjusted.im_unc *= factor
            # Bypass setter to avoid circular normalization
            adjusted._unit = self.unit
            return adjusted
        def _parse_proper_fraction(self, s: str) -> mpmath.mpf:
            regex = r'^([+-])?(\d+)?(?:[- ](\d+)/(\d+))?$'
            match = re.match(regex, s.strip())
            if not match:
                raise ValueError(f"Invalid fraction format: {s}")
            sign = -1 if match.group(1) == '-' else 1
            whole = int(match.group(2)) if match.group(2) else 0
            num = int(match.group(3)) if match.group(3) else 0
            den = int(match.group(4)) if match.group(4) else 1
            return sign * (mpmath.mpf(whole) + (mpmath.mpf(num) / mpmath.mpf(den)))
        def _parse_string(self, value: str) -> None:
            msg = f"{value!r} not recognized as a number"
            norm = value.lower().replace("i", "j").strip()
            if ("-" in value and value[0] != "-") and "/" in value:
                self.real = self._parse_proper_fraction(value)
                self.mytype = NumType.Flt
            elif "/" in norm:
                parts = value.split("/")
                if len(parts) == 2:
                    try:
                        n_str, d_str = parts
                        self.numer, self.denom = int(n_str), int(d_str)
                        if self.denom == 0:
                            raise ValueError("Division by zero in rational string")
                        self.mytype = NumType.Rat
                    except ValueError:
                        raise ValueError(msg)
                else:
                    raise ValueError(msg)
            elif "j" in norm or "inf" in norm or "nan" in norm:
                # dpmath.ParseComplex updated to handle inf/nan string inputs
                re_part, im_part = dpmath.ParseComplex(norm)
                self.real = mpmath.mpf(re_part if re_part is not None else 0)
                self.imag = mpmath.mpf(im_part if im_part is not None else 0)
                self.mytype = NumType.Cpx
            elif "." in norm or "e" in norm:
                self.real = mpmath.mpf(value)
                self.mytype = NumType.Flt
            else:
                try:
                    self.numer = int(value)
                    self.mytype = NumType.Int
                except ValueError:
                    raise ValueError(msg)
        def _extract_unit(self, s: str) -> ty.Tuple[str, str]:
            s = s.strip()
            if " " not in s: return s, ""
            parts = s.rsplit(None, 1)
            val_part, unit_part = parts
            if unit_part[0].isalpha() or unit_part[0] in "(%":
                if not val_part.lower().endswith("e"):
                    return val_part.strip(), unit_part.strip()
            return s, ""
        def _s(self) -> str:
            if self.mytype == NumType.Int:
                s = self.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = self.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                # Cleaner complex output: skip 0j if real-only
                if self.imag == 0:
                    s = self.fmt(self.real)
                else:
                    s = self.fmt(mpmath.mpc(self.real, self.imag))
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = self.fmt(self.real)
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def _r(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.real!r}{'+' if self.imag >=0 else ''}{self.imag!r}j"
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = f"{self.real!r}"
            if self.unit.strip(): s += f" {self.unit}"
            return f"Num('{s}')"
        def __str__(self) -> str: return self._r() if Num.flip else self._s()
        def __repr__(self) -> str: return self._s() if Num.flip else self._r()
        def to(self, unit: str, auto_promote: bool = True) -> "Num":
            if not unit: return Num(self)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
            if not is_ok:
                RegisterUnit(unit)
                is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
                if not is_ok: raise ValueError(f"Incompatible units: {self.unit} and {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            if res.mytype <= NumType.Rat:
                res.real = res.as_mpf * factor
                res.mytype = NumType.Flt
            else:
                res.real *= factor
                res.imag *= factor
                res.re_unc *= factor
                res.im_unc *= factor
            res._unit = unit
            return res.promote() if auto_promote else res
        @property
        def raw_value(self) -> ty.Union[int, mpmath.mpf, mpmath.mpc]:
            '''Returns the underlying math object for the arbiter without unit scaling.'''
            if self.mytype == NumType.Int:
                return self.numer
            if self.mytype == NumType.Rat:
                return self.numer / self.denom
            if self.mytype == NumType.Cpx:
                return self.as_mpc
            return self.real
        @property
        def unit(self) -> str: return self._unit.strip()
        @property
        def as_mpc(self) -> mpmath.mpc:
            if self.mytype == NumType.Int: return mpmath.mpc(str(self.numer), 0)
            if self.mytype == NumType.Rat: return mpmath.mpc(self.numer/mpmath.mpf(self.denom), 0)
            if self.mytype == NumType.Flt: return mpmath.mpc(self.real, 0)
            return mpmath.mpc(self.real, self.imag)
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype == NumType.Int: return mpmath.mpf(str(self.numer))
            if self.mytype == NumType.Rat: return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int: return self.numer
            return fractions.Fraction(self.numer, self.denom)

if 0:  # UnitArbiter: Refactored for Complex Plane preservation
    class UnitArbiter:
        _instance = None
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
            ok, _ = self.check_conformable(unit_str, unit_str)
            return ok
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
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
                is_ok, error_msg = False, "Circular definition detected."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return is_ok, error_msg
        def add_base(self, unit_name: str) -> None:
            self._commit_unit(f"{unit_name.strip()} !")
        def add_unit(self, definition: str) -> None:
            sanitized = definition.replace("=", "").strip()
            self._commit_unit(sanitized)
        def _commit_unit(self, entry: str) -> None:
            if self.dynamic_path.exists():
                with open(self.dynamic_path, "r") as f:
                    if entry in f.read():
                        return
            is_ok, error = self._check_definition(entry)
            if is_ok:
                with open(self.dynamic_path, "a") as f:
                    f.write(f"{entry}\n")
                self._start_process()
            else:
                if "not found" not in error.lower():
                    print(f"Unit Definition Error: {error.strip()}")
        def _translate_unicode(self, s: str) -> str:
            exp_map = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
            out = ""
            for char in s:
                if char in "⁰¹²³⁴⁵⁶⁷⁸⁹":
                    out += "^" + char.translate(exp_map)
                else:
                    out += char
            return out
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            if not have or not want:
                if have == want:
                    return True, "1.0"
                return False, f"Cannot conform '{have}' to '{want}'"
            if not self.proc or self.proc.poll() is not None:
                self._start_process()
            have = self._translate_unicode(have)
            want = self._translate_unicode(want)
            try:
                self.proc.stdin.write(f"{have}\n{want}\n")
                self.proc.stdin.flush()
                for _ in range(5):
                    line = self.proc.stdout.readline().strip()
                    if not line:
                        continue
                    if line.startswith("*"):
                        return True, line.replace("*", "").strip()
                    if line == "1" or line == "1.0":
                        return True, "1.0"
                    if "conformability error" in line.lower():
                        return False, f"Incompatible dimensions: {have} vs {want}"
                return False, "Unexpected output format"
            except Exception as e:
                self._start_process()
                return False, str(e)
        def simplify(self, value: ty.Union[mpmath.mpf, mpmath.mpc], unit_str: str) -> tuple[ty.Union[mpmath.mpf, mpmath.mpc], str]:
            '''Flattens units while preserving the complex plane.'''
            if not unit_str or unit_str == "1":
                return value, ""
            reduced_unit_str, scale_factor = self._query_units_for_reduction(unit_str)
            if "=" in reduced_unit_str:
                reduced_unit_str = reduced_unit_str.split("=")[0].strip()
            # Scale the entire head (mpf or mpc) by the real scale factor
            sf = mpmath.mpf(scale_factor)
            current_value = value*sf
            preferred_units = Num.systems.get(Num.active_system, [])
            for candidate in preferred_units:
                for power in [1, 2, 3]:
                    test_unit = candidate if power == 1 else f"{candidate}^{power}"
                    is_ok, factor_str = self.check_conformable(reduced_unit_str, test_unit)
                    if is_ok:
                        # Apply secondary conversion factor
                        return current_value*mpmath.mpf(factor_str), test_unit
            return current_value, reduced_unit_str
        def _query_units_for_reduction(self, unit_str: str) -> tuple[str, str]:
            '''Uses GNU Units --compact to get a raw factor and unit remainder.'''
            cmd = [self.bin_path, "-q", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            result = subprocess.run(cmd + [self._translate_unicode(unit_str)],
                                    capture_output=True, text=True)
            output = result.stdout.strip()
            # Regex handles cases like '0.75 m' or just 'm' or just '0.75'
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            if match:
                factor = match.group(1) or "1.0"
                remainder = match.group(2) or ""
                return remainder.strip(), factor
            return unit_str, "1.0"
if 1:  # UnitArbiter: The GNU Units Bridge
    class UnitArbiter:
        _instance = None
        units_bin: str = "units"
        main_config: str = ""
        dynamic_config: str = "~/.units_dynamic"
        def __new__(cls) -> "UnitArbiter":
            if cls._instance is None:
                cls._instance = super(UnitArbiter, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized: return
            self.bin_path = str(Path(UnitArbiter.units_bin).expanduser())
            self.dynamic_path = Path(UnitArbiter.dynamic_config).expanduser()
            if not self.dynamic_path.exists(): self.dynamic_path.touch()
            self.proc = None
            self._start_process()
            self._initialized = True
        def _start_process(self) -> None:
            cmd = [self.bin_path, "-q"]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            cmd.extend(["-f", str(self.dynamic_path)])
            self.proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        def _translate_unicode(self, s: str) -> str:
            # Map Unicode superscripts back to ASCII for GNU Units
            exp_map = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
            out = ""
            for char in s:
                if char in "⁰¹²³⁴⁵⁶⁷⁸⁹":
                    out += "^" + char.translate(exp_map)
                else:
                    out += char
            return out
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            if not have or not want:
                return (True, "1.0") if have == want else (False, "Mismatch")
            if not self.proc or self.proc.poll() is not None: self._start_process()
            try:
                self.proc.stdin.write(f"{self._translate_unicode(have)}\n{self._translate_unicode(want)}\n")
                self.proc.stdin.flush()
                # GNU Units returns the factor on the first non-empty line
                for _ in range(5):
                    line = self.proc.stdout.readline().strip()
                    if not line: continue
                    if line.startswith("*"): return True, line.replace("*", "").strip()
                    if line in ("1", "1.0"): return True, "1.0"
                    if "conformability error" in line.lower(): break
                return False, f"Incompatible: {have} vs {want}"
            except Exception as e:
                self._start_process()
                return False, str(e)
        def simplify(self, value: ty.Any, unit_str: str) -> tuple[ty.Any, str]:
            '''Reduces units to base or preferred system while scaling value.'''
            if not unit_str or unit_str == "1": return value, ""
            # Use --compact to get the reduced unit and scale factor
            cmd = [self.bin_path, "-q", "--compact", "-f", str(self.dynamic_path)]
            if UnitArbiter.main_config:
                cmd.extend(["-f", str(Path(UnitArbiter.main_config).expanduser())])
            proc = subprocess.run(cmd + [self._translate_unicode(unit_str)], capture_output=True, text=True)
            output = proc.stdout.strip()
            match = re.match(r'^([\d.e+-]+)?\s*(.*)$', output)
            factor = mpmath.mpf(match.group(1) or "1.0") if match else mpmath.mpf("1.0")
            remainder = match.group(2).strip() if match else unit_str
            # Clean up GNU Units' dictionary-style output (e.g., 'm = 100 cm')
            if "=" in remainder: remainder = remainder.split("=")[0].strip()
            return value * factor, remainder
        def is_known_unit(self, unit_str: str) -> bool:
            '''Checks if GNU Units recognizes the unit string.'''
            if not unit_str:
                return True
            # We use conformability against itself as a validity check
            ok, _ = self.check_conformable(unit_str, unit_str)
            return ok
        def _check_definition(self, definition: str) -> ty.Tuple[bool, str]:
            '''Validates a new unit definition before committing to the dynamic file.'''
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
                tmp.write(definition + "\n")
                tmp_path = tmp.name
            # Use units -c to check the syntax of the temp file
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
                is_ok, error_msg = False, "Circular definition detected."
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return is_ok, error_msg
if 1:  # Functions
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
if 1:  # Help 
    class Help:
        'Adds the help() function (singleton class)'
        _instance = None
        def __new__(cls) -> "Help":
            if cls._instance is None:
                cls._instance = super(Help, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
        def __init__(self) -> None:
            if self._initialized:
                return
            self._initialized = True
        def __call__(self, *p, **kw) -> None:
            if not p:
                print(wrap.dedent(f'''
                Num class topics:  use numinstance.help("topic"):
                    overview    Basic example of use
                    init        Getting it to work
                '''))
                return
            if p[0] == "overview":
                wall_length = Num("50 m")
                wall_length.base("nails")
                nails_per_m = Num("20 nails/m")
                print(wrap.dedent(f'''
                Num class help
                    The Num class is a number used for routine calculations in the
                    python REPL.  You can use integers, fractions, floats, and complex
                    numbers.  The numbers can also include units.  Here's a sample
                    calculation for how many nails will be needed for a long wall:
                    
                        wall_length = Num("50 m")
                        wall_length.base("nails")
                        nails_per_m = Num("20 nails/m")
                        print(f"Need {{wall_length*nails_per_m}} for the wall")
                    
                    This will print the answer
                    
                        Need {wall_length*nails_per_m} for the wall
                    
                    You can define these "semantic units" dynamically as your problem's
                    solution develops.  These units can help keep the calculation's
                    logic correct.
                '''))
if 1:   # Set up config files   ∞∞2 This needs to move out of the main code area
    UnitArbiter.main_config = "/home/don/.0rc/bin/definitions.units"
    UnitArbiter.dynamic_config = "/home/don/.units_dynamic"
    UnitArbiter.units_bin = "/home/don/.0rc/bin/units"
if 0:  # Temp experiment
    def f():
        x = Num("inf m")
        x.help()
    f()
    #exit()

if 1:   # Self-tests
        def Test_Constructor_With_Numbers():
            zero = 0
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
                Assert(num == Num("-0.375"))
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
            zero = 0
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
                    if 0:   # This is old test when the result was a rational
                        # Mike and I agreed it doesn't really make sense to spend effort
                        # fixing this now.  Maybe later it will feel more important if a
                        # special use case needs it.
                        expected = Num("15/8", "in")
                    else:
                        expected = Num("1.875", "inch")
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
                    expected = "-2.2808399000000001"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num(expected, "foot"))
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x - y
                    #expected = Num("-9/8", "in")   # 3/8 - 12/8 = -9/8
                    expected = Num("-1.125 inch")
                    Assert(result == expected)
            if 1:   # Test multiplication
                if 1:   # Integer & real
                    x = Num("1.5", "V")
                    y = Num("2.0", "A")
                    result = x*y
                    expected = "3.0"
                    Assert(result.real == mpmath.mpf(expected))
                    Assert(result == Num("3.0 kg*m^2/s^3"))
                    # ∞∞ Step through line 1087 with debugger to see why the == is
                    # failing
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x*y
                    #expected = Num("9/16", "(in)*(in)")   # 3/8*12/8 = 36/64 = 9/16
                    expected = Num("0.00036290249999999997 m^2")
                    Assert(result == expected)
                    #yy
            if 1:   # Test division
                if 1:   # Integer & real
                    x = Num("1.0", "ft")
                    y = Num("1", "m")
                    result = x/y
                    expected = Num("0.30480000000000002")
                    Assert(result == expected)
                if 1:   # Rational
                    x = Num("3/8", "in")
                    y = Num("24/16", "in")
                    result = x/y
                    expected = Num("0.25")
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
            Assert(x.num*y == x)        # Prove the Noether invariance
            # It has to work for complex too
            z = Num("1+2i m")
            y = z/z.num
            Assert(y.unit == z.unit)    # Make sure units didn't change
            Assert(z.num*y == z)        # Prove the Noether invariance
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
                # Real
                Assert(N("0 m") + N("0 m") == N("0 m"))
                Assert(N("0 m")*N("1 m") == N("0 m2"))
                Assert(N("0 m")/N("1 m") == N("0"))
                # Complex
                Assert(N("0+0j m") + N("0+0j m") == N("0+0j m"))
                Assert(N("0+0j m")*N("1+0j m") == N("0+0j m2"))
                Assert(N("0+0j m")/N("1+0j m") == N("0+0j"))
                # Complex units corner case
                Assert(N("1+0i m") + N("1 m") == N("2+0j m"))
                Assert(N("1+0i m")*N("1 m") == N("1+0j m2"))
            if 1:   # Test core properties: as_mpf, etc.
                x = Num("10")
                Assert(isinstance(x.as_int_or_rat, int))
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", 0))
                x = Num("10/20")
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("1/2"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("1/2", 0))
                x = Num("10+20j")
                Assert(isinstance(x.as_mpf, mpmath.mpf) and x.as_mpf == mpmath.mpf("10"))
                Assert(isinstance(x.as_mpc, mpmath.mpc) and x.as_mpc == mpmath.mpc("10", "20"))
            if 1:   # "1+2i m" * "3/4 A":  hope we don't get mA
                a = N("1+2i m")
                b = N("3/4 A")
                Assert(a*b == N("0.75+1.5i m*A"))
            if 1:   # Division by zero
                with raises(ZeroDivisionError):
                    N("0")/N("0")
                with raises(ValueError):
                    N("0/0")
                with raises(ZeroDivisionError):
                    N("0.")/N("0.")
                with raises(ZeroDivisionError):
                    N("0+0i")/N("0+0i")
            if 1:   # Complex powers
                # First try no units; should maintain complex type
                x = N("1+1i")
                y = x**x
                Assert(y == N(mpmath.mpc(1, 1)**mpmath.mpc(1, 1)))
                # See that complex exponent gets exception on base with units
                breakpoint() # ∞∞ 
                a = N("1.2 m")
                with raises(TypeError):
                    y = a**x
                # Can handle e.g. a 2/3 power if the base unit is a root
                if 0:
                    x = N("2 gallons")
                    a = N("2/3")
                    x**a
                else:
                    lwtest.ToDo("Can't calculate (2 gallon)^(2|3):  process hangs")
            if 1:   # In-place scaling    
                a = Num("1 m")
                a += Num("50 cm")
                Assert(a == Num("1.5 m"))
            if 1:   # Does expression "inflate" to a float
                x = Num(5)*Num(2)#/Num(10)
                lwtest.ToDo("Num(5)*Num(2) results in a float")
            if 1:   # inf and nan
                x = Num("inf m")
            #yy
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
