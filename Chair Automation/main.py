# Main.py
# version = 2.0.10.13

import machine #import Pin, PWM, Timer
import sys
import micropython
import ntptime
import rp2
import time
import _thread
from webserver import *
from functions import *
from config import *
import config
import gc
import os
# import uasyncio #import core

micropython.alloc_emergency_exception_buf(100)																																																					

onceUp = False 
onceDn = False

# ------ Wait on config to get completely loaded -------
#
try: # Step 1: Wait for it to be defined
    time.sleep(.1)
    configLoading == False
except NameError:
    onceUp = False # bullshit code. We're good to go now
    
while configLoading: # Step 2: The REAL waiter
    time.sleep(.1)
# ---------------------------------------------------------


print("main.py IPL: (chair) startup  BETA version " + version + "\n")
tm_Dn_Runtime = 0
is_OFF = OFF
is_ON = ON

# up relay interrupt
def irq_rly_Up(p):
    if not p.value():
        a=1
        led_UP.duty_u16(brightness_NormIntensityLed)    
    else:
        led_UP.duty_u16(0)
    
# down relay interrupt
def irq_rly_Dn(p):
    if not p.value():
        led_DN.duty_u16(brightness_HighIntensityLed)
        a=1
    else:
        led_DN.duty_u16(0)
        
# home limit interrupt
def irq_sw_RiseHome(p):
    if not p.value():
        led_riseHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_riseHome.duty_u16(0)
      
# recl limit interrupt
def irq_sw_Recl(p):
    if not p.value():
        led_reclHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_reclHome.duty_u16(0)
 
# Define object interrupt paths
sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) 	# interrupt for led_riseHome
sw_ReclHome.irq(lambda p:irq_sw_Recl(p))   # interrupt for led_lower
rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn
        
def SwitchDebounce():
    while Check_Button_Press() & id_sw_All:
        time.sleep(.1)

# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)

def Is_Home(mute = False):
    if sw_RiseHome.value() == is_OFF or sw_ReclHome.value() == is_OFF:
        if not mute:
            if (use_sw_RiseHome and sw_RiseHome.value() == is_OFF) and (use_sw_ReclHome and sw_ReclHome.value() == is_OFF):
                printF("main -> ", "IsHome() FORBIDDEN STATE: Both sw_RiseHome & sw_RclnHome are open.")
                printF("main -> ", "IsHome()"," Please check your riseHome and reclHome switches and connections.")
                return False
            if use_sw_ReclHome and sw_ReclHome.value() == is_ON:
                printF("main -> ", "sw_RiseHome NOT at Home position.")
        return False
    else:
        #config.tm_Dn_Runtime = 0.0
        if not mute:
            printF("main -> ", "At Home position.")
        return True

rly_Up(1)
rly_Dn(1)

Is_Home()

# Establish wifi...
WebServerCommon()

printF('Ready...')


# --------------- Button Array Interrupts -------------------|
def MainUp():												#|
    irqCheck(btn_Main_Up, rly_Up, led_UP, "Main_Up2")		#|
def MainDn():												#|
    irqCheck(btn_Main_Dn, rly_Dn, led_DN, "Main_Down")		#|
def MainUp2():												#|
    irqCheck(btn_Main_Up2, rly_Up, led_UP, "Main_Up")		#|
def MainDn2():												#|
    irqCheck(btn_Main_Dn2, rly_Dn, led_DN, "Main_Down2")	#|
                                                            #|
def LogicUp():												#|
    irqCheck(btn_Logic_Up, rly_Up, led_UP, "Logic_Up")		#|
def LogicDn():												#|
    irqCheck(btn_Logic_Dn, rly_Dn, led_DN, "Logic_Down")	#|
def LogicUp2():												#|
    irqCheck(btn_Logic_Up2, rly_Up, led_UP, "Logic_Up2")	#|
def LogicDn2():												#|
    irqCheck(btn_Logic_Dn2, rly_Dn, led_DN, "Logic_Down2")	#|
# -----------------------------------------------------------|

# ------------------ Core Switch Module -------------------
def irqCheck(ctrl, relay, led, ctlText):
    if WEBCTL:
        return
    
    global tm_Dn_Runtime
    onceUp = False
    while ctrl.value():
        relay.value(ON)
        #led.duty_u16(brightness_NormIntensityLed)
        if not onceUp:
            tm = time.ticks_us() 
            printF("-------------------- ", ctlText, " --------------------")
            printF("main -> ", ctlText, " pressed")
            onceUp = True

    if onceUp:
        relay.value(OFF)
        #led.duty_u16(0)
        secs = time.ticks_diff(time.ticks_us(), tm) / 1000000
        if relay == rly_Up:
            tm_Dn_Runtime -= secs
        else:
            tm_Dn_Runtime += secs
                
        tm_Dn_Runtime = round(tm_Dn_Runtime, 2)
        printF("main -> ", ctlText, " released (", str(float("%.2f" % (secs))), " seconds, Total = ", str(tm_Dn_Runtime), ")")
        onceUp = False
# ---------------------------------------------------------

def mainRunner():
    while True:
        1==1
        MainUp()
        MainDn()
        MainUp2()
        MainDn2()
        
        LogicUp()
        LogicDn()
        LogicUp2()
        LogicDn2()
        
#time.sleep(.01)
        
try:
    mainRunner()
    #uasyncio.run(main())
                
# Exit/error...
except KeyboardInterrupt:
    # Make sure relays are off
    rly_Up.value(is_OFF)
    rly_Dn.value(is_OFF)
    DisconnectWebServer()
    printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")

# except Exception as Argument:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working
#     rly_Up.value(is_OFF)
#     rly_Dn.value(is_OFF)
#     f = open("Errors.txt", "a")
#     f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
#     f.close()

finally:
    led_UP.deinit()
    led_reclHome.deinit()
    led_riseHome.deinit()
    led_DN.deinit()


       

