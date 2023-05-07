from machine import Pin
import machine
# version...
version = "2.0.4.28"

enableLogging = True

# timing vars (seconds)...
tm_failSafeSeconds = 60
tm_out_to_home = 20
tm_top_wait = 8
tm_down_step = 8
tm_Dn_Runtime = 0
tm_HomeOverRun = float(0.2)
tm_1_wait = 1
tm_10_wait = 8

ignore_none = 0
ignore_sw_Up = 1
ignore_sw_Dn = 2
ignore_both = 3
ignore_sw_Home = 4

#	LED
led_home	= Pin(26, Pin.OUT)
led_rly_Up	= Pin(14, Pin.OUT)
led_rly_Dn	= Pin(15, Pin.OUT)
led_log_Up	= Pin(17, Pin.OUT)
led_log_Dn	= Pin(18, Pin.OUT)

#	Control
rly_Up 		= Pin(0, Pin.OUT)
rly_Dn 		= Pin(1, Pin.OUT)
sw_Occupancy= Pin(2, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Home 	= Pin(3, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Upper 	= Pin(4, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Lower 	= Pin(5, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Up   	= Pin(6, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Dn   	= Pin(7, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main2_Up = Pin(8, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main2_Dn = Pin(9, Pin.IN,  pull = Pin.PULL_UP)   # enable internal pull-up resistor, set pin high on creation
sw_Main_Up	= Pin(11, Pin.IN, pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation
sw_Main_Dn	= Pin(10, Pin.IN, pull = Pin.PULL_UP)  # enable internal pull-up resistor, set pin high on creation

sw_Home_chg = False

actual_time = '2023, 1, 1, 1, 5, 48, 1, 94'
day = 0

ON = False
OFF = True
UP = True
DN = False

