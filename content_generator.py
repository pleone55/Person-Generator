# Author: Casey Arndt
# Date: 28 February 2021

import sys, wikipedia, wikipediaapi, json, threading
from tkinter import *
from bs4 import BeautifulSoup
from multiprocessing.connection import Client, Listener
from keys import *


outfile = "output.csv"
FONT_SIZE = 11
FONT = "TkDefaultFont"
STATE_FILE = "states.json"


class GUI:
    def __init__(self, main):
        # Frame for input widgets
        self.input_frame = Frame(main)

        # Create label and input field for primary keyword
        self.primary_label = Label(self.input_frame, text="City Name", font=(FONT, FONT_SIZE))
        self.primary_input = Entry(self.input_frame, font=(FONT, FONT_SIZE))

        # Create label and input field for secondary keyword
        self.secondary_label = Label(self.input_frame, text="State Name", font=(FONT, FONT_SIZE))
        self.secondary_input = Entry(self.input_frame, font=(FONT, FONT_SIZE))

        # Create label and text box for output
        self.output_label = Label(main, text="Output", font=(FONT, FONT_SIZE))
        self.output_box = Text(main, font=(FONT, FONT_SIZE))

        # Buttons
        self.button_frame = Frame(main)
        self.content_button = Button(self.button_frame, text="Generate Content", \
            font=(FONT, FONT_SIZE), command=self.generate_content)
        self.save_button = Button(self.button_frame, text="Save Content", \
            font=(FONT, FONT_SIZE), command=self.save_content)

        self.place_widgets()


    def place_widgets(self):
        """
        Places widgets on the grid.
        """
        self.input_frame.grid(row=0, column=0, pady=20)
        self.primary_label.grid(row=0, column=0)
        self.primary_input.grid(row=1, column=0, padx=20)
        self.secondary_label.grid(row=0, column=1)
        self.secondary_input.grid(row=1, column=1, padx=20)

        self.output_label.grid(row=1, column=0, pady=10)
        self.output_box.grid(row=2, column=0)

        self.button_frame.grid(row=3, column=0, pady=20)
        self.content_button.grid(row=0, column=0, pady=10)
        self.save_button.grid(row=0, column=1, pady=10)


    def generate_content(self):
        """
        Generates content from a city name and a state name, placing it in output box.
        """
        city = self.primary_input.get()
        state = self.secondary_input.get()
        # Delete any content in output box before generating new content
        self.output_box.delete(0.0, "end")

        # Generate content
        if not city:
            city = client(PORT_2, state)
            self.primary_input.insert(0, city)

        output = generate_state_content(city, state)

        # Place output in output box
        self.output_box.insert(0.0, output)
        
        return

    def save_content(self):
        """
        Saves the content in the output box to csv file.
        """
        input_line = self.primary_input.get() + ';' + self.secondary_input.get()
        content = self.output_box.get("1.0", END).rstrip()

        write_output(outfile, input_line, content)

        return



def read_input(filepath: str) -> object:
    """
    Reads input from a csv file.
    :param filepath: File from which to read input.
    :returns: List
    """
    # Open file for reading, closing when done
    with open(filepath, "r") as infile:
        # Read line, discard header
        line = infile.readline()
        line = infile.readline().strip()


        return line

def verify_outfile():
    pass

def write_output(filepath: str, input:str, output: str) -> None:
    """
    Writes output to a file.
    :param filepath: Filepath of the output file.
    :param output: Output to be written to file.
    :returns: Nothing.
    """
    header = "input_keywords,output_content"
    line = input + ',' + "'" + output + "'\n"

    # Write header and line to file if it does not exist
    if not filepath:
        # Open file for writing
        with open(filepath, "w") as outfile:
            # Write header
            outfile.write(header + "\n")
            # Write input and output, seperated by comma
            outfile.write(line)
            return
    # Append line only if file already exists
    else:
        with open(filepath, "a") as outfile:
            outfile.write(line)
            return


def find_article(keyword: str) -> str:
    """
    Finds a wikipedia article matching a provided keyword. 
    :param keyword: Keyword to be searched for a matching wikipedia article.
    :returns: Wikipedia page object.
    """
    # Get list of possible matches
    pages = wikipedia.search(keyword)
    # Get page that correlates to first possible match
    try:
        page = wikipedia.page(pages[0], auto_suggest=False, redirect=True)
        return page.url[30:] # Removes https://en.wikipedia.org/wiki/ from url
    # In case no matches
    except: 
        return None


def find_paragraph(primary:str, secondary:str, content: list) -> str:
    """
    Searches a list of paragraphs of a wikipedia page for one containing two keywords.
    :param primary: First keyword.
    :param secondary: Second keyword.
    :param content: List of paragraphs of a wikipedia page.
    :returns: String of matching paragraph (if found).
    """
    output = None

    # Iterate over paragraphs
    for paragraph in content:
        # Convert each paragraph to lower case
        lower = paragraph.lower()
        # Check if paragraph contains both keywords
        if primary.lower() in lower and secondary.lower() in lower:
            output = paragraph.rstrip()
            break

    return output


def get_content(page: str) -> list:
    """
    Gets all of the content on a page of a wikipedia article.
    :param page: Page title of wikipedia page.
    :returns: List of paragraphs.
    """
    wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.HTML)
    page_py = wiki_wiki.page(page)
    content = page_py.text
    soup = BeautifulSoup(content, "html.parser")
    paragraphs = []
    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph.text)

    return paragraphs

def generate_content(primary: str, secondary: str) -> str:
    """
    Generates the content from two keywords.
    :param primary: Primary keyword
    :param secondary: Secondary keyword
    :returns: Content generated
    """
    # Get article
    article = find_article(primary)
    if not article:
        output = f"No article found matching: {primary}"
        return output
    
    # Get paragraph
    content = get_content(article)
    paragraph = find_paragraph(primary, secondary, content)
    if not paragraph:
        output = f"No paragraph found matching: {primary} & {secondary}"
        return output
    
    output = paragraph
    return output


def generate_state_content(city: str, state: str) -> str:
    """
    Generates the content from two keywords.
    :param primary: Primary keyword
    :param secondary: Secondary keyword
    :returns: Content generated
    """
    # Get article
    city_state = city + ", " + state
    article = find_article(city_state)
    if not article:
        output = f"No article found matching: {city_state}"
        return output
    
    # Get paragraph
    content = get_content(article)
    paragraph = find_paragraph(city, "", content)
    if not paragraph:
        output = f"No paragraph found matching: {city}"
        return output
    
    output = paragraph
    return output


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
            print(f"Content-Generator received: {message} as listener.")
            if message == "close":
                connection.close()
                break
            else:
                #states = load_json(STATE_FILE)
                #state = states[message]
                state = message
                results = generate_content(state, "")
                print(f"Content-Generator sending: {results} as listener.")
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
    print(f"Content-Generator received: {message} as client.")
    connection.send("close")
    connection.close()
    return message


def load_json(json_file):
    """
    Returns a dictionary version of a json file.
    """
    with open(json_file) as infile:
        json_dict = json.load(infile)

    return json_dict


def start_gui() -> None:
    """
    Starts graphical user interface.
    """    
    root = Tk()
    root.title("Content Generator")
    gui = GUI(root)
    root.mainloop()

    return   


def process_csv() -> None:
    """
    Attempts to process an input csv file.
    """
    # Get inputs
    infile = sys.argv[1]
    input_line = read_input(infile)
    keywords = [keyword for keyword in input_line.split(";")]
    # Verify inputs
    if len(keywords) < 2:
        print("Input file has incorrect format. Confirm that it has a header "
        "and next line follows the format: 'primary_keyword;secondary_keyword'")
        return

    output = generate_content(keywords[0], keywords[1])

    # write output to file
    write_output(outfile, input_line, output)
    return


if __name__ == "__main__":
    # Check args
    if len(sys.argv) < 2 or sys.argv[1] == '&':
        # Start listening for connections in background
        listen_thread = threading.Thread(target=listen, name="Listener", args=[PORT_1])
        listen_thread.start()
        
        start_gui()
        exit

    # Start as GUI
    elif sys.argv[1].upper() == "GUI":
        start_gui()
        exit

    # Process csv file
    else:
        process_csv()
        exit