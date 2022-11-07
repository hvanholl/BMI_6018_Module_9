
##### -------- Hannah Van Hollebebeke, u0697848 --------- ####
##### ---- BMI_6018, Homework 5 Pandas Data Cleaning ---- ####

#%% Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%% Importing Data
flights = pd.read_csv('flights.csv')
flights.head(10)
weather = pd.read_csv('weather.csv')
weather_np = weather.to_numpy()

#%% Pandas Data Filtering/Sorting Question Answering

##### ----------- use flights_data ------------- ####

#Question 1 How many flights were there from JFK to SLC? Int
    # Filter for rows that have 'origin' column as JFK AND 'dest' as SLC
q_1 = flights.loc[(flights['origin'] == 'JFK') & (flights['dest'] == 'SLC')]
print(f'Question 1: {len(q_1)} flights come from JFK to SLC out of {len(flights)} total')
print(q_1[['origin', 'dest']].head(5))

#Question 2 How many airlines fly to SLC? Should be int
    # first filter for SLC 'dest' then count unique values in 'carrier' column 
q_2 = pd.unique(flights['carrier'][flights['dest'] == 'SLC'])
print(f'Question 2: {len(q_2)} airlines fly to SLC of {len(pd.unique(flights["carrier"]))} total')

#Question 3 What is the average arrival delay for flights to RDU? float
    # filter for RDU 'dest' and take mean of 'arr_delay'
    # Round to 2 decimal places so it is easier to read
q_3 = flights['arr_delay'][flights['dest'] == 'RDU'].mean().round(2)
print(f'Question 3: The mean arrival delay for flights to RDU is {q_3} minutes')

#Question 4 What proportion of flights to SEA come from the two NYC airports (LGA and JFK)?  float
    # filter for SEA flights and count rows for denominator
    # count 'origin' values if LGA -OR- JFK for numerator
sea = flights.loc[flights['dest'] == 'SEA']  # create new df with only seattle destinations
num = len(sea.loc[((sea['origin'] == 'LGA') | (sea['origin'] == 'JFK'))]) # filter seattle df for specified origins and count the length
q_4 = num/len(sea)    # The proportion is the length of the filtered seattle df/the length of the full seattle df
print(f'Question 4: The proportion of flights coming from JFK or LGA (n = {num}) of all seattle flights (n = {len(sea)}) is {round(q_4, 2)*100}%')

#Question 5 Which date has the largest average depature delay? Pd slice with date and float
#please make date a column. Preferred format is 2013/1/1 (y/m/d)
    # use to_datetime method, specify the column names to use and use strftime to custom format the date
    # default format is yyyy-mm-dd. the # in front of onth and day will remove leading zeros for windows
flights['date'] = pd.to_datetime(flights[['year', 'month', 'day']]).dt.strftime('%Y/%#m/%#d') 
    # groupby date and sort, take mean of each date for dep_delay, select the largest values (argument is # values to return)
dep_delay_mean = flights.groupby('date', sort = True)['dep_delay'].mean().nlargest(1) 
q_5 = str(dep_delay_mean.index[0])     # convert the resulting series to just the date
print(f'Question 5: The largest average departure delay occurred on {q_5}')

#Question 6 Which date has the largest average arrival delay? pd slice with date and float
arr_delay_mean = flights.groupby('date', sort = True)['arr_delay'].mean().nlargest(1) 
q_6 = str(arr_delay_mean.index[0])     # convert the resulting series to just the date
print(f'Question 6: The largest average departure delay occurred on {q_6}')

#Question 7 Which flight departing LGA or JFK in 2013 flew the fastest? pd slice with tailnumber and speed
#speed = distance/airtime
    # The dataset already only contains data from 2013
lga_jfk = flights.loc[((flights['origin'] == 'LGA') | (flights['origin'] == 'JFK'))]# filter seattle df for specified origins
lga_jfk['speed'] = lga_jfk['distance']/lga_jfk['air_time']   # Add column calculating the speed
q_7 = lga_jfk['tailnum'][lga_jfk['speed'] == lga_jfk['speed'].max()]   # find the maximum value for speed and select the tailnum at that row
print(f'Question 7: The fastest flight from LGA or JFK was tailnum{q_7.values}')

#Question 8 Replace all nans in the weather pd dataframe with 0s. Pd with no nans
q_8 = weather.fillna(0)   # use fillna method on whole dataframe with argument 0 to specify what to replace with
print(weather[16:19]['pressure'])   
print(q_8[16:19]['pressure'])   # There were some NaN values in these rows in the pressure column so this is to verify that they were replaced
print(f'Question 8: The NaN values were replaced with zeros. Examples that changed are printed above')

# Run as needed to get the column names
# print(q_8.columns)

#%% Numpy Data Filtering/Sorting Question Answering
#Use weather_data_np
#Question 9 How many observations were made in Feburary? Int
all_2013 = len(weather_np)  # total number of rows in df, or total observations
feb = weather_np[weather_np[:, 3] == 2.0]   # Select rows where month is Feb (2.0)
feb_count = len(feb[:, 0:4])   # count filtered observations
print(f'Question 9: {feb_count} weather observations were made in February out of {all_2013} total')

#Question 10 What was the mean for humidity in February? Float
q_10 = np.mean(feb[:, 8])    # use np method mean on the df filtered for feb select column index 8 for humidity
print(f'Question 10: The mean humidity in Feb was {round(q_10, 2)}%')

#Question 11 What was the std for humidity in February? Float
q_11 = np.std(feb[:, 8])   # Repeat above but with st. dev (std) instead
print(f'Question 11: The standard deviation of the humidity in Feb was {round(q_11, 2)}%')
