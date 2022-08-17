import socket
import ctypes
import numpy as np

def ChannelIteration(string):
    return [string + f' CH {CH}' for CH in range(1,5)]


class SERVER:
    def __init__(self, port):
        self.port = port
        self.ip_address = self.get_ip_address()
        self.server_address = (self.ip_address, self.port)
        
        
    def get_ip_address(self):
        local_hostname = socket.gethostname()
        ip_address = socket.gethostbyname(local_hostname)
        print("IP addres: ", ip_address)
        return ip_address
    
    def server_port(self,sock):
        server_address = self.server_address
        print ('starting up on %s port %s' % server_address)
        sock.bind(server_address)

    #only run after prot comunication
    def connection_to_client(self, sock):
        # listen for incoming connections (server mode) with one connection at a time
        sock.listen(1)
        # wait for a connection
        print ('waiting for a connection')
        connection, client_address = sock.accept()
    
        print ('connection from', client_address)
        
        return connection, client_address
    

    
    def get_order(self, sock, connection, GetFrequencyNum, GetWavelengthNum):
        
        while True: 
            print('waiting for an order')
            order = connection.recv(64)
        
            if order:
                if order.decode() in ChannelIteration('f'):
                    # output received data
                    CH = int(order.decode().split(' ')[-1])
                    f_str = str(GetFrequencyNum(ctypes.c_long(CH), ctypes.c_double(0.0)))
                    #f_str = str(np.random.normal(394, 0.5))
                    connection.send(f_str.encode())
                    
                elif order.decode() in ChannelIteration('wl'):
                    # output received data
                    CH = order.decode().split(' ')[-1]
                    wl_str = str(GetWavelengthNum(ctypes.c_long(CH), ctypes.c_double(0.0)))
                    connection.send(wl_str.encode())
                    
                elif order.decode() == 'close connection':
                    close="connection closed"
                    connection.send(close.encode())
                    connection.close()
                    connection, client_address=self.connection_to_client(sock)
                    
                elif order.decode() == 'break':
                    broken="get order broken"
                    connection.send(broken.encode())
                    break
            
                else:
                    massage='order not valid' 
                    connection.send(massage.encode())
            
            else:
                    pass
class CLIENT:
    def __init__(self, port):
        self.port = port
        self.ip_address = self.get_ip_address()
        self.client_address = (self.ip_address, self.port)
    
    def get_ip_address(self):
        local_hostname = socket.gethostname()
        ip_address = socket.gethostbyname(local_hostname)
        print("IP addres: ",ip_address)
        return ip_address   
    
    def connect_to_server(self,sock, ip_address_server):
        server_address = (ip_address_server, self.port)
        sock.connect(server_address)
        print("Client connected to server {}".format(server_address))
          
    def send_order(self, sock, order):
        text_order = str(order).encode("utf-8")
        sock.sendall(text_order)  
    
    def listen(self, sock):
        message=sock.recv(4096)
        return message.decode()
        
    def ask_f(self, sock, CH):
        self.send_order(sock, f'f CH {CH}')

    def get_f(self,sock, CH):
        self.ask_f(sock, CH) 
        answer = sock.recv(4096)
        return np.round(float(answer.decode()), 6)

    def ask_wl(self, sock, CH):
        self.send_order(sock, f'wl CH {CH}')
        
    def get_wl(self,sock, CH):
        self.ask_wl(sock, CH) 
        answer = sock.recv(4096)
        return float(answer.decode())

    def break_waiting_order(self,sock):
        self.send_order(sock,'f')
        
    def saludar(self):
        print("Hola, soy una galleta muy sabrosa")

    
