#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
import random
import sqlite3
import datetime
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
            'device': 'http://{}/device_service'.format(root_path),
            'media': 'http://{}/Media'.format(root_path),
            'event': 'http://{}/Events'.format(root_path),
            'imaging': 'http://{}/Imaging'.format(root_path),
            'analytics': 'http://{}/Analytics'.format(root_path),
            'deviceio': 'http://{}/DeviceIo'.format(root_path)
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

        device_cap = wrap_param_with_ns('tt', device_capabilities)
        device_cap['tt:XAddr'] = self.service_addr['device']

        media_cap = wrap_param_with_ns('tt', media_capabilities)
        media_cap['tt:XAddr'] = self.service_addr['media']

        event_cap = wrap_param_with_ns('tt', event_capabilities)
        event_cap['tt:XAddr'] = self.service_addr['event']

        imaging_cap = wrap_param_with_ns('tt', imaging_capabilities)
        imaging_cap['tt:XAddr'] = self.service_addr['imaging']

        deviceio_cap = wrap_param_with_ns('tt', deviceio_capcabilities)
        deviceio_cap['tt:XAddr'] = self.service_addr['deviceio']

        if args[0]['Category'].lower() == 'all':
            capabilities = {
                'tds:Capabilities': {
                    'tt:Device': device_cap,
                    'tt:Events': event_cap,
                    'tt:Media': media_cap,
                    'tt:Imaging': imaging_cap,
                    'tt:Extension':{
                        'tt:DeviceIO': deviceio_cap
                    }
                }}
        else:
            pass    # Todo: error process
        return capabilities

    def get_system_date_and_time(self, *args, **kwgs):
        '''GetSystemDateAndTime'''
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        time_setting['UTCDateTime'] = {
            'Time':{
                'Hour': utc_now.hour,
                'Minute': utc_now.hour,
                'Second': utc_now.second
            },
            'Date':{
                'Year': utc_now.year,
                'Month': utc_now.month,
                'Day': utc_now.day
            }
        }
        time_setting['LocalDateTime'] = {
            'Time':{
                'Hour': now.hour,
                'Minute': now.hour,
                'Second': now.second
            },
            'Date':{
                'Year': now.year,
                'Month': now.month,
                'Day': now.day
            }
        }
        data_time = wrap_param_with_ns('tt', time_setting)
        return {'tds:SystemDateAndTime': data_time}

    def get_services(self, *args, **kwgs):
        ''' GetServices '''
        print('****************')
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
            service['tds:Namespace'] = namespace_map[server][1]
            service['tds:XAddr'] = self.service_addr[server]
            service['tds:Capabilities'] = self._wrap_capability(namespace_map[server][0], eval(server+'_capabilities'))
            service['tds:Version'] = wrap_param_with_ns('tt', service_version)
            service_list.append({'tds:Service': service})
        return {'NO_WRAP': service_list}

    def _wrap_capability(self, ns, capabilities, cap_name='Capabilities'):
        cap_with_attr = '{0}:{1}'.format(ns, cap_name)
        capability = {}
        has_sub_dict = False
        for cap in capabilities:
            if not isinstance(capabilities[cap], dict):
                if isinstance(capabilities[cap], bool):
                    cap_with_attr = '{0} {1}="{2}"'.format(cap_with_attr, cap, str(capabilities[cap]).lower())
            else:
                has_sub_dict = True

        if has_sub_dict:
            sub_cap = {}
            for cap in capabilities:
                if isinstance(capabilities[cap], dict):
                    sub_cap.update(self._wrap_capability(ns, capabilities[cap], cap))
            return{cap_with_attr: sub_cap}
        else:
            return {cap_with_attr: None}


    def get_service_capabilities(self, *args, **kwgs):
        print(args, kwgs)
        return {}


class Media(object):
    ''' Media profile '''
    def get_profiles(self):
        ''' GetProfiles '''
        pass


class OnvifIPC(object):
    '''
    onvif摄像机类
    '''
    def __init__(self, ip, port, ptz=False):
        '''
        a tuple of IP and port, eg: ("192.168.1.9", 8080)
        '''
        with OnvifServer((ip, port)) as self.server:
            self.server.register_instance(DeviceManagement(ip, port), "/onvif/device_service")
            self.server.register_instance(Media(), "onvif/Media")
            self.server.serve_forever()

if __name__ == '__main__':
    OnvifIPC("192.168.1.9", 8000)
