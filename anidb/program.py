import threading
import Queue
import time
import sys
import subprocess
from datetime import datetime
import time


from os import path
from anidb import GUI
from anidb import database
from anidb import udp_api
from anidb import file_manager


class Program(object):
    def __init__(self, file_path = 'local_db.db', new = False):
        if path.isfile(file_path):
            self.mydb = database.Local_DB(file_path,new=False)
        else:   
            self.mydb = database.Local_DB(file_path,new=True)
        self.all_job = self.mydb.list_job()
        self.mydb.close()
        self.db_path = file_path
        
        # Setting up queues
        self.msg_queue = Queue.Queue() # Queue for printing message to screen
        self.job_list_queue = Queue.Queue() # Queue to update table in GUI
        # Redirect stdout to msg_queue to be displayed in GUI
        sys.stdout = StdoutRedirector(self.msg_queue)
        self.command_queue = Queue.Queue()
        self.lock = threading.Lock()
        
        # Start GUI object
        self.GUI = GUI.GUI_window(self.msg_queue, self.job_list_queue, self.command_queue, self.lock)
        self.isRunning = True
        self.thread_log = threading.Thread(target=self.monitor_log)
        self.thread_log.start()
        sys.stdout = StdoutRedirector(self.msg_queue)
        self.thread_command = threading.Thread(target=self.monitor_command)
        self.thread_command.start()

        self.only_available_job = {}
        for dict in self.all_job.values():
            file_path = path.join(dict['folder'],dict['file_name'])
            if path.isfile(file_path):
                self.only_available_job[dict['file_name']] = dict
            else:
                pass
        
        self.show_all = True
        
        
    def parse_command(self):
        '''Parse a command, which is a tuple of 2
        '''
        while self.command_queue.qsize():
            self.commandRunning = True
            try:
                command = self.command_queue.get(0)
                if command[0] == 'CONNECT':
                    self.connect_udp()
                elif command[0] == 'ADD_FILES':
                    self.scan_folder(command[1])
                elif command[0] == 'OPEN_FOLDER':
                    self.open_folder(command[1])
                elif command[0] == 'EXIT':
                    self.isRunning = False
                elif command[0] == 'REHASH':
                    self.rehash(command[1])
                elif command[0] == 'SHOW_ALL':
                    self.show_all = command[1]
                    self.showall()
                else: # Not recognized. Do nothing
                    pass
                self.command_queue.task_done()
            except Queue.Empty:
                pass
                
    def open_folder(self,file_name):
        folder = self.mydb.get_info_filename(file_name)['folder'] 
        if path.isdir(folder):
            cmd = 'explorer "%s"' % folder.replace('/','\\')
            print "Opening folder: %s" % folder
            subprocess.Popen(cmd)    
        else:
            print "Folder not found"
            
        
    def connect_udp(self):
        self.connect = udp_api.UDP_Conn()
        self.connect.get_session()
     
    def scan_folder(self, file_path):
        ''' Scan folder. At the end return a full list of dictionaries 
        containing info of files in the localdb
        '''
        if not path.isdir(file_path): # User press cancel or sth
            print "Path not selected or invalid path"
        else:
            file_manager.scan_folder(self.mydb, self.connect, file_path)
            print "Adding files complete"
            self.update_job_lib()
            self.reload_table()
    
    def rehash(self,file_name):
        info = self.mydb.get_info_filename(file_name)
        folder = info['folder']
        fid = info['fid']
        ed2k = self.mydb.get_info_fid(fid)['ed2k']
        file_path = path.join(folder, file_name)
        if path.isfile(file_path): # If file exist. Otherwise ignore
            print "Hashing %s" % file_name
            new_ed2k = file_manager.get_ed2k(file_path)
            if new_ed2k == ed2k:
                print "File integrity confirmed." 
                self.mydb.update_job(file_name)
            else:
                print "File have changed"
                self.mydb.delete_job(file_name)
                file_manager.check_file(self.mydb, self.connect, file_path)  
            self.update_job_lib()
            self.GUI.update_entry(fid, last_checked = self.all_job[file_name]['last_checked'])
        else:
            print "Rehash: File not found"
        
        
    def showall(self):
        if self.show_all:
            print "Showing all files"   
        else:
            print "Showing only available files"
        self.reload_table() 
    
    def reload_table(self):
        
        if self.show_all:
            self.GUI.update_table(self.all_job)
        else:
            self.GUI.update_table(self.only_available_job)
        
        
    def update_job_lib(self):
        self.all_job = self.mydb.list_job()
        self.only_available_job = {}
        for dict in self.all_job.values():
            file_path = path.join(dict['folder'],dict['file_name'])
            if path.isfile(file_path):
                self.only_available_job[dict['file_name']] = dict
            else:
                pass
    
    def start(self):   
        self.GUI.start(self.all_job)
        # self.GUI.update_log()
        
    def monitor_command(self):
        sys.stdout = StdoutRedirector(self.msg_queue)
        self.mydb = database.Local_DB(self.db_path)
        
        while self.isRunning:
            time.sleep(0.1)
            self.parse_command()
        
    def monitor_log(self):
        sys.stdout = StdoutRedirector(self.msg_queue)
        while self.isRunning:
            time.sleep(.1)
            self.GUI.update_log()
        

        
class StdoutRedirector(object):
    def __init__(self,text_queue):
        self.text_queue = text_queue
        
    def write(self,string):
        self.text_queue.put(string)
        
        
def main():
    myp = Program()
    myp.start()

main()