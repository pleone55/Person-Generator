<<<<<<< HEAD
import pandas
import numpy
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
import random
import sys
from multiprocessing.connection import Listener, Client
from keys import *
import threading

#Data options
DATA_OPTIONS = [
    "State Selection...",
    "Alaska",
    "Arizona",
    "California",
    "Colorado",
    "Hawaii",
    "Idaho",
    "Montana",
    "New Mexico",
    "Nevada",
    "Oregon",
    "Utah",
    "Washington",
    "Wyoming"
]

#Headers
HEADING = ["NUMBER", "STREET", "UNIT", "CITY", "DISTRICT", "REGION", "POSTCODE"]

#Main Class for Desktop Application
class GUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.answer_var = IntVar()          #will be used to hold the int value of the user input number to generate
        self.frame1 = Frame(self.master)
        self.frame1.pack(side=TOP)
        
        #wrappers to separate the sections for state selection, data, and content generator
        self.wrapper1 = LabelFrame(self.master, text="State Select")
        self.wrapper2 = LabelFrame(self.master, text="Data List")
        self.wrapper3 = LabelFrame(self.master, text="State Content")
        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
        
        #Create a label for the title
        self.label = Label(text = "Person Generator", pady = 10, width = 60)
        self.label.pack(in_=self.frame1, side=TOP)
        
        #Tree to hold the values of the addresses to be listed on the application
        self.my_tree = Treeview(self.wrapper2)
    
    def number_data_from_csv(self):
        """Function fills out the appropriate data fields after reading the csv file provided"""
        col_list = ["input_state", "input_number_to_generate"]
        df = pandas.read_csv(sys.argv[1], skipinitialspace=True, usecols=col_list)
        
        #insert the value from the csv file into the entry box for the number of addresses to generate
        self.number_to_generate.insert(END, int(df["input_number_to_generate"].values))
        self.number_to_generate["state"] = "disabled"
        
    def create_entry_box(self):
        """Function determines whether user provides their own csv file to fill out the appropriate data fields of the application.
            If no csv file provided user selects the state and number to generate"""
        self.generate = Button(self.master, text = "Generate", command=self.generate_data_set, width=15)
        self.clear = Button(self.master, text = "Clear", command=self.clearDataFields, width=15)
        self.number_to_generate = Entry(self.master, justify=CENTER, fg="black", bg="white", width=15)
        
        #pack to the window frame
        self.generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10, padx=5)
        self.clear.pack(in_=self.wrapper1, side=RIGHT, pady=10, padx=5)
        self.number_to_generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10)
        if len(sys.argv) > 1:
            self.number_data_from_csv()
    
    def state_data_from_csv(self, default):
        """Function sets the default state to the state from the input.csv"""
        #create a new array to hold the value of the state in the input.csv
        new_state_default = []
        col_list = ["input_state", "input_number_to_generate"]
        df = pandas.read_csv(sys.argv[1], skipinitialspace=True, usecols=col_list)
        #loop over the DATA_OPTIONS and compare its values with the value in the csv file
        for i in DATA_OPTIONS:
            if df['input_state'].values == i:
                new_state_default.append(i)
        self.default.set(new_state_default[0])

        self.cb = Combobox(self.master, justify="center", values=new_state_default, width=30)
        self.cb.current(0)
        self.cb.pack(in_=self.wrapper1, side=LEFT, padx=50, pady=10)
        self.cb.bind("<<ComboboxSelected>>", self.data_selection)
        self.cb["state"] = "disabled"
        
    def create_dropdown_list(self):
        """Function that creates a dropdown list of the states and fills the appropriate state field if input.csv is provided
        If no input.csv is provided dropdown displays the entire list of states."""
        self.default = StringVar(self.master)
        #create a regular dropbox with the values of the DATA_OPTIONS array
        self.default.set(DATA_OPTIONS[0])
        self.cb = Combobox(self.master, justify="center", values=DATA_OPTIONS, width=30)
        self.cb.current(0)
        self.cb.pack(in_=self.wrapper1, side=LEFT, padx=50, pady=10)
        self.cb.bind("<<ComboboxSelected>>", self.data_selection)
        
        #check if there is an argument on the command line
        if len(sys.argv) > 1:
            self.state_data_from_csv(self.default)
    
    def data_selection(self, event):
        """Function that determines the selected value from the DATA_OPTIONS array"""
        selected = self.cb.get()
        if selected:
            self.cb["state"] = "disabled"
            print("Hit clear to change states")
    
    def clearDataFields(self):
        """Clears the data fields to generate a new set of data"""
        self.cb["state"] = "normal"
        self.my_tree.delete(*self.my_tree.get_children())
        self.number_to_generate.delete(0, "end")
        self.t.destroy()
        self.send_city["state"] = "disabled"
        clear_message = messagebox.showinfo(title="State cleared", message="State field cleared. You may now select a new state")
        print("Data Fields Cleared You may now select a different state")
    
    def check_file_name(self, selected):
        """Function that checks the name that was selected from the dropbox and sets the filename"""
        filename = ''
        
        if selected == "Alaska":
            filename = 'ak.csv'
        elif selected == "Arizona":
            filename = 'az.csv'
        elif selected == "California":
            filename = 'ca.csv'
        elif selected == "Colorado":
            filename = 'co.csv'
        elif selected == "Hawaii":
            filename = 'hi.csv'
        elif selected == "Idaho":
            filename = 'id.csv'
        elif selected == "Montana":
            filename = 'mt.csv'
        elif selected == "New Mexico":
            filename = 'nm.csv'
        elif selected == "Nevada":
            filename = 'nv.csv'
        elif selected == "Oregon":
            filename = 'or.csv'
        elif selected == "Utah":
            filename = 'ut.csv'
        elif selected == "Washington":
            filename = 'wa.csv'
        elif selected == "Wyoming":
            filename = 'wy.csv'
        
        return filename
    
    def read_csv_file(self, filename):
        """Function counts the number of rows in the csv file, skips the headers and produces a random sample of addresses"""
        n = sum(1 for line in open(filename, encoding='UTF8'))
        s = int(self.answer_var)
        skip = sorted(random.sample(range(1, n+1), n-s))
        df = pandas.read_csv(filename, header=0, skiprows=skip)
        #select the specific headers to read from
        selected_data = df[HEADING]
        #error check to ensure no more than 500 rows is generated due to time constraints
        if len(selected_data) > 500:
            self.error_message = messagebox.showerror(title="Error", message="Data request too large. Please reduce the number of addresses to generate to less than 500")
            raise RuntimeError("Data request too large. Please reduce the number of addresses to generate")
            return
        
        #create a list of the data generated. select the columns 
        self.my_tree["column"] = list(selected_data.columns)
        self.my_tree["show"] = "headings"
        
        self.df_rows = selected_data.to_numpy().tolist()
        
        self.display_to_tree(s)
    
    def display_to_tree(self, s):
        """Function takes in the number of items to generate to pass to write_to_output_csv
            Loops over df_rows to insert to application"""
        for row in self.df_rows:
            self.my_tree.insert("", "end", values=row)
        
        self.my_tree.pack()
        
        self.write_to_output_csv(self.cb.get(), s, self.df_rows)
    
    def generate_data_set(self):
        """This function generates the data of pseudo-random addresses from the selected csv files. 
            The sample data is based upon the number the user entered to generate the data"""
        #get the selected state and number of items to generate
        selected = self.cb.get()
        self.answer_var = self.number_to_generate.get()
        
        #check that the entry box is not empty before running the application
        if self.answer_var == '':
            self.error_message = messagebox.showerror(title="Error", message="Please enter a number of pseudo-random addresses to generate")
            raise ValueError("Please enter a number of pseudo-random addresses to generate")
            return

        filename = self.check_file_name(selected)
        if filename == '':
            self.error_message = messagebox.showerror(title="Error", message="Please select a State to generate data")
            raise FileNotFoundError("Please select a State to generate data")
            return
        
        #Read the files, receive and send data to content generator
        self.read_csv_file(filename)
        print("Retreiving state paragraph from wikipedia...")
        self.receive_state_paragraph(selected)
        print("Paragraph from wikipedia received")
    
    def write_to_output_csv(self, state_selected, number_gen, data):
        """Function that writes the data to output.csv"""
        """Creates a dictionary that holds the data set"""
        filename = 'output.csv'
        df = {'input_state': state_selected, 'input_number_to_generate':number_gen, 'output_content_type': "addresses", 'output_content_value': data}
        df = pandas.DataFrame(df)
        df.to_csv(filename, sep=",", index=False, header=True)
        output_message = messagebox.showinfo(title="Data Exported", message=f"Data has been exported to {filename}")
    
    def receive_state_paragraph(self, selected):
        """Receive data from content generator"""
        c = Client(('localhost', PORT_1), authkey=AUTHKEY)
        c.send(selected)
        msg = c.recv()
        print(f"Person-Generator received {msg} as client.")
        self.t = Text(self.master, height=10, width=100)
        self.t.pack(in_=self.wrapper3)
        self.t.insert(END, msg)
        c.send('close')
        c.close()


"""
Casey's code for listening and returning city name below.
"""

states = {
    "Alaska": [],
    "Arizona": [],
    "California": [],
    "Colorado": [],
    "Hawaii": [],
    "Idaho": [],
    "Montana": [],
    "New Mexico": [],
    "Nevada": [],
    "Oregon": [],
    "Utah": [],
    "Washington": [],
    "Wyoming": []
}

state_codes = {
    "Alaska": "AK",
    "Arizona": "AZ",
    "California": "CA",
    "Colorado": "CO",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Montana": "MT",
    "New Mexico": "NM",
    "Nevada": "NV",
    "Oregon": "OR",
    "Utah": "UT",
    "Washington": "WA",
    "Wyoming": "WY"
}

def listen(port: int) -> None:
    """
    Listens for a connection. If one is established, generates content and sends it to the Client.
    :param port: Port number of the connection.
    """
    listener = Listener(("localhost", port), authkey=AUTHKEY)
    running = True
    while running:
        connection = listener.accept()
        while True:
            message = connection.recv()
            print(f"Person-Generator received: {message} as listener.")
            if message == "close":
                connection.close()
                break
            else:
                state = message

                results = get_city(state)
                print(f"Person-Generator sending: {results} as listener.")
                connection.send(results)
    return


def client(port: int, keyword: str) -> str:
    """
    Establishes a connection with a server, sending keywords and receives generated content.
    :param port: Port number of the connection.
    :param keywords: list of two keywords
    :returns: String of generated content.
    """
    connection = Client(("localhost", port), authkey=AUTHKEY)
    connection.send(keyword)
    message = connection.recv()
    print(f"Person-Generator received: {message} as client.")
    connection.send("close")
    connection.close()
    return message


def verify_state(state):
    """Verify state is an option."""
    if state not in states:
        return False
    else:
        return True

def get_filepath(state):
    """Gets filepath for the states csv file."""
    if not verify_state:
        return False
    else:
        filepath = state_codes[state].lower() + ".csv"
        return filepath

def get_cities(state):
    """Gets a list of cities from a csv file on the state."""
    filepath = get_filepath(state)
    if not filepath:
        return False

    with open(filepath) as infile:
        line = infile.readline()
        while line:
            # Convert line into list, grab city
            entry = line.split(",")
            try:
                city = entry[5]
            except:
                city = None
            if city:
                # Append if to list of cities if not already in list
                if city.upper() != "CITY":
                    states[state].append(city)
            # Move to next line
            line = infile.readline()

    return True

def get_city(state):
    """Gets a single city from the state."""
    if not states[state]:
        flag = get_cities(state)
        if not flag:
            return "City not found."
    
    max_index = len(states[state]) - 1

    random_index = random.randrange(max_index)

    return states[state][random_index]


#main loop
def main():

    root = Tk()
    root.title("Person Generator")
    gui = GUI(master = root)
    gui.create_dropdown_list()
    gui.create_entry_box()
    gui.mainloop()

if __name__=="__main__":

    # Start listening for connections in background
    listen_thread = threading.Thread(target=listen, name="Listener", args=[PORT_2])
    listen_thread.start()

=======
import csv
import pandas
import numpy
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
import random
import sys

#Data options
DATA_OPTIONS = [
    "State Selection...",
    "AK",
    "AZ",
    "CA",
    "CO",
    "HI",
    "ID",
    "MT",
    "NM",
    "NV",
    "OR",
    "UT",
    "WA",
    "WY"
]

#Headers
HEADING = ["NUMBER", "STREET", "UNIT", "CITY", "DISTRICT", "REGION", "POSTCODE"]

#Main Class for Desktop Application
class GUI(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.master.geometry("1450x900")
        self.answer_var = IntVar()          #will be used to hold the int value of the user input number to generate
        #create frame to hold everything
        self.frame1 = Frame(self.master)
        self.frame1.pack(side=TOP)
        
        #wrappers to separate the sections
        self.wrapper1 = LabelFrame(self.master, text="State Select")    #state and number to generate
        self.wrapper2 = LabelFrame(self.master, text="Data List")       #displays the data
        self.wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        self.wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        
        #Create a label for the title
        self.label = Label(text = "Person Generator", pady = 10, width = 60)
        self.label.pack(in_=self.frame1, side=TOP)
        
        #Tree to hold the values of the addresses to be listed on the application
        self.my_tree = Treeview(self.wrapper2)
    
    #Creates the entry box to select the states
    def create_entry_box(self):
        """If the user provides their own csv file to be read from the application will read the csv file for the number of addresses to generate
        and insert that number into the entry box. Entry box is disbaled to prevent altering of the number to generate"""
        """If no user csv is provided, then an empty Entry box is created instead"""
        if len(sys.argv) > 1:
            #list of columns to search for in the input.csv
            col_list = ["input_state", "input_number_to_generate"]
            df = pandas.read_csv(sys.argv[1], skipinitialspace=True, usecols=col_list)
            
            #create generate and clear buttons and entry field
            self.generate = Button(self.master, text = "Generate", command=self.generate_data_set, width=15)
            self.clear = Button(self.master, text = "Clear", command=self.clearDataFields, width=15)
            self.number_to_generate = Entry(self.master, justify=CENTER, fg="black", bg="white", width=15)
            
            #insert the value from the csv file into the entry box for the number of addresses to generate
            self.number_to_generate.insert(END, int(df["input_number_to_generate"].values))
            #disable the entry box to prevent alteration
            self.number_to_generate["state"] = "disabled"
            
            #pack to the window frame
            self.generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10, padx=5)
            self.clear.pack(in_=self.wrapper1, side=RIGHT, pady=10, padx=5)
            self.number_to_generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10)
        else:
            #if no csv file is provided create empty entry box and buttons
            self.generate = Button(self.master, text = "Generate", command=self.generate_data_set, width=15)
            self.clear = Button(self.master, text = "Clear", command=self.clearDataFields, width=15)
            self.number_to_generate = Entry(self.master, justify=CENTER, fg="black", bg="white", width=15)
            
            #pack to the window frame
            self.generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10, padx=5)
            self.clear.pack(in_=self.wrapper1, side=RIGHT, pady=10, padx=5)
            self.number_to_generate.pack(in_=self.wrapper1, side=RIGHT, pady = 10)
    
    #Creates a dropdown list of the states to select from. Determines if user provided csv file is given
    def create_dropdown_list(self):
        """Function that creates a dropdown box using ComboBox. If user provides their own csv file, the file is read searching the headers provided to us by the TA.
        Creates a new array of the state that is provided by the input.csv and sets the default of that index to initial value of the dropdown box. If no user input.csv is provided
        then the default is set to the 0 index of the DATAOPTIONS array where the user can select the state they wish to generate addresses from"""
        #Create a string variable to hold the data set options
        self.default = StringVar(self.master)
        #create a new array to hold the value of the state in the input.csv
        new_state_default = []
        #check if there is an argument on the command line
        if len(sys.argv) > 1:
            #column list to check for in the csv file
            col_list = ["input_state", "input_number_to_generate"]
            #read the file
            df = pandas.read_csv(sys.argv[1], skipinitialspace=True, usecols=col_list)
            #loop over the DATA_OPTIONS and compare its values with the value in the csv file
            for i in DATA_OPTIONS:
                if df['input_state'].values == i:
                    #append to the array
                    new_state_default.append(i)
                    #set as the default of the dropbox
            self.default.set(new_state_default[0])
            #Create list of data sets to choose from
            self.cb = Combobox(self.master, justify="center", values=new_state_default, width=30)
            #set the current value to the value of the array
            self.cb.current(0)
            self.cb.pack(in_=self.wrapper1, side=LEFT, padx=50, pady=10)
            self.cb.bind("<<ComboboxSelected>>", self.data_selection)
            #disable the dropbox
            self.cb["state"] = "disabled"
            
        else:
            #create a regular dropbox with the values of the DATA_OPTIONS array
            self.default.set(DATA_OPTIONS[0])
            #Create list of data sets to choose from
            self.cb = Combobox(self.master, justify="center", values=DATA_OPTIONS, width=30)
            self.cb.current(0)
            self.cb.pack(in_=self.wrapper1, side=LEFT, padx=50, pady=10)
            self.cb.bind("<<ComboboxSelected>>", self.data_selection)
    
    #Function that determines the selected value from the DATA_OPTIONS array and disables the dropbox until cleared to start over
    def data_selection(self, event):
        selected = self.cb.get()
        
        #determine selected value
        if selected:
            self.cb["state"] = "disabled"
            print("Hit clear to change states")
    
    #Clears the data fields to generate a new set of data
    def clearDataFields(self):
        self.cb["state"] = "normal"
        #clears the tree list of data 
        self.my_tree.delete(*self.my_tree.get_children())
        #clear entry box
        self.number_to_generate.delete(0, "end")
        #message that displays showing the data was cleared
        clear_message = messagebox.showinfo(title="State cleared", message="State field cleared. You may now select a new state")
        print("Data Fields Cleared You may now select a different state")
    
    #Function that checks the name that was selected from the dropbox and sets the filename
    def check_file_name(self, selected):
        selected = self.cb.get()
        filename = ''
        
        if selected == "AK":
            filename = 'ak.csv'
        elif selected == "AZ":
            filename = 'az.csv'
        elif selected == "CA":
            filename = 'ca.csv'
        elif selected == "CO":
            filename = 'co.csv'
        elif selected == "HI":
            filename = 'hi.csv'
        elif selected == "ID":
            filename = 'id.csv'
        elif selected == "MT":
            filename = 'mt.csv'
        elif selected == "NM":
            filename = 'nm.csv'
        elif selected == "NV":
            filename = 'nv.csv'
        elif selected == "OR":
            filename = 'or.csv'
        elif selected == "UT":
            filename = 'ut.csv'
        elif selected == "WA":
            filename = 'wa.csv'
        elif selected == "WY":
            filename = 'wy.csv'
        
        return filename
    
    #Function that generates the set of data
    def generate_data_set(self):
        """This function generates the data of pseudo-random addresses from the selected csv files using pandas. The range is based off the beginning of the file, excluding the header
        until it reaches the end of the file. The sample data is based upon the number the user entered to generate the data"""
        #get the selected state
        selected = self.cb.get()
        #set the number of addresses to generate
        self.answer_var = self.number_to_generate.get()
        #check that the entry box is not empty before running the application
        if self.answer_var == '':
            self.error_message = messagebox.showerror(title="Error", message="Please enter a number of pseudo-random addresses to generate")
            raise ValueError("Please enter a number of pseudo-random addresses to generate")
            return
        #call the check_file_name function that determines the filename to read into
        filename = self.check_file_name(selected)
        #check that a state is selected
        if filename == '':
            self.error_message = messagebox.showerror(title="Error", message="Please select a State to generate data")
            raise FileNotFoundError("Please select a State to generate data")
            return
        #count the number of rows in the csv file selected summing by 1
        n = sum(1 for line in open(filename, encoding='UTF8'))
        #make self.answer a var to be used for the data sample
        s = int(self.answer_var)
        #skips the header of the csv file so that isnt selected in the random sample
        #the sample begins after the header and contniues to pick random addresses until the number provided by the user is reached
        skip = sorted(random.sample(range(1, n+1), n-s))
        #read the file
        df = pandas.read_csv(filename, header=0, skiprows=skip)
        #select the specific headers to read from
        selected_data = df[HEADING]
        #error check to ensure no more than 500 rows is generated due to time constraints
        if len(selected_data) > 500:
            self.error_message = messagebox.showerror(title="Error", message="Data request too large. Please reduce the number of addresses to generate to less than 500")
            raise RuntimeError("Data request too large. Please reduce the number of addresses to generate")
            return
        #create a list of the data generated. select the columns 
        self.my_tree["column"] = list(selected_data.columns)
        self.my_tree["show"] = "headings"
        
        #loop over the selected columns and add them to the headings of the tree
        for column in self.my_tree["column"]:
            self.my_tree.heading(column, text=column)
        
        #retreive the data of those columns
        df_rows = selected_data.to_numpy().tolist()
        
        #loop over the rows and insert into the tree
        for row in df_rows:
            self.my_tree.insert("", "end", values=row)
        
        self.my_tree.pack()
        
        #call the write_to_output_csv function to generate a csv file 
        self.write_to_output_csv(selected, self.answer_var, df_rows)
        print(selected_data)
    
    #Function takes the data outputted to the screen and writes to a csv file called output.csv
    def write_to_output_csv(self, state_selected, number_gen, data):
        filename = 'output.csv'
        #create a dictionary that hold the data set
        df = {'input_state': state_selected, 'input_number_to_generate':number_gen, 'output_content_type': "addresses", 'output_content_value': data}
        df = pandas.DataFrame(df)
        #write to csv file
        df.to_csv(filename, sep=",", index=False, header=True)
        output_message = messagebox.showinfo(title="Data Exported", message=f"Data has been exported to {filename}")

#main loop
def main():
    root = Tk()
    root.title("Person Generator")
    gui = GUI(master = root)
    gui.create_dropdown_list()
    gui.create_entry_box()
    gui.mainloop()

if __name__=="__main__":
>>>>>>> a7df2c5807447430621fae9f733511be230b127b
    main()