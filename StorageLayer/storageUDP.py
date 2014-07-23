__author__ = 'cjuffo'

#    Cleiton Juffo
#    UDP STORAGE LAYER - Python 2.7
#    MUSIC PLAYER SERVICE

import sqlite3 as lite
import socket


musicDB = lite.connect('music.db')

# Function checkUsername checks to see if Username does or does not exist
# If it exists, a user cannot be created with a duplicate username      
def checkUsername(user):
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("SELECT COUNT(*) FROM Users WHERE Username=?",(user,))
            total = musicCur.fetchone()[0]
        except Exception as error:
            print  "ERROR::USERNAME NOT FOUND"
        musicCur.close()
    if total == 0:
        return False
    else:
        return True

# Function checkSongID checks to see if a songID does or does not exist
# If it exists, a song cannot be created with a duplicate songID. Must be unique    
def checkSongID(ID):
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("SELECT COUNT(*) FROM Songs WHERE songID=?",(ID,))
            total=musicCur.fetchone()[0]
        except Exception as error:
            print  "ERROR::NO SONGID MATCH"
        musicCur.close()
    if total == 0:
        return False
    else:
        return True
 
# Function checkPassword verifies log in information   
def checkPassword(username, password):
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("SELECT Password FROM Users WHERE Username=?",(username,))
            passw=musicCur.fetchone()[0]
            if password == passw:
                return True
            else:
                return False
        except Exception as error:
            print  "ERROR::USERNAME NOT FOUND"
        musicCur.close()
    
# Search for a song, returns all information
def findSong(query, option):
    if(option=="title"): 
        with musicDB:
            musicCur = musicDB.cursor()
            try:
                musicCur.execute("SELECT * FROM Songs WHERE Title=?",(query,))
                songlist=musicCur.fetchall()
                song = '||'.join(['::'.join(map(str,row)) for row in songlist])
            except Exception as error:
                mess =  "ERROR||NOT FOUND"
                musicCur.close()
                return mess
            if song == "":
                musicCur.close()
                return "ERROR||NOT FOUND"
            musicCur.close()
            return song
    if(option=="artist"): 
        with musicDB:
            musicCur = musicDB.cursor()
            try:
                musicCur.execute("SELECT * FROM Songs WHERE Artist=?",(query,))
                songlist=musicCur.fetchall()
                song = '||'.join(['::'.join(map(str,row)) for row in songlist])
            except Exception as error:
                mess =  "ERROR||NOT FOUND"
                musicCur.close()
                return mess
            if song == "":
                musicCur.close()
                return "ERROR||NOT FOUND"
            musicCur.close()
            return song
    if(option=="genre"):
        with musicDB:
            musicCur = musicDB.cursor()
            try:
                musicCur.execute("SELECT * FROM Songs WHERE Genre=?",(query,))
                songlist=musicCur.fetchall()
                song = '||'.join(['::'.join(map(str,row)) for row in songlist])
            except Exception as error:
                mess =  "ERROR||NOT FOUND"
                musicCur.close()
                return mess

            if song == "":
                musicCur.close()
                return "ERROR||NOT FOUND"
            musicCur.close()
            return song
    if(option=="rating"): 
        with musicDB:
            musicCur = musicDB.cursor()
            try:
                musicCur.execute("SELECT * FROM Songs WHERE Rating>=?",(query,))
                songlist=musicCur.fetchall()
                song = '||'.join(['::'.join(map(str,row)) for row in songlist])
            except Exception as error:
                mess =  "ERROR||NOT FOUND"
                musicCur.close()
                return mess
            if song == "":
                musicCur.close()
                return "ERROR||NOT FOUND"
            musicCur.close()
            return song
    if (option == "all"):
        with musicDB:
            musicCur = musicDB.cursor()
            musicCur.execute("SELECT * FROM Songs")
            songlist = musicCur.fetchall()
            song = '||'.join(['::'.join(map(str, row)) for row in songlist])
            if song == "":
                return "ERROR||NO SONGS FOUND"
            musicCur.close()
            return song

    if(option=="one"):
        with musicDB:
            musicCur = musicDB.cursor()
            try:
                musicCur.execute("SELECT * FROM Songs WHERE songID=?",(query,))
                songlist=musicCur.fetchall()
                song = '||'.join(['::'.join(map(str,row)) for row in songlist])
            except Exception as error:
                mess =  "ERROR||NOT FOUND"
                musicCur.close()
                return mess
            if song == "":
                musicCur.close()
                return "ERROR||NOT FOUND"
            musicCur.close()
            return song

### UPDATE SQL TABLE WITH NEW CALCULATED RATING        
def updateRating(songID, userID, rating):
    with musicDB:
        musicCur = musicDB.cursor()
        musicCur.execute("SELECT Rating FROM Ratings WHERE songID=? AND userID=?",(songID,userID,))
        data=musicCur.fetchone() 
        if data is None:    #doesn't exist in ratings table
            try:
                musicCur.execute("INSERT INTO Ratings VALUES(?, ?, ?)",(songID, userID, rating))
            except Exception as error:
                mess =  "ERROR:: NO RAT INSERT"
                musicCur.close()
                return mess
        else:
            try:
                musicCur.execute("UPDATE Ratings SET Rating = ? WHERE songID = ? AND userID = ?",(rating, songID, userID))
            except Exception as error:
                mess =  "ERROR:: NO RAT UPDATE"
                musicCur.close()
                return mess
        try:
            musicCur.execute("SELECT AVG(Rating) FROM Ratings WHERE songID=?",(songID,))
            newRating=musicCur.fetchone()[0]
        except Exception as error:
                mess =  "ERROR:: NO SONG ID FOUND"
                musicCur.close()
                return mess
        try:
            musicCur.execute("UPDATE Songs SET Rating = ? WHERE songID = ?",(newRating, songID))
            musicCur.close()
            song = "OK::"+str(songID)+"::"+str(newRating)
        except Exception as error:
                mess =  "ERROR:: NO UPDATE RAT"
                musicCur.close()
                return mess
        musicCur.close()
        return song
        
        
### Process all incoming request messages - Acts as the protocol.    
def processMessage(message):
    parseMess=message.split("::")
    print "RECEIVED: ", parseMess
    if parseMess[0]== "USR":
        if parseMess[1]=="IN":
            if checkUsername(parseMess[2]) and checkPassword(parseMess[2],parseMess[3]):
                return "USR::OK::"+parseMess[2]
            else:
                return "USR::ERROR::LOGIN NOT AUTHORIZED"
        elif parseMess[1]=="OUT":
                return "OK::Logged Out"
    elif parseMess[0]=="SRCH":
        if parseMess[1]=="ART":
            outMess = findSong(parseMess[2], "artist")
            return outMess
        elif parseMess[1]=="TITLE":
            outMess = findSong(parseMess[2], "title")
            return outMess
        elif parseMess[1]=="GEN":
            outMess = findSong(parseMess[2], "genre")
            return outMess
        elif parseMess[1]=="RAT":
            outMess = findSong(parseMess[2], "rating")
            return outMess
        elif parseMess[1]=="ALL":
            outMess = findSong("all", "all")
            return outMess
        elif parseMess[1]=="ONE":
            outMess = findSong(parseMess[2], "one")
            return outMess
    elif parseMess[0]=="RAT":
        outMess = updateRating(parseMess[1],parseMess[2],parseMess[3])   
        return outMess
    else:
        return "ERROR::UNKNOWN ERROR"
        
    
        
def main():
    
    print "MUSIC STORAGE DATA LAYER"
    print "Listening for communications ..."


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 6666))
    buf_size = 2048
    while True:
        dataFromClient, address = server_socket.recvfrom(buf_size)
        print "---------------------------------------------------------------------------------------"
        print "-- [BEGIN] --" 
        outMess=processMessage(dataFromClient)
        print "SENDING: ",outMess
        server_socket.sendto(outMess, address)
        print "-- [END] --"

        
main()
    