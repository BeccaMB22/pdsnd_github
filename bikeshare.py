import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Text Format Variables
text_col_red='\033[95m'
text_col_blue='\033[94m'
text_normal='\033[0m'
text_bold='\u001b[1m'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington).
    while True: #to handle invalid inputs
        try:
            city_input=input('Which city of the following ones do you want to analyse: {}Chicago, New York City or Washington?{}\n Please enter the city name: '.format(text_col_blue,text_normal))
            city=city_input.lower().strip(' ')
            if city=='chicago' or city=='new york city' or city=='washington':
                break
            else:
                print(text_col_red+'This city cannot be analysed. Please pay attention to the correct spelling and spaces.'+text_normal)
        except:
            print(text_col_red+'!!!! That\'s not the right input for this filter! Please write a city name!'+text_normal)

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month_input=input('Is there a spezific month between {}january and june{} you want to analyse or {}all{} of them?\n Please enter: '.format(text_col_blue,text_normal,text_col_blue,text_normal))
            month=month_input.lower().strip(' ')
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            if month in months or month=="all":
                break
            else:
                print(text_col_red+
                      'This month cannot be analysed. Please pay attention to the correct spelling. Data is only available for Januar till June'
                      +text_normal)
        except:
            print(text_col_red+'!!!! That\'s not the right input for this filter! Please write a month, e.g. January!'+text_normal)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_input=input('Is there a spezific weekday (e.g. {}Monday{} you want to analyse or {}all{} of them?\n Please enter: '.format(text_col_blue,text_normal,text_col_blue,text_normal))
            day=day_input.lower().strip(' ')
            weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday']
            if day in weekdays or day=="all":
                break
            else:
                print(text_col_red+'This weekday cannot be analysed. Please pay attention to the correct spelling.'+text_normal)
        except:
            print(text_col_red+'!!!! That\'s not the right input for this filter! Please write a weekday, e.g. Monday!'+text_normal)

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month #e.g. 1=Jan
    df['day_of_week'] = df['Start Time'].dt.weekday_name #e.g. Sunday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1 #+1 because Index Jan=0 but Jan should be 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    return df

def see_raw_data(df):
    row_count=0 #start Value = first 5 rows
    while True and (row_count+5)<len(df.index):
        try:
            next_row_input=input('Do you want to see the next 5 rows of raw data?\n Please enter yes or no: ')
            next_row=next_row_input.lower().strip(' ')
            if (row_count+5)<=len(df.index): # query
                if next_row=='yes':
                    print(df.iloc[row_count:row_count+5])
                    row_count+=5
                elif next_row=='no':
                    break
                else:
                    print(text_col_red+'That\'s not the right input! Please write yes or no!'+text_normal)
            else:
                print(df.iloc[row_count:])
        except:
            print(text_col_red+'!!!! That\'s not the right input! Please write yes or no!'+text_normal)
    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (df)    df - Pandas DataFrame containing city data filtered by month and day
    """

    print(text_bold+'\nCalculating The Most Frequent Times of Travel...\n'+text_normal)
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create 1 new column: start hour (extract from the Start Time column)
    df['Start Hour'] = df['Start Time'].dt.hour

    # find the most popular Times:
    # Month
    popular_month =df['month'].mode()[0]
    # Day
    popular_weekday=df['day_of_week'].mode()[0]
    # Start Hour
    popular_hour=df['Start Hour'].mode()[0]
    print('Most common...\n month: {}\n day: {}\n hour: {}'.format(popular_month,popular_weekday,popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
        Args:
        (df)    df - Pandas DataFrame containing city data filtered by month and day"""

    print(text_bold+'\nCalculating The Most Popular Stations and Trip...\n'+text_normal)
    start_time = time.time()

    # display most commonly used start station
    popular_st_station=df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination']='starts at '+df['Start Station']+' and ends at '+df['End Station']
    frequ_combi=df['Combination'].mode()[0]

    print('Most common...\n Start Station: {}\n End Station: {}\nThe most frequent trip {}.'
          .format(popular_st_station,popular_end_station,frequ_combi))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
       Args:
        (df)    df - Pandas DataFrame containing city data filtered by month and day"""

    print(text_bold+'\nCalculating Trip Duration...\n'+text_normal)
    start_time = time.time()

    # TO DO: display total travel time
    trav_time=df['Trip Duration'].values
    trav_time_total_hour=round(trav_time.sum()/3600,1) #in hours
    trav_time_av_min=int(trav_time.mean()/60) #in min
    trav_time_av_sec=int(trav_time.mean()%60) #Rest in Sec

    # TO DO: display mean travel time
    print('During the chosen period, the total travel time was {} hours.\nOne trip lasts on average {}min {}sec.'
          .format(trav_time_total_hour,trav_time_av_min,trav_time_av_sec))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
       Args:
        (df)    df - Pandas DataFrame containing city data filtered by month and day
        (str)   city - name of the city to analyze"""

    print(text_bold+'\nCalculating User Stats...\n'+text_normal)
    start_time = time.time()

    # Display counts of user types
    user_type_count=df['User Type'].unique().size

    if city!='washington': # only available for NYC and Chicago
        # Display counts of gender
        gender_count=df['Gender'].dropna().unique().size

        # Display earliest, most recent, and most common year of birth
        year_min=int(df.nsmallest(1,'Birth Year')['Birth Year'].values[0])
        year_max=int(df.nlargest(1,'Birth Year')['Birth Year'].values[0])
        year_common=int(df['Birth Year'].dropna().mode()[0])

        text_gender_year='The users have {} types of gender.\n{} is the earliest,\n{} is the most recent and\n{} is the most common Birth Year'.format(gender_count,year_min,year_max,year_common)
    else:
        text_gender_year='For Washington there are no information about the users gender and birth year.'

    print('There are {} types of users.\n'.format(user_type_count)+text_gender_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        print('Hello! Let\'s explore some US bikeshare data!')
        filter_ok='no'
        while filter_ok=='no':  # set filters
            city, month, day = get_filters()
            while True:
                try:
                    filter_ok_input=input('Do you want to filter by: \nCity: {}\nMonth: {}\nWeekday: {}? \n Please enter yes or no: '
                            .format(city.title(),month.title(),day.title()))
                    filter_ok=filter_ok_input.lower().strip(' ')
                    if filter_ok=='yes' or filter_ok=='no':
                        break
                    else:
                        print(text_col_red+'That\'s not the right input! Please write yes or no!'+text_normal)
                except:
                    print(text_col_red+'!!!! That\'s not the right input! Please write yes or no!'+text_normal)
        print('-'*40)

        df = load_data(city, month, day) #load and filter data
        see_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
