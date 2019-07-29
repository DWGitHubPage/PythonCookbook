# Python3.7.4
# Chapter 6.


# 6.1 Reading & Writing CSV Data

import csv

with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        print(row)

from collections import namedtuple

with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    for r in f_csv:
        print(r)

with open('stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row)

headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
        ]
with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    print(rows)

headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]

with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
    print(rows)

# Performing extra type conversions on CSV data.

col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        # Apply conversions to the row items
        row = tuple(convert(value) for convert, value in zip(col_types, row))
        print(rows)

# Example converting selected fields of dictionaries.

print('Reading as dicts with type conversion')
field_types = [ ('Price', float),
            ('Change', float),
            ('Volume', int) ]
with open('stocks.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key]))
            for key, conversion in field_types)
        print(row)


# 6.2 Reading & Writing JSON Data

"""How to turn Python data structure into JSON"""

import json

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
    }

json_str = json.dumps(data)
print(data)

# Here is how to turn JSON-encoded string back into Python data structure.

data = json.loads(json_str)
print(json_str)

"""If you're using files instead of strings, use json.dump() & json.load()
to encode & decode JSON data"""

# Writing JSON data

with open('data.json', 'w') as f:
    json.dump(data, f)

# Reading data back
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)

"""The format of JSON encoding is almost identical to Python except None
is null"""

print(json.dumps(False))

d = {'a': True,
     'b': 'Hello',
     'c': None}

print(json.dumps(d))

# Using pprint() function to alphabetize & output a dictionary better.

from urllib.request import urlopen
import json

u = urlopen('http://twitter.com/search.json?q=python&rpp=5')
resp = json.loads(b'{}')

from pprint import pprint

print(pprint(resp))

"""Creating different kinds of objects with object_pairs_hook or
object_hook"""

s = '{"name": "ACME", "shares": 50, "price": 490.1}'

from collections import OrderedDict     
data = json.loads(s, object_pairs_hook=OrderedDict)

print(data)

# Turning a JSON dictionary into a Python object.

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONObject)

print(data.name)
print(data.shares)
print(data.price)

# Serializing instances with function method.

def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d

# 6.3 Parsing Simple XML Data

from urllib.request import urlopen
from xml.etree.ElementTree import parse

# Download the RSS feed & parse it.

u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)

# Extract & output tags of interest.

for item in doc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

    print(title)
    print(date)
    print(link)
    print()

# Other attributes.

print(doc)

e = doc.find('channel/title')

print(e)
print(e.tag)
print(e.text)
print(e.get('some_attribute'))


# 6.4 Parsing Huge XML Files Incrementally

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)


    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

from xml.etree.ElementTree import parse
from collections import Counter

potholes_by_zip = Counter()

doc = parse('potholes.xml')
for pothole in doc.iterfind('row/row'):
    potholes_by_zip[pothole.findtext('zip')] += 1

for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

from collections import Counter
potholes_by_zip = Counter()


data = parse_and_remove('potholes.xml', 'row/row')
for pothole in data:
    potholes_by_zip[pothole.findtext('zip')] += 1


for zipcode, num in potholes_by_zip.most_common():
    print(zipcode, num)

data = iterparse('potholes.xml',('start','end'))
next(data)

elem_stack[-2].remove(elem)


# 6.5 Turning a Dictionary into XML

from xml.etree.ElementTree import Element
def dict_to_xml(tag, d): 
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

s = { 'name': 'GOOG', 'shares': 100, 'price':490.1 }
e = dict_to_xml('stock', s)

print(e)

# Converting to a byte string.

from xml.etree.ElementTree import tostring

print(tostring(e))

# If you want to attach attributes to an element, use its set() method.

e.set('_id', '1234')

print(tostring(e))

# If you need to manually escape or unescape characters:

from xml.sax.saxutils import escape, unescape

print(escape('<spam>'))


# 6.6 Parsing, Modifying, & Rewriting XML

from xml.etree.ElementTree import parse, Element

doc = parse('pred.xml')
root = doc.getroot()

print(root)

# Remove a few elements.

root.remove(root.find('sri'))
root.remove(root.find('cr'))

# Insert a new element after <nm>...</nm>

print(root.getchildren().index(root.find('nm')))

e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

# Write back to a file.

doc.write('newpred.xml', xml_declaration=True)


# 6.7 Parsing XML Documents with Namespaces

from xml.etree.ElementTree import parse, Element

doc = parse('thor.xml')
root = doc.getroot()

print(doc.findtext('author'))
print(doc.find('content'))      

# A query involving a namespace (doesn't work)
doc.find('content/html')

# Works if fully qualified.

print(doc.find('content/{http://www.w3.org/1999/xhtml}html'))

# Doesn't work.

doc.findtext('content/{http://www.w3.org/1999/xhtml}html/head/title')

# Fully qualified.

print(doc.findtext('content/{http://www.w3.org/1999/xhtml}html/'
'{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/1999/xhtml}title'))

# Simplify matters by wrapping namespace handling into a utility class.

class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)
    def register(self, name, uri):
        self.namespaces[name] = '{'+uri+'}'
    def __call__(self, path):
        return path.format_map(self.namespaces)

ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')

print(doc.find(ns('content/{html}html')))
print(doc.findtext(ns('content/{html}html/{html}head/{html}title')))

from xml.etree.ElementTree import iterparse
for evt, elem in iterparse('thor.xml', ('end', 'start-ns', 'end-ns')):

    print(evt, elem)


# 6.8 Interacting with a Relational Database

stocks = [
    ('GOOG', 100, 4901),
    ('AAPL', 50, 545.75),
    ('FB', 150, 7.45),
    ('HPQ', 75, 33.2),
    ]

import sqlite3

db = sqlite3.connect('database.db')

c = db.cursor()

db.commit()

print(c.executemany('insert into portfolio values (?, ?, ?)', stocks))

for row in db.execute('select * from portfolio'):
    print(row)

min_price = 100
for row in db.execute('select * from portfolio where price >= ?',
                      (min_price,)):
    print(row)


# 6.9 Decoding & Encoding Hexadecimal Digits

# Initial byte string
s = b'hello'

# Encode as hex
import binascii

h = binascii.b2a_hex(s)

print(h)

# Decode back to bytes
print(binascii.a2b_hex(h))

# Similar functionality can be found in base64 module.

import base64

h = base64.b16encode(s)

print(h)

print(base64.b16decode(h))

# To coerce it to Unicode for output, you need an extra decoding step.

h = base64.b16encode(s)

print(h)

print(h.decode('ascii'))


# 6.10 Decoding & Encoding Base64

# Some byte data
s = b'hello'

import base64

# Encode as Base64
a = base64.b64encode(s)

print(a)

# Decode from Base64

print(base64.b64decode(a))

# If you're mixing Base64 with Unicode text, need to add another step.

a = base64.b64encode(s).decode('ascii')

print(a)


# 6.11 Reading & Writing Binary Arrays of Structures

from struct import Struct

def write_records(records, format, f):
    '''
    Write a sequence of tuples to a binary file of structures.
    '''
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))

# Example
if __name__ == '__main__':
    records = [ (1, 2.3, 4.5),
                (6, 7.8, 9.0),
                (12, 13.4, 56.7) ]

    with open('data.b', 'wb') as f:
        write_records(records, '<idd', f)

# Several approaches for reading this file back into a list of tuples.

from struct import Struct

def read_records(format, f):
    record_struct = Struct(format)
    chunks = iter(lambda: f.read(record_struct.size), b'')
    return (record_struct.unpack(chunk) for chunk in chunks)

# Example
if __name__ == '__main__':
    with open('data.b', 'rb') as f:
        for rec in read_records('<idd', f):
            print(rec)

# To read the file entirely into a byte string with a single read & convert it.

from struct import Struct

def unpack_records(format, data):
    record_struct = Struct(format)
    return (record_struct.unpack_from(data, offset)
            for offset in range(0, len(data), record_struct.size))

# Example
if __name__ == '__main__':
    with open('data.b', 'rb') as f:
        data = f.read()

    for rec in unpack_records('<idd', data):
        print(rec)

# To declare a new structure, simply create an instance of Struct such as:

record_struct = Struct('<idd')

# Using pack() and unpack methods().

from struct import Struct

record_struct = Struct('<idd')

print(record_struct.size)

print(record_struct.pack(1, 2.0, 3.0))

import struct

print(struct.pack('<idd', 1, 2.0, 3.0))

# Another example.

f = open('data.b', 'rb')
chunks = iter(lambda: f.read(20), b'')

print(chunks)

for chk in chunks:
    print(chk)

# Another way of writing code without using a generator comprehension.
def read_records(format, f):
    record_struct = Struct(format)
    while True:
        chk = f.read(record_struct.size)
        if chk == b'':
            break
        yield record_struct.unpack(chk)
    return records

# If you use unpack() instead of unpack)from(), you would need to modify code like this:

def unpack_records(format, data):
    record_struct = Struct(format)
    return (record_struct.unpack(data[offset:offset + record_struct.size])
        for offset in range(0, len(data), record_struct.size))

# Using numpy instead.

import numpy as np

f = open('data.b', 'rb')
records = np.fromfile(f, dtype='<i, <d, <d')

print(records)
print(records[0])
print(records[1])


# 6.12 Reading Nested & Variable-Sized Binary Structures

polys = [
            [ (1.0, 2.5), (3.5, 4.0), (2.5, 1.5) ],
            [ (7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0) ],
            [ (3.4, 6.3), (1.2, 0.5), (4.6, 9.2) ],
        ]

import struct
import itertools

def write_polys(filename, polys):
    # Determine bounding box
    flattened = list(itertools.chain(*polys))
    min_x = min(x for x, y in flattened)
    max_x = max(x for x, y in flattened)
    min_y = min(y for x, y in flattened)
    max_y = max(y for x, y in flattened)

    with open(filename, 'wb') as f:
        f.write(struct.pack('<iddddi',
                            0x1234,
                            min_x, min_y,
                            max_x, max_y,
                            len(polys)))
        for poly in polys:
            size = len(poly) * struct.calcsize('<dd')
            f.write(struct.pack('<i', size+4))
            for pt in poly:
                f.write(struct.pack('<dd', *pt))

# Call it with our polygon data
write_polys('polys.bin', polys)

# Reading the resulting data back.

import struct

def read_polys(filename):
    with open(filename, 'rb') as f:
        # Read the header
        header = f.read(40)
        file_code, min_x, min_y, max_x, max_y, num_polys = \
            struct.unpack('<iddddi', header)

        polys = []
        for n in range(num_polys):
            pbytes, = struct.unpack('<i', f.read(4))
            polys = []
            for m in range(pbytes // 16):
                pt = struct.unpack('<dd', f.read(16))
                poly.append(pt)
            polys.append(poly)
    return polys

# A more complex way & less messier way by way of creating a class.

import struct

class StructField:
    '''
    Descriptor representing a simple structure field
    '''
    def __init__(self, format, offset):
        self.format = format
        self.offset = offset
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.format,
                                   instance._buffer, self.offset)
            return r[0] if len(r) == 1 else r

class Structure:
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)

# You can now define a structure as a high-level class that mirrors the info.

class PolyHeader(Structure):
    file_code = StructField('<i', 0)
    min_x = StructField('<d', 4)
    min_y = StructField('<d', 12)
    max_x = StructField('<d', 20)
    max_y = StructField('<d', 28)
    num_polys = StructField('<i', 36)

# Example using that class to read the header from the data written earlier.

f = open('polys.bin', 'rb')
phead = PolyHeader(f.read(40))

print(phead.file_code == 0x1234)
print(phead.min_x)
print(phead.min_y)
print(phead.max_x)
print(phead.max_y)
print(phead.num_polys)

# The above is too verbose, now to read the data using a metaclass.

class StructureMeta(type):
    '''
    Metaclass that automatically creates StructField descriptors
    '''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        bytes_order = ''
        offset = 0
        for format, fieldname in fields:
            if format.startswith(('<','>','!', '@')):
                byte_order = format[0]
                format = format[1:]
            format = byte_order + format
            setattr(self, fieldname, StructField(format, offset))
            offset += struct.calcsize(format)
        setattr(self, 'struct_size', offset)

class Structure(metaclass=StructureMeta):
    def __init__(self, bytedata):
        self._buffer = bytedata

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))

# Now you can write a structure definition like this:

class PolyHeader(Structure):
    _fields_ = [
        ('<i', 'file_code'),
        ('d', 'min_x'),
        ('d', 'min_y'),
        ('d', 'max_x'),
        ('d', 'max_y'),
        ('i', 'num_polys')
    ]

f = open('polys.bin', 'rb')
phead = PolyHeader.from_file(f)

print(phead.file_code == 0x1234)
print(phead.min_x)
print(phead.min_y)
print(phead.max_x)
print(phead.max_y)
print(phead.num_polys)

# Supporting nested binary structures with a new supporting descriptor.

class NestedStruct:
    '''
    Descriptor representing a nested structure
    '''
    def __init__(self, name, struct_type, offset):
        self.name = name
        self.struct_type = struct_type
        self.offset = offset
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            data = instance._buffer[self.offset:
                                self.offset+self.struct_type.struct_size]
            result = self.struct_type(data)
            '''Save resulting structure back on instance to
            avoid further recomputation of this step'''
            setattr(instance, self.name, result)
            return result

class StructureMeta(type):
    '''Metaclass that automatically creates StructField descriptors'''
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if isinstance(format, StructureMeta):
                setattr(self, fieldname, NestedStruct(fieldname, format, offset))
                offset += format.struct_size
            else:
                if format.startswith(('<', '>', '!', '@')):
                    byte_order = format[0]
                    format = format[1:]
                format = byte_order + format
                setattr(self, fieldname, StructField(format, offset))
                offset += struct.calcsize(format)
        setattr(self, 'struct_size', offset)

class Structure(metaclass=StructureMeta):
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))

if __name__ == '__main__':
    class Point(Structure):
        _fields_ = [
            ('<d', 'x'),
            ('d', 'y')
            ]

    class PolyHeader(Structure):
        _fields_ = [
            ('<i', 'file_code'),
            (Point, 'min'),
            (Point, 'max'),
            ('i', 'num_polys')
            ]

f = open('polys.bin', 'rb')
phead = PolyHeader.from_file(f)

print(phead.file_code == 0x1234)
print('min.x=', phead.min.x)
print('max.x=', phead.max.x)
print('min.y=', phead.min.y)
print('max.y=', phead.max.y)
print('num_polys=', phead.num_polys)

'''Write a class to represent a chunk of binary data along
with a utility function for interpreting the contents in
different ways'''

class SizedRecord:
    def __init__(self, bytedata):
        self._buffer = memoryview(bytedata)

    @classmethod
    def from_file(cls, f, size_fmt, includes_size=True):
        sz_nbytes = struct.calcsize(size_fmt)
        sz_bytes = f.read(sz_nbytes)
        sz, = struct.unpack(size_fmt, sz_bytes)
        buf = f.read(sz - includes_size * sz_nbytes)
        return cls(buf)

    def iter_as(self, code):
        if isinstance(code, str):
            s = struct.Struct(code)
            for off in range(0, len(self._buffer), s.size):
                yield s.unpack_from(self._buffer, off)
        elif isinstance(code, StructureMeta):
            size = code.struct_size
            for off in range(0, len(self._buffer), size):
                data = self._buffer[off:off+size]
                yield code(data)

f = open('polys.bin', 'rb')
phead = PolyHeader.from_file(f)

print(phead.num_polys)

polydata = [ SizedRecord.from_file(f, '<i')
             for n in range(phead.num_polys) ]

print(polydata)

# Using the iter_as() method to interpret data.

for n, poly in enumerate(polydata):
    print('Polygon', n)
    for p in poly.iter_as('<dd'):
        print(p)

for n, poly in enumerate(polydata):
    print('Polygon', n)
    for p in poly.iter_as(Point):
        print(p.x, p.y)

# An alternativ e formulation of the read_polys() function.

class Point(Structure):
    _fields_ = [
        ('<d', 'x'),
        ('d', 'y')
        ]

class PolyHeader(Structure):
    _fields_ = [
        ('<i', 'file_code'),
        (Point, 'min'),
        (Point, 'max'),
        ('i', 'num_polys')
    ]

def read_polys(filename):
    polys = []
    with open(filename, 'rb') as f:
        phead = PolyHeader.from_file(f)
        for n in range(phead.num_polys):
            rec = SizedRecord.from_file(f, '<i')
            poly = [ (p.x, p.y)
                     for p in rec.iter_as(Point) ]
            polys.append(poly)
        return polys


# 6.13 Summarizing Data & Performing Statistics

import pandas

rats = pandas.read_csv('rats.csv', skip_footer=1)
print(rats)
print(rats['Current Activity'].unique()

crew_dispatched = rats[rats['Current Activity'] == 'Dispatch Crew']

print(len(crew_dispatched)
print(crew_dispatched['ZIP Code'].value_counts()[:10])

# Group by completion date

print(dates = crew_dispatched.groupby('Completion Date'))
print(len(dates))

# Determine counts on each day.

date_counts = dates.size()

print(date_counts[0:10])

# Sort the counts.

date_counts.sort()

print(date_counts[-10:])
