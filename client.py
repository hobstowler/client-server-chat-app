import socket


class Client:
    def __init__(self):
        pass

    def connect(self, host: str = None, port: int = None):
        if not host:
            host = input('Server address: ')
        if not port:
            port = int(input('Port:'))

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = 'something'
        client_socket.send(message.encode())
        serv_res = client_socket.recv(4096).decode()
        print('Server >>', serv_res)

        while message != '/q':
            message = input('You >>')
            client_socket.send(message.encode())
            serv_res = client_socket.recv(4096).decode()
            print('Server >>', serv_res)


if __name__ == '__main__':
    client = Client()
    client.connect('127.0.0.1', 9508)
