from http.server import HTTPServer

class HTTPServer(BaseHTTPServer.HTTPServer):

    _continue = True

    def serve_until_shutdown(self):
        while self._continue:
            self.handle_request()

    def shutdown(self):
        self._continue = False
        # We fire a last request at the server in order to take it out of the
        # while loop in `self.serve_until_shutdown`.
        try:
            urllib2.urlopen(
                'http://%s:%s/' % (self.server_name, self.server_port))
        except urllib2.URLError:
            # If the server is already shut down, we receive a socket error,
            # which we ignore.
            pass
        self.server_close()

