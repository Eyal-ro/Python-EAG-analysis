from tkinter import *
from tkinter import filedialog,messagebox
import statistics
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

EagGui = Tk()



Browsebutton = Button(EagGui,width = 15,text= "BROWSE",command = file_path)
Browsebutton.grid(row = 1, column = 1)

Generatebutton = Button(EagGui,text="Upload file",command = generate)
Generatebutton.grid(row = 2, column = 1)

filepathlabel = Label(EagGui,text = "Data file path:",font = ('Times 10'))
filepathlabel.grid(row = 3, column = 1)

AnalysisTimeFrameLabel = Label(EagGui,text = "Select analysis time frame (in seconds):",font = ('Times 10'))
AnalysisTimeFrameLabel.grid(row = 4, column = 0)

AnalysisTimeFrame = Entry(EagGui)
AnalysisTimeFrame.grid(row = 4, column = 1)

B = Button(text="Slice data", command=slice_data)
B.grid(row = 4, column = 2)

FirstExperiment = Label(EagGui,text = "Select first experiment #:",font = ('Times 10'))
FirstExperiment.grid(row = 5, column = 0)
FirstExperimentNumber = Entry(EagGui)
FirstExperimentNumber.grid(row = 5, column = 1)

SecondExperiment = Label(EagGui,text = "Select second experiment #:",font = ('Times 10'))
SecondExperiment.grid(row = 6, column = 0)
SecondExperimentNumber = Entry(EagGui)
SecondExperimentNumber.grid(row = 6, column = 1)

StabilityButton = Button(text="Compute", command=calculate_stability)
StabilityButton.grid(row=6, column=2)

label_StabilityButton = Label(EagGui, text="Response stability: ")
label_StabilityButton.grid(row=6, column=3)

entry_Stability = Label(EagGui, width=15, height=1, bg="light grey")
entry_Stability.grid(row=6, column=4)

ExperimentsToAnalyze = Label(EagGui,text = "Experiments to analyze:",font = ('Times 10'))
ExperimentsToAnalyze.grid(row=7, column=0)
ExperimentsToAnalyzeEntry = Entry(EagGui)
ExperimentsToAnalyzeEntry.grid(row = 7, column = 1)

BlankExperiments = Label(EagGui,text = "Blank Experiments:",font = ('Times 10'))
BlankExperiments.grid(row=8, column=0)
BlankExperimentsEntry = Entry(EagGui)
BlankExperimentsEntry.grid(row = 8, column = 1)

PlotBlankExperiments = Button(text="Plot blank", command=plot_blanks)
PlotBlankExperiments.grid(row=8, column=2)


exit_button = Button(EagGui, text="Exit", bg="red",command=EagGui.destroy)
exit_button.grid(row = 20, column = 1)

EagGui.attributes("-topmost", True)
EagGui.title('EAG analysis GUI')


EagGui.mainloop()