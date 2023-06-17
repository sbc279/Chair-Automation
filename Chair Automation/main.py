# version = 2.0.6.15

from machine import Pin
from machine import Timer
import ntptime
import rp2
import time
from functions import *
import config
import micropython

micropython.alloc_emergency_exception_buf(100)																																																					

OFF_i	 = config.OFF
ON_i = config.ON
UP = config.UP
DN = config.DN

onceUp = False
onceDn = False
tm = float(0.0)

#once = False
printF("main.py IPL: (c)2023 Craver Engineering\n\n")

#ip = do_connect()


def Is_Home(runTime, mute = False):
    runTime = round(runTime, 2)
    if runTime > -0.1 and runTime < 0.1:
        runTime = 0.0
    
    config.tm_Dn_Runtime = runTime
    if config.sw_Home.value() == OFF_i:
        if not mute:
            printF("main -> ", "NOT at Home position. config.tm_Dn_Runtime = ", str(runTime))
        return False
    else:
        if runTime > 0:
            runTime = 0
        config.tm_Dn_Runtime = runTime
        if not mute:
            printF("main -> ", "At Home position. config.tm_Dn_Runtime = ", str(runTime))
        return True

# up relay
def irq_rly_Up(p):
    config.led_upper.value(not p.value())
    #config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
    #print(str(config.tm_Dn_Runtime))

# down relay
def irq_rly_Dn(p):
    config.led_lower.value(not p.value())
    #config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
 
# home limit 
def irq_sw_Home(p):
    config.led_home.value(not p.value())

# upper limit
def irq_sw_Upper(p):
    config.led_upper.value(not p.value())

# lower limit
def irq_sw_Lower(p):
    config.led_lower.value(not p.value())
    
# occup limit    
def irq_sw_Occup(p):
    config.led_occup.value(not p.value())
    
config.sw_Home.irq(lambda p:irq_sw_Home(p)) 	# interrupt for led_Home
config.sw_Upper.irq(lambda p:irq_sw_Upper(p))   # interrupt for led_upper
config.sw_Lower.irq(lambda p:irq_sw_Lower(p))   # interrupt for led_lower
config.sw_Occup.irq(lambda p:irq_sw_Occup(p))   # interrupt for led_occup
config.rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
config.rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn

def SwitchDebounce():
    while Check_Button_Press() & config.id_sw_all:
        time.sleep(.1)
        
# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
config.actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
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
time.sleep(.5)
config.rly_Up.value(OFF_i)
config.rly_Dn.value(OFF_i)
config.led_home.value(not config.sw_Home.value())
config.led_upper.value(not config.sw_Upper.value())
config.led_lower.value(not config.sw_Lower.value())
config.led_occup .value(not config.sw_Occup.value())

Is_Home(0)
print("")

try:
    while True:
        #tm = time.ticks_ms() 
        if config.tm_Dn_Runtime > -0.1 and config.tm_Dn_Runtime < 0.1:
            config.tm_Dn_Runtime = 0.0 

 # Logic UP switch...
        if config.sw_Up.value() == 1 and config.sw_Dn.value() == 0:
            SwitchDebounce()
            result = ""
            printF("------------------------- UP Procedure Started -------------------------")
            if (Is_Home(config.tm_Dn_Runtime) and config.tm_Dn_Runtime <= 0) or config.tm_Dn_Runtime < 0: # at home  
                # up 'n out
                if config.sw_Home.value() == ON:
                    config.tm_Dn_Runtime = 0
                tm = time.ticks_ms()
                config.rly_Up.value(ON_i)
                result = Up_To_Out()
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                print("ok " + resultStr + " " + str(resultVal))
                if resultStr.find("Time (True)") or resultStr.find("wait -> config.sw_Home interrupt"):
                    config.tm_Dn_Runtime = 0.0                
            else:
                printF("main -> ", "rly_Up ON")
                if config.tm_Dn_Runtime == 0:
                    printF("main -> ", "**UNUSUAL STATE** VALUE COMBO NOT PERMITTED: sw_Home=False + sw_Up=True + tm_Dn_Runtime=0 ")
                    printF("                           Possible broken or unplugged home switch and/or wire?")
                    printF("main -> ", "Aborted")
                    ErrorFlash(config.id_sw_home)
                else:
                    tm = time.ticks_ms()
                    config.rly_Up.value(ON_i)
                    result = Wait_Time(config.tm_Dn_Runtime, 1, config.id_all, False).strip()
                    resultStr = result.split(',')[0]
                    resultVal = result.split(',')[1]
                    
                    #config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
                    printF("main -> ", "rly_Up OFF_i")
                    config.rly_Up.value(OFF_i)
                    print(resultStr + "<--")
                    if resultStr != "config.sw_Up interrupt":
                        if config.sw_Home.value() == 1:
                            printF("main -> ", "Home position overrun: compensating " + str(config.tm_HomeOverRun) + " seconds...")
                            time.sleep(.1)
                            #tm = time.ticks_ms()
                            config.rly_Dn.value(ON_i)
                            printF("main -> ", "rly_Dn ON")
                            Wait_Time(config.tm_HomeOverRun, 1, 0, config.tm_sw_bounce)
                            config.rly_Dn.value(OFF_i)
                            printF("main -> ", "rly_Dn OFF")
                            printF("main -> overrun complete. ", "rly_Dn OFF")
                            
                    config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
                
            if  resultStr != "Time (True)":
                printF( "main -> Out_To_Home interrupt")
            
            config.rly_Up.value(OFF_i)
            
            if resultStr == "config.tm_Dn_Runtime reached 0":
                printF( "main -> config.tm_Dn_Runtime reached 0")
                #config.tm_Dn_Runtime = 0.0
            
            Is_Home(config.tm_Dn_Runtime)
            printF("------------------------- UP Procedure Completed -------------------------\n")

# Logic DN switch...
        if config.sw_Dn.value() == 1 and config.sw_Up.value() == 0:
            SwitchDebounce()
            result = ""
            printF("------------------------- DOWN Procedure Started -------------------------")
            printF("main -> ", "1:sw_Dn pressed")
            if not Is_Home(config.tm_Dn_Runtime) and config.tm_Dn_Runtime < 0:
                printF("main -> 2:calling Down_To_Home()")
                tm = time.ticks_ms()
                result = Down_To_Home()
                config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
            else:
                if (config.tm_Dn_Runtime >= 0 and config.sw_Home.value() == ON) or config.tm_Dn_Runtime > 0:
                    config.rly_Dn.value(ON_i)
                    printF("main -> ", "3:rly_Dn ON")
                    tm = time.ticks_ms()
                    result = Wait_Time(config.tm_down_step, 1, config.id_sw_all, config.tm_Dn_Runtime < 0).strip()
                    resultStr = result.split(',')[0]
                    resultVal = result.split(',')[1]

                    config.tm_Dn_Runtime += float(resultVal) #RunSeconds(tm, time.ticks_ms())
                    config.rly_Dn.value(OFF_i)
                else:
                    printF("main -> ", "4:**UNUSUAL STATE** VALUE COMBO NOT PERMITTED: sw_Home=False sw_Dn=True + tm_Dn_Runtime=0")
                    printF("                          Possible broken or unplugged home switch and/or wire?")
                    ErrorFlash(config.id_sw_upper)
            printF("main -> ", "5:rly_Dn OFF")

            #config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
#             print(str(config.tm_Dn_Runtime))
            print(resultStr)
            if resultStr == "  wait -> config.sw_Home interrupt":
                printF("main -> ", "Home position overrun: compensating " + str(config.tm_HomeOverRun) + " seconds...")
                time.sleep(.1)
                tm = time.ticks_ms()
                config.rly_Dn.value(ON_i)
                printF("main -> ", "rly_Dn ON")
                Wait_Time(config.tm_HomeOverRun, 1, 0, config.tm_sw_bounce)
                config.rly_Dn.value(OFF_i)
                printF("main -> ", "rly_Dn OFF")
                printF("main -> overrun complete. ", "rly_Dn OFF")
                config.tm_Dn_Runtime = 0.0
            config.rly_Dn.value(OFF_i)
            Is_Home(config.tm_Dn_Runtime)
#             print(str(config.tm_Dn_Runtime))
            printF("------------------------- DOWN Procedure Completed -------------------------\n")

# Main UP switch...
        while Check_Button_Press() & config.id_sw_Main_Up + config.id_sw_Main_Up2 + config.id_sw_Up2:
            if not onceUp:
                tm = time.ticks_ms()
                config.rly_Up.value(ON_i)
                printF("-------------------- MAIN UP --------------------")
                printF("main -> ", "sw_Main_Up pressed")
                onceUp = True
                
        # Up button released...
        if onceUp is True:
            config.rly_Up.value(OFF_i)
            config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
            printF("main -> ", "sw_Main_Up released (", str(config.tm_Dn_Runtime), ") seconds")
            Is_Home(config.tm_Dn_Runtime)
            print("")
            onceUp = False

# Main DN switch...         
        while Check_Button_Press() & config.id_sw_Main_Dn + config.id_sw_Main_Dn2 + config.id_sw_Dn2:
            if not onceDn:
                config.rly_Dn.value(ON_i)
                tm = time.ticks_ms()
                printF("-------------------- MAIN DOWN --------------------")
                printF("main -> ", "sw_Main_Dn pressed")
                onceDn = True
                
        # Dn button released...
        if onceDn is True:
            config.rly_Dn.value(OFF_i)
            config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
            printF("main -> ", "sw_Main_Dn released (", str(config.tm_Dn_Runtime), ") seconds")
            Is_Home(config.tm_Dn_Runtime)
            print("")
            onceDn = False

# Failsafe...
        if (config.rly_Up.value() == ON or config.rly_Dn.value() == ON) and RunSeconds(tm, time.ticks_ms()) > config.tm_failSafeSeconds:
            config.led_upper.off()
            config.led_occup.off()
            config.rly_Up.value(OFF_i)
            config.rly_Dn.value(OFF_i)
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
    config.rly_Up.value(OFF_i)
    config.rly_Dn.value(OFF_i)
    #init_pins(Pin)
    printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")
  
# except Exception as Argument:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working
#     config.rly_Up.value(OFF_i)
#     config.rly_Dn.value(OFF_i)
#     f = open("Errors.txt", "a")
#     f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
#     f.close()

#finally:


