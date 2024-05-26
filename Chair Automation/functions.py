# Functions.py 
# version = 5.26.24

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
    return round((nowTick/1000 - startTick/1000) / 1000, precision)

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
    if btn_Logic_Up.value() == True:     # 1, Logic up
        ret = id_btn_Logic_Up 			
    if btn_Logic_Up2.value() == True:    # 2, Logic up, bank 2
        ret += id_btn_Logic_Up2 		
    if btn_Logic_Dn.value() == True:     # 4, Logic down
        ret += id_btn_Logic_Dn 		
    if btn_Logic_Dn2.value() == True:    # 8, Logic down ,bank 2    
        ret += id_btn_Logic_Dn2 	
        
    if btn_Main_Up.value() == True:      # 32, Main up
        ret += id_btn_Main_Up 	
    if btn_Main_Up2.value() == True:     # 64, Main up, bank 2
        ret += id_btn_Main_Up2 	
    if btn_Main_Dn.value() == True:      # 16, Main down
        ret += id_btn_Main_Dn 	
    if btn_Main_Dn2.value() == True:     # 128, Main down, bank 2
        ret += id_btn_Main_Dn2 	
    
    # Limit switches...
    if sw_RiseHome.value() == False and use_sw_RiseHome: 	# 256, Rise home switch (if enabled)
        ret += id_sw_RiseHome
    if sw_Upper.value() == False and use_sw_Upper:			# 512, Rise upper switch (if enabled)
        ret += id_sw_Upper
    if sw_ReclHome.value() == False and use_sw_ReclHome:	# 1024, Recline home switch (if enabled)
        ret += id_sw_ReclHome
    if sw_Lower.value() == False and use_sw_Lower:			# 2048, Recline lower switch (if enabled)
        ret += id_sw_Lower
    return ret

def SetBinString(spacer = "", binValue = 0, strString = ""):
    if binValue & id_btn_Logic_Up:						# 1
        return spacer + "btn_Logic_Up" + strString
    if binValue & id_btn_Logic_Dn:						# 2
        return spacer + "btn_Logic_Dn" + strString
    if binValue & id_btn_Logic_Up2:						# 4
        return spacer + "btn_Logic_Up2" + strString
    if binValue & id_btn_Logic_Dn2:						# 8
        return spacer + "btn_Logic_Dn2" + strString
    if binValue & id_btn_Main_Up: 						# 16
        return spacer + "btn_Main_Up" + strString
    if binValue & id_btn_Main_Up2: 						# 32
        return spacer + "btn_Main_Up2" + strString                
    if binValue & id_btn_Main_Dn: 						# 64
        return spacer + "btn_Main_Dn" + strString    
    if binValue & id_btn_Main_Dn2: 						# 128
        return spacer + "btn_Main_Dn2" + strString    
    if binValue & id_sw_RiseHome:  # and use_sw_RiseHome:  	# 256 (if enabled)
        return spacer + "sw_RiseHome" + strString
    if binValue & id_sw_Upper and use_sw_Upper:  		# 512 (if enabled)
        return spacer + "sw_Upper" + strString
    if binValue & id_sw_ReclHome: # and use_sw_ReclHome:	# 1024 (if enabled)
        return spacer + "sw_reclHome" + strString
    if binValue & id_sw_Lower and use_sw_Lower:  		# 2048 (if enabled)
        return spacer + "sw_Upper" + strString        
   
    return ""

def WaitLogic(duration, useTime, watchBin):
    spacer = Space(1) + "waitLogic -> "
    once = False
    wtm = time.ticks_ms()
    trigger = 0
    exitReason = ""
    
#     if not useTime, and watchBin > 0:
#         # # For the duration, Watch for 'watchBin' switch only
#         watchBinStr = SetBinString("\t\t" , watchBin, " edge detection ONLY is being monitored" + lf)
#         printF(spacer, "Watched Edge Detection ONLY for: " + str(watchedBin))
#         while exitReason == "":
#         not Check_Button_Press() == watchBin or not RunSeconds(wtm, time.ticks_ms(), 2) >= duration):
#             time.sleep(.01)
#         
#         exitReason = "Duration reached 0"
#         Summary(wtm, interrupt, exitReason)            
#         return exitReason + "," + str(RunSeconds(wtm, time.ticks_ms()))
    
    if useTime and watchBin > 0:
        # For the duration, but Watch for any switch (ignoring the'watchBin' switch)
        printF(spacer, "Waiting ", str(duration), " seconds while Watching Edge Detection: " + str(watchBin))
        printF(spacer, SetBinString("\t\t" , watchBin, " edge detection is being monitored"))
        # NORMAL opereation
        while exitReason == "":
            if RunSeconds(wtm, time.ticks_ms(), 2) >= duration:
                exitReason = "Duration reached 0"
                interrupt = False
                time.sleep(.01)
            else:
                trigger = Check_Button_Press()
                if watchedBin & trigger:
                    exitReason = SetBinString(spacer, watchBin & trigger, " interrupt")
                    interrupt = True
                    time.sleep(.01)
            
        Summary(spacer, wtm, interrupt, exitReason)
        return exitReason + "," + str(RunSeconds(wtm, time.ticks_ms()))
    
    if not useTime and watchBin > 0:
        # For the duration ONLY, while watching for any switch (ignoring the'watchBin' switch)
        printF(spacer, "Waiting ", str(duration), " seconds ONLY, while Watching Edge Detection: " + str(watchBin))
        printF(spacer, SetBinString("\t\t" , watchBin, " edge detection is being monitored"))
        while exitReason == "":
            if RunSeconds(wtm, time.ticks_ms(), 2) >= duration:
                exitReason = "Duration reached 0"
                interrupt = False
                time.sleep(.01)
            else:
                trigger = Check_Button_Press()
                if not watchBin & trigger:
                    exitReason = SetBinString(spacer, watchBin & trigger, " interrupt")
                    interrupt = True
                    time.sleep(.01)
            
        Summary(spacer, wtm, interrupt, exitReason)
        return exitReason + "," + str(RunSeconds(wtm, time.ticks_ms()))

def Summary(spacer, wtm, interrupt, exitReason):
    if interrupt:   
        printF(spacer + "EXIT: INTERRUPTED - Reason = " + exitReason)
    else:
        printF(spacer + "EXIT: Completed - Reason = " + exitReason)
    printF(spacer + "Complete wait time = ", str(RunSeconds(wtm, time.ticks_ms())), " seconds - Returning to caller")
    
            
# def Wait_Time(seconds, spc = 1, watchedBin = 0, checkRunTime = False, Dn_Runtime = 0):
# 
#     # Compensate for PICO's latency
#     picoLatency = 0 #.11
#     
#     seconds = seconds - picoLatency
#     spacer = Space(spc) + "wait -> "
#     once = False
#     wtm = time.ticks_ms()
#     trigger = 0
#     exitReason = ""
#     complete = False
#     lf = "\n\t\t"
#     watchedBinStr = "none"
#     interrupt = False
#     
#     if watchedBin > 0:
#         watchedBinStr = SetBinString("\t\t" , watchedBin, " edge detection is being monitored" + lf)
# 
#     printF(spacer, "Watched Edge Detection: " + str(watchedBin))
# 
#     if checkRunTime == True:
#         watchedBinStr += spacer + "tm_Dn_Runtime is being monitored" + lf
# 
#     if watchedBinStr.endswith(lf): # strip off the trailing feed/tab, if needed        
#        watchedBinStr = watchedBinStr.rstrip(lf)        
#          
#     while exitReason == "":
#         if checkRunTime == True and Dn_Runtime > 0:
#             if RunSeconds(wtm, time.ticks_ms(), 2) > abs(Dn_Runtime):
#                 exitReason = "tm_Dn_Runtime reached 0"
#                 interrupt = True
#         
#         trigger = Check_Button_Press()
#        
#         if watchedBin & trigger:
#             exitReason = SetBinString(spacer, watchedBin & trigger, " interrupt")
#             interrupt = True
#         
# #         if exitReason == "" and (checkRunTime and RunSeconds(wtm, time.ticks_ms(), 2) > seconds):
# #             trigger = -1
# #             exitReason = "Time (True)"
# 
#     if interrupt:   
#         printF(spacer + "EXIT: INTERRUPTED - Reason = " + exitReason)
#     else:
#         printF(spacer + "EXIT: Completed - Reason = " + exitReason)
#     printF(spacer + "Complete wait time = ", str(RunSeconds(wtm, time.ticks_ms())), " seconds - Returning to caller")
#     once = False
#     
#     return exitReason + "," + str(RunSeconds(wtm, time.ticks_ms()))

def Up_To_Out(tm_Dn_Runtime = 0):
    spc = 1
    spacer = Space(spc) + "topToHome -> "
    rly_Up.value(ON)
    #led_BLU.duty_u16(brightness_NormIntensityLed)
    printF(spacer + "Up_To_Out() activated.  tm_Dn_Runtime = ", str(tm_Dn_Runtime))
    printF(spacer + "rly_Up ON")
    
## ----- Go UP -----
    
#     if True #sw_RiseHome.value() == False:
    tm_temp = tm_out_to_home # - tm_Dn_Runtime
#     else:
#         tm_temp = tm_out_to_home

    printF(spacer + "Waiting " + str(tm_temp) + " seconds")
    # result = Wait_Time(tm_temp, spc + 1, id_all - id_sw_RiseHome - id_sw_ReclHome - id_btn_Logic_Up, False)
    watchBin = id_all - id_sw_RiseHome + id_btn_Logic_Up
    result = WaitLogic(tm_out_to_home, False, watchBin)
    
    printF(result)
    resultStr = result.split(',')[0]
    resultVal = result.split(',')[1]
    
    printF(spacer, "rly_Up OFF")
    rly_Up.value(OFF)
    
    if resultStr != "btn_Logic_Upper interrupt" and resultStr != "Time (True)":
        printF(spacer, "Out_To_Home interrupt")
        printF(spacer + "EXIT: Returning to caller (l:234)")
        return result
    else:
## ----- TopWait -----
        
        # Manually turn on the LED's
        led_BLU.duty_u16(brightness_NormIntensityLed)
        led_WHT.duty_u16(brightness_NormIntensityLed)
        
        printF(spacer, str(tm_top_wait) + " second wait")
        # result = Wait_Time(tm_top_wait, spc + 1, id_all - id_sw_ReclHome + id_sw_RiseHome).strip()
        result = WaitLogic(tm_top_wait, False, id_sw_allLimits) #id_all - id_sw_RiseHome)
        resultStr = result.split(',')[0]
        resultTime = float(result.split(',')[1])
        
        # Manually turn off the LED's
        led_WHT.duty_u16(0)
        led_BLU.duty_u16(0)
        # The relay interrupt will resume LED control from here
        
        if resultStr != "Time (True)":
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
            
## ----- Go DOWN -----
            resultTime = float(result.split(',')[1])
            durationTime = tm_out_to_home - abs(tm_Dn_Runtime)
            printF(spacer, "TopWait complete")
            printF(spacer, "tm_Dn_Runtime = ", tm_Dn_Runtime)
            printF(spacer, "Time consumed: ", resultTime)
            printF(spacer, "durationTime = ", durationTime)
            result = Down_To_Home(spc + 1, tm_out_to_home)
            
    printF(spacer + "EXIT: Returning to caller")
    return result

def Down_To_Home(spc = 1, duration = float(0.0)):
    spacer = Space(spc) + "downToHome -> "
    rly_Dn.value(ON)
    printF(spacer, "rly_Dn ON")
    printF(spacer, "duration = ", duration)
    ignorer = 0
    #if id_sw_ReclHome:
    ignorer = id_btn_Logic_Dn  
    # result = Wait_Time(tm_out_to_home, spc + 1, id_all - ignorer, False)
    result = WaitLogic(tm_out_to_home, False, id_all - id_btn_Logic_Dn)
    resultStr = result.split(',')[0]
    resultTime = result.split(',')[1]

    rly_Dn.value(OFF)
    printF(spacer, "rly_Dn OFF")
    
    if sw_RiseHome.value() == False:
        printF(spacer, ": complete. At home")
    else:
        if resultStr == "Time (True)" or resultStr == "tm_Dn_Runtime reached 0": 
            printF(spacer, "Dn timeout reached: ", resultTime, ' seconds without home interrupt')
        else:
            printF(spacer, resultStr, " interrupt detected")
            
    printF(spacer + " EXIT: Returning to caller: ", resultTime)
    return result

def SelfCheck():
    printF("SelfCheck...")
    ledTime = float(0.2)
    breakTime = float(0.1)
    
    led_RED.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_WHT.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_YEL.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    led_BLU.duty_u16(brightness_NormIntensityLed)
    time.sleep(ledTime)
    
    
    time.sleep(ledTime)
    for x in range(.2):
        led_BLU.duty_u16(0)
        led_YEL.duty_u16(0)
        led_WHT.duty_u16(0)
        led_RED.duty_u16(0)
        time.sleep(breakTime)#------------------------------------------
        led_BLU.duty_u16(brightness_HighIntensityLed)
        led_YEL.duty_u16(brightness_HighIntensityLed)
        led_WHT.duty_u16(brightness_HighIntensityLed)
        led_RED.duty_u16(brightness_HighIntensityLed)
        time.sleep(breakTime)
    
    led_BLU.duty_u16(0)
    time.sleep(ledTime)
    led_YEL.duty_u16(0)
    time.sleep(ledTime)
    led_WHT.duty_u16(0)
    time.sleep(ledTime)
    led_RED.duty_u16(0)
    
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


