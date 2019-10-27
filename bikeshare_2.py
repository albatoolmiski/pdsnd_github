import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    while True:
        try:
            city = input("Enter the name of the city (chicago, new york city, washington): ").lower()
        except:
            print('\nNot a valid city, please try again!')
            continue

        if city not in ('chicago', 'new york city', 'washington'):
            print('\nPlease, try again')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input(\
            '\nSelect a month:\nAll, January, February, March, April, May, June\nYour selection: ')\
            .lower()
        except:
            print('\nPlease try again!')
            continue

        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('\nplease, try again')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input(\
            '\nSelect a day:\nAll, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\nYour selection: ')\
            .lower()
        except:
            print('\nplease try again!')
            continue

        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('\nPlease, try again')
            continue
        else:
            break

    print('-' * 40)
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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:',  most_common_month)
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:',  most_common_day_of_week)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:',most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_Station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', start_Station)
    # display most commonly used end station
    end_Station = df['End Station'].mode()[0]
    print('Most Common End Station:', end_Station)

    # display most frequent combination of start station and end station trip
    df['Combination Station'] = df['Start Station'] + '/' + df['End Station']
    print('Most Frequent Trip Station Combination:', df['Combination Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_Type_Counts = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_Type_Counts)
    print('\n')
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_Counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_Counts)
    else:
        print('\nGender column not available in the city you entered to provide the data')
    print('\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliestYear = int(df['Birth Year'].min())
        recentYear = int(df['Birth Year'].max())
        commonYear = int(df['Birth Year'].mode()[0])

        print('Earliest: {}, most recent: {}, and most common year of birth: {}'.format(earliestYear, recentYear,
                                                                                        commonYear))
    else:
        print('The city you selected does not have Birth Year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# Shows raw data to the users
def displayRawData(cityName):
    raw_data = pd.read_csv(CITY_DATA[cityName])
    data_count = 5
    while True:
        try:
            print(raw_data.iloc[:data_count, :raw_data.shape[1]])
            requestData = input('\nDo you want to see more raw data for the city you selected?\n')
        except:
            continue

        if requestData.lower() == 'yes':
            data_count = data_count + 5
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

        rawData = input('\nWould you like to view the raw data of the city you selected?\n')
        if rawData.lower() != 'yes':
            break
        else:
            displayRawData(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
