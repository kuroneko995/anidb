from anidb import classes
from anidb import GUI
from os import path
from Tkinter import * ### (1)
from ttk import *
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
        
    def save(self, save_file = 'data.txt'):
        """Save current database into a file. If not specified default to data.txt in same directory"""
        myfile = open('data.txt','w') 
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
        if is_anime_folder(folder_path):
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
                    if path.isfile(path.join(folder_path,file)): # Check if it is a file                    
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
        while directory != []:
            folder_path = directory.pop()
            directory = [path.join(folder_path, branch) for branch in os.listdir(folder_path)]  + directory
            if path.isdir(folder_path): #If it is a folder
                add_folder(self, folder_path)
            else: # If not, ignore
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
    
def main():
    my_db = Anime_database()
    my_db.load()
    root = Tk()
    my_GUI = GUI.GUI_window(root)
    for Series in my_db.series_list.keys():
        my_GUI.addSeries(Series, location = my_db.series_list[Series].location)
        for Episode in my_db.series_list[Series].episode_list.values():
            my_GUI.addEpisode(Series, location=Episode.filepath, CRC=Episode.crc32, eps_number = Episode.number)
    root.mainloop()
