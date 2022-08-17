""" Comunicación WavelengthMeter """
import time
from ctypes import cdll
import ctypes

wlmData= cdll.LoadLibrary("wlmData.dll")

GetWavelengthNum = wlmData.GetWavelengthNum
GetWavelengthNum.restype = ctypes.c_double

GetFrequencyNum= wlmData.GetFrequencyNum
GetFrequencyNum.restype = ctypes.c_double


X = ctypes.c_double(0.0)

time.sleep(0.2)
print(" initial frequency: {} nm".format(GetFrequencyNum(X)))


""" Comunicación con CLIENT"""

import sys
sys.path.insert(0,"..")
from _CLIENT_SERVER_DLC_CLASS_ import SERVER
import socket

server = SERVER(port = 40128)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.server_port(sock)
connection, client_address = server.connection_to_client(sock)
server.get_order(sock, connection, GetFrequencyNum, GetWavelengthNum)









