from Tkinter import * ### (1)
import tkFileDialog
import ttk

class GUI_window:
    def __init__(self, msg_queue = None, job_list_queue=None, command_queue = None):
        self.msg_queue = msg_queue
        self.jobs = job_list_queue
        self.command_queue = command_queue
        
        
        # Set up the Frames
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.exitGUI)
        self.text_container = Frame(self.root,height=50)
        self.text_container.pack(side = BOTTOM, expand= False, fill=BOTH )
        self.main_container = Frame(self.root)
        self.main_container.pack(side=BOTTOM, expand=True, fill='both')
        self.button_container = Frame(self.root)
        self.button_container.pack(side=TOP, expand=False, fill=X)
        
        
        # Set up the TreeView 
        self.table = ttk.Treeview(self.main_container)
        self.table.configure(columns = 3)
        self.table["columns"]=("number","size","last_checked")
        
        # Columns in the TreeView
        self.table.heading("#0", text="Name")
        self.table.column("number", stretch=False, width = 30)
        self.table.heading("number", text="#",command=lambda: \
                     self.treeview_sort_column( "number", False))
        self.table.column("size", stretch=False,width =60)
        self.table.heading("size", text="Size (KB)",command=lambda: \
                     self.treeview_sort_column( "size", False))
        self.table.column("last_checked", stretch=False, width=120)
        self.table.heading("last_checked", text="Last checked",command=lambda: \
                     self.treeview_sort_column( "last_checked", False))
        
        # Set up scrollbar
        self.tableScrollbar = Scrollbar(self.main_container, orient="vertical", command = self.table.yview)
        self.tableScrollbar.pack(side= RIGHT, fill= Y)
        self.table.configure(yscrollcommand=self.tableScrollbar.set)
        self.table.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Set up buttons
        self.bOpenFolder = Button(self.button_container, text="Open Folder", command=self.open_folder)
        self.bReHash = Button(self.button_container, text="Rehash", command = self.rehash)
        self.bAddFiles = Button(self.button_container, text="Add Files", command = self.add_files)
        self.bConnectUDP = Button(self.button_container, text="Connect", command=self.connect_udp)
        self.bOpenFolder.pack(side=LEFT)
        self.bReHash.pack(side=LEFT)
        self.bAddFiles.pack(side=LEFT)
        self.bConnectUDP.pack(side=LEFT)
        # Set up logging text box
        self.log = Text(self.text_container, height =10)
        
        
        self.textScrollbar = Scrollbar(self.text_container, orient="vertical", command = self.log.yview)
        self.textScrollbar.pack(side= RIGHT, fill= Y)
        self.log.configure(yscrollcommand=self.textScrollbar.set)
        self.log.pack(fill=X, expand =False)
    
    def connect_udp(self):
        self.command_queue.put(("CONNECT",))
     
    def open_folder(self):
        fid = self.table.selection()[0]
        if not fid in self.table.get_children(''): # if a file not an anime selected
            
            file_name = unicode(self.table.item(fid,'text'))
            self.command_queue.put(("OPEN_FOLDER",file_name))
            # print self.command_queue
    

    
    def rehash(self):
        pass
        
    def add_files(self):
        # t = threading.Thread(target=self.add_files_thread, args=())
        # self.threads.append(t)
        # t.start()
        file_path = tkFileDialog.askdirectory(initialdir='C:\\')
        if file_path == None: # User press cancel or sth
            pass
        else:
            self.command_queue.put(("ADD_FILES", file_path))
            
        
    def update_table(self, list_job):
        for dict in list_job:
            if not self.table.exists(dict['fid']): # Update new files added
                #['anime_name', 'anime_episodes', 'epno', 'ep_name', 'fid']
                self.add_one_entry(dict['anime_name'], id=dict['fid'], ep_name=dict["file_name"], number=dict["epno"], 
                            size=dict['size'], last_checked=dict['last_checked'])
            
            # return file_path
        
        
    def add_one_entry(self, anime_name, id=None, ep_name="", number="", size="", last_checked=""):
        if not self.table.exists(anime_name): # Parent is non-empty and not exist
            self.table.insert("",0, iid=anime_name, text=anime_name, values=("","",last_checked))
        if not self.table.exists(id):
            self.table.insert(anime_name,0,iid=id,text=ep_name, values=(number, size, last_checked))
        self.sort_anime()
        self.sort_name()
        
    def start(self,job_list):
        for dict in job_list:
        #['anime_name', 'anime_episodes', 'epno', 'ep_name', 'fid', 'file_name', 'folder', 'last_checked']
            self.add_one_entry(dict['anime_name'], id=dict['fid'], ep_name=dict["file_name"], number=dict["epno"], 
                    size=dict['size'], last_checked=dict['last_checked'])
        
        # Sort items before starting
        self.sort_anime()
        self.sort_name()
        self.root.mainloop()

    def sort_anime(self):
        '''Sort episodes in each anime'''
        for item in self.table.get_children():
            self.treeview_sort_column("number",False, parent=item)
    
    def sort_name(self):
        l = [k for k in self.table.get_children()]
        l.sort()
        # rearrange items in sorted positions
        for index, k in enumerate(l):
            self.table.move(k, "", index)       
        
    def treeview_sort_column(self, col, reverse, parent =""):
        l = [(self.table.set(k, col), k) for k in self.table.get_children(parent)]
        l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.table.move(k, parent, index)

        # reverse sort next time
        self.table.heading(col, command=lambda: \
                   self.treeview_sort_column(col, not reverse))
    

    def update_log(self):
        while self.msg_queue.qsize():
            try:
                msg = self.msg_queue.get(0)
                self.log.insert('end',msg)
                self.log.see('end')
            except Queue.Empty:
                pass
        
    def exitGUI(self):
        self.command_queue.put(('EXIT',))
        self.root.quit()

        

# def main():
    # newGUI = GUI_window('local_db.db')
    # newGUI.start()
    
# main()