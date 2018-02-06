# virtualIPC
使用Python编写的一个虚拟onvif网络摄像机
用于视频监控平台需要接入大量摄像机，进行性能测试的场景
该工具包括两个模块: onvif server 框架和业务应用模块
## 开发环境
* Python3.6

## onvif server
onvif server模块实现了一个webservice，参考了Python标准库中的simpleXMLRPC模块代码。
相关代码：onvifserver/server.py, 包括三个部分
1. OnvifServerDispatcher
2. OnvifServerRequestHandler
3. OnvifServer

## 应用模块


## 使用方法
```
from virtual_ipc import OnvifIPC

OnvifIPC("192.168.1.9", 8001)
```
如果要创建批量的虚拟设备, 穿件多个OnvifIPC实例即可：
```
ip_port_list = [
    ('192.168.1.2', 80),
    ('192.168.1.2', 82),
    ('192.168.1.2', 83),
    ('192.168.1.2', 84),
]
for ip, port in ip_port_list:
    OnvifIPC(ip, port)
```