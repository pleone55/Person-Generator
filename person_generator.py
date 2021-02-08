from tkinter import *
from tkinter.ttk import Combobox

#Data options
DATA_OPTIONS = [
    "Data Selection...",
    "State IDs",
    "Addresses",
    "Date of Births",
    "Heights and Weights"
]

class GUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("600x450")
        self.frame1 = Frame(self.master)
        self.frame1.pack(side=TOP)
        self.frame2 = Frame(self.master)
        self.frame2.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        #Create a label for the title
        self.label = Label(text = "Person Generator", pady = 10, width = 20)
        self.label.pack(side=TOP)
    
    def create_dropdown_list(self):
        #Create a string variable to hold the data set options
        self.default = StringVar(self.master)
        self.default.set(DATA_OPTIONS[0])
        
        #Create list of data sets to choose from
        self.cb = Combobox(self.master, values=DATA_OPTIONS)
        self.cb.current(0)
        self.cb.pack(side=LEFT, padx=30)
        self.cb.bind("<<ComboboxSelected>>", self.data_selection)
    
    def data_selection(self, event):
        selected = self.cb.get()
        
        #determine selected value
        if selected == "State IDs":
            StateID.create_entry_box(self)
            self.cb["state"] = "disabled"
            print("Generating pseudo-random State IDs")
        elif selected == "Addresses":
            DateOfBirth.create_entry_box(self)
            self.cb["state"] = "disabled"
            print("Generating pseudo-random Addresses")
        elif selected == "Date of Births" :
            print("Generating pseudo-random Date of Births")
        elif selected == "Heights and Weights":
            print("Generating pseudo-random Heights and Weights")
    
    def clearDataFields(self):
        self.generate.destroy()
        self.clear.destroy()
        self.number_to_generate.destroy()
        self.field_to_generate.destroy()
        self.cb["state"] = "normal"
        print("Data Fields Cleared")

class StateID(GUI):
    def __init__(self, master):
        super().__init__(master)
    
    def create_entry_box(self):
        self.generate = Button(self.master, text = "Generate")
        self.clear = Button(self.master, text = "Clear", command=self.clearDataFields)
        self.field_to_generate = Entry(fg="black", bg="white", width=40)
        self.number_to_generate = Entry(fg="black", bg="white", width=5)
        
        #pack to the window frame
        self.generate.pack(side="right", pady = 30)
        self.clear.pack(side="right", pady = 30)
        self.field_to_generate.pack(side=LEFT, pady = 40)
        self.number_to_generate.pack(side=LEFT, pady = 30)

class DateOfBirth(StateID):
    def __init__(self, master):
        super().__init__(master)

def main():
    root = Tk()
    root.title("Person Generator")
    gui = GUI(master = root)
    gui.create_dropdown_list()
    gui.mainloop()

if __name__=="__main__":
    main()