# version = 2.0.10.10

from machine import Pin, PWM, Timer
import micropython
import ntptime
import rp2
import time
import _thread
from functions import *
from config import *
import config

micropython.alloc_emergency_exception_buf(100)																																																					

is_OFF = OFF
is_ON = ON

onceUp = False 
onceDn = False
tm = float(0.0)

#once = False
print("main.py IPL: (chair) startup  BETA version " + version + "\n")
#if enableWiFi:
#    ip = do_connect()

# up relay
def irq_rly_Up(p):
    if not p.value():
        led_UP.duty_u16(brightness_NormIntensityLed)    
    else:
        led_UP.duty_u16(0)
    
# down relay
def irq_rly_Dn(p):
    if not p.value():
        led_DN.duty_u16(brightness_HighIntensityLed)    
    else:
        led_DN.duty_u16(0)
        
# home limit 
def irq_sw_RiseHome(p):
    if not p.value():
        led_riseHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_riseHome.duty_u16(0)
      
# recl limit
def irq_sw_Recl(p):
    if not p.value():
        led_reclHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_reclHome.duty_u16(0)
    
   
sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) 	# interrupt for led_riseHome
sw_ReclHome.irq(lambda p:irq_sw_Recl(p))   # interrupt for led_lower
rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn
        
def SwitchDebounce():
    while Check_Button_Press() & id_sw_all:
        time.sleep(.1)

# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)
tm_Dn_Runtime = 0

def Is_Home(mute = False):
    printF("sw_RiseHome: ",str(sw_RiseHome.value() == is_ON))
    printF("sw_ReclHome: ",str(sw_ReclHome.value() == is_ON),"\n")
    if sw_RiseHome.value() == is_OFF or sw_ReclHome.value() == is_OFF:
        if not mute:
            if sw_RiseHome.value() == is_OFF and sw_ReclHome.value() == is_OFF:
                printF("main -> ", "ERROR! Both sw_RclnHome & sw_RclnHome are open!")
                return False
            if sw_ReclHome.value() == is_OFF:
                printF("main -> ", "sw_RclnHome NOT at Home position.")
            else:
                printF("main -> ", "sw_RiseHome NOT at Home position.")
        return False
    else:
        config.tm_Dn_Runtime = 0
        if not mute:
            printF("main -> ", "At Home position.")
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

#SelfCheck()

Is_Home()

print("")

try:
    while True:
           
 # Logic UP switch...
        if sw_Up.value() == is_OFF:
            SwitchDebounce()
            result = ""
            printF("------------------------- UP Procedure Started -------------------------")
            if sw_ReclHome.value() == is_ON or sw_RiseHome.value() == is_OFF:
                # up 'n out
                tm = time.ticks_ms()
                rly_Up.value(is_ON)
                result = Up_To_Out(tm_Dn_Runtime) 
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                #tm_Dn_Runtime -= float(resultVal)
                printF("main -> ", resultStr.replace("  wait -> ", ""))
            else:
                printF("main -> ", "rly_Up ON")
                tm = time.ticks_ms()
                rly_Up.value(is_ON)
                ignorer = id_sw_riseHome
                if use_sw_RiseHome:
                    ignorer = id_sw_riseHome                
                result = Wait_Time(tm_down_step + 2, 1, id_all - ignorer, False)
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                printF("main -> ", "rly_Up is_OFF")
                rly_Up.value(is_OFF)
                tm_Dn_Runtime -= float(resultVal)
                if resultStr.find("sw_reclHome"):
                    tm_Dn_Runtime -= 0
                    printF( "main -> sw_reclHome interrupt")
            Is_Home()
            printF("------------------------- UP Procedure Completed -------------------------\n")
            SwitchDebounce()
            
# Logic DN switch.../
        if sw_Dn.value() == 1 :
            SwitchDebounce()
            result = ""
            resultStr = ""
            resultVal = float(0.0)
            printF("main -> ", "1:sw_Dn pressed")
            if sw_RiseHome.value() == is_OFF:
                printF("main -> 2:calling Down_To_Home()")
                tm = time.ticks_ms()

                result = Down_To_Home(1, tm_home_to_out)
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                rly_Dn.value(is_OFF)
                tm_Dn_Runtime += float(resultVal) 
            else:
                rly_Dn.value(is_ON)
                printF("main -> ", "3:rly_Dn ON")
                tm = time.ticks_ms()
                result = Wait_Time(tm_down_step, 1, id_sw_all)
                resultStr = result.split(',')[0]
                resultVal = result.split(',')[1]
                tm_Dn_Runtime += float(resultVal)
                rly_Dn.value(is_OFF)
                printF("main -> ", resultStr)
            Is_Home()
            printF("------------------------- DOWN Procedure Completed -------------------------\n")
            SwitchDebounce()
            
# Main UP switch...
        while Check_Button_Press() & id_sw_Main_Up + id_sw_Main_Up2 + id_sw_Up2:
            if not onceUp:
                tm = time.ticks_ms()
                rly_Up.value(is_ON)
                printF("-------------------- MAIN UP --------------------")
                printF("main -> ", "sw_Main_Up pressed")
                onceUp = True
                
        # Up button released...
        if onceUp is True:
            rly_Up.value(is_OFF)
            secs = float("%.2f" % RunSeconds(tm, time.ticks_ms()))
            tm_Dn_Runtime -= secs
            tm_Dn_Runtime = float("%.2f" % tm_Dn_Runtime)
            printF("main -> ", "sw_Main_Up released (", str(float("%.2f" % secs)), " seconds, Total = ", str(tm_Dn_Runtime), ")")
            onceUp = False
            Is_Home()
            
# Main DN switch...         
        while Check_Button_Press() & id_sw_Main_Dn + id_sw_Main_Dn2 + id_sw_Dn2:
            if not onceDn:
                rly_Dn.value(is_ON)
                tm = time.ticks_ms()
                printF("-------------------- MAIN DOWN --------------------")
                printF("main -> ", "sw_Main_Dn pressed")
                onceDn = True
                
        # Dn button released...
        if onceDn is True:
            rly_Dn.value(is_OFF)
            secs = float("%.2f" % RunSeconds(tm, time.ticks_ms()))
            tm_Dn_Runtime += secs
            tm_Dn_Runtime = float("%.2f" % tm_Dn_Runtime)
            printF("main -> ", "sw_Main_Dn released (", str(float("%.2f" % secs)), " seconds, Total = ", str(tm_Dn_Runtime), ")")  
            onceDn = False
            Is_Home()
            
        # Failsafe...
        if (rly_Up.value() == ON or rly_Dn.value() == ON) and RunSeconds(tm, time.ticks_ms()) > tm_failSafeSeconds:
            rly_Up.value(is_OFF)
            rly_Dn.value(is_OFF)
            printF("Main -> FAILSAFE TIMEOUT: ", str(tm_failSafeSeconds), "second abort")
         
        time.sleep(.1)
        
# ^^^^^^^^^^^^^^^^^^ Loop point ^^^^^^^^^^^^^^^^^^

# Exit/error...
except KeyboardInterrupt:
    # Make sure relays are off
    rly_Up.value(is_OFF)
    rly_Dn.value(is_OFF)
    printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")
  
except Exception as Argument:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working
    rly_Up.value(is_OFF)
    rly_Dn.value(is_OFF)
    f = open("Errors.txt", "a")
    f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
    f.close()

finally:

    rly_Up.value(is_OFF)
    rly_Dn.value(is_OFF)
    led_UP.deinit()
    led_reclHome.deinit()
    led_riseHome.deinit()
    led_DN.deinit()
