import socket
import sys
import json

class ServerStub(object):
    """docstring for ServerStub."""

    def add(self, x,y):
        return x+y

    def __init__(self):
        super(ServerStub, self).__init__()

    def unmarshall_message(self, data):
        try:
            json_data = json.loads(data)
            if json_data['id'] == 'get_functions':
                return json.dumps({'id': 'get_functions', 'content': [('add', 'x,y', 'params: x,y -> x+y')]})
            else:
                func = getattr(self, json_data['id'])
                return json.dumps({ 'id': 'res', 'content': func(*json_data['params']) })
        except Exception as e:
            raise

def main():
    s = ServerStub()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 4000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    sock.listen(1)

    while True:
        # Wait for a connection
        print >>sys.stderr, 'waiting for a connection'
        connection, client_address = sock.accept()

        try:
            print >>sys.stderr, 'connection from', client_address

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
