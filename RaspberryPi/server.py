import socket
import threading
import time
import errno
import pickle
import sys
sys.path.append('/home/hitryy/_Projects/BeFOUND/BeFOUND/Server-settings/')
from server_settings import *

'''Socket server UDP non-multithreading for receiving data
from LoRa'''
class ServerMediator:

    def __init__(self, port, port_to_send, host = "127.0.0.1", host_to_send = "127.0.0.1", socket_timeout = 8):
        self.port = port
        self.host = host
        self.port_to_send = port_to_send
        self.host_to_send = host_to_send
        self.__socket_timeout = socket_timeout
        self.__run = False
        print('Server init. ADDRESS: {0}, PORT: {1}'.format(self.host,
                                                            self.port))
        print("'stop' to stop server"
              "'info' to get info about server")

    def __repr__(self):
        return 'Server(port={}, host={})'.format(self.port, self.host)

    def __create_or_update_socket_to_send(self):
        self.__sock_to_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock_to_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock_to_send.connect((self.host_to_send, self.port_to_send))

    def start_listen_and_send(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))
        self.__sock.settimeout(self.__socket_timeout)

        self.__create_or_update_socket_to_send()

        self.__run = True
        print("Server started... Socket timeout: {0} sec.".format(self.__socket_timeout))
        while self.__run:
            try:
                self.data = self.__sock.recv(1024).encode()
                time.sleep(0.01)
                # data_l = [self.data]
                self.__sock_to_send.send(self.data.encode())
                print('Received: <{0}>'.format(self.data))
            except socket.timeout:
                print('Socket timeout. Dont pay attention to this message')
            except IOError as e:
                if e.errno == errno.EPIPE:
                    print('Local server rejected connection, because timeout left. Connect again')
                    self.__create_or_update_socket_to_send()

        self.__sock.close()
        self.__sock_to_send.close()
        print('Server now is stopped')

    def stop_listening(self):
        self.__run = False
        print('Server is closing...')

if __name__ == '__main__':
    server = ServerMediator(MEDIATOR_SERVER_PORT, MEDIATOR_SERVER_PORT_TO_SEND, MEDIATOR_SERVER_HOST, MEDIATOR_SERVER_HOST_TO_SEND, MEDIATOR_SERVER_SOCKET_TIMEOUT)
    t = threading.Thread(target=server.start_listen_and_send)
    t.start()

    while True:
        input_msg = input()
        if (input_msg == 'stop'):
            server.stop_listening()
            break
        elif (input_msg == 'info'):
            print(repr(server))

    t.join()
