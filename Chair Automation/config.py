from machine import Pin
import machine
# version...
version = "2.0.5.30"

enableLogging = False
debugLog = "ChairLog.log"

# Timing variables (seconds)...
tm_failSafeSeconds = 60
tm_out_to_home = 20
tm_top_wait = 8
tm_down_step = 8
tm_HomeOverRun = float(.30)
tm_sw_bounce = float(.5)
tm_1_wait = 1
tm_10_wait = 8
tm_5_wait = 5

#   Status enums
id_none = 		0
id_sw_Up = 		1
id_sw_Up2 = 	2
id_sw_Dn = 		4
id_sw_Dn2 = 	8
id_sw_Main_Up = 16
id_sw_Main_Up2 = 32
id_sw_Main_Dn = 64
id_sw_Main_Dn2 = 128
id_led_home = 	256
id_led_upper = 	512
id_led_lower = 	1024
id_led_occup = 	2048

#	Control
rly_Up 		= Pin(0, Pin.OUT)
rly_Dn 		= Pin(1, Pin.OUT)
sw_Main_Dn2 = Pin(6, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main_Up2 = Pin(7, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main_Dn	= Pin(9, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main_Up	= Pin(8, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Up_2   	= Pin(12, Pin.IN, pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Dn_2   	= Pin(13, Pin.IN, pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Up   	= Pin(10, Pin.IN, pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation

#   Limit switches
sw_Home 	= Pin(2, Pin.IN,  pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation
sw_Upper 	= Pin(3, Pin.IN,  pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation
sw_Lower 	= Pin(4, Pin.IN,  pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation
sw_Occup    = Pin(5, Pin.IN,  pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation

#	LED led_power = tied directly to pin 36 (3.3vdc)
led_home	= Pin(20, Pin.OUT) # 18=yel 19=red 20=blu 21=wht
led_upper   = Pin(18, Pin.OUT)
led_lower   = Pin(19, Pin.OUT)
led_occup   = Pin(21, Pin.OUT)

#   All unused PICO GPIO pins are scoped INPUT and pulled HIGH/UP by default
# unusedGpio = [14, 15, 16, 22, 26, 27]
# for i in unusedGpio:
#     Pin(i, Pin.IN, pull = Pin.PULL_UP)

#   Misc global variables
actual_time = '2023, 1, 1, 1, 5, 48, 1, 94' # just the format for now
day = 0
tm_Dn_Runtime = 0


ON = False
OFF = True
UP = True
DN = False
