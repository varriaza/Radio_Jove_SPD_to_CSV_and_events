# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 13:53:05 2018

@author: Victor A
"""
import os
from datetime import datetime, timedelta
import dateutil.parser as dparser
import csv

#-----------------------------------------------------------------------------
# Functions Below
    
    # Function that will return any possible events for the date(s) given 
    # Note file_start_time is the full date and time!       
def find_data_events(file_start_time,file_end_time,data_date,data_times):
    events_list = []
    # Isolate the date only (we don't want the time at this point)
    start_date = dparser.parse(file_start_time[0:10],fuzzy=True, dayfirst=False)
    end_date = dparser.parse(file_end_time[0:10],fuzzy=True, dayfirst=False)
    
    # Do a binary search to see if we have an event that day, 
    #    and convert the date to a string (it was of type datetime)
    start_search = binary_search(data_date,start_date.strftime("%Y-%m-%d"))
    end_search = False
    if (start_date!= end_date):
        end_search = binary_search(data_date,end_date.strftime("%Y-%m-%d"))
    
    #Check if we got any maches
    if (start_search != False):
        #The index is stored in the second position
        index = start_search[1]
        events_list.append(data_times[index])
    if (end_search != False):
        #The index is stored in the second position
        index = end_search[1]
        events_list.append(data_times[index])    
    return events_list

def find_event_times(events_list,csv_data):
    # !!!!!!!!!!!!!*****NOTE*****!!!!!!!!!!!!!
    # We assume that our csv_data has less than or approx. equal to 24 hours 
    # of data, even if it covers two days.
    # We also assume recording does not start on 00:00!!!!!!!!!
    # If recording does start then, things get messed up in the,
    # ***** DAY1 ONLY ***** and ***** DAY2 ONLY ***** sections.
    
    # Loop through events list and find relevant times in csv
    # NOTE! There might be two entries in this double list!
    # One for the start day and the other for the end day
    
    # Test to see if the data spans two days or one
    #print(events_list)
    if (len(events_list) > 1):
        start_day_events = events_list[0]
        end_day_events = events_list[1]
    else:
        start_day_events = events_list[0]
        end_day_events = []
        
    # Make Bool to test to see if we find data
    data_found = False
    
    #------
    # Test if the end_day has an event that could be confused to have started
    # in the start_day. eg: the data begins at 9am and ends at 9am the next day (24 hours). 
    # If we have an event on the end day at 10 am, we do not want to pick this up!
    # SOLUTION -> split event into day1 and day2 so we can handle them separately  
    #-------
    
    event_start_times1 = []
    event_end_times1 = []
    
    event_start_times2 = []
    event_end_times2 = []
    
    # Lists that hold the event types of the starting day and ending day
    #event_start_list = []
    #event_end_list = []
    
    # Get starting and ending times of the events
    if (end_day_events == []):
        for event in start_day_events:
            # Get times for events from start_day
            event_start_times1.append(event[5:10])
            event_end_times1.append(event[11:16])

    else:
        for event in start_day_events:
            # Get times for events from start_day
            event_start_times1.append(event[5:10])
            event_end_times1.append(event[11:16])
            
        for event in end_day_events:
            # Get times for events from end_day
            event_start_times2.append(event[5:10])
            event_end_times2.append(event[11:16])
    
    # Create list to hold our new data list 
    new_csv_list = ['Possible Events \n']
    # Create indexs
    csv_index = 0
    time_index = 0
      
    # ***** DAY1 ONLY *****
    # Extract relevant data lines and add them to new_csv_list
    for start_time in event_start_times1:
        # In case of overlaping events reset csv_index
        csv_index = 0
        for line in csv_data:
            # Find the time from the line's date
            # [line index][second value is date][get time from date string]
            csv_time = csv_data[csv_index].split(",")
            csv_time = csv_time[2][11:16]
            if (csv_time == "00:00"):
                break
            # If the csv_time is between our start and end event time record it
            if (start_time <= csv_time and event_end_times1[time_index] >= csv_time):
                # If we are just starting out or at the beginning of a new possible
                # event, then add which kind it is (aka Io A, or Io B or Io C)
                current_place = new_csv_list[len(new_csv_list)-1]
                if(current_place == '\n' or len(new_csv_list) == 1):
                    new_csv_list.append(events_list[0][time_index][0:4]+'\n')
                new_csv_list.append(line)
                data_found = True
            # Add to index so the next line will be accurately found
            csv_index = csv_index + 1
        
        # When we finish trying to find an event add in a space to separate events 
        new_csv_list.append('\n')
        # This makes sure the event_end_times stays synced with the start_times
        time_index = time_index + 1    
        
        
    # Reset indexes
    csv_index = 0
    time_index = 0
     
    # ***** DAY2 ONLY *****
    if (event_start_times2 != []):
        # Add a line to make sure we know these are for the second half of the data
        new_csv_list.append('Day 2 \n')
        
        # We can skip all the csv_data lines that are before 00:00
        csv_time = csv_data[csv_index].split(",")
        csv_time = csv_time[2][11:16]
        while (csv_time != '00:00'):
            csv_index = csv_index + 1
            csv_time = csv_data[csv_index].split(",")
            csv_time = csv_time[2][11:16]
        
        # Now we have reached 00:00 we can set this as our starting place for 
        # the day 2 loops
        new_starting_index = csv_index
        
        # Extract relevant data lines and add them to new_csv_list
        for start_time in event_start_times2:
            # In case of overlaping events reset csv_index to new_starting_index
            csv_index = new_starting_index
            csv_length = len(csv_data)
            for csv_index in range(new_starting_index,csv_length-1):
                # Find the time from the line's date
                # [line index][second value is date][get time from date string]
                csv_time = csv_data[csv_index].split(",")
                csv_time = csv_time[2][11:16]
                # If the csv_time is between our start and end event time record it
                if (start_time <= csv_time and event_end_times2[time_index] >= csv_time):
                    # If we are just starting out or at the beginning of a new possible
                    # event, then add which kind it is (aka Io A, or Io B or Io C)
                    current_place = new_csv_list[len(new_csv_list)-1]
                    if(current_place == '\n' or current_place == 'Day 2' or \
                       current_place == 'Day 2 \n' or len(new_csv_list) == 1):
                        new_csv_list.append(events_list[1][time_index][0:4]+'\n')
                    new_csv_list.append(csv_data[csv_index])
                    data_found = True
                # Add to index so the next line will be accurately found
                #csv_index = csv_index + 1
            
            # When we finish trying to find an event add in a space to separate events 
            new_csv_list.append('\n')
            # This makes sure the event_end_times stays synced with the start_times
            time_index = time_index + 1
            
    # If we actually found some events return the list otherwise return an empty list
    if (data_found == True):
        return new_csv_list
    else:
        empty_list = []
        return empty_list

def binary_search(a_list, item):
    """Performs iterative binary search to find the position of an integer in a given, sorted, list.

    a_list -- sorted list of integers
    item -- integer you are searching for the position of
    """
    r_list = []
    first = 0
    last = len(a_list) - 1

    while first <= last:
        i = (first + last) / 2

        if a_list[i] == item:
            r_list.append(item)
            r_list.append(i)
            return r_list
        elif a_list[i] > item:
            last = i - 1
        elif a_list[i] < item:
            first = i + 1
    
    return False

def open_csv_file(csv_file_name):
    with open(csv_file_name) as data_file:
        csv_data = data_file.readlines()
        data_file.close()
        return csv_data


def load_predictions_data(predictions_data):
    # Number of lines before data starts in predictions_data
    ignore_lines = 8
    # Number of lines between data
    #data_spacing = 3
    # Data lists
    data_date = []
    data_times = []
    count = 0;
    # Empty list that will hold values until we get all of the times
    data_to_append = []
    
    for line in predictions_data:
        # ignore the first 9 lines
        if (count>ignore_lines):
            # All of the dates start with the '<' symbol
            if line.startswith('<'):
                # Find numbers in line
                numbers = [int(s) for s in line.split() if s.isdigit()]
                # Turn numbers from 2016-2-3 to 2016-02-03 so we can match later
                year = str(numbers[0])
                month = str(numbers[1])
                day = str(numbers[2])
                if (len(month) <2):
                    month = '0' + month
                if (len(day)<2):
                    day = '0' + day
                # Put numbers found above into date format (Year-Month-Day)
                data_date.append(year + '-' + month + '-' + day)
                
            # Note: ' Io' needs the space before it!
            elif line.startswith(' Io'): 
                # split line into non-space list
                new_line = line.split()
                new_line_length = len(new_line)
            
                # itterate over list to find when you get the first entry that has a number
                for x in range(0,new_line_length,2):   
                    # data will be in format: ['Io', 'B', '03:22', '06:01','Io', 'C', '07:22', '08:01'] for example
                    if (new_line[x][0].isdigit()):
                        # When a time is found take the values two behind to get the Io event type and
                        # then take the value and the one ahead to get start and stop times
                        # the data is entered as [Io A,03:23-04:45]
                        data_to_append.append(
                                new_line[x-2] + ' ' + new_line[x-1] + \
                                              ' ' + new_line[x]+ '-' + new_line[x+1])
                        
            elif (line.startswith('_')):
                data_times.append(data_to_append)
                data_to_append = []
        count = count + 1
    return_data = [data_date,data_times]
    return return_data


def main_func(csv_list):
    # For Victor's flashdrive
    #os.chdir('F:\\Radio_Jove') 
    # For Victor's flashdrive on the laptop
    #os.chdir('E:\\Radio_Jove')
    
    # os.getcwd()
    # returns current working directory
    
    # os.listdir(current_dir)
    # Lists out files in current_dir 
    
    
    ###### Get current directory
    old_dir = os.getcwd()
    ###### Go to directory with '2016-2020.txt'
    os.chdir('C:\Users\spencer\AppData\Local\VirtualStore\Program Files (x86)\Radio-SkyPipe II\\')
    
    # File that has predictions from Radio Jupiter Pro
    pro_predictions = '2016-2020.txt'
    # List to hold info from file
    predictions_data = []
    
    # Open file and read lines into list
    with open(pro_predictions) as data_file:
        predictions_data = data_file.readlines()
        data_file.close()
    
    get_data = load_predictions_data(predictions_data)
    data_date = get_data[0]
    data_times = get_data[1]
    
    ###### Return to old directory
    os.chdir(old_dir)

    
    for csv_file in csv_list:
        csv_data = open_csv_file(csv_file)
        csv_length = len(csv_data)
        csv_data_start = csv_data[1].split(",")
        csv_data_end = csv_data[csv_length-1].split(",")
        # Note file_start_time is the full date and time! 
        file_start_time = csv_data_start[2]
        # Note file_end_time is the full date and time! 
        file_end_time = csv_data_end[2]
        
        # events_list is a list of all possible events given the file
        events_list = find_data_events(file_start_time,file_end_time,data_date,data_times)
        
        if (events_list != []):
            # try to find if we have data for any of the possible events
            new_csv_data = find_event_times(events_list,csv_data)

            # If we have an event time record it otherwise note no events
            if (new_csv_data != []):
                new_csv_file = csv_file[:-4] + '_events.csv'        
                with open(new_csv_file,'w') as csv_file_open:
                    csv_file_open.write("".join(new_csv_data))
                    csv_file_open.close()
                    print("+++++ Events found for: " + csv_file[:-4] + " +++++")
            else:
                new_csv_file = csv_file[:-4] + '_events.csv'        
                with open(new_csv_file,'w') as csv_file_open:
                    csv_file_open.write("----- No events found -----")
                    csv_file_open.close()
                    print("----- No events found for: " + csv_file[:-4] + " -----")
        else:
            new_csv_file = csv_file[:-4] + '_events.csv'        
            with open(new_csv_file,'w') as csv_file_open:
                csv_file_open.write("----- No events found -----")
                csv_file_open.close()
                print("----- No events found for: " + csv_file[:-4] + " -----")
            
    return

# End of functions
#-----------------------------------------------------------------------------
#*****************************************************************************
# Start of executable code 
        
#### Uncomment to test (also need to uncomment os.chir() in main_func)
#csv_list = ['UT160401155704.csv']
#main_func(csv_list)









