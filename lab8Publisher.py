import machine
from machine import ADC
from network import WLAN
import time, socket
import requests
from machine import Pin, PWM
import cryptolib
import umqtt.robust as umqtt

HOSTNAME = '172.20.10.6'
PORT = 8080
TOPIC = 'temp/pico'

# setting wifi
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

# network name and pwd
ssid = 'iPhone (2)'
password = 'TargetPlanet'

temp_sensor = ADC(4)


def connect(
        wifi_obj,
        ssid,
        password,
        timeout=10
):
    wifi_obj.connect(ssid, password)

    while timeout > 0:
        if wifi_obj.status() != 3:
            time.sleep(1)
            timeout -= 1

        else:
            return True

    return False


def read_temp():
    global temp_sensor

    value = temp_sensor.read_u16()
    voltage = value * (3.3 / 2 ** 16)
    temperature = 27 - (voltage - 0.706) / .001721

    return temperature


print(str(read_temp))

if not connect(wifi, ssid, password):
    print('wifi couldn\'t connect')
else:
    print("connected to wifi")

mqtt = umqtt.MQTTClient(
    client_id=b'publish',
    server=HOSTNAME.encode(),
    port=PORT,
    keepalive=7000
)

mqtt.connect()

mqtt.publish(TOPIC, str(read_temp()).encode())