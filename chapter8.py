# Python3.7.4
# Chapter 8.


# 8.1 Changing the String Representation of Instances

class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

p = Pair(3, 4)

print(p)  # __str__() output

p = Pair(3, 4)

print('p is {0!r}'.format(p))
print('p is {0}'.format(p))

f = open('file.dat')

print(f)

# An alternative way to write the implementation of __repr__:

def __repr__(self):
    return 'Pair(%r, %r)' % (self.x, self.y)


# 8.2 Customizing String Formatting

_formats = {
        'ymd' : '{d.year}-{d.month}-{d.day}',
        'mdy' : '{d.month}/{d.day}/{d.year}',
        'dmy' : '{d.day}/{d.month}/{d.year}'
        }

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

d = Date(2012, 12, 21)

print(format(d))
print(format(d, 'mdy'))
print('The date is {:ymd}'.format(d))
print('The date is {:mdy}'.format(d))

from datetime import date

d = date(2019, 12, 21)

print(format(d))
print(format(d, '%A, %B %d, %Y'))
print('The end is {:%d %b %Y}. Goodbye'.format(d))


# 8.3 Making Objects Support the Context-Management Protocol

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None

from functools import partial

conn = LazyConnection(('www.python.org', 80))
# Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))

'''A different implementation to allow more than one
socket connection at a time'''

from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()
    
# Example use.

from functools import partial

conn = LazyConnection(('www.python.org', 80))
with conn as s1:
    with conn as s2:


# 8.4 Saving Memory When Creating a Large Number of Instances

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    
# 8.5 Encapsulationg Names in a Class

class A:
    def __init__(self):
        self._internal = 0  # An internal attribute
        self.public = 1     # A public attribute

    def public_method(self):     # A public method

    def _internal_method(self):  # An Internal method

# You may also encounter the use of two leading underscores(__)

class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):

    def public_method(self):
        self.__private_method()

# Using two underscores can't be overrriden with inheritance.

class C(B):
    
    def __init__(self):
        super().__init__()
        self.__private = 1    # Doesn't override B.__private
    def __private_method(self):

'''Use one underscore usually, a double underscore involving
subclassing'''

'''Sometimes you want to have a trailing underscore so it
doesn't clash with a reserved word'''

# 8.6 Creating Managed Attributes

class Person:

    def __init__(self, first_name):
        self.set_first_name(first_name)

    # Getter function
    def get_first_name(self):
        return self._first_name

    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

a = Person('Guido')

# Make a property from existing get/set methods
name = property(get_first_name, set_first_name, del_first_name)

# Properties can also be a away to define computed attributes.

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius

c = Circle(4.0)

print(c.radius)
print(c.area)
print(c.perimeter)

# Directly using getter/setter functions.

p = Person('Guido')

print(p._first_name)
print(p.set_first_name('Larry'))


# 8.7 Calling a Method on a Parent Class

class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()

'''Handling the __init__() method to make sure parents are
properly initialized'''


class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

'''Another common use of super() in in code that overrides
any of Python's special methods'''

class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            setattr(self._obj, name, value)

# Using super() method so __init__() method gets called once.

class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')

c = C()

'''The MRO(Method Resolution Order) list is a linear ordering
of all the base classes'''

print(C.__mro__)

'''Super() doesn't go to the direct parent of a class next in
the MRO & you can use it in a class with no direct parent'''

class A:
    def spam(self):
        print('A.spam')
        super().spam()

class B:
    def spam(self):
        print('B.spam')
        
class C(A,B):
    pass

c = C()

print(c.spam)
print(C.__mro__)


# 8.8 Extending a Property in a Subclass

class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


'''Example of a class inheriting from Person & extends
name property with new functionality'''

class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson('Guido')

print(s.name)

s.name = 'Larry'

# If you only want to extend onf of the methods of a property:

class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name

# Or alternatively, just for the setter.

class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

# Another example if you want to redefine one of the methods.

class SubPerson(Person):
    def name(self):
        print('Getting name')
        return super().name

s = SubPerson('Guido')

print(s.name)

s.name = 'Larry'

print(s.name)

# Extending a descriptor

class String:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        instance.__dict__[self.name] = value

    # A class with a descriptor
class Person:
    name = String('name')
    def __init__(self, name):
        self.name = name

    # Extending a descriptor with a property
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)


# 8.9 Creating a New Kind of Class or Instance Attribute

# Descriptor attribute for an integer type-checked attribute.

class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)

print(p.x)

p.y = 5

print(Point.x)

# A more advanced descriptor involving a class decorator.

# Descriptor for a type-checked attribute.

class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected ' + str(self.expected_type))
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

# Class decorator that applies it to selected attributes
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class.
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

# Example use.
@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

if __name__ == '__main__':
    s = Stock('ACME', 100, 490.1)
    print(s.name, s.shares, s.price)
    s.shares = 50
    try:
        s.shares = 'a lot'
    except TypeError as e:
        print(e)


# 8.10 Using Lazily Computed Properties

class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
        
# Now to utilize that code:

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

c = Circle(4.0)

print(c.radius)
print(c.area)
print(c.area)
print(c.perimeter)
print(c.perimeter)

'''Note that "Computing area" & "Computing perimeter" onky appear once'''

c = Circle(4.0)

# Get instance variables.

print(vars(c))

# Compute area & observe variables afterward.

print(c.area)
print(vars(c))

'''Delete the variable & see property trigger again. The computed value
becomes mutable after it's created'''

del c.area

print(vars(c))
print(c.area)

print(c.area)

c.area = 25

print(c.area)

# A slightly less efficient implentation.

def lazyproperpty(func):
    name = '_lazy_' + func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
        return lazy

# If you use above version, set operations are not allowed.

c = Circle(4.0)

print(c.area)
print(c.area)

# c.area = 25  Not able to set attribute.


# 8.11 Simplifying the Initialization of Data Structures

class Structure:
    # Class variable that specifies expected fields
        _fields = []
        def __init__(self, *args):
            if len(args) != len(self._fields):
                raise TypeError('Expected {} arguments'.format(len(self._fields)))

            # Set the arguments
            for name, value in zip(self._fields, args):
                setattr(self, name, value)

# Example class definitions
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    class Point(Structure):
        _fields = ['x', 'y']

    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2

s = Stock('ACME', 50, 91.1)
p = Point(2, 3)
c = Circle(4.5)

# Several design options to support keyword arguments.

class Structure:
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))

        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid arguments(s): {}'.format(','.join(kwargs)))

# Example use
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, price=91.1)
    s3 = Stock('ACME', shares=50, price=91.1)

'''Use keyword arguments as a means for adding additional attributes
to the structure not specified in _fields'''

class Structure:
    #Class variable that specifies expected fields
    _fields = []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))

# Example use
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

s1 = Stock('ACME', 50, 91.1)
s2 = Stock('ACME', 50, 91.1, date='8/2/2019')

# Example of a "frame hack" to initialize instance variables.

def init_fromlocals(self):
    import sys
    locs = sys._getframe(1).f_locals
    for k, v in locs.items():
        if k != 'self':
            setattr(self, k, v)

class Stock:
    def __init__(self, name, shares, price):
        init_fromlocals(self)
        
        
# 8.12 Defining an Interface or Abstract Base Class

from abc import ABCMeta, abstractmethod

class Istream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass
    @abstractmethod
    def write(self, data):
        pass

class SocketStream(IStream):
    def read(self, maxbytes=-1):
    
    def write(self, data):

def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')

import io

# Register the built-in I/) classes as supporting our interface

IStream.register(io.IOBase)

# Open a normal file & type check

f = open('foo.txt')
isinstance(f, IStream)

from abc import ABCMeta, abstractmethod

class A(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @classmethod
    @abstractmethod
    def method(cls):
        pass

    @staticmethod
    @abstractmethod
    def method2():
        pass

import collections

# Check if x is a sequence.
if isinstance(x, collections.Sequence):

# Check if x is iterable.
if isinstance(x, collections.Iterable):

# Check if x has a size.
if isinstance(x, collections.Sized):

# Check if x is a mapping.
if isinstance(x, collections.Mapping):

from decimal import Decimal
import numbers

x = Decimal('3.4')
isinstance(x, numbers.Real)  # Returns False


# 8.13 Implementing a Data Model or Type System

class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        self.__dict__.update(opts)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

def Typed(expected_type, cls=None):
    if cls is None:
        return lambda cls: Typed(expected_type, cls)

    super_set = cls.__set__
    def __set__(self, instance, value):
        if not isinstance(value, expected_type):
            raise TypeError('expected ' + str(expected_type))
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

def Unsigned(cls):
    super_set = cls.__set__
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

def MaxSized(cls):
    super_init = cls.__init__
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        self.size = opts['size']
        super_init(self, name, **opts)
    cls.__init__ = __init__

    super_set = cls.__set__
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instance, value)
    cls.__set__ = __set__
    return cls

@Typed(int)
class Integer(Descriptor):
    pass

@Unsigned
class UnsignedInteger(Integer):
    pass

@Typed(float)
class Float(Descriptor):
    pass

@Unsigned
class UnsignedFloat(Float):
    pass

@Typed(str)
class String(Descriptor):
    pass

@MaxSized
class SizedString(String):
    pass

# Class decorator to apply constraints
def check_attributes(**kwargs):
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate

# A metaclass that applies checking
class checkedmeta(type):
    def __new__(cls, clsname, bases, methods):
        # Attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, methods)

# Testing code
def test(s):
    print(s.name)
    s.shares = 75
    print(s.shares)
    try:
        s.shares = -10
    except ValueError as e:
        print(e)
    try:
        s.price = 'a lot'
    except TypeError as e:
        print(e)

    try:
        s.name = 'ABRACADABRA'
    except ValueError as e:
        print(e)

# Various Examples:
if __name__ == '__main__':
    print("# --- Class with descriptors")
    class Stock:
        # Specify constraints
        name = SizedString('name', size=8)
        shares = UnsignedInteger('shares')
        price = UnsignedFloat('price')
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

    s = Stock('ACME',50,91.1)
    test(s)

    print("# --- Class with class decorator")
    @check_attributes(name=SizedString(size=8), 
                      shares=UnsignedInteger,
                      price=UnsignedFloat)
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

    s = Stock('ACME',50,91.1)
    test(s)

    print("# --- Class with metaclass")
    class Stock(metaclass=checkedmeta):
        name   = SizedString(size=8)
        shares = UnsignedInteger()
        price  = UnsignedFloat()
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

    s = Stock('ACME',50,91.1)
    test(s)


# 8.14 Implementing Custom Containers

import collections.abc
import bisect

class SortedItems(collections.Sequence):
    def __init__(self, initial=None):
        self._items = sorted(initial) if initial is not None else []

    # Required sequence methods
    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    # Method for adding an item in the right location
    def add(self, item):
        bisect.insort(self._items, item)

if __name__ == '__main__':
    
    items = SortedItems([5, 1, 3])
    
    print(list(items))
    print(items[0])
    print(items[-1])
    
    items.add(2)
    
    print(list(items))
    
    items.add(-10)
    
    print(list(items))
    print(items[1:4])
    print(3 in items)
    print(len(items))

    for n in items:
        print(n)

# Example 2.

items = SortedItems()

import collections

print(isinstance(items, collections.Iterable))
print(isinstance(items, collections.Sequence))
print(isinstance(items, collections.Container))
print(isinstance(items, collections.Sized))
print(isinstance(items, collections.Mapping))

# Suppose you have a class that inherits from collections.MutableSequence:

class Items(collections.MutableSequence):
    def __init__(self, initial=None):
        self._items = list(initial) if initial is not None else []

    # Required sequence methods.
    def __getitem__(self, index):
        print('Getting:', index)
        return self._items[index]

    def __setitem__(self, index, value):
        print('Setting:', index, value)
        self._items[index] = value

    def __delitem__(self, index):
        print('Deleting:', index)
        del self._items[index]

    def insert(self, index, value):
        print('Inserting:', index, value)
        self._items.insert(index, value)

    def __len__(self):
        print('Len')
        return len(self._items)

a = Items([1, 2, 3])

print(len(a))
print(a.append(4))
print(a.append(2))
print(a.count(2))
print(a.remove(3))


# 8.15 Delegating Attribute Access

class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
        # Delegate to the internal self._a instance.
        return self._a.spam(x)

    def foo(self):
        # Delegate to the internal self._a instance.
        return self._a.foo()

    def bar(self):
        pass

# If you have many methods to delegate use this alternative approach.

class A:
    def spam(self, x):
        pass

    def foo(self):
        pass

    class B:
        def __init__(self):
            self._a = A()

        def bar(self):
            pass

        # Expose all of the methods defined on class A.
        def __getattr__(self, name):
            return getattr(self._a, name)

b = B()
b.bar()
b.spam(42)

# Another example of delegation is in the implementation of proxies.

'''A proxy class that wraps around another object, but
exposes its public attributes'''

class Proxy:
    def __init__(self, obj):
        self._obj = obj

    # Delegate attribute lookup to internal obj
    def __getattr__(self, name):
        print('getattr:', name)
        return getattr(self._obj, name)

    # Delegate attribute assignment
    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr:', name, value)
            setattr(self._obj, name, value)

    # Delegate attribute deletion
    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._obj, name)

# To use that proxy class, you wrap it around another instance.

class Spam:
    def __init__(self, x):
        self.x = x
    def bar(self, y):
        print('Spam.bar:', self.x, y)

# Create an instance.

s = Spam(2)

# Create a proxy around it.

p = Proxy(s)

# Access the proxy.

print(p.x)
print(p.bar(3))
p.x = 37

# Example of a solution involving delegation.

class A:
    def spam(self, x):
        print('A.spam', x)

    def foo(self):
        print('A.foo')

class B:
    def __init__(self):
        self._a = A()

    def spam(self, x):
        print('B.spam', x)
        self._a.spam(x)

    def bar(self):
        print('B.bar')

    def __getattr__(self, name):
        return getattr(self._a, name)

# Example manually delegating associated special methods.

class ListLike:
    def __init__(self):
        self._items = []
    def __getattr__(self, name):
        return getattr(self._items, name)

    # Added special methods to support certain list operations.
    def __len__(self):
        return len(self._items)
    def __getitem__(self, index):
        return self._items[index]
    def __setitem__(self, index, value):
        self._items[index] = value
    def __delitem__(self, index):
        del self._items[index]


# 8.16 Defining More Than One Constructor in a Class

import time

class Date:
    #Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternative constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

a = Date(2019, 8, 2)
b = Date.today()

# Example with inheritance.

class NewDate(Date):
    pass

c = Date.today()
d = NewDate.today()

# Using __init__() method to allow for different calling conventions.

class Date:
    def __init__(self, *args):
        if len(args) == 0:
            t = time.localtime()
            args = (t.tm_year, t.tm_mon, t.tm_mday)
        self.year, self.month, self.day = args

a = Date(2019, 8, 2)  # Clear. A specific date.


# 8.17 Creating an Instance Without Invoking __init__()

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

d = Date.__new__(Date)

# Now to set the appropriate instance variables.

data = {
    'year': 2019,
    'month':8,
    'day':2
    }

for key, value in data.items():
    setattr(d, key, value)

print(d.year)
print(d.month)

# Example of an alternate constructor.

from time import localtime

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def today(cls):
        d = cls.__new__(cls)
        t = localtime()
        d.year = t.tm_year
        d.month = t.tm_mon
        d.day = t.tm_mday
        return d
    
    
# 8.18 Extending Classes with Mixins

class LoggedMappingMixin:
    __slots__ = ()

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)

class SetOnceMappingMixin:
    __slots__ = ()
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)

class StringKeysMappingMixin:
    __slots__ = ()
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings!')
        return super().__setitem__(key, value)


# 8.19 Implementing Stateful Objects or State Machines

class Connection:
    def __init__(self):
        self.state = 'CLOSED'

    def read(self):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('reading')

    def write(self, date):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('writing')

    def open(self):
        if self.state == 'OPEN':
            raise RuntimeError('Already open')
        self.state = 'OPEN'

    def close(self):
        if self.state == 'CLOSED':
            raise RuntimeError('Already closed')
        self.state  = 'CLOSED'

# A more elegant approach:

class Connection:
    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate

    # Delegate to the state class
    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)

# Connection state base class.

class ConnectionState:

    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()

# Implementation of different states

class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

c = Connection()

print(c._state)

c.open()

print(c._state)

c.read()
c.write('hello')
c.close()

print(c._state)

# Another example:

class Connection:
    def __init__(self):
        self.new_state(ClosedConnection)

    def new_state(self, newstate):
        self.__class__ = newstate

    def read(self):
        raise NotImplementedError()

    def write(self, data):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

class ClosedConnection(Connection):
    def read(self):
        raise RuntimeError('Not open')

    def write(self, data):
        raise RuntimeError('Not open')

    def open(self):
        self.new_state(OpenConnection)

    def close(self):
        raise RuntimeError('Already closed')

class OpenConnection(Connection):
    def read(self):
        print('reading')

    def write(self, data):
        print('writing')

    def open(self):
        raise RuntimeError('Already open')

    def close(self):
        self.new_state(ClosedConnection)

c = Connection()
c
c.open()

print(c)
print(c.read())
c.close()
print(c)

# Example with large if-elif-else blocks.

# Original implementation

class State:
    def __init__(self):
        self.state = 'A'
    def action(self, x):
        if state == 'A':
            state = 'B'

        elif state == 'B':
            state = 'C'

        elif state == 'C':
            state = 'A'

# Alternative implementation

class State:
    def __init__(self):
        self.new_state(State_A)

    def new_state(self, state):
        self.__class__ = state

    def action(self, x):
        raise NotImplementedError()

class State_A(State):
    def action(self, x):
        self.new_state(State_B)

class State_B(State):
    def action(self, x):
        self.new_state(State_C)

class State_C(State):
    def action(self, x):
        self.new_state(State_A)


# 8.20 Calling a Method on an Object Given the Name As a String

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)

p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)

# Alternative using operator.methodcaller()

import operator

operator.methodcaller('distance', 0, 0)(p)

points = [
    Point(1, 2),
    Point(3, 0),
    Point(10, -3),
    Point(-5, -7),
    Point(-1, 8),
    Point(3, 2)
]

# Sort by distance from origin (0, 0)

points.sort(key=operator.methodcaller('distance', 0, 0))
print(points)

# Provide the appropriate self argument.

p = Point(3, 4)
d = operator.methodcaller('distance', 0, 0)

print(d(p))


# 8.21 Implementing the Visitor Pattern

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

# Representation of 1 + 2 * (3 - 4) / 5

t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)

class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand

e = Evaluator()

print(e.visit(t4))

'''Example of a class that translates an expression into operations
on a stack machine'''

class StackCode(NodeVisitor):
    def generate_code(self, node):
        self.instructions = []
        self.visit(node)
        return self.instructions

    def visit_Number(self, node):
        self.instructions.append(('PUSH', node.value))

    def binop(self, node, instruction):
        self.visit(node.left)
        self.visit(node.right)
        self.instructions.append((instruction,))

    def visit_Add(self, node):
        self.binop(node, 'ADD')

    def visit_Sub(self, node):
        self.binop(node, 'SUB')

    def visit_Mul(self, node):
        self.binop(node, 'MUL')

    def visit_Div(self, node):
        self.binop(node, 'DIV')

    def unaryop(self, node, instruction):
        self.visit(node.operand)
        self.instructions.append((instruction,))

    def visit_Negate(self, node):
        self.unaryop(node, 'NEG')

s = StackCode()
print(s.generate_code(t4))

# Example if you were to write an HTTP framework.

class HTTPHandler:
    def handle(self, request):
        methname = 'do_' + request.request_method
        getattr(self, methname)(request)

    def do_GET(self, request):
        pass
    
    def do_POST(self, request):
        pass
    
    def do_HEAD(self, request):
        pass


# 8.22 Implementing the Visitor Pattern Without Recursion

import types

class Node:
    pass

class Visit:
    def __init__(self, node):
        self.node = node

class NodeVisitor:
    def visit(self, node):
        stack = [ Visit(node) ]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last, Visit):
                    stack.append(self._visit(stack.pop().node))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()
        return last_result

    def _visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)
    
    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        yield (yield Visit(node.left)) + (yield Visit(node.right))

    def visit_Sub(self, node):
        yield (yield Visit(node.left)) - (yield Visit(node.right))

    def visit_Mul(self, node):
        yield (yield Visit(node.left)) * (yield Visit(node.right))

    def visit_Div(self, node):
        yield (yield Visit(node.left)) / (yield Visit(node.right))

    def visit_Negate(self, node):
        yield -(yield Visit(node.operand))
    
if __name__ == '__main__':
    # 1 + 2*(3-4) / 5
    t1 = Sub(Number(3), Number(4))
    t2 = Mul(Number(2), t1)
    t3 = Div(t2, Number(5))
    t4 = Add(Number(1), t3)

    # Evaluate it
    e = Evaluator()
    print(e.visit(t4))     


# 8.23 Managing Memory in Cyclic Data Structures

import weakref

class Node:
    def __init__(self, value):
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node({!r:})'.format(self.value)

    # Property that manages the parent as a weak-reference.
    @property
    def parent(self):
        return self._parent if self._parent is None else self._parent()

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

root = Node('parent')
c1 = Node('child')
root.add_child(c1)

print(c1.parent)

del root

print(c1.parent)

# Another example & the usual rules of how garbage collection don't apply.

# Class just to illustrate when deletion occurs.

class Data:
    def __del__(self):
        print('Data.__del__')

# Node class involving a cycle.

class Node:
    def __init__(self):
        self.data = Data()
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

a = Data()
del a
a = Node()
del a
a = Node()
a.add_child(Node())
del a

# Forcing garbage collection.

import gc

gc.collect()

# Example of weak references eliminating reference cycles.

import weakref

a = Node()
a_ref = weakref.ref(a)

print(a_ref)

print(a_ref())

del a

print(a_ref())


# 8.24 Making Classes Support Comparison Operations

from functools import total_ordering

class Room:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.square_feet = self.length * self.width

@total_ordering
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = list()

    @property
    def living_space_footage(self):
        return sum(r.square_feet for r in self.rooms)

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(self.name,
                                              self.living_space_footage,
                                              self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage

# Build a few houses, and add rooms to them.

h1 = House('h1', 'Cape')
h1.add_room(Room('Master Bedroom', 14, 21))
h1.add_room(Room('Living Room', 18, 20))
h1.add_room(Room('Kitchen', 12, 16))
h1.add_room(Room('Office', 12, 12))
h2 = House('h2', 'Ranch')
h2.add_room(Room('Master Bedroom', 14, 21))
h2.add_room(Room('Living Room', 18, 20))
h2.add_room(Room('Kitchen', 12, 16))
h3 = House('h3', 'Split')
h3.add_room(Room('Master Bedroom', 14, 21))
h3.add_room(Room('Living Room', 18, 20))
h3.add_room(Room('Office', 12, 16))
h3.add_room(Room('Kitchen', 15, 17))
houses = [h1, h2, h3]

print('Is h1 bigger than h2?', h1 > h2) 
print('Is h2 smaller than h3?', h2 < h3) 
print('Is h2 greater than or equal to h1?', h2 >= h1) 
print('Which one is biggest?', max(houses))
print('Which is smallest?', min(houses))


# 8.25 Creating Cached Instances

import logging

a = logging.getLogger('foo')
b = logging.getLogger('bar')

print(a is b)

c = logging.getLogger('foo')

print(a is c)

# Use a factory function to implement that behavior.

class Spam:
    def __init__(self, name):
        self.name = name

# Caching support

import weakref

_spam_cache = weakref.WeakValueDictionary()

def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s

a = get_spam('foo')
b = get_spam('bar')

print(a is b)

c = get_spam('foo')

print(a is c)

a = get_spam('foo')
b = get_spam('bar')
c = get_spam('foo')

print(list(_spam_cache))

del a
del c

print(list(_spam_cache))

del b

print(list(_spam_cache))

'''Putting the caching code into a separate manager class &
gluing things together'''

import weakref

class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
    def get_spam(self, name):
        if name not in self._cache:
            s = Spam(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

    def clear(self):
        self._cache.clear()

class Spam:
    manager = CachedSpamManager()

    def __init__(self, name):
        self.name = name

    def get_spam(name):
        return Spam.manager.get_spam(name)

a = Spam('foo')
b = Spam('foo')

print(a is b)

# Using __init__() to give hint to users not to instantiate Spam.

class Spam:
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Can't instantiate directly")

    # Alternative constructor
    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name

import weakref

class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
    def get_spam(self, name):
        if name not in self._cache:
            s = Spam._new(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s
