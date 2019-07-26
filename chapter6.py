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
