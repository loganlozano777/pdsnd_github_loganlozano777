import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(): #when it says get_filters, it means the parameters for the load_data function
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(('/'*40),'\n' + ('/'*40))
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['chicago', 'new york city', 'washington']
    months = [ 'january', 'february', 'march', 'april', 'may', 'june','all']
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    # TO DO: get user input for city (chicago, new york city, washington). 
    global city
    city = input('Enter city: ').lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter month (january - june): ').lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the day of the week: ').lower()

    #HINT: Use a while loop to handle invalid inputs
    while (city not in cities) or (month not in months) or (day not in days_of_week):
        if (city not in cities):
            print('\n', 'Please enter the correct city. ', sep = '')
            city = input('Enter city: ').lower()
        elif (month not in months):
            print('\n', 'Please enter the correct month. ', sep = '')
            month = input('Enter month (january - june): ').lower()
        elif (day not in days_of_week):
            print('\n', 'Please enter the correct day of the week. ', sep = '')
            day = input('Enter the day of the week: ').lower()

    print(('/'*40) + '\n' + ('/'*40) + '\n')

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
#     print(CITY_DATA[city]) #tested to see if I got correct city
    df = pd.read_csv('./' + CITY_DATA[city]) 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract the month and day
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable # I used part of Udacity practice problem #3 here
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day to create new filtered dataframe
    if day != 'all':
        df = df[df['day'] == day.title()]
        
    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('This is the most common month: {}'.format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('This is the most common day: {}'.format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour
    most_common_hour = most_common_hour.mode()[0]
    print('This is the most common hour: {}'.format(most_common_hour))    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    These statistics include most commonly used start station, most commonly used end station, 
    and most frequent combination of start station and end station trip.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()
    # print(type(most_common_start_station)) #just checking what the type is 
    print('This is the most commonly used start station: {}'.format(most_common_start_station[0]))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()
    print('This is the most commonly used end station: {}'.format(most_common_end_station[0]))

    # TO DO: display most frequent combination of start station and end station trip
    largest_group = df.groupby(['Start Station', 'End Station'])
    group_count = largest_group.size().reset_index(name='Count')
    largest_group = group_count.nlargest(1, 'Count')
    # Since I know I'm only getting one row but two columns in return I decided to format by indicies
    print('Most frequent combination of start station and end station trip: {} and {}'.format(largest_group.values[0][0], largest_group.values[0][1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('This is the total trip duration of the stations in the city of {}: {}'.format(city, total_travel_time))  
    
    # TO DO: display mean travel time
    total_travel_time = df['Trip Duration'].mean()
    print('This is the mean trip duration of the stations in the city of {}: {}'.format(city, total_travel_time))  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Those statistics include counts of Male values, counts of female values, 
    earliest birth year, most recent birth year, and most common birth year.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    unique_user_type = df['User Type'].unique() # returns a numpy.ndarray
    for unique_value in unique_user_type:
        unique_value_count = df[df['User Type'] == unique_value].count()[0]
        print('This is the count of {}\'s: {}'.format(unique_value, unique_value_count)) 
    
    # I decided to use two if statements to keep the statistics separted to keep better readability
    # TO DO: Display counts of each gender (only available for NYC and Chicago)
    if city == 'washington':
        print('Sorry, there are no counts of gender for {}'.format(city))
    else:
        male_count = df[df['Gender'] == 'Male'].count()[0]
        female_count = df[df['Gender'] == 'Female'].count()[0]
        print('Counts for Male: {} \nCounts for Female: {}'.format(male_count, female_count))

    # TO DO: Display earliest, most recent, and most common year of birth (only available for NYC and Chicago)
    if city == 'washington':
        print('Sorry, there are no records of birth year for {}'.format(city))
    else:
        earliest = df['Birth Year'].min()
        print('This is the earliest birth year: {}'.format(earliest))
        most_recent = df['Birth Year'].max()
        print('This is the most recent birth year: {}'.format(most_recent))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('This is the most common birth year: {}'.format(most_common_birth_year))
    
def raw_data(df, batch_size=5):
    """ 
    Asks if user wants to see the raw data. 
    
    If yes, then iterate through the raw data 5 rows at a time 
    """
    user_input = input('Would you like to see the raw data of {}.csv? (5 rows at a time) \n'.format(city))
    while True:
        if user_input.lower() != 'yes':
            break
        for key, five_rows in df.groupby(np.arange(len(df)) // batch_size): #reading through pandas and numpy online documentation helped me to piece together the groupby and arange methods 
            print(five_rows)
            user_input = input('Would you like to see {} more rows?\n'.format(batch_size))

            if user_input.lower() == 'yes':
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
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
