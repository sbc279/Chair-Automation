# Main.py
# version = 5.22.24

import micropython
#from webserver import *
from functions import *
from config import *
import config
# import uasyncio #import core

micropython.alloc_emergency_exception_buf(100)																																																					
onceUp = False 
onceDn = False
printF("main.py IPL: (chair) startup  BETA version ", version)
print("")
printF("main.py IPL: Waiting for configuration to signal ready...")

# ------ Wait on config to get completely loaded -------
#
try: # Step 1: Wait for it to be defined
    time.sleep(.1)
    configLoading == False
except NameError:
    onceUp = False # bullshit code. We're good to go now
    
while configLoading: # Step 2: The REAL waiter
    time.sleep(.1)
# ---------------------------------------------------------

rly_Up(1) # force an off
rly_Dn(1) # force an off
tm_Dn_Runtime = 0
is_OFF = OFF
is_ON = ON
start = float(0.0)
    
printF("main.py IPL: Configuration loaded, received ready signal")
print("")

# --------------- Button Array Interrupts -------------------|
def MainUp():												#|
    irqCheck(btn_Main_Up, rly_Up, led_RED, "Main_Up2")		#|
def MainDn():												#|
    irqCheck(btn_Main_Dn, rly_Dn, led_BLU, "Main_Down")		#|
def MainUp2():												#|
    irqCheck(btn_Main_Up2, rly_Up, led_RED, "Main_Up")		#|
def MainDn2():												#|
    irqCheck(btn_Main_Dn2, rly_Dn, led_BLU, "Main_Down2")	#|
                                                            #|
def LogicUp():                                              #|
    irqCheck(btn_Logic_Up, rly_Up, led_RED, "Logic_Up", 1)	#|
def LogicDn():												#|
    irqCheck(btn_Logic_Dn, rly_Dn, led_BLU, "Logic_Down", 2)#|
def LogicUp2():												#|
    irqCheck(btn_Logic_Up2, rly_Up, led_RED, "Logic_Up2")	#|
def LogicDn2():												#|
    irqCheck(btn_Logic_Dn2, rly_Dn, led_BLU, "Logic_Down2")	#|
# -----------------------------------------------------------|

# ---------------- Core Switch Comon Module -----------------
def irqCheck(ctrl, relay, led, ctlText, idx = 0):
#     if WEBCTL:
#         printF("main -> ","Switch control disabled. Active web in use")
#         return
    
    global tm_Dn_Runtime
    onceUp = False
    while ctrl.value():
        if not onceUp:
            printF("-------------------- ", ctlText, " --------------------")
            tm = time.ticks_us()
            if idx == 1: # ------------------------------- Logic Up
                LogicUpCtl(ctlText, relay)
                onceUp = True
            else:
                if idx == 2: # --------------------------- Logic Down
                    LogicDnCtl(ctlText, relay)
                    onceUp = True
                else:
                    relay.value(ON)
                    printF("main -> ", ctlText, " pressed")
                    onceUp = True
            SwitchDebounce() # kill any pending button presses

    if onceUp:
        relay.value(OFF)
        secs = float(time.ticks_diff(time.ticks_us(), tm) / 1000000)
        printF("main -> ", ctlText, " released (", str(float("%.2f" % (secs))), " seconds, Total = ", round(tm_Dn_Runtime, 2), ")")
        onceUp = False
        
# ------------------------------------------------------------------------------------------

def LogicUpCtl(ctlText, relay):
    # Should we go up and out?
    if sw_RiseHome.value() == ON or tm_Dn_Runtime < 0:
        result = Up_To_Out(abs(tm_Dn_Runtime))
        printF("main -> ", ctlText, " completed. (", round(tm_Dn_Runtime, 2), ")")
        print('--------------------------------------------------------------------------------')
        printF('--> Up_To_Out Results:', result)
        print('--------------------------------------------------------------------------------')
        return
    else:
        # No, so go up for as long as we went down
        printF('--> Up to home position...')
        relay.value(ON)
        Wait_Time(tm_Dn_Runtime, 1, id_sw_All-id_btn_Logic_Up)
        printF('--> At RclnHome')
        relay.value(OFF)
    SwitchDebounce() # kill any pending button presses

# ------------------------------------------------------------------------------------------

def LogicDnCtl(ctlText, relay):
    printF("main -> ", ctlText, " pressed")
    duration = 0
    # Should we go down to home?
    if sw_ReclHome.value() == ON:
        if sw_RiseHome.value() == OFF:
            duration = abs(tm_Dn_Runtime)
        else:
            duration = tm_out_to_home - tm_Dn_Runtime                        
        Down_To_Home(1, duration)
        SwitchDebounce() # kill any pending button presses
    else:
        # No, so take a step down
        relay.value(ON)
        Wait_Time(tm_down_step, 1, id_sw_All - id_btn_Logic_Dn)
    SwitchDebounce() # kill any pending button presses

# ------------------------------------------------------------------------------------------

# up relay interrupt
def irq_rly_Up(p):
    global tm_Dn_Runtime
    global start
    if not p.value():
        start = float(time.ticks_ms())
        led_BLU.duty_u16(brightness_NormIntensityLed)    
    else:
        tm_Dn_Runtime += round((start/1000 - time.ticks_ms()/1000), 2)
        led_BLU.duty_u16(0)
    
# down relay interrupt
def irq_rly_Dn(p):
    global tm_Dn_Runtime
    global start
    if not p.value():
        start = float(time.ticks_ms())
        led_RED.duty_u16(brightness_HighIntensityLed)
    else:
        tm_Dn_Runtime -= round((start/1000 - time.ticks_ms()/1000), 2)
        led_RED.duty_u16(0)
        
# home limit interrupt
def irq_sw_RiseHome(p):
    if not p.value():
        led_YEL.duty_u16(brightness_NormIntensityLed)
    else:
        led_YEL.duty_u16(0)
      
# recl limit interrupt
def irq_sw_Recl(p):
    if not p.value():
        led_WHT.duty_u16(brightness_NormIntensityLed)
    else:
        led_WHT.duty_u16(0)
 
# Define object interrupt paths
sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) # interrupt for led_YEL
sw_ReclHome.irq(lambda p:irq_sw_Recl(p))     # interrupt for led_WHT
rly_Up.irq(lambda p:irq_rly_Up(p))		     # interrupt for rly_Up
rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	     # interrupt for rly_Dn
        
def SwitchDebounce():
    while Check_Button_Press() & id_sw_All:
        time.sleep(.1)

# ntptime.settime() # set pico's clock
UTC_OFFSET = -5 * 60 * 60   # change the '-5' according to your time zone
actual_time = time.localtime(time.ticks_ms() + UTC_OFFSET)

def Is_Home(mute = False):
    if sw_RiseHome.value() == is_OFF or sw_ReclHome.value() == is_OFF:
        if not mute:
            if (use_sw_RiseHome and sw_RiseHome.value() == is_OFF) and (use_sw_ReclHome and sw_ReclHome.value() == is_OFF):
                print()
                printF("main -> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  WARNING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
                printF("main -> ", "IsHome() FORBIDDEN STATE: Both sw_RiseHome & sw_RclnHome are open.")
                printF("main -> ", "IsHome()"," Please check your riseHome and reclHome switches and connections.")
                printF("main -> <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  WARNING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>") 
                print()
                return False
            if use_sw_ReclHome and sw_ReclHome.value() == is_ON:
                printF("main -> ", "sw_RiseHome NOT at Home position.")
        return False
    else:
        if not mute:
            printF("main -> ", "At Home position.")
        return True

SelfCheck()
ShowOptions()
Is_Home()

# Establish wifi...
#WebServerCommon()

printF('Ready...')

def mainRunner():
    while True:
        1==1
        MainUp()
        MainDn()
        MainUp2()
        MainDn2()
        
        LogicUp()
        LogicDn()
        LogicUp2()
        LogicDn2()
        
try:
    mainRunner()
    #uasyncio.run(main())
                
# Exit/error...
except KeyboardInterrupt:
    # Make sure relays are off
    rly_Up.value(is_OFF)
    rly_Dn.value(is_OFF)
    #DisconnectWebServer()
    printF("------------- main.py Exiting   (c)2023 CRAVER Engineering -------------")

# except Exception as Argument:  
#     # this catches ALL other exceptions including errors.  
#     # You won't get any error messages for debugging  
#     # so only use it once your code is working
#     rly_Up.value(is_OFF)
#     rly_Dn.value(is_OFF)
#     f = open("Errors.txt", "a")
#     f.write("ERROR: " + str(Argument) + " \nSTerminating main.py \n")
#     f.close()

#finally:
    led_RED.deinit()
    led_WHT.deinit()
    led_YEL.deinit()
    led_BLU.deinit()


       

 
