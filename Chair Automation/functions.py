# Functions.py 
# version = 2.0.10.13

from secret import *
from config import *
import network
import time

def init_pins(Pin):
    for x in range(28):
         Pin(x).init()

def printF(msg, msg2 = "", msg3 = "", msg4 = "", msg5 = "", msg6 = "", msg7 = "", msg8 = ""):
    UTC_OFFSET = -5 * 60 * 60
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    ptm = actual_time
    formatted_time = "{:02}/{:02}/{:02} {:02}:{:02}:{:02}".format(ptm[0], ptm[1], ptm[2], ptm[3], ptm[4], ptm[5])
    mssg = "{}: {}{}{}{}{}{}{}{}"
    message = mssg.format(formatted_time, msg, msg2, msg3, msg4, msg5, msg6, msg7, msg8)
    print(message)
    if enableFileLog:
        f = open(logFilename, "a")
        f.write(message + "\n")
        f.close()
        
def RunSeconds(startTick, nowTick, precision = 2):
    return round((nowTick/1000 - startTick) / 1000, precision)

def IsPlural(number):
    if number > 1:
        return "s"
    else:
        return ""        
         
def Space(spc):
    str = ""
    for i in range(0, spc):
        str += " "
    return str

def Check_Button_Press():
    ret = 0
        
    # Controller switches...    
    if btn_Logic_Up.value() == OFF:     # 1, Logic up
        ret = id_btn_Logic_Up 			
    if btn_Logic_Up2.value() == OFF:    # 2, Logic up, bank 2
        ret += id_btn_Logic_Up2 		
    if btn_Logic_Dn.value() == OFF:     # 4, Logic down
        ret += id_btn_Logic_Dn 		
    if btn_Logic_Dn2.value() == OFF:    # 8, Logic down ,bank 2    
        ret += id_btn_Logic_Dn2 	
        
    if btn_Main_Up.value() == OFF:      # 32, Main up
        ret += id_btn_Main_Up 	
    if btn_Main_Up2.value() == OFF:     # 64, Main up, bank 2
        ret += id_btn_Main_Up2 	
    if btn_Main_Dn.value() == OFF:      # 16, Main down
        ret += id_btn_Main_Dn 	
    if btn_Main_Dn2.value() == OFF:     # 128, Main down, bank 2
        ret += id_btn_Main_Dn2 	
    
    # Limit switches...
    if sw_RiseHome.value() == 0 and use_sw_RiseHome: 	# 256, Rise home switch (if enabled)
        ret += id_sw_riseHome
    if sw_Upper.value() == 0 and use_sw_Upper:			# 512, Rise upper switch (if enabled)
        ret += id_sw_Upper
    if sw_ReclHome.value() == 0 and use_sw_ReclHome:	# 1024, Recline home switch (if enabled)
        ret += id_sw_ReclHome
    if sw_Lower.value() == 0 and use_sw_Lower:			# 2048, Recline lower switch (if enabled)
        ret += id_sw_Lower
    return ret

def SetBinString(spacer = "", binValue = 0, strString = ""):
    binStr = ""
    if binValue & id_btn_Logic_Up:						# 1
        binStr += spacer + "btn_Logic_Up" + strString
    if binValue & id_btn_Logic_Dn:						# 2
        binStr += spacer + "btn_Logic_Dn" + strString
    if binValue & id_btn_Logic_Up2:						# 4
        binStr += spacer + "btn_Logic_Up2" + strString
    if binValue & id_btn_Logic_Dn2:						# 8
        binStr += spacer + "btn_Logic_Dn2" + strString
    if binValue & id_btn_Main_Up: 						# 16
        binStr += spacer + "btn_Main_Up" + strString
    if binValue & id_btn_Main_Up2: 						# 32
        binStr += spacer + "btn_Main_Up2" + strString                
    if binValue & id_btn_Main_Dn: 						# 64
        binStr += spacer + "btn_Main_Dn" + strString    
    if binValue & id_btn_Main_Dn2: 						# 128
        binStr += spacer + "btn_Main_Dn2" + strString    
    if binValue & id_sw_riseHome and use_sw_RiseHome:  	# 256 (if enabled)
        binStr += spacer + "sw_RiseHome" + strString
    if binValue & id_sw_Upper and use_sw_Upper:  		# 512 (if enabled)
        binStr += spacer + "sw_Upper" + strString
    if binValue & id_sw_ReclHome and use_sw_ReclHome:	# 1024 (if enabled)
        binStr += spacer + "sw_reclHome" + strString
    if binValue & id_sw_Lower and use_sw_Lower:  		# 2048 (if enabled)
        binStr += spacer + "sw_Upper" + strString        

    return binStr
                
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

def SelfCheck():
    ledTime = float(0.1)
    
    led_UP.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_reclHome.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_riseHome.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_DN.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    
    
    time.sleep(ledTime)
    
    led_DN.duty_u16(0)
    time.sleep(ledTime)
    led_riseHome.duty_u16(0)
    time.sleep(ledTime)
    led_reclHome.duty_u16(0)
    time.sleep(ledTime)
    led_UP.duty_u16(0)
    
    time.sleep(ledTime)

def ShowOptions():
    if enableWiFi:
        #ip = do_connect()
        printF("WiFi is enabled")
    else:
        printF("WiFi is disabled")
    if enableFileLog:
        printF("File logging is enabled: ", logFilename)
    else:
        printF("File Logging is disabled")

    if use_sw_RiseHome:
        printF("RiseHome is enabled")
    else:
        printF("RiseHome is disabled")

    if use_sw_ReclHome:
        printF("ReclHome is enabled")
    else:
        printF("ReclHome is disabled")    


