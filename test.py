"""HTTP server main."""

import sys
import time
import tornado
from tornado.web import stream_request_body, RequestHandler
from tornado.ioloop import IOLoop
import os

DELAY = float(os.environ.get("DELAY", 0.1))

@stream_request_body
class UploadHandler(RequestHandler):
    """Tasks API request handler"""

    def __init__(self, application, request, **kwargs):
        self.received = 0
        self.request_started = None
        self.chunks = 0
        super(UploadHandler, self).__init__(application, request, **kwargs)

    def post(self):
        self.chunks = 0
        self.received = 0
        self.request_started = None
        print "Done"

    def data_received(self, data):
        time.sleep(DELAY)
        self.chunks += 1
        self.received += len(data)
        if self.request_started:
            print self.chunks, time.time() - self.request_started, self.received
        else:
            self.request_started = time.time()

def main():
    """main entry point to http api"""

    app = tornado.web.Application([
        (r"/api/upload", UploadHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
