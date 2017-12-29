#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
import random
from onvifserver.server import OnvifServer, Fault, OnvifServerError
from ipc_params import *


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
            'event': '{}/Events'.format(root_path),
            'analytics': '{}/Analytics'.format(root_path),
            'imaging': '{}/Imaging'.format(root_path)
        }


    def get_device_information(self, *args, **kwgs):
        '''
        GetDeviceInformation
        '''
        seeds = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        serial_number = ''.join(random.sample(seeds, 12))
        device_info = wrap_param_with_ns('tds', device_information)
        device_info['tds:SerialNumber'] = serial_number
        return device_info


    def get_capabilities(self, *args, **kwgs):
        '''GetCapabilities'''
        if 'Category' not in args[0]:
            raise OnvifServerError('Category Not found')

        device_cap = wrap_param_with_ns('tt', device_capabilties)
        device_cap['tt:XAddr'] = self.service_addr['device']

        media_cap = wrap_param_with_ns('tt', media_capabilities)
        media_cap['tt:XAddr'] = self.service_addr['media']

        event_cap = wrap_param_with_ns('tt', event_capabilities)
        event_cap['tt:XAddr'] = self.service_addr['event']

        imaging_cap = wrap_param_with_ns('tt', imaging_capabilities)
        imaging_cap['tt:XAddr'] = self.service_addr['imaging']

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
        return {}


    def get_services(self, *args, **kwgs):
        ''' GetServices '''
        if 'IncludeCapability' not in args[0]:
            raise OnvifServerError('IncludeCapability not found')
        else:
            if args[0]['IncludeCapability'].lower() == 'true':
                include_cap = True
            else:
                include_cap = False
        service_list = []

        for server in self.service_addr:
            service = {}
            service['tds:Namespace'] = namespace_map[server]
            service['tds:XAddr'] = self.service_addr[server]
            service['tds:Capabilities'] = self._wrap_capability(eval(server+'_capabilities'))
            service['tds:Version'] = wrap_param_with_ns('tt', service_version)
            service_list.append({'tds:Service': service})
        return service_list

    def _wrap_capability(self, capabilities):
        return None


    def get_service_capabilities(self, *args, **kwgs):
        print(args, kwgs)
        return {}


class Media(object):
    ''' Media profile '''
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
