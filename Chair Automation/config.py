# Config.py version...
version = "2.0.2.23"

from machine import Pin, PWM
import machine
# import socket
# import network
# import time
# from functions import *
# -------------------------- User-specific settings. Change at-will. --------------------------

# Timing variables (float) seconds
tm_home_to_out = float(23.0)    # From normal position to fully raised
tm_top_wait = float(10.0)       # Time to wait (fully raised) to exit, before lowering
tm_down_step = float(8.5)       # From normal position to recline 

# Options...
enableLogging = True
enableFileLog = False 
logFilename = "ChairLog.log"
enableWiFi = True
use_sw_RiseHome = False
use_sw_ReclHome = False
use_sw_Upper = False
use_sw_Lower = False
abort = False

# LED brightness
ledFreq = 1000
brightness_NormIntensityLed = 5000 # Between 0 - 10000
brightness_AltNormIntensityLed = 1000 # Between 0 - 10000 (usually white-colored LED's. Very bright)
brightness_HighIntensityLed = 2000

# -------------------------- Below are system variables, and should not be changed. --------------------------

# Timing variables (float) seconds
tm_failSafeSeconds = float(60.0)
tm_sw_bounce = float(.1)

# bin enums
id_none = 		 0
id_sw_Up = 		 1
id_sw_Up2 = 	 2
id_sw_Dn = 		 4
id_sw_Dn2 = 	 8
id_sw_Main_Up =  32
id_sw_Main_Up2 = 64
id_sw_Main_Dn =  16
id_sw_Main_Dn2 = 128
id_sw_riseHome = 256
id_sw_upper = 	 512
id_sw_reclHome = 1024
id_sw_lower = 	 2048
id_led_home = 	 4096
id_led_upper = 	 8192
id_led_lower = 	 16384
id_led_occup = 	 32768

# bin enum control groups
id_sw_all = 	    255
id_sw_allLimits =	3840
id_all =			4095
    
# Control
rly_Up 		= Pin(0,  Pin.OUT)                        # Main UP relay output
rly_Dn 		= Pin(1,  Pin.OUT)                        # Main DOWN relay output
sw_RiseHome	= Pin(2,  Pin.IN, pull = Pin.PULL_UP)     # Rise Home Limit switch,     internal pull-up resistor
sw_ReclHome = Pin(3,  Pin.IN, pull = Pin.PULL_UP)     # Recline Home Limit switch,  internal pull-up resistor
sw_Upper	= Pin(4,  Pin.IN, pull = Pin.PULL_UP)     # Upper Limit switch,         internal pull-up resistor
sw_Lower    = Pin(5,  Pin.IN, pull = Pin.PULL_UP)     # Occupancy Limit switch,     internal pull-up resistor
sw_Main_Dn2 = Pin(9,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 2 DOWN,   internal pull-down resistor
sw_Main_Dn = Pin(7,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 2 UP,     internal pull-down resistor
sw_Main_Up	= Pin(8,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 1 UP,     internal pull-down resistor
sw_Main_Up2	= Pin(6,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 1 DOWN,   internal pull-down resistor
sw_Up   	= Pin(10, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 1 UP,    internal pull-down resistor
sw_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 1 DOWN,  internal pull-down resistor
sw_Up_2   	= Pin(12, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 2 UP,    internal pull-down resistor
sw_Dn_2   	= Pin(13, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 2 DOWN,  internal pull-down resistor

# NOTE: 'led_power' is tied directly to pin 36 (3.3vdc) and NOT under program control
l_power		= Pin(16, Pin.OUT)
l_reclHome  = Pin(21, Pin.OUT) 
l_riseHome  = Pin(18, Pin.OUT) 
l_up        = Pin(19, Pin.OUT) 
l_dn        = Pin(20, Pin.OUT)

led_Power = PWM(l_power)
led_UP = PWM(l_up)
led_reclHome = PWM(l_reclHome)
led_riseHome = PWM(l_riseHome)
led_DN = PWM(l_dn)

led_Power.freq(ledFreq)
led_UP.freq(ledFreq)
led_reclHome.freq(ledFreq)
led_riseHome.freq(ledFreq-500)
led_DN.freq(ledFreq)

#   All unused PICO GPIO pins are scoped INPUT and pulled DOWN by default
unusedGpio = [17, 22]
for i in unusedGpio:
    Pin(i, Pin.IN, pull = Pin.PULL_DOWN)

#   Misc global variables
tm_Dn_Runtime = float(0.0)

ON = False  # Seems ironic I know, but some input pins are pulled HIGH by default, making the states opposite of what one would think. 
OFF = True  # Example: When CLOSED (remember it's pulled HIGH when open) it's LOW (or FALSE). So we report the closed state as ON (or TRUE).
HI = True
LO = False 

#  String utils...
lf = "\n\t\t"

            
