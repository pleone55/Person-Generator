# Person Generator

Person Generator Project for CS361 at Oregon State. 
Application gives the user a select number of states to choose from in order to generate pseudo-random addresses from that state based off the number provided by the user. Once the user hits generate, the output data is written to output.csv. Once the addresses are displayed on the screen, a request is made to Content Generator to receive the first paragrpah from Wikipedia about the state selected. The paragraph is displayed on the application for the user to view.

Instructions

To run Person Generator: 

py or python3 person_generator.py

A provided csv file from the user may be used as well to be read from. The input.csv file reads the first row only which contains the state to generator data for and the number of items.

To run:

py or python3 person_generator.py input.csv

To Run Content Generator:

py or python3 content_generator.py

This application, provided by my teammate, can be ran as an application or just as a server to receive the Wikipedia paragraph.

To run as server:

py or python3 content_generator.py &

Project is a desktop application using Tkinter
