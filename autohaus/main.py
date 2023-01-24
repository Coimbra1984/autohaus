import flask
import argparse
import urllib.parse
import autohaus
from threading import Thread
import time
import sys
import threading
from werkzeug.serving import make_server

app = flask.Flask("autohaus-server")

class ServerThread(threading.Thread):

    def __init__(self, app, host, port):
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

parser = argparse.ArgumentParser(description='Autohaus server')
parser.add_argument('--port', type=int, default=5001)
parser.add_argument('--host', type=str, default="127.0.0.1")
parser.add_argument('--restBasePath', type=str, default="/autohaus/api/v1.0/")

args = parser.parse_args()

def doStop(delay):
    print("exiting in %d seconds"%delay)
    time.sleep(delay)
    global server
    server.shutdown()

@app.route(urllib.parse.urljoin(args.restBasePath, 'stop'), methods=['POST'])
def stop():
    thread = Thread(target=doStop, args=(1,))
    thread.start()
    return flask.jsonify({"success": True}), 200

@app.route(urllib.parse.urljoin(args.restBasePath, 'version'), methods=['GET'])
def version():
    autohaus
    return flask.jsonify({"version": autohaus.__version__}), 200

if __name__ == '__main__':
    # app.run(debug=False, port=args.port, host=args.host)
    server = ServerThread(app, port=args.port, host=args.host)
    server.start()