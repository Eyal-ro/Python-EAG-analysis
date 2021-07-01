import pathlib
from typing import Union
import numpy as np
import pandas as pd


class EAGanalysis:
    """
    Reads and analyzes data generated by the EAG experiment.
    Attributes: arrange data and analyze it (minus Blank and offset)
    """

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        """Reads csv file and returns it as pd data frame.

        Parameters
        ----------
        fname : pathlib.Path
            Filename for the columnar data containing the EAG measurements.

        Returns
        -------
        self.data : pd.DataFrame
        """

        if type(data_fname) == str:
            data_fname = pathlib.Path(data_fname)
        if data_fname.is_file():
            self.data_fname = data_fname
        else:
            return "File is invalid"

        self.data = pd.read_csv(
            self.data_fname, sep="\t", names=['Time', 'Value'])

    def arrange_data(self, data_range):

        """Takes pd.DataFrame and arrange the experiments in separate columns .
        Also slice the DataFrame (keeps only the time duration asked by the user)

        Parameters
        ----------
        self.data - pd dataframe
        data_range - Duration of recording (in sec) the user wants ti analyze

        Returns
        -------
        self.del_Unnecessary_lines - the df after slicing.
        """
        Times = self.data.iloc[:, 0]
        data_range = data_range * 100

        Find_Signal = Times[Times.str.contains('Signal') == True]
        # returns all the places were the word signal is in
        Signal_index = Find_Signal.index
        # returns the indexes that self.data later be sliced by
        names = []
        # the next loop will slice the dataframe and split it into a list of data frames.
        # Each object in this list is an experiment
        for i, j in enumerate(Signal_index):
            names.append(i)
            if i < (len(Signal_index) - 1):
                names[i] = pd.DataFrame(
                    self.data[Signal_index[i]:Signal_index[i + 1]])
                names[i].reset_index(drop=True, inplace=True)
            else:
                names[len(Signal_index) - 1] = pd.DataFrame(
                    self.data[Signal_index[i]:])
                names[-1].reset_index(drop=True, inplace=True)

        Output = pd.concat(names, axis=1)
        # Combines all list objects into one dataframe

        self.del_Unnecessary_lines = Output.iloc[4:data_range]
        # delet all the lines after 800 (8 seconds)

    def transpose(self):

        """Transposed the sliced dataframe, give it new index and data type

        Parameters
        ----------
        self.del_Unnecessary_lines - dataframe

        Returns
        -------
        self.values_only - dataframe
        """

        Transpose = self.del_Unnecessary_lines.transpose(copy=True)
        # Turns rows into columns and vise versa

        Transpose.columns = Transpose.iloc[0]
        # Assign row as column headers

        self.values_only = Transpose.drop(labels='Time')
        # leave only values in the data frame

        self.values_only = self.values_only.astype('float64')
        # Change data type from object to float.

    def multi_indexing(self):

        """Assign multi- indexing to the df

                Parameters
                ----------
                self.values_only - df

                Returns
                -------
                self.values_only - with multi_indexing
                """

        num_of_exp = []
        for i in range(1, (len(self.values_only) // 3) + 1):
            num_of_exp.append(i)

        index = pd.MultiIndex.from_product([
            num_of_exp, [1, 2, 'D']], names=['#_of_experiment', 'Channel'])

        self.values_only = self.values_only.set_index(index)

    def getAverageOfExperiments(self, experiment_list, channel):
        count = 0
        for i in experiment_list:
            count += 1
            if count == 1:
                data = self.values_only.loc[int(i)].loc[channel].copy()
            else:
                data += self.values_only.loc[int(i)].loc[channel]

        data = data / count

        return data

    def average_blank(self, blank_experiments):
        """
        This function creates an average of the blank experiments and return it as pandas Series

                Parameters
                ----------
                self.values_only - df
                blank_experiments - The numbers of blank experiments according to the user's input

                Returns
                -------
                self.channel1/2_blank_avg  - pandas Series
                """

        self.channel1_blank_avg = self.values_only.loc[
            (blank_experiments, 1), slice(None)].mean()
        self.channel2_blank_avg = self.values_only.loc[
            (blank_experiments, 2), slice(None)].mean()

    def minus_blank(self):
        """
        This function will subtract the blank experiments from all other experiments in the same channel

                  Parameters
                  ----------
                  self.values_only - df
                  self.channel1/2_blank_avg - pandas series

                  Returns
                  -------
                  self.minus_blank_1/2  - 2 df of the data minus blank, one for each channel
                  """

        channel1_minus_blank = self.values_only.subtract(
            self.channel1_blank_avg, axis=1, level=1)
        channel2_minus_blank = self.values_only.subtract(
            self.channel2_blank_avg, axis=1, level=2)

        self.minus_blank_1 = channel1_minus_blank.loc[
            (slice(None), 1), slice(None)]
        self.minus_blank_2 = channel2_minus_blank.loc[
            (slice(None), 2), slice(None)]

    def offset(self, samples_to_offset=100):

        """This function will apply an offset on the data.
        This offset will take the first 100 samples (or more depends on the user input, 100 is the default value),
        and subtract its median from all the values of the same experiment

                  Parameters
                  ----------
                  self.minus_blank1/2 - df
                  samples_to_offset - Number (int) inserted by the user.

                  Returns
                  -------
                  self.offset_1/2  - 2 df of the data after offset, one for each channel
                  """

        median_channel_1 = self.minus_blank_1.iloc[
                           :, :samples_to_offset].median(axis=1)
        median_channel_2 = self.minus_blank_2.iloc[
                           :, :samples_to_offset].median(axis=1)

        self.offset_1 = self.minus_blank_1.subtract(median_channel_1, axis=0)
        self.offset_2 = self.minus_blank_2.subtract(median_channel_2, axis=0)

        self.offset_1 = self.offset_1.reset_index(drop=True)
        self.offset_2 = self.offset_2.reset_index(drop=True)
        # Reset the indecies

        self.offset_1.index = self.offset_1.index + 1
        self.offset_2.index = self.offset_2.index + 1
        # strating the index from 1 instead of 0

    def calculate_stability(self, first_experiments, second_experiments):

        """
                This function creates an average of the first and last experiment's min points (with the same stimuli)
                and give its ratio (1st/last)
                        Parameters
                        ----------
                        self.offset_1/2 - df
                        first_experiments - The numbers of the first 3 experiments according to the user's input
                        second_experiments - The numbers of the last 3 experiments of the same stimuli as the first
                        according to the user's input.
                        Returns
                        -------
                        response_stability - float for channel 1 and for channel 2
                        """
        channel1_start_avg = self.offset_1.loc[
            (first_experiments), slice(None)].min(axis=1).mean()

        channel2_start_avg = self.offset_2.loc[
            (first_experiments), slice(None)].min(axis=1).mean()

        channel1_end_avg = self.offset_1.loc[
            (second_experiments), slice(None)].min(axis=1).mean()

        channel2_end_avg = self.offset_2.loc[
            (second_experiments), slice(None)].min(axis=1).mean()

        self.response_stability1 = channel1_start_avg / channel1_end_avg
        self.response_stability2 = channel2_start_avg / channel2_end_avg

    def compare_sides(self, channel_1):

        """ Compare the response of left and right antenna recorded in parallel according to
        the equation: (R-L)/(R+L)

                  Parameters
                  ----------
                  self.offset1/2 - df
                  channel_1 - will be either R or L, according to the user input

                  Returns
                  -------
                  self.compare_sides_val - panda series of the ratios (the equation results)
                  """

        min_value_1 = self.offset_1.min(axis=1).abs()
        min_value_2 = self.offset_2.min(axis=1).abs()
        # get the min value, turn in to its absolute value

        sum = min_value_1.add(min_value_2)

        # the next part is depend which of the channels is L and Which is Right
        # (according to the user's input), eventually I wish subtract L from R.

        if channel_1 == 'R':
            diff = min_value_1.subtract(min_value_2)
        else:
            diff = min_value_2.subtract(min_value_1)

        self.compare_sides_val = diff / sum

    def prism_ready(self):

        """
            This function transpose the final data after analysis in order to later export it to txt
            in a format that fits to prism
                  Parameters
                  ----------
                  self.offset1/2 - df

                  Returns
                  -------
                  self.Prism1/2 - transposed df
                  """

        self.Prism1 = self.offset_1.transpose(copy=True)
        self.Prism2 = self.offset_2.transpose(copy=True)
        # Turns rows into columns and vise versa

    def export_to_excel(self, file_name):
        """
                  Export all the analyzed data into excel file

                        Parameters
                        ----------
                        self.values_only - df
                        self.offset_1/2 - df
                        self.compare_sides_val - pandas Series

                        Returns
                        -------
                        xlsx file with multipule sheets
                        """

        with pd.ExcelWriter(file_name) as writer:
            self.values_only.to_excel(writer, sheet_name='all_experiments')
            self.offset_1.to_excel(writer, sheet_name='channel1')
            self.offset_2.to_excel(writer, sheet_name='channel2')
            self.compare_sides_val.to_excel(writer, sheet_name='Left Vs. Right')

    def export_to_txt(self, file_name1, file_name2):
        """
                  Export the analyzed data, after transposed, into two txt files

                        Parameters
                        ----------
                        self.Prism1/2 - df

                        Returns
                        -------
                       Two txt files
                        """
        self.Prism1.reset_index(level=0, inplace=True)
        txt_1 = self.Prism1.to_numpy()
        np.savetxt(file_name1, txt_1, fmt="%s")

        self.Prism2.reset_index(level=0, inplace=True)
        txt_2 = self.Prism2.to_numpy()
        np.savetxt(file_name2, txt_2, fmt="%s")
