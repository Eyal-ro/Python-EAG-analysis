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

