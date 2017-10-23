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
                print("El cliente nos manda ", line.decode('utf-8'))
                User = line[14:-10].decode('utf-8')
                print(User)
                self.Users[User] = self.client_address[0]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                
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
