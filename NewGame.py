# File: NewGame.py
# Author: Quinn Leonard
#
# PySweeper new game GUI
# This file contains the Tkinter GUI for creating a new PySweeper game

from tkinter import *

# Default board parameters
DEFAULTS = (10, 10, 10)

# get_board_parameters()
# Function for loading a GUI for grabbing game parameters from the user
#
# Returns a tuple of ints in the form (width, height, bombs)
def get_board_parameters():

    # Initialize GUI Window
    window = Tk()
    window.title("New Game")
    window.geometry("300x150")
    window.resizable(width=False,height=False)
    window.configure(background="azure4")
    window.grid_anchor(N)

    # Title
    Label(window, background="azure4", text="New Game", font=("Arial", 16, "bold")).grid(row=0, columnspan=2)

    # Width
    Label(window, background="azure4", text="Board Width: ").grid(row=1)
    widthBox = Spinbox(window, background="azure2", from_=1, to=100, width=10, textvariable=StringVar(value="10"))
    widthBox.grid(row=1,column=1)

    # Height
    Label(window, background="azure4", text="Board Height: ").grid(row=2)
    heightBox = Spinbox(window, background="azure2", from_=1, to=100, width=10, textvariable=StringVar(value="10"))
    heightBox.grid(row=2,column=1)

    # Bombs
    Label(window, background="azure4", text="Mine Count: ").grid(row=3)
    bombBox = Spinbox(window, background="azure2", from_=0, to=10000, width=10, textvariable=StringVar(value="10"))
    bombBox.grid(row=3,column=1)

    # Initialize default values
    width, height, bombs = DEFAULTS
    valid = False
    errorText = StringVar()

    # get_board_parameters()
    # Callback function for the start button
    def on_start():
        nonlocal width, height, bombs, valid

        # Set width
        try:
            if int(widthBox.get()) in range(1,101):
                width = int(widthBox.get())
            else:
                errorText.set("Width must be an integer between 1 and 100") 
                return
        except:
            errorText.set("Width must be an integer between 1 and 100") 
            return       
        
        # Set height
        try:
            if int(heightBox.get()) in range(1,101):
                height = int(heightBox.get())
            else:
                errorText.set("Height must be an integer between 1 and 100") 
                return
        except:
            errorText.set("Height must be an integer between 1 and 100") 
            return         

        # Set bombs
        try:
            if int(bombBox.get()) in range(0, width*height):
                bombs = int(bombBox.get())
            else:
                errorText.set("Mine count must be an integer between 0 and " + str((width*height) - 1)) 
                return
        except:
            errorText.set("Mine count must be an integer between 0 and " + str((width*height) - 1)) 
            return      

        # If values set properly, close the window
        valid = True
        window.destroy()

    # Start button
    Button(window, background="azure3", text="Start Game", command=on_start).grid(row=4,columnspan=2)

    # Error label
    Label(window, background="azure4", textvariable=errorText, fg="red").grid(row=5,columnspan=2)

    window.mainloop()

    # If window closes with valid inputs, return them. Otherwise, return default parameters
    if valid:
        return width, height, bombs
    else:
        return DEFAULTS