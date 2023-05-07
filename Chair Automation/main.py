from machine import Pin
from machine import Timer
import ntptime
import rp2
import time
from functions import *
import config
import micropython
micropython.alloc_emergency_exception_buf(100)																																																					

OFF = config.OFF
ON = config.ON
UP = config.UP
DN = config.DN
lastMotion = UP
config.tm_Dn_Runtime = 0

once = False
printF("main.py IPL: (c)2023 Craver Engineering LLC \n\n")

ip = do_connect()

def Is_Home(mute = False):
    config.tm_Dn_Runtime = round(config.tm_Dn_Runtime, 2)
    if config.tm_Dn_Runtime > -0.8 and config.tm_Dn_Runtime < 0.8:
        config.tm_Dn_Runtime = 0.0
    if config.sw_Home.value() == OFF:
        if not mute:
            printF("main -> ", "NOT at Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return False
    else:
        config.tm_Dn_Runtime = 0
        if not mute:
            printF("main -> ", "At Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return True
    
def irq_sw_Home(p):
    config.tm_Dn_Runtime = 0
    config.sw_Home_chg = True  # both rise and fall
    config.led_home.value(config.sw_Home.value())

def irq_rly_Up(p):
    config.led_rly_Up.value(not config.led_rly_Up.value())
    
def irq_rly_Dn(p):
    config.led_rly_Dn.value(not config.led_rly_Dn.value())
    
# def irq_sw_Up(p):
#     config.led_log_Up.value(not config.sw_up.value())
#     config.led_log_Up.Value(not config.sw_Up.value())
# def irq_sw_Dn(p):
#     config.led_log_Dn.value(not config.led_log_Dn.value())
#     config.led_log_Dn.Value(config.sw_Dn.value())
    
config.sw_Home.irq(lambda p:irq_sw_Home(p)) 	  # interrupt for sw_Home
config.rly_Up.irq(lambda p:irq_rly_Up(p)) 		  # interrupt for rly_Up
config.rly_Dn.irq(lambda p:irq_rly_Dn(p)) 		  # interrupt for rly_Dn
# config.sw_Up.irq(lambda p:irq_sw_Up(p)) # interrupt for led_log_Up
# config.sw_Dn.irq(lambda p:irq_sw_Dn(p)) # interrupt for led_log_Up

ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your timezone
config.actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
config.rly_Up.value(OFF)
config.rly_Dn.value(OFF)
config.led_rly_Up.value(OFF)
config.led_rly_Dn.value(OFF)
config.led_log_Up.value(OFF)
config.led_log_Dn.value(OFF)
config.led_home.value(OFF)

config.tm_Dn_Runtime = 0

print("\n")
print("------------- (c)2023 CRAVER Engineering.  All rights reserved -------------")
print("                              version " + config.version)
print("         Raspberry Recliner Chair auxiliary controller experiment.")
print("         This program is designed for and will only work with the propietary")
print("         hardware controller containing a Raspberry Pico HW microcontroller.")
print("                     See schematic Chair.kicad_sch")
print("")
print("  License is hereby granted to use this software and distribute it freely, as ")
print("  long as this copyright notice is retained and modifications are clearly marked.")
print("")
print("                   ALL WARRANTIES ARE HEREBY DISCLAIMED.    ")
print("")
print("----------------------------------------------------------------------------")
print("")
print("chair.py startup    BETA version ", config.version)
Is_Home()
print("")

try:
    while True:
        tm = time.ticks_ms()
        
 # Logic UP switch...
        if config.sw_Up.value() == ON:
            if not once:
                printF("------------------------- UP Procedure Started -------------------------")
                printF("main -> ", "sw_Up pressed")
                config.rly_Up.value(ON)
                once = True
                if Is_Home() or config.tm_Dn_Runtime <= 0: # at home  
                    # up 'n out
                    result = Top_To_Home()
                else:
                    printF("main -> ", "rly_Up ON")
                    if config.tm_Dn_Runtime == 0:
                        printF("main -> ", "UNUSUAL STATE: VALUE COMBO NOT PERMITTED: AtHome=False with tm_Dn_Runtime=0")
                        printF("                       Possible broken home switch/wire")
                        printF("main -> ", "using a default ", str(config.tm_10_wait)," seconds")
                        result = Wait_Time(config.tm_10_wait, 1, config.ignore_sw_Up, .5)
                        printF("main -> ", "rly_Up OFF")
                        config.rly_Up.value(OFF)
                        continue
                    else:
                        result = Wait_Time(config.tm_Dn_Runtime, 1, config.ignore_sw_Up, .5)
                        config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
                    printF("main -> ", "rly_Up OFF")
                    config.rly_Up.value(OFF)
                    if Is_Home(True):
                        printF("main -> ", "Home position overrun: compensating " + str(config.tm_HomeOverRun) + " seconds...")
                        time.sleep(.1)
                        config.rly_Dn.value(ON)
                        Wait_Time(config.tm_HomeOverRun, 1, config.ignore_sw_Home)
                        config.rly_Dn.value(OFF)
                        printF("main -> overrun complete. ", "rly_Dn OFF")
            config.rly_Up.value(OFF)
            lastMotion = UP
            while config.sw_Up.value() == ON:
                time.sleep(.1)
        if once is True:
            Is_Home()
            printF("------------------------- UP Procedure Completed -------------------------\n")
            once = False

# Logic DN switch...
        if config.sw_Dn.value() == ON:
            if not once:
                printF("------------------------- DOWN Procedure Started -------------------------")
                printF("main -> ", "sw_Dn pressed")
                config.rly_Dn.value(ON)
                printF("main -> ", "rly_Dn ON")
                if not Is_Home() or config.tm_Dn_Runtime < 0:
                    printF("main -> calling Down_To_Home()")
                    Down_To_Home()
                else:
                    Wait_Time(config.tm_down_step, 1, config.ignore_sw_Home, config.tm_down_step)
                    config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
                once = True
            config.rly_Dn.value(OFF)
            printF("main -> ", "rly_Dn OFF")
            lastMotion = DN
            while config.sw_Dn.value() == ON:
                time.sleep(.1)
        if once is True:
            Is_Home()
            printF("------------------------- DOWN Procedure Completed -------------------------\n")
            once = False
            
# Main UP switch...
        while config.sw_Main_Up.value() == ON or config.sw_Main2_Up.value() == ON:
            if not once:
                config.rly_Up.value(ON)
                #config.led_main_Up.value(ON)
                printF("-------------------- MAIN UP --------------------")
                printF("main -> ", "sw_Main_Up pressed")
                once = True
        if once is True:
            config.rly_Up.value(OFF)
            ut = time.ticks_ms()
            config.tm_Dn_Runtime -= RunSeconds(tm, ut)
            printF("main -> ", "sw_Main_Up released (", str(RunSeconds(tm, ut) ), ") seconds")
            Is_Home()
            print("")
            once = False

# Main DN switch...         
        while config.sw_Main_Dn.value() == ON or config.sw_Main2_Dn.value() == ON:
            if not once:
                config.rly_Dn.value(ON)
                printF("-------------------- MAIN DOWN --------------------")
                printF("main -> ", "sw_Main_Dn pressed")
                once = True
        if once is True:
            config.rly_Dn.value(OFF)
            ut = time.ticks_ms()
            config.tm_Dn_Runtime += RunSeconds(tm, ut)
            printF("main -> ", "sw_Main_Dn released (", str(RunSeconds(tm, ut)  ), ") seconds")
            Is_Home()
            print("")
            once = False

# Cleanup...
        once = False
        config.rly_Up.value(OFF)
        config.rly_Dn.value(OFF)
      
                
        if RunSeconds(tm, time.ticks_ms()) > config.tm_failSafeSeconds and (config.rly_Up.value()==ON or config.rly_Dn.value()==ON):
            config.sw_Up.value(OFF)
            config.sw_Dn.value(OFF)
            config.rly_Up.value(OFF)
            config.rly_Dn.value(OFF)
            printF(spacer + " wait -> FAILSAFE TIMEOUT: ", str(config.tm_failSafeSeconds), "second abort")
        
        time.sleep(.1)
        
# ^^^^^^^^^^^^^^^^^^ Loop point ^^^^^^^^^^^^^^^^^^

# Exit/error...
except KeyboardInterrupt:  
    # Make sure relays are off
    config.rly_Up.value(OFF)
    config.rly_Dn.value(OFF)
    init_pins(Pin)
    printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")
  
# except Exception as Argument:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working
#     config.rly_Up.value(OFF)
#     config.rly_Dn.value(OFF)
#     f = open("Errors.txt", "a")
#     f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
#     f.close()

#finally:



