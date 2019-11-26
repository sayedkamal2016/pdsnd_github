import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def filters():

    # getting the city input
    while True:
        try:
            city = input('insert which city you eant to examine >> ').lower()

            if city in city_data:
                print('ok, let\'s go on')
                break
            elif city not in city_data:
                print('city is not in our list, retry and check the name')

        except:

            pass

    # getting month input

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        try:
            month = input('if you want to filter data by a specific month, please inter month name, if not enter (all)\n ').lower()

            if month in months:
                print('ok let\s do it')
                break
            elif month not in months:
                print('wrong intery, please recheck')


        except:
            pass



    # getting day name
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            day = input('one final thing, do you want to filter data by specific day? if not inter (all)\n').lower()

            if day in days:
                print('ok, let\'s do the magic')
                break
            elif day not in days:
                print('wrong entery. please recheck')
        except:

            pass

    return city,month,day

def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # use the index of the day list to get the corresponding int

        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    common_month = months[common_month - 1]
    print('The most common month is: ', common_month.title())


    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day is: ', common_day)


    # the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_hour = df['start_hour'].mode()[0]
    if common_hour > 12:
        pm = common_hour - 12
        print('\nThe most common hour is: {} PM '.format(pm))
    else:
        print('\nThe most common hour is: {} AM '.format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))


    print('*'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_s_station = df['Start Station'].mode()[0]
    print('The most common used start station is: ' , common_s_station )

    # display most commonly used end station
    common_e_station = df['End Station'].mode()[0]
    print('\nThe most common used end station is: ' , common_e_station )

    # display most frequent combination of start station and end station trip
    df['start_end_stations'] = 'from ' + df['Start Station'] + ' station ' + 'to ' + df['End Station'] + ' station.'
    common_trip = df['start_end_stations'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip is the trip:\n\n ' , common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    hours = int(total_time // 60)
    minutes = int(total_time % 60)
    print('The total travel time is: {}  hours and {} minutes '.format(hours , minutes))
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    m_hours = int(mean_time // 60)
    m_minutes = int(mean_time % 60)

    print('\nThe mean travel time is: {} hours and {} minutes'.format(m_hours ,m_minutes ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users_count = df['User Type'].value_counts()

    subs_count =  users_count.iloc[0]

    print('There are {} Subscriber-type users'.format(subs_count))

    cust_count = users_count.iloc[1]
    print('\nThere are {} Customer-type users'.format(cust_count))

    null_count = df['User Type'].isnull().sum()

    print('\nThere are {} non-type users'.format(null_count))

    ind_count = df['User Type'].size - (null_count + cust_count  + subs_count)
    print( '\nThere are {} independant-type users'.format(ind_count))

    # Display counts of gender
    print ('\n Getting Gender Data ...')
    if 'Gender' in df.columns:

        # Display counts of gender
        gender_type_count = df['Gender'].value_counts()

        male_count = gender_type_count.iloc[0]
        print('\nThere are {} males'.format(male_count))

        female_count = gender_type_count.iloc[1]
        print('\nThere are {} females'.format(female_count))

        nogender_type_count = df['Gender'].isnull().sum()
        print('\nThere are {} unidentified genders'.format(nogender_type_count))

    else:
        print('Gender information is not available for this city')


    print ('\n Getting Birth year Data Data ...')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # earliest year
        er_year = df['Birth Year'].min()
        print('\nThe earliest year of birth is: ' , int(er_year) )

        #recent year
        re_year = df['Birth Year'].max()
        print('\nThe most recent year of birth is: ' , int(re_year) )

        #most common year of birth
        comm_year = df['Birth Year'].mode()[0]
        print('\n The most common year of birth is: ' , int(comm_year) )

    else:
        print('Birth year information is not available for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_to_display(df):
    lis = ['yes' , 'no']
    start = 0
    end = 5
    while True:
        try:
            prompt = input('Do yo wish to display some row data?').lower()

            if prompt == lis[0]:

                df2 = df.iloc[start:end]
                print('\nhere are five rows of data\n', df2)
                start += 5
                end +=5
            elif prompt == lis[1]:
                break

            else:
                print('Wrong entry please inter yes or no')
        except:

            pass




def main():
    while True:
        city, month, day = filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_to_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
