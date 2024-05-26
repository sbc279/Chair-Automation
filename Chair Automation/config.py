# Config.py version...
version = "5.26.24"

from machine import Pin, PWM
import machine
import json
configLoading = True
WEBCTL = False
WEBPOST = 0
WEBREQUEST = ""

tm_home_to_out  			= 0.0    # From normal position to fully raised
tm_top_wait     			= 0.0    # Time to wait (fully raised) to exit, before lowering
tm_out_to_home				= 0.0
tm_down_step    			= 0.0    # From normal position to recline
tm_failSafeSeconds 			= 0.0
tm_sw_bounce 				= 0.0
ledFreq         			= 0
brightness_NormIntensityLed = 0
brightness_MediumIntensityLed = 0
brightness_HighIntensityLed = 0
enableFileLog   			= False
logFilename     			= ""
enableWiFi      			= False
use_sw_RiseHome 			= False
use_sw_ReclHome 			= False
use_sw_Upper    			= False
use_sw_Lower    			= False
enableWiFi 					= True
jsonFilename				= './chairCfg.json'
mainHtmlPage 				= './HTML/main.html'
setupHtmlPage				= './HTML/setup.html'
thisIp						= '0.0.0.0'

# -------------------------- User-specific settings. Change at-will. --------------------------
with open (jsonFilename, 'r') as file:
    # Load the JSON data from the file
    json_data 	= json.load(file)

enableWiFi 		= bool(json_data['enableWiFi'])

# Timing variables (float) seconds
tm_home_to_out 	= float(json_data['homeToOut'])    # From normal position to fully raised
tm_top_wait 	= float(json_data['topWait'])       # Time to wait (fully raised) to exit, before lowering
tm_down_step 	= float(json_data['downStep'])       # From normal position to recline 
tm_out_to_home 	= float(json_data['outToHhome'])


# Options...
enableFileLog 	= bool(json_data['enableFileLog'])
logFilename 	= json_data['logFilename']
enableWiFi 		= bool(json_data['enableWiFi'])
use_sw_RiseHome = bool(json_data['switchRiseHome'])
use_sw_ReclHome = bool(json_data['switchReclHome'])
use_sw_Upper 	= bool(json_data['switchUpper'])
use_sw_Lower 	= bool(json_data['switchLower'])

# LED brightness
ledFreq 						= int(json_data['ledFrequency'])
brightness_NormIntensityLed 	= int(json_data['ledNormal'])
brightness_MediumIntensityLed 	= int(json_data['ledMedium'])
brightness_HighIntensityLed 	= int(json_data['ledHigh'])

# Timing variables (float) seconds
tm_failSafeSeconds 	= int(json_data['failSafeSeconds'])
tm_sw_bounce 		= float(json_data['switchbounce'])

# Misc...
ctrl_sw_RiseHome 	= False
ctrl_sw_ReclHome 	= False

# bin enums
id_none 			= 0
id_btn_Logic_Up 	= 1
id_btn_Logic_Up2 	= 2
id_btn_Logic_Dn 	= 4
id_btn_Logic_Dn2 	= 8
id_btn_Main_Dn 		= 16
id_btn_Main_Up 		= 32
id_btn_Main_Up2 	= 64
id_btn_Main_Dn2 	= 128
if use_sw_RiseHome:
    id_sw_RiseHome 	= 256
else:
    id_sw_RiseHome 	= 0
    
id_sw_Upper 		= 512
if use_sw_RiseHome:
    id_sw_RiseHome 	= 256
else:
    id_sw_RiseHome 	= 0

if use_sw_RiseHome:
    id_sw_RiseHome 	= 256
else:
    id_sw_RiseHome 	= 0
   
if use_sw_ReclHome:
    id_sw_ReclHome 	= 1024
else:
    id_sw_ReclHome 	= 0 

id_sw_Lower 		= 2048
id_led_Home 		= 4096
id_led_REDper 		= 8192
id_led_Lower 		= 16384
id_led_Occup 		= 32768

# bin enum control groups 3072

id_sw_all = 	    255
id_sw_allLimits =	3840
id_all =			4095

# id_sw_all 			= 255b #3072 #255
id_btn_All 			= 3840 #1023 # 3840
# id_all				= 4095
    
# Control
rly_Up 			= Pin(0,  Pin.OUT)                        # Main UP relay output
rly_Dn 			= Pin(1,  Pin.OUT)                        # Main DOWN relay output
sw_RiseHome		= Pin(2,  Pin.IN, pull = Pin.PULL_UP)     # Rise Home Limit switch,     internal pull-up resistor
sw_ReclHome 	= Pin(3,  Pin.IN, pull = Pin.PULL_UP)     # Recline Home Limit switch,  internal pull-up resistor
sw_Upper		= Pin(4,  Pin.IN, pull = Pin.PULL_UP)     # Upper Limit switch,         internal pull-up resistor
sw_Lower    	= Pin(5,  Pin.IN, pull = Pin.PULL_UP)     # Occupancy Limit switch,     internal pull-up resistor

btn_Main_Dn2 	= Pin(8,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 2 DOWN,   internal pull-down resistor
btn_Main_Dn  	= Pin(6,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 2 UP,     internal pull-down resistor
btn_Main_Up		= Pin(9,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 1 UP,     internal pull-down resistor
btn_Main_Up2	= Pin(7,  Pin.IN, pull = Pin.PULL_DOWN)   # Main switch, bank 1 DOWN,   internal pull-down resistor
btn_Logic_Up   	= Pin(10, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 1 UP,    internal pull-down resistor
btn_Logic_Dn   	= Pin(11, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 1 DOWN,  internal pull-down resistor
btn_Logic_Up2   = Pin(12, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 2 UP,    internal pull-down resistor
btn_Logic_Dn2	= Pin(13, Pin.IN, pull = Pin.PULL_DOWN)   # Logic switch, bank 2 DOWN,  internal pull-down resistor

# Control...
if use_sw_RiseHome:
    ctrl_sw_RiseHome = sw_RiseHome.value() == 0
else:
    ctrl_sw_RiseHome = False

if use_sw_ReclHome:
    ctrl_sw_ReclHome = sw_ReclHome.value() == 0
else:
    ctrl_sw_ReclHome = False
    
# NOTE: 'led_power' is tied directly to pin 36 (3.3vdc) and NOT under program control
l_power		= Pin(16, Pin.OUT)
l_reclHome  = Pin(21, Pin.OUT) 
l_riseHome  = Pin(18, Pin.OUT) 
l_up        = Pin(19, Pin.OUT) 
l_dn        = Pin(20, Pin.OUT)

led_Power 	= PWM(l_power)
led_RED 	= PWM(l_up)
led_WHT 	= PWM(l_reclHome)
led_YEL 	= PWM(l_riseHome)
led_BLU 	= PWM(l_dn)

led_Power.freq(5000)
led_RED.freq(ledFreq)
led_WHT.freq(ledFreq)
led_YEL.freq(ledFreq)
led_BLU.freq(ledFreq)

#   All unused PICO GPIO pins are scoped INPUT and pulled DOWN by default
#unusedGpio = [17, 22]
#for i in unusedGpio:
#    Pin(i, Pin.IN, pull = Pin.PULL_DOWN)

#   Misc global variables
tm_Dn_Runtime = float(0.0)


ON = False  # Seems ironic I know, but some input pins are pulled HIGH by default, making the states opposite of what one would think. 
OFF = True  # Example: When CLOSED (remember it's pulled HIGH when open) it's LOW (or FALSE). So we report the closed state as ON (or TRUE).
HI = True
LO = False 

#  String utils...
lf = "\n\t\t"

configLoading = False
