import time
from config import *

def SwitchDebounce():
    while Check_Button_Press() & id_sw_All:
        time.sleep(.1)

def Is_Home(mute = False):
    if sw_RiseHome.value() == OFF or sw_ReclHome.value() == OFF:
        if (use_sw_RiseHome and sw_RiseHome.value() == OFF) and (use_sw_ReclHome and sw_ReclHome.value() == OFF):
            printF("main -> ", "IsHome() FORBIDDEN STATE: Both sw_RiseHome & sw_RclnHome are open.")
            printF("main -> ", "IsHome()"," Please check your riseHome and reclHome switches and connections.")
            return False
        if use_sw_ReclHome and sw_ReclHome.value() == ON:
           printF("main -> ", "sw_RiseHome NOT at Home position.")
        return False
    else:
        tm_Dn_Runtime = 0.0
        printF("main -> ", "At Home position.")
        return True
    
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

