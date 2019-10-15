import socket
import sys
import pickle

class A(object):
    """docstring for A."""

    def __init__(self):
        super(A, self).__init__()
        funcs = self.fetchParams()
        self.buildFunctions(funcs)

    def fetchParams(self):
        funcs = [('add', 'x,y')]
        return funcs

    def buildFunctions(self, funcs):
        for func in funcs:
            name, params = func
            self.make_method(name, params.split(','))

    def make_method(self, name, params):
        def _method(self, *params):
            if name == 'add':
                return params[0] + params[1]
        setattr(self.__class__, name, _method)

a = A()
print(a.add(1,2))


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 4000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def add(x,y):
    print('lol')

try:
    # Send data
    data = sock.recv(1024)
    data = pickle.loads(data)
    print(data['add'](3,4))


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
