anidb
Author: Dang Minh Nguyen
Date: 7/2/2014

=====

A python program I wrote to scan and maintain data of my anime files. It connect to anidb.net through the UDP protocol to collect data and store it in a local database file. You need to have an anidb account to use this program. You can change your local port and username/password in the config.txt file.

Currently the program support the following function:
-Add files: Scan a folder for recognized anime files. Only check extensions .avi, .mkv, .mp4
-Rehash: Hash the file using ed2k and check for integrity
-Open folder: Open the file in explorer
-View/Hide unavailable files: If you have an external HDD and you scan files on it, you can choose to hide those files when the HDD is disconnected

Files are organized based on anime, not folders. If a file has the wrong hash, anidb will not recognize it.

Any comments, suggestions or bugs can be send to ndminh92@gmail.com
