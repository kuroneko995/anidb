from anidb import classes
from os import path
import os
import pickle

class Anime_database:
    """Anime database object. Contain list of series, and list of drives
    Attributes:
        series_list : list of all Series object. indexed by series name
        drives_list : list of all external HDD containing the files
    """
    def __init__(self):
        self.series_list = {}
        self.drives_list = {}

def load_database():
    """Load database in same directory. Return database file if success. 
    If no file found, return empty databse"""
    file_path = path.join(os.getcwd(), 'data.txt')
    if path.isfile(file_path): #databse file found
        save_file = open(file_path)
        my_db = pickle.load(save_file)
        return my_db
    else:
        return False
        
def save_database(database_object):
    save_file = open('data.txt','w')
    
    pickle.dump(database_object, save_file)
    
    
def scan_folder(search_path):
    """UNDER CONSTRUCTION
    """
    directory = []
    directory += os.listdir(search_path)
    while directory != []:
        folder_name = directory.pop()
        if path.isdir(path.join(folder_path, folder_name)): #If it is a folder
            pass
        else: # If not, ignore
            pass
    
def add_files(folder_path, database):
    """Check if folder is an anime folder. 
    If yes, add files immediately inside folder to database object
    If no, pass
    """
    if is_anime_folder(folder_path):
        folder_name = path.split(folder_path)[1]
        parse = parse_folder_name(folder_name)
        series_name = parse[0]
        
        quality = parse[1] # not used 
        fansubs = parse[2] # not used
        if series_name in database.series_list:
            # Series exists.update files list 
            pass
        else: # Series not in database. Add new series
            database.series_list[series_name] = classes.Series(folder_name)
            thisSeries = database.series_list[series_name]
            for file in os.listdir(folder_path):                
                if path.isfile(path.join(folder_path,file)): # Check if it is a file                    
                    eps_number = get_eps_number(file)                    
                    Eps = classes.Episode(eps_number,"",file,
                                            path.join(folder_path,file))                 
                    thisSeries.add_episode(Eps)
                else:
                    pass
    else:
        pass

def get_eps_number(filename):
    """Parse the folder name and return the episode number
    Assumption of folder naming is:
    Mahou Shoujo Madoka Magica [1080p, Doki]
    """
    temp_split = filename.split("[")
    eps_number = ""
    for char in temp_split[1]:
        if char in "0123456789":
            eps_number += char 
            if len(eps_number) >= 2:
                break
                
    return int(eps_number)

        
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