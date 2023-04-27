from machine import Pin
from machine import Timer
import ntptime
import rp2
import time
from functions import *
import config
import micropython
micropython.alloc_emergency_exception_buf(100)																																																					

UP = True
DN = False
lastMotion = UP

once = False
printF("main.py IPL: (c)2023 Craver Engineering LLC \n\n")

ip = do_connect()
  
def Is_Home():
    config.tm_Dn_Runtime = round(config.tm_Dn_Runtime, 2)
    if config.tm_Dn_Runtime > -0.5 and config.tm_Dn_Runtime < 0.5:
        config.tm_Dn_Runtime = 0.0
        
    if config.sw_Home.value() == OFF:
        printF("main -> ", "NOT at Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return False
    else:
        config.tm_Dn_Runtime = 0
        printF("main -> ", "At Home position. config.tm_Dn_Runtime = ", str(config.tm_Dn_Runtime))
        return True
    
def irq_sw_Home(p):
    config.tm_Dn_Runtime = 0
    config.sw_Home_chg = True  # both rise and fall
        
config.sw_Home.irq(lambda p:irq_sw_Home(p)) # interrupt for sw_Home

ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your timezone
config.actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
      
config.rly_Up.value(OFF)
config.rly_Dn.value(OFF)
config.tm_Dn_Runtime = 0


print("\n")
printF("------------- (c)2023 CRAVER Engineering.  All rights reserved -------------")
printF("                              version " + config.version)
printF("         Raspberry Recliner Chair auxiliary controller experiment.")
printF("         This program is designed for and will only work with the propietary")
printF("         hardware controller containing a Raspberry Pico HW microcontroller.")
printF("                     See schematic Chair.kicad_sch")
printF("")
printF("  License is hereby granted to use this software and distribute it freely, as ")
printF("  long as this copyright notice is retained and modifications are clearly marked.")
printF("")
printF("                   ALL WARRANTIES ARE HEREBY DISCLAIMED.    ")
printF("")
printF("----------------------------------------------------------------------------")
printF("")
printF("chair.py startup    BETA version ", config.version)

config.tm_Dn_Runtime = -1
Is_Home()
    
#try:

while True:
    
    tm = time.ticks_ms()
    config.sw_Home_chg = False
    
# Logic UP switch...
    if config.sw_Up.value() == ON:
        if not once:
            printF("main -> ", "sw_Up pressed")
            config.rly_Up.value(ON)
            once = True
            if config.sw_Home.value() == ON or config.tm_Dn_Runtime <= 0: # at home
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
                if Is_Home():
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
        config.tm_Dn_Runtime
        printF("main -> ", "sw_released")
        Is_Home()
        once = False
        time.sleep(.2)

# Logic DN switch...
    if config.sw_Dn.value() == ON:
        if not once:
            printF("main -> ", "sw_Dn pressed")
            config.rly_Dn.value(ON)
            printF("main -> ", "rly_Dn ON")

            if not Is_Home():
                printF("main -> calling Down_To_Home()")
                Down_To_Home()
            else:
                Wait_Time(config.tm_down_step, 1, config.ignore_sw_Home, 1)
                config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
            once = True

        config.rly_Dn.value(OFF)
        printF("main -> ", "rly_Dn OFF")
        lastMotion = DN
        while config.sw_Dn.value() == ON:
            time.sleep(.1)
            
    if once is True:
        printF("main -> ", "sw_released")
        Is_Home()
        once = False
        time.sleep(.5)
        
# Main UP switch...
    while config.sw_Main_Up.value() == ON:
        if not once:
            config.rly_Up.value(ON)
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
    while config.sw_Main_Dn.value() == ON:
        if not once:
            config.rly_Dn.value(ON)
            printF("main -> ", "sw_Main_Dn pressed")
            once = True
        
    if once is True:
        config.rly_Dn.value(OFF)
        ut = time.ticks_ms()
        config.tm_Dn_Runtime += RunSeconds(tm, ut)
        printF("main -> ", "sw_Main_Dn released (", str(RunSeconds(tm, ut)  ), ") seconds")
        Is_Home()
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
# 
# except KeyboardInterrupt:  
# 
#     # Make sure relays are off
#     config.rly_Up.value(OFF)
#     config.rly_Dn.value(OFF)
#             
#     init_pins(Pin)
# 
#     
#     printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")
#   
# #6except Exception as Argument:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working
# #     config.rly_Up.value(OFF)
# #     config.rly_Dn.value(OFF)
# #     f = open("Errors.txt", "a")
# #     f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
# #     f.close()
# 
# #finally:

