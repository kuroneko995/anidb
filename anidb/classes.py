import sys
import zlib
import os
import datetime

QUALITY = ['unknown', 'TV', 'DVD', 'BD']

class Series(object):
    """An anime series. Contain information about all files"""
    
    def __init__(self, location="", name= "", episode_number=99):  
        """Set default values for a blank series"""
        self.name = name
        self.location = location
        self.episode_number = episode_number
        self.episode_list = {}
        #quality = QUALITY[0] 
    
    def get_episode(self, number):
        return self.episode_list[number]
        

        
    def print_episode_list(self):
        for episode in self.episode_list:            
            print self.episode_list[episode].filename
            
           
    def add_episode(self, new_Episode):
        if new_Episode.number in self.episode_list:
            print self.name + ": Error. Already have that episode"
        else:
            print self.name +": Adding episode:", new_Episode.number
            self.episode_list[new_Episode.number] = new_Episode
            
    
    
    
class Episode(object):
    """An anime episode. Contain information about just one episode
    Attribute:
        number      : episode number
        filename    : system file name. may include whitespace
        filepath    : system file path
        crc32       : crc32 hash of the file
        last_checked: date of the last crc32 check
        
    Methods:
        __init__    : initialize new Episode
        print_name  : print the filename
    """
    
    def __init__(self, number=0, crc32="", filename="", filepath=""):
        self.number = number
        self.crc32 = crc32
        self.filename = filename
        self.filepath = filepath
        self.crc_match = True
        self.last_checked = datetime.date(1,1,1)
        
    def print_name(self):
        print self.filename
       
    def right_path(filepath):
        """Check if the path recorded corresponds to file"""
        return path.isfile(filepath)
    
    def get_crc32():
        """Return CRC32 hash of file
        If no file found return "" 
        """
        if os.path.isfile(self.filepath):
            myfile = open(self.filepath, 'rb')
            data = myfile.read()
            myfile.close()
            crc = zlib.crc32(data)
            return "%X" %(crc & 0xFFFFFFFF) #Convert to unsigned hex
        else: # No file found
            return ""
        
    def update_crc32():
        """Update file crc32, setting crc_match to False if wrong
        Return True if successful, False if mismatch
        First time check update crc and check in file name
        """
        crc_check = self.get_crc32()
        if self.crc32 == "": #First time
            self.crc32 = crc_check
            if crc_check in self.filename:
                crc_match = True
                return True
            else:
                crc_match = False
                return False        
        elif crc_check == self.crc32: #Second time, crc match
            self.lastchecked = self.lastchecked.today()
            return True
        else:
            self.crc32 = crc_check
            return False
            
"""
For checking directories use
    os.listdir
    os.path.isdir
    path.isfile
Python has crc32 in stdlib

"""
