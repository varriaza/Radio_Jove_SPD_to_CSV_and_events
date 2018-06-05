# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 13:44:30 2018

@author: Victor A
"""

import os
import SPD_Reader_Vic
import Prediction_Data_Reader

##############################################################################
# Functions








##############################################################################

# For Victor's computer
#os.chdir('C:\\Users\\Victor A\Desktop\Radio_Jove_Research\\1705_test') 

# For Victor's flashdrive
#os.chdir('F:\\Radio_Jove\\University_of_Delawa_test') 

# For Victor's flashdrive on the laptop
os.chdir('C:\Users\spencer\AppData\Local\VirtualStore\Program Files (x86)\Radio-SkyPipe II\University_of_Delawa\\') 

#os.chdir('F:\Radio_Jove\University_of_Delawa_test')

# os.chdir('C:\\Users\\Victor A\desktop') 
# sets the current path to this location

# os.getcwd()
# returns current working directory

# os.listdir(current_dir)
# Lists out files in current_dir 


#prints current directory
current_dir = os.getcwd()
#print(current_dir)

# prints files in current directory
Jove_data_folder = os.listdir(current_dir)
#print(files)

for f_year_months in Jove_data_folder:
    # For Victor's flashdrive
    #os.chdir('F:\\Radio_Jove\\University_of_Delawa_test\\' + f_year_months)
    # For Victor's flashdrive Laptop
    os.chdir('C:\Users\spencer\AppData\Local\VirtualStore\Program Files (x86)\Radio-SkyPipe II\University_of_Delawa\\' + f_year_months)
    
    
    current_dir = os.getcwd()
    f_year_month_day = os.listdir(current_dir)
    
    for file_name in f_year_month_day:
        # For Victor's Computer
        #os.chdir('C:\\Users\\Victor A\Desktop\Radio_Jove_Research\\1705_test\\' + file_name) 
        
        # For Victor's flashdrive
        #os.chdir('F:\\Radio_Jove\\University_of_Delawa_test\\' + f_year_months + '\\' + file_name) 
        # For Victor's flashdrive Laptop
        os.chdir('C:\Users\spencer\AppData\Local\VirtualStore\Program Files (x86)\Radio-SkyPipe II\University_of_Delawa\\' + f_year_months + '\\' + file_name) 
        
        # list of spd files in current directory
        spd_files = []
        current_dir = os.getcwd()
        files_lower = os.listdir(current_dir)
        
        # spd file test
        for item in files_lower:
            # Test to see if the file is an spd file
            item_bool = item.endswith(".spd")
            if item_bool:
                # if it is an spd file add it to the list
                spd_files.append(item)
        
        # list of csv files in current directory
        csv_files = []
        
        # csv file test
        for item in files_lower:
            # Test to see if the file is a csv file
            item_bool = item.endswith(".csv")
            # Make sure the file is not an events csv file
            other_csv = item.endswith("events.csv")
            if item_bool and not other_csv:
                # if it is a csv file add it to the list
                csv_files.append(item)

        # Make the list of spd_files a string so we can print it nicely
        str_list = ', '.join(str(fil) for fil in spd_files)
        if (str_list != ''):
            # Print found spd files ### Old code ("current_dir[-16:]" prints only the last 16 characters) ###
            print("Found the following .SPD files:\n (" + str_list + ") \n In directory: \n" + current_dir)
            print('\n')
        else:
            print("No files found in directory: \n" + current_dir)
            print("\n")
            print('_____________________________________________________________')
            continue
        
        # Loop through found .SPD files and call David's program on each one.
        for spd in spd_files:
            # Make sure the spd file does not already have a matching csv file
            spd_has_csv = False
            for csv in csv_files:
                #print('spd: ' + spd[:-4])
                #print('csv: ' + csv[:-4])
                #print(spd[:-4] == csv[:-4])
                #print("")
                if (spd[:-4] == csv[:-4]):
                    spd_has_csv = True
                    break
                else:
                    spd_has_csv = False
                
            if not(spd_has_csv): #and (csv_files == []):
                #print("Reading file: " + spd)
                SPD_Reader_Vic.main(spd)
                print("Finished creating csv for file: " + spd)
                print("\n")
            else:
                print(spd + ' already has a csv')
                print("\n")
        
        ############# Regular data csv code finished #############
        ############# Start events csv code here     #############
        
        # Get a list of all of the files in the current directory (again)
        files_lower2 = os.listdir(current_dir)
        #print(current_dir)
        #print(os.getcwd())
        # list of csv files in current directory
        csv_files = []       
        # csv file test
        for item in files_lower2:
            #print(item)
            # Test to see if the file is a csv file
            item_bool = item.endswith(".csv")
            # Make sure not to add files with events.csv's already created
            other_csv = item.endswith("events.csv")
            #print(item_bool)
            if item_bool and not other_csv:
                # if it is a csv file add it to the list 
                csv_files.append(item)
                
        # create dummy holding list
        holding_list  = []
        # Remove files from csv_files that also share a name with events.csv files
        for csv in csv_files:
            csv_has_events_csv = False
            for item in files_lower2: 
                #print('csv: ' + csv[:-4])
                #print('events csv: ' + item[:-11])
                #print(csv[:-4] == item[:-11])
                if (csv[:-4] == item[:-11]):
                    csv_has_events_csv = True
                    break
                else:
                    csv_has_events_csv = False
            if not csv_has_events_csv:
                holding_list.append(csv)
                
        # assign our dummy variable to the real one again
        csv_files = holding_list
        #print(csv_files)
        if (csv_files != []):        
            print("Creating events.csv files for: ")
            print(csv_files)        
            # call the events.csv function with the list of csv's
            ######## MAKE SURE THE os.chdir functions in that file point to the right place!!!
            Prediction_Data_Reader.main_func(csv_files)
            print("\n")
            print("Done creating events.csv files.")
        else:
            print("No events.csv files needed to be created")     
        print('_____________________________________________________________')



