__author__ = 'cjuffo'

#    Cleiton Juffo
#    TCP MID LAYER - Python 2.7
#    MUSIC PLAYER SERVICE

import socket, threading, sys, os

host = "localhost"
TCPport = 9999
UDPport = 6666
address = (host, UDPport)
buf_size = 16000
socket_backlog = 4

#SOCK_DGRAM == UDP Datagram
socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#SOCK_STREAM == TCP Socket
socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TELL SYSTEM TO REUSE LOCAL SOCKET IF OTHER SOCKET IS BUSY
socket_TCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_TCP.bind((host,TCPport))
threads = []

# ArrayList currentUsers keeps track of current users logged in
currentUsers = [20]
# Dictionary ID keeps track of matching between port number and userID to help with logging off
ID = {}



def processMessage(message, port):

    parseMess = message.split("::")
    print "RECEIVED["+str(port)+"]: "+ message

    if parseMess[0] == "USR":
        if parseMess[1] == "IN":
            if currentUsers.__contains__(parseMess[2]):
                return "ERROR::ALREADY LOGGED IN"
            data="USR::IN::"+parseMess[2]+"::"+parseMess[3]
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            login = "USR::OK::" + parseMess[2]
            if recv_data == login:
                currentUsers.append(parseMess[2])
                ID[str(port)] = parseMess[2]
                return "OK::LOGIN AUTHORIZED"
            else:
                return "ERROR::NOT AUTHORIZED"
        elif parseMess[1] == "OUT":
            currentUsers.remove(parseMess[2])
            del ID[str(port)]

    elif parseMess[0] == "SRCH":
        if parseMess[1] == "ART":
            data="SRCH::ART::"+parseMess[2]
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            return recv_data
        elif parseMess[1] == "TITLE":
            data="SRCH::TITLE::"+parseMess[2]
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            return recv_data
        elif parseMess[1] == "GEN":
            data="SRCH::GEN::"+parseMess[2]
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            return recv_data
        elif parseMess[1] == "RAT":
            data="SRCH::RAT::"+parseMess[2]
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            return recv_data
        elif parseMess[1] == "ALL":
            data="SRCH::ALL"
            socket_UDP.sendto(data, address)
            recv_data, addr = socket_UDP.recvfrom(buf_size)
            return recv_data
    elif parseMess[0] == "RAT":
        data="RAT::"+parseMess[1]+"::"+parseMess[2]+"::"+parseMess[3]
        socket_UDP.sendto(data, address)
        recv_data, addr = socket_UDP.recvfrom(buf_size)
        return recv_data

    ### TODO: WRITE METHOD TO SEND OVER THE SONG
    elif parseMess[0] == "DOWN":
        data = "SRCH::ONE::" + parseMess[1]
        socket_UDP.sendto(data, address)
        recv_data, addr = socket_UDP.recvfrom(buf_size)

        return "DOWNLOAD::"+recv_data

    else:
        return "ERROR::UNKNOWN ERROR"

class ClientThread(threading.Thread):

    def __init__(self,ip,port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print "\n+++++ New thread started for IP: "+self.ip+" on Port: "+str(self.port)+" +++++"


    def run(self):
        print "\tConnection from IP: "+self.ip+" on Port: "+str(self.port)
        while True:
            try:
                data = self.socket.recv(buf_size)
                print data
                while data or 0:
                    outMess = processMessage(data, self.port)
                    if outMess.startswith("DOWNLOAD"):
                        print "SENDING SONG"
                        splitMess = outMess.split("::")
                        songID = splitMess[1]
                        songPath = splitMess[2]
                        songTitle = splitMess[3]
                        songArt = splitMess[4]
                        songGenre = splitMess[5]
                        songRat = splitMess[6]
                        songInfo = "::".join([songID,songTitle,songArt,songGenre,songRat])
                        print ("SENDING[%s]: %s" % (str(self.port),songInfo))
                        self.socket.send(songInfo)
                        if self.socket.recv(1024) != "OK":
                            print "ERROR IN PROCESSING !!!!"
                            return
                        bytes_remaining = os.path.getsize(songPath)
                        print "BYTES REMAINING: %s" % bytes_remaining
                        print ("SENDING[%s]: %s" % (str(self.port),str(bytes_remaining)))
                        self.socket.send(str(bytes_remaining))
                        max_chunk = 10240
                        f_handle = open(songPath, 'rb')
                        while bytes_remaining > 0:
                            data = f_handle.read(min(bytes_remaining, max_chunk))
                            self.socket.send(data)
                            bytes_remaining -= len(data)
                            print bytes_remaining
                        f_handle.close()

                    else:
                        print ("SENDING[%s]: %s" % (str(self.port),outMess))
                        self.socket.send(outMess)
                        data = self.socket.recv(buf_size)
                else:
                    self.socket.close()
                    try:
                        UNAME = ID[str(self.port)]
                        currentUsers.remove(UNAME)
                        print "\tClient from IP: "+self.ip+" on Port: "+str(self.port)+" disconnected..."
                        break
                    except:
                        print "\tClient from IP: "+self.ip+" on Port: "+str(self.port)+" disconnected..."
                        break
            except:
                self.socket.close()
                try:
                    UNAME = ID[str(self.port)]
                    currentUsers.remove(UNAME)
                    print "\tClient from IP: "+self.ip+" on Port: "+str(self.port)+" disconnected..."
                    break
                except:
                    print "\tClient from IP: "+self.ip+" on Port: "+str(self.port)+" disconnected..."
                    break

def main():
    print "TCP MIDDLE LAYER"
    print "\nListening for incoming connections..."
    while True:
        # .listen specifies max number of queued connections - cj
        socket_TCP.listen(socket_backlog)
        # accept and spin off a new thread
        (clientsock, (ip, port)) = socket_TCP.accept()
        newthread = ClientThread(ip, port, clientsock)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()

main()