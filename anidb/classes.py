import sys
import zlib
import os

QUALITY = ['unknown', 'TV', 'DVD', 'BD']

class Series(object):
    """An anime series. Contain information about all files"""
    
    def __init__(self, location="", episode_number=0):  
        """Set default values for a blank series"""
        self.location = location
        self.episode_number = episode_number
        self.episode_list = [None for i in range (episode_number)]
        #quality = QUALITY[0] 
        
        
    def get_episode(self, number):
        return self.episode_list[number]
        
    def get_episode_list(self):
        list = [None]
        for episode in self.episode_list:
            list.append(episode)
        return list
        
    def print_episode_list(self):
        for episode in self.episode_list:
            if episode != None:
                print episode.filename
            else: # no episode there yet
                pass
           
    def add_episode(self, episode):
        if self.episode_list[episode.number] != None:
            print "Error. Already have that episode"
        else:
            self.episode_list[episode.number] = episode
    
class Episode(object):
    """An anime episode. Contain information about just one episode"""
    
    def __init__(self, number=0, crc32="", filename="", filepath=""):
        self.number = number
        self.crc32 = crc32
        self.filename = filename
        self.filepath = filepath
   
    def print_filename(self):
        print self.filename
    
"""
For checking directories use
    os.listdir
    os.path.isdir
    os.isfile
Python has crc32 in stdlib

"""
