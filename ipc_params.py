#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

def wrap_param_with_ns(ns, params):
    ''' 给参数封装namespace '''
    if not isinstance(params, dict):
        raise ValueError()
    new = {}
    for key in params:
        ns_key = '{0}:{1}'.format(ns, key)
        if isinstance(params[key], dict):
            new[ns_key] = wrap_param_with_ns(ns, params[key])
        else:
            new[ns_key] = params[key]
    return new


##################### service map  #####################
service_addr = {
    'device': '/device_service',
    'media': '/Media',
    'event': '/Events',
    'analytics': '/Analytics',
    'imaging': '/Imaging',
    'deviceio': '/DeviceIo'
}

service_version = {
    'Major': 2,
    'Minor': 20
}

namespace_map = {
    'device': ('tds', 'http://www.onvif.org/ver10/device/wsdl'),
    'media': ('trt', 'http://www.onvif.org/ver10/media/wsdl'),
    'event': ('tev', 'http://www.onvif.org/ver10/events/wsdl'),
    'analytics': ('tan', 'http://www.onvif.org/ver20/analytics/wsdl'),
    'imaging': ('timg', 'http://www.onvif.org/ver20/imaging/wsdl')
}


##################### Camera Capabilities  #####################
device_capabilities = {
    'Network': {
        'IPFilter': True,
        'IPVersion6': False,
        'ZeroConfiguration': False,
        'DynDNS':True,
    },
    'System': [
        {'DiscoveryResolve': False},
        {'DiscoveryBye': True},
        {'RemoteDiscovery': False},
        {'SystemBackup': False},
        {'FirmwareUpgrade': True},
        {'SystemLogging': False},
        {'SupportedVersions':{
            'Major': 2,
            'Minor': 60,
        }},
        {'SupportedVersions':{
            'Major': 2,
            'Minor': 40,
        }},
        {'SupportedVersions':{
            'Major': 2,
            'Minor': 20,
        }},
        {'SupportedVersions':{
            'Major': 2,
            'Minor': 10,
        }},
        {'SupportedVersions':{
            'Major': 2,
            'Minor': 0,
        }},
    ],
    'Security': {
        'TLS1.1': False,
        'TLS1.2': False,
        'OnboardKeyGeneration': False,
        'AccessPolicyConfig': False,
        'DefaultAccessPolicy': False,
        'X.509Token': False,
        'SAMLToken': False,
        'KerberosToken': False,
        'RELToken': False,
        'SupportedEAPMethod': 0,
        'RemoteUserHandling': False
    },
    'IO': {
        'InputConnectors':2,
        'RelayOutputs': 0
    }
}

media_capabilities = {
    'StreamingCapabilities': {
        'RTPMulticast': False,
        'RTP_TCP': True,
        'RTP_RTSP_TCP': True
    },
    'Extension':{
        'ProfileCapabilities':{
            'MaximumNumberOfProfiles': 3
        }
    }
}

event_capabilities = {
    'WSSubscriptionPolicySupport': True,
    'WSPullPointSupport': True,
    'WSPausableSubscriptionManagerInterfaceSupport': False
}

imaging_capabilities = {}

analytics_capabilities = {
    'RuleSupport': True,
    'AnalyticsModuleSupport': True
}

deviceio_capcabilities = {
    'VideoSources': 1,
    'VideoOutputs': 0,
    'AudioSources': 0,
    'AudioOutputs': 0,
    'RelayOutputs': 0
}


############### System config ###########

device_information = {'Manufacturer': 'GOSUN',
                'FirmwareVersion': 'V1.0.0 build 180102',
                'Model': 'GS-TEST-DaShen01',
                'SerialNumber': '000000000000'}

time_setting = {
    'DateTimeType': 'Manual',
    'DaylightSavings': False,
    'TimeZone': {'TZ': 'GMT+08:00'}
}

############# Media Profiles ##############
