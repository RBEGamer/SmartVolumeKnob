import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


import config

# SETUP USB REMOTE CONTROL
consumer = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
