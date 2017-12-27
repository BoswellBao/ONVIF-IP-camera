#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
import random
from onvifserver.server import OnvifServer, Fault


class DeviceManagement(object):
    '''
    onvif server 设备管理相关功能
    '''
    def __init__(self, ip, port, ptz=False):
        self.ip = ip
        self.port = port
        self.ptz = ptz
        if self.port == 80:
            root_path = "{}/onvif".format(self.ip)
        else:
            root_path = "{0}:{1}/onvif".format(self.ip, self.port)
        
        self.service_addr = {
            'device': '{}/device_service'.format(root_path),
            'media': '{}/Media'.format(root_path),
            'event': '{}/Event'.format(root_path),
            'analytics': '{}/Analytics'.format(root_path),
            'imaging': '{}/Imaging'.format(root_path)
        }

    def get_device_information(self, *args, **kwgs):
        '''
        GetDeviceInformation
        '''
        seeds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        serial_number = ''.join(random.sample(seeds, 12))
        device_info = {'tds:Manufacturer': 'GOSUN',
                        'tds:Firmware_Version': 'V5.4.0 build 160613',
                        'tds:Model': 'GS-TEST-DaShen01',
                        'tds:SerialNumber': serial_number}
        return device_info

    def get_capabilities(self, *args, **kwgs):
        '''GetCapabilities'''
        device_cap = {
            'tt:XAddr':self.service_addr['device'],
            'tt:Network': {
                'tt:IPFilter': True,
                'tt:IPVersion6': False,
                'tt:ZeroConfiguration': False,
                'tt:DynDNS':True,
            },
            'tt:System': {
                'tt:DiscoveryResolve': False,
                'tt:DiscoveryBye': True,
                'tt:RemoteDiscovery': False,
                'tt:SystemBackup': False,
                'tt:FirmwareUpgrade': False,
                'tt:SystemLogging': False,
            },
            'tt:Security': {
                'tt:AccessPolicyConfig': False,
                'tt:DefaultAccessPolicy': False,
                'tt:X.509Token': False,
                'tt:SAMLToken': False,
                'tt:KerberosToken': False,
                'tt:RELToken': False,
                'tt:SupportedEAPMethod': False,
                'tt:RemoteUserHandling': False
            },
            'tt:IO': {
                'tt:InputConnectors':2,
                'tt:RelayOutputs': 0
            }
        }

        media_cap = {
            'tt:XAddr':self.service_addr['media'],
            'tt:StreamingCapabilities': {
                'tt:RTPMulticast': False,
                'tt:RTP_TCP': True,
                'tt:RTP_RTSP_TCP': True
            }
        }

        event_cap = {
            'tt:XAddr':self.service_addr['event'],
            'tt:WSSubscriptionPolicySupport': True,
            'tt:WSPullPointSupport': True,
            'tt:WSPausableSubscriptionManagerInterfaceSupport': False
        }

        imaging_cap = {
            'tt:XAddr':self.service_addr['imaging']
        }

        if args[0]['Category'].lower() == 'all':
            capabilities = {
                'tds:Capabilities': {
                    'tt:Device': device_cap,
                    'tt:Events': event_cap,
                    'tt:Imaging': imaging_cap,
                    'tt:Media': media_cap,
                }}
        else:
            pass    # Todo: error process
        return capabilities

    def get_system_date_and_time(self, *args, **kwgs):
        '''GetSystemDateAndTime'''
        return None

    def get_services(self, *args, **kwgs):
        return None

    def get_service_capabilities(self, *args, **kwgs):
        print(args, kwgs)
        return None


class Media(object):
    pass


class OnvifIPC(object):
    '''
    onvif摄像机类
    '''
    def __init__(self, ip, port):
        '''
        a tuple of IP and port, eg: ("192.168.1.9", 8000)
        '''
        with OnvifServer((ip, port)) as self.server:
            self.server.register_instance(DeviceManagement(ip, port), "/onvif/device_service")
            self.server.serve_forever()



if __name__ == '__main__':
    OnvifIPC("192.168.1.9", 8000)
