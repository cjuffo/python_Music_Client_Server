python_Music_Client_Server
==========================

Python Client-Server Music Project by cjuffo

== About ==

This was my final project for the Network Programming class. We had to utilized three seperate tiers (as opposed to two) in order to implement TCP, UDP and database queries. 

== Overall Design ==

The project will involve allowing multiple clients to access the Data Business Layer by
entering their username and password. Upon being granted access, the client will allow the
user to search for songs through various queries (song title, artist, genre and rating), download
a song to play locally, rate a song or display recently played songs. The Mid Layer will handle all
requests from the client, and will access the Data Storage portion to verify information. The
Data Storage will hold information relative to a user and for the entire catalog of songs. The
Data Storage will not hold the actual song (MP3) but only a path. The songs will be stored in a
database relative to the Data Business Layer, and the path returned from the Data Storage
Layer will allow access to that song, which in turn will be sent over to the client. Upon searching
for a song, the user can initiate a download by songID. Once the song is downloaded, it is
automatically played by Windows Media Player and the program allows the user to rate the
song. The Mid Layer allows multiple clients using multi-threading.

== Source Files ==

NOTE: Denotes directory and python script location. Each component [client, mid, storage] will be in its own folder.
Client: MusicClient/MusicClient.py
TCP/MT Mid: MidLayer/midTCP.py
UDP Storage: StorageLayer/storageUDP.py

== Compiling Instructions ==

Songs will only play on Windows OS since the python script initiates Windows Media Player.
Python 2.7 needs to be installed [use ninite.com for Windows executable). Download three all files and unzip. All scripts need to be executed in their own terminal or cmd window. SQLite should already be included with Python 2.7.
Window 1: $ python storageUDP.py
Window 2: $ python midTCP.py
Window 3: $ python MusicClient.py

Note that for Windows, python path must be set in the environment variables path in order to use python command in cmd. If Python 2.7 is already installed on windows, double clicking each python script will open up the python environment for each script

== PDF ==

The PDF contains more information, specifications and diagrams.

