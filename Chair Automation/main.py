# Main.py
version = 2.1

import sys

import micropython
import time
import _thread
import config
from config import *
from webserver import *
from logic import *
from interrupts import *

micropython.alloc_emergency_exception_buf(100)																																																					

once = False 
stat = 0

print("main.py IPL: (chair) startup  BETA version " + version + "\n")
tm_Dn_Runtime = 0

# # Define object interrupt paths
sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) 	# interrupt for led_riseHome
sw_ReclHome.irq(lambda p:irq_sw_Recl(p))   # interrupt for led_lower
rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn

# Initialize     
rly_Up(OFF)
rly_Dn(OFF)
Is_Home()

printF('Ready...')

def mainProc():
    while True:
        while btn_Main_Up.value or btn_Main_Up2.value or btn_Logic_Up2.value:
            if stat == 0:
                stat = 1
                rly_Up(ON)
            
        while btn_Main_Dn.value or btn_Main_Up2.value or btn_Logic_Dn2.value:
            if stat == 0:
                stat = 2           
                rly_Dn(ON)
            
  # ------------------------------------

        while btn_Logic_Up.value:
            if stat == 0:
                stat = 3
                rly_Up(ON)
                
        while btn_Logic_Dn.value:
            if stat == 0:
                stat = 4
                rly_Up(ON)
        
        # turn the relays off
        if stat > 0:
            if stat & 1:
                rly_Up(OFF)
            if stat & 2:
                rly_Dn(OFF)
            stat = 0    

        
# Startup.....................
try:
    # Transfer control to mainProc...
    mainProc()
    #uasyncio.run(main())
                
# Exit/error...
except KeyboardInterrupt:
    # Make sure relays are off
    rly_Up.value(OFF)
    rly_Dn.value(OFF)
    DisconnectWebServer()
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

finally:
    led_UP.deinit()
    led_reclHome.deinit()
    led_riseHome.deinit()
    led_DN.deinit()


       

