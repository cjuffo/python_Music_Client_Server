__author__ = 'cjuffo'


#    Cleiton Juffo
#    DATABASE MANIPULATION FILE - Python 2.7
#    MUSIC PLAYER SERVICE

import sqlite3 as lite

musicDB = lite.connect('music.db')

#####
#    SQLITE FUNCTIONS TO CREATE TABLES, ADD A USER, ADD A SONG - ONLY USED ONCE BY ME TO INITIALIZE TABLES
#####

def createTables():
    with musicDB:
        musicCur = musicDB.cursor()
        musicCur.execute("CREATE TABLE Users(Username TEXT PRIMARY KEY, Password TEXT)")
        musicCur.execute("CREATE TABLE Songs(songID INTEGER PRIMARY KEY, Path TEXT, Title TEXT, Artist TEXT, Genre TEXT, Rating FLOAT )")
        musicCur.execute("CREATE TABLE Ratings(songID INTEGER, userID INTEGER, Rating FLOAT)")
        musicCur.close()

def addUser():
    uNameCheck = True
    while uNameCheck:
        username = raw_input("Enter Username: ")
        uNameCheck = checkUsername(username)
    password = raw_input("Enter Password: ")
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("INSERT INTO Users VALUES(?, ?)",(username, password))
        except Exception as error:
            mess =  "ERROR::NO USER INSERT"
            musicCur.close()
            return mess
        musicCur.close()

def addSong():
    idCheck= True
    while idCheck:
        ID = raw_input("Enter SONGID: ")
        songID = int(ID)
        idCheck=checkSongID(songID)
    path = raw_input("Enter Path: ")
    title = raw_input("Enter Title: ")
    artist = raw_input("Enter Artist: ")
    genre = raw_input("Enter Genre: ")
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("INSERT INTO Songs VALUES(?, ?, ?, ?, ?, NULL)",(songID, path, title, artist, genre))
        except Exception as error:
            mess =  "ERROR::NO SONG INSERT"
            musicCur.close()
            return mess
        musicCur.close()

####
#    END OF SQLITE CREATE FUNCTIONS ###############################################
####
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
        except Exception as error:
            print  "ERROR::USERNAME NOT FOUND"
        musicCur.close()
    if password == passw:
        return True
    else:
        return False

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
            song = "RAT::OK::"+str(songID)+"::"+str(newRating)
        except Exception as error:
                mess =  "ERROR:: NO UPDATE RAT"
                musicCur.close()
                return mess
        musicCur.close()
        return song

def updatePath(songID, newPath):
    print songID
    print newPath
    with musicDB:
        musicCur = musicDB.cursor()
        try:
            musicCur.execute("UPDATE Songs SET Path = ? WHERE songID = ?",(newPath, songID))
        except Exception as error:
            mess =  "ERROR:: NO PATH UPDATE"
            musicCur.close()
            print mess

        musicCur.close()

def main():
    print "DATABASE EDITOR : MUSIC STORAGE"

    print("\n1) Create Tables \t2) Add New Songs\n3) Add New Users \t4) Update Path\n5) Terminate")
    index = input("\n\tENTER NUMBER: ")
    if index==1:
        createTables()
    elif index==2:
        i = 0
        number = input("How many new songs? : ")
        while i < number:
            addSong()
            i +=1
    elif index==3:
        i = 0
        number = input("How many new users? : ")
        while i < number:
            addUser()
            i +=1
    elif index ==4:
        while True:
            songid = raw_input("SONG ID: ")
            newPath = raw_input("SONG PATH: ")
            updatePath(songid,newPath)
            cont = input("\t\tUPDATE MORE? 1) Y 2) N")
            if cont == 2:
                break


main()