import time
import network
from network import WLAN
from machine import Pin, PWM
import umqtt.robust as umqtt

# Wifi Connection SetUp
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

# Wifi Credentials
ssid = 'iPhone (2)'
password = 'TargetPlanet'


def connect(
        wifi_obj,
        ssid,
        password,
        timeout=10
):
    wifi_obj.connect(ssid, password)

    while timeout > 0:
        # status() != means its not yet fully connected
        if wifi_obj.status() != 3:
            time.sleep(1)
            timeout -= 1

        else:
            # Successfully connected
            return True

            # Timed out
    return False


# Run the connection function and verify status
if not connect(wifi, ssid, password):
    print('wifi couldn\'t connect')
else:
    print("connected to wifi")

# MQQT AND HARDWARE CONFIGURAION

# IP address of our MQQT broker
HOSTNAME = '172.20.10.6'
# Port number
PORT = 8080
# MQQT topic to subscribe
TOPIC = 'temp/pico'

led_pin = machine.Pin(22, machine.Pin.OUT)
import time
import network
from network import WLAN
from machine import Pin, PWM
import umqtt.robust as umqtt

# Wifi Connection SetUp
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

# Wifi Credentials
ssid = 'iPhone (2)'
password = 'TargetPlanet'


def connect(
        wifi_obj,
        ssid,
        password,
        timeout=10
):
    wifi_obj.connect(ssid, password)

    while timeout > 0:
        # status() != means its not yet fully connected
        if wifi_obj.status() != 3:
            time.sleep(1)
            timeout -= 1

        else:
            # Successfully connected
            return True

            # Timed out
    return False


# Run the connection function and verify status
if not connect(wifi, ssid, password):
    print('wifi couldn\'t connect')
else:
    print("connected to wifi")

# MQQT AND HARDWARE CONFIGURAION

# IP address of our MQQT broker
HOSTNAME = '172.20.10.6'
# Port number
PORT = 8080
# MQQT topic to subscribe
TOPIC = 'temp/pico'

led_pin = machine.Pin(22, machine.Pin.OUT)

# Initialize the MQQT client using umqtt
mqtt = umqtt.MQTTClient(
    client_id=b'Subscribe',
    server=HOSTNAME.encode(),
    port=PORT,
    keepalive=7000  # Keep-alive ping in seconds
)


# Callback function
def callback(TOPIC, message):
    print(f'I received the message "{message}" for topic "{TOPIC}"')
    try:
        # Decode the message from bytes to a string then conver into a float number
        msg_str = message.decode() if isinstance(message, bytes) else message
        temp = float(msg_str)

        # Check temperture and control the led
        if temp >= 25:
            led_pin.value(1)
            print("Temperature high – LED ON")
        else:
            led_pin.value(0)
            print("Temperature normal – LED OFF ")
    except Exception as e:
        print("Error parsing message:", e)


mqtt.connect()
print("MQQT CONNECT")
mqtt.set_callback(callback)
mqtt.subscribe(b'temp/pico')
print('waiting for message')

try:
    while True:
        mqtt.wait_msg()

except KeyboardInterrupt:
    print("Disconnecting...")
    mqtt.disconnect()

# while True:
#
#     pwm_led.duty_u16
#

# Initialize the MQQT client using umqtt
mqtt = umqtt.MQTTClient(
    client_id=b'Subscribe',
    server=HOSTNAME.encode(),
    port=PORT,
    keepalive=7000  # Keep-alive ping in seconds
)


# Callback function
def callback(TOPIC, message):
    print(f'I received the message "{message}" for topic "{TOPIC}"')
    try:
        # Decode the message from bytes to a string then conver into a float number
        msg_str = message.decode() if isinstance(message, bytes) else message
        temp = float(msg_str)

        # Check temperture and control the led
        if temp >= 25:
            led_pin.value(1)
            print("Temperature high – LED ON")
        else:
            led_pin.value(0)
            print("Temperature normal – LED OFF ")
    except Exception as e:
        print("Error parsing message:", e)


mqtt.connect()
print("MQQT CONNECT")
mqtt.set_callback(callback)
mqtt.subscribe(b'temp/pico')
print('waiting for message')

try:
    while True:
        mqtt.wait_msg()

except KeyboardInterrupt:
    print("Disconnecting...")
    mqtt.disconnect()