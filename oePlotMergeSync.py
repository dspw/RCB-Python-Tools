# DSP Wireless, Inc. - DSPW - Robert Paugh - 04/12/25

import requests
import matplotlib.pyplot as plt
from collections import OrderedDict
from open_ephys.analysis import Session

# Plot Stream Variables
startIdx = 0000
endIdx = 60000
startCh = 0
endCh = 0
numStreams = 2

# ======= Set to directory where your OE data is stored. ======= #
#directory = '/Volumes/gannet4MB/Open Ephys/2025-04-25_00-43-33'

directory = '2025-04-25_00-43-33'

fullPath = '/Volumes/gannet4MB/Open Ephys/' + directory

# ======= Set to experiment number. ======= #
# index at 0 so experimentNN - 1
recordingsNum = 2


# get data from the Session
#session = Session(directory)
session = Session(fullPath)
recordnode = session.recordnodes[0]
myRecording = session.recordnodes[0].recordings[recordingsNum]

# get Sample numbers
sampleNum0 = myRecording.continuous[0].sample_numbers
sampleNum1 = myRecording.continuous[1].sample_numbers

# in case recordings are not all same length
idxDiff = abs(len(sampleNum0) - len(sampleNum1))
endIdx = len(sampleNum0) - (3*idxDiff) 

# Get Timestamps 
timeStamp0 = myRecording.continuous[0].timestamps[startIdx:endIdx]
timeStamp1 = myRecording.continuous[1].timestamps[startIdx:endIdx]

#Get Events
# events are 0/1, mult by 350 so can see on the plot
eventTime0 = myRecording.events.timestamp
states0 = myRecording.events.state *350 

eventTime1 = myRecording.events.timestamp
states1 = myRecording.events.state *350

# Plot the Data
plt.title('oePlotMerge')
plt.xlabel('Time Stamps')
plt.ylabel('Samples (uV)')
#plt.xlabel('Sample Number')

if numStreams >= 1:
    data0Chx = myRecording.continuous[0].get_samples(start_sample_index=startIdx, end_sample_index=endIdx, selected_channels=(startCh,endCh))
    plt.plot(timeStamp0, data0Chx, color = 'red', label = 'data0')
#    plt.plot(sampleNum0, data0Chx, color = 'red', label = 'data0')
    plt.step(eventTime0, states0 + -20,color = 'green', label = 'event0') # add offset so easier to see on plot

if numStreams >= 2:
    data1Chx = myRecording.continuous[1].get_samples(start_sample_index=startIdx, end_sample_index=endIdx, selected_channels=(startCh,endCh))
    plt.plot(timeStamp1, data1Chx, color = 'blue',label = 'data1')
#    plt.plot(sampleNum0, data1Chx, color = 'blue',label = 'data1')
    plt.step(eventTime1, states1 + 20,color = 'orange', label = 'event1') # add offset so easier to see on plot
 
# Get handles and labels
handles, labels = plt.gca().get_legend_handles_labels()

# Create a dictionary of unique labels and handles
by_label = OrderedDict(zip(labels, handles))

# Create the legend with unique labels
plt.legend(by_label.values(), by_label.keys(),loc='best')

plt.grid()
plt.show()

