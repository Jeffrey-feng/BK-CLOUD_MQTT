# BK-CLOUD_MQTT
利用数莓派采集数据，基于mqtt的云服务上传存储，实现断线重传

运行环境：树莓派2B
编程语言：python3

依赖库：
pip3 install paho-mqtt 

详细API 使用参考
https://pypi.org/project/paho-mqtt/


软件调用的硬件接口有USB（华为4G），DH11（温湿度），RGB(LED)。
云端显示采用中国移动ONENET，
显示地址https://open.iot.10086.cn/device/data?pid=182062&did=501998536

模拟机舱温度，每隔3秒上传数据，自动检测4G信号，当连接云端时，LED显示绿色，4G断开时，显示红色。

运行命令python3 mqtt1.py
