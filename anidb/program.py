import threading
import Queue
import time
import sys
import subprocess
from anidb import GUI
from anidb import database
from anidb import udp_api
from anidb import file_manager


class Program(object):
    def __init__(self, file_path = 'local_db.db', new = False):
     
        self.mydb = database.Local_DB(file_path, new)
        self.initial_db = self.mydb.list_job()
        self.mydb.close()
        self.db_path = file_path
        
        # Setting up queues
        self.msg_queue = Queue.Queue() # Queue for printing message to screen
        self.job_list_queue = Queue.Queue() # Queue to update table in GUI
        # Redirect stdout to msg_queue to be displayed in GUI
        sys.stdout = StdoutRedirector(self.msg_queue)
        self.command_queue = Queue.Queue()
        
        # Start GUI object
        self.GUI = GUI.GUI_window(self.msg_queue, self.job_list_queue, self.command_queue)
        self.isRunning = True
        self.thread1 = threading.Thread(target=self.monitor_log)
        self.thread1.start()
        self.thread2 = threading.Thread(target=self.monitor_command)
        self.thread2.start()
        
        
    def parse_command(self):
        '''Parse a command, which is a tuple of 2
        '''
        while self.command_queue.qsize():
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
                else: # Not recognized. Do nothing
                    pass
            except Queue.Empty:
                pass
                
    def open_folder(self,file_name):
        folder = self.mydb.get_info_filename(file_name)['folder'] 
        cmd = 'explorer "%s"' % folder.replace('/','\\')
        print "Opening folder: %s" % folder
        subprocess.Popen(cmd)    
        
    def connect_udp(self):
        self.connect = udp_api.UDP_Conn()
        self.connect.get_session()
     
    def scan_folder(self, file_path):
        ''' Scan folder. At the end return a full list of dictionaries 
        containing info of files in the localdb
        '''
        if file_path == None: # User press cancel or sth
            pass
        else:
            file_manager.scan_folder(self.mydb, self.connect, file_path)
            print "Adding files complete"
            a = self.mydb.list_job()
            # return file_path
            self.GUI.update_table(a)
            
            
    def start(self):
        
        
        self.GUI.start(self.initial_db)
        
    def monitor_command(self):
        sys.stdout = StdoutRedirector(self.msg_queue)
        self.mydb = database.Local_DB(self.db_path)
        
        while self.isRunning:
            time.sleep(0.1)
            self.parse_command()
        
        
    def monitor_log(self):
        sys.stdout = StdoutRedirector(self.msg_queue)
        while self.isRunning:
            time.sleep(1)
            self.GUI.update_log()
        

        
class StdoutRedirector(object):
    def __init__(self,text_queue):
        self.text_queue = text_queue
        
    def write(self,string):
        self.text_queue.put(string)
        