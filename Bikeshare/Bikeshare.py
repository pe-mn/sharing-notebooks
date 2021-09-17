import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city = 'chicago'
filter_type = 'month'
month, day = 1, 0


def month_check():
    while True:
        try:
            month = int(input('Which month? Please type your response as an integer (e.g., 1=january).\n'
                              'Type "all" to apply no filter\n'))
        except ValueError:
            print("\n(Please, enter an integer between 1 and 12)")
            continue
        if month in range(1, 13):
            break
        else:
            print("\n(Please, enter an integer between 1 and 12)")
            continue

    return month

def day_check():
    while True:
        try:
            day = int(input('Which day? Please type your response as an integer (e.g., 0=Monday).\n'))
        except ValueError:
            print("\n(Please, enter an integer between 0 and 6)")
            continue
        if day in range(7):
            break
        else:
            print("\n(Please, enter an integer between 0 and 6)")
            continue

    return day



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Loop until a break statement is encountered

    while True:
        # Start an error-handling block
        try:
            # Get the user input and make it an integer
            city = str(input('Would you like to see data for chicago, new york city, or washington?\n')).lower()
        # If a ValueError is raised, it means that the input was not a number
        except ValueError:
            print("Please, choose one of the cities chicago, new_york_city, or washington?")
            # So, jump to the top of the loop and start-over
            continue
        # If we get here, then the input was a number.  So, see if it equals 1 or 2
        if city in ('chicago', 'new york city', 'washington'):
            # If so, break the loop because we got valid input
            break

    while True:
        try:
            filter_type = str(input('Would you like to filter by month, day, both or not at all? \n'
                                    'Type "none" to apply no time filter.\n')).lower()
        except ValueError:
            print("Please, choose one of the filters (month, day, both, none)")
            # So, jump to the top of the loop and start-over
            continue
        # If we get here, then the input was a number.  So, see if it equals 1 or 2
        if filter_type in ('month', 'day', 'both', 'none'):
            # If so, break the loop because we got valid input
            break

    if filter_type == 'month':
        month_check()
        print('Just one moment... Loading the data')

    elif filter_type == "day":
        day_check()
        print('Just one moment... Loading the data')

    elif filter_type == "both":
        month_check()
        day_check()
        print('Just one moment... Loading the data')

    elif filter_type == "none":
        print('you chose to apply no filter ')
        print('Just one moment... Loading the data')

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day and hour from the Start Time column
    df['monthFilt'] = df['Start Time'].dt.month
    df['dayFilt'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # Apply filter to the dataframe
    if filter_type == 'month':
        filt = (df['monthFilt'] == month)
        df = df[filt]

    elif filter_type == "day":
        filt = (df['dayFilt'] == day)
        df = df[filt]

    elif filter_type == "both":
        filt = (df['monthFilt'] == month) & (df['dayFilt'] == day)
        df = df[filt]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    m = df.monthFilt.mode()[0]
    popular_month = calendar.month_name[m]
    print('What is the most popular month for travelling?\n', popular_month)

    # display the most common day of week
    d = df.dayFilt.mode()[0]
    popular_day = calendar.day_name[d]
    print('What is the most popular day for travelling?\n', popular_day)

    # display the most common start hour
    popular_hour = df.hour.mode()[0]
    print('What is the most popular hour of the day to start your travels?\n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('What is the most popular start station?\n', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('What is the most popular End station?\n', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = (df['Start Station'] + ' ' + df['End Station']).mode()[0]
    print('What is the most popular Trip?\n', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    travel_time = df['Travel Time'].sum()
    print('The total travel time: ', travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What is the breakdown of users?')
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    print('\nWhat is the breakdown of gender?')

    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    else:
        print('No gender data to share.')

    """ I don't understand why when I choose washington the code inside the if statement runs ! """
    #if city in ('chicago', 'new york city'):
        #gender_count = df.value_counts()
        #print(gender_count)
    #else:
        #print('No gender data to share.')

    # Display earliest, most recent, and most common year of birth
    print('\nWhat is the oldest, youngest, and most popular year of birth?')
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        popular = df['Birth Year'].mode()[0]
        print(f'oldest: {oldest}   youngest: {youngest}   most popular: {popular} ')
    else:
        print('No birth year data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        i = 0
        while True:
            raw_data = str(input('Would you like to display 5 lines of raw data? (yes/ no)\n')).lower()
            if raw_data in ('yes', 'y'):
                print(df.iloc[i:i+5])
                i += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
