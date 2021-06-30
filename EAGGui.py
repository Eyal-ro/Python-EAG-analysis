
from tkinter import *


EagGui = Tk()

Browsebutton = Button(EagGui, width=15, text="Browse")
Browsebutton.grid(row=1, column=1)
filepathlabel = Label(EagGui, text="Data file path:", font=('Times 10'))
filepathlabel.grid(row=3, column=1)
Generatebutton = Button(EagGui, text="Upload file")

EagGui.mainloop()

