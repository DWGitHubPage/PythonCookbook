# Python3.7.4
# Chapter 9.


# 9.1 Putting a Wrapper Around a Function

import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    while n > 0:
        n -= 1

print(countdown(100000))
print(countdown(10000000))

# With these next two examples, they are equivalent.

class A:
    @classmethod
    def method(cls):
        pass

class B:
    def method(cls):
        pass
    method = classmethod(method)


# 9.2 Preserving Function Metadata When Writing Decorators

import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n:int):
    while n > 0:
        n -= 1



print(countdown(100000))
print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)

# How to access the wrapped function directly.

print(countdown.__wrapped__(1000000))

# The underlying signature of the wrapped function.

from inspect import signature

print(signature(countdown))


# 9.3 Unwrapping a Decorator

from functools import wraps

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 1')
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 2')
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def add(x, y):
    return x + y

print(add(2, 3))
print(add.__wrapped__(2, 3))


# 9.4 Defining a Decorator That Takes Arguments

from functools import wraps
import logging

def logged(level, name=None, message=None):
    '''If name & message aren't specified, they default
    to the function's module & name'''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

# If you have code like this:

@decorator(x, y, z)
    def func(a, b):
        pass

# The decoration process evaluates as follows:

def func(a, b):
    pass

func = decorator(x, y, z)(func)


# 9.5 Defining a Decorator with User Adjustable Attributes

from functools import wraps, partial
import logging

# Utility decorator to attach a function as an attribute of obj.

def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate

# Example use:

@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

# Various attributes being changed after definition.

import logging

logging.basicConfig(level=logging.DEBUG)

print(add(2, 3))

# Change the log message.

add.set_message('Add called')

print(add(2, 3))

# Change the log level.

add.set_level(logging.WARNING)

print(add(2, 3))

# Example adding another decorator.

import time

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return r
    return wrapper

@timethis
@logged(logging.DEBUG)
def countdown(n):
    while n > 0:
        n -= 1

# Accessor methods still work:

print(countdown(10000000))

countdown.set_level(logging.WARNING)
countdown.set_message("Counting down to zero")

print(countdown(1000000))

# Still works if decorators are in opposite order:

@logged(logging.DEBUG)
@timethis
def countdown(n):
    while n > 0:
        n -= 1

print(countdown(10000000))

# Accessor functions to return the value of various settings.

@attach_wrapper(wrapper)
def get_level():
    return level

# Alternative.

wrapper.get_level = lambda: level

'''Alternative formulation based on direct access to
function attributes'''

@wraps(func)
def wrapper(*args, **kwargs):
    wrapper.log.log(wrapper.level, wrapper.logmsg)
    return func(*args, **kwargs)

# Attach adjustable attributes
wrapper.level = level
wrapper.logmsg = logmsg
wrapper.log = log


# 9.6 Defining a Decorator That Takes an Optional Argument

from functools import wraps, partial
import logging

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)
    return wrapper

# Example use.

@logged
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')

# A  decorator where all arguments are optional could also be applied.

@logged()
def add(x, y):
    return x+y

# This is how the calling sequence would be of code above:

def add(x, y):
    return x + y
add = logged(add)

@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')

# The calling sequence of code above is as follows:

def spam():
    print('Spam!')
spam = logged(level=logging.CRITICAL, name='example')(spam)


# 9.7 Enforcing Type Checking on a Function Using a Decorator

def typeassert(x, y):
    pass

typeassert(int, int)
def add(x, y):
    return x + y

print(add(2, 3))

# An implementation of the @typeassert decorator.

from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

    # Map function argument names to supllied types.
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supllied arguments.
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must {}'.format(name, bound_types[name])
                            )
            return func(*args, **kwargs)
        return wrapper
    return decorate

@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)

print(spam(1, 2, 3))

def decorate(func):
    # If in optimized mode, disable type checking
    if not __debug__:
        return func

# Extracing signature info. from a callable.

from inspect import signature

def spam(x, y, z=42):
    pass

sig = signature(spam)

print(sig)
print(sig.parameters)
print(sig.parameters['z'].name)
print(sig.parameters['z'].default)
print(sig.parameters['z'].kind)

# An example of what happens when using the bind_partial() method.

bound_types = sig.bind_partial(int, z=int)

print(bound_types)
print(bound_types.arguments)

'''Example with sig.bind() method & how unlike bind_partial(),
it does not allow for missing arguments'''

bound_values = sig.bind(1, 2, 3)

print(bound_values.arguments)

for name, value in bound_values.arguments.items():
    if name in bound_types.arguments:
        if not isinstance(value, bound_types.arguments[name]):
            raise TypeError()

'''Following code works even though default value of items is
of the "wrong" type'''

@typeassert(int, list)
def bar(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items

print(bar(2))


# 9.8 Defining Decorators As Part of a Class

from functools import wraps

class A:
    # Decorator as an instance method
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)
        return wrapper

    # Decorator as a class method
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)
        return wrapper

# As an instance method.
a = A()

@a.decorator1
def spam():
    pass

# As a class method
@A.decorator2
def grok():
    pass

# Example of decorators in a class in the standar library.

class Person:
    # Create a property instance
    first_name = property()

    # Apply decorator methdods
    @first_name.getter
    def first_name(self):
        return self._first_names

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

# Example of potential use with inheritance.

class B(A):
    @A.decorator2
    def bar(self):
        pass

# Defining Decorators As Classes

import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

@Profiled
def add(x, y):
    return x + y

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)

print(add(2, 3))
print(add(4, 5))
print(add.ncalls)

s = Spam()

print(s.bar(1))
print(s.bar(2))
print(s.bar(3))

# Example showing underlying mechanics.

s = Spam()
def grok(self, x):
    pass

print(grok.__get__(s, Spam))

'''Example alternative formulation of the decorator
using closures & nonlocal variables'''

import types
from functools import wraps

def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)
    wrapper.ncalls = lambda: ncalls
    return wrapper

# Example
@profiled
def add(x, y):
    return x + y

print(add(2, 3))
print(add(4, 5))
print(add.ncalls())


# 9.10 Applying Decorators to Class & Static Methods

import time
from functools import wraps

# Simple decorator.

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return r
    return wrapper

'''Class illustrating application of the
decorator to different kinds of methods'''

class Spam:
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1

s = Spam()

print(s.instance_method(1000000))
print(Spam.class_method(1000000))
print(Spam.static_method(100000))

'''If you get the order of decorators wrong,
you'll get an error'''

# If you want to define an abstract class method, use this code:

from abc import ABCMeta, abstractmethod

class A(metaclass=ABCMeta):
    @classmethod
    @abstractmethod

    def method(cls):
        pass


# 9.11 Writing Decorators That Add Arguments to Wrapped Functions

from functools import wraps

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

@optional_debug
def spam(a, b, c):
    print(a, b, c)

print(spam(1, 2, 3))
print(spam(1, 2, 3, debug=True))

# Example of code that can be refactored:

def a(x, debug=False):
    if debug:
        print('Calling a')

def b(x, y, z, debug=False):
    if debug:
        print('Calling b')

def c(x, y, debug=False):
    if debug:
        print('Calling c')

# Refactored:

@optional_debug
def a(x):

    @optional_debug
    def b(x, y, z):

        @optional_debug
        def c(c, y):
            pass

'''So there are no possible name clashes, especially with the
debug argument, add an extra check'''

from functools import wraps
import inspect

def optional_debug(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

# Proper management of function signatures.

@optional_debug
def add(x, y):
    return x + y

import inspect

print(inspect.signature(add))

# Above code can be fixed by making this modification:

from functools import wraps
import inspect

def optional_debu(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter('debug',
                                   inspect.Parameter.KEYWORD_ONLY,
                                   default=False))
    wrapper.__signature__ = sig.replace(parameters=parms)
    return wrapper

@optional_debug
def add(x, y):
    return x + y

print(inspect.signature(add))
print(add(2, 3))


# 9.12 Using Decorators to Patch Class Definitions

def log_getattribute(cls):
    #Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class & return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use.
@log_getattribute
class A:
    def __init__(self, x):
        self.x = x
    def spam(self):
        pass

a = A(42)

print(a.x)
print(a.spam())

# Alternative involving inheritance.

class LoggedGetattribute:
    def __getattribute__(self, name):
        print('getting:', name)
        return super().__getattribute__(name)

# Example:
class A(LoggedGetattribute):
    def __init__(self, x):
        self.x = x
    def spam(self):
        pass


# 9.13 Using a Metaclass to Control Instance Creation

class Spam:
    def __init__(self, name):
        self.name = name

a = Spam('Guido')
b = Spam('Diana')

# Example if you didn't want any instances at all:

class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")

# Example.
class Spam(metaclass=NoInstances):
    @staticmethod
    def grok(x):
        print('Spam.grok')

print(Spam.grok(42))

# Example implementing singleton pattern( where only one class is created).

class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# Example

class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')

a = Spam()
b = Spam()

print(a is b)

c = Spam()

print(a is c)

# Example creating cached instances.

import weakref

class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# Example.

class Spam(metaclass=Cached):
    def __init__(self, name):
        print('Creating Spam({!r})'.format(name))
        self.name = name

# Example showing the behavior of this class:

a = Spam('Guido')
b = Spam('Diana')
c = Spam('Guido')  # Cached

print(a is b)      # False
print(a is c)      # True. Cached value returned

'''Example if you didn't use a metaclass, hiding classes behind
an extra factory function'''

class Spam:
    def __init__(self):
        print('Creating Spam')

_spam_instance = None
def Spam():
    global _spam_instance
    if _spam_instance is not None:
        return _spam_instance
    else:
        _spam_instance = _Spam()
        return _spam_instance


# 9.14 Capturing Class Attribute Definition Order

from collections import OrderedDict

# A set of descriptors for various types.
class Typed:
    _expected_type = type(None)
    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise TypeError('Expected ' + str(self._expected_type))
        instance.__dict__[self._name] = value

class Integer(Typed):
    _expected_type = int

class Float(Typed):
    _expected_type = float

class String(Typed):
    _expected_type = str

# Metaclass that uses an OrderedDict for class body.

class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        order = []
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                order.append(name)
        d['_order'] = order
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return OrderedDict()

# Example to serialize the instance data as a line of CSV data.

class Structure(metaclass=OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self, name)) for name in self._order)

# Example use.

class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('GOOG', 100, 490.1)

print(s.name)
print(s.as_csv())

# Example that rejects duplicate definitions.

from collections import OrderedDict

class NoDupOrderedDict(OrderedDict):
    def __init__(self, clsname):
        self.clsname = clsname
        super().__init__()
    def __setitem__(self, name, value):
        if name in self:
            raise TypeError('{} already in {}'.format(name, self.clsname))
        super().__setitem__(name, value)

class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        d['_order'] = [name for name in clsdict if name [0] != '_']
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(cls, clsname, bases):
        return NoDupOrderedDict(clsname)

class A(metaclass=OrderedMeta):
    def spam(self):
        pass
    # def spam(self): Traceback: TypeError: spam already in A
        # pass

    
# 9.15 Defining a Metaclass That Takes Optional Arguments

from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass

# In custom metaclasses, additional keywords can be supplied:

class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, *, debug=False, synchronize=False):
        return super().__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, *, debug=False, synchronize=False):
        return super().__new__(cls, name, bases, ns)

    # Required
    def __init__(self, name, bases, ns, *, debug=False, synchronize=False):
        super().__init__(name, bases, ns)

class Spam(metaclass=MyMeta, debug=True, synchronize=True):
    pass

'''Example using keyword arguments to configure a metaclass
as an alternative to using class variables'''

class Spam(metaclass=MyMeta):
    debug = True
    synchronize = True


# 9.16 Enforcing an Argument Signature on *args & **kwargs

from inspect import Signature, Parameter

parms = [ Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
          Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=42),
          Parameter('z', Parameter.KEYWORD_ONLY, default=None) ]

sig = Signature(parms)

print(sig)

'''Now that you have a signature object, you can bind it to *args
& **kwargs using the signature's bind() method'''

def func(*args, **kwargs):
    bound_values = sig.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
        print(name, value)

func(1, 2, z=3)
func(1)
func(1, z= 3)
func(y=2, x=1)
# func(1, 2, 3, 4) Can't have more than three positional arguments.

# Example enforcing function signatures.

from inspect import Signature, Parameter

def make_sig(*names):
    parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
             for name in names]
    return Signature(parms)

class Structure:
    __signature__ = make_sig()
    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)

# Example use.

class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')

class Point(Structure):
    __signature__ = make_sig('x', 'y')

# Example of how the Stock class works:

import inspect

print(inspect.signature(Stock))

s1 = Stock('ACME', 100, 490.1)

# Example creating signature objects through a custom metaclass.

from inspect import Signature, Parameter

def make_sig(*names):
    parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
             for name in names]
    return Signature(parms)

class StructureMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsdict['__signature__'] = make_sig(*clsdict.get('_fields', []))
        return super().__new__(cls, clsname, bases, clsdict)

class Structure(metaclass=StructureMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)

# Example.

class Stock(Structure):
    _fields = ['name', 'shares', 'price']

class Point(Structure):
    _fields = ['x', 'y']

'''When defining custom signatures, often, it's useful to store the
signature in a special attribute __signature__. If you do that, the
inspect module will see the sig. & report it as the calling convention'''

import inspect

print(inspect.signature(Stock))
print(inspect.signature(Point))


# 9.17 Enforcing Coding Conventions in Classes

class MyMeta(type):
    def __new__(self, clsname, bases, clsdict):
        '''clsname is name of class being defined.
           bases is tuple of bas classes
           clsdict is class dictionary'''
        return super().__new__(cls, clsname, bases, clsdict)

# Alternatively, if __init__() is defined:

class MyMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)

# To use metaclass, you incorporate it into a top-level base class.

class Root(metaclass=MyMeta):
    pass

class A(Root):
    pass

class B(Root):
    pass

'''Examples of a metaclass that rejects any class definition
containing methods with mixed-case names'''

class NoMixedCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('Bad attribute name: ' + name)
        return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self):  
        pass

'''Example of a metaclass that checks the definition of
redefined methods to make sure they have the same calling
signature as the original method in superclass'''

from inspect import signature
import logging

class MatchSignaturesMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        sup = super(self, self)  # Not a typo, In a metaclass, self is a class object.
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            # Get the previous def. (if any) & compare the signatures.
            prev_dfn = getattr(sup, name, None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:  # If they are equal.
                    logging.warning('Signature mismatch in %s. %s != %s',
                                    value.__qualname__, prev_sig, val_sig)

# Example.

class Root(metaclass=MatchSignaturesMeta):
    pass

class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass

# Class with redefined methods, but slightly different signatures.

class B(A):
    def foo(self, a, b):
        pass

    def spam(self, x, y):
        pass
    

# 9.18 Defining Classes Programmatically

def __init__(self, name, shares, price):
    self.name = name
    self.shares = shares
    self.price = price

def cost(self):
    return self.shares * self.price

cls_dict = {
    '__init__' : __init__,
    'cost' : cost,
    }

import types

Stock = types.new_class('Stock', (), {}, lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__

s = Stock('ACME', 50, 91.1)

print(s)
print(s.cost())

'''If the class you want to create involves a different metaclass,
it would be specified in the third argument to types.new_class()'''

import abc

Stock = types.new_class('Stock', (), {'metaclass': abc.ABCMeta},
                        lambda ns: ns.update(cls_dict))

Stock.__module__ = __name__

print(Stock)
print(type(Stock))

# Example of creating new class object with collections.namedtuple()

import collections

Stock = collections.namedtuple('Stock', ['name', 'shares', 'price'])

print(Stock)

# Example of creating a class directly.

import operator
import types
import sys

def named_tuple(classname, fieldnames):
    # Populate a dictionary of field property accessors
    cls_dict = { name: property(operator.itemgetter(n))
                 for n, name in enumerate(fieldnames) }

    # Make a __new__ function & add to the class dict
    def __new__(cls, *args):
        if len(args) != len(fieldnames):
            raise TypeError('Expected {} arguments'.format(len(fieldnames)))
        return tuple.__new__(cls, args)

    cls_dict['__new__'] = __new__

    # Make the class
    cls = types.new_class(classname, (tuple,), {},
                          lambda ns: ns.update(cls_dict))

    # Set the module to that of the caller
    cls.__module__ = sys._getframe(1).f_globals['__name__']
    return cls

Point = named_tuple('Point', ['x', 'y'])

print(Point)

p = Point(4, 5)

print(len(p))
print(p.x)
print('%s %s' % p)

# Way to create a class using types.prepare_class()

import types

metaclass, kwargs, ns = types.prepare_class('Stock', (), {'metaclass': type})


# 9.19 Initializing Class Members at Definition Time

import operator

class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))

# The above code allows simple tuple-based data structures to be defined.

class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

    class Point(StructTuple):
        _fields = ['x', 'y']

    s = Stock('ACME', 50, 91.1)

    print(s)
    print(s[0])
    print(s.name)
    print(s.shares * s.price)


# 9.20 Implementing Multiple Dispatch with Function Annotations

class Spam:
    def bar(self, x:int, y:int):
        print('Bar 1:', x, y)
    def bar(self, s:str, n:int = 0):
        print('Bar 2:', s, n)

s = Spam()
s.bar(2, 3)
s.bar('hello')

# Combination of metaclasses & descriptors.

import inspect
import types

class MultiMethod:
    def __init__(self, name):
        self._methods = {}
        self.__name__ = name

    def register(self, meth):
        sig = inspect.signature(meth)

        # Build a type signature from the method's annotations
        types = []
        for name, parm in sig.parameters.items():
            if name == 'self':
                continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError(
                    'Argument {} must be annotated with a type'.format(name)
                    )
            if not isinstance(parm.annotation, type):
                raise TypeError(
                    'Argument {} annotation must be a type'.format(name)
                    )
            if parm.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth
            types.append(parm.annotation)

        self._methods[tuple(types)] = meth

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            raise TypeError('No matching method for types {}'.format(types))

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

class MultiDict(dict):
    '''
    Special dictionary to build multimethods in a metaclass
    '''
    def __setitem__(self, key, value):
        if key in self:
            # If key already exists, it must be a multimethod or callable
            current_value = self[key]
            if isinstance(current_value, MultiMethod):
                current_value.register(value)
            else:
                mvalue = MultiMethod(key)
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key, mvalue)
        else:
            super().__setitem__(key, value)

class MultipleMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        return type.__new__(cls, clsname, bases, dict(clsdict))

    @classmethod
    def __prepare__(cls, clsname, bases):
        return MultiDict()

class Spam(metaclass=MultipleMeta):
    def bar(self, x:int, y:int):
        print('Bar 1:', x, y)
    def bar(self, s:str, n:int = 0):
        print('Bar 2:', s, n)

import time

class Date(metaclass=MultipleMeta):
    def __init__(self, year: int, month:int, day:int):
        self.year = year
        self.month = month
        self.day = day

    def __init__(self):
        t = time.localtime()
        self.__init__(t.tm_year, t.tm_mon, t.tm_mday)

s = Spam()
s.bar(2, 3)
s.bar('hello')
s.bar('hello', 5)

d = Date(2019, 8, 5)
e = Date()

print(e.year)
print(e.month)
print(e.day)

b = s.bar

print(b)
print(b.__self__)
print(b.__func__)
print(b(2, 3))
print(b('hello'))

# Example in which we will rewrite the following using decorators.

class multimethod:
    def __init__(self, func):
        self._methods = {}
        self.__name__ = func.__name__
        self._default = func

    def match(self, *types):
        def register(func):
            ndefaults = len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults+1):
                self._methods[types[:len(types) - n]] = func
            return self
        return register

    def __call__(self, *args):
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self, instance)
        else:
            return self

# Now using decorators.

class Spam:
    @multimethod
    def bar(self, *args):
        raise TypeError('No matching method for bar')

    @bar.match(int, int)
    def bar(self, x, y):
        print('Bar 1:', x, y)

    @bar.match(str, int)
    def bar(self, s, n = 0):
        print('Bar 2:', s, n)


# 9.21 Avoiding Repetitive Property Methods

# The repetitive way:

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name must be a string')
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError('age must be an int')
        self._age = value

# A simpler way:

def typed_property(name, expected_type):
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))
        setattr(self, storage_name, value)
    return prop

# Example use.

class Person:
    name = typed_property('name', str)
    age = typed_property('age', int)
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Tweaking the above code with the functools.partial() function.

from functools import partial

String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)

class Person:
    name = String('name')
    age = Integer('age')
    def __init__(self, name, age):
        self.name = name
        self.age = age


# 9.22 Defining Context Managers the Easy Way

import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))

with timethis('counting'):
    n = 10000000
    while n > 0:
        n -= 1

'''A more advanced context manager that implements
a kind of transaction on a list object'''

@contextmanager
def list_transaction(orig_list):
    working = list(orig_list)
    yield working
    orig_list[:] = working

'''The idea with the above code is that changes made to a list only
take effect if an entire code block runs to completion with no exceptions'''

items = [1, 2, 3]
with list_transaction(items) as working:
    working.append(4)
    working.append(5)

print(items)

'''How you would normally write a context manager, defining it
with __enter__() & __exit__() methods'''

import time

class timethis:
    def __init__(self, label):
        self.label = label
    def __enter__(self):
        selfstart = time.time()
    def __exit__(sel, exc_ty, exc_val, exc_tb):
        end = time.time()
        print('{}: {}'.format(self.label, end - self.start))


# 9.23 Executing Code with Local Side Effects

# Execute a fragment of code in the global namespace:

a = 13
exec('b = a + 1')

print(b)

# Now the same experiment inside a function:
def test():
    a = 13
    exec('b = a + 1')
    print(b)
    
# test() NameError: global name 'b' is not defined

'''To fix that problem, you need to use the locals() function to
obtain a dictionary of the local variables prior to the call to exec()'''

def test():
    a = 13
    loc = locals()  # This line is what fixes it.
    exec('b = a + 1')
    b = loc['b']
    print(b)

test()

# Another example.

def test1():
    x = 0
    exec('x += 1')
    print(x)

test1()

# Experiment example to inspect the value of the dictionary after execution.

def test2():
    x = 0
    loc = locals()
    print('before:', loc)
    exec('x += 1')
    print('after:', loc)
    print('x =', x)

test2()

# Another example showing order of operations.

def test3():
    x = 0
    loc = locals()
    print(loc)
    exec('x += 1')
    print(loc)
    locals()
    print(loc)

test3()

# You can also make your own dictionary & pass it to exec().

def test4():
    a = 13
    loc = { 'a' : a }
    glb = { }
    exec('b = a + 1', glb, loc)
    b = loc['b']
    print(b)

test4()


# 9.24 Parsing & Analzying Python Source

x = 42

print(eval('2 + 3*4 + x'))
exec('for i in range(11): print(i)')

# Compile code into an abstract syntax tree(AST) that can be analyzed.

import ast

ex = ast.parse('2 + 3*4 + x', mode='eval')

print(ex)
print(ast.dump(ex))

top = ast.parse('for i in range(10): print(i)', mode='exec')

print(top)
print(ast.dump(top))

'''Example of a class that records info. about which names
are loaded, stored, & deleted'''

import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.loaded = set()
        self.stored = set()
        self.deleted = set()
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.loaded.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.stored.add(node.id)
        elif isinstance(node.ctx, ast.Del):
            self.deleted.add(node.id)

if __name__ == '__main__':
    code = '''
for i in range(11):
    print(i)

del i
'''

    # Parse into an AST
    top = ast.parse(code, mode='exec')

    # Feed the AST to analyze name usage
c = CodeAnalyzer()
c.visit(top)
print('Loaded:', c.loaded)
print('Stored:', c.stored)
print('Deleted:', c.deleted)

# AST's can be compiled & executed using the compile() function.

exec(compile(top, '<stdin>', 'exec'))

'''Example of a decorator that lowers globally accessed names into the
body of a function by reparsing the function body's source code,
rewriting the AST, & recreating the function's code object'''

import ast
import inspect

class NameLower(ast.NodeVisitor):
    def __init__(self, lowered_names):
        self.lowered_names = lowered_names

    def visit_FunctionDef(self, node):
        code = '__globals = globals()\n'
        code += '\n'.join("{0} = __globals['{0}']".format(name)
                          for name in self.lowered_names)

        code_ast = ast.parse(code, mode='exec')

        # Inject new statements into the function body
        node.body[:0] = code_ast.body

        # Save the function object
        self.func = node

# Decorator that turns global names into locals

def lower_names(*namelist):
    def lower(func):
        srclines = inspect.getsource(func).splitlines()
        # Skip source lines prior to the @lower_names decorator
        for n, line in enumerate(srclines):
            if '@lower_names' in line:
                break

        src = '\n'.join(srclines[n+1:])
        # Hack to deal with indented code
        if src.startswith((' ', '\t')):
            src = 'if 1:\n' + src
        top = ast.parse(src, mode='exec')

        # Transform the AST
        cl = NameLower(namelist)
        cl.visit(top)

        # Execute the modified AST
        temp = {}
        exec(compile(top, '', 'exec'), temp, temp)

        # Pull out the modified code object
        func.__code__ = temp[func.__name__].__code__
        return func
    return lower

INCR = 1

@lower_names('INCR')
def countdown1(n):
    while n > 0:
        n -= INCR

def countdown2(n):
    __globals = globals()
    INCR = __globals['INCR']
    while n > 0:
        n -= INCR

# Running a performance check:

if __name__ == '__main__':
    import time
    print('Running a performance check')

    start = time.time()
    countdown1(100000000)
    end = time.time()
    print('countdown1:', end-start)

    start = time.time()
    countdown2(100000000)
    end = time.time()
    print('countdown2:', end-start)


# 9.25 Disassembling Python Byte Code

def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
    print('Blastoff!')

import dis

dis.dis(countdown)

'''The raw byte code interpreted by the dis() function is
available on functions as follows:'''

print(countdown.__code__.co_code)

c = countdown.__code__.co_code

import opcode

opcode.opname[c[0]]

print(opcode.opname[c[0]])
print(opcode.opname[c[3]])

'''Generator function to take raw byte code sequence
& turn it into opcodes & arguments'''

import opcode

def generate_opcodes(codebytes):
    extended_arg = 0
    i = 0
    n = len(codebytes)
    while i < n:
        op = codebytes[i]
        i += 1
        if op >= opcode.HAVE_ARGUMENT:
            oparg = codebytes[i] + codebytes[i+1]*256 + extended_arg
            extended_arg = 0
            i += 2
            if op == opcode.EXTENDED_ARG:
                extended_arg = oparg * 65536
                continue
        else:
            oparg = None
        yield (op, oparg)

for op, oparg in generate_opcodes(countdown.__code__.co_code):
    print(op, opcode.opname[op], oparg)

# You can replace the raw byte code of any function that you want.

def add(x, y):
    return x + y

c = add.__code__

print(c)
print(c.co_code)
