import customtkinter as ck
import tkinter as tk
from PIL import Image, ImageTk
from stock_checker import check_stock
import time

from main import run_main

ck.set_appearance_mode("Dark")
ck.set_default_color_theme("dark-blue")

app = ck.CTk()
app.geometry("800x440")

frame = ck.CTkFrame(master=app)
frame.pack(pady=20, padx=60, fill="both", expand="True")

prevMessage = -1

def run_simulation():
    global prevMessage
    
    currSym = str(stockSymbol.get())
    currIter = int(iterEntry.get())
    
    if prevMessage != -1:
        prevMessage.destroy()
        
    if check_stock(currSym) and currIter >= 2:
        
        print("running")
        successLabel = ck.CTkLabel(master=frame, 
                                   text="Your simualtion is complete, chart and analysis \n are in their respective folders.",
                                   font=("Ubuntu", 20),
                                   text_color="green")
        successLabel.pack(pady=12, padx=10)
        prevMessage = successLabel
        run_main(currSym, currIter)
    else:
        print("incorrect")
        failLabel = ck.CTkLabel(master=frame,
                                text= "Ticker is Invalid or iteration is less than 2",
                                font=("Ubuntu", 20),
                                text_color="red")
        failLabel.pack(pady=12, padx=10)
        prevMessage = failLabel

# top label
label = ck.CTkLabel(master=frame, text="Monte Carlo Stock Simulation", font=("Ubuntu", 25))
label.pack(pady=12, padx=10)


# symbol entry
stockSymbol = ck.CTkEntry(master=frame, placeholder_text="Enter Nasdaq Ticker Symbol", font=("Ubuntu", 8))
stockSymbol.pack(pady=12, padx=10)

#interation entry
iterEntry = ck.CTkEntry(master=frame, placeholder_text="Enter # of iterations", font=("Ubuntu", 8))
iterEntry.pack(pady=12, padx=10)

#submission button
button = ck.CTkButton(master=frame, text="Generate simulation", command=run_simulation)
button.pack(pady=12, padx = 10)


app.mainloop()
