from toptica.lasersdk.dlcpro.v2_4_0 import DLCpro, NetworkConnection
from PySimpleGUI import Window, WIN_CLOSED, Text, Button, InputText, VSeparator, Column, Combo
import numpy as np
import PySimpleGUI as sg

sg.theme('DarkBlack1')
sg.set_options(font = ('Courier New', 10))

""" Funciones que crean textos y botones en la interfaz"""

def connectionBoxGUI(saveData, respond):
    # Caja de la conexcion a los láseres y al server
    
    serverTitle = [Text("Connection to server")]
    
    enterIP = [Text('IP:'), InputText(saveData['serverIP'], key='serverIP',s=(12,1))]
    enterPortAndConnect = [Text('Port:'), InputText(saveData['port'], key='port',s=(5,1)), Button(respond['server connection state'][0], key = "__CONNECT_SERVER__", button_color = respond['server connection state'][1])]
    
    server = [serverTitle, enterIP, enterPortAndConnect]
    laser12 = [ [Text("Connection DLC pro 1 & 2")],
               [Text("IP:"), InputText(saveData['__DLC_IP_12__'], key='__DLC_IP_12__',s=(12,1))],
               [Button(respond['DLC 12 connection state'][0], key = "__CONNECT_DLC_12__", button_color=respond['DLC 12 connection state'][1])] ]
    laser34 = [ [Text("Connection DLC pro 3 & 4")],
               [Text("IP:"), InputText(saveData['__DLC_IP_34__'],  key='__DLC_IP_34__', s=(12,1))],
               [Button(respond['DLC 34 connection state'][0], key = "__CONNECT_DLC_34__", button_color = respond['DLC 34 connection state'][1])]         ]
    connectionRow = [Column(laser12), VSeparator(), Column(laser34), VSeparator(), Column(server)]
    
    return connectionRow
        
def laserBoxGUI_12(saveData, laserNumber):
    # Caja de la información de los láseres 1 y 2 (UV)
    laserColumn = [
          [Text(f'Laser {laserNumber}')],
          [Text('SetPoint'), InputText(saveData[f'setPoint {laserNumber}'], key =f'setPoint {laserNumber}', size=(10,1)), 
           Text('THz'), Button('<', key = f"Enter {laserNumber}", bind_return_key = False)],
          [Button(u'\u2191', key = f'up {laserNumber}'), Button(u'\u2193', key = f'down {laserNumber}'),
           Combo( saveData[f'freqStepArr {laserNumber}'], size=(5, 3), enable_events=True, bind_return_key=True, key=f'freqStepArr {laserNumber}', default_value = int(np.round(saveData[f'freqStep {laserNumber}']*10**6))),
           Text('MHz')], 
          [Text("Monitor", key = "monitor {laserNumber}"), 
           Button("OFF",  button_color="red", key = f"monitorButton {laserNumber}", size = (3, 1))],
          [Text("Stabilization", key = "stabilization {laserNumber}"), 
           Button("OFF",  button_color="red", key = f"stabilizationButton {laserNumber}", size = (3, 1))],
          [Text('Frequency: '), Text('', key = f'freq {laserNumber}')],
          [Text('act Current:'), Text('', key = f'curr {laserNumber}')],
          [Text('set Current:'), Text('', key = f'setCurr {laserNumber}')],
          [Text('act Voltage:'), Text('', key = f'volt {laserNumber}')],
          [Text('set Voltage:'), Text('', key = f'setVolt {laserNumber}')],
          
          ]
    return laserColumn
    
def laserBoxGUI_34(saveData, laserNumber):
    # Caja de la información de los láseres 3 y 4 (IR)
    laserColumn = [
          [Text(f'Laser {laserNumber}')],
          [Text('SetPoint'), InputText(saveData[f'setPoint {laserNumber}'], key =f'setPoint {laserNumber}', size=(10,1)), 
           Text('THz'), Button('<', key = f"Enter {laserNumber}", bind_return_key = False)],
          [Button(u'\u2191', key = f'up {laserNumber}'), Button(u'\u2193', key = f'down {laserNumber}'),
           Combo(saveData[f'freqStepArr {laserNumber}'], size=(5, 3), enable_events=True, bind_return_key=True, key=f'freqStepArr {laserNumber}',  default_value = int(np.round(saveData[f'freqStep {laserNumber}']*10**6))),
           Text('MHz')],  
          [Text("Monitor", key = "monitor {laserNumber}"), 
           Button("OFF",  button_color="red", key = f"monitorButton {laserNumber}", size = (3, 1))],
          [Text("Stabilization", key = "stabilization {laserNumber}"), 
           Button("OFF",  button_color="red", key = f"stabilizationButton {laserNumber}", size = (3, 1))],
          [Text('Frequency: '), Text('', key = f'freq {laserNumber}')],
          [Text('act Current:'), Text('', key = f'curr {laserNumber}')],
          [Text('set Current:'), Text('', key = f'setCurr {laserNumber}')],
          ]
    return laserColumn
     
def digitalFilterGUI(saveData, respond):
    # La interfaz completa (una ventana)
    
    laserColumn1 = laserBoxGUI_12(saveData, 1)
    laserColumn2 = laserBoxGUI_12(saveData, 2)
    laserColumn3 = laserBoxGUI_34(saveData, 3)
    laserColumn4 = laserBoxGUI_34(saveData, 4)
    setPointRow = [Column(laserColumn1), VSeparator(), Column(laserColumn2), 
                VSeparator(), Column(laserColumn3), VSeparator(), Column(laserColumn4)]
    
    dlcRow = connectionBoxGUI(saveData, respond)
    saveDataRow = [ Button('save data', key = '__SAVE_DATA__')]
    
    layout = [dlcRow, setPointRow, saveDataRow]
             
    #create the window
    window = Window('DLC Stabilization', layout, finalize=True)
     
    bindButtonsWithLeftClick(window)
    bindButtonsWithMouseWheel(window) 
       
    return window


""" Funciones que usa la interfaz"""

def initialRespond():
    # Crea un diccionario que va a contener el estado de los procesos (conexiones, monitoreo de
    # frecuencia, estabilizaciones)
    
    respond = {}
    
    respond['stop'] = False
    respond['monitorArrayTF'] = np.array([False, False, False, False])
    respond['stabilizationArrayTF'] = np.array([False, False, False, False])
    respond['iu'] = np.zeros(4) # Cuenta las veces que el wavelenghtMeter lee -3 == underexposure
    
    respond['DLC 12 connection state'] = np.array(['Connect', None])
    respond['DLC 34 connection state'] = np.array(['Connect', None])
    respond['server connection state'] = np.array(['Connect', None])
    
    respond['client'] = 'object client once connection is made'
    respond['sock'] = 'object sock once connection is made'
    
    respond['monitorFunction 1'], respond['monitorFunction 2'] = logMonitorDataN_12, logMonitorDataN_12
    respond['monitorFunction 3'], respond['monitorFunction 4'] = logMonitorDataN_34, logMonitorDataN_34
    
    respond['stabilizationFunction 1'], respond['stabilizationFunction 2'] = stabilizationN_voltage, stabilizationN_voltage
    respond['stabilizationFunction 3'], respond['stabilizationFunction 4'] = stabilizationN_current, stabilizationN_current 
    
    return respond
       
def saveDataInFile(saveData):
    # Función que rescribe el archivo saveData.txt con el diccionario saveData
    with open("saveData.txt", "w+") as file:
           file.write(str(saveData))

def DLCproConnection(saveData, respond, dlcNumber):
    # Conección con el DLC. Usa la IP guardada en saveData y guarda el estado de la conección en respond
    __LASER_ID__ = saveData[f'__DLC_IP_{dlcNumber}__']     
    if dlcNumber == "12":
        try:
            dlc12 = DLCpro(NetworkConnection(__LASER_ID__))
            dlc12.open()
            respond['DLC 12 connection state'] = np.array(["Connected", 'green'])
            respond['dlc 12'] = dlc12
            respond['dlc 1'],  respond['dlc 2'] = dlc12, dlc12
            respond['dlc laser 1'], respond['dlc laser 2'] = dlc12.laser1, dlc12.laser2
        except:
            respond['dlc 12'] = "none"
            
            respond['DLC 12 connection state'] = np.array(["Connection failed", 'red'])
        return 
    
    elif dlcNumber == "34":
        try:
            dlc34 = DLCpro(NetworkConnection(__LASER_ID__))
            dlc34.open()
            respond['DLC 34 connection state'] = np.array(["Connected", 'green'])
            respond['dlc 34'] = dlc34
            respond['dlc 3'],  respond['dlc 3'] = dlc34, dlc34
            respond['dlc laser 3'], respond['dlc laser 4'] = dlc34.laser1, dlc34.laser2
                
        except:
            respond['dlc 34'] = "none"
            respond['DLC 34 connection state'] = np.array(["Connection failed", 'red'])                
        return 
    else:
        pass
    
def serverConnection(saveData, respond):
    # Usa el IP y el puerto guardado en saveData para conectarse y guarda el estado de conexión en respond
    print(f'Server Connection on port {saveData["port"]}')
    import sys
    sys.path.insert(0,"..")
    from _CLIENT_SERVER_DLC_CLASS_ import CLIENT
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.settimeout(3)
    client = CLIENT(port = int(saveData['port']))
    try:
        client.connect_to_server(sock, saveData['serverIP'])
        respond['server connection state'] = ['Connected', 'green']
    except:
        respond['server connection state'] = ['Connection failed', 'red']
        print("Client connection failed")
    respond['sock'] = sock
    respond['client'] = client

def enterKeysArr():
    # Listado de botones que se van a enlazar con el enter
    return ["__DLC_IP_12__", "__DLC_IP_34__", "setPoint 1", "setPoint 2", "setPoint 3", "setPoint 4", "serverIP", "port"]

def mouseWheelKeysArr():
    # Listado de botones/textos que se enlazan con la "ruedita del mouse"
    return ["setPoint 1", "setPoint 2", "setPoint 3", "setPoint 4"]

def bindButtonsWithLeftClick(window):
    # Binds all the buttons in the list with the left click.
    enterKeys = enterKeysArr()
    for key in enterKeys:
        window[key].bind("<Button-1>", " LEFT CLICK")

def bindButtonsWithMouseWheel(window):
    # Binds all the buttons in the list with the mousewheel.
    mouseWheelKeys = mouseWheelKeysArr()
    for key in mouseWheelKeys:
        window[key].bind("<Button-4>", " MOUSE WHEEL U")
        window[key].bind("<Button-5>", " MOUSE WHEEL D")
        
def activeEnterWithClick(window, clickButton):
    # Cuando uno hace click sobre un texto se activa el enter en ese cuadro y se desactiva en todo el resto
    enterKeys = enterKeysArr()
    for key in enterKeys:
        window[key].BindReturnKey = False
    window[clickButton].BindReturnKey = True   



def laserNumberIteration(string):
    return [ string + f" {laserNumber}" for laserNumber in range(1,5)]

def laserNumberIterationPLusClick(string):
    return [ string + f" {laserNumber}" + " LEFT CLICK" for laserNumber in range(1,5)]

def laserNumberIterationMouseWheelU(string):
    return [ string + f" {laserNumber}" + " MOUSE WHEEL U" for laserNumber in range(1,5)]

def laserNumberIterationMouseWheelD(string):
    return [ string + f" {laserNumber}" + " MOUSE WHEEL D" for laserNumber in range(1,5)]


def monitorAction(monitorRespond):
    # Cambia el estado del botón de monitoreo
    if monitorRespond == False:
        newRespond, button, color = True, 'ON', 'green'

    elif monitorRespond == True:
        newRespond, button, color = False, 'OFF', 'red'
    
    else:
        print("monitor respond not correct")
        
    return newRespond, button, color

def stabilizationAction(stabilizationRespond):
    # Cambia el estado del botón de estabilización
    if stabilizationRespond == False:
        newRespond, button, color = True, 'ON', 'green'

    elif stabilizationRespond == True:
        newRespond, button, color = False, 'OFF', 'red'
    
    else:
        print("stabilization respond not correct")
        
    return newRespond, button, color

""" readAndWriteWindow  es la función que lee todas las acciones/eventos 
que ocurren en la interfaz y hace algo al respecto según el evento. """
        
def readAndWriteWindow(window, pid, setPoint, respond):
        event, values = window.read(timeout=0)
        
        respond['stop'] = False
         
        if event != "__TIMEOUT__":
            print(event, values)
            
        # Set Point 
        if event in laserNumberIterationPLusClick("setPoint"):
            
            laserNumber = int(event.split(" ")[1])
            activeEnterWithClick(window, f"Enter {laserNumber}")
        
        elif event in laserNumberIteration("Enter"):
            laserNumber = int(event.split(" ")[1])
            saveData[f'setPoint {laserNumber}'] = float(values[f'setPoint {laserNumber}'])
        
        elif event in laserNumberIterationMouseWheelU("setPoint"):
            laserNumber = int(event.split(" ")[1])
            try:
                readSetPoint = float(values[f'setPoint {laserNumber}'])
            except:
                readSetPoint = float(saveData[f'setPoint {laserNumber}'])
                
            saveData[f'setPoint {laserNumber}'] = readSetPoint + saveData[f'freqStep {laserNumber}']
            window[f'setPoint {laserNumber}'].update(saveData[f'setPoint {laserNumber}'])

        elif event in laserNumberIterationMouseWheelD("setPoint"):
            laserNumber = int(event.split(" ")[1])        
            try:
                readSetPoint = float(values[f'setPoint {laserNumber}'])
            except:
                readSetPoint = float(saveData[f'setPoint {laserNumber}'])
                
            saveData[f'setPoint {laserNumber}'] = readSetPoint - saveData[f'freqStep {laserNumber}']  
            window[f'setPoint {laserNumber}'].update(saveData[f'setPoint {laserNumber}'])
            

        elif event in laserNumberIteration("up"):
            laserNumber = int(event.split(" ")[1])        
            laserNumber = int(event.split(" ")[1])        
            try:
                readSetPoint = float(values[f'setPoint {laserNumber}'])
            except:
                readSetPoint = float(saveData[f'setPoint {laserNumber}'])
                
            saveData[f'setPoint {laserNumber}'] = readSetPoint  + saveData[f'freqStep {laserNumber}']
            window[f'setPoint {laserNumber}'].update(saveData[f'setPoint {laserNumber}'])

        
        elif event in laserNumberIteration("down"):
            laserNumber = int(event.split(" ")[1])               
            try:
                readSetPoint = float(values[f'setPoint {laserNumber}'])
            except:
                readSetPoint = float(saveData[f'setPoint {laserNumber}'])
                
            saveData[f'setPoint {laserNumber}'] = readSetPoint - saveData[f'freqStep {laserNumber}']
            window[f'setPoint {laserNumber}'].update(saveData[f'setPoint {laserNumber}'])

        #change frequency step
        elif event in laserNumberIteration("freqStepArr"):
            laserNumber = int(event.split(" ")[1])
            #print(values['freqStepArr {laserNumber}'])
            saveData[f'freqStep {laserNumber}'] = values[f'freqStepArr {laserNumber}']*0.000001
        
        # DLC CONNECTION
        elif event in ['__DLC_IP_12__ LEFT CLICK', '__DLC_IP_34__ LEFT CLICK']:
            dlcNumber = int(event.split('_')[-3])
            activeEnterWithClick(window, f'__CONNECT_DLC_{dlcNumber}__')

        elif event in ["__CONNECT_DLC_12__", "__CONNECT_DLC_34__"]:
            dlcNumber = event.split("_")[-3]
            saveData[f'__DLC_IP_{dlcNumber}__'] = values[f'__DLC_IP_{dlcNumber}__']
            
            DLCproConnection(saveData, respond, dlcNumber)                              
            button, color = respond[f'DLC {dlcNumber} connection state']
            window[f"__CONNECT_DLC_{dlcNumber}__"].update(button, button_color=color)
        
        # SERVER CONNECTION
        elif event in ['serverIP LEFT CLICK', 'port LEFT CLICK' ]:
            activeEnterWithClick(window, '__CONNECT_SERVER__')                 
            
        elif event == '__CONNECT_SERVER__':
            saveData['serverIP'] = values['serverIP'] # new IP
            saveData['port'] = values['port']
            serverConnection(saveData, respond)
            button, color = respond['server connection state']
            window['__CONNECT_SERVER__'].update(button, button_color = color)

        # MONITOR
        elif event in laserNumberIteration("monitorButton"):
            laserNumber = int(event.split(" ")[1])            
            respond["monitorArrayTF"][laserNumber-1], button, color = monitorAction(respond["monitorArrayTF"][laserNumber-1])
            window[f"monitorButton {laserNumber}"].update(button, button_color = color)
            
        # STABILIZATION
        elif event in laserNumberIteration("stabilizationButton"):
            laserNumber = int(event.split(" ")[1])            
            respond["stabilizationArrayTF"][laserNumber-1], button, color = stabilizationAction(respond["stabilizationArrayTF"][laserNumber-1])
            window[f"stabilizationButton {laserNumber}"].update(button, button_color = color)   
            
            if respond["stabilizationArrayTF"][laserNumber-1]:
                pid.make_PID_vectors_1laser(saveData, respond, laserNumber, N=1000)
                respond["monitorArrayTF"][laserNumber-1], button, color = True, "ON", "green"              
                window[f"monitorButton {laserNumber}"].update(button, button_color = color)
                saveData[f"setPoint {laserNumber}"] = values[f"setPoint {laserNumber}"]

       # SAVE DATA
        elif event == '__SAVE_DATA__':
            saveDataInFile(saveData)
           
        elif event == WIN_CLOSED:
            respond['client'].send_order(respond['sock'], 'close connection')
            respond['stop'] = True
            
        elif event == WIN_CLOSED:
            respond['stop'] = True  
            try:
                respond['client'].send_order(respond['sock'],  'close connection')
            except:
                pass
                            
        return 
    
""""Funciones que estabilizan un laser con la corriente o voltaje"""

def stabilizationN_current(pid, saveData, respond, laserNumber, time0):
    # Hace la estabilización en corriente para un laser (el "laserNumber")
    
         # New Measurments         
         iu = respond['iu'][laserNumber -1]
         setCurrent = saveData[f'setCurr {laserNumber}']
         newFrequency = saveData[f'newF {laserNumber}']
         newAverageFrequency = pid.averageFrequency(saveData, laserNumber) 
         newTime =  time.time()-time0
         
         
         setNewCurrent, newError = pid.digitalFilterCurrent(saveData, laserNumber, newAverageFrequency)
         
     
        # Handle current error and underexpose     
         if setNewCurrent >= saveData[f'hCurrent {laserNumber}'] or setNewCurrent <= saveData[f'lCurrent {laserNumber}']: # mA
             print(f"Current too high or too low ({setNewCurrent} mA)")
         
             if newFrequency == -3:
                 print(f"Error: Low Exposure. time {np.round(newTime)} s") 
                 setNewCurrent =  setCurrent
                 newFrequency, newError = np.nan, np.nan # creo que prescindibles   
                 respond['iu'][laserNumber-1] = iu + 1
                 if respond['iu'][laserNumber-1] > 5:
                     respond['stabilizationArrayTF'][laserNumber - 1] = False
                     saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], setNewCurrent, newFrequency, newAverageFrequency,  newError]
                     respond['iu'][laserNumber-1] = 0
                     
                     return         
             else:
                 respond['stabilizationArrayTF'][laserNumber - 1] = False
                 saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], setNewCurrent, newFrequency, newAverageFrequency,  newError]
                 return  
         
    
         # Set new current           
         respond[f'dlc laser {laserNumber}'].dl.cc.current_set.set(setNewCurrent)
         respond['stabilizationArrayTF'][laserNumber - 1] = True
         saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], setNewCurrent, newFrequency, newAverageFrequency,  newError] 
         
         print('newError: ', newError, '. newSetCurrent: ', setNewCurrent) 
         return  

def stabilizationN_voltage(pid, saveData, respond, laserNumber, time0):
    # Hace la estabilización en voltaje para un láser (el "laserNumber")
    
         # New Measurments         
         iu = respond['iu'][laserNumber -1]
         setVoltage = saveData[f'setVolt {laserNumber}']
         newFrequency = saveData[f'newF {laserNumber}']
         newAverageFrequency = pid.averageFrequency(saveData, laserNumber) 
         newTime =  time.time()-time0
         
         
         setNewVoltage, newError = pid.digitalFilterVoltage(saveData, laserNumber, newAverageFrequency)
         
     
        # Handle Voltage error and underexpose     
         if setNewVoltage >= saveData[f'hVoltage {laserNumber}'] or setNewVoltage <= saveData[f'lVoltage {laserNumber}']: # mA
             print(f"Voltage too high or too low ({setNewVoltage} V)")
         
             if newFrequency == -3:
                 print(f"Error: Low Exposure. time {np.round(newTime)} s") 
                 setNewVoltage =  setVoltage
                 newFrequency, newError = np.nan, np.nan # creo que prescindibles   
                 respond['iu'][laserNumber-1] = iu + 1                 
                 if respond['iu'][laserNumber-1] > 5:
                     respond['stabilizationArrayTF'][laserNumber - 1] = False
                     saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], saveData[f'setCurr {laserNumber}'], saveData[f'newV {laserNumber}'], setNewVoltage, newFrequency, newAverageFrequency,  newError]
                     respond['iu'][laserNumber-1] = 0
                     return 
                     
             else:
                 respond['stabilizationArrayTF'][laserNumber - 1] = False
                 saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], saveData[f'setCurr {laserNumber}'], saveData[f'newV {laserNumber}'], setNewVoltage, newFrequency, newAverageFrequency,  newError]
                 return  
         
    
         # Set new voltage           
         respond[f'dlc laser {laserNumber}'].dl.pc.voltage_set.set(setNewVoltage)
         respond['stabilizationArrayTF'][laserNumber - 1] = True
         saveData[f'newData {laserNumber}'] = [newTime, saveData[f'newC {laserNumber}'], saveData[f'setCurr {laserNumber}'], saveData[f'newV {laserNumber}'], setNewVoltage, newFrequency, newAverageFrequency,  newError]
         
         print('newError: ', newError, '. newSetVoltage: ', setNewVoltage) 
         return 
     
def stabilizationAll(pid, saveData, respond, time0):
    # Se fija qué botones de estabilización se encuentran encendidos y aplica la función estabilización
    # en los láseres donde el botón está encendido

    stabilizationArrayT = np.where(respond["stabilizationArrayTF"] == True)[0]
    
    for N in stabilizationArrayT:  
        laserNumber = N + 1
        respond[f'stabilizationFunction {laserNumber}'](pid, saveData, respond, laserNumber, time0)
        
        pid.refresh_one_1laser(saveData, laserNumber)
            
        if not respond["stabilizationArrayTF"][N]:
            window[f"stabilizationButton {laserNumber}"].update("OFF", button_color = "red")

def logMonitorDataN_12(window, saveData, laserNumber):
    # Loggea los datos de corriente (actual y set), voltajes (actual y set) y frecuencia de los láseres 1 y 2
    try:
        actCurrent = respond[f'dlc laser {laserNumber}'].dl.cc.current_act.get()
    except:
        actCurrent = np.nan
    
    try:
        setCurrent = respond[f'dlc laser {laserNumber}'].dl.cc.current_set.get()
    except:
        setCurrent = np.nan

    try:
        voltage = respond[f'dlc laser {laserNumber}'].dl.pc.voltage_act.get()
    except:
        voltage = np.nan

    try:
        setVoltage = respond[f'dlc laser {laserNumber}'].dl.pc.voltage_set.get()
    except:
        setVoltage = np.nan       
        
    try:
        frequency = respond['client'].get_f(respond['sock'], saveData[f'CH {laserNumber}'])
    except:
        frequency = np.nan


        
    window[ f'freq {laserNumber}'].update(frequency)
    saveData[f'newF {laserNumber}'] = frequency
    
    window[ f'curr {laserNumber}'].update(actCurrent)
    saveData[ f'newC {laserNumber}'] = actCurrent
    
    window[f'setCurr {laserNumber}'].update(setCurrent)
    saveData[f'setCurr {laserNumber}'] = setCurrent
    
    window[f'volt {laserNumber}'].update(voltage)
    saveData[f'newV {laserNumber}'] = voltage
    
    window[f'setVolt {laserNumber}'].update(setVoltage)
    saveData[f'setVolt {laserNumber}'] = setVoltage    

    return

def logMonitorDataN_34(window, saveData, laserNumber):
    # Loggea los datos de corriente (actual y set) y frecuencia de los láseres 3 y 4
    try:
        actCurrent = respond[f'dlc laser {laserNumber}'].dl.cc.current_act.get()
    except:
        actCurrent = np.nan
    
    try:
        setCurrent = respond[f'dlc laser {laserNumber}'].dl.cc.current_set.get()
    except:
        setCurrent = np.nan
    try:
        frequency = respond['client'].get_f(respond['sock'], saveData[f'CH {laserNumber}'])
    except:
        frequency = np.nan
        
    window[ f'freq {laserNumber}'].update(frequency)
    saveData[f'newF {laserNumber}'] = frequency
    
    window[ f'curr {laserNumber}'].update(actCurrent)
    saveData[ f'newC {laserNumber}'] = actCurrent
    
    window[f'setCurr {laserNumber}'].update(setCurrent)
    saveData[f'setCurr {laserNumber}'] = setCurrent

    return
    

def logMonitorData(window,saveData, respond): # para que el respond?
    monitorArrayT = np.where(respond["monitorArrayTF"] == True)[0]
    for N in monitorArrayT:
        laserNumber = N+1
        respond[f'monitorFunction {laserNumber}'](window, saveData, laserNumber)

""" .............................................................................................. """
""" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ALGORITMO QUE CORRE LA INTERFAZ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> """
""" .............................................................................................. """

import time
from _PID_CLASS_ import PID

pid = PID()

with open('saveData.txt') as file:
    nan = np.nan
    saveData = eval(file.read())

respond = initialRespond()

window = digitalFilterGUI(saveData, respond)

t0 = time.time()
while not respond['stop']:
    # log frequency and begin digital filter
    t = time.time()-t0
    if t >= 0.2:
        t0 = time.time()
        
        #stabilization fuction
        logMonitorData(window, saveData, respond)
        stabilizationAll(pid, saveData, respond, t0)           
        
    readAndWriteWindow(window, pid, saveData, respond)
