from Tkinter import * ### (1)


class MyApp:
    def __init__(self, parent, number = 4):
        self.myContainer1 = Frame(parent, height = 400, width = 100)
        self.myContainer1.pack()
        
        # for i in range(0,4):
            # myButton = Button(self.myContainer1, text="Goodbye!"+str(i)) ### (4)
            # myButton.pack()	
            # myButton.grid(row=i, column = 1)
            # myButton2 = Button(self.myContainer1, text = "Hello" + str(i))
            # myButton2.pack()
            # myButton2.grid(row = i, column = 2)
        myscroll = Scrollbar(parent)
        myscroll.pack(side = RIGHT, fill = Y)    
            
        w = Listbox(self.myContainer1, yscrollcommand = myscroll.set)
        z = Listbox(self.myContainer1, yscrollcommand = myscroll.set)
        for i in range(1,50):
            w.insert(i,"zthis is fun"+str(i))
            z.insert(i,"this is not"+str(i))
        
        w.pack()
        z.pack()
        w.grid(row=1, column=1)
        z.grid(row=1, column=2)
        
        myscroll.config( command = w.yview )
        
       
            
        
		
root = Tk()
myapp = MyApp(root)  ### (2)
root.mainloop()      ### (3)

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