# version = 2.0.6.02

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
global tm
tm = float(0.0)

once = False
printF("main.py IPL: (c)2023 Craver Engineering LLC \n\n")

#ip = do_connect()

def Is_Home(mute = False):
    config.tm_Dn_Runtime = round(config.tm_Dn_Runtime, 2)
    if config.tm_Dn_Runtime > -0.1 and config.tm_Dn_Runtime < 0.1:
        config.tm_Dn_Runtime = 0.0
        
    if config.sw_Home.value() == OFF:
        if not mute:
            printF("main -> ", "NOT at Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return False
    else:
        #config.tm_Dn_Runtime = 0
        if not mute:
            printF("main -> ", "At Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return True

def irq_rly_Up_fall(p):
    global tm
    tm = time.ticks_ms()
        
def irq_rly_Dn_fall(p):
    global tm
    tm = time.ticks_ms()
        
def irq_sw_Home(p):
    #config.tm_Dn_Runtime = 0
    config.led_home.value(p.value())

# upper limit
def irq_sw_Upper(p):
    config.led_upper.value(not p.value())

# lower limit
def irq_sw_Lower(p):
    config.led_lower.value(not p.value())

# home limit
def irq_home(p):
    config.led_home.value(not p.value())
    
# occup limit    
def irq_sw_Occup(p):
    config.led_occup.value(not p.value())
    
config.sw_Home.irq(lambda p:irq_home(p)) 	# interrupt for led_Home
config.sw_Upper.irq(lambda p:irq_sw_Upper(p))   # interrupt for led_upper
config.sw_Lower.irq(lambda p:irq_sw_Lower(p))   # interrupt for led_lower
config.sw_Occup.irq(lambda p:irq_sw_Occup(p))   # interrupt for led_occup
config.rly_Up.irq(lambda p:irq_rly_Up_fall(p), trigger=Pin.IRQ_FALLING) 		# interrupt for rly_Up
config.rly_Dn.irq(lambda p:irq_rly_Dn_fall(p), trigger=Pin.IRQ_FALLING)  		# interrupt for rly_Dn

def SwitchDebounce():
    while Check_Button_Press() & config.ignore_all_sw:
        time.sleep(.1)
        
# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
config.actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
config.rly_Up.value(OFF)
config.rly_Dn.value(OFF)

config.led_occup.value(not OFF)	# not = temp
config.led_lower.value(not OFF)	# not = temp
config.led_upper.value(not OFF)	# not = temp
config.led_home.value(not OFF)	# not = temp
 
config.tm_Dn_Runtime = 0

print("\n")
print("------------- (c)2023 CRAVER Engineering.  All rights reserved -------------")
print("                              version " + config.version)
print("         Raspberry Recliner Chair auxiliary controller experiment.")
print("         This program is designed for and will only work with the proprietary")
print("         hardware controller. See schematic Chair.kicad_sch")
print("")
print("  License is hereby granted to use this software and distribute it freely, as ")
print("  long as this copyright notice is retained, modifications are clearly marked,")
print("  and the usage is NOT part of any commercial entity.")
print("")
print("      ALL WARRANTIES, EITHER EXPRESSED OR IMPLIED, ARE HEREBY DISCLAIMED.    ")
print("")
print("----------------------------------------------------------------------------")
print("")
print("chair.py startup    BETA version ", config.version)

SelfCheck()

Is_Home()
print("")

try:
    while True:
        #tm = time.ticks_ms()
        
 # Logic UP switch...
        if config.sw_Up.value() == 1 and config.sw_Dn.value() == 0:
            result = ""
            once = False
            if not once:
                printF("------------------------- UP Procedure Started -------------------------")
                printF("main -> ", "sw_Up pressed")
                
                once = True
                if Is_Home() or config.tm_Dn_Runtime <= 0: # at home  
                    # up 'n out
                    config.rly_Up.value(ON)
                    result = Up_To_Out()
                else:
                    printF("main -> ", "rly_Up ON")
                    if config.tm_Dn_Runtime == 0:
                        printF("main -> ", "UNUSUAL STATE: VALUE COMBO NOT PERMITTED: AtHome=False with tm_Dn_Runtime=0")
                        printF("                       Possible broken home switch/wire")
                        printF("main -> ", "Aborted")
                        ErrorFlash(config.ignore_led_home)
                        continue
                    else:
                        config.rly_Up.value(ON)
                        result = Wait_Time(config.tm_Dn_Runtime, 1, config.ignore_led_home + config.id_sw_Up + config.id_dn_runtime, config.tm_1_wait, True)
                        
                        config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
                        printF("main -> ", "rly_Up OFF")
                        config.rly_Up.value(OFF)
                        
#                     if Is_Home(True):
#                         printF("main -> ", "Home position overrun: compensating " + str(config.tm_HomeOverRun) + " seconds...")
#                         time.sleep(.1)
#                         config.rly_Dn.value(ON)
#                         Wait_Time(config.tm_HomeOverRun, 1, 0, config.tm_sw_bounce)
#                         config.rly_Dn.value(OFF)
#                         printF("main -> overrun complete. ", "rly_Dn OFF")
                if  result != "Time (True)":
                    printF( "main -> Out_To_Home interrupt")
            
            config.rly_Up.value(OFF)
            lastMotion = UP
            SwitchDebounce()
            if once is True:
                if result == "config.tm_Dn_Runtime reached 0":
                    #printF( "main -> config.tm_Dn_Runtime reached 0")
                    config.tm_Dn_Runtime = 0.0
            Is_Home()
            printF("------------------------- UP Procedure Completed -------------------------\n")
            once = False

# Logic DN switch...
        if config.sw_Dn.value() == 1 and config.sw_Up.value() == 0:
            if not once:
                printF("------------------------- DOWN Procedure Started -------------------------")
                printF("main -> ", "sw_Dn pressed")
                config.rly_Dn.value(ON)
                printF("main -> ", "rly_Dn ON")
                if not Is_Home() or config.tm_Dn_Runtime < 0:
                    printF("main -> calling Down_To_Home()")
                    Down_To_Home()
                else:
                    if config.tm_Dn_Runtime == 0:
                        config.tm_Dn_Runtime = .01
                    result = Wait_Time(config.tm_down_step, 1, config.ignore_led_home, config.tm_down_step)
                    config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
                once = True
            config.rly_Dn.value(OFF)
            printF("main -> ", "rly_Dn OFF")
            lastMotion = DN
            SwitchDebounce()
        if once is True:
            Is_Home()
            printF("------------------------- DOWN Procedure Completed -------------------------\n")
            once = False


# Main UP switch...
        while Check_Button_Press() & config.ignore_sw_Main_Up + config.ignore_sw_Main_Up2 + config.ignore_sw_Up2: #.sw_Main_Up.value() == 1 and config.sw_Main_Dn.value() == 0) or (config.sw_Main_Up2.value() == 0 and config.sw_Main_Dn2.value() == 1):
            if not once:
                config.rly_Up.value(ON)
                printF("-------------------- MAIN UP --------------------")
                printF("main -> ", "sw_Main_Up pressed")
                once = True
        if once is True:
            config.rly_Up.value(OFF)
            ut = time.ticks_ms()
            config.tm_Dn_Runtime -= RunSeconds(tm, ut)
            printF("main -> ", "sw_Main_Up released (", str(config.tm_Dn_Runtime), ") seconds")
            Is_Home()
            print("")
            once = False

# Main DN switch...         
        while Check_Button_Press() & config.ignore_sw_Main_Dn + config.ignore_sw_Main_Dn2 + config.ignore_sw_Dn2: #(config.sw_Main_Dn.value() == 1 and config.sw_Main_Up.value() == 0) or (config.sw_Main_Dn2.value() == 0 and config.sw_Main_Up2.value() == 1):
            if not once:
                config.rly_Dn.value(ON)
                printF("-------------------- MAIN DOWN --------------------")
                printF("main -> ", "sw_Main_Dn pressed")
                once = True
        if once is True:
            config.rly_Dn.value(OFF)
            ut = time.ticks_ms()
            config.tm_Dn_Runtime += RunSeconds(tm, ut)
            printF("main -> ", "sw_Main_Dn released (", str(config.tm_Dn_Runtime), ") seconds")
            Is_Home()
            print("")
            once = False

# Cleanup...
        once = False
        config.rly_Up.value(OFF)
        config.rly_Dn.value(OFF)
      
                
        if round(config.tm_Dn_Runtime, 2) > config.tm_failSafeSeconds and (config.rly_Up.value()==ON or config.rly_Dn.value()==ON):
            config.sw_Up.value(OFF)
            config.sw_Dn.value(OFF)
            config.rly_Up.value(OFF)
            config.rly_Dn.value(OFF)
            printF(spacer + " wait -> FAILSAFE TIMEOUT: ", str(config.tm_failSafeSeconds), "second abort")
        
        time.sleep(.1)
        
# ^^^^^^^^^^^^^^^^^^ Loop point ^^^^^^^^^^^^^^^^^^

# Exit/error...
except KeyboardInterrupt:
    config.led_home.value(not OFF)	# not = temp
    config.led_upper.value(not OFF)	# not = temp
    config.led_lower.value(not OFF)	# not = temp
    config.led_occup.value(not OFF)	# not = temp

    # Make sure relays are off
    config.rly_Up.value(OFF)
    config.rly_Dn.value(OFF)
    #init_pins(Pin)
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


