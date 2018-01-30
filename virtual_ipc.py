#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
import random
import datetime
import re
import threading
from onvifserver.server import OnvifServer, OnvifServerError
from onvifserver import utils
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
            root_path = "http://{}".format(self.ip)
        else:
            root_path = "http://{0}:{1}".format(self.ip, self.port)
        self.service_addr = {}
        for server in utils.service_addr:
            self.service_addr[server] = '{0}{1}'.format(root_path, utils.service_addr[server])

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
        '''
        GetCapabilities
        '''
        if 'Category' not in kwgs['BODY']:
            raise OnvifServerError('Category Not found')

        device_cap = wrap_param_with_ns('tt', device_capabilities)
        device_cap['tt:XAddr'] = self.service_addr['device']

        media_cap = wrap_param_with_ns('tt', media_capabilities)
        media_cap['tt:XAddr'] = self.service_addr['media']

        event_cap = wrap_param_with_ns('tt', event_capabilities)
        event_cap['tt:XAddr'] = self.service_addr['event']

        imaging_cap = wrap_param_with_ns('tt', imaging_capabilities)
        imaging_cap['tt:XAddr'] = self.service_addr['imaging']

        deviceio_cap = wrap_param_with_ns('tt', deviceio_capabilities)
        deviceio_cap['tt:XAddr'] = self.service_addr['deviceio']

        if kwgs['BODY']['Category'].lower() == 'all':
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
        elif kwgs['BODY']['Category'].lower() == 'media':
            capabilities = {
                'tds:Capabilities': {
                    'tt:Media': media_cap,
                }
            }
        else:
            pass    # Todo: error process
        return capabilities

    def get_system_date_and_time(self, *args, **kwgs):
        '''
        GetSystemDateAndTime
        '''
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
        '''
        GetServices
        '''
        if 'IncludeCapability' not in kwgs['BODY']:
            raise OnvifServerError('IncludeCapability not found')
        else:
            if kwgs['BODY']['IncludeCapability'].lower() == 'true':
                include_cap = True
            else:
                include_cap = False

        service_list = []
        for server in self.service_addr:
            service = {}
            service['tds:Namespace'] = utils.namespace_map[server][1]
            service['tds:XAddr'] = self.service_addr[server]
            if include_cap:
                service['tds:Capabilities'] = self._wrap_capability(utils.namespace_map[server][0], eval(server+'_capabilities'))
            service['tds:Version'] = wrap_param_with_ns('tt', utils.service_version)
            service_list.append({'tds:Service': service})
        return {'NO_WRAP': service_list}

    def _wrap_capability(self, ns, capabilities, cap_name='Capabilities'):
        '''
        将能力集封装为xml节点属性
        '''
        cap_with_attr = '{0}:{1}'.format(ns, cap_name)
        capability = {}
        has_sub_dict = False
        attri_dict = {}
        for cap in capabilities:
            if not isinstance(capabilities[cap], dict):
                attri_dict[cap] = capabilities[cap]
            else:
                has_sub_dict = True
        capability['ATTRI'] = attri_dict

        # 对子集循环迭代
        if has_sub_dict:
            for cap in capabilities:
                if isinstance(capabilities[cap], dict):
                    capability.update(self._wrap_capability(ns, capabilities[cap], cap))
        return {cap_with_attr: capability}

    # Todo
    def get_service_capabilities(self, *args, **kwgs):
        print(args, kwgs)
        return {}


class Media(object):
    '''
    Media profile
    '''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_profiles(self, **kwgs):
        '''
        GetProfiles
        '''
        profile1 = wrap_param_with_ns('tt', media_profile1)
        profile2 = wrap_param_with_ns('tt', media_profile2)
        profile_list = [
            {'trt:Profiles': profile1},
            {'trt:Profiles':profile2},
            ]
        return {'NO_WRAP': profile_list}

    def get_stream_uri(self, **kwgs):
        '''
        GetStreamUri
        '''
        stream_type = kwgs['BODY']['StreamSetup']['Stream']
        protocol = kwgs['BODY']['StreamSetup']['Transport']['Protocol']
        print(stream_type, protocol)
        if stream_type != 'RTP-Unicast' or protocol != 'UDP':
            raise OnvifServerError('Only RTP-unicast and udp is supported')
        url = 'rtsp://{0}:554/media/video'.format(self.ip)
        stream_url_info = {
            'tt:Url': url,
            'tt:InvalidAfterConnect': False,
            'tt:InvalidAfterReboot': False,
            'tt:Timeout': 'PT100S'
        }

        return {'trt:MediaUri': stream_url_info}

    def get_video_encoder_configurations(self, **kwgs):
        ''' GetVideoEncoderConfigurations '''
        encoder1 = media_profile1['VideoEncoderConfiguration']
        encoder2 = media_profile2['VideoEncoderConfiguration']
        encoder_conf = [
            {'trt:Configurations': encoder1},
            {'trt:Configurations': encoder2}
        ]
        return {'NO_WRAP': encoder_conf}


class Events(object):
    '''
    告警与事件订阅模块
    '''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        if self.port == 80:
            root_path = "http://{}".format(self.ip)
        else:
            root_path = "http://{0}:{1}".format(self.ip, self.port)
        self.event_notify_add = '{0}/onvif/event_notify'.format(root_path)

    def subscribe(self, *args, **kwgs):
        '''
        告警订阅
        '''
        notify_address = kwgs['BODY']['ConsumerReference']['Address']
        sub_time = kwgs['BODY']['InitialTerminationTime']
        subscribe = re.findall(r"\d+\.?\d*", sub_time)[0]
        if sub_time[-1].lower() == 's':
            subscribe = int(subscribe)
        elif sub_time[-1].lower() == 'm':
            subscribe = int(subscribe) * 60
        elif sub_time[-1].lower() == 'h':
            subscribe = int(subscribe) * 3600

        ret_dict = {}
        ret_dict['wsnt:SubscriptionReference'] = {'wsa5:Address': self.event_notify_add}
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=subscribe)
        ret_dict['wsnt:CurrentTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        ret_dict['wsnt:TerminationTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        return ret_dict


class OnvifIPC(object):
    '''
    onvif摄像机, 实现一个虚拟的onvif摄像机业务
    OnvifIPC("192.168.1.9", 8000)
    '''
    def __init__(self, ip, port, ptz=False):
        '''
        a tuple of IP and port, eg: ("192.168.1.9", 8080)
        '''
        with OnvifServer((ip, port)) as server:
            server.register_instance(DeviceManagement(ip, port), utils.service_addr['device'])
            server.register_instance(Media(ip, port), utils.service_addr['media'])
            server.register_instance(Events(ip, port), utils.service_addr['event'])
            server.serve_forever()

if __name__ == '__main__':
    OnvifIPC("192.168.1.9", 8001)
