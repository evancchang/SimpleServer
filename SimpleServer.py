#python3
import http.server

import sys
import logging
import cgi

import os
import json

# From http://watson-http.readthedocs.org/en/latest/_modules/watson/http/wsgi.html
def read_binary(self):
    """Override for FieldStorage.read_binary method.

    Existing FieldStorage method raises a "TypeError: must be str, not bytes"
    when CONTENT_LENGTH is specified for a body that isn't key=value pairs.
    Decoding the data into the relevant encoding resolves the issue.
    """
    self.file = self.make_file()
    todo = self.length
    if todo >= 0:
        while todo > 0:
            data = self.fp.read(min(todo, self.bufsize)) # bytes
            if not isinstance(data, bytes):
                raise ValueError("%s should return bytes, got %s"
                                 % (self.fp, type(data).__name__))
            self.bytes_read += len(data)
            if not data:
                self.done = -1
                break
            data = data.decode(self.encoding)  # The fix
            self.file.write(data)
            todo = todo - len(data)

cgi.FieldStorage.read_binary = read_binary

class MyHandler(http.server.SimpleHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        print("send header")
        self.send_response(201)
        self.end_headers()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        print(form)
        print(form.value)

    def do_GET(self):
        http.server.SimpleHTTPRequestHandler.do_GET(self)

def test(HandlerClass = MyHandler,
         ServerClass = http.server.HTTPServer):
    http.server.test(HandlerClass, ServerClass, port=8080)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage SimpleServer.py [port]")
        sys.exit()
    test()
