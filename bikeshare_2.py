import time
import pandas as pd
import numpy as np
import os

CITY_DATA = { 'chicago': 'Data/chicago.csv',
              'new york': 'Data/new_york_city.csv',
              'washington': 'Data/washington.csv' }
months =["january","february","march","april","may","june"]
days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]





def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) check - holds the user choice of filter  day, month , both, or not at all
    """

    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #var check to store the choice of the user if he want to filter by day, month, both, or not at all
    city,month,day,check='','','',''
    while city not in CITY_DATA:
        try:
            city = input("please Enter city name from Chicago, New York, Washington: \n").lower()
        except Exception as e:
            print("your input is not valid!, please try again. \n \n")
            continue
        if city not in CITY_DATA:
            print("your input is not valid!, please try again. \n \n")


    print('\nYou picked ',city,'\n')
    #chcek user input for month, day, both, or none
    choices = ['none','month','both','day']
    while check not in choices :
        try:
            check = input("would you like to filter your data by month, day, both, or not all? Type 'none' for no time filter. \n ").lower()
        except Exception as e:
            print("your input is not valid!, please try again. \n \n")
            continue
        if  check not in choices:
            print("your input is not valid!, please try again. \n \n")



    # get user input for both month and day
    if check =='both'  :
        while month not in months :
            try:
                month = input("which month? January, February, March, April, May, or June \n ").lower()
            except Exception as e:
                print("your input is not valid!, please try again. \n \n")
                continue
            if  month not in months :
                print("your input is not valid!, please try again. \n \n")

        while day not in days :
            try:
                day = input("which day? please type your response as integer (e.g., 1=sunday) \n ")
                day = int(day)
                day = days[day-1]
            except Exception as e:
                print("your input is not valid!, please try again. \n \n")
                continue
            if  day not in days :
                print("your input is not valid!, please try again. \n \n")


    elif check=='month':
            while month not in months :
                try:
                    month = input("which month? January, February, March, April, May, or June \n ").lower()
                except Exception as e:
                    print("your input is not valid!, please try again. \n \n")
                    continue
                if  month not in months :
                    print("your input is not valid!, please try again. \n \n")

    elif  check=='day':
        while day not in days :
            try:
                day = input("which day? please type your response as integer (e.g., 1=sunday) \n ")
                day = int(day)
                day = days[day-1]
            except Exception as e:
                print("your input is not valid!, please try again. \n \n")
                continue
            if  day not in days :
                print("your input is not valid!, please try again. \n \n")

    else:
        month = check
        day = check


    print('-'*40)
    return city, month, day, check


def load_data(city, month, day,check):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) check -holds the user choice of filter  day, month , both, or not at all
    Returns:
        df - Pandas DataFrame containing city data filtered by month, day, both, or no filter
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    #converting start time to datetime
    df['Start Time']= pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    #extracting day name of the start time note: method weekday_name didn't work so I used day_name()
    df['day_of_week']= df['Start Time'].dt.day_name()

    # if the user choose to filter by both day and month
    if check == 'both':
        month = months.index(month)+1
        day = day.title()
        df = df[ (df['month']==month) & (df['day_of_week']== day)]

    # if the user choose to filter by month
    elif month != 'none' and month!= '':
        month = months.index(month)+1
        df = df[df['month'] == month]
    # if the user choose to filter by day
    elif day != 'none' and day !='':
        day = day.title()
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print("Most common month: ",months[df['month'].mode()[0]-1])

    # display the most common day of week
    print("Most common day of the week: ",df['day_of_week'].mode()[0])


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common hour in the day: ",df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used Start station: ",df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most commonly used End station: ",df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start & End']=df['Start Station']+" 'AND' "+df['End Station']
    print("Most frequent combination of Start and end station: ",df['Start & End'].mode()[0])




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Duration in minutes'] = df['Trip Duration']/60
    print('Total Duration time in minutes: ' ,  df['Duration in minutes'].sum())


    # display mean travel time
    print("Avg Duration time: ", df['Duration in minutes'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Types:\n",df['User Type'].value_counts(),'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Count of Gender : \n",df['Gender'].value_counts(),'\n')
    else:
        print('no Gender data to share\n')


    # Display earliest, most recent, and most common year of birth
    print('What is the oldest, youngest, and popular year of birth, respectively?')
    if 'Birth Year' in df.columns:
        print(int(df['Birth Year'].min()),", ",int(df['Birth Year'].max()),", and ",int(df['Birth Year'].mode()[0]))
    else:
        print('no Birth Year to share\n')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display():
    """ Displays all the fucntions outputs and take user inputs and handle it"""
    city,month,day,check=get_filters()
    df= load_data(city,month,day,check)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    print('-'*40)
    print('-'*40)
    # str to store user input if he wants to see some raw data or not
    option= ''
    #index for get 5 raws from the DataFrame each time the user enter yes
    cnt=0
    df['Start Time'] = df['Start Time'].dt.strftime("%m/%d/%Y %H:%M:%S")
    while True:
        try:
            option = input("Would you like to see individual trip data? Type 'Yes' or 'No'. \n").lower()

        except Exception as e:
            print("your input is not valid!, please try again. \n")
            continue
        if option !='yes' and option!='no':

            print("your input is not valid!, please try again. \n")
            continue
        elif option =='yes':
            #check if cnt ig going to be eqaul to the size of the actual dataframe
            if (cnt+5) == df.shape[0]:
                print('There are no data to share.\n')
                break
            else:
                trip_data = df[cnt:cnt+5].to_dict('records')
                cnt+=5
            print('\n')
            for record in trip_data:
                print(record,'\n')
            continue
        else:
            break
    print('-'*40)



def main():
    display()
    # str to store user input if he wants to start the program again or not
    restart=''
    print('\n')
    while True:
        try:
            restart = input("Would you like to start again? Type 'Yes' or 'No'. \n").lower()
        except Exception as e:
            print("your input is not valid!, please try again. \n")
            continue

        if restart !='yes' and restart!='no':
            print("your input is not valid!, please try again. \n")
            continue
        elif restart =='yes':
            os.system('clear')
            display()
        else:
            break




if __name__ == "__main__":
	main()
