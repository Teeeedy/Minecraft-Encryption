import socket
import select
import sys
from .util import flatten_parameters_to_bytestring

""" @author: Aron Nieminen, Mojang AB"""

class RequestError(Exception):
    pass

class Connection:
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.lastSent = ""

    def setCryptoSession(self, session):
        self.cryptographySession = session

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            e =  "Drained Data: <%s>\n"%data.strip()
            e += "Last Message: <%s>\n"%self.lastSent.strip()
            sys.stderr.write(e)

    def send(self, f, *data):
        """
        Sends data. Note that a trailing newline '\n' is added here

        The protocol uses CP437 encoding - https://en.wikipedia.org/wiki/Code_page_437
        which is mildly distressing as it can't encode all of Unicode.
        """

        s = b"".join([f, b"(", flatten_parameters_to_bytestring(data), b")", b"\n"])
        self._send(s)

    def _send(self, s):
        """
        The actual socket interaction from self.send, extracted for easier mocking
        and testing
        """
        recipientPublicKey = self.cryptographySession.recipient_public_key
        if recipientPublicKey is None:
            print("CANNOT SEND PACKET; PUBLIC KEY NOT GENERATED")
            return
        
        # print(recipientPublicKey)
        cipherText = self.cryptographySession.encrypt(s)
        signatureText = self.cryptographySession.sign(s)

        s = f'{bytes.decode(cipherText)},{bytes.decode(signatureText)}\n'
        s = bytes(s, "utf-8")

        self.drain()
        self.lastSent = s

        self.socket.sendall(s)

    def receive(self):
        """Receives data. Note that the trailing newline '\n' is trimmed"""
        s = self.socket.makefile("r").readline().rstrip("\n")

        #TODO DECRYPT
        skipDecryption = False
        if("NO_ENCRYPTION:" in s):
            s = s.replace("NO_ENCRYPTION:", "")
            skipDecryption = True
        

        if not skipDecryption:
            if(",") not in s:
                print("MESSAGE DOES NOT CONTAIN SIGNATURE- IGNORING MESSAGE")
                return None
            s, signature = s.split(',')
            s = self.cryptographySession.decrypt(bytes(s, 'utf-8'))

            verfication_value = self.cryptographySession.verify(s, bytes(signature, 'utf-8'))

            if(verfication_value == False):
                print("SIGNATURE NOT VERIFIABLE - IGNORING MESSAGE")

                return None

        if s == Connection.RequestFailed:
            raise RequestError("%s failed"%self.lastSent.strip())
        return s
    
    def sendRaw(self, f, *data):
        """
        Sends data. Note that a trailing newline '\n' is added here

        The protocol uses CP437 encoding - https://en.wikipedia.org/wiki/Code_page_437
        which is mildly distressing as it can't encode all of Unicode.
        """

        s = b"".join([f, b"(", flatten_parameters_to_bytestring(data), b")", b"\n"])
        self._sendRaw(s)

    def _sendRaw(self, s):
        """
        The actual socket interaction from self.send, extracted for easier mocking
        and testing
        """
        s = b'NO_ENCRYPTION:' + s

        self.drain()
        self.lastSent = s

        self.socket.sendall(s)

    def sendReceive(self, *data):
        """Sends and receive data"""
        self.send(*data)
        return self.receive()

    def sendReceiveRaw(self, *data):
        """Sends and receive data"""
        self.sendRaw(*data)
        return self.receive()
