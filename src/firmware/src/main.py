import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import machine
import random
from utime import sleep_us
import uasyncio as aio


from static_modules import ledring
import config
import helper
# NEEDED FOR ENCODER
from sys import platform
if 'esp' in platform: 
    from rotary_irq_esp import RotaryIRQ
elif 'rp' in platform:
    from rotary_irq_rp2 import RotaryIRQ
else:
    from rotary_irq_pyb import RotaryIRQ


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

def handle_encoder_change(_direction: int = 0):
    if _direction > 0:
        consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        target_led_h = (target_led_h + 1) % MAX_LED_HSV_VALUE
    elif _direction < 0:
        consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        target_led_h = (target_led_h - 1) % MAX_LED_HSV_VALUE
    
    
    target_led_v = MAX_LED_HSV_VALUE




if __name__ == "__main__":

    # SETUP USB REMOTE CONTROL
    consumer = ConsumerControl(usb_hid.devices)
    kbd = Keyboard(usb_hid.devices)
    consumer.send(ConsumerControlCode.VOLUME_DECREMENT)


    # INIT LED RING
    ledring.ledring().set_neopixel_full_hsv(ledring.ledring().COLOR_PRESET_HSV_H__BLUE)

    ## REGISTER ENCODER BUTTON EVENTS BY REMAPPING THE ENCODER SWITCH 
    encoder_button_pin: machine.Pin = machine.Pin(config.CFG_ENCODER_SW_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    # CONFIGURE ENCODER
    encoder: RotaryIRQ = RotaryIRQ(pin_num_clk=config.CFG_ENCODER_CLK_PIN, pin_num_dt=config.CFG_ENCODER_DT_PIN, min_val=encoder_middle_point-encoder_middle_point, max_val=encoder_middle_point*2, reverse=config.CFG_ENCODER_INVERT, range_mode=RotaryIRQ.RANGE_WRAP)
    encoder.set_current_value(encoder_middle_point)



    async def main_task():
        last_update: int = helper.millis()
        last_userinteraction_update: int = helper.millis()

        current_encoder_value: int = encoder_middle_point
        while True:
            await aio.sleep_ms(1)


            # HANDLE ENCODER
            current_encoder_value = encoder.value()
            if current_encoder_value != encoder_middle_point:
                last_userinteraction_update = helper.millis()
                    
                if current_encoder_value > encoder_middle_point:
                    handle_encoder_change(-1)
                elif current_encoder_value < encoder_middle_point:
                    handle_encoder_change(1)
                    
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


        