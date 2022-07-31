# Author: Hobs Towler
# GitHub username: hobstowler
# Date: 6/22/2022
# Description: A script for a small web server that sends a message when a user connects to it.
import random
import socket

# Code Adapted from examples and documenation at:
# https://docs.python.org/3/library/socket.html
# date: 7/31/2022

# Word list pulled from:
# https://7esl.com/6-letter-words/
# date: 7/31/2022


class Server:
    _conn_ask = False
    _host = '127.0.0.1'
    _port = 9508
    _client_handle = 'SERVER >>'
    _server_handle = 'CLIENT >>'

    _game_mode = False
    _game_word = ''
    _guesses = 5
    _num_guesses = 0


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
            print(self._client_handle, message)
            reply = 'Would you like to play a game? (yes/no)'
            conn.send(reply.encode())
            print(self._server_handle, reply)

            message = conn.recv(4096).decode()
            print(self._client_handle, message)
            if message == 'yes':
                self._game_mode = True
                self.start_game()
                reply = f'Alright, let\'s play Wordle!\r\nI\'ll pick a 6-letter word and give you {self._guesses} ' \
                        f'guesses to get it right\r\nIf you get the right letter and position, I\'ll denote that with' \
                        f' "$"\r\nIf you get the right letter, but the wrong position, I\'ll denote that with a "!"' \
                        f'\r\nSo, Give me your first guess...'
                conn.send(reply.encode())
                print(self._server_handle, reply)
            else:
                reply = 'Ok, maybe next time...\r\nIf you want to play, just say "/game"'
                conn.send(reply.encode())
                print(self._server_handle, reply)

            while message != '/q':
                message = conn.recv(4096).decode()
                print(self._client_handle, message)
                if self._game_mode:
                    if message == '/q':
                        reply = 'Okay! If you want to play again, just say "/game". If you want to quit fully, just ' \
                                'say "/q" one more time.'
                    else:
                        reply = self.parseResponse(message)
                else:
                    if message == '/q':
                        reply = 'Goodbye!'
                    else:
                        reply = input(self._server_handle + ' ')
                conn.send(reply.encode())
                print(self._server_handle, reply)

            serv_socket.close()
            break

    def start_game(self):
        words = []
        with open('words') as file:
            for line in file:
                words.append(line.strip())
        self._game_word = random.choice(words).lower()
        print(self._game_word)

    def parseResponse(self, message):
        message = message.strip()
        if len(message) < 6:
            return 'Word is too short. Try again.'
        if len(message) > 25:
            return 'Word is waaaaaaaaay too long. Try again.'
        if len(message) > 6:
            return 'Word is too long. Try again.'

        self._num_guesses += 1
        message = message.lower()
        if message == self._game_word:
            return f'You got the word in {self._num_guesses} guess{"es" if self._num_guesses > 1 else ""}! {self._game_word}'


        answer = f'You guessed:\r\n{message}\r\n'
        guess_score = 0
        for i in range(len(message)):
            if message[i] == self._game_word[i]:
                answer += '$'
                guess_score += 2
            elif message[i] in self._game_word:
                answer += '!'
                guess_score += 1
            else:
                answer += '_'
        if guess_score >= 10:
            answer += f' Wow! You\'re getting close!'
        elif guess_score >= 7:
            answer += f' That was a pretty good guess.'
        elif guess_score >= 3:
            answer += f' Keep going, you\'ll get there.'
        remaining = self._guesses - self._num_guesses
        guesses = f' {remaining} guess{"es" if self._num_guesses > 1 else ""} left'
        answer += guesses

        return answer



if __name__ == '__main__':
    server = Server()
    server.start()