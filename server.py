import socket
import sys
import json
import math

class ServerStub(object):
    """docstring for ServerStub."""
    def add(self, x,y):
        return x+y

    def mult(self, x,y):
        return x*y

    def sqrt(self, x):
        return x**(1/2)

    def __init__(self):
        super(ServerStub, self).__init__()
        self.availableMethods = [
            ('add', 'x,y', 'params: x,y -> x+y'),
            ('mult', 'x,y', 'params: x,y -> x*y'),
            ('sqrt', 'x', 'params: x -> sqrt(x)')
        ]


    def unmarshall_message(self, data):
        try:
            json_data = json.loads(data)
            if json_data['id'] == 'get_functions':
                return json.dumps({'id': 'get_functions', 'content': self.availableMethods}).encode('utf8')
            else:
                func = getattr(self, json_data['id'])
                return json.dumps({ 'id': 'res', 'content': func(*json_data['params']) }).encode('utf8')
        except Exception as e:
            raise

def main():
    s = ServerStub()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 4000)
    print('starting up on {} port {}'.format(sys.stderr, server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('Connection from {}'.format(client_address))

            while True:
                data = connection.recv(4096)
                # Process data
                if data:
                    stub_res = s.unmarshall_message(data)
                    if stub_res:
                        print('sending {}'.format(stub_res))
                        connection.send(stub_res)
                else:
                    break
        finally:
            # Clean up the connection
            connection.close()

if __name__ == '__main__':
    main()
