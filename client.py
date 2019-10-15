import socket
import sys
import json

class ClientStub(object):
    """docstring for ClientStub."""

    def __init__(self):
        super(ClientStub, self).__init__()
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 4000)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        self.sock.connect(server_address)
        self.fetchParams()

    def fetchParams(self):
        message = {'id': 'get_functions', 'content': []}
        try:
            self.sock.send(json.dumps(message))
            data = self.sock.recv(4096)
            if data:
                res = self.unmarshall_message(data)
        except Exception as e:
            raise
        finally:
            pass

    def buildFunctions(self, funcs):
        for func in funcs:
            name, params, desc = func
            self.make_method(name, params.split(','))

    def unmarshall_message(self, data):
        json_data = json.loads(data)
        # message with all server functions
        if json_data['id'] == 'get_functions':
            self.buildFunctions(json_data['content'])
        # message with result of RPC
        elif json_data['id'] == 'res':
            return json_data['content']

    def make_method(self, name, params):
        def _method(self, *params):
            message = {'id': name, 'params': params}
            self.sock.send(json.dumps(message))
            data = self.sock.recv(4096)
            if data:
                res = self.unmarshall_message(data)
                return res
            return None
        setattr(self.__class__, name, _method)

def main():
    a = ClientStub()
    res = a.add(-1,4)
    print(res)
if __name__ == '__main__':
    main()
