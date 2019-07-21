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


# 2.6 Searching & Replacing Case-Insensitive Text

text = 'UPPER PYTHON, lower python, Mixed Python'

print(re.findall('python', text, flags=re.IGNORECASE))
print(re.sub('python', 'snake', text, flags=re.IGNORECASE))

# Support function to fix replacing text to match text.

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
        return replace
        print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE))


# 2.7 Specifying a Regular Expression for the Shortest Match

str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'

print(str_pat.findall(text1))

text2 = 'Computer says "no." Phone says "yes."'

print(str_pat.findall(text2))

# Add (?) to fix not matching the two quoted strings & makes it nongreedy.

str_pat = re.compile(r'\"(.*?)"')

print(str_pat.findall(text2))


# 2.8 Writing a Regular Expression for Multiline Patterns

comment = re.compile(r'/\*(.*?)\*')
text1 = '/* this is a comment */'
text2 = '''/* this is a
              multiline comment */
'''
print(comment.findall(text1))                    
print(comment.findall(text2))

# To fix, add support for newlines.

comment = re.compile(r'/\*((?:.|\n)*?)\*/')

print(comment.findall(text2))

# re.DOTALL makes the (.) match all characters, including newlines.

comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)

print(comment.findall(text2))


# 2.9 Normalizing Unicode Text to a Standard Representation

s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'

print(s1)
print(s2)

s1 == s2  # False

print(len(s1))  # 14
print(len(s2))  # 15

"""To fix multiple representations, normalize
text into standard representation."""

import unicodedata

t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
t1 == t2  # True

print(ascii(t1))

t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
t3 == t4  # True

print(ascii(t3))

# Add extra compatibility.

s = '\ufb01'  # A single character

print(s)
print(unicodedata.normalize('NFD', s))

# Combined letters are broken apart here

print(unicodedata.normalize('NFKD', s))
print(unicodedata.normalize('NFKC', s))

# Wanting to remove all diacritical marks from text.

t1 = unicodedata.normalize('NFD', s1)
print(''.join(c for c in t1 if not unicodedata.combining(c)))


# 2.10 Working with Unicode Characters in Regular Expressions

import re

num = re.compile('\d+')
print(num.match('123'))

# Arabic digits

print(num.match('\u0661\u0662\u0663'))

# Using an escape sequence to match all characters

arabic = re.compile('[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+')

"""Be aware of special cases, like case-insensitive matching
with case folding."""

pat = re.compile('stra\u00dfe', re.IGNORECASE)
s = 'straße'

print(pat.match(s))

pat.match(s.upper())

print(s.upper())


# 2.11 Stripping Unwanted Characters from Strings

# Whitespace stripping.

s = '   hello world  \n'

print(s.strip())
print(s.lstrip())
print(s.rstrip())

# Character stripping.

t = '-----hello====='
print(t.lstrip('-'))
print(t.strip('-='))

# Stripping doesn't apply to any text in middle of string.

s = '    hello      world    \n'
s = s.strip()
print(s)

"""Need to use replace() or regular expression substitution
if you need to alter inner space"""

print(s.replace(' ', ''))

import re

print(re.sub('\s+', ' ', s))  # Adding the space in between "hello world"


# 2.12 Sanitizing & Cleaning Up Text

s = 'pýtĥöñ\fis\tawesome\r\n'

print(s)

remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None
}
a = s.translate(remap)
print(a)

import unicodedata
import sys

cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
                        if unicodedata.combining(chr(c)))

b = unicodedata.normalize('NFD', a)
print(b)

# Map all Unicode dec. digit characters to equivalent in ASCII.

digitmap = { c: ord('0') + unicodedata.digit(chr(c))
             for c in range(sys.maxunicode)
             if unicodedata.category(chr(c)) == 'Nd' }

print(len(digitmap))

# Arabic digits.

x = '\u0661\u0662\u0663'
print(x.translate(digitmap))

# Clean up code with I/) decoding & encoding functions.

print(a)

b = unicodedata.normalize('NFD', a)
print(b.encode('ascii', 'ignore').decode('ascii'))

# Another way to clean up whitespace & faster.

def clean_spaces(s):
    s = s.replace('\r', '')
    s = s.replace('\t', ' ')
    s = s.replace('\f', ' ')
    return s
    print(s)
    
# 2.13 Aligning Text Strings

text = 'Hello World'

print(text.ljust(20))
print(text.rjust(20))
print(text.center(20))

# Optional &&65.180.&&fill character.

print(text.rjust(20,'='))
print(text.center(20,'*'))

# Align with format() function.

print(format(text, '>20'))
print(format(text, '<20'))
print(format(text, '^20'))

# Include fill character other than a space.

print(format(text, '=>20s'))
print(format(text, '*^20s'))

# Format codes can be used to format multiple values.

print('{:>10s} {:>10s}'.format('Hello', 'World'))

# format() isn't specific only to strings.

x = 1.2345

print(format(x, '>10'))
print(format(x, '^10.2f'))

# % operator used to format text in older code.

print('%-20s' % text) # Prints Hello World
print('%20s' % text)

"""Best to use format() function or method"""


# 2.14 Combining and Concatenating Strings.
"""Fastest way is to use join() method"""

parts = ['Is', 'Chicago', 'Not', 'Chicago?']

print(' '.join(parts))
print(','.join(parts))
print(''.join(parts))

# If combining a few strings the "+" operator works well.

a = 'Is Chicago'
b = 'Not Chicago?'

print(a + ' ' + b)

# "+" operator works well with more complicated string formatting.

print('{} {}'.format(a,b))
print(a + ' ' + b)

"""If combining string literals together in source code,
you can simply place them adjacent to each other with no "+" operator"""

a = 'Hello' 'World'
print(a)

"""Using generator expression to convert data to strings and
concatenation st the same time"""

data = ['ACME', 50, 91.1]

print(','.join(str(d) for d in data))

# Be careful not to make things more difficult than it should be.

print(a + ':' + b + ':' + b)  # Ugly
print(': '.join([a, b, b]))    # Ugly

print(a, b, a, sep=': ')       # Better

# Using generator function using yield.

def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'

text = ' '.join(sample())

print(text)


# 2.15 Interpolating Variables in Strings

s = '{name} has {n} messages.'
print(s.format(name='Guido', n=37))

# Using format_map() & vars()

name = 'Guido'
n = 37
print(s.format_map(vars()))

# Also works with instances.

class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n

a = Info('Guido', 37)
print(s.format_map(vars(a)))

# Can't use format() & format_map() if a value is missing.

# print(s.format(name='Guido'))

# A way to avoid that is with __missing__() method.

class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'

del n
print(s.format_map(safesub(vars())))

# Hide variable substition behind small utilitiy function.

import sys

def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))

name = 'Guido'
n = 37

print(sub('Hello {name}'))
print(sub('You have {n} messages.'))
print(sub('Your favorite color is {color}'))

# Using template strings.

import string

s = string.Template('$name has $n messages.')
print(s.substitute(vars()))


# 2.16 Reformatting Text to a Fixed Number of Columns

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap

print(textwrap.fill(s, 70))
print(textwrap.fill(s, 40))
print(textwrap.fill(s, 40, initial_indent='     '))
print(textwrap.fill(s, 40, subsequent_indent='     '))

# How to get terminal size.

import os

# print(os.get_terminal_size().columns)


# 2.17 Handling HTML & XML Entities in Text

s = 'Elements are written as "<tag>text</tag>".'

import html

print(s)
print(html.escape(s))

# Disable escaping of quotes.

print(html.escape(s, quote=False))

"""Emiting text as ASCII & want to embed character code entities
for non-ASCII characters, use the errors='xmlcharrefreplace' argument.
"""

s = 'Spicy Jalapeño'
print(s.encode('ascii', errors='xmlcharrefreplace'))

# Replacing entities in text manually outside of HTML or XML parser's.

s  = 'Spicy &quot;Jalape&#241;o&quot.'

print(html.unescape(s))

t = 'The prompt is &gt;&gt;&gt;'

from xml.sax.saxutils import unescape

print(unescape(t))


# 2.18 Tokenizing Text

text = 'foo = 23 + 42 * 10'

tokens = [('NAME', 'foo'), ('EQ','='), ('NUM', '23'), ('PLUS', '+'),
          ('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]

import re

NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

# Next to tokenize, use scanner() method of pattern objects.

scanner = master_pat.scanner('foo 42')

print(scanner.match())

from collections import namedtuple
Token = namedtuple('Token', ['type','value'])
def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())
# Example use
for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)

# Filter out whitespace.

tokens = (tok for tok in generate_tokens(master_pat, text)
          if tok.type != 'WS')
for tok in tokens:
    print(tok)

"""The order of tokens in master regular expression matters.
The longer pattern goes first"""

LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ]))

# Need to watch out for patterns that form substrings.

PRINT = r'(P<PRINT>print)'
NAME = r'(P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'

master_pat = re.compile('|'.join([PRINT, NAME]))

for tok in generate_tokens(master_pat, 'printer'):
    print(tok)
