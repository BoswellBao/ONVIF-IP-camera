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
        if key == 'ATTRI':
            continue
        ns_key = '{0}:{1}'.format(ns, key)
        if isinstance(params[key], dict):
            new[ns_key] = wrap_param_with_ns(ns, params[key])
        else:
            new[ns_key] = params[key]
    return new


##################### Camera Capabilities  #####################
device_capabilities = {
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
        'FirmwareUpgrade': True,
        'SystemLogging': False,
    },
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
    'ProfileCapabilities':{
        'MaximumNumberOfProfiles': 3
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

deviceio_capabilities = {
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

media_profile1 = {
    'ATTRI': {
        'fixed': True,
        'token': 'Profile1',
    },
    'Name': 'Profile1',
    'VideoSourceConfiguration': {
        'ATTRI': {
            'xsi:type': 'tt:VideoSourceConfiguration',
            'token': 'video_source_config'
        },
        'Name': 'video_source_config',
        'UseCount': 2,
        'SourceToken': 'video_source',
        'Bounds':{
            'ATTRI': {
                'height': 1080,
                'width': 1920,
                'y': 1,
                'x': 1
            }
        }
    },
    'VideoEncoderConfiguration':{
        'ATTRI': {
            'xsi:type': "tt:VideoEncoderConfiguration",
            'token': "video_encoder_Main"
        },
        'Name': 'video_encoder_Main',
        'UseCount': 2,
        'Encoding': 'H264',
        'Resolution': {
            'Width': 1920,
            'Height': 1080,
        },
        'Quality': 4,
        'RateControl': {
            'FrameRateLimit': 25,
            'EncodingInterval': 1,
            'BitrateLimit': 4096,
        },
        'H264': {
            'GovLength': 50,
            'H264Profile': 'High'
        },
        'Multicast': {
            'Address': {
                'Type': 'IPv4',
                'IPv4Address': '0.0.0.0',
            },
            'Port': 0,
            'TTL': 3,
            'AutoStart': False,
        },
        'SessionTimeout': 'PT60S',
    }
}

media_profile2 = {
    'ATTRI': {
        'fixed': True,
        'token': 'Profile2',
    },
    'Name': 'Profile2',
    'VideoSourceConfiguration': {
        'ATTRI': {
            'xsi:type': 'tt:VideoSourceConfiguration',
            'token': 'video_source_config'
        },
        'Name': 'video_source_config',
        'UseCount': 2,
        'SourceToken': 'video_source',
        'Bounds':{
            'ATTRI': {
                'height': 1080,
                'width': 1920,
                'y': 1,
                'x': 1
            }
        }
    },
    'VideoEncoderConfiguration':{
        'ATTRI': {
            'xsi:type': "tt:VideoEncoderConfiguration",
            'token': "video_encoder_substream"
        },
        'Name': 'video_encoder_substream',
        'UseCount': 2,
        'Encoding': 'H264',
        'Resolution': {
            'Width': 1080,
            'Height': 720,
        },
        'Quality': 4,
        'RateControl': {
            'FrameRateLimit': 25,
            'EncodingInterval': 1,
            'BitrateLimit': 2018,
        },
        'H264': {
            'GovLength': 50,
            'H264Profile': 'High'
        },
        'Multicast': {
            'Address': {
                'Type': 'IPv4',
                'IPv4Address': '0.0.0.0',
            },
            'Port': 0,
            'TTL': 3,
            'AutoStart': False,
        },
        'SessionTimeout': 'PT60S',
    }
}
