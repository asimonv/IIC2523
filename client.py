#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        print('connecting to {} port {}'.format(sys.stderr, server_address))
        self.sock.connect(server_address)
        self.fetchParams()

    def showAvailableFunctions(self):
        print('==== Available Functions ====')
        for f in self.functionData:
            print('{}({}): {}'.format(*f))
        print('=============================\n')

    def fetchParams(self):
        message = {'id': 'get_functions', 'content': []}
        try:
            self.sock.sendall(json.dumps(message).encode('utf8'))
            data = self.sock.recv(4096)
            if data:
                self.unmarshall_message(data)
        except Exception as e:
            raise
        finally:
            pass

    def buildFunctions(self, funcs):
        res = []
        self.functionData = funcs
        for func in funcs:
            name, params, desc = func
            res.append(self.make_method(name, params.split(',')))

    def unmarshall_message(self, data):
        json_data = json.loads(data)
        # message with all server functions
        if json_data['id'] == 'get_functions':
            print('* functions loaded *\n')
            return self.buildFunctions(json_data['content'])
        # message with result of RPC
        elif json_data['id'] == 'res':
            return json_data['content']

    def make_method(self, name, params):
        def _method(self, *params):
            message = {'id': name, 'params': params}
            self.sock.sendall(json.dumps(message).encode('utf8'))
            data = self.sock.recv(4096)
            if data:
                return self.unmarshall_message(data)
        setattr(self.__class__, name, _method)
        return _method

def main():
    a = ClientStub()
    a.showAvailableFunctions()
    points = [[3,3],[5,-1],[-2,4]]
    print(a.kClosest(points, 2))
if __name__ == '__main__':
    main()
