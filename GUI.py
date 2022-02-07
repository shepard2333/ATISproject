from base64 import decode
from tkinter import *
import tkinter
import sys
import os

# Create an instance of tkinter window
win = Tk()
win.geometry("800x350")
win.title("AWOS tool")
def save_text():
   text_file = open("ICAO.txt", "w")
   text_file.write(my_text_box.get(1.0, END))
   text_file.close()

def save_text_decode_y():
    text_file = open("yn.txt", "w")
    text_file.write("y")
    text_file.close()

def save_text_decode_n():
    text_file = open("yn.txt", "w")
    text_file.write("n")
    text_file.close()

def save_text_taf_y():
    text_file = open("taf.txt", "w")
    text_file.write("y")
    text_file.close()

def save_text_taf_n():
    text_file = open("taf.txt", "w")
    text_file.write("n")
    text_file.close()

# Create label
l = Label(win, text = "Decode? Y/N")
l.pack()



decode1 = Button(win, text="decode", command=lambda:save_text_decode_y())
decode1.pack()

raw = Button(win, text="undecode", command=lambda:save_text_decode_n())
raw.pack()
save_text_taf_n()
taf = Button(win, text="includes TAF", command=lambda:save_text_taf_y())
taf.pack()



# Creating a text box widget
my_text_box = Text(win, height=1, width=10)
my_text_box.pack()
x = Label(win, text = "Input ICAO Code")
x.pack()

def run():
    os.system('python atis2.5.py')



# Create a button to save the text


save = Button(win, text="save", command=lambda:save_text())
save.pack()

a = Button(win, text="send to print",command=run)
a.pack()


def close_window():
    win.destroy()

button = tkinter.Button(text = "Finished", 
                   command = close_window)
button.pack()

win.mainloop()



