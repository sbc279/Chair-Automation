# Functions.py 
# version = 2.1

from config import *
import network
import time
from utility import *

                
def Wait_Time(seconds, spc = 1, watchedBin = 0, checkRunTime = False):

    # Compensate for PICO's latency
    picoLatency = 0 #.11
    
    seconds = seconds - picoLatency
    spacer = Space(spc) + "wait -> "
    once = False
    wtm = time.ticks_ms()
    trigger = 0
    exitReason = ""
    complete = False
    lf = "\n\t\t"
    watchedBinStr = "none"

    if watchedBin > 0:
        watchedBinStr = SetBinString("\t\t" , watchedBin, " edge detection is being monitored" + lf)

    printF(spacer, "Watched Edge Detection: " + str(watchedBin))
    printF(spacer, "Adjusted Wait Time: ", str(seconds) + " second", IsPlural(seconds)) 
    if checkRunTime == True:
        watchedBinStr += spacer + "tm_Dn_Runtime is being monitored" + lf
        
    if watchedBinStr.endswith(lf): # strip off the trailing feed/tab, if needed        
       watchedBinStr = watchedBinStr.rstrip(lf)        
    
    while exitReason == "":
        if checkRunTime == True:
            if abs(tm_Dn_Runtime) - RunSeconds(wtm, time.ticks_ms()) <= 0:
                exitReason = "tm_Dn_Runtime reached 0"
        
        trigger = Check_Button_Press()
       
        if watchedBin & trigger:
            exitReason = SetBinString(spacer, watchedBin & trigger, " interrupt")
        
        if exitReason == "" and (RunSeconds(wtm, time.ticks_ms(), 2) > seconds):
            trigger = -1
            exitReason = "Time (True)"

        
    printF(spacer + "EXIT: Completed - Reason = " + exitReason)
    printF(spacer + "Complete wait time = ", str(RunSeconds(wtm, time.ticks_ms())), " seconds - Returning to caller")
    once = False
    
    return exitReason + "," + str(RunSeconds(wtm, time.ticks_ms()))

def Up_To_Out(spc = 1, tm_Dn_Runtime= 0):
    spacer = Space(spc) + "topToHome -> "
    rly_Up.value(ON)
    printF(spacer + "Up_To_Out() activated.  tm_Dn_Runtime = ", str(tm_Dn_Runtime))
    printF(spacer + "rly_Up ON")
    
## ----- Go UP -----
    
    if sw_RiseHome.value() == ON:
        tm_temp = tm_out_to_home - tm_Dn_Runtime
    else:
        tm_temp = tm_out_to_home

    printF(spacer + "Waiting " + str(tm_temp) + " seconds")
    result = Wait_Time(tm_temp, spc + 1, id_All - id_sw_riseHome - id_sw_ReclHome)

    printF(result)
    resultStr = result.split(',')[0]
    resultVal = result.split(',')[1]
    
    printF(spacer, "rly_Up OFF")
    rly_Up.value(OFF)
    
    if resultStr != "sw_Upper interrupt" and resultStr != "Time (True)":
        printF(spacer, "Out_To_Home interrupt")
        printF(spacer + "EXIT: Returning to caller (l:234)")
        return result
    else:
## ----- TopWait -----
        
        # Manually turn on the LED's
        led_DN.duty_u16(brightness_NormIntensityLed)
        led_UP.duty_u16(brightness_NormIntensityLed)
        
        printF(spacer, str(tm_top_wait) + " second wait")
        result = Wait_Time(tm_top_wait, spc + 1, id_All - id_sw_ReclHome - id_sw_riseHome).strip()
        resultStr = result.split(',')[0]

        # Manually turn off the LED's
        led_UP.duty_u16(0)
        # The relay interrupt will resume LED control from here
        
        if resultStr != "Time (True)":
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
            
## ----- Go DOWN -----
            led_DN.duty_u16(brightness_NormIntensityLed)
            printF(spacer, "TopWait complete")
            result = Down_To_Home(spc + 1, tm_temp)
            led_DN.duty_u16(0)
            
    printF(spacer + "EXIT: Returning to caller")
    return result

def Down_To_Home(spc = 1, duration = float(0.0)):
    spacer = Space(spc) + "downToHome -> "
    rly_Dn.value(ON)
    printF(spacer, "rly_Dn ON")
    printF(spacer, "tm_Dn_Runtime = " + str(duration))
    ignorer = 0
    if id_sw_ReclHome:
        ignorer = id_sw_ReclHome   
    result = Wait_Time(duration, spc + 1, id_All - ignorer, False)
    resultStr = result.split(',')[0]
    resultVal = result.split(',')[1]

    rly_Dn.value(OFF)
    printF(spacer, "rly_Dn OFF")
    
    if sw_RiseHome.value() == ON:
        printF(spacer, ": complete. At home")
    else:
        if resultStr == "Time (True)" or resultStr == "tm_Dn_Runtime reached 0": 
            printF(spacer, "Dn timeout reached: ", str(resultVal), ' seconds without home interrupt')
        else:
            printF(spacer, resultStr, " interrupt detected")
            
    printF(spacer + " EXIT: Returning to caller: " + str(resultVal))
    return result


