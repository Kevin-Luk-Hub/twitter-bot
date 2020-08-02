import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime, timedelta
from logger import *
from bs4 import BeautifulSoup
import requests


def get_previous_dates():
    start_date = date.today() - timedelta(days=1)
    end_date = date(2020, 4, 13)
    delta = start_date - end_date
    dates = []

    for i in range(delta.days + 1):
        day = start_date - timedelta(days=i)
        dates.append(day.strftime('%m-%d-%Y'))

    return dates


def getCovidData(state):
    raw_files = []
    dates = get_previous_dates()

    logging.info('Retrieving data from GitHub for the state of {}'.format(
        state.capitalize()))

    for i in range(0, len(dates)):
        raw_files.append(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv".format(dates[i]))

    df_list = [pd.read_csv(file) for file in raw_files]

    df = pd.concat(df_list)
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    filt = df['Province_State'] != state
    df.drop(index=df[filt].index, inplace=True)
    df['Recovered'].replace(0.0, np.nan, inplace=True)
    df.sort_values(by='Last_Update', ascending=True, inplace=True)
    df['Last_Update'] = df['Last_Update'].apply(lambda date: date[0:10])
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], format='%Y-%m-%d')
    df = df.set_index("Last_Update")

    logging.info('Finished getting data from GitHub')

    return df


def getUSData():
    try:
        response = requests.get(
            'https://www.cdc.ov/coronavirus/2019-ncov/cases-updates/cases-in-us.html')
    except:
        logging.error('Cannot retrieve overall COVID-19 data for US')

    soup = BeautifulSoup(response.text, 'html.parser')

    us_data = soup.find_all(class_='count')

    total_cases = us_data[0].text
    total_death = us_data[1].text

    tweet = 'As of today, the US has had {} total cases of COVID-19 and {} deaths caused by the virus. Please stay safe! #COVID19'.format(
        total_cases, total_death)

    return tweet


def getCityData(city):
    df_confirmed = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

    df_deaths = df2 = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

    df_confirmed['Combined_Key'] = df_confirmed['Combined_Key'].apply(
        lambda key: key[:-4])
    df_confirmed = df_confirmed.set_index("Combined_Key")

    try:
        curr_date = date.today().strftime('%m/%d/%y').lstrip("0").replace(" 0", " ")
        confirmed_cases = "{:,}".format(df_confirmed.loc[city, curr_date])
    except:
        curr_date = date.today() - timedelta(days=1)
        curr_date = curr_date.strftime(
            '%m/%d/%y').lstrip("0").replace(" 0", " ")
        confirmed_cases = "{:,}".format(df_confirmed.loc[city, curr_date])

    df_deaths['Combined_Key'] = df_deaths['Combined_Key'].apply(
        lambda key: key[:-4])
    df_deaths = df_deaths.set_index("Combined_Key")

    try:
        curr_date = date.today().strftime('%m/%d/%y').lstrip("0").replace(" 0", " ")
        death_cases = "{:,}".format(df_deaths.loc[city, curr_date])
    except:
        curr_date = date.today() - timedelta(days=1)
        curr_date = curr_date.strftime(
            '%m/%d/%y').lstrip("0").replace(" 0", " ")
        death_cases = "{:,}".format(df_deaths.loc[city, curr_date])

    return confirmed_cases, death_cases


def create_graph(dataframe, state):
    confirmed_y = dataframe['Confirmed']
    plt.style.use('bmh')

    plt.plot(confirmed_y, color='#008fd5', label='Confirmed')

    if not(dataframe['Recovered'].isnull().all()):
        recovered_y = dataframe['Recovered']
        plt.plot(recovered_y, color='#e5ae38', label='Recovered')

    dead_y = dataframe['Deaths']
    plt.plot(dead_y, color='#c70d00', label='Deaths')

    plt.xlabel('Time Period', labelpad=10)
    plt.ylabel('Number of Cases', labelpad=10)

    if state == "District of Columbia":
        plt.title('COVID-19 Case Breakdown for the District of Columbia')
    else:
        plt.title('COVID-19 Case Breakdown for the State of {}'.format(state))

    plt.legend()
    plt.tight_layout()
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.tick_params(axis='y', which='major', labelsize=8)
    plt.subplots_adjust(bottom=0.12)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    plt.savefig("{}.png".format(state))
    plt.close()

    logging.info('Created graph for {}'.format(state))


def create_state_tweet(dataframe, state):
    confirmed = "{:,}".format(dataframe.iloc[-1]['Confirmed'])
    deaths = "{:,}".format(dataframe.iloc[-1]['Deaths'])

    try:
        recovered = "{:,}".format(int(dataframe.iloc[-1]['Recovered']))
        recovered_tweet = 'Additionally, {} people have recovered from the virus.'.format(
            recovered)
    except:
        recovered_tweet = 'I cannot report on the number of people that have recovered from the virus because I do not have the data.'

    if(state == 'District of Columbia'):
        tweet = 'Since April 13, 2020, the {} has had {} confirmed cases of COVID-19 and {} deaths caused by COVID-19. {}'.format(
            state, confirmed, deaths, recovered_tweet)
    else:
        tweet = 'Since April 13, 2020, the state of {} has had {} confirmed cases of COVID-19 and {} deaths caused by COVID-19. {}'.format(
            state, confirmed, deaths, recovered_tweet)

    logging.info('Created tweet for {}'.format(state))

    return tweet


def create_city_tweet(city):
    confirmed_cases, death_cases = getCityData(city)

    tweet = 'Reports say that {} has had {} confirmed cases of COVID-19 and {} deaths caused by the virus.'.format(
        city, confirmed_cases, death_cases)

    return tweet
