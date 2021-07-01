from GUI_helper_functions import *
from tkinter import messagebox
import os


def file_path():
    """
    Get file path from user and upload the data.

    Returns
    -------
    loadedData.
    """
    global filepath, loadedData
    filepath = StringVar()
    # Fetch the file path of the hex file browsed.
    if (filepath == ""):
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
    """
    Sliced and arrange the raw data.

    ----------
    AnalysisTimeFrame : input from user (in sec)
    SlicedData : Slice button status
    Returns
    -------
    sliced data.
    """
    # allows running tests in test_EAGGui.py file
    global loadedData
    if testing != None:
        loadedData = testing
    time_frame = AnalysisTimeFrame.get()
    if not time_frame.isdecimal():
        mb.showerror(
            "Error", "The analysis time frame must only contain numbers")
    time_frame = int(AnalysisTimeFrame.get())
    loadedData.arrange_data(time_frame)
    loadedData.transpose()
    loadedData.multi_indexing()
    SlicedData["state"] = DISABLED


def plot_blanks(SlicedData, BlankExperimentsEntry, EagGui):
    """
    Plot blank experiments.

    ----------
    BlankExperimentsEntry : Blank experimentrs numbers
    EagGui : the GUI
    Returns
    -------
    A figure into the GUI.
    """
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
    """
    Plot the experimnts on channel 1.

    ----------

    Returns
    -------
    A figure into the GUI.
    """
    global experiments_ch1
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_ch1 = ExperimentsToAnalyzeEntry.get()
    experiments_ch1 = pharse_experiments_input(experiments_ch1)
    fig = plot_experiments_data(experiments_ch1, loadedData, 1)
    canvas = FigureCanvasTkAgg(fig, master=EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row=15, column=1)


def plot_experiments_ch2(SlicedData, ExperimentsToAnalyzeEntry, EagGui):
    """
    Plot the experimnts on channel 2.

    ----------

    Returns
    -------
    A figure into the GUI.
    """
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_ch2 = ExperimentsToAnalyzeEntry.get()
    experiments_ch2 = pharse_experiments_input(experiments_ch2)
    fig = plot_experiments_data(experiments_ch2, loadedData, 2)
    canvas = FigureCanvasTkAgg(fig, master=EagGui)
    canvas.draw()
    canvas.get_tk_widget().grid(row=15, column=1)


def subtract_blank(SlicedData, BlankExperimentsEntry,
                   OffsetSampelsEntry, SubstractBlankExperiments):
    """
    Substract blank experiments and offset from data.

    ----------
    BlankExperimentsEntry : Number of blank experiments.
    OffsetSampelsEntry : Number of sumpels to offset.
    SubstractBlankExperiments : The button.

    Returns
    -------
    Data after blanks and offset substraction.

    """
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


def calculate_stability(SubstractBlankExperiments, FirstExperimentNumber1,
                        SecondExperimentNumber1,
                        entry_Stability, entry_Stability2):
    """
    Calculate the preperation stability.

    ----------
    SubstractBlankExperiments : Validation that the data was preprocessed
    FirstExperimentNumber1 : The first experiment.
    SecondExperimentNumber1 : The second experiment.
    entry_Stability : The place for the output
    entry_Stability2 : The place for the output

    Returns
    -------
    Stability values for both channels.

    """
    if SubstractBlankExperiments["state"] == NORMAL:
        mb.showerror(
            "Error",
            "Please press the button 'Subtract blank and offset' first")

    first_experiments = FirstExperimentNumber1.get()
    second_experiments = SecondExperimentNumber1.get()

    first_experiments = pharse_experiments_input(first_experiments)
    second_experiments = pharse_experiments_input(second_experiments)

    loadedData.calculate_stability(first_experiments, second_experiments)

    response_stability = loadedData.response_stability1
    response_stability_2 = loadedData.response_stability2

    entry_Stability.configure(text=str(response_stability))
    entry_Stability2.configure(text=str(response_stability_2))


def export_data_to_excel(SlicedData, ExcelFileNameEntry, excel_button):
    """
    Export the data to excel and txt.

    ----------
    ExcelFileNameEntry : file name from user input.
    excel_button : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
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


def remove_experiments_from_data(SlicedData, ExperimentsToRemoveEntry1,
                                 RemovesExperiments):
    """
    Remove specified experiments from data.
    ----------
    ExperimentsToRemoveEntry1 : experiments numbers to remove
    RemovesExperiments : the button
        DESCRIPTION.

    Returns
    -------
    None.

    """
    global experiments_to_remove
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_to_remove1 = ExperimentsToRemoveEntry1.get()
    experiments_to_remove1 = pharse_experiments_input(experiments_to_remove1)
    loadedData.offset_1 = loadedData.offset_1.drop(
        experiments_to_remove1, axis=0)
    RemovesExperiments["state"] = DISABLED


def remove_experiments_from_data2(SlicedData, ExperimentsToRemoveEntry2,
                                  RemovesExperiments2):
    """
    Same as above for channel 2

    """
    global experiments_to_remove
    if SlicedData["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced first!")
    experiments_to_remove2 = ExperimentsToRemoveEntry2.get()
    experiments_to_remove2 = pharse_experiments_input(experiments_to_remove2)
    loadedData.offset_2 = loadedData.offset_2.drop(
        experiments_to_remove2, axis=0)
    RemovesExperiments2["state"] = DISABLED


def PlotWithLabels_func(SlicedData, SubstractBlankExperiments, num_of_labels):
    """
    Make modular window for the specified number of labels.

    ----------
    num_of_labels : Number of different labels

    Returns
    -------
    None.

    """
    # create popup gui for specific labeling
    EagLabels = Tk()
    EagLabels.title("Plotting by labels")
    all_label_rows = []
    EagLabels.attributes('-topmost', 'true')
    try:
        num_of_labels = int(num_of_labels)
    except:
        mb.showerror("Error", "You didn't enter a number, so we choose 4")
        num_of_labels = 4

    for i in range(num_of_labels):
        row = []
        row.append(Label(EagLabels, text="Select experiments matching label " + str(i + 1) + ":", font=('Times 10')))
        row[-1].grid(row=i, column=0)
        row.append(Entry(EagLabels))
        row[-1].grid(row=i, column=1)
        row.append(Label(EagLabels, text="Select label " + str(i + 1) + ":", font=('Times 10')))
        row[-1].grid(row=i, column=2)
        row.append(Entry(EagLabels))
        row[-1].grid(row=i, column=3)
        all_label_rows.append(row)
    # create button for making the plot
    PlottingChannel_1_Button = Button(EagLabels, width=15, text="Create Plot channel 1", command=
    lambda SlicedData=SlicedData,
           all_label_rows=all_label_rows,
           EagLabels=EagLabels, SubstractBlankExperiments=SubstractBlankExperiments,
           channel=1:
    plot_labels(SlicedData, all_label_rows, SubstractBlankExperiments, EagLabels, channel))
    PlottingChannel_1_Button.grid(row=num_of_labels, column=0, columnspan=4)
    PlottingChannel_2_Button = Button(EagLabels, width=15, text="Create Plot channel 2", command=
    lambda SlicedData=SlicedData,
           all_label_rows=all_label_rows,
           EagLabels=EagLabels, SubstractBlankExperiments=SubstractBlankExperiments,
           channel=2:
    plot_labels(SlicedData, all_label_rows, SubstractBlankExperiments, EagLabels, channel))
    PlottingChannel_2_Button.grid(row=num_of_labels, column=2, columnspan=4)
    EagLabels.mainloop()


def plot_labels(SlicedData, all_label_rows, SubstractBlankExperiments, EagLabels, channel):
    """
    Plot the experiments with the specified labels.

    ----------
    EagLabels : The window from the previous function
    channel : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # gets the number of experiments per label and plots them
    if SlicedData["state"] == NORMAL or SubstractBlankExperiments["state"] == NORMAL:
        mb.showerror("Error", "The data needs to be sliced and both offset and blank needs to be substracted  first!")
        EagLabels.destroy()
        return
    experiments = []
    labels = []
    for i in range(len(all_label_rows)):
        current_experiment = all_label_rows[i][1].get()
        if current_experiment == "":
            continue
        experiments.append(pharse_experiments_input(current_experiment))
        labels.append(all_label_rows[i][3].get())
    fig = plot_experiments_label_data(experiments, labels, loadedData, channel)
    canvas = FigureCanvasTkAgg(fig, master=EagLabels)
    canvas.draw()
    canvas.get_tk_widget().grid(row=15, column=1)


def compare_recording_sides(selection):
    """
    Compare the two sides (R/L).

    ----------
    selection : R/L specified by user.

    Returns
    -------
    None.

    """
    loadedData.compare_sides(selection)


def main():
    """
    The GUI main function.

    Returns
    -------
    None.

    """
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
        command=lambda AnalysisTimeFrame=AnalysisTimeFrame, SlicedData=SlicedData:
            slice_data(AnalysisTimeFrame, SlicedData))
    SlicedData.grid(row=4, column=2)

    FirstExperiment = Label(
        EagGui, text="Select first experiment # :", font=('Times 10'))
    FirstExperiment.grid(row=8, column=0)
    FirstExperimentNumber1 = Entry(EagGui)
    FirstExperimentNumber1.grid(row=8, column=1)

    SecondExperiment = Label(
        EagGui, text="Select last experiment # :", font=('Times 10'))
    SecondExperiment.grid(row=9, column=0)
    SecondExperimentNumber1 = Entry(EagGui)
    SecondExperimentNumber1.grid(row=9, column=1)

    entry_Stability = Label(EagGui, width=15, height=1, bg="light grey")
    entry_Stability.grid(row=8, column=4)

    entry_Stability2 = Label(EagGui, width=15, height=1, bg="light grey")
    entry_Stability2.grid(row=9, column=4)

    StabilityButton = Button(
        text="Compute", command=lambda
            SlicedData=SlicedData, FirstExperimentNumber1=FirstExperimentNumber1,
            SecondExperimentNumber1=SecondExperimentNumber1,
            entry_Stability=entry_Stability, entry_Stability2=entry_Stability2:
        calculate_stability(
            SlicedData, FirstExperimentNumber1,
            SecondExperimentNumber1, entry_Stability, entry_Stability2))
    StabilityButton.grid(row=8, column=2)

    label_StabilityButton = Label(EagGui, text="Response stability- channel 1: ")
    label_StabilityButton.grid(row=8, column=3)

    label_StabilityButton = Label(EagGui, text="Response stability- channel 2: ")
    label_StabilityButton.grid(row=9, column=3)

    ExperimentsToAnalyze = Label(
        EagGui, text="Experiments to analyze:", font=('Times 10'))
    ExperimentsToAnalyze.grid(row=5, column=0)
    ExperimentsToAnalyzeEntry = Entry(EagGui)
    ExperimentsToAnalyzeEntry.grid(row=5, column=1)

    PlotExperimentsCh1 = Button(
        text="Plot experiments channel 1", command=
        lambda SlicedData=SlicedData,
               ExperimentsToAnalyzeEntry=ExperimentsToAnalyzeEntry,
               EagGui=EagGui:
        plot_experiments_ch1(SlicedData, ExperimentsToAnalyzeEntry, EagGui))
    PlotExperimentsCh1.grid(row=5, column=2)

    PlotExperimentsCh2 = Button(
        text="Plot experiments channel 2", command
        =lambda SlicedData=SlicedData,
                ExperimentsToAnalyzeEntry=ExperimentsToAnalyzeEntry,
                EagGui=EagGui:
        plot_experiments_ch2(SlicedData, ExperimentsToAnalyzeEntry, EagGui))
    PlotExperimentsCh2.grid(row=5, column=3)

    BlankExperiments = Label(
        EagGui, text="Blank Experiments:", font=('Times 10'))
    BlankExperiments.grid(row=6, column=0)
    BlankExperimentsEntry = Entry(EagGui)
    BlankExperimentsEntry.grid(row=6, column=1)

    OffsetSampels = Label(
        EagGui, text="# of sampels for offset:", font=('Times 10'))
    OffsetSampels.grid(row=7, column=0)
    OffsetSampelsEntry = Entry(EagGui)
    OffsetSampelsEntry.grid(row=7, column=1)

    PlotBlankExperiments = Button(text="Plot blank",
                                  command=lambda SlicedData=SlicedData,
                                                 BlankExperimentsEntry=BlankExperimentsEntry,
                                                 EagGui=EagGui: plot_blanks(
                                      SlicedData,
                                      BlankExperimentsEntry, EagGui))
    PlotBlankExperiments.grid(row=6, column=2)

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
    SubstractBlankExperiments.grid(row=7, column=2)

    num_of_labels_label = Label(text="# of labels for plotting:", font=('Times 10'))
    num_of_labels_label.grid(row=12, column=0)

    num_of_labels_entry = Entry(EagGui)
    num_of_labels_entry.grid(row=12, column=1)

    PlotWithLabels = Button(
        text="Plot experiments with labels", command=
        lambda SlicedData=SlicedData, SubstractBlankExperiments=SubstractBlankExperiments:
        PlotWithLabels_func(SlicedData, SubstractBlankExperiments, num_of_labels_entry.get()))
    PlotWithLabels.grid(row=12, column=2)

    ExperimentsToRemove = Label(EagGui, text="Experiments to remove from data-channel 1:", font=('Times 10'))
    ExperimentsToRemove.grid(row=10, column=0)
    ExperimentsToRemoveEntry1 = Entry(EagGui)
    ExperimentsToRemoveEntry1.grid(row=10, column=1)

    ExperimentsToRemove = Label(
        EagGui, text="Experiments to remove from data-channel 2:", font=('Times 10'))
    ExperimentsToRemove.grid(row=11, column=0)
    ExperimentsToRemoveEntry2 = Entry(EagGui)
    ExperimentsToRemoveEntry2.grid(row=11, column=1)

    RemovesExperiments = Button(
        text="Remove specified experiments -1")
    RemovesExperiments.configure(command=lambda SlicedData=SlicedData,
                                                ExperimentsToRemoveEntry1=
                                                ExperimentsToRemoveEntry1,
                                                RemovesExperiments=RemovesExperiments:
    remove_experiments_from_data(
        SlicedData,
        ExperimentsToRemoveEntry1,
        RemovesExperiments))
    RemovesExperiments.grid(row=10, column=2)

    RemovesExperiments2 = Button(
        text="Remove specified experiments-2")
    RemovesExperiments2.configure(command=lambda SlicedData=SlicedData,
                                                 ExperimentsToRemoveEntry2=ExperimentsToRemoveEntry2,
                                                 RemovesExperiments2=RemovesExperiments2:
    remove_experiments_from_data2(
        SlicedData,
        ExperimentsToRemoveEntry2,
        RemovesExperiments2))
    RemovesExperiments2.grid(row=11, column=2)

    CompareSidesLabel = Label(EagGui, text="Choose if ch1 is Right or Left"
                              , font=('Times 10'))
    CompareSidesLabel.grid(row=13, column=1)
    R_or_L = StringVar(EagGui)
    # variable.set('R') # default value
    R_or_L_menu = OptionMenu(EagGui, R_or_L, 'R', 'L', command=compare_recording_sides)
    R_or_L_menu.grid(row=13, column=2)

    ExcelFileName = Label(EagGui, text=
    "Type excel file name (without .xlsx):"
                          , font=('Times 10'))
    ExcelFileName.grid(row=14, column=0)
    ExcelFileNameEntry = Entry(EagGui)
    ExcelFileNameEntry.grid(row=14, column=1)

    excel_button = Button(
        EagGui, text="Export to excel and to Text", bg="green")
    excel_button.configure(command=lambda SlicedData=SlicedData,
                                          ExcelFileNameEntry=ExcelFileNameEntry,
                                          excel_button=excel_button:
    export_data_to_excel(
        SlicedData,
        ExcelFileNameEntry, excel_button))
    excel_button.grid(row=14, column=2)

    exit_button = Button(EagGui, text="Exit", bg="red", command=EagGui.destroy)
    exit_button.grid(row=20, column=1)

    EagGui.attributes("-topmost", True)
    EagGui.title('EAG analysis GUI')
    # EagGui.attributes('-fullscreen',True)

    EagGui.mainloop()


if __name__ == "__main__":
    main()
