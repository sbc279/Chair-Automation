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
tm_HomeOverRun = float(1.8)
tm_1_wait = 1
tm_10_wait = 8

ignore_none = 0
ignore_sw_Up = 1
ignore_sw_Dn = 2
ignore_both = 3
ignore_sw_Home = 4

rly_Up 		= Pin(0, Pin.OUT)
rly_Dn 		= Pin(1, Pin.OUT)
sw_Home 	= Pin(5, Pin.IN,  pull = Pin.PULL_UP) # enable internal pull-up resistor, set pin high on creation
sw_Up   	= Pin(12, Pin.IN, pull = Pin.PULL_UP) # enable internal pull-up resistor, set pin high on creation
sw_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_UP) # enable internal pull-up resistor, set pin high on creation
sw_Main_Up	= Pin(15, Pin.IN, pull = Pin.PULL_UP) # enable internal pull-up resistor, set pin high on creation
sw_Main_Dn	= Pin(14, Pin.IN, pull = Pin.PULL_UP) # enable internal pull-up resistor, set pin high on creation
sw_Home_chg = False

actual_time = '2023, 1, 1, 1, 5, 48, 1, 94' # just to instantiate it
day = 0

ON = False
OFF = True
UP = True
DN = False

