import machine
import micropython
import network
import socket
import time
from config import *
import config
from secret import *
from functions import *
from createSetup import *
import json
#from MicroWebSrv2 import *
import ujson

pHeader = "webServer: "

# ---------------------------- wifi --------------------------
#s = socket.socket()
#cl = socket.AF_INET[0]  #.array #AF_INIT#addr = network.WLAN(network.STA_IF)

printF(pHeader, 'reading mainHtml.txt')   
f = open('mainHtml.txt')
htmlMain = f.read()
f.close()
html = htmlMain
txt = ''
printF(pHeader, 'creating setup html page')
htmlSetup = Create()

    # ---------------------------- wifi --------------------------			
def clientSend(cl):
    printF(pHeader, 'processing post-back data')
    global s
    stateis = "Idle"
    chk = False
    if enableWiFi:
        config.WEBREQUEST = str(config.WEBREQUEST)
        stop = config.WEBREQUEST.find('/0')
        upOut = config.WEBREQUEST.find('/1')
        lDown = config.WEBREQUEST.find('/2')
        down = config.WEBREQUEST.find('/3')
        up = config.WEBREQUEST.find('/up')
        setup = config.WEBREQUEST.find('/setup')
        back = config.WEBREQUEST.find('/back')
        showFile = config.WEBREQUEST.find('/showfile')
        
        if stop == 6:
            printF(pHeader, 'proccessing :stop')
            if rly_Dn.value() == ON:
                rly_Dn.value(OFF)
            if rly_Up.value() == ON: 
                rly_Up.value(OFF)
            abort = True # force a functions.Wait interrupt
            #SendResponse(cl)
            return                
        if upOut == 6:
#             # up 'n out
            printF(pHeader, 'proccessing :uOut')
            tm = time.ticks_ms()
            rly_Up.value(config.is_ON)
            result = Up_To_Out(tm_Dn_Runtime) 
            resultStr = result.split(',')[0]
            resultVal = result.split(',')[1]
            #tm_Dn_Runtime -= float(resultVal)
            printF(pHeader, resultStr.replace("  wait -> ", ""))
            return
        if up == 6:
            printF(pHeader, 'proccessing :up')
            #stateis = "Main UP"
            if rly_Dn.value() == ON:
                rly_Dn.value(OFF)
            rly_Up.value(ON)
            #SendResponse(cl)
            return                
        if down == 6:
            printF(pHeader, 'proccessing :down')
            #stateis = "Main DOWN"
            if rly_Up.value() == ON: 
                rly_Up.value(OFF)
            rly_Dn.value(ON)
            #SendResponse(cl)
            return                
        if lDown == 6:
            printF(pHeader, 'proccessing :lDown')
            stateis = "Logic DOWN"
            SendResponse(cl)
            return
        if setup == 6:
            printF(pHeader, 'proccessing :setup')
            stateis = ""
            #SetVars()
            htmlSetup = Create()            
            SendResponse(cl, htmlSetup) # Setup page
            return
        if back == 6:
            printF(pHeader, 'proccessing :back')
            stateis = ""
            SendResponse(cl, htmlMain)
            return
        if showFile == 6:
            printF(pHeader, 'proccessing :showFile')
            stateis = "showFile"
            return

                    
        SendResponse(cl, htmlMain) # Main page
        return

                
def SendResponse(cl, txt = ""):
    printF(pHeader, 'sending response')
    cl.sendall('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + txt)
    cl.close()
    

def DisconnectWebServer():
    if enableWiFi:
        printF(pHeader, 'disconnecting socket')
        #cl, addr = s.accept()
        socket.socket().close()
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        #socket.socket().close()
        printF(pHeader, 'WiFi connection closed')   
        
def WebServerCommon():
    global s
    if enableWiFi:
        printF(pHeader, 'establishing ip connectivity')
        wlan = network.WLAN(network.STA_IF)
        printF(pHeader, wlan)
        wlan.active(True)
        wlan.connect(secrets['ssid'], secrets['password'])
        
        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            printF(pHeader, 'waiting for connection...')
            time.sleep(1)
        
        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            printF(pHeader, 'connected')
            status = wlan.ifconfig()
            printF(pHeader, 'ip = ', status[0] )
            config.WEBCTL = True
            
         
        # Open socket
        s = socket.socket()
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind(addr)
        s.listen(1)
        printF(pHeader, 'Socket created: ', s.gethostbyname(),", ", s.IPPROTO_IP)
        s.setsockopt(s.SOL_SOCKET, 20, handler)
                   
        printF(pHeader, 'listening on', addr)

        stateis = ""
                       
        
def handler(svr):
    cs, ca = svr.accept()
    #cl, addr = s.accept()
    
  
    config.WEBREQUEST = cs.recv(1024) #(1024)
    method, url, *_ = config.WEBREQUEST.decode().split('\r\n')[0].split()
    printF(pHeader, "WEBREQUEST received: ", url)
#     
    
    if method == 'POST':
        config.WEBPOST = 0
        printF(pHeader, "POST postback received ")
        if url == '/restart':
            if str(config.WEBREQUEST).find("restarter") > 0:
                printF(pHeader, "restart config.WEBREQUESTed")
                machine.reset()
            
        if url == '/data':
            printF(pHeader, "json data payload detected")
            # Read JSON data from the config.WEBREQUEST
            json_data = "{" + str(config.WEBREQUEST).split("{")[1]
            json_data = json_data.replace("\"", '"')
            json_data = json_data.replace(",",",\r\n")
            json_data = json_data.replace("'","")
            
            # Save the JSON data to a file
            save_json(json_data)
            printF(pHeader, "Received JSON data") 
            
            SendResponse(cs,"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
           
        else:
            stateis=""
            
            clientSend(cs)
    else:
        stateis=""
        clientSend(cs)
        return
                                                  
# Function to save JSON data to a file
def save_json(json_data):
            # Save the JSON data to a file
            printF(pHeader, "save_data: Saving json data to ", jsonFilename)
            with open(jsonFilename, 'w') as f:
                f.write(json_data)
                printF(pHeader, 'save_data: issuing flush()')
                f.flush()
                f.close()
                
            time.sleep(.1)
            
def Timer(WEBPOST, payload): # Every 5 seconds
    if not payload == "":
        config.WEBPOST = config.WEBPOST + 1

    else:
        if config.WEBPOST >= 6:
            DisconnectWebServer()
            config.WEBCTL = False        
            config.WEBPOST = 0
            return WEBPOST

tim = Timer(3)                                   # create a timer object using timer 3
tim.init(mode=Timer.PERIODIC)                    # initialize it in periodic mode
tim_ch = tim.channel(Timer.A, freq=5)            # configure channel A at a frequency of 5Hz

# Call Timer(WEBPOST, payload) every cycle of the timer
tim_ch.irq(handler=lambda t:Timer(config.WEBPOST, config.WEBconfig.WEBREQUEST), trigger=Timer.TIMEOUT)        