# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 7/31/2022
# Description: Class and methods for a chat server with optional Wordle clone to play.

# Code Adapted from examples and documentation at:
# https://docs.python.org/3/library/socket.html
# date: 7/31/2022

# Word list pulled from:
# https://7esl.com/6-letter-words/
# date: 7/31/2022

import socket
from game import Game


class Server:
    """
    An object representing the server of a CLI chat app.
    """
    _conn_ask = False
    _host = '127.0.0.1'
    _port = 9508
    _client_handle = 'CLIENT >>'
    _server_handle = 'SERVER >>'

    _game = None

    def start_game(self):
        """
        Starts up a new game and sends the message to the player with instructions
        :return: the instructions to the player
        """
        self._game = Game()
        self._game.start()

        reply = f'Alright, let\'s play 6-Word!\r\n\t\t  I\'ll pick a 6-letter word and give you {self._game.guesses} ' \
                f'guesses to get it right\r\n\t\t  If you get the right letter and position, I\'ll denote that with' \
                f' "$"\r\n\t\t  If you get the right letter, but the wrong position, I\'ll denote that with a "!"' \
                f'\r\n\t\t  (If you want to stop, just say "/end")'\
                f'\r\n\t\t  So, Give me your first guess...'
        return reply

    def start(self):
        """
        Starts the server.
        """
        if self._conn_ask:
            self._port = int(input('Port #:'))

        # define connection and socket
        connection = (self._host, self._port)
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # binds the socket to the specified IP and port then begins listening for a new connection
        serv_socket.bind(connection)
        serv_socket.listen()
        print(f'listening on {self._host}:{self._port}')

        # main loop
        while True:
            conn, addr = serv_socket.accept()
            message = conn.recv(4096).decode()
            print(self._client_handle, message)
            reply = 'Would you like to play a game? (yes/no)'
            conn.send(reply.encode())
            print(self._server_handle, reply)

            message = conn.recv(4096).decode()
            print(self._client_handle, message)

            # evaluate first message from client and populate then send a reply
            if message == '/q':
                reply = 'Ok... Goodbye, I guess?'
            elif message == 'yes':
                reply = self.start_game()
            else:
                reply = 'Ok, maybe next time...\r\n\t\t  If you want to play, just say "/game"'
            conn.send(reply.encode())
            print(self._server_handle, reply)

            # main reply loop
            while message != '/q':
                message = conn.recv(4096).decode()
                print(self._client_handle, message)

                # quit
                if message == '/q':
                    reply = 'Goodbye!'
                    print(self._server_handle, reply)
                # condition where we are playing a game
                elif self._game:
                    # quit a game in progress
                    if message == '/end':
                        self._game = None
                        reply = 'Okay, we can just chat for now! If you want to play again, just say "/game". If you ' \
                                'want to quit fully, just say "/q".'
                        print(self._server_handle, reply)
                    # parse message in game
                    else:
                        reply = self._game.parse_response(message)
                        # check to see if the game is over
                        if self._game.finished:
                            self._game = None
                            reply += f'\r\n\t\t  Since the game is over, let\'s go back to chatting...'\
                                     f'\r\n\t\t  If you want to play another game, say "/game".'
                            print(self._server_handle, reply)
                # start a new game
                elif message == '/game':
                    reply = self.start_game()
                    print(self._server_handle, reply)
                # get input while chatting
                else:
                    reply = input(self._server_handle + ' ')

                conn.send(reply.encode())

            serv_socket.close()
            break


if __name__ == '__main__':
    server = Server()
    server.start()
