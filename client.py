# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 7/31/2022
# Description: Class and methods for a chat client.

import socket


class Client:
    """
    An object representing the client of a CLI chat app.
    """
    _client_handle = 'YOU >>'
    _server_handle = 'SERVER >>'

    def connect(self, host: str = None, port: int = None):
        """
        Connect to a host. If host and/or port are not specified, user will be prompted to enter those details.
        :param host: The host address
        :param port: The host port
        """
        if not host:
            host = input('Server address: ')
        if not port:
            port = int(input('Port:'))

        # build the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # send first connection message and print
        message = f'Connected to host on {host}:{port}!'
        client_socket.send(message.encode())
        print(self._client_handle, message)

        # get first response
        serv_res = client_socket.recv(4096).decode()
        print(self._server_handle, serv_res)

        # loop while we're not trying to quit
        while message != '/q':
            message = input(self._client_handle + ' ')
            client_socket.send(message.encode())
            serv_res = client_socket.recv(4096).decode()
            print(self._server_handle, serv_res)


if __name__ == '__main__':
    client = Client()
    client.connect('127.0.0.1', 9508)
