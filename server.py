# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 6/22/2022
# Description: A script for a small web server that sends a message when a user connects to it.

import socket

# Code Adapted from examples and documenation at:
# https://docs.python.org/3/library/io.html#io.TextIOWrapper
# https://docs.python.org/3/library/socket.html
# on 6/22/2022

# Requests pulled from project instructions at:
# https://canvas.oregonstate.edu/courses/1878268/assignments/8929461?module_item_id=22337858
# on 6/22/2022

CONN = ('127.0.0.1', 8503)


class Server:
    _conn_ask = False
    _host = '127.0.0.1'
    _port = 9507

    def __init__(self):
        pass

    def set_port(self, new_port: int):
        self._port = new_port

    def set_prompt(self, value: bool):
        self._conn_ask = value

    def start(self):
        if self._conn_ask:
            self._port = int(input('Port #:'))

        # define connection and socket
        connection = (self._host, self._port)
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binds the socket to the specified IP and port then begins listening for a new connection
        serv_socket.bind(connection)
        serv_socket.listen()
        print(f'listening on {self._host}:{self._port}')

        while True:
            conn, addr = serv_socket.accept()
            message = conn.recv(4096).decode()
            print('Client >>', message)
            reply = 'Connection established. Say Hi!'
            conn.send(reply.encode())
            print('Server >>', reply)

            while message != 'quit':
                message = conn.recv(4096).decode()
                print('Client >>', message)
                reply = input()
                conn.send(reply.encode())
                print('Server >>', reply)

            reply = 'Goodbye'
            conn.send(reply)
            print('Server >>', reply)
            serv_socket.close()
            break


if __name__ == '__main__':
    server = Server()
    server.start()