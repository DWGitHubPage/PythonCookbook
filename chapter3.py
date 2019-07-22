# Python3.7.4
# Chapter 3.

# 3.1 Rounding Numerical Values

# For simple rounding, use built-in round(value, ndigits) function.

print(round(1.23, 1))
print(round(1.27, 1))
print(round(-1.27, 1))
print(round(1.25361, 3))

"""Value that is halway between twho choices, will round to nearest
even digit"""

a = 1627731
print(round(a, -1))
print(round(a, -2))
print(round(a, -3))

"""Don't confuse rounding with formatting a value for output. If you
need to output a value with a certain number of decimal places, don't
use round, just specify it"""

x = 1.23456

print(format(x, '0.2f'))
print(format(x, '0.3f'))
print('value is {:0.3f}'.format(x))

# Resist urge to round floating-point numbers to fix problems

a = 2.1
b = 4.2
c = a + b

print(c)

c = round(c, 2)

print(c)


# 3.2 Performing Accurate Decimal Calculations

# Some possible errors.

a = 4.2
b = 2.1

print((a + b) == 6.3)

# For more accuracy, use decimal module.

from decimal import Decimal

a = Decimal('4.2')
b = Decimal('2.1')

print(a + b)
print((a + b) == Decimal('6.3'))

"""A major feature of decimal is you can control different aspects
of calculations including number of digits & rounding by creating a
local context & change its settings"""

from decimal import localcontext

a = Decimal('1.3')
b = Decimal('1.7')

print(a / b)

with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)

with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)

"""Be careful with effects of subtractive cancellation & adding
large & small numbers together"""

nums = [1.23e+18, 1, -1.23e+18]

print(sum(nums))  # 1 disappears

# More accurate implementation.

import math

print(math.fsum(nums))


# 3.3 Formatting Numbers for Output

x = 1234.56789

# Two decimal places of accuracy.

print(format(x, '0.2f'))

# Right justified in 10 chars, one-digit accuracy.

print(format(x, '>10.1f'))

# Left justified.

print(format(x, '<10.1f'))

# Centered.

print(format(x, '^10.1f'))

# Inclusion of thousands seperator.

print(format(x, ','))
print(format(x, '0,.1f'))

# If you want to use exponential notation, change the f to an e or E.

print(format(x, 'e'))
print(format(x, '0.2E'))

# Same format codes are used in the .format() method.

print('The value is {:0,.2f}'.format(x))

"""When the number of digits is restricted, values are rounded away
according to the same rules of the round() function"""

print(x)
print(format(x, '0.1f'))
print(format(-x, '0.1f'))

# Using the locale module & swapping separator chars with translate() method.

swap_seperators = { ord('.'):',', ord(','):'.' }

print(format(x, ',').translate(swap_seperators))

# Using % to format.

print('%0.2f' % x)
print('%10.1f' % x)
print('%-10.1f' % x)

"""That formatting is acceptable but less powerful than the
format() method & some features are not supported with the % operator"""


# 3.4 Working with Binary, Octal, & Hexadecimal Integers

x = 1234
print(bin(x))
print(oct(x))
print(hex(x))

# You can also use format() function.

print(format(x, 'b'))
print(format(x, 'o'))
print(format(x, 'x'))

"""Integers are signed, if you're using negative numbers, their output
will also include a sign"""

x = -1234
print(format(x, 'b'))
print(format(x, 'x'))

"""If you need to produce an unsigned value instead, you need to add in
the maximum value to set the bit length."""

# For a 32-bit value.

x = -1234

print(format(2**32 + x, 'b'))
print(format(2**32 + x, 'x'))

# To convert integer strings in different bases, use the int() function.

print(int('4d2', 16))
print(int('10011010010', 2))

"""Using octal values is different in python than other languages. Make
sure to prefix octal value with 0o"""

import os

# print(os.chmod('script.py', 0o755))


# 3.5 Packing & Unpacking Large Integers from Bytes

data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

# To interpret bytes as an integer, use int..from_bytes().

print(len(data))
print(int.from_bytes(data, 'little'))
print(int.from_bytes(data, 'big'))

"""To convert a large integer value back into byte string,
use int.to_bytes() method"""

x = 94522842520747284487117727783387188

print(x.to_bytes(16, 'big'))
print(x.to_bytes(16, 'little'))

# Using the struct module but it is limited, need to unpack & combine them.

print(data)

import struct

hi, lo = struct.unpack('>QQ', data)

print((hi << 64) + lo)

# Using a hexadecimal value.

x = 0x01020304

print(x.to_bytes(4, 'big'))
print(x.to_bytes(4, 'little'))

"""If you try to pack an integer into a byte string but it won't fit,
you'll get an error, best to use int..bit_length() method"""

x = 523 ** 23

print(x)
print(x.bit_length())

nbytes, rem = divmod(x.bit_length(), 8)
if rem:
    nbytes += 1

print(x.to_bytes(nbytes, 'little'))


# 3.6 Performing Complex-Valued Math

a = complex(2, 4)
b = 3 - 5j

print(a)
print(b)

# How to get real, imaginary, & conjugate values.

print(a.real)
print(a.imag)
print(a.conjugate())

# Also, usual mathematical operators work as well.

print(a + b)
print(a * b)
print(a / b)
print(abs(a))

# Use the cmath module to get sines, cosines, or square roots.

import cmath

print(cmath.sin(a))
print(cmath.cos(a))
print(cmath.exp(a))

# Using numpy to make arrays of complex values & perform operations.

import numpy as np

a = np.array([2+3j, 4+5j, 6-7j, 8+9j])

print(a)
print(a + 2)
print(np.sin(a))

"""Python's standard math functions don't produce complex values
by default so it's unlikely that value will show up in code"""

import math

# print(math.sqrt(-1))  Won't work.

"""Need to explicitly use cmath to declare the use of a complex type
libraries that know about them"""

import cmath

print(cmath.sqrt(-1))


# 3.7 Working with Infinity & NaNs(Not a Number)

a = float('inf')
b = float('-inf')
c = float('nan')

print(a)
print(b)
print(c)

# To test for these values, use math.isinf() & math.isnan() functions.

print(math.isinf(a))
print(math.isnan(c))


"""Be aware of some issues, like infinite values will propagate in calculations
in a mathematical manner"""

a = float('inf')

print(a + 45)
print(a * 10)
print(10 / a)

# Certain operations are undefined & will result in a NaN result.

a = float('inf')

print(a/a)

b = float('-inf')

print(a + b)

# NaN values propagate through all operations without raisin exception.

c = float('nan')

print(c)
print(c / 2)
print(c * 2)
print(math.sqrt(c))

# NaN value never compare as equal.

c = float('nan')
d = float('nan')

print(c == d)
print(c is d)

# 3.8 Calculating with Fractions

from fractions import Fraction

a = Fraction(5, 4)
b = Fraction(7, 16)

print(a + b)
print(a * b)

# Getting numerator/denominator

c = a * b

print(c.numerator)
print(c.denominator)

# Converting to a float

print(float(c))

# Limiting the denominator of a value.

print(c.limit_denominator(8))

# Converting a float to a fraction.

x = 3.75
y = Fraction(*x.as_integer_ratio())

print(y)
