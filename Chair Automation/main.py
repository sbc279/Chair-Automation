# version = 2.0.7.17

from machine import Pin, PWM, Timer
import _thread
import ntptime
import rp2
import time
import _thread
from functions import *
import config
import micropython
# from config import config

micropython.alloc_emergency_exception_buf(100)																																																					

OFF_i = config.OFF
ON_i = config.ON
UP = config.UP
DN = config.DN

onceUp = False
onceDn = False
tm = float(0.0)
ledOn = (config.duty_cycle/100)*65_535

# Set LED brightness ----------------------------------------
ledOn = 10000 #(config.duty_cycle/100)*65_535
pwm_homeLed = PWM(config.led_home) # Attach PWM object on the LED pin
pwm_reclLed = PWM(config.led_recl) # Attach PWM object on the LED pin
# pwm_upperLed = PWM(config.led_upper) # Attach PWM object on the LED pin
# pwm_occupLed = PWM(config.led_occup) # Attach PWM object on the LED pin
pwm_homeLed.freq(config.ledFreq)
pwm_reclLed.freq(config.ledFreq)
# pwm_upperLed.freq(config.ledFreq)
# pwm_occupLed.freq(config.ledFreq)
# ---------------------------------------------------------------

#once = False
print("main.py IPL: (chair) startup  BETA version " + config.version + "\n")

if config.enableWiFi:
    ip = do_connect()

x = 0

def SetZeroTime():
    if config.use_sw_RiseHome and config.sw_RiseHome.value() and config.use_sw_ReclHome and config.sw_ReclHome.value():
        config.tm_Dn_Runtime = 0.0
        return True
    else:
        return False
        
# up relay
def irq_rly_Up(p):
    x = 0
    config.led_occup.value(not p.value())
#     if not p.value():
#         pwm_occupLed.duty_u16(10000)
#     else:
#         pwm_occupLed.deinit()    

# down relay
def irq_rly_Dn(p):
    x = 0
    config.led_upper.value(not p.value())
#     if not p.value():
#         pwm_upperLed.duty_u16(10000)
#     else:
#         pwm_upperLed.deinit() #   config.led_lower.value(not p.value())
 
# home limit 
def irq_sw_RiseHome(p):
    if not p.value():
        pwm_homeLed.duty_u16(10000)
    else:
        pwm_homeLed.deinit()
        
# # upper limit
# def irq_sw_Upper(p):
#     x = 0
#     if not p.value():
#         pwm_upperLed.duty_u16(10000)
#     else:
#         pwm_upperLed.deinit()
        
# recl limit
def irq_sw_Recl(p):
    x = 0
    if not p.value():
        pwm_reclLed.duty_u16(10000)
    else:
        pwm_reclLed.deinit()
    
# # occup limit    
# def irq_sw_Occup(p):
#     x = 0
#     if not p.value():
#         pwm_occupLed.duty_u16(10000)
#     else:
#         pwm_occupLed.deinit()  
#J9
def irq_J9(p):
    # Immediately remove J9's power...
    config.plug_J9.value(OFF_i)
    time.sleep(.5)
    config.plug_J9.value(config.enableJ9)
    
config.sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) 	# interrupt for led_Home
#config.sw_Upper.irq(lambda p:irq_sw_Upper(p))   # interrupt for led_upper
config.sw_ReclHome.irq(lambda p:irq_sw_Recl(p))   # interrupt for led_lower
#config.sw_Occup.irq(lambda p:irq_sw_Occup(p))   # interrupt for led_occup
config.rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
config.rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn
config.sw_J9.irq(lambda p:irq_J9(p))			# interrupt for sw_J9
                 
def SwitchDebounce():
    while Check_Button_Press() & config.id_sw_all:
        time.sleep(.1)
        
# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
config.actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
config.tm_Dn_Runtime = 0

def Is_Home(runTime, mute = False):
    runTime = round(runTime, 2)
    if (runTime >= -0.1 and runTime <= 0.1) or SetZeroTime() :
        runTime = 0.0

    config.tm_Dn_Runtime = runTime
    if  (config.use_sw_RiseHome and config.sw_RiseHome.value() == OFF_i) or (config.use_sw_ReclHome and config.sw_ReclHome.value() == OFF_i):
        if not mute:
            printF("main -> ", "sw_RiseHome NOT at Home position. config.tm_Dn_Runtime = ", str(runTime))
            SetZeroTime()
            return False
    else:
        if not mute:
            printF("main -> ", "At Home position. config.tm_Dn_Runtime = ", str(runTime))
            SetZeroTime()        
        return True
print("""
------------------- Copyright 2023 CRAVER Engineering. -------------------

    Recliner Chair auxiliary controller experiment. This program is
    designed for and will only work with the proprietary hardware
    controller. See schematic Chair.kicad_sch.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.
    If not, see <https://www.gnu.org/licenses/gpl-3.0.html#license-text>
 

--------------------------------------------------------------------------\n""")

printF("*started*")

# SelfCheck()
# time.sleep(.5)
# config.rly_Up.value(OFF_i)
# config.rly_Dn.value(OFF_i)
# config.led_home.value(not config.sw_RiseHome.value())
# config.led_upper.value(not config.sw_Upper.value())
# config.led_recl.value(not config.sw_ReclHome.value())
# config.led_occup .value(not config.sw_Occup.value())
# 
# 
# 
Is_Home(0)
print("")

#_thread.start_new_thread(Blink, (2,5))

try:
    while True:
        if config.tm_Dn_Runtime >= -0.3 and config.tm_Dn_Runtime <= 0.3:
            config.tm_Dn_Runtime = 0.0
            
 # Logic UP switch...
        if config.sw_Up.value() == 1:
            SwitchDebounce()
            result = ""
            printF("------------------------- UP Procedure Started -------------------------")
            #if (config.use_sw_RiseHome and not config.sw_RiseHome.value() and config.tm_Dn_Runtime <= 0) or config.tm_Dn_Runtime <= 0:
            if(config.use_sw_RiseHome and config.sw_RiseHome.value() == ON_i and config.use_sw_ReclHome and config.sw_ReclHome.value() == ON_i) or (config.use_sw_RiseHome and config.sw_RiseHome.value() == OFF_i) or (config.use_Times and config.tm_Dn_Runtime <= 0):
                # up 'n out
                tm = time.ticks_ms()
                config.rly_Up.value(ON_i)
                result = Up_To_Out() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                if resultStr.startswith("Time (True)") > 0: # or 
                    config.tm_Dn_Runtime -= float(resultVal)
                else:            
                    printF("main -> ", resultStr)
                    config.tm_Dn_Runtime = 0.0
     
            else:
                printF("main -> ", "rly_Up ON")
                tm = time.ticks_ms()
                config.rly_Up.value(ON_i)
                ignorer = config.id_sw_riseHome
                if config.use_sw_ReclHome:
                    ignorer -= config.id_sw_reclHome
                result = Wait_Time(config.tm_Dn_Runtime, 1, config.id_all - ignorer, False)
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                printF("main -> ", "rly_Up OFF_i")
                config.rly_Up.value(OFF_i)
                config.tm_Dn_Runtime -= float(resultVal)
                if config.use_sw_ReclHome and resultStr.find("sw_reclHome"):
                    config.tm_Dn_Runtime = 0
                    printF( "main -> sw_reclHome interrupt")
                else:
                    if config.sw_RiseHome.value() == 1:
                        config.led_occup.on()
                        printF("main -> ", "Home position overrun: compensating " + str(config.tm_HomeOverRun) + " seconds...")
                        time.sleep(.1)
                        config.rly_Dn.value(ON_i)
                        printF("main -> ", "rly_Dn ON")
                        Wait_Time(config.tm_HomeOverRun, 1, 0, config.tm_sw_bounce)
                        config.rly_Dn.value(OFF_i)
                        printF("main -> ", "rly_Dn OFF")
                        printF("main -> overrun complete. ", "rly_Dn OFF")
                        config.led_occup.off()
                
                config.rly_Up.value(OFF_i)
               
            Is_Home(config.tm_Dn_Runtime)
            printF("------------------------- UP Procedure Completed -------------------------\n")
            SwitchDebounce()
            
# Logic DN switch...
        if config.sw_Dn.value() == 1 :
            SwitchDebounce()
            result = ""
            printF("------------------------- DOWN Procedure Started -------------------------")
            resultStr = ""
            resultVal = float(0.0)
            printF("main -> ", "1:sw_Dn pressed")
            if (config.use_sw_RiseHome and config.sw_RiseHome.value() == OFF_i) or (config.use_Times and config.tm_Dn_Runtime < 0):
                printF("main -> 2:calling Down_To_Home()")
                tm = time.ticks_ms()
                result = Down_To_Home()
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                config.rly_Dn.value(OFF_i)
                config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
            else:
                config.rly_Dn.value(ON_i)
                printF("main -> ", "3:rly_Dn ON")
                tm = time.ticks_ms()
                result = Wait_Time(config.tm_down_step, 1, config.id_sw_all) # , config.tm_Dn_Runtime < 0)
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                config.tm_Dn_Runtime += float(resultVal)
                config.rly_Dn.value(OFF_i)
                printF("main -> ", resultStr)

            Is_Home(config.tm_Dn_Runtime)
            printF("------------------------- DOWN Procedure Completed -------------------------\n")
            SwitchDebounce()
            
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
            #Is_Home(config.tm_Dn_Runtime)
            printF("")
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
            #Is_Home(config.tm_Dn_Runtime)
            printF("")
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
    config.led_recl.value(not OFF)	# not = temp
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


