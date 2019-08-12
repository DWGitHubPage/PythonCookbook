# Python3.7.4
# Chapter 10.


# 10.2 Controlling the Import of Everything

def spam():
    pass

def grok():
    pass

blah = 42

# Only export 'spam' & 'grok'

__all__ = ['spam', 'grok']


# 10.3 Importing Package Submodules Using Relative Names

mypackage/
__init__.py
A/
    __init__.py
    spam.py
    grok.py
B/
    __init__.py
    bar.py

'''If the module mypackage.A.spam wants to import the module grok
located in the same directory, it should include an import
statement like this:'''

from . import grok

'''If the same module wants to import the module B.bar located in a
different directory, it can use an import statement like this:'''

from ..B import bar


'''Imports involving modules in the same package can either use
fully specifiied absolute names or relative imports using the syntax
shown. For example:'''


from mypackage.A import grok  # Ok
from . import grok            # Ok
import grok                   # Error   
from . import grok            # Ok
import .grok                  # Error



# 10.4 Splitting a Module into Multiple Files

# mymodule.py

class A:
    def spam(self):
        print('A.spam')

class B(A):
    def bar(self):
        print('B.bar')

'''Suppose you want to split mymodule.py into two files, one for
each class definition. Replace mymodule.py with a directory called
mymodule & create the following files:'''

mymodule/
    __init__.py
    a.py
    b.py

# In the a.py file put this code:

class A:
    def spam(self):
        print('A.spam')

# In the b.py file, put this code:

from .a import A

class B(A):
    def bar(self):
        print('B.bar')

# Finally, in the __init__.py file, glue the two files together:

from .a import A
from .b import B
    

# And it's easier to put:

from mymodule import A, B

'''Perhaps you only want to load components as they are needed,
to do that, here is a slight variation of __init__.py'''

def A():
    from .a import A
    return A()

def B():
    from .b import B
    return B()

# Classes A & B have been replaced by functions that load the desired classes.

import mymodule

a = mymodule.A()

print(a.spam())

'''A downside of lazy loading is that inheritance & type checking
might break. You might have to change your code slightly'''

if isinstance(x, mymodule.A):   # Error

if isinstance(x, mymodule.a.A): # Ok


# 10.5 Making Separate Directories of Code Import Under a Common Namespace

'''To unify separate directories under a common namespace, you omit
__init__.py files in the directories where the components join together:
'''

foo-package/
    spam/
        blah.py

bar-package/
    spam/
        grok.py


import sys
sys.path.extend(['foo'package', 'bar-package'])

import spam.blah
import spam.grok

'''Now the two different package directories merge together &
you can import either spam.blah or spam.grok'''


#10.6 Reloading Modules

import spam
import importlib

print(imp.reload(spam))

'''reload() doesn't update definitions that have been imported using
statements such as "from module import 'name''''

def bar():
    print('bar')

def grok()"
print('grok')

import spam
from spam import grok

print(spam.bar())
print(grok())

# Without quitting Python, edit source code of spam.py

def grok():
    print('New grok')

# Now go back to interactive session, perform a reload and try:

import importlib

print(imp.reload(spam)
print(spam.bar())
print(grok())
print(spam.grok())

'''It's best not to reload modules in production code, save it for
debugging or interactive sessions'''


# 10.7 Making a Directory or Zip File Runnable As a Main Script
'''
myapplication/
     spam.py
     bar.py
     grok.py
     __main__.py
'''

# If you package all of your code up into a zip file:
'''
 bash % ls
        spam.py    bar.py   grok.py   __main__.py
        bash % zip -r myapp.zip *.py
        bash % python3 myapp.zip
        ... output from __main__.py ...
'''


#10.8 Reading Data Files Within a Package

import pkgutil

data = pkgutil.get_data(__package__, 'somedata.dat')


# 10.9 Adding Directories to sys.path

bash % env PYTHONPATH=/some/dir:/other/dir python3

import sys

sys.path

# Second approach is to create a .pth file that lists directories like:

# myapplication.pth
/some/dir
/other/dir


# Constructing an appropriate absolute path using module-level variables.

import sys

from os.path import abspath, join, dirname

sys.path.insert(0, abspath(dirname('__file__'), 'src'))


#10.10 Importing Modules Using a Name Given in a String

import importlib

math = importlib.import_module('math')

print(math.sin(2))

mod = importlib.import_module('urllib.request')
u = mod.urlopen('http://www.python.org')

'''
import_module() can perform relative imports but you need
to give it an extra argument'''

import importlib

b = importlib.import_module('.b', __package__)


# 10.11 Loading Modules from a Remote Machine Using Import Hooks


# First create the following directory:

testcode/
    spam.py
    fib.py
    grok/
        __init__.py
        blah.py

# Then put some statements & functions in each file.

# spam.py

print("I'm spam")

def hello(name):
    print('Hello %s' % name)

# fib.py

print("I'm fib")

def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# grok/__init__.py

print("I'm grok.__init__")

# grok/blah.py

print("I'm grok.blah")

# Now go to testcode directory & run python like this:

bash % cd testcode
bash % python3 -m http.server 15000

# Leave the server running & start a separate Python interpreter.

from urllib.request import urlopen

u = urlopen('http://localhost:15000/fib.py')
data = u.read().decode('utf-8')

print(data)

# Creating an explicit loading function to load a remote module.

import imp
import urllib.request
import sys

def load_module(url):
    u = urllib.request.urlopen(url)
    source = u.read().decode('utf-8')
    mode = sys.modules.setdefault(url, imp.new_module(url))
    code = compile(source, url, 'exec')
    mod.__file__ = url
    mod.__package__ = ''
    exec(code, mod.__dict__)
    return mod

# Here's how you would use the function.

fib = load_module('http://localhost:15000/fib.py')
fib.fib.(10)

spam = load_module('http://localhost:15000/spam.py')
spam.hello('Guido')

print(fib)
print(spam)

'''Creating a custom importer. The first part is to create
a meta path importer'''

import sys
import importlib.abc
import imp
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

# Debugging
import logging

log = logging.getLogger(__name__)

# Get links from a given URL

def _get_links(url):
    class LinkParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                attrs = dict(attrs)
                links.add(attrs.get('href').rstrip('/'))

    links = set()
    try:
        log.debug('Getting links from %s' % url)
        u = urlopen(url)
        parser = LinkParser()
        parser.feed(u.read().decode('utf-8'))

    except Exception as e:
        log.debug('Could not get links. %s', e)
    log.debug('links: %r', links)
    return links

class UrlMetaFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._links   = {}
        self._loaders = { baseurl : UrlModuleLoader(baseurl) }

    def find_module(self, fullname, path=None):
        log.debug('find_module: fullname=%r, path=%r', fullname, path)
        if path is None:
            baseurl = self._baseurl
        else:
            if not path[0].startswith(self._baseurl):
                return None
            baseurl = path[0]

        parts = fullname.split('.')
        basename = parts[-1]
        log.debug('find_module: baseurl=%r, basename=%r', baseurl, basename)

         # Check link cache
         if basename not in self._links:
             self._links[baseurl] = _get_links(baseurl)

         # Check if it's a package
         if basename in self._links[baseurl]:
             log.debug('find_module: trying package %r', fullname)
             fullurl = self._baseurl + '/' + basename
             # Attempt to load the package (which accesses __init__.py)
             loader = UrlPackageLoader(fullurl)
             try:
                 loader.load_module(fullname)
                 self._links[fullurl] = _get_links(fullurl)
                 self._loaders[fullurl] = UrlModuleLoader(fullurl)
                 log.debug('find_module: package %r loaded', fullname)
             except ImportError as e:
                 log.debug('find_module: package failed. %s', e)
                 loader = None
             return loader

        # A normal module
        filename = basename + '.py'
        if filename in self._links[baseurl]:
            log.debug('find_module: module %r found', fullname)
            return self._loaders[baseurl]
        else:
            log.debug('find_module: module %r not found', fullname)
            return None

    def invalidate_caches(self):
        log.debug('invalidating link cache')
        self._links.clear()

# Module Loader for a Url
class UrlModuleLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._source_cache = {}

    def module_repr(self, module):
        return '<urlmodule %r from %r>' % (module.__name__, module__file__)

    # Required method
    def load_module(self, fullname):
        code = self.get_code(fullname)
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = self.get_filename(fullname)
        mod.__loader__ = delf
        mod.__package__ = fullname.rpartition('.')[0]
        exec(code, mod.__dict__)
        return mod

    # Optional extensions
    def get_code(self, fullname):
        src = self.get_source(fullname)
        return compile(src, self.get_filen
         
    def get_data(self, path):
        pass

    def get_filename(self, fullname):
        return self._baseurl + '/' + fullname.split('.')[-1] + '.py'

    def get_source(self, fullname):
        filename = self.get_filename(fullname)
        log.debug('loader: reading %r', filename)
        if filename in self._source_cache:
            log.debug('loader: cached %r', filename)
            return self._source_cache[filename]
        try:
            u = urlopen(filename)
            source = u.read().decode('utf-8')
            log.debug('loader: %r loaded', filename)
            self._source_cache[filename] = source
            return source
        except (HTTPError, URLError) as e:
            log.debug('loader: %r failed.  %s', filename, e)
            raise ImportError("Can't load %s" % filename)

    def is_package(self, fullname):
        return False

# Package loader for a URL
class UrlPackageLoader(UrlModuleLoader):
    def load_module(self, fullname):
        mod = super().load_module(fullname)
        mod.__path__ = [ self._baseurl ]
        mod.__package__ = fullname

    def get_filename(self, fullname):
        return self._baseurl + '/' + '__init__.py'

    def is_package(self, fullname):
        return True

# Utility functions for installing/uninstalling the loader
_installed_meta_cache = { }
def install_meta(address):
    if address not in _installed_meta_cache:
        finder = UrlMetaFinder(address)
        _installed_meta_cache[address] = finder
        sys.meta_path.append(finder)
        log.debug('%r installed on sys.meta_path', finder)
    
def remove_meta(address):
    if address in _installed_meta_cache:
        finder = _installed_meta_cache.pop(address)
        sys.meta_path.remove(finder)
        log.debug('%r removed from sys.meta_path', finder)

# Path finder class for a URL
class UrlPathFinder(importlib.abc.PathEntryFinder):
    def __init__(self, baseurl):
        self._links = None
        self._loader = UrlModuleLoader(baseurl)
        self._baseurl = baseurl

    def find_loader(self, fullname):
        log.debug('find_loader: %r', fullname)
        parts = fullname.split('.')
        basename = parts[-1]
        # Check link cache
        if self._links is None:
            self._links = []     # See discussion
            self._links = _get_links(self._baseurl)

        # Check if it's a package
        if basename in self._links:
            log.debug('find_loader: trying package %r', fullname)
            fullurl = self._baseurl + '/' + basename
            # Attempt to load the package (which accesses __init__.py)
            loader = UrlPackageLoader(fullurl)
            try:
                loader.load_module(fullname)
                log.debug('find_loader: package %r loaded', fullname)
            except ImportError as e:
                log.debug('find_loader: %r is a namespace package', fullname)
                loader = None
            return (loader, [fullurl])

        # A normal module
        filename = basename + '.py'
        if filename in self._links:
            log.debug('find_loader: module %r found', fullname)
            return (self._loader, [])
        else:
            log.debug('find_loader: module %r not found', fullname)
            return (None, [])

    def invalidate_caches(self):
        log.debug('invalidating link cache')
        self._links = None

# Check path to see if it looks like a URL
_url_path_cache = {}
def handle_url(path):
    if path.startswith(('http://', 'https://')):
        log.debug('Handle path? %s. [Yes]', path)
        if path in _url_path_cache:
            finder = _url_path_cache[path]
        else:
            finder = UrlPathFinder(path)
            _url_path_cache[path] = finder
        return finder
    else:
        log.debug('Handle path? %s. [No]', path)

def install_path_hook():
    sys.path_hooks.append(handle_url)
    sys.path_importer_cache.clear()
    log.debug('Installing handle_url')
    
def remove_path_hook():
    sys.path_hooks.remove(handle_url)
    sys.path_importer_cache.clear()
    log.debug('Removing handle_url')


import urlimport

urlimport.install_meta('http://localhost:15000')

import fib
import spam
import grok.blah

grok.blah.__file__


# 10.12 Patching Modules on Import


import importlib
import sys
from collections import defaultdict

_post_import_hooks = defaultdict(list)

class PostImportFinder:
    def __init__(self):
        self._skip = set()

    def find_module(self, fullname, path=None):
        if fullname in self._skip:
            return None
        self._skip.add(fullname)
        return PostImportLoader(self)

class PostImportLoader:
    def __init__(self, finder):
        self._finder = finder

    def load_module(self, fullname):
        importlib.import_module(fullname)
        module = sys.modules[fullname]
        for func in _post_import_hooks[fullname]:
            func(module)
        self._finder._skip.remove(fullname)
        return module

def when_imported(fullname):
    def decorate(func):
        if fullname in sys.modules:
            func(sys.modules[fullname])
        else:
            _post_import_hooks[fullname].append(func)
        return func
    return decorate
    
sys.meta_path.insert(0, PostImportFinder())


# Example applying decorators to existing definitions.

from postimport import when_imported
from functools import wraps


def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling', func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return wrapper

# Example
@when_imported('math')
def add_logging(mod):
    mod.cos = logged(mod.cos)
    mod.sin = logged(mod.sin)

if __name__ == '__main__':
    import math
    print(math.cos(2))
    print(math.sin(2))


# 10.13 Installing Packages Just for Yourself

python3 setup.py install --user

# Or:

pip install --user packagename


#10.14 Creating a New Python Environment

# On windows:

bash % pyvenv Spam
bash %

# To include already installed packages as part of virtual environment.

bash % pyvenv --system-site-packages Spam
bash %


# 10.15 Distributing Packages

# First write a setup.py file:

# setup.py

from distutils.core import setup

setup(name='projectname',
      version='1.0',
      author="Your name',
      author_email='you@youraddress.com',
      url='http://www.you.com/projectname',
      packages=['projectname', 'projectname.utils'],

'''Next, make a file MANIFEST.in that lists various nonsource files
that you want to include in your package'''

# MANIFEST.in

include *.txt
recursive-include examples *
recursive-include Doc *

# Make sure both these files appear in the top-level directory of package.

# Now you can make a source distribution by typing:

% bash python3 setup.py sdist



