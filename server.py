#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    Users = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        for line in self.rfile:

            if line[:8].decode('utf-8') == 'REGISTER':
                print(line.decode('utf-8'))
                User = line[13:-10].decode('utf-8')
                self.Users[User] = self.client_address[0]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif line.decode('utf-8').split(':')[0] == 'Expires':
                date = line.decode('utf-8').split(':')[1]
                date = date[:-2]
                if date == '0':
                    print('Expirado')
                    del self.Users[User]
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                else:
                    print('NO expirado')
                
        print(self.Users)
if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
