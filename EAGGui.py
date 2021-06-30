from tkinter import *
from tkinter import filedialog,messagebox
from EAG_analysis_class import *
import statistics
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

EagGui = Tk()

def file_path():
        global filepath
        filepath = StringVar()
        #Fetch the file path of the hex file browsed.
        if(filepath == ""):
            filepath = filedialog.askopenfilename( initialdir = os.getcwd() ,
                 title = "select a file", filetypes = [("Data files", "*.ASC")])
        else:
            filepath = filedialog.askopenfilename( initialdir=filepath,
                 title = "select a file", filetypes = [("Data files", "*.ASC")])

def generate():
        global loadedData
       #Validation of entry fields, if left empty.
        if filepath == "":
            messagebox.showinfo('Information','please select a file')
        else:
            filepathlabel.config(text=filepath)
            loadedData = EAGanalysis(filepath)

def slice_data():
    # slices the data by "AnalysisTimeFrame" input
    time_frame = int(AnalysisTimeFrame.get())
    loadedData.arrange_data(time_frame)
    loadedData.multi_indexing()
    B["state"] = DISABLED

def calculate_stability():
    #
    first_experiments = int(FirstExperimentNumber.get())
    second_experiments = int(SecondExperimentNumber.get())
    first_experiment_data=loadedData.values_only.loc[first_experiments].loc[1]
    second_experiment_data=loadedData.values_only.loc[second_experiments].loc[1]
    response_stability = statistics.mean(first_experiment_data.tolist()) \
        / statistics.mean(second_experiment_data.tolist())
    entry_Stability.configure(text=str(response_stability))

def plot_blanks():
    # gets the number of blank experiments and plots them
    blank_experiments = BlankExperimentsEntry.get()
    blank_experiments=blank_experiments.split(',')
    new_blank_experiments = []
    indeces_to_remove = []
    for j in range(0,len(blank_experiments)):
        if '-' in blank_experiments[j]:
            new_blank_experiments = new_blank_experiments + list(range(int(blank_experiments[j].split('-')[0]),int(blank_experiments[j].split('-')[1])+1))
            indeces_to_remove.append(j)
    for ele in sorted(indeces_to_remove, reverse = True):
        del blank_experiments[ele]
    blank_experiments = blank_experiments + new_blank_experiments
    fig = Figure(figsize = (5, 5))
    plot1 = fig.add_subplot(111)
    for i in blank_experiments:
        plot1.plot(loadedData.values_only.loc[int(i)].loc[1])
        plot1.set_title('Blank experiments', loc='center')
    plot1.legend(blank_experiments)
    canvas = FigureCanvasTkAgg(fig,master = EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 15, column = 1)

def plot_experiments_ch1():
    # gets the number of blank experiments and plots them
    experiments_ch1 = ExperimentsToAnalyzeEntry.get()
    experiments_ch1=experiments_ch1.split(',')
    new_experiments_ch1 = []
    indeces_to_remove = []
    for j in range(0,len(experiments_ch1)):
        if '-' in experiments_ch1[j]:
            new_experiments_ch1 = new_experiments_ch1 + list(range(int(experiments_ch1[j].split('-')[0]),int(experiments_ch1[j].split('-')[1])+1))
            indeces_to_remove.append(j)
    for ele in sorted(indeces_to_remove, reverse = True):
        del experiments_ch1[ele]
    experiments_ch1 = experiments_ch1 + new_experiments_ch1
    fig = Figure(figsize = (5, 5))
    plot1 = fig.add_subplot(111)
    for i in experiments_ch1:
        plot1.plot(loadedData.values_only.loc[int(i)].loc[1])
        plot1.set_title('Experiments channel 1', loc='center')
    plot1.legend(experiments_ch1)
    canvas = FigureCanvasTkAgg(fig,master = EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 15, column = 1)

def plot_experiments_ch2():
    # gets the number of blank experiments and plots them
    experiments_ch2 = ExperimentsToAnalyzeEntry.get()
    experiments_ch2=experiments_ch2.split(',')
    new_experiments_ch2 = []
    indeces_to_remove = []
    for j in range(0,len(experiments_ch2)):
        if '-' in experiments_ch2[j]:
            new_experiments_ch2 = new_experiments_ch2 + list(range(int(experiments_ch2[j].split('-')[0]),int(experiments_ch2[j].split('-')[1])+1))
            indeces_to_remove.append(j)
    for ele in sorted(indeces_to_remove, reverse = True):
        del experiments_ch2[ele]
    experiments_ch2 = experiments_ch2 + new_experiments_ch2
    fig = Figure(figsize = (5, 5))
    plot1 = fig.add_subplot(111)
    for i in experiments_ch2:
        plot1.plot(loadedData.values_only.loc[int(i)].loc[2])
        plot1.set_title('Experiments channel 2', loc='center')
    plot1.legend(experiments_ch2)
    canvas = FigureCanvasTkAgg(fig,master = EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 15, column = 1)

def subtract_blank():
    blank_experiments = BlankExperimentsEntry.get()
    blank_experiments=blank_experiments.split(',')
    new_blank_experiments = []
    indeces_to_remove = []
    for j in range(0,len(blank_experiments)):
        if '-' in blank_experiments[j]:
            new_blank_experiments = new_blank_experiments + list(range(int(blank_experiments[j].split('-')[0]),int(blank_experiments[j].split('-')[1])+1))
            indeces_to_remove.append(j)
    for ele in sorted(indeces_to_remove, reverse = True):
        del blank_experiments[ele]
    blank_experiments = blank_experiments + new_blank_experiments
    loadedData.average_blank(blank_experiments)
    loadedData.minus_blank()
    if not OffsetSampelsEntry.get():
        loadedData.offset()
    else:
        loadedData.offset(int(OffsetSampelsEntry.get()))
    SubstractBlankExperiments["state"] = DISABLED

def export_data_to_excel():
    temp_file_name = ExcelFileNameEntry.get()
    temp_file_name = "".join(i for i in temp_file_name if i not in "\/:*?<>|")
    loadedData.export_to_excel(temp_file_name + '.xlsx')
    excel_button["state"] = DISABLED

# canv = Canvas()
# canv.grid(row=0, column=0)
# img = ImageTk.PhotoImage(Image.open("sagol-logo-144.png"))
# canv.create_image(1, 1, anchor=NW, image=img)

# canv2 = Canvas()
# canv2.grid(row=0, column=4)
# img2 = ImageTk.PhotoImage(Image.open("python_logo.jpg"))
# canv2.create_image(1, 1, anchor=NW, image=img2)

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

PlotExperimentsCh1 = Button(text="Plot experiments channel 1", command=plot_experiments_ch1)
PlotExperimentsCh1.grid(row=7, column=2)

PlotExperimentsCh2 = Button(text="Plot experiments channel 2", command=plot_experiments_ch2)
PlotExperimentsCh2.grid(row=7, column=3)

BlankExperiments = Label(EagGui,text = "Blank Experiments:",font = ('Times 10'))
BlankExperiments.grid(row=8, column=0)
BlankExperimentsEntry = Entry(EagGui)
BlankExperimentsEntry.grid(row = 8, column = 1)

OffsetSampels = Label(EagGui,text = "# of sampels for offset:",font = ('Times 10'))
OffsetSampels.grid(row=9, column=0)
OffsetSampelsEntry = Entry(EagGui)
OffsetSampelsEntry.grid(row = 9, column = 1)

PlotBlankExperiments = Button(text="Plot blank", command=plot_blanks)
PlotBlankExperiments.grid(row=8, column=2)

SubstractBlankExperiments = Button(text="Subtract blank and offset", command=subtract_blank)
SubstractBlankExperiments.grid(row=9, column=2)

ExcelFileName = Label(EagGui,text = "Type excel file name (without .xlsx):",font = ('Times 10'))
ExcelFileName.grid(row=10, column=0)
ExcelFileNameEntry = Entry(EagGui)
ExcelFileNameEntry.grid(row = 10, column = 1)

excel_button = Button(EagGui, text="Export to excel", bg="green",command=export_data_to_excel)
excel_button.grid(row = 10, column = 2)

exit_button = Button(EagGui, text="Exit", bg="red",command=EagGui.destroy)
exit_button.grid(row = 20, column = 1)

EagGui.attributes("-topmost", True)
EagGui.title('EAG analysis GUI')


EagGui.mainloop()