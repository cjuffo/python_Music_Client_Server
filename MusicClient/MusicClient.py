import sys

import socket
import subprocess

__author__ = 'cjuffo'

import socket

HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


class lastPlayed:
    def __init__(self, id=000, path= "", title="", artist="", genre="", rating=0.0):
        self.id = id
        self.path = path
        self.title = title
        self.artist = artist
        self.genre = genre
        self.rating = rating

lastSong = lastPlayed()

def downloadSong(songID, userID):
    download = "::".join(["DOWN",str(songID)])
    sock.send(download)
    song = sock.recv(4096)
    songInfo = song.split("::")
    if songInfo[0] == "ERROR":
        print "ERROR IN DOWNLOAD"
        return
    lastSong.id =songInfo[0]
    lastSong.title = songInfo[1]
    lastSong.artist = songInfo[2]
    lastSong.genre = songInfo[3]
    lastSong.rating = songInfo[4]

    sock.send("OK")
    size_mp3 = sock.recv(4096)
    print "SIZE OF MP3 %s" % size_mp3
    bytes_remaining = int(size_mp3)
    max_chunk = 10240
    filename = ".".join([str(songID), "mp3"])
    f_handle = open(filename, 'wb')
    while bytes_remaining > 0:
        data = sock.recv(min(bytes_remaining, max_chunk))
        f_handle.write(data)
        f_handle.flush()
        bytes_remaining -= len(data)
    print "\n\t\tDownload Finished"
    f_handle.close()
    subprocess.call([filename], shell="True")

    choice = input("\t\tDo you wish to rate this song? 1) Yes 2) No \n\t\tEnter: ")

    if choice == 1:
        newrating = input("\n\t\t\tEnter rating from 1 to 5: ")
        if newrating<1 or newrating>5:
            newrating = input("\n\t\t\tPlease enter a rating from 1 to 5: ")
        sock.send("RAT::"+str(songID)+"::"+userID+"::"+str(newrating))
        reply = sock.recv(1024)
        splitReply = reply.split("::")
        print splitReply
        if splitReply[0]=="OK":
            print "\n\t\tNew Rating for this song is now: %.2f" % float(splitReply[2])


def main():

    index=0
    login=False
    done=False
    USR=""

    while login == False:
        uname= raw_input("Enter username:  ")
        upw = raw_input("Enter password:  ")
        sock.send("USR::IN::"+uname+"::"+upw)
        reply = sock.recv(2048)
        parseMess = reply.split("::")
        if parseMess[0]=="OK":
            USR=uname
            print "\n\t\t"+ parseMess[1]
            login = True
        else:
            print "\n\t\t"+ parseMess[1]


    while done == False:
        print("\n1) Search By Song Title \t2) Search By Artist of Song\n3) Search By Song Genre \t4) Search By Song Rating\n5) Show for all songs   \t6) Log Out")
        index = input("\n\tENTER NUMBER: ")
        #Search By Song Title
        if index==1:
            print "\n\t\t******* SEARCH BY TITLE *******"
            query= raw_input("Enter Song Title:  ")
            sock.send("SRCH::TITLE::"+ query)
            reply = sock.recv(2048)
            message = reply.split("||")
            if message[0]!="ERROR":
                listindex =0
                print "Found Song(s): \n"
                while listindex < len(message):
                    song = message[listindex].split("::")
                    print "******* Song Number "+str(listindex+1)+" *******"
                    print "\tSong ID: "+ song[0] +"\n\tTITLE: "+ song[2]
                    print "\tARTIST: "+ song[3]+ "\n\tGENRE: "+ song[4]
                    if song[5]!= "None":
                        rating = float(song[5])
                        print "\tRATING: %.2f" % rating
                    else:
                        print "\tRATING: NO RATING YET"
                    print "\n"
                    listindex +=1

                choice = input("\t\tDo you wish to download one of these songs? 1) Yes 2) No\nENTER: ")

                if choice == 1:
                    downloadID = input("\n\t\t\tEnter Song ID to download: ")
                    downloadSong(downloadID,USR)
            else:
                print "\n\tSearch Error !!!"
                print "\n\tERROR CODE: "+ message[1]

        #Search By Song Artist
        elif index==2:
            print "\n\t\t******* SEARCH BY ARTIST *******"
            query = raw_input("Enter Artist Name:  ")
            sock.send("SRCH::ART::"+ query)
            reply = sock.recv(2048)
            message = reply.split("||")
            if message[0]!="ERROR":
                listindex =0
                print "Found Song(s): \n"
                while listindex < len(message):
                    song = message[listindex].split("::")
                    print "******* Song Number "+str(listindex+1)+" *******"
                    print "\tSong ID: "+ song[0] +"\n\tTITLE: "+ song[2]
                    print "\tARTIST: "+ song[3]+ "\n\tGENRE: "+ song[4]
                    if song[5]!= "None":
                        rating = float(song[5])
                        print "\tRATING: %.2f" % rating
                    else:
                        print "\tRATING: NO RATING YET"
                    print "\n"
                    listindex +=1
                choice = input("\t\tDo you wish to download one of these songs? 1) Yes 2) No\nENTER: ")

                if choice == 1:
                    downloadID = input("\n\t\t\tEnter Song ID to download: ")
                    downloadSong(downloadID,USR)
            else:
                print "\n\tSearch Error !!!"
                print "\n\tERROR CODE: "+ message[1]

        #Search By Song Genre
        elif index==3:
            print "\n\t\t******* SEARCH BY GENRE *******"
            query = raw_input("Enter Genre:  ")
            sock.send("SRCH::GEN::"+ query)
            reply = sock.recv(2048)
            message = reply.split("||")
            if message[0]!="ERROR":
                listindex =0
                print "Found Song(s): \n"
                while listindex < len(message):
                    song = message[listindex].split("::")
                    print "******* Song Number "+str(listindex+1)+" *******"
                    print "\tSong ID: "+ song[0] +"\n\tTITLE: "+ song[2]
                    print "\tARTIST: "+ song[3]+ "\n\tGENRE: "+ song[4]
                    if song[5]!= "None":
                        rating = float(song[5])
                        print "\tRATING: %.2f" % rating
                    else:
                        print "\tRATING: NO RATING YET"
                    print "\n"
                    listindex +=1
                choice = input("\t\tDo you wish to download one of these songs? 1) Yes 2) No\nENTER: ")

                if choice == 1:
                    downloadID = input("\n\t\t\tEnter Song ID to download: ")
                    downloadSong(downloadID,USR)
            else:
                print "\n\tSearch Error !!!"
                print "\n\tERROR CODE: "+ message[1]

        #Search By Song Rating
        elif index==4:
            print "\n\t\t******* SEARCH BY RATING (>X) *******"
            query = raw_input("Enter Minimum Rating[1 to 5]:  ")
            sock.send("SRCH::RAT::"+ query)
            reply = sock.recv(2048)
            message = reply.split("||")
            if message[0]!="ERROR":
                listindex =0
                print "Found Song(s): \n"
                while listindex < len(message):
                    song = message[listindex].split("::")
                    print "******* Song Number "+str(listindex+1)+" *******"
                    print "\tSong ID: "+ song[0] +"\n\tTITLE: "+ song[2]
                    print "\tARTIST: "+ song[3]+ "\n\tGENRE: "+ song[4]
                    if song[5]!= "None":
                        rating = float(song[5])
                        print "\tRATING: %.2f" % rating
                    else:
                        print "\tRATING: NO RATING YET"
                    print "\n"
                    listindex +=1
                choice = input("\t\tDo you wish to download one of these songs? 1) Yes 2) No\nENTER: ")

                if choice == 1:
                    downloadID = input("\n\t\t\tEnter Song ID to download: ")
                    downloadSong(downloadID,USR)
            else:
                print "\n\tSearch Error !!!"
                print "\n\tERROR CODE: "+ message[1]
        #Display all songs
        elif index==5:
            print "\n\t\t******* ALL SONGS) *******"
            sock.send("SRCH::ALL")
            reply = sock.recv(12000)
            message = reply.split("||")
            if message[0]!="ERROR":
                listindex =0
                print "Found Song(s): \n"
                while listindex < len(message):
                    song = message[listindex].split("::")
                    print "******* Song Number "+str(listindex+1)+" *******"
                    print "\tSong ID: "+ song[0] +"\n\tTITLE: "+ song[2]
                    print "\tARTIST: "+ song[3]+ "\n\tGENRE: "+ song[4]
                    if song[5]!= "None":
                        rating = float(song[5])
                        print "\tRATING: %.2f" % rating
                    else:
                        print "\tRATING: NO RATING YET"
                    print "\n"
                    listindex +=1
                choice = input("\t\tDo you wish to download one of these songs? 1) Yes 2) No\nENTER: ")

                if choice == 1:
                    downloadID = input("\n\t\t\tEnter Song ID to download: ")
                    downloadSong(downloadID,USR)
            else:
                print "\n\tSearch Error !!!"
                print "\n\tERROR CODE: "+ message[1]


        #LOG OUT
        elif index==6:
            print "************ Client Terminated ************"
            sock.send("USR::OUT::"+uname)
            sock.close()
            done = True




if __name__ == "__main__":
    main()