from onvifserver.server import OnvifServer

def get_device_info_function(params):
    device_info = {'manufacturer': 'GOSUN',
                    'Firmware_Version': 'V5.4.0 build 160613',
                    'Model': 'DS-2DE72XYZIW-ABC/VS',
                    'SerialNumber': '00408C1836B2'}
    return device_info



if __name__ == '__main__':
    with OnvifServer(("192.168.1.9", 8000)) as server:
        server.register_function(get_device_info_function, "GetDeviceInformation")
        server.serve_forever()
