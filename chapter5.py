# Python3.7.4
# Chapter 5 & other examples.


# 5.1 Reading & Writing Text Data

# Read entire file as a single string:

file = open('somefile.txt')
type(file)
print(file)

# Iterate over the lines of the file:

with open('somefile.txt', 'r') as f:
    line = f.readline()
    while line != '':
        print(line, end='')
        line = f.readline()

# Write chunks of text data.

with open('somefile.txt', 'r') as f:
  print(f.read())

# Redirected print statement.
"""Commented out so it doesn't delete file"""

with open('somefile.txt', 'w') as f:
    print(f)

# If text is in a different encoding, supply optional parameter.

with open('somefile.txt', 'r', encoding='latin-1') as f:
    data = f.read()
    print(data)

# If you don't use with statement, need to close the file.

f = open('somefile.txt', 'r')
data = f.read()
f.close()

# Supplying newline='' argument.

"""Read with disabled newline translation"""
with open('somefile.txt', 'r', newline='') as f:
   print(f)

# Some common error handling schemes you might need.

f = open('somefile.txt', 'r', encoding='ascii', errors='replace')
f.read()

# Ignore bad chars entirely.

g = open('somefile.txt', 'r', encoding='ascii', errors='ignore')
g.read()

"""Extra codes dealing with same subject matter"""

print("Reading a simple text file (UTF-8)")
with open('somefile.txt', 'rt') as f:
    for line in f:
        print(repr(line))

# Reading a text file with universal newlines turned off
print("Reading text file with universal newlines off")
with open('somefile.txt', 'rt', newline='') as f:
    for line in f:
        print(repr(line))

# Reading text file as ASCII with replacement error handling
print("Reading text as ASCII with replacement error handling")
with open('somefile.txt', 'rt', encoding='ascii', errors='replace') as f:
    for line in f:
        print(repr(line))

# Reading text file as ASCII with ignore error handling
print("Reading text as ASCII with ignore error handling")
with open('somefile.txt', 'rt', encoding='ascii', errors='ignore') as f:
    for line in f:
        print(repr(line))

# 5.2 Printing to a File

with open('somefile.txt', 'rt') as f:
    print('Hello World', file=f)


# 5.3 Printing with a Different Separator or Line Ending

print('ACME', 50, 91.5)
print('ACME', 50, 91.5, sep=',')
print('ACME', 50, 91.5, sep=',', end='!!\n')

"""The use of an end argument is also a way to suppress the output of
newlines in output"""

# Example:

for i in range(5):
    print(i + 1)

for i in range(5):
    print(i + 1, end=' ')

# Using str.join() to do same thing.

row = ('ACME', '50', '91.5')
print(', '.join(row))

# This one prints before one abov:

print(', '.join(str(x) for x in row))

# Even simpler way.

print(*row, sep=', ')


# 5.4 Reading & Writing Binary Data

"""Read the entire file as a single byte string"""

with open('somefile.txt', 'rb') as f:
    data = f.read()

"""Write binary data to a file"""

with open('somefile.txt', 'wb') as f:
    f.write(b'Hello World')

"""Semantic differences between byte strings & text strings pose
a potential gotcha. Be aware that indexing & iteration return integer
byte values instead of byte strings"""

# Text String:

t = 'Hello World'
print(t[0])

for c in t:
    print(c)

# Byte String:

b = b'Hello World'
print(b[0])

for c in b:
    print(c)

"""If you need to read/write text from binary-mode file,
make sure to decode & encode it"""

with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))

"""Another aspect of binary I/O is that objects such as arrays & C
structures can be used for writing without any conversion to a bytes object"""

import array

nums = array.array('i', [1, 2, 3, 4])
with open('data.bin', 'wb') as f:
    f.write(nums)

"""Many objects allow binary data to be directly read into underlying
memory using readinto() method of files. Also, this method might not
be usable depending on word size & byte ordering"""

import array

a = array.array('i', [ 0, 0, 0, 0, 0, 0])
with open('data.bin', 'rb') as f:
    f.readinto(a)

print(a)


# 5.5 Writing to a File That Doesn't Already Exist

import os

if not os.path.exists('somefile'):
    with open('somefile', 'wt') as f:
        f.write('Hello\n')
else:
    print('File already exists!')


# 5.6 Performing I/O Operation on a String

import io

s = io.StringIO()

print(s.write('Hello World\n'))
print('This is a test', file=s)

# Get all values of the data written so far.

print(s.getvalue())

# Wrap a file interface around an existing string.

s = io.StringIO('Hello\nWorld\n')

print(s.read(4))
print(s.read())

# If you're operating with binary date, use the io.BytesIO class instead.

s = io.BytesIO()
s.write(b'binary data')

print(s.getvalue())


# 5.7 Reading & Writing Compressed Datafiles

"""To read compressed files as text"""

import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()

import bz2 
with gzip.open('somefile.bz2', 'rt') as f:
    text = f.read()

# To write compressed data.

import gzip

with gzip.open('somefile.gz', 'wt') as f:
    f.write(text)

# When writing compressed data, compression level can be specified.

with gzip.open('somefile.gz', 'wt', compresslevel=5) as f:
    f.write(text)

"""gzip.open() & bz2.open() can be layered on top of an existing
file in binary mode"""

import gzip

f = open('somefile.gz', 'rb')
with gzip.open(f,'rt') as g:
    text = g.read()


# 5.8 Iterating Over Fixed-Sized Records

from functools import partial

RECORD_SIZE = 32

with open('somefile.txt', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        print(r)
      

# 5.9 Reading Binary Data into a Mutable Buffer

import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

# Example illustrating the usage:

"""Write a sample file"""
with open('somefile.bin', 'wb') as f:
    f.write(b'Hello world')

buf = read_into_buffer('somefile.bin')

print(buf)

buf[0:5] = b'Hallo'

print(buf)

with open('newsample.bin', 'wb') as f:
    f.write(buf)

# Example reading a binary file consisting of equally sized records.

record_size = 32

buf = bytearray(record_size)
with open('somefile', 'rb') as f:
    while True:
        n = f.readinto(buf)
        if n < record_size:
            break

""" Using memoryview, which lets you make zero-copy slices of an existing
buffer & change its contents"""

print(buf)

m1 = memoryview(buf)
m2 = m1[-5:]

print(m2)

m2[:] = b'World'

print(buf)


# 5.10 Memory Mapping Binary Files

import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

size = 1000000
with open('data', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

# Example of memory mapping the contents using memory_map() function.

m = memory_map('data')

print(len(m))
print(m[0:10])
print(m[0])

# Reassign a slice.

m[0:11] = b'Hello World'
m.close()

# Verify that changes were made.

with open('data', 'rb') as f:
    print(f.read(11))

# Mmap object returned by mmap() can also be used as a context manager.

with memory_map('data') as m:
    print(len(m))
    print(m[0:11])

print(m.closed)

# If read-access is needed instead, use mmap.ACCESS_READ for access argument.

# m = memory_map(somefile, mmap.ACCESS_READ)

"""If you want to modify data locally but don't want those changes written
back to the original file, use mmap.ACCESS_COPY:"""

# m = memory_map(filename, mmap.ACCESS_COPY)

# Interpret the data differently using memoryview.

m = memory_map('data')

# Memoryview of unsigned integers:

v = memoryview(m).cast('I')
v[0] = 7

print(m[0:4])

print(v[0])


# Manipulating Pathnames

import os

path = '/Users/beazley/Data/data.csv'

# Get the last component of the path.

print(os.path.basename(path))

# Get the directory name.

print(os.path.dirname(path))

# Join path components together.

print(os.path.join('tmp', 'data', os.path.basename(path)))

# Expand the user's home directory.

path = '~/Data/data.csv'

print(os.path.expanduser(path))

# Split the file extension.

print(os.path.splitext(path))


# 5.12 Testing for the Existence of a File

import os

print(os.path.exists('/etc/passwd'))
print(os.path.exists('/tmp/spam'))
print(os.path.exists('somefile'))

# You can perform further tests to see what kind of file it might be.

# Is a regular file.

print(os.path.isfile('/etc/passwd'))

# Is a directory.

print(os.path.isdir('/etc/passwd'))

# Is a symbolic link.

print(os.path.islink('/usr/local/bin/python3'))

# Get the file linked to.

print(os.path.realpath('/usr/local/bin/python3'))

"""You can also get metadata from the os.path module"""

print(os.path.getsize('/etc/passwd'))
print(os.path.getmtime('/etc/passwd'))

import time

print(time.ctime(os.path.getmtime('/etc/passwd')))


# 5.13 Getting a Directory Listing

import os

names = os.listdir('Python')

# If you need to filter the data, use a list comprehension.

import os.path

# Get all regular files.

names = [name for name in os.listdir('Python')
         if os.path.isdir(os.path.join('Python', name))]

# Using startswith() & endswith() methods can help filter as well.

pyfiles = [name for name in os.listdir('Python')
           if name.endswith('.py')]

# For filename matching, you might use glob or fnmatch modules instead.

import glob

pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch

pyfiles = [name for name in os.listdir('Python')
           if fnmatch(name, '*.py')]

"""For additional metadata use additional functions in os.path module
or use os.stat() function"""

# Example of getting a directory listing.

import os
import os.path
import glob

pyfiles = glob.glob('*.py')

# Get file sizes & modification dates.

name_sz_date = [(name, os.path.getsize(name), os.path.getmtime(name))
                for name in pyfiles]

for name, size, mtime in name_sz_date:
    print(name, size, mtime)

# Alternative: Get file metadata.

file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)


# 5.14 Bypassing Filename Encoding

import sys

print(sys.getfilesystemencoding())  # utf-8

"""If you want to bypass that encoding, specify a filename using a
raw byte string instead"""

with open('somefile.txt', 'w') as f:
    f.write('Spicy')

# Directory listing (decoded).

import os

print(os.listdir('.'))

# Directory listing (raw).

print(os.listdir(b'.'))

# Open file with raw filename.

with open(b'somefile.txt') as f:
    print(f.read())


# 5.15 Printing Bad Filenames

filename = f

def bad_filename(filename):
    return repr(filename)[1:-1]

try:
    print(filename)
except UnicodeEncodeError:
    print(bad_filename(filename))
    
# Example showing bad filename encoded with Latin-1 instead of UTF-8.

import os

files = os.listdir('.')

print(files)

# Outputting filename & having it crash.

for name in files:
    print(name)
#   print(spam.py)  # NameError

for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
            print(bad_filename(name))

#  Another option to re-encode the value in some way.

def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')

# Using this version produces the following output.

for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))


# 5.16 Adding or Changing the Encoding of an Already Open File

import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
text = f.read()

f = open('sample.txt', 'w')

print(f)
print(f.buffer)
print(f.buffer.raw)

# Detach method.

b = f.detach()

print(b)

f = io.TextIOWrapper(b, encoding='latin-1')

print(f)
        

# 5.17 Writing Bytes to a Text File

import sys

print(sys.stdout.write('Hello\n'))


# 5.18 Wrapping an Existing File Descriptor As a File Object

# Open a low-level file descriptor.

import os

fd = os.open('somefile.txt', os.O_WRONLY | os.O_CREAT)

# Turn into a proper file.

f = open(fd, 'wt')
f.write('hello world\n')
f.close()

"""When the high-level file object is closed or destroyed, the underlying
file descriptor will also be closed. If you don't want that, supply the
optional closefd=False argument to open().

Replace f.close() above with:

f = open(fd, 'wt', closefd=False)
"""

# An example using sockets.

from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
    print('Got connection from', addr)

    # Make text-mode file wrappers for socket reading/writing.
    client_in = open(client_sock.fileno(), 'rt', encoding='latin-1',
                     closefd=False)
    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1',
                      closefd=False)
    
    # Echo lines back to the client using file I/O.
    for line in client_in:
        client_out.write(line)
        client_out.flush()
    client_sock.close()

def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        echo_client(client, addr)

"""The above code only works on Unix-based systems. Use the makefile()
method if you need to cross platform"""


# 5.19 Making Temporary Files & Directories

from tempfile import TemporaryFile

with TemporaryFile('w+t') as f:
    # Read/write to the file.
    f.write('Hello World\n')
    f.write('Testing\n')

    # Seek back to beginning & read the data.
    f.seek(0)
    data = f.read()

# Or you can use the file like this:

f = TemporaryFile('w+t')
f.close()

# To make a temporary directory, use tempfile.TemporaryDirectory().

from tempfile import TemporaryDirectory

with TemporaryDirectory() as dirname:
    print('dirname is:', dirname)
    

# At a lower level, you can also use mkstemp() & mkdtemp().

import tempfile

print(tempfile.mkstemp())
print(tempfile.mktemp())


# 5.20 Communicating with Serial Ports

import serial

#ser = serial('/dev/ttyusbmodem641',  # Device name varies
             #       baudrate=9600,
              #      bytesize=8,
               #     parity='N',
               #     stopbits=1)


# 5.21 Serializing Python Objects

import pickle

data = (1, 2, 3)
f = open('somefile', 'wb')
pickle.dump(data, f)

s = pickle.dumps(data)


# Restore from a file.

f = open('somefile', 'rb')
data = pickle.load(f)

# Restore from a string.

data = pickle.loads(s)

# Working with multiple objects.

import pickle

f = open('somedata', 'wb')
pickle.dump([1, 2, 3, 4], f)
pickle.dump('hello', f)
pickle.dump({'Apple', 'Pear', 'Banana'}, f)
f.close()

f = open('somedata', 'rb')

print(pickle.load(f))
print(pickle.load(f))
print(pickle.load(f))

"""You can pickle functions, classes, & instances but the resulting
data only encodes name references to the associated code objects"""

import math
import pickle

print(pickle.dumps(math.cos))

