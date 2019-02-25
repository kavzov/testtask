import socket


host = ''
port = 8080
que = 1
proper_path = '/ping'
response_msg = 'Unknown url\n'

# Socket settings
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(que)

while True:
    # Accept data at socket
    conn, addr = server_socket.accept()

    # Get request path from request headers
    path = conn.recv(1024).decode().split(' ')[1]

    # if path is '/ping', set the appropriate response message
    if path == proper_path:
        response_msg = 'Cats service. Version 0.1\n'

    # Send message to client
    conn.send(response_msg.encode())

    # Close connection with client
    conn.close()
