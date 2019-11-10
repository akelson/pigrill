import bluepy.btle as btle
import json
import datetime

if __name__ == "__main__":
    scan_result = {}

    try:
        scanner = btle.Scanner()
        devices = scanner.scan(10.0)
        scan_result['devices'] = []
        scan_result['start_time'] = str(datetime.datetime.now()),
        for device in devices:
            device_info = {}
            device_info['addr'] = device.addr
            device_info['scan_data'] = device.getScanData()
            scan_result['devices'].append(device_info)
        scan_result['end_time'] = str(datetime.datetime.now()),
        scan_result['status'] = "complete"
    except Exception as e:
        print e
        scan_result['status'] = "failed"

    print json.dumps(scan_result)
