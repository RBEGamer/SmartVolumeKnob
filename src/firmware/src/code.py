import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import rotaryio
import board
import random
from static_modules import ledring
from static_modules import config
from static_modules import helper



# CONSTANTS
TIME_ELAPSED_DIVIDER: int = 2
USER_INTERACTION_TIMEOUT_TIME: int = 100 #FADE LEDS DOWN AFTER x SECONDS OF INATIVITY
MAX_LED_HSV_VALUE: int = 100 # FOR SCALING BACK FROM 0-X => 0-1.0

# VARIABLES
encoder_middle_point: int = 1
current_led_h: int = 0
current_led_v: int = 0
target_led_h: int = random.randrange(0, MAX_LED_HSV_VALUE+1)
target_led_v: int = 200

def handle_encoder_change(_direction: int = 0, _amount: int = 1):
    global target_led_h
    global target_led_v
    for i in range(_amount):
        if _direction > 0:
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        elif _direction < 0:
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
    
    target_led_h = (target_led_h +(_direction*_amount)) % MAX_LED_HSV_VALUE
    target_led_v = MAX_LED_HSV_VALUE






# SETUP USB REMOTE CONTROL
consumer = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
consumer.send(ConsumerControlCode.VOLUME_DECREMENT)


# INIT LED RING
ledring.ledring().clear()
ledring.ledring().set_neopixel_full_hue_value(ledring.ledring().COLOR_PRESET_HSV_H__BLUE)

## REGISTER ENCODER BUTTON EVENTS BY REMAPPING THE ENCODER SWITCH 

encoder = rotaryio.IncrementalEncoder(config.CFG_ENCODER_CLK_PIN, config.CFG_ENCODER_DT_PIN)
# CONFIGURE ENCODER



def exec():
    global target_led_h
    global target_led_v
    global current_led_h
    global current_led_v
    
    last_update: int = helper.millis()
    last_userinteraction_update: int = helper.millis()

    current_encoder_value: int = encoder_middle_point
    while True:
    


        # HANDLE ENCODER
        current_encoder_value = encoder.position
        if current_encoder_value != encoder_middle_point:
            last_userinteraction_update = helper.millis()
                
            if current_encoder_value > encoder_middle_point:
                handle_encoder_change(-1, current_encoder_value)
            elif current_encoder_value < encoder_middle_point:
                handle_encoder_change(1, current_encoder_value)
                
        # HANDLE LED FADING
        if  abs(last_update - helper.millis()) > (10/TIME_ELAPSED_DIVIDER):
            last_update = helper.millis()
            # FADE HUE
            if target_led_h > current_led_h:
                current_led_h = current_led_h + 1
            if target_led_h < current_led_h:
                current_led_h = current_led_h - 1

            # FADE BRIGHNESS
            if target_led_v > current_led_v:
                current_led_v = current_led_v + 1
            if target_led_v < current_led_v:
                current_led_v = current_led_v - 1

        # HANDLE LED INACTIVITY FADE
        if abs(last_userinteraction_update - helper.millis()) > USER_INTERACTION_TIMEOUT_TIME:
            if target_led_v > 0:
                target_led_v = target_led_v - 1

        # UPDATE LED
        # SCALE 0-100 to 0.1
        ledring.ledring().set_neopixel_full_hue_value(abs(current_led_h / MAX_LED_HSV_VALUE), abs(current_led_v / MAX_LED_HSV_VALUE))         


        
exec()