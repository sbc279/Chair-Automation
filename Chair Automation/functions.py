# version = "2.0.5.30"

import network
import time
from secrets import *
import config

trigger = 0
OFF = config.OFF
ON = config.ON
UP = config.UP
DN = config.DN
lastMotion = UP

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

def printF(msg, msg2 = "", msg3 = "", msg4 = ""):
    UTC_OFFSET = -5 * 60 * 60
    config.actual_time = time.localtime(time.time() + UTC_OFFSET)
    tm = config.actual_time
    tm = config.actual_time
    formatted_time = "{:02}/{:02}/{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
    mssg = "{}: {}{}{}{}"
    strng = mssg.format(formatted_time, msg, msg2, msg3, msg4)
    print(strng)
    if config.enableLogging == True:
        f = open(config.debugLog, "a")
        f.write(strng + "\n")
        f.close()
         
         
def Check_Button_Press():
    trigger = 0
    ret = 0
    
# Is the switch pressed?    
    if config.sw_Up.value() == 1:
        ret += config.id_sw_Up 			# 1
    if config.sw_Up_2.value() == 1:        
        ret += config.id_sw_Up2 		# 2
    if config.sw_Dn.value() == 1:
        ret += config.id_sw_Dn 			# 4
    if config.sw_Dn_2.value() == 1:        
        ret += config.id_sw_Dn2 		# 8
    if config.sw_Main_Up.value() == 0:
        ret += config.id_sw_Main_Up 	# 16
    if config.sw_Main_Up2.value() == 0:
        ret += config.id_sw_Main_Up2 	# 32
    if config.sw_Main_Dn.value() == 0:
        ret += config.id_sw_Main_Dn 	# 64
    if config.sw_Main_Dn2.value() == 0:
        ret += config.id_sw_Main_Dn2 	# 128
    
# Is the led on?
    if config.led_home.value() == 1:
        ret += config.id_led_home  		# 256
    if config.led_upper.value() == 1:
        ret += config.id_led_upper 		# 512
    if config.led_lower.value() == 1:
        ret += config.id_led_lower 		# 1024
    if config.led_occup.value() == 1:
        ret += config.id_led_occup 		# 2048
        
#     if config.tm_Dn_Runtime > 0:
#         ret += 4096
    
    return ret

# def resetIrqChange():
#     for x in range(1, 2, 3, 4):
#         config.chg(x) = False

def RunSeconds(startTick, nowTick, precision = 2):
    return round((nowTick - startTick) / 1000, precision)

def IsPlural(number):
    if number > 1:
        return "s"
    else:
        return ""
    
def Wait_Time(seconds, spc = 1, edgeDetect = 0, delay = 0): # 0=none, 1=up, 2=dn, 4=home, 8=both
    # Compensate for PICO delay
    picoDelay = .08
    seconds = seconds - picoDelay
    spacer = Space(spc) + "wait -> "
    once = False
    tm = time.ticks_ms()
    trigger = 0
    exitReason = ""
    edgeDetectStr = "FULL" 
    homeValue = config.sw_Home.value()
        
    if edgeDetect == -1:     			# 0
        edgeDetectStr ="All switches edge disabled for " + str(delay) + " second" + IsPlural(delay)    
    if edgeDetect & config.id_sw_Up:    # 1
        edgeDetectStr = "config.sw_Up edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & config.id_sw_Dn:    # 2
        edgeDetectStr = "config.sw_Dn edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & (config.id_sw_Up2 or config.id_main_sw_Up2):
        edgeDetectStr = "config.sw_main_Up edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & (config.id_sw_Dn2 or config.id_main_sw_Dn2):
        edgeDetectStr = "config.sw_main_Up edge disabled for " + str(delay) + " second" + IsPlural(delay)

    if edgeDetect & config.id_led_home:  # 8
        edgeDetectStr ="config.sw_Home edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & config.id_led_upper:  # 8
        edgeDetectStr ="config.sw_Upper edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & config.id_led_lower:  # 8
        edgeDetectStr ="config.sw_Lower edge disabled for " + str(delay) + " second" + IsPlural(delay)
    if edgeDetect & config.id_led_occup:  # 8
        edgeDetectStr ="config.sw_Occup edge disabled for " + str(delay) + " second" + IsPlural(delay)
        
    printF(spacer, "Edge Detection: " + edgeDetectStr)
    printF(spacer, "Duration: " + str(seconds + picoDelay) + " second" + IsPlural(delay) + " wait...")
    
    complete = False
    while trigger == 0:
        if RunSeconds(tm, time.ticks_ms()) > config.tm_failSafeSeconds: # 60 second failsafe
            config.sw_Up.value(OFF)
            config.sw_Dn.value(OFF)
            config.rly_Up.value(OFF)
            config.rly_Dn.value(OFF)
            printF(spacer + " wait -> Complete FAILSAFE abort")
            return False
        
        if not once:
            printF(spacer, "interrupt delay enabled")
            once = True
    
        if RunSeconds(tm, time.ticks_ms()) > delay: # Don't start checking until after "delay" (if it's not zero)
            
            trigger = Check_Button_Press()
           
        if trigger == 0 and RunSeconds(tm, time.ticks_ms(), 2) > seconds:
            trigger = -1
            exitReason = "Time (True)"
     
    if trigger == 1:
        exitReason = "config.sw_Up interrupt"
    if trigger == 2:
        exitReason = "config.sw_Up2 iterrupt"            
    if trigger == 4:
        exitReason = "config.sw_Dn interrupt"
    if trigger == 8:
        exitReason = "config.sw_Dn2 iterrupt"            
    if trigger == 16:
        exitReason = "config.sw_Main_Up interrupt"
    if trigger == 32:
        exitReason = "config.sw_Main_Up2 iterrupt"
    if trigger == 64:
        exitReason = "config.sw_Main_Dn interrupt"
    if trigger == 128:
        exitReason = "config.sw_Main_Dn2 interrupt"
    if trigger == 256:
        exitReason = "config.sw_Home interrupt"
    if trigger == 512:
        if not edgeDetect & trigger:
            exitReason = "config.sw_Upper interrupt"
    if trigger == 1024:
        exitReason = "config.sw_Lower interrupt"
    if trigger == 2048:
        exitReason = "config.sw_Occup interrupt"
#     if trigger & 4098:
#         exitReason = "config.tm_Dn_Runtime 0 reached"
        
    printF(spacer + "EXIT: Completed - Reason = " + exitReason)
    printF(spacer + "Complete wait time = ", str(RunSeconds(tm, time.ticks_ms())), " seconds - Returning to caller")
    once = False
    return exitReason #== "Time (True)"

def Space(spc):
    str = ""
    for i in range(0, spc):
        str += " "
    return str

def Top_To_Home(spc = 1):
    spacer = Space(spc) + "topToHome -> "
    config.rly_Up.value(ON)
    printF(spacer + "Top_To_Home() activated")
    printF(spacer + "config.rly_Up ON")
    printF(spacer + "Waiting " + str(config.tm_out_to_home + config.tm_Dn_Runtime) + " seconds")
    tm = time.ticks_ms()
    result = Wait_Time(config.tm_out_to_home + config.tm_Dn_Runtime, spc + 1, 0, config.tm_1_wait) #ignore sw_Home for 1 second
    config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
    printF(spacer, "config.rly_Up OFF")
    config.rly_Up.value(OFF)
    if result != "config.sw_Upper interrupt" and result != "Time (True)":
        printF(spacer, "Out_To_Home interrupt")
        printF(spacer + "EXIT: Returning to caller (l:234)")
        printF(spacer, str(config.tm_top_wait) + " second wait")
#         while config.sw_Up.value() == 1 or config.sw_Dn.value() == 1:
#             time.sleep(.1)
        return False
    else:
        printF(spacer, str(config.tm_top_wait) + " second wait")
        result = Wait_Time(config.tm_top_wait, spc + 1, 0, config.tm_top_wait + 1)
#         printF(spacer, "-- here --")
        if result != "Time (True)":
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
            printF(spacer, "TopWait complete")
            Down_To_Home(spc + 1)
      
      
    printF(spacer + "EXIT: Returning to caller")
    return result

def Down_To_Home(spc = 1):
    spacer = Space(spc) + "downToHome -> "
    aborted = False
    tm = time.ticks_ms()
    printF(spacer, "goDn_Rcln & GPIO.wait_for_edge(sw_posHome)")
    config.rly_Dn.value(ON)
    printF(spacer, "config.rly_Dn ON")
    
    ignored = config.id_sw_Dn + config.id_sw_Dn2 + config.id_sw_Main_Dn + config.id_sw_Main_Dn2
    result = Wait_Time(abs(config.tm_out_to_home), spc + 1, config.id_led_upper, config.tm_1_wait) #Dn, config.tm_1_wait)
    config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
    config.rly_Dn.value(OFF)
    printF(spacer, "config.rly_Dn OFF")
    
    if config.sw_Home.value() == ON:
        config.tm_Dn_Runtime = 0
        printF(spacer, ": complete. At home")
    else:
        printF(spacer, "Dn timeout reached: ", str(config.tm_out_to_home), ' seconds without home interrupt')
              
    printF(spacer + " EXIT: Returning to caller")
                           



