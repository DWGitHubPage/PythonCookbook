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


# 3.9 Calculating with Large Numerical Arrays

# Differences between lists & NumPy arrays.

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

print(x * 2)
# print(x + 10)  # TypeError: can only concatenate list (not 'int') to list

print(x + y)

# Numpy arrays.

import numpy as np

ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

print(ax * 2)
print(ax + 10)
print(ax + ay)
print(ax * ay)

# Computing the value of a polynomial.

def f(x):
    return 3*x**2 - 2*x + 7

print(f(ax))

"""NumPy provides a collection of "universal functions" that also
allow for array operations"""

print(np.sqrt(ax))
print(np.cos(ax))

# Using universal functions can be hundreds of times faster than looping.

grid = np.zeros(shape=(10_000, 10_000), dtype=float)

print(grid)
print(grid + 10)

# Extending Python's list indexing functionality with multidimensional arrays.

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

print(a)

# Select row 1.

print(a[1])

# Select column 1.

print(a[:, 1])

# Select a subregion & change it.

print(a[1:3, 1:3])
print(a[1:3, 1:3] + 10)

# Broadcast a row vector across an operation on all rows.

print(a + [100, 101, 102, 103])
print(a)

# Conditional assignment on an array.

print(np.where(a < 10, a, 10))


# 3.10 Performing Matrix & Linear Algebra Calculations.

import numpy as np

m = np.matrix([[1, -2, 3], [0, 4, 5], [7, 8, -9]])

print(m)

# Return transpose.

print(m.T)

# Return inverse.

print(m.I)

# Create a vector & multiply.

v = np.matrix([[2], [3], [4]])

print(v)
print(m * v)

# More operations with numpy.linalg subpackage.

import numpy.linalg

# Determinant.

print(numpy.linalg.det(m))

# Eigenvalues.

print(numpy.linalg.eigvals(m))

# Solve for x in mx = v.

x = numpy.linalg.solve(m, v)

print(x)
print(m * x)
print(v)


# 3.11 Picking Things at Random

import random

values = [1, 2, 3, 4, 5, 6]

print(random.choice(values))
print(random.choice(values))
print(random.choice(values))
print(random.choice(values))

"""Take a sampling of N items were selected items are removed from
future consideration"""

print(random.sample(values, 2))
print(random.sample(values, 2))
print(random.sample(values, 3))
print(random.sample(values, 3))

# Shuffling items in a sequence in place use random.shuffle().

random.shuffle(values)

print(values)

random.shuffle(values)

print(values)

# To produce random integers, use random.randint().

print(random.randint(0, 10))
print(random.randint(0, 10))
print(random.randint(0, 10))
print(random.randint(0, 10))
print(random.randint(0, 10))
print(random.randint(0, 10))


"""To produce uniforma floating-point values in rane 0 to 1,
use random.random()"""

print(random.random())
print(random.random())
print(random.random())

# To get random-bits expressed as an integer, use random.getrandbits().

print(random.getrandbits(200))

"""The random module computes random numbers using the Mersenne Twister
algorithm. It's a deterministic algorithm, but you can alter the initial
seed by using the random.seed() function"""

print(random.seed())             # Seed based on system time or os.urandom()
print(random.seed(12345))        # Seed based on integer given
print(random.seed(b'bytedata'))  # Seed based on byte data

"""Functions in random() shouldn't be used in cryptography, use ssl
modules instead"""

import ssl

print(ssl.RAND_bytes(1))
print(ssl.RAND_bytes(5))


# 3.12 Converting Days to Seconds, & Other Basic Time Conversions

from datetime import timedelta

a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b

print(c.days)
print(c.seconds)
print(c.seconds / 3600)
print(c.total_seconds() / 3600)

"""If you need specific dates & times, create datetime instances &
use the standard mathematical operations to manipulate them"""

from datetime import datetime

a = datetime(2012, 9, 23)

print(a + timedelta(days=10))

b = datetime(2012, 12, 21)
d = b - a

print(d.days)

now = datetime.today()

print(now)
print(now + timedelta(minutes=10))

# With calculations, datetime is aware of leap years.

a = datetime(2012, 2, 1)
b = datetime(2012, 2, 28)

print(a - b)
print((a - b).days)

c = datetime(2013, 3, 1)
d = datetime(2013, 2, 28)

print((c - d).days)

"""For more complex date manipulations such as time zones, holidays, etc.,
use dateutil module"""

a = datetime(2012, 9, 23)

from dateutil.relativedelta import relativedelta

print(a + relativedelta(months=+1))

# Time between two dates.

b = datetime(2012, 12, 21)
d = b - a

print(d)

d = relativedelta(b, a)

print(d)
print(d.months)
print(d.days)


# 3.13 Determining Last Friday's Date

from datetime import datetime, timedelta

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']

def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

print(datetime.today())
print(get_previous_byday('Monday'))
print(get_previous_byday('Tuesday'))
print(get_previous_byday('Friday'))

"""The optional start_date can be supplied using another datetim instance"""

print(get_previous_byday('Sunday', datetime(2012, 12, 21)))

"""If you're doing a lot of date calculations, might be better off
installing python-dateutil package"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *

d = datetime.now()

print(d)

# Next Friday

print(d + relativedelta(weekday=FR))

# Last Friday

print(d + relativedelta(weekday=FR(-1)))


# 3.14 Finding the Date Range for the Current Month

from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)

a_day = timedelta(days=1)
first_day, last_day = get_month_range()
while first_day < last_day:
    print(first_day)
    first_day += a_day

# Using a generator to calculate dates.

def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

for d in date_range(datetime(2012, 9, 1), datetime(2012, 10, 1),
                    timedelta(hours=6)):
    print(d)


# 3.15 Converting Strings into Datetimes

from datetime import datetime

text = '2012-09-20'
y = datetime.strptime(text, '%Y-%m-%d')
z = datetime.now()
diff = z - y

print(diff)

# datetime can also work in reverse & make it more readable.

print(z)

nice_z = datetime.strftime(z, '%A %B %d, %Y')

print(nice_z)

# Performance of strptime() is often bad, best to use a custom solution instead.

from datetime import datetime

def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


# 3.16 Manipulating Dates Involving Time Zones

from datetime import datetime
from pytz import timezone
import pytz

d = datetime(2012, 12, 21, 9, 30, 0)

print(d)

# Localize the date for Chicago.

central = timezone('US/Central')
loc_d = central.localize(d)

print(loc_d)

"""Once the date has been localized, it can be converted to other time
zones, such as in Bangalore"""

bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))

print(bang_d)

# Make sure to be aware of daylight saving transitions & other details.

# This example would be wrong:

d = datetime(2013, 3, 10, 1, 45)
loc_d = central.localize(d)

print(loc_d)

later = loc_d + timedelta(minutes=30)

print(later)

# Above is wrong because it doesn't account for the one-hour skip in local time.

from datetime import timedelta

later = central.normalize(loc_d + timedelta(minutes=30))

print(later)

# Converting time zones to UTC time.

print(loc_d)

utc_d = loc_d.astimezone(pytz.utc)

print(utc_d)

# Now to convert it to appropriate timze zone.

later_utc = utc_d + timedelta(minutes=30)

print(later_utc.astimezone(central))

# How to find timezeone of a country.

import pytz

utc = pytz.utc

print(pytz.country_timezones['IN'])
