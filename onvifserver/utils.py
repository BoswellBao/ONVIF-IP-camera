#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
from lxml import etree
import re

# onvif soap namespace defined in <ONVIF-Core-Specification> chap5.3
ns_soap = {
    'tt': 'http://www.onvif.org/ver10/schema',
    'tds': 'http://www.onvif.org/ver10/device/wsdl',
    'trt': 'http://www.onvif.org/ver10/media/wsdl',
    'tev': 'http://www.onvif.org/ver10/events/wsdl',
    'ter': 'http://www.onvif.org/ver10/error',
    'dn': 'http://www.onvif.org/ver10/network/wsdl',
    'tns1': 'http://www.onvif.org/ver10/topics',
    # standard namespace
    'wsdl': 'http://schemas.xmlsoap.org/wsdl/',
    'wsoap12': 'http://schemas.xmlsoap.org/wsdl/soap12/',
    'http': 'http://schemas.xmlsoap.org/wsdl/http/',
    'soapenc': 'http://www.w3.org/2003/05/soap-encoding',
    'soapenv': 'http://www.w3.org/2003/05/soap-envelope',
    'xs': 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'd': 'http://schemas.xmlsoap.org/ws/2005/04/discovery',
    'wsadis': 'http://schemas.xmlsoap.org/ws/2004/08/addressing',
    'wsa': 'http://www.w3.org/2005/08/addressing',
    'wstop': 'http://docs.oasis-open.org/wsn/t-1',
    'wsnt': 'http://docs.oasis-open.org/wsn/b-2',
    'xop': 'http://www.w3.org/2004/08/xop/include'
}

bool_map = {
    True: 'true',
    False: 'false'
}

def soap_encode(params, method, path):
    '''
    构造并返回soap消息体
        params: 要封装的参数，字典形式，如下, 
        字典的值可以是一个列表，但是最小单元必须是一个字典：
            'tds:capcabilities':{
                'tt:device':{
                    'tt:xaddr': 'device_services',
                    'tt:network': 'IPV6',
                    'tt:system': 'discovery'
                },
                'tt:events':{
                    'tt:xaddr': 'Events',
                    'tt:WSSubscriptionPolicySupport': True,
                    'tt:WSPullPointSupport': False
                },
                'tt:Media':{
                    'tt:XAddr': 'Media',
                    'tt:RTPMulticast': True,
                    'tt:RTP_RTSP_TCP':True
                },
                'respon':[
                    {'server': '123'},
                    {'server': '345'},
                    {'server': '789'}
                ]
                'tt:imaging': None
            }}

        method:
            请求的方法名，如GetCapabilities
        path:
            请求路径
    '''
    response_method = '{0}Response'.format(method)
    if path == '/onvif/device_service':
        ns = 'tds'
    elif path == '/onvif/media':
        ns = 'trt'
    return _wrap_soap_message(ns, response_method, params)

def soap_decode(data):
    '''
    解析客户端的请求消息的操作名称与参数
    '''
    soapenv = etree.fromstring(data)
    method = soapenv[0][0]
    method_name = _get_node_tag(method)
    if len(method)>0:
        params = _get_method_params(method)
    else:
        params = {}
    return method_name, params

def _get_method_params(parent_node):
    '''
    解析参数信息，将参数打包为一个列表返回。
    return value:
        [{'Category': 'All'}]
        [{'IncludeCapability': 'true'}]
    '''
    params_list = []
    for param in parent_node:
        tmp_dict = {}
        param_name = _get_node_tag(param)
        if len(param) > 0:
            sub_param = _get_method_params(param)   # recursively phrase sub node
            sub_param_name = _get_node_tag(param)
            tmp_dict[sub_param_name] = sub_param
        else:
            if param.text:
                tmp_dict[param_name] = param.text
        params_list.append(tmp_dict)
    return params_list

def _get_node_tag(node):
    '''
    解析出xml节点tag，过滤掉其namespace
    '''
    pattern = r'[^{}]+(?={|$)'
    return re.findall(pattern, node.tag)[0]


def _wrap_soap_message(ns, response_method, params):
    '''封装soap消息'''
    header = _wrap_soap_head()
    param = _wrap_params(params)
    body = '''<{0}:{1}>{2}</{0}:{1}>'''.format(ns, response_method, param)
    return '''{0}{1}</SOAP-ENV:Body></SOAP-ENV:Envelope>'''.format(header, body)


def _wrap_soap_head():
    '''封装soap namespace'''
    response_soap_header = r'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"'''
    for ns in ns_soap:
        ns_string = ''' xmlns:{0}="{1}"'''.format(ns, ns_soap[ns])
        response_soap_header += ns_string
    return '{0}><SOAP-ENV:Body>'.format(response_soap_header)


def _wrap_params(params):
    ''' 封装参数 '''
    body = ''
    for key in params:
        if isinstance(params[key], dict):
            sub_node = _wrap_params(params[key])
            body = '''{0}<{1}>{2}</{1}>'''.format(body, key, sub_node)
        elif isinstance(params[key], list):
            list_node = ''
            for item in params[key]:
                list_node += _wrap_params(item)
            body = '''{0}<{1}>{2}</{1}>'''.format(body, key, list_node)
        else:
            if isinstance(params[key], bool):
                params[key] = bool_map[params[key]]
            if params[key] is None:
                body = '''{0}<{1}/>'''.format(body, key)
            else:
                body = '''{0}<{1}>{2}</{1}>'''.format(body, key, params[key])
    return body


if __name__ == '__main__':
    test_dict = {
        'capcabilities':{
            'device':{
                'xaddr': 'device_services',
                'network': 'IPV6',
                'system': 'discovery'
            },
            'events':{
                'xaddr': 'Events',
                'WSSubscriptionPolicySupport': True,
                'WSPullPointSupport': False
            },
            'Media':{
                'XAddr': 'Media',
                'RTPMulticast': True,
                'RTP_RTSP_TCP':True
            },
            'respon':[
                {'server': '123'},
                {'server': '345'},
                {'server': '789'}
            ]
        }}
    body = _wrap_params(test_dict)
    print(body)
