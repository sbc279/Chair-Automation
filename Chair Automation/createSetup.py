import machine
import sys
import micropython
import json


def Create():
    # Open the JSON file
    with open('chairCfg.json', 'r') as file:
        # Read the contents of the file
        data = file.read()

        fl = open('./HTML/setupHtml.scr', 'rt')
        htmlMain = fl.read()
        fl.close()
        
        # Parse the JSON data
        jsonData = json.loads(data)
        
        line = htmlMain #str(lines)
       
        
        line = line.replace("^idRiseHome^", (str(jsonData["switchRiseHome"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idRclnHome^", (str(jsonData["switchReclHome"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idSwitchUpper^", (str(jsonData["switchUpper"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idSwitchLower^", (str(jsonData["switchLower"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idUseFileLog^", (str(jsonData["enableFileLog"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idEnableWiFi^", (str(jsonData["enableWiFi"]).replace("True", "checked").replace("False", "")))
        line = line.replace("^idFilename^", str(jsonData["logFilename"]))
        line = line.replace("^idHomeToOut^", str(jsonData["outToHhome"]))
        line = line.replace("^idDebounce^", str(jsonData["switchbounce"]))
        line = line.replace("^idTopWait^", str(jsonData["topWait"]))
        line = line.replace("^idLedFrequency^", str(jsonData["ledFrequency"]))
        line = line.replace("^idOutToHome^", str(jsonData["outToHhome"]))
        line = line.replace("^idLedNormal^", str(jsonData["ledNormal"]))
        line = line.replace("^idRclnStep^", str(jsonData["downStep"]))
        line = line.replace("^idLedMedium^", str(jsonData["ledMedium"]))
        line = line.replace("^idFailsafe^", str(jsonData["failSafeSeconds"]))
        line = line.replace("^idLedHigh^", str(jsonData["ledHigh"]))
        #line = line.replace("^ip^", str('192.168.7.218'))
        
        return line
    
