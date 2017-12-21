#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
from lxml import etree
import re

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


def soap_encode(params, method):
    '''
    构造并返回soap消息体
    '''
    header = _wrap_soap_head()
    body = r'''<tds:GetDeviceInformationResponse>
        <tds:Manufacturer>GoSun Test</tds:Manufacturer>
        <tds:Model>Mars01</tds:Model>
        <tds:FirmwareVersion>1.00</tds:FirmwareVersion>
        <tds:SerialNumber>00408C1836B2</tds:SerialNumber>
        <tds:HardwareId>170</tds:HardwareId>
        </tds:GetDeviceInformationResponse>'''
    return _wrap_soap_message(header, body)

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
        params = None
    return method_name, params

def _get_method_params(parent_node):
    '''
    解析参数信息，将参数打包为一个列表返回。
    '''
    params_list = []
    for param in parent_node:
        tmp_dict = {}
        param_name = _get_node_tag(param)
        if len(param) > 0:
            sub_param = _get_method_params(param)
            sub_param_name = _get_node_tag(param)
            tmp_dict[sub_param_name] = sub_param
        else:
            if param.text:
                tmp_dict[param_name] = param.text
        params_list.append(tmp_dict)
    return params_list

def _get_node_tag(node):
    pattern = r'[^{}]+(?={|$)'
    return re.findall(pattern, node.tag)[0]


def _wrap_soap_head():
    response_soap_header = r'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"'''
    for ns in ns_soap:
        ns_string = '''xmlns:{0}="{1}"'''.format(ns, ns_soap[ns])
        response_soap_header += ns_string
    return '{0}<SOAP-ENV:Body>'.format(response_soap_header)

def _wrap_soap_message(header, body):
    return '''{0}{1}</SOAP-ENV:Body></SOAP-ENV:Envelope>'''.format(header, body)


if __name__ == '__main__':
    soap = b'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
    <SOAP-ENV:Body>
    <tds:GetCapabilities>
    <tds:Category>All</tds:Category>
    </tds:GetCapabilities>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

    name, params = soap_decode(soap)
    print(name)
    print(params)
    # header = _wrap_soap_head(['tt', 'tds'])
    # print(header)
