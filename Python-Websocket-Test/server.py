#!/usr/bin/env python3
# server.py

import socket
import hashlib
import base64


def dohandshake(self, header, key=None):
    logging.debug("Begin handshake: %s" % header)
    digitRe = re.compile(r'[^0-9]')
    spacesRe = re.compile(r'\s')
    part = part_1 = part_2 = origin = None
    for line in header.split('\\r\\n')[1:]:
        name, value = line.split(': ', 1)
        if name.lower() == "sec-websocket-key1":
            key_number_1 = int(digitRe.sub('', value))
            spaces_1 = len(spacesRe.findall(value))
            if spaces_1 == 0:
                return False
            if key_number_1 % spaces_1 != 0:
                return False
            part_1 = key_number_1 / spaces_1
        elif name.lower() == "sec-websocket-key2":
            key_number_2 = int(digitRe.sub('', value))
            spaces_2 = len(spacesRe.findall(value))
            if spaces_2 == 0:
                return False
            if key_number_2 % spaces_2 != 0:
                return False
            part_2 = key_number_2 / spaces_2
        elif name.lower() == "sec-websocket-key":
            part = bytes(value, 'UTF-8')
        elif name.lower() == "origin":
            origin = value
    if part:
        logging.debug("Using challenge + response")
        #challenge = struct.pack('!I', part_1) + struct.pack('!I', part_2) + key
        #response = hashlib.md5(challenge).digest()
        sha1 = hashlib.sha1()
        sha1.update(part)
        sha1.update("258EAFA5-E914-47DA-95CA-C5AB0DC85B11".encode('utf-8'))
        accept = (b64encode(sha1.digest())).decode("utf-8", "ignore")
        handshake = WebSocket.handshake % {
            'accept': accept,
            'origin': origin,
            'port': self.server.port,
            'bind': self.server.bind
        }
        #handshake += response
    else:
        logging.warning("Not using challenge + response")
        handshake = WebSocket.handshake % {
            'origin': origin,
            'port': self.server.port,
            'bind': self.server.bind
        }
    logging.debug("Sending handshake %s" % handshake)
    self.client.send(bytes(handshake, 'UTF-8'))
    return True


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
       
        print('Sending: ')
        print(handshakeheader)
        conn.sendall(handshakeheader.encode('utf-8'))
        print('-------------------')

        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

        
