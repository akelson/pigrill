from flask import Flask
from flask import jsonify
import datetime
import time
from subprocess import Popen, PIPE
from igrill import IGrillV2Peripheral
import json

class Server(object):
    def __init__(self):
        self.periph = None
        self.scan_proc = None
        self.scan_ret = {"status":"not_started"}
        self.device_prefrences = {}
        self.last_read_time = None
        self.last_sensor_data = {}

    def scan(self):
        if self.scan_proc == None:
            self.scan_proc = Popen(
                ["sudo", "/usr/bin/python", "scanner.py"],
                stdout=PIPE, stderr=PIPE)
            self.scan_ret = {"status":"running"}
        return "ok"

    def devices(self):
        if self.periph:
            addr = self.periph.addr
            if addr in self.device_prefrences:
                name = self.device_prefrences[addr]["name"]
            else:
                name = "Unknown Device"
            return jsonify([{"name" : name, "addr" : addr}])
        else:
            return jsonify([])
        
    def scan_result(self):
        if self.scan_proc and None != self.scan_proc.poll():
            scan_ret, err = self.scan_proc.communicate()
            self.scan_ret = json.loads(scan_ret)

            devices = {}
            for device in self.scan_ret["devices"]:
                for scan_item in device["scan_data"]:
                    if "Short Local Name" == scan_item[1]:
                        addr = device["addr"]
                        name = scan_item[2]
                        devices[addr] = name

            for (adddr, name) in devices.items():
                if not addr in self.device_prefrences:
                    self.device_prefrences[addr] = {"name" : name}
                        
            print err
            self.scan_proc = None
        return jsonify(self.scan_ret)

    def connect(self, addr):
        self.periph = IGrillV2Peripheral(addr)
        return "ok"

    def disconnect(self):
        if self.periph:
            # There seems to be a race condition where calling disconnect to soon
            # after reading characteristics causes an error.
            time.sleep(5);
            self.periph.disconnect()
            self.periph = None
            self.last_sensor_data = {}
        return "ok"

    def sensor_data(self):
        now = datetime.datetime.now()
        if None == self.last_read_time:
            self.last_read_time = now
        min_delta = datetime.timedelta(seconds=1)
        delta = now - self.last_read_time

        if self.periph and delta > min_delta:
            self.last_read_time = now 
            self.last_sensor_data = {
                'time' : str(datetime.datetime.now()),
                'temperature': self.periph.read_temperature(),
                'battery': self.periph.read_battery()}

        return jsonify(self.last_sensor_data)

if __name__ == "__main__":
    server = Server()
    print server.scan()

    app = Flask(__name__)

    @app.route('/')
    def index():
        with open("html/index.html", "r") as f:
            return f.read()
        
    @app.route('/scan')
    def scan():
        return server.scan()

    @app.route('/scan_result')
    def scan_result():
        return server.scan_result()

    @app.route('/devices')
    def devices():
        return server.devices()

    @app.route('/connect/<addr>')
    def connect(addr):
        return server.connect(addr)

    @app.route('/disconnect')
    def disconnect():
        return server.disconnect()

    @app.route('/sensor_data')
    def sensor_data():
        return server.sensor_data()

    app.run(debug=False, host="0.0.0.0")
