import socket


def run():
    proper_path = '/ping'

    # Socket settings
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 8080))
    server_socket.listen(1)

    while True:
        response_msg = 'Cats service. Version 0.1\n'

        # Accept data at socket
        conn, addr = server_socket.accept()

        # Get request path from request headers
        path = conn.recv(1024).decode().split(' ')[1]

        # if path is '/ping', set the appropriate response message
        if path != proper_path:
            response_msg = '\n'

        # Send message to client
        conn.send(response_msg.encode())

        # Close connection with client
        conn.close()


if __name__ == '__main__':
    run()
