import numpy as np
import pandas as pd
import re
import datetime




#ALL FUNCTIONS


#FUNCTION TO DIVIDE DATE AND TIME OF COLUMN 9
def datetime_divider(data):
    for i in range(len(data)):
        
        if re.match(r'^\d', str(data[i])):
            pattern = re.compile(r'\d{1,8}')
            a = pattern.findall(str(data[i]))
            data[i] = (a[0], a[1])   
        else:
            data[i]= [np.nan, np.nan] 
            
    return data            



#FUNCTION TO GET DATA IN DESIRED DATE FORMAT  
def date_modifier(data):
    for j in range(len(data)):
        
        if re.match(r'\d', str(data[j])):
            year = str(data[j][:4])
            month = str(data[j][4:6])
            day = str(data[j][6:])
            data[j] = '-'.join([year, month, day])            
        else:
            data[j] = np.nan
            
    return data

            

#FUNCTION TO GET DAT IN DESIRED TIME FORMAT
def time_modifier(data):
    for k in range(len(data)):
        
        if re.match(r'\d', str(data[k])):
            m = int(data[k][:2])
            mi = str(data[k][2:4])
            sec = str(data[k][4:])
            
            if m>= 12:
                if m == 12:
                    hr = str(m)
                else:
                    hr = str(m-12)
                merd = 'PM'
            else:
                if m == 0:
                    hr = str(12)
                else:
                    hr = str(m)
                merd = 'AM'
            
            data[k] = ':'.join([hr, mi, sec])+ ' ' + merd
        else:
            data[k] = np.nan
            
    return data
                
#abc = ['031245', '125649', '', '004526', '152412']
#time_modifier(['125649'])



#FUNCTION TO REPLACE SIMPLE WITH STANDARD TERMINOLOGY
def replace_simple_with_Standard_terminology(dataset):
    
    dataset[5] = dataset[5].replace('Originating', 'Outgoing')
    dataset[5] = dataset[5].replace('Terminating', 'Incoming')
    
    dataset[267] = dataset[267].replace('Success', 'Voice Portal')
    dataset[312] = dataset[312].replace('Shared Call Appearance', 'Second Device')
    
    return dataset



#FUNCTION TO REMOVE UNWANTED DATA IN COLUMN 312 and REPLACE WITH NAN
def remove_Unwanted_data(data):
    for i in range(len(data)):
        
        if data[i] == 'Second Device' or data[i] == 'Primary Device':
            continue
        else:
            data[i] = np.nan
        
    return data



#FUNCTION TO REPLACE NAN VALUES OF DATA1(147 COLUMN)
# replace missing data of 147 column, with create the data from 312 and 267
def combine_All_Services(data1, data2, data3):

    for i in range(len(data1)):
        if data1[i] is np.nan:
            
            if data2[i] is not np.nan and data3[i] is not np.nan:
                data1[i] = str(data2[i])+ "," + str(data3[i])
            
            elif data2[i] is not np.nan:
                data1[i] = data2[i]
            
            else:
                data1[i] = data3[i]
            
        else:
            continue
    return data1
 


# Convert data into a specific format
def call_time_fetcher(data):

    for i in range(len(data)):
        data[i] = str(data[i])
        if data[i]!="nan":
            year = data[i][:4]
            month = data[i][4:6]
            day = data[i][6:8]
            hours = data[i][8:10]
            minutes = data[i][10:12]
            seconds = str(round(float(data[i][12:])))
            if int(seconds) >= 60:
                seconds = int(seconds) -60
                minutes = int(minutes)+1 
            if int(minutes) >=60:
                hours = int(hours)+1
                minutes  = int(minutes) - 60 
            data[i] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}" 
        else:
            data[i] = np.nan
    return data



# TO GET THE HOURLY RANGE IN WHICH CALL WAS RECEIVED
def hourly_range(data):    
    for i in range(len(data)):
        data[i] = str(data[i])
        if data[i]!="nan":
            if re.search("PM", data[i]):
                time_data =  re.findall("\d+", data[i])
                if time_data[0] != "12":
                    time_data = int(time_data[0]) + 12
                else:
                    time_data = time_data[0]
                
            else:
                time_data =  re.findall("\d+", data[i])
                if int(time_data[0]) == 12:
                    time_data = f"0{int(time_data[0]) - 12}"
                else:
                    time_data = time_data[0]
                
                
            data[i] = f"{time_data}:00 - {time_data}:59"
        else:
            data[i] = np.nan
    return data



# TO GET THE WEEKLY RANGE IN WHICH CALL WAS RECEIVED
def weekly_range(data): 
    for i in range(len(data)):
        data[i] = str(data[i])
        if data[i] != "nan":
            year, month, day = [int(x) for x in data[i].split("-")]
            result = datetime.date(year, month, day)
            data[i] = result.strftime("%A")
        else:
            data[i] = np.nan
    return data












#MAIN CODE OF PROJECT
    
dataset_name = 'raw_cdr_data.csv'
raw_cdr_data = pd.read_csv(dataset_name, header = None, low_memory=False)

print(raw_cdr_data.head(5))



raw_cdr_data['date'], raw_cdr_data['time'] = zip(*datetime_divider(raw_cdr_data[9].tolist()))
raw_cdr_data['date'].head()
raw_cdr_data['time'].head()


raw_cdr_data['date'] = date_modifier(raw_cdr_data['date'].tolist())
raw_cdr_data['date'].head()


raw_cdr_data['time'] = time_modifier(raw_cdr_data['time'].tolist())
raw_cdr_data['time'].head()


# replace few names to desired names(standard)
raw_cdr_data = replace_simple_with_Standard_terminology(raw_cdr_data)
raw_cdr_data[312].unique()


# replace unwanted values of 312 with NAN
raw_cdr_data[312] = remove_Unwanted_data(raw_cdr_data[312].tolist())


print(raw_cdr_data[147])


# replace null value of 147 and replace with 312, 267
raw_cdr_data[147] = combine_All_Services(raw_cdr_data[147].tolist(),
                                             raw_cdr_data[312].tolist(),
                                             raw_cdr_data[267].tolist())






#print(raw_cdr_data['date'].tail(5)+ ' '+ raw_cdr_data['time'].tail(5) )





# to convert starttime(9) and endtime(13) to desired format
raw_cdr_data["starttime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[9].tolist()))
print(raw_cdr_data["starttime"])



raw_cdr_data["endtime"] = pd.to_datetime(call_time_fetcher(raw_cdr_data[13].tolist()))
print(raw_cdr_data["endtime"])


# find duration of call
raw_cdr_data["duration"] =  (raw_cdr_data["endtime"] - raw_cdr_data["starttime"]).astype("timedelta64[m]")
print(raw_cdr_data["duration"])



# Creates 1 hour range for 24 hours
raw_cdr_data["hourly_range"] = hourly_range(raw_cdr_data["time"].tolist())
print(raw_cdr_data["hourly_range"])



# Creates range in Week ( Monday to Sunday )
raw_cdr_data["weekly_range"] = weekly_range(raw_cdr_data["date"].tolist())
print(raw_cdr_data["weekly_range"])


# un-neccessary columns removed
raw_cdr_data = raw_cdr_data.drop("time", axis=1)
    
# Save the transformed data in CSV format for further use
raw_cdr_data.to_csv("cdr_data.csv", index = None)












