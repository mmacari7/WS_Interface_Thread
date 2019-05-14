from __future__ import print_function
import json
import argparse
import datetime
import os
import threading
import base64
import sys
from time import sleep

try:
    import websocket
except:
    print("Error importing websocket")
    sys.exit(1)

#Class to establish loop connection to websocket
class Client:
    def __init__(self, url, json_dir):
        # Start the web-socket service
        print("Connecting to: ", url)
        self.ws = websocket.WebSocketApp(
            url,
            on_open=lambda ws: self.on_open(ws),
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_close=lambda ws: self.on_close(ws)
        )

        # Sets variables for JSON log
        self.json_dir = json_dir
        self.json_log = None

        # Open json file for writing
        self.open_json()

        # Starts a thread on the web-socket, tells it to run forever
        # Attempting to start thread
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        print("Started connection thread")


    # On open function
    # Send command via API to get data
    def on_open(self, ws):
        print("Opening Connection")
        self.ws.send(json.dumps({"command": "xxxxxxxxx", "id": "xxxxxxxxxxx"}))
        return

    # On message function
    def on_message(self, ws, message):
        data = json.loads(message)
        json.dump(data, self.json_log)
        print(list(data.keys()))
        self.json_log.write('\n')
        return

    # On web-socket close
    def on_close(self, ws):
        if(self.json_log):
            print("Closing JSON Log")
            self.close_json()
        print("Closing Connection")
        return

    # Open JSON File
    def open_json(self):
        if(self.json_log == None):
            fn = "{}_targetCandidate_log.json".format(datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M_%S"))
            if(not os.path.isdir(self.json_dir)):
                os.makedirs(self.json_dir)
            path = os.path.join(self.json_dir, fn)
            self.json_log = open(path, "w+")
            print("JSON file opened, writing to: " + path)

        return

    # Function to close JSON file
    def close_json(self):
        self.json_log.close()
        return

    def start(self):
        if(not websocket):
            print("Error: websocket-client is required. Install using 'pip install websocket-client' or see 'https://github.com/websocket-client/websocket-client")
            exit(1)

        conn_timeout = 15
        while not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1

        if(conn_timeout):
            print("Connected")
        msg_count = 0
        sleep(1)

        try:
            while(self.ws.sock.connected):
                self.ws.send(json.dumps({"command": "xxxxxx", "xxxxxxxx": {"videoBandWidthLimit": xxxxxx}}))
                sleep(1)
                msg_count += 1
        except KeyboardInterrupt:
            self.ws.close()
        return


# Adds arguments for cmd execution
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="ip address or hostname of device", default="xxxxxxxxxx")
parser.add_argument("--json_dir", help="directory to save json data", default=".\\xxxxxxxx")
parser.add_argument("--port", help="port used to connect to api", type=int, default=xxxx)
parser.add_argument("--endpoint", help="api endpoint", default="xxxxxxx")
args = parser.parse_args()

# Set URL to arguments for websocket connection
url = "ws://{}:{}/{}".format(args.host, args.port, args.endpoint)

c = Client(url, args.json_dir)
c.start()

