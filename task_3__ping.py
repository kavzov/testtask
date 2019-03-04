from http.server import BaseHTTPRequestHandler
from utils import run_server


class Task3RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ GET request handler """
        VALID_PATH = '/ping'
        response_msg = 'Cats service. Version 0.1\n'

        # Check for '/ping' request path
        if self.path != VALID_PATH:
            response_msg = '\n'

        # Send response
        self.wfile.write(response_msg.encode('utf-8'))


def main():
    run_server(handler=Task3RequestHandler)


if __name__ == '__main__':
    main()
