import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) and make sure the input is in lower case.
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('\nSorry, I didn\'t get that. please try again.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june) and make sure the input is in lower case.
    while True:
        month = input('\nWhich month would you like to filter by? January, February, March, April, May, June or type \'all\' if you do not have any preference?\n').strip().lower()
        #Return an invalid statement if the inputed txt not as listed
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('\nSorry I didn\'t get that. Please try again.\n')
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday) and make sure the input is in lower case.
    while True:
        day = input('\nWhich day of the week would you like to filter by? Sunday, Monday, Tuesday ... Saturday or type \'all\' if you don\'t have any preference?\n').strip().lower()
        #Return an invalid statement if the inputed txt not as listed
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print('\nSorry I didn\'t get that. Please try again.\n')
            continue
        else:
            break


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract day from the Start Time column to create a week day column
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month) + 1
   
       # filter by month to create the new dataframe
       df = df[df['month'] == month]

   # filter by day of week if applicable
    if day != 'all':
       # filter by day of week to create the new dataframe
       df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # The code will display the most common month by using mode()
    popular_month = df['month'].mode()[0]
    print('\nThe most common month: ', popular_month)


    # The code will display the most common day of the week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week: ', popular_day_of_week)


    # The code will display the most popular start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print('\nThe most common used start station: ', most_common_start_station)


    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print('\nThe most common end station: ', most_common_end_station)


    # display most frequent combination of start station and end station trip
    #group the results by start station and end station
    combination_station = df.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = combination_station['Trip Duration'].count().max()
    most_freq_trip = combination_station['Trip Duration'].count().idxmax()
    print('\nThe most common used combination of start station and end station trip: {}, {}'.format(most_freq_trip[0], most_freq_trip[1]))
    print('\nCount of trips: ', most_freq_trip_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_to_str(total_seconds):
    """ Converts seconds to human readble format 
        
        Args:
            (int) total_seconds - number of seconds to be converted
        Returns:
            (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
        """
        
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    
    day_hour_str = ''
    if weeks > 0:
        day_hour_str = day_hour_str + '{} weeks, '.format(weeks)
    if days > 0:
        day_hour_str = day_hour_str + '{} days, '.format(days)
    if hours > 0:
        day_hour_str = day_hour_str + '{} hours, '.format(hours)
    if minutes > 0:
        day_hour_str = day_hour_str + '{} minutes, '.format(minutes)
    
    """always show the seconds when total more than 1 minute"""
    if seconds > 59:
        day_hour_str = day_hour_str + '{} secondes, '.format(seconds)
        
    return day_hour_str

        

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    #print the complete time in seconds
    print('\nTotal travel time: ', total_travel_time, ' seconds')
    #print the travel time in human readble format
    print('\nActual total tavel time:', convert_to_str(total_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    #print the complete time in seconds
    print('\nMean travel time: ', mean_travel_time, ' seconds')
    #print the travel time in human readble format
    print('\nActual mean travel time: ', convert_to_str(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCount of user types:\n', user_types)


    # Display counts of gender
    """Display the count of each type of genders.
       If there is no data display a message"""
    try:
        gender_types = df['Gender'].value_counts()
        print('\nCount of genders:\n', gender_types)
    except:
        KeyError('\nCount of genders:\nThe data only available for NYC and Chicago.')


    # Display earliest, most recent, and most common year of birth
    """Display the earlies, most recent, and most common birth year.
       If there is no data display a message"""
    try:
        earliest_year = df['Birth Year'].min()
        print('\nThe earliest birth year: ', earliest_year)
    except:
        KeyError('\nThe earliest birth year:\nThe data only available for NYC and Chicago.')

    try:
        recent_year = df['Birth Year'].max()
        print('\nThe most recent birth year: ', recent_year)
    except:
        KeyError('\nThe most recent birth year:\nThe data only available for NYC and Chicago.')
        
    try:
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('\nThe most common birth year: ', most_common_birth_year)
    except:
       KeyError('\nThe most common birth year:\nThere\'s no data available for this month.')
       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    
    """
    Ask if the user would like to view 5 rows of the data.
    Display the requested 5 rows then ask again if they would like to see 5 more.
    Continue asking until the user enter no.
        
    Returns:
        df - 5 rows of the selected city
    """
    print('\nRaw data is available...\n')
    
    show_row = 5
    start_row = 0
    end_row = show_row - 1
    
    while True:
        
        display_data = input('\nWould you like to view 5 raw data? Enter yes or no.\n').strip().lower()
        if display_data == 'yes':
            """Display show_row number of rows, but display to the user as a string from row as 1
               For example: if start_row = 0 and end_row = 5, display to the user as 'row 1 to 5"""
            print('\nDisplaying rows from {} to {}:'.format(start_row + 1, end_row + 1))
            print('\n', df.iloc[start_row : end_row + 1])
            start_row = start_row + show_row
            end_row = end_row + show_row
            continue
        else:
            break
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
