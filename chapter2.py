# Python3.7.4


# 2.1 Splitting Strings on Any of Multiple Delimiters

line = "asdf fjdk; afed, fjek asdf,    foo"

import re

print(sorted(re.split(r"[;,\s]\s*", line)))

fields = re.split(r'(;|,|\s)\s*', line)
print(fields)

values = fields[::2]
delimiters = fields[1::2] + ['']

print(values)
print(delimiters)

# Reform the line using the same delimiters

print(''.join(v+d for v, d in zip(values, delimiters)))
print(re.split(r'(?:,|;|\s)\s*', line))


# 2.2 Matching Text at the Start or End of a String

filename = 'spam.txt'

print(filename.endswith('.txt'))

print(filename.startswith('file:'))

url = 'http://www.python.org'

print(url.startswith('http:'))

# Check against multiple choices with a tuple

import os

filenames = os.listdir('.')

print(filenames)

print([name for name in filenames if name.endswith(('.c', '.h')) ])

print(any(name.endswith('.py') for name in filenames))

# Another example

from urllib.request import urlopen

def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

choices = ['http:', 'ftp:']
url = 'http://www.python.org'

print(url.startswith(tuple(choices)))

# Can be done with slices but far less elegant

filename = 'spam.txt'

print(filename[-4:] == '.txt')

url = 'http://www.python.org'

print(url[:5] == 'http:' or url[:6] == 'https:' or url[:4] == 'ftp:')


# example using regular expression

import re

url = 'http://www.python.org'

print(re.match('http:|https:|ftp:', url))


# 2.3 Matching Strings Using Shell Wildcard Patterns.


from fnmatch import fnmatch, fnmatchcase

print(fnmatch('foo.txt', '*.txt'))
print(fnmatch('foo.txt', '??o.txt'))
print(fnmatch('Dat45.csv', 'Dat[0-9]*'))

names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
print([name for name in names if fnmatch(name, 'Dat*.csv')])

# fnmatch() uses same case-sensitivity rules as the system's filesystem.

# Example on OS X.

print(fnmatch('foo.txt', '*.TXT'))

# Example on Windows.

print(fnmatch('foo.txt', '*.TXT'))

# Using fnmatchcase

print(fnmatchcase('foo.txt', '*.TXT'))


# Use with data processing of nonfilename strings.

addresses = [
    '5412 N CLARK ST',
    '1060 W ADDISON ST',
    '1039 W GRANVILLE AVE',
    '2122 N CLARK ST',
    '4802 N BROADWAY',
]

from fnmatch import fnmatchcase

print([addr for addr in addresses if fnmatchcase(addr, '* ST')])
print([addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')])


# 2.4 Matching and Searching for Text Patterns

text = "yeah, but no, but yeah, but no, but yeah"

# Not a match.
print(text == 'yeah')

# Match at start or end.

print(text.startswith('yeah'))

print(text.endswith('no'))

# Search for location of first occurrence.

print(text.find('no'), (text.find('but')))


# For more complicated matching, use regular expressions & re module.

text1 = '11/27/2010'
text2 = 'Nov 27, 2019'

import re

# Simple matching: /d+ means match one or more digits.

if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

# Create pattern object if you're doing a lot of matching.

datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')

if datepat.match(text2):
    print('yes')
else:
    print('no')

"""match() always tries to find match at start of string.
To find all occurrences of a pattern, use findall()
"""

text = 'Today is 11/27/2019. PyCon starts 3/13/2019.'
print(datepat.findall(text))

# With regular expressions, common to capture groups by parts of pattern.

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

m = datepat.match('11/27/2019')
print(m)

# Extract the contents of each group.

print(m.group(0))  # The full date
print(m.group(1))  # The month
print(m.group(2))  # The day of month
print(m.group(3))  # The year
print(m.groups())  # The full date captured individually in ''

month, day, year = m.groups()

print(text)

print(datepat.findall(text))

for month, day, year in datepat.findall(text):
    print('{}-{}-{}'.format(year, month, day))


# Finding matches iteratively using finditer()

for m in datepat.finditer(text):
    print(m.groups())

# Remember that match() starts at the beginning of strings.

# Might have this problem.

m = datepat.match('11/27/2019abcdef')
print(m.group())

# To get an exact match include the end-marker ($)

datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
datepat.match('11/27/2019abcdefg')

print(datepat.match('11/27/2019'))

# Using module-level functions instead.

print(re.findall(r'(\d+)/(\d+)/(\d+)', text))


# 2.5 Searching & Replacing Text

text = 'yeah, but no, but yeah, but no, but yeah'

print(text.replace('yeah', 'yep'))

# For more complicated patterns, use the sub()function/methods in re module.

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

import re

print(re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text))

# Consider compiling it you're performing repeated substitutions.

import re

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

print(datepat.sub(r'\3-\1-\2', text))

# Using a substitution callback function for more complicated substitutions.

from calendar import month_abbr

def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

print(datepat.sub(change_date, text))

"""To know how many subsitutions were made in addition to getting
replacement text, use re.subn() intead."""

newtext, n = datepat.subn(r'\3-\1-\2', text)

print(newtext)
print(n)


