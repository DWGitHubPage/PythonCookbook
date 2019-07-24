# Python3.7.4
# Chapter 4.


# 4.1 Manually Consuming an Iterator

with open('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:
        pass

"""Normally, StopIteration is used to signal the end of iteration. If you're
using next() manually, you can instruct it to return a terminating value
such as None, instead"""

with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print(line, end='')

# This is what happens illustrating basic mechanics during iteration.

items = [1, 2, 3]

# Get the iterator.

it = iter(items)  # Invokes items.__iter__()

# Run the iterator

print(next(it))   # Invokes it.__next__()
print(next(it))
print(next(it))


# 4.2 Delegation Iteration

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

# Example:

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)


# 4.3 Creating New Iteration Patterns with Generators

# Example creating generator that produces range of floating-point numbers.

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

"""To use this function, iterate over it using a for loop or some other
function that consumes an iterable"""

for n in frange(0, 4, 0.5):
    print(n)

print(list(frange(0, 1, 0.125)))

"""The presence of a yield statement in a function turns it into a
generator. Unlike a normal function, a generator only runs in response
to iteration"""

def countdown(n):
    print('Starting to count from', n)
    while n > 0:
            yield n
            n -= 1
    print('Done!')

# Create the generator, no output appears.

c = countdown(3)

print(c)

# Run to first yield & emit a value.

print(next(c))  # 3
print(next(c))  # 2
print(next(c))  # 1
# print(next(c))  # Done! & Traceback error.


# 4.4 Implementing the Iterator Protocol

"""Traversing nodes in a depth-first pattern"""

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# Example:

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)

# Alternative implementation of the depth_first() method.

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, other_node):
        self._children.append(other_node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator(object):
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node

        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)

        # Advance to the next child & start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


# 4.5 Iterating in Reverse

a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

"""Only works if object has a size that can be determined or implements
a __reversed__() special method"""

f = open('somefile.txt')
for line in reversed(list(f)):
    print(line, end='')

"""Turning an iterable into a list as shown could consume a lot of memory
if it's large"""

# Reversed iteration customized on user-defined classes.

class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse Iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1
            
            
# 4.6 Defining Generator Functions with Extra State

from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clearn(self):
        self.history.clear()

with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')

"""Including an extra step of calling iter() if you're going to drive
iteration using a technique other than a for loop"""

f = open('somefile.txt')
lines = linehistory(f)

# print(next(lines)) TypeError

# Call iter() first, then start iterating.

it = iter(lines)

print(next(it))
print(next(it))


# 4.7 Taking a Slice of an Iterator

def count(n):
    while True:
        yield n
        n += 1

c = count(0)
# c[10:20]  TypeError

# Now using slicing.

import itertools

for x in itertools.islice(c, 10, 20):
    print(x)


# 4.8 Skipping the First Part of an Iterable


from itertools import dropwhile

# Commented out example.

# with open('/etc/passwd') as f:


# If you know exact number items to skip, use itertools.islice()

from itertools import islice

items = ['a', 'b', 'c', 1, 4, 10, 15]

for x in islice(items, 3, None):
    print(x)
#   for line in dropwhile(lambda line: line.startswith('#'), f):
#       print(line, end='')


# 4.9 Iterating Over All Possible Combinations or Permutations

items = ['a', 'b', 'c']

from itertools import permutations

for p in permutations(items):
    print(p)

# If you want permutations of a smaller length, give length argument.

for p in permutations(items, 2):
    print(p)

"""Use itertools.combinations() to produce sequence of combinations
taken from the input"""

from itertools import combinations, combinations_with_replacement

for c in combinations(items, 3):
    print(c)

for c in combinations(items, 2):
    print(c)


"""Use itertools.combinations_with_replacement() function to allow
the same item to be chosen more than once"""

for c in combinations_with_replacement(items, 3):
    print(c)


# 4.10 Iterating Over the Index-Value Pairs of a Sequence

my_list = ['a', 'b', 'c']

for idx, val in enumerate(my_list):
    print(idx, val)

# To print output with canonical line numbers starting at 1 instead of 0.

my_list = ['a', 'b', 'c']

for idx, val in enumerate(my_list, 1):
    print(idx, val)

"""This case is useful for tracking line numbers in files if you
want to use a line number in an error message"""

def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])

            except ValueError as e:
                print('Line {}: Parse error: {}'.format(lineno, e))

# Applying enumerate to a sequence of tuples.

data = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

for n, (x, y) in enumerate(data, 1):
    print(n, data)


# 4.11 Iterating Over Multiple Sequences Simultaneously

xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 63, 99]

for x, y in zip(xpts, ypts):
    print(x, y)

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']

for i in zip(a, b):
    print(i)

# If that behavior isn't what you need, use itertools.zip_longest().

from itertools import zip_longest

for i in zip_longest(a, b):
    print(i)

for i in zip_longest(a, b, fillvalue=0):  # Instead of None
    print(i)

# Another example.

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]

s = dict(zip(headers, values))
print(s)

# Can also write it like this & it looks cleaner.

for name, val in zip(headers, values):
    print(name, '=', val)
    
# You can also pass more than two sequences of input.

a = [1, 2, 3]
b = [10, 11, 12]
c = ['x', 'y', 'z']

for i in zip(a, b, c):
    print(i)

# Storing values in a list() function.

print(zip(a, b))
print(list(zip(a, b)))


# 4.12 Iterating on Items in Separate Containers

from itertools import chain

a = [1, 2, 3, 4]
b = ['x', 'y', 'z']

for x in chain(a, b):
    print(x)

# Various working sets of items

active_items = set()
inactive_items = set()

# Iterate over all items

for item in chain(active_items, inactive_items):
    for item in active_items:
        for item in inactive_items:
            end

# Inefficient way to write it:

# for x in a + b:

# Better:

for x in chain(a, b):
    print(x)

    
# 4.13 Creating Data Processing Pipelines

import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    # Find filenames in directory tree that match shell wildcard pattern.
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def gen_opener(filenames):
    """Open sequence of filenames one at a time, file closes &
        goes to next iteration"""
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    # Chain sequence of iterators into a single sentence.
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    # Look for regex pattern in a sequence of lines.
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

# Now to find all log lines that contain the word python:

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

"""To extend pipeline further, feed data into generator expressions, this
will find number of bytes transferred & sums the total"""

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None, 1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))


# 4.14 Flattening a Nested Sequence

from collections.abc import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]

# Produces 1 2 3 4 5 6 7 8

for x in flatten(items):
    print(x)  

# If you don't use yield statement, then use for loop.

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable):
            for i in flatten(x):
                yield i
        else:
            yield x


# 4.15 Iterating in Sorted Order Over Merged Sorted Iterables

import heapq

a = [1, 4, 7, 10]
b = [2, 5, 6, 11]

for c in heapq.merge(a, b):
    print(c)

# Example merging two sorted files.

import heapq

with open('somefile.txt', 'rt') as file1, \
     open('somefile.txt') as file2, \
     open('merged_file', 'wt') as outf:

    for line in heapq.merge(file1, file2):
        outf.write(line)


# 4.16 Replacing Infinite while Loops with an Iterator

CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)

# Best to replace that code as:

def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)

# Example using files.

import sys

f = open('/etc/passwd')
for chunk in iter(lambda: f.read(10), ''):
    n = sys.stdout.write(chunk) 
