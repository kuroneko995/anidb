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
        w = Listbox(myContainer1)
        z = Listbox(myContainer1)
        for i in range(1,50):
            w.insert(i,"zthis is fun"+str(i))
            z.insert(i,"this is not"+str(i))
        w.grid(row=1, column=1)
        z.grid(row=1, column=2)
        
        #scrollbar = Scrollbar(self.myContainer1)
        #scrollbar.pack( side = RIGHT, fill=Y )
            
        
		
root = Tk()
myapp = MyApp(root)  ### (2)
root.mainloop()      ### (3)