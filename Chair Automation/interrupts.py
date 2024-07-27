from config import *

# up relay interrupt
def irq_rly_Up(p):
    if not p.value():
        led_UP.duty_u16(brightness_NormIntensityLed)    
    else:
        led_UP.duty_u16(0)
    
# down relay interrupt
def irq_rly_Dn(p):
    if not p.value():
        led_DN.duty_u16(brightness_HighIntensityLed)
    else:
        led_DN.duty_u16(0)
        
# home limit interrupt
def irq_sw_RiseHome(p):
    if not p.value():
        led_riseHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_riseHome.duty_u16(0)
      
# recl limit interrupt
def irq_sw_Recl(p):
    if not p.value():
        led_reclHome.duty_u16(brightness_NormIntensityLed)
    else:
        led_reclHome.duty_u16(0)
 
# # Define object interrupt paths
# sw_RiseHome.irq(lambda p:irq_sw_RiseHome(p)) 	# interrupt for led_riseHome
# sw_ReclHome.irq(lambda p:irq_sw_Recl(p))   # interrupt for led_lower
# rly_Up.irq(lambda p:irq_rly_Up(p))		# interrupt for rly_Up
# rly_Dn.irq(lambda p:irq_rly_Dn(p))	 	# interrupt for rly_Dn
