# version = 2.0.7.17
import config
from secrets import *
from config import *
import network
import time
# import _thread

def do_connect(ssid=secrets['ssid'],psk=secrets['password']):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)
    printF("Establishing Internet connectivity via the \""+ secrets['ssid']+ "\" access point...")
    # Wait for connect or fail
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        time.sleep(1)
 
    # Handle connection error
    if wlan.status() != 3:
        printF('Connectivity failed. No Internet connection')
        printF('Attempting to run without it. Date ranges will be incorrect.')
        printF('Please check the credentials in the file \"secrets.py\"')
        return '0'
        #raise RuntimeError('WIFi connection failed')
    else:
        printF(secrets['ssid'], ' WiFi connection established')
        ip=wlan.ifconfig()[0]
        printF('Details: ', wlan.ifconfig())
        return ip
 
def init_pins(Pin):
    for x in range(28):
         Pin(x).init()


def printF(msg, msg2 = "", msg3 = "", msg4 = "", msg5 = "", msg6 = ""):
    UTC_OFFSET = -5 * 60 * 60
    actual_time = time.localtime(time.time() + UTC_OFFSET)
    ptm = actual_time
    formatted_time = "{:02}/{:02}/{:02} {:02}:{:02}:{:02}".format(ptm[0], ptm[1], ptm[2], ptm[3], ptm[4], ptm[5])
    mssg = "{}: {}{}{}{}{}{}"
    strng = mssg.format(formatted_time, msg, msg2, msg3, msg4, msg5, msg6)
    if config.enableLogging:
        print(strng)
    if config.enableFileLog:
        f = open(config.logFilename, "a")
        f.write(strng + "\n")
        f.close()
        
def RunSeconds(startTick, nowTick, precision = 2):
    return round((nowTick - startTick) / 1000, precision)

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
    if sw_Up.value() == 1:
        ret = id_sw_Up 			# 1, Logic up
    if sw_Up_2.value() == 1:        
        ret += id_sw_Up2 		# 2, Logic down
    if sw_Dn.value() == 1:
        ret += id_sw_Dn 		# 4, Logic up, bank 2
    if sw_Dn_2.value() == 1:        
        ret += id_sw_Dn2 		# 8, Logic down ,bank 2
    if sw_Main_Up.value() == 1:
        ret += id_sw_Main_Up 	# 16, Main up
    if sw_Main_Up2.value() == 1:
        ret += id_sw_Main_Up2 	# 32, Main down
    if sw_Main_Dn.value() == 1:
        ret += id_sw_Main_Dn 	# 64, Main up, bank 2
    if sw_Main_Dn2.value() == 1:
        ret += id_sw_Main_Dn2 	# 128, Main down, bank 2
    
    # Limit switches...
    #if not  id_ignoreLimitsSwitches:
    if sw_RiseHome.value() == 0:
        ret += id_sw_riseHome  	# 256, Limit switch rise 'Home'
    if sw_Upper.value() == 0:
        ret += id_sw_upper 		# 512, Limit switch 'Upper'
    if sw_ReclHome.value() == 0:
        ret += id_sw_reclHome 	# 1024, Limit switch 'Lower'
    if sw_Occup.value() == 0:
        ret += id_sw_occup 		# 2048, Limit switch 'Occupancy'
    return ret

def SetBinString(spacer = "", binValue = 0, strString = ""):
    binStr = ""
    if binValue & id_sw_Up:    # 1
        binStr += spacer + "sw_Up" + strString
    if binValue & id_sw_Dn:    # 2
        binStr += spacer + "sw_Dn" + strString
    if binValue & id_sw_Up2:	# 4
        binStr += spacer + "sw_Up2" + strString
    if binValue & id_sw_Dn2:	# 8
        binStr += spacer + "sw_Dn2" + strString
    if binValue & id_sw_Main_Up: # 16
        binStr += spacer + "sw_Main_Up" + strString
    if binValue & id_sw_Main_Up2: # 32
        binStr += spacer + "sw_Main_Up2" + strString                
    if binValue & id_sw_Main_Dn: #64
        binStr += spacer + "sw_Main_Dn" + strString    
    if binValue & id_sw_Main_Dn2: #128
        binStr += spacer + "sw_Main_Dn2" + strString    
    if binValue & id_sw_riseHome:  # 256
        binStr += spacer + "sw_RiseHome" + strString
    if binValue & id_sw_upper:  # 512
        binStr += spacer + "sw_Upper" + strString
    if binValue & id_sw_reclHome:  # 1024
        binStr += spacer + "sw_reclHome" + strString
    if binValue & id_sw_occup:  # 2048
        binStr += spacer + "sw_Occup" + strString
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

    printF(spacer, "Watched Edge Detection: " + str(watchedBin)) #lf + watchedBinStr)
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

def Up_To_Out(spc = 1):
    spacer = Space(spc) + "topToHome -> "
    rly_Up.value(ON)
    printF(spacer + "Up_To_Out() activated")
    printF(spacer + "rly_Up ON")
    
## ----- Go UP -----
    
    if sw_RiseHome.value() == OFF:
        tm_temp = tm_home_to_out - abs(tm_Dn_Runtime)
    else:
        tm_temp = tm_home_to_out

    printF(spacer + "Waiting " + str(tm_temp) + " seconds")
    result = Wait_Time(tm_temp, spc + 1, id_all - id_sw_riseHome - id_sw_reclHome) # - id_sw_reclHome)

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
        led_occup.on()
        printF(spacer, str(tm_top_wait) + " second wait")
        result = Wait_Time(tm_top_wait, spc + 1, id_all - id_sw_reclHome - id_sw_riseHome).strip()
        resultStr = result.split(',')[0]

        led_occup.off()
        if resultStr != "Time (True)":
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
## ----- Go DOWN -----
            printF(spacer, "TopWait complete")
            result = Down_To_Home(spc + 1, tm_temp)
     
    printF(spacer + "EXIT: Returning to caller")
    return result

def Down_To_Home(spc = 1, duration = float(0.0)):
    spacer = Space(spc) + "downToHome -> "
    aborted = False
    config.rly_Dn.value(ON)
    sec=float(0)
    sec = config.tm_Dn_Runtime #float(tm_home_to_out) + tm_Dn_Runtim

    if duration > 0.0:
        sec = duration
    printF(spacer, "rly_Dn ON")
    printF(spacer, "tm_Dn_Runtime = " + str(sec))
    result = Wait_Time(sec, spc + 1, id_all - id_sw_reclHome, False)

    resultStr = result.split(',')[0]
    resultVal = result.split(',')[1]

    rly_Dn.value(OFF)
    printF(spacer, "rly_Dn OFF")
    
    if config.sw_RiseHome.value() == ON:
        printF(spacer, ": complete. At home")
        #config.tm_Dn_Runtime = 0.0
    else:
        if resultStr == "Time (True)" or resultStr == "tm_Dn_Runtime reached 0": #resultStr == "sw_RiseHome interrupt":
            printF(spacer, "Dn timeout reached: ", str(resultVal), ' seconds without home interrupt')
            #tm_Dn_Runtime = 0.0
        else:
            printF(spacer, resultStr, " interrupt detected")
            #runTime = float(resultVal)
        #config.tm_Dn_Runtime += float(resultVal) + 0.8
            
    printF(spacer + " EXIT: Returning to caller: " + str(config.tm_Dn_Runtime))
    return result
                           
# def SelfCheck():
#     ledTime = float(0.105)
#     
#     
#     #time.sleep(ledTime)
#     
#     
#     #time.sleep(ledTime)
#     led_upper.on()
#     led_occup.on()
#     led_recl.on()
#     #time.sleep(ledTime)
#     led_home.on()
#     
#     time.sleep(.5)
#     
#     led_home.off()
#     time.sleep(ledTime)
#     led_recl.off()
#     time.sleep(ledTime)
#     led_occup.off()    
#     
#     led_upper.off()
#     time.sleep(ledTime)
# 
# #     
# #     time.sleep(ledTime)
# #     led_occup.off()
#     time.sleep(ledTime)
#     #ErrorFlash() # not really an error

def ErrorFlash(id = 0):
    old_Occ = led_occup.value()
    old_Low = led_recl.value()
    old_Hi = led_upper.value()
    old_Home = led_home.value()
    
    led_occup.off()
    led_recl.off()
    led_upper.off()
    led_home.off()
    
    for x in [1, 2, 3]:
        led_recl.toggle()
        led_occup.toggle()
        led_upper.toggle()
        led_home.toggle()
        time.sleep(.1)

    if id > 0:
        for x in [1, 2, 3]:
            if id & id_sw_reclHome:
                led_recl.toggle()
            if id & id_sw_occup:
                led_occup.toggle()                
            if id & id_sw_upper:
                led_upper.toggle()
            if id & id_sw_RiseHome:
                led_home.toggle()
            time.sleep(.5)
        
    led_occup.value(old_Occ)
    led_recl.value(old_Low)
    led_upper.value(old_Hi)
    led_home.value(old_Home)

        
     

