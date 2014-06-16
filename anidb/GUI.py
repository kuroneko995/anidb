from Tkinter import * ### (1)
import ttk

class GUI_window:
    def __init__(self, parent, number = 4):
        self.myContainer = Frame(parent)
        self.myContainer.pack(expand=True, fill=Y)
        self.parent = parent
       
        
        
        self.view = ttk.Treeview(self.myContainer)
        self.view.configure(columns = 3)
        self.view["columns"]=("one","two","three")
        self.myScrollbar = Scrollbar(self.myContainer, orient="vertical", command = self.view.yview)
        self.myScrollbar.pack(side= RIGHT, fill= Y)
        self.view.configure(yscrollcommand=self.myScrollbar.set)
        
        
        #map (lambda col : col.configure(yscrollcommand=myScrollbar.set,),columns)
       
        self.view.heading("one", text="Path")
        self.view.heading("two", text="CRC")
        self.view.heading("three", text="Episode number")
        
        id2 = self.view.insert("", 1, "dir2", text="Dir 2")
        self.view.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
        #self.view.resizable(width=True,height=True)    
        self.view.pack(side=LEFT, fill=BOTH, expand=True)
        
    def addSeries(self,series_name, location = "", CRC="", eps_number=0):
        self.view.insert("",0,iid=series_name, text=series_name,values=(location,CRC,eps_number))
        
    def addEpisode(self, series_name, location = "", CRC="", eps_number=0):
        self.view.insert(series_name,0,text="Episode " + str(eps_number),values=(location, CRC, eps_number))
    

	
#root = Tk()
#myapp = MyApp(root)  ### (2)

#for i in range(100):
 #   myapp.addEntry("Line "+str(i))
#root.mainloop()      ### (3)
"""


root = Tk()
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill=Y )

mylist = Listbox(root, yscrollcommand = scrollbar.set )
for line in range(100):
   mylist.insert(END, "This is line number " + str(line))

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()
"""