# Python-EAG-analysis

This project creates an easy-to-use dashboard that allow researchers to load, pre-process and plot initial EAG data from .ASC files.

## Installing and executing the program

* Download all folders from the following link : https://www.dropbox.com/sh/fqueakv37j9f6u1/AAA8sDu4T7JmOr0SpZq1c0zHa?dl=0
* Run the 'EAGGui' file in the 'dist' folder
* The program can also be run using a Python IDE by running the EAGGui.py file.


## Description

Electroantennogram (EAG) is a technique for measuring the average output of an insect antenna for a given odor.
Syntech is a German company that does development and production of biophysical instrumentation, particularly for the study of insect chemoreception.
Syntech also provides a specific recording programs design to record from their various instruments, one of them in AUTOSPIKE.
While AUTOSPIKE integrated with some analysis functions, some desirable options are missing.
Furthermore, working with large volume of data crushed the program on several occasions.

This package can take data recorded from 2 channels in parallel and import from AUTOSPIKE in ASCII format (.ASC), analyzed and plot it in several ways.


![alt text](https://github.com/Eyal-ro/Python-EAG-analysis/blob/master/Orthoptera_image%20(3).jpg?raw=true)

@Keren Levy

### Special functions

#### The Response Stability function

Insect’s antenna signal tends to decay over time. Drop of the signal below a certain threshold must be considered while analyzing the results. This function will take the average of the minimum EAG values measured in the first experiment (for a given odorant) and compare it with the corresponding value of the last experiments with the same stimuli. The experimenter must design his experiment to have the same stimuli at the beginning and at the end.

#### Compare sides function

This function allows to compare the respond of the insect’s left and right antennae. 
It takes the minimal value from each of the two channels taken in the same experiment and compare them using the following equation:

(|Min val R|-|min val L|)/(|Min val R|+|min val L|)

#### Analysis

All the data is going through the process of subtract blank and offset.
Subtract blank will take the control experiments (response to wind/solvent) and subtract their average from the data according to time points (per channel). This way only the antenna response to the odorant will be manifested in the final data.
Offset will take the first 100 samples (or more depends on the user input), and subtract its median from all the values of the same experiment.

### Files descriptions

* EAGGui.py - Contains the GUI backbone and command functions.
* GUI_helper_functions.py - Contains GUI helper functions (such as plotting etc.).
* EAG_analysis_class.py - Contains the functions that generate an object of the EAG class.
* tests_EAG_analysis_class.py - Test script containing tests for multiple methods of EAG_analysis_class, using test files pre-made (in test_files folder).    
* tests_EAGGui.py - Test script containing tests for EAGGui.

(Detailed descriptions for each individual function are located in the function docstring)

## Getting Started

### Dependencies

* This package was generated using Python 3 on a Windows 10 machine. 
* Running the EAGGui.exe file does not have any pre-requirements. Alternatively, running the EAGGui.py code automatically install the necessary Python packages. 


#### Guideline for EAG analysis GUI

1.	Click the 'Upload file' button to load select a data file (type ASC) to the dashboard.
2.	Choose the analysis time frame in seconds by filling analysis time window and click the 'Slice data' button. 
    - Please note, you cannot work on unsliced data and will not be able to procced. 
4.	Enter number of experiments for initial analysing. 
5.	Choose which channel to plot from by clicking on the 'Plot experiments channel 1' or 'Plot experiments channel 2'.
6.	Fill the blank experiments number and create plot with only the blank experiments by clicking on 'Plot blank'.
7.	For checking response stability per channel, choose first and second experiments numbers wanted by filling the appropriate windows with experiments numbers, and click on 'Compute'.
8.	Fill the number of samples for offset.
    - In case it is not filled, default is 100.
10.	Click the 'Subtract blank and offset' to remove blank experiments and offset samples from the data.
11.	If there are unwanted experiments that needs to be removed, fill relevant number of experiments, and click on 'Removed specified experiments - 1' for removing from channel 1 data or 'Removed specified experiments - 2' from removing from channel 2 data. 
12.	For initial plotting of labeled experiments, fill number of labels and click on 'Plot experiments with labels'.
    - In case button is clicked but number of labeled is empty, default number is 4.
14.	 For each label, fill relevant experiments numbers and which label is it. When finished, click on 'Create Plot channel 1' or ' Create Plot channel 2' for plotting from wanted channel.
15.	Before exporting, choose which side if channel 1 - if it is either right or left.
    - Channel 2 will be the other side by default.  
13.	Click on 'Export to excel' button to export data as .xlsx file to wanted folder.



## Help

In case the script is changed, there are pre-made test files with real data for you to check it with. 

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names:

* Eyal Rozenfeld
* Yifat Weiss
* Neta Shvil




## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
