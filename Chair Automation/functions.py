import network
import time
from secrets import *
import config

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
    tm = config.actual_time
    if config.enableLogging:
        tm = config.actual_time
        formatted_time = "{:02}/{:02}/{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
        mssg = "{}: {}{}{}{}"
        strng = mssg.format(formatted_time, msg, msg2, msg3, msg4)
        print(strng)
  
def Check_Button_Press():
    trigger = ""
    if config.sw_Dn.value() == ON:
        trigger = "config.sw_Dn interrupt"

    if config.sw_Up.value() == ON:
        trigger = "config.sw_Up interrupt"

    if config.sw_Home_chg == True:
        config.sw_Home_chg = False
        trigger = "config.sw_Home interrupt"
         
    return trigger

def RunSeconds(startTick, nowTick, precision = 2):
    return round((nowTick - startTick) / 1000, precision)

def Wait_Time(seconds, spc = 1, edgeDetect = 0, delay = 0): # 0=none, 1=up, 2=dn, 3=home, 4=both

    spacer = Space(spc) + "wait -> "
    once = False
    tm = time.ticks_ms()
    trigger = ""
    buttonVal = ""
    edgeDetectStr = "FULL" 
    
    if edgeDetect == config.ignore_sw_Up:
        edgeDetectStr = "config.sw_Up edge disabled for " + str(delay) + " seconds"    
    if edgeDetect == config.ignore_sw_Dn:
        edgeDetectStr = "config.sw_Dn edge disabled for " + str(delay) + " seconds"
    if edgeDetect == config.ignore_both:
        edgeDetectStr ="config.sw_Up & config.sw_Dn edge disabled for " + str(delay) + " seconds"
    if edgeDetect >= config.ignore_sw_Home:
        edgeDetectStr ="config.sw_Home edge disabled for " + str(delay) + " seconds"
    if edgeDetect == config.ignore_none:
        edgeDetectStr ="All switches edge disabled for " + str(delay) + " seconds"
        
    printF(spacer, "Edge Detection: " + edgeDetectStr)
    printF(spacer, "Duration: " + str(seconds) + " second wait...")
    
    complete = False
    while not len(trigger):
        if RunSeconds(tm, time.ticks_ms()) > config.tm_failSafeSeconds: # 60 second failsafe
            config.sw_Up.value(OFF)
            config.sw_Dn.value(OFF)
            config.rly_Up.value(OFF)
            config.rly_Dn.value(OFF)
            printF(spacer + " wait -> Complete FAILSAFE abort")
            return False
        
        if not once:
            config.sw_Home_chg == False
            printF(spacer, "interrupt delay enabled")
            once = True
        
        if RunSeconds(tm, time.ticks_ms()) > delay: # Don't start checking until after "delay" (if it's not zero)
            buttonVal = Check_Button_Press()
            
            if (edgeDetect != config.ignore_sw_Dn or edgeDetect != config.ignore_none) and buttonVal == "config.sw_Dn interrupt":
                trigger = "config.sw_Dn interrupt"
            else:
                if (edgeDetect != config.ignore_sw_Up or edgeDetect != config.ignore_none) and buttonVal == "config.sw_Up interrupt":
                    trigger = "config.sw_Up interrupt"
                else:
                    if (edgeDetect != config.ignore_sw_Home or edgeDetect != config.ignore_none) and buttonVal == "config.sw_Home interrupt":
                        trigger = "config.sw_Home interrupt"
        
        if trigger == "" and RunSeconds(tm, time.ticks_ms(), 2) > seconds:
            trigger = "Time (True)"
            
        time.sleep(.250)
            
    printF(spacer + " wait -> Complete wait time = ", str(RunSeconds(tm, time.ticks_ms())), " seconds")
    printF(spacer + " wait -> EXIT: Completed - Reason = " + trigger + " - Returning to caller")
    print("")
    once = False
    return trigger == "Time (True)"

def Space(spc):
    str = ""
    for i in range(0, spc):
        str += " "
    return str

def Top_To_Home(spc = 1):
    spacer = Space(spc) + "topToHome -> "
    config.rly_Up.value(ON)
    printF(spacer + " -> Top_To_Home() activated")
    printF(spacer + " -> ", "config.rly_Up ON")
    printF(spacer + " ->  Waiting " + str(config.tm_out_to_home) + " seconds")
    tm = time.ticks_ms()
    
    result = Wait_Time(config.tm_out_to_home - config.tm_Dn_Runtime, spc + 1, config.ignore_sw_Home, config.tm_1_wait) #ignore sw_Home for 1 second
    printF(spacer, "config.rly_Up OFF")
    config.rly_Up.value(OFF)
    config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
    
    if result is False:
        printF(spacer, "Out_To_Home interrupt")
        printF(spacer, str(config.tm_top_wait) + " second wait")
        while config.sw_Up.value() == ON or config.sw_Dn.value() == ON:
            time.sleep(.1)
    else:
        printF(spacer, str(config.tm_top_wait) + " second wait")
        result = Wait_Time(config.tm_top_wait, spc + 1, config.ignore_sw_Home)
            
        if result is False:
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
            Down_To_Home(spc + 1)
      
    printF(spacer + " -> EXIT: Returning to caller")

def Down_To_Home(spc = 1):
    spacer = Space(spc) + "downToHome -> "
    aborted = False
    tm = time.ticks_ms()
    printF(spacer, "goDn_Rcln & GPIO.wait_for_edge(sw_posHome)")
    config.rly_Dn.value(ON)
    printF(spacer, "config.rly_Dn ON")
    
    result = Wait_Time(abs(config.tm_Dn_Runtime), spc + 1, config.ignore_both, 1) #Dn, config.tm_1_wait)
    config.rly_Dn.value(OFF)
    config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
    
    printF(spacer, "config.rly_Dn OFF")
    
    if result is False or config.sw_Home.value() == ON:
        printF(spacer, ": complete.")
    else:
        printF(spacer, "Dn timeout reached: ", str(config.tm_out_to_home), ' seconds without home interrupt')
              
    printF(spacer + " EXIT: Returning to caller")
                           
