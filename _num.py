from __future__ import annotations
'''
Tue 7 Apr 2026 Tasks

- Get multiplication to work:  
    - Test case:
            x = Num("1", "ft")  # Is 0.3048 m
            y = Num("1", "m")   # Is 1 m
            x - y
            Should get Num("mpf('-0.69520000000000004')", "ft")
            but we're getting the negative of the correct answer, so there's a flip
            somewhere.
    - Num("2", "V")*Num("3.5", "A") -> Num("7", "(V)*(A)")
- Add nbs to string between number and unit
- Consider updating RoundOff to use mpf
- Need infection model for REPL
    - You can start off using int, float, complex, but as soon as one of these encounter
      a Num, a Num is always returned.  But the user has to type Num(x) to start the
      ball rolling.  The clue in the REPL is that the Num objects will always be
      colorized, but the python built-in types won't.  Thus, the REPL will behave like
      you're used to unless you deliberately use Num.
- Should Num have a .on attribute for colorizing?
- GNU units
    - It appears it will accept arbitrary fractions in the "a|b" form

'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import decimal
        import enum
        import fcntl
        import fractions
        import getopt
        import operator
        import os
        import pathlib
        import re
        import string
        import subprocess
        import sys
        import threading
        import time
        import typing as ty
    if 1:   # Custom imports
        import columnize
        import dpstr
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
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        #
        Columnize = columnize.Columnize
        dedent = wrap.dedent
    if 1:   # Global variables
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
if 0:   # Old Num class
    '''Represent a general number useful for routine calculations
        
            Warning:  The internal representation uses mpmath, so it's your responsibility
            as the user to ensure the mpmath context has sufficient resolution for your
            problems.
            
            The vision for this number class is for a "simple" view of the numerical
            universe in a python REPL (read-eval-print loop).  If you studied math as 
            e.g. an engineer/scientist in college, then you learned about some different
            number fields:  integers, rationals, reals, and complex numbers, the bedrock of
            practical math.  When doing calculations, we smoothly move between these fields
            as needed, converting things almost subconsciously, but it's harder for the
            computer stuff because these things (numbers) are usually types that often can't 
            unconsciously interact.  My vision for this Num class was to see if the
            following number types could be put into a logical single container:
                
                These "blackboard" symbols are used to denote the mathematical sets:
                    ℕ   Natural numbers:  the integers 1, 2, ...
                    ℤ   Positive and negative integers and zero
                    ℝ   Real numbers
                    ℂ   Complex numbers:  a pair of real numbers
            
                python's int, a representation of ℤ
                python's fractions.Fraction, a representation of ℚ
                python's float ℝ
                python's decimal.Decimal, another representation of ℝ
                python's complex ℂ
                mpmath's mpf, another representation of ℝ
                mpmath's mpc, another representation of ℂ
            
            Two other "types" needed to be addressed:
            
                - Because real-world practical problems include uncertainty, we need
                  some way to capture the notion of physical uncertainty in the numbers.
                  Python's uncertainties package is a good tool, but it lacks the
                  machinery to handle uncertainty in complex numbers, something I wanted
                  this Num class to handle.  If your first reaction is "that's not
                  needed", consider the output of an LCR meter: in general, you're given
                  back a complex impedance Z = ESR + X*i and the two real numbers can
                  have different (though perhaps correlated) uncertainty.  Though there
                  are other "number" types (vectors, matrices, quaternions, etc.) that
                  pop up in routine calculations, the Num type handles most of the
                  practical work.
            
                - Numbers based on physical measurement include units, which form their
                  own dimensional algebra and complicate things, as two real numbers x =
                  "3.4 m/s" and y = "6.7 A" are different types and have more
                  complicated arithmetic properties than "bare" numbers.  For example,
                  you cannot add x and y, but you're allowed to multiply them.
            
            Here's a very important practical notion of "logical" units.  We usually
            think of units as e.g. the familiar SI units.  However, almost all practical
            calculations involve some types of units.  For example, if you're measuring
            out pet food mass to feed some dogs and cats, you'd probably want the
            calculation to use the "units" kg_cat_food and kg_dog_food, assuming the
            dogs and cats get fed different foods.  This "unit orthogonality" helps
            keeps the animals fed properly, avoiding a mistake of mixing the foods,
            which might show up in a calculation as having units of
            kg_cat_food*kg_dog_food or a sum of 'kg_cat_food + kg_dog_food'.  The
            example isn't trivial -- if you're not convinced, look up the
            non-chump-change units mistake of the Mars Climate Orbiter, a loss of about
            half a billion 2026 dollars.  It's a shame the programming tools we have
            don't natively support both physical and logical units.  One of my goals in
            this Num class was providing a tool to do just this, because when the units
            in some arithmetical calculation aren't consistent, it's likely an error has
            been made.  Every scientist or engineer has learned to use such errors as
            red flags.
        
            Note for constructor
                # Note the user can supply a new unit string, changing the dimension
                # of value.  This is a deliberately allowed pattern:  the user needs
                # the number, but wants to change the unit "vector".
    '''

    class Num:
        '''Represent a general number useful for routine calculations'''
        # Pick color based on number type
        type_color = {  # Match number types in dpdb.py for debugger
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        def __init__(self, value: ty.Optional[NumericalTypes] = None, unit: str = "") -> None:
            if 1:  # Default internal state representation
                self.numer: int = 0
                self.denom: int = 1
                self.real: mpmath.mpf = mpmath.mpf("0")
                self.imag: mpmath.mpf = mpmath.mpf("0")
                self.re_unc: mpmath.mpf = mpmath.mpf("0")
                self.im_unc: mpmath.mpf = mpmath.mpf("0")
                self.correl: mpmath.mpf = mpmath.mpf("0")
                self._unit = ""
                self.unit = unit  # Uses setter for stripping
                self.mytype: NumType = NumType.Int
                if value is None:
                    return
            if 1:  # High-Precision Conversion Logic
                if isinstance(value, Num):  # Copy constructor
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
                elif isinstance(value, mpmath.mpf):
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
                    msg = f"{value!r} not recognized as a number"
                    normalized = set(value.lower().replace("i", "j").strip())
                    if "/" in normalized:
                        try:
                            self.numer, self.denom = [int(i) for i in value.split("/")]
                            self.mytype = NumType.Rat
                        except Exception as e: raise ValueError(msg) from e
                    elif "j" in normalized:
                        re, im = dpmath.ParseComplex(value)
                        self.real = mpmath.mpf(re)
                        self.imag = mpmath.mpf(im)
                        self.mytype = NumType.Cpx
                    elif "." in normalized or "e" in normalized:
                        try:
                            self.real = mpmath.mpf(value)
                            self.mytype = NumType.Flt
                        except Exception as e: raise ValueError(msg) from e
                    else:
                        try:
                            self.numer = int(value)
                            self.mytype = NumType.Int
                        except Exception as e: raise ValueError(msg) from e
                else:
                    raise TypeError(f"Type of {value!r} is not supported")
        def _binary_op(self, other: "Num", op_func: ty.Callable) -> "Num":
            target_type = max(self.mytype.value, other.mytype.value)
            if target_type <= NumType.Rat.value:
                return Num(op_func(self.as_int_or_rat, other.as_int_or_rat))
            if target_type == NumType.Unc.value:
                return self._do_uncertainty_math(other, op_func) # type: ignore
            # Real/Complex Promotion
            a = self.real if self.mytype >= NumType.Flt else self.as_mpf
            b = other.real if other.mytype >= NumType.Flt else other.as_mpf
            # If either is complex, use mpc to ensure mpmath handles it correctly
            if self.mytype == NumType.Cpx or other.mytype == NumType.Cpx:
                ac = mpmath.mpc(self.real, self.imag)
                bc = mpmath.mpc(other.real, other.imag)
                return Num(op_func(ac, bc))
            return Num(op_func(a, b))
        def _check_units(self, other: "Num") -> mpmath.mpf:
            '''Returns the multiplier to convert other.unit -> self.unit.'''
            if (not self.unit and not other.unit) or (self.unit == other.unit):
                return mpmath.mpf("1")
            arbiter = UnitArbiter()
            # We need: magnitude in other.unit * factor = magnitude in self.unit
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
            return mpmath.mpf(factor_str)
        def _normalize(self, other: "Num") -> "Num":
            '''Returns a copy of other scaled to self.unit.'''
            factor = self._check_units(other)
            if factor == 1:
                return Num(other)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf * factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real = adjusted.real * factor
                adjusted.imag = adjusted.imag * factor
            adjusted.unit = self.unit
            return adjusted
        # Arithmetic Methods
        def __add__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adj = self._normalize(other_num)
            res = self._binary_op(adj, operator.add)
            res.unit = self.unit
            return res
        def __sub__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adj = self._normalize(other_num)
            res = self._binary_op(adj, operator.sub)
            res.unit = self.unit
            return res
        def __mul__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            res = self._binary_op(other_num, operator.mul)
            if not self.unit and not other_num.unit: res.unit = ""
            elif self.unit and not other_num.unit: res.unit = self.unit
            elif not self.unit and other_num.unit: res.unit = other_num.unit
            else: res.unit = f"({self.unit})*({other_num.unit})"
            return res
        def __rmul__(self, other: ty.Any) -> "Num":
            return self.__mul__(other)
        def __truediv__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            if other_num.as_mpf == 0: raise ZeroDivisionError("Tractor at 0 divisor.")
            res = self._binary_op(other_num, operator.truediv)
            if not self.unit and not other_num.unit: res.unit = ""
            elif self.unit and not other_num.unit: res.unit = self.unit
            elif not self.unit and other_num.unit: res.unit = f"1/({other_num.unit})"
            else: res.unit = f"({self.unit})/({other_num.unit})"
            return res
        def __rtruediv__(self, other: ty.Any) -> "Num":
            return Num(other) / self
        def __eq__(self, other: ty.Any) -> bool:
            other_num = Num(other)
            if self.unit != other_num.unit: return False
            target_type = max(self.mytype.value, other_num.mytype.value)
            if target_type <= NumType.Rat.value:
                return self.as_int_or_rat == other_num.as_int_or_rat
            return bool(self.as_mpf == other_num.as_mpf)
        if 1:   # String interpolation
            def __str__(self) -> str:
                if self.mytype == NumType.Int: s = fmt.fmt(self.numer)
                elif self.mytype == NumType.Rat: s = fmt.fmt(fractions.Fraction(self.numer, self.denom))
                elif self.mytype == NumType.Cpx: s = fmt.fmt(mpmath.mpc(self.real, self.imag))
                elif self.mytype == NumType.Unc: s = f"{self.real} ± {self.re_unc}"
                else: s = fmt.fmt(self.real)
                unit_str = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
                color = Num.type_color.get(self.mytype, t.wht)
                return f"{color}{s}{t.n}{unit_str}"
            def __repr__(self) -> str:
                if self.mytype == NumType.Int: s = str(self.numer)
                elif self.mytype == NumType.Rat: s = f"{self.numer}/{self.denom}"
                elif self.mytype == NumType.Cpx: s = f"{self.real!r}+{self.imag!r}j"
                elif self.mytype == NumType.Unc: s = f"{self.real} ± {self.re_unc}"
                else: s = f"{self.real!r}"
                return f'Num("{s}", "{self.unit}")'
        if 1:   # Properties
            @property
            def unit(self) -> str:
                return self._unit.strip()
            @unit.setter
            def unit(self, value: str) -> None:
                self._unit = value.strip() if value else ""
            @property
            def as_mpf(self) -> mpmath.mpf:
                if self.mytype == NumType.Int: return mpmath.mpf(str(self.numer))
                if self.mytype == NumType.Rat: return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
                return self.real
            @property
            def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
                if self.mytype == NumType.Int: return self.numer
                return fractions.Fraction(self.numer, self.denom)
else:  # Section: Core Num Class and Unit Registration
    class Num:
        '''Represent a general number useful for routine calculations'''
        type_color = {
            NumType.Int: t("mag", "gry1"),
            NumType.Rat: t("brn", "gry1"),
            NumType.Flt: t("ygr", "gry1"),
            NumType.Cpx: t("sky", "gry1"),
            NumType.Unc: t("pur", "gry1"),
        }
        def __init__(self, value: ty.Optional[ty.Any] = None, unit: str = "") -> None:
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
                elif isinstance(value, mpmath.mpf):
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
        def _parse_string(self, value: str) -> None:
            msg = f"{value!r} not recognized as a number"
            normalized = set(value.lower().replace("i", "j").strip())
            if "/" in normalized:
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
        def _normalize(self, other: "Num") -> "Num":
            '''Returns a copy of other scaled to self.unit.'''
            if (not self.unit and not other.unit) or (self.unit == other.unit):
                return Num(other)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(other.unit, self.unit)
            if not is_ok:
                raise ValueError(f"Unit Mismatch: {self.unit} vs {other.unit}")
            factor = mpmath.mpf(factor_str)
            adjusted = Num(other)
            if adjusted.mytype <= NumType.Rat:
                adjusted.real = adjusted.as_mpf*factor
                adjusted.mytype = NumType.Flt
            else:
                adjusted.real = adjusted.real*factor
                adjusted.imag = adjusted.imag*factor
            adjusted.unit = self.unit
            return adjusted
        def __add__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            result = self._binary_op(adjusted, operator.add)
            result.unit = self.unit
            return result
        def __sub__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            adjusted = self._normalize(other_num)
            result = self._binary_op(adjusted, operator.sub)
            result.unit = self.unit
            return result
        def __mul__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            result = self._binary_op(other_num, operator.mul)
            if not self.unit and not other_num.unit:
                result.unit = ""
            elif self.unit and not other_num.unit:
                result.unit = self.unit
            elif not self.unit and other_num.unit:
                result.unit = other_num.unit
            else:
                result.unit = f"({self.unit})*({other_num.unit})"
            return result
        def __rmul__(self, other: ty.Any) -> "Num":
            return self.__mul__(other)
        def __truediv__(self, other: ty.Any) -> "Num":
            other_num = Num(other)
            if other_num.as_mpf == 0:
                raise ZeroDivisionError("Tractor at 0 divisor.")
            result = self._binary_op(other_num, operator.truediv)
            if not self.unit and not other_num.unit:
                result.unit = ""
            elif self.unit and not other_num.unit:
                result.unit = self.unit
            elif not self.unit and other_num.unit:
                result.unit = f"1/({other_num.unit})"
            else:
                result.unit = f"({self.unit})/({other_num.unit})"
            return result
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
        def __str__(self) -> str:
            if self.mytype == NumType.Int:
                s = fmt.fmt(self.numer)
            elif self.mytype == NumType.Rat:
                s = fmt.fmt(fractions.Fraction(self.numer, self.denom))
            elif self.mytype == NumType.Cpx:
                s = fmt.fmt(mpmath.mpc(self.real, self.imag))
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = fmt.fmt(self.real)
            unit_string = f" {t.whtl}{self.unit}{t.n}" if self.unit else ""
            color = Num.type_color.get(self.mytype, t.wht)
            return f"{color}{s}{t.n}{unit_string}"
        def __repr__(self) -> str:
            if self.mytype == NumType.Int:
                s = str(self.numer)
            elif self.mytype == NumType.Rat:
                s = f"{self.numer}/{self.denom}"
            elif self.mytype == NumType.Cpx:
                s = f"{self.real!r}+{self.imag!r}j"
            elif self.mytype == NumType.Unc:
                s = f"{self.real} +/- {self.re_unc}"
            else:
                s = f"{self.real!r}"
            return f'Num("{s}", "{self.unit}")'
        @property
        def unit(self) -> str:
            return self._unit.strip()
        @unit.setter
        def unit(self, value: str) -> None:
            self._unit = value.strip() if value else ""
        @property
        def as_mpf(self) -> mpmath.mpf:
            if self.mytype == NumType.Int:
                return mpmath.mpf(str(self.numer))
            if self.mytype == NumType.Rat:
                return mpmath.mpf(self.numer)/mpmath.mpf(self.denom)
            return self.real
        @property
        def as_int_or_rat(self) -> ty.Union[int, fractions.Fraction]:
            if self.mytype == NumType.Int:
                return self.numer
            return fractions.Fraction(self.numer, self.denom)
        def to(self, unit: str) -> "Num":
            '''Convert current Num to the specified unit.'''
            if not unit:
                return Num(self)
            arbiter = UnitArbiter()
            is_ok, factor_str = arbiter.check_conformable(self.unit, unit)
            if not is_ok:
                raise ValueError(f"Cannot convert {self.unit} to {unit}")
            factor = mpmath.mpf(factor_str)
            res = Num(self)
            # Switch to Flt if we are scaling
            if res.mytype <= NumType.Rat:
                res.real = res.as_mpf*factor
                res.mytype = NumType.Flt
            else:
                res.real = res.real*factor
                res.imag = res.imag*factor
            res.unit = unit
            return res
        def promote(self) -> "Num":
            '''Attempt to simplify the unit string using high-precision rounding.'''
            if not self.unit:
                return self
            arbiter = UnitArbiter()
            candidate = arbiter.discover_best_unit(self.unit)
            if candidate == self.unit:
                return self
            is_ok, factor_str = arbiter.check_conformable(self.unit, candidate)
            if is_ok:
                factor = mpmath.mpf(factor_str)
                # Check if factor is 1.0 within 12 digits
                if self.round_off(factor, digits=12) == 1:
                    return self.to(candidate)
            return self
        def round_off(self, val: ty.Any, digits: int = 12) -> ty.Any:
            '''Round the significand to clean up floating point noise.'''
            if isinstance(val, (int, fractions.Fraction)):
                return val
            if isinstance(val, mpmath.mpf):
                d = decimal.Decimal(mpmath.nstr(val, 17))
                with decimal.localcontext() as ctx:
                    ctx.prec = digits
                    d = +d
                return mpmath.mpf(str(d))
            return val

if 0:  # Section: Unit Arbiter and Registration
    class UnitArbiter:
        '''A singleton with a lock for GNU Units communication.'''
        _instance: ty.Optional["UnitArbiter"] = None
        _lock = threading.Lock()
        def __new__(cls):
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UnitArbiter, cls).__new__(cls)
                    cls._instance._init_arbiter()
            return cls._instance
        def _init_arbiter(self):
            self.path = os.path.expanduser("~/.units_dynamic")
            if not os.path.exists(self.path):
                open(self.path, "a").close()
            self.proc = None
            self._start_process()
        def _start_process(self):
            if self.proc:
                self.proc.terminate()
            # Added -d 15 for 15-digit precision consistency
            cmd = ["units", "-q", "-d", "15", "-f", "/home/don/.0rc/bin/definitions.units", "-f", self.path]
            Dbg(f"Starting 'units' process with command\n  {cmd}")
            self.proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            '''Returns (is_match, multiplier_or_error_string)'''
            with self._lock:
                try:
                    Dbg(f"check_conformable:  have = {have}, want = {want}")
                    if not have or not want:
                        return False, "0"
                    query = f"{have}\n{want}\n"
                    self.proc.stdin.write(query)
                    self.proc.stdin.flush()
                    line_1 = self.proc.stdout.readline().strip()
                    # If it's a conformability error, it outputs 3 lines.
                    # We need to consume all of them to keep the pipe clean.
                    if "conformability error" in line_1:
                        line_2 = self.proc.stdout.readline().strip()
                        line_3 = self.proc.stdout.readline().strip()
                        Dbg(f"  conformability error: {line_2} vs {line_3}")
                        return False, line_1
                    if not line_1 or "error" in line_1 or "unknown" in line_1.lower():
                        Dbg(f"  error in units call: {line_1}")
                        return False, line_1
                    line_2 = self.proc.stdout.readline().strip()
                    Dbg(f"  line_1 = {line_1!r}")
                    Dbg(f"  line_2 = {line_2!r}")
                    # Factor is the reciprocal of line 1 (the 'want' per 'have')
                    factor_string = line_1.split()[-1]
                    Dbg(f"  returning True, factor_string = {factor_string!r}")
                    return True, factor_string
                except Exception as e:
                    Dbg(f"Restarting 'units' process: {e!r}", color="yel")
                    self._start_process()
                    return False, str(e)
        def add_primitive(self, unit_name: str) -> None:
            '''Inject a new primitive into the dynamic units file.'''
            if not unit_name:
                return
            with self._lock:
                with open(self.path, "a+") as f_handle:
                    try:
                        fcntl.flock(f_handle, fcntl.LOCK_EX)
                        f_handle.seek(0)
                        content = f_handle.read()
                        if unit_name not in content:
                            f_handle.write(f"{unit_name}\tprimitive\n")
                            f_handle.flush()
                            Dbg(f"Added primitive '{unit_name}' to {self.path}", color="grn")
                            self._start_process()
                    finally:
                        fcntl.flock(f_handle, fcntl.LOCK_UN)
        def discover_best_unit(self, unit_expr: str) -> str:
            '''Return the standard named unit equivalent to the expression.'''
            if not unit_expr or "*" not in unit_expr and "/" not in unit_expr:
                return unit_expr
            with self._lock:
                try:
                    # '?' followed by 'quit' to clear the pipe
                    query = f"{unit_expr}\n?\nquit\n"
                    self.proc.stdin.write(query)
                    self.proc.stdin.flush()
                    candidates = []
                    while True:
                        line = self.proc.stdout.readline().strip()
                        if not line or "You want:" in line:
                            break
                        parts = line.split()
                        if parts:
                            candidates.append(parts[0])
                    # Preference list for promotion
                    priority = ["N", "J", "W", "Pa", "V", "A", "Ohm", "Hz", "F", "H", "T", "Wb"]
                    for p in priority:
                        if p in candidates:
                            return p
                    return unit_expr
                except Exception as e:
                    Dbg(f"Promotion failed: {e!r}")
                    self._start_process()
                    return unit_expr
        def promote(self) -> "Num":
            '''Attempt to simplify the unit string to a named standard unit.'''
            if not self.unit:
                return self
            arbiter = UnitArbiter()
            new_unit = arbiter.discover_best_unit(self.unit)
            if new_unit != self.unit:
                # Double check the factor is 1 before finalizing
                is_ok, factor = arbiter.check_conformable(self.unit, new_unit)
                if is_ok and factor == "1":
                    Dbg(f"Promoted {self.unit} -> {new_unit}", color="grn")
                    res = Num(self)
                    res.unit = new_unit
                    return res
            return self
else: # New Unit Arbiter and Registration
    class UnitArbiter:
        '''A singleton with a lock for GNU Units communication.'''
        _instance: ty.Optional["UnitArbiter"] = None
        _lock = threading.Lock()
        def __new__(cls):
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UnitArbiter, cls).__new__(cls)
                    cls._instance._init_arbiter()
            return cls._instance
        def _init_arbiter(self):
            self.path = os.path.expanduser("~/.units_dynamic")
            if not os.path.exists(self.path):
                open(self.path, "a").close()
            self.proc = None
            self._start_process()
        def _start_process(self):
            if self.proc:
                self.proc.terminate()
            # Forced high precision to ensure RoundOff has enough data
            cmd = ["units", "-q", "-d", "15", "-f", "/home/don/.0rc/bin/definitions.units", "-f", self.path]
            Dbg(f"Starting 'units' process with command\n  {cmd}")
            self.proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        def check_conformable(self, have: str, want: str) -> ty.Tuple[bool, str]:
            '''Returns (is_match, multiplier_or_error_string)'''
            with self._lock:
                try:
                    if not have or not want:
                        return False, "0"
                    query = f"{have}\n{want}\n"
                    self.proc.stdin.write(query)
                    self.proc.stdin.flush()
                    line_1 = self.proc.stdout.readline().strip()
                    if "conformability error" in line_1:
                        self.proc.stdout.readline() # Consume line 2
                        self.proc.stdout.readline() # Consume line 3
                        return False, line_1
                    if not line_1 or "error" in line_1 or "unknown" in line_1.lower():
                        return False, line_1
                    line_2 = self.proc.stdout.readline().strip()
                    factor_string = line_1.split()[-1]
                    return True, factor_string
                except Exception as e:
                    self._start_process()
                    return False, str(e)
        def discover_best_unit(self, unit_expr: str) -> str:
            '''Return the standard named unit equivalent to the expression.'''
            if not unit_expr:
                return ""
            with self._lock:
                try:
                    query = f"{unit_expr}\n?\nquit\n"
                    self.proc.stdin.write(query)
                    self.proc.stdin.flush()
                    candidates = []
                    while True:
                        line = self.proc.stdout.readline().strip()
                        if not line or "You want:" in line:
                            break
                        parts = line.split()
                        if parts:
                            candidates.append(parts[0])
                    priority = ["N", "J", "W", "Pa", "V", "A", "Ohm", "Hz", "F", "H", "T", "Wb"]
                    for p in priority:
                        if p in candidates:
                            return p
                    return unit_expr
                except Exception as e:
                    self._start_process()
                    return unit_expr

if 1:  # Section: Register unit
    def RegisterUnit(unit_name: ty.Optional[str]) -> None:
        '''Register a new primitive unit if it is unknown to the arbiter.'''
        if not unit_name:
            return
        arbiter = UnitArbiter()
        # Existence check: compare unit to itself.
        # This avoids dimension mismatches with '1'.
        is_known, message = arbiter.check_conformable(unit_name, unit_name)
        if not is_known and "unknown" in message.lower():
            arbiter.add_primitive(unit_name)

if 0:  # Section: Discovery Pipe Test
    def Test_Discovery_Pipe():
        '''Test if '?' dump works over a non-interactive pipe without a pager.'''
        arbiter = UnitArbiter()
        unit_to_test = "kg m^2 / s^2"
        try:
            Dbg(f"Testing discovery pipe for: {unit_to_test}", color="sky")
            # We send the unit, then the '?', then 'quit' just to be safe
            query = f"{unit_to_test}\n?\nquit\n"
            arbiter.proc.stdin.write(query)
            arbiter.proc.stdin.flush()
            Dbg("Reading response from pipe...", color="mag")
            lines_captured = 0
            # We'll read until the pipe is empty or we hit a timeout
            while lines_captured < 100:
                line = arbiter.proc.stdout.readline().strip()
                if not line:
                    break
                # We expect to see units like 'joule', 'newton meter', etc.
                Dbg(f"  [{lines_captured:02d}] {line}")
                lines_captured += 1
                # If we see the next prompt, we're done with the list
                if "You want:" in line:
                    break
            if lines_captured > 5:
                print(f"{t.grn}Success:{t.n} Captured {lines_captured} conformable units.")
            else:
                print(f"{t.red}Failure:{t.n} Captured only {lines_captured} lines. Pager might be blocking.")
        except Exception as e:
            print(f"{t.red}Error during pipe test:{t.n} {e!r}")

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
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
        def Warn(*msg, **kw):
            print(*msg, file=sys.stderr)
        def Error(*msg, status=1):
            Warn(f"{t.err}", end="")
            Warn(*msg)
            Warn(f"{t.n}")
            exit(status)
        def Usage(status=1):
            print(dedent(f'''
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
    if 1:
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        #if args:
        #    for arg in args:
        #        pass    # Do stuff
    if 1:   # Demo & tests for module
        zero = mpmath.mpf(0)
        def Demo():
            pass
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
                    expected = "-2.2808399000000001"
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
        if 0:   # Special one-off test area
            Test_Discovery_Pipe()
            exit()
            
        exit(run(globals(), regexp=r"^Test_", halt=1, verbose=0)[0])
