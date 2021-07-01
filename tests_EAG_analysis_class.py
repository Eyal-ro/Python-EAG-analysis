from EAG_analysis_class import *
from os import path


def compare_data_to_csv(csv, data):
    """compare pre-made real data file and test panda data frame,
        while ignoring NaN values, and estimating them as equals if the
        difference between them is smaller than python rounding resolution

        Parameters
        ----------
        csv - path to csv file
        data - pd dataframe

        Returns
        -------
        bool - True if the data stored in the csv is equal to the pd dataframe. False otherwise.
        """
    small_threshold = 10**-8

    real_data = pd.read_csv("tests_files/"+csv)
    diff = np.nan_to_num(np.nan_to_num(real_data.values.squeeze()).astype(float)-
                         np.nan_to_num(data.values).astype(float))
    return np.array_equal(np.abs(diff) < np.ones_like(diff) * small_threshold, np.ones_like(diff)) # if the difference
                                                                                                  # between the arrays
                                                                                                  # is smaller than csv
                                                                                                  # saving resolution


def test_input_valid():
    try:
        temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
        return "success test_input_valid"
    except TypeError:
        return "error test_input_valid"


def test_input_invalid():
    try:
        temp = EAGanalysis("4356")
        return "error test_input_invalid"
    except TypeError:
        return "success test_input_invalid"


def test_arrange_data_slicing(slice=6):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    if len(temp.del_Unnecessary_lines)>slice*100:
        return "error test_arrange_data_func"
    else:
        return "success test_arrange_data_func"

    
def test_arrange_data_rearrangement(slice=6):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    if compare_data_to_csv("arrange_data_test.csv",temp.del_Unnecessary_lines):
        return "success test_arrange_data_rearrangement"
    else:
        return "error test_arrange_data_rearrangement"

    
def test_transpose(slice=6):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    if compare_data_to_csv("transpose_test.csv", temp.values_only):
        return "success test_transpose"
    else:
        return "error test_transpose"

    
def test_multi_indexing(slice=6):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    if compare_data_to_csv("multi_indexing_test.csv", temp.values_only):
        return "success test_multi_indexing"
    else:
        return "error test_multi_indexing"

    
def test_multi_indexing(slice=6):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    if compare_data_to_csv("multi_indexing_test.csv", temp.values_only):
        return "success test_multi_indexing"
    else:
        return "error test_multi_indexing"


def test_average_blank_channel1(slice=6, blank_experiments=1):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    if -524.2147651006711 == temp.channel1_blank_avg:
        return "success test_average_blank_channel1"
    else:
        return "error test_average_blank_channel1"


def test_average_blank_channel2(slice=6, blank_experiments=1):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    if -215.55872483221478 == temp.channel2_blank_avg:
        return "success test_average_blank_channel2"
    else:
        return "error test_average_blank_channel2"

    
def test_minus_blank_channel1(slice=6,blank_experiments=1):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    if compare_data_to_csv("minus_blank_channel1_test.csv", temp.minus_blank_1):
        return "success test_minus_blank_channel1"
    else:
        return "error test_minus_blank_channel1"


def test_minus_blank_channel2(slice=6, blank_experiments=1):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    if compare_data_to_csv("minus_blank_channel2_test.csv", temp.minus_blank_2):
        return "success test_minus_blank_channel2"
    else:
        return "error test_minus_blank_channel2"

    
def test_offset_channel1(slice=6, blank_experiments=1, sampels_to_offset=100):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    temp.offset(sampels_to_offset)
    if compare_data_to_csv("offset_channel1_test.csv", temp.offset_1):
        return "success test_offset_channel1"
    else:
        return "error test_offset_channel1"

    
def test_offset_channel2(slice=6, blank_experiments=1, sampels_to_offset=100):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    temp.offset(sampels_to_offset)
    if compare_data_to_csv("offset_channel2_test.csv", temp.offset_2):
        return "success test_offset_channel2"
    else:
        return "error test_offset_channel1"


def test_compare_sides(slice=6,blank_experiments=1, sampels_to_offset=100):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    temp.offset(sampels_to_offset)
    temp.compare_sides()
    if compare_data_to_csv("compare_sides_test.csv", temp.compare_sides_val):
        return "success test_compare_sides"
    else:
        return "error test_compare_sides"


def test_compare_sides(slice=6, blank_experiments=1, sampels_to_offset=100, channel_1="R"):
    temp = EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    temp.offset(sampels_to_offset)
    temp.compare_sides(channel_1)
    if compare_data_to_csv("compare_sides_test.csv", temp.compare_sides_val):
        return "success test_compare_sides"
    else:
        return "error test_compare_sides"


def test_export_to_excel(slice=6,blank_experiments=1, sampels_to_offset=100):
    temp=EAGanalysis('Raw data - mix and segments, 12.5.21.ASC')
    temp.arrange_data(slice)
    temp.transpose()
    temp.multi_indexing()
    temp.average_blank(blank_experiments)
    temp.minus_blank()
    temp.offset(sampels_to_offset)
    temp.compare_sides("R")
    temp.export_to_excel("Raw data - mix and segments, 12.5.21.xlsx")
    if path.exists("Raw data - mix and segments, 12.5.21.xlsx"):
        return "success test_export_to_excel"
    else:
        return "error test_export_to_excel"

    
if __name__ == "__main__":
    methods = ["test_input_valid", "test_input_invalid",
               "test_arrange_data_slicing", "test_arrange_data_rearrangement",
               "test_transpose", "test_multi_indexing", "test_average_blank_channel1", "test_average_blank_channel2",
               "test_minus_blank_channel1", "test_minus_blank_channel2", "test_offset_channel1", "test_offset_channel2",
               "test_compare_sides", "test_export_to_excel"]
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
