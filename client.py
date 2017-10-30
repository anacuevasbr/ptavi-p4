#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Leemos los parámatros
if len(sys.argv) != 6:
        sys.exit('Usage: client.py ip puerto register' +
                 'sip_address expires_value')
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
User = sys.argv[4]


if sys.argv[3] == 'register':
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((SERVER, PORT))
        my_socket.send(bytes('REGISTER sip:' + User + ' SIP/2.0\r\n' +
                       'Expires:' + sys.argv[5] + '\r\n\r\n', 'utf-8'))
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))

    print("Socket terminado.")
