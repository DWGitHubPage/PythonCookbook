# Python3.7.4
# Chapter 11 Network & Web Programming


# 11.1 Interacting with HTTP Services As a Client

from urllib import request, parse

# Base URL being accessed.

url = 'http://httpbin.org/get'

# Dictionary of query parameters.

parms = {
    'name1' : 'value1',
    'name2' : 'value2'
    }

# Encode the query string.

querystring = parse.urlencode(parms)

# Make a GET request & read the response.

u = request.urlopen(url+'?' + querystring)
resp = u.read()

import json
from pprint import pprint

json_resp = json.loads(resp.decode('utf-8'))
pprint(json_resp)

'''Sending the query parameters in the request body using a POST method,
encode them, & supply them as an optional argument to urlopen()'''

from urllib import request, parse

# Base URL being accessed.

url = 'http://httpbin.org/post'

# Dictionary of query parameters

parms = {
    'name1' : 'value1',
    'name2' : 'value2'
    }

# Encode the query string.

querystring = parse.urlencode(parms)

# Make a POST request & read the response.

u = request.urlopen(url, querystring.encode('ascii'))
resp = u.read()

'''If you need to supply some custom HTTP headers in the outgoing
request like a change to the user-agent field, make a dictionary
containing their value & creat a Request instance & pass it to urlopen()'''

from urllib import request, parse

# Extra headers.

headers = {
    'User-agen' : 'none/ofyourbusiness',
    'Spam' : 'Eggs'
    }

req = request.Request(url, querystring.encode('ascii'), headers=headers)

# Make a request & read the response.

u = request.urlopen(req)
resp = u.read()

# If your interaction with a service is more complicated, use requests library.

import requests

# Base URL being accessed.

url = 'http://httpbin.org/post'

# Dictionary of query parameters.

parms = {
    'name1' : 'value1',
    'name2' : 'value2'
    }

# Extra headers.

headers = {
    'User-agen' : 'none/ofyourbusiness',
    'Spam' : 'Eggs'
    }

resp = requests.post(url, data=parms, headers=headers)

# Decode text returned by the request.

text = resp.text

# Example using requests to make a HEAD request & extract fields.

import requests

resp = requests.head('http://www.python.org/index.html')

status = resp.status_code
#last_modified = resp.headers['last-modified']
content_type = resp.headers['content-type']
content_length = resp.headers['content-length']

print(status)
print(last_modified)
print(content_type)
print(content_length)

'''Example that executes a login into the Python Package index
using basic authentication'''

import requests

resp = requests.get('http://pypi.python.org/pypi?:action=login',
                    auth=('user', 'password'))

# Using requests to pass HTTP cookies from one request to the next.

import requests

# First request.

resp1 = requests.get(url)

# Second requests with cookies received on first requests.

resp2 = requests.get(url, cookies=resp1.cookies)

# Using requests to upload content.

import requests

url = 'http://httpbin.org/post'
files = { 'file': ('data.csv', open('data.csv', 'rb')) }

r = requests.post(url, files=files)

# Testing with httpbin.org is ideal over experimenting with a real site.

import requests

r = requests.get('http://httpbin.org/get?name=Dave&n=37',
                 headers = { 'User=agent': 'goaway/1.0' })

resp = r.json

print(resp['headers']


# 11.2 Creating a TCP Server

from socketserver import BaseRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)

if __name__ == '__main__':
    serv = TCPServer(('', 20_000), EchoHandler)
    serv.serve_forever()

'''To test the server, run it & open a separate Python process
that connects to it'''

from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20_000))

print(s.send(b'Hello'))
print(s.recv(8182))

'''It might be easier to defina a slightly different handler.
This one uses StreamRequestHandler base class to put a file-like
interface on the underlying socket'''

from socketserver import StreamRequestHandler, TCPServer

class EchoHandler(StreamRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # self.rfile is a file-like object for reading
        for line in self.rfile:
            # self.wfile is a file-like object for writing
            self.wfile.write(line)

if __nsme__ == '__main__':
    serv = TCPServer(('', 20_000), Echohandler)
    serv.serve_forever()

'''TCP servers re single threaded & can only serve one client at
a time. To handle multiple clients, instantiate a ForkingTCP Server
or ThreadingTCPServer object instead'''

from socketserver import ThreadingTCPServer

if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 20_000), EchoHandler)
    serv.serve_forever()

'''One issue with forking & threaded servers is that they spawn
a new process or thread on each client connection. Malicious hackers
might exploit this to make the server explode. You can create a
pre-allocated pool of worker threads or processes to stop that'''

if __name__ == '__main__':
    from threading import Thread
    NWORKERS = 16
    serv = TCPServer(('', 20_000), EchoHandler)
    for n in range(NWORKERS):
        t = Thread(target=serv.serve_forever)
        t.daemon = True
        t.start()
    serv.serve_forever()

'''Sometimes you might want to adjust the underlying socket by
setting options. To do this supply the bind_and_activate=False
argument'''

if __name__ == '__main__':
    serv = TCPServer(('', 20_000), EchoHandler, bind_and_activate=False)
    # Set up various socket options
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # Bind & activate
    serv.server_bind()
    serv.server_activate()
    serv.serve_forever()

# Set socket option before instantiating the server.

if __name__ == '__main__':
    TCPServer.allow_reuse_address = True
    serv = TCPServer(('', 20_000), EchoHandler)
    serv.serve_forever()

'''The StreamRequestHandler class is more flexible & supports features
that can be enabled through the specification of additional
class variables'''

import socket

class EchoHandler(StreamRequestHandler):
    # Optional settings (defaults shown)
    timeout = 5                      # Timeout on all socket operations
    rbufsize = -1                    # Read buffer size
    wbufsize = 0                     # Write buffer size
    disable_nagle_algorithm = False  # Sets TCP_NODELAY socket option
    def handle(self):
        print('Got connection from', self.client_address)
        try:
            for line in self.rfile:
                # self.wfile is a file-like object for writing
                self.wfile.write(line)
        except socket.timeout:
            print('Timed out!')

# Example of directly programming a server with Sockets.

from socket import socket, AF_INET, SOCK_STREAM

def echo_hanlder(address, client_sock):
    print('Got connection from {}'.format(address))
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()

def echo_server(address, blacklog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)

if __name__ == '__main__':
    echo_server(('', 20_000))


# 11.3 Creating a UDP Server

# Example of a simple time server.

from socketserver import BaseRequestHandler, UDPServer
import time

class TimeHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        msg, sock = self.request
        resp = time.ctime()
        sock.sendto(resp.encode('ascii'), self.client_address)

if __name__ == '__main__':
    serv = UDPServer(('', 20_000), TimeHandler)
    serv.serve_forever()

'''To test the server, run it & then open a separate Python process
that sends messages to it'''

from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
s.sendto(b'', ('localhost', 20_000))
s.recvfrom(8192)

'''If you want concurrent operation, instantiate a ForkingUDPServer
or ThreadingUDPServer object instead'''

from socketserver import ThreadingUDPServer

if __name__ == '__main__':
    serv = ThreadingUDPServer(('', 20_000), TimeHandler)
    serv.serve_forever()

# Example implementing a UDP server directly using sockets.

from socket import socket, AF_INET, SOCK_DGRAM
import time

def time_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)
    while True:
        msg, addr = sock.recvfrom(8192)
        print('Got message from', addr)
        resp = time.ctime()
        sock.sendto(resp_encode('ascii'), addr)

if __name__ == '__main__':
    time_server(('', 20_000))
    

# 11.4 Generating a Range of IP Addresses from a CIDR

import ipaddress

net = ipaddress.ip_network('123.45.67.64/27')

net   # In shell.

for a in net:
    print(a)

net6 = ipaddress.ip_network('12:3456:78:90ab:cd:ef01:23:30/125')

print(net6)

for a in net6:
    print(a)

# Networking objects also allow indexing like arrays. Example:

print(net.num_addresses)
print(net[0])
print(net[1])
print(net[-2])

# You can also perform operations such as a check for network membership.

a = ipaddress.ip_address('123.45.67.69')

print(a in net)

b = ipaddress.ip_address('123.45.67.123')

print(b in net)

'''An IP address & network address can be specified together
as an IP interface'''

inet = ipaddress.ip_interface('123.45.67.73/27')

print(inet.network)
print(inet.ip)

'''It's not possible to use an instance of IPv4Address as a
substitute for address string, instead you have to explicitly
convert it using str() first'''

a = ipaddress.ip_address('127.0.0.1')

from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect((str(a), 8080))


# 11.5 Creating a Simple REST-Based Interface

# resty.py

import cgi
    
def notfound_404(environ, start_response):
    start_response('404 Not Found', [ ('Content-type', 'text/plain') ])
    return [b'Not Found']

class PathDispatcher:
    def __init__(self):
        self.pathmap = {}

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(environ['wsgi.input'],
                                  environ=environ)
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = { key: params.getvalue(key) for key in params }
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function

# To use the dispatcher, write different handlers:

import time

_hello_resp = '''\
<html>
    <head>
        <title>Hello {name}</title>
    </head>
    </body>
        <h1>Hello {name}!</h1>
    </body>
</html>'''

def hello_world(environ, start_response):
    start_response('200 OK', [ ('Content-type', 'text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
    <year>{t.tm_year}<year>
    <month>{t.tm_mon}</month>
    <day>{t.tm_mday}</day>
    <hour>{t.tm_hour}</hour>
    <minute>{t.tm_min}</minute>
    <second>{t.tm_sec}</second>
</time>'''

def localtime(environ, start_response):
    start_response('200 OK', [ ('Content-type', 'application/xml') ])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')

if __name__ == '__main__':
    import resty
    from wsgiref.simple_server import make_server

    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()

# To test the server:

u = urlopen('http://localhost:8080/hello?name=Guido')

print(u.read().decode('utf-8'))

u = urlopen('http://localhost:8080/localtime')

print(u.read().decode('utf-8'))

'''In WSGI, you implement applications in the form of a callable
that accepts this calling convention'''

import cgi

def wsgi_app(environ, start_response):

    def wsgi_app(envriron, start_response):
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        # Parse the query parameters
        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)

# Example returning a sequence of byte strings.

def wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])

def wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    resp = []
    resp.append(b'Hello World\n')
    resp.append(b'Goodbye!\n')
    return resp

def wsgi_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    yield b'Hello World\n'
    yield b'Goodbye!\n'

# Example with a suitable __call__()method

class WSGIApplication:
    def __init__(self):

        def __call__(self, environ, start_response):

'''An important part of using WSGI is that nothing is specific to a
particular web server. This is the whole idea, the standard is server &
framework neutral, you can plug your application into a variety of servers'''

# Code used for testing:

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Create the dispatcher & register functions
    dispatcher = PathDispatcher()

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()


# 11.6 Implementing a Simple Remote Procedure Call with XML-RPC

from xmlrpc.server import SimpleXMLRPCServer

class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys']
    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

        def get(self, name):
            return self._data[name]

        def set(self, name, value):
            self._data[name] = value

        def delete(self, name):
            del self._data[name]

        def exists(self, name):
            return name in self._data

        def keys(self):
            return list(self._data)

        def serve_forever(self):
            self._serv.serve_forever()

        # Example
if __name__ == '__main__':
    kvserv = KeyValueServer(('', 15_000))
    kvserv.serve_forever()

# Accessing it remotely from a client.

from xmlrpc.client import ServerProxy

s = ServerProxy('http://localhost:15000', allow_none=True)
s.set('foo', 'bar')
s.set('spam', [1, 2, 3])

print(s.keys())
print(s.get('foo'))
print(s.get('spam'))
s.delete('spam')
print(s.exists('spam'))

# Another example.

from xmlrpc.server import SimpleXMLRPCServer

def add(x, y):
    return x + y

serv = SimpleXMLRPCServer(('', 15000))
serv.register_function(add)
serv.serve_forever()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 3)
s.set('foo', p)
s.get('foo')

# Handling binary data.

s.set('foo', b'Hello World')
s.get('foo')
_.data


# 11.7 Communicating Simply Between Interpreters

# Example of an echo server:

from multiprocessing.connection import Listener
import traceback

def echo_client(conn):
    try:
        while True:
            msg = conn.recv()
            conn.send(msg)
    except EOFError:
        print('Connection closed')

def echo_server(address, authkey):
    serv = Listener(address, authkey=authkey)
    while True:
        try:
            client = serv.accept()
            echo_client(client)
        except Exception:
            traceback.print_exc()

echo_server(('', 25000), authkey=b'peekaboo')

# Example of a client connecting to a server & sending messages.

from multiprocessing.connection import Client

c = Client(('localhost', 25000), authkey=b'peekaboo')
c.send('hello')
print('Got:', c.recv())
c.send(42)
print('Got:', c.recv())
c.send([1, 2, 3,4, 5])
print('Got:', c.recv())


# 11.8 Implementing Remote Procedure Calls

import pickle

class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = pickle.loads(connection.recv())
                # Run the RPC & send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(pickle.dumps(r))
                except Exception as e:
                    connection.send(pickle.dumps(e))
        except EOFError:
            pass

# To use the handler, you need to add it into a messaging server.

from multiprocessing.connection import Listener
from threading import Thread

def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()

# Some remote functions
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

# Register with a handler
    handler = RPCHandler()
    handler.register_function(add)
    handler.register_function(sub)

# Run the server
    rcp_server(handler, ('localhost', 17000), authkey=b'peekaboo')

'''To access the server from a remote client, you need to create a
corresponding RPC proxy class that forwards requests'''

import pickle

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(pickle.dumps((name, args, kwargs)))
            result = pickle.loads(self._connection.recv())
            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc

# To use the proxy, wrap it around a connection to the server.

from multiprocessing.connection import Client

c = Client(('localhost', 17000), authkey=b'peekaboo')
proxy = RPCProxy(c)
print(proxy.add(2, 3))
print(proxy.sub(2, 3))

# You can also easily adapt this to JSON encoding.

import json

class RPCHandler:
    def __init__(self):
        self._functions = { }
    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = json.loads(connection.recv())
                # Run the RPC & send a response
                try:
                    r = self._functions[func_name](*args, **kwargs)
                    connection.send(json.dumps(r))
                except Exception as e:
                    connection.send(json.dumps(str(e)))
        except EOFError:
            pass

# jsonrpcclient.py

import json

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(json.dumps((name, args, kwargs)))
            result = json.loads(self._connection.recv())
            return result
        return do_rpc


# 11.9 Authenticating Clients Simply

import hmac
import os

def client_authenticate(connection, secret_key):
    message = connection.recv(32)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    connection.send(digest)

def server_authenticate(connection, secret_key):
    message = os.urandom(32)
    connection.send(message)
    hash = hmac.new(secret_key, message)
    digest = hash.digest()
    response = connection.recv(len(digest))
    return hmac.compare_digest(digest, response)

'''To use these functions, you incorporate them into existing networking
or messaging code. For example, with sockets:'''

from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'peekaboo'
def echo_handler(client_sock):
    if not server_authenticate(client_sock, secret_key):
        client_soc.close()
        return
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)

def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    while True:
        c, a = s.accept()
        echo_handler(c)

echo_server(('', 18000))

# Within a client, you would do this:

from socket import socket, AF_INET, SOCK_STREAM

secret_key = b'peekaboo'

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 18000))
client_authenticate(s, secret_key)
s.send(b'Hello World')
resp = s.recv(1024)


# 11.10 Adding SSL to Network Services

from socket import socket, AF_INET, SOCK_STREAM
from socket import SOL_SOCKET, SO_REUSEADDR
import ssl

KEYFILE = 'server_key.pem'   # Private key of the server
CERTFILE = 'server_cert.pem'  # Server certificate (given to client)

def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b'':
            break
        s.send(data)
    s.close()
    print('Connection closed')

def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1)

    # Wrap with an SSL layer requiring client certs
    s_ssl = ssl.wrap_socket(s,
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            server_side=True
                            )
    # Wait for connections
    while True:
        try:
            c, a = s_ssl.accept()
            print('Got connection', c, a)
            echo_client(c)
        except Exception as e:
            print('{}: {}'.format(e.__class__.__name__, e))

    echo_server(('', 20000))

'''Now for an interactive session that shows how to connect to the server
as a client'''

from socket import socket, AF_INET, SOCK_STREAM
import ssl

s = socket(AF_INET, SOCK_STREAM)
ssl_s = ssl.wrap_socket(s,
                        cert_reqs=ssl.CERT_REQUIRED,
                        ca_certs = 'server_cert.pem',
                        )
ssl_s.connect(('localhost', 20000))
ssl_s.send(b'Hello World?')
resp = ssl_s.recv(8192)
print('Got:', resp)

# Done
ssl_s.close()

# SSL can be added through a mixin class.

import ssl

class SSLMixin:
    def __init__(self, *args,
                 keyfile=None, certfile=None, ca_certs=None,
                 cert_reqs=ssl.NONE,
                 **kwargs):
        self._keyfile = keyfile
        self._certfile = certfile
        self._ca_certs = ca_certs
        self._cert_reqs = cert_reqs
        super().__init__(*args, **kwargs)

    def get_request(self):
        client, addr = super().get_request()
        client_ssl = ssl.wrap_socket(client,
                                     keyfile = self._keyfile,
                                     certfile = self._certfile,
                                     ca_certs = self._ca_certs,
                                     cert_reqs = self._cert_reqs,
                                     server_side = True)
        return client_ssl, addr

# To use mixin class, you can mix it with other server classes.

from xmlrpc.server import SimpleXMLRPCServer

class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
    pass

# Here the XML-RPC server is modified slightly.

import ssl
from xmlrpc.server import SimpleXMLRPCServer
from sslmixin import SSLMixin

class SSLSimpleXMLRPCServer(SSLMixin, SimpleXMLRPCServer):
    pass

class KeyValueServer:
    _rpc_methods_ ['get', 'set', 'delete', 'exists', 'keys']
    def __init__(self, *args, **kwargs):
        self._data = {}
        self._serv = SSLSimpleXMLRPCServer(*args, allow_none=True, **kwargs)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._ser.serve_forever()

if __name__ == '__main__':
    KEYFILE='server_key.pem'
    CERTFILE='server_cert.pem'
    kvserv = KeyValueServer(('', 15000),
                            keyfile=KEYFILE,
                            certfile=CERTFILE),
    kvserv.serve_forever()

from xmlrpc.client import ServerProxy

s = ServerProxy('https://localhost:15000', allow_none=True)
s.set('foo', 'bar')
s.set('spam', [1, 2, 3])

print(s.keys())
print(s.get('foo'))
print(s.get('spam'))
s.delete('spam')
print(s.exists('spam'))

'''Example of how to set up a secure XML-RPC connection that verifies
the server's certificate'''

from xmlrpc.client import SafeTransport, ServerProxy
import ssl

class VerifyCertSafeTransport(SafeTransport):
    def __init__(self, cafile, certfile=None, keyfile=None):
        SafeTransport.__init__(self)
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self._ssl_context.load_verify_locations(cafile)
        if cert:
            self._ssl_context.load_cert_chain(certfile, keyfile)
        self._ssl_context.verify_mode = ssl.CERT_REQUIRED

    def make_connection(self, host):
        s = super().make_connection((host, {'context': self._ssl_context}))

        return s

# Create the client proxy

s = ServerProxy('https://localhost:15000',
                transport=VerifyCertSafeTransport('server_cert.pem'),
                allow_none=True)

# If the server wants to verify the client, change the server startup:

if __name__ == '__main__':
    KEYFILE = 'server_key.pem'
    CERTFILE = 'server_cert.pem'
    CA_CERTS = 'client_cert.pem'

    kvserv = KeyValueServer(('', 15000),
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            ca_certs=CA_CERTS,
                            cert_reqs=ssl.CERT_REQUIRED,
                            )
    kvserv.serve_forever()

'''To make the XML-RPC client present its certificates, change the
ServerProxy initialization to this:'''

s = ServerProxy('https://localhost:15000',
                transport=VerifyCertSafeTransport('server_cert.pem',
                                                  'client_cert.pem',
                                                  'client_key.pem'),
                allow_none=True)

# You can create self-signed certificates as well:

#!/bin/sh

openssl req -new -x509 -days 365 -nodes -out server_cert.pem \
        -keyout server_key.pem
openssl req -new -x509 -days 365 -nodes -out client_cert.pem \
        -keyout client_key.pem


# 11.11 Passing a Socket File Descriptor Between Processes

import multiprocessing
from multiprocessing.reduction import recv_handle, send_handle
import socket

def worker(in_p, out_p):
    out_p.close()
    while True:
        fd = recv_handle(in_p)
        print('CHILD: GOT FD', fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print('CHILD: RECV {!R}'.format(msg))
                s.send(msg)

def server(address, in_p, out_p, worker_pid):
    in_p.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, TRUE)
    s.bind(address)
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)
        send_handle(out_p, client.fileno(), worker_pid)
        client.close()

if __name__ == '__main__':
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1, c2))
    worker_p.start()

    server_p = multiprocessing.Process(target=server,
                args=(('', 15000), c1, c2, worker_p.pid))
    server_p.start()

    c1.close()
    c2.close()

# You can also implement the server & worker as completely separate programs.

from multiprocessing.connection import Listener
from multiprocessing.reduction import send_handle
import socket

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = Listener(work_address, authkey=b'peekaboo')
    worker = work_serv.accept()
    worker_pid = worker.recv()

    # Now run a TCP/IP server & send clients to worker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.blind(('', port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)
        send_handle(worker, client.fileno(), worker_pid)
        client.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))

# Here is the corresponding client code:

from multiprocessing.connection import Client
from multiprocessing.reduction import recv_handle
import os
from socket import socket, AF_INET, SOCK_STREAM

def worker(server_address):
    serv = Client(server_address, authkey=b'peekaboo')
    serv.send(os.getpid())
    while True:
        fd = recv_handle(serv)
        print('WORKER: GOT FD', fd)
        with socket(AF_INET, SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print('WORKER: RECV {!r}'.format(msg))
                client.send(msg)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: worker. py server_address', fie=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])

'''Implementation of the server that shows how to
pass descriptors using sockets'''

import socket
import struct

def send_fd(sock, fd):
    sock.sendmsg([b'x'],
                 [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('i', fd))])
    ack = sock.recv(2)
    assert ack == b'OK'

def server(work_address, port):
    # Wait for the worker to connect
    work_serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    work_serv.bind(work_address)
    work_serv.listen(1)
    worker, addr = work_serv.accept()

    # Now run a TCP/IP server & send clients to worker
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(('', port))
    s.listen(1)
    while True:
        client, addr = s.accept()
        print('SERVER: Got connection from', addr)
        send_fd(worker, client.fileno())
        client.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: server.py server_address port', file=sys.stderr)
        raise SystemExit(1)

    server(sys.argv[1], int(sys.argv[2]))

# An implementation of worker using sockets.

import socket
import struct

def recv_fd(sock):
    msg, ancdata, flags, addr = sock.recvmsg(1,
                                    socket.CMSG_LEN(struct.calcsize('i')))

    cmsg_level, cmsg_type, cmsg_data = ancdata[0]
    assert cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS
    sock.sendall(b'OK')
    return struct.unpack('i', cmsg_data)[0]

def worker(server_address):
    serv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    serv.connect(server_address)
    while True:
        fd = recv_fd(serv)
        print('WORKER: GOT FD', fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as client:
            while True:
                msg = client.recv(1024)
                if not msg:
                    break
                print('WORKER: RECV {!r}'.format(msg))
                client.send(msg)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: worker.py server_address', file=sys.stderr)
        raise SystemExit(1)

    worker(sys.argv[1])


# 11.12 Understanding Event-Driven I/O)

class EventHandler:
    def fileno(self):
        'Return the associated file descriptor'
        raise NotImplemented('must implement')

    def wants_to_receive(self):
        'Return True if receiving is allowed'
        return False

    def handle_receive(self):
        'Perform the receive operation'
        pass

    def wants_to_send(self):
        'Return True if sending is requested'
        return False

    def handle_sent(self):
        'Send outgoing data'
        pass

# Instances of this class then get plugged into an event loop.

import select

def event_loop(handlers):
    while True:
        wants_recv = [h for h in handlers if h.wants_to_receive()]
        wants_send = [h for h in handlers if h.wants_to_send()]
        can_recv, can_send, _ = select.select(wants_recv, wants_send, [])
        for h in can_recv:
            h.handle_receive()
        for h in can_send:
            h.handle_send()

'''Example of two simple handlers that illustrate two
UDP-based network services'''

import socket
import time

class UDPServer(EventHandler):
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(address)

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

class UDPTimeServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(1)
        self.sock.sendto(time.ctime().encode('ascii'), addr)

class UDPEchoServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(8192)
        self.sock.sendto(msg, addr)

if __name__ == '__main__':
    handlers = [ UDPTimeServer(('', 14000)), UDPEchoServer(('', 15000)) ]
    event_loop(handlers)

# To test the code, you can try connecting it from another Python interpreter.

from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.sendto(b'',('localhost', 14000))
s.recvfrom(128)
s.sendto(b'Hello', ('localhost', 15000))
s.recvfrom(128)

# Example of TCP echo client.

class TCPServer(EventHandler):
    def __init__(self, address, client_handler, handler_list):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind(address)
        self.sock.listen(1)
        self.client_handler = client_handler
        self.handler_list = handler_list

    def fileno(self):
        return self.sock.fileno()

    def wants_to_receive(self):
        return True

    def handle_receive(self):
        client, addr = self.sock.accept()
        # Add the client to the event loop's handler list
        self.handler_list.append(self.client_handler(client, self.handler_list))

class TCPClient(EventHandler):
    def __init__(self, sock, handler_list):
        self.sock = sock
        self.handler_list = handler_list
        self.outgoing = bytearray()

    def fileno(self):
        return self.sock.fileno()

    def close(self):
        self.sock.close()
        # Remove myself from the event loop's handler list
        self.handler_list.remove(self)

    def wants_to_send(self):
        return True if self.outgoing else False

    def handle_send(self):
        nsent = self.sock.send(self.outgoing)
        self.outgoing = self.outgoing[nsent:]

class TCPEchoClient(TCPClient):
    def wants_to_receive(self):
        return True

    def handle_receive(self):
        data = self.sock.recv(8192)
        if not data:
            self.close()
        else:
            self.outgoing.extend(data)

if __name__ == '__main__':
    handlers = []
    handlers.append(TCPServer(('', 16000), TCPEchoClient, handlers))
    event_loop(handlers)

# Example of event loop that uses the concurrent.futures module.

from concurrent.futures import ThreadPoolExecutor
import os

class ThreadPoolHandler(EventHandler):
    def __init__(self, nworkers):
        if os.name == 'posix':
            self.signal_done_sock, self.done_sock = socket.socketpair()
        else:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self.signal_done_sock = socket.socket(socket.AF_INET,
                                                  socket.SOCK_STREAM)
            self.signal_done_sock.connect(server.getsockname())
            self.done_sock, _ = server.accept()
            server.close()

        self.pending = []
        self.pool = ThreadPoolExecutor(nworkers)

    def fileno(self):
        return self.done_sock.fileno()

    # Callback that executes when the thread is done
    def _complete(self, callback, r):
        self.pending.append((callback, r.result()))
        self.signal_done_sock.send(b'x')

    # Run a function in a thread pool
    def run(self, func, args=(), kwargs={}, *, callback):
        r = self.pool.submit(func, *args, **kwargs)
        r.add_done_callback(lambda r: self._complete(callback, r))

    def wants_to_receive(self):
        return True

    # Run callback functions of completed work
    def handle_receive(self):
        # Invoke all pending callback functions
        for callback, result in self.pending:
            callback(result)
            self.done_sock.recv(1)
        self.pending = []

'''Example of a simple server that shows how to use the thread pool to
carry out a long-running calculation'''

# A really bad Fibonacci implementation
def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n - 2)

class UDPFibServer(UDPServer):
    def handle_receive(self):
        msg, addr = self.sock.recvfrom(128)
        n = int(msg)
        pool.run(fib, (n,), callback=lambda r: self.respond(r, addr))

    def respond(self, result, addr):
        self.sock.sendto(str(result).encode('ascii'), addr)

if __name__ == '__main__':
    pool = ThreadPoolHandler(16)
    handlers = [pool, UDPFibServer(('', 16000))]
    event_loop(handlers)

# Trying the sever with another Python program.

from socket import *

sock = socket(AF_INET, SOCK_DGRAM)
for x in range(40):
    sock.sendto(str(x).encode('ascii'), ('localhost', 16000))
    resp = sock.recvfrom(8192)
    print(resp[0])


# 11.13 Sending & Receiving Large Arrays

def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]

# To test the program, create a server & client program connected over a socket.

from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 25000))
s.listen(1)
c, a = s.accept()


# In the client, in a separate interpreter:

from socket import *

c = socket = (AF_INET, SOCK_STREAM)
c.connect(('localhost', 25000))


# Now you can blast a huge array through the connection using numpy.

# Server
import numpy

a = numpy.arange(0.0, 50000000.0)
send_from(a, c)

# Client
import numpy

a = numpy.zeros(shape=50000000, dtype=float)
a[0:10]
recv_into(a, c)
a[0:10]
