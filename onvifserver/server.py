#! -*- coding:utf-8 -*-
#
# Copyright 2017 , donglin-zhang, Hangzhou, China
#
# Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.0;
# you may not use this file except in compliance with the License.
#
import socketserver
from http.server import BaseHTTPRequestHandler
import re
import traceback
from onvifserver.utils import soap_decode, soap_encode


class Error(Exception):
    """Base class for server errors."""
    def __str__(self):
        return repr(self)


class OnvifServerError(Error):
    def __init__(self, faultString):
        self.faultString = faultString

    def __repr__(self):
        return "<%s: %r>" % (self.__class__.__name__, self.faultString)


class Fault(Error):
    """onvif server fault."""
    def __init__(self, faultCode, faultString, **extra):
        Error.__init__(self)
        self.faultCode = faultCode
        self.faultString = faultString
    def __repr__(self):
        return "<%s %s: %r>" % (self.__class__.__name__,
                                self.faultCode, self.faultString)


class OnvifServerDispatcher(object):
    '''
    onvif服务端任务分发处理模块，根据不同请求url路径将消息分发至对应的模块中
    '''
    def __init__(self, allow_none=False, encoding=None, use_builtin_types=False):
        self.funcs = {}
        self.instances = {}
        self.server_path = []
        self.allow_none = allow_none
        self.encoding = encoding or 'utf-8'
        self.use_builtin_types = use_builtin_types

    def register_instance(self, instance, path):
        """
        注册一个对象来响应对应的onvif请求
        参数：
            instance: 用户实现的onvifserver类.
                      类中如果包含_dispatch函数client请求的方法和参数会传递到_dispatch中，
                      如_dispatch(“GetDeviceInformation”, None), 否则，使用内置_dispatch

                      类处理请求函数命名要求如下，如获取设备信息方法为“GetDeviceInformation”，
                      那么函数命名应为get_device_information, 'GetServiceCapabilities'应命名
                      为get_service_capabilities
            path: server path, 如'/onvif/device_service'
        """
        self.instances[path] = instance
        self.server_path.append(path)

    def register_function(self, function, name=None):
        """
        Registers a function to respond to onvif server.
        The optional name argument can be used to set a Unicode name
        for the function.
        """
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    def _marshaled_dispatch(self, data, dispatch_method = None, path = None):
        """
        Todo
        """
        if path not in self.server_path:
            raise OnvifServerError('Unsupported server')

        try:
            method, params = soap_decode(data)
            # generate response
            if dispatch_method is not None:
                response = dispatch_method(method, params, path)
            else:
                response = self._dispatch(method, params, path)
            # wrap response in a singleton tuple
            response = soap_encode(response, method, path)
        except Fault as fault:
            print('an error happened in dispatch')  # just for debug
            # response = soap_error(fault, allow_none=self.allow_none,encoding=self.encoding)
        return response.encode(self.encoding, 'xmlcharrefreplace')

    def _dispatch(self, method, params, path):
        """
        dsf
        """
        func = None
        try:
            # check to see if a matching function has been registered
            func = self.funcs[method]
        except KeyError:
            try:
                instance = self.instances[path]
            except KeyError:
                raise Exception('server "%s" is not supported' % path)
            else:
                # whether a instance has a _dispatch
                if hasattr(instance, '_dispatch'):
                    return instance._dispatch(method, params)
                else:
                    pattern = r'[A-Z][a-z]+'
                    match = re.findall(pattern, method)
                    func = eval('instance.' + '_'.join(match).lower())

        if func is not None:
            return func(**params)
        else:
            raise Exception('method "%s" is not supported' % method)


class OnvifServerRequestHandler(BaseHTTPRequestHandler):
    """onvif server request handler class.

    Handles all HTTP POST requests and attempts to decode them as
    onvif-client requests.
    """
    # Class attribute listing the accessible path components;
    # paths not on this list will result in a 404 error.

    #if not None, encode responses larger than this, if possible
    encode_threshold = 1400 #a common MTU

    #Override form StreamRequestHandler: full buffering of output
    #and no Nagle.
    wbufsize = -1
    disable_nagle_algorithm = True


    def do_POST(self):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as XML-RPC calls,
        which are forwarded to the server's _dispatch method for handling.
        """
        if 'onvif' not in self.path:
            self.report_404()
            return
        try:
            # Get arguments by reading body of request.
            # We read this in chunks to avoid straining
            # socket.read(); around the 10 or 15Mb mark, some platforms
            # begin to have problems (bug #792570).
            max_chunk_size = 10*1024*1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                chunk = self.rfile.read(chunk_size)
                if not chunk:
                    break
                L.append(chunk)
                size_remaining -= len(L[-1])
            data = b''.join(L)

            data = self.decode_request_content(data)
            if data is None:
                return #response has been sent

            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None), self.path
                )
        except Exception as e: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)

            # Send information about the exception if requested
            if hasattr(self.server, '_send_traceback_header') and \
                    self.server._send_traceback_header:
                self.send_header("X-exception", str(e))
                trace = traceback.format_exc()
                trace = str(trace.encode('ASCII', 'backslashreplace'), 'ASCII')
                self.send_header("X-traceback", trace)

            self.send_header("Content-length", "0")
            print(e)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Connection", "close")
            self.send_header("Content-type", "application/soap+xml; charset=utf-8")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    def decode_request_content(self, data):
        '''
        检测消息内容是否为soap+xml消息
        '''
        #support gzip encoding of request
        content_type = self.headers.get("content-type", "unknown").lower()
        if content_type == "unknown":
            self.send_response(501, "unknown content-type")
        if  "application/soap+xml" in content_type:
            return data
        else:
            self.send_response(501, "content-type %r not supported" % content_type)
        self.send_header("Content-length", "0")
        self.end_headers()

    def report_404 (self):
        ''' Report a 404 error '''
        self.send_response(404)
        response = b'No such page'
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_request(self, code='-', size='-'):
        """Selectively log an accepted request."""

        if self.server.logRequests:
            BaseHTTPRequestHandler.log_request(self, code, size)


class OnvifServer(socketserver.TCPServer, OnvifServerDispatcher):
    """
    基于python socketserver，参考xmlRPC.server搭建的soap webservice框架，
    用于实现onvif server端业务, 框架提供创建创建webservice，并处理客户端请
    求的功能，上层应用只需要实现业务操作的相关接口即可，例如下面的代码实现了
    ONVIF摄像机GetDeviceInformation功能：
    from onvifserver.server import OnvifServer

    with OnvifServer(("192.168.1.9", 8000)) as server:
        server.register_introspection_functions()

        def get_device_info_function(a):
            device_info = {'manufacturer': 'GOSUN',
                            'Firmware_Version': 'V5.4.0 build 160613',
                            'Model': 'DS-2DE72XYZIW-ABC/VS'}
            return device_info
        server.register_function(get_device_info_function, "GetDeviceInformation")
        server.serve_forever()
    """

    allow_reuse_address = True

    # Warning: this is for debugging purposes only! Never set this to True in
    # production code, as will be sending out sensitive information (exception
    # and stack trace details) when exceptions are raised inside
    # SimpleXMLRPCRequestHandler.do_POST
    _send_traceback_header = False

    def __init__(self, addr, requestHandler=OnvifServerRequestHandler,
                 logRequests=True, allow_none=False, encoding=None,
                 bind_and_activate=True, use_builtin_types=False):
        self.logRequests = logRequests
        self.dispatchers = {}
        OnvifServerDispatcher.__init__(self, allow_none, encoding, use_builtin_types)
        socketserver.TCPServer.__init__(self, addr, requestHandler, bind_and_activate)
