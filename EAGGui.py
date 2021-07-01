
from GUI_helper_functions import *
from tkinter import messagebox
import os


TESTING = True


def file_path():
    global filepath, loadedData
    filepath = StringVar()
    # Fetch the file path of the hex file browsed.
    if(filepath == ""):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title="select a file",
                                              filetypes=[("Data files",
                                                          "*.ASC")])
    else:
        filepath = filedialog.askopenfilename(initialdir=filepath,
                                              title="select a file",
                                              filetypes=[("Data files",
                                                          "*.ASC")])
    loadedData = EAGanalysis(filepath)


def slice_data(AnalysisTimeFrame, SlicedData, testing=None):
    # if testing!=None:
    #     loadedData=testing
    # slices the data by "AnalysisTimeFrame" input
    time_frame = AnalysisTimeFrame.get()
    if not time_frame.isdecimal():
        mb.showerror(
            "Error", "The analysis time frame must only contain numbers")
    time_frame = int(AnalysisTimeFrame.get())
    loadedData.arrange_data(time_frame)
    loadedData.transpose()
    loadedData.multi_indexing()
    SlicedData["state"] = DISABLED


def calculate_stability_1(SubstractBlankExperiments, FirstExperimentNumber1, SecondExperimentNumber1,entry_Stability):

    if SubstractBlankExperiments["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be analyzed first. Please press the button 'Subtract blank and offset' ")
    if SubstractBlankExperiments["state"] == DISABLED:
        if not FirstExperimentNumber1.get().isdecimal(
                ) or not SecondExperimentNumber1.get().isdecimal():
            mb.showerror(
                "Error", "The input must only contain numbers")
        first_experiments = int(FirstExperimentNumber1.get())
        second_experiments = int(SecondExperimentNumber1.get())

        loadedData.calculate_stability(first_experiments, second_experiments)

        response_stability = loadedData.response_stability1

        entry_Stability.configure(text=str(response_stability))

def calculate_stability_2(SubstractBlankExperiments, FirstExperimentNumber2, SecondExperimentNumber2,entry_Stability):

    if SubstractBlankExperiments["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be analyzed first. Please press the button 'Subtract blank and offset' ")
    if SubstractBlankExperiments["state"] == DISABLED:
        if not FirstExperimentNumber2.get().isdecimal(
                ) or not SecondExperimentNumber2.get().isdecimal():
            mb.showerror(
                "Error", "The input must only contain numbers")
        first_experiments = int(FirstExperimentNumber2.get())
        second_experiments = int(SecondExperimentNumber2.get())

        loadedData.calculate_stability(first_experiments, second_experiments)

        response_stability = loadedData.response_stability2

        entry_Stability.configure(text=str(response_stability))

def plot_blanks(SlicedData, BlankExperimentsEntry, EagGui):
    # gets the number of blank experiments and plots them
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    global blank_experiments
    blank_experiments = BlankExperimentsEntry.get()
    blank_experiments = pharse_experiments_input(blank_experiments)
    fig1, fig2 = plot_blank_experiments_data(blank_experiments, loadedData)
    canvas1 = FigureCanvasTkAgg(fig1, master=EagGui)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=15, column=1)
    canvas2 = FigureCanvasTkAgg(fig2, master=EagGui)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=15, column=2)


def plot_experiments_ch1(SlicedData, ExperimentsToAnalyzeEntry, EagGui):
    # gets the number of blank experiments and plots them
    global experiments_ch1
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_ch1 = ExperimentsToAnalyzeEntry.get()
    experiments_ch1 = pharse_experiments_input(experiments_ch1)
    fig = plot_experiments_data(experiments_ch1, loadedData,1)
    canvas = FigureCanvasTkAgg(fig, master=EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row=15, column=1)


def plot_experiments_ch2(SlicedData, ExperimentsToAnalyzeEntry, EagGui):
    # gets the number of blank experiments and plots them
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_ch2 = ExperimentsToAnalyzeEntry.get()
    experiments_ch2 = pharse_experiments_input(experiments_ch2)
    fig = plot_experiments_data(experiments_ch2, loadedData,2)
    canvas = FigureCanvasTkAgg(fig, master=EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row=15, column=1)


def subtract_blank(SlicedData, BlankExperimentsEntry, OffsetSampelsEntry, 
                    SubstractBlankExperiments):
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")

    blank_experiments = BlankExperimentsEntry.get()
    blank_experiments = pharse_experiments_input(blank_experiments)
    loadedData.average_blank(blank_experiments)
    loadedData.minus_blank()
    if not OffsetSampelsEntry.get():
        loadedData.offset()
    else:
        loadedData.offset(int(OffsetSampelsEntry.get()))
    SubstractBlankExperiments["state"] = DISABLED


def export_data_to_excel(SlicedData, ExcelFileNameEntry, excel_button):
    global file_dir, temp_file_name
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")

    temp_file_name = ExcelFileNameEntry.get()
    temp_file_name = "".join(i for i in temp_file_name if i not in "\/:*?<>|")
    file_dir = filedialog.askdirectory()
    loadedData.prism_ready()
    loadedData.export_to_txt(file_dir + '/' + temp_file_name + '_channel_1.txt',
                             file_dir + '/' + temp_file_name + '_channel_2.txt')
    loadedData.export_to_excel(file_dir + '/' + temp_file_name + '.xlsx')
    excel_button["state"] = DISABLED


def remove_experiments_from_data(SlicedData, ExperimentsToRemoveEntry,
                                  RemovesExperiments):
    global experiments_to_remove
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")

    experiments_to_remove = ExperimentsToRemoveEntry.get()
    experiments_to_remove = pharse_experiments_input(experiments_to_remove)
    # print(loadedData.offset_1)
    loadedData.offset_1 = loadedData.offset_1.drop(
        experiments_to_remove, axis=0)
    loadedData.offset_2 = loadedData.offset_2.drop(
        experiments_to_remove, axis=0)
    RemovesExperiments["state"] = DISABLED


def main():
    EagGui = Tk()

    Browsebutton = Button(EagGui, width=15, text="Upload file", command=file_path)
    EagGui.update()
    Browsebutton.grid(row=1, column=1)

    AnalysisTimeFrameLabel = Label(
        EagGui, text="Select analysis time frame (in seconds):", font=(
            'Times 10'))
    AnalysisTimeFrameLabel.grid(row=4, column=0)

    AnalysisTimeFrame = Entry(EagGui)
    AnalysisTimeFrame.grid(row=4, column=1)

    SlicedData = Button(text="Slice data")
    SlicedData.configure(
        command=lambda
        AnalysisTimeFrame=AnalysisTimeFrame, SlicedData=SlicedData:
            slice_data(AnalysisTimeFrame, SlicedData))
    SlicedData.grid(row=4, column=2)

    FirstExperiment = Label(
        EagGui, text="Select first experiment # - channel 1:", font=('Times 10'))
    FirstExperiment.grid(row=5, column=0)
    FirstExperimentNumber1 = Entry(EagGui)
    FirstExperimentNumber1.grid(row=5, column=1)

    SecondExperiment = Label(
        EagGui, text="Select last experiment # - channel 1:", font=('Times 10'))
    SecondExperiment.grid(row=6, column=0)
    SecondExperimentNumber1 = Entry(EagGui)
    SecondExperimentNumber1.grid(row=6, column=1)

    entry_Stability = Label(EagGui, width=15, height=1, bg="light grey")
    entry_Stability.grid(row=6, column=4)

    StabilityButton = Button(
        text="Compute", command=lambda
        SlicedData=SlicedData, FirstExperimentNumber1=FirstExperimentNumber1,
        SecondExperimentNumber1=SecondExperimentNumber1,
        entry_Stability=entry_Stability:
    calculate_stability_1(
        SlicedData, FirstExperimentNumber1,
        SecondExperimentNumber1, entry_Stability))
    StabilityButton.grid(row=6, column=2)
    # SlicedData = Button(text="Slice data")
    # SlicedData.configure(command=lambda AnalysisTimeFrame=AnalysisTimeFrame,
    #                                    SlicedData=SlicedData: slice_data(AnalysisTimeFrame, SlicedData))
    # SlicedData.grid(row=7, column=7)

    label_StabilityButton = Label(EagGui, text="Response stability: ")
    label_StabilityButton.grid(row=6, column=3)

    ExperimentsToAnalyze = Label(
        EagGui, text="Experiments to analyze:", font=('Times 10'))
    ExperimentsToAnalyze.grid(row=7, column=0)
    ExperimentsToAnalyzeEntry = Entry(EagGui)
    ExperimentsToAnalyzeEntry.grid(row=7, column=1)

    PlotExperimentsCh1 = Button(
        text="Plot experiments channel 1", command=
        lambda SlicedData=SlicedData,
        ExperimentsToAnalyzeEntry=ExperimentsToAnalyzeEntry,
        EagGui=EagGui:
        plot_experiments_ch1(SlicedData, ExperimentsToAnalyzeEntry, EagGui))
    PlotExperimentsCh1.grid(row=7, column=2)

    PlotExperimentsCh2 = Button(
        text="Plot experiments channel 2", command
        =lambda SlicedData=SlicedData,
        ExperimentsToAnalyzeEntry=ExperimentsToAnalyzeEntry,
        EagGui=EagGui:
        plot_experiments_ch2(SlicedData, ExperimentsToAnalyzeEntry, EagGui))
    PlotExperimentsCh2.grid(row=7, column=3)

    BlankExperiments = Label(
        EagGui, text="Blank Experiments:", font=('Times 10'))
    BlankExperiments.grid(row=8, column=0)
    BlankExperimentsEntry = Entry(EagGui)
    BlankExperimentsEntry.grid(row=8, column=1)

    OffsetSampels = Label(
        EagGui, text="# of sampels for offset:", font=('Times 10'))
    OffsetSampels.grid(row=9, column=0)
    OffsetSampelsEntry = Entry(EagGui)
    OffsetSampelsEntry.grid(row=9, column=1)

    PlotBlankExperiments = Button(text="Plot blank",
                                  command=lambda SlicedData=SlicedData,
                                  BlankExperimentsEntry=BlankExperimentsEntry,
                                  EagGui=EagGui: plot_blanks(
                                      SlicedData,
                                      BlankExperimentsEntry, EagGui))
    PlotBlankExperiments.grid(row=8, column=2)

    SubstractBlankExperiments = Button(
        text="Subtract blank and offset")
    SubstractBlankExperiments.configure(command=lambda SlicedData=SlicedData,
                                        BlankExperimentsEntry=
                                        BlankExperimentsEntry,
                                        OffsetSampelsEntry=OffsetSampelsEntry,
                                        SubstractBlankExperiments=
                                        SubstractBlankExperiments:
                                            subtract_blank(
                                                SlicedData,
                                                BlankExperimentsEntry,
                                                OffsetSampelsEntry,
                                                SubstractBlankExperiments))
    SubstractBlankExperiments.grid(row=9, column=2)

    ExperimentsToRemove = Label(
        EagGui, text="Experiments to remove from data:", font=('Times 10'))
    ExperimentsToRemove.grid(row=10, column=0)
    ExperimentsToRemoveEntry = Entry(EagGui)
    ExperimentsToRemoveEntry.grid(row=10, column=1)

    RemovesExperiments = Button(
        text="Remove specified experiments")
    RemovesExperiments.configure(command=lambda SlicedData=SlicedData,
                                 ExperimentsToRemoveEntry=
                                 ExperimentsToRemoveEntry,
                                 RemovesExperiments=RemovesExperiments:
                                     remove_experiments_from_data(
                                         SlicedData,
                                         ExperimentsToRemoveEntry,
                                         RemovesExperiments))
    RemovesExperiments.grid(row=10, column=2)

    ExcelFileName = Label(
        EagGui, text=
        "Type excel file name (without .xlsx):", font=('Times 10'))
    ExcelFileName.grid(row=11, column=0)
    ExcelFileNameEntry = Entry(EagGui)
    ExcelFileNameEntry.grid(row=11, column=1)

    excel_button = Button(
        EagGui, text="Export to excel", bg="green")
    excel_button.configure(command=lambda SlicedData=SlicedData,
                           ExcelFileNameEntry=ExcelFileNameEntry,
                           excel_button=excel_button:
                               export_data_to_excel(
                                   SlicedData,
                                   ExcelFileNameEntry, excel_button))
    excel_button.grid(row=11, column=2)

    exit_button = Button(EagGui, text="Exit", bg="red", command=EagGui.destroy)
    exit_button.grid(row=20, column=1)

    EagGui.attributes("-topmost", True)
    EagGui.title('EAG analysis GUI')
    # EagGui.attributes('-fullscreen',True)

    EagGui.mainloop()


if __name__ == "__main__":
    main()


