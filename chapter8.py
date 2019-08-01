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
