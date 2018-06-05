
'''
This example reads a Radio Skypipe data file, with single data channel (the default)
This reads and prints the raw header info, and then reads and displays the first 
    1000 time/value records
    
Note: command line argument is the file spec.
'''


'''
Type SkyPipeHeader
     version As String * 10
     Start As Double 
     Finish As Double
     Lat As Double
     Lng As Double
     MaxY As Double
     MinY As Double
     TimeZone As Integer
     Source As String * 10
     Author As String * 20
     LocalName As String * 20
     Location As String * 40
     Channels As Integer
     NoteLength As Long
 End Type
 '''



import struct
import sys
import os
import csv
import math
from datetime import datetime, timedelta


def main(spd):
#    if len(sys.argv) < 2:
#        print ('No file Specified')
#        return

    # Change a string that ends in .spd to end in .csv
    def spd_to_csv(file_name):
        new_str = file_name[:-3]
        new_str = new_str + "csv"
        #print("The new file name is: " + new_str)
        return new_str
    
    # Taken from stack overflow 
    # https://stackoverflow.com/questions/29387137/how-to-convert-a-given-ordinal-number-from-excel-to-a-date
    def from_excel_ordinal(ordinal, epoch=datetime(1900, 1, 1)):
        # Adapted from above, thanks to @Martijn Pieters 
    
        if ordinal > 59:
            ordinal -= 1  # Excel leap year bug, 1900 is not a leap year!
        inDays = int(ordinal)
        frac = ordinal - inDays
        #inHours = int(round(frac*24))
        #inMin = int(round(frac*24*60))
        #inSecs = int(round(frac * 86400.0))
        inSecs = float(frac * 86400.0)
        #inMilli = round((inSecs-math.trunc(inSecs))*1000)
    
        return epoch + timedelta(days=inDays - 1, seconds=inSecs)
    
    filename = spd
    print ('Processing Filename:', filename)

    osstat = os.stat(filename)
    filesize =  osstat.st_size
    #print ('File Size:', str(filesize))


    # Find out what byte order your system uses
    #print("Native byteorder: ", sys.byteorder)
            
    
    br = BinaryReader(filename) 
    try:
        # read the header
        # https://docs.python.org/3/library/struct.html

        length = 0

        header_field_names = (
            'version', 'start', 'finish', 'lat', 'lng', 'maxy', \
            'miny', 'timezone', 'source', 'author', 'localname', \
            'location', 'channels', 'notelength')
                
        # read header 
        format_string = '< 10s d d d d d d h 10s 20s 20s 40s h i';
        data_size = struct.calcsize(format_string)
        length += data_size
        header_tuple = br.readfields(format_string, data_size)
        
        hdr_dict = dict(  zip(header_field_names, header_tuple) )
    
        # print header info 
#        for k, v in hdr_dict.items():
#            print (k, v)
        
        # read notes
        notelength = hdr_dict.get('notelength')
        length += notelength
        format_string = '< %is' % (notelength)
        
        # print notes
        # ***** DO NOT COMMENT OUT THE LINE BELOW!!! IT MESSES WITH THE DATES AND VALUES! *****
        notes_tuple = br.readfields(format_string, notelength)
        #notes = 'Notes: %s' % (notes_tuple[0])
        #print (notes)
        
        # read data
        record_count = (filesize - length)/16;
        #print ('Record count: ', record_count)
        
        # Count for number of data (time/value) seen
        count = 1
        
        # Create list to hold time and data values
        data_list = []

        
        int_record_count = int(record_count)
        #print("int_record_count: %f" %int_record_count)
        
        record_format_num = int_record_count/2
        #print("record_format_num: %f" %record_format_num)
        
        record_format_str = str(record_format_num)
              
        ############################################################
        # Test code
        
        # We get the *4 from:
        # 790713/197678 = 4
        # where 790713 = int_record_count
        # and 197678 = was the final count gotten without the *4
        record_format_num = (int_record_count * 4/2)
        #print("record_format_num: %f" %record_format_num)
        
        record_format_str = str(record_format_num)
        
        
        ############################################################
        
        # read record in batches (read the first batch)
        batch_size = 1000
        data_size = batch_size * 16
        format_string = '< '+ record_format_str + 'd'
        
        # old code
        #data_tuple = br.readfields(format_string, data_size_multiplier*data_size)
        
        # I am guessing the *8 is because each one is 8 bits?
        data_tuple = br.readfields(format_string, record_format_num*8)
        
        for x in range(0, record_format_num, 2):
            d1 = data_tuple[x]
            d2 = data_tuple[x+1]
            # Add data to list
            data_list.append([d1,d2])
            # print data
            #print ("%f - Date/value: %f, %f" % (count,d1, d2))
            
            count = count + 1
            
            
        ### Test outputs ******************************************************
        #print("Date: %f" %(data_list[0][0]))
        #print("value: %f" %(data_list[1000][1]))
        
        # The final count value should be equal to record_count+1
        #print("Final record count value is: %f" %count-1)
        #print("Final Date: %f" %(data_list[count-2][0]))
        #print("Final value: %f" %(data_list[count-2][1]))
        
        # If the amount of records does not match the found records print error!
        if (int_record_count != count-1):
            print("***** Warning! The amount of records initially found does not match the amount of counted records *****")
        
        ###********************************************************************
        
        
#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$##$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$
#
# To get an acutal date from the date here use excels serial converter
# Go to Format -> Format Cells -> Custom -> Then under "Type:" enter
# m/d/yyyy h:mm:ss.000 AM/PM where the ".000" is for milliseconds
#
# ALSO NOTE: EXCEL CHANGES THE DATA TO WHAT IT THINKS YOU WANT!!!
# DO **NOT** USE EXCEL TO LOOK AT THE REAL DATES/TIMES!!!
#
#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$##$#$#$#$#$#$#$#$#$#$#$#$#$#$#$#$
        
        csv_name = spd_to_csv(spd)
        with open(csv_name,'wb') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Date (serial)","Value","Date (regular)"])
            
            for x in range(0, count-1):
                #print("Date: %f" %(data_list[x][0]))
                #print("value: %f" %(data_list[x][1]))
                d1 = data_list[x][0]
                d2 = data_list[x][1]
                
                # from stack overflow see function floatHourToTime
                pyDT = from_excel_ordinal(d1)
                writer.writerow([d1, d2, pyDT])
            
            # Close the file!!!
            csv_file.close()
                
            
    
    except BinaryReaderEOFException: 
        # One of our attempts to read a field went beyond the end of the file. 
        print ('Error: File seems to be corrupted.')
        

    




class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'

class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        'int8'   :'b',
        'uint8'  :'B',
        'int16'  :'h',
        'uint16' :'H',
        'int32'  :'i',
        'uint32' :'I',
        'int64'  :'q',
        'uint64' :'Q',
        'float'  :'f',
        'double' :'d',
        'char'   :'s'}

    # class constructor
    def __init__(self, fileName):
        #print('BinaryReader Constructor...')
        self.file = open(fileName, 'rb')
        return;

    # read a piece of data    
    def read(self, typeName):
        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.file.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)[0]

    # read a bunch of fields at once
    def readfields(self, format_string, size):
        # see https://docs.python.org/3/library/struct.html                
        data = self.file.read(size)
        datalist = struct.unpack(format_string, data)

        return datalist


    def __del__(self):
        #print('BinaryReader Destructor...')
        self.file.close()

        
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
    
