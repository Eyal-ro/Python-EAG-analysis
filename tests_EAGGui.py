from EAGGui import *
import GUI_helper_functions

def test_slice_button_is_disabled():
    loadedData = EAGanalysis("Raw data - mix and segments, 12.5.21.ASC")

    #main loop
    test_main = Tk()
    AnalysisTimeFrame = Entry(test_main)
    AnalysisTimeFrame.insert(0, "1")
    SlicedData = Button(text="Slice data")

    #checked if slice data disabled
    slice_data(AnalysisTimeFrame,SlicedData,loadedData)
    if SlicedData["state"] == DISABLED:
        test_main.destroy()
        return "success test_slice_button_is_disabled"
    else:
        test_main.destroy()
        return "error test_slice_button_is_disabled"


    test_main.mainloop()
   

def test_subtract_blank_button_is_disabled():
    loadedData = EAGanalysis("Raw data - mix and segments, 12.5.21.ASC")

    #main loop
    test_main = Tk()
    SlicedData = Button(text="Slice data")
    SlicedData["state"]=DISABLED
    BlankExperimentsEntry = Entry(test_main)
    BlankExperimentsEntry.insert(0, "1")
    OffsetSampelsEntry = Entry(test_main)
    SubstractBlankExperiments = Button(
        text="Subtract blank and offset")
    #checked if slice data disabled
    subtract_blank(SlicedData, BlankExperimentsEntry, OffsetSampelsEntry,
                   SubstractBlankExperiments)
    if SubstractBlankExperiments["state"] == DISABLED:
        test_main.destroy()
        return "success test_subtract_blank_button_is_disabled"
    else:
        test_main.destroy()
        return "error test_subtract_blank_button_is_disabled"


    test_main.mainloop()


if __name__ == "__main__":
    methods = ["test_slice_button_is_disabled", "test_subtract_blank_button_is_disabled"]
    results = []
    failed = []
    passed = []

    for method in methods:
        result = eval(method)()
        if "error" in result:
            failed.append(result)
        else:
            passed.append(result)

    print("Tests failed:")
    for fail in failed:
        print(fail)

    print("Tests passed:")
    for success in passed:
        print(success)


