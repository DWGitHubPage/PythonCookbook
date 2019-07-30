# Python3.7.4
# Chapter 7.


# 7.1 Writing Functions That Accept Any Number of Arguments

def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

# Sample use.
avg(1, 2)
avg(1, 2, 3, 4)

'''To accept any number of keyword arguments,
use an argument that starts with **'''

import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name=name,
                attrs=attr_str,
                value=html.escape(value))
    return element

# Creates '<item size="large" quantity="6">Albatross</item>'

make_element('item', 'Albatross', size='large', quantity=6)

# Creates '<p>&lt;spam&gt;</p>'

make_element('p', '<spam>')

'''If you want a function to accept any number of positional &
keyword-only arguments, use * and ** together'''

def anyargs(*args, **kwargs):
    print(args)   # A tuple
    print(kwargs) # A dict

def a(x, *args, y):
    pass

def b(x, *args, y, **kwargs):
    pass


# 7.2 Writing Functions That Only Accept Keyword Arguments

def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True)       # TypeError
recv(1024, block=True)  

def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10)
minimum(1, 5, 2, -5, 10, clip=0)


# 7.3 Attaching Informational Metadata to Function Arguments

def add(x:int, y:int) -> int:
    return x + y

'''Example of storing function annotation in a
function's __annotations__ attribute'''

print(add.__annotations__)


# 7.4 Returning Multiple Values from a Function

'''Simply return a tuple. Creating a tuple with a comma instead
of parentheses'''

def myfun():
    return 1, 2, 3

a, b, c = myfun()

print(a, b, c)

# Another example.

a = (1, 2)  # With parentheses

print(a)

b = 1, 2   # Without parentheses

print(b)

# Tuple unpacking.

x = myfun()
print(x)


# 7.5 Defining Functions with Default Arguments

def spam(a, b=42):
    print(a, b)

print(spam(1))  # a=1, b=42
print(spam(2))  # a =1, b=2

'''If default value is supposed to be a mutable container, such as a
list, set, or dictionary, use None as the default'''

def spam(a, b=None):
    if b is None:
        b = []

'''If you want to write code that tests whether an optional argument
was given a value or not, use this idiom'''

_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

print(spam(1))
print(spam(1, 2))
print(spam(1, None))

'''Values assigned as a default are bound only once at the time
of function definition'''

x = 42
def spam(a, b=x):
    print(a, b)

print(spam(1))

x = 23

print(spam(1))


# 7.6 Defining Anonymous or Inline Functions

'''Simple functions that do nothing more than evaluate an expression
can be replaced by a lambda expression'''

add = lambda x, y: x + y

print(add(2, 3))
print(add('hello', 'world'))

# The use of lambda is the same as typing:

def add(x, y):
    return x + y

print(add(2, 3))

'''Typically, lambda is used in the context of some other operation,
such as sorting or a data reduction'''

names = ['David Beazley', 'Brian Jones',
         'Raymond Hettinger', 'Ned Batchelder']

print(sorted(names, key=lambda name: name.split()[-1].lower()))


# 7.7 Capturing Variables in Anonymous Functions

# Consider the behavior of the following code:

x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

print(a(10))
print(b(10))

'''The value of x used in the lambda expression is a free variable
that gets bound at runtime, not definition time'''

x = 15

print(a(10))

x = 3

print(a(10))

'''If you want an anonymous function to capture a value at the point of
definition & keep it, include the value as a default value'''

x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y

print(a(10))
print(b(10))


# Creating a list of lambda expressions using a list comprehension.

funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0))

# Now compare previous code to the next:

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))

# Function now captures value of n at time of definition.


# 7.8 Making an N-Argument Callable Work As a Callable with Fewer Arguments

def spam(a, b, c, d):
    print(a, b, c, d)

from functools import partial

s1 = partial(spam, 1)

print(s1(2, 3, 4))
print(s1(4, 5, 6))

s2 = partial(spam, d=42)

print(s2(1, 2, 3))
print(s2(4, 5, 6))

s3 = partial(spam, 1, 2, d=42)

print(s3(3))
print(s3(4))
print(s3(5))

'''Examples of the problem of making seemingly incompatible
bits of code work together'''

points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]

import math

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

'''Using partial() to sort all the points according to distance
from some other point'''

pt = (4, 3)
points.sort(key=partial(distance,pt))

print(points)

'''Using multiprocessing to asynchronously compute a result which
is handed to a callback function that accepts both the result &
an optional logging argument'''

def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)

# A sample function
def add(x, y):
    return x + y

if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()

# A simple echo server.

from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            self.wfile.write(b'GOT:' + line)

serv = TCPServer(('', 15000), EchoHandler)
serv.serve_forever()

# Using __init__() method that accepts an additional configuration argument.

class EchoHandler(StreamRequestHandler):

    def __init__(self, *args, ack, **kwargs):
        self.ack = ack
        super().__init__(*args, **kwargs)
    def handle(self):
        for line in self.rfile:
            self.wfile.write(self.ack + line)

# Using partial() as a workaround.

from functools import partial

serv = TCPServer(('', 15000), partial(EchoHandler, ack=b'RECEIVED:'))
serv.serve_forever()

# Using a lambda expression but this is more verbose.

points.sort(key=lambda p: distance(pt, p))

p.apply_async(add, (3, 4), callback=lambda result: output_result(result, log))

serv = TCPServer(('', 15000),
                 lambda *args, **kwargs: EchoHandler(*args,
                                                     ack=b'RECEIVED:',
                                                     **kwargs))


# 7.9 Replacing Single Method Classes with Functions

from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo.

yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM, AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

# The class could be replaced by a simpler function.

def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# Example use.

yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))


# 7.10 Carrying Extra State with Callback Functions

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)

def print_result(result):
    print('Got:', result)

def add(x, y):
    return x + y

print(apply_async(add, (2, 3), callback=print_result))
print(apply_async(add, ('hello', 'world'), callback=print_result))

# Use a bound-method instead of a simple function.

class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()

print(apply_async(add, (2, 3), callback=r.handler))
print(apply_async(add, ('hello', 'world'), callback=r.handler))

# You can also use a closure to capture state.

def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

handler = make_handler()

print(apply_async(add, (2, 3), callback=handler))
print(apply_async(add, ('hello', 'world'), callback=handler))

# Using a coroutine to do the same thing.

def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

handler = make_handler()
next(handler)

print(apply_async(add, (2, 3), callback=handler.send))
print(apply_async(add, ('hello', 'world'), callback=handler.send))

'''Carrying state int a callback using an extra argument &
partial function application'''

class SequenceNo:
    def __init__(self):
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got: {}'.format(seq.sequence, result))

seq = SequenceNo()
from functools import partial

print(apply_async(add, (2, 3), callback=partial(handler, seq=seq)))
print(apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq)))

# Example using a lambda.

print(apply_async(add, (2, 3), callback=lambda r: handler(r, seq)))


# 7.11 Inlining Callback Functions

def apply_async(func, args, *, callback):
    result = func(*args)

    callback(result)

from queue import Queue
from functools import wraps

class Asnyc:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def inlined_async(func):
        @wraps(func)
        def wrapper(*args):
            f = func(*args)
            result_queue = Queue()
            result_queue.put(None)
            while True:
                result = result_queue.get()
                try:
                    a = f.send(result)
                    apply_async(a.func, a.args, callback=result_queue.put)
                except StopIteration:
                    break
            return wrapper

# Now to inline the callback steps using yield statements.

    def add(x, y):
        return x + y

    @inlined_async
    def test():
        r = yield Asnyc(add, (2, 3))
        print(r)
        r = yield Async(add, ('hello', 'world'))
        print(r)
        for n in range(10):
            r = yield Asnyc(add, (n, n))
            print(r)
        print('Goodbye')

'''Using multiprocessing library & have async operations executed
in separate processes'''

if __name__ == '__main__':

import multiprocessing
pool = multiprocessing.Pool()
apply_async = pool.apply_async

test()


# 7.12 Accessing Variables Defined Inside a Closure

def sample():
    n = 0
    def func():
        print('n=', n)

    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func

f = sample()

print(f())

f.set_n(10)

print(f())
print(f.get_n())

# Closures emulating instances of a class.

import sys

class ClosureInstance:
    def __init__(self, locals=None):
        if locals is None:
            locals = sys._getframe(1).f_locals

        self.__dict__.update((key,value) for key, value in locals.items()
                            if callable(value))

    def __len__(self):
        return self.__dict__['__len__']()

def Stack():
    items = []

    def push(item):
        items.append(item)

    def pop():
        return items.pop()

    def __len__():
        return len(items)

    return ClosureInstance()

s = Stack()

print(s)

s.push(10)
s.push(20)
s.push('Hello')

print(len(s))
print(s.pop())
print(s.pop())
print(s.pop())

# Test the performance against a class like:

class Stack2:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)

from timeit import timeit

s = Stack()

print(timeit('s.push(1);s.pop()', 'from __main__ import s'))

s = Stack2()

print(timeit('s.push(1);s.pop()', 'from __main__ import s'))

'''The closure version runs 8% faster because there is no
extra self variable involved'''




