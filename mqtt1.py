#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paho.mqtt.client as mqtt
import struct
import json
import time
import RPi.GPIO
import RGB_lib
from datetime import date
from datetime import datetime
import dht11

R,G,B=18,23,24
DEV_ID = "501998536"
PRO_ID = "182062"
AUTH_INFO = "end1"
API_KEY = "7XBF=3K4QUPzCyGVY93ylOv=6AU="
TYPE_JSON = 0x01
TYPE_FLOAT = 0x17
temp=0


# Error values
MQTT_ERR_AGAIN = -1
MQTT_ERR_SUCCESS = 0
MQTT_ERR_NOMEM = 1
MQTT_ERR_PROTOCOL = 2
MQTT_ERR_INVAL = 3
MQTT_ERR_NO_CONN = 4
MQTT_ERR_CONN_REFUSED = 5
MQTT_ERR_NOT_FOUND = 6
MQTT_ERR_CONN_LOST = 7
MQTT_ERR_TLS = 8
MQTT_ERR_PAYLOAD_SIZE = 9
MQTT_ERR_NOT_SUPPORTED = 10
MQTT_ERR_AUTH = 11
MQTT_ERR_ACL_DENIED = 12
MQTT_ERR_UNKNOWN = 13
MQTT_ERR_ERRNO = 14
MQTT_ERR_QUEUE_SIZE = 15

def error_string(mqtt_errno):
    """Return the error string associated with an mqtt error number."""
    if mqtt_errno == MQTT_ERR_SUCCESS:
        return "No error."
    elif mqtt_errno == MQTT_ERR_NOMEM:
        return "Out of memory."
    elif mqtt_errno == MQTT_ERR_PROTOCOL:
        return "A network protocol error occurred when communicating with the broker."
    elif mqtt_errno == MQTT_ERR_INVAL:
        return "Invalid function arguments provided."
    elif mqtt_errno == MQTT_ERR_NO_CONN:
        return "The client is not currently connected."
    elif mqtt_errno == MQTT_ERR_CONN_REFUSED:
        return "The connection was refused."
    elif mqtt_errno == MQTT_ERR_NOT_FOUND:
        return "Message not found (internal error)."
    elif mqtt_errno == MQTT_ERR_CONN_LOST:
        return "The connection was lost."
    elif mqtt_errno == MQTT_ERR_TLS:
        return "A TLS error occurred."
    elif mqtt_errno == MQTT_ERR_PAYLOAD_SIZE:
        return "Payload too large."
    elif mqtt_errno == MQTT_ERR_NOT_SUPPORTED:
        return "This feature is not supported."
    elif mqtt_errno == MQTT_ERR_AUTH:
        return "Authorisation failed."
    elif mqtt_errno == MQTT_ERR_ACL_DENIED:
        return "Access denied by ACL."
    elif mqtt_errno == MQTT_ERR_UNKNOWN:
        return "Unknown error."
    elif mqtt_errno == MQTT_ERR_ERRNO:
        return "Error defined by errno."
    else:
        return "Unknown error."

def build_payload(type, payload):
    datatype = type
    packet = bytearray()
    packet.extend(struct.pack("!B", datatype))
    if isinstance(payload, str):
        udata = payload.encode('utf-8')
        length = len(udata)
        packet.extend(struct.pack("!H" + str(length) + "s", length, udata))
    return packet

def on_connect(client, userdata, flags, rc):
    print ("connected with result code " + mqtt.connack_string(rc))
    json_body = json.dumps(json2temperature())
    packet = build_payload(TYPE_JSON, json_body)
    client.publish("$dp", packet, qos=2)

def on_message(client, userdata, msg):
    print('[topic:]'+msg.topic + '  ' + '[payload:]'+str(msg.payload))
    if msg.topic == 'upload': # 如果收到upload主题，就将数据类型3（json数据2）内容上传给OneNET平台
        dp_load = '{"a":1,"c":3,"b":2,"d":4}'
        dp_type = 3
        dp_len = len(dp_load)
        dp=bytearray()
        dp.append(dp_type)
        dp.append((dp_len >> 8) & 0xFF)
        dp.append(dp_len & 0xFF)
        dp = dp + dp_load
        print('repr&&&&&&&:',repr(dp))
        (rc, final_mid) = client.publish('$dp', str(dp), 2, True)
    if '$creq' in msg.topic: # 如果收到OneNET下发的主题，然后将信息转发给test主题，其他设备将会收到
        (rc, final_mid) = client.publish('test', str(msg.payload), 2, True)
        print(msg.payload)


def on_publish(client, userdata, mid):
    print ("<<<<PUBACK")
    print ("mid:" + str(mid))
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        try:
            print ("Unexpected disconnection with rc: " + str(rc) + "! Datetime: " + str(datetime.datetime.now()))
            print (error_string(rc))
            print ("Reconnecting, please wait...")
            time.sleep(3)
        except Exception as e:
            print ("General exception in MQTT with rc: " + str(rc))
            print (e)
    else:
        print ("Normal disconnect with rc: " + str(rc) + "! Datetime: " + str(datetime.datetime.now()))
                  

def on_log(mqttc, obj, level, string):
    print("Log:" + string)

def set_RGB_Configure():
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setwarnings(False)
   
def json2temperature():
    data ={}
    instance_dh11 = dht11.DHT11(pin=17)
    result = instance_dh11.read()

    if result.is_valid():
        datapoints =[{"at":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"value":result.temperature}]
        temp =result.temperature
    else:
        datapoints =[{"at":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"value":temp}]
    datastreams=[{"id":"temperature","datapoints":datapoints}]
    data['datastreams']=datastreams
    time.sleep(2)
    return data

def main():
    client = mqtt.Client(client_id=DEV_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=PRO_ID, password=API_KEY)
    client.connect('183.230.40.39', 6002, 60)
    client.loop_start()
    # Continue the network loop, exit when an error occurs
    rc = 0
    set_RGB_Configure()
    instance_rgb = RGB_lib.RGB(R,G,B)
    instance_rgb.setOut()
    while True: 
        try:
            json_body =  json.dumps(json2temperature())
            packet = build_payload(TYPE_JSON, json_body)
            print ("PUBLISH>>>>")
            print(packet)
            rc,mid =client.publish("$dp", packet, qos=2)
            if rc ==0:
                instance_rgb.setRedOff()
                instance_rgb.setBlueOff()
                instance_rgb.setGreenOn()
                
            else:
                instance_rgb.setGreenOff()
                instance_rgb.setBlueOff()
                instance_rgb.setRedOn()
            print(" slepp time")  
            time.sleep(10)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("General exception in MQTT with rc: " + str(rc))
            print (e)
    print("rc: " + str(rc))
    client.loop_stop()
    client.disconnect()

def maintest():
    json2temperature()
    
if __name__ == '__main__':
    main()
