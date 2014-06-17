from anidb import classes
from anidb import GUI
from os import path
from Tkinter import * ### (1)
from ttk import *
import os
import pickle
import zlib
import datetime
EXTENSIONS = ['.mkv', '.avi', '.mp4']


class Anime_database:
    """Anime database object. Contain list of series, and list of drives
    Attributes:
        series_list : list of all Series object. indexed by series name
        drives_list : list of all external HDD containing the files
    """
    def __init__(self):
        self.series_list = {}
        self.drives_list = {}
        
    def save(self, save_file = 'data.txt'):
        """Save current database into a file. If not specified default to data.txt in same directory"""
        myfile = open(save_file,'w') 
        pickle.dump(self, myfile)    
         
    def load(self, load_path = ""):
        """Load database from file. If not specified, load 'data.txt' in same directory"""
        file_path = path.join(os.getcwd(), 'data.txt')
        if not path.isfile(load_path) and not path.isfile(file_path):
            print "Error loading"
            return
        elif path.isfile(load_path):
            file_path = load_path
        else: # Path is wrong, default to data.txt
            pass
        save_file = open(file_path)
        loaded_db = pickle.load(save_file)
        self.series_list = loaded_db.series_list
        self.drives_list = loaded_db.drives_list
        save_file.close()

    def add_folder(self, folder_path):
        """Check if folder is an anime folder. 
        If yes, add files immediately inside folder to self
        If no, pass
        """
        folder_name = path.split(folder_path)[1]
        if is_anime_folder(folder_name):
            folder_name = path.split(folder_path)[1]
            parse = parse_folder_name(folder_name)
            series_name = parse[0] # Get anime name from folder
            
            quality = parse[1] # Quality (not used)
            fansubs = parse[2] # Fansub group (not used)
            if series_name in self.series_list:
                # Series exists.update files list. Do nothing
                # TO BE UPDATED
                pass
            else: # Series not in database. Add new series
                self.series_list[series_name] = classes.Series(location=folder_path, 
                                                name = series_name)
                thisSeries = self.series_list[series_name]
                
                for file in os.listdir(folder_path):                
                    if path.isfile(path.join(folder_path,file)) and "mkv" in file: # Check if it is a file                    
                        eps_number = get_eps_number(file)                    
                        Eps = classes.Episode(eps_number,"",file,
                                                path.join(folder_path,file))                 
                        thisSeries.add_episode(Eps)
                    else:
                        pass
        else: #Not an anime folder, do nothing
            pass    
    
    
    def scan_folder(self, search_path):
        """Depth first search into search_path to look for anime folders and add
        to databse. Use a queue.
        """
        directory = []
        directory += [path.join(search_path, branch) for branch in os.listdir(search_path)] 
        #print "Debug scan_folder1", [ path.join(search_path, branch) for branch in os.listdir(search_path)]
        while directory != []:
            folder_path = directory.pop()
            #print "Debug scan_folder:"+folder_path+"and"+branch
           
            if path.isdir(folder_path): #If it is a folder
                #print "Debug. Scanning folder:" + folder_path
                self.add_folder(folder_path)
                directory = [path.join(folder_path, branch) for branch in os.listdir(folder_path)]  + directory
            else: # If not, ignore
                pass

class Hash_entry:
    def __init__(self, crc32="", crc32_match=False, ed2k="", ed2k_match=False):
        self.crc32 = crc32
        self.crc32_match = crc32_match
        self.crc32_date = datetime.date(1,1,1)
        self.ed2k = ed2k
        self.ed2k_match = ed2k_match        
        self.ed2k_date = datetime.date(1,1,1)
        
        

    
    
                
class Hash_database:
    """Basically a few dictionaries with keys as filenames and entry as  hashes
    """
    dict_list = ["crc32", "ed2k"]
    
    def __init__(self,crc32_dict = "", ed2k_dict = ""):
        """Load files if any. Must contain full path"""
        if path.isfile(crc32_dict):
            self.crc32_dict = self.load("crc32", crc32_dict)
        else:
            self.crc32_dict = {}
            
        if path.isfile(ed2k_dict):
            self.ed2k_dict = self.load("ed2k", ed2k_dict)
        else:
            self.ed2k_dict = {}
            
    def load(self, dict_name, file_path=""):
        """Try to load hash dictionary from file. If invalid path return 'Invalid path'"""
        if path.isfile(file_path):
            myfile = open(file_path, 'r')
        elif file_path == "":
            myfile = open(dict_name + '_hash.dat','r')
        else:
            return "Invalid path"
        
        if dict_name == "crc32":
            self.crc32_dict = pickle.load(myfile)
        elif dict_name == "ed2k":
            self.ed2k_dict = pickle.load(myfile)
        else:
            return "Wrong dictionary selected"
        myfile.close()
        return "Dictionary loaded"
        
    def save(self, dict_name, save_file = ''):
            
        if save_file == '':
            myfile = open(dict_name + '_hash.dat','w')
        else:
            myfile = open(save_file, 'w')
               
        if dict_name == "crc32":
            pickle.dump(self.crc32_dict, myfile)       
        elif dict_name == "ed2k":
            pickle.dump(self.ed2k_dict, myfile)
        else:
            pass
        
        myfile.close()
    
    
    
    def add(self, hash_type, file_path):
        if not path.isfile(file_path):
            return ""
        else:        
            file_name = path.split(file_path)[1] 
            if not is_anime_file(file_path):
                return ""
                
            myfile = open(file_path, 'rb')
            data = myfile.read()
            myfile.close()
            if hash_type == "crc32":
                print "Hashing: " + file_name
                crc32 = zlib.crc32(data)
                self.crc32_dict[file_name] = Hash_entry()
                entry = self.crc32_dict[file_name]
                entry.crc32 = "%X" %(crc32 & 0xFFFFFFFF) #Convert to unsigned hex
                entry.crc32_date = entry.crc32_date.today()
                entry.crc32_match = entry.crc32 in file_name
            elif hash_type == "ed2k":
                pass
            else:
                pass
                
    def update(self, hash_type, file_path):
        if hash_type == "crc32":
            dict = self.crc32_dict
            
        if not path.isfile(file_path):
            return ""
        else:
            file_name = path.split(file_path)[1]
            if file_name in dict:
                myfile = open(file_path, 'rb')
                data = myfile.read()
                myfile.close()
                crc32 = zlib.crc32(data)
                entry = self.crc32_dict[file_name]
                entry.crc32 = "%X" %(crc32 & 0xFFFFFFFF) #Convert to unsigned hex
                entry.crc32_date = entry.crc32_date.today()
                entry.crc32_match = entry.crc32 in file_name
            else:
                self.add(hash_type, file_path)
                    
    def update_folder(self, hash_type, search_path):
        """Depth first search into search_path to look for anime files
        If new file, add to database after hashing.
        If already in database update the hash
        """
        directory = []
        directory += [path.join(search_path, branch) for branch in os.listdir(search_path)] 
        #print "Debug scan_folder1", [ path.join(search_path, branch) for branch in os.listdir(search_path)]
        while directory != []:
            folder_path = directory.pop()
            #print "Debug scan_folder:"+folder_path+"and"+branch
           
            if path.isdir(folder_path): #If it is a folder               
                directory = [path.join(folder_path, branch) for branch in os.listdir(folder_path)]  + directory
            elif path.isfile(folder_path):
                self.update(hash_type, folder_path)
            else: # If not, ignore
                pass                
                
    def add_new_folder(self, hash_type, search_path):
        """Depth first search into search_path to look for anime files
        If new file, add to database after hashing.
        If already in database update the hash
        """
        directory = []
        directory += [path.join(search_path, branch) for branch in os.listdir(search_path)] 
        
        while directory != []:
            folder_path = directory.pop()
            if path.isdir(folder_path): #If it is a folder               
                directory = [path.join(folder_path, branch) for branch in os.listdir(folder_path)]  + directory
            elif path.isfile(folder_path): # If it is a file
                file_name = path.split(folder_path)[1] 
                if is_anime_file(file_name) and file_name not in self.crc32_dict:
                    self.add(hash_type, folder_path) # Add if it's not in the database
            else: # If not, ignore
                pass                
         
    def display(self, hash_type):
        if hash_type == "crc32":
            for key in self.crc32_dict:
                entry = self.crc32_dict[key]
                print key + " CRC32 Match: " + str(entry.crc32_match)

  
def is_anime_file(file_name):
        is_anime = False
        for type in EXTENSIONS:
            if type in file_name:
                is_anime = True
                break
        return is_anime

  
def get_eps_number(filename):
    """Parse the folder name and return the episode number
    Assumption of folder naming is:
    Mahou Shoujo Madoka Magica [1080p, Doki]
    """
    #print "Debug.get_eps_number, filename:"+filename
    eps_number = ""
    for char in filename:
        if char in "0123456789":
            eps_number += char 
            if len(eps_number) >= 2:
                break
    if eps_number == "":
        result = 0
    else:
        result = int(eps_number)
        
    return result

        
def parse_folder_name(folder_name):
    """Parse the folder name and retunrn a list
    [Series name, quality, fansub group]
    Assumption of folder naming is:
    Mahou Shoujo Madoka Magica [1080p, Doki]
    """
    series_name = ""
    fansubs = ""
    quality = ""
    temp_split = folder_name.split('[')
    series_name = strip_spaces(temp_split[0])
    temp_split = temp_split[1].split(',')
    quality = strip_spaces(temp_split[0])
    fansubs = strip_spaces(temp_split[1][:-1]) # Remove ] at the end of the split
    return [series_name, quality, fansubs]

def strip_spaces(string):
    return string.lstrip().rstrip()

def is_anime_folder(folder_name):
    return "[" in folder_name and "]" in folder_name
    

