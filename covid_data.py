import pandas as pd
import numpy as np
import matplotlib
import requests
from utils import get_previous_dates
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
# url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

# querystring = {"date": "2020-07-18"}

# headers = {
#     'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
#     'x-rapidapi-key': "fe50ef6954msh39d259c6247a27bp1b8b89jsndf4254f2ec79"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)


# class State:
#     def __init__(self, state_name, positive_cases, positive_increase, death, death_increase):
#         self.state_name = state_name
#         self.positi


def get_dataframe(state):
    raw_files = []
    dates = get_previous_dates(30)

    for i in range(0, len(dates)):
        raw_files.append(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv".format(dates[i]))

    df_list = [pd.read_csv(file) for file in raw_files]

    df = pd.concat(df_list)
    pd.options.display.max_columns = None
    pd.options.display.max_rows = None

    filt = df['Province_State'] != state
    df.drop(index=df[filt].index, inplace=True)
    df.sort_values(by='Last_Update', ascending=True, inplace=True)
    df['Last_Update'] = df['Last_Update'].apply(lambda date: date[5:10])

    return df


def create_graph(dataframe, state):
    x_dates = dataframe['Last_Update']

    x_indexes = np.arange(len(x_dates))

    confirmed_y = dataframe['Confirmed']
    plt.style.use('bmh')

    plt.plot(x_indexes, confirmed_y,
             color='#008fd5', label='Confirmed')

    recovered_y = dataframe['Recovered']
    plt.plot(x_indexes, recovered_y,
             color='#e5ae38', label='Recovered')

    dead_y = dataframe['Deaths']
    plt.plot(x_indexes, dead_y,
             color='#c70d00', label='Deaths')

    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.title('COVID-19 Case Breakdown for the State of {}'.format(state))

    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45, ticks=x_indexes, labels=x_dates)
    plt.tick_params(axis='x', which='major', labelsize=8)
    plt.tick_params(axis='y', which='major', labelsize=8)
    plt.subplots_adjust(bottom=0.12)

    FOLDER_NAME = './state_graphs'

    plt.savefig(FOLDER_NAME + "/{}_overall.png".format(state))


create_graph(get_dataframe('Washington'), 'Washington')
plt.show()
