from http.server import HTTPServer, BaseHTTPRequestHandler


class TestTaskHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ GET request handler """
        proper_path = '/ping'
        response_msg = 'Unknown url\n'

        # Check for '/ping' request path
        if self.path == proper_path:
            response_msg = 'Cats service. Version 0.1\n'

        # Send response
        self.wfile.write(response_msg.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=TestTaskHTTPRequestHandler):
    host = ''
    port = 8080
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
