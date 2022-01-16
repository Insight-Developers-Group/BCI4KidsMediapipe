#!/usr/bin/env python3
# server.py

import socket
import hashlib
import base64
from bitstring import BitArray



def decodeWebsocketFrame(data):
    msg = []
    offset = 0
    while (offset + 6 < len(data)):
        length = data[offset + 1] - 0x80
        if (length <=125):
            print("Length of Message: {}, Offset: {}".format(length,offset))
            key = []
            key.append(data[offset+2])
            key.append(data[offset+3])
            key.append(data[offset+4])
            key.append(data[offset+5])
            decoded = []
            for i in range(length):
                position = offset+6+i
                decoded.append(data[position] ^ key[i % 4])
            offset = offset + 6+ length
            msg.append(decoded)
        else:
            a = data[offset+2]
            b = data[offset+3]
            length = (a<<8) + b
            key = []
            key.append(data[offset+4])
            key.append(data[offset+5])
            key.append(data[offset+6])
            key.append(data[offset+7])
            decoded = []
            for i in range(length):
                realPos = offset + 8 + i
                decoded[i] = (data[realPos] ^ key[i % 4])
            offset = offset + 8+ length
            msg.append(decoded)
    return msg






HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9898        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)

        data = conn.recv(1024).decode("utf-8") 
        headerasdict = {
        }
        print(type(data))
        print('Data: {}'.format(data))


        for line in data.split('\r\n')[1:len(data.split('\r\n')) -2]:
            print(line)
            parts = line.split(': ')
            headerasdict[parts[0]] = parts[1]
        
        print(headerasdict)
        key = headerasdict['Sec-WebSocket-Key']
        magicString = key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        hash_object = hashlib.sha1(magicString.encode('utf-8'))
        h = hash_object.digest()
        # print(h)
        # print(type(h))
        b = base64.b64encode(h)
        print('-------')
        print(b)
        print(type(b))

        handshakeheader = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept:{}\r\n\r\n".format(b.decode('utf-8'))
    #    b'\x81\x8f\x04\xb8K$I\xc1kJe\xd5.\x04m\xcbknk\xd0%'
        print('Sending: ')
        print(handshakeheader)
        conn.sendall(handshakeheader.encode('utf-8'))
        print('-------------------')

        while True:
            print("Wait for new data")
            data = conn.recv(1024)
            print("Data Recieved: ")
            print(data)
            
            #Integrity Check: Data recieved:
            if ( data[0] != 129):
                print("Invalid Data")
                pass
            messages = decodeWebsocketFrame(data)
            print(messages)
            for msg in messages:
                text= ""
                for letter in msg:
                    text = text + bytes.fromhex(hex(letter)[2:]).decode('utf-8')
                print(text)
            print("------------------------------")


            if not data:
                break
            # conn.sendall(data)

# https://stackoverflow.com/questions/9182350/decode-a-websocket-frame/25558586