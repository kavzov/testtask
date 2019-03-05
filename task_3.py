#!/usr/bin/env python
import socket


def main():
    VALID_PATH = '/ping'

    # Socket settings
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 8080))
    server_socket.listen(1)

    while True:
        response_msg = 'Cats service. Version 0.1\n'

        # Receive data from client socket
        client_socket = server_socket.accept()[0]
        data = client_socket.recv(1024).decode('utf-8')

        # Get request path from request headers
        try:
            path = data.split(' ')[1]
        except (AttributeError, IndexError):
            path = None

        # if path is not '/ping' set empty response message
        if path != VALID_PATH:
            response_msg = '\n'

        # Send message to client
        client_socket.send(response_msg.encode('utf-8'))

        # Close connection with client
        client_socket.close()


if __name__ == '__main__':
    main()
