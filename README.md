# Python-EAG-analysis

This project creates an easy-to-use dashboard that allow researchers to load, pre-process and plot initial EAG data from .ASC files.

## Description

Electroantennogram (EAG) is a technique for measuring the average output of an insect antenna for a given odor.
Syntech is a German company that does development and production of biophysical instrumentation, particularly for the study of insect chemoreception.
Syntech also provides a specific recording programs design to record from their various instruments, one of them in AUTOSPIKE.
While AUTOSPIKE integrated with some analysis functions, some desirable options are missing.
Furthermore, working with large volume of data crushed the program on several occasions.

This package can take data recorded from 2 channels in parallel and exported from AUTOSPIKE in ASCII format (.ASC), analyzed and plot it in several ways.
An in-depth paragraph about your project and overview of use.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets

Guideline for EAG analysis GUI:

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

For more examples, please refer to the Documentation.

## Help

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
