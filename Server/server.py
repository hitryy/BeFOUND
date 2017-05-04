import socket
import threading
import time
import pickle
import sys
import logging
sys.path.append('/home/hitryy/_Projects/BeFOUND/BeFOUND/Network-settings/')
from network_settings import *
from connection import Connection
from program_info import *

'''Socket multithreading server
for local server on station for communicating with raspberry(ies)'''
class Server:

    # init server based on port, host, count of listeners, client timeout
    def __init__(self, port, host = "127.0.0.1", port_count = 10,
        client_timeout = 8):
        self.port = port
        self.host = host
        self.__port_count = port_count
        self.__client_timeout = client_timeout
        self.__run = False
        self.__connected_clients = []

        log = '{0} Server init. ADDRESS: {1}, PORT: {2}'.format(
            SERVER_NAME,
            self.host,
            self.port)
        logging.info(log)
        print(log)

        print("'stop' to stop server"
              "'info' to get info about server")

    # represent an instance
    def __repr__(self):
        return 'Server(port={}, host={})'.format(self.port, self.host)

    # start server, each client has own thread
    def start_listen(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set options for reusing address (port)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))
        self.__sock.listen(self.__port_count)
        self.__run = True

        log = "Server started... Count of ports to listen: {0}\n"
              "Client timeout: {1} sec."
              .format(self.__port_count, self.__client_timeout)
        logging.info(log)
        print(log)

        while self.__run:
            try:
                client, addr = self.__sock.accept()
                client.settimeout(self.__client_timeout)

                connection = Connection()
                client_thread = threading.Thread(
                    target = self.__listen_to_client,
                    args = (client, addr, connection))
                connection.set_thread(client_thread)
                self.__connected_clients.append(connection)

                client_thread.start()
            except:
                pass
            self.__connected_clients = self.check_clients_working()

        self.__sock.close()
        for c in self.__connected_clients:
            c.thread.join()

        log = "Server now is stopped"
        logging.info(log)
        print(log)

    # for receiving data from client, binds to thread
    def __listen_to_client(self, client, addr, connection):
        while self.__run:
            try:
                self.data = client.recv(1024).decode()
                # print(type(pickle.loads(self.data)))

                if (not self.data):
                    log = 'Client disconnected. ADDRESS: {0}, PORT: {1}'
                          .format(addr[0], addr[1])
                    logging.info(lg)
                    print(log)

                    break

                log_recv = 'Received: <{0}> from {1}'.format(self.data, addr[0])
                logging.info(log_recv)
                print(log_recv)
            except socket.timeout:
                log_ex = 'Client timeout. ADDRESS: {0}, PORT: {1}'
                         .format(addr[0], addr[1])
                logging.warning(lg_ex)
                print(log_ex)

                break

        client.close()
        connection.closed = True

    # stop server
    def stop_server(self):
        log = "Trying to stop server..."
        logging.info(log)
        print(log)
        
        self.__run = False
        self.__sock.close()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host,
                                                                   self.port))

    # chech all threads, join thread if connection.closed is True
    def check_clients_working(self):
        working_clients = []
        for c in self.__connected_clients:
            if c.closed:
                c.thread.join()
            else:
                working_clients.append(c)
        return working_clients

if __name__ == '__main__':
    logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                        level = logging.DEBUG, filename = u'main_s.log')
    server = Server(LOCAL_SERVER_PORT, LOCAL_SERVER_HOST,
                    LOCAL_SERVER_PORT_COUNT, LOCAL_SERVER_CLIENT_TIMEOUT)
    t = threading.Thread(target=server.start_listen)
    t.start()

    while True:
        input_msg = input()
        if (input_msg == 'stop'):
            server.stop_server()
            break
        elif (input_msg == 'info'):
            print(repr(server))

    t.join()

    print(CAPTION)
