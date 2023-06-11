from machine import Pin
import machine
# version...
version = "2.0.6.02"

enablePrint = True
enableLogging = False
debugLog = "ChairLog.log"

# Timing variables (float) seconds...
tm_failSafeSeconds = float(60.0)
tm_out_to_home = float(20.0)
tm_top_wait = float(8.0)
tm_down_step = float(8.0)
tm_HomeOverRun = float(.30)
tm_sw_bounce = float(.5)
tm_1_wait = float(1.0)
tm_10_wait = float(8.0)
tm_5_wait = float(5.0)

# enums
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
id_dn_runtime =	4096

#   yeah, this is pretty much redundant
ignore_none = 		0
ignore_sw_Up = 		1
ignore_sw_Up2 = 	2
ignore_sw_Dn = 		4
ignore_sw_Dn2 = 	8
ignore_sw_Main_Up = 16
ignore_sw_Main_Up2 = 32
ignore_sw_Main_Dn = 64
ignore_sw_Main_Dn2 = 128
ignore_led_home = 	256
ignore_led_upper = 	512
ignore_led_lower = 	1024
ignore_led_occup = 	2048

#   enum control groups
ignore_all_sw =     255
ignore_allLimits =	3840
ignore_all =		4095

#	Control
rly_Up 		= Pin(0,  Pin.OUT)                        # Main UP relay output
rly_Dn 		= Pin(1,  Pin.OUT)                        # Main DOWN relay output
sw_Home 	= Pin(2,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Upper 	= Pin(3,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Lower 	= Pin(4,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Occup    = Pin(5,  Pin.IN, pull = Pin.PULL_UP)     # Limit switch - enable internal pull-up resistor
sw_Main_Dn2 = Pin(6,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Up2 = Pin(7,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Dn	= Pin(8,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Main_Up	= Pin(9,  Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Up   	= Pin(10, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Up_2   	= Pin(12, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor
sw_Dn_2   	= Pin(13, Pin.IN, pull = Pin.PULL_DOWN)   # enable internal pull-down resistor

#	 NOTE: 'led_power' is tied directly to pin 36 (3.3vdc) and NOT under program control
led_upper   = Pin(18, Pin.OUT) # 18=yel
led_lower   = Pin(19, Pin.OUT) # 19=red
led_home	= Pin(20, Pin.OUT) # 20=blu
led_occup   = Pin(21, Pin.OUT) # 21=wht

#   All unused PICO GPIO pins are scoped INPUT and pulled DOWN by default
unusedGpio = [14, 15, 16, 17, 22]
for i in unusedGpio:
    Pin(i, Pin.IN, pull = Pin.PULL_DOWN)

#   Misc global variables
actual_time = '2023, 1, 1, 1, 5, 48, 1, 94' # just the format for now
day = 0
tm_Dn_Runtime = float(0.0)


ON = False
OFF = True
UP = True
DN = False




