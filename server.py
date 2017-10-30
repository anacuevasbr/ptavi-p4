#!/usr/bin/python3
# -*- coding: utf-8 -*-


import json
import socketserver
import sys
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    """
    Echo server class
    """
    DicUsers = {}

    def register2json(self):
        """
        Gets the dictionary and turns it into a json file
        """
        json.dump(self.DicUsers, open('registered.json', 'w'))

    def json2register(self):
        """
        Gets a json file and turns it into a dictionary file
        """
        try:
            with open('registered.json', 'r') as file:
                self.DicUsers = json.load(file)
        except FileNotFoundError:
            print('NO existe el fichero')

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        checks if the dictionary is empty an calls json 2 register
        """
        if self.DicUsers == {}:
            self.json2register()

        for line in self.rfile:

            if line[:8].decode('utf-8') == 'REGISTER':
                print(line.decode('utf-8'))
                Sip_ad = line[13:-10].decode('utf-8')
                self.DicUsers[Sip_ad] = [self.client_address[0], 0]
            
            elif line.decode('utf-8').split(':')[0] == 'Expires':
                date = line.decode('utf-8').split(':')[1]
                date = time.time() + float(date[:-2])
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(date))
                timenow = time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.gmtime(time.time()))
                self.DicUsers[Sip_ad][1] = date
                self.register2json()
                Delete = []
                for User in self.DicUsers:
                    if str(self.DicUsers[User][1]) <= timenow:
                        Delete.append(User)
                    else:
                        print('NO expirado')
                for User in Delete:
                    del self.DicUsers[User]
                    self.register2json()
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
