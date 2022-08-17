import numpy as np

def nanList(N):
    a = np.empty(N)
    a[:] = np.nan
    return a.tolist()

def moove(vector, newData):
    newVector = np.zeros_like(vector)
    newVector[:-1] = vector[1:]
    newVector[-1] = newData
    return newVector.tolist()
                 
class PID:
    def __init__(self):
        print("")

    def make_PID_vectors_1laser(self, saveData, respond, laserNumber, N):
            #saveData['PID vectors labels {laserNumber}'] = ['measureTimes', 'currents', 'setCurrents', 'voltages', 'setVoltages','frequency', 'averageFrequency','errorSignal']
            if laserNumber in [1, 2]:
                #saveData['PID vectors labels {laserNumber}'] = ['measureTimes', 'currents', 'setCurrents', 'voltages', 'setVoltages','frequency', 'averageFrequency','errorSignal']
                saveData[f'PID vectors {laserNumber}'] = [nanList(N),nanList(N),nanList(N),nanList(N), nanList(N), nanList(N), nanList(N), nanList(N)]
                
                # frequency
                try: 
                    sock = respond['sock']
                    client = respond['client']
                    saveData[f'PID vectors {laserNumber}'][5][-1] = client.get_f(sock, saveData[f'CH {laserNumber}']) # frequencies
                except:
                    saveData[f'PID vectors {laserNumber}'][5][-1] = np.nan
                            
                # setVoltages
                saveData[f'PID vectors {laserNumber}'][3][-1] = respond[f'dlc laser {laserNumber}'].dl.pc.voltage_set.get()
                
            if laserNumber in [3, 4]:
                #saveData['PID vectors labels {laserNumber}'] = ['measureTimes', 'currents', 'setCurrents','frequency', 'averageFrequency','errorSignal']
                saveData[f'PID vectors {laserNumber}'] = [nanList(N),nanList(N),nanList(N), nanList(N), nanList(N), nanList(N)]              
                
                # frequency
                try: 
                    sock = respond['sock']
                    client = respond['client']
                    saveData[f'PID vectors {laserNumber}'][3][-1] = client.get_f(sock, saveData[f'CH {laserNumber}']) # frequencies
                except:
                    saveData[f'PID vectors {laserNumber}'][3][-1] = np.nan

            # measureTimes
            saveData[f'PID vectors {laserNumber}'][0][-1] = 0             
            # Error signal
            # saveData[f'PID vectors {laserNumber}'][-1][-1] =  saveData[f'setPoint {laserNumber}'] - saveData[f'PID vectors {laserNumber}'][3][-1] # error signal
            saveData[f'PID vectors {laserNumber}'][-1][-1] = 0
            
            # setCurrent
            saveData[f'PID vectors {laserNumber}'][2][-1] = respond[f'dlc laser {laserNumber}'].dl.cc.current_set.get()
     
    def digitalFilterCurrent(self, saveData, laserNumber, newF):
        # Devuelve la nueva corriente según términos prop e integral
        newError = float(saveData[f'setPoint {laserNumber}']) - newF
        newSetCurrent = saveData[f'setCurr {laserNumber}'] - saveData[f'Kp {laserNumber}']*newError  
        
        return   newSetCurrent, newError

    def digitalFilterVoltage(self, saveData, laserNumber, newF):
        # Devuelve la nueva corriente según términos prop e integral
        newError = float(saveData[f'setPoint {laserNumber}']) - newF
        newSetVoltage = saveData[f'setVolt {laserNumber}'] + saveData[f'Kp {laserNumber}']*newError  
        
        return   newSetVoltage, newError

    def refresh_one_1laser(self, saveData, laserNumber):
        # Agarra la data nueva del diccionario y la agrega a los PID vectors
        newData = saveData[f'newData {laserNumber}']
        
        for index, vector in enumerate(saveData[f'PID vectors {laserNumber}']):
           vector = moove(vector, newData[index]) 
           saveData[f'PID vectors {laserNumber}'][index] = vector
    
    def averageFrequency(self, saveData, laserNumber):
        n = saveData[f'NAVER {laserNumber}']
        frequencies = saveData[f'PID vectors {laserNumber}'][5]
        frequencyCutMoove = moove(frequencies[-n:], saveData[f'newF {laserNumber}'])
        return np.nanmean(frequencyCutMoove)
    
 