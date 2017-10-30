#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import json
import socketserver
import sys
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    DicUsers = {}

    def register2json(self, User):
        print(User)
        json.dump(self.DicUsers, open('Users.json', 'w'))
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        for line in self.rfile:

            if line[:8].decode('utf-8') == 'REGISTER':
                print(line.decode('utf-8'))
                Sip_ad = line[13:-10].decode('utf-8')
                self.DicUsers[Sip_ad] = [self.client_address[0], 0]
                self.register2json(Sip_ad)
            elif line.decode('utf-8').split(':')[0] == 'Expires':
                date = line.decode('utf-8').split(':')[1]
                date = time.time() + float(date[:-2])
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(date))
                print(date)
                self.DicUsers[Sip_ad][1] = date
                Delete = []
                for User in self.DicUsers:
                    if self.DicUsers[User][1] <= time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.gmtime(time.time())):
                        print('Expirado')
                        Delete.append(User)
                    else:
                        print('NO expirado')
                for User in Delete:
                    del self.DicUsers[Sip_ad]
                    self.register2json(User)
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                    
                
        print(self.DicUsers)
if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', int(sys.argv[1])), SIPRegisterHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
