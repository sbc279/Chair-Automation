from machine import Pin
import machine
# version...
version = "2.0.6.30"

# Options...
enableLogging = True
enableFileLog = False
logFilename = "ChairLog.log"

ignoreLimitsSwitches = False
use_sw_RiseHome = True
use_sw_ReclHome = False
use_sw_Upper = False
use_sw_Occup = False

enableWiFi = False
enableJ9 = False

# Timing variables (float) seconds...
tm_failSafeSeconds = float(60.0)
tm_home_to_out = float(23.0)
tm_top_wait = float(10.0)
tm_down_step = float(8.5)
tm_HomeOverRun = float(.9)
tm_sw_bounce = float(.5)
tm_1_wait = float(1.0)
tm_10_wait = float(8.0)
tm_5_wait = float(5.0)

# enums
id_none = 		 0
id_sw_Up = 		 1
id_sw_Up2 = 	 2
id_sw_Dn = 		 4
id_sw_Dn2 = 	 8
id_sw_Main_Up =  16
id_sw_Main_Up2 = 32
id_sw_Main_Dn =  64
id_sw_Main_Dn2 = 128
id_sw_riseHome = 256
id_sw_upper = 	 512
id_sw_reclHome = 1024
id_sw_occup = 	 2048
id_led_home = 	 4096
id_led_upper = 	 8192
id_led_lower = 	 16384
id_led_occup = 	 32768

#   enum control groups
id_sw_all = 	    255
id_sw_allLimits =	3840
id_all =			4095
id_ignoreLimitsSwitches = 0
if ignoreLimitsSwitches:
    id_ignoreLimitsSwitches = id_sw_allLimits
    
#	Control
rly_Up 		= Pin(0,  Pin.OUT)                        # Main UP relay output
rly_Dn 		= Pin(1,  Pin.OUT)                        # Main DOWN relay output
sw_RiseHome	= Pin(2,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Upper 	= Pin(3,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_ReclHome	= Pin(4,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Occup    = Pin(5,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Main_Dn2 = Pin(6,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Up2 = Pin(7,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Up	= Pin(8,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Dn	= Pin(9,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Up   	= Pin(10, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Up_2   	= Pin(12, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Dn_2   	= Pin(13, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_J9		= Pin(14, Pin.IN, pull = Pin.PULL_UP)     # J9 plug - enable internal pull-up resistor
plug_J9 	= Pin(15, Pin.OUT)                        # Plug J9 power

#	 NOTE: 'led_power' is tied directly to pin 36 (3.3vdc) and NOT under program control
led_upper   = Pin(18, Pin.OUT) # 18=yel
led_lower   = Pin(19, Pin.OUT) # 19=red
led_home	= Pin(20, Pin.OUT) # 20=blu
led_occup   = Pin(21, Pin.OUT) # 21=wht

#   All unused PICO GPIO pins are scoped INPUT and pulled DOWN by default
unusedGpio = [14, 16, 17, 22]
for i in unusedGpio:
    Pin(i, Pin.IN, pull = Pin.PULL_DOWN)

#   Misc global variables
actual_time = '2023, 1, 1, 1, 5, 48, 1, 94' # just the format for now
day = 0
tm_Dn_Runtime = float(0.0)
tm_temp = float(0.0)

ON = False
OFF = True
UP = True
DN = False




