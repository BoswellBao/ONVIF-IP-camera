#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#

def wrap_param_with_ns(ns, params):
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
    'imaging': '/Imaging'
}

service_version = {
    'Major': 2,
    'Minor': 20
}

namespace_map = {
    'device': 'http://www.onvif.org/ver10/device/wsdl',
    'media': 'http://www.onvif.org/ver10/media/wsdl',
    'event': 'http://www.onvif.org/ver10/events/wsdl',
    'analytics': 'http://www.onvif.org/ver20/analytics/wsdl',
    'imaging': 'http://www.onvif.org/ver20/imaging/wsdl'
}


device_information = {'Manufacturer': 'GOSUN',
                'FirmwareVersion': 'V1.0.0 build 1314',
                'Model': 'GS-TEST-DaShen01',
                'SerialNumber': '000000000000'}

##################### Camera Capabilities  #####################
device_capabilties = {
    'Network': {
        'IPFilter': True,
        'IPVersion6': False,
        'ZeroConfiguration': False,
        'DynDNS':True,
    },
    'System': {
        'DiscoveryResolve': False,
        'DiscoveryBye': True,
        'RemoteDiscovery': False,
        'SystemBackup': False,
        'FirmwareUpgrade': False,
        'SystemLogging': False,
    },
    'Security': {
        'AccessPolicyConfig': False,
        'DefaultAccessPolicy': False,
        'X.509Token': False,
        'SAMLToken': False,
        'KerberosToken': False,
        'RELToken': False,
        'SupportedEAPMethod': False,
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
    }
}

event_capabilities = {
    'WSSubscriptionPolicySupport': True,
    'WSPullPointSupport': True,
    'WSPausableSubscriptionManagerInterfaceSupport': False
}

imaging_capabilities = {}

