# version = 2.0.6.02

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
    if config.enablePrint:
        print(strng)
    if config.enableLogging == True:
        f = open(config.debugLog, "a")
        f.write(strng + "\n")
        f.close()
         
         
def Check_Button_Press(checkRunTime = False, startTicks = float(0.0)):
    #trigger = 0
    ret = 0
    
# Is the switch pressed?    
    if config.sw_Up.value() == 1:
        ret += config.ignore_sw_Up 			# 1
    if config.sw_Up_2.value() == 1:        
        ret += config.ignore_sw_Up2 		# 2
    if config.sw_Dn.value() == 1:
        ret += config.ignore_sw_Dn 			# 4
    if config.sw_Dn_2.value() == 1:        
        ret += config.ignore_sw_Dn2 		# 8
    if config.sw_Main_Up.value() == 1:
        ret += config.ignore_sw_Main_Up 	# 16
    if config.sw_Main_Up2.value() == 1:
        ret += config.ignore_sw_Main_Up2 	# 32
    if config.sw_Main_Dn.value() == 1:
        ret += config.ignore_sw_Main_Dn 	# 64
    if config.sw_Main_Dn2.value() == 1:
        ret += config.ignore_sw_Main_Dn2 	# 128
    
# Is the led on?
    if config.led_home.value() == 1:
        ret += config.ignore_led_home  		# 256
    if config.led_upper.value() == 1:
        ret += config.ignore_led_upper 		# 512
    if config.led_lower.value() == 1:
        ret += config.ignore_led_lower 		# 1024
    if config.led_occup.value() == 1:
        ret += config.ignore_led_occup 		# 2048
 
    if checkRunTime == True:
        rt = abs(config.tm_Dn_Runtime) - RunSeconds(startTicks, time.ticks_ms(), 2)
        rt = round(rt, 2)
        if rt > -0.1 and rt < 0.1:
            ret += config.id_dn_runtime
    
    return ret

def RunSeconds(startTick, nowTick, precision = 2):
    return round((nowTick - startTick) / 1000, precision)

def IsPlural(number):
    if number > 1:
        return "s"
    else:
        return ""
    
def Wait_Time(seconds, spc = 1, ignoredBin = 0, ignoredDelay = 0, checkRunTime = False):
    
    # id_none = 		-1
    # id_all =			0
    # id_sw_Up = 		1
    # id_sw_Up2 = 		2
    # id_sw_Dn = 		4
    # id_sw_Dn2 = 		8
    # id_sw_Main_Up = 	16
    # id_sw_Main_Up2 = 	32
    # id_sw_Main_Dn = 	64
    # id_sw_Main_Dn2 = 	128
    # id_led_home = 	256
    # id_led_upper = 	512
    # id_led_lower = 	1024
    # id_led_occup = 	2048    

    # Compensate for PICO's latency
    picoLatency = 0
    
    seconds = seconds - picoLatency
    spacer = Space(spc) + "wait -> "
    once = False
    tm = time.ticks_ms()
    trigger = 0
    exitReason = ""
    ignoredBinStr = "\n\t\t" 
    homeValue = config.sw_Home.value()

    if ignoredBin == -1: 	    			# 0
        ignoredBinStr ="All switches edge enabled after " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) 
    else:
        if ignoredBin == 0: 	    			# 0
            ignoredBinStr ="All switches edge disabled"
        else:
            if ignoredBin & config.ignore_sw_Up:    # 1
                ignoredBinStr += spacer + "config.sw_Up edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_sw_Dn:    # 2
                ignoredBinStr += spacer + "config.sw_Dn edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_sw_Up2:	# 4
                ignoredBinStr += spacer + "config.sw_Up2 edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_sw_Dn2:	# 8
                ignoredBinStr += spacer + "config.sw_Dn2 edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_sw_Main_Up: # 16
                ignoredBinStr += spacer + "config.sw_Main_Up edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_sw_Main_Up2: # 32
                ignoredBinStr += spacer + "config.sw_Main_Up2 edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"                
            if ignoredBin & config.ignore_sw_Main_Dn: #64
                ignoredBinStr += spacer + "config.sw_Main_Dn edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"    
            if ignoredBin & config.ignore_sw_Main_Dn2: #128
                ignoredBinStr += spacer + "config.sw_Main_Dn2 edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"    
            if ignoredBin & config.ignore_led_home:  # 256
                ignoredBinStr += spacer + "config.sw_Home edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_led_upper:  # 512
                ignoredBinStr += spacer + "config.sw_Upper edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_led_lower:  # 1024
                ignoredBinStr += spacer + "config.sw_Lower edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if ignoredBin & config.ignore_led_occup:  # 2048
                ignoredBinStr += spacer + "config.sw_Occup edge disabled for " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay) + "\n\t\t"
            if checkRunTime and ignoredBin & config.id_dn_runtime:  # 4096
                ignoredBinStr += spacer + "tm_Dn_Runtime is being monitored" # after " + str(ignoredDelay) + " second" + IsPlural(ignoredDelay)



            # strip off the trailing feed/tab, if needed        
            if ignoredBinStr.endswith("\n\t\t"):
               ignoredBinStr = ignoredBinStr.rstrip("\n\t\t") 
    
        
    printF(spacer, "Edge Detection: " + ignoredBinStr)
    printF(spacer, "Duration: " + str(seconds + picoLatency) + " second" + IsPlural(ignoredDelay) + " wait...")
    
    complete = False
    while exitReason == "":
        if round(config.tm_Dn_Runtime, 2) > config.tm_failSafeSeconds: # 60 second failsafe
            config.sw_Up.value(OFF)
            config.sw_Dn.value(OFF)
            config.rly_Up.value(OFF)
            config.rly_Dn.value(OFF)
            printF(spacer + " wait -> Complete FAILSAFE abort")
            return False
        
        if checkRunTime == True:
            rt = abs(config.tm_Dn_Runtime) - RunSeconds(tm, time.ticks_ms(), 2)
            rt = round(rt, 2)
            if rt > -0.5 and rt < 0.5:
                trigger = config.id_dn_runtime
                exitReason = "config.tm_Dn_Runtime reached 0"
#         print(str(ignoredDelay))
#         print(str(config.tm_Dn_Runtime))
        ut = time.ticks_ms()
        if RunSeconds(tm, ut, 2) >= ignoredDelay: # Don't start checking until after "ignoredDelay" (if it's not zero)
            if not once:
                if ignoredDelay > 0:
                    printF(spacer, "Interrupt Delay enabled")
                else:
                    printF(spacer, "Interrupt Delay disabled")
                once = True
            
            trigger = Check_Button_Press(checkRunTime, tm)
            
            if (ignoredBin & config.ignore_none) and trigger > 0:
                exitReason = "all triggers are enabled. Activated trigger interrupt = " + str(trigger)
            else:
                if not ignoredBin & trigger:
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
                        exitReason = "config.sw_Upper interrupt"
                    if trigger == 1024:
                        exitReason = "config.sw_Lower interrupt"
                    if trigger == 2048:
                        exitReason = "config.sw_Occup interrupt"         
                    if checkRunTime == False and trigger == 4096:
                        exitReason = "config.id_dn_runtime interrupt: tm_Dn_Runtime reached 0"
                        
            if exitReason == "" and trigger == 0 and (RunSeconds(tm, time.ticks_ms(), 2) > seconds):
                trigger = -1
                exitReason = "Time (True)"

        
    printF(spacer + "EXIT: Completed - Reason = " + exitReason)
    printF(spacer + "Complete wait time = ", str(round(config.tm_Dn_Runtime, 2)), " seconds - Returning to caller")
    once = False
    return exitReason #== "Time (True)"

def Space(spc):
    str = ""
    for i in range(0, spc):
        str += " "
    return str

def Up_To_Out(spc = 1):
    spacer = Space(spc) + "topToHome -> "
    config.rly_Up.value(ON)
    printF(spacer + "Up_To_Out() activated")
    printF(spacer + "config.rly_Up ON")
    
    global tm
    tm = time.ticks_ms()
    if config.sw_Home.value() == OFF:
        printF(spacer + "Waiting " + str(config.tm_out_to_home - abs(config.tm_Dn_Runtime)) + " seconds")
        result = Wait_Time(config.tm_out_to_home - abs(config.tm_Dn_Runtime), 1, config.ignore_led_home + config.id_sw_Up + config.id_dn_runtime, config.tm_1_wait, False)
    else:
        printF(spacer + "Waiting " + str(config.tm_out_to_home) + " seconds")
        result = Wait_Time(config.tm_out_to_home + config.tm_Dn_Runtime, spc + 1, config.ignore_led_home, config.tm_1_wait) #ignore sw_Home for 1 second
        
    config.tm_Dn_Runtime -= RunSeconds(tm, time.ticks_ms())
    printF(spacer, "config.rly_Up OFF")
    config.rly_Up.value(OFF)
    if result != "config.sw_Upper interrupt" and result != "Time (True)":
        printF(spacer, "Out_To_Home interrupt")
        printF(spacer + "EXIT: Returning to caller (l:234)")
        return result
    else:
        printF(spacer, str(config.tm_top_wait) + " second wait")
        result = Wait_Time(config.tm_top_wait, spc + 1, config.ignore_allLimits, config.tm_top_wait + 1)
#         printF(spacer, "-- here --")
        if result != "Time (True)":
            printF(spacer, "Out_To_Home TopWait interrupt")
        else:
            printF(spacer, "TopWait complete")
            result = Down_To_Home(spc + 1)

    printF(spacer + "EXIT: Returning to caller")
    return result

def Down_To_Home(spc = 1):
    spacer = Space(spc) + "downToHome -> "
    aborted = False
    global tm
    tm = time.ticks_ms()
    printF(spacer, "goDn_Rcln & GPIO.wait_for_edge(sw_posHome)")
    config.rly_Dn.value(ON)
    printF(spacer, "config.rly_Dn ON")
    
    #ignored = config.ignore_sw_Dn + config.ignore_sw_Dn2 + config.ignore_sw_Main_Dn + config.ignore_sw_Main_Dn2 + config.ignore_led_upper
    result = Wait_Time(config.tm_out_to_home, spc + 1, config.ignore_sw_Dn, config.tm_1_wait) #Dn, config.tm_1_wait)
    config.tm_Dn_Runtime += RunSeconds(tm, time.ticks_ms())
    config.rly_Dn.value(OFF)
    printF(spacer, "config.rly_Dn OFF")
    
    if config.sw_Home.value() == ON:
        config.tm_Dn_Runtime = 0
        printF(spacer, ": complete. At home")
    else:
        if result == "Time (True)":
            printF(spacer, "Dn timeout reached: ", str(config.tm_out_to_home), ' seconds without home interrupt')
        else:
            print(result)
            if result == "configg.tm_Dn_Runtime reached 0":
                printF(spacer, "config.tm_Dn_Runtime reached 0")
                config.tm_Dn_Runtime = 0.0
            else:
                printF(spacer, result, "interrupt detected")
    printF(spacer + " EXIT: Returning to caller")
    return result
                           
def SelfCheck():
    ledTime = float(0.15)
    time.sleep(.75)
    config.led_occup.value(1)
    time.sleep(ledTime)
    config.led_lower.value(1)
    time.sleep(ledTime)
    config.led_upper.value(1)
    time.sleep(ledTime)
    config.led_home.value(1)
    time.sleep(.4585)
    config.led_home.value(0)
    time.sleep(ledTime)
    config.led_upper.value(0)
    time.sleep(ledTime)
    config.led_lower.value(0)
    time.sleep(ledTime)
    config.led_occup.value(0)
    time.sleep(ledTime)
    ErrorFlash() # not really an error

def ErrorFlash(id = 0):
    old_Occ = config.led_occup.value()
    old_Low = config.led_lower.value()
    old_Hi = config.led_upper.value()
    old_Home = config.led_home.value()
    
    config.led_occup.value(0)
    config.led_lower.value(0)
    config.led_upper.value(0)
    config.led_home.value(0)
    
    for x in [1, 2, 3, 4, 5, 6]:
        config.led_occup.toggle()
        config.led_lower.toggle()
        config.led_upper.toggle()
        config.led_home.toggle()
        time.sleep(.1)

    if id > 0:
        for x in [1, 2, 3, 4, 5, 6, 7, 8]:
            if id & config.ignore_led_occup:
                config.led_occup.toggle()
            if id & config.ignore_led_lower:
                config.led_lower.toggle()
            if id & config.ignore_led_upper:
                config.led_upper.toggle()
            if id & config.ignore_led_home:
                config.led_home.toggle()
            time.sleep(.5)
        
    config.led_occup.value(old_Occ)
    config.led_lower.value(old_Low)
    config.led_upper.value(old_Hi)
    config.led_home.value(old_Home)

