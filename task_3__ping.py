from http.server import HTTPServer, BaseHTTPRequestHandler


class TestTaskHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ GET request handler """
        valid_path = '/ping'
        response_msg = 'Cats service. Version 0.1\n'

        # Check for '/ping' request path
        if self.path != valid_path:
            response_msg = '\n'

        # Send response
        self.wfile.write(response_msg.encode('utf-8'))


def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, TestTaskHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
